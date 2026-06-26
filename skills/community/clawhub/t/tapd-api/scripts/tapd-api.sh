#!/bin/bash
# TAPD API 完整工具
# 支持所有 18 个模块和 70+ API 方法

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_CLIENT="$SCRIPT_DIR/tapd_client.py"

# 使用说明
usage() {
    cat << 'EOF'
TAPD API 完整工具

用法: ./tapd-api.sh <module> <action> [options]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
核心模块 (Core Modules)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  story       需求 (14 methods)
  task        任务 (7 methods)
  bug         缺陷 (9 methods)
  iteration   迭代 (5 methods)
  test        测试用例 (10 methods)

扩展模块 (Extended Modules)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  comment     评论 (4 methods)
  wiki        Wiki (4 methods)
  timesheet   工时 (4 methods)
  workspace   工作空间/成员 (3 methods)
  workflow    工作流状态 (1 method)

高级模块 (Advanced Modules)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  boardcard   看板工作项 (3 methods)
  module      模块管理 (4 methods)
  relation    关联关系 (1 method)
  release     发布计划 (2 methods)
  version     版本管理 (4 methods)
  role        角色 (1 method)
  launchform  发布评审 (3 methods)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
常用操作 (Actions)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  list        列表查询
  count       计数统计
  create      创建记录
  update      更新记录
  (其他模块特定操作请查看文档)

选项 (Options)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  --workspace <id>    工作空间 ID
  --limit <n>         返回数量
  --id <id>           记录 ID
  --name <name>       名称/标题
  --status <status>   状态过滤

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
使用示例 (Examples)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  # 获取需求列表
  ./tapd-api.sh story list --limit 10

  # 获取需求计数
  ./tapd-api.sh story count

  # 获取缺陷列表（指定状态）
  ./tapd-api.sh bug list --status new --limit 20

  # 获取任务计数
  ./tapd-api.sh task count

  # 获取迭代列表
  ./tapd-api.sh iteration list

  # 获取项目成员
  ./tapd-api.sh workspace users

  # 获取工作流状态映射
  ./tapd-api.sh workflow status_map

  # 获取测试用例
  ./tapd-api.sh test list --limit 5

  # 获取工时记录
  ./tapd-api.sh timesheet list

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
文档 (Documentation)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  README.md           快速开始
  SKILL.md            完整文档
  reference/          参考资料和示例

总计: 18 模块, 70+ API 方法
EOF
}

# 检查参数
if [ $# -lt 2 ]; then
    usage
    exit 1
fi

# 检查 Python 客户端
if [ ! -f "$PYTHON_CLIENT" ]; then
    echo "❌ 错误: Python 客户端不存在: $PYTHON_CLIENT"
    exit 1
fi

MODULE=$1
ACTION=$2
shift 2

# 调用 Python 客户端
python3 "$PYTHON_CLIENT" "$MODULE" "$ACTION" "$@"
