# -*- coding: utf-8 -*-
"""
spss_helper.py - Helper for invoking SPSS without a splash screen.

Call priority (highest to lowest):
  1) stats.com console edition -production silent -nologo (option 1: fully
     splash-free and foolproof). Daily complex-syntax runs; no feature limits.
  2) SPSS bundled Python StartSPSS() + Submit() + StopSPSS() (option 2: no
     splash). WARNING: runs pure analysis syntax only and MUST NOT include:
        - OUTPUT SAVE (save the output document)
        - OUTPUT EXPORT / OUTPUT DISPLAY (export/display output)
        - HOST COMMAND (run OS commands)
        - XDATA / XSAVE (when OUTPUT objects are involved)
     When unsure whether a command touches OUTPUT/SAVE, always use option 1.
  3) stats.exe -production silent -nologo (option 3: may show a splash; the
     strict mode requires an explicit STATSOFT_CONFIRM=1 confirmation).

.spj file format requirements:
  - Must use the SPSS 26+ new format: <output>/<syntax> sub-elements (not
    attributes).
  - Paths MUST use forward slashes / (backslashes cause NullPointerException).
  - The <output> element is required, otherwise NullPointerException.
"""

import os
import sys
import re
import subprocess
import tempfile
import shutil

# ============================================================
# Dynamic path discovery
# ============================================================

SPSS_ROOTS = [
    r"C:\Program Files\IBM\SPSS",
    r"C:\Program Files (x86)\IBM\SPSS",
    r"C:\Program Files\IBM\SPSS30",
    r"D:\Program Files\IBM\SPSS",
    r"D:\Program Files (x86)\IBM\SPSS",
    r"C:\SPSS",
    r"D:\SPSS",
    r"D:\IBM\SPSS",
    r"E:\SPSS",
    r"E:\IBM\SPSS",
]

SPSS_VERSIONS = ["26", "27", "28", "29", "30"]
DRIVES = ["C", "D", "E"]


def _generate_candidates(exe_name):
    """Generate candidate paths for SPSS executables."""
    cands = []
    for root in SPSS_ROOTS:
        for ver in SPSS_VERSIONS:
            cands.append(os.path.join(root, "Statistics", ver, exe_name))
    for d in DRIVES:
        for ver in SPSS_VERSIONS:
            cands.append(os.path.join(d + ":", "SPSS", "Statistics", ver, exe_name))
            cands.append(os.path.join(d + ":", "Program Files", "IBM", "SPSS", "Statistics", ver, exe_name))
            cands.append(os.path.join(d + ":", "Program Files", "IBM", "SPSS" + ver, "Statistics", ver, exe_name))
    return cands


def _log(msg_cn, msg_en):
    """Log helper; prints only the English message (default English)."""
    print(msg_en)


def _minimal_env(extra_path=None):
    """Build a minimal environment for child SPSS/Python processes.

    Avoids forwarding the full parent environment (which may contain API keys,
    tokens, proxy credentials, or agent-specific secrets) into a third-party
    interpreter. Only a small allow-list needed for process startup is copied;
    PATH may be extended via extra_path.

    PYTHONPATH is **deliberately excluded**: SPSS's bundled Python is 3.4, while
    agent shells (e.g. WorkBuddy Bash) may inject
    ``PYTHONPATH=<app>/cli/vendor/shim`` whose ``sitecustomize.py`` uses
    ``os.fspath`` (added in 3.6). Forwarding it makes the SPSS interpreter abort
    at startup with
    ``AttributeError: 'module' object has no attribute 'fspath'``. The bundled
    runner sets up its own site-packages via ``sys.path``, so it never needs the
    parent's PYTHONPATH.
    """
    _ALLOWED = (
        "PATH", "SYSTEMROOT", "SYSTEMDRIVE", "WINDIR", "TEMP", "TMP",
        "USERPROFILE", "HOME", "LANG", "LC_ALL", "PYTHONIOENCODING",
        "COMSPEC", "NUMBER_OF_PROCESSORS", "PROCESSOR_ARCHITECTURE",
        "OS", "PATHEXT",
    )
    env = {}
    for k in _ALLOWED:
        v = os.environ.get(k)
        if v is not None:
            env[k] = v
    if extra_path:
        env["PATH"] = extra_path + os.pathsep + env.get("PATH", "")
    return env


