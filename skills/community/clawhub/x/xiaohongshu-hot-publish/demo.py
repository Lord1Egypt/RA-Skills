#!/usr/bin/env python3
"""
小红书热点发布系统演示
生成一个完整的发布页面并展示所有功能

版本: 1.1.0
"""

import os
import sys
import webbrowser
from datetime import datetime
from create_hot_publish_page import XiaohongshuHotPublishGenerator

def print_section(title: str, char: str = "="):
    """打印章节标题"""
    print(f"\n{char * 60}")
    print(f" {title}")
    print(f"{char * 60}")

def create_demo_page():
    """创建演示页面"""
    print_section("小红书热点半自动化发布系统演示", "🎯")
    
    # 获取当前时间用于文件名
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # 创建生成器
    print("1. 🛠️ 创建内容生成器...")
    generator = XiaohongshuHotPublishGenerator(
        theme="AI编程工具2026",
        brand_name="蒲公英AI编程"
    )
    
    print(f"   主题: {generator.theme}")
    print(f"   品牌: {generator.brand_name}")
    
    # 生成内容
    print("\n2. 📝 生成小红书风格内容...")
    contents = generator.generate_contents(4)
    
    # 显示生成的内容
    print_section("生成内容预览", "📋")
    
    for i, content in enumerate(contents, 1):
        print(f"\n{i}. {content['title']}")
        print(f"   📍 类型: {content['content_type']}")
        print(f"   🎯 Emoji: {content['emoji']}")
        print(f"   ⏰ 时间: {content['time_suggestion']['display']}")
        print(f"   🏷️  标签: {', '.join(['#' + tag for tag in content['tags'][:3]])}...")
        print(f"   📊 字数: {content['word_count']}")
    
    # 生成HTML页面
    print("\n3. 🎨 生成HTML发布页面...")
    output_file = f"demo_xiaohongshu_{timestamp}.html"
    html_content = generator.generate_html_page(output_file)
    
    # 获取文件信息
    file_size = os.path.getsize(output_file)
    abs_path = os.path.abspath(output_file)
    
    print_section("生成结果", "✅")
    print(f"📄 文件: {output_file}")
    print(f"📦 大小: {file_size:,} 字节")
    print(f"📁 路径: {abs_path}")
    print(f"📊 内容数量: {len(contents)}")
    
    return output_file, generator

def show_feature_highlights():
    """展示功能亮点"""
    print_section("功能亮点", "✨")
    
    features = [
        ("🎨 美观界面", "现代化渐变设计，响应式布局"),
        ("🤖 智能生成", "基于主题自动生成小红书风格内容"),
        ("⚡ 高效发布", "一键复制，智能时间管理"),
        ("📱 多端适配", "完美支持桌面和移动端"),
        ("🔧 高度可定制", "支持品牌、主题、样式自定义"),
        ("⌨️ 键盘快捷键", "Ctrl+C复制、数字键切换内容"),
        ("💾 本地存储", "保存发布状态，刷新不丢失"),
        ("🔄 实时更新", "自动更新时间显示"),
        ("🎯 内容分类", "支持多种内容类型和主题"),
        ("🏷️ 智能标签", "自动生成相关话题标签")
    ]
    
    for emoji, description in features:
        print(f"  {emoji} {description}")

def show_usage_instructions():
    """显示使用说明"""
    print_section("使用说明", "📖")
    
    instructions = [
        "1. 打开生成的HTML文件",
        "2. 点击内容标签切换不同内容",
        "3. 点击『📋 一键复制』按钮复制内容",
        "4. 点击『🌐 打开小红书』在新标签页打开平台",
        "5. 发布后点击『✅ 标记为已发布』更新状态",
        "6. 使用键盘快捷键提高效率:",
        "   • Ctrl+C: 复制当前内容",
        "   • 数字键1-4: 切换到对应内容",
        "   • 空格键: 打开小红书"
    ]
    
    for instruction in instructions:
        print(f"  {instruction}")

def show_technical_details(generator):
    """显示技术细节"""
    print_section("技术细节", "🔧")
    
    details = [
        ("Python版本", f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"),
        ("内容类型", f"{len(set([c['content_type'] for c in generator.contents]))} 种"),
        ("标签数量", f"平均 {sum(len(c['tags']) for c in generator.contents) // len(generator.contents)} 个/内容"),
        ("内容字数", f"平均 {sum(c['word_count'] for c in generator.contents) // len(generator.contents)} 字/内容"),
        ("时间建议", "智能时间分配算法"),
        ("错误处理", "多重复制方法确保稳定性")
    ]
    
    for label, value in details:
        print(f"  {label}: {value}")

def open_in_browser(file_path: str):
    """在浏览器中打开文件"""
    print_section("浏览器预览", "🌐")
    
    try:
        abs_path = os.path.abspath(file_path)
        url = f"file://{abs_path}"
        
        print(f"正在打开浏览器...")
        webbrowser.open(url)
        print(f"✅ 已在默认浏览器中打开")
        print(f"📎 URL: {url}")
        
    except Exception as e:
        print(f"❌ 打开浏览器失败: {e}")
        print(f"请手动打开文件: {abs_path}")

def show_next_steps():
    """显示下一步建议"""
    print_section("下一步建议", "🚀")
    
    suggestions = [
        "📚 阅读 README.md 了解完整功能",
        "🔧 修改 template.html 自定义样式",
        "🤖 扩展 create_hot_publish_page.py 添加新内容类型",
        "📱 测试移动端显示效果",
        "🔄 集成到你的工作流中",
        "🌟 分享给其他小红书创作者"
    ]
    
    for suggestion in suggestions:
        print(f"  • {suggestion}")

def main():
    """主函数"""
    try:
        # 创建演示页面
        output_file, generator = create_demo_page()
        
        # 展示功能亮点
        show_feature_highlights()
        
        # 显示使用说明
        show_usage_instructions()
        
        # 显示技术细节
        show_technical_details(generator)
        
        # 询问是否打开浏览器
        print_section("浏览器预览选项", "💻")
        choice = input("\n是否在浏览器中打开生成的页面？(y/n): ").strip().lower()
        
        if choice == 'y':
            open_in_browser(output_file)
        else:
            print(f"\n📁 文件位置: {os.path.abspath(output_file)}")
            print("💡 你可以稍后手动打开文件查看效果")
        
        # 显示下一步建议
        show_next_steps()
        
        print_section("演示完成", "🎉")
        print(f"✨ 演示完成!")
        print(f"📄 生成的页面文件: {output_file}")
        print(f"📊 数据文件: {output_file.replace('.html', '.json')}")
        print("\n感谢使用小红书热点发布系统！")
        
        # 显示文件位置
        print(f"\n📍 文件位置:")
        print(f"   HTML: {os.path.abspath(output_file)}")
        print(f"   JSON: {os.path.abspath(output_file.replace('.html', '.json'))}")
        
    except KeyboardInterrupt:
        print("\n\n👋 用户中断，演示结束")
    except ValueError as e:
        print(f"\n❌ 参数错误: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 演示过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()