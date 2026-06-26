"""Compatibility wrapper for legacy imports.

The canonical CLI now lives at ``yumnb.cli``.
This file remains as a thin shim so existing local references do not break.
"""

from yumnb.cli import *  # noqa: F401,F403
from yumnb.cli import main


if __name__ == "__main__":
    main()
