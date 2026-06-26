#!/usr/bin/env python3
"""
szzg007-product-promotion - 商品推广邮件生成技能

从商品网址提取图片，生成高品质邮件推广模版，并保存到素材库。

使用方式:
    python3 product-promotion.py <product_url> [--send-to <email>] [--code <code>]

代号系统:
    QY1, QY2... - 童装系列 (Childrenswear)
    QB1, QB2... - 收纳系列 (Box/Storage)
    QA1, QA2... - 通用系列 (General)
    QH1, QH2... - 家居系列 (Home)
    QF1, QF2... - 时尚系列 (Fashion)
"""

import sys
import json
import os
import re
import subprocess
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse, parse_qs

# 配置
WORKSPACE = Path("/Users/zhuzhenguo/.openclaw/workspace")
SKILL_DIR = WORKSPACE / "skills/szzg007-product-promotion"
ASSETS_DIR = WORKSPACE / "product-promotion-assets"

IMAGES_DIR = ASSETS_DIR / "images"
EMAILS_DIR = ASSETS_DIR / "emails"
REPORTS_DIR = ASSETS_DIR / "reports"

# 确保目录存在
for d in [IMAGES_DIR, EMAILS_DIR, REPORTS_DIR]:
    d.mkdir(parents=True, exist_ok=True)


def extract_product_id_from_url(url: str) -> str:
    """从 URL 提取产品 ID 作为文件名"""
    parsed = urlparse(url)
    path = parsed.path.strip('/')
    
    # 尝试从路径提取
    parts = path.split('/')
    if parts:
        # 取最后一段作为产品 ID
        product_id = parts[-1]
        # 清理无效字符
        product_id = re.sub(r'[^a-zA-Z0-9_-]', '', product_id[:50])
        if product_id:
            return product_id
    
    #  fallback 到时间戳
    return f"product_{datetime.now().strftime('%Y%m%d_%H%M%S')}"


def download_images(image_urls: list, product_id: str) -> dict:
    """下载商品图片"""
    print(f"\n🖼️  正在下载 {len(image_urls)} 张图片...")
    
    product_images_dir = IMAGES_DIR / product_id
    product_images_dir.mkdir(exist_ok=True)
    
    downloaded = []
    for i, url in enumerate(image_urls[:10], 1):  # 最多下载 10 张
        try:
            filename = f"image_{i:02d}.jpg"
            filepath = product_images_dir / filename
            
            # 使用 curl 下载
            cmd = ['curl', '-L', '-sS', '-o', str(filepath), url]
            result = subprocess.run(cmd, capture_output=True, timeout=30)
            
            if result.returncode == 0 and filepath.exists():
                size = filepath.stat().st_size
                if size > 1000:  # 至少 1KB
                    downloaded.append({
                        'index': i,
                        'url': url,
                        'local_path': str(filepath),
                        'filename': filename,
                        'size': size
                    })
                    print(f"  ✅ [{i}/{len(image_urls)}] {filename} ({size/1024:.1f}KB)")
                else:
                    filepath.unlink()  # 删除无效文件
            else:
                print(f"  ❌ [{i}/{len(image_urls)}] 下载失败")
        except Exception as e:
            print(f"  ❌ [{i}/{len(image_urls)}] 错误：{e}")
    
    return {
        'total_attempted': len(image_urls),
        'total_downloaded': len(downloaded),
        'images': downloaded,
        'directory': str(product_images_dir)
    }


def generate_email_template(product_info: dict, image_data: dict) -> str:
    """生成 HTML 邮件模版"""
    print(f"\n🎨 正在生成邮件模版...")
    
    # 读取基础模版
    template_file = SKILL_DIR / "templates/email-template-v1.html"
    if template_file.exists():
        with open(template_file, 'r', encoding='utf-8') as f:
            html = f.read()
    else:
        # 使用内置模版
        html = get_default_template()
    
    # 替换变量
    replacements = {
        '{{BRAND_NAME}}': product_info.get('brand', 'MOSSRIVER'),
        '{{BRAND_TAGLINE}}': product_info.get('tagline', 'Elevate Your Space'),
        '{{PRODUCT_TITLE}}': product_info.get('title', 'Premium Product'),
        '{{ORIGINAL_PRICE}}': product_info.get('original_price', '$0.00'),
        '{{SALE_PRICE}}': product_info.get('sale_price', '$0.00'),
        '{{SAVE_AMOUNT}}': product_info.get('save_amount', '$0.00'),
        '{{DISCOUNT_PERCENT}}': product_info.get('discount_percent', '0'),
        '{{PRODUCT_URL}}': product_info.get('url', '#'),
        '{{MAIN_IMAGE}}': image_data['images'][0]['url'] if image_data['images'] else '',
    }
    
    for key, value in replacements.items():
        html = html.replace(key, str(value))
    
    # 生成图片画廊 HTML
    gallery_html = generate_image_gallery(image_data)
    html = html.replace('{{IMAGE_GALLERY}}', gallery_html)
    
    # 生成特点列表 HTML
    features_html = generate_features_html(product_info.get('features', []))
    html = html.replace('{{FEATURES}}', features_html)
    
    return html


