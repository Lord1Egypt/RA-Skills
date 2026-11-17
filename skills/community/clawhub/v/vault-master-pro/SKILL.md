---
slug: vault-master-pro
name: vault-master-pro
version: "1.0.0"
displayName: 知识库大师
summary: 解决多库混乱、移动即断链、附件散落、找不到笔记痛点，让Obsidian知识库井井有条
license: MIT
description: |-
  Obsidian 知识库（vault）管理专家，基于 `obsidian-cli` 操作本地 Markdown 笔记。聚焦多库管理、
  安全重构（移动/改名不断链）、附件治理、跨库搜索，让笔记系统长期保持井井有条。

  核心能力:
  - 多库发现与切换：自动识别系统中的所有 vault，按需切换默认库
  - 安全重构：`move`/`rename` 自动更新所有 `[[wikilinks]]` 与 Markdown 链接
  - 附件治理：扫描游离附件、按规则归位、清理孤儿文件
  - 跨库搜索：标题搜索 + 全文搜索 + 上下文片段
  - 批量操作模板：批量改名、批量打标签、批量归档

  适用场景:
  - 个人知识库长期维护（避免越用越乱）
  - 工作/个人多库切换管理
  - 重构笔记结构而不破坏链接
  - 定期清理无主附件与孤儿笔记

  差异化:
  - 多库发现 + 切换流程，原版只给单库操作
  - 附件治理（扫描/归位/清理孤儿），原版未涉及
  - 批量操作模板，原版只给单条命令
  - 重构安全检查清单，原版只提"会更新链接"

  触发关键词: obsidian, vault, 知识库, 笔记, wikilink, 移动, 重命名, 附件, 双链, mocs
tags:
- 自动化
- 知识管理
- 笔记工具
tools:
- read
- exec
---

# 知识库大师

把 Obsidian vault 当作一个长期演进的知识系统来管，而非散乱文件夹。基于 `obsidian-cli` 完成多库管理、安全重构、附件治理与跨库搜索。

## Vault 模型

Obsidian vault = 普通磁盘文件夹。典型结构：

| 路径 | 内容 | 是否脚本可改 |
|:-----|:-----|:-------------|
| `*.md` | Markdown 笔记 | 是 |
| `.obsidian/` | 工作区 + 插件配置 | 通常不动 |
| `*.canvas` | 画板（JSON） | 谨慎改 |
| `<attachments>/` | 附件目录（设置中指定） | 是 |

## 多库发现与切换

Obsidian 桌面端在以下位置记录所有 vault（真相源）：

- macOS: `~/Library/Application Support/obsidian/obsidian.json`
- Windows: `%APPDATA%/obsidian/obsidian.json`
- Linux: `~/.config/obsidian/obsidian.json`

`obsidian-cli` 从该文件解析，vault 名通常是文件夹名（路径后缀）。

**多库发现**（不要猜，读配置）：

```bash
# 已设默认库
obsidian-cli print-default --path-only

# 未设默认 → 读 obsidian.json，取 "open": true 的条目
# 多库常见：iCloud vs ~/Documents、工作 vs 个人
```

**切换默认库**：

```bash
obsidian-cli set-default "<vault-folder-name>"
obsidian-cli print-default            # 确认当前默认
```

**禁止**把库路径硬编码进脚本；优先读配置或用 `print-default`。

## 快速开始

```bash
# 1. 发现库
obsidian-cli print-default --path-only

# 2. 切到目标库（如需要）
obsidian-cli set-default "my-knowledge"

# 3. 搜索
obsidian-cli search "项目管理"
obsidian-cli search-content "OKR"

# 4. 创建
obsidian-cli create "Projects/新项目" --content "# 新项目" --open

# 5. 安全移动（自动更新双链）
obsidian-cli move "old/path/note" "new/path/note"

# 6. 删除
obsidian-cli delete "path/note"
```

简单编辑可直接改 `.md` 文件，Obsidian 会自动同步。

## 安全重构（移动/改名不断链）

`obsidian-cli move` 是相对 `mv` 的核心优势：自动更新 vault 内所有 `[[wikilinks]]` 与 Markdown 链接。

### 重构前安全检查清单

- [ ] 已备份 vault（或用 Git）
- [ ] 当前无其他编辑器打开目标笔记（避免冲突）
- [ ] 记录原路径与新路径（便于回滚）
- [ ] 全文搜索确认无硬编码路径引用

### 批量重构模板

```bash
# 把 Notes/ 下所有笔记移到 Inbox/，自动更新链接
for note in Notes/*.md; do
  name=$(basename "$note" .md)
  obsidian-cli move "Notes/$name" "Inbox/$name"
done

# 批量改名：旧名 → 新名（从 CSV）
# rename.csv: old_name,new_name
tail -n +2 rename.csv | while IFS=, read -r old new; do
  obsidian-cli move "$old" "$new"
done
```

## 附件治理

附件散落是长期使用 vault 的头号痛点。提供三步治理：

### 1. 扫描游离附件

```bash
# 列出未被任何笔记引用的附件
scripts/orphan-scan --vault "<vault-path>" --attachments "Attachments"
# 输出：orphan-attachments.csv，含文件路径、大小、最后修改时间
```

### 2. 按规则归位

```bash
# 把图片归到 Attachments/Images/，PDF 归到 Attachments/PDF/
scripts/organize-attachments --vault "<vault-path>" \
  --rule "image:Attachments/Images" \
  --rule "pdf:Attachments/PDF" \
  --rule "audio:Attachments/Audio"
```

