---
name: wb-to-openclaw
version: 1.0.0
description: |
  WorkBuddy Skill → OpenClaw Skill 格式转换+ClawHub一键发布工具。
  自动将 WorkBuddy 平台的 SKILL.md 适配为 OpenClaw/ClawHub 规范格式，
  校验 frontmatter 字段、slug 规则、文件类型白名单、安全审核一致性，
  完成后直接发布到 ClawHub。

  适用场景：
  - "把这个skill转成OpenClaw格式"（格式转换）
  - "发布skill到ClawHub"（转换+发布）
  - "检查这个skill能不能通过ClawHub审核"（合规校验）
  - "批量转换skill"（多Skill同时处理）
metadata:
  openclaw:
    emoji: "🔄"
    author: "以七"
---

# WB to OpenClaw — Skill 格式转换+发布工具 v1.0.0

> **核心价值：一次转换，双平台可用。**

你是一个 Skill 格式转换专家，负责将 WorkBuddy 平台的 Skill 适配为 OpenClaw/ClawHub 规范格式，并完成发布。

---

## 快速模式识别

| 用户说 | 触发操作 |
|--------|---------|
| "把XX skill转成OpenClaw格式" | 格式转换 |
| "发布XX到ClawHub" | 转换+发布 |
| "检查XX能不能通过ClawHub审核" | 合规校验 |
| "批量转换所有skill" | 批量处理 |

---

## 工作流程

### 完整流程（转换+发布）

```
Step 1: 读取源 Skill
  → 读取 WorkBuddy skill 目录下的 SKILL.md 和所有子文件
  → 识别 frontmatter 字段、正文结构、references/scripts/assets 内容

Step 2: 格式转换
  → 执行 frontmatter 字段映射（见转换规则）
  → 执行正文适配（见正文规则）
  → 复制合法文件到 OpenClaw 目录

Step 3: 合规校验
  → 执行全部校验规则（见校验清单）
  → 输出校验报告
  → 如有问题，自动修复或提示用户

Step 4: 发布到 ClawHub
  → 确认已登录（clawhub whoami）
  → 执行 clawhub publish
  → 处理 slug 冲突、版本号等
  → 输出发布结果
```

### 仅转换（不发布）

执行 Step 1-3，输出适配后的文件到 `~/.openclaw/workspace/skills/<slug>/`。

### 仅校验

执行 Step 3，输出校验报告。

---

## 转换规则

### Frontmatter 字段映射

| WorkBuddy 字段 | OpenClaw 对应 | 转换操作 |
|---------------|--------------|---------|
| `name` | `name` | 直接保留 |
| `version` | `version` | 直接保留（必须 semver） |
| `description` | `description` | 直接保留 |
| `agent_created: true` | — | **删除**（OpenClaw 无此字段） |
| `description_zh` | — | **删除**（OpenClaw 无此字段） |
| — | `metadata.openclaw.emoji` | 新增，从 skill 主题推断 |
| — | `metadata.openclaw.author` | 新增，默认"以七"（用户可自定义） |
| — | `metadata.openclaw.homepage` | 新增，如有 GitHub 仓库则填写 |
| — | `metadata.openclaw.requires` | 新增，如 skill 使用了环境变量或外部 CLI |
| — | `metadata.openclaw.envVars` | 新增，如 skill 需要环境变量 |
| — | `metadata.openclaw.os` | 新增，如 skill 仅支持特定 OS |

### 正文适配规则

1. **删除 WorkBuddy 专有工具引用**：
   - `Skill` 工具调用 → 替换为说明文字"使用对应平台工具加载"
   - `SkillManage` → 删除或替换
   - `working_memory` 相关流程 → 替换为"使用文件系统持久化"
   - `TaskCreate/TaskUpdate/TaskList` → 替换为通用任务管理描述

2. **保留通用内容**：
   - 设计原则、工作流、模式识别表 → 直接保留
   - Prompt 模板、结构模板 → 直接保留
   - 代码脚本 → 直接保留（但检查文件类型是否在白名单中）

3. **精简过长的 SKILL.md**：
   - OpenClaw 嵌入上限约 40 个非 .md 文件
   - 如正文超过 500 行，考虑拆分到 references/ 子文件
   - 核心工作流保留在 SKILL.md，详细模板移至 references/

### 文件复制规则

1. `references/*.md` → 直接复制
2. `references/*.yaml` / `*.yml` → 直接复制
3. `references/*.html` → 直接复制（MIME: text/html）
4. `references/*.json` → 直接复制
5. `scripts/*.py` / `*.js` / `*.bat` → 直接复制（文本文件）
6. `assets/*.png` / `*.jpg` → **不复制**（二进制文件不在白名单）
7. 总包大小上限 **50MB**，超限需裁剪

---

## 合规校验清单

### 🔴 必须通过（P0）

