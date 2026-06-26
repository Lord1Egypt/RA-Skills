# Docker Setup Reference

Read this file if Phase 0 confirmed you are inside a Docker container.

## Why Docker Is Different

Docker containers run without a real display and with restricted Linux
capabilities. Chromium needs special flags and system libraries that are
not present in most base images. Without the correct setup it will crash
immediately with errors like:

- `No usable sandbox!`
- `Failed to connect to the bus`
- `Exited with code 127`
- `error while loading shared libraries`

## Required Launch Flags (ALWAYS use all 5)

```python
DOCKER_ARGS = [
    "--no-sandbox",            # disables Chrome sandbox (not needed inside Docker)
    "--disable-dev-shm-usage", # use /tmp instead of /dev/shm (prevents OOM crashes)
    "--disable-gpu",           # no GPU available in container
    "--disable-setuid-sandbox",# required when running as root
    "--single-process",        # more stable in memory-constrained containers
]
```

Never omit these. Always pass them to `p.chromium.launch(args=DOCKER_ARGS)`.

## Install Paths by Base Image

### Ubuntu / Debian (most common)
```bash
apt-get update -qq
apt-get install -y python3-pip curl wget -qq
pip3 install playwright
python3 -m playwright install chromium
python3 -m playwright install-deps chromium
```

### Alpine Linux
Alpine uses musl libc which is incompatible with Playwright's bundled Chromium.
Use the system Chromium instead:

```bash
apk add --no-cache \
    chromium nss freetype harfbuzz \
    ca-certificates ttf-freefont \
    python3 py3-pip

pip3 install playwright

# Point Playwright to system Chromium
export PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH=$(which chromium-browser || which chromium)
python3 -m playwright install chromium
```

### Node.js based image (no Python)
```bash
npx playwright install chromium
```
Then use the Node.js Playwright API instead of Python.

## Common Errors and Fixes

| Error | Fix |
|---|---|
| `No usable sandbox` | Add `--no-sandbox` and `--disable-setuid-sandbox` |
| `/dev/shm` crash | Add `--disable-dev-shm-usage` |
| `libXss.so.1 not found` | Run `python3 -m playwright install-deps chromium` |
| `Running as root without --no-sandbox is not supported` | Add `--no-sandbox` |
| `Timeout waiting for browser` | Add `--single-process`, reduce concurrency |
| `error: externally-managed-environment` (pip) | Use `pip3 install --break-system-packages playwright` |

## Memory Considerations

Chromium uses significant memory. In constrained containers:
- Minimum recommended: 512MB RAM
- Recommended: 1GB+ RAM
- Check with: `free -h`
- If memory is very low, close browser between test phases

## Checking Available Memory Before Launch

```python
import subprocess
result = subprocess.run(['free', '-m'], capture_output=True, text=True)
print(result.stdout)
# If available memory < 300MB, warn the user before launching
```
