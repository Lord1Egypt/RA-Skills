"""Smoke tests for the redacta package public API.

Run:  python3 -m pytest        (or)  python3 tests/test_redacta.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from redacta import redact, reinstate, is_valid_nhs, __version__  # noqa: E402

passed = 0


def check(name, cond):
    global passed
    assert cond, "FAILED: " + name
    passed += 1


check("version present", isinstance(__version__, str) and __version__)

redacted, report, token_map = redact(
    "NHS Number: 943 476 5919, email jo@example.com")
check("nhs tokenised", "[NHS_NUMBER_1]" in redacted)
check("email tokenised", "[EMAIL_1]" in redacted)
check("report counts", report.get("NHS_NUMBER") == 1)
check("token map maps back", token_map["[NHS_NUMBER_1]"] == "943 476 5919")

check("round trip", reinstate(redacted, token_map)
      == "NHS Number: 943 476 5919, email jo@example.com")

# accepts the full object shape too
check("reinstate accepts full object",
      reinstate(redacted, {"token_map": token_map, "report": report})
      == "NHS Number: 943 476 5919, email jo@example.com")

check("validator exported", is_valid_nhs("9434765919") and not is_valid_nhs("9434765918"))

print("All %d checks passed." % passed)
