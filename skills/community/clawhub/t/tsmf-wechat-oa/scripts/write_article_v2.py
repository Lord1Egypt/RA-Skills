#!/usr/bin/env python3
"""
微信公众号文章写作主流程 V2
参考项目工作流：话题分析 → 资料搜索 → 大纲生成 → 自动写作 → 排版优化 → 生成封面 → 推送草稿
支持根据 cron_job 自动判断模式
"""

import os
import sys
import json
import argparse
from typing import Dict, List, Optional
from datetime import datetime

# 导入自定义模块
sys.path.insert(0, os.path.dirname(__file__))
from outline_generator import OutlineGenerator
from html_writer import HTMLWriter
from content_validator import ContentValidator, verify_article_facts
from cron_detector import get_writing_mode, get_mode_description
from content_searcher import ContentSearcher
from ai_writer import AIWriter

# 微信公众号配置 - 从环境变量读取（无默认值，必须配置）
WECHAT_APP_ID = os.getenv('WECHAT_APP_ID', '')
WECHAT_APP_SECRET = os.getenv('WECHAT_APP_SECRET', '')



class ArticleWriterV2:
    """文章写作主控类 V2 - 完整工作流"""
    
    def __init__(self):
        self.outline_gen = OutlineGenerator()
        self.html_writer = HTMLWriter()
        self.validator = ContentValidator()
        self.searcher = ContentSearcher()
        self.ai_writer = AIWriter()
    
    def auto_write(self, topic: str, word_count: int = 1500) -> Dict:
        """
        自动写作模式 - 完整工作流（参考项目设计）
        
        流程：
        [1] 话题分析 → [2] 资料搜索 → [3] 大纲生成 → [4] 自动写作 → 
        [5] 排版优化 → [6] 生成封面 → [7] 推送草稿
        
        Args:
            topic: 文章主题
            word_count: 目标字数
            
        Returns:
            包含完整信息的结果字典
        """
        print(f"\n🚀 开始自动写作: {topic}")
        print(f"📌 模式: {get_mode_description()}")
        print("=" * 60)
        
        # [1] 话题分析
        print("\n[1/7] 话题分析...")
        article_type, confidence = self.outline_gen.analyze_topic(topic)
        type_name = self.outline_gen.TEMPLATES[article_type]['name']
        print(f"   检测到类型: {type_name} (置信度: {confidence:.0%})")
        
        # [2] 资料搜索（使用 Tavily Search）
        print("\n[2/7] 资料搜索与验证...")
        search_result = self.searcher.search_and_summarize(topic, article_type)
        print(f"   搜索查询: {search_result['query_count']} 个")
        print(f"   找到资料: {search_result['result_count']} 条")
        if search_result['summary']:
            print(f"   资料摘要: {search_result['summary'][:100]}...")
        
        # [3] 大纲生成
        print("\n[3/7] 生成文章大纲...")
        outline = self.outline_gen.generate_outline(topic, word_count, article_type)
        print(f"   文章结构 ({outline['word_count']}字):")
        for i, section in enumerate(outline['sections'], 1):
            print(f"   {i}. {section['title']} ({section['word_count']}字)")
        
        # [4] 自动写作（使用 AI）
        print("\n[4/7] AI 自动写作...")
        sections = self.ai_writer.write_full_article(
            topic=topic,
            outline=outline,
            search_summary=search_result
        )
        
        # [5] 排版优化
        print("\n[5/7] 排版优化...")
        html_content = self.html_writer.write_article(topic, sections)
        html_content = self.html_writer.add_footer(html_content, "小爪制作，需要审核")
        print("   ✓ HTML 生成完成")
        
        # 内容验证
        print("\n[验证] 检查内容准确性...")
        full_text = '\n'.join([s['content'] for s in sections])
        is_valid, warnings = verify_article_facts(full_text)
        if warnings:
            print(f"   ⚠️  发现 {len(warnings)} 处需要核实:")
            for w in warnings[:3]:
                print(f"      - {w}")
        else:
            print("   ✓ 未发现明显问题")
        
        # [6] 生成封面
        print("\n[6/7] 生成封面...")
        cover_html = self._generate_cover_html(topic, article_type)
        print(f"   ✓ 封面 HTML 已生成: {cover_html}")
        print("   💡 提示: 请用浏览器打开 HTML 文件，下载 PNG 封面")
        
        # [7] 推送草稿（自动模式时自动推送）
        print("\n[7/7] 推送草稿...")
        
        # 获取 access_token
        access_token = self._get_access_token()
        thumb_media_id = ""
        media_id = None
        
        if access_token:
            # 尝试使用默认封面
            default_cover = "images/cover.jpg"
            if os.path.exists(default_cover):
                thumb_media_id = self._upload_cover_image(access_token, default_cover) or ""
            
            # 推送草稿
            media_id = self._push_draft(
                access_token=access_token,
                title=topic,
                content=html_content,
                thumb_media_id=thumb_media_id
            )
        
        if media_id:
            print(f"   ✓ 草稿已推送，Media ID: {media_id}")
        else:
            print("   ⚠️  推送失败或跳过，文章已保存到本地")
            print(f"   如需手动推送: python3 push_draft.py --file <文件路径> --title \"{topic}\"")
        
        print("\n" + "=" * 60)
        print("✅ 自动写作完成!")
        
        return {
            'title': topic,
            'html_content': html_content,
            'outline': outline,
            'article_type': article_type,
            'search_result': search_result,
            'warnings': warnings,
            'cover_html': cover_html,
            'thumb_media_id': thumb_media_id,
            'media_id': media_id,
            'sections': sections
        }
    
    def guided_write(self, topic: str, word_count: int = 1500, 
                     style: str = None, requirements: str = None) -> Dict:
        """
        指定主题写作模式（半自动，可交互）
        
        流程与自动模式相同，但在关键节点允许用户干预
        
        Args:
            topic: 文章主题
            word_count: 目标字数
            style: 指定风格
            requirements: 特殊要求
            
        Returns:
            包含完整信息的结果字典
        """
        print(f"\n🎯 开始指定主题写作: {topic}")
        print(f"📌 模式: {get_mode_description()}")
        print("=" * 60)
        
        # [1] 确认需求
        print("\n[1/7] 确认写作需求...")
        if style:
            print(f"   指定风格: {style}")
        if requirements:
            print(f"   特殊要求: {requirements}")
        print(f"   目标字数: {word_count}字")
        print("   💡 提示: 在实际交互中，这里会询问用户确认需求")
        
        # [2] 资料搜索（用户可参与）
        print("\n[2/7] 资料搜索...")
        article_type, _ = self.outline_gen.analyze_topic(topic)
        if style:
            article_type = style
        search_result = self.searcher.search_and_summarize(topic, article_type)
        print(f"   找到 {search_result['result_count']} 条相关资料")
        print("   💡 提示: 用户可提供参考资料或修改搜索方向")
        
        # [3] 大纲确认（用户审核）
        print("\n[3/7] 生成并确认大纲...")
        outline = self.outline_gen.generate_outline(topic, word_count, article_type)
        
        print(f"\n📋 文章大纲 ({outline['type_name']}):")
        outline_text = self.outline_gen.outline_to_text(outline)
        print(outline_text)
        print("\n💡 提示: 在实际交互中，这里会询问用户是否修改大纲")
        
        # [4] 分段写作（用户可干预）
        print("\n[4/7] 分段写作...")
        sections = []
        
        for i, section in enumerate(outline['sections'], 1):
            print(f"\n   写作第 {i}/{len(outline['sections'])} 部分: {section['title']}")
            print(f"   目标字数: {section['word_count']}字")
            print(f"   关键点: {', '.join(section['key_points'][:2])}")
            
            # 使用 AI 写作
            content = self.ai_writer.write_section(
                title=section['title'],
                word_count=section['word_count'],
                key_points=section['key_points'],
                context=topic,
                search_results=search_result.get('results')
            )
            
            sections.append({
                'title': section['title'],
                'content': content
            })
            
            actual_length = len(content.replace(' ', '').replace('\n', ''))
            print(f"   ✓ 完成 ({actual_length}字)")
            print("   💡 提示: 实际交互中，这里会展示内容并询问是否修改")
        
        # [5] 排版优化
        print("\n[5/7] 排版优化...")
        html_content = self.html_writer.write_article(topic, sections)
        
        # [6] 内容验证
        print("\n[6/7] 验证内容准确性...")
        full_text = '\n'.join([s['content'] for s in sections])
        is_valid, warnings = verify_article_facts(full_text)
        if warnings:
            print(f"   ⚠️  发现 {len(warnings)} 处需要核实")
        else:
            print("   ✓ 内容检查通过")
        
        # [7] 添加页脚
        print("\n[7/7] 添加页脚...")
        html_content = self.html_writer.add_footer(html_content, "小爪制作，需要审核")
        
        print("\n" + "=" * 60)
        print("✅ 指定主题写作完成!")
        
        return {
            'title': topic,
            'html_content': html_content,
            'outline': outline,
            'article_type': outline['type'],
            'search_result': search_result,
            'warnings': warnings,
            'sections': sections
        }
    
    def _generate_cover_html(self, topic: str, style: str = "minimal") -> str:
        """生成封面 HTML 文件"""
        # 根据主题选择配色
        themes = {
            'minimal': {'bg': 'linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%)', 'accent': '#0984e3'},
            'warm': {'bg': 'linear-gradient(135deg, #8b6914 0%, #d4c4a8 100%)', 'accent': '#f5f0e8'},
            'tech': {'bg': 'linear-gradient(135deg, #0d1117 0%, #161b22 50%, #21262d 100%)', 'accent': '#58a6ff'},
            'fresh': {'bg': 'linear-gradient(135deg, #ff6b6b 0%, #4ecdc4 50%, #45b7d1 100%)', 'accent': '#ffffff'},
            'magazine': {'bg': 'linear-gradient(135deg, #1a1a1a 0%, #3d3d3d 50%, #5a5a5a 100%)', 'accent': '#c0a080'}
        }
        
        theme = themes.get(style, themes['minimal'])
        
        html_content = f'''<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
.cover {{ 
    width: 900px; 
    height: 383px; 
    background: {theme['bg']}; 
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', sans-serif;
}}
.title {{
    color: {theme['accent']};
    font-size: 42px;
    font-weight: 700;
    text-align: center;
    letter-spacing: 2px;
    padding: 0 40px;
    line-height: 1.3;
}}
.badge {{
    background: rgba(225, 112, 85, 0.9);
    color: white;
    padding: 12px 35px;
    border-radius: 30px;
    font-size: 18px;
    font-weight: 500;
    margin-top: 25px;
}}
</style>
</head>
<body>
<div class="cover">
    <div class="title">{topic}</div>
    <div class="badge">小爪制作，需要审核</div>
</div>
</body>
</html>'''
        
        # 保存 HTML 文件
        cover_file = f"cover_{datetime.now().strftime('%Y%m%d')}_{topic[:10]}.html"
        with open(cover_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"   ✓ 封面 HTML 已生成: {cover_file}")
        return cover_file
    
    def _get_access_token(self) -> Optional[str]:
        """获取微信 Access Token"""
        import requests
        url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={WECHAT_APP_ID}&secret={WECHAT_APP_SECRET}"
        try:
            response = requests.get(url, timeout=30)
            result = response.json()
            if 'access_token' in result:
                return result['access_token']
            else:
                print(f"   ⚠️  获取 Token 失败: {result}")
                return None
        except Exception as e:
            print(f"   ⚠️  请求失败: {e}")
            return None
    
    def _upload_cover_image(self, access_token: str, image_path: str) -> Optional[str]:
        """上传封面图片到微信，获取 thumb_media_id"""
        import requests
        
        if not os.path.exists(image_path):
            print(f"   ⚠️  封面图片不存在: {image_path}")
            return None
        
        url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={access_token}&type=thumb"
        try:
            print(f"   📤 正在上传封面...")
            with open(image_path, 'rb') as f:
                files = {'media': f}
                response = requests.post(url, files=files, timeout=30)
            result = response.json()
            if 'media_id' in result:
                print(f"   ✓ 封面上传成功")
                return result['media_id']
            else:
                print(f"   ⚠️  封面上传失败: {result}")
                return None
        except Exception as e:
            print(f"   ⚠️  上传异常: {e}")
            return None
    
    def _push_draft(self, access_token: str, title: str, content: str, 
                   thumb_media_id: str, author: str = "小爪") -> Optional[str]:
        """推送草稿到微信公众号"""
        import requests
        
        url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={access_token}"
        data = {
            "articles": [{
                "title": title,
                "content": content,
                "author": author,
                "digest": f"{title} - 小爪制作",
                "thumb_media_id": thumb_media_id,
                "show_cover_pic": 1,
                "need_open_comment": 1,
                "only_fans_can_comment": 0
            }]
        }
        
        try:
            print(f"   📤 正在推送草稿...")
            response = requests.post(
                url,
                data=json.dumps(data, ensure_ascii=False).encode('utf-8'),
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            result = response.json()
            if 'media_id' in result:
                print(f"   ✓ 草稿推送成功")
                return result['media_id']
            else:
                print(f"   ⚠️  推送失败: {result}")
                return None
        except Exception as e:
            print(f"   ⚠️  请求异常: {e}")
            return None
    
    def save_article(self, result: Dict, output_dir: str = "_drafts") -> str:
        """保存文章到文件"""
        # 确保目录存在
        os.makedirs(output_dir, exist_ok=True)
        
        # 生成文件名
        date_str = datetime.now().strftime("%Y-%m-%d")
        safe_title = result['title'][:20].replace(' ', '_').replace('/', '_')
        filename = f"{date_str}-{safe_title}.html"
        filepath = os.path.join(output_dir, filename)
        
        # 保存 HTML
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(result['html_content'])
        
        # 同时保存大纲 JSON
        outline_filename = f"{date_str}-{safe_title}.json"
        outline_filepath = os.path.join(output_dir, outline_filename)
        with open(outline_filepath, 'w', encoding='utf-8') as f:
            json.dump(result['outline'], f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 文章已保存:")
        print(f"   HTML: {filepath}")
        print(f"   大纲: {outline_filepath}")
        
        return filepath


def main():
    parser = argparse.ArgumentParser(
        description='微信公众号文章写作工具 V2 - 完整工作流'
    )
    parser.add_argument('topic', nargs='?', help='文章主题')
    parser.add_argument('--mode', '-m', choices=['auto', 'guided'],
                       default=get_writing_mode(),  # 根据 cron_job 自动判断
                       help=f'写作模式 (默认: {get_writing_mode()})')
    parser.add_argument('--words', '-w', type=int, default=1500,
                       help='目标字数 (默认1500)')
    parser.add_argument('--style', '-s', help='指定文章风格')
    parser.add_argument('--output', '-o', default='_drafts',
                       help='输出目录')
    parser.add_argument('--no-save', action='store_true',
                       help='不保存文件，仅输出到控制台')
    
    args = parser.parse_args()
    
    if not args.topic:
        print("=" * 70)
        print("微信公众号全自动写作工具 V2")
        print("=" * 70)
        print("\n使用方法:")
        print("  python3 write_article_v2.py '文章主题'")
        print("  python3 write_article_v2.py '文章主题' --words 2000")
        print("\n模式说明:")
        print(f"  当前检测到的模式: {get_mode_description()}")
        print("  auto    - 全自动写作（检测到定时任务时默认）")
        print("  guided  - 指定主题写作（无定时任务时默认）")
        print("\n环境变量:")
        print("  TAVILY_API_KEY      - Tavily 搜索 API Key")
        print("  ANTHROPIC_API_KEY   - Claude API Key（用于AI写作）")
        print("  WECHAT_AUTO_MODE    - 设置为 true 强制自动模式")
        print("=" * 70)
        return
    
    # 创建写作器
    writer = ArticleWriterV2()
    
    # 根据模式写作
    if args.mode == 'auto':
        result = writer.auto_write(args.topic, args.words)
    else:
        result = writer.guided_write(args.topic, args.words, args.style)
    
    # 保存文件
    if not args.no_save:
        filepath = writer.save_article(result, args.output)
        print(f"\n📝 下一步:")
        print(f"   推送草稿: python3 push_draft.py --file {filepath} --title \"{result['title']}\"")


if __name__ == "__main__":
    main()
