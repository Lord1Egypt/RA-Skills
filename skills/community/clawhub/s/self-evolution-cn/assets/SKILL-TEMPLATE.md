# 技能模板

从学习记录中提取技能的模板。复制并自定义。

---

## SKILL.md 模板

```markdown
---
name: skill-name-here
description: "简洁描述何时以及为什么使用此技能。包括触发条件。"
---

# 技能名称

简要介绍解释此技能解决的问题及其起源。

## 快速参考

| 情况 | 操作 |
|------|------|
| [触发 1] | [操作 1] |
| [触发 2] | [操作 2] |

## 背景

为什么这个知识很重要。它防止什么问题。原始学习的上下文。

## 解决方案

### 分步说明

1. 第一步，包含代码或命令
2. 第二步
3. 验证步骤

### 代码示例

\`\`\`language
// 演示解决方案的示例代码
\`\`\`

## 常见变体

- **变体 A**：描述和处理方法
- **变体 B**：描述和处理方法

## 注意事项

- 警告或常见错误 #1
- 警告或常见错误 #2

## 相关

- 相关文档的链接
- 相关技能的链接

## 来源

从学习记录中提取。
- **学习 ID**：LRN-YYYYMMDD-XXX
- **原始类别**：correction | insight | knowledge_gap | best_practice
- **提取日期**：YYYY-MM-DD
```

---

## 最小模板

对于不需要所有部分的简单技能：

```markdown
---
name: skill-name-here
description: "此技能的作用以及何时使用它。"
---

# 技能名称

[一句话的问题陈述]

## 解决方案

[直接解决方案，包含代码/命令]

## 来源

- 学习 ID：LRN-YYYYMMDD-XXX
```

---

## 带脚本的模板

对于包含可执行帮助程序的技能：

```markdown
---
name: skill-name-here
description: "此技能的作用以及何时使用它。"
---

# 技能名称

[介绍]

## 快速参考

| 命令 | 目的 |
|------|------|
| `./scripts/helper.sh` | [它的作用] |
| `./scripts/validate.sh` | [它的作用] |

## 使用方法

### 自动化（推荐）

\`\`\`bash
./skills/skill-name/scripts/helper.sh [args]
\`\`\`

### 手动步骤

1. 步骤一
2. 步骤二

## 脚本

| 脚本 | 描述 |
|------|------|
| `scripts/helper.sh` | 主要工具 |
| `scripts/validate.sh` | 验证检查器 |

## 来源

- 学习 ID：LRN-YYYYMMDD-XXX
```

---

## 命名约定

- **技能名称**：小写，空格用连字符
  - 好的：`docker-m1-fixes`、`api-timeout-patterns`
  - 不好的：`Docker_M1_Fixes`、`APITimeoutPatterns`

- **描述**：以动作动词开头，提及触发条件
  - 好的："处理 Apple Silicon 上的 Docker 构建失败。当构建因平台不匹配而失败时使用。"
  - 不好的："Docker 东西"

- **文件**：
  - `SKILL.md` - 必需，主要文档
  - `scripts/` - 可选，可执行代码
  - `references/` - 可选，详细文档
  - `assets/` - 可选，模板

---

## 提取检查清单

从学习创建技能之前：

- [ ] 学习已验证（状态：resolved）
- [ ] 解决方案广泛适用（不是一次性）
- [ ] 内容完整（包含所有需要的上下文）
- [ ] 名称遵循约定
- [ ] 描述简洁但信息丰富
- [ ] 快速参考表可操作
- [ ] 代码示例已测试
- [ ] 记录了来源学习 ID

创建之后：

- [ ] 使用 `promoted_to_skill` 状态更新原始学习
- [ ] 将 `Skill-Path: skills/skill-name` 添加到学习元数据
- [ ] 通过在新会话中阅读来测试技能
