"""Integração meteorológica e regras de recomendação."""
import requests

GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"


def get_weather(city: str) -> dict:
    """Busca coordenadas e clima atual; lança ValueError em entradas inválidas."""
    city = city.strip()
    if len(city) < 2:
        raise ValueError("Digite uma cidade com pelo menos 2 caracteres.")
    try:
        geo_response = requests.get(GEO_URL, params={"name": city, "count": 1, "language": "pt", "format": "json"}, timeout=12)
        geo_response.raise_for_status()
        locations = geo_response.json().get("results") or []
        if not locations:
            raise ValueError("Cidade não encontrada. Tente incluir o estado ou país.")
        location = locations[0]
        response = requests.get(WEATHER_URL, params={
            "latitude": location["latitude"], "longitude": location["longitude"],
            "current": "temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,wind_speed_10m,weather_code",
            "timezone": "auto",
        }, timeout=12)
        response.raise_for_status()
        current = response.json()["current"]
        return {
            "cidade": location["name"], "pais": location.get("country", ""),
            "horario": current["time"], "temperatura": current["temperature_2m"],
            "sensacao": current["apparent_temperature"], "umidade": current["relative_humidity_2m"],
            "precipitacao": current["precipitation"], "vento": current["wind_speed_10m"],
            "codigo": current["weather_code"],
        }
    except requests.RequestException as exc:
        raise RuntimeError("Não foi possível consultar a API. Verifique sua conexão.") from exc
    except (KeyError, TypeError, ValueError) as exc:
        if isinstance(exc, ValueError):
            raise
        raise RuntimeError("A API retornou dados incompletos.") from exc


def recommend(data: dict) -> list[str]:
    """Gera orientações baseadas nas condições atuais (não em previsão futura)."""
    tips = []
    if data["precipitacao"] > 0 or data["codigo"] in {51, 53, 55, 61, 63, 65, 80, 81, 82, 95, 96, 99}:
        tips.append("Há indicação de precipitação: considere levar guarda-chuva.")
    if data["sensacao"] >= 32:
        tips.append("Sensação de calor elevada: hidrate-se e evite exposição prolongada.")
    if data["sensacao"] <= 12:
        tips.append("Sensação de frio: considere levar um agasalho.")
    if data["vento"] >= 40:
        tips.append("Ventos fortes: tenha atenção em atividades ao ar livre.")
    if not tips:
        tips.append("Condições atuais sem alertas definidos pelas regras do aplicativo.")
    return tips
