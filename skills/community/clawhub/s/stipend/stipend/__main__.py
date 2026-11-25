"""Makes `python -m stipend` work.

Without this the package could only be driven as `python -m stipend.cli`, while
every instruction we publish — the site, skill.md, the licence email, the
manifest — says `python -m stipend` or a bare `stipend`. Three invocations were
documented and none of them ran.
"""

import sys

from .cli import main

if __name__ == "__main__":
    sys.exit(main())
