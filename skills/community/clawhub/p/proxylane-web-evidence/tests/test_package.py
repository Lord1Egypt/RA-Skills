import importlib.util
from pathlib import Path
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("package_candidate", ROOT / "scripts/package_candidate.py")
package = importlib.util.module_from_spec(spec)
spec.loader.exec_module(package)


class PackageTests(unittest.TestCase):
    def test_known_secret_scan_rejects_without_echoing_value(self):
        secret = "synthetic-test-secret-value"
        output = package.scan([("file.txt", ("private: " + secret).encode())], [secret])
        self.assertEqual(output, [{"file": "file.txt", "category": "known_secret_value"}])
        self.assertNotIn(secret, str(output))

    def test_url_credentials_only_synthetic_loopback_allowed(self):
        self.assertEqual(package.scan([("test", b"http://fixture-user:fixture-password@127.0.0.1:9")]), [])
        # Construct a deliberately unsafe SYNTHETIC URI at test runtime; the
        # shipped source contains no credential-bearing external connection.
        unsafe_fixture = ("http://" + "synthetic-unsafe-user:synthetic-unsafe-password@" + "example.invalid:9").encode()
        blocked = package.scan([("test", unsafe_fixture)])
        self.assertEqual(blocked[0]["category"], "non_fixture_url_credentials")

    def test_allowlist_excludes_runtime_output_cache_and_live_capture(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for name in ["SKILL.md", "scripts/collect.py", ".runtime/bin/python", "output/live.json", "scripts/__pycache__/x.pyc", "dist/older.zip", "unknown-live.json"]:
                path = root / name; path.parent.mkdir(parents=True, exist_ok=True); path.write_text("synthetic fixture")
            self.assertEqual([p.relative_to(root).as_posix() for p in package.files(root)], ["SKILL.md", "scripts/collect.py"])
            destination = root / "dist/candidate.zip"
            result = package.package(destination, root=root)
            self.assertEqual(result["status"], "candidate_packaged")
            self.assertFalse(result["published"])
            with zipfile.ZipFile(destination) as archive:
                self.assertEqual(set(archive.namelist()), {"proxylane-web-evidence/SKILL.md", "proxylane-web-evidence/scripts/collect.py", "proxylane-web-evidence/PACKAGE-MANIFEST.json"})


if __name__ == "__main__":
    unittest.main()
