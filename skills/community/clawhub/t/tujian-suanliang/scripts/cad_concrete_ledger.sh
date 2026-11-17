#!/usr/bin/env bash
exec bash "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/run_cad.sh" cad_concrete_ledger "$@"
