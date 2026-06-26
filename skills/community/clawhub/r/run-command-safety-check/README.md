# 命令执行安全检查官

## 功能
在执行 shell 方案前检查危险模式，如 pipe-to-shell、覆盖式删除、危险重定向或混淆执行。

## 适用场景
- 脚本审查
- 命令复核
- CI 前检查

## 推荐实现边界
- 模式：`pattern_audit` —— 扫描文本或目录中的高风险模式、差异和规则命中。
- 输入：命令文本、脚本文件或目录
- 输出：以 Markdown 为主，强调可审阅、可追踪、可补充。
- 风险控制：优先输出替代与审查意见，不执行命令。

## 安装要求
- `python3`
- 无额外三方依赖
- 建议在支持 `skills/` 目录加载的 OpenClaw 工作区中使用

## 目录结构
- `SKILL.md`：Skill 说明与路由规则
- `README.md`：功能、场景、安装、用法和风险说明
- `SELF_CHECK.md`：本 Skill 的规范与质量自检
- `scripts/run.py`：本地可执行脚本，负责生成或审计结果
- `resources/spec.json`：结构化配置，驱动脚本与模板
- `resources/template.md`：输出模板
- `examples/example-input.md`：示例输入
- `examples/example-output.md`：示例输出
- `tests/smoke-test.md`：冒烟测试步骤

## 触发示例
- 检查这段 shell 命令安不安全
- 识别 pipe-to-shell 和 rm 风险

## 输入输出示例
### 输入侧重点
- 危险模式
- 中风险模式
- 背景说明

### 本地命令
```bash
python3 scripts/run.py --input examples/example-input.md --output out.md
```

### 预期输出
- 结构化 Markdown
- 明确的待确认项
- 面向当前场景的下一步建议

## 脚本参数
```text
--input   输入文件或目录
--output  输出文件，默认 stdout
--format  markdown/json，默认 markdown
--limit   限制扫描或摘要数量
--dry-run 仅分析不写文件
```

## 常见问题
**问：这个 Skill 会直接修改外部系统吗？**  不会，默认只生成草案、清单或只读审计结果。
**问：没有 shell/exec 工具还能用吗？**  可以，Skill 会直接按模板产出文本结果。
**问：脚本依赖什么？**  只依赖 `python3` 和 Python 标准库。

## 风险提示
- 仅使用本地输入内容，不联网补事实。
- 默认不删除、不写外部系统、不发消息、不发布。
- 若输入含个人信息或敏感材料，建议先脱敏再处理。
