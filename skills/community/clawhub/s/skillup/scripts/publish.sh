#!/bin/sh

set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname "$0")" && pwd)
SKILLUP_ROOT=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)
. "$SCRIPT_DIR/lib/common.sh"
. "$SCRIPT_DIR/lib/github.sh"
. "$SCRIPT_DIR/lib/xiaping.sh"
. "$SCRIPT_DIR/lib/openclaw.sh"
. "$SCRIPT_DIR/lib/clawhub.sh"

main "$@"