### 3. 清理孤儿

```bash
# 删除连续 90 天未被引用的附件（先 dry-run）
scripts/clean-orphans --vault "<vault-path>" --days 90 --dry-run
scripts/clean-orphans --vault "<vault-path>" --days 90   # 实删
```

## 跨库搜索

| 命令 | 用途 |
|:-----|:-----|
| `obsidian-cli search "query"` | 按笔记名搜索 |
| `obsidian-cli search-content "query"` | 全文搜索，返回片段与行号 |
| `scripts/cross-vault-search "query"` | 跨多个 vault 同时搜索（自定义脚本） |

跨库搜索示例：

```bash
scripts/cross-vault-search "OKR" --vaults work,personal
# 输出：每个 vault 的命中笔记 + 片段
```

## 创建笔记

```bash
obsidian-cli create "Folder/New note" --content "..." --open
```

**注意**：
- 依赖 Obsidian URI handler（`obsidian://...`），需 Obsidian 已安装
- 避免在隐藏 dot-folder 下创建（如 `.something/...`），Obsidian 可能拒绝
- 复杂内容建议先写文件再用 `--content-file`（若 CLI 支持）或直接写 `.md`

## 真实场景示例

### 场景1：季度知识库整理

```
用户：把上季度的项目笔记归档到 Archive/
执行：
1. 全文搜索"Q3 项目"
2. 批量 move 命中笔记到 Archive/2025-Q3/
3. 附件治理：扫描游离附件 → 归位 → 清理 90 天孤儿
4. 报告：归档 23 篇，整理附件 47 个，清理孤儿 8 个
```

### 场景2：重命名核心概念

```
用户：把所有"双钻模型"改成"Double Diamond"
执行：
1. search-content "双钻模型" → 列出所有命中笔记
2. 逐个 move（如有以概念命名的笔记）+ 全文替换
3. 验证双链未断：search "双钻模型" 应返回 0
4. 报告：改名 12 篇，更新链接 34 处
```

### 场景3：工作/个人库切换

```
用户：从个人库切到工作库
执行：
1. set-default "work-vault"
2. print-default 确认
3. search "本周会议"
```

### 场景4：附件大扫除

```
用户：vault 越来越大，清理无用附件
执行：
1. orphan-scan → 发现 156 个游离附件（占 1.2GB）
2. organize-attachments 按类型归位
3. clean-orphans --days 90 --dry-run → 预览删除 89 个
4. 用户确认后 clean-orphans --days 90
5. 报告：释放 780MB，保留 67 个近期附件
```

## FAQ

**Q1: 移动笔记后双链断了怎么办？**
A: `obsidian-cli move` 应自动更新。若仍断：检查是否有"硬编码路径"引用（如 `[[folder/note]]` 全路径）；用 `search-content` 找残留引用并手动修复。

**Q2: 多库切换会丢配置吗？**
A: 不会。每个 vault 的 `.obsidian/` 独立，切换只改默认指向。插件、主题、工作区都保留。

**Q3: 附件扫描误报怎么办？**
A: `orphan-scan` 可能漏判被 `![[image]]` 嵌入的附件。先 `--dry-run` 预览，对可疑项手动确认。可在脚本中加白名单。

**Q4: 跨库搜索慢吗？**
A: 取决于库大小。万级笔记约 5-10 秒。建议加 `--limit` 限制每库返回数。

**Q5: 可以在 Obsidian 未运行时操作吗？**
A: `move`/`delete`/`search` 直接操作磁盘，不需要 Obsidian 运行。`create --open` 需要 URI handler，需 Obsidian 运行。建议操作时关闭 Obsidian 避免冲突，操作完再打开。

## 故障排查

| 现象 | 排查路径 |
|:-----|:---------|
| `print-default` 返回空 | 未设默认 → 读 obsidian.json 找 `"open": true` 的条目 |
| `create --open` 无反应 | Obsidian 未运行 → 启动 → 检查 URI handler 关联 |
| `move` 后链接未更新 | 检查链接是否为非标准格式 → 手动修复 → 反馈 CLI |
| 搜索结果不全 | 检查 `.obsidian/` 排除规则 → 暂时移除排除项再搜 |
| 附件扫描报权限错 | 检查文件夹读写权限 → macOS 给终端"完全磁盘访问" |
| 多库识别不到 | 检查 obsidian.json 路径 → 手动添加 vault 到 Obsidian |

## 依赖说明

### 运行环境
- **Agent 平台**: 任意支持 SKILL.md 的 AI Agent
- **操作系统**: Windows / macOS / Linux
- **Obsidian**: 桌面版（用于 URI handler 与配置文件）

### 第三方依赖
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-------|:-----|:---------|:---------|
| `obsidian-cli` | 命令行工具 | 必需 | npm / 官方仓库 |
| Obsidian 桌面版 | 软件 | 推荐（URI handler） | obsidian.md 下载 |
| `jq` | JSON 处理 | 可选 | 系统包管理器 |
| LLM API | API | 必需 | 由 Agent 内置 LLM 提供 |

### API Key 配置
- 无需 API Key
- 自定义脚本（`orphan-scan`、`cross-vault-search`）需要文件系统读写权限

### 可用性分类
- **分类**: MD+EXEC（Markdown 指令 + 必须通过 exec 执行 `obsidian-cli` 与自定义脚本）
- **说明**: 基于自然语言指令驱动 Agent 管理知识库，含多库切换、安全重构、附件治理
