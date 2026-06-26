# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.1.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Permissions Required

This skill requires the following system permissions:

| Permission | Description | Risk Level |
|------------|-------------|------------|
| `screen_capture` | Capture screenshots | Medium |
| `keyboard_input` | Simulate keyboard input | Medium |
| `mouse_input` | Simulate mouse movements and clicks | Low |
| `clipboard_access` | Read/write clipboard | High |
| `shell_execution` | Execute shell commands | High |

## Sensitive Operations

The following operations are marked as sensitive and recommend user approval:

- `desktop_shell` - Execute arbitrary shell commands
- `desktop_clipboard_get` - Read clipboard (may contain sensitive data)
- `desktop_screenshot` - Capture screen (may contain private information)
- `desktop_get_state` - Get full desktop state including screenshot

## User Approval

**Recommended**: Enable approval mode in OpenClaw settings.

When enabled:
1. Sensitive operations will request user confirmation before execution
2. User can approve, deny, or modify parameters
3. Whitelist can be configured to skip approval for trusted operations

## Sandbox Support

This skill supports sandboxed execution:
- Screen capture can be limited to specific regions
- Shell commands can be executed in restricted environments
- Mouse/keyboard operations respect system boundaries

## Reporting a Vulnerability

If you discover a security vulnerability, please report it via:
- GitHub Issues: https://github.com/openclaw/clawhub/issues
- Email: security@openclaw.ai

## Best Practices

1. **Review Commands**: Always review shell commands before approval
2. **Limit Access**: Only grant necessary permissions
3. **Test Environment**: Test in isolated environments first
4. **Audit Logs**: Review operation logs regularly
5. **Clipboard Caution**: Be aware clipboard may contain sensitive data

## Implementation

This skill includes:
- Complete Python implementation (`scripts/rpa.py`)
- Explicit OS restriction (Windows only)
- Installation specifications in `skill.json`
- User approval mechanisms for sensitive operations
