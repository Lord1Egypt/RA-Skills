#!/usr/bin/env bash
# 单入口：DWG/DXF -> 几何 -> 梁对象 -> 结构模型 -> 混凝土分账 -> 统一报告。
exec bash "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/run_cad.sh" cad_quantity_pipeline "$@"
