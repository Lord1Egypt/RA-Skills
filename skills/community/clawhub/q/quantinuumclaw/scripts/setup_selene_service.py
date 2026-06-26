#!/usr/bin/env python3
"""
Guppy/Selene Quantum Skill - Setup Selene Service

This script scaffolds a new Selene backend service for a quantum application.
It generates the service structure, API endpoints, and integration with Guppy algorithms.

Usage:
    python3 setup_selene_service.py --app-name "quantum-optimizer" --use-case "portfolio-optimization"

Options:
    --app-name       Name of the quantum application (used in filenames, URLs)
    --use-case       Quantum use case: optimization, chemistry, ml, random, crypto, etc.
    --description    Brief description of the application
    --output-dir     Output directory (default: current directory)
"""

import argparse
import os
import sys
from pathlib import Path
from datetime import datetime

# Template for Selene service main.py
SELENE_MAIN_TEMPLATE = '''#!/usr/bin/env python3
"""
{app_name} - Selene Service
Quantum {use_case} application powered by Guppy
Generated: {timestamp}
"""

import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
import uvicorn
from typing import Dict, Any, List

# Import Guppy quantum runtime
try:
    import guppy as qp
    from guppy import *
    GUPPY_AVAILABLE = True
except ImportError:
    GUPPY_AVAILABLE = False
    print("Warning: Guppy not installed. Quantum functions will be mocked.")

app = FastAPI(
    title="{app_name}",
    description="{description}",
    version="1.0.0"
)

# CORS configuration - adjust for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Restrict to frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Quantum algorithm implementation
class Quantum{use_case_title}:
    def __init__(self):
        if GUPPY_AVAILABLE:
            # Initialize quantum hardware/emulator
            self.hw = None  # Configure based on Quantinuum hardware
            print("Quantum hardware initialized")
        else:
            print("Running in mock mode (Guppy not available)")

    def run_quantum_computation(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute quantum algorithm with provided parameters.

        Args:
            params: Dictionary of input parameters for the quantum circuit

        Returns:
            Dictionary with computation results
        """
        try:
            if GUPPY_AVAILABLE:
                # TODO: Implement actual Guppy quantum circuit
                # Example structure:
                # q = qp.quantum()
                # with q:
                #     # Build quantum circuit using Guppy syntax
                #     q.h(0)
                #     q.cx(0, 1)
                #     q.measure_all()
                # result = q.execute()
                pass
                result = {
                    "status": "success",
                    "result": "quantum_result_placeholder",
                    "confidence": 0.95,
                    "execution_time_ms": 1250
                }
            else:
                # Mock response for testing without quantum hardware
                result = {
                    "status": "success_mock",
                    "result": f"mock_quantum_result_for_{params}",
                    "confidence": 1.0,
                    "execution_time_ms": 0
                }
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Quantum computation failed: {{str(e)}}")

# Initialize quantum processor
quantum_processor = Quantum{use_case_title}()

# API Endpoints
@app.get("/health")
async def health_check():
    """Health check endpoint for Fly.io"""
    return {{
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "guppy_available": GUPPY_AVAILABLE
    }}

@app.post("/api/{use_case}/compute")
async def compute(params: Dict[str, Any]):
    """
    Main quantum computation endpoint.

    Example request body:
    {{
        "param1": "value1",
        "param2": 42,
        "shots": 1000
    }}

    Returns quantum computation results.
    """
    result = quantum_processor.run_quantum_computation(params)
    return {{
        "application": "{app_name}",
        "use_case": "{use_case}",
        "timestamp": datetime.utcnow().isoformat(),
        **result
    }}

@app.get("/api/info")
async def get_info():
    """Return service information and available endpoints"""
    return {{
        "service": "{app_name}",
        "description": "{description}",
        "version": "1.0.0",
        "quantum_backend": "Quantinuum" if GUPPY_AVAILABLE else "mock",
        "endpoints": [
            "GET /health",
            "POST /api/{use_case}/compute",
            "GET /api/info"
        ]
    }}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
'''

# Template for requirements.txt
REQUIREMENTS_TEMPLATE = '''fastapi==0.104.1
uvicorn[standard]==0.24.0
guppy==0.1.0  # TODO: Update to actual Guppy version
pydantic==2.5.0
python-dotenv==1.0.0
'''

# Template for fly.toml
FLYTOML_TEMPLATE = '''# Fly.io configuration for {app_name}
# Generated: {timestamp}

app = "{app_name}"
primary_region = "lhr"  # London - adjust as needed

[build]
  dockerfile = "Dockerfile"

[env]
  PORT = "8080"
  # QUANTUM_HARDWARE = "h2"  # Uncomment and configure as needed

[[http_services]]
  internal_port = 8080
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 0
  processes = ["app"]

  [[http_services.checks]]
    interval = "10s"
    timeout = "2s"
    method = "GET"
    path = "/health"

  [[http_services.checks]]
    interval = "30s"
    timeout = "2s"
    method = "GET"
    path = "/api/info"
'''

