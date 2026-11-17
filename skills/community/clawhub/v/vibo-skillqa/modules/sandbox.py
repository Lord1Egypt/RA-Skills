"""Sandbox infrastructure (Sandbox) + sandbox run module (SandboxRun).

Sandbox isolates every executed script:
- the skill is copied into a temporary `skillqa_*` directory and only the
  copy is ever executed (the original is read-only);
- cleaned environment: fake tokens replace every real credential,
  proxies are stripped, HOME/TMPDIR point inside the temp root;
- per-run working directories inside the temp root;
- hard timeout: SIGTERM, then SIGKILL after a 2 s grace period;
  timed-out runs are marked `timed_out` with exit code 137;
- unbuffered child output (PYTHONUNBUFFERED=1 and `python -u`), so leaked
  secrets written to stdout/stderr are never lost to buffering;
- network namespace via `unshare -n` when running as root and available.

ExecResult is a plain dict:
{exit_code, stdout, stderr, timed_out, duration_ms, rss_kb}
"""

import os
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

# Fake tokens always injected into the sandbox environment.
FAKE_ENV = {
    "FAKE_API_KEY": "sk-fake-0000-1111",
    "OPENAI_API_KEY": "REDACTED-SECRET",
    "ANTHROPIC_API_KEY": "sk-ant-fake-0000",
    "OPENCLAW_API_KEY": "fake-openclaw-0000",
    "GITHUB_TOKEN": "ghp_fake_0000_1111_2222",
    "AWS_ACCESS_KEY_ID": "AKIAFAKE000000000",
    "AWS_SECRET_ACCESS_KEY": "fake0000secret",
    "TELEGRAM_BOT_TOKEN": "0000000000:fake",
    "HF_TOKEN": "hf_fake_0000",
    "DATABASE_URL": "sqlite:///:memory:",
}
# Exact fake values are ignored by the secret-leak scanner.
FAKE_VALUES = set(FAKE_ENV.values())

# License-management scripts: their no-args/--help behaviour is not a skill
# defect (they need a license file / the full package). Reported warn, not fail.
LICENSE_SCRIPT_RE = re.compile(
    r"(license|activate|migrate_secrets|check_license|verify_license)", re.I)

SECRET_NAME_RE = re.compile(r"(TOKEN|KEY|SECRET|PASSWORD|CREDENTIAL|AUTH)", re.I)
PROXY_NAMES = {"http_proxy", "https_proxy", "all_proxy", "ftp_proxy", "no_proxy"}

# Directories never scanned for skill scripts (vendored/aux content).
IGNORE_DIRS = {
    ".git", "__pycache__", "node_modules", ".venv", "venv",
    "fixtures", "qa_reports", "docs", ".hermes", ".openclaw",
}

SCRIPT_EXTS = (".py", ".sh", ".js")


def exec_result(exit_code, stdout, stderr, timed_out=False, duration_ms=0, rss_kb=None):
    """Build an ExecResult dict (stable contract)."""
    return {
        "exit_code": exit_code,
        "stdout": stdout,
        "stderr": stderr,
        "timed_out": timed_out,
        "duration_ms": duration_ms,
        "rss_kb": rss_kb,
    }


def discover_scripts(skill_dir):
    """Find executable skill scripts: *.py / *.sh / *.js.

    Root scripts always win.  Subdirectories are scanned only when the root
    contains at most one script, so helper folders are still tested.
    """
    skill_dir = Path(skill_dir)
    root_scripts = [
        p for p in skill_dir.iterdir()
        if p.is_file() and p.suffix.lower() in SCRIPT_EXTS
    ]
    scripts = list(root_scripts)
    if len(root_scripts) <= 1:
        for p in sorted(skill_dir.rglob("*")):
            if not p.is_file() or p.suffix.lower() not in SCRIPT_EXTS:
                continue
            if p.parent == skill_dir:
                continue
            rel_parts = p.relative_to(skill_dir).parts[:-1]
            if any(part in IGNORE_DIRS for part in rel_parts):
                continue
            scripts.append(p)
    return sorted(set(scripts), key=lambda p: str(p.relative_to(skill_dir)))


