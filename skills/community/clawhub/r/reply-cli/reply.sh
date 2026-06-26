#!/bin/bash

# Load the Reply API key: prefer env var, fall back to Docker secret
if [[ -z "$REPLY_API_KEY" ]] && [[ -f "/run/secrets/reply_key" ]]; then
    export REPLY_API_KEY=$(cat /run/secrets/reply_key)
fi

if [[ -z "$REPLY_API_KEY" ]]; then
    echo "Error: REPLY_API_KEY is not set. Set it in your environment or as a Docker secret at /run/secrets/reply_key"
    exit 1
fi

# Pass all arguments to reply-cli
npx reply-cli "$@"
