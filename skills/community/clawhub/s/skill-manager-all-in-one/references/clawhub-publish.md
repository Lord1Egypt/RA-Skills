# ClawHub Publish Reference | ClawHub 发布参考

> 本文件是 SKILL.md 的发布操作补充，承上启下。两步验证的完整原则见 SKILL.md Phase 2 步骤 2。

---

## 发布前检查（两步验证第一步）

### A. 完整清单核对

对照 SKILL.md 第 6 章【统一检查清单】逐项执行：

**通用质量基线（G01-G06）+ ClawHub 专项（CH01-CH12）**逐项标注 ✅ / ⚠️。

### B. 脚本安全检查（如技能含 Python/Bash 等脚本）

| 检查要点 | 说明 |
|---------|------|
| 输入校验 | 用户输入是否经过验证和过滤，避免直接拼接到命令或路径中 |
| 权限最小化 | 是否遵循最小权限原则，无过度权限申请 |
| 凭据保护 | API Key、Token 等敏感信息不出现在日志、报错、返回值中 |
| 依赖完整性 | 代码 import 的包是否全部出现在 requirements.txt / package.json 中 |

### C. 文件大小检查

```bash
du -sh <skill-dir>
```

**超过 50MB 必须处理：**
- 立即报告用户
- 将模型/大文件临时移出，等待上传成功后再移回
- 等待用户明确指示后再操作

### D. 对外表述检查（ClawHub 目标）

- `name`：先英文后中文，`EN Title | 中文标题`
- `description`：先英文后中文，≤150字符，英文短句在前
- Changelog：先英文后中文，数字列表，正式语气
- README 关键标题：先英文后中文

### E. 拟定 Changelog

通过 `--changelog "..."` 参数传入，不写在 SKILL.md 里：

```
1. [English update]. [中文更新]。
2. [English update]. [中文更新]。
```

---

## 第二步用户汇报内容（必须全部列出）

| 汇报项 | 内容 |
|--------|------|
| Display name | 双语格式 `EN Title | 中文标题` |
| Skill slug | 小写字母 + 连字符 |
| description | 先英文后中文，≤150字符 |
| 目标平台 | ClawHub |
| 当前版本 | 来自 `clawhub inspect <slug>` |
| 新版本号 | 在已发布版本上递增 |
| Changelog | 完整英中文双语内容 |
| 文件大小 | 超过50MB需特别标注 |
| 核对清单结果 | G01-G06 + CH01-CH12，逐项 ✅ / ⚠️ |
| 有⚠️项时的问题与解决方案 | 说明问题 + 修复方案 |
| **发布命令** | `clawhub publish ...` 完整命令 |

**⚠️ 确认前不得执行任何发布类命令。确认标志：用户回复「确认-<username>」。**

---

## CLI 命令

优先使用 PATH 中的 `clawhub`。若不存在，先尝试 OpenClaw 托管路径：

```bash
CLAWHUB_BIN=$(command -v clawhub || true)
if [ -z "$CLAWHUB_BIN" ] && [ -x "$HOME/.openclaw/tools/node/npm/bin/clawhub" ]; then
  CLAWHUB_BIN="$HOME/.openclaw/tools/node/npm/bin/clawhub"
fi
[ -n "$CLAWHUB_BIN" ] || { echo "clawhub command not found"; exit 1; }
```

### 发布命令

```bash
"$CLAWHUB_BIN" publish <path> \
  --slug <slug> \
  --name "EN Title | 中文标题" \
  --version <version> \
  --changelog "<text>"
```

**⚠️ 双语展示名必须显式传 `--name`，不能只依赖 _meta.json 或 SKILL.md 自动同步。**

### 管理命令

```bash
"$CLAWHUB_BIN" delete <slug> --yes    # 软删除（两步验证后才可执行）
"$CLAWHUB_BIN" hide <slug> --yes     # 隐藏（两步验证后才可执行）
"$CLAWHUB_BIN" unhide <slug> --yes   # 恢复
"$CLAWHUB_BIN" undelete <slug> --yes  # 取消删除
"$CLAWHUB_BIN" sync
```

> `--yes` 是 CLI 必需参数。所有破坏性操作均要求用户先通过两步验证。

### Inspect 命令

