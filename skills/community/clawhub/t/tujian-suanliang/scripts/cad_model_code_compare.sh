#!/usr/bin/env bash
# 梁对象编号级模型自检入口。
exec bash "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/run_cad.sh" cad_model_code_compare "$@"
