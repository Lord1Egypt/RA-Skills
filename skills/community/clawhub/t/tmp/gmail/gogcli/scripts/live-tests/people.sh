#!/usr/bin/env bash

set -euo pipefail

run_people_tests() {
  run_required "people" "people me" gog people me --json >/dev/null
}
