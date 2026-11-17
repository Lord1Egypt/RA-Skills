#!/usr/bin/env python3
"""
Anti-hallucination checker (anti_hallucination_check) — automated review tool for cloud outputs
Version: v2.0 | Date: 2026-08-05
Companion doc: anti-hallucination constraint prompt v1.1

Purpose: run an anti-hallucination self-check on the output of every LoomLoom cloud pipeline step,
     checking against the "catalog text submitted to the cloud" (fact boundary):
       1. whether every course code in the output appears in the input (prevent fabrication)
       2. whether fabricated codes are known cross-university pollution (COMP1000/MATH1001/PHYS1100 etc.)
       3. whether the decision step's why_rejected references courses outside the input (should be [] with no candidate pool)
       4. whether schedule session slots exactly match the TIMETABLE section (prevent "real course + fake times")
       5. whether the default_timetable declaration is missing

Usage:
    python3 anti_hallucination_check.py <output_json> <input_catalog.txt> [--context decision|schedule|catalog|recommend]
    python3 anti_hallucination_check.py --self-test   # run 8-scenario regression tests

Exit code: 0 = passed (no violations), 1 = hallucination detected
"""
import json, re, sys

KNOWN_CROSS_UNIVERSITY = {
    "COMP1000": "Macquarie University (MQ) - cross-university pollution",
    "MATH1001": "UQ College pre-university only (not UG)",
    "PHYS1100": "not a UQ course",
}

def extract_codes(text):
    """Extract course codes shaped like ABC1234 (4 digits) or COMP90038 (5 digits)"""
    return set(re.findall(r'\b([A-Z]{3,4}\d{4,5})\b', text.upper()))

def parse_timetable_block(input_catalog_text):
    """Parse the TIMETABLE section into a record list [(code, type, day, start, end)]"""
    block = re.search(r'TIMETABLE:\s*(.*?)(?:\n\n|\Z)', input_catalog_text, re.DOTALL)
    if not block:
        return []
    records = []
    for line in block.group(1).splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        m = re.match(
            r'([A-Z]{3,4}\d{4,5})\s*\|\s*(\w+)\s*\|\s*(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\s*\|\s*(\d{2}:\d{2})-(\d{2}:\d{2})',
            line, re.IGNORECASE)
        if m:
            records.append((m.group(1).upper(), m.group(2), m.group(3), m.group(4), m.group(5)))
    return records

def anti_hallucination_check(output_json, input_catalog_text, context="decision"):
    """
    Anti-hallucination self-check.
    output_json: cloud step output (dict)
    input_catalog_text: catalog text submitted to the cloud
    context: catalog / recommend / schedule / decision
    Returns {"passed": bool, "violations": [...], "warnings": [...]}
    """
    violations, warnings = [], []
    input_codes = extract_codes(input_catalog_text)
    output_codes = extract_codes(json.dumps(output_json, ensure_ascii=False))
    phantom = set(output_codes) - set(input_codes)

    # Check 1: every course code must come from the input
    for c in sorted(phantom):
        origin = KNOWN_CROSS_UNIVERSITY.get(c)
        note = f" [{origin}]" if origin else ""
        violations.append(f"fabricated course code {c}{note} — not present in the input catalog")

    # Check 2: fabricated code appears in a field value
    def walk(obj, path=""):
        if isinstance(obj, dict):
            for k, v in obj.items():
                walk(v, f"{path}.{k}" if path else k)
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                walk(v, f"{path}[{i}]")
        elif isinstance(obj, str):
            if re.match(r'^[A-Z]{3,4}\d{4,5}$', obj.strip()) and obj.strip().upper() in phantom:
                violations.append(f"{path}: fabricated course code appears in a field value")
    walk(output_json)

    # Check 3: decision step why_rejected
    if context == "decision":
        why = output_json.get("report", {}).get("selection_reasoning", {}).get("why_rejected")
        if why is None:
            warnings.append("why_rejected field missing (should explicitly output [] or a candidate list)")
        elif isinstance(why, list) and len(why) > 0:
            bad = [i.get("course_code", "").upper() for i in why
                   if isinstance(i, dict) and i.get("course_code", "").upper() not in input_codes]
            if bad:
                violations.append(f"why_rejected references courses outside the input: {bad} (should be [] with no candidate pool)")
        elif isinstance(why, list) and len(why) == 0:
            warnings.append("why_rejected=[] correct (no candidate pool in input)")

    # Check 4: schedule session slots must exactly match the TIMETABLE section
    if context == "schedule":
        tt_records = parse_timetable_block(input_catalog_text)
        tt_flat = {(r[0], r[2], r[3], r[4]) for r in tt_records}
        has_default = output_json.get("default_timetable") is True
        for s in output_json.get("schedule", []):
            code = str(s.get("course_code", "")).upper()
            day = s.get("day", "")
            st, et = s.get("start_time", ""), s.get("end_time", "")
            if has_default:
                continue
            key = (code, day, st, et)
            if key not in tt_flat:
                relaxed = any(r[0] == code and r[2] == day and r[3] == st for r in tt_records)
                if not relaxed:
                    violations.append(
                        f"schedule: {code} {day} {st}-{et} not in the input TIMETABLE section and default_timetable=true not declared")
                else:
                    warnings.append(
                        f"schedule: {code} {day} {st}-{et} start matches but end time differs from the TIMETABLE section (possibly rounded; suggest verifying)")
        if has_default:
            warnings.append("default_timetable=true declared (default timetable, needs verification)")

    return {"passed": len(violations) == 0, "violations": violations, "warnings": warnings}