class Sandbox:
    """One sandbox per test run. Owns the temp root and execution helpers."""

    def __init__(self, lang="ru", timeout=15):
        self.lang = lang
        self.timeout = timeout
        self.tmp_root = Path(tempfile.mkdtemp(prefix="skillqa_"))
        self.skill_dir = self.tmp_root / "skill"
        self.home_dir = self.tmp_root / "home"
        self.tmp_dir = self.tmp_root / "tmp"
        self.home_dir.mkdir(exist_ok=True)
        self.tmp_dir.mkdir(exist_ok=True)
        self._run_counter = 0
        self._unshare = self._probe_unshare()

    # ------------------------------------------------------------------
    # lifecycle
    # ------------------------------------------------------------------
    def copy_skill(self, src):
        src = Path(src)
        ignore = shutil.ignore_patterns(
            ".git", "__pycache__", "*.pyc", "node_modules",
            ".venv", "venv", "qa_reports",
        )
        shutil.copytree(src, self.skill_dir, ignore=ignore, symlinks=False)

    def cleanup(self):
        """Remove the temp root. This is the ONLY allowed rmtree."""
        root = str(self.tmp_root)
        if os.path.basename(root).startswith("skillqa_"):
            shutil.rmtree(root, ignore_errors=True)

    # ------------------------------------------------------------------
    # environment
    # ------------------------------------------------------------------
    def env(self, extra=None):
        """Whitlisted environment: only safe vars, no real secrets, no proxies.

        Whitelist instead of blacklist: variables with unexpected names must
        never reach untrusted skill code (SkillSpector: Env Variable Harvesting).
        """
        env = {}
        for k in ("PATH", "HOME", "LANG", "LC_ALL", "TMPDIR", "SHELL", "USER"):
            if k in os.environ:
                env[k] = os.environ[k]
        env.update(FAKE_ENV)
        env.update({
            "PATH": os.path.dirname(sys.executable) + ":/usr/bin:/bin",
            "HOME": str(self.home_dir),
            "TMPDIR": str(self.tmp_dir),
            "SHELL": "/bin/sh",
            "LANG": "C.UTF-8",
            "NO_PROXY": "*",
            "PYTHONUNBUFFERED": "1",
            "PYTHONDONTWRITEBYTECODE": "1",
        })
        if extra:
            env.update(extra)
        return env

    def run_dir(self, tag="run"):
        self._run_counter += 1
        d = self.tmp_root / f"{tag}_{self._run_counter}"
        d.mkdir(parents=True, exist_ok=True)
        return d

    # ------------------------------------------------------------------
    # network isolation
    # ------------------------------------------------------------------
    @staticmethod
    def _probe_unshare():
        if os.geteuid() != 0:
            return False
        if not shutil.which("unshare"):
            return False
        try:
            r = subprocess.run(["unshare", "-n", "true"],
                               capture_output=True, timeout=5)
            return r.returncode == 0
        except Exception:
            return False

    # ------------------------------------------------------------------
    # execution
    # ------------------------------------------------------------------
    def _interpreter(self, script, interpreter=None):
        if interpreter:
            return interpreter, None
        ext = Path(script).suffix.lower()
        if ext == ".py":
            # Use the tester's own interpreter (sys.executable), NOT bare
            # "python3" resolved via the sandbox PATH: /usr/bin/python3 may be
            # a different minor version and fail to load compiled modules
            # (e.g. core.cpython-311.so on Python 3.12).
            return sys.executable, None
        if ext == ".sh":
            if shutil.which("bash"):
                return "bash", None
            return None, "bash not found"
        if ext == ".js":
            if shutil.which("node"):
                return "node", None
            return None, "node not found"
        # extension-less script: honour shebang when present
        try:
            first = Path(script).read_text(errors="replace").splitlines()[0]
            if first.startswith("#!"):
                interp = first[2:].strip().split()[0]
                base = os.path.basename(interp)
                found = shutil.which(base) or interp
                if os.path.exists(found):
                    return found, None
                return "bash", None
        except Exception:
            pass
        return None, "unsupported script type"

    def run_script(self, script, args=None, env_extra=None, cwd=None,
                   timeout=None, interpreter=None):
        """Run one skill script in the sandbox. Returns ExecResult dict."""
        args = list(args or [])
        timeout = timeout or self.timeout
        t0 = time.monotonic()
        cwd = cwd or self.run_dir()
        cwd = Path(cwd)
        cwd.mkdir(parents=True, exist_ok=True)

        interp, warn = self._interpreter(script, interpreter)
        if interp is None:
            return exec_result(127, "", warn or "no interpreter",
                               False, 0, None)

        cmd = []
        if self._unshare:
            cmd += ["unshare", "-n", "--"]
        cmd += [interp]
        if (Path(script).suffix.lower() == ".py"
                and os.path.basename(interp).startswith("python")):
            cmd += ["-u"]  # unbuffered: never lose stdout/stderr
        cmd += [str(script)] + args
        return self._execute(cmd, cwd=cwd, env=self.env(env_extra),
                             timeout=timeout, t0=t0)

    def run_cmd(self, cmd, env_extra=None, cwd=None, timeout=None):
        """Run an arbitrary command (e.g. `python3 -c "import x"`) in the sandbox."""
        timeout = timeout or self.timeout
        t0 = time.monotonic()
        cwd = cwd or self.run_dir()
        cwd = Path(cwd)
        cwd.mkdir(parents=True, exist_ok=True)
        if self._unshare:
            cmd = ["unshare", "-n", "--"] + list(cmd)
        return self._execute(list(cmd), cwd=cwd, env=self.env(env_extra),
                             timeout=timeout, t0=t0)

    def _execute(self, cmd, cwd, env, timeout, t0):
        proc = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            cwd=str(cwd), env=env, stdin=subprocess.DEVNULL,
            start_new_session=True,
        )
        pid = proc.pid
        out_chunks, err_chunks = [], []

        def _drain(stream, buf):
            try:
                while True:
                    chunk = stream.read(65536)
                    if not chunk:
                        break
                    buf.append(chunk)
            except Exception:
                pass

        t1 = threading.Thread(target=_drain, args=(proc.stdout, out_chunks), daemon=True)
        t2 = threading.Thread(target=_drain, args=(proc.stderr, err_chunks), daemon=True)
        t1.start()
        t2.start()

        deadline = time.monotonic() + timeout
        timed_out = False
        exit_code = None
        reaped = False
        while time.monotonic() < deadline:
            # peek at the child state WITHOUT reaping (WNOWAIT), so os.wait4
            # below still returns the per-run rusage
            try:
                info = os.waitid(os.P_PID, pid,
                                 os.WEXITED | os.WNOHANG | os.WNOWAIT)
            except OSError:
                info = True  # child already reaped -> stop polling
            if info:
                break
            time.sleep(0.05)
        else:
            # hard timeout: SIGTERM, then SIGKILL after a grace period
            timed_out = True
            try:
                os.killpg(pid, signal.SIGTERM)
            except (ProcessLookupError, PermissionError):
                pass
            try:
                proc.wait(timeout=2)
            except subprocess.TimeoutExpired:
                try:
                    os.killpg(pid, signal.SIGKILL)
                except (ProcessLookupError, PermissionError):
                    pass
                try:
                    proc.wait(timeout=2)
                except Exception:
                    pass
            exit_code = 137
            reaped = True

        # Peak RSS (VmHWM) — read while the (zombie) process is still visible.
        rss_kb = None
        try:
            with open(f"/proc/{pid}/status", "r", errors="replace") as fh:
                for line in fh:
                    if line.startswith("VmHWM"):
                        rss_kb = int(line.split()[1])
                        break
        except Exception:
            pass

        if not reaped:
            try:
                _, wstatus, ru = os.wait4(pid, 0)
                exit_code = os.waitstatus_to_exitcode(wstatus)
                proc.returncode = exit_code
                if rss_kb is None and getattr(ru, "ru_maxrss", 0):
                    rss_kb = int(ru.ru_maxrss)
            except ChildProcessError:
                exit_code = proc.returncode if proc.returncode is not None else -1

        t1.join()
        t2.join()
        stdout = b"".join(out_chunks).decode("utf-8", errors="replace")
        stderr = b"".join(err_chunks).decode("utf-8", errors="replace")
        if timed_out:
            exit_code = 137
        duration_ms = int((time.monotonic() - t0) * 1000)
        return exec_result(exit_code, stdout, stderr, timed_out, duration_ms, rss_kb)

    MAX_PARALLEL = 20  # hard cap: runaway n must not exhaust the host

    def run_many(self, script, n, timeout=None, interpreter=None):
        """Run n instances concurrently, each in its own par_<i> directory."""
        timeout = timeout or self.timeout
        results = []
        n = max(1, min(int(n), self.MAX_PARALLEL))

        def _one(i):
            cwd = self.tmp_root / f"par_{i}"
            cwd.mkdir(parents=True, exist_ok=True)
            return self.run_script(script, cwd=cwd, timeout=timeout,
                                   interpreter=interpreter)

        with ThreadPoolExecutor(max_workers=n) as ex:
            futs = [ex.submit(_one, i) for i in range(n)]
            for f in futs:
                try:
                    results.append(f.result())
                except Exception as e:  # pragma: no cover
                    results.append(exec_result(-1, "", f"runner error: {e}"))
        return results


