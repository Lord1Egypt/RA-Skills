#!/bin/bash
# scripts/run.sh in the tabstack skill directory
cd "$(dirname "$0")/.." && npx tsx ./scripts/tabstack.ts "$@"