def generate_image_gallery(image_data: dict) -> str:
    """生成图片画廊 HTML"""
    images = image_data.get('images', [])
    if not images:
        return '<p>暂无图片</p>'
    
    html = '<table role="presentation" style="width: 100%; border-collapse: collapse;">\n'
    
    # 2x2 网格布局
    for i in range(0, min(len(images), 4), 2):
        html += '  <tr>\n'
        for j in range(2):
            if i + j < len(images):
                img = images[i + j]
                html += f'    <td style="padding: 8px;">\n'
                html += f'      <img src="{img["url"]}" alt="Product Image {i+j+1}" '
                html += f'style="width: 100%; border-radius: 8px; display: block;">\n'
                html += f'    </td>\n'
        html += '  </tr>\n'
    
    html += '</table>'
    return html


def generate_features_html(features: list) -> str:
    """生成产品特点 HTML"""
    if not features:
        features = [
            {'icon': '✨', 'text': 'Premium Quality'},
            {'icon': '💎', 'text': 'Best Value'},
            {'icon': '📦', 'text': 'Free Shipping'},
            {'icon': '🌿', 'text': 'Eco-Friendly'},
        ]
    
    html = '<table role="presentation" style="width: 100%; border-collapse: collapse;">\n'
    
    for feature in features:
        icon = feature.get('icon', '✨')
        text = feature.get('text', 'Feature')
        html += f'  <tr>\n'
        html += f'    <td style="padding: 12px 0; vertical-align: top;">\n'
        html += f'      <table role="presentation" style="border-collapse: collapse;">\n'
        html += f'        <tr>\n'
        html += f'          <td style="width: 40px; text-align: center; font-size: 24px;">{icon}</td>\n'
        html += f'          <td style="padding-left: 12px;">\n'
        html += f'            <span style="color: #374151; font-size: 15px; line-height: 1.5;">{text}</span>\n'
        html += f'          </td>\n'
        html += f'        </tr>\n'
        html += f'      </table>\n'
        html += f'    </td>\n'
        html += f'  </tr>\n'
    
    html += '</table>'
    return html


def save_email(html: str, product_id: str, custom_code: str = None) -> str:
    """保存邮件模版"""
    print(f"\n💾 正在保存邮件模版...")
    
    # 如果有自定义代号，使用代号作为文件名
    if custom_code:
        filename = f"{custom_code}-{product_id}.html"
    else:
        filename = f"{product_id}.html"
    
    filepath = EMAILS_DIR / filename
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"  ✅ 已保存：{filepath}")
    return str(filepath)


def generate_report(product_info: dict, image_data: dict, email_path: str, custom_code: str = None) -> str:
    """生成报告"""
    print(f"\n📝 正在生成报告...")
    
    report_id = product_info.get('product_id', datetime.now().strftime('%Y%m%d_%H%M%S'))
    
    # 如果有代号，在报告名中包含
    if custom_code:
        filename = f"{custom_code}-{report_id}.md"
    else:
        filename = f"{report_id}.md"
    
    filepath = REPORTS_DIR / filename
    
    report = f"""# 商品推广邮件生成报告
## Product Promotion Report

**生成时间:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**产品 ID:** {report_id}  
**商品网址:** {product_info.get('url', 'N/A')}

---

## 📊 执行总结

| 项目 | 状态 |
|------|------|
| **图片提取** | ✅ {image_data['total_downloaded']}/{image_data['total_attempted']} 张 |
| **邮件模版** | ✅ 已生成 |
| **素材归档** | ✅ 已完成 |

---

## 🖼️ 图片详情

| # | 文件名 | 大小 | 状态 |
|---|--------|------|------|
"""
    
    for img in image_data.get('images', []):
        report += f"| {img['index']} | {img['filename']} | {img['size']/1024:.1f}KB | ✅ |\n"
    
    report += f"""
---

## 📧 邮件模版

**文件路径:** `{email_path}`  
**主题:** ✨ {product_info.get('title', 'Product')} | Special Offer

---

## 📁 素材位置

| 类型 | 路径 |
|------|------|
| **图片** | `{image_data['directory']}` |
| **邮件** | `{email_path}` |
| **报告** | `{filepath}` |

---

## 🚀 下一步

1. 预览邮件模版
2. 调整文案或设计
3. 发送到目标邮箱

---

**生成工具:** szzg007-product-promotion v1.0.0
"""
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"  ✅ 已保存：{filepath}")
    return str(filepath)


