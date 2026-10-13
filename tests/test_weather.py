"""Testes unitários sem necessidade de internet."""
import unittest
from unittest.mock import Mock, patch
from weather import get_weather, recommend


class WeatherTests(unittest.TestCase):
    def test_empty_city(self):
        with self.assertRaises(ValueError):
            get_weather(" ")

    def test_unknown_city(self):
        response = Mock()
        response.json.return_value = {"results": []}
        with patch("weather.requests.get", return_value=response):
            with self.assertRaisesRegex(ValueError, "não encontrada"):
                get_weather("CidadeInventada")

    def test_rain_recommendation(self):
        data = {"precipitacao": 2, "codigo": 61, "sensacao": 22, "vento": 10}
        self.assertIn("guarda-chuva", " ".join(recommend(data)))

    def test_heat_and_wind(self):
        data = {"precipitacao": 0, "codigo": 0, "sensacao": 35, "vento": 50}
        self.assertEqual(len(recommend(data)), 2)

    def test_normal_conditions(self):
        data = {"precipitacao": 0, "codigo": 0, "sensacao": 22, "vento": 8}
        self.assertEqual(len(recommend(data)), 1)


if __name__ == "__main__":
    unittest.main()
