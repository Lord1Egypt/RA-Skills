#!/usr/bin/env bash
# log-transaction.sh — Append a transaction record to the spend-ledger log.
#
# Usage (argument):
#   log-transaction.sh '<json_object>'
#
# Usage (stdin — preferred, avoids shell escaping issues):
#   echo '<json_object>' | log-transaction.sh
#
# The JSON object should contain fields matching the transaction schema:
#   service.url, service.name, service.category,
#   amount.value, amount.currency, amount.chain,
#   tx_hash, context.session_key, context.skill,
#   context.user_request, context.tool_name, context.tool_args_summary,
#   status
#
# Fields not provided will be filled with defaults by the logging module.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SERVER_DIR="$SCRIPT_DIR/../server"

if [ $# -ge 1 ]; then
  JSON="$1"
else
  JSON="$(cat)"
fi

if [ -z "$JSON" ]; then
  echo "Usage: log-transaction.sh '<json_object>'  OR  echo '<json>' | log-transaction.sh" >&2
  exit 1
fi

node --input-type=module -e "
import { appendTransaction } from '${SERVER_DIR}/transactions.js';
const txn = JSON.parse(process.argv[1]);
// Normalize status aliases agents commonly produce
if (txn.status === 'success') txn.status = 'confirmed';
// Mark as manually logged (same as server API POST)
txn.source = 'manual';
const record = appendTransaction(txn);
console.log(JSON.stringify(record, null, 2));
" "$JSON"