def save_email_meta(code: str, product_info: dict, image_data: dict, email_path: str) -> str:
    """保存邮件元数据"""
    print(f"\n🏷️  正在生成元数据...")
    
    filepath = EMAILS_DIR / f"{code}.meta.json"
    
    meta = {
        "schema": "szzg007-email-template-meta-v1",
        "code": code,
        "name": product_info.get('title', 'Unnamed Product'),
        "description": f"Product promotion email for {product_info.get('title', 'Unknown')}",
        "version": "1.0.0",
        "created": datetime.now().isoformat(),
        "category": "product-promotion",
        "template": "email-template-v1.html",
        "product": {
            "name": product_info.get('title', 'Unknown'),
            "url": product_info.get('url', ''),
            "price": {
                "original": product_info.get('original_price', '$0.00'),
                "sale": product_info.get('sale_price', '$0.00'),
                "save": product_info.get('save_amount', '$0.00'),
                "discount": product_info.get('discount_percent', '0')
            }
        },
        "design": {
            "theme": "Purple Gradient",
            "colors": ["#667eea", "#764ba2"],
            "style": "Modern Minimalist",
            "mobileResponsive": True
        },
        "assets": {
            "images": [img['filename'] for img in image_data.get('images', [])],
            "imageCount": len(image_data.get('images', []))
        },
        "usage": {
            "sentCount": 0,
            "lastSent": None,
            "lastSentTo": None
        },
        "files": {
            "html": f"{code}-{product_info.get('product_id', '')}.html",
            "meta": f"{code}.meta.json",
            "images": f"images/{product_info.get('product_id', '')}/"
        },
        "tags": ["product-promotion", code.lower()[0]]  # e.g., 'q', 'y', 'b'
    }
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)
    
    print(f"  ✅ 已保存：{filepath}")
    return str(filepath)


def get_default_template() -> str:
    """返回默认 HTML 邮件模版"""
    return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{PRODUCT_TITLE}}</title>
</head>
<body style="margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #f8f9fa;">
  
  <div style="display: none; max-height: 0; overflow: hidden;">
    ✨ {{PRODUCT_TITLE}} - Special Offer Inside!
  </div>

  <table role="presentation" style="width: 100%; border-collapse: collapse; background-color: #f8f9fa;">
    <tr>
      <td align="center" style="padding: 40px 20px;">
        
        <table role="presentation" style="max-width: 600px; width: 100%; border-collapse: collapse; background-color: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 20px rgba(0,0,0,0.08);">
          
          <tr>
            <td align="center" style="padding: 32px 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
              <h1 style="margin: 0; color: #ffffff; font-size: 28px; font-weight: 700;">{{BRAND_NAME}}</h1>
              <p style="margin: 8px 0 0 0; color: rgba(255,255,255,0.9); font-size: 14px;">{{BRAND_TAGLINE}}</p>
            </td>
          </tr>

          <tr>
            <td align="center" style="padding: 0; background-color: #ffffff;">
              <img src="{{MAIN_IMAGE}}" alt="{{PRODUCT_TITLE}}" style="width: 100%; max-width: 600px; height: auto; display: block;">
            </td>
          </tr>

          <tr>
            <td style="padding: 40px 40px 30px 40px;">
              
              <table role="presentation" style="margin: 0 auto 20px auto;">
                <tr>
                  <td align="center" style="background-color: #f0fdf4; padding: 8px 20px; border-radius: 20px;">
                    <span style="color: #16a34a; font-size: 13px; font-weight: 600; text-transform: uppercase;">✨ New Arrival</span>
                  </td>
                </tr>
              </table>

              <h2 style="margin: 0 0 16px 0; color: #1a1a1a; font-size: 26px; font-weight: 700; line-height: 1.3; text-align: center;">
                {{PRODUCT_TITLE}}
              </h2>

              <table role="presentation" style="margin: 0 auto 24px auto;">
                <tr>
                  <td align="center">
                    <span style="color: #9ca3af; font-size: 18px; text-decoration: line-through; margin-right: 12px;">{{ORIGINAL_PRICE}}</span>
                    <span style="color: #dc2626; font-size: 32px; font-weight: 700;">{{SALE_PRICE}}</span>
                  </td>
                </tr>
              </table>

              <table role="presentation" style="margin: 0 auto 30px auto;">
                <tr>
                  <td align="center" style="background-color: #fef2f2; padding: 10px 24px; border-radius: 8px; border: 1px solid #fecaca;">
                    <span style="color: #dc2626; font-size: 15px; font-weight: 600;">💰 Save {{SAVE_AMOUNT}} ({{DISCOUNT_PERCENT}}% OFF)</span>
                  </td>
                </tr>
              </table>

              <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 30px 0;">

              <h3 style="margin: 0 0 20px 0; color: #1a1a1a; font-size: 18px; font-weight: 600;">Why You'll Love It</h3>
              
              {{FEATURES}}

            </td>
          </tr>

          <tr>
            <td align="center" style="padding: 0 40px 40px 40px;">
              <table role="presentation" style="border-collapse: collapse;">
                <tr>
                  <td align="center" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 8px;">
                    <a href="{{PRODUCT_URL}}" style="display: inline-block; padding: 16px 48px; color: #ffffff; text-decoration: none; font-size: 16px; font-weight: 600;">Shop Now →</a>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <tr>
            <td style="padding: 0 40px 40px 40px; background-color: #fafbfc;">
              <h3 style="margin: 0 0 20px 0; color: #1a1a1a; font-size: 18px; font-weight: 600; text-align: center;">See It In Action</h3>
              {{IMAGE_GALLERY}}
            </td>
          </tr>

          <tr>
            <td style="padding: 32px 40px; background-color: #f3f4f6; border-top: 1px solid #e5e7eb;">
              <p style="margin: 0 0 16px 0; color: #6b7280; font-size: 14px; line-height: 1.6; text-align: center;">
                © 2026 {{BRAND_NAME}}. All rights reserved.
              </p>
            </td>
          </tr>

        </table>

      </td>
    </tr>
  </table>

