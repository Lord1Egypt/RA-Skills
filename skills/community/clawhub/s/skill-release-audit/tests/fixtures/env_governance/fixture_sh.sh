#!/bin/bash
# frozen sample: shell forms
OUT="${SRP_OUTPUT_DIR:-/tmp/out}"
REQ="${MUST_HAVE_VAR:?MUST_HAVE_VAR is required}"
echo "$OUT" "$REQ" "$PLAIN_VAR"
