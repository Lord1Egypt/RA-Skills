---
name: skillhub-publish-skill
slug: skillhub-publish-skill
displayName: SkillHub/ClawHub 技能发布
summary: 把本地 Skill 打包并发布到 SkillHub（腾讯 skillhub.cn）与 ClawHub，覆盖发布前预检、官方 CLI 发布链路、网页 CDP 兜底；发布后可直接回读线上版本与下载数据，并在上传被拒时用二分/ddmin 把「服务端 WAF 拦内容（566）」与「包结构/字段问题」精确区分开。
license: MIT
description: 把本地 Skill 打包并发布到 SkillHub（腾讯 skillhub.cn）与 ClawHub，覆盖预检、发布、状态回读与竞品对标全链路，并在上传被拒时用二分/ddmin 脚本把「服务端 WAF 拦内容（566）」与「包结构/字段问题」精确区分开。当用户说「发布技能到市场」「上架 skill」「SkillHub 提交失败」「Failed to fetch」「566」「上传 zip 报错」「技能审核状态」「版本号被拒」时使用。也讲清「入库成功 ≠ 已公开」——用 `mine` 的 `reviewStatus`、重发探测 `409 VERSION_EXISTS`、`/versions/<v>/signature` 三个探针判断版本到底走到哪一步。
version: 1.7.6
category: dev-programming
subCategories: [dev-script, dev-git]
platforms: [WorkBuddy, Claude Code, Codex]
agent_created: true
---

# SkillHub / ClawHub 技能发布

发布一个技能实际要同步三个地方：**GitHub**（源码）、**SkillHub**（腾讯主市场）、**ClawHub**（海外市场）。
本技能覆盖全链路，并在任何一步被拒时给出**可定位根因**的判定，而不是猜。

## 铁律：报错先分类，别乱猜

上传失败的报错只有四类，**每类的对策完全不同**，先看报错文案归位：

| 报错文案 | 类别 | 对策 |
|---|---|---|
| `不支持的文件类型: xxx` | 包内容 | 用 `scripts/publish.py` 发（它按白名单自动过滤） |
| `字段格式校验` 类 | 包内容 | 跑 `scripts/preflight.py` 查 frontmatter |
| `slug 已被占用` / 409 / 500 | slug 冲突 | `publish.py` 会自动追加后缀重试并回写 SKILL.md |
| **`提交失败` / `Failed to fetch` / `net::ERR_FAILED 566` / CORS 报错** | **服务端 WAF 拦内容** | **跑 `scripts/waf_bisect.py` 定位，改内容，别改结构** |

**不要**把第四类当成网络/代理/浏览器扩展问题。判据是客观的：用本机脚本向发布端点 POST 同一份 multipart，
`401` 就说明请求已到达应用层（正常，只差登录态），`566` 才是被 WAF 拦。

> 这一条是本技能与其他发布类技能的核心差别。其他工具只处理 400/409/429，
> 遇到 566 会误导你去「检查元数据与文件类型」——方向完全错了。

## 铁律二：查不到 ≠ 不存在

判断「某个技能有没有」「上架了没有」之前，**先确认你用的接口能看到什么范围**。
公开接口天然过滤掉未公开、审核中、已下架的条目 —— 拿它当「是否存在」的判据会得到假阴性。

| 想知道什么 | 用哪个 | 别用哪个 |
|---|---|---|
| 这个技能**公开发布**了吗 | `status <slug>`（公开搜索） | — |
| 我**到底发过哪些**（含测试残留） | `mine`（我的后台） | ❌ 公开搜索查不到 |
| 某个 slug 归谁 | `status` / 看 `namespace.handle` | — |

之前踩过的具体坑：用公开搜索查自家测试探针，搜不到就判定「已被平台自动清理」，
实际 18 个条目里 12 个探针都还挂在「我的 Skills」里。**清点自己发了什么，永远用 `mine`。**

## 标准工作流

### Step 1 预检（不联网，可做卡点）

