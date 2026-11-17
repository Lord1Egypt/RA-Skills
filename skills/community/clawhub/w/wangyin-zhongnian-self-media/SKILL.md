---
name: wangyin-zhongnian-self-media
description: 网瘾中年的自媒体技能——微信公众号「网瘾中年」专用内容生产与发布全流程。覆盖选题评估、创作简报、爆款公式匹配、公众号原生写作、去AI味精修、AIGC合规守门、封面生成、草稿箱推送、数据复盘九个环节。触发词："写一篇公众号""发一篇""推草稿箱""推送草稿""做选题""软广""日报排版""复盘阅读数据""爆款公式""网瘾中年"。不用于X/小红书/抖音等其他平台创作，不用于纯代码任务，不用于视频号发布（走独立视频自动化）。
---

# 网瘾中年的自媒体技能

> 基于 [yanhua1010/self-media-content-workflow](https://github.com/yanhua1010/self-media-content-workflow)（MIT）改造。
> 通用多平台套件 → 微信公众号「网瘾中年」单账号专用。发布层由 wenyan CLI 替换为本机已验证的 baoyu-post-to-wechat 通道。

## TL;DR 路由

| 用户说 | 入口 |
|---|---|
| 「写一篇/发一篇 XX」 | 第 1 步选题评估起，走完 1→8 |
| 「把这篇推草稿箱」（文章已存在） | 第 5 步起：去AI味→合规→封面→推送 |
| 「这个选题能不能写」 | 只跑第 1 步，输出判定 |
| 「日报数据怎么样/复盘」 | 只跑第 9 步 |
| 推送报错 | 直接查第 8 步 fallback 表 |

## 账号档案（硬编码，不可猜测）

| 项 | 值 |
|---|---|
| 公众号 | 网瘾中年（AppID `wxd1a166e3a3e98b5c`，账号名 `wangyinzhongnian`） |
| 作者 | Eric，12 年汽车零部件研发，300+ 检测报告、40+ 量产车型 |
| 定位 | 汽车 NVH 圈里的 AI 熟练工——用工程经验挣钱，AI 只是工具 |
| 读者 | 汽车零部件工程师（小白到 10 年），痛点驱动、同行传播 |
| 尾签 | `> **Eric** \| 公众号「网瘾中年」`（唯一合法尾签） |
| 文章目录 | `C:\Users\guoyu\WorkBuddy\WorkBuddy实用课程\`，命名 `YYYYMMDD_网瘾中年_标题.md` |

## 工作流（9 步，顺序执行）

每步输入/输出速查（执行时逐步核对，缺输出不得进入下一步）：

| 步 | 输入 | 输出 |
|---|---|---|
| 1 选题评估 | 一句话选题/链接/素材 | 通过判定 或 弃用原因+2 个替代选题 |
| 2 创作简报 | 模糊选题 | ≤3 问确认后的简报（清晰选题跳过） |
| 3 公式匹配 | 已通过选题 | 公式编号（1-5）+ 匹配理由 |
| 4 正文写作 | 公式+简报 | 完整 md 文章（frontmatter 含 title） |
| 5 去 AI 味 | 初稿 md | 零残留扫描报告 + 精修稿 |
| 6 合规守门 | 精修稿 | 守门员退出码 + 放行/阻断结论 |
| 7 封面生成 | 终稿标题 | ≥1 张封面图路径 |
| 8 推送草稿箱 | 终稿+封面+用户确认 | media_id 或失败诊断 |
| 9 数据回填 | media_id/后台数据 | memory 记录 + 追踪文件更新 |

### 1. 选题评估

输入一句话选题/链接/素材，按顺序检查：

1. 扫描座椅红线词（座椅/滑轨/调角器/头枕/腰托/靠背/坐垫/Brose/博泽）→ **命中即整题弃用，无例外**。
2. 扫描境外未备案 AI 品牌（Codex/OpenAI/ChatGPT/Cursor/Claude Code/Anthropic 等）→ 命中则换 R5 白名单工具（WorkBuddy/DeepSeek/Kimi/Qwen/通义灵码等）或弃题。
3. 检查同主题 7 天内是否已发（查 `C:/Users/guoyu/WorkBuddy/Claw/.workbuddy/memory/wechat-data-tracking.md` 或近期文章目录）→ 重复则延期。
4. 工具/产品类选题：无一手实测（真实截图 ≥6 + 翻车 ≥1 + 可复制交付物）→ 降级进日报或改纯观点文，规则见 `C:/Users/guoyu/WorkBuddy/Claw/.workbuddy/memory/tool-review-standards.md`。

**失败分支**：4 项任一不通过 → 输出弃用原因 + 2 个替代选题方向，停止，不进入第 2 步。

### 2. 创作简报（可跳过）

选题模糊时最多问 3 个问题：目标读者层级（小白/进阶/B 端）、内容目标（涨粉/信任/转化）、核心判断一句话。用户已明确的不重复问。清晰选题直接跳到第 3 步。

### 3. 爆款公式匹配（写大纲前强制）

从 5 套公式选 1 套，规则文件 `C:/Users/guoyu/WorkBuddy/Claw/.workbuddy/memory/viral-formula-selector-rules.md`：教程类默认公式一；收尾文强制公式五；日报用 B 组公式需检查冷却期（连续 2 发后必须换结构或停 3-5 天，见 references/data-conclusions.md）。

**失败分支**：无公式可匹配 → 说明原因，按公式一兜底，并在产出中标注 `formula: fallback-1`。

### 4. 正文写作

规范详见 [references/writing-standards.md](references/writing-standards.md)。硬底线：

- ≥1500 字（周更长文 ≥10000 字）；有案例 + AI 辅助点 + 可复用工具。
- 标题：教程 ≤15 字、观点/故事 ≤30 字、测评 ≤20 字、日报 20-50 字；须含数字；禁「我/我用 WorkBuddy/我用 AI」开头；禁末尾「…」；禁「12 年」主打。教程类合规样例：《NVH报告归档从3天压到10分钟》（13字·含数字·不以「我」开头）。
- 第一人称承担判断，从具体经历/冲突/结果进入，禁行业套话开头。
- 强制大纲骨架（写正文前先按此填充，占满才动笔）：
  1. 钩子：一个具体冲突/翻车瞬间（≤80字）
  2. 背景：为什么这件事值得汽车零部件工程师关心（1段）
  3. 做法：分步操作，每步给 prompt/命令/参数（核心，占全文 60%）
  4. 结果：量化前后对比（必须含数字）
  5. 复用：读者可直接抄走的模板/清单
  6. 尾签 `> **Eric** \| 公众号「网瘾中年」` + 2-3 个 `#标签`
- 文末 2-3 个精准 `#标签`（禁 #AI #公众号 #自媒体 #汽车 等宽词），词库 `C:/Users/guoyu/WorkBuddy/Claw/.workbuddy/memory/wechat-tag-library.md`。
- WorkBuddy 教程类：先读 `C:/Users/guoyu/WorkBuddy/Claw/.workbuddy/memory/workbuddy-official-docs-canonical.md`，文末加 `📘 官方文档正典：<URL>`。

### 5. 去 AI 味精修（强制，不得跳过）

执行 deslop-zh + anti-slop-taste 双检查：破折号替换、「不是A而是B」重写、AI 黑话清除（赋能/抓手/闭环/沉淀等典型套话）、段末总结句删除。跑 `anti_slop_check.py` 扫描至零残留。

**失败分支**：扫描仍有残留 → 修复后二次扫描；连续 3 轮仍残留 → 🛑 **STOP**：列出残留项交人工处理，不得带残留进入第 6 步。

### 6. AIGC 合规守门（强制，不得跳过）

```
python C:/Users/guoyu/.workbuddy/skills/aigc-compliance-guard/scripts/compliance_precheck.py <文章.md>
```

- 退出码 0 → 放行。
- 退出码 1 → 🛑 **STOP：硬阻断，禁止推送**。按报告改写后重跑，直至 0 或 2。三轮改写仍为 1 → 弃题，回第 1 步换选题。
- 退出码 2 → 🔴 **CHECKPOINT：人工复核**。逐条判断灰名单命中是否为正常资讯语境，误报放行须把理由记录到当日 memory。

红线全集见 [references/compliance-redlines.md](references/compliance-redlines.md)。**禁止在文中加任何免责声明/备案链接**（贴条即违规）。

### 7. 封面生成

≥1 张，大字数字、强对比；禁纯白底小字封面。按文章类型三选一：

- 日报：固定纯蓝版式，跑 `C:/Users/guoyu/WorkBuddy/Claw/公众号文章撰写/generate_daily_cover.py`（900×420，渐变 `#1a3a6c→#2d6cb5`）。
- 教程/观点/软广：文生图，火山 ARK（`ARK_API_KEY` 环境变量，BASE_URL `https://ark.cn-beijing.volces.com/api/v3`，模型 `doubao-seedream-5-0-260128`），尺寸 900×500，提示词须含「大字数字+强对比+工程蓝」要素。
- 兜底：PIL 纯色底大字版式（字号 ≥120px，底色深蓝 `#004a85`，文字白色）。

**失败分支**：文生图 API 失败 → 降级 PIL 纯色大字版式；PIL 也失败 → 用最近一张同类型封面兜底并标注。

### 8. 推送草稿箱

🔴 **CHECKPOINT：推送属外部写操作。除非用户已在本轮明确说「推送/发草稿箱」，否则先展示标题+摘要+封面，等确认。**

唯一合法命令（已验证）：

```
cd "<文章所在目录>" && npx -y bun "C:\Users\guoyu\.workbuddy\skills\baoyu-post-to-wechat\scripts\wechat-api.ts" <文章.md> --theme modern --color "#005BAC" --no-cite --cover <封面路径> --account wangyinzhongnian
```

- 标题含空格时不用 `--title` 参数（解析异常），写进 frontmatter `title` 字段。
- 只写草稿，**永不群发**。

**失败分支（三段式 fallback 表）**：

| 触发条件 | 一线修复 | 仍失败兜底 |
|---|---|---|
| 报 `40164`（IP 不在白名单） | 停止重试，`curl -s ifconfig.me` 输出当前出口 IP，提示 Eric 去公众号后台「设置与开发→基本配置→IP白名单」添加，等确认后重推 | 出口 IP 再次跳变 → 重新查 IP 给 Eric 二次添加；连续 3 次跳变 → 交付手动发布包（文章 md + 封面 + 推送命令），当日停止自动重试 |
| 报 `45106` | 官方已停用素材永久化接口，忽略该错误 | 检查草稿箱是否实际入箱：有 media_id 返回 = 成功；无 media_id → 按「其他错误」处理 |
| 报 `Cannot find module '@baoyu-skills/wechat-api'` | 用错了废弃脚本（`C:\Users\guoyu\.baoyu-skills\` 旧版），改用第 8 步唯一合法路径重跑 | 合法路径也报模块缺失 → `npx -y bun --version` 检查 bun 可用性，输出诊断结果交人工 |
| 报 `40001`/`42001`（token 无效或过期） | 检查 `C:\Users\guoyu\.baoyu-skills\.env` 凭证是否存在且未改动 | 凭证在但仍失败 → 停止，提示 Eric 核对 AppSecret 是否被重置，不猜测不重试 |
| 封面文件不存在或路径错 | 核对 `--cover` 参数指向的文件是否存在，修正相对/绝对路径 | 封面确实缺失 → 回到第 7 步重新生成，禁止无封面推送 |
| 其他未知错误 | 原样输出完整报错，不猜测原因 | 不换野路子通道（禁 wenyan/手写 requests），交付手动发布包并记录报错到当日 memory |

### 9. 数据回填与复盘

推送成功后：media_id 写入当日 `.workbuddy/memory/YYYY-MM-DD.md`；发布后数据（阅读/在看/收藏/评论）回填 `C:/Users/guoyu/WorkBuddy/Claw/.workbuddy/memory/wechat-data-tracking.md`。复盘只比较同类型同时段基线，样本 <3 不改长期策略。数据结论沉淀见 [references/data-conclusions.md](references/data-conclusions.md)。

## 反例黑名单（不要做什么）

- ❌ 不写座椅及子系统内容——无例外，命中即弃。
- ❌ 不用 wenyan CLI / `.baoyu-skills` 旧脚本 / 手写 requests 调公众号 API——唯一通道是第 8 步命令。
- ❌ 不加免责声明、备案链接、「AI 辅助生成」标识贴条。
- ❌ 不出现 `workbuddy.homes` / AlephAITech / 「📚 延伸阅读」/ MIT License 字样于正文。
- ❌ 不用「12 年老兵 × AI 实践者」口号；不用非标准尾签。
- ❌ 不跳过去 AI 味检查和合规守门员，哪怕用户催得急。
- ❌ 不直接群发；不在未确认时推送草稿箱。
- ❌ 不编造阅读量、转化数据、用户评价；后台没有的字段留空不估算。
- ❌ 18:30 后不发工具教程/泛观点（数据证实无效档），只发钱类/复盘/B 端/互动内容。
- ❌ 标题不出现截断符「…」、不以「我」开头、教程类不超 15 字。

## 与源套件的模块映射

| 源模块（9 个） | 本技能去向 |
|---|---|
| content-workflow 总控 | 本文件 9 步工作流 |
| content-brief | 第 2 步 |
| content-strategy | 弃用（账号定位已固化在档案区） |
| trend-radar | 第 1 步选题评估 + 日报自动化承担 |
| platform-copywriting | 第 4 步 + references/writing-standards.md |
| short-video | 弃用（视频线由独立自动化 1779081620573 承担） |
| content-analytics | 第 9 步 |
| content-delivery | 第 8-9 步（命名/目录规范已内化） |
| wechat-publisher | 第 8 步（wenyan → baoyu-post-to-wechat） |
