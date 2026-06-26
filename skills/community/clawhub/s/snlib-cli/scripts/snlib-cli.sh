#!/usr/bin/env bash
set -euo pipefail

exec clojure \
  -Srepro \
  -Sdeps '{:deps {io.github.ruseel/snlib-cli {:mvn/version "20260407"}}}' \
  -M -m snlib.cli "$@"
