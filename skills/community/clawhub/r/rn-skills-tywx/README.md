# Xiaohongshu Creator Skill / 小红书爆款创作助手

An automated Claude Code Skill for creating trending Xiaohongshu (Little Red Book) content in the **Fashion & Neo-Chinese Aesthetics** niche.

一个全自动的 Claude Code Skill，专注于**时尚穿搭与新中式美学**赛道的小红书爆款内容创作。

---

## Features / 功能

- **Trend Scouting** — Auto-collect trending topics from Xiaohongshu, Weibo, Douyin, Vogue, Pinterest & Instagram
- **Topic Filtering** — Score and rank topics by relevance, popularity, and originality (with history dedup)
- **Copywriting** — Generate viral-style captions using proven title formulas and engaging body templates
- **AI Image Generation** — Produce 6 editorial-quality images per post via Alibaba Tongyi Wanxiang (通义万相) API
- **Local Export** — Save everything (copy, images, metadata) to organized local folders

---

- **素材收集** — 自动从小红书、微博、抖音、Vogue、Pinterest、Instagram 收集热门趋势
- **选题筛选** — 按赛道匹配度、热度、差异化评分排序（自动去重）
- **文案生成** — 基于 7 类爆款标题公式 + 种草型正文模板生成文案
- **AI 配图** — 通过阿里云通义万相 API 生成 6 张杂志级配图（支持中文 prompt，新中式风格更佳）
- **本地保存** — 文案、图片、元数据按日期+标题归档到本地目录

## Niche Coverage / 赛道覆盖

**Fashion Styles / 穿搭风格：**
Offduty, Softfit, Airy Layering, Staycation, Dark Academia, Sportique

**Neo-Chinese Aesthetics / 新中式美学：**
Neo-Chinese Fashion, Guochao, Tea Ceremony, Incense Art, Calligraphy

## Project Structure / 项目结构

```
rn-skills/
├── .claude/skills/
│   └── xiaohongshu-creator.md   # Main Skill / 主 Skill 文件
├── config/
│   ├── keywords.json            # Niche keywords / 赛道关键词库
│   ├── title-formulas.json      # Title formulas / 爆款标题公式
│   └── image-styles.json        # Image style presets / 图片风格预设
├── output/                      # Generated content / 生成内容输出
└── history.json                 # Creation history / 创作历史记录
```

## Prerequisites / 前置条件

1. [Claude Code](https://claude.com/claude-code) CLI installed
2. Alibaba Cloud DashScope API Key (for Tongyi Wanxiang image generation)
   - Get it from [阿里云百炼平台](https://bailian.console.aliyun.com/)

```bash
export DASHSCOPE_API_KEY="sk-your-key-here"
```

## Usage / 使用方式

Open Claude Code in this project directory, then:

在本项目目录下打开 Claude Code，然后：

```
# Full pipeline — generate 2 posts / 全自动生成 2 条笔记
创作小红书

# Trend scouting only / 仅收集素材和推荐选题
收集素材

# Create from a specific topic / 指定选题创作
根据"新中式茶道穿搭"创作

# Custom count / 自定义数量
创作小红书 3条
```

## Output / 输出示例

Each run creates a timestamped folder under `output/`:

每次运行会在 `output/` 下创建带时间戳的文件夹：

```
output/2026-03-15_新中式叠穿/
├── 文案.md          # Title + body + hashtags / 标题+正文+话题标签
├── cover.png        # Cover image / 封面图
├── page_1.png       # Full outfit shot / 全身穿搭展示
├── page_2.png       # Detail close-up / 细节特写
├── page_3.png       # Side/back angle / 侧面/背面
├── page_4.png       # Scene interaction / 场景互动
├── page_5.png       # Accessory close-up / 配饰特写
└── metadata.json    # Creation metadata / 创作元数据
```

## Cost Estimate / 成本估算

Using Tongyi Wanxiang `wanx2.1-t2i-turbo` model:

使用通义万相 `wanx2.1-t2i-turbo` 模型：

| Item / 项目 | Cost / 成本 |
|------|------|
| turbo (~6 images/post) | ~¥0.24/post |
| 2 posts/day | ~¥0.48/day |
| Monthly (60 posts) | ~¥14.4/month (~$2) |
| plus model (higher quality) | ~¥0.96/post, ~¥57.6/month (~$8) |

## License / 许可

MIT