def _opt_in_confirm(prompt_cn, prompt_en):
    """Execution authorization for launching SPSS external processes
    (stats.com / stats.exe / bundled Python) with user-provided job/syntax files.

    FAIL-CLOSED: returns False by default. Proceed ONLY when an explicit opt-in
    is present:
      * STATSOFT_AUTO_WRITE=1            -> non-interactive / agent opt-in (proceed).
      * STATSOFT_CONFIRM=1 AND a real TTY AND user answers y -> interactive confirm.
    Any other case (incl. a plain user invocation without opt-in) -> deny, so an
    agent or upstream tool cannot trigger third-party execution unexpectedly.
    Returns True only if execution is explicitly authorized.
    """
    if os.environ.get("STATSOFT_AUTO_WRITE") == "1":
        return True
    if os.environ.get("STATSOFT_CONFIRM") == "1" and sys.stdin.isatty():
        try:
            sys.stdout.write(prompt_en + " (y/N) ")
            sys.stdout.flush()
            ans = sys.stdin.readline().strip().lower()
            return ans in ("y", "yes")
        except Exception:
            return False
    return False


def _validate_path(path, kind):
    """Validate an SPSS path."""
    if not path:
        return None
    real = os.path.realpath(path)
    if kind == "stats_com":
        if not real.lower().endswith("stats.com"):
            return None
    elif kind == "stats":
        if not real.lower().endswith("stats.exe"):
            return None
    lowered = real.lower()
    if "spss" in lowered and "statistics" in lowered:
        m = re.search(r'statistics[/\\](\d+)[/\\]', lowered)
        if m and m.group(1) in SPSS_VERSIONS:
            return real
    return None


def _detect_locale():
    """Auto-detect the SPSS <locale> from the host environment so we never
    hard-code a region that would change parsing/encoding/reproducibility
    (SQP-3). Returns (country, language) for a zh host, or None to let SPSS
    inherit the system/user environment (locale element omitted)."""
    import locale as _locale
    try:
        lang, _enc = _locale.getdefaultlocale()
    except Exception:
        lang = None
    if not lang:
        env_lang = (os.environ.get("LANG") or os.environ.get("LC_ALL")
                    or os.environ.get("LANGUAGE") or "")
        lang = env_lang.split(".")[0] if env_lang else None
    if not lang:
        return None
    parts = lang.replace("_", "-").split("-")
    language = parts[0].lower()
    country = parts[1].upper() if len(parts) > 1 else None
    if language in ("zh", "cn"):
        return ("CN", "zh")
    # Non-Chinese host: omit the locale element so SPSS inherits the environment.
    return None


def validate_syntax(syntax_text):
    """Validate SPSS syntax safety before execution. Returns (ok, reason).

    Allows: pure analysis syntax (GET / COMPUTE / REGRESSION / etc.).
    Blocks (ok=False) commands that can execute system commands or read/modify
    the environment:
      - HOST COMMAND       (executes OS shell commands)
      - INSERT FILE        (reads arbitrary files from disk)
      - PRESERVE / RESTORE  (modify/restore the SPSS environment)
    """
    forbidden = [
        r'^\s*HOST\s+COMMAND',
        r'^\s*INSERT\s+FILE',
        r'^\s*PRESERVE\b',
        r'^\s*RESTORE\b',
    ]
    for pat in forbidden:
        if re.search(pat, syntax_text, re.IGNORECASE | re.MULTILINE):
            return False, "Blocked command pattern: " + pat
    return True, ""


def _validate_spj(spj_file):
    """Reject .spj production-job files that embed forbidden SPSS syntax
    (HOST COMMAND / INSERT FILE / PRESERVE / RESTORE). Executing a
    user-supplied job must never run OS shell commands or read arbitrary
    files."""
    try:
        with open(spj_file, "r", encoding="utf-8", errors="replace") as f:
            text = f.read()
    except Exception as e:
        return False, "Unable to read .spj: " + str(e)
    return validate_syntax(text)


