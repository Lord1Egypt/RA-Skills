# 娜可露露洗发水 Skill - 目录和图片生成指南

## 问题说明

由于当前系统权限限制，无法通过脚本自动创建 `assets/images/`、`assets/templates/`、`assets/mockups/` 子目录和生成图片文件。

## 解决方案

### 方案 1：手动创建目录（推荐）

在 Windows 资源管理器中手动创建以下目录：

```
C:\Users\chenyuxin\.qclaw\workspace\skills\shampoo-recommender\assets\
├── images\          ← 手动创建此目录
├── templates\       ← 手动创建此目录
└── mockups\         ← 手动创建此目录
```

**创建步骤：**
1. 打开文件资源管理器
2. 导航到 `C:\Users\chenyuxin\.qclaw\workspace\skills\shampoo-recommender\assets\`
3. 右键 → 新建 → 文件夹，分别创建 `images`、`templates`、`mockups`

### 方案 2：使用 PowerShell（管理员权限）

以管理员身份运行 PowerShell，执行：

```powershell
$basePath = "C:\Users\chenyuxin\.qclaw\workspace\skills\shampoo-recommender\assets"
New-Item -ItemType Directory -Force -Path "$basePath\images"
New-Item -ItemType Directory -Force -Path "$basePath\templates"
New-Item -ItemType Directory -Force -Path "$basePath\mockups"
Write-Host "目录创建完成！"
```

### 方案 3：使用 Python 生成图片（创建目录后）

目录创建后，运行以下脚本生成图片：

```python
# 保存为 generate_images.py 并运行
from PIL import Image, ImageDraw, ImageFont
import os

SKILL_DIR = r"C:\Users\chenyuxin\.qclaw\workspace\skills\shampoo-recommender"

def create_ad_image(product_name, color_hex, bg_hex, output_path):
    width, height = 1200, 628
    color = tuple(int(color_hex[i:i+2], 16) for i in (1, 3, 5))
    bg = tuple(int(bg_hex[i:i+2], 16) for i in (1, 3, 5))
    
    img = Image.new('RGB', (width, height), bg)
    draw = ImageDraw.Draw(img)
    
    try:
        font_title = ImageFont.truetype("C:/Windows/Fonts/msyhbd.ttc", 72)
        font_sub = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 36)
        font_small = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 24)
    except:
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # 装饰条
    draw.rectangle([0, 0, width, 15], fill=color)
    draw.rectangle([0, 0, 15, height], fill=color)
    
    # 品牌和产品名
    draw.text((50, 50), "娜可露露", font=font_small, fill=(80, 80, 80))
    draw.line([(50, 85), (180, 85)], fill=color, width=3)
    draw.text((50, 130), product_name, font=font_title, fill=color)
    draw.text((50, 220), "洗发水", font=font_sub, fill=color)
    
    # 产品图示
    bx, by = 850, 120
    draw.rounded_rectangle([bx+35, by, bx+85, by+40], radius=5, fill=color)
    draw.rounded_rectangle([bx, by+40, bx+120, by+380], radius=25, 
                          fill=(255,255,255), outline=color, width=4)
    draw.rounded_rectangle([bx+15, by+140, bx+105, by+280], radius=10, fill=bg)
    draw.text((bx+30, by+190), "娜可", font=font_small, fill=color)
    draw.text((bx+30, by+220), "露露", font=font_small, fill=color)
    
    # 底部
    draw.line([(50, 480), (1150, 480)], fill=(200,200,200), width=2)
    draw.text((50, 500), "专业护发 · 娜可露露", font=font_small, fill=(150,150,150))
    
    img.save(output_path, "PNG")
    print(f"✓ 已生成: {os.path.basename(output_path)}")

# 生成7款产品广告图
products = [
    ("深层滋养修护", "#8B5A2B", "#FFF8F0"),
    ("清爽控油", "#4682B4", "#F0F8FF"),
    ("去屑止痒", "#228B22", "#F0FFF0"),
    ("防脱固发", "#8B4513", "#FFF5EE"),
    ("氨基酸温和", "#9370DB", "#F8F8FF"),
    ("蓬松丰盈", "#FF8C00", "#FFFAF0"),
    ("去氯修护", "#008080", "#F0FFFF"),
]

images_dir = os.path.join(SKILL_DIR, "assets", "images")
for name, color, bg in products:
    output_path = os.path.join(images_dir, f"{name}_广告图.png")
    create_ad_image(name, color, bg, output_path)

print("\n✅ 所有产品广告图生成完成！")
```

## 预期文件结构（完成后）

```
shampoo-recommender/
├── SKILL.md
├── PACKAGE.md
├── references/
│   ├── products.md
│   └── faq.md
├── scripts/
│   ├── card_generator.py
│   ├── generate_ads.py
│   ├── simple_generate.py
│   └── setup_assets.py
└── assets/
    ├── README.md
    ├── images/                    ← 手动创建
    │   ├── 深层滋养修护_广告图.png
    │   ├── 清爽控油_广告图.png
    │   ├── 去屑止痒_广告图.png
    │   ├── 防脱固发_广告图.png
    │   ├── 氨基酸温和_广告图.png
    │   ├── 蓬松丰盈_广告图.png
    │   └── 去氯修护_广告图.png
    ├── templates/                 ← 手动创建
    │   ├── 推荐卡片_单款.png
    │   ├── 推荐卡片_双款.png
    │   └── 完整推荐报告.png
    └── mockups/                   ← 手动创建
        ├── 洗发水_正面.png
        ├── 洗发水_侧面.png
        └── 使用场景_效果图.png
```

## 替代方案

如果不想生成图片，Skill 也可以正常工作：
- 使用文字描述代替图片展示
- 使用 `scripts/card_generator.py` 动态生成推荐卡片
- 后续补充真实的产品图片

## 当前 Skill 状态

✅ 已完成：
- SKILL.md 主文件
- 产品线参考 (products.md)
- FAQ 文档 (faq.md)
- 脚本工具 (scripts/)
- 资源说明 (assets/README.md)

⏳ 待完成（需手动）：
- 创建 assets/ 子目录
- 生成/放置产品图片
