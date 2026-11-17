# Setup

## Run the MCP server

```bash
export REA_BRIDGE_TOKEN="$(openssl rand -hex 32)"
docker run -d --name rea \
  -e REA_BRIDGE_TOKEN \
  -p 127.0.0.1:8080:8080 \
  --read-only \
  --tmpfs /tmp:rw,nosuid,size=4g \
  --tmpfs /home/rea:rw,nosuid,size=256m \
  --cap-drop ALL \
  --security-opt no-new-privileges \
  -v "$PWD/targets:/work:ro" \
  psyb0t/reverse-engineer-anything:latest
```

- The bridge refuses to start without a token of at least 32 characters, and
  every request must send `Authorization: Bearer <token>`.
- Publish the port on `127.0.0.1` unless a reverse proxy with TLS sits in
  front. Behind a proxy, add its hostname to `REA_BRIDGE_ALLOWED_HOSTS`.
- `/tmp` needs room: JADX and Apktool work on private copies of each APK there.
  It cannot be `noexec`, because the JVM loads native libraries from it.
- Health: `GET /healthz` (no token) returns `{"status":"ok","sessions":N}`.

## Opt-in tools

Native decompilation needs Ghidra, which the image installs on demand. Add
`-e REA_INSTALL=ghidra -v rea-tools:/opt/rea-tools` to the run command. The
first start downloads Ghidra 12.1.4 (570 MB) from its official GitHub release,
checks it against the SHA-256 pinned in the image and unpacks it into the
volume; later starts reuse it. The first start needs network access and, with
a read-only root, the volume. On arm64 the install refuses, because Ghidra's
official release has no arm64 decompiler. To use your own Ghidra instead, mount
it and set `GHIDRA_INSTALL_DIR`, which takes precedence.

For a native library inside an APK, pull it out with `extract_artifact` (or
mount it alongside the APK), then `open_binary` it and use the function tools.

## Connect a client

Claude Code:

```bash
claude mcp add --transport http rea http://localhost:8080/mcp \
  --header "Authorization: Bearer $REA_BRIDGE_TOKEN"
```

Any client that speaks Streamable HTTP takes the same URL and header. For a
stdio-only client, run REA's own stdio server instead, with no bridge and no
token:

```json
{
  "mcpServers": {
    "rea": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "--read-only",
        "--tmpfs",
        "/tmp:rw,nosuid,size=4g",
        "--tmpfs",
        "/home/rea:rw,nosuid,size=256m",
        "--cap-drop",
        "ALL",
        "--security-opt",
        "no-new-privileges",
        "-v",
        "/absolute/path/to/targets:/work:ro",
        "psyb0t/reverse-engineer-anything:latest",
        "mcp"
      ]
    }
  }
}
```

## Bridge environment

| Variable                          | Default                     | Description                                                          |
| --------------------------------- | --------------------------- | -------------------------------------------------------------------- |
| `REA_BRIDGE_TOKEN`                | required                    | Bearer token, at least 32 characters. Never passed to REA.           |
| `REA_BRIDGE_PORT`                 | `8080`                      | Listen port inside the container.                                    |
| `REA_BRIDGE_HOST`                 | `0.0.0.0`                   | Listen address inside the container.                                 |
| `REA_BRIDGE_PATH`                 | `/mcp`                      | MCP endpoint path.                                                   |
| `REA_BRIDGE_ALLOWED_HOSTS`        | `localhost,127.0.0.1,[::1]` | Accepted `Host` header names (DNS rebinding guard). `*` disables it. |
| `REA_BRIDGE_MAX_SESSIONS`         | `4`                         | Concurrent MCP sessions, each with its own REA process.              |
| `REA_BRIDGE_IDLE_TIMEOUT_SECONDS` | `1800`                      | Idle sessions are closed and their REA process stopped.              |
| `REA_BRIDGE_MAX_BODY_BYTES`       | `4194304`                   | Largest accepted request body.                                       |
| `REA_BRIDGE_LOG_LEVEL`            | `info`                      | `debug`, `info`, `warn` or `error`.                                  |
| `REA_INSTALL`                     | unset                       | Comma-separated opt-in tools to install on start (`ghidra`).         |
| `REA_TOOLS_DIR`                   | `/opt/rea-tools`            | Install location for opt-in tools; mount a volume here.              |

REA's own variables pass through unchanged, for example `REA_JADX_HEAP_MIB`,
`REA_JADX_OPERATION_TIMEOUT_MS`, `REA_LOG_LEVEL` and
`REA_MCP_MAX_RESPONSE_BYTES`. The image presets `REA_JADX_MCP_JAR`,
`REA_APKTOOL_COMMAND`, `REA_ADB_PATH` and `JAVA_HOME`.

## Android devices

adb runs inside the container. Reach a device over the network with the
container on a network that can see it (`--network` for the CLI wrapper), then
connect from a tool call or `adb connect HOST:PORT`. USB passthrough needs the
device node passed with `--device`; prefer network adb.

## Troubleshooting

- `401`: the token is missing or wrong. `403`: the `Host` header is not in
  `REA_BRIDGE_ALLOWED_HOSTS`. `503`: every session slot is busy.
- A file is not found: pass the container path (`/work/app.apk`), not the host
  path.
- Large APKs time out: raise `REA_JADX_HEAP_MIB` and
  `REA_JADX_OPERATION_TIMEOUT_MS`, and give the container more memory.
