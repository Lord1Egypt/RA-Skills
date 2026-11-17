# SkillHub 平台字段规范（实测）

写在这里的都是**读 CLI 源码 + 真实发布验证过**的结论，不是文档推断。
凡是与「看起来应该怎样」冲突的地方，以这里为准。

## 一、两套字段，互不相认

| 用途 | 平台读（驼峰） | WorkBuddy 本机读（下划线） | 缺失后果 |
|---|---|---|---|
| 商店展示名 | **`displayName`** | `display_name` | 平台**不报任何错**，商店列表直接显示英文 slug —— 典型静默失败 |
| 技能标识 | `slug`（= `name`） | `name` | CLI 硬报错 `SKILL.md 缺少 slug` |
| 版本 | `version` | 同名字段 | CLI 硬报错 `SKILL.md 缺少 version` |
| 列表摘要 | `summary` | — | 列表摘要为空 |
| 标签 | `tags` | `trigger` | 标签为空，商店搜不到 |
| 分类 | `category` | 同名字段 | 不报错，上架后显示「未分类」 |
| 中英文介绍 | `description_zh` / `description_en` | 同名字段 | 上架被打回 |

**要发布的技能，两套都写。** `display_name` 可以带「 · 功能列举」后缀给本机搜索用，
`displayName` 保持干净（平台 CLI 只当展示名）。

## 二、CLI 的硬校验只有三个字段

`~/.skillhub/skills_store_cli.py` 里的 `_validate_metadata()`，缺任一个直接 `die()`：

1. `slug` —— 必须 kebab-case、长度 2–128
2. `version` —— 必须合法 SemVer
3. `displayName` —— 非空

其余全是「不报错但会静默降级」，所以**不要拿「发布成功」当字段齐全的证据**。

## 三、平台解析器比 YAML 窄得多

CLI 自带的 `parse_skill_md_frontmatter` **不做键名归一化，也不剥行尾注释**，
只认两种写法：`key: 值` 与 `key: [a, b]`。三种「完全合法的 YAML」在平台上会静默丢内容：

| 写法 | 平台读到什么 |
|---|---|
| `description: >-` + 缩进块 | 字面量 `>-`（两个字符） |
| `tags:` + 多行 `- 项` | 空 |
| `category: development  # 分类` | 整串含注释 → 于是「未分类」 |

**对策**：长文本折成一行、列表用 `[a, b]`、注释独立成行（或干脆不留注释）。
这些写法对完整 YAML 解析器同样合法，两边都安全。

> ⚠️ `fix` 只规整 **平台会读的字段**（`PLATFORM_KEYS`）。`trigger` / `display_name` /
> `agent_created` 是 WorkBuddy 本机字段，平台根本不看，把它们的多行列表压成单行
> 反而会把本机技能弄坏 —— 所以脚本会跳过。

## 四、发布 payload 只有 9 个键（没有 category）

```
slug / version / displayName / summary / description / tags / license / homepage / changelog
```

**没有 `category`。** 所以分类**不是**「CLI 忘传了」，而是这条通道压根没有它。
另外 `description_zh` / `description_en` 也不在 payload 里 —— 服务端会另外从上传的
`SKILL.md` 里解析。

## 五、13 个分类枚举

| key | 含义 |
|---|---|
| `office-efficiency` | 办公效率 |
| `content-creation` | 内容创作 |
| `dev-programming` | 开发编程 |
| `data-analysis` | 数据分析 |
| `design-media` | 设计多媒体 |
| `ai-agent` | AI Agent |
| `knowledge-management` | 知识管理 |
| `business-ops` | 商业运营 |
| `education` | 教育学习 |
| `professional` | 行业专业 |
| `it-ops-security` | IT 运维与安全 |
| `life-service` | 生活服务 |
| `pay-skill` | 付费技能 |

注意 **`development` 不在枚举内**，对应的是 `dev-programming`。
`GET https://api.skillhub.cn/api/v1/categories` 可查全量。

## 六、文件类型白名单

平台扫描仓库时**逐个文件**校验扩展名，命中一个就整单拒收，报错形如
`不支持的文件类型: icons/xxx-icon.png`。

白名单：`.md .txt .py .js .json .yaml .toml .sh .html .css .csv` 等纯文本。

四类高频越界：

| 文件 | 哪来的 | 怎么处理 |
|---|---|---|
| `.gitignore` / `.gitattributes` | git 仓库自带、点开头 | 迁到 `.git/info/exclude` 与 `.git/info/attributes`（git 官方支持位置，行为一致，但不在工作区、不进仓库） |
| `icons/*.png` | 技能图标 | 图标走平台「图标」入口**单独上传**，本身就不该放进技能目录 |
| `*.template` | 骨架模板 | 改用 `.md` 后缀 |
| `*.zip` / `*.xlsx` / `*.pdf` | 附件、打包产物 | 一律放技能目录之外 |

> **最容易错的一条认知**：「本地打包器已经排除了」≠「发布时不会校验」。
> 本地打包脚本有自己的黑名单，平台走的是**自己的扩展名白名单**，两套规则互不相干。

自查一句话：

```bash
git ls-files | sed 's/.*\.//' | sort -u
```

期望输出只有 `md` / `py` / `json` / `txt` 之类；出现 `gitignore`、`png`、`template` 就要先清理。
