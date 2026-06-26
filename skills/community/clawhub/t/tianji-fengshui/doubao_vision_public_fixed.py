#!/usr/bin/env python3
"""
豆包视觉模型分析器（公共API KEY版）
直接从配置文件中读取公共API KEY
"""

import os
import sys
import json
import base64
import requests
from pathlib import Path
from PIL import Image
import time

class DoubaoVisionPublicAnalyzer:
    """豆包视觉模型分析器（公共API KEY版）"""
    
    def __init__(self, config_path=None):
        """初始化分析器，从配置文件读取公共API KEY"""
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), "public_api_config_simple.json")
        
        self.config = self.load_config(config_path)
        self.api_config = self.config["model_routing"]["image_analysis"]
        self.image_config = self.config.get("image_processing", {})
        
        # 检查API KEY
        self.api_key = self.api_config.get("api_key")
        if not self.api_key or self.api_key == "PUBLIC_API_KEY_HERE":
            print("⚠️  警告: 请先在配置文件中配置公共API KEY")
            print("💡 提示: 将PUBLIC_API_KEY_HERE替换为你的公共API KEY")
            self.api_key = None
        
    def load_config(self, config_path):
        """加载配置文件"""
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # 默认配置
        return {
            "model_routing": {
                "image_analysis": {
                    "model": "doubao-seed-2-0-pro-260215",
                    "provider": "volcengine",
                    "api_key": "PUBLIC_API_KEY_HERE",
                    "base_url": "https://ark.cn-beijing.volces.com/api/v3",
                    "capabilities": ["vision", "text"]
                }
            },
            "image_processing": {
                "optimize_size": True,
                "max_width": 768,
                "max_height": 768,
                "quality": 85,
                "convert_png_to_jpg": True
            }
        }
    
    def optimize_image(self, image_path):
        """优化图片尺寸和质量"""
        try:
            with Image.open(image_path) as img:
                # 获取原始信息
                original_size = img.size
                original_mode = img.mode
                original_format = img.format
                
                # 检查是否需要优化
                max_width = self.image_config.get("max_width", 768)
                max_height = self.image_config.get("max_height", 768)
                
                if img.width <= max_width and img.height <= max_height:
                    print(f"✅ 图片尺寸合适: {img.width}x{img.height} (无需优化)")
                    return image_path
                
                # 计算新尺寸
                width_ratio = max_width / img.width
                height_ratio = max_height / img.height
                ratio = min(width_ratio, height_ratio)
                
                new_width = int(img.width * ratio)
                new_height = int(img.height * ratio)
                
                # 调整尺寸
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # 保存优化后的图片
                temp_dir = "/tmp/tianji_fengshui_public"
                os.makedirs(temp_dir, exist_ok=True)
                
                optimized_path = os.path.join(temp_dir, f"optimized_{int(time.time())}.jpg")
                
                # 转换格式如果需要
                if img.mode != 'RGB' and self.image_config.get("convert_png_to_jpg", True):
                    img = img.convert('RGB')
                
                quality = self.image_config.get("quality", 85)
                img.save(optimized_path, 'JPEG', quality=quality, optimize=True)
                
                print(f"🔄 图片优化完成: ({new_width}, {new_height}) (原始: {original_size[0]}x{original_size[1]})")
                return optimized_path
                
        except Exception as e:
            print(f"❌ 图片优化失败: {e}")
            return image_path
    
    def encode_image(self, image_path):
        """将图片编码为Base64"""
        try:
            with open(image_path, "rb") as image_file:
                image_data = image_file.read()
                base64_image = base64.b64encode(image_data).decode('utf-8')
            
            print(f"📊 图片数据: {len(image_data)} 字节, Base64: {len(base64_image)} 字符")
            return base64_image
            
        except Exception as e:
            print(f"❌ 图片编码失败: {e}")
            return None
    
    def analyze_image(self, image_path, analysis_type="general"):
        """分析图片"""
        if not self.api_key:
            return {"success": False, "error": "未配置API KEY"}
        
        if not os.path.exists(image_path):
            return {"success": False, "error": f"图片文件不存在: {image_path}"}
        
        print(f"🧭 玄机子·豆包视觉分析（公共API版）")
        print("=" * 50)
        print(f"🔒 API密钥来源: 配置文件")
        print(f"✅ API密钥已配置")
        print(f"🖼️  分析图片: {os.path.basename(image_path)}")
        print(f"📋 分析类型: {analysis_type}")
        
        try:
            # 1. 优化图片
            print("🔄 优化图片...")
            optimized_path = self.optimize_image(image_path)
            
            # 2. 编码图片
            print("🔄 编码图片...")
            base64_image = self.encode_image(optimized_path)
            if not base64_image:
                return {"success": False, "error": "图片编码失败"}
            
            # 3. 准备API请求
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            # 根据分析类型准备提示词
            if analysis_type == "palm":
                prompt = "请详细分析这张掌纹图片，包括生命线、智慧线、感情线等主要掌纹特征，以及手掌形状、手指长度比例等。请用专业但易懂的语言描述。"
            elif analysis_type == "face":
                prompt = "请详细分析这张面相图片，包括额头、眉毛、眼睛、鼻子、嘴巴、下巴等面部特征。请用专业但易懂的语言描述面相特点。"
            elif analysis_type == "fengshui":
                prompt = "请分析这张风水布局图片，包括方位、门窗位置、家具摆放、空间布局等。请用专业但易懂的语言描述风水特点。"
            else:
                prompt = "请详细描述这张图片的内容，包括人物、场景、物体、颜色、构图等所有可见元素。"
            
            payload = {
                "model": self.api_config["model"],
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                "max_tokens": self.config.get("doubao_settings", {}).get("max_tokens", 3000),
                "temperature": self.config.get("doubao_settings", {}).get("temperature", 0.7)
            }
            
            # 4. 调用API
            print("🚀 调用豆包视觉模型API...")
            start_time = time.time()
            
            response = requests.post(
                self.api_config["base_url"] + "/chat/completions",
                headers=headers,
                json=payload,
                timeout=self.config.get("doubao_settings", {}).get("timeout_seconds", 120)
            )
            
            response_time = time.time() - start_time
            
            print(f"✅ API响应时间: {response_time:.2f}秒")
            print(f"📡 状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                analysis = result["choices"][0]["message"]["content"]
                
                return {
                    "success": True,
                    "analysis": analysis,
                    "usage": result.get("usage", {}),
                    "response_time": response_time,
                    "image_size": len(base64_image),
                    "optimized_path": optimized_path,
                    "api_source": "public_config"
                }
            else:
                error_msg = f"API调用失败: {response.status_code} - {response.text}"
                print(f"❌ {error_msg}")
                return {"success": False, "error": error_msg}
                
        except requests.exceptions.Timeout:
            error_msg = "API请求超时"
            print(f"❌ {error_msg}")
            return {"success": False, "error": error_msg}
        except Exception as e:
            error_msg = f"分析过程中出错: {str(e)}"
            print(f"❌ {error_msg}")
            return {"success": False, "error": error_msg}

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("使用方法: python3 doubao_vision_public_fixed.py <图片路径> [分析类型]")
        print("分析类型: general(默认), palm, face, fengshui")
        sys.exit(1)
    
    image_path = sys.argv[1]
    analysis_type = sys.argv[2] if len(sys.argv) > 2 else "general"
    
    analyzer = DoubaoVisionPublicAnalyzer()
    result = analyzer.analyze_image(image_path, analysis_type)
    
    print("\n" + "=" * 50)
    print("分析结果:")
    print("=" * 50)
    
    if result["success"]:
        print(result["analysis"])
    else:
        print(f"❌ 分析失败: {result.get('error', '未知错误')}")

if __name__ == "__main__":
    main()