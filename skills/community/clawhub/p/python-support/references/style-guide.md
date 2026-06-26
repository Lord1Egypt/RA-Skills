# Python Style Guide

## PEP 8 Compliance

Follow PEP 8 guidelines with these specific adjustments:

- Line length: 100 characters (not 79)
- String quotes: Use double quotes for human-readable text, single quotes otherwise
- Type hints: Required for all public function signatures

## Code Structure

```python
#!/usr/bin/env python3
"""Module docstring."""

import subprocess
import sys
from pathlib import Path
from typing import Optional

def function_name(param1: str, param2: Optional[int] = None) -> bool:
    """Function docstring."""
    return True

if __name__ == "__main__":
    main()
```

## Error Handling

```python
try:
    result = subprocess.run(
        ["command", "arg1"],
        capture_output=True,
        text=True,
        check=True
    )
except subprocess.CalledProcessError as e:
    print(f"Error: {e.stderr}", file=sys.stderr)
    sys.exit(1)
```
