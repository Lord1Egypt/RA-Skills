# 微信公众号文章自动生成技能

> 从抓取同行到生成 MUX 版图文的完整自动化流水线

---

## 📌 技能概述

**技能名称**: `wechat-article-auto-gen`

**版本**: 1.0.0

**适用场景**:
- 公众号文章批量创作
- 同行文章改写 MUX 化
- AI 配图生成
- 封面设计自动化

**核心能力**:
- ✅ 文章抓取与解析
- ✅ AI 内容改写
- ✅ 分镜自动拆分
- ✅ 提示词生成
- ✅ AI 配图生成（火山方舟/即梦）
- ✅ 封面设计
- ✅ HTML 交付

---

## 🎯 标准工作流

### Phase 1: 需求确认（5 分钟）

**输入**:
- 文章主题
- 目标受众
- 核心信息（门店、活动、服务）
- 参考文章（可选）

**输出**:
- 文章大纲
- 配图需求（6-8 张）
- 封面设计要求

---

### Phase 2: 内容创作（30 分钟）

#### 模块 A: 标题生成

**原则**:
1. 品牌优先（MUX 开头）
2. 简短有力（≤15 字）
3. 价值明确

**标题公式**:
```
MUX | [核心价值/主题]
```

**示例**:
```python
TITLES = [
    "MUX | 教练团带你科学训练",
    "MUX | 常熟人的减脂增肌指南",
    "MUX | 150 分钟健身真相",
]
```

---

#### 模块 B: 文章结构

**标准结构**:
```markdown
💪 科学健身 · 专业指导 · 成就更好的自己

🏋️ 5 家门店 | ⏰ 11:00-23:00 | 👨🏫 专业教练 | 🎯 一对一

[开篇引入：痛点共鸣 + 本地化表达]

## 章节 1: [核心内容]
[正文 + 配图 1]

## 章节 2: [核心内容]
[正文 + 配图 2]

...

## 真实案例
[数据支撑]

## 行动号召
[到店体验引导]

─────────────────────
📍 MUX 米欧克斯健身（5 店通用）
⏰ 营业时间：11:00-23:00
💪 服务：专业健身指导 | 器械训练 | 团课
🎁 特色：新手友好 | 环境好 | 教练专业
```

---

#### 模块 C: 同行文章改写（可选）

**流程**:
```python
def rewrite_article(source_url, brand="MUX"):
    # 1. 抓取原文
    raw = scrape_article(source_url)
    
    # 2. AI 改写（MUX 化）
    rewritten = llm_rewrite(
        raw,
        prompt=f"""
        将以下文章改写为{brand}品牌版本：
        - 品牌名称替换为{brand}
        - 门店信息替换为{brand}实际门店
        - 语气口语化、真实可信
        - 避免绝对化用词
        - 添加团购引导
        """
    )
    
    # 3. 合规检查
    if not compliance_check(rewritten):
        return rewrite_article(source_url, brand)  # 重试
    
    return rewritten
```

---

### Phase 3: 配图生成（30 分钟）

#### 火山方舟配置

```python
VOLCANO_CONFIG = {
    "api_key": "565ec265-1b1e-4fa4-bcd8-c3d37c6a6198",
    "api_url": "https://ark.cn-beijing.volces.com/api/v3/images/generations",
    "model": "doubao-seedream-5-0-260128",
    "size": "2048x2048",  # 最小尺寸
}
```

#### 提示词模板

```python
def build_prompt(scene, brand_elements=True):
    """构建生图提示词"""
    templates = {
        "健身房环境": """
            亚洲风格健身房前台，MUX Logo 墙，
            紫色和橙色品牌灯光，现代简约装修，
            摄影级画质，广角镜头，16:9 构图
        """,
        "身材对比": """
            亚洲人身材前后对比，左边普通身材，右边肌肉线条明显，
            健身房背景，激励氛围，真实可信，
            摄影级画质，16:9 构图
        """,
        "有氧运动": """
            亚洲女性在跑步机上运动，健身房环境，
            专注表情，汗水，运动装备专业，
            暖色调，活力氛围，摄影级画质
        """,
        "力量训练": """
            亚洲男性在力量训练区，哑铃杠铃器械，
            肌肉训练场景，专业健身，力量与美感，
            深色调，戏剧性光影，橙色点缀
        """,
        "健康饮食": """
            健康餐摆盘，鸡胸肉 + 西兰花 + 糙米，
            营养均衡，色彩丰富，俯拍视角，
            清新自然，美食摄影风格
        """,
        "教练指导": """
            亚洲教练指导亚洲学员，一对一教学，
            专业认真，学员专注，健身房环境，
            温暖氛围，摄影级画质
        """,
    }
    
    prompt = templates.get(scene, "")
    
    if brand_elements:
        prompt += " MUX 品牌元素，紫色橙色配色"
    
    return prompt.strip()
```