| # | 校验项 | 规则 | 修复方式 |
|---|--------|------|---------|
| 1 | SKILL.md 存在 | 目录下必须有 SKILL.md 或 skill.md | 创建 |
| 2 | name 字段 | frontmatter 中必须有 name | 从目录名派生 |
| 3 | version 字段 | 必须符合 semver（X.Y.Z） | 补充默认 1.0.0 |
| 4 | description 字段 | frontmatter 中必须有 description | 从正文第一段提取 |
| 5 | slug 合法 | 小写+数字+连字符，匹配 `^[a-z0-9][a-z0-9-]*$` | 自动转换 |
| 6 | 文件类型白名单 | 所有文件扩展名必须在 TEXT_FILE_EXTENSIONS 白名单中 | 删除不合规文件 |
| 7 | 总包大小 | ≤ 50MB | 裁剪大文件 |
| 8 | 环境变量声明一致性 | 代码中引用的环境变量必须在 frontmatter 中声明 | 补充声明 |

### 🟡 建议通过（P1）

| # | 校验项 | 规则 | 修复方式 |
|---|--------|------|---------|
| 9 | emoji 字段 | metadata.openclaw.emoji 建议填写 | 从 skill 主题推断 |
| 10 | author 字段 | 建议填写 | 默认"以七" |
| 11 | 无 WorkBuddy 专有字段 | 不含 agent_created / description_zh 等 | 删除 |
| 12 | 无 WorkBuddy 专有工具引用 | 正文中不引用 Skill/SkillManage/working_memory | 替换为通用描述 |

### 🟢 可选优化（P2）

| # | 校验项 | 规则 | 修复方式 |
|---|--------|------|---------|
| 13 | homepage 字段 | 建议填写 | 询问用户 |
| 14 | 正文行数 | 建议 ≤ 500 行，超出考虑拆分 | 拆分到 references/ |
| 15 | 非 .md 文件数量 | 建议 ≤ 40 个 | 合并或精简 |

---

## 发布操作指南

### 前置条件

1. **登录 ClawHub**：
   ```bash
   clawhub login                              # 浏览器登录
   clawhub login --token <TOKEN> --no-browser  # Token 登录
   ```
2. **确认登录状态**：`clawhub whoami`

### 发布命令

```bash
clawhub publish <skill目录路径> \
  --version <semver版本号> \
  --name "<显示名称>" \
  --slug <url-safe-slug> \
  --changelog "<更新日志>"
```

### 关键参数说明

| 参数 | 必填 | 说明 |
|------|------|------|
| `--version` | **是** | semver 格式，不从 SKILL.md 读取 |
| `--name` | 否 | 显示名称，默认从 frontmatter 读取 |
| `--slug` | 否 | URL 标识符，默认从目录名派生；冲突时需手动指定 |
| `--changelog` | 否 | 更新日志文本 |
| `--owner` | 否 | 发布到组织/用户名下 |
| `--tags` | 否 | 标签，默认 "latest" |

### 常见问题处理

| 问题 | 原因 | 解决 |
|------|------|------|
| `--version must be valid semver` | 版本号格式错误 | 必须用 X.Y.Z 格式，通过 --version 传入 |
| `Slug is already taken` | slug 被其他开发者占用 | 用 --slug 指定新 slug（加前缀） |
| `Not logged in` | 未登录 | 执行 clawhub login |
| 文件被拒绝 | 二进制文件 | 删除 .png/.jpg 等二进制文件 |

### 发布后验证

```bash
# 查看 Skill 信息
clawhub info <slug>

# 搜索已发布 Skill
clawhub search <关键词>
```

---

## 批量处理模式

当用户说"批量转换所有skill"时：

1. 扫描 `~/.workbuddy/skills/` 下所有子目录
2. 对每个含有 SKILL.md 的目录执行转换
3. 输出转换结果表格：

| Skill | 版本 | Slug | 校验结果 | 发布状态 |
|-------|------|------|---------|---------|
| murder-mystery-creator | 1.8.0 | murder-mystery-creator | ✅ P0全过 | ✅ 已发布 |
| ... | ... | ... | ... | ... |

4. 用户确认后批量执行发布

---

## 注意事项

1. **许可证**：ClawHub 上所有 Skill 默认 MIT-0 许可，不支持自定义许可
2. **付费**：ClawHub 不支持付费 Skill，不要添加定价元数据
3. **slug 永久性**：slug 一旦发布不可更改（除非删除重发）
4. **版本递增**：同 slug 重新发布必须递增版本号
5. **安全审核**：ClawScan 会检查代码行为与 frontmatter 声明是否一致，确保环境变量声明完整

---

## references/ 文件索引

| 文件 | 用途 |
|------|------|
| `openclaw-skill-spec.md` | OpenClaw SKILL.md 格式完整规范（从官方文档提取） |
| `text-file-extensions.txt` | ClawHub 允许的文件扩展名白名单 |
| `conversion-examples.md` | 转换示例：WorkBuddy → OpenClaw 对照 |
