#!/usr/bin/env bash
set -euo pipefail

DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$DIR"

clawhub publish "$DIR" \
  --slug x-growth-automation \
  --name "X Growth Automation" \
  --version 0.1.0 \
  --tags latest,x,twitter,automation,growth,openclaw \
  --changelog "Initial public release: multilingual X automation skill scaffold with setup questionnaire, rollout guidance, and reusable project generator."
