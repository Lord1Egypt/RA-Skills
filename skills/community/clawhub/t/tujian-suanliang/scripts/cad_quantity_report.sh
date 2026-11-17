#!/usr/bin/env bash
# 合并已有算量 JSON，生成构件规格、钢筋型号、梁板状态和异常统一报告。
exec bash "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/run_cad.sh" cad_quantity_report "$@"
