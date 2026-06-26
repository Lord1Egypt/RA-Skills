#!/bin/bash

# 薪酬调研助手 - 执行脚本
# 调用全局安装的 salary-natural 命令

# 检查 salary-natural 是否已安装
if ! command -v salary-natural &> /dev/null; then
    echo "错误：salary-natural 命令未找到"
    echo "请先安装：cd /Users/claw/.openclaw/workspace-ideacat/hr-skills/salary-research && npm link"
    exit 1
fi

# 执行 salary-natural 命令，传递所有参数
salary-natural "$@"