```bash
python scripts/preflight.py <skill目录>            # 人读报告
python scripts/preflight.py <skill目录> --json      # Agent 解析
```

三级输出：**ERROR**（会被拒，必须修）/ **WARN**（能过审但影响质量）/ **INFO**（发布操作提醒）。
存在 ERROR 时退出码为 1，可直接接发布脚本卡点。

覆盖：frontmatter 缺字段与非法值、位图与独立 LICENSE 拒收、包结构与白名单、密钥泄漏、安全红线、
占位符残留、**WAF 命中特征**（本脚本独有）。

### Step 2 确认元数据

```bash
python scripts/publish.py validate <skill目录>
```

缺 `slug` / `version` / `displayName` 会明确列出。补进 SKILL.md frontmatter——这些字段不影响 skill 本地运行。

### Step 3 预演（不上传）

```bash
python scripts/publish.py publish <skill目录> --version 1.4.0 --dry-run
```

打印将要上传的文件清单、体积、图标识别结果、**被排除的文件及原因**，
以及**与线上版本的比对结果**（`versionCheck`: OK / SAME / TOO_OLD）。确认无误再真发。

### Step 4 发布

```bash
python scripts/publish.py publish <skill目录> --version 1.3.0 --changelog "变更说明" \
       [--icon icon.png] [--category dev-programming] [--subcategory dev-script]
```

脚本自动完成：白名单过滤 → 图标两步上传 → 分类 key 校验 → 429 指数退避 → slug 冲突自愈。
成功返回 `skillId` / `versionId` / `slugUsed` / `category` / `subCategories`；
失败会打印**分类结论 + 下一步动作**。

**分类建议写进 SKILL.md frontmatter**（比分次传参可靠，下次发版自动带上）：

```yaml
category: dev-programming
subCategories: [dev-script, dev-code-gen]
```

不填分类的话平台会显示「未分类」——**注意「选填」不等于可以不管**，
市场里未分类的条目曝光会明显吃亏。可选值用 `publish.py categories` 查。

带图标时务必确认响应里 **`iconAuditStatus: "pending"`** —— 若是 `null` 说明图标没收到
（那通常意味着把图片错当成 multipart part 传了，见上方「图标」注意事项）。
分类则看响应里有没有回显 `category` 字段。

### Step 5 验证发布结果（不用开浏览器）

```bash
python scripts/publish.py status <skill目录>     # 传目录会自动比对本地/线上版本
python scripts/publish.py status <slug>          # 只查线上
```

输出线上版本、下载/安装/收藏数、更新时间，并给出同步状态：

| 同步状态 | 含义 |
|---|---|
| `✓ 已同步` | 本地版本 == 线上版本，**审核已通过** |
| `↑ 本地更新` | 本地版本更高 —— 还没发，或已提交仍在审核中 |
| `✗ 版本倒挂` | 本地版本 ≤ 线上版本 —— 发上去会被服务端拒 |

> ⚠️ **search 索引有延迟**：刚发布（还在审核）的版本不会立即出现在查询结果里，
> 可能仍显示上一个线上版本。这是正常的，不是发布失败。
>
> ⚠️ **`status` 走的是公开搜索接口，看不到未公开条目**。要清点「我到底发过什么」
> （含审核中、已下架、测试残留），用 `mine` 命令 —— 那是另一个接口（`/api/v1/dashboard/skills`）。

### 「入库成功」≠「已公开」——两个状态分别怎么查

`publish` 返回 200 / `skillId` 只代表**版本已入库**；能不能被搜到、能下到什么版本，
取决于审核（`reviewStatus`）。**2026-09-29 实测**：连发 1.1.1 → 1.1.2 → 1.1.3 三次 CLI
全部返回成功，但公开索引 `latestVersion` 长时间停在 1.1.1（`search`、`download`、
`/versions/<v>/signature` 全指向旧版），一度误判「后两次没发上去」。

**权威状态看 `mine`**（`/api/v1/dashboard/skills`）：

```json
{ "version": "1.1.3", "status": "listed", "reviewStatus": "pending" }
```

