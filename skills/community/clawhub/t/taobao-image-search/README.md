# Taobao (淘宝) Image Search Skill

Taobao (淘宝) image search and add-to-cart skill with script-first execution and browser-fallback. Now featuring automated login handling.

## Features

- **Search by Image**: Find identical or similar products on Taobao (淘宝) using an image.
- **Automated Workflow**: Automatically enters product details and attempts to add to cart.
- **Auto Login Detection**: Automatically checks for login status. if not logged in, it opens a login window and waits for completion before resuming the task.
- **Structured Results**: Produces detailed JSON results, execution logs, and screenshots for verification.

## Quick Start

### 1. Installation

1. Clone or copy these scripts to your environment.
2. Install Playwright and browser dependencies:
   ```bash
   npm install playwright
   npx playwright install chromium
   ```

### 2. Prepare Test Image

The project uses `test.png` by default. You can also provide any local image path during execution:

```bash
node run-taobao-task.js --image /absolute/path/to/your-image.png
```

### 3. Run with Automatic Login

You no longer need to run a separate cookie-saving script. Simply run the orchestrator:

```bash
node run-taobao-task.js --image ./test.png --headed
```

**How it works:**
1. The script checks if you are logged into Taobao (淘宝).
2. If **not logged in**, a browser window will pop up.
3. Complete the login in that window.
4. The script **automatically detects** your success and **resumes the search task** immediately.

### 4. Advanced Configuration

You can pass arguments directly to the orchestrator:

```bash
node run-taobao-task.js --image ./test.png --headed --delay-ms 5000
```

Available arguments:
- `--image, -i`: Path to the image (default: `test.png`).
- `--headless` / `--headed`: Running mode (default: `--headed`).
- `--out-dir`: Output directory (default: `verification-artifacts`).
- `--delay-ms`: Additional wait time for slow networks (default: `5000`).

## Output Artifacts

- `verification-artifacts/result.json`: Structured results.
- `verification-artifacts/run-log.txt`: Detailed execution logs.
- `verification-artifacts/*.png`: Screenshots of key steps.

Key Result Fields:
- `success`: Whether the overall flow succeeded.
- `loginCheck.isLoggedIn`: Login status.
- `addToCart.success`: Whether the "Add to Cart" confirmation was detected.

## Project Structure

- `SKILL.md`: Instructions for OpenClaw/Codex (Script-first).
- `run-taobao-task.js`: The main orchestrator with auto-login support.
- `auto-login-taobao.js`: Background script for login monitoring.
- `verify-taobao-runner.js`: The underlying automation script.

## Security & Privacy Note

> [!CAUTION]
> **This skill persists browser session tokens locally.**
> - Storage locations: `verification-artifacts/taobao-storage-state.json` and `.pw-user-data-taobao/`.
> - These files contain active session cookies for Taobao. **Do not share or upload them.**
> - Use the skill on trusted machines only.
> - To completely log out and remove tokens, delete these directories manually.

## Troubleshooting

- **Login Timeout**: If you don't log in within 10 minutes, the task will stop.
- **Selector Changes**: If Taobao (淘宝) changes its page structure, refer to the browser fallback instructions in `SKILL.md`.
- **Add to Cart Failure**: Usually caused by SKU selection requirements, risk control, or session expiration.