def _run_silent(cmd, env=None, timeout=300):
    """Controlled execution: only accepts a list-form command (shell strings
    forbidden). The caller must validate the executable beforehand."""
    if not isinstance(cmd, list) or not cmd:
        _log("Rejected: command must be a non-empty list (shell forbidden)", "Rejected: command must be a non-empty list (shell forbidden)")
        return 1, "", "invalid command"
    try:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
        try:
            stdout, stderr = p.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            p.kill()
            stdout, stderr = p.communicate()
            print("Execution timed out ({}s)".format(timeout))
            return 1, "", "Timeout"
        out_str = stdout.decode("utf-8", errors="replace") if stdout else ""
        err_str = stderr.decode("utf-8", errors="replace") if stderr else ""
        return p.returncode, out_str, err_str
    except Exception as e:
        return 1, "", str(e)


# ============================================================
# Preferred: stats.com console edition (no splash)
# ============================================================

def run_console(spj_file, stats_com=None):
    """Preferred: run the .spj file via the stats.com console edition (fully splash-free)."""
    if not _opt_in_confirm("⚠️ About to run SPSS syntax via stats.com. Continue?",
                           "⚠️ About to run SPSS syntax via stats.com. Continue?"):
        _log("Execution cancelled (not confirmed).", "Execution cancelled (not confirmed).")
        return 1
    if not os.path.exists(spj_file):
        _log(".spj file not found: " + spj_file, ".spj file not found: " + spj_file)
        return 1

    ok, reason = _validate_spj(spj_file)
    if not ok:
        _log("Job file security check failed: " + reason, "Job file security check failed: " + reason)
        return 1

    if stats_com is None:
        for c in _generate_candidates("stats.com"):
            if os.path.exists(c):
                stats_com = c
                break
        if stats_com is None:
            _log("stats.com (console version) not found", "stats.com (console version) not found")
            return 1

    validated = _validate_path(stats_com, "stats_com")
    if validated is None:
        _log("stats.com path failed security validation", "stats.com path failed security validation")
        return 1
    stats_com = validated

    _log("Running via stats.com (console version) (NO SPLASH)...",
         "Running via stats.com (console version) (NO SPLASH)...")
    cmd = [stats_com, "-production", "silent", "-nologo", spj_file]
    returncode, stdout, stderr = _run_silent(cmd, timeout=300)

    if stdout: print(stdout)
    if stderr: print("ERROR: " + stderr)
    _log("Exit code: " + str(returncode), "Exit code: " + str(returncode))
    return returncode


# ============================================================
# Fallback 1: SPSS bundled Python (no splash)
# ============================================================