# ---------------------------------------------------------------------------
# SandboxRun — verification module (behaviour / crashes)
# ---------------------------------------------------------------------------

def _check(name, status, detail):
    return {"name": name, "status": status, "detail": detail}


def _module_status(checks):
    if any(c["status"] == "fail" for c in checks):
        return "fail"
    if any(c["status"] == "warn" for c in checks):
        return "warn"
    return "pass"


def _traceback_kind(text):
    """Classify a traceback: 'import' (real defect), 'missing_file' (needs
    license/config — a peculiarity, not a crash), or 'crash' (real)."""
    if not re.search(r"Traceback \(most recent call last\):", text):
        return None
    if re.search(r"\b(ImportError|ModuleNotFoundError)\b", text):
        return "import"
    if re.search(r"\b(FileNotFoundError|IsADirectoryError|NotADirectoryError|ENOENT)\b", text):
        return "missing_file"
    if re.search(r"\bOSError\b|PermissionError", text):
        return "missing_file"
    return "crash"


def _traceback_summary(text):
    """Return the exception line of the last traceback, if any."""
    m = re.search(r"Traceback \(most recent call last\):\n(?:.*\n)*?(\w+(?:\.\w+)*: .+)", text)
    if m:
        return m.group(1).strip()
    return None


def _snapshot(dirp):
    snap = {}
    for p in Path(dirp).rglob("*"):
        if p.is_file():
            try:
                snap[str(p)] = p.stat().st_mtime_ns
            except OSError:
                pass
    return snap


