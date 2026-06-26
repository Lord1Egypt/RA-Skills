#!/bin/bash
# synapse-code init — 初始化项目的 Synapse + Pipeline 环境

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
project_path="${1:-.}"

python3 "$SCRIPT_DIR/../scripts/init_project.py" "$project_path"
