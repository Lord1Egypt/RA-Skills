"""
OpenSSF Scorecard-inspired checks for skills.
Evaluates open source security health metrics.
"""

from pathlib import Path
from dataclasses import dataclass
from typing import List


@dataclass
class ScorecardResult:
    check_name: str
    score: int  # 0-10
    reason: str


def run_scorecard(skill_dir: str) -> List[ScorecardResult]:
    """Run OpenSSF-inspired scorecard checks on a skill."""
    skill_path = Path(skill_dir)
    results = []

    # Check 1: Has license?
    has_license = (skill_path / "LICENSE").exists() or (skill_path / "LICENSE.md").exists()
    results.append(ScorecardResult(
        check_name="License",
        score=10 if has_license else 0,
        reason="License file found" if has_license else "No license file",
    ))

    # Check 2: Has README?
    has_readme = (skill_path / "README.md").exists()
    results.append(ScorecardResult(
        check_name="Documentation",
        score=10 if has_readme else 0,
        reason="README found" if has_readme else "No README",
    ))

    # Check 3: Has tests?
    has_tests = (skill_path / "tests").exists() or (skill_path / "test").exists()
    results.append(ScorecardResult(
        check_name="Tests",
        score=10 if has_tests else 0,
        reason="Test directory found" if has_tests else "No tests",
    ))

    # Check 4: Has CI?
    has_ci = (skill_path / ".github").exists() or (skill_path / "ci-templates").exists()
    results.append(ScorecardResult(
        check_name="CI/CD",
        score=10 if has_ci else 0,
        reason="CI config found" if has_ci else "No CI config",
    ))

    # Check 5: Has SECURITY.md?
    has_security = (skill_path / "SECURITY.md").exists()
    results.append(ScorecardResult(
        check_name="Security Policy",
        score=10 if has_security else 3,
        reason="SECURITY.md found" if has_security else "No security policy",
    ))

    # Check 6: Has CHANGELOG?
    has_changelog = (skill_path / "CHANGELOG.md").exists()
    results.append(ScorecardResult(
        check_name="Changelog",
        score=10 if has_changelog else 5,
        reason="CHANGELOG found" if has_changelog else "No changelog",
    ))

    return results


def print_scorecard(results: List[ScorecardResult]):
    """Print scorecard results nicely."""
    print("=" * 50)
    print("  OpenSSF-Inspired Scorecard")
    print("=" * 50)
    total = 0
    for r in results:
        star = "★" * (r.score // 10)
        print(f"  {r.check_name:20s} {r.score:3d}/10  {star}")
        print(f"  {'':20s} {r.reason}")
        total += r.score
    avg = total // len(results)
    print("=" * 50)
    print(f"  Overall: {avg}/10")
    print("=" * 50)


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python scorecard.py <skill_dir>")
        sys.exit(1)
    results = run_scorecard(sys.argv[1])
    print_scorecard(results)