#### 批量生成

```python
async def generate_images(prompts, output_dir="images"):
    """批量生成配图"""
    os.makedirs(output_dir, exist_ok=True)
    
    tasks = []
    for i, prompt in enumerate(prompts):
        output = f"{output_dir}/{i+1:02d}.jpg"
        task = asyncio.create_task(
            volcano_generate(prompt, output)
        )
        tasks.append(task)
    
    await asyncio.gather(*tasks)
    print(f"✅ 生成{len(prompts)}张图片")
```

---

### Phase 4: 封面设计（20 分钟）

**封面规格**:
- 尺寸：900×383 像素
- 格式：JPG
- 大小：<2MB

**设计模板**:
```python
from PIL import Image, ImageDraw, ImageFont

def design_cover(background_img, title, subtitle, bottom_text):
    # 1. 加载背景
    bg = Image.open(background_img).convert("RGBA")
    bg = bg.resize((900, 383))
    
    # 2. 添加蒙版（加深背景）
    overlay = Image.new('RGBA', bg.size, (0, 0, 0, 128))
    bg = Image.alpha_composite(bg, overlay)
    
    # 3. 添加文字
    draw = ImageDraw.Draw(bg)
    
    # MUX 大字
    font_mux = ImageFont.truetype("Arial Bold.ttf", 120)
    draw.text((450, 120), "MUX", fill='white', 
              font=font_mux, anchor="mm")
    
    # 副标题
    font_sub = ImageFont.truetype("Arial Bold.ttf", 40)
    draw.text((450, 220), subtitle, fill='white',
              font=font_sub, anchor="mm")
    
    # 底部橙色条
    draw.rectangle([(0, 320), (900, 383)], fill='#FF6B00')
    draw.text((450, 352), bottom_text, fill='white',
              font=font_sub, anchor="mm")
    
    # 4. 保存
    bg.convert("RGB").save("cover.jpg", quality=90)
```

---

### Phase 5: HTML 整合（15 分钟）

**HTML 模板**:
```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{{title}}</title>
    <style>
        body { font-family: -apple-system, sans-serif; max-width: 677px; margin: 0 auto; }
        .brand-header { text-align: center; color: #666; font-size: 14px; }
        .brand-info { background: #f5f5f5; padding: 10px; text-align: center; }
        .section { margin: 30px 0; }
        .section img { width: 100%; height: auto; }
        .footer { border-top: 1px solid #eee; padding-top: 20px; color: #999; font-size: 12px; }
    </style>
</head>
<body>
    <div class="brand-header">💪 科学健身 · 专业指导 · 成就更好的自己</div>
    <div class="brand-info">🏋️ 5 家门店 | ⏰ 11:00-23:00 | 👨🏫 专业教练 | 🎯 一对一</div>
    
    <h1>{{title}}</h1>
    
    {{content}}
    
    <div class="footer">
        📍 MUX 米欧克斯健身（5 店通用）<br>
        ⏰ 营业时间：11:00-23:00<br>
        💪 服务：专业健身指导 | 器械训练 | 团课
    </div>
</body>
</html>
```

**图片 Base64 嵌入**:
```python
import base64

def image_to_base64(image_path):
    with open(image_path, 'rb') as f:
        return base64.b64encode(f.read()).decode()

def build_html(title, content, images):
    for i, img_path in enumerate(images):
        base64_img = image_to_base64(img_path)
        content = content.replace(
            f"![配图{i+1}]({img_path})",
            f'<img src="data:image/jpeg;base64,{base64_img}">'
        )
    
    html = HTML_TEMPLATE.replace("{{title}}", title).replace("{{content}}", content)
    return html
```

---

## 📁 文件结构

```
wechat-article-auto-gen/
├── SKILL.md                 # 技能文档
├── config.py                # 配置管理
├── scraper.py               # 文章抓取
├── rewriter.py              # 内容改写
├── storyboard.py            # 分镜拆分
├── prompt_gen.py            # 提示词生成
├── image_gen.py             # AI 生图
├── cover_design.py          # 封面设计
├── html_builder.py          # HTML 整合
└── outputs/                 # 输出目录
    ├── articles/            # 文章 HTML
    ├── images/              # 配图
    └── covers/              # 封面
```

