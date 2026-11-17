---
name: yotta-skill-creator
slug: yotta-skill-creator
version: 0.1.7
displayName: 元造·技能创建助手
summary: 一键生成合规技能目录与全套发布件脚手架，命名校验 + 结构自检，支持自用模式。
description: '元造 —— 从内嵌模板一键生成合规技能目录并做结构自检：命名校验（yotta- 前缀 / 小写连字符 / 元X 规范 / 目标不重复）+ 完整发布件脚手架（SKILL.md / README 中英四方式安装 / package.json / CHANGELOG / LICENSE / NOTICE / install.sh + bin/install.js / .gitignore / .npmignore / publish.yml / references / assets）+ 占位符替换 + 结构自检；--self-use 自用模式只生成技能本体（SKILL.md / references / 可选 CLI），不生成任何发布件。触发：新建一个 yotta- 技能、从零搭技能脚手架、想把发布规范里的坑固化成模板时；或用户说 元造 / 造技能 / 脚手架 / scaffold / 新建技能 等。边界（Do NOT trigger）：不替用户写技能正文与脚本逻辑（SKILL.md 正文 / scripts 需人工开发）；不做发布前校验与三源发布（那是元守 yotta-publish-guard）；不做既有技能目录的批量改造。'
tags: [技能创建, 脚手架, 发布件, 模板, skill creator, scaffold]
category: dev-programming
license: MIT
homepage: https://github.com/YottaMeta/yotta-skill-creator
metadata:
  zh_name: 元造
---
# 元造（yotta-skill-creator）

**端到端造技能脚手架**：输入 `yotta-<名称>` + 中文名 + 描述，一键生成符合元阁发布规范的
技能目录，生成后立即做结构自检，通过才输出「脚手架合格」。

- **create**：命名校验 → 内嵌模板 → 占位符替换 → 结构自检，输出完整技能目录。
- **--self-use 自用模式**：只生成技能本体（SKILL.md / references / 可选 CLI），不生成任何发布件——
  造一个自用技能不需要推 GitHub / npm / ClawHub。

零依赖（Python 3.8+ 标准库），Windows + Linux + macOS 通用。

## 何时使用

- 要新建一个 `yotta-` 技能，想从合规骨架起步，不重复踩发布规范里的坑；
- 需要一个不打算发布的自用技能，只要 SKILL.md + references（可选 CLI）；
- 想给团队 / 其他智能体统一「造技能」入口，保证命名、结构、发布件一致。

**Do NOT trigger**：
- 不替用户写技能正文与脚本逻辑——脚手架只生成骨架与模板，正文 / 算法 / 测试需人工开发；
- 不做发布前校验与三源发布——那是元守（yotta-publish-guard）的职责；
- 不做既有技能目录的批量改名 / 迁移——直接编辑目标目录。

## 快速使用

```bash
# 完整发布版脚手架（生成全套发布件）
python3 scripts/yotta_skill_creator.py create yotta-my-tool \
    --zh 元工 --desc "做什么 + 何时触发 + 边界" --summary "一句话简介"

# 自用模式：只生成技能本体，不生成任何发布件
python3 scripts/yotta_skill_creator.py create yotta-private \
    --zh 元私 --desc "自用技能描述" --self-use

# 同时生成 CLI 骨架 + 测试；跳过 banner / install.sh 可选
python3 scripts/yotta_skill_creator.py create yotta-tool2 \
    --zh 元工 --desc "..." --with-cli --no-banner --skip-installer
```

生成目录后按提示编辑 SKILL.md 正文 / scripts，再交给元守（publish-guard）做发布前检查。

## 命名校验（不通过即拒绝）

| 规则 | 要求 | 反例 |
|---|---|---|
| 前缀 | 必须以 `yotta-` 开头 | `my-tool` |
| 字符 | 小写字母 / 数字 / 连字符，不以连字符收尾 | `yotta-Bad` / `yotta-` |
| 长度 | ≤ 64 字符 | 超长名 |
| 中文名 | `元X`：以「元」开头，2-8 字符 | `工具`（缺「元」） |
| 目标 | 输出目录不存在（不覆盖） | 已存在的同名目录 |

## 生成内容

**完整模式（默认）**：SKILL.md（四要素 frontmatter）/ README.md + README.zh-CN.md（四方式安装）/
package.json / CHANGELOG.md / LICENSE(MIT) / NOTICE / install.sh + bin/install.js /
.gitignore / .npmignore / .github/workflows/publish.yml / references/ / assets/。

**自用模式（--self-use）**：只生成 SKILL.md / references/（加 --with-cli 时含 scripts/），
不生成 README 中英 / package / CHANGELOG / LICENSE / NOTICE / install.sh / publish.yml 等发布件。

选项速查（详见 references/cli-reference.md）：

| 选项 | 作用 |
|---|---|
| `--zh 元X` | 中文名（必需，元X 规范） |
| `--desc "..."` | SKILL.md 描述：做什么 + 何时触发 + 边界（必需） |
| `--summary "..."` | 一句话简介（README 用；缺省 = desc） |
| `--out <目录>` | 输出父目录（缺省 = 当前目录，生成 `<out>/<name>/`） |
| `--with-cli` | 同时生成 CLI 骨架 + 测试（scripts/） |
| `--no-banner` | 跳过 assets/ 素材目录 |
| `--skip-installer` | 不生成 install.sh / bin/install.js（并从 package.json 去掉 bin） |
| `--self-use` | 自用模式：只生成技能本体，不生成发布件 |

## 结构自检（生成后自动执行）

生成后立即校验，任何一项不通过返回退出码 2：

- 必需文件齐全（完整模式含发布件 / 自用模式含技能本体；`--with-cli` 含 scripts + 测试）；
- frontmatter：`name` 与目录名一致，`description` / `version` / `license` 齐全；
- 版本对齐：package.json / SKILL.md / CHANGELOG 顶部一致；
- README 中英各含「四方式安装」（npx / git clone / Download ZIP / install.sh）；
- 无残留占位符；Markdown 代码围栏配对。

## 退出码

| 退出码 | 含义 |
|---|---|
| 0 | 成功，脚手架合格 |
| 2 | 参数 / 命名 / 自检不通过 |
| 4 | 致命异常 |
| 130 | Ctrl+C 中断 |

## 行为锚点

1. **只生成、不覆盖**：目标目录已存在即拒绝，不覆盖任何文件。
2. **模板内嵌**：模板随发布包分发（`template/`），不依赖仓库 `tools/`。
3. **生成即自检**：`create` 结束前自动跑结构自检，通过才算完成。
4. **自用模式默认不碰发布件**：`--self-use` 明确「造技能 ≠ 发布」。

## 与工坊 / 工具链分工

- 元造（本技能）= **造**：生成合规脚手架 + 结构自检；
- 元守 yotta-publish-guard = **守**：发布前聚合校验 / 版本对齐 / 查重 / 打包检查 / 发布命令；
- 仓库 `tools/scaffold-skill.py` / `tools/validate-skill.py` = 内部实现；工坊技能把流程「技能化」
  并自包含（发布包内带实现副本），任何智能体装了就能用。
- 推荐链路：**元造 create（脚手架）→ 人工开发正文 / 脚本 / 测试 → 元守 check / pack / versions / names → publish（三源或指定渠道）**。

## 渐进披露

- references/cli-reference.md —— 完整参数 / 命名规则 / 退出码 / 自用模式差异
- references/scaffold-structure.md —— 生成目录结构与每个文件的用途（完整 / 自用对照）
- references/tutorial.md —— 中文教程（新手全流程：造 → 自检 → 交给元守）
