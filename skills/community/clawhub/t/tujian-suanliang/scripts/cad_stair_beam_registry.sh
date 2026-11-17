#!/usr/bin/env bash
# 楼梯梁独立台账入口。
exec bash "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/run_cad.sh" cad_stair_beam_registry "$@"
