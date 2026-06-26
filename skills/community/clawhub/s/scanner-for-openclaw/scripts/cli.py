#!/usr/bin/env python3
"""
OpenClaw Security Scanner - CLI Wrapper

Provides `openclaw security-scan` command interface.
Delegates directly to security_scan.main() without subprocess.

Usage:
    openclaw security-scan [OPTIONS]

Options:
    --ports-only      Only scan network ports
    --channels        Only audit channel policies
    --permissions     Only analyze permissions
    --output, -o FILE Save report to file
    --verbose, -v     Verbose output
    --help, -h        Show this help
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from security_scan import main as scan_main


def main():
    try:
        scan_main()
    except SystemExit as e:
        return e.code if e.code is not None else 0
    except KeyboardInterrupt:
        print("\nScan interrupted by user")
        return 130
    except Exception as e:
        print(f"Error running security scan: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
