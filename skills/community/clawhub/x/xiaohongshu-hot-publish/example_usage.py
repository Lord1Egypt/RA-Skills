#!/usr/bin/env python3
"""
小红书热点发布系统使用示例
展示如何使用XiaohongshuHotPublishGenerator生成发布页面

版本: 1.1.0
"""

import os
import sys
import webbrowser
from datetime import datetime
from create_hot_publish_page import XiaohongshuHotPublishGenerator

def print_header(title: str):
    """打印标题"""
    print("\n" + "=" * 60)
    print(f" {title}")
    print("=" * 60)

def example_basic_usage():
    """示例1：基本用法"""
    print_header("示例1：基本用法 - Python学习内容")
    
    # 创建生成器
    generator = XiaohongshuHotPublishGenerator(
        theme="Python学习",
        brand_name="蒲公英AI编程"
    )
    
    # 生成3个内容
    print("正在生成内容...")
    contents = generator.generate_contents(3)
    
    # 生成HTML页面
    output_file = "example_python_learning.html"
    generator.generate_html_page(output_file)
    
    print(f"✅ 页面已生成: {output_file}")
    print(f"📊 生成内容数量: {len(contents)}")
    
    # 显示内容摘要
    print("\n📋 内容摘要:")
    for i, content in enumerate(contents, 1):
        print(f"  {i}. {content['title']}")
        print(f"     类型: {content['content_type']}")
        print(f"     状态: {content['time_suggestion']['display']}")
    
    return output_file

def example_custom_brand():
    """示例2：自定义品牌"""
    print_header("示例2：自定义品牌 - AI工具推荐")
    
    generator = XiaohongshuHotPublishGenerator(
        theme="AI编程工具",
        brand_name="技术达人小张"
    )
    
    # 生成4个内容
    contents = generator.generate_contents(4)
    
    # 生成HTML页面
    output_file = "example_ai_tools.html"
    generator.generate_html_page(output_file)
    
    print(f"✅ 页面已生成: {output_file}")
    print(f"🎨 品牌名称: {generator.brand_name}")
    print(f"📊 生成内容数量: {len(contents)}")
    
    return output_file

def example_different_themes():
    """示例3：不同主题测试"""
    print_header("示例3：不同主题测试")
    
    themes = [
        ("数据分析", "数据分析师小李"),
        ("健身计划", "健身达人小王"),
        ("旅行攻略", "旅行家小陈"),
        ("效率工具", "效率专家小赵")
    ]
    
    generated_files = []
    
    for theme, brand in themes:
        print(f"\n🎯 主题: {theme}")
        print(f"🏷️  品牌: {brand}")
        
        generator = XiaohongshuHotPublishGenerator(theme=theme, brand_name=brand)
        contents = generator.generate_contents(2)
        
        # 生成文件名
        safe_theme = theme.replace(' ', '_')
        output_file = f"example_{safe_theme}.html"
        generator.generate_html_page(output_file)
        
        generated_files.append(output_file)
        print(f"✅ 已生成: {output_file}")
        print(f"  内容类型: {contents[0]['content_type']}, {contents[1]['content_type']}")
    
    return generated_files

def example_interactive():
    """示例4：交互式生成"""
    print_header("示例4：交互式生成")
    
    print("🎯 自定义内容生成")
    print("-" * 40)
    
    # 获取用户输入
    theme = input("请输入内容主题（如：Python学习、健身计划等）: ").strip()
    if not theme:
        theme = "Python学习"
        print(f"使用默认主题: {theme}")
    
    brand = input("请输入品牌名称（回车使用默认）: ").strip()
    if not brand:
        brand = "内容创作者"
        print(f"使用默认品牌: {brand}")
    
    try:
        num = int(input("请输入生成内容数量（1-5）: ").strip())
        if num < 1 or num > 5:
            num = 3
            print(f"使用默认数量: {num}")
    except:
        num = 3
        print(f"使用默认数量: {num}")
    
    # 生成内容
    print(f"\n🚀 正在生成内容...")
    generator = XiaohongshuHotPublishGenerator(theme=theme, brand_name=brand)
    contents = generator.generate_contents(num)
    
    # 生成HTML页面
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    safe_theme = theme.replace(' ', '_').replace('/', '_')[:20]
    output_file = f"xiaohongshu_{safe_theme}_{timestamp}.html"
    
    generator.generate_html_page(output_file)
    
    print(f"\n✅ 生成完成!")
    print(f"   文件: {output_file}")
    print(f"   主题: {theme}")
    print(f"   品牌: {brand}")
    print(f"   内容数量: {len(contents)}")
    
    # 显示生成的内容
    print(f"\n📋 生成的内容:")
    for i, content in enumerate(contents, 1):
        print(f"  {i}. {content['title']}")
    
    return output_file

