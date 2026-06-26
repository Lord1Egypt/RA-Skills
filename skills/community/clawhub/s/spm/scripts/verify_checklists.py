#!/usr/bin/env python3
"""
verify_checklists.py — Automated verification of checklist items

Usage:
  ./scripts/verify_checklists.py code        # Verify CODE-COMPLETION checklist items
  ./scripts/verify_checklists.py deploy     # Verify DEPLOYMENT-READINESS checklist items
  ./scripts/verify_checklists.py all        # Run all verifications

This script checks items that can be validated automatically (via commands, file checks, etc.)
It outputs a JSON report that can be referenced in the checklist markdown.
"""

import os
import sys
import json
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
os.chdir(PROJECT_ROOT)

def run_cmd(cmd, check=True):
    """Run shell command and capture output."""
    result = subprocess.run(
        cmd, shell=True, capture_output=True, text=True, check=False
    )
    if check and result.returncode != 0:
        return {"ok": False, "output": result.stderr}
    return {"ok": result.returncode == 0, "output": result.stdout + result.stderr}

def check_type_check():
    """npm run type-check"""
    if not (PROJECT_ROOT / "package.json").exists():
        return {"name": "TypeScript type check", "passed": True, "output": "No package.json — skipped"}
    res = run_cmd("npm run type-check", check=False)
    return {
        "name": "TypeScript type check",
        "passed": res["ok"],
        "output": res["output"][-500:]  # tail
    }

def check_lint():
    """npm run lint"""
    if not (PROJECT_ROOT / "package.json").exists():
        return {"name": "ESLint check", "passed": True, "output": "No package.json — skipped"}
    res = run_cmd("npm run lint", check=False)
    return {
        "name": "ESLint check",
        "passed": res["ok"],
        "output": res["output"][-500:]
    }

def check_tests():
    """npm test"""
    if not (PROJECT_ROOT / "package.json").exists():
        return {"name": "Unit tests", "passed": True, "output": "No package.json — skipped"}
    res = run_cmd("npm test", check=False)
    return {
        "name": "Unit tests",
        "passed": res["ok"],
        "output": res["output"][-500:]
    }

def check_secrets():
    """grep for common secret patterns in src/"""
    cmd = r"grep -rE 'API_KEY|SECRET|PASSWORD|TOKEN|PRIVATE|AUTH' --include='*.ts' --include='*.js' src/ 2>/dev/null | grep -v 'node_modules' || true"
    res = run_cmd(cmd, check=False)
    found = res["output"].strip() != ""
    return {
        "name": "No secrets in code",
        "passed": not found,
        "output": "Secrets found:\n" + res["output"] if found else "No secrets detected"
    }

def check_no_console_log():
    """grep for console.log statements in src/ (except logger)"""
    cmd = r"grep -rE 'console\.log\(' --include='*.ts' --include='*.js' src/ 2>/dev/null | grep -v 'node_modules' || true"
    res = run_cmd(cmd, check=False)
    found = res["output"].strip() != ""
    return {
        "name": "No console.log in production code",
        "passed": not found,
        "output": "console.log found:\n" + res["output"] if found else "No console.log statements"
    }

def check_coverage():
    """Check test coverage report (assumes coverage/ directory or jest-html-report)"""
    coverage_file = PROJECT_ROOT / "coverage" / "coverage-summary.json"
    if not coverage_file.exists():
        return {
            "name": "Test coverage",
            "passed": False,
            "output": "Coverage report not found. Run npm run test:coverage first."
        }
    try:
        with open(coverage_file) as f:
            data = json.load(f)
        total = data.get("total", {})
        pct = total.get("lines", {}).get("pct", 0)
        passed = pct >= 80
        return {
            "name": "Test coverage ≥ 80%",
            "passed": passed,
            "output": f"Line coverage: {pct}%"
        }
    except Exception as e:
        return {
            "name": "Test coverage",
            "passed": False,
            "output": f"Error reading coverage: {e}"
        }

def verify_code_checklist():
    """Run all automated checks for CODE-COMPLETION."""
    checks = [
        check_type_check,
        check_lint,
        check_tests,
        check_secrets,
        check_no_console_log,
        check_coverage,
    ]
    results = []
    for fn in checks:
        try:
            res = fn()
            results.append(res)
        except Exception as e:
            results.append({
                "name": fn.__name__,
                "passed": False,
                "output": str(e)
            })
    return results

def verify_deployment_checklist():
    """Deployment readiness automated checks."""
    results = []

    # E2E script exists and is executable
    e2e_script = PROJECT_ROOT / "scripts" / "e2e.sh"
    results.append({
        "name": "E2E script exists and executable",
        "passed": e2e_script.exists() and os.access(e2e_script, os.X_OK),
        "output": str(e2e_script) if e2e_script.exists() else "Missing scripts/e2e.sh"
    })

    # .env.example exists
    env_example = PROJECT_ROOT / ".env.example"
    results.append({
        "name": ".env.example exists",
        "passed": env_example.exists(),
        "output": str(env_example) if env_example.exists() else "Missing .env.example"
    })

    # config/default.yaml exists (if using config-as-code)
    config_file = PROJECT_ROOT / "config" / "default.yaml"
    results.append({
        "name": "Config file exists (config/default.yaml)",
        "passed": config_file.exists(),
        "output": str(config_file) if config_file.exists() else "Missing config/default.yaml"
    })

    # Health endpoint reachable (if worker deployed to staging)
    # This is a soft check: just report not reachable, don't fail automatically
    health_url = os.getenv("HEALTH_CHECK_URL")
    if health_url:
        res = run_cmd(f"curl -sf {health_url}", check=False)
        results.append({
            "name": "Health endpoint reachable",
            "passed": res["ok"],
            "output": res["output"][-200:]
        })
    else:
        results.append({
            "name": "Health endpoint reachable (skipped, set HEALTH_CHECK_URL)",
            "passed": True,
            "output": "HEALTH_CHECK_URL not set — skipped"
        })

    return results

def main():
    if len(sys.argv) < 2:
        print("Usage: verify_checklists.py [code|deploy|all]")
        sys.exit(1)

    mode = sys.argv[1]
    all_results = []

    if mode in ("code", "all"):
        all_results.extend(verify_code_checklist())

    if mode in ("deploy", "all"):
        all_results.extend(verify_deployment_checklist())

    # Print summary
    print("\n=== Checklist Verification Report ===")
    for r in all_results:
        status = "✅" if r["passed"] else "❌"
        print(f"{status} {r['name']}")
        if not r["passed"] or len(r["output"].strip()) > 0:
            print(f"   → {r['output'].strip()[:200]}")

    # Save JSON report
    report_file = PROJECT_ROOT / "docs" / "checklists" / "verification-report.json"
    report_file.parent.mkdir(parents=True, exist_ok=True)
    with open(report_file, "w") as f:
        json.dump({
            "timestamp": subprocess.getoutput("date -u +%Y-%m-%dT%H:%M:%SZ"),
            "results": all_results
        }, f, indent=2)
    print(f"\n📄 Full report: {report_file}")

    # Exit 0 if all passed, 1 otherwise
    if all(r["passed"] for r in all_results):
        print("\n✅ All checks passed")
        sys.exit(0)
    else:
        failed = sum(1 for r in all_results if not r["passed"])
        print(f"\n❌ {failed} check(s) failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
