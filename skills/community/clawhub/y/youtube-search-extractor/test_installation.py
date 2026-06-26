#!/usr/bin/env python3
"""YouTube搜索结果视频链接提取器 - 安装验证脚本"""

import subprocess
import sys
import os

def check_agent_browser_installed():
    """检查agent-browser是否已安装"""
    print("🔍 检查agent-browser安装...")
    
    try:
        result = subprocess.run(['agent-browser', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"✅ agent-browser已安装，版本: {version}")
            return True
        else:
            print(f"❌ agent-browser未安装，返回码: {result.returncode}")
            return False
            
    except FileNotFoundError:
        print("❌ agent-browser未找到，请先安装")
        return False
    except Exception as e:
        print(f"❌ 检查agent-browser安装时出错: {e}")
        return False

def test_basic_functionality():
    """测试基本功能"""
    print("\n🔍 测试基本功能...")
    
    test_keyword = "python tutorial"
    test_output = "test_python"
    
    try:
        # 运行简单搜索
        result = subprocess.run(
            ['python3', 'youtube_search_extractor.py', test_keyword, test_output, '--wait-time', '3', '--max-links', '3'],
            capture_output=True, text=True, timeout=60
        )
        
        if result.returncode == 0:
            print("✅ 测试搜索成功")
            
            # 检查输出文件
            if os.path.exists(f"{test_output}.html") and os.path.getsize(f"{test_output}.html") > 0:
                print(f"✅ HTML文件已生成: {test_output}.html")
            else:
                print(f"⚠️  HTML文件未生成或为空: {test_output}.html")
            
            if os.path.exists(f"{test_output}_links.txt") and os.path.getsize(f"{test_output}_links.txt") > 0:
                print(f"✅ 链接文件已生成: {test_output}_links.txt")
                
                # 检查链接格式
                with open(f"{test_output}_links.txt", 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                link_count = content.count("https://www.youtube.com/watch?v=")
                if link_count >= 3:
                    print(f"✅ 找到 {link_count} 个视频链接")
                else:
                    print(f"⚠️  只找到 {link_count} 个视频链接")
                    
            return True
            
        else:
            print(f"❌ 测试搜索失败，返回码: {result.returncode}")
            if result.stdout:
                print("标准输出:")
                print(result.stdout)
            if result.stderr:
                print("错误输出:")
                print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ 测试超时")
        return False
    except Exception as e:
        print(f"❌ 测试时出错: {e}")
        import traceback
        print(traceback.format_exc())
        return False

def cleanup_test_files():
    """清理测试文件"""
    test_files = ['test_python.html', 'test_python_links.txt']
    for file_name in test_files:
        try:
            if os.path.exists(file_name):
                os.remove(file_name)
                print(f"✅ 已删除测试文件: {file_name}")
        except Exception as e:
            print(f"❌ 删除文件时出错: {e}")

def main():
    """主函数"""
    print("=== YouTube Search Extractor 安装验证 ===")
    
    # 检查当前目录
    if not os.path.exists('youtube_search_extractor.py'):
        print("❌ 请在youtube-search-extractor目录下运行此脚本")
        return False
    
    # 检查依赖
    dependencies_ok = True
    
    if not check_agent_browser_installed():
        dependencies_ok = False
    
    if not dependencies_ok:
        print("\n❌ 依赖检查失败，请先安装所需依赖")
        print("\n安装命令:")
        print("npm install -g agent-browser")
        print("agent-browser install")
        return False
    
    # 测试功能
    print("\n=== 开始功能测试 ===")
    test_ok = test_basic_functionality()
    
    # 清理
    cleanup_test_files()
    
    if test_ok:
        print("\n🎉 安装成功！YouTube Search Extractor 已准备好使用")
        return True
    else:
        print("\n❌ 安装失败，请检查上述错误信息")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
