---
name: recruit-page
description: 生成高端黑金风格私人圈子/社群招募长图并发送到飞书。当用户说"生成招募页"、"做一个招募图"、"私人圈子招募页"、"帮我生成会员招募海报"、或提到需要私人俱乐部/高端社群/付费圈子的招募宣传图时触发。支持自定义品牌名、发起人、服务内容、定价、名额等信息。
---

# Recruit Page Generator

生成黑金风格竖版招募长图（750px 宽），适用于私人圈子、付费社群、高端俱乐部等场景。

## 核心脚本

```
scripts/generate.py
```

## 快速使用

### 最简调用（全用默认值，谢导私人圈子）

```bash
python3 scripts/generate.py --output /tmp/recruit.png
```

### 自定义配置

创建 `config.json`，然后：

```bash
python3 scripts/generate.py --config config.json --output /tmp/recruit.png
```

### 生成 + 直接发飞书

```bash
python3 scripts/generate.py \
  --config config.json \
  --output /tmp/recruit.png \
  --send-feishu \
  --receive-id ou_xxx \
  --app-id cli_xxx \
  --app-secret xxx
```

`--receive-id-type` 默认 `open_id`，群聊传 `chat_id`。

## config.json 结构

```json
{
  "brand_name": "谢导私人圈子",
  "tagline": "AI 时代的企业家私人智囊团",
  "badge": "PRIVATE CIRCLE · 私人圈子",
  "hero_intro": "你不缺信息，你缺的是<strong>一个真正懂你的人</strong>在身边。",

  "founder_name": "谢导",
  "founder_emoji": "🔍",
  "founder_tags": ["AI 产品专家", "开源 LLM 业务增长", "心光年创始人", "2000+ 学员"],
  "founder_intro": "负责开源 LLM 商业增长，创办<strong>心光年觉醒读书会</strong>，7.2 万粉丝。",

  "price": "9,980",
  "price_unit": "¥",
  "quota": "30",
  "perks": [
    "每月私董会共创（限 8 人）",
    "年内私聊直通车 · 24h 响应",
    "谢导背书的资源精准撮合",
    "心光年全年共读资料库"
  ],

  "services": [
    {
      "title": "私董会共创",
      "tag": "每月一次 · 深度共创",
      "desc": "谢导带领圈子成员，每月拆解一个<strong>真实 AI 增长案例</strong>。"
    },
    {
      "title": "私聊直通车",
      "tag": "年内随时 · 24h 响应",
      "desc": "随时向谢导提一个问题，<strong>24 小时内必回</strong>。"
    },
    {
      "title": "资源网络撮合",
      "tag": "谢导背书 · 精准对接",
      "desc": "谢导亲自审核每位成员，<strong>定向撮合</strong>你需要的资源。"
    }
  ],

  "for_who": [
    {"icon": "🚀", "title": "想用 AI 做增长的创业者", "desc": "知道 AI 很重要，但不知道从哪里切入"},
    {"icon": "💡", "title": "在某个领域有深厚积累",  "desc": "有专业认知，但缺少高密度的同频交流"},
    {"icon": "🔗", "title": "需要精准资源对接的人",  "desc": "不缺人脉，但缺少真正有质量的引荐"},
    {"icon": "🎯", "title": "处于关键决策节点",      "desc": "面临重大选择，需要一针见血的外部视角"}
  ],

  "footer_quote": "真正的价值，<strong>不在于你认识多少人</strong>，<br>而在于在关键时刻，<strong>有人愿意为你背书</strong>。",
  "year": "2026"
}
```

所有字段均可选，未传的使用内置默认值（谢导私人圈子版本）。

## 飞书发图流程（channel=feishu 时）

脚本内置飞书发送逻辑（`--send-feishu`），也可手动：

```bash
# 1. 获取 token（从 ~/.openclaw/openclaw.json 读取 channels.feishu.appId/appSecret）
# 2. 上传图片 → 获取 image_key
# 3. 发送 image 类型消息
```

详见 `scripts/generate.py` 中的 `send_feishu()` 函数。

## 依赖

- `playwright`（已安装）
- `curl`（系统自带）
- Python 3.10+

## 页面结构

固定 7 个区块（顺序不可变）：

1. **Hero** — 品牌名 + Tagline + 开场白
2. **创始人** — 头像 + 标签 + 简介
3. **为谁设计** — 2×2 网格，4 种目标人群
4. **核心服务** — 1-N 条服务（推荐 3 条）
5. **定价** — 年费 + 权益清单 + 名额
6. **入圈流程** — 固定 4 步（提交→审阅→面谈→入圈）
7. **底部** — 金句 + CTA 按钮 + 品牌签名
