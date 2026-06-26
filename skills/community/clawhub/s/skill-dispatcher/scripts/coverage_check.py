"""
Coverage gap detector for skill-dispatcher.
Compares available skills against Covered Skills Registry.
Usage: python coverage_check.py skill1 "skill name with spaces" skill3 ...
Output: Covered/Uncovered report.
Exit code: 0 if all covered, 1 if gaps found.
"""
import sys
import re
from pathlib import Path


def get_covered_skills(dispatcher_path: str = None) -> set[str]:
    """Extract covered skill names from dispatcher SKILL.md registry."""
    if dispatcher_path is None:
        dispatcher_path = Path.home() / ".openclaw" / "skills" / "skill-dispatcher" / "SKILL.md"
    else:
        dispatcher_path = Path(dispatcher_path)

    text = dispatcher_path.read_text(encoding="utf-8")

    # Find the Covered Skills Registry section
    marker = "## 📋 Covered Skills Registry"
    idx = text.find(marker)
    if idx == -1:
        print(f"ERROR: 'Covered Skills Registry' not found in {dispatcher_path}", file=sys.stderr)
        sys.exit(2)

    # Extract all backtick-wrapped skill names from the registry section
    registry_section = text[idx:]
    names = re.findall(r'`([^`]+)`', registry_section)
    return set(names)


def main():
    if len(sys.argv) < 2:
        print("Usage: python coverage_check.py <skill1> [skill2] ...", file=sys.stderr)
        print("Pass all skill names from available_skills as arguments.", file=sys.stderr)
        sys.exit(2)

    current_skills = set(sys.argv[1:])
    covered = get_covered_skills()

    in_both = current_skills & covered
    uncovered = current_skills - covered
    missing_from_registry = covered - current_skills  # in registry but not installed

    print(f"Covered: {len(in_both)}/{len(current_skills)}")
    print(f"Registry total: {len(covered)}")

    if uncovered:
        print(f"\n⚠️  UNCOVERED ({len(uncovered)}):")
        for s in sorted(uncovered):
            print(f"  - {s}")
        print("\n→ Run New Skill Onboarding Protocol for each.")

    if missing_from_registry:
        print(f"\n📌 In registry but not installed ({len(missing_from_registry)}):")
        for s in sorted(missing_from_registry):
            print(f"  - {s}")

    if not uncovered:
        print("\n✅ All skills covered.")

    sys.exit(1 if uncovered else 0)


if __name__ == "__main__":
    main()
