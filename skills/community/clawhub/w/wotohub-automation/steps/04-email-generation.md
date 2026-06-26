# Step 4: 邮件生成

## 目标

基于产品和红人信息，AI 自动生成个性化的合作邀约邮件。当前链路采用：**宿主模型 drafts 优先，脚本仅作显式兼容兜底**；生成对象必须由用户指定；**subject 和正文默认一律使用英文，只有用户明确指定其他语言时才切换**；正文以 HTML 为主，纯文本为兼容 fallback。

新增执行原则：**质量优先于速度**。真实发信场景中，默认应先准备 model-first personalized drafts，再进入发送；不得为了省步骤而默认直接使用 fallback 脚本稿发出。

## 执行步骤

### 4.1 准备邮件要素

**产品信息：**
- 产品名称
- 核心卖点
- 价格/优惠
- 产品链接

**红人信息：**
- 红人昵称
- 频道类型
- 粉丝量
- 往期内容风格

**合作信息：**
- 合作形式：免费样品/付费合作/联盟分成
- 佣金比例（可选）
- 内容要求

### 4.2 生成邮件模板

使用以下Prompt生成个性化邮件：

```
请为[红人昵称]生成一封TikTok红人合作邀约邮件，要求：

产品信息：
- 产品名称：[产品名称]
- 产品卖点：[卖点1, 卖点2, 卖点3]
- 产品价格：$[价格]
- 产品链接：[链接]

红人信息：
- 粉丝量：[粉丝]
- 内容风格：[风格描述]

合作要求：
- 合作形式：免费样品+佣金分成
- 佣金比例：10%
- 内容形式：产品测评/教程视频

要求：
1. 邮件语气友好、专业
2. 突出产品与红人风格的匹配度
3. 强调合作价值（免费产品+佣金）
4. 结尾有明确的CTA
5. 当前 skill 的短邀约模式下，长度控制在150字以内
```

### 4.3 邮件优化

邮件内容完全通用，由数据驱动而非模板：

- **有 GMV 数据**的达人 → 强调销量背书和产品是自然延伸
- **有带货经验**的达人 → 强调内容风格和品类契合
- **高互动率**达人 → 强调受众信任度和社区活跃度
- **品类标签匹配** → 强调内容和产品方向天然对口
- **有历史内容命中**（带货产品 / 视频标题 / 描述 / recentVideos / recentProducts） → 强调“你过去就做过这类内容，这次合作很自然”
- **无明显数据信号** → 通用开场 + 产品核心卖点

更多细节见上方「邮件生成逻辑（通用型）」章节。

## 输出格式

```
## 📧 邀约邮件

**主题：** Partnership Opportunity with [品牌名] for [红人昵称]

**正文：**
Dear [红人昵称],

[生成的邮件内容...]

Best regards,
[你的名字]
[品牌名]
```

## 搜索结果到邀约桥接

### Canonical Campaign Brief（建议主线）

为减少跨步骤字段漂移，建议优先统一到一个 canonical campaign brief，再进入邮件生成。

参考：`references/campaign-brief-schema.md`

邮件生成阶段最低要求：
- `product.productName`
- `outreach.senderName`
- `outreach.offerType`

推荐节奏：
1. 搜索 / 推荐完成
2. 用户确认目标达人
3. 若缺关键 brief，只追问缺口字段
4. 生成模型优先 drafts
5. 脚本仅作兜底

### 先决条件

