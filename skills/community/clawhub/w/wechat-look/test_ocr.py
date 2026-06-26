#!/usr/bin/env python3
"""
OCR功能测试脚本
"""

import json
import subprocess
import sys
from pathlib import Path

def test_ocr_functionality():
    """测试OCR功能"""
    print("🔍 开始OCR功能测试...")
    
    # OCR脚本路径
    ocr_script = Path(__file__).parent / "ocr_node" / "ocr.js"
    
    if not ocr_script.exists():
        print("❌ OCR脚本不存在:", ocr_script)
        return False
    
    # 测试用的示例图片URL（包含文字的简单图片）
    test_images = [
        "https://via.placeholder.com/800x600/000000/FFFFFF?text=Hello+World+Test+OCR",
        "https://via.placeholder.com/1024x768/000000/FFFFFF?text=OpenClaw+WeChat+Reader+OCR+Test",
        "https://via.placeholder.com/640x480/000000/FFFFFF?text=Chinese+测试+文字识别+功能"
    ]
    
    all_passed = True
    
    for i, image_url in enumerate(test_images, 1):
        print(f"\n📝 测试 {i}/{len(test_images)}: {image_url}")
        
        try:
            # 执行OCR
            result = subprocess.run(
                ["node", str(ocr_script), image_url],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                print(f"❌ OCR执行失败: {result.stderr}")
                all_passed = False
                continue
            
            # 解析结果
            try:
                ocr_result = json.loads(result.stdout)
                
                if "error" in ocr_result:
                    print(f"❌ OCR识别错误: {ocr_result['error']}")
                    all_passed = False
                else:
                    print(f"✅ OCR成功 - 字数: {ocr_result.get('wordCount', 0)}, 置信度: {ocr_result.get('confidence', 0)}%, 耗时: {ocr_result.get('processingTime', 0)}ms")
                    print(f"   识别文本: {ocr_result.get('text', '')[:100]}...")
                    
                    if ocr_result.get('wordCount', 0) > 0:
                        print("✅ 文字识别成功")
                    else:
                        print("⚠️  未识别到文字")
                        
            except json.JSONDecodeError as e:
                print(f"❌ JSON解析失败: {e}")
                print(f"   原始输出: {result.stdout}")
                all_passed = False
                
        except subprocess.TimeoutExpired:
            print("❌ OCR执行超时")
            all_passed = False
        except Exception as e:
            print(f"❌ 执行异常: {e}")
            all_passed = False
    
    print(f"\n🎯 测试总结: {'全部通过 ✅' if all_passed else '存在失败 ❌'}")
    return all_passed

def test_dependencies():
    """测试依赖是否安装"""
    print("\n🔧 检查依赖...")
    
    # 检查Node.js版本
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        node_version = result.stdout.strip()
        print(f"✅ Node.js版本: {node_version}")
        
        # 检查版本是否>=18
        version_num = int(node_version.replace('v', '').split('.')[0])
        if version_num < 18:
            print(f"❌ Node.js版本过低，需要>=18，当前: {node_version}")
            return False
            
    except Exception as e:
        print(f"❌ Node.js检查失败: {e}")
        return False
    
    # 检查npm包是否安装
    package_json = Path(__file__).parent / "ocr_node" / "package.json"
    node_modules = Path(__file__).parent / "ocr_node" / "node_modules"
    
    if not package_json.exists():
        print("❌ package.json不存在")
        return False
    
    if not node_modules.exists():
        print("❌ node_modules不存在，请先运行: cd ocr_node && npm install")
        return False
    
    print("✅ 依赖检查通过")
    return True

if __name__ == "__main__":
    print("🚀 OCR功能完整测试")
    print("=" * 50)
    
    # 检查依赖
    if not test_dependencies():
        print("❌ 依赖检查失败，请先解决上述问题")
        sys.exit(1)
    
    # 测试OCR功能
    if test_ocr_functionality():
        print("\n🎉 所有测试通过！OCR功能正常")
        sys.exit(0)
    else:
        print("\n❌ 测试失败，请检查错误信息")
        sys.exit(1)