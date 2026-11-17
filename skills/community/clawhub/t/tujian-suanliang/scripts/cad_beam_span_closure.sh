#!/usr/bin/env bash
# 对账梁净跨口径与支座扣减，判定偏少编号的长度差是支座推定还是真缺几何。
exec bash "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/run_cad.sh" cad_beam_span_closure "$@"
