if __name__ == "__main__" and __package__ is None:
    # Direct execution: make absolute imports work.
    import os
    import sys

    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from recamera_intellisense._cli import main
else:
    from ._cli import main

raise SystemExit(main())