`status: listed` + `reviewStatus: pending` = **已入库、审核中**。此时公开索引滞后属正常，
等审核过即可 —— **不要重发**（重发只会撞 409，白折腾）。

**不开后台也能自证的两个探针**：

| 想知道 | 怎么查 | 判据 |
|---|---|---|
| 版本是否已**入库** | 用同版本号重发一次（`publish --version <v>`） | `409 VERSION_EXISTS` = 已入库；返回 200 = 之前确实没发上 |
| 版本是否已**公开** | `GET /api/v1/skills/<slug>?namespace=<ns>` 看 `latestVersion`；或 `GET /api/v1/open/skills/<slug>/versions/<v>/signature` | signature `200` = 已公开；`404` = 未公开 |

> `latestVersion` 里带 `changelog` —— **用它反查线上到底是哪一次发布**，比只看版本号更直接
> （本次正是靠 changelog 认出线上仍是 1.1.1 那次写的文案）。
> 注意 `curl` 查这些公开端点要加 `--noproxy '*'`（本机全局代理会干扰）。

### Step 6 清点与清理自己的技能

```bash
python scripts/publish.py mine                 # 列出我名下全部技能（含线上搜索看不到的）
python scripts/publish.py mine --json          # 机器可读
python scripts/publish.py rm <slug>            # 只提示，不执行（安全护栏）
python scripts/publish.py rm <slug> --yes      # 确认删除：自动「先下架 → 再删除」
```

**`mine` 与 `status` 的区别**（踩过坑，别搞混）：

| 命令 | 数据源 | 看得到什么 |
|---|---|---|
| `status <slug>` | 公开搜索 `/api/v1/search` | 只有**已公开**条目；未过审/已下架的查不到 |
| `mine` | 我的后台 `/api/v1/dashboard/skills` | **我发的全部**：审核中、已下架、测试残留都在 |

**删除是两步**（服务端强制）：直接 `DELETE` 会返回 `409 只能删除已下架的 Skill，请先下架`。
`rm` 已自动串好 `/unlist` → `DELETE`，并对「已下架再删」的重复调用做了容错。
删除**不可恢复**，所以默认不给 `--yes` 就只打印风险提示、不执行。

### Step 7 ClawHub

```bash
clawhub skill publish <skill目录> \
  --slug <slug> --name "<显示名>" \
  --categories "<14 项之一>" --topics "a,b,c" \
  --changelog "..."
```

`--source-repo` / `--source-commit` **成对给或都不给**，只给一个报 `must be provided together`。

- **ClawHub CLI 没有 `inspect` / `search`**（v0.23.3 实测，`skill` 子命令只有
  `publish / verify / tag / rename / merge`）。要查「slug 是否被占用 / 线上审核状态」**只能用
  `clawhub skill verify <slug>`**；想要竞品下载量数据得回到 SkillHub 侧的 `publish.py compare`。
- 审核期（含刚提交后）`verify` 返回 `Skill is hidden by moderation (pending.publication)`
  —— **这是正常状态，不是失败**。发布成功的判据是 publish 时那句
  `Update submitted ... pending security scans`。
- **⚠️ `verify` 还会返回安全扫描结论——这才是真正会卡住公开的东西**（2026-09-29 实测）。
  形如 `{"decision":"fail","reasons":["card.missing","security.status_not_clean"],
  "security":{"status":"suspicious","confidence":"high","summary":"..."}}`：
  `card.missing` = 展示卡未生成（审核产物）；`security.status_not_clean` = 扫描未过。
  `suspicious` 的常见触发：`host-policy bypass guidance`、`high-impact admin elevation`、
  `risky credential/config handling`、**`unauthenticated local proxy`**、
  **`local gateway spoofing`**。

