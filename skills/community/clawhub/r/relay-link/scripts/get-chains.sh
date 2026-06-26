#!/bin/bash
# List supported chains from Relay Link API
curl -s "https://api.relay.link/chains" | jq '.chains[] | { name, id, displayName }'
