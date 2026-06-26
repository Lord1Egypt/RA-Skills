# Seedream Image Skill | Seedream 即梦 图像技能

**EN:** [Seedream 5.0/4.0](https://jimeng.jianying.com/) (即梦AI) — text-to-image, image editing, multi-image fusion, character consistency, knowledge cards, posters, PPT, e-commerce, group/storyboard; describe idea → review prompt → confirm and auto-download to `output/`.  
**中文：** 即梦AI — 文生图、图生图、多图融合、角色一致性、知识卡片、海报、PPT、电商、组图/分镜；描述想法 → 审核提示词 → 确认后自动下载到 `output/`。

[English](#english) | [中文](#中文)

---

<a id="english"></a>

## English

### Features

- **Text-to-image** — Portraits, landscapes, posters, cards; 200+ style keywords
- **Image editing** — Style transfer, element add/remove, lighting, retouching
- **API generation** — One-command via `generate.py`; images auto-download to `output/`
- **Character consistency** — Same face/clothing/pose across multiple images (storyboards)
- **Knowledge cards** — Infographic, tarot, blueprint, game card, scroll styles
- **E-commerce** — Product photography, brand-style prompts
- **Multi-image fusion** — Up to 10 reference images with element control
- **Group generation** — Up to 10 related images per call (storyboards, variations)
- **Text in images** — 99%+ accuracy for Chinese/English when wrapped in quotes

### Install

```bash
npx skills add ppdbxdawj/ai-skills@seedream-image
```

Manual: `git clone https://github.com/ppdbxdawj/ai-skills.git` → `cp -r ai-skills/seedream-image ~/.cursor/skills/`

### How It Works

1. **Describe** your image idea in natural language.
2. **Review** the agent-generated Seedream prompt.
3. **Confirm** (and say if you need multiple images). The agent runs the API and downloads to `output/`.

**One-time setup:** [Volcengine IAM](https://console.volcengine.com/iam/keymanage/) keys + enable [Jimeng 4.0](https://console.volcengine.com/ai/ability/detail/10). In the folder that contains `generate.py`, create `.env` with `VOLC_ACCESSKEY` and `VOLC_SECRETKEY`, or export them. Run `pip install -r requirements.txt`. Do not commit `.env`.

### Example Prompts

**Portrait Photography**
```
Young Asian man, clean features, black oversized sweater,
sitting by library window reading, sunlight on side face,
Tyndall light, cool tones, shallow depth of field, 85mm prime lens,
cinematic realism style, ultra HD
```

**Knowledge Card (Fantasy RPG Style)**
```
Design a fantasy RPG game skill card explaining "[CONCEPT]".
Include a cool glowing icon, skill description in game language,
energy cost and cooldown timer. Dark fantasy style with luminous
magical rune borders.
```

**E-commerce Product Shot**
```
Create a product showcase for this [PRODUCT] in [BRAND] style,
clean white background, highlighting texture and material quality,
professional commercial photography, high contrast.
```

### Use Cases

| Scenario | Key Prompts |
|----------|-------------|
| Social media avatar | `square composition` `solid background` `icon style` |
| Knowledge card | `infographic` `clean layout` `target audience: ...` |
| PPT background | `for PPT cover background` `whitespace` `matte background` |
| E-commerce hero | `product hero shot` `commercial photography` `clean background` |
| Poster design | `movie poster level` `dramatic lighting` `large whitespace` |
| Brand design | `brand VI visual` `include logo/packaging/cards` |
| Character cosplay | `keep face unchanged` `realistic costume` `same pose` |
| Storyboard / comic | `generate a set of comics` `storyboard` `group image` |
| Education | `comparison chart` `info poster` `knowledge explainer` |

<details>
<summary><b>Advanced: Manual CLI Usage</b></summary>

```bash
# Text-to-image (default: 1 image)
python generate.py --prompt "A cute cat in a garden, watercolor style"

# Image editing (with reference image)
python generate.py --prompt "Change background to beach" --image-urls "https://example.com/photo.jpg"

# Specify resolution (still 1 image by default)
python generate.py --prompt "Product hero shot" --width 2560 --height 1440

# Group image generation (use --no-force-single)
python generate.py --prompt "Generate 4 blind box figures: crow, rabbit, dog, cat" --no-force-single
```

</details>

### File structure

`SKILL.md` · `generate.py` · `requirements.txt` · `examples.md` · `reference.md` · `marketplace.json`

---

<a id="中文"></a>

## 中文

### 功能特性

- **文生图** — 人物、风景、海报、卡片；200+ 风格词
- **图像编辑** — 风格迁移、元素增删、光影、人像美化
- **API 生图** — 一键调用 `generate.py`，图片自动下载到 `output/`
- **角色一致性** — 多图保持同一人脸/服装/姿势（分镜可用）
- **知识卡片** — 信息图、塔罗、蓝图、游戏技能卡、古籍风
- **电商** — 产品图、品牌风格
- **多图融合** — 最多 10 张参考图、元素可控
- **组图** — 一次最多 10 张（分镜、变体）
- **图中文字** — 中英文用引号包裹，99%+ 准确率

### 安装

```bash
npx skills add ppdbxdawj/ai-skills@seedream-image
```

手动：克隆仓库后执行 `cp -r ai-skills/seedream-image ~/.cursor/skills/`

### 使用流程

1. **描述**想法（自然语言）
2. **审核** Agent 生成的 Seedream 提示词
3. **确认**（需多张时说明），Agent 调 API 并下载到 `output/`

**首次配置**：在 [火山引擎 IAM](https://console.volcengine.com/iam/keymanage/) 获取密钥并开通 [即梦 4.0](https://console.volcengine.com/ai/ability/detail/10)。在 `generate.py` 所在目录建 `.env` 写入 `VOLC_ACCESSKEY`、`VOLC_SECRETKEY`，或使用环境变量。执行 `pip install -r requirements.txt`。勿提交 `.env`。

### 提示词示例

**人物写真**
```
清秀亚洲青年男性，黑色宽松毛衣，坐在图书馆靠窗位置低头看书，
窗外阳光透进来打在侧脸，丁达尔光，冷色调，浅景深背景虚化，
85mm定焦，写实电影剧照风格，超高清
```

**知识卡片（游戏技能卡风格）**
```
设计一张幻想RPG游戏中的技能卡片，用文字和图像解释"[概念]"。
有游戏化的技能名称，卡片上有酷炫图标、技能描述（用游戏化语言解释概念）、
消耗的"精力值"和冷却时间。整体是暗黑奇幻风格，带有发光的魔法符文边框。
```

**电商产品图**
```
为这件[产品]创建网店展示图，风格类似于[GUCCI/PRADA/Nike]，
简洁白色背景，突出产品质感，专业商业摄影风格，高对比度。
```

### 使用场景速查

| 场景 | 关键提示词 |
|------|-----------|
| 社交头像 | `正方形构图` `纯色背景` `图标风格` |
| 知识卡片 | `信息图` `排版清晰` `目标受众：...` |
| PPT 背景 | `用于PPT封面背景` `留白构图` `哑光背景` |
| 电商主图 | `电商主图` `产品展示` `专业商业摄影` |
| 海报设计 | `电影海报级别` `戏剧光` `大面积留白` |
| 品牌设计 | `品牌VI视觉` `包含logo/包装/卡片` |
| 角色 Cos | `保持人脸不变` `写实质感服饰` `相同姿势` |
| 分镜漫画 | `生成一组漫画` `分镜图` `组图` |
| 教育培训 | `对比图` `信息海报` `知识科普` |

<details>
<summary><b>进阶：手动命令行用法</b></summary>

```bash
# 文生图（默认 1 张）
python generate.py --prompt "一只猫在花园里玩耍，水彩风格"

# 图像编辑（传入参考图）
python generate.py --prompt "将背景换成海滩" --image-urls "https://example.com/photo.jpg"

# 指定分辨率（默认 1 张）
python generate.py --prompt "电商主图，产品特写" --width 2560 --height 1440

# 组图生成（加 --no-force-single）
python generate.py --prompt "生成4张分别关于春夏秋冬的盲盒组图" --no-force-single
```

</details>

### 文件结构

`SKILL.md` · `generate.py` · `requirements.txt` · `examples.md` · `reference.md` · `marketplace.json`
