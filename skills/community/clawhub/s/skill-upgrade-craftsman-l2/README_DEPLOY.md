# 技能升级巧匠 L2 - 部署包

## 📦 包含内容

- `SKILL.md`：核心技能文件，含 frontmatter（name / description / trigger），可直接部署到支持 Skill 格式的平台（如 Trae IDE）；也可将其正文内容复制到 Coze / Dify 的 Prompt 编排区使用。
- `TEST_PROMPTS.md`：6 道覆盖五机制会诊、分流判断、去打架、衔接契约和完整交付的测试题。
- `README_DEPLOY.md`：本部署说明。

## 🚀 部署步骤

### 方式 A：部署到 Trae IDE（推荐）

将整个 `技能升级巧匠L2/` 目录复制到目标项目的 `.trae/skills/` 下即可。系统会自动读取 `SKILL.md` 的 frontmatter 完成注册。

### 方式 B：部署到 Coze / Dify 等平台

1. 创建一个新的 Agent，命名为"技能升级巧匠 L2"。
2. 将 `SKILL.md` 中 `---` 之后（从 `# 技能升级巧匠 L2` 开始）的正文内容，完整复制到 Agent 的 Prompt 编排区。
3. 配置一个大语言模型（推荐 Claude-3.5-Sonnet 或 GPT-4o）。
4. 在右侧预览区，复制 `TEST_PROMPTS.md` 中的测试题 1 发送给 Agent。
5. 观察 Agent 是否先做五机制会诊，而不是直接改写。

## L1 和 L2 的关系

| | L1 | L2 |
|:---|:---|:---|
| 输入 | 任何质量的 Prompt / Skill 草稿 | 已有基础结构但不够稳定的 Skill |
| 目标 | 较稳可用 | A 级可用 |
| 核心动作 | 接包诊断 → 基础改造 | 五机制会诊 → 系统化升级 |

建议用法：

- 拿到一个全新草稿 → 先用 L1
- 拿到一个已有 Skill 但调不对/接不上/会打架 → 用 L2
- 不确定该用哪个 → 先用 L1 做基础诊断，L1 会自动建议是否该进入 L2

## ⚠️ 注意事项

- L2 假定输入 Skill 已经具备基本结构（有 frontmatter、有 workflow 雏形）
- 如果输入只是一段纯文本 prompt，L2 会建议先回 L1
- L2 不会假装平台能做到"自动联动"，统一写成"推荐下一步"
