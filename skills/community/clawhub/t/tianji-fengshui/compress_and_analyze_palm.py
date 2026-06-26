#!/usr/bin/env python3
"""
玄机子·掌纹图片压缩与分析脚本（增强集成版）
专门用于压缩掌纹图片（保持原貌），然后进行天机分析
支持命令行参数和交互式输入
"""

import sys
import os
import json
import base64
import time
import argparse
from PIL import Image
import requests

def get_openclaw_config_path():
    """获取OpenClaw配置路径，支持多种环境"""
    # 方法1: 环境变量
    env_path = os.getenv('OPENCLAW_CONFIG_PATH')
    if env_path:
        return env_path
    
    # 方法2: 用户主目录
    home_path = os.path.expanduser('~/.openclaw/openclaw.json')
    if os.path.exists(home_path):
        return home_path
    
    # 方法3: 默认路径（仅用于开发）
    return '/tmp/openclaw_test_config.json'

def compress_image_keep_original(image_path, max_dimension=1024, quality=85):
    """
    压缩图片但保持原貌
    保持原始比例，只减小尺寸和文件大小
    """
    print(f"📸 压缩图片: {os.path.basename(image_path)}")
    print(f"   原则: 保持原貌，只减小尺寸")
    
    try:
        with Image.open(image_path) as img:
            original_width, original_height = img.size
            original_format = img.format
            original_mode = img.mode
            
            print(f"   原始尺寸: {original_width}x{original_height}")
            print(f"   原始格式: {original_format}")
            print(f"   原始模式: {original_mode}")
            
            # 计算压缩后的尺寸（保持比例）
            if max(original_width, original_height) > max_dimension:
                ratio = max_dimension / max(original_width, original_height)
                new_width = int(original_width * ratio)
                new_height = int(original_height * ratio)
            else:
                new_width = original_width
                new_height = original_height
            
            print(f"   压缩后尺寸: {new_width}x{new_height}")
            print(f"   比例保持: {original_width/original_height:.3f}:1 → {new_width/new_height:.3f}:1")
            
            # 高质量重采样
            img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # 生成临时文件路径
            temp_dir = "/tmp/tianji_fengshui"
            os.makedirs(temp_dir, exist_ok=True)
            
            base_name = os.path.splitext(os.path.basename(image_path))[0]
            compressed_path = os.path.join(temp_dir, f"{base_name}_compressed_keep_original.jpg")
            
            # 保存压缩图片（保持原貌）
            if img.mode != 'RGB':
                img_resized = img_resized.convert('RGB')
            
            img_resized.save(compressed_path, 'JPEG', quality=quality, optimize=True, progressive=True)
            
            # 验证压缩结果
            with Image.open(compressed_path) as compressed_img:
                comp_width, comp_height = compressed_img.size
                if comp_width != new_width or comp_height != new_height:
                    print(f"⚠️  警告: 压缩后尺寸不匹配: {comp_width}x{comp_height} (期望: {new_width}x{new_height})")
                    return None
            
            print(f"✅ 压缩成功: {compressed_path}")
            print(f"   文件大小: {os.path.getsize(compressed_path):,}字节")
            
            return compressed_path
            
    except Exception as e:
        print(f"❌ 压缩失败: {e}")
        return None

