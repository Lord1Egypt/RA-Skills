"""
Ejecutor de pruebas unitarias para security-maintainer.
"""

import sys
import unittest
from pathlib import Path

# Añadir src al sys.path
root_dir = Path(__file__).resolve().parent
src_dir = root_dir / "src"
sys.path.insert(0, str(src_dir))

if __name__ == "__main__":
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=str(root_dir / "tests"), pattern="test_*.py")
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)
