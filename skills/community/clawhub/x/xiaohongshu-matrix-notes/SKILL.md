---
name: xiaohongshu-matrix-notes
description: Use when producing 小红书/RedNote matrix-account image+text 笔记 at scale — mimicking a 对标(benchmark) account and turning product photos into AI model try-on / lifestyle / still-life images plus 种草 captions for women's fashion (穿搭/大码/包/鞋) seeding accounts.
---

# 小红书矩阵号图文生产

把"对标账号 + 产品图"批量变成像该账号的小红书图文笔记(AI 出图 + 文案)。一条已跑通 50+ 篇的流水线。

## When to use
- 要为某个新小红书号(矩阵号)按某个对标账号的风格批量产出笔记
- 有产品图(衣/包/鞋),要做成"真人模特上身 / 真人生活大片 / 产品静物"图 + 文案
- 要给某号补轮次(同博主、新产品/场景)

## 8 步流程
| 步 | 做什么 | 用什么 |
|---|---|---|
| 1 采集 | 扒对标账号真实笔记做风格拆解(标题公式/图数/封面/配色/选题/标签) | `scripts/fetch_xhs.py <user_id> <名> <页数>`(tikhub) |
| 2 定博主 | 出 1 张定妆图锁脸(或用对标提供的脸),**交用户确认**后才批量 | `scripts/ofox_gen.py "<prompt>" persona.png` |
| 3 选品 | 从素材选符合该号调性的产品(注意颜色款,核对避免出错款) | 人工 + 拼缩略图 |
| 4 场景 | **每篇分配不同场景**(硬性);篇内一致 | 写进 prompt |
| 5 批量出图 | 博主图+产品图双参考,并发 3 + 重试 | `scripts/ofox_gen.py` 批量(见 batch 模式) |
| 6 封面 | 穿搭合集号=竖条拼贴+标题;生活/静物号=单图取最佳 | `scripts/build_cover.py`(拼贴号) |
| 7 文案 | 套该号标题公式 + 口吻 + 标签 | 按风格拆解写 |
| 8 自检 | **逐篇核对全部**:博主一致/产品高保真/无裁切/调性对 | 拼总览图逐一看 |

## 关键脚本(scripts/)
- **fetch_xhs.py** — tikhub 采集。需 `TIKHUB_TOKEN`。key 权限通常是 `xiaohongshu/app_v2`(非 web_v3),用 `get_user_posted_notes`。给 UA 头避免 403。
- **ofox_gen.py** — Ofox `openai/gpt-image-2` 出图。需 `OFOX_API_KEY`(sk-of-…)。无参考图=文生图;有参考图=`/images/edits`(博主图+产品图)。内置重试(SSL 易断)。
- **build_cover.py** — 竖条拼贴封面:人脸检测对齐 + 标题。需中文 Black 字体(见下)。

## 血泪经验(务必读 references/lessons.md)
- **出图通道**:OpenRouter 常报"region not available";用 **Ofox**(`api.ofox.ai/v1/images/...`)。
- **跨图锁脸**:每次出图都带同一张定妆图做参考 → 人物一致。
- **封面对齐**:细节多,优先用 `build_cover.py`;若某 look 检测失败裁头/空格,**换掉那张 look**(每篇多出 1-2 张备用)而不是硬调算法。
- **产品高保真**:prompt 写"严格保留颜色/版型/细节";每篇至少 1 个主推产品高度还原,配饰(帽/镜)可为装饰不必自家。
- **生活种草号博主**:白皙透亮、有生命力(明亮阳光+干净暖墙+动态灿笑)、贵妇非名媛、浅色夏装;**忌**暗沉/油腻精修/普通阿姨感。

## 铁律
- **照对标号真实长相还原,别脑补"高级感"**:背景元素/拍摄视角/精修程度/封面排版全照搬对标号描述进 prompt。自己想象 ins 风 = 必出 AI 棚图。
- **静物号背景=真实居家随手拍**(木地板/草编毯/裙摆/自然光),prompt 明写"不要影棚不要精修";每篇 4 产品为底 + 2 上脚(见 references)。
- **标题/选题照对标爆款公式,别写「产品名+卖点」种草模板**:先扒对标 summary.md 爆款榜,提炼该号自己的公式(生活方式号=情绪/瞬间;旅居号=固定句式如"在意大利常背的…";度假号=英文vibe+emoji;店主号=对话小剧场)。模板腔=没钩子=划走。
- **出图前先问用户**(尤其新博主/新方向);定妆图、pilot 是强制确认点。
- **做完逐项自检全部结果**再汇报(不抽查)。
- 每篇场景互不相同;每篇至少一个主推产品高度还原。

## 字体(build_cover 需要)
下载一次:`curl -sL -o scripts/fonts/NotoSansSC.ttf "https://github.com/google/fonts/raw/main/ofl/notosanssc/NotoSansSC%5Bwght%5D.ttf"`(可变字重,用 Black)。

## 参考
- `references/lessons.md` — 全部踩坑与解法
- `references/persona-and-style.md` — 博主设定 + 风格拆解模板
