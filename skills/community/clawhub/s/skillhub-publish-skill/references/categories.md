# 分类与二级标签（category / subCategories）

## 为什么需要单独讲

发布 Skill 时**分类是选填的**，前端表单明确标注「（选填）」，
且前端的 `buildPayload` 在两者都为空时**完全不传这两个字段**
（而不是传空串）。结果就是：不传 → 平台存空 → 后台显示「未分类」。

`publish.py` 在 1.7.0 之前**从未构造过这两个字段**，所以用脚本发的技能
一律是「未分类」，而走网页后台发的通常有分类 —— 这就是同一批技能里
「有的有分类、有的没有」的原因。

## 字段规格（从前端 bundle 的 buildPayload 反查）

```js
// 精简后的前端逻辑
const c = form.category?.trim() ?? "";
let u = {};
c ? u = { category: c, subCategories: form.subCategories ?? [] }
  : prevCategory && (u = { category: prevCategory, subCategories: [] });
return { slug, displayName, version, summaryZh, changelog, iconUrl, ...u };
```

| 字段 | 类型 | 约束 |
|---|---|---|
| `category` | string（key） | **单选**，一级分类的 `key` |
| `subCategories` | string[]（key 数组） | **最多 3 个**，且必须属于所选一级分类 |

**关键**：两者都为空时**不要传**这两个字段。传空串 `""` 反而可能被存成脏值。

## 分类数据从哪来

两个**公开端点**（不带 token 也能拿）：

```
GET /api/v1/categories     -> {count, items:[{key, level, name, nameEn, sortOrder, active}]}
GET /api/v1/subcategories  -> {count, items:[{key, parentKey, name, ...}]}
```

本脚本封装：

```bash
python publish.py categories                  # 列全部（一级 + 二级）
python publish.py categories --parent dev-programming   # 只看某个一级下的二级
python publish.py categories --json           # 机器可读
```

⚠️ **别用前端 bundle 里的兜底表当权威**。bundle 里有个 `Bg` 常量列了 7 个分类
（`ai-intelligence` / `developer-tools` / `productivity` / ...），那是**离线兜底**，
和线上真实 key **完全对不上**。以 `/api/v1/categories` 的返回为准。

## 怎么填：category 与 subCategories 的 CLI / frontmatter 两种写法

### 写法 A：CLI 参数（临时用）

```bash
python publish.py publish ./my-skill \
    --category dev-programming \
    --subcategory dev-script --subcategory dev-code-gen
```

`--subcategory` 可重复传，超过 3 个会被截断并告警。

### 写法 B：写进 SKILL.md frontmatter（推荐，长期生效）

```yaml
category: dev-programming
subCategories: [dev-script, dev-code-gen]
```

也接受逗号分隔的字符串：`subCategories: dev-script, dev-code-gen`。

**优先级**：CLI 参数 > frontmatter。写进 frontmatter 后每次发版自动带上，
不用记着传参 —— 这是避免「下次发版又变未分类」的正解。

## 校验行为

`resolve_category()` 会在提交前校验：

| 情况 | 行为 |
|---|---|
| `category` key 不存在 | **剔除**，不提交分类，打 WARN 并提示用 `categories` 查 |
| `subCategories` 里有不属于该一级分类的 | **剔除该条**，其余保留，打 WARN |
| `subCategories` 超过 3 个 | 截断到 3 个，打 WARN 并列出被丢弃的 |
| 网络/接口失败 | 跳过校验按原样提交，打 WARN（不阻断发布） |

设计取舍：**宁可少提交也不要提交错误值**。平台对未知 key 是报错还是静默接受
未实测，剔除更安全，也让用户看见自己写错了。

## 回读与补录

```bash
python publish.py mine        # 列表新增「分类」列，未分类的会显式标出
```

已发布的技能想补分类 → **发一个新版本**（分类只在 publish 时提交，
没有独立的改分类端点，和图标同理）：

```bash
# 1. 先把分类写进 SKILL.md frontmatter（一劳永逸）
# 2. 升版本号
# 3. 重新发布
python publish.py publish ./my-skill --changelog "补上分类标签"
```

## 本机 7 个技能的分类对照（2026-09-19 定）

| slug | 一级分类 | 二级标签 |
|---|---|---|
| `skillhub-publish-skill` | `dev-programming` 开发编程 | `dev-script`, `dev-git` |
| `zero-dep-icon-gen` | `design-media` 设计多媒体 | `design-image-gen`, `design-visual-asset` |
| `web-console-cdp-upload` | `dev-programming` 开发编程 | `dev-script` |
| `aliyun-oss-static-deploy-skill` | `it-ops-security` IT 运维与安全 | `itops-devops`, `itops-config` |
| `aliyun-oidc-cert-renew` | `it-ops-security` IT 运维与安全 | `itops-devops`, `itops-security-scan` |
| `wechat-file-organizer` | `office-efficiency` 办公效率 | `office-automation`, `office-doc` |
| `workbuddy-checkin` | `office-efficiency` 办公效率 | `office-automation` |

⚠️ `wechat-file-organizer` 线上当前是「开发编程」（早年走网页后台发的），
按上表应属「办公效率」。想纠正需发新版本（分类只在 publish 时提交）。

## 平台全部一级分类（13 个，2026-09-19 实测）

`pay-skill` / `office-efficiency` / `content-creation` / `dev-programming` /
`data-analysis` / `design-media` / `ai-agent` / `knowledge-management` /
`business-ops` / `education` / `professional` / `it-ops-security` / `life-service`

二级分类共 96 个，每个一级下 8 个。完整列表用 `publish.py categories` 拉。
