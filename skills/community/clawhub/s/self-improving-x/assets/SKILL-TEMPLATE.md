# 技能模板

从学习内容创建技能的模板。复制并自定义。

---

## SKILL.md 模板

```markdown
---
name: skill-name-here
description: "关于何时以及为何使用此技能的简洁描述。包括触发条件。"
---

# 技能名称

简要介绍此技能解决的问题及其来源。

## 快速参考

| 场景 | 操作 |
|-----------|--------|
| [触发 1] | [操作 1] |
| [触发 2] | [操作 2] |

## 背景

为什么这些知识很重要。它防止什么问题。来自原始学习内容的上下文。

## 解决方案

### 步骤

1. 带代码或命令的第一步
2. 第二步
3. 验证步骤

### 代码示例

\`\`\`language
// 演示解决方案的示例代码
\`\`\`

## 常见变体

- **变体 A**: 描述及如何处理
- **变体 B**: 描述及如何处理

## 陷阱

- 警告或常见错误 #1
- 警告或常见错误 #2

## 相关

- 相关文档链接
- 相关技能链接

## 来源

从学习条目中提取。
- **学习 ID**: LRN-YYYYMMDD-XXX
- **原始类别**: correction | insight | knowledge_gap | best_practice
- **提取日期**: YYYY-MM-DD
```

---

## 最小模板

对于不需要所有部分的简单技能：

```markdown
---
name: skill-name-here
description: "此技能的作用及何时使用。"
---

# 技能名称

[一句话的问题陈述]

## 解决方案

[直接解决方案及代码/命令]

## 来源

- 学习 ID: LRN-YYYYMMDD-XXX
```

---

## 带脚本的模板

对于包含可执行辅助工具的技能：

```markdown
---
name: skill-name-here
description: "此技能的作用及何时使用。"
---

# 技能名称

[介绍]

## 快速参考

| 命令 | 用途 |
|---------|---------|
| `./scripts/helper.sh` | [它的作用] |
| `./scripts/validate.sh` | [它的作用] |

## 使用

### 自动化（推荐）

\`\`\`bash
./skills/skill-name/scripts/helper.sh [args]
\`\`\`

### 手动步骤

1. 第一步
2. 第二步

## 脚本

| 脚本 | 描述 |
|--------|-------------|
| `scripts/helper.sh` | 主要工具 |
| `scripts/validate.sh` | 验证检查器 |

## 来源

- 学习 ID: LRN-YYYYMMDD-XXX
```

---

## 命名约定

- **技能名称**: 小写，空格用连字符
  - 好: `docker-m1-fixes`、`api-timeout-patterns`
  - 坏: `Docker_M1_Fixes`、`APITimeoutPatterns`

- **描述**: 以动作动词开头，提到触发条件
  - 好: "处理 Apple Silicon 上的 Docker 构建失败。当构建因平台不匹配而失败时使用。"
  - 坏: "Docker 东西"

- **文件**:
  - `SKILL.md` - 必需，主要文档
  - `scripts/` - 可选，可执行代码
  - `references/` - 可选，详细文档
  - `assets/` - 可选，模板

---

## 提取检查清单

从学习内容创建技能之前：

- [ ] 学习内容已验证（状态: resolved）
- [ ] 解决方案广泛适用（不是一次性的）
- [ ] 内容完整（有所有需要的上下文）
- [ ] 名称符合约定
- [ ] 描述简洁但有信息量
- [ ] 快速参考表可操作
- [ ] 代码示例已测试
- [ ] 来源学习 ID 已记录

创建后：

- [ ] 用 `promoted_to_skill` 状态更新原始学习内容
- [ ] 在学习元数据中添加 `技能路径: skills/skill-name`
- [ ] 在新会话中测试技能以确保它是独立的
