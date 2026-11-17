#!/usr/bin/env python3
"""
statsoft-cmdstan.py — CmdStan CLI wrapper (cross-platform)

Usage:
    statsoft-cmdstan model <model.stan> <data.csv> [-o output_dir]
    statsoft-cmdstan install [-v <version>]
    statsoft-cmdstan info
"""
import argparse, json, os, re, shlex, shutil, subprocess, sys, tempfile

_ANSI_RE = re.compile(r'\x1b\[[0-9;]*[A-Za-z]|\x1b\][^\x07]*\x07|[\x00-\x08\x0b\x0c\x0e-\x1f]')


def _sanitize(text):
    """Strip ANSI escape sequences and other control characters from subprocess
    output before printing, to prevent terminal/log injection (OH1 fix)."""
    if not text:
        return text
    return _ANSI_RE.sub('', text)


def _safe_arg(value):
    """Safely encode a user-controlled value (e.g. a file path) for display.

    A malicious filename could embed terminal escape sequences, newlines, or
    log-forging characters. We first shell-quote the value (so spaces/special
    chars are visibly delimited), strip ANSI/control bytes, and finally collapse
    newlines/carriage-returns/tabs to spaces so echoing it to a terminal or log
    on a single line cannot inject or forge content (OH1 fix)."""
    s = _sanitize(shlex.quote(str(value)))
    return s.replace('\r', ' ').replace('\n', ' ').replace('\t', ' ')


def get_config():
    """Read config.json if available."""
    cfg_path = os.path.join(os.path.dirname(__file__), '..', '..', 'config.json')
    if os.path.exists(cfg_path):
        with open(cfg_path, 'r') as f:
            return json.load(f)
    return {}

def user_authorized_to_run():
    """EXPLICIT, NAMED opt-in before building/running an external Stan model.

    FAIL-CLOSED: returns False by default. Building/running a Stan model
    COMPILES and EXECUTES user-supplied, untrusted native code. Proceed ONLY
    when an explicit opt-in is present:
      * STATSOFT_CMDSTAN_RUN=1           -> dedicated, named opt-in for model runs.
      * STATSOFT_AUTO_WRITE=1            -> master override (agent/CI non-interactive).
      * STATSOFT_CONFIRM=1 AND a real TTY -> prompt y/N; only 'y' proceeds.
      * otherwise                        -> deny. An agent or upstream tool cannot
                                           trigger a build/run unexpectedly.
    Returns True only if the external build/run is explicitly authorized.
    """
    if os.environ.get("STATSOFT_CMDSTAN_RUN") == "1":
        return True
    if os.environ.get("STATSOFT_AUTO_WRITE") == "1":
        return True
    if os.environ.get("STATSOFT_CONFIRM") == "1" and sys.stdin.isatty():
        try:
            sys.stdout.write(
                "WARNING: this will COMPILE and RUN user-supplied Stan code as native "
                "binaries (untrusted native-code execution). Continue? (y/N) ")
            sys.stdout.flush()
            return sys.stdin.readline().strip().lower() in ("y", "yes")
        except Exception:
            return False
    return False


def _reveal():
    """Disclosure gate: install paths/versions/config snippets are shown ONLY
    when STATSOFT_REVEAL=1 is set. Default (unset) returns False so detection
    emits only a boolean installed/not-installed result (SDI-3)."""
    return os.environ.get("STATSOFT_REVEAL") == "1"


def _verify():
    """Verification gate: launching a third-party binary purely to obtain a
    version (e.g. stanc --version) requires STATSOFT_VERIFY=1. Default returns
    False so no external binary is executed for verification (SDI-3)."""
    return os.environ.get("STATSOFT_VERIFY") == "1"


def find_cmdstan():
    """Locate CmdStan installation."""
    # 1. Try config.json
    cfg = get_config()
    if "CmdStan" in cfg and os.path.exists(cfg["CmdStan"].get("path", "")):
        return cfg["CmdStan"]["path"]
    # 2. Env var
    for var in ("CMDSTAN", "CMDSTAN_PATH", "CmdStan_DIR"):
        val = os.environ.get(var)
        if val and os.path.isdir(val):
            return val
    # 3. Common paths
    home = os.path.expanduser("~")
    candidates = [
        os.path.join(home, ".cmdstanpy", "cmdstan"),
        os.path.join(home, ".cmdstan"),
        "/opt/cmdstan",
        os.environ.get("CONDA_PREFIX", "") and os.path.join(os.environ["CONDA_PREFIX"], "lib", "cmdstan"),
    ]
    for c in candidates:
        if c and os.path.isfile(os.path.join(c, "bin", "stanc")):
            return c
    return None

def cmdstan_info():
    """Show CmdStan environment info.

    Disclosure is gated: without STATSOFT_REVEAL=1 the command reports only
    whether CmdStan is present. Install path, stanc version, and make/local
    contents are revealed ONLY after explicit opt-in (SDI-3). The stanc
    --version binary launch is itself gated behind STATSOFT_VERIFY=1.
    """
    path = find_cmdstan()
    if not path:
        print("CmdStan not found")
        return
    if not _reveal():
        print("CmdStan found (details hidden; set STATSOFT_REVEAL=1 to reveal).")
        return
    print("=== CmdStan Environment ===")
    print(f"  Path: {path}")
    stanc = os.path.join(path, "bin", "stanc")
    if os.path.isfile(stanc):
        if _verify():
            ver = subprocess.run([stanc, "--version"], capture_output=True, text=True)
            print(f"  stanc: {_sanitize(ver.stdout.strip())[:60]}")
        else:
            print("  stanc: (version hidden; set STATSOFT_VERIFY=1 to query)")
    makefile = os.path.join(path, "make", "local")
    if os.path.isfile(makefile):
        with open(makefile) as f:
            lines = ["  " + l.strip() for l in f.readlines() if l.strip() and not l.startswith("#")]
            for l in lines[:5]:
                print(f"  {l}")

