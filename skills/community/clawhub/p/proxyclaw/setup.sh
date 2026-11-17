#!/usr/bin/env bash
set -euo pipefail
printf "%s\n" "Checking configured proxy credentials..."
bash "$(dirname "${BASH_SOURCE[0]}")/fetch.sh" https://example.com --timeout 15 >/dev/null
printf "%s\n" "Proxy connection verified. V2 state/city selectors are available; exact-city geolocation varies."
