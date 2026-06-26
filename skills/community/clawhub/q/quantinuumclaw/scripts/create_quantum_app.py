#!/usr/bin/env python3
"""
Guppy/Selene Quantum Skill - Complete Quantum Application Creator

This script orchestrates the full workflow of creating a quantum application:
1. Creates Selene backend service with Guppy algorithm
2. Deploys backend to Fly.io
3. Creates Lovable frontend connected to backend
4. Provides deployment instructions

Usage:
    python3 create_quantum_app.py --app-name "quantum-optimizer" --use-case "portfolio-optimization"

Options:
    --app-name       Name of the quantum application (used for backend and frontend)
    --use-case       Quantum compute use case: optimization, chemistry, ml, random, crypto, etc.
    --description    Brief description of the application
    --region         Fly.io region (default: lhr)
    --org            Fly.io organization (default: personal)
    --deploy         Skip Fly.io deployment if not specified
    --skip-frontend  Skip Lovable frontend creation
"""

import argparse
import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime

def run_script(script_path, args_dict):
    """Run another Python script from this skill"""
    cmd = ["python3", str(script_path)] + [f"--{k}" for k, v in args_dict.items() if v]
    print(f"\n$ {' '.join(cmd)}")
    result = subprocess.run(cmd)
    if result.returncode != 0:
        raise RuntimeError(f"Script failed: {script_path}")

def create_quantum_app(app_name, use_case, description, region, org, deploy, skip_frontend):
    """Orchestrate full quantum application creation"""

    print("="*60)
    print("🚀 QUANTUM APPLICATION CREATOR")
    print("="*60)
    print(f"App Name: {app_name}")
    print(f"Use Case: {use_case}")
    print(f"Description: {description}")
    print(f"Region: {region}")
    print(f"Organization: {org}")
    print(f"Deploy to Fly.io: {'Yes' if deploy else 'No'}")
    print(f"Create frontend: {'No' if skip_frontend else 'Yes'}")
    print("="*60)

    base_dir = Path.cwd()
    skill_dir = Path(__file__).parent.parent

    # Step 1: Create Selene backend
    print("\n🔧 Step 1: Creating Selene backend service...")
    setup_script = skill_dir / "scripts" / "setup_selene_service.py"
    backend_args = {
        "app-name": app_name,
        "use-case": use_case,
        "description": description,
        "output-dir": str(base_dir)
    }
    run_script(setup_script, backend_args)

    backend_dir = base_dir / app_name

    # Step 2: Deploy to Fly.io (if requested)
    if deploy:
        print("\n☁️  Step 2: Deploying to Fly.io...")
        deploy_script = skill_dir / "scripts" / "flyio_deploy.py"
        deploy_args = {
            "app-name": app_name,
            "service-dir": str(backend_dir),
            "region": region,
            "org": org
        }
        run_script(deploy_script, deploy_args)
        backend_url = f"https://{app_name}.fly.dev"
    else:
        backend_url = f"http://localhost:8080"
        print(f"\n⚠️  Skipping Fly.io deployment.")
        print(f"   Backend will run locally at {backend_url}")

    # Step 3: Create Lovable frontend (if not skipped)
    if not skip_frontend:
        print("\n🎨 Step 3: Creating Lovable frontend...")
        frontend_script = skill_dir / "scripts" / "lovable_integrate.py"
        frontend_args = {
            "app-name": app_name,
            "backend-url": backend_url,
            "quantum-use-case": use_case,
            "output-dir": str(base_dir)
        }
        run_script(frontend_script, frontend_args)
        frontend_dir = base_dir / f"{app_name}-frontend"
    else:
        frontend_dir = None
        print("\n⚠️  Skipping frontend creation.")

    # Summary
    print("\n" + "="*60)
    print("✅ QUANTUM APPLICATION CREATED")
    print("="*60)
    print(f"\nBackend: {backend_dir}")
    print(f"  • main.py - Selene service with Guppy integration")
    print(f"  • fly.toml - Fly.io configuration")
    print(f"  • Dockerfile - Container definition")
    print(f"  • Backend URL: {backend_url}")

    if frontend_dir:
        print(f"\nFrontend: {frontend_dir}")
        print(f"  • Lovable React + TypeScript project")
        print(f"  • QuantumDashboard component for results")
        print(f"  • Configured to connect to {backend_url}")
        print(f"\nTo run frontend locally:")
        print(f"  cd {frontend_dir} && npm install && npm run dev")

    print("\n📋 NEXT STEPS:")
    if deploy:
        print(f"1. Backend is live at {backend_url}")
        print(f"   Test: curl {backend_url}/health")
    else:
        print(f"1. Start backend: cd {backend_dir} && python main.py")
        print(f"   Test: curl {backend_url}/health")

    if frontend_dir:
        print(f"2. Start frontend: cd {frontend_dir} && npm install && npm run dev")
        print(f"   Open: http://localhost:5173")

    print("\n3. Implement your actual Guppy quantum algorithm:")
    print(f"   Edit {backend_dir}/main.py → Quantum{use_case.title()} class")
    print("   Replace mock implementation with real quantum circuit")

    print("\n4. Test quantum endpoint:")
    print(f"   curl -X POST {backend_url}/api/{use_case}/compute -H 'Content-Type: application/json' -d '{{}}'")

    print("\n5. Deploy frontend to Lovable when ready:")
    print("   - Import project into Lovable")
    print("   - Set VITE_API_URL environment variable")
    print("   - Deploy to Lovable hosting")

    print("\n📚 REFERENCES:")
    print("   • Guppy guide: ../references/guppy_guide.md")
    print("   • Selene API: ../references/selene_api.md")
    print("   • Fly.io config: ../references/flyio_config.md")
    print("   • Lovable patterns: ../references/lovable_patterns.md")

    print("\n🎉 Your quantum application is ready!")
    print("="*60)

def main():
    parser = argparse.ArgumentParser(description="Create complete quantum application stack")
    parser.add_argument("--app-name", required=True, help="Application name (e.g., quantum-optimizer)")
    parser.add_argument("--use-case", required=True, help="Quantum use case (optimization, chemistry, ml, random, crypto)")
    parser.add_argument("--description", default="Quantum computing web application", help="Brief description")
    parser.add_argument("--region", default="lhr", help="Fly.io region (default: lhr - London)")
    parser.add_argument("--org", default="personal", help="Fly.io organization (default: personal)")
    parser.add_argument("--deploy", action="store_true", help="Deploy to Fly.io automatically")
    parser.add_argument("--skip-frontend", action="store_true", help="Skip Lovable frontend creation")

    args = parser.parse_args()

    try:
        create_quantum_app(
            args.app_name,
            args.use_case,
            args.description,
            args.region,
            args.org,
            args.deploy,
            args.skip_frontend
        )
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Failed to create quantum application: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