def run_model(model_file, data_file, output_dir=None):
    """Build and run a Stan model.

    SECURITY/DISCLOSURE: running a Stan model invokes `make` and the compiled
    model binary (THIRD-PARTY / UNTRUSTED native code execution; gated by
    user_authorized_to_run). The build runs `make -C <cmdstan_path> <model_target>`
    where model_target is the model file path WITHOUT its .stan suffix; CmdStan
    writes compiled artifacts (e.g. <model>/.exe/.o) NEXT TO THE MODEL SOURCE and
    updates make/local — this is inherent to CmdStan and occurs OUTSIDE the skill
    directory. Runtime sampling output is written to `output_dir` (default: a
    temporary directory that is cleaned up). Treat model execution as running
    UNTRUSTED native code supplied by the user.
    """
    path = find_cmdstan()
    if path is None:
        print("ERROR: CmdStan not found. Run setup_cmdstan.sh first.")
        sys.exit(1)

    # Check model file
    if not os.path.isfile(model_file):
        print(f"ERROR: Model file {model_file} not found.")
        sys.exit(1)

    # Explicit opt-in before executing external build/run processes
    if not user_authorized_to_run():
        print("Cancelled: model run not authorized. Set STATSOFT_CMDSTAN_RUN=1 "
              "(or STATSOFT_AUTO_WRITE=1), or run with STATSOFT_CONFIRM=1 in a TTY.")
        sys.exit(1)

    # Runtime outputs are confined to output_dir (temp by default, cleaned up).
    cleanup_output = False
    if not output_dir:
        output_dir = tempfile.mkdtemp(prefix="cmdstan_out_")
        cleanup_output = True
    os.makedirs(output_dir, exist_ok=True)
    print("[disclosure] CmdStan build writes compiled artifacts into the CmdStan "
          "tree next to the model (outside the skill dir, inherent to Stan).")
    print(f"[disclosure] Runtime sampling output -> {output_dir} "
          f"(cleaned up after run: {cleanup_output}).")

    # Build model — resolve to a real existing file and derive the make target
    # from its FULL path (not a basename joined to cwd), so a crafted/relative
    # model path cannot redirect the build elsewhere (AST4).
    model_file = os.path.abspath(model_file)
    if not os.path.isfile(model_file):
        print(f"ERROR: Model file {model_file} not found.")
        sys.exit(1)
    model_target = os.path.splitext(model_file)[0]
    print("WARNING: building & running a Stan model executes UNTRUSTED native code "
          "compiled from the user-supplied .stan file (artifacts land outside the "
          "skill directory, inherent to CmdStan).")
    print(f"Building model: {_safe_arg(model_file)}")
    build = subprocess.run([
        "make", "-C", path, model_target
    ], capture_output=True, text=True)
    if build.returncode != 0:
        print("Build failed:\n" + _sanitize(build.stderr))
        if cleanup_output:
            shutil.rmtree(output_dir, ignore_errors=True)
        sys.exit(1)

    # Run — execute the compiled binary (UNTRUSTED native code) next to the
    # model source, matching the build target (CmdStan behavior). Confine
    # runtime sampling output to the (temp/confined) output directory.
    run_bin = model_target + (".exe" if os.name == "nt" else "")
    if not os.path.isfile(run_bin):
        run_bin = model_target
    if not os.path.isfile(run_bin):
        print(f"ERROR: compiled model not found at {run_bin}")
        sys.exit(1)
    args = [run_bin, "sample", "num_samples=2000", "num_warmup=1000"]
    if data_file:
        args.append(f"data file={data_file}")
    args.append(f"output file={os.path.join(output_dir, 'output.csv')}")
    # Encode every argument safely before echoing the reconstructed command line,
    # so a crafted model_file/data_file cannot inject terminal/log content (OH1).
    print("Command: " + " ".join(_safe_arg(a) for a in args))

    try:
        proc = subprocess.run(args, capture_output=True, text=True)
    finally:
        if cleanup_output:
            shutil.rmtree(output_dir, ignore_errors=True)
    # Bound + sanitize subprocess output before relaying (OH1): truncate size
    # and keep trusted status messages separate from untrusted stdout/stderr.
    MAX_OUT = 8000
    print(_sanitize(proc.stdout)[:MAX_OUT])
    if proc.returncode != 0:
        print(_sanitize(proc.stderr)[:MAX_OUT], file=sys.stderr)
    sys.exit(proc.returncode)

def main():
    parser = argparse.ArgumentParser(prog="statsoft-cmdstan", description="CmdStan CLI wrapper")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("info", help="Show CmdStan environment")

    run_p = sub.add_parser("model", help="Build and run Stan model")
    run_p.add_argument("model", help="Stan model file (.stan)")
    run_p.add_argument("data", help="Data file (CSV)")
    run_p.add_argument("-o", "--output", help="Output directory")

    install_p = sub.add_parser("install", help="Install CmdStan (via cmdstanpy or installer)")
    install_p.add_argument("-v", "--version", help="CmdStan version")

    args = parser.parse_args()

    if args.command == "model":
        run_model(args.model, args.data, args.output)
    elif args.command == "info":
        cmdstan_info()
    elif args.command == "install":
        print("Install via:\n  bash install_cmdstan.sh")
        print("Or via cmdstanpy:\n  pip install cmdstanpy && python -c 'import cmdstanpy; cmdstanpy.install_cmdstan()'")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
