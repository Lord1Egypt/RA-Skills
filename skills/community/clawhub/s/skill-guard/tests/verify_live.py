"""Exercise the real registry and scanner in a disposable workspace; no mocked CLIs."""

import argparse
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("safe_install", ROOT / "scripts/safe_install.py")
guard = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(guard)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("slug")
    parser.add_argument("--version", required=True)
    parser.add_argument("--expect", choices=("clean", "findings"), required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    guard.arguments([args.slug, "--version", args.version])
    report = {"slug": args.slug, "version": args.version, "expected_scan": args.expect,
              "scanner": guard.SCANNER, "checks": [], "complete": False}

    def check(name, success):
        report["checks"].append({"name": name, "passed": bool(success)})
        print(("PASS: " if success else "FAIL: ") + name, flush=True)
        if not success:
            raise RuntimeError(name)

    def run(command, cwd, env):
        # Keep raw output in memory: even scanner errors can quote sensitive text.
        return subprocess.run(command, cwd=cwd, env=env, stdin=subprocess.DEVNULL,
                              capture_output=True, timeout=300)

    try:
        check("Required real CLIs are available", all(shutil.which(tool) for tool in ("clawhub", "uvx")))
        with tempfile.TemporaryDirectory(prefix="skill-guard-live-") as temporary:
            work = Path(temporary).resolve()
            env = dict(os.environ)
            downloaded = work / "download"
            downloaded.mkdir(mode=0o700)
            fetched = run(["clawhub", "--workdir", str(downloaded), "--dir", "skills", "--no-input",
                           "install", args.slug, "--version", args.version], work, env)
            check("Real ClawHub download succeeds", fetched.returncode == 0)
            staged = downloaded / "skills" / args.slug
            files = guard.snapshot(staged)
            inspected = run(["uvx", "--from", guard.SCANNER, "snyk-agent-scan", "inspect",
                             "--json", "--skills", str(staged)], work, env)
            check("Real scanner local inspection succeeds", inspected.returncode == 0)
            data = json.loads(inspected.stdout)
            check("Inspection returns one path", isinstance(data, dict) and len(data) == 1)
            path, result = next(iter(data.items()))
            check("Inspection path matches the skill or parent", Path(path).expanduser() in (staged, staged.parent))
            check("Inspection reports one skill and no MCP servers",
                  result.get("error") is None and result.get("servers") == [] and len(result.get("skills", [])) == 1)
            skill = result["skills"][0]
            names = [entry["path"] for entry in skill.get("files", [])]
            check("Real scanner inspection covers every staged file",
                  skill.get("error") is None and len(names) == len(set(names)) and set(names) == set(files))
            report["inspected_file_count"] = len(names)

            unauthenticated = work / "no-auth"
            old = unauthenticated / "skills" / args.slug
            old.mkdir(parents=True)
            (old / "old.txt").write_text("existing installation sentinel")
            no_auth_env = dict(env, CLAWHUB_WORKDIR=str(unauthenticated))
            no_auth_env.pop("SNYK_TOKEN", None)
            command = [str(ROOT / "scripts/safe-install.sh"), args.slug, "--version", args.version]
            refused = run(command + ["--force"], work, no_auth_env)
            check("Missing authentication blocks the real installer",
                  refused.returncode == 1 and b"SNYK_TOKEN" in refused.stderr)
            check("Missing authentication preserves the existing installation",
                  (old / "old.txt").read_text() == "existing installation sentinel"
                  and not (unauthenticated / ".skill-guard").exists())

            if not env.get("SNYK_TOKEN"):
                report["blocked_reason"] = "SNYK_TOKEN is unavailable; authenticated scan and promotion checks were not run."
                print("BLOCKED: " + report["blocked_reason"], flush=True)
                return 2

            live = work / "guarded-install"
            target = live / "skills" / args.slug
            live_env = dict(env, CLAWHUB_WORKDIR=str(live))
            if args.expect == "findings":
                target.mkdir(parents=True)
                (target / "old.txt").write_text("existing installation sentinel")
                blocked = run(command + ["--force"], work, live_env)
                check("Authenticated findings block installation", blocked.returncode == 2)
                check("Findings preserve the existing installation",
                      (target / "old.txt").read_text() == "existing installation sentinel")
                check("Flagged candidate remains in quarantine",
                      len(list((live / ".skill-guard").glob("run-*/skills/" + args.slug + "/SKILL.md"))) == 1)
            else:
                installed = run(command, work, live_env)
                check("Authenticated clean scan installs the skill", installed.returncode == 0)
                actual = guard.snapshot(target)
                check("Installed file set matches the registry download", set(actual) == set(files))
                check("Installed payload matches the registry download",
                      all(actual[name][0] == value[0] for name, value in files.items()
                          if name != ".clawhub/origin.json"))
                (target / "local-marker.txt").write_text("preserve this in backup")
                replaced = run(command + ["--force"], work, live_env)
                check("Authenticated clean replacement succeeds", replaced.returncode == 0)
                backups = list((live / ".skill-guard").glob("run-*/previous-skill/local-marker.txt"))
                check("Replacement retains the previous installation",
                      len(backups) == 1 and backups[0].read_text() == "preserve this in backup"
                      and not (target / "local-marker.txt").exists())
                before = guard.snapshot(target)
                refused = run(command, work, live_env)
                check("Existing installation is preserved without force",
                      refused.returncode == 1 and guard.snapshot(target) == before)
            report["complete"] = True
            return 0
    except (RuntimeError, OSError, ValueError, KeyError, TypeError, subprocess.TimeoutExpired, guard.Blocked) as error:
        report["failure_type"] = type(error).__name__
        print("Live verification failed; raw tool output was withheld.", file=sys.stderr)
        return 1
    finally:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, indent=2) + "\n")


if __name__ == "__main__":
    sys.exit(main())