# Template for Dockerfile
DOCKERFILE_TEMPLATE = '''# Dockerfile for {app_name} Selene service
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8080

# Run the service
CMD ["python", "main.py"]
'''

# Template for .env.example
ENV_EXAMPLE_TEMPLATE = '''# Environment variables for {app_name}
# Copy this file to .env and fill in values

# Quantinuum quantum hardware credentials (if using real hardware)
# QUANTUM_HARDWARE=h2  # or other hardware identifier
# QUANTUM_API_KEY=your_quantinuum_api_key

# Fly.io will set PORT automatically
'''

def create_selene_service(app_name, use_case, description, output_dir):
    """Create a complete Selene service project structure"""

    # Create output directory
    project_dir = Path(output_dir) / app_name
    project_dir.mkdir(parents=True, exist_ok=True)

    print(f"Creating Selene service: {project_dir}")

    # Convert use_case to title case for class names
    use_case_title = use_case.replace("-", " ").title().replace(" ", "")

    # Generate files
    timestamp = datetime.utcnow().isoformat()

    # main.py
    main_content = SELENE_MAIN_TEMPLATE.format(
        app_name=app_name,
        use_case=use_case,
        use_case_title=use_case_title,
        description=description,
        timestamp=timestamp
    )
    (project_dir / "main.py").write_text(main_content)
    print("  ✓ Created main.py")

    # requirements.txt
    (project_dir / "requirements.txt").write_text(REQUIREMENTS_TEMPLATE.format(
        app_name=app_name,
        use_case=use_case
    ))
    print("  ✓ Created requirements.txt")

    # fly.toml
    (project_dir / "fly.toml").write_text(FLYTOML_TEMPLATE.format(
        app_name=app_name,
        use_case=use_case,
        timestamp=timestamp
    ))
    print("  ✓ Created fly.toml")

    # Dockerfile
    (project_dir / "Dockerfile").write_text(DOCKERFILE_TEMPLATE.format(
        app_name=app_name,
        use_case=use_case,
        timestamp=timestamp
    ))
    print("  ✓ Created Dockerfile")

    # .env.example
    (project_dir / ".env.example").write_text(ENV_EXAMPLE_TEMPLATE.format(
        app_name=app_name,
        use_case=use_case
    ))
    print("  ✓ Created .env.example")

    # README.md with instructions
    readme_content = f'''# {app_name}

{description}

## Quantum Use Case
{use_case}

## Local Development

1. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\\\Scripts\\\\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment:
   ```bash
   cp .env.example .env
   # Edit .env with your quantum credentials if needed
   ```

4. Run locally:
   ```bash
   python main.py
   ```

   Service will be available at http://localhost:8080

## API Endpoints

- `GET /health` - Health check
- `POST /api/{use_case}/compute` - Execute quantum algorithm
- `GET /api/info` - Service information

## Deploy to Fly.io

1. Install Fly CLI: https://fly.io/docs/hands-on/install-flyctl/

2. Login: `fly auth login`

3. Launch app: `fly launch --now`

4. Set secrets (if needed): `fly secrets set QUANTUM_API_KEY=your_key`

5. Open: `fly open`

## Quantum Algorithm Implementation

The quantum algorithm is in `main.py` in the `Quantum{use_case_title}` class.
Currently it runs in mock mode if Guppy is not installed. To use real quantum hardware:

1. Install Guppy: `pip install guppy`
2. Configure quantum hardware in the `__init__` method
3. Implement the actual Guppy quantum circuit in `run_quantum_computation()`

See `../references/guppy_guide.md` for Guppy syntax and examples.
'''
    (project_dir / "README.md").write_text(readme_content)
    print("  ✓ Created README.md")

    # .gitignore
    gitignore_content = '''__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv/
.env
*.log
.DS_Store
'''
    (project_dir / ".gitignore").write_text(gitignore_content)
    print("  ✓ Created .gitignore")

    print(f"\n✅ Selene service created at: {project_dir}")
    print(f"\nNext steps:")
    print(f"1. cd {project_dir}")
    print(f"2. Install dependencies and configure .env")
    print(f"3. Implement actual Guppy algorithm in main.py")
    print(f"4. Test locally: python main.py")
    print(f"5. Deploy: fly launch --now")

    return project_dir

def main():
    parser = argparse.ArgumentParser(description="Setup Selene quantum service")
    parser.add_argument("--app-name", required=True, help="Application name")
    parser.add_argument("--use-case", required=True, help="Quantum use case (optimization, chemistry, ml, etc.)")
    parser.add_argument("--description", default="Quantum computing web service", help="Brief description")
    parser.add_argument("--output-dir", default=".", help="Output directory (default: current)")

    args = parser.parse_args()

    try:
        create_selene_service(args.app_name, args.use_case, args.description, args.output_dir)
        print("\n✅ Setup complete!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
