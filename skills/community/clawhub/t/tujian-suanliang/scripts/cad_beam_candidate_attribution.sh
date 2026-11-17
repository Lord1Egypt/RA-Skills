#!/usr/bin/env bash
# 复核梁截面口径，归属图框内未覆盖候选段，拆出本图框无法解释的梁缺口。
exec bash "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/run_cad.sh" cad_beam_candidate_attribution "$@"
