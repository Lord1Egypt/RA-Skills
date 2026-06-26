---
name: vefaas
description: Deploy and manage serverless applications on Volcengine veFaaS. Use when the user wants to deploy web apps, agents, skills as APIs, tool pages, webhook functions, manage existing functions (pull code, upload and deploy), configure environment variables, or work with veFaaS services.
allowed-tools: Bash(vefaas:*)
metadata:
  clawdbot:
    primaryEnv: VOLC_ACCESS_KEY_ID
    requires:
      bins:
        - node
        - npm
        - vefaas
      env:
        - VOLC_ACCESS_KEY_ID
        - VOLC_SECRET_ACCESS_KEY
    install:
      kind: tarball
      url: https://vefaas-cli.tos-cn-beijing.volces.com/volcengine-vefaas-latest.tgz
      bin: vefaas
---
# vefaas: Volcengine FaaS CLI

**vefaas** is the command-line tool for Volcengine Function Service (veFaaS). It enables serverless application deployment, function management, and configuration through a streamlined workflow.

## Installation

```bash
npm i -g https://vefaas-cli.tos-cn-beijing.volces.com/volcengine-vefaas-latest.tgz
```

> **Note**: The domain `volces.com` is Volcengine (ByteDance cloud). This tarball is the official distribution channel for the CLI — not published to npm registry. Install method matches the front matter `metadata.install` spec.

Verify installation:

```bash
vefaas --version
```

> **Tip**: `vefaas -v` (or `vefaas --version`) will print the current version and, if a newer release is available, show instructions on how to update. When a user encounters unsupported features or wants to check for updates, run this command first.

## Core Workflow

The typical deployment pattern:

1. **Check Node.js**: `node --version` (requires >= 18, recommended 20+)
   - If version is too low, switch using nvm (`nvm use 20`) or fnm (`fnm use 20`), or manually install a newer version

2. **Check CLI**: `vefaas --version` to verify installation

3. **Authenticate** (try in order, stop at first success):

   a. **Auto-check (preferred)**: `vefaas login --check` — the CLI auto-detects available credentials (Ark Skill, injected tokens, etc.). If this passes, proceed to step 4.
   b. **SSO**: `vefaas login --sso` — if browser is available.
   c. **AK/SK**: `vefaas login --accessKey <AK> --secretKey <SK>` — last resort, prompt user.

4. **Pre-flight check** (MUST do before every deploy): `vefaas inspect`

   - `framework` / `language` correct → don't touch start command or build settings
   - `port` wrong → fix in code (e.g., `process.env.PORT || 3000`), or override via `--port` at deploy time
   - **Check dependency files**: ensure `package.json` (Node.js) or `requirements.txt` (Python) lists all runtime deps — the server only installs what's declared, not what's globally installed locally

5. **Deploy**:
   ```bash
   # New app
   vefaas deploy --newApp <n> --gatewayName $(vefaas run listgateways --first) --yes

   # Existing app
   vefaas deploy --app <n> --yes
   ```

   If you need to override specific parameters that `inspect` got wrong (port, build command, start command, etc.), pass them directly at deploy time:
   ```bash
   vefaas deploy \
     --newApp my-app \
     --gatewayName $(vefaas run listgateways --first) \
     --buildCommand "npm run build" \
     --outputPath dist \
     --command "node dist/index.js" \
     --port 3000 \
     --yes
   ```

6. **Access**: `vefaas domains` to view URLs

## Quick Commands

| Purpose | Command |
|---------|---------|
| Check version / update | `vefaas -v` (shows version and update instructions if available) |
| Check auth | `vefaas login --check` **(preferred, auto-detects credentials)** |
| Login (SSO) | `vefaas login --sso` (opens browser, auto-completes) |
| Login (AK/SK) | `vefaas login --accessKey <AK> --secretKey <SK>` (last resort) |
| Init from template | `vefaas init --template <n>` |
| Inspect project | `vefaas inspect` (**run before deploy to verify detection**) |
| Deploy new app | `vefaas deploy --newApp <n> --gatewayName $(vefaas run listgateways --first) --yes` |
| Deploy existing | `vefaas deploy --app <n> --yes` |
| List gateways | `vefaas run listgateways --first` |
| View URLs | `vefaas domains` |
| Set env var | `vefaas env set KEY VALUE` |
| View config | `vefaas config list` |
| Pull code | `vefaas pull --func <n>` |

## Global Options

| Option | Description |
|--------|-------------|
| `-d, --debug` | Enable debug mode for troubleshooting |
| `--yes` | Non-interactive mode (required for CI/AI coding) |
| `--region` | Region override (e.g., cn-beijing) |

## Cookbooks

Step-by-step guides for common scenarios:

- **[Template Quickstart](cookbooks/template-quickstart.md)** — Create and deploy from official templates
- **[Deploy Existing Code](cookbooks/deploy-existing-code.md)** — Deploy your existing project
- **[Deploy an Agent](cookbooks/deploy-agent.md)** — Deploy a conversational AI agent as an HTTP endpoint
- **[Publish Skill as API](cookbooks/publish-skill-as-api.md)** — Turn an OpenClaw skill into a remote service
- **[Generate Tool Page](cookbooks/generate-tool-page.md)** — Generate and deploy a shareable online tool from a natural language request
- **[Deploy Webhook](cookbooks/deploy-webhook.md)** — Deploy a webhook / glue function to connect two services
- **[Manage Functions](cookbooks/manage-functions.md)** — Manage functions (pull code, upload and deploy)

## References

Detailed documentation on specific topics:

- **[Configuration](references/configuration.md)** — Config files and settings
- **[Framework Detection](references/framework-detection.md)** — Supported frameworks and auto-detection
- **[Troubleshooting](references/troubleshooting.md)** — Debug mode, common issues, and solutions

## Security

- **Declared credentials only**: This skill uses `VOLC_ACCESS_KEY_ID` and `VOLC_SECRET_ACCESS_KEY` as declared in the front matter. The agent should not read or probe for any other env vars, `.env` files, or credential files.
- **Debug output**: `vefaas --debug` may print request/response payloads that contain tokens or secrets. Do not log, store, or surface debug output to the user unless they explicitly request troubleshooting. When sharing debug output, redact any values that look like keys, tokens, or secrets.

## Important Notes

- Always use `--yes` for non-interactive mode in CI/CD and AI coding scenarios
- Use `$(vefaas run listgateways --first)` to get an available gateway
- Config is stored in `.vefaas/config.json` after linking
- Use `--debug` or `-d` to troubleshoot issues (see Security section for caveats)
- **Auth**: always start with `vefaas login --check` — the CLI auto-detects available credentials
- Always run `vefaas inspect` before **every** deploy — check framework/language detection, port, and dependency files (`package.json` / `requirements.txt`). Fix issues before deploying, not after
- When a feature is unsupported or you suspect the CLI is outdated, run `vefaas -v` to check version and see update instructions