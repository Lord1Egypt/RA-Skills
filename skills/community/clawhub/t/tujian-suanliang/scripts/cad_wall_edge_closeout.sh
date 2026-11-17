#!/usr/bin/env bash
# 墙身空间闭合收口：逐格解释边缘构件面域外面积，并给特殊构件定归属。
exec bash "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/run_cad.sh" cad_wall_edge_closeout "$@"
