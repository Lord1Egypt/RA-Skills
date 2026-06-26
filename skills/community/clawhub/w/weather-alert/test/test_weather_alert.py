"""Tests for weather-alert skill."""

import json
import os
import sys
import unittest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import weather_alert as wa


class TestWeatherIcons(unittest.TestCase):
    def test_known_code(self):
        self.assertEqual(wa.get_weather_icon(0), "☀️")
        self.assertEqual(wa.get_weather_icon(63), "🌧")
        self.assertEqual(wa.get_weather_icon(95), "⛈")

    def test_unknown_code(self):
        self.assertEqual(wa.get_weather_icon(999), "🌡")


class TestWeatherDescriptions(unittest.TestCase):
    def test_clear(self):
        self.assertEqual(wa.get_weather_description(0), "Clear sky")

    def test_rain(self):
        self.assertEqual(wa.get_weather_description(63), "Rain moderate")

    def test_unknown(self):
        self.assertEqual(wa.get_weather_description(999), "Unknown")


class TestFormatCurrent(unittest.TestCase):
    def test_valid_data(self):
        current = {
            "temperature_2m": 12.5,
            "apparent_temperature": 10.2,
            "relative_humidity_2m": 65,
            "precipitation": 0.0,
            "wind_speed_10m": 15,
            "wind_direction_10m": 270,
            "surface_pressure": 101300,
            "uv_index": 3.2,
            "weather_code": 2,
        }
        result = wa.format_current(current, None, "TestCity")
        self.assertIn("TestCity Weather", result)
        self.assertIn("12.5°C", result)
        self.assertIn("10.2°C", result)
        self.assertIn("65%", result)
        self.assertIn("15 km/h", result)

    def test_empty_data(self):
        result = wa.format_current(None, None, "Empty")
        self.assertIn("Could not fetch", result)


class TestFormatForecast(unittest.TestCase):
    def test_valid_daily(self):
        daily = {
            "time": ["2026-04-17", "2026-04-18", "2026-04-19"],
            "weather_code": [0, 61, 95],
            "temperature_2m_min": [5, 3, 8],
            "temperature_2m_max": [18, 10, 15],
            "precipitation_probability_max": [0, 80, 90],
            "wind_speed_10m_max": [15, 30, 45],
            "uv_index_max": [5, 2, 6],
            "precipitation_sum": [0.0, 5.2, 12.0],
            "snowfall_sum": [0, 0, 0],
        }
        result = wa.format_forecast(daily, 3)
        self.assertIn("7-Day Forecast", result)
        self.assertIn("18°", result)
        self.assertIn("🌧", result)

    def test_empty_data(self):
        result = wa.format_forecast(None)
        self.assertIn("No forecast data", result)


class TestCheckAlerts(unittest.TestCase):
    def setUp(self):
        self.config = {
            "alerts": {
                "rain_threshold": 60,
                "temp_min": 5,
                "temp_max": 30,
                "wind_max": 40,
                "snow_depth": 5,
                "uv_max": 7,
                "frost_threshold": 0,
            }
        }

    def test_no_alerts(self):
        current = {
            "temperature_2m": 15,
            "precipitation": 0,
            "wind_speed_10m": 10,
            "wind_gusts_10m": 15,
            "uv_index": 3,
        }
        daily = {
            "temperature_2m_min": [5],
        }
        alerts = wa.check_alerts(current, daily, self.config)
        self.assertEqual(alerts, [])

    def test_temp_below_threshold(self):
        current = {"temperature_2m": 2}
        daily = {"temperature_2m_min": [2]}
        alerts = wa.check_alerts(current, daily, self.config)
        self.assertTrue(any("Temperature" in a for a in alerts))

    def test_rain_alert(self):
        current = {"temperature_2m": 15}
        daily = {
            "temperature_2m_min": [5],
            "precipitation_probability_max": [80],
        }
        alerts = wa.check_alerts(current, daily, self.config)
        self.assertTrue(any("Rain" in a for a in alerts))

    def test_uv_alert(self):
        current = {"temperature_2m": 25, "uv_index": 9}
        daily = {"temperature_2m_min": [10]}
        alerts = wa.check_alerts(current, daily, self.config)
        self.assertTrue(any("UV" in a for a in alerts))

    def test_frost_alert(self):
        current = {"temperature_2m": 5}
        daily = {"temperature_2m_min": [-2]}
        alerts = wa.check_alerts(current, daily, self.config)
        self.assertTrue(any("Frost" in a for a in alerts))

    def test_wind_alert(self):
        current = {
            "temperature_2m": 15,
            "wind_speed_10m": 50,
            "wind_gusts_10m": 65,
            "uv_index": 3,
        }
        daily = {"temperature_2m_min": [5]}
        alerts = wa.check_alerts(current, daily, self.config)
        self.assertTrue(any("Wind" in a for a in alerts))


class TestFormatEvent(unittest.TestCase):
    def test_good_conditions(self):
        daily = {
            "time": ["2026-04-17"],
            "temperature_2m_min": [8],
            "temperature_2m_max": [18],
            "precipitation_probability_max": [10],
            "precipitation_sum": [0],
            "wind_speed_10m_max": [10],
            "uv_index_max": [4],
            "snowfall_sum": [0],
        }
        result = wa.format_event_suitability(daily, "running", "TestCity")
        self.assertIn("Good:", result)

    def test_bad_conditions(self):
        daily = {
            "time": ["2026-04-17"],
            "temperature_2m_min": [-5],
            "temperature_2m_max": [2],
            "precipitation_probability_max": [90],
            "precipitation_sum": [10],
            "wind_speed_10m_max": [45],
            "uv_index_max": [1],
            "snowfall_sum": [15],
        }
        result = wa.format_event_suitability(daily, "picnic", "TestCity")
        self.assertIn("Bad:", result)


class TestConfigLoading(unittest.TestCase):
    def test_default_config(self):
        config = wa.load_config()
        self.assertIn("default_location", config)
        self.assertIn("alerts", config)
        self.assertEqual(config["default_location"]["name"], "Prague")


if __name__ == "__main__":
    unittest.main()
