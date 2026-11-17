# 上架与分发形态（发布 ≠ 上线 / 插件形态包）

> 从 SKILL.md 正文迁来：打包上架时才需要读这一份。

### 发布 ≠ 上线：线上字段分三档更新

上架动作是 `skillhub publish <技能目录> --changelog "..."`（网页发布等价）。**命令返回成功只代表「平台已受理」**，
商店里的字段不是一次性全变，实测分三档：

| 档位 | 字段 | 时机 |
|---|---|---|
| **立即** | `tags` | 秒级生效（skill 级索引，不等审核） |
| **随审核** | `version` / `summary` / `description` / 版本列表 / 下载包 | 只有**审核通过**的版本才写进 `latestVersion` |
| **CLI 改不了** | `category` | **发布 payload 里没有这个字段**，只能去网页 dashboard 改 |

判定「是否真的上线」看**版本列表里有没有刚发的版本号**，不要看命令返回值。`stats.versions` 会把待审版本也计入，
所以「计数涨了但列表没动」= 正在审核。

只读查询接口（无需登录，用来复核发布结果）：

```bash
GET https://api.skillhub.cn/api/v1/skills/<slug>                               # latestVersion / summary / category / stats.versions
GET https://api.skillhub.cn/api/v1/skills/<slug>/versions?page=1&pageSize=20   # 各版本 + 过审后的安全报告
GET https://api.skillhub.cn/api/v1/download?slug=<slug>                        # 看 Content-Disposition 的 filename 是哪个版本
```

反面写法别踩：`/api/v1/skills/@handle/slug` 返回 **405**，`/api/v1/skills/resolve?slug=` 返回 **400**。

---

### 插件形态包（`--as-plugin`）的结构

只有要把技能**作为插件**分发时才用：

```
<plugin-name>/
├── .codebuddy-plugin/
│   └── plugin.json          # 插件清单
└── skills/                  # 技能默认位置，AI 从这里发现技能
    └── <skill-name>/
        ├── SKILL.md
        ├── scripts/
        ├── references/
        └── templates/
```

平台若报结构类错误、提示不接受顶层目录，加 `--flat-root` 换成「zip 根即插件根」的形态。

`plugin.json` 由脚本从 SKILL.md 的 frontmatter 自动生成：

| 字段 | 来源 | 说明 |
|---|---|---|
| `name` | 技能目录名 | kebab-case |
| `version` | `version` | 缺省 `1.0.0` |
| `description` | `description`（剥掉触发词长尾后截 200 字） | 平台中文搜索匹配的就是它，功能描述要留全 |
| `description_en` | `description_en` | |
| `author.name` | `author` | 字符串自动转成 `{"name": ...}` |
| `category` | `category` | 展示分类（字符串，如 `development`） |
| `keywords` | 名字拆词 + 前 6 个 trigger | 平台检索用 |

> ⚠️ 这是**插件**清单的字段集，与**专家**清单（`expertType` / `displayName` / `categoryId`…）
> 不是一套，别互抄。专家的分类是 `categoryId`（数字枚举），技能是 `category`（字符串）。
| `skills` | **不写** | 技能放 `skills/` 就是平台默认位置，靠默认发现。显式写 `["./skills"]` 有语义风险——平台可能理解为"技能目录列表"，于是去找该目录下层的 SKILL.md，结果一个技能都加载不到 |

> **平铺也合法**：真实市场里 `skill-creator`、`agent-browser` 都是「插件根下直接放 SKILL.md」。但那种写法要靠 `skills` 字段指向插件根，多一处可能出错的地方；统一放进 `skills/`（平台默认位置）最稳，所以脚本默认这么打。

---

## 上架阶段的两个坑

**技能目录里留下非白名单文件，整次发布被拒** —— SkillHub 绑定 GitHub 仓库发布时，会按「文件类型白名单」逐个校验仓库里的文件，命中一个就整单拒收（报「**不支持的文件类型: xxx**」）。除图标外，最容易被忽略的两类：
    - **git 仓库自带的元数据**：`.gitignore`、`.gitattributes` —— 点开头的隐藏文件一律不在白名单里
    - **非白名单扩展名**：`.template`、`.zip`、`.xlsx` 等

    三条对策：
    - `.gitignore` / `.gitattributes` → 迁到 `.git/info/exclude` 与 `.git/info/attributes`（git 官方支持的位置，行为完全一致，但不在工作区、不进仓库，因而扫不到）
    - 模板类文件用 `.md` 后缀，别用 `.template`
    - 图标输出到技能目录之外

    自查一句话：`git ls-files` 列出的每个文件，都该是 `.md` / `.py` / `.json` / `.txt` / `.sh` / `.yaml` 这类纯文本。

**拿 `✓ Published` 当「已经上线」** —— 返回成功只表示平台**已受理**。实测线上字段分三档：`tags` 秒级生效；`version` / `summary` / 描述 / 版本列表 / 下载包要等**三线安全审核**（内容合规 + 科恩漏洞扫描 + 云鼎 AI 安全评估）通过才写进 `latestVersion`；`category` 走 CLI 永远不变。所以发完立刻去商店看「没变化」是正常的，别急着重发——先查版本列表确认新版本号在不在。


另外 7 条低频坑见 `references/pitfalls.md`（打包/上架报错时再查）。

