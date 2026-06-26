#!/bin/bash
# List supported tokens from Relay Link API
# Usage: ./get-tokens.sh [limit]
LIMIT=${1:-20}
curl -s "https://api.relay.link/currencies/v1" | jq ".currencies[0:$LIMIT][] | { name, symbol, address, chainId }"
