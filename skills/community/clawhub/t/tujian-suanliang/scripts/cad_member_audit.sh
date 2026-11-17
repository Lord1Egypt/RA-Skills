#!/usr/bin/env bash
exec python3 "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/cad_member_audit.py" "$@"
