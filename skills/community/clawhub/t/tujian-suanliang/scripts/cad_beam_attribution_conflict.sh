#!/usr/bin/env bash
# 同轴同截面异编号的梁段与模型梁定责，用引线标注判谁对。
exec bash "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/run_cad.sh" cad_beam_attribution_conflict "$@"
