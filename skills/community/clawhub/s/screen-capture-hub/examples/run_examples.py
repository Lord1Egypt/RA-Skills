#!/usr/bin/env python3
"""
OPENCLAW(龙虾)-屏幕查看器 使用示例
运行此脚本演示所有功能
"""

import os
import sys
import subprocess
from pathlib import Path

def print_header():
    """打印标题"""
    print("=" * 70)
    print("OPENCLAW(龙虾)-屏幕查看器 - 功能演示")
    print("=" * 70)
    print("此脚本将演示屏幕查看器的各种功能")
    print("请确保已安装所有依赖")
    print("=" * 70)

def check_dependencies():
    """检查依赖"""
    print("\n1. 检查系统依赖...")
    
    # 检查Python版本
    version = sys.version_info
    print(f"   Python版本: {sys.version.split()[0]}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("   [失败] 需要Python 3.8或更高版本")
        return False
    else:
        print("   [成功] Python版本符合要求")
    
    # 检查脚本目录
    script_dir = Path(__file__).parent.parent / "scripts"
    if not script_dir.exists():
        print(f"   [失败] 脚本目录不存在: {script_dir}")
        return False
    
    print("   [成功] 脚本目录检查通过")
    return True

def run_basic_screenshot():
    """运行基本截图示例"""
    print("\n2. 基本截图演示...")
    
    try:
        # 使用快速截图工具
        cmd = ["python", "scripts/quick_capture.py", "-o", "example_basic.png"]
        print(f"   执行命令: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        
        if result.returncode == 0:
            print("   基本截图测试完成")
            if Path("example_basic.png").exists():
                file_size = Path("example_basic.png").stat().st_size
                print(f"   截图文件已保存: example_basic.png ({file_size/1024:.1f}KB)")
                return True
            else:
                print("   警告: 截图文件未生成")
                return False
        else:
            print(f"   错误: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"   异常: {e}")
        return False

def run_screen_info():
    """运行屏幕信息获取"""
    print("\n3. 屏幕信息获取演示...")
    
    try:
        cmd = ["python", "scripts/screenshot.py", "--list-displays"]
        print(f"   执行命令: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        
        if result.returncode == 0:
            print("   屏幕信息获取完成")
            lines = result.stdout.strip().split('\n')
            for line in lines:
                if line.strip():
                    print(f"   {line.strip()}")
            return True
        else:
            print(f"   错误: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"   异常: {e}")
        return False

def run_region_capture():
    """运行区域截图演示"""
    print("\n4. 区域截图演示...")
    
    try:
        cmd = [
            "python", "scripts/screenshot.py",
            "--region", "100,100,500,400",
            "--output", "example_region.png"
        ]
        print(f"   执行命令: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        
        if result.returncode == 0:
            print("   区域截图测试完成")
            if Path("example_region.png").exists():
                file_size = Path("example_region.png").stat().st_size
                print(f"   区域截图已保存: example_region.png ({file_size/1024:.1f}KB)")
                return True
            else:
                print("   警告: 区域截图文件未生成")
                return False
        else:
            print(f"   错误: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"   异常: {e}")
        return False

def run_ocr_test():
    """运行OCR测试"""
    print("\n5. OCR文字识别演示...")
    
    try:
        cmd = ["python", "scripts/test_ocr.py"]
        print(f"   执行命令: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        
        if result.returncode == 0:
            print("   OCR功能测试完成")
            return True
        else:
            print("   OCR功能测试失败")
            print(f"   错误信息: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"   异常: {e}")
        return False

def run_analysis_test():
    """运行分析功能测试"""
    print("\n6. 屏幕分析演示...")
    
    try:
        cmd = ["python", "scripts/analyze_screen.py", "--task", "screen_info"]
        print(f"   执行命令: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        
        if result.returncode == 0:
            print("   屏幕分析测试完成")
            return True
        else:
            print("   屏幕分析测试失败")
            if result.stdout:
                print(f"   输出: {result.stdout[:200]}...")
            return False
            
    except Exception as e:
        print(f"   异常: {e}")
        return False

def cleanup_example_files():
    """清理示例文件"""
    print("\n7. 清理示例文件...")
    
    files_to_clean = [
        "example_basic.png",
        "example_region.png",
        "ocr_test_image.png"
    ]
    
    cleaned = 0
    for file_name in files_to_clean:
        if Path(file_name).exists():
            Path(file_name).unlink()
            cleaned += 1
    
    if cleaned > 0:
        print(f"   已清理 {cleaned} 个示例文件")
    else:
        print("   没有需要清理的文件")

def main():
    """主函数"""
    print_header()
    
    # 检查依赖
    if not check_dependencies():
        print("\n[失败] 系统依赖检查失败")
        print("请先安装必要的依赖:")
        print("  1. Python 3.8或更高版本")
        print("  2. 运行依赖检查: python scripts/dependency_check.py")
        sys.exit(1)
    
    results = {
        'basic': run_basic_screenshot(),
        'info': run_screen_info(),
        'region': run_region_capture(),
        'ocr': run_ocr_test(),
        'analysis': run_analysis_test()
    }
    
    # 显示结果
    print("\n" + "=" * 70)
    print("功能演示结果:")
    print("=" * 70)
    
    test_names = {
        'basic': '基本截图',
        'info': '屏幕信息',
        'region': '区域截图',
        'ocr': 'OCR识别',
        'analysis': '屏幕分析'
    }
    
    all_passed = True
    for test_key, passed in results.items():
        status = "[成功]" if passed else "[失败]"
        print(f"  {test_names[test_key]:10} {status}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 70)
    
    if all_passed:
        print("[成功] 所有功能测试通过!")
        print("您的OPENCLAW(龙虾)-屏幕查看器已成功安装并配置完成")
        
        print("\n下一步操作建议:")
        print("  1. 查看详细文档: cat README.md")
        print("  2. 测试更多功能: python scripts/test_screenshot.py")
        print("  3. 查看使用示例: examples/目录")
        print("  4. 获取帮助: python scripts/screenshot.py --help")
        
        # 清理示例文件
        cleanup_example_files()
        
        return True
    else:
        print("[警告] 部分功能测试失败")
        
        print("\n问题解决建议:")
        print("  1. 检查依赖: python scripts/dependency_check.py")
        print("  2. 安装缺少的依赖:")
        print("     pip install pillow pyautogui")
        print("  3. 安装OCR功能:")
        print("     pip install pytesseract")
        print("     并从 https://github.com/UB-Mannheim/tesseract/wiki 下载Tesseract")
        print("  4. 查看详细错误日志")
        
        return False

if __name__ == "__main__":
    try:
        success = main()
        if success:
            sys.exit(0)
        else:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n[信息] 用户中断演示")
        sys.exit(1)