#!/usr/bin/env python3
"""
normalize_testfile.py — Normalize test file name to TEST.md.
- TEST.md present       → use as-is
- Test.md present       → rename to TEST.md (LEGACY: modifies target skill dir)
- TESTS.md present      → rename to TEST.md (LEGACY: modifies target skill dir)
- None of the above     → create TEST.md template, exit code 2 (caller should warn user)

⚠️ Renaming is a side-effect on the target skill directory.
   Use --dry-run to preview without changes.
"""
import argparse
import os
import sys


TEMPLATE = """\
# TEST.md

## Meta

```yaml
skill_name: {skill_name}
version: "1.0"
maintainer: ""
```

## Test Cases

### Case 1: Basic functionality

```yaml
id: case_001
name: Basic functionality
type: normal
trigger: "describe the user trigger phrase here"
script_cmd: ""
expected_output: ""
expected_output_mode: contains
expected_agent_response: "describe the expected AI response semantics"
```

### Case 2: Error handling

```yaml
id: case_002
name: Error handling
type: error
trigger: "describe the error trigger phrase here"
script_cmd: ""
expected_output: ""
expected_output_mode: contains
expected_agent_response: "describe the expected error response semantics"
```
"""


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--skill-dir", required=True)
    p.add_argument("--dry-run", action="store_true",
                   help="Preview rename/create actions without modifying the target skill dir")
    return p.parse_args()


def main():
    args = parse_args()
    skill_dir = os.path.realpath(args.skill_dir)
    skill_name = os.path.basename(skill_dir)

    test_md = os.path.join(skill_dir, "TEST.md")
    test_md_compat = os.path.join(skill_dir, "Test.md")
    tests_md = os.path.join(skill_dir, "TESTS.md")

    if os.path.exists(test_md):
        print("  → TEST.md already present, using as-is")
    elif os.path.exists(test_md_compat):
        if args.dry_run:
            print(f"  [dry-run] Would rename Test.md → TEST.md in {skill_dir}")
        else:
            print(f"  ⚠️  Renaming Test.md → TEST.md (MODIFIES target skill dir: {skill_dir})")
            os.rename(test_md_compat, test_md)
            print("  → Rename complete: Test.md → TEST.md")
    elif os.path.exists(tests_md):
        if args.dry_run:
            print(f"  [dry-run] Would rename TESTS.md → TEST.md in {skill_dir}")
        else:
            print(f"  ⚠️  Renaming TESTS.md → TEST.md (MODIFIES target skill dir: {skill_dir})")
            os.rename(tests_md, test_md)
            print("  → Rename complete: TESTS.md → TEST.md")
    else:
        if args.dry_run:
            print(f"  [dry-run] Would create TEST.md template at: {test_md}")
            sys.exit(2)
        with open(test_md, "w", encoding="utf-8") as f:
            f.write(TEMPLATE.format(skill_name=skill_name))
        print(f"  → No test file found, created TEST.md template at: {test_md}")
        print(f"  ⚠️  Please edit {test_md} with real test cases, then re-run")
        sys.exit(2)


if __name__ == "__main__":
    main()