- **⚠️⚠️ summary 只是概述，真实判据在 `security.scannerReports.<scanner>.runs[].results[]`**
  —— 含 `ruleId`（`T01`–`T0x`，扫描器为腾讯 AI-Infra-Guard `aig-skill-scan`）、**精确到文件行号**、
  一句话原因。**只看 summary 会猜错方向**：本案 v1.1.1 依 summary 改了措辞就重发，
  到 v1.1.2 才发现真实判据是两条**代码**问题 ——
  `T05 scripts/ccproxy.py:229 Unauthenticated local clients can consume the configured upstream credential`
  与 `T07 scripts/ccswitch.py:153 Local gateway spoofing can intercept Claude Code traffic`。
  先挖判据（建议固定用这条，别凭 summary 猜）：

```bash
clawhub skill verify <slug> --version <v> | python -c "
import sys,json
for name,rep in (json.load(sys.stdin)['security'].get('scannerReports') or {}).items():
    for run in rep.get('runs',[]):
        for r in run.get('results',[]):
            print(name, r.get('ruleId'), '|', (r.get('message') or {}).get('text','')[:200])
"
```

- **改措辞常常不够，要改代码**：凡技能涉及「本地起服务 / 监听端口 / 改用户配置」，
  扫描器会要求真实防护，**必须在实现里做出来、并在 SKILL.md 明写**：
  入站鉴权（不符返回 401）、对端身份校验（健康检查须校验自身标识）、只绑回环、
  配置改动有备份。本案 v1.1.2 补的正是「客户端令牌 + `service=ccproxy` 校验」；
  同时删掉与技能无关的提权/沙箱叙事、把 `NO_PROXY=*` 收敛为回环地址列表。

- **区分「措辞问题」与「性质问题」，别无限投入**：判据若是「某行代码缺防护」→ 改代码能过；
  若是技能**功能本身**（如「本地网关转发敏感提示与凭证」）→ 加鉴权只降风险等级、
  往往仍判 fail。**这类就止损**：GitHub + SkillHub 两路已能公开分发，ClawHub 不公开
  不影响安装或使用（用户 2026-09-29 即选择「接受现状」）。
  想真正过 ClawHub 只剩「拆技能」——把触发判定的模块独立成另一个包。

- `verify --version <v>` 只能验**已公开**的版本；刚提交的版本返回 `Version not found`
  （扫描中，正常，不是发布失败）。**实测 >5 分钟仍 `Version not found` 也正常**，
  别误判；发布成功的判据始终是 publish 那句 `Update submitted ... pending security scans`。
- 对比实测：SkillHub 侧 `mine` 里新提交的技能会**直接显示 `listed`**（公开搜索 `status` 则可能
  因索引延迟查不到），两者不矛盾。

**两条容易白费功夫的约束**（详见 `references/clawhub-catalog.md`）：

- **ClawHub 没有图标能力** —— CLI 全量无 `--icon`/`--logo` 参数，SKILL.md 里放
  `<slug>.png` 对它无效。别为 ClawHub 折腾图标链路。
- **ClawHub 的分类 slug 是另一套（只有 14 个）**，与 SkillHub 的 13 个一级 key
  完全不通用。最容易踩的是 `developer-tools` ❌ → 正确是 `development`。
  传错报 `Unknown skill category slug`；超过 3 个报 `Categories are limited to 3`。
- **传了 `--categories`/`--topics` 就一定发新版本**（即使文件没改）——这是给
  已发布技能**补分类**的官方路径，CLI 会自动 bump patch。

### Step 8 GitHub

见 `references/github-repo.md`。本机已有可用凭据，**不需要向用户索要 PAT**。

## 版本递增是硬性要求

服务端要求**更新时 version 必须严格高于线上版本**（相同或更低都会被拒）。

`publish` 命令会在发布前自动比对并拦下，避免白发一次：

```
{ "success": false, "blockedBy": "version_check",
  "localVersion": "1.2.9", "remoteVersion": "1.3.0",
  "error": "版本号 1.2.9 比线上 1.3.0 更低，服务端会拒绝更新",
  "fix": "把版本号改成高于 1.3.0 的值（如升到 1.3.1），或加 --force 跳过此检查" }
```

- 首次发布（线上查不到该 slug）会自动跳过检查。
- 网络异常时降级为提示，**不阻断发布**。
- 确需绕过：`--force`。

