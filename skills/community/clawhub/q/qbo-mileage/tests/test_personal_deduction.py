import json
import unittest
from pathlib import Path

from qbo_mileage.config import load_config
from qbo_mileage.pipeline import GenerateOptions, generate


def make_temp_dir(name):
    path = Path.cwd() / ".test-tmp" / name
    path.mkdir(parents=True, exist_ok=True)
    return path


class PersonalDeductionTest(unittest.TestCase):
    def test_personal_legs_export_zero_deduction(self):
        root = make_temp_dir("personal-deduction")
        fixture_path = root / "events.json"
        fixture_path.write_text(
            json.dumps(
                [
                    {
                        "id": "a",
                        "start": "2026-05-04T09:00:00",
                        "end": "2026-05-04T10:00:00",
                        "title": "Dentist",
                        "location": "456 Oak Ave",
                        "type": "Personal",
                    }
                ]
            ),
            encoding="utf-8",
        )
        config_path = root / "config.json"
        config_path.write_text(
            json.dumps(
                {
                    "home_base": "Home",
                    "vehicle": "Tesla M3",
                    "timezone": "America/New_York",
                    "irs_rates": {"2026": 0.725},
                    "sources": [
                        {
                            "type": "fixture",
                            "enabled": True,
                            "name": "fixture",
                            "fixture": {"path": str(fixture_path)},
                        }
                    ],
                    "distance": {
                        "engine": "static",
                        "static_miles": 10,
                        "cache_path": str(root / "cache.json"),
                    },
                    "output": {"directory": str(root / "out")},
                }
            ),
            encoding="utf-8",
        )

        result = generate(load_config(config_path), GenerateOptions(month="2026-05", dry_run=True))

        self.assertEqual(2, len(result.legs))
        for leg in result.legs:
            self.assertEqual("PERSONAL", leg.trip_type)
            self.assertEqual(0.0, leg.deduction)
        self.assertEqual(20.0, result.total_miles)
        self.assertEqual(0.0, result.total_deduction)


if __name__ == "__main__":
    unittest.main()
