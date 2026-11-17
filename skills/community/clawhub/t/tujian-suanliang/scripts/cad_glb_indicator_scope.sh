#!/usr/bin/env bash
# 广联达清单口径与构件实物量口径逐类对账，输出混凝土算量范围边界。
exec bash "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/run_cad.sh" cad_glb_indicator_scope "$@"