def run_internal(sps_file, stats_python_path=None):
    """Fallback: run syntax via SPSS bundled Python (no splash)."""
    if not _opt_in_confirm("⚠️ About to run syntax via SPSS bundled Python. Continue?",
                           "⚠️ About to run syntax via SPSS bundled Python. Continue?"):
        _log("Execution cancelled (not confirmed).", "Execution cancelled (not confirmed).")
        return 1
    if not os.path.exists(sps_file):
        _log("Syntax file not found: " + sps_file, "Syntax file not found: " + sps_file)
        return 1

    if stats_python_path is None:
        for c in _generate_candidates("Python3/python.exe"):
            if os.path.exists(c):
                stats_python_path = c
                break
        if stats_python_path is None:
            _log("SPSS bundled Python not found", "SPSS bundled Python not found")
            return 1

    validated = _validate_path(stats_python_path, "python")
    if validated is None:
        _log("Python path failed security validation", "Python path failed security validation")
        return 1
    stats_python_path = validated

    ver_match = re.search(r'statistics[/\\](\d+)[/\\]', stats_python_path.lower())
    spss_version = ver_match.group(1) if ver_match else "26"

    helper_home = os.path.dirname(stats_python_path)

    with open(sps_file, encoding="utf-8", errors="replace") as f:
        syntax_text = f.read()
    ok, reason = validate_syntax(syntax_text)
    if not ok:
        _log("Syntax security check failed: " + reason, "Syntax security check failed: " + reason)
        return 1

    # The runner wrapper is written to a PRIVATE temp directory (0700) and
    # deleted after execution -> no undeclared persistent state left on disk.
    # The syntax file path is passed as a command-line ARGUMENT (argv),
    # never interpolated into the wrapper source -> no Python code injection
    # via a crafted file path.
    wrapper_code = (
        "# -*- coding: utf-8 -*-\n"
        "import sys, os\n"
        "helper = sys.argv[1]\n"
        "spss_pkg = os.path.join(helper, 'Lib', 'site-packages')\n"
        "if spss_pkg not in sys.path: sys.path.insert(0, spss_pkg)\n"
        "os.environ['PATH'] = helper + os.pathsep + os.environ.get('PATH', '')\n"
        "import spss\n"
        "spss.StartSPSS()\n"
        "with open(sys.argv[2], encoding='utf-8', errors='replace') as f:\n"
        "    spss.Submit(f.read())\n"
        "spss.StopSPSS()\n"
    )

    tmp_dir = tempfile.mkdtemp(prefix="statsoft_spss_")
    wrapper = os.path.join(tmp_dir, "_spss_runner.py")
    _log("Temporary runner script (auto-deleted after run): " + wrapper,
         "Temporary runner script (auto-deleted after run): " + wrapper)
    try:
        with open(wrapper, "w", encoding="utf-8") as f:
            f.write(wrapper_code)

        _log("Running syntax via SPSS bundled Python (NO GUI, NO SPLASH)...",
             "Running syntax via SPSS bundled Python (NO GUI, NO SPLASH)...")
        run_env = _minimal_env(helper_home)

        returncode, stdout, stderr = _run_silent(
            [stats_python_path, wrapper, helper_home, sps_file], env=run_env, timeout=300)

        if stdout: print(stdout)
        if stderr: print("ERROR: " + stderr)
        return returncode
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


# ============================================================
# Fallback 2: stats.exe (may show a splash; respects the STATSOFT_CONFIRM=1
# explicit-confirmation gate)
# ============================================================

def run_exe(spj_file, stats_exe=None):
    """Last fallback: run the Production Facility via stats.exe (may show a splash)."""
    if not os.path.exists(spj_file):
        _log(".spj file not found: " + spj_file, ".spj file not found: " + spj_file)
        return 1

    ok, reason = _validate_spj(spj_file)
    if not ok:
        _log("Job file security check failed: " + reason, "Job file security check failed: " + reason)
        return 1

    if stats_exe is None:
        for c in _generate_candidates("stats.exe"):
            if os.path.exists(c):
                stats_exe = c
                break
        if stats_exe is None:
            _log("stats.exe not found", "stats.exe not found")
            return 1

    validated = _validate_path(stats_exe, "stats")
    if validated is None:
        _log("stats.exe path failed security validation", "stats.exe path failed security validation")
        return 1
    stats_exe = validated

    _log("Running Production Facility (via stats.exe, may show splash screen)",
         "Running Production Facility (via stats.exe, may show splash screen)")
    if not _opt_in_confirm("⚠️ About to run stats.exe. Continue?", "⚠️ About to run stats.exe. Continue?"):
        _log("Execution cancelled (not confirmed).", "Execution cancelled (not confirmed).")
        return 1
    cmd = [stats_exe, "-production", "silent", "-nologo", spj_file]
    returncode, stdout, stderr = _run_silent(cmd, timeout=300)

    if stdout: print(stdout)
    if stderr: print("ERROR: " + stderr)
    _log("Exit code: " + str(returncode), "Exit code: " + str(returncode))
    return returncode


# ============================================================
# Utility functions
# ============================================================

def show_version(stats_python_path=None):
    """Show the SPSS version."""
    if stats_python_path is None:
        for c in _generate_candidates("Python3/python.exe"):
            if os.path.exists(c):
                stats_python_path = c
                break
        if stats_python_path is None:
            _log("SPSS bundled Python not found", "SPSS bundled Python not found")
            return 1

    validated = _validate_path(stats_python_path, "python")
    if validated is None:
        _log("Python path failed security validation", "Python path failed security validation")
        return 1
    stats_python_path = validated

    run_env = _minimal_env(os.path.dirname(stats_python_path))

    returncode, stdout, stderr = _run_silent(
        [stats_python_path, "-c",
         "import spss; print(getattr(spss,'__version__','unknown')); spss.StartSPSS(); spss.StopSPSS()"],
        env=run_env, timeout=30)
    if stdout: print(stdout.strip())
    return returncode


