# ClawHub 分类与话题（--categories / --topics）

ClawHub 与 SkillHub 是两套**完全独立**的分类体系。别把 SkillHub 的 13 个一级
分类 key 拿来喂 ClawHub —— 服务端会直接报 `Unknown skill category slug`。

## 结论速查

| 维度 | SkillHub | ClawHub |
|---|---|---|
| 分类 | ✅ 有（`category` 单选 + `subCategories` ≤3） | ✅ 有（`categories` ≤3 个，多选） |
| 话题/标签 | ❌ 无 | ✅ 有（`topics` ≤5 个，自由文本） |
| 图标 | ✅ 有（`iconUrl`，需单独上传接口） | ❌ **完全没有**（CLI 无任何图标参数） |
| 分类清单从哪拿 | 公开端点 `/api/v1/categories` | ❌ **无公开端点**，只能从前端 bundle 抄或试 |
| 改分类的方式 | 重新 publish（无独立端点） | 重新 publish（传 `--categories` 即触发） |

## 图标：ClawHub 没有这个需求

CLI 全量排查（`skill publish` / `package publish` / `sync` / 顶层）——
**没有任何 `--icon` / `--logo` / `--image` / `--cover` 参数**。

```bash
clawhub skill publish --help | grep -iE "icon|logo|image|cover|avatar"   # 无输出
```

但 API 响应里 `skill.icon` 字段**存在**（读得到），只是 CLI 写不进去：

```bash
clawhub inspect oracis/zero-dep-icon-gen --json | python -c "import json,sys; print(json.load(sys.stdin)['skill']['icon'])"
# -> null（因为发布时没传过）
```

**结论**：`icon` 是只读字段，SKILL.md 里放 `<slug>.png` 对 ClawHub 无效。
想给 ClawHub 上的技能配图标，只能在**网页后台**操作（CLI 不支持）。
所以「生成图标 → 发布」这条链路对 ClawHub 不成立，不用为它折腾。

## 分类：真正的 14 个 slug（实测可用）

ClawHub **没有**公开的分类清单端点（`/api/categories`、`/api/v1/categories`、
`/api/topics` 全 404）。权威清单藏在网页前端 bundle 里。

**两个 bundle 各有一套表，只有一套能用来发技能 —— 这是最大的坑：**

| bundle 变量 | 条目数 | 用途 | 能否用于 `--categories` |
|---|---|---|---|
| `Fp`（导出为 `c`） | **14** | **技能分类** | ✅ **用这个** |
| `Np`（导出为 `s`） | 22 | 插件/市场分类 | ❌ 服务端拒绝 |
| `Pp`（导出为 `o`） | 3 | 插件运行时 | ❌ 服务端拒绝 |

### ✅ 技能可用的 14 个分类 slug

```
integrations     Integrations
automation       Automation
research         Research
development      Development
productivity     Productivity
communication    Communication
creative         Creative
knowledge        Knowledge
agents           Agents
operations       Operations
security         Security
finance          Finance
lifestyle        Lifestyle
other            Other
```

### ❌ 长得很像但会被拒的 slug（来自那 22 项插件表）

以下这些**看着更"专业"、全部会被拒**，别用：

```
channels  models  agent-runtimes  memory  context  voice  web  media
security*  integrations*  developer-tools  infrastructure  documents-files
inbox-collaboration  productivity*  scheduling  finance-payments
sales-marketing  data-analytics  agent-orchestration  research*  other*
```

带 `*` 的是与 14 项表**撞名**的（`security` / `integrations` / `productivity`
/ `research` / `other`）—— 这几个恰好两边都有，能用，但别以为整张表都能用。

**高危易踩**：`developer-tools` ❌（应该用 `development`）、
`documents-files` ❌、`inbox-collaboration` ❌、`data-analytics` ❌。

## 约束（实测）

| 约束 | 值 | 报错原文 |
|---|---|---|
| 分类数量上限 | **3** | `Categories are limited to 3` |
| 无效 slug | 立即拒绝 | `Unknown skill category slug "xxx"` |
| 话题数量上限 | **5** | 前端 `Maximum 5 topics` |
| `other` 与其他并存 | 服务端**接受** | 前端 UI 会禁用其他项，CLI 传得进去 |

