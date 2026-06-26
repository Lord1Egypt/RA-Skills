"""Compatibility wrapper for legacy imports.
Canonical implementation now lives at ``yumnb.tts``.
"""

from yumnb.tts import *  # noqa: F401,F403


if __name__ == "__main__":
    from yumnb.tts import main
    main()
