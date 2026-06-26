#!/usr/bin/env python3
"""
Guppy/Selene Quantum Skill - Fly.io Deployment

This script automates deployment of Selene quantum services to Fly.io.
It handles: app creation, configuration, secrets, build, and launch.

Usage:
    python3 flyio_deploy.py --app-name "quantum-optimizer" --region "lhr" --org "personal"

Options:
    --app-name       Name of the Fly.io app (must be unique globally)
    --service-dir    Path to Selene service directory (default: ./<app-name>)
    --region         Fly.io region (default: lhr - London)
    --org            Fly.io organization (default: personal)
    --setup-only     Only create app and configure, don't build/deploy
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path

def run_command(cmd, cwd=None, capture_output=False):
    """Run a shell command and return result"""
    print(f"$ {' '.join(cmd)}")
    result = subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=capture_output,
        text=True
    )
    if result.returncode != 0:
        print(f"❌ Command failed with exit code {result.returncode}")
        if result.stderr:
            print(f"Error: {result.stderr}")
        raise RuntimeError(f"Command failed: {' '.join(cmd)}")
    if capture_output:
        return result.stdout.strip()
    return None

def check_flyctl_installed():
    """Check if flyctl is installed and authenticated"""
    try:
        result = subprocess.run(["fly", "--version"], capture_output=True, text=True)
        print(f"✅ flyctl version: {result.stdout.strip()}")
    except FileNotFoundError:
        print("❌ flyctl not found. Install from: https://fly.io/docs/hands-on/install-flyctl/")
        sys.exit(1)

    # Check authentication
    try:
        run_command(["fly", "auth", "whoami"])
        print("✅ flyctl authenticated")
    except:
        print("❌ Not authenticated. Run: fly auth login")
        sys.exit(1)

def create_fly_app(app_name, region, org):
    """Create a new Fly.io app"""
    print(f"\n🚀 Creating Fly.io app: {app_name}")

    # Check if app already exists
    try:
        result = run_command(["fly", "apps", "list"], capture_output=True)
        if app_name in result:
            print(f"⚠️  App '{app_name}' already exists. Skipping creation.")
            return
    except:
        pass  # If list fails, we'll try to create anyway

    cmd = ["fly", "apps", "create", app_name, "--region", region, "--org", org]
    run_command(cmd)
    print(f"✅ App created")

def configure_secrets(app_name, env_file_path):
    """Set secrets on Fly.io from .env file"""
    print(f"\n🔐 Configuring secrets for {app_name}")

    if not env_file_path.exists():
        print(f"⚠️  .env file not found at {env_file_path}. Skipping secrets.")
        return

    # Read .env file
    secrets = {}
    for line in env_file_path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            secrets[key.strip()] = value.strip()

    # Set secrets on Fly.io
    for key, value in secrets.items():
        if value and not value.startswith("your_"):  # Skip placeholder values
            cmd = ["fly", "secrets", "set", f"{key}={value}", "--app", app_name]
            run_command(cmd)
            print(f"  ✓ Set secret: {key}")

    print(f"✅ Secrets configured")

def deploy_app(app_name, service_dir):
    """Deploy the app to Fly.io"""
    print(f"\n📦 Deploying {app_name} to Fly.io...")

    cmd = ["fly", "deploy", "--app", app_name]
    run_command(cmd, cwd=service_dir)
    print(f"✅ Deployed successfully")

def open_app(app_name):
    """Open the deployed app in browser"""
    print(f"\n🌐 Opening {app_name}...")
    cmd = ["fly", "open", "--app", app_name]
    run_command(cmd)
    print(f"✅ App is live!")

def show_status(app_name):
    """Show app status and logs"""
    print(f"\n📊 Status for {app_name}:")
    print("\n--- App Info ---")
    run_command(["fly", "apps", "show", app_name])

    print("\n--- Recent Logs ---")
    try:
        run_command(["fly", "logs", "--app", app_name, "--tail=50"])
    except:
        print("(No logs available yet)")

def main():
    parser = argparse.ArgumentParser(description="Deploy Selene service to Fly.io")
    parser.add_argument("--app-name", required=True, help="Fly.io app name (globally unique)")
    parser.add_argument("--service-dir", help="Path to Selene service directory (default: ./<app-name>)")
    parser.add_argument("--region", default="lhr", help="Fly.io region (default: lhr - London)")
    parser.add_argument("--org", default="personal", help="Fly.io organization (default: personal)")
    parser.add_argument("--setup-only", action="store_true", help="Only create app and configure, skip build/deploy")
    parser.add_argument("--skip-secrets", action="store_true", help="Skip secret configuration")

    args = parser.parse_args()

    # Determine service directory
    if args.service_dir:
        service_dir = Path(args.service_dir).resolve()
    else:
        service_dir = Path.cwd() / args.app_name

    if not service_dir.exists():
        print(f"❌ Service directory not found: {service_dir}")
        print("   Use --service-dir to specify the correct path")
        sys.exit(1)

    # Check for main.py
    if not (service_dir / "main.py").exists():
        print(f"❌ main.py not found in {service_dir}")
        print("   Ensure this is a valid Selene service directory")
        sys.exit(1)

    try:
        # Step 1: Check flyctl
        check_flyctl_installed()

        # Step 2: Create app
        create_fly_app(args.app_name, args.region, args.org)

        # Step 3: Configure secrets
        if not args.skip_secrets:
            env_file = service_dir / ".env"
            if not env_file.exists():
                env_file = service_dir / ".env.example"
                print(f"⚠️  .env not found, using .env.example as reference")
            configure_secrets(args.app_name, env_file)

        # Step 4: Deploy (unless setup-only)
        if not args.setup_only:
            deploy_app(args.app_name, service_dir)
            open_app(args.app_name)
            show_status(args.app_name)
        else:
            print(f"\n✅ Setup complete. App '{args.app_name}' is configured but not deployed.")
            print(f"   To deploy manually: cd {service_dir} && fly deploy")

        print(f"\n🎉 Fly.io deployment prepared for {args.app_name}!")

    except Exception as e:
        print(f"\n❌ Deployment failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
