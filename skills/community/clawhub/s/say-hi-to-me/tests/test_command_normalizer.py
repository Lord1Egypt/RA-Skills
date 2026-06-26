import sys
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from command_normalizer import normalize_input  # noqa: E402


class CommandNormalizerTests(unittest.TestCase):
    def test_role_confirm_command(self) -> None:
        result = normalize_input("/hi 角色 确认")
        self.assertEqual(result["intent"], "role_confirm_activation")

    def test_role_confirm_natural_language(self) -> None:
        result = normalize_input("确认启用")
        self.assertEqual(result["intent"], "role_confirm_activation")

    def test_role_save_natural_language(self) -> None:
        result = normalize_input("保存为咖啡店长")
        self.assertEqual(result["intent"], "role_save")
        self.assertEqual(result["args"]["name"], "咖啡店长")


if __name__ == "__main__":
    unittest.main()
