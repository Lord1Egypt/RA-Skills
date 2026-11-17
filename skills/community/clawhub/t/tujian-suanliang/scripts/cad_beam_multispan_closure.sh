#!/usr/bin/env bash
# 按带宽数把多跨梁同轴跨支座续接，量化梁缺口中有多少来自链被支座截断。
exec bash "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/run_cad.sh" cad_beam_multispan_closure "$@"