---

## 🔧 核心代码模块

### 1. 文章抓取

```python
import requests
from bs4 import BeautifulSoup

def scrape_article(url):
    """抓取公众号文章"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    title = soup.find("h1").get_text()
    content = soup.find("div", id="js_content").get_text()
    
    return {"title": title, "content": content}
```

---

### 2. AI 改写

```python
def llm_rewrite(raw_content, brand="MUX"):
    """AI 改写文章"""
    prompt = f"""
    将以下文章改写为{brand}品牌版本：
    
    原文：
    {raw_content}
    
    要求：
    1. 品牌名称替换为{brand}
    2. 门店信息替换为{brand}实际门店
    3. 语气口语化、真实可信
    4. 避免绝对化用词（最、第一等）
    5. 添加团购引导（左下角）
    6. 保持原文核心信息
    7. 字数控制在 1500-2000 字
    """
    
    response = call_llm_api(prompt)
    return response.content
```

---

### 3. 分镜拆分

```python
def create_storyboard(content):
    """将文章拆分为分镜"""
    paragraphs = content.split("\n\n")
    storyboard = []
    
    for i, para in enumerate(paragraphs):
        if len(para) > 50:  # 长段落需要配图
            storyboard.append({
                "section": i,
                "text": para,
                "need_image": True,
                "image_prompt": generate_image_prompt(para)
            })
        else:
            storyboard.append({
                "section": i,
                "text": para,
                "need_image": False
            })
    
    return storyboard
```

---

### 4. 合规检查

```python
COMPLIANCE_RULES = [
    ("最", "避免绝对化用词"),
    ("第一", "避免绝对化用词"),
    (" guaranteed", "避免承诺性用词"),
    ("7 天瘦 20 斤", "避免夸大效果"),
]

def compliance_check(content):
    """检查内容合规性"""
    issues = []
    for rule, reason in COMPLIANCE_RULES:
        if rule in content:
            issues.append(f"{reason}: 发现'{rule}'")
    
    if issues:
        print("⚠️ 合规问题:")
        for issue in issues:
            print(f"  - {issue}")
        return False
    
    return True
```

---

## ⚠️ 故障排查

### 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 抓取失败 | URL 无效/反爬 | 检查 URL，添加 User-Agent |
| 改写质量差 | Prompt 不清晰 | 优化 Prompt，添加示例 |
| 生图失败 | API Key 余额不足 | 检查余额，充值 |
| 图片不符 | Prompt 描述不清 | 细化提示词，添加约束 |
| 封面文字错位 | 字体缺失 | 检查字体路径，用系统字体 |
| HTML 过大 | 图片未压缩 | 压缩图片至<300KB/张 |

---

## 📊 输出规格

| 项目 | 标准值 |
|------|--------|
| **文章字数** | 1500-2000 字 |
| **配图数量** | 6-8 张 |
| **图片尺寸** | 2048x2048（最小） |
| **封面尺寸** | 900×383 |
| **HTML 大小** | <5MB |
| **生成时间** | <2 小时 |

---

## 🔄 自我迭代机制

### 每篇文章后

1. **收集反馈**: 用户满意点/不满意点
2. **记录问题**: 生成过程中的问题
3. **优化 Prompt**: 根据效果调整提示词
4. **更新模板**: 改进文章结构

### 每周回顾

1. **爆款分析**: 哪些文章阅读高？为什么？
2. **配图优化**: 哪些图点击高？风格偏好？
3. **标题迭代**: 哪些标题打开率高？
4. **合规更新**: 平台规则变更追踪

### 月度升级

- 新增内容类别
- 优化生图模型（跟进新版本）
- 改进 HTML 模板
- 技能文档版本升级

---

## 📝 品牌模板

### MUX 米欧克斯健身房

**品牌调性**: 专业、激励、亲切

**核心信息**:
- 5 家门店（江苏常熟）
- 营业时间：11:00-23:00
- 服务：健身指导、器械训练、团课

**文案风格**:
- 口语化、真实可信
- 避免过度营销
- 引导合规（团购在左下角）

---

## 📝 变更记录

| 日期 | 版本 | 变更内容 |
|------|------|----------|
| 2026-03-25 | v1.0 | 初始版本，基于 mux-article-factory 沉淀 |

---

*技能文档版本：v1.0 | 最后更新：2026-03-25*
