#!/usr/bin/env bash
# query-log.sh — Query the spend-ledger transaction log.
#
# Usage:
#   query-log.sh [--from DATE] [--to DATE] [--service NAME] [--skill NAME] [--summary daily|weekly|monthly] [--by-service] [--by-skill] [--verify]
#
# Examples:
#   query-log.sh                              # All transactions
#   query-log.sh --from 2026-03-01            # Since March 1
#   query-log.sh --summary daily              # Daily rollups
#   query-log.sh --by-service                 # Breakdown by service
#   query-log.sh --verify                     # Verify hash chain

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SERVER_DIR="$SCRIPT_DIR/../server"

FROM=""
TO=""
SERVICE=""
SKILL=""
SUMMARY=""
BY_SERVICE=false
BY_SKILL=false
VERIFY=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --from) FROM="$2"; shift 2 ;;
    --to) TO="$2"; shift 2 ;;
    --service) SERVICE="$2"; shift 2 ;;
    --skill) SKILL="$2"; shift 2 ;;
    --summary) SUMMARY="$2"; shift 2 ;;
    --by-service) BY_SERVICE=true; shift ;;
    --by-skill) BY_SKILL=true; shift ;;
    --verify) VERIFY=true; shift ;;
    *) echo "Unknown option: $1" >&2; exit 1 ;;
  esac
done

node --input-type=module -e "
import { queryTransactions, summarize, groupBy, verifyChain } from '${SERVER_DIR}/transactions.js';

const filters = {};
if ('${FROM}') filters.from = '${FROM}';
if ('${TO}') filters.to = '${TO}';
if ('${SERVICE}') filters.service = '${SERVICE}';
if ('${SKILL}') filters.skill = '${SKILL}';

if (${VERIFY}) {
  console.log(JSON.stringify(verifyChain(), null, 2));
} else if ('${SUMMARY}') {
  const txns = queryTransactions(filters);
  console.log(JSON.stringify(summarize(txns, '${SUMMARY}'), null, 2));
} else if (${BY_SERVICE}) {
  const txns = queryTransactions(filters);
  console.log(JSON.stringify(groupBy(txns, 'service'), null, 2));
} else if (${BY_SKILL}) {
  const txns = queryTransactions(filters);
  console.log(JSON.stringify(groupBy(txns, 'skill'), null, 2));
} else {
  const txns = queryTransactions(filters);
  console.log(JSON.stringify(txns, null, 2));
}
"
