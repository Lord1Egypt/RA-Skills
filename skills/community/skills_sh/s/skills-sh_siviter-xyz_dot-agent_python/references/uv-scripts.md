# uv Scripts Guidelines

Guidelines for adhoc Python scripts in uv-managed projects. Use uv's inline script metadata (PEP 723) to ensure dependencies are source controlled and scripts are executable.

## Declaring Script Dependencies

Use `uv add --script` to declare dependencies inline in the script file:

```bash
uv add --script script.py 'requests<3' 'rich'
```

This adds inline metadata at the top of the script:

```python
# /// script
# dependencies = [
#   "requests<3",
#   "rich",
# ]
# ///

import requests
from rich.pretty import pprint
# ... rest of script
```

## Executable Scripts with Shebang

For executable scripts, use the shebang format that works with uv:

```python
#!/usr/bin/env -S uv run --script
#
# /// script
# requires-python = ">=3.12"
# dependencies = ["httpx"]
# ///

import httpx
# ... rest of script
```

Make scripts executable with `chmod +x script.py`, then run directly: `./script.py`

## Running Scripts

- Use `uv run script.py` to execute scripts (uv automatically manages the environment)
- Scripts with inline metadata ignore project dependencies (no need for `--no-project` flag)
- Use `uv lock --script script.py` to create a lockfile (`script.py.lock`) for reproducibility

## Best Practices

- **Always declare dependencies inline** for adhoc scripts to ensure they're source controlled
- **Use shebang** (`#!/usr/bin/env -S uv run --script`) for executable scripts
- **Lock dependencies** using `uv lock --script` for reproducibility
- **Specify Python version** in metadata if required: `requires-python = ">=3.12"`

## References

Based on [uv documentation on declaring script dependencies](https://docs.astral.sh/uv/guides/scripts/#declaring-script-dependencies).
