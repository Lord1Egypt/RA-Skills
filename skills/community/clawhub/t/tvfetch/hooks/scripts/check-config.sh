#!/usr/bin/env bash
# tvfetch SessionStart hook — validates configuration
# Non-blocking: only prints warnings, never fails the session.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Detect Windows (Git Bash / MSYS / Cygwin)
if [[ "$OSTYPE" == "msys"* ]] || [[ "$OSTYPE" == "cygwin"* ]] || [[ "$(uname -s 2>/dev/null)" =~ MINGW ]]; then
    PYTHON="python"
else
    PYTHON="python3"
fi

# 1. Python version check
PY_VERSION=$($PYTHON --version 2>&1)
if [[ $? -ne 0 ]]; then
    echo "TVFETCH WARNING: Python not found. Install Python 3.11+"
else
    # Check for 3.11+
    PY_MINOR=$($PYTHON -c "import sys; print(sys.version_info.minor)" 2>/dev/null)
    if [[ -n "$PY_MINOR" ]] && [[ "$PY_MINOR" -lt 11 ]]; then
        echo "TVFETCH WARNING: Python 3.11+ required, found $PY_VERSION"
    fi
fi

# 2. tvfetch package check
$PYTHON -c "import tvfetch" 2>/dev/null
if [[ $? -ne 0 ]]; then
    echo "TVFETCH WARNING: tvfetch not installed. Run: pip install -e $SKILL_DIR"
fi

# 3. Core dependencies check
$PYTHON -c "import websocket, httpx, pandas, click, rich" 2>/dev/null
if [[ $? -ne 0 ]]; then
    echo "TVFETCH WARNING: Missing dependencies. Run: pip install websocket-client httpx pandas click rich"
fi

# 4. Auth token status
$PYTHON "$SKILL_DIR/scripts/lib/config.py" --check-auth-quiet 2>/dev/null

# 5. Cache directory writability
$PYTHON -c "
from pathlib import Path
p = Path.home() / '.tvfetch'
p.mkdir(exist_ok=True)
(p / '.write_test').touch()
(p / '.write_test').unlink()
" 2>/dev/null
if [[ $? -ne 0 ]]; then
    echo "TVFETCH WARNING: Cannot write to ~/.tvfetch/ — cache may be disabled"
fi

# 6. Network connectivity (quick, non-blocking)
$PYTHON -c "
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(2)
try:
    s.connect(('data.tradingview.com', 443))
    s.close()
except:
    print('TVFETCH WARNING: Cannot reach data.tradingview.com — offline mode only')
" 2>/dev/null

exit 0
