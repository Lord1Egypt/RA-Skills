---
name: skill-editor
description: "编辑、完善或审查 AgentSkills。当需要创建新技能、对现有 SKILL.md 进行修改、清理/审计/整理技能文件时激活此技能。触发词：编辑技能, skill 注意事项, metadata 检查, 完善技能, 清理技能, 审计技能, skill 规范, 编写 skill, 新建技能"
metadata:
  version: 1.2.4
  author: lejian
  homepage: https://clawhub.ai/skills/skill-editor
  tags:
    - skill
    - editor
    - openclaw
  openclaw:
    requires:
      env.vars: {}
---

# Skill Editor

编辑和完善 AgentSkills 的指南。创建或修改技能时参考此指南。

## 目录结构

```
skills/<skill-name>/
├── SKILL.md          # 必须：技能定义文件
├── package.json      # 必须（publish 时需要 displayName 等元信息）
├── scripts/          # 可选：脚本文件
└── references/       # 可选：参考文档
```

**不要**创建额外的文档文件（README.md、CHANGELOG.md 等）。

---

## Frontmatter 必检清单

每次编辑 SKILL.md 时，**必须**检查以下字段是否正确：

### 必要字段一览

| 字段 | 要求 | 常见错误 |
|------|------|----------|
| `name` | kebab-case，与目录名一致 | 写成驼峰、大小写不匹配目录名 |
| `description` | 触发条件描述，含中英文关键词，100 字左右 | 太短（无触发词）、太长（超过 200 字） |
| `metadata` | 顶级字段，与 name、description 平级 | 缺失、缩进错误、嵌套在 description 下 |
| `requires.env.vars` | 脚本依赖的环境变量必须声明，不能只写在正文 | 脚本用了变量但 `requires.env.vars` 为空或漏填 |

---

### metadata 块（必须存在）

**结构**：

```yaml
metadata:
  version: 1.0.0
  author: <作者名>
  homepage: <技能主页 URL>
  tags:
    - <标签1>
    - <标签2>
  openclaw:
    requires:
      env.vars: {}   # 无依赖时必须写空对象，不能省略
```

**关键规则**：

1. `metadata` 是顶级字段，与 `name`、`description` 平级
2. `openclaw.requires.env.vars` 填写脚本依赖的环境变量（如 API Token）
3. 没有环境变量依赖时，`requires.env.vars` 写空对象 `{}`，**不能省略 `openclaw.requires` 块**

---

### package.json（publish 时必须保留）

发布到 ClawHub 需要 package.json 中的 `displayName` 等元信息。

**典型结构**：

```json
{
  "name": "skill-name",
  "version": "1.0.0",
  "displayName": "技能显示名称",
  "description": "技能一句话描述"
}
```

**编辑时注意事项**：
- 不要删除或覆盖 package.json
- 改完 SKILL.md 后检查 package.json 是否仍然完整

> ⚠️ **clawhub publish 不会自动读取 package.json 的 displayName**，必须通过 `--name` 显式传入。如果只传 `--version` 不传 `--name`，clawhub 会使用 package.json 中的 `name` 字段而非 `displayName`，导致发布后显示的名称不正确。

---

## 正确示例

**无环境变量依赖**：

```yaml
---
name: my-skill
description: "我的技能描述"
metadata:
  version: 1.0.0
  author: lejian
  homepage: https://clawhub.ai/skills/my-skill
  tags:
    - my-skill
  openclaw:
    requires:
      env.vars: {}
---
```

**有环境变量依赖**：

```yaml
---
name: my-api-skill
description: "调用外部 API 的技能"
metadata:
  version: 1.0.0
  author: lejian
  homepage: https://clawhub.ai/skills/my-api-skill
  tags:
    - api
  openclaw:
    requires:
      env.vars:
        MY_API_TOKEN: "API Token，说明配置方式"
        LEJIAN_AUTH_TOKEN: "乐荐 API Token，配置方式：openclaw config set env.vars.LEJIAN_AUTH_TOKEN <token>"
---
```

---

## 常见错误

❌ `metadata` 缩进错误（嵌套在 description 下面）或字段缺失
❌ `requires.env.vars` 写成空对象 `{}`，但实际脚本有环境变量依赖
❌ `requires` 写成 `require` 或其他拼写
❌ 只在正文写"需要配置 API Token"，但 `requires.env.vars` 为空
❌ 环境变量名与脚本中实际使用的名字不一致
❌ 编辑 SKILL.md 时覆盖/删除了 package.json（publish 时丢 displayName）
❌ `description` 缺少触发词，导致 skill 无法被正确激活

---

## 编辑现有技能时的检查项

> 💡 建议先加载 `skill-creator` 技能了解编辑流程，但这不是强制要求，可以直接编辑 skill 文件。

1. **修改 `description`** — 确认触发词仍然准确，保留中英文关键词
2. **修改 `name`** — 同时修改目录名，保持一致
3. **新增环境变量依赖** — 同时在 `metadata.openclaw.requires.env.vars` 中声明
4. **version 更新** — 如有实质性变更，版本号 +0.0.1
5. **删除环境变量依赖** — 从 `requires.env.vars` 中移除对应条目
6. **检查 package.json** — 确保 displayName、version 等字段没有在编辑时被覆盖
7. **版本一致性** — 修改 version 后，**必须确保 SKILL.md metadata.version 和 package.json version 完全一致**，否则 clawhub 发布后会显示旧版本
8. **发布时** — clawhub publish 的 `--version` 参数也必须与上述两处版本号保持一致，三者缺一不可

---

## 常见问题处理

### 忘记加 metadata

在 `description` 行**之后**、`---` 行**之前**插入 metadata 块：

```python
pattern = r'(description: [^\n]+\n)(\n---\n# )'
replacement = r'\1metadata:\n  version: 1.0.0\n  author: lejian\n  homepage: ...\n  tags:\n    - xxx\n  openclaw:\n    requires:\n      env.vars: {}\n\2'
```

### 检查所有 skill 的 metadata 完整性

```bash
find ~/workspace/agent/skills -name "SKILL.md" | while read f; do
  if grep -q "^metadata:" "$f"; then
    echo "✅ $f"
  else
    echo "❌ $f (missing metadata)"
  fi
done
```

### 查找所有 skills 目录

```
~/workspace/agent/skills/                  # 用户安装的 skill
~/workspace/agent/extensions/*/skills/     # 扩展自带的 skill
~/.npm-global/lib/node_modules/openclaw/skills/  # 内置 skill
```