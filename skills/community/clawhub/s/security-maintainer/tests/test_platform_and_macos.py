"""
Pruebas unitarias para el detector inteligente de plataforma y el adaptador de macOS.
"""

import unittest
from pathlib import Path

from security_maintainer.inventory.platform_detector import (
    PlatformDetector,
    HostOSType,
    RuntimeMountType,
)
from security_maintainer.inventory.macos import MacOSInventoryAdapter


class TestPlatformAndMacOS(unittest.TestCase):

    def test_platform_detector_returns_valid_structure(self):
        info = PlatformDetector.detect()
        self.assertIn("mount_type", info)
        self.assertIn("host_os", info)
        self.assertIn("description", info)
        self.assertIn(info["host_os"], ["windows", "macos", "linux"])

    def test_macos_adapter_parsing_with_fixture(self):
        fixture_data = {
            "brew_outdated": {
                "formulae": [
                    {
                        "name": "openssl@3",
                        "installed_versions": ["3.0.12"],
                        "current_version": "3.0.13"
                    }
                ],
                "casks": [
                    {
                        "name": "visual-studio-code",
                        "installed_versions": ["1.85.0"],
                        "current_version": "1.86.0"
                    }
                ]
            }
        }
        adapter = MacOSInventoryAdapter(config={}, fixture_data=fixture_data)
        self.assertTrue(adapter.is_available())
        items = adapter.collect()

        self.assertEqual(len(items), 3)
        names = [i.name for i in items]
        self.assertIn("macOS Operating System", names)
        self.assertIn("openssl@3", names)
        self.assertIn("visual-studio-code", names)
        self.assertEqual(items[0].target_name, "macOS Host")


if __name__ == "__main__":
    unittest.main()
