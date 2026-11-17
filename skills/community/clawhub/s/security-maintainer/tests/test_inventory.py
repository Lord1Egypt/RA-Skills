"""
Pruebas unitarias para los adaptadores de inventario de Windows, WSL y proyectos.
"""

import unittest
import json
from pathlib import Path

from security_maintainer.inventory.windows import WindowsInventoryAdapter
from security_maintainer.inventory.wsl import WSLInventoryAdapter
from security_maintainer.models import EnvironmentType, ManagerType

FIXTURES_DIR = Path(__file__).parent / "fixtures"


class TestInventoryAdapters(unittest.TestCase):

    def setUp(self):
        with open(FIXTURES_DIR / "winget_sample.json", "r", encoding="utf-8") as f:
            self.winget_data = json.load(f)
        with open(FIXTURES_DIR / "wsl_sample.json", "r", encoding="utf-8") as f:
            self.wsl_data = json.load(f)

    def test_windows_inventory_parsing(self):
        config = {
            "windows": {
                "excluded_packages": ["Microsoft.Edge"], # Exclusión explícita
                "allowed_packages": []
            }
        }
        adapter = WindowsInventoryAdapter(config, fixture_data=self.winget_data)
        items = adapter.collect()

        # Debe incluir Git y cURL, pero excluir Edge
        ids = [i.id for i in items]
        self.assertIn("Git.Git", ids)
        self.assertIn("cURL.cURL", ids)
        self.assertNotIn("Microsoft.Edge", ids)

        # Software en registro sin gestor debe marcarse como manual
        reg_item = next((i for i in items if i.id == "LegacyInternalTool_v1"), None)
        self.assertIsNotNone(reg_item)
        self.assertTrue(reg_item.requires_manual_intervention)
        self.assertFalse(reg_item.update_mechanism_available)

    def test_wsl_inventory_parsing_and_stopped_policy(self):
        config = {
            "wsl": {
                "auto_start_stopped_distros": False, # Política por defecto: no arrancar paradas
                "distributions": {
                    "OpenClawGateway": {
                        "security_updates_only": True,
                        "excluded_packages": []
                    }
                }
            }
        }
        adapter = WSLInventoryAdapter(config, fixture_data=self.wsl_data)
        items = adapter.collect()

        # OpenClawGateway está activa y tiene updates
        running_names = [i.name for i in items if i.target_name == "WSL:OpenClawGateway"]
        self.assertIn("openssl", running_names)

        # tmux no es de seguridad, por lo que con security_updates_only no debe incluirse
        self.assertNotIn("tmux", running_names)

        # ArchLinux está parada, debe registrarse como omitida según política sin arrancar
        arch_item = next((i for i in items if "ArchLinux" in i.target_name), None)
        self.assertIsNotNone(arch_item)
        self.assertTrue(arch_item.requires_manual_intervention)
        self.assertIn("detenida", arch_item.notes.lower())


if __name__ == "__main__":
    unittest.main()