def analyze_palm_with_tianji(image_path, gender="male", hand="left"):
    """
    使用天机分析掌纹图片
    """
    print(f"\n🧠 开始天机分析: {gender}性{hand}手")
    
    try:
        # 读取OpenClaw配置
        config_path = get_openclaw_config_path()
        print(f"📋 读取配置: {config_path}")
        
        if not os.path.exists(config_path):
            print(f"❌ 配置文件不存在: {config_path}")
            return {"success": False, "error": "配置文件不存在"}
        
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        # 获取API密钥
        doubao_api_key = None
        deepseek_api_key = None
        
        # 从环境变量获取
        doubao_api_key = os.getenv('DOUBAO_API_KEY')
        deepseek_api_key = os.getenv('DEEPSEEK_API_KEY')
        
        # 从配置获取
        if not doubao_api_key and 'volcengine' in config.get('models', {}):
            doubao_api_key = config['models']['volcengine'].get('apiKey')
        
        if not deepseek_api_key and 'deepseek' in config.get('models', {}):
            deepseek_api_key = config['models']['deepseek'].get('apiKey')
        
        if not doubao_api_key:
            print("❌ 未找到豆包API密钥")
            return {"success": False, "error": "未找到豆包API密钥"}
        
        # 读取并编码图片
        with open(image_path, 'rb') as f:
            image_data = f.read()
        
        image_base64 = base64.b64encode(image_data).decode('utf-8')
        
        # 构建请求
        url = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {doubao_api_key}",
            "Content-Type": "application/json"
        }
        
        # 构建提示词
        prompt = f"""你是一位精通中国传统掌相学、风水命理的大师玄机子。请分析这张{gender}性{hand}手的掌纹图片。

请提供详细专业的掌纹分析报告，包括：

1. **掌型分析**：手掌形状、手指比例、手掌厚薄
2. **主要掌纹**：生命线、智慧线、感情线、命运线的特征
3. **特殊纹路**：是否有特殊符号、岛纹、分叉、中断等
4. **五行分析**：根据掌纹特征分析五行属性
5. **运势解读**：健康、事业、财运、感情等方面的运势
6. **建议指导**：基于掌纹特征给出具体建议

请以专业、详细、具体的方式进行分析，避免笼统描述。"""

        payload = {
            "model": "doubao-seed-2-0-pro-260215",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 4000
        }
        
        print("📡 调用豆包视觉模型进行分析...")
        start_time = time.time()
        
        response = requests.post(url, headers=headers, json=payload, timeout=120)
        response_time = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            analysis = result['choices'][0]['message']['content']
            
            return {
                "success": True,
                "analysis": analysis,
                "response_time": response_time
            }
        else:
            print(f"❌ API调用失败: {response.status_code}")
            print(f"响应: {response.text[:200]}")
            return {
                "success": False,
                "error": f"API调用失败: {response.status_code}",
                "response": response.text[:500]
            }
            
    except Exception as e:
        print(f"❌ 分析过程中出错: {e}")
        return {"success": False, "error": str(e)}

