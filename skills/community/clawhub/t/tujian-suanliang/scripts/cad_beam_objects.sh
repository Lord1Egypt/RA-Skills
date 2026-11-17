#!/usr/bin/env bash
# 梁中心线对象生成与复核入口。
exec bash "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/run_cad.sh" cad_beam_objects "$@"