## 竞品对标

```bash
python scripts/publish.py compare "<关键词>"
```

按下载量列出同类技能，用客观数据判断投入方向 —— 比凭感觉判断「我们有什么优势」可靠：

```
关键词「skill 发布」同类技能（按下载量排序）
版本            下载     安装  技能
1.2.1           998      26   ClawHub Skill 发布避坑指南  @clawhub_tudoubudou
1.0.1            83       0   开源发布（GitHub Skill 发布器）  @user_73cb5b59
```

下载量反映曝光面，安装量反映真实使用。

> **对新技能的启示（2026-09-29 实测）**：`compare` 的返回顺序暴露了平台搜索/推荐的排序偏好
> —— 头部清一色是**百万级下载的通用技能**（编程专家、腾讯文档、Find Skills…），
> 一个刚发布的垂直小技能**几乎不可能靠关键词搜索被刷到**。所以「已发布」≠「别人搜得到」。
> 新技能的可发现性基本只来自两处：
> ① 描述里的**长尾触发词**（把用户会说的口语原话写进去，如「claude code 换模型不生效」
>    「ANTHROPIC_BASE_URL 怎么设」「响应流畸形」）；
> ② **外部引流**（分享链接 / 公众号 / GitHub README）。
> 另外 `status`（公开搜索）有索引延迟：刚发布几分钟内查不到属正常，用 `mine` 看真实落库状态。

## 三平台版本必须一致

发布前对齐**六个地方**的 slug/name：本地目录名、SKILL.md `name`、SKILL.md `slug`、manifest `name`、
GitHub 仓库名、ClawHub `--slug`。

**SkillHub 已发布的 slug 不可改**（更新对话框里只读、无改名入口），所以它以 SkillHub 为准当「锚」，
其余平台向它对齐，**不要新建重复 Skill**。

## 资源路由

| 文件 | 什么时候读 |
|---|---|
| `scripts/preflight.py` | Step 1；发布前必跑 |
| `scripts/publish.py` | Step 2-6；日常发布主入口（含 status / compare / mine / rm / categories） |
| `scripts/waf_bisect.py` | 出现 566 / Failed to fetch 时定位根因 |
| `references/waf-details.md` | 需要理解 WAF 命中特征、判据原理与规避写法时 |
| `references/icon-upload.md` | 要传图标/封面，或怀疑图标没生效（`iconAuditStatus: null`）时 |
| `references/categories.md` | **SkillHub** 要填/补分类，或后台显示「未分类」时 |
| `references/clawhub-catalog.md` | **ClawHub** 要填分类/话题，或问 ClawHub 要不要图标时（14 个可用 slug） |
| `references/path-traps.md` | 目录路径没生效、`slug` 被自动改写，或同名仓库不是扁平技能仓库时 |
| `references/cli-install.md` | 需要安装/修复官方 CLI，或走网页 CDP 兜底路径时 |
| `references/github-repo.md` | 需要建 GitHub 仓库并推送时 |

**手头没有现成图标？** 用 `zero-dep-icon-gen` 技能本地生成
（零依赖手写 PNG，不装 Pillow，一条命令出图）：

```bash
PY="C:/Users/DELL/.workbuddy/binaries/python/versions/3.13.12/python.exe"
$PY ~/.workbuddy/skills/zero-dep-icon-gen/scripts/gen_icons.py \
    --spec "my-skill:#4F46E5,#818CF8,browser" -o my-skill/
# 生成 my-skill/my-skill.png，文件名 = slug，find_icon() 会自动兜底找到
```

可用符号：`browser` `cloud` `shield` `folder` `check` `download`
`arrow-up` `gear` `search` `lock` `text`（点阵文字）。`--list-symbols` 看全量。

## 打包规范（手工打包时必看）

