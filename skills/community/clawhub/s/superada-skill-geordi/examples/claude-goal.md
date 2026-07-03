# Example Claude Code goal

Goal: Add OAuth refresh-token rotation in a repo whose primary tool is Claude Code.

Install and run:

```bash
geordi init --goal "Add OAuth refresh-token rotation" --mode claude
geordi mission add "Implement refresh-token rotation and tests" --accept "npm test -- auth" --scope "Auth flow, refresh helper, and tests only."
geordi run --mode claude --model "sonnet"
```

If your shared agent rules live outside the default `~/.agents/AGENTS.md` path:

```bash
GEORDI_AGENTS_FILE=/path/to/AGENTS.md geordi run --mode claude --model "sonnet"
```

For stricter sandboxed runs, prefer the explicit permission mode override:

```bash
GEORDI_CLAUDE_ARGS="-p --permission-mode bypassPermissions --output-format text" geordi run --mode claude --model "sonnet"
```
