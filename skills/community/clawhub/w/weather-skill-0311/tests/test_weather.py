import io
import json
import subprocess
import sys
import unittest
from pathlib import Path
from unittest import mock

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts' / 'weather.py'
sys.path.insert(0, str(SCRIPT.parent))

import weather  # noqa: E402


class WeatherSkillTests(unittest.TestCase):
    def test_offline_mode_returns_sample_payload(self) -> None:
        result = weather.get_weather('北京', offline=True)
        self.assertEqual(result['city'], '北京')
        self.assertEqual(result['weather'], '晴朗')
        self.assertEqual(result['temp_c'], '15')

    def test_online_mode_parses_http_response(self) -> None:
        payload = {
            'current_condition': [
                {
                    'temp_C': '22',
                    'temp_F': '71',
                    'humidity': '30',
                    'weatherDesc': [{'value': 'Partly cloudy'}],
                    'windspeedKmph': '8',
                    'observation_time': '06:30 PM',
                }
            ]
        }

        class FakeResponse(io.BytesIO):
            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc, tb):
                self.close()
                return False

        with mock.patch('weather.urllib.request.urlopen', return_value=FakeResponse(json.dumps(payload).encode('utf-8'))):
            result = weather.get_weather('Tokyo')

        self.assertEqual(result['city'], 'Tokyo')
        self.assertEqual(result['weather'], 'Partly cloudy')
        self.assertEqual(result['wind'], '8 km/h')

    def test_cli_offline_outputs_json(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(SCRIPT), '北京', '--offline'],
            check=True,
            capture_output=True,
            text=True,
        )
        payload = json.loads(completed.stdout)
        self.assertEqual(payload['city'], '北京')
        self.assertIn('temp_c', payload)


if __name__ == '__main__':
    unittest.main()
