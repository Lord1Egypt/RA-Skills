#!/usr/bin/env bash
# TradeMemory Protocol — MT5 Sync Setup (Interactive)
# Guides user through connecting MetaTrader 5 to TradeMemory.

set -euo pipefail

echo "=================================="
echo "  MT5 Sync Setup for TradeMemory"
echo "=================================="
echo ""
echo "This script sets up automatic trade syncing from MetaTrader 5."
echo "Your EA stays untouched — mt5_sync.py reads trades via the MT5 API."
echo ""

# Check OS — MT5 Python API only works on Windows
if [[ "$OSTYPE" != "msys" && "$OSTYPE" != "cygwin" && "$OSTYPE" != "win32" ]]; then
    echo "[WARN] MetaTrader 5 Python API only runs on Windows."
    echo "       On Linux/macOS, you can still use TradeMemory by:"
    echo "         - Manually recording trades via MCP tools"
    echo "         - Sending trades through the REST API"
    echo "         - Writing a custom sync script for your platform"
    echo ""
    echo "See: https://github.com/mnemox-ai/tradememory-protocol/blob/master/docs/MT5_SYNC_SETUP.md"
    exit 0
fi

# Install MT5 dependencies
echo "[1/4] Installing MT5 Python dependencies..."
python3 -m pip install MetaTrader5 python-dotenv requests fastapi uvicorn pydantic
echo "[OK] Dependencies installed"
echo ""

# Clone repo if not already present
REPO_DIR="tradememory-protocol"
if [ ! -d "$REPO_DIR" ]; then
    echo "[2/4] Cloning tradememory-protocol..."
    git clone https://github.com/mnemox-ai/tradememory-protocol.git
    cd "$REPO_DIR"
else
    echo "[2/4] Repository already exists, skipping clone."
    cd "$REPO_DIR"
fi
echo ""

# Create .env from template
if [ ! -f ".env" ]; then
    echo "[3/4] Setting up credentials..."
    if [ -f ".env.example" ]; then
        cp .env.example .env
    else
        cat > .env << 'ENVEOF'
# MT5 Account
MT5_LOGIN=your_login_here
MT5_PASSWORD=your_password_here
MT5_SERVER=YourBroker-Server

# TradeMemory API
TRADEMEMORY_API=http://localhost:8000

# Sync interval (seconds)
SYNC_INTERVAL=60
ENVEOF
    fi
    echo ""
    echo "  >> Edit .env with your MT5 credentials:"
    echo "     MT5_LOGIN     = your account number"
    echo "     MT5_PASSWORD   = your password"
    echo "     MT5_SERVER     = your broker server (e.g. ForexTimeFXTM-Demo01)"
    echo ""
    read -p "  Press Enter after editing .env to continue..."
else
    echo "[3/4] .env already exists, skipping."
fi
echo ""

# Verify MT5 connection
echo "[4/4] Testing MT5 connection..."
python3 -c "
import MetaTrader5 as mt5
from dotenv import load_dotenv
import os

load_dotenv()
login = int(os.getenv('MT5_LOGIN', '0'))
password = os.getenv('MT5_PASSWORD', '')
server = os.getenv('MT5_SERVER', '')

if not mt5.initialize():
    print('[ERROR] MT5 initialize failed. Is MetaTrader 5 running?')
    mt5.shutdown()
    exit(1)

if not mt5.login(login, password=password, server=server):
    print(f'[ERROR] MT5 login failed: {mt5.last_error()}')
    mt5.shutdown()
    exit(1)

info = mt5.account_info()
print(f'[OK] Connected: Account #{info.login}, Balance: \${info.balance:.2f}')
mt5.shutdown()
" 2>/dev/null || echo "[WARN] Could not verify MT5 connection. Make sure MT5 is running and .env is correct."

echo ""
echo "=================================="
echo "  Setup Complete"
echo "=================================="
echo ""
echo "To start syncing:"
echo "  Terminal 1:  python3 -m src.tradememory.server"
echo "  Terminal 2:  python3 mt5_sync.py"
echo ""
echo "Trades will auto-sync every 60 seconds."
echo "Full guide: https://github.com/mnemox-ai/tradememory-protocol/blob/master/docs/MT5_SYNC_SETUP.md"
echo ""
