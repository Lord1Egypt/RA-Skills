# Deployment flow

## Objective
Get the Open-AutoGLM phone agent running locally on the user's computer.

## Standard path
1. Check host tools
2. Clone or update the repo
3. Create and activate a repo-local `.venv`
4. Prepare the phone
5. Install Python dependencies into `.venv`
6. Configure the model endpoint
7. Verify the deployment from `.venv`
8. Run a smoke test from `.venv`

## Host tools
- `git`
- Python 3.10+
- `adb` for Android
- `hdc` for HarmonyOS

The exact install and command path may differ across macOS, Linux, and Windows.

## Repo path
Default to a folder inside the current workspace unless the user asks otherwise.

## Host OS rule
- detect the host OS before suggesting install commands
- do not assume Homebrew or bash on Windows
- on Windows, prefer PowerShell-friendly commands and `winget` when available
- detect whether the available Python interpreter is at least 3.10 before creating `.venv`
- if the default Python is too old but the host can self-install a newer one, do that automatically
- if GitHub update/pull fails transiently but the local repo is already usable, continue from the local repo instead of failing early

## Python environment rule
- create `.venv` in the repo root after clone or update
- activate `.venv` before any Python install or execution step
- install all project dependencies into `.venv`
- run all Python commands from `.venv`
- use OS-appropriate activation commands
  - macOS / Linux: `source .venv/bin/activate`
  - Windows PowerShell: `.\.venv\Scripts\Activate.ps1`
  - Windows cmd: `.venv\Scripts\activate.bat`

## Android path
Phone-side steps:
- Developer Options on
- USB debugging on
- USB debugging (security settings) on if present
- data-capable USB cable connected
- authorization popup accepted
- ADB Keyboard installed and enabled

Then check:
- `adb devices`
- `adb shell ime list -a`

## HarmonyOS path
Phone-side steps:
- Developer Options on
- USB debugging on
- wireless debugging if needed
- data-capable cable or Wi‑Fi connection
- authorization accepted

Then check:
- `hdc list targets`

## iPhone path
Use the repo’s iOS guide. Do not use ADB assumptions.

## Model modes
### BigModel
- base-url: `https://open.bigmodel.cn/api/paas/v4`
- model: `autoglm-phone`
- user provides API key

### Third-party compatible
- user provides OpenAI-compatible `base-url`
- user provides `model`
- user provides `apikey` if required

### Self-hosted
- the server must expose `/v1`
- the service must be reachable from the laptop running the agent

## Verification rule
Do not call deployment successful until a verification command returns a sane response.

## Smoke-test rule
Always start with a short task before doing a long or expensive task.
