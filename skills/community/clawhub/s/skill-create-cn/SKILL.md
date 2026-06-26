---
name: create-skill
description: "在需要新建或优化技能、判断复用还是重建、并生成最小可用技能文件时使用。"
metadata: { "openclaw": { "emoji": "🎨" } }
---

# Skill: 技能创建向导 (create-skill)

用于高效创建或优化技能，优先避免重复建设，并保持产物最小可用。

## 何时使用

- 需要创建新技能（如“创建技能”“新建 skill”“写 SKILL.md”）
- 需要优化已有技能（结构混乱、触发词不清、描述不聚焦）
- 不确定应“扩展已有技能”还是“全新创建”
- 需要最小可用产物（默认仅 `SKILL.md`，必要时再加脚本）

## 常见触发词

- 创建技能
- 新建技能
- create-skill
- skill create
- 优化技能
- 重写 SKILL.md
- 复用已有技能

## 执行清单

1. **搜索相似技能**
   - 基于关键词查找同类能力，避免重复造轮子。
   - 给出候选技能和复用点（可继承的触发词、结构、示例）。

2. **选择创建策略**
   - `扩展已有技能`：已有技能覆盖 60% 以上需求时优先使用。
   - `全新创建`：现有技能不匹配核心场景时使用。
   - `取消创建`：若已有技能可直接满足需求，则停止创建并给出使用指引。

3. **收集最小必要信息**
   - 技能名（`name`，小写连字符）
   - 场景描述（`description`，只写“何时使用”）
   - 触发词（3-8 个）
   - 输出目标（仅文档 / 文档+脚本）

4. **生成文件**
   - 生成区域：skill只在 工作目录/skills 下生成
   - 默认生成：`SKILL.md`
   - 仅当确有必要时再生成 `*.js` 或 `*.sh`
   - 如使用脚本并需要依赖，再补 `package.json`

5. **输出后续建议**
   - 提供如何验证触发效果
   - 提供如何继续迭代（补示例、补反例、补边界）

## 输出标准

- **优先精简**：默认只产出 `SKILL.md`
- **描述聚焦**：`description` 仅描述触发条件，不写执行流程
- **结构清晰**：至少包含“何时使用 / 执行清单 / 输出标准”
- **可复用**：优先复用已有技能，而非重复创建
- **可验证**：提供最少 1 组触发词验证方式

## 最佳实践

- 先搜索后创建，避免功能重叠
- 优先扩展，再考虑新建
- 文档先行，脚本后置
- 触发词要覆盖同义表达
- 每次改动后做一次触发验证

### OpenClaw YAML Frontmatter 规范
每个技能建议包含标准 YAML frontmatter：

```yaml
---
name: skill-name
description: "在......场景下使用"
homepage: https://example.com (可选)
metadata: { "openclaw": { "emoji": "🎨", "requires": { "bins": ["node"] } } }
---
```

**核心字段**：
- `name`: 技能名称（小写，用连字符连接）
- `description`: 使用场景描述（建议 50 字以内）
- `homepage`: 相关主页URL（可选）
- `metadata.openclaw`: OpenClaw元数据
  - `emoji`: 技能表情符号（如🎨、📊、⚡等）
  - `requires`: 依赖要求
    - `bins`: 需要的二进制文件（如`node`、`bash`、`curl`）
    - `node_modules`: 需要的npm包
    - `env`: 需要的环境变量

**示例**：
- 文档指导型：`metadata: { "openclaw": { "emoji": "📚" } }`
- Node.js技能：`metadata: { "openclaw": { "emoji": "⚡", "requires": { "bins": ["node"] } } }`
- Shell技能：`metadata: { "openclaw": { "emoji": "🐚", "requires": { "bins": ["bash"] } } }`

## 快速自检

- `name` 是否为小写连字符格式
- `description` 是否只描述“何时使用”
- 是否已提供 3-8 个触发词
- 是否默认只生成了 `SKILL.md`
- 是否明确说明何时需要脚本文件