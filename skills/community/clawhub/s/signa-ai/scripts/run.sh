#!/bin/bash
cd "$(dirname "$0")"

# Check AT balance directly
python3 wallet.py --network mainnet balance S-FH56-5NA6-E75H-DPAM9
echo ""
# Check worker balance
python3 wallet.py --network mainnet balance S-44S7-32XB-5DM5-5AL3K
