# 工作坊议程设计师

## 功能
把会议目标、参会人、时间与约束拆成可执行议程、分段脚本、产出物与会后跟进。

## 适用场景
- 工作坊设计
- 客户共创会
- 内部对齐会

## 推荐实现边界
- 模式：`structured_brief` —— 把输入材料整理成结构化 Markdown 成品。
- 输入：会议目标、参与者、时长、已知冲突点
- 输出：以 Markdown 为主，强调可审阅、可追踪、可补充。
- 风险控制：不会自动发出邀请，也不会修改日历。

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
- 为 90 分钟跨团队 workshop 设计议程
- 把目标和参与者整理成工作坊 runbook

## 输入输出示例
### 输入侧重点
- 目标与成功标准
- 议程分段
- 主持提示

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
