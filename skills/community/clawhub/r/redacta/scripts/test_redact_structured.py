#!/usr/bin/env python3
"""Self-contained tests for the structured redaction layer.

Run:  python3 scripts/test_redact_structured.py
No dependencies. Exits non-zero if any assertion fails.
"""

from redact_structured import redact_structured, is_valid_nhs, is_valid_ni

passed = 0


def check(name, cond):
    global passed
    if cond:
        passed += 1
    else:
        raise AssertionError("FAILED: " + name)


# --- validators ------------------------------------------------------------

check("NHS demo number validates", is_valid_nhs("9434765919"))
check("NHS bad checksum rejected", not is_valid_nhs("9434765910"))
check("NHS all-same rejected", not is_valid_nhs("0000000000"))
check("NI valid prefix", is_valid_ni("AB"))
check("NI invalid prefix BG", not is_valid_ni("BG"))
check("NI bad first letter Q", not is_valid_ni("QA"))


# --- the landing-page demo letter -----------------------------------------

demo = ("Dear Mrs Patricia Hartley, DOB: 14/03/1952 (age 73), "
        "NHS Number: 943 476 5919. Following your recent review, your "
        "ferritin remains low and we recommend continuing oral iron.")
red, report, tmap = redact_structured(demo)

check("DOB tokenised", "[DATE_OF_BIRTH_1]" in red)
check("DOB original captured", tmap.get("[DATE_OF_BIRTH_1]") == "14/03/1952")
check("NHS tokenised", "[NHS_NUMBER_1]" in red)
check("NHS original captured", tmap.get("[NHS_NUMBER_1]") == "943 476 5919")
check("name left for reasoning layer", "Patricia Hartley" in red)
check("age left for reasoning layer", "age 73" in red)
check("clinical content preserved", "ferritin remains low" in red)
check("report counts NHS", report.get("NHS_NUMBER") == 1)
check("report counts DOB", report.get("DATE_OF_BIRTH") == 1)


# --- clinical date must NOT be redacted ------------------------------------

appt = "Your next appointment is on 15 March 2026 at the clinic."
red2, _, _ = redact_structured(appt)
check("clinical date survives", "15 March 2026" in red2)
check("no DOB token on clinical date", "DATE_OF_BIRTH" not in red2)


# --- token consistency: same value -> same token ---------------------------

twice = "NHS 943 476 5919 was checked. Confirm NHS 943 476 5919 on file."
red3, rep3, _ = redact_structured(twice)
check("repeated NHS number collapses to one token", rep3.get("NHS_NUMBER") == 1)
check("both occurrences replaced", "943 476 5919" not in red3)


# --- other structured identifiers ------------------------------------------

mix = ("Contact: jane.doe@example.com or 07700 900123. "
       "Address postcode SW1A 1AA. NI number: AB 12 34 56 C. "
       "Hospital Number: A1234567.")
red4, rep4, _ = redact_structured(mix)
check("email redacted", "[EMAIL_1]" in red4)
check("UK phone redacted", "[PHONE_1]" in red4)
check("postcode redacted", "[POSTCODE_1]" in red4)
check("NI number redacted", "[NI_NUMBER_1]" in red4)
check("MRN redacted", "[MRN_1]" in red4)
check("raw email gone", "jane.doe@example.com" not in red4)


# --- distinct values get distinct numbers ----------------------------------

two_pats = "Patient A NHS 943 476 5919; Patient B NHS 401 023 2137."
red5, rep5, _ = redact_structured(two_pats)
check("two NHS numbers -> two tokens", rep5.get("NHS_NUMBER") == 2)
check("NHS_NUMBER_2 present", "[NHS_NUMBER_2]" in red5)


print("All %d checks passed." % passed)
