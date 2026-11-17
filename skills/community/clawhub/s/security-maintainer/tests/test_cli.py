"""
Pruebas integradas de comandos CLI con fixtures simulados.
"""

import unittest
import json
import tempfile
from pathlib import Path

from security_maintainer.cli import cmd_audit, cmd_plan, cmd_apply
from security_maintainer.models import ActionStatus

FIXTURES_DIR = Path(__file__).parent / "fixtures"


class DummyArgs:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class TestCLI(unittest.TestCase):

    def setUp(self):
        with open(FIXTURES_DIR / "winget_sample.json", "r", encoding="utf-8") as f:
            self.winget_data = json.load(f)
        with open(FIXTURES_DIR / "wsl_sample.json", "r", encoding="utf-8") as f:
            self.wsl_data = json.load(f)
        with open(FIXTURES_DIR / "osv_sample.json", "r", encoding="utf-8") as f:
            self.osv_data = json.load(f)
        with open(FIXTURES_DIR / "cisa_kev_sample.json", "r", encoding="utf-8") as f:
            self.kev_data = json.load(f)

        self.fixture_bundle = {
            "windows": self.winget_data,
            "wsl": self.wsl_data,
            "osv": self.osv_data["osv"],
            "cisa_kev": self.kev_data,
            "distro_trackers": {
                "backports": {
                    "ubuntu": {
                        "openssl": {
                            "CVE-2024-2511": "3.0.13-0ubuntu3.4"
                        }
                    }
                }
            }
        }

        self.config = {
            "mode": "ask",
            "windows": {
                "allow_major_upgrades": False,
                "allow_reboots": False,
                "excluded_packages": ["Microsoft.Edge"]
            },
            "wsl": {
                "auto_start_stopped_distros": False,
                "distributions": {
                    "OpenClawGateway": {
                        "security_updates_only": True
                    }
                }
            },
            "execution": {
                "max_actions_per_run": 10,
                "plan_validity_minutes": 30
            }
        }

    def test_cli_audit_flow(self):
        args = DummyArgs(environment="all", all=True)
        ret = cmd_audit(args, self.config, self.fixture_bundle)
        self.assertEqual(ret, 0)

    def test_cli_plan_flow(self):
        args = DummyArgs(environment="all")
        ret = cmd_plan(args, self.config, self.fixture_bundle)
        self.assertEqual(ret, 0)


if __name__ == "__main__":
    unittest.main()
