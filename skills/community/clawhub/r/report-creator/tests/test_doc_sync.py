import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "check-doc-sync.py"
TMP_ROOT = ROOT / ".tmp-test-doc-sync"
TMP_ROOT.mkdir(exist_ok=True)


def write_fixture_repo(
    tmp_path: Path,
    *,
    skill: str,
    readme_en: str,
    readme_zh: str,
    checklist: str,
) -> Path:
    root = tmp_path / "repo"
    (root / "references").mkdir(parents=True, exist_ok=True)
    (root / "SKILL.md").write_text(skill, encoding="utf-8")
    (root / "README.md").write_text(readme_en, encoding="utf-8")
    (root / "README.zh-CN.md").write_text(readme_zh, encoding="utf-8")
    (root / "references" / "review-checklist.md").write_text(checklist, encoding="utf-8")
    return root


def run_checker(repo_root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--root", str(repo_root), *args],
        capture_output=True,
        text=True,
        timeout=15,
    )


def make_case_dir(name: str) -> Path:
    case_dir = TMP_ROOT / name
    shutil.rmtree(case_dir, ignore_errors=True)
    case_dir.mkdir(parents=True, exist_ok=True)
    return case_dir


def test_doc_sync_checker_passes_for_valid_fixture():
    repo = write_fixture_repo(
        make_case_dir("valid"),
        skill=(
            "--review [file]\n"
            "references/review-checklist.md\n"
            "references/review-report-template.md\n"
            "silent final review pass\n"
            "one-pass automatic refinement\n"
            "no file given\n"  # v4 guardrails: context-backed generate prose
            "IR from context\n"  # v4 guardrails: IR-from-context routing
            "report_class: mixed\n"  # v4 guardrails: optional report_class prose
            "extract exactly one valid IR block from context\n"
            "Never render the surrounding conversation.\n"
            "Load reference files minimally\n"
            "load only the references that materially help the current render path\n"
            "Thin Routing Over Prompt Growth\n"
            "Contracts and Gates Beat Prompt Soup\n"
        ),
        readme_en=(
            "/report --review\n"
            "13-checkpoint review system\n"
            "silent final review\n"
            "review-report-template.md\n"
            "Capability Growth Must Reduce Context Load\n"
            "Move quality checks off the hot path.\n"
        ),
        readme_zh=(
            "/report --review\n"
            "13 项检查点\n"
            "静默终审\n"
            "review-report-template.md\n"
            "能力增长先减少上下文负担\n"
            "质量机制后移\n"
        ),
        checklist=(
            "### 1.1 BLUF Opening\n"
            "### 1.5 Takeaway After Data\n"
            "### 2.3 Conditional Reader Guidance\n"
            "## Rejected Candidates\n"
        ),
    )

    result = run_checker(repo, "--dry-run")

    assert result.returncode == 0, result.stdout + result.stderr
    assert "PASS" in result.stdout


def test_doc_sync_checker_fails_on_drift():
    repo = write_fixture_repo(
        make_case_dir("drift"),
        skill="--generate only\n",
        readme_en="Two-step with review\n",
        readme_zh="支持中间审查\n",
        checklist="placeholder\n",
    )

    result = run_checker(repo, "--dry-run")

    assert result.returncode == 1
    assert "skill-contract" in result.stdout
    assert "readme-en-contract" in result.stdout
    assert "readme-zh-contract" in result.stdout
    assert "checklist-contract" in result.stdout


def test_repo_docs_are_current():
    result = run_checker(ROOT, "--dry-run")

    assert result.returncode == 0, result.stdout + result.stderr
