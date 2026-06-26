#!/usr/bin/env python3
"""YouTube搜索结果视频链接提取器 - 无守护进程模式测试脚本"""

import subprocess
import sys
import os
import time

def test_without_daemon():
    """测试无守护进程模式"""
    print("🔍 测试无守护进程模式...")
    
    test_keyword = "python tutorial"
    test_output = "test_python"
    
    try:
        # 关闭可能存在的浏览器实例
        subprocess.run(['agent-browser', 'close'], capture_output=True, text=True)
        
        # 使用独立会话测试
        result = subprocess.run(
            ['agent-browser', '--session', 'test-session', 'open', 
             f"https://www.youtube.com/results?search_query={test_keyword}"],
            capture_output=True, text=True, timeout=30
        )
        
        if result.returncode == 0:
            print("✅ 搜索页面已加载")
            
            # 等待页面加载
            time.sleep(3)
            
            # 获取页面内容
            result = subprocess.run(
                ['agent-browser', '--session', 'test-session', 'get', 'html', 'body'],
                capture_output=True, text=True, timeout=30
            )
            
            if result.returncode == 0 and len(result.stdout) > 10000:
                print("✅ 页面内容获取成功")
                
                # 保存页面内容
                with open(f"{test_output}.html", 'w', encoding='utf-8') as f:
                    f.write(result.stdout)
                
                print(f"✅ 页面内容已保存到: {test_output}.html")
                
                # 测试链接提取
                from youtube_search_extractor import YouTubeSearchExtractor
                extractor = YouTubeSearchExtractor()
                
                with open(f"{test_output}.html", 'r', encoding='utf-8') as f:
                    html_content = f.read()
                
                links = extractor.extract_video_links(html_content)
                
                if len(links) > 0:
                    print(f"✅ 成功提取 {len(links)} 个视频链接")
                    
                    # 保存链接列表
                    with open(f"{test_output}_links.txt", 'w', encoding='utf-8') as f:
                        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                        f.write(f"# YouTube搜索结果：'{test_keyword}' ({timestamp})\n")
                        f.write(f"# 找到 {len(links)} 个相关视频\n\n")
                        
                        for i, link in enumerate(links[:3], 1):
                            f.write(f"{i}. {link}\n")
                    
                    print(f"✅ 链接列表已保存到: {test_output}_links.txt")
                    return True
                
                else:
                    print("❌ 未找到视频链接")
                    return False
                    
            else:
                print(f"❌ 无法获取页面内容: {result.returncode}")
                if result.stderr:
                    print(f"错误信息: {result.stderr}")
                return False
                
        else:
            print(f"❌ 无法访问搜索页面: {result.returncode}")
            if result.stderr:
                print(f"错误信息: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ 操作超时")
        return False
    except Exception as e:
        print(f"❌ 测试时出错: {e}")
        import traceback
        print(traceback.format_exc())
        return False
        
    finally:
        # 清理资源
        try:
            subprocess.run(['agent-browser', '--session', 'test-session', 'close'], 
                         capture_output=True, text=True, timeout=10)
        except:
            pass

def cleanup_test_files():
    """清理测试文件"""
    test_files = ['test_python.html', 'test_python_links.txt']
    for file_name in test_files:
        try:
            if os.path.exists(file_name):
                os.remove(file_name)
        except:
            pass

def main():
    """主函数"""
    print("=== YouTube Search Extractor 无守护进程模式测试 ===")
    
    if not os.path.exists('youtube_search_extractor.py'):
        print("❌ 请在正确的目录下运行")
        return False
    
    print("⏳ 测试可能需要几秒钟，请耐心等待...")
    
    success = test_without_daemon()
    
    if success:
        print("\n✅ 测试成功！无守护进程模式功能正常")
        
        # 显示提取的链接预览
        if os.path.exists('test_python_links.txt'):
            print("\n📄 提取的链接列表预览:")
            with open('test_python_links.txt', 'r', encoding='utf-8') as f:
                print(f.read())
                
        cleanup_test_files()
        return True
    else:
        print("\n❌ 测试失败")
        cleanup_test_files()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