def save_analysis_report(analysis_result, original_image, compressed_image, gender, hand):
    """保存分析报告"""
    try:
        report_dir = "/tmp/tianji_fengshui_reports"
        os.makedirs(report_dir, exist_ok=True)
        
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        report_file = os.path.join(report_dir, f"palm_analysis_{gender}_{hand}_{timestamp}.txt")
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("=" * 70 + "\n")
            f.write(f"🧭 玄机子·天机掌纹分析报告\n")
            f.write(f"📅 分析时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"👤 性别: {gender}性 | 手: {hand}手\n")
            f.write("=" * 70 + "\n\n")
            
            f.write("📸 图片信息:\n")
            f.write(f"   原始图片: {original_image}\n")
            f.write(f"   压缩图片: {compressed_image}\n")
            
            with Image.open(original_image) as img:
                f.write(f"   原始尺寸: {img.size[0]}x{img.size[1]}像素\n")
            
            with Image.open(compressed_image) as img:
                f.write(f"   压缩尺寸: {img.size[0]}x{img.size[1]}像素\n")
            
            f.write("\n" + "=" * 70 + "\n")
            f.write("📊 分析结果:\n")
            f.write("=" * 70 + "\n\n")
            
            if analysis_result["success"]:
                f.write(analysis_result["analysis"])
                f.write(f"\n\n⏱️  响应时间: {analysis_result.get('response_time', 0):.2f}秒\n")
            else:
                f.write(f"分析失败: {analysis_result.get('error', '未知错误')}\n")
        
        return report_file
        
    except Exception as e:
        print(f"❌ 保存报告失败: {e}")
        return None

def analyze_palm(image_path, gender="male", hand="left", max_dimension=1024, quality=85):
    """
    主分析函数：压缩图片并进行天机分析
    """
    print("=" * 70)
    print("🧭 玄机子·掌纹压缩与分析系统（增强集成版）")
    print("=" * 70)
    
    if not os.path.exists(image_path):
        print(f"❌ 图片不存在: {image_path}")
        return False
    
    print(f"📸 原始图片: {os.path.basename(image_path)}")
    print(f"👤 分析参数: {gender}性{hand}手")
    
    # 1. 压缩图片（保持原貌）
    print("\n" + "=" * 70)
    print("🔄 开始压缩图片（保持原貌原则）")
    print("-" * 40)
    
    compressed_image = compress_image_keep_original(image_path, max_dimension, quality)
    
    if not compressed_image:
        print("❌ 图片压缩失败，无法继续分析")
        return False
    
    # 2. 使用天机分析
    print("\n" + "=" * 70)
    analysis_result = analyze_palm_with_tianji(compressed_image, gender, hand)
    
    print("\n" + "=" * 70)
    print("分析结果:")
    print("=" * 70)
    
    if analysis_result and analysis_result["success"]:
        print("✅ 天机分析成功！")
        print(f"⏱️  响应时间: {analysis_result.get('response_time', 0):.2f}秒")
        
        print("\n" + "=" * 70)
        print(f"🧭 玄机子·天机掌纹分析报告（{gender}性{hand}手·完整原貌）")
        print("=" * 70)
        
        # 显示分析报告
        analysis = analysis_result["analysis"]
        print(analysis)
        
        print("\n" + "=" * 70)
        
        # 保存报告
        report_file = save_analysis_report(analysis_result, image_path, compressed_image, gender, hand)
        print(f"\n💾 完整报告已保存到: {report_file}")
        print("💡 报告包含：专业压缩 + 完整原貌分析 + 传统掌相学 + 五行八卦 + 综合运势")
        
        # 显示压缩效果
        print("\n📊 压缩效果对比（保持原貌）:")
        with Image.open(image_path) as orig_img:
            orig_size = orig_img.size
        with Image.open(compressed_image) as comp_img:
            comp_size = comp_img.size
        
        print(f"   原始: {orig_size[0]}x{orig_size[1]}像素, {os.path.getsize(image_path):,}字节")
        print(f"   压缩后: {comp_size[0]}x{comp_size[1]}像素, {os.path.getsize(compressed_image):,}字节")
        print(f"   尺寸保持: {orig_size[0]/orig_size[1]:.3f}:1 → {comp_size[0]/comp_size[1]:.3f}:1")
        print(f"   原貌保持: ✅ 比例不变，内容完整，细节保留")
        
        return True
        
    else:
        print("❌ 天机分析失败")
        if analysis_result:
            print(f"错误: {analysis_result.get('error', '未知错误')}")
        
        print("\n💡 备选方案：基于压缩图片的初步分析")
        print("-" * 40)
        print(f"根据压缩处理：")
        print(f"1. {gender}性{hand}手掌纹（完整原貌）")
        print(f"2. 专业压缩保持比例和内容")
        print(f"3. 优化文件大小便于API传输")
        print()
        print(f"玄机子原则：")
        print(f"- 保持图片原貌，不剪裁不扭曲")
        print(f"- 优化传输效率，不损失分析质量")
        print(f"- 基于完整掌纹进行专业分析")
        print(f"- 提供具体可操作建议")
        print()
        print(f"如需更详细分析，请确保：")
        print(f"1. 图片清晰度足够")
        print(f"2. 手掌完全展开")
        print(f"3. 光线均匀，无阴影反光")
        
        return False

def main():
    """主函数：解析命令行参数并执行分析"""
    parser = argparse.ArgumentParser(description='玄机子·掌纹图片压缩与分析系统')
    parser.add_argument('image', help='掌纹图片路径')
    parser.add_argument('--gender', '-g', choices=['male', 'female'], default='male', 
                       help='性别: male(男性) 或 female(女性)，默认 male')
    parser.add_argument('--hand', '-H', choices=['left', 'right'], default='left',
                       help='手: left(左手) 或 right(右手)，默认 left')
    parser.add_argument('--max-dimension', '-d', type=int, default=1024,
                       help='最大边长（像素），默认 1024')
    parser.add_argument('--quality', '-q', type=int, default=85,
                       help='JPEG质量（1-100），默认 85')
    
    args = parser.parse_args()
    
    # 执行分析
    success = analyze_palm(
        image_path=args.image,
        gender=args.gender,
        hand=args.hand,
        max_dimension=args.max_dimension,
        quality=args.quality
    )
    
    if success:
        print("\n🎉 分析完成！")
        sys.exit(0)
    else:
        print("\n❌ 分析失败")
        sys.exit(1)

if __name__ == "__main__":
    main()