# Linux server + VNC setup (one-time)

All paths: `{baseDir}/scripts/`.

## 1. Install Google Chrome (RHEL / Fedora example)

Version must match the chromedriver you install. Example **148.0.7778.215**:

```bash
sudo dnf install -y \
  https://dl.google.com/linux/chrome/rpm/stable/x86_64/google-chrome-stable-148.0.7778.215-1.x86_64.rpm

google-chrome-stable --version
```

## 2. Install chromedriver (same version)

**Automatic** (reads version from `google-chrome-stable`; **no sudo** — installs to `~/.local/bin`):

```bash
bash {baseDir}/scripts/install_chromedriver.sh
```

Creates `{baseDir}/scripts/chromedriver.env`; `zhihu_publish.sh` loads it automatically.

**System-wide** (optional):

```bash
sudo env CHROMEDRIVER_INSTALL_DIR=/usr/local/bin bash {baseDir}/scripts/install_chromedriver.sh
```

**Manual** (user dir, example **147.0.7727.55**):

```bash
mkdir -p ~/.local/bin
wget https://storage.googleapis.com/chrome-for-testing-public/147.0.7727.55/linux64/chromedriver-linux64.zip
unzip -o chromedriver-linux64.zip
mv -f chromedriver-linux64/chromedriver ~/.local/bin/
chmod +x ~/.local/bin/chromedriver
export CHROMEDRIVER_PATH=$HOME/.local/bin/chromedriver
```

Verify match:

```bash
bash {baseDir}/scripts/verify_chrome_stack.sh
```

## 3. Python + skill setup

```bash
bash {baseDir}/scripts/setup.sh
```

Uses `python3 -m pip install --user` (no root). On **Python 3.6**, installs **selenium 3.141.x**; on 3.7+ installs selenium 4.x.

If you already installed selenium as root and `python3 -c 'import selenium'` works, setup is optional.

If pip fails with `Permission denied` under `/usr/local/lib/...`, you ran system-wide pip — use `setup.sh` instead.

## 4. Start Chrome (debug port 9222)

```bash
bash {baseDir}/scripts/start_chrome_debug.sh
```

Log in to Zhihu in VNC.

## 5. Verify

```bash
bash {baseDir}/scripts/zhihu_publish.sh --check --json
```

## Why chromedriver if Chrome is already open?

Selenium **attaches** via `chromedriver` + `debuggerAddress`. It does not replace Chrome; it is a small bridge. **Major version must match** Chrome or you get errors like `chromedriver executable needs to be in PATH` or session failures.

## Environment variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `CHROMEDRIVER_PATH` | `/usr/local/bin/chromedriver` if on PATH | Explicit driver path |
| `CHROMEDRIVER_INSTALL_DIR` | `~/.local/bin` if `/usr/local/bin` not writable | install_chromedriver.sh target |
| `CHROME_VERSION` | auto from Chrome | Force driver version, e.g. `148.0.7778.215` |
| `CHROME_DEBUG_PORT` | `9222` | Remote debugging |
| `CHROME_USER_DATA_DIR` | `~/.chrome-zhihu-automation` | Login profile |

## Browser closed?

`zhihu_publish.sh` **auto-starts** Chrome when port 9222 is down (same profile, login usually kept).

```bash
bash {baseDir}/scripts/zhihu_publish.sh --check --json
```

Manual only if needed:

```bash
bash {baseDir}/scripts/ensure_chrome_debug.sh
```

### DISPLAY (VNC)

OpenClaw `exec` must see the same display as VNC, or Chrome starts headless/invisible:

```bash
export DISPLAY=:1   # use your VNC display, often :1 or :0
```

Put this in the OpenClaw gateway service environment if agents run without an interactive shell.
