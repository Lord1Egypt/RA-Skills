#!/usr/bin/env bash
# 结构模型、梁净跨、墙柱/板拓扑与分级混凝土台账入口。
exec bash "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/run_cad.sh" cad_structure_model "$@"