```bash
"$CLAWHUB_BIN" inspect <slug>                              # 基本信息
"$CLAWHUB_BIN" inspect <slug> --tag latest                # 最新版本
"$CLAWHUB_BIN" inspect <slug> --version X.Y.Z              # 指定版本
"$CLAWHUB_BIN" inspect <slug> --versions --limit 20       # 版本历史
"$CLAWHUB_BIN" inspect <slug> --files                     # 文件列表
"$CLAWHUB_BIN" inspect <slug> --file SKILL.md             # 查看文件内容
"$CLAWHUB_BIN" inspect <slug> --json                      # 元数据 JSON
```

### 登录状态

```bash
"$CLAWHUB_BIN" whoami              # 确认登录状态
"$CLAWHUB_BIN" login               # 未登录时执行
```

---

## 核心规则要点

### Display name 双保险

ClawHub 页面标题由发布记录的 display-name 控制。双语名必须两处一致：

1. `SKILL.md` YAML frontmatter：`name: EN Title | 中文标题`
2. 发布命令：`--name "EN Title | 中文标题"`

实测仅改 `name:` 或 `_meta.displayName` 更新版本时，ClawHub 顶部展示名可能不会同步中文。

### ClawHub Summary 规则

本地源字段是 SKILL.md frontmatter `description`。发布后 ClawHub 将其作为 registry `summary` 暴露，CLI 打印为 `Summary:`。

ClawHub 预览区域很短：即使英文在前，只要英文太长，中文仍可能被截断。双语技能应让英文短句在前，中文紧随其后：

```yaml
description: "TTS helper. TTS 朗读助手；支持文本转语音，长文本自动分段。"
```

发布后同时复验 `Latest:` 和 `Summary:`，不要只看版本号。

### 版本冲突

如果发布失败并提示 `Version already exists`，应先与用户确认，再升版本号重新发布。

### 发布后扫描状态

发布后立即 `inspect` 可能提示安全扫描中、技能暂时隐藏。这是临时状态，不是发布失败。短暂等待后再次 inspect，直到能看到最新版本和摘要。

---

## 安全扫描结果查看步骤

1. 打开 ClawHub 技能页面（如 `https://clawhub.ai/<username>/<slug>`）
2. 找到 **Security Scan** 区域
3. 找到 **OpenClaw** 徽章旁边的 **Details ▾** 按钮
4. 点击 **Details ▾** 展开才能看到完整 Assessment（包含 Purpose、Install Mechanism、Credentials 等逐项评估）

⚠️ Summary 只是一句话概括，**必须展开 Details 才能看到完整 Assessment**。

完整汇报格式见 SKILL.md「安全扫描说明」章节的 SOP 模板。

---

*本文件职责：发布操作细节（检查步骤 + 汇报内容 + 命令速查 + 规则要点），配合 SKILL.md 流程骨架使用。*
---

## Inspect 命令参考 | Inspect Reference

### 工具选择原则

**先查 CLI help，再决定用 CLI 还是 Dashboard。** CLI 会持续更新，不要假设某个命令永远不变。

| 场景 | 用 CLI 还是 Dashboard |
|------|----------------------|
| 查看全部已发布技能 | Dashboard |
| 查看卡片摘要 | Dashboard |
| 查看扫描状态和概览 | Dashboard |
| 单个技能详情 | CLI |
| 当前最新版本 | CLI |
| 文件列表 | CLI |
| 元数据直接查询 | CLI |
| 可重复检查 / 脚本化流程 | CLI |

### 常用 Inspect 命令

```bash
clawhub --help              # 先查当前 CLI 行为
clawhub whoami              # 确认登录状态
clawhub inspect <slug>      # 查看单个技能详情
clawhub inspect <slug> --tag latest
clawhub inspect <slug> --version 1.0.0
clawhub inspect <slug> --versions --limit 20
clawhub inspect <slug> --files
clawhub inspect <slug> --file SKILL.md
clawhub inspect <slug> --json
```

### 本地目录 vs CLI list 的区别

手工复制进 `~/.openclaw/workspace/skills/` 的技能，可能本地存在但仍不会出现在 `clawhub list` 中。

- `clawhub list` 是 CLI lockfile 视角，不等于扫描目录下的所有文件夹
- 需要时，两个检查都要做

### 登录说明

浏览器登录和 CLI 登录是两套状态。如果 CLI 提示 `Not logged in`：

```bash
clawhub login
clawhub whoami
```

### 状态含义

| 状态 | 含义 |
|------|------|
| `Scanning` | 安全扫描进行中 |
| `Pending` | 结果尚未完全稳定 |
| `Benign` | 基本通过扫描 |
| `Suspicious` | 需要人工复核 |
| `Hidden` | 当前不公开显示 |