class SandboxRun:
    name = "sandbox"
    title = {"ru": "Песочница (запуск скриптов)", "en": "Sandbox run"}

    @staticmethod
    def _internal(ctx):
        """True for internal (non-public) skills: their scripts depend on
        project environment (network, paths, tokens), so sandbox failures
        are expected and reported as warnings, not defects."""
        try:
            md = Path(ctx.skill_path) / "SKILL.md"
            txt = md.read_text(encoding="utf-8", errors="replace")
            head = txt.split("---", 2)
            return len(head) >= 2 and re.search(r"(?m)^internal:\s*true", head[1]) is not None
        except Exception:
            return False

    def run(self, ctx):
        t = ctx.t
        checks = []
        scripts = discover_scripts(ctx.sandbox.skill_dir)
        if not scripts:
            if self._internal(ctx):
                checks.append(_check("scripts_discovered", "pass",
                                     t("check.scripts_discovered.none")))
            else:
                checks.append(_check("scripts_discovered", "warn",
                                     t("check.scripts_discovered.none")))
            return {"module": self.name, "status": "warn", "checks": checks,
                    "details": t("check.scripts_discovered.summary")}

        rows = []
        isolated_ok = True
        original_snapshot = _snapshot(ctx.skill_path)
        internal = self._internal(ctx)

        for script in scripts:
            rel = str(script.relative_to(ctx.sandbox.skill_dir))

            # 1) plain run with empty argv
            r = ctx.sandbox.run_script(script, [])
            ctx.run_outputs.append(r)
            rows.append(f"  {rel}: exit={r['exit_code']}, "
                        f"{r['duration_ms']} ms, timed_out={r['timed_out']}")
            name = f"run_{script.name}"
            tb = _traceback_summary(r["stderr"] + "\n" + r["stdout"])
            if r["timed_out"]:
                isolated_ok = False
                checks.append(_check(name, "fail",
                                     t("check.run.timeout", s=ctx.timeout)))
            elif r["exit_code"] == 0:
                if r["stderr"].strip():
                    checks.append(_check(name, "warn", t("check.run.warn")))
                else:
                    checks.append(_check(name, "pass", t("check.run.ok", ms=r["duration_ms"])))
            else:
                err_all = r["stderr"] + "\n" + r["stdout"]
                if LICENSE_SCRIPT_RE.search(script.name):
                    checks.append(_check(name, "warn", t("check.run.warn")))
                elif re.search(r"usage|use:|required|требуется|использование", err_all, re.I):
                    checks.append(_check(name, "warn", t("check.run.warn")))
                elif (r["exit_code"] == 127
                        or "ModuleNotFoundError" in err_all
                        or "No module named" in err_all
                        or "command not found" in err_all
                        or "not found in PATH" in err_all):
                    # environment gap (missing dependency/interpreter), not a
                    # skill defect — warn, don't fail
                    checks.append(_check(name, "warn", t("check.run.env")))
                else:
                    detail = t("check.run.fail", code=r["exit_code"])
                    if tb:
                        detail = f"{detail}: {tb[:150]}"
                    checks.append(_check(name, "warn" if internal else "fail", detail))

            # 2) --help
            rh = ctx.sandbox.run_script(script, ["--help"])
            ctx.run_outputs.append(rh)
            rows.append(f"  {rel} --help: exit={rh['exit_code']}, "
                        f"{rh['duration_ms']} ms, timed_out={rh['timed_out']}")
            name = f"help_{script.name}"
            hout = rh["stdout"] + "\n" + rh["stderr"]
            if rh["timed_out"]:
                isolated_ok = False
                checks.append(_check(name, "fail", t("check.help.timeout", s=ctx.timeout)))
            elif rh["exit_code"] == 0:
                checks.append(_check(name, "pass", t("check.help.ok")))
            elif LICENSE_SCRIPT_RE.search(script.name):
                checks.append(_check(name, "warn", t("check.help.warn", code=rh["exit_code"])))
            elif re.search(r"usage|use:|help|использование", hout, re.I):
                checks.append(_check(name, "warn", t("check.help.warn", code=rh["exit_code"])))
            elif (rh["exit_code"] == 127 or "ModuleNotFoundError" in hout
                  or "No module named" in hout or "command not found" in hout):
                checks.append(_check(name, "warn", t("check.help.warn", code=rh["exit_code"])))
            elif _traceback_summary(hout):
                if _traceback_kind(hout) == "missing_file" or (
                        _traceback_kind(hout) == "import" and LICENSE_SCRIPT_RE.search(script.name)):
                    checks.append(_check(name, "warn", t("check.help.warn", code=rh["exit_code"])))
                else:
                    checks.append(_check(name, "warn" if internal else "fail", t("check.help.crash")))
            else:
                checks.append(_check(name, "warn" if internal else "fail", t("check.help.fail", code=rh["exit_code"])))

            # 3) no arguments
            rn = ctx.sandbox.run_script(script, [])
            ctx.run_outputs.append(rn)
            rows.append(f"  {rel} (no args): exit={rn['exit_code']}, "
                        f"{rn['duration_ms']} ms, timed_out={rn['timed_out']}")
            name = f"noargs_{script.name}"
            nout = rn["stdout"] + "\n" + rn["stderr"]
            if rn["timed_out"]:
                isolated_ok = False
                checks.append(_check(name, "fail", t("check.noargs.timeout", s=ctx.timeout)))
            elif rn["exit_code"] != 0:
                if LICENSE_SCRIPT_RE.search(script.name):
                    checks.append(_check(name, "warn", t("check.noargs.warn_code", code=rn["exit_code"])))
                elif (rn["exit_code"] == 127 or "ModuleNotFoundError" in nout
                      or "No module named" in nout or "command not found" in nout):
                    checks.append(_check(name, "warn", t("check.noargs.warn_code", code=rn["exit_code"])))
                elif _traceback_summary(nout):
                    _kind = _traceback_kind(nout)
                    if _kind == "missing_file":
                        checks.append(_check(name, "warn", t("check.noargs.warn_code", code=rn["exit_code"])))
                    else:
                        checks.append(_check(name, "warn" if internal else "fail", t("check.noargs.crash")))
                elif re.search(r"usage|error|required|требуется|использование", nout, re.I):
                    checks.append(_check(name, "pass", t("check.noargs.ok", code=rn["exit_code"])))
                else:
                    checks.append(_check(name, "warn", t("check.noargs.warn_code", code=rn["exit_code"])))
            else:
                checks.append(_check(name, "warn", t("check.noargs.warn")))

        # 4) isolation
        after_snapshot = _snapshot(ctx.skill_path)
        wrote_original = [
            p for p, mt in after_snapshot.items()
            if p not in original_snapshot or original_snapshot[p] != mt
        ]
        if wrote_original:
            checks.append(_check("sandbox_isolated", "fail",
                                 t("check.sandbox_isolated.fail",
                                   files=", ".join(wrote_original[:3]))))
        elif not isolated_ok:
            checks.append(_check("sandbox_isolated", "warn",
                                 t("check.sandbox_isolated.warn")))
        else:
            checks.append(_check("sandbox_isolated", "pass",
                                 t("check.sandbox_isolated.ok")))

        status = _module_status(checks)
        n_fail = sum(1 for c in checks if c["status"] == "fail")
        n_warn = sum(1 for c in checks if c["status"] == "warn")
        details = t("module.summary", total=len(checks), fail=n_fail, warn=n_warn)
        details += "\n" + "\n".join(rows)
        return {"module": self.name, "status": status, "checks": checks,
                "details": details}
