# Example Cursor goal

Goal: Refactor a settings panel into a shared component using the Cursor agent.

Install and run:

```bash
geordi init --goal "Refactor settings panel into shared component" --mode cursor
geordi mission add "Extract SettingsPanel and add unit tests" --accept "npm test -- settings" --scope "Settings UI and shared component only."
geordi run --mode cursor --model "gpt-5"
```

If your shared agent rules live outside the default `~/.agents/AGENTS.md` path:

```bash
GEORDI_AGENTS_FILE=/path/to/AGENTS.md geordi run --mode cursor --model "gpt-5"
```

To switch the headless output format for streaming receipts:

```bash
GEORDI_CURSOR_ARGS="-p --trust --output-format stream-json" geordi run --mode cursor --model "gpt-5"
```
