#!/usr/bin/env python3
"""
Unit tests for skill-security-scanner
"""

import unittest
import tempfile
import shutil
from pathlib import Path

# Add skill source to path
import sys
SKILL_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(SKILL_DIR / "source"))

from scanner import SecurityScanner

class TestSecurityScanner(unittest.TestCase):
    def setUp(self):
        """Create a temporary skill directory for each test"""
        self.test_dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        """Clean up test directory"""
        shutil.rmtree(self.test_dir)

    def create_skill(self, name: str, files: dict) -> Path:
        """Helper: create a skill with given files"""
        skill_path = self.test_dir / name
        skill_path.mkdir()
        for relpath, content in files.items():
            file_path = skill_path / relpath
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content)
        return skill_path

    def test_detects_eval(self):
        """Test that eval() is flagged as high severity"""
        skill = self.create_skill("test_eval", {
            "source/main.py": "result = eval(user_input)"
        })
        scanner = SecurityScanner(str(skill))
        results = scanner.scan()
        self.assertEqual(results["findings"], 1)
        self.assertEqual(results["issues"][0]["type"], "dangerous_function")
        self.assertEqual(results["issues"][0]["severity"], "high")
        self.assertIn("eval", results["issues"][0]["message"])

    def test_detects_exec(self):
        """Test that exec() is flagged"""
        skill = self.create_skill("test_exec", {
            "source/main.py": "exec(code_string)"
        })
        scanner = SecurityScanner(str(skill))
        results = scanner.scan()
        self.assertGreaterEqual(results["findings"], 1)

    def test_detects_pickle_loads(self):
        """Test pickle.loads detection"""
        skill = self.create_skill("test_pickle", {
            "source/main.py": "pickle.loads(untrusted_data)"
        })
        scanner = SecurityScanner(str(skill))
        results = scanner.scan()
        self.assertGreaterEqual(results["findings"], 1)

    def test_detects_subprocess_shell_true(self):
        """Test subprocess.Popen with shell=True"""
        skill = self.create_skill("test_subprocess", {
            "source/main.py": "subprocess.Popen('ls', shell=True)"
        })
        scanner = SecurityScanner(str(skill))
        results = scanner.scan()
        self.assertGreaterEqual(results["findings"], 1)

    def test_detects_os_system(self):
        """Test os.system detection"""
        skill = self.create_skill("test_os_system", {
            "source/main.py": "os.system('rm -rf /')"
        })
        scanner = SecurityScanner(str(skill))
        results = scanner.scan()
        self.assertGreaterEqual(results["findings"], 1)

    def test_detects_hardcoded_secrets(self):
        """Test hardcoded API keys and tokens"""
        # Use longer strings to match patterns (20+ chars)
        skill = self.create_skill("test_secrets", {
            "source/config.py": 'API_KEY = "sk-1234567890abcdef1234567890abcdef"\nGITHUB_TOKEN = "ghp_1234567890abcdefghijklmnopqrstuvwxyz"'
        })
        scanner = SecurityScanner(str(skill))
        results = scanner.scan()
        self.assertGreaterEqual(results["findings"], 2)

    def test_detects_http_urls(self):
        """Test insecure HTTP URLs"""
        skill = self.create_skill("test_http", {
            "source/net.py": 'requests.get("http://example.com/api")'
        })
        scanner = SecurityScanner(str(skill))
        results = scanner.scan()
        self.assertGreaterEqual(results["findings"], 1)
        self.assertEqual(results["issues"][0]["type"], "insecure_communication")

    def test_detects_path_traversal(self):
        """Test path traversal patterns"""
        skill = self.create_skill("test_traversal", {
            "source/io.py": 'open("../../../etc/passwd")'
        })
        scanner = SecurityScanner(str(skill))
        results = scanner.scan()
        self.assertGreaterEqual(results["findings"], 1)
        self.assertEqual(results["issues"][0]["type"], "path_traversal")

    def test_clean_skill_passes(self):
        """Test that a clean skill produces no findings"""
        skill = self.create_skill("test_clean", {
            "source/main.py": 'print("Hello, world!")\nreturn 42'
        })
        scanner = SecurityScanner(str(skill))
        results = scanner.scan()
        self.assertEqual(results["findings"], 0)
        self.assertEqual(results["risk_level"], "low")

    def test_severity_threshold(self):
        """Test that severity threshold filtering works"""
        skill = self.create_skill("test_threshold", {
            "source/main.py": "result = eval(user_input)"  # high severity
        })
        scanner = SecurityScanner(str(skill), severity_threshold="critical")
        results = scanner.scan()
        # High severity should be filtered if threshold is critical
        self.assertEqual(results["findings"], 0)

    def test_risk_score_calculation(self):
        """Test risk score is calculated correctly"""
        skill = self.create_skill("test_score", {
            "source/main.py": "eval(input()); API_KEY='sk-123'"
        })
        scanner = SecurityScanner(str(skill))
        results = scanner.scan()
        self.assertGreater(results["risk_score"], 0)
        self.assertLessEqual(results["risk_score"], 100)

    def test_multi_file_scan(self):
        """Scanning multiple Python files"""
        skill = self.create_skill("test_multi", {
            "source/module1.py": "eval('test')",
            "source/module2.py": "exec('test')",
            "source/config.py": "API_KEY='sk-1234567890abcdef1234567890abcdef'"
        })
        scanner = SecurityScanner(str(skill))
        results = scanner.scan()
        self.assertGreaterEqual(results["findings"], 3)
        self.assertEqual(results["total_files"], 3)

if __name__ == "__main__":
    unittest.main(verbosity=2)