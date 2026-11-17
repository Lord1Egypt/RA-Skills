#!/usr/bin/env bash
set -euo pipefail
node --test "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/projects.test.js"