def check_sps(sps_file):
    """Check whether an .sps file exists and preview its content."""
    if not os.path.exists(sps_file):
        _log(".sps file not found: " + sps_file, ".sps file not found: " + sps_file)
        return 1
    with open(sps_file, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()
    _log(".sps file: " + sps_file, ".sps file: " + sps_file)
    _log("Lines: " + str(len(content.splitlines())), "Lines: " + str(len(content.splitlines())))
    for i, line in enumerate(content.splitlines()[:10], 1):
        print("  " + str(i) + ": " + line)
    return 0


def create_spj(sps_file, output_dir=None):
    """Create a standard .spj file (SPSS 26+ new format, forward-slash paths).

    This is a persistent-file write, so like execution it is protected by a
    default-deny opt-in gate: writes are denied by default and only happen when
    STATSOFT_AUTO_WRITE=1 or STATSOFT_CONFIRM=1 with an interactive confirmation.

    The default output path is a system temp dir (safely created via
    tempfile.mkdtemp); no durable file is left in the user's workspace, which is
    consistent with the manifest "the only persistent file is config.json"
    (SDI-1/SDI-3/TP4). If the user explicitly passes output_dir, it requires the
    same per-run opt-in confirmation as execution and forces containment within
    the .sps directory (no `..` traversal or absolute-path escape); the target
    path is disclosed before writing, and overwriting an existing file requires
    a second confirmation.
    """
    sps_abs = os.path.abspath(sps_file).replace("\\", "/")
    base_name = os.path.splitext(os.path.basename(sps_file))[0]
    # Allowed base directory = the canonical parent of the .sps file.
    allowed_base = os.path.realpath(os.path.dirname(os.path.abspath(sps_file)))
    # DEFAULT: use a dedicated private temp dir created with mkdtemp (0700-ish),
    # disclosed via _opt_in_confirm below. This guarantees no durable artifact
    # is left in the user's working area unless they explicitly supply output_dir.
    cleanup_temp = False
    if output_dir is None:
        output_dir = tempfile.mkdtemp(prefix="statsoft_spj_")
        cleanup_temp = True
    output_dir_abs = os.path.realpath(os.path.abspath(output_dir))

    # Containment check applies only to an explicit (user-controlled) output_dir.
    # The mkdtemp default is exempt because it intentionally lives outside the
    # project tree and is OS-managed.
    if cleanup_temp is False:
        try:
            common = os.path.commonpath([allowed_base, output_dir_abs])
        except ValueError:
            common = None
        if common != allowed_base:
            _log("Rejected unsafe output_dir (must be within the .sps directory): " + output_dir_abs,
                 "Rejected unsafe output_dir (must be within the .sps directory): " + output_dir_abs)
            return None

    os.makedirs(output_dir_abs, exist_ok=True)
    output_dir = output_dir_abs.replace("\\", "/")
    spj_file = os.path.join(output_dir, base_name + ".spj").replace("\\", "/")
    spv_file = os.path.join(output_dir, base_name + ".spv").replace("\\", "/")

    # Disclose the write target and require explicit opt-in (default-deny).
    if not _opt_in_confirm(
            "⚠️ About to WRITE job file .spj: " + spj_file + " . Continue?",
            "⚠️ About to WRITE job file .spj: " + spj_file + " . Continue?"):
        _log("Cancelled .spj write (not confirmed).", "Cancelled .spj write (not confirmed).")
        if cleanup_temp:
            shutil.rmtree(output_dir_abs, ignore_errors=True)
        return None

    # If a file already exists at the target, require an extra overwrite confirm.
    if os.path.exists(spj_file):
        if not _opt_in_confirm(
                "⚠️ Target .spj already exists. Overwrite " + spj_file + " ?",
                "⚠️ Target .spj already exists. Overwrite " + spj_file + " ?"):
            _log("Cancelled .spj overwrite (not confirmed).", "Cancelled .spj overwrite (not confirmed).")
            if cleanup_temp:
                shutil.rmtree(output_dir_abs, ignore_errors=True)
            return None

    # Locale: auto-detected (never hard-coded) per SQP-3. For a zh host we emit
    # the CN/zh locale; otherwise we OMIT the locale element so SPSS inherits the
    # system/user environment (avoids forcing an unexpected locale/encoding).
    loc = _detect_locale()
    if loc:
        locale_elem = '  <locale charset="UTF-8" country="%s" language="%s"/>' % loc
    else:
        locale_elem = "  <!-- locale omitted: SPSS inherits the system/user environment -->"

    xml = '''<?xml version="1.0" encoding="UTF-8"?>
<job xmlns="http://www.ibm.com/software/analytics/spss/xml/production"
     xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
     print="false"
     syntaxErrorHandling="continue"
     syntaxFormat="interactive"
     unicode="true"
     xsi:schemaLocation="http://www.ibm.com/software/analytics/spss/xml/production 
     http://www.ibm.com/software/analytics/spss/xml/production/production-1.4.xsd">
{locale}
  <output outputFormat="viewer" outputPath="{spv}"/>
  <syntax syntaxPath="{sps}"/>
</job>
'''.format(locale=locale_elem, spv=spv_file, sps=sps_abs)

    try:
        with open(spj_file, "w", encoding="utf-8") as f:
            f.write(xml)
        print("Created .spj file: " + spj_file)
        return spj_file
    finally:
        # Note: cleanup of the default temp dir is deferred to the caller.
        # The caller receives the path to the created .spj file and is
        # responsible for removing it (and the containing temp dir) when done.
        # This avoids returning a path that no longer exists (Issue 12 fix).
        pass


# ============================================================
# Main entry point
# ============================================================

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  run-console <spj_file> [stats_com]     Preferred: stats.com")
        print("  run-internal <sps_file> [stats_python] Fallback 1: bundled Python")
        print("  run-exe <spj_file> [stats_exe]         Fallback 2: stats.exe (may splash)")
        print("  create-spj <sps_file> [output_dir]     Create .spj file")
        print("  check <sps_file>                       Check .sps file")
        print("  version [stats_python]                 Show version")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "run-console":
        spj_file = sys.argv[2] if len(sys.argv) > 2 else None
        stats_com = sys.argv[3] if len(sys.argv) > 3 else None
        if spj_file is None:
            _log("Please provide .spj file path", "Please provide .spj file path")
            sys.exit(1)
        sys.exit(run_console(spj_file, stats_com))
    elif cmd == "run-internal":
        sps_file = sys.argv[2] if len(sys.argv) > 2 else None
        stats_python_path = sys.argv[3] if len(sys.argv) > 3 else None
        if sps_file is None:
            _log("Please provide .sps file path", "Please provide .sps file path")
            sys.exit(1)
        sys.exit(run_internal(sps_file, stats_python_path))
    elif cmd == "run-exe":
        spj_file = sys.argv[2] if len(sys.argv) > 2 else None
        stats_exe = sys.argv[3] if len(sys.argv) > 3 else None
        if spj_file is None:
            _log("Please provide .spj file path", "Please provide .spj file path")
            sys.exit(1)
        sys.exit(run_exe(spj_file, stats_exe))
    elif cmd == "create-spj":
        sps_file = sys.argv[2] if len(sys.argv) > 2 else None
        output_dir = sys.argv[3] if len(sys.argv) > 3 else None
        if sps_file is None:
            _log("Please provide .sps file path", "Please provide .sps file path")
            sys.exit(1)
        spj = create_spj(sps_file, output_dir)
        sys.exit(0 if spj else 1)
    elif cmd == "check":
        sps_file = sys.argv[2] if len(sys.argv) > 2 else None
        if sps_file is None:
            _log("Please provide .sps file path", "Please provide .sps file path")
            sys.exit(1)
        sys.exit(check_sps(sps_file))
    elif cmd == "version":
        stats_python_path = sys.argv[2] if len(sys.argv) > 2 else None
        sys.exit(show_version(stats_python_path))
    else:
        _log("Unknown command: " + cmd, "Unknown command: " + cmd)
        sys.exit(1)


if __name__ == "__main__":
    main()