## 关键行为：传了 --categories 就一定会发新版本

前端 bundle 与 CLI 源码（`publish.js:36,74`）都有一条：

```js
const hasExplicitCatalogMetadata =
    options.categories !== undefined || options.topics !== undefined;
// ...
if (!explicitVersion && resolved.match && !hasExplicitCatalogMetadata) {
    // 文件指纹相同 -> 直接返回 unchanged，什么都不做
    return { status: "unchanged" };
}
```

**含义**：文件完全没改，只要传了 `--categories`，就**不会**走 `unchanged`
短路，而是照常发一个新版本。这正好是给**已发布技能补分类**的官方路径 ——
不用改 SKILL.md 的 version，CLI 会自动 bump patch。

## 用法

```bash
# 补分类（会自动发一个 patch 版本）
clawhub skill publish <dir> \
  --slug <slug> --name "<显示名>" \
  --categories "development" \
  --topics "icon,png,stdlib" \
  --changelog "补充分类与话题元数据"

# 多分类（≤3）
--categories "development,creative"

# 只看会发生什么（注意：dry-run 不做分类校验，不会报 Unknown slug）
--dry-run --json
```

⚠️ **`--dry-run` 不校验分类** —— 传个瞎编的 slug 也返回 `would-publish`。
想验证 slug 是否有效，必须**真发一次**（或者先用一个无害的小技能试探）。

## 回读的限制

```bash
clawhub inspect <owner>/<slug> --json
```

- `topics` ✅ 能读到
- `categories` ❌ **读不到**（不在公开响应里，网页 UI 走另一个字段）
- `icon` 能读到，但恒为 `null`

`clawhub inspect` 的**文本**输出只渲染 `Tags`，连 `topics` 都不显示。
要看话题必须加 `--json`。

→ 因此**发完分类无法用 CLI 自证**，只能去网页后台肉眼确认。
发布时留意服务端是否报 `Unknown skill category slug`，这是唯一的即时反馈。

## 话题的隐藏地雷：保留词（reserved topic）

`--topics` 是自由文本，但**某些词被平台保留**，传了直接报错、整个发布失败：

```
Error: Topic "clawhub" is reserved by ClawHub (reset in 12s)
```

实测 `clawhub` 是保留词（大小写不敏感，估计 `skillhub`、`openclaw` 之类同理）。
**踩坑经过**：给 `skillhub-publish-skill` 传 `--topics "publish,skill,skillhub,clawhub"`，
因为含 `clawhub` 整个发布失败；去掉它（`publish,skill,skillhub`）立即成功。

**对策**：发之前先排除明显的平台名/品牌词。如果发布在 JSON 管道里报
`Expecting value: line 1 column 1` 解析失败，多半是 topic 含保留词导致服务端没回 JSON，
直接去掉可疑词重试即可（不需要改别的）。

## 安全扫描会拦「自动换 slug + 回写本地文件」

ClawHub 发布前要过安全扫描（Tencent AI-Infra-Guard / `aig-skill-scan`）。
如果技能代码里**在 slug 冲突时自动发布到后备 slug 并改写本地 metadata**，会被规则
**T09「Slug Conflict Automatically Publishes to an Unapproved Fallback Identifier」**
判为 `suspicious`（置信度高），结果新版本一直卡在 `pending` 无法晋级成 latest。

`clawhub skill verify <slug>` 能看到：`.security.verdict = suspicious`、
`.security.summary = ...can automatically publish under a different public slug and
rewrite local metadata after a conflict...`。

**对策**：把这类「冲突自愈」逻辑整个删掉，改为 slug 冲突时**明确失败并提示换名**。
（skillhub-publish-skill 自身 1.7.3 就这么改的——详见 `references/path-traps.md` 坑 2。）
注意：扫描是**静态分析整段代码**，即使把兜底逻辑做成「默认关闭的 opt-in」也没用，
只要那段代码还在就会被标；必须彻底移除才过得了扫描。
