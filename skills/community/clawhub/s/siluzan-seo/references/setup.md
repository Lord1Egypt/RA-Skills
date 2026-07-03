# 安装与配置

## 一键安装（推荐）

构建发布后，`dist/skill/scripts/` 内含与 CSO 同源的安装脚本（构建时注入 `siluzan-seo-cli` / `siluzan-seo` 占位符）：

- **macOS / Linux / WSL：**
  ```bash
  bash <(curl -fsSL https://unpkg.com/siluzan-seo-cli@latest/dist/skill/scripts/install.sh)
  ```
- **Windows PowerShell：**
  ```powershell
  irm https://unpkg.com/siluzan-seo-cli@latest/dist/skill/scripts/install.ps1 | iex
  ```

脚本步骤：Node.js 检测 → 全局安装 `siluzan-seo-cli` → `siluzan-seo init --global --force`。**不执行 login**，也无需 API Key。

测试环境 CLI：`npm install -g siluzan-seo-cli@beta`，脚本中 `INSTALL_CMD` 会随构建环境切换。

---

## 手动安装

```bash
npm install -g siluzan-seo-cli
siluzan-seo init          # 写入当前项目 AI 助手 skill 目录
siluzan-seo init --global # 写入各平台全局 skill 目录
siluzan-seo update        # 升级 CLI 并刷新已安装 skill 文件
```

环境要求：**Node.js 18+**

### `init` 支持的 `--ai` 目标

| 值 | 写入路径 |
|----|---------|
| `cursor` | `.cursor/skills/siluzan-seo/` |
| `claude` | `.claude/skills/siluzan-seo/` |
| `deerflow` | `skills/public/siluzan-seo/` |
| `openclaw` / `openclaw-workspace` | `skills/siluzan-seo/` |
| `openclaw-global` | `~/.openclaw/skills/siluzan-seo/` |
| `workbuddy` / `workbuddy-workspace` | `.workbuddy/skills/siluzan-seo/` |
| `workbuddy-global` | `~/.workbuddy/skills/siluzan-seo/` |
| `all` | 当前项目下全部平台目录 |

WorkBuddy 也可将 `seo-traffic-page/`、`blog/`、`backlink-article/` 子目录分别作为独立 Skill 安装（见各子目录 `SKILL.md`）。

---

## 与 siluzan-cso 的关系

| 能力 | siluzan-seo | siluzan-cso |
|------|-------------|-------------|
| SEO JSON schema 生成 | ✅ Skill 文档 + 子目录 prompts | ❌ |
| 企业 RAG / 三库写稿 | 工作流中另用 CSO Skill | ✅ |
| 登录 / API Key | ❌ 不需要 | ✅ |
| 导出 Word/PDF | ✅ `export` 命令 | ❌ |

做 RAG 拉企业资料时，在 Agent 工作流里加载 **siluzan-cso** 即可，与 SEO CLI 安装无关。
