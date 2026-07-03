#!/usr/bin/env python3
"""
statsoft-cmdstan.py — CmdStan CLI wrapper (cross-platform)

Usage:
    statsoft-cmdstan model <model.stan> <data.csv> [-o output_dir]
    statsoft-cmdstan install [-v <version>]
    statsoft-cmdstan info
"""
import argparse, json, os, subprocess, sys

def get_config():
    """Read config.json if available."""
    cfg_path = os.path.join(os.path.dirname(__file__), '..', '..', 'config.json')
    if os.path.exists(cfg_path):
        with open(cfg_path, 'r') as f:
            return json.load(f)
    return {}

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
    """Show CmdStan environment info."""
    path = find_cmdstan()
    print("=== CmdStan Environment ===" if path else "CmdStan not found")
    if path:
        print(f"  Path: {path}")
        stanc = os.path.join(path, "bin", "stanc")
        if os.path.isfile(stanc):
            ver = subprocess.run([stanc, "--version"], capture_output=True, text=True)
            print(f"  stanc: {ver.stdout.strip()[:60]}")
        makefile = os.path.join(path, "make", "local")
        if os.path.isfile(makefile):
            with open(makefile) as f:
                lines = ["  " + l.strip() for l in f.readlines() if l.strip() and not l.startswith("#")]
                for l in lines[:5]:
                    print(f"  {l}")

def run_model(model_file, data_file, output_dir=None):
    """Build and run a Stan model."""
    path = find_cmdstan()
    if path is None:
        print("ERROR: CmdStan not found. Run setup_cmdstan.sh first.")
        sys.exit(1)

    # Check model file
    if not os.path.isfile(model_file):
        print(f"ERROR: Model file {model_file} not found.")
        sys.exit(1)

    # Build model
    print(f"Building model: {model_file}")
    build = subprocess.run([
        "make", "-C", path, os.path.join(os.getcwd(), os.path.basename(model_file)).replace(".stan", "")
    ], capture_output=True, text=True)
    if build.returncode != 0:
        print(f"Build failed:\n{build.stderr}")
        sys.exit(1)

    # Run
    print(f"Running model with data: {data_file}")
    args = [os.path.join(path, "bin", os.path.basename(model_file).replace(".stan", ""))]
    args += ["sample", f"num_samples=2000", f"num_warmup=1000"]
    if data_file:
        args.append(f"data file={data_file}")
    print(f"Command: {' '.join(args)}")

    proc = subprocess.run(args, capture_output=True, text=True)
    print(proc.stdout)
    if proc.returncode != 0:
        print(proc.stderr, file=sys.stderr)
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