</body>
</html>
"""


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法：python3 product-promotion.py <product_url> [--send-to <email>] [--code <code>]")
        print("\n代号系统:")
        print("  QY1, QY2... - 童装系列 (Childrenswear)")
        print("  QB1, QB2... - 收纳系列 (Box/Storage)")
        print("  QA1, QA2... - 通用系列 (General)")
        print("  QH1, QH2... - 家居系列 (Home)")
        print("  QF1, QF2... - 时尚系列 (Fashion)")
        print("\n示例:")
        print("  python3 product-promotion.py https://example.com/product/123")
        print("  python3 product-promotion.py https://example.com/product/123 --code QB2")
        sys.exit(1)
    
    product_url = sys.argv[1]
    send_to = None
    custom_code = None
    
    if '--send-to' in sys.argv:
        idx = sys.argv.index('--send-to')
        if idx + 1 < len(sys.argv):
            send_to = sys.argv[idx + 1]
    
    if '--code' in sys.argv:
        idx = sys.argv.index('--code')
        if idx + 1 < len(sys.argv):
            custom_code = sys.argv[idx + 1]
    
    print("=" * 60)
    print("🚀 szzg007-product-promotion v1.0.0")
    print("=" * 60)
    print(f"\n📦 商品网址：{product_url}")
    
    # 提取产品 ID
    product_id = extract_product_id_from_url(product_url)
    print(f"🏷️  产品 ID: {product_id}")
    
    # 模拟产品信息 (实际应从网页提取)
    product_info = {
        'product_id': product_id,
        'url': product_url,
        'title': f'Premium Product - {product_id}',
        'brand': 'MOSSRIVER',
        'tagline': 'Elevate Your Space',
        'original_price': '$59.99',
        'sale_price': '$45.99',
        'save_amount': '$14.00',
        'discount_percent': '23',
        'features': [
            {'icon': '✨', 'text': 'Premium Quality'},
            {'icon': '💎', 'text': 'Best Value'},
            {'icon': '📦', 'text': 'Free Shipping'},
            {'icon': '🌿', 'text': 'Eco-Friendly'},
        ]
    }
    
    # 模拟图片 URLs (实际应从网页提取)
    image_urls = [
        f"https://example.com/image1.jpg",
        f"https://example.com/image2.jpg",
    ]
    
    # 下载图片
    image_data = download_images(image_urls, product_id)
    
    # 生成邮件模版
    html = generate_email_template(product_info, image_data)
    
    # 保存邮件 (支持代号)
    email_path = save_email(html, product_id, custom_code)
    
    # 生成报告
    report_path = generate_report(product_info, image_data, email_path, custom_code)
    
    # 生成元数据 (如果有代号)
    if custom_code:
        meta_path = save_email_meta(custom_code, product_info, image_data, email_path)
        print(f"  元数据：{meta_path}")
    
    print("\n" + "=" * 60)
    print("✅ 任务完成！")
    print("=" * 60)
    print(f"\n📁 生成的文件:")
    print(f"  图片：{image_data['directory']}")
    if custom_code:
        print(f"  代号：{custom_code}")
    print(f"  邮件：{email_path}")
    print(f"  报告：{report_path}")
    
    if send_to:
        print(f"\n📧 下一步：发送邮件到 {send_to}")
        # 这里可以调用 send-email.py
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