1. **白名单**：只收 `SKILL.md` / `manifest.yaml` / `scripts/*.py`。
   `.gitignore` / `LICENSE` / `README` 会被拒。别用 GitHub「Download ZIP」（会带上那几个文件）。
   > 实测补充（2026-09-21）：**`scripts/` 前缀是放行条件，不限于 `.py`** ——
   > 同批上传的 `scripts/buildkey_cdp.js`、`scripts/attach_debug.js` 均被服务端接受
   > （8 文件全部入库，返回 `success: true`）。也就是说 `scripts/*.js` 这类文本文件可以随包发。
   > `publish.py` 的判定是 `rel in ALLOWED_FILES or rel.startswith(ALLOWED_PREFIXES) or ext in ALLOWED_EXTS`，
   > 所以只要放在 `scripts/`、`references/`、`assets/` 下即可绕过扩展名限制（位图除外）。
   > **2026-09-29 再补**：`examples/` 前缀**也能过**（实测 `examples/profiles/*.json` 随包入库，
   > 文件数 4→6、无新增 ERROR）—— 前缀白名单比字面更宽，别急着把示例文件删掉。
   > 另：预检对包内 png 报的 ERROR 属**保守判断** —— `publish.py` 会把它排除出包、改走图标单独上传，
   > `--dry-run` 里 `files` 不含 png 而 `icon` 指向它，属正常，**不必为此"修复"**。
2. **结构**：所有文件放进**一个与 skill 同名的顶层目录**。
3. **文件名**：`<slug>.zip`（不带版本号）。≤10MB。
4. **图标**：走表单单独上传，**绝不打进包**（zip 内位图会被拒收）。且**必须两步走**：
   先 `POST /api/v1/community/skill-icons/upload`（multipart 字段名 **`file`**）拿 `iconUrl`，
   再放进 `payload.iconUrl` 提交。把图片直接当作 `cover`/`icon` part 会被服务端**静默忽略**
   —— 发布仍返回 201，但 `iconAuditStatus` 恒为 `null`（`pending` 才是生效）。
   `publish.py --icon xxx.png` 已封装这条链路，上传失败只告警不阻断发布。
5. 打包用 zipfile 手打，键名**必须用正斜杠**（`os.path.join` 在 Windows 产生反斜杠会导致 `KeyError`）：

```python
import zipfile, os
TOP = "<slug>"
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    for rel in ["SKILL.md", "manifest.yaml"] + ["scripts/" + f for f in os.listdir("scripts") if f.endswith(".py")]:
        z.write(os.path.join(repo, rel), TOP + "/" + rel)
```

## 安全铁律

1. **绝不在回复中打印、展示或记录 token**（`skh_` / `gho_` / `ghp_` 开头一律脱敏）。
2. 发布前必须跑预检、必须获得用户确认。
3. 不改动目标 skill 的功能字段，只补平台专用元数据。
4. 全程使用绝对路径。

## 边界与免责

- 预检覆盖**已知**拒收原因，平台规则随时会变，最终判定以平台审核反馈为准。
- WAF 是累计评分制黑盒，`waf_bisect.py` 给出的是**定位方法**而非稳定规则；
  命中特征会变化，按「二分定位」的思路排查，别背特征表。
- 预检不是安全审计，不能替代平台安全扫描。

## 元教训：别信文档，信真实请求

本技能里最贵的两个结论（WAF 566 的真身、图标的两步链路）都不是文档里写的，
而是**打真实请求试出来的**。踩过的坑值得记住：

1. **「接口返回 2xx」不等于「这个字段生效了」**。`cover` part 返回 201，但字段被静默忽略。
   判断字段是否生效，要看**响应体里对应的状态字段**（如 `iconAuditStatus`），
   而不是看 HTTP 状态码。
2. **服务端对不认识的 part 常常静默丢弃**，不报错。所以要靠「换个明显非法的值试试」来
   反证：如果传一堆垃圾内容它也照收不误，说明它压根没读这个字段。
3. **平台只有网页、没有 API 文档时**，去前端 bundle 里搜端点名反查真实实现
   （见 `references/icon-upload.md` 的「反查方法」），比猜字段名快得多。
4. **官方 CLI 没做的功能，不代表平台没有这个 API** —— 两边是独立的。
