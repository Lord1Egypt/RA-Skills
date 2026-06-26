#!/usr/bin/env bash
set -euo pipefail

grep -q '^id:' skill.yaml
grep -q '^name:' skill.yaml
grep -q '^version:' skill.yaml
echo "lint passed"
