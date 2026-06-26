#!/bin/bash
WFID="$1"
RESULTS_DIR="$(pwd)/results"
if [ -z "$WFID" ]; then echo "Usage: $0 <wf-id>"; exit 1; fi
mkdir -p "$RESULTS_DIR/$WFID"
# collect any logs matching wf id
cp -v results/${WFID}.json "$RESULTS_DIR/$WFID/" 2>/dev/null || true
echo "report generated at $RESULTS_DIR/$WFID/"
