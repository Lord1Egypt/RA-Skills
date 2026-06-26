# Weekly Ops Review

Slug: `weekly-ops-review`

## 功能定位

Turn scattered notes, metrics, and unfinished tasks into a weekly operating review with wins, misses, blockers, and next-week priorities.

## 适用场景

- 当用户需要：周复盘
- 当用户手头已有原始材料，需要快速整理成可执行输出
- 当用户希望先预览方案、再决定是否落盘或批量处理

## 安装要求

- OpenClaw / AgentSkills 兼容目录结构
- `python3` 可执行文件在 PATH 中可用
- 无远程安装脚本、无隐藏联网依赖、无未声明凭据要求

## 目录结构

- `SKILL.md`：触发描述、工作流、输出契约
- `scripts/weekly_review_pack.py`：本地辅助脚本
- `resources/review_template.md`：被 SKILL/README 引用的资源文件
- `examples/example-prompt.md`：触发与输入示例
- `tests/smoke-test.md`：最小冒烟测试
- `SELF_CHECK.md`：规范与安全自检
- `CHANGELOG.md`：变更记录

## 触发示例

- `周复盘`
- `weekly review`
- `经营周报`
- `整理这周做了什么`
- `next week priorities`

## 建议输入

- notes
- metrics
- task list
- calendar highlights
- goals

## 预期输出

- weekly review memo
- metrics snapshot
- priority list
- carry-over board

## 辅助脚本

脚本：`scripts/weekly_review_pack.py`

建议先运行帮助信息确认参数：

```bash
python3 scripts/weekly_review_pack.py --help
```

该脚本设计原则：

- 本地执行，便于审计与回滚
- 输入输出路径显式传入
- 不使用 `curl|bash`、远程直灌、base64 混淆执行
- 仅处理用户明确提供的文件或目录

## 输入输出示例

输入示例见：`examples/example-prompt.md`

输出示例建议至少包含：

- 结构化主结果
- 未决问题 / 风险项
- 可交付给他人的摘要或清单

## 常见问题

### 1. 这个 skill 会直接改我的文件吗？

默认不应直接进行破坏性批量操作；应优先生成预览、清单或草案，只有在用户明确要求时才建议执行进一步动作。

### 2. 这个 skill 需要联网吗？

当前目录内未声明联网依赖，也没有内置远程下载步骤。是否联网应由具体会话任务决定，而不是由 skill 包本身强制触发。

### 3. 资源文件的作用是什么？

`resources/review_template.md` 为脚本或说明提供模板、规则、清单或模式参考，便于输出格式统一、可复用、可审计。

## 风险提示

- 对用户提供的数据、文本、截图或本地文件进行整理时，应先确认范围与目标。
- 涉及重命名、移动、合并、覆盖、生成正式对外内容时，应先给预览版本。
- 对不确定字段使用“待确认”标记，不应编造事实。

## 安全审计结论

- 依赖边界：仅声明 `python3`
- 凭据边界：未声明环境变量依赖
- 执行边界：本地脚本、本地资源、显式输入
- 高风险模式检查：未引入 `curl|bash`、远程管道执行、混淆载荷或私有 API 绑定
