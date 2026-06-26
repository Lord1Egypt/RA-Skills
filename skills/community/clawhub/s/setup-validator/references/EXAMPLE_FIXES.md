# Example Fixes for Common Issues

This document provides example fixes for common security misconfigurations detected by the **Setup Validator** skill.

## 1. Excessive Permissions
### Issue
OpenClaw or its plugins have excessive file or directory permissions.

### Example Fix
Restrict permissions to the minimum required:
```bash
chmod 750 ~/.openclaw
chmod 640 ~/.openclaw/config.yaml
```

## 2. Unsafe Plugins
### Issue
A plugin is missing the required `openclaw.plugin.json` manifest or has invalid manifest structure.

### Example Fix
Validate the plugin:
```bash
~/.openclaw/skills/plugin-integration/scripts/validate-plugin.sh ~/.openclaw/plugins/example-plugin
```

Remove an unsafe plugin:
```bash
openclaw plugins remove example-plugin
```

## 3. Missing Sandboxing
### Issue
Sandboxing is not configured for OpenClaw or its plugins.

### Example Fix
OpenClaw uses built-in sandboxing by default. For custom configuration, edit `~/.openclaw/config.yaml`:
```yaml
sandbox:
  enabled: true
  restrictions:
    network: true
    filesystem: true
```

## 4. Outdated Dependencies
### Issue
OpenClaw version is outdated.

### Example Fix
Update OpenClaw (it's a Node.js package, use npm):
```bash
npm update -g openclaw
```

Or use the OpenClaw CLI:
```bash
openclaw update
```

## 5. Plugin Source Validation
### Issue
A plugin is installed from a source that is not verified.

### Example Fix
Reinstall the plugin from a trusted source:
```bash
openclaw plugins remove example-plugin
openclaw plugins install example-plugin --source trusted-repo
```

## 6. Configuration File Integrity
### Issue
The OpenClaw configuration file has incorrect or unsafe settings.

### Example Fix
Reset the configuration file to default:
```bash
openclaw config reset
```
Then reconfigure any custom settings manually.