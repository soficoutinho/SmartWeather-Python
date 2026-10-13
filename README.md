# SmartWeather — Assistente Inteligente de Clima

Aplicação de automação em **Python** que consulta a API REST da Open-Meteo, apresenta condições meteorológicas atuais, gera recomendações com regras explícitas, registra consultas em SQLite e exporta histórico CSV.

## Tecnologias
- Python 3.12+
- Tkinter (interface gráfica; biblioteca padrão do Python)
- requests (requisições HTTP)
- SQLite e csv (biblioteca padrão)
- API Open-Meteo: https://open-meteo.com/

## Instalação (Windows PowerShell)
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

Se a ativação estiver bloqueada, execute diretamente `\.venv\Scripts\python.exe -m pip install -r requirements.txt` e `\.venv\Scripts\python.exe main.py`.

## Testes
```powershell
python -m unittest discover -s tests -v
```

## Fluxo da automação
1. Usuário informa a cidade.
2. Geocoding API encontra latitude e longitude (primeiro resultado).
3. Forecast API retorna as condições **atuais**.
4. Regras determinísticas produzem recomendações.
5. A consulta é armazenada no banco SQLite.
6. A interface mostra o resultado e permite exportar todo o histórico em CSV.

## Limitações
- Os avisos são informativos e **não** substituem alertas oficiais de tempo severo.
- Precipitação exibida é atual, não probabilidade futura de chuva.
- Em cidades homônimas, a API utiliza o primeiro resultado; pode ser necessário refinar o nome da cidade.
- É necessária conexão à internet para consultar a API.
