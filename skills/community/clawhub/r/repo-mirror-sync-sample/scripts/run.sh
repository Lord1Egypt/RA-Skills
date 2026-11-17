#!/usr/bin/env bash
set -euo pipefail
echo "demo:{input:-none}" | sha256sum | cut -d" " -f1
