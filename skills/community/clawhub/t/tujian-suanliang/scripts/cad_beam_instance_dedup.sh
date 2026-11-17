#!/usr/bin/env bash
# 判算量实例与模型梁是否同一根物理梁，防双口径重复计量。
exec bash "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/run_cad.sh" cad_beam_instance_dedup "$@"
