# 发布排错与复核

按「症状 → 原因 → 处置」组织。每一条都是真机上发生过的。

## 一、命令返回 ≠ 已经上线

`skillhub publish <目录> --changelog "..."` 返回

```
✓ Published: skillId=201994 status=None
```

**只代表平台已受理**。线上字段分三档更新：

| 档位 | 字段 | 时机 |
|---|---|---|
| **立即** | `tags` | 秒级生效（skill 级索引，不等审核） |
| **随审核** | `version` / `summary` / `description` / 版本列表 / 下载包 | 只有**审核通过**的版本才写进 `latestVersion` |
| **CLI 改不了** | `category` | 发布 payload 里没有这个字段，只能网页 dashboard 改 |

每版都会跑三线审核：**内容合规 + 科恩漏洞扫描 + 云鼎 AI 安全评估**。实测一版约 **3 分钟**过审。

**判据**：看 `GET /api/v1/skills/<slug>/versions` 的**版本列表里有没有刚发的版本号**。

```
stats.versions = 4，但版本列表只有 3 个  →  第 4 个在审核中（正常，别重发）
```

⚠️ **`stats.versions` 会把待审版本也计入**，所以「计数涨了但列表没动」= 审核中，不是失败。
不要因为看到商店没变化就立刻重发一版 —— 会平白多出几个版本号。

## 二、🔴 分类（category）改不了

两次实测：

1. CLI 发布 payload 固定 9 个键，**没有 `category`**；
2. 更关键 —— SKILL.md 里写 `category: dev-programming`、**过审成为 `latestVersion` 之后，
   线上 `skill.category` 依然是 `ai-agent`**，说明**平台根本不解析 SKILL.md 的 category**。

**结论：改 SKILL.md 的 category 对外零作用，改分类只能去网页 dashboard。**
发布后用 `GET /api/v1/skills/<slug>` 复核 `skill.category`，若不对就提醒用户
去 https://skillhub.cn/dashboard 手动改。

## 三、只读状态接口（无需登录，用来复核）

```bash
GET https://api.skillhub.cn/api/v1/skills/<slug>
    # latestVersion.version / latestVersion.changelog
    # skill.category / skill.summary_zh / skill.tags / skill.stats.versions / skill.securityReports

GET https://api.skillhub.cn/api/v1/skills/<slug>/versions?page=1&pageSize=20
    # versions[] = 已过审版本 + 安全报告

GET https://api.skillhub.cn/api/v1/download?slug=<slug>
    # 只看响应头 Content-Disposition 的 filename = 当前可下载版本

GET https://api.skillhub.cn/api/v1/search?q=<slug>&page=1&pageSize=10
    # 商店搜索结果；注意 q= 是模糊匹配，短前缀会返回兜底热门榜，**不能用来判重**
```

反面写法别踩：`/api/v1/skills/@handle/<slug>` 返回 **405**；
`/api/v1/skills/resolve?slug=` 返回 **400**。

`scripts/skillhub_publish.py status <slug> --expect <version>` 就是这三个接口的封装。

## 四、slug 被占用

平台报 `slug 'xxx' 已被其他用户占用` 时，先用下载接口筛，不要凭感觉猜：

```bash
curl -s -o /dev/null -w "%{http_code}\n" "https://api.skillhub.cn/api/v1/download?slug=<候选名>"
# 200 = 平台上已有同名「已发布」技能
# 404 = 公开层面无此技能
```

两个反直觉点：

- **404 ≠ 可用**：已被占用但**尚未公开发布**（草稿 / 审核中 / 私有）的 slug 同样是 404。
  实测反例：`skill-generator` 已被占用（发布被拒），但下载接口 404、搜索也零命中。
- **自己发的技能也返回 302/200**：这个接口不能区分「谁发的」。要认作者看
  `namespace.handle` / `owner.handle`。

**结论**：外部接口只能排除「已被别人发布」的名字，最终仍需在发布表单里试一次。

改名要 **`name` / 目录名 / 仓库名三处同步** —— 绑 GitHub 发布时 slug 取自 SKILL.md 的 `name`。

## 五、Windows / Git Bash 环境坑

### 1. `RuntimeError: Could not determine home directory`

在 Git Bash 里直接跑 `skillhub` 会崩（shim 的 `HOME` / `PATH` 残缺）。绕法是改用系统 python
调用 CLI 主程序，并**显式把 `HOME` / `USERPROFILE` 指向 Windows 用户目录**：

```bash
# 用本脚本就不用手写这段 —— cli_env() 已内置
env HOME="$USERPROFILE" PYTHONIOENCODING=utf-8 \
  python ~/.skillhub/skills_store_cli.py publish <技能目录> --dry-run
```

`scripts/skillhub_publish.py` 已经内置这件事（`cli_env()`），直接用本脚本就不用操心。

### 2. python 解释器

本机 managed Python 3.13 跑带网络请求的脚本会 **segfault**。脚本默认优先
`%LOCALAPPDATA%\Microsoft\WindowsApps\python.exe`（系统 3.11.9）。
需要覆盖时设环境变量 `SKILLHUB_PYTHON`。

### 3. 传给原生 python 的路径别名

一律用 Windows 绝对路径（`C:/...`）。Git Bash 的 `/c/...` 会被原生 python
当**相对当前盘**解析，实际落到 `D:\c\Users\...`。

## 六、发布前三条快查（不发 HTTP）

1. `python scripts/skillhub_publish.py check <技能目录>`
2. 本地市场体检（若装了 ym-skill-generator）：`audit_skill.py <dir> --market`
3. 想看「平台到底会读到什么字段、会传哪些文件」，直接调 CLI 自己的解析器：

```python
import importlib.util, json
spec = importlib.util.spec_from_file_location("cli", r"~/.skillhub/skills_store_cli.py".replace("~", HOME))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
md = m.parse_skill_md_frontmatter(Path(dir) / "SKILL.md")
files = m._collect_skill_files(Path(dir))
```

比读文档准 —— 平台解析器的怪癖全在这里暴露。
注意 `_PUBLISH_EXCLUDE_DIRS` / `_PUBLISH_EXCLUDE_PATTERNS` **不排**
`.gitignore` / `.gitattributes` / `icons/`。

## 七、发布后要不要同步 git 仓库

CLI 发布走的是上传通道，**不需要**先推 GitHub。只有当你同时在用「网页绑定 GitHub 发布」
那条线时，才需要保证仓库已同步。本机沙箱常拦 `git push` / `git fetch`
（`Empty reply from server` / `502`），但 `gh api` 通：

```bash
python ~/.workbuddy/tools/push_via_api.py <仓库目录>   # 加 --dry-run 先看计划
```

**验证只看 tree sha** —— API 重建的 commit sha 必然与本地不同，那不是不一致。
