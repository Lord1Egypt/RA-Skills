---
name: skill-cleaner
version: 1.0.0
description: >
  扫描工作区所有 Skill，检测授权、配置和环境变量是否齐全，
  并可按需禁用或卸载无效 Skill。
triggers:
  - 清理无效 skill
  - 检查技能健康状态
  - 卸载配置缺失的技能
  - 扫描不能用的技能
entrypoint: python3 skill_cleaner.py
actions:
  report:
    command: python3 skill_cleaner.py
    description: 生成完整的 Skill 健康诊断报告
  clean:
    command: python3 skill_cleaner.py clean $ACTION $SKILL_NAMES
    description: 执行清理，ACTION 为 disable 或 uninstall
parameters:
  - name: ACTION
    type: string
    required: true
  - name: SKILL_NAMES
    type: string
    required: true
---
# Skill Cleaner

## 作用
自动找出已安装但无法使用的 Skill（缺少 API Key、被禁用、文件损坏），并帮你清理它们。

## 触发场景
- 用户说：“检查我的技能状态”
- 用户说：“为什么我的 XXX 技能用不了？”
- 用户说：“清理那些不能用的技能”

## 工作流程
1. 调用 `report` 动作获取诊断报告。
2. 向用户展示无效 Skill 列表，并询问是否清理。
3. 用户确认后，调用 `clean` 动作执行 disable/uninstall。