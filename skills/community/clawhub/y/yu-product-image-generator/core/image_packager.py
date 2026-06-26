#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
打包下载模块
将生成的图片打包成 ZIP 文件
"""

import os
import zipfile
import shutil
from datetime import datetime
from typing import List, Optional


class ImagePackager:
    """图片打包器"""
    
    def __init__(self, output_dir: str = None):
        if output_dir is None:
            output_dir = os.path.join(os.path.dirname(__file__), 'output')
        
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def create_zip(
        self,
        image_paths: List[str],
        product_name: str = "产品",
        customer_name: str = None
    ) -> str:
        """
        创建 ZIP 压缩包
        
        Args:
            image_paths: 图片路径列表
            product_name: 产品名称
            customer_name: 客户名称（可选）
        
        Returns:
            ZIP 文件路径
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # 生成文件名
        if customer_name:
            zip_filename = f"商品图_{customer_name}_{product_name}_{timestamp}.zip"
        else:
            zip_filename = f"商品图_{product_name}_{timestamp}.zip"
        
        zip_path = os.path.join(self.output_dir, zip_filename)
        
        # 创建 ZIP
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for img_path in image_paths:
                if os.path.exists(img_path):
                    # 只保留文件名，不包含路径
                    arcname = os.path.basename(img_path)
                    zipf.write(img_path, arcname)
        
        # 打印信息
        zip_size = os.path.getsize(zip_path) / 1024
        print(f"📦 ZIP 打包完成：{zip_filename}")
        print(f"   文件数：{len(image_paths)}")
        print(f"   大小：{zip_size:.1f} KB")
        print(f"   路径：{zip_path}")
        
        return zip_path
    
    def create_preview_html(
        self,
        image_paths: List[str],
        product_name: str = "产品"
    ) -> str:
        """
        创建预览 HTML
        
        Args:
            image_paths: 图片路径列表
            product_name: 产品名称
        
        Returns:
            HTML 文件路径
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        html_filename = f"预览_{product_name}_{timestamp}.html"
        html_path = os.path.join(self.output_dir, html_filename)
        
        # 生成 HTML
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{product_name} - 商品图预览</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        h1 {{
            text-align: center;
            color: #333;
        }}
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }}
        .card {{
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        .card img {{
            width: 100%;
            height: 300px;
            object-fit: cover;
        }}
        .card-info {{
            padding: 15px;
            text-align: center;
            color: #666;
        }}
    </style>
</head>
<body>
    <h1>{product_name} - 商品图预览</h1>
    <div class="grid">
"""
        
        for idx, img_path in enumerate(image_paths, start=1):
            # 使用相对路径或 file:// 协议
            img_rel_path = os.path.relpath(img_path, self.output_dir)
            html_content += f"""
        <div class="card">
            <img src="{img_rel_path}" alt="图{idx}">
            <div class="card-info">图{idx}</div>
        </div>
"""
        
        html_content += """
    </div>
</body>
</html>
"""
        
        # 保存 HTML
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"📄 预览 HTML 已生成：{html_filename}")
        
        return html_path
    
    def cleanup_temp_files(self, days_old: int = 7):
        """清理临时文件"""
        import time
        
        now = time.time()
        cutoff = now - (days_old * 86400)
        
        for filename in os.listdir(self.output_dir):
            filepath = os.path.join(self.output_dir, filename)
            if os.path.getmtime(filepath) < cutoff:
                try:
                    if os.path.isfile(filepath):
                        os.remove(filepath)
                        print(f"🗑️  已删除旧文件：{filename}")
                except Exception as e:
                    print(f"删除文件失败 {filename}: {e}")


# 便捷函数
def package_images(
    image_paths: List[str],
    product_name: str = "产品",
    customer_name: str = None,
    create_preview: bool = True
) -> dict:
    """便捷函数：打包图片"""
    packager = ImagePackager()
    
    result = {
        'zip_path': packager.create_zip(image_paths, product_name, customer_name)
    }
    
    if create_preview:
        result['preview_path'] = packager.create_preview_html(image_paths, product_name)
    
    return result


if __name__ == '__main__':
    # 测试
    print("📦 图片打包器 - 测试")
    print("=" * 50)
    
    # 模拟测试
    test_images = [
        '/tmp/generated_image_1.jpg',
        '/tmp/generated_image_2.jpg',
        '/tmp/generated_image_3.jpg'
    ]
    
    result = package_images(test_images, "测试产品", "测试客户")
    
    print(f"\n打包结果：")
    print(f"  ZIP: {result['zip_path']}")
    if 'preview_path' in result:
        print(f"  预览：{result['preview_path']}")