def example_batch_generation():
    """示例5：批量生成"""
    print_header("示例5：批量生成多个主题")
    
    # 批量生成配置
    batch_config = [
        {"theme": "Python入门", "brand": "编程新手指南", "num": 3},
        {"theme": "数据分析", "brand": "数据科学社区", "num": 4},
        {"theme": "前端开发", "brand": "前端工程师", "num": 3},
        {"theme": "机器学习", "brand": "AI学习社", "num": 4}
    ]
    
    generated_files = []
    
    for config in batch_config:
        print(f"\n🎯 生成: {config['theme']}")
        
        generator = XiaohongshuHotPublishGenerator(
            theme=config['theme'],
            brand_name=config['brand']
        )
        
        contents = generator.generate_contents(config['num'])
        
        # 生成文件名
        safe_theme = config['theme'].replace(' ', '_')
        timestamp = datetime.now().strftime('%H%M%S')
        output_file = f"batch_{safe_theme}_{timestamp}.html"
        
        generator.generate_html_page(output_file)
        generated_files.append(output_file)
        
        print(f"✅ 已生成: {output_file}")
        print(f"  内容数量: {len(contents)}")
        print(f"  内容类型: {', '.join(set([c['content_type'] for c in contents]))}")
    
    print(f"\n📊 批量生成完成!")
    print(f"   总共生成: {len(generated_files)} 个文件")
    
    return generated_files

def open_in_browser(file_path: str):
    """在浏览器中打开文件"""
    try:
        abs_path = os.path.abspath(file_path)
        url = f"file://{abs_path}"
        webbrowser.open(url)
        print(f"🌐 已在浏览器中打开: {file_path}")
    except Exception as e:
        print(f"⚠️  打开浏览器失败: {e}")

def show_usage_guide():
    """显示使用指南"""
    print_header("使用指南")
    
    guide = """
📖 使用方法:

1. 命令行使用:
   python create_hot_publish_page.py "主题" --brand "品牌" --num 3

2. Python代码中使用:
   from create_hot_publish_page import XiaohongshuHotPublishGenerator
   
   generator = XiaohongshuHotPublishGenerator("主题", "品牌")
   generator.generate_contents(3)
   generator.generate_html_page("output.html")

3. 作为OpenClaw技能:
   - 将文件夹复制到 ~/.openclaw/skills/
   - 当用户提到"小红书发布"等关键词时自动激活

🎯 功能特点:
   - 智能内容生成
   - 一键复制到剪贴板
   - 时间管理和状态跟踪
   - 响应式设计，支持移动端
   - 键盘快捷键支持

🔧 自定义选项:
   - 修改 template.html 中的样式
   - 在 create_hot_publish_page.py 中扩展内容类型
   - 调整时间建议算法
   - 添加新的标签规则
    """
    
    print(guide)

def main():
    """主函数"""
    print("小红书热点半自动化发布系统 - 使用示例")
    print("=" * 60)
    
    while True:
        print("\n请选择示例:")
        print("1. 基本用法 (Python学习)")
        print("2. 自定义品牌 (AI工具推荐)")
        print("3. 不同主题测试")
        print("4. 交互式生成")
        print("5. 批量生成")
        print("6. 查看使用指南")
        print("7. 退出")
        print()
        
        try:
            choice = input("请输入选择 (1-7): ").strip()
            
            if choice == '1':
                file = example_basic_usage()
                if input("\n是否在浏览器中打开? (y/n): ").lower() == 'y':
                    open_in_browser(file)
                    
            elif choice == '2':
                file = example_custom_brand()
                if input("\n是否在浏览器中打开? (y/n): ").lower() == 'y':
                    open_in_browser(file)
                    
            elif choice == '3':
                files = example_different_themes()
                if files and input("\n是否打开第一个文件? (y/n): ").lower() == 'y':
                    open_in_browser(files[0])
                    
            elif choice == '4':
                file = example_interactive()
                if input("\n是否在浏览器中打开? (y/n): ").lower() == 'y':
                    open_in_browser(file)
                    
            elif choice == '5':
                files = example_batch_generation()
                if files and input("\n是否打开第一个文件? (y/n): ").lower() == 'y':
                    open_in_browser(files[0])
                    
            elif choice == '6':
                show_usage_guide()
                
            elif choice == '7':
                print("\n感谢使用，再见！")
                break
                
            else:
                print("无效选择，请重新输入")
            
            input("\n按回车键继续...")
            
        except KeyboardInterrupt:
            print("\n\n👋 用户中断，程序退出")
            break
        except Exception as e:
            print(f"\n❌ 出现错误: {e}")
            import traceback
            traceback.print_exc()
            input("\n按回车键继续...")

if __name__ == '__main__':
    main()