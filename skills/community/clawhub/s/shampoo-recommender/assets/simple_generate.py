#!/usr/bin/env python3
"""
快速生成洗发水广告图示例
"""

# 产品列表
products = [
    {"name": "深层滋养修护", "color": "#8B5A2B", "bg": "#FFF8F0"},
    {"name": "清爽控油", "color": "#4682B4", "bg": "#F0F8FF"},
    {"name": "去屑止痒", "color": "#228B22", "bg": "#F0FFF0"},
    {"name": "防脱固发", "color": "#8B4513", "bg": "#FFF5EE"},
    {"name": "氨基酸温和", "color": "#9370DB", "bg": "#F8F8FF"},
    {"name": "蓬松丰盈", "color": "#FF8C00", "bg": "#FFFAF0"},
    {"name": "去氯修护", "color": "#008080", "bg": "#F0FFFF"},
]

# 输出 HTML 预览
html_output = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>娜可露露洗发水广告图预览</title>
    <style>
        body { font-family: sans-serif; margin: 20px; }
        .product-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            max-width: 1400px;
        }
        .product-card {
            border: 1px solid #ddd;
            border-radius: 12px;
            padding: 20px;
            background-color: white;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        .product-title {
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .product-color {
            height: 120px;
            border-radius: 8px;
            margin-bottom: 10px;
        }
        .product-info {
            font-size: 14px;
            color: #666;
        }
        .placeholder {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            height: 200px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            margin-bottom: 15px;
        }
        .placeholder-text {
            background-color: rgba(0,0,0,0.5);
            padding: 10px 20px;
            border-radius: 4px;
        }
        .footer {
            margin-top: 40px;
            text-align: center;
            color: #888;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <h1>娜可露露洗发水广告图预览</h1>
    <p>以下为7款产品的广告图样式设计（需要填充真实图片）</p>
    
    <div class="product-grid">
"""

for i, product in enumerate(products):
    html_output += f"""
        <div class="product-card">
            <div class="placeholder">
                <div class="placeholder-text">{product['name']}</div>
            </div>
            <div class="product-title">{product['name']}</div>
            <div class="product-color" style="background-color: {product['color']};"></div>
            <div class="product-info">
                设计颜色: {product['color']}<br>
                背景色: {product['bg']}<br>
                建议尺寸: 1200 × 628 px
            </div>
        </div>
"""

html_output += """
    </div>
    
    <div class="footer">
        <h3>📁 assets/images/目录文件建议</h3>
        <ul>
            <li>深层滋养修护_广告图.png</li>
            <li>清爽控油_广告图.png</li>
            <li>去屑止痒_广告图.png</li>
            <li>防脱固发_广告图.png</li>
            <li>氨基酸温和_广告图.png</li>
            <li>蓬松丰盈_广告图.png</li>
            <li>去氯修护_广告图.png</li>
        </ul>
        <p>文件命名需与产品名称一致，格式为PNG或JPG</p>
        <p>生成时间：2026-03-21</p>
    </div>
</body>
</html>
"""

print("已生成HTML预览代码。广告图需要用户自行填充真实图片，本预览展示了样式设计建议。")
print("\n产品列表:")
for product in products:
    print(f"  {product['name']}: 主色 {product['color']}, 背景 {product['bg']}")
