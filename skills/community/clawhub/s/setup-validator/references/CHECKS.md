# Setup Validator Checks

This document describes the checks performed by the **Setup Validator** skill. Each check includes a description, potential risks, and recommended fixes.

## 1. Excessive Permissions
### Description
Checks if OpenClaw or its plugins have excessive file or directory permissions.

### Risks
- Unauthorized access to sensitive files.
- Potential for privilege escalation attacks.

### Recommended Fix
- Restrict permissions to the minimum required:
  ```bash
  chmod 750 ~/.openclaw
  chmod 640 ~/.openclaw/config.yaml
  ```

## 2. Unsafe Plugins
### Description
Identifies plugins missing the required `openclaw.plugin.json` manifest or with invalid manifest structure.

### Risks
- Malicious plugins can execute arbitrary code.
- Plugins without manifests may not load correctly.
- Vulnerable plugins may expose sensitive data.

### Recommended Fix
- Validate plugin manifests:
  ```bash
  ~/.openclaw/skills/plugin-integration/scripts/validate-plugin.sh <plugin-dir>
  ```
- Remove unsafe plugins:
  ```bash
  openclaw plugins remove <plugin-name>
  ```
- Install plugins only from trusted sources.

## 3. Missing Sandboxing
### Description
Checks if sandboxing is configured for OpenClaw and its plugins.

### Risks
- Unrestricted access to system resources.
- Potential for sandbox escapes.

### Recommended Fix
- OpenClaw uses built-in sandboxing by default.
- Optional: Configure custom sandbox settings in `~/.openclaw/config.yaml`:
  ```yaml
  sandbox:
    enabled: true
    restrictions:
      network: true
      filesystem: true
  ```

## 4. Outdated Dependencies
### Description
Checks for outdated OpenClaw version using npm (OpenClaw is a Node.js package).

### Risks
- Known vulnerabilities in outdated versions.
- Compatibility issues with newer system components.
- Missing security patches.

### Recommended Fix
- Update OpenClaw:
  ```bash
  npm update -g openclaw
  ```
- Or use the OpenClaw CLI:
  ```bash
  openclaw update
  ```

## Example Output
```plaintext
📋 Checking Permissions...
  ✅ No issues found

📋 Checking Plugins...
  🚨 Unsafe Plugin: Plugin 'example-plugin' lacks an openclaw.plugin.json manifest file.
     Fix: Remove the plugin with `openclaw plugins remove example-plugin` or add a valid manifest.

📋 Checking Sandboxing...
  ℹ️ Sandboxing Info: No explicit sandbox configuration found. OpenClaw uses built-in sandboxing by default.

📋 Checking Dependencies...
  🚨 Outdated Dependencies: OpenClaw version 1.0.0 is outdated (latest: 1.2.0).
     Fix: Update OpenClaw with `npm update -g openclaw`.

============================================================
🚨 2 issue(s) detected
```