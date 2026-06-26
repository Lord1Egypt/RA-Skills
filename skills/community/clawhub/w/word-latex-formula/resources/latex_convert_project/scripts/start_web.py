from __future__ import annotations

import argparse
import subprocess
import sys
import time
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description="Start the quick Word formula conversion Web UI.")
    parser.add_argument("--api-port", type=int, default=8000)
    parser.add_argument("--web-port", type=int, default=5173)
    args = parser.parse_args()

    api_cmd = [
        sys.executable,
        "-m",
        "uvicorn",
        "services.api.app.main:app",
        "--host",
        "127.0.0.1",
        "--port",
        str(args.api_port),
    ]
    npm = shutil.which("npm.cmd") or shutil.which("npm")
    if npm is None:
        print("npm was not found. Please install Node.js and run `npm install` in apps/web first.", file=sys.stderr)
        return 2
    web_cmd = [npm, "run", "dev", "--", "--host", "127.0.0.1", "--port", str(args.web_port)]

    print(f"API: http://127.0.0.1:{args.api_port}/api/health")
    print(f"Web: http://127.0.0.1:{args.web_port}")
    print("Press Ctrl+C to stop both processes.")

    api = subprocess.Popen(api_cmd, cwd=ROOT)
    web = subprocess.Popen(web_cmd, cwd=ROOT / "apps" / "web")
    try:
        while True:
            api_code = api.poll()
            web_code = web.poll()
            if api_code is not None:
                return api_code
            if web_code is not None:
                return web_code
            time.sleep(0.5)
    except KeyboardInterrupt:
        return 0
    finally:
        for process in (web, api):
            if process.poll() is None:
                process.terminate()
        for process in (web, api):
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()


if __name__ == "__main__":
    raise SystemExit(main())