生成邮件前必须满足：
- 用户已经明确指定目标达人（按 `bloggerId/besId` 或推荐序号；对应执行层字段一般为 `selected_blogger_ids` 或 `selected_ranks`）
- 系统已自动补齐 brief；若仍缺关键字段，只追问缺口，不使用长表单
- 默认输出英文（包括 subject 和正文）；若用户明确指定语言，应优先由宿主模型生成目标语言 drafts；脚本 fallback 保持轻量保守，不作为完整多语言文案引擎
- 默认先由宿主模型生成 `subject + htmlBody + plainTextBody`；没有 `host drafts` 时，不应静默 fallback
- 脚本只在模型 drafts 缺失且操作者显式允许 fallback 时兜底
- 新接入默认应提供 `hostDrafts`；若走 campaign cycle write-back，则使用 `host_drafts_per_cycle`
- 历史兼容入口如 `emailModelDrafts / hostEmailDrafts` 仍可吸收，但不应继续用于新示例或新接入
- 若提供 host drafts，每个 draft 应显式包含目标达人的 `bloggerId/besId`
- 当前 skill 不再依赖 `nickname` 绑定 model drafts；缺少达人 ID 的 draft 会直接回退到脚本兜底
- 脚本 fallback 现提供最小可用的 `en/es/ja/ko` 标题与正文；高质量多语言仍建议由模型层生成

如果缺最小 brief，默认应返回一个轻量补齐模板，优先只追问：
- `productName`
- `senderName`
- `offerType`

推荐追问方式示例：
```text
请直接补齐下面这几个字段（没有的留空也行，我会继续接着补）：
* productName:
* senderName:
* offerType:
```

当前 skill 提供脚本：

```bash
python3 scripts/generate_outreach_emails.py --input /tmp/search-result.json --cooperation sample --limit 10
```

作用：
- 从搜索结果中提取达人信息
- 根据达人标签/风格生成明显差异化的邀约角度
- 默认输出英文邮件（未显式指定语言时，subject 和正文都必须按英文生成）
- 生成前必须先询问用户署名；未拿到署名时，不得用 `[Your Name]`、`Your Name` 或空白署名占位
- 每位达人单独生成差异化邮件
- 当前正文默认控制在 250 个英文单词以内

重要限制：
- `generate_outreach_emails.py` 是 fallback 生成器，不应作为真实批量外发的默认主链路
- 如果是正式发信，优先顺序应为：`达人确认 -> host drafts -> 校验 -> 发送`
- 只有在拿不到 host drafts，且操作者明确接受 fallback 质量时，才应使用脚本稿继续发送
- 当前编排层默认会把“缺少 host drafts”视为阻塞条件，而不是自动回退到 fallback

## 邮件生成逻辑（通用型）

> 邮件生成**完全基于数据驱动**，无固定模板。`generate_outreach_emails.py` 会根据每个达人的**真实数据信号**动态选择最合适的 hook、卖点和 social-proof 片段组合。

### 动态选择机制

| 数据信号 | 触发条件 | 邮件角度 |
|----------|----------|---------|
| 高 GMV | 近30天 GMV > $10,000 | 强调"你的销量数据很亮眼，这款产品是自然延伸" |
| 有带货经验 | `hasProduct=true` | 强调"你已经有带货内容，这是很好的契合点" |
| 历史内容命中 | `historyAnalysis.matchedTerms` 非空，或能提取到历史标题/描述样本 | 强调"你过去就在做这类内容，这次合作延续性很强" |
| 高互动率 | 互动率 ≥ 4% | 强调"你的受众信任你，推什么都能带起来" |
| 品类匹配 | 标签与产品相关 | 强调品类天然契合，内容方向对口 |
| 默认兜底 | 以上均无 | 通用开场 + 产品卖点 |

### 邮件结构（固定段落，非模板）

```
Hi {昵称},

{数据驱动的开场 hook}

{产品核心卖点自然描述}

{数据信号 social-proof（粉丝量/GMV/互动率等）}

{合作方式（sample/paid/affiliate）}
{CTA}
```

所有段落均由片段池随机组合，每次生成均有差异化。

### 卖点翻译

产品卖点关键词会自动翻译为自然语言，例如：
- `vlog camera` → "it's designed for on-the-go vlogging with smooth stabilization"
- `4k video` → "stunning 4K video quality that looks great on camera"
- `face tracking` → "smart face/object tracking so you never lose focus"

扩展卖点池只需编辑 `_ANGLE_POOL` 字典即可。

## 注意事项

1. 邮件长度不宜过长
2. 避免过度推销语气
3. 突出产品独特卖点
4. 提供明确的合作方式
