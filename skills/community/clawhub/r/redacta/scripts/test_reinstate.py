#!/usr/bin/env python3
"""Self-contained tests for the re-identification layer.

Run:  python3 scripts/test_reinstate.py
No dependencies. Exits non-zero if any assertion fails.
"""

from redact_structured import redact_structured
from reinstate import load_token_map, reinstate

passed = 0


def check(name, cond):
    global passed
    if cond:
        passed += 1
    else:
        raise AssertionError("FAILED: " + name)


# --- basic restore ---------------------------------------------------------

tmap = {"[NHS_NUMBER_1]": "943 476 5919", "[PATIENT_NAME_1]": "Patricia Hartley"}
text, changed = reinstate(
    "Dear [PATIENT_NAME_1], your NHS number is [NHS_NUMBER_1].", tmap)
check("name restored", "Patricia Hartley" in text)
check("nhs restored", "943 476 5919" in text)
check("changed flag set", changed is True)
check("no tokens left", "[" not in text)


# --- no tokens present -----------------------------------------------------

_, changed2 = reinstate("nothing to do here", {"[EMAIL_1]": "x@y.com"})
check("no change when no tokens", changed2 is False)


# --- [NAME_1] vs [NAME_10] -------------------------------------------------

tmap2 = {"[PATIENT_NAME_1]": "Anna", "[PATIENT_NAME_10]": "Zoe"}
text2, _ = reinstate("[PATIENT_NAME_10] and [PATIENT_NAME_1]", tmap2)
check("no token-prefix collision", text2 == "Zoe and Anna")


# --- round trip with the real redaction layer ------------------------------

original = ("NHS Number: 943 476 5919, NI: AB 12 34 56 C, "
            "email jo@example.com, tel 0113 278 4532")
red, _report, tmap3 = redact_structured(original)
restored, _ = reinstate(red, tmap3)
check("round trip restores original", restored == original)


# --- load_token_map accepts both shapes ------------------------------------

bare = '{"[NHS_NUMBER_1]": "943 476 5919"}'
full = '{"redacted_text": "x", "report": {}, "token_map": {"[NHS_NUMBER_1]": "943 476 5919"}}'
check("loads bare map", load_token_map(bare) == {"[NHS_NUMBER_1]": "943 476 5919"})
check("loads full object", load_token_map(full) == {"[NHS_NUMBER_1]": "943 476 5919"})

for bad in ('{}', '[]', '{"foo": "bar"}', '{"[NHS_NUMBER_1]": 123}'):
    try:
        load_token_map(bad)
        raise AssertionError("FAILED: bad map accepted: " + bad)
    except ValueError:
        passed += 1


print("All %d checks passed." % passed)
