# Hooks

## activator.sh
Runs before prompts to surface relevant patterns from memory.

```bash
./activator.sh [context]
```

## error-detector.sh
Runs after errors to log them for later analysis.

```bash
./error-detector.sh [type] [detail]
```

## Integration
For OpenClaw, add to your configuration:
- activator.sh as `pre-prompt-hook`
- error-detector.sh as `post-error-hook`

## Permissions
Ensure scripts are executable:
```bash
chmod +x hooks/*.sh
```
