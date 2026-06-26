#!/usr/bin/env python3
"""Create a local scaffold for observing an untrusted binary without running it."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from textwrap import dedent


def write(path: Path, content: str, force: bool) -> None:
    if path.exists() and not force:
        raise SystemExit(f"{path} already exists; pass --force to overwrite")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dedent(content).lstrip(), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, help="Output directory for the scaffold")
    parser.add_argument("--sample-name", default="sample.bin", help="Expected artifact filename under ./artifact")
    parser.add_argument("--timeout", default="180", help="Observation timeout in seconds")
    parser.add_argument("--force", action="store_true", help="Overwrite existing scaffold files")
    args = parser.parse_args()

    out = Path(args.out).expanduser().resolve()
    sample_name = args.sample_name
    timeout = args.timeout

    for directory in ["artifact", "config", "logs", "mock-rpc"]:
        (out / directory).mkdir(parents=True, exist_ok=True)

    write(
        out / "Dockerfile",
        """
        FROM debian:bookworm-slim

        RUN apt-get update \\
          && apt-get install -y --no-install-recommends \\
            ca-certificates strace procps iproute2 lsof file binutils findutils jq tini python3 \\
          && rm -rf /var/lib/apt/lists/*

        RUN useradd -r -u 10001 sandbox
        USER sandbox
        WORKDIR /work
        ENTRYPOINT ["/usr/bin/tini", "--"]
        """,
        args.force,
    )

    base_service = {
        "build": ".",
        "user": "10001:10001",
        "working_dir": "/work/artifact",
        "read_only": True,
        "cap_drop": ["ALL"],
        "security_opt": ["no-new-privileges:true"],
        "pids_limit": 128,
        "mem_limit": "768m",
        "cpus": "1.0",
        "tmpfs": ["/tmp:rw,nosuid,nodev,noexec,size=128m"],
        "volumes": [
            "./artifact:/work/artifact:ro",
            "./config:/work/config:ro",
            "./logs:/logs:rw",
        ],
        "command": [
            "/usr/bin/timeout",
            timeout,
            "/usr/bin/strace",
            "-f",
            "-yy",
            "-s",
            "256",
            "-o",
            "/logs/strace.log",
            "/bin/false",
        ],
    }

    offline = {
        "services": {
            "sample": {
                **base_service,
                "network_mode": "none",
            }
        }
    }

    mock_network = {
        "services": {
            "rpc-mock": {
                "image": "python:3.12-slim",
                "working_dir": "/mock-rpc",
                "volumes": ["./mock-rpc:/mock-rpc:ro"],
                "command": ["python", "server.py"],
                "networks": ["sandbox_net"],
            },
            "sample": {
                **base_service,
                "networks": ["sandbox_net"],
            },
        },
        "networks": {"sandbox_net": {"internal": True}},
    }

    write(out / "compose.offline.json", json.dumps(offline, indent=2) + "\n", args.force)
    write(out / "compose.mock-rpc.json", json.dumps(mock_network, indent=2) + "\n", args.force)
    write(
        out / "mock-rpc" / "server.py",
        """
        from http.server import BaseHTTPRequestHandler, HTTPServer
        import json

        class Handler(BaseHTTPRequestHandler):
            def do_POST(self):
                length = int(self.headers.get("content-length", "0"))
                body = self.rfile.read(length).decode("utf-8", "replace")
                with open("/tmp/rpc-requests.log", "a", encoding="utf-8") as log:
                    log.write(body + "\\n")
                try:
                    request = json.loads(body)
                    method = request.get("method")
                    request_id = request.get("id")
                except Exception:
                    method = None
                    request_id = None
                result = {"context": {"slot": 1}, "value": None}
                if method == "getHealth":
                    result = "ok"
                elif method == "getLatestBlockhash":
                    result = {"context": {"slot": 1}, "value": {"blockhash": "11111111111111111111111111111111", "lastValidBlockHeight": 1}}
                response = {"jsonrpc": "2.0", "id": request_id, "result": result}
                data = json.dumps(response).encode()
                self.send_response(200)
                self.send_header("content-type", "application/json")
                self.send_header("content-length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)

        HTTPServer(("0.0.0.0", 8899), Handler).serve_forever()
        """,
        args.force,
    )
    write(
        out / "RUNBOOK.md",
        f"""
        # Sandbox Runbook

        Place the sample at `./artifact/{sample_name}` and record its SHA-256 before any run.

        The generated compose files deliberately run `/bin/false`. Replace only the final
        command element with the exact approved command when you are ready to observe.

        Offline tier:

        ```bash
        docker compose -f compose.offline.json build
        docker compose -f compose.offline.json run --rm sample
        ```

        Mock RPC tier:

        ```bash
        docker compose -f compose.mock-rpc.json build
        docker compose -f compose.mock-rpc.json up --abort-on-container-exit
        ```

        Keep logs under `./logs` and never mount real wallets or production secrets.
        """,
        args.force,
    )

    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