def self_test():
    """8-scenario regression tests"""
    input_catalog = """UQ Bachelor of Biomedical Science (2546). Each course = 2 units. Year 1 Semester 1 (starts 2027-02-22): BIOM1001 Fund Bio Sci I (compulsory); CHEM1100 Chemistry 1 (compulsory); SCIE1000 Theory & Practice (compulsory); BIOL1020 Genes Cells & Evolution (compulsory). 2027 S1: starts 2027-02-22, 13 teaching weeks, ends 2027-05-28.

TIMETABLE:
BIOM1001 | Lecture | Monday | 09:00-10:00 | weeks 1-13
BIOM1001 | Tutorial | Tuesday | 14:00-15:00 | weeks 1-13
CHEM1100 | Lecture | Monday | 14:00-15:00 | weeks 1-13
CHEM1100 | Lecture | Tuesday | 09:00-10:00 | weeks 1-13
SCIE1000 | Lecture | Monday | 11:00-12:00 | weeks 1-13
SCIE1000 | Workshop | Tuesday | 10:00-12:00 | weeks 1-13
BIOL1020 | Lecture | Monday | 10:00-11:00 | weeks 1-13
BIOL1020 | Tutorial | Wednesday | 10:00-11:00 | weeks 1-13
BIOL1020 | Practical | Friday | 09:00-12:00 | weeks 1-12
"""
    cases = [
        ("T1 decision report - real hallucination", "decision",
         {"report": {"selection_reasoning": {"why_rejected": [
             {"course_code": "MATH1001", "reasoning": "math"},
             {"course_code": "PHYS1100", "reasoning": "physics"},
             {"course_code": "COMP1000", "reasoning": "computer science"}]}}}, "block"),
        ("T2 decision report - follows constraints", "decision",
         {"report": {"selection_reasoning": {"why_rejected": []}}}, "pass"),
        ("T3 candidate pool compliant", "decision",
         {"report": {"selection_reasoning": {"why_rejected": [
             {"course_code": "SCIE1000", "reasoning": "low match"}]}}}, "pass"),
        ("T4 schedule - fabricated slot (Sat 7am)", "schedule",
         {"schedule": [{"course_code": "BIOL1020", "session_type": "Practical",
                        "day": "Saturday", "start_time": "07:00", "end_time": "10:00"}]}, "block"),
        ("T5 schedule - default declared", "schedule",
         {"default_timetable": True, "schedule": [{"course_code": "BIOM1001",
          "session_type": "Lecture", "day": "Monday", "start_time": "09:00", "end_time": "10:00"}]}, "pass"),
        ("T6 schedule - exact match to real slot", "schedule",
         {"schedule": [{"course_code": "BIOL1020", "session_type": "Practical",
                        "day": "Friday", "start_time": "09:00", "end_time": "12:00"}]}, "pass"),
        ("T7 schedule - start matches, end differs", "schedule",
         {"schedule": [{"course_code": "BIOL1020", "session_type": "Practical",
                        "day": "Friday", "start_time": "09:00", "end_time": "11:00"}]}, "warn-pass"),
        ("T8 catalog - fabricated course", "catalog",
         {"courses": [{"course_code": "BIOM1001"}, {"course_code": "MATH1001"}]}, "block"),
    ]
    print("Anti-hallucination checker v2 regression tests (8 scenarios)")
    print("=" * 72)
    all_ok = True
    for name, ctx, out, expect in cases:
        r = anti_hallucination_check(out, input_catalog, ctx)
        behaves = "pass" if r["passed"] else "block"
        match = (behaves == expect) or (expect == "warn-pass" and r["passed"] and len(r["warnings"]) > 0)
        all_ok = all_ok and match
        print(f"\n─── {name} | expected: {expect} | actual: {behaves} {'OK' if match else 'MISMATCH'}")
        for v in r["violations"]:
            print(f"   [blocked] {v}")
        for w in r["warnings"]:
            print(f"   [note] {w}")
    print(f"\n{'All passed OK' if all_ok else 'MISMATCH found'}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        sys.exit(self_test())
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(2)
    out = json.load(open(sys.argv[1], encoding="utf-8"))
    catalog = open(sys.argv[2], encoding="utf-8").read()
    ctx = "decision"
    if "--context" in sys.argv:
        ctx = sys.argv[sys.argv.index("--context") + 1]
    r = anti_hallucination_check(out, catalog, ctx)
    print(json.dumps(r, ensure_ascii=False, indent=2))
    sys.exit(0 if r["passed"] else 1)
