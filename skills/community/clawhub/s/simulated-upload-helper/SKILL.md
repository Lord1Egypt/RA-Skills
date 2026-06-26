name: simulated-upload-helper
description: 当用户说“模拟上传”时，直接触发已有 skill 的发布流程，不创建新 skill。
version: 0.1.1

# Simulated Upload Helper

## 用途
这个 skill 用于快速触发本地 skills 的上传/发布流程，只调用发布脚本，不创建任何新 skill。

## 触发词
- 模拟上传
- 上传 skill
- 发布 skills
- 一键发布

## 执行步骤
1. 判断用户是否指定了 skill 名：
   - 指定 skill 名：执行单个发布。
   - 未指定 skill 名：执行按变更批量发布。
2. 调用仓库中的发布脚本：
   - 批量模式：`./publish-skills.sh --root ".cursor/skills"`
   - 单个模式：`./publish-skills.sh --root ".cursor/skills" --skill "<skill目录名>"`
3. 输出发布结果；若失败，返回错误信息并给出排查建议。

## 约束
- 严禁创建新的 skill 目录或 `SKILL.md` 文件。
- 严禁修改用户未要求变更的 skill 内容。
- 所有路径带空格时必须使用双引号。
- 上传前确认环境变量：
  - `CLAWHUB_TOKEN`（可选，供无交互登录）
  - `CLAWHUB_REGISTRY`（可选，覆盖默认 registry）
 - 若未设置 `CLAWHUB_TOKEN`，需提前执行 `clawhub login`。

## 示例
用户输入：`模拟上传`

期望行为：
1. 直接执行发布命令（单个或批量）。
2. 不创建任何测试 skill。
3. 返回成功或失败原因。
