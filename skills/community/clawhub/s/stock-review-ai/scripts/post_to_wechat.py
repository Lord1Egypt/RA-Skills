import requests
import json
import os
import re
from typing import Optional, Dict, List, Any
from pathlib import Path
import markdown

from utils.logger import get_logger
from config import Settings

class WeChatPoster:
    """WeChat Official Account Poster"""
    
    def __init__(self, config: Settings):
        self.config = config
        self.logger = get_logger(__name__)
        self.access_token = None
        self.token_expires = 0
    
    def create_draft(self, market_summary: str, ai_analysis: Optional[str], date: str, 
                     title: Optional[str] = None, cover_image_path: Optional[str] = None) -> Optional[str]:
        """
        Create a WeChat Official Account draft
        
        Args:
            market_summary: market summary Markdown
            ai_analysis: AI analysis Markdown
            date: date
            title: custom title (if None, auto-generated)
            cover_image_path: path to cover image
            
        Returns:
            draft media_id if successful, None otherwise
        """
        if not self.config.has_wechat:
            self.logger.warning("WeChat credentials not configured")
            return None
        
        try:
            # 1. Get access token
            token = self._get_access_token()
            if not token:
                self.logger.error("Failed to get access token")
                return None
            
            # 2. Build article title
            if not title:
                title = f"A股全市场复盘：{date} 深度解析及AI洞察"
            
            # 3. Convert markdown to WeChat-ready HTML
            content_html = self._convert_md_to_wechat_html(market_summary, ai_analysis, date)
            
            # 4. Upload cover image and get media_id
            thumb_media_id = None
            if cover_image_path is None or not os.path.exists(cover_image_path):
                self.logger.warning("No cover image provided, using default")
                # 使用默认封面图或留空
                # thumb_media_id = self._get_default_thumb_media_id()
                possible_covers = [
                    Path.cwd() / "cover.jpg",
                    Path(__file__).parent / "cover.jpg",
                    Path(__file__).parent.parent / "cover.jpg",
                    Path(__file__).parent.parent.parent / "cover.jpg",
                ]
                for p in possible_covers:
                    if p.exists():
                        cover_image_path = str(p)
                        print(f"✅ 使用默认封面: {cover_image_path}")
                        break
            thumb_media_id = self._upload_image_as_thumb(token, cover_image_path)
            
            if not thumb_media_id:
                self.logger.error("No valid cover image media_id")
                return None
            
            # 5. Create draft
            url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={token}"
            
            # 生成摘要（取内容前100字）
            digest = self._generate_digest(content_html)
            
            data = {
                "articles": [{
                    "title": title,
                    "author": "AI复盘助手",
                    "digest": digest,
                    "content": content_html,
                    "thumb_media_id": thumb_media_id,
                    "show_cover_pic": 1,
                    "need_open_comment": 1,
                    "only_fans_can_comment": 0
                }]
            }
            
            self.logger.info(f"Creating WeChat draft: {title}")
            
            response = requests.post(
                url, 
                data=json.dumps(data, ensure_ascii=False).encode('utf-8'),
                headers={'Content-Type': 'application/json'}
            )
            result = response.json()
            
            if 'media_id' in result:
                media_id = result['media_id']
                self.logger.info(f"✅ WeChat draft created successfully: {media_id}")
                return media_id
            else:
                self.logger.error(f"❌ Failed to create draft: {result}")
                return None
                
        except Exception as e:
            self.logger.error(f"WeChat draft creation failed: {e}")
            import traceback
            self.logger.error(traceback.format_exc())
            return None
    
    def _convert_md_to_wechat_html(self, market_summary: str, ai_analysis: Optional[str], date: str) -> str:
        """Convert markdown to WeChat-friendly HTML with proper styling"""
        # 合并内容
        full_md = market_summary
        if ai_analysis:
            full_md += f"\n\n## 🤖 AI深度分析与洞察\n\n{ai_analysis}"
        
        # 剔除 Markdown 元数据 (Frontmatter)
        full_md = re.sub(r'^---.*?---', '', full_md, flags=re.DOTALL | re.MULTILINE)

        # 1. 转换 Markdown（启用表格、代码块等扩展）
        html = markdown.markdown(full_md, extensions=['tables', 'fenced_code', 'extra'])

        # 2. 移除所有现有的 style 属性（避免重复）
        html = re.sub(r'\s+style=(["\']).*?\1', '', html, flags=re.DOTALL)

        # 3. 注入内联样式
        styles = {
            'h1': 'margin: 15px 0 10px; padding-left: 10px; border-left: 5px solid #07C160; font-size: 20px; font-weight: bold; color: #333; line-height: 1.4;',
            'h2': 'margin: 15px 0 10px; padding-left: 10px; border-left: 5px solid #07C160; font-size: 19px; font-weight: bold; color: #333; line-height: 1.4;',
            'h3': 'margin: 12px 0 8px; font-size: 18px; font-weight: bold; color: #444;',
            'p': 'margin: 8px 0; line-height: 1.6; color: #3f3f3f; font-size: 15px; text-align: justify;',
            'table': 'width: 100%; border-collapse: collapse; margin: 10px 0; font-size: 13px; table-layout: fixed;',
            'th': 'background-color: #f1f1f1; border: 1px solid #dfe2e5; padding: 8px; font-weight: bold; color: #555;',
            'td': 'border: 1px solid #dfe2e5; padding: 8px; text-align: left; word-break: break-word;',
            'strong': 'color: #d63031; font-weight: bold;',
            'blockquote': 'margin: 10px 0; padding: 12px; border-left: 4px solid #07C160; background: #f8f8f8; color: #666;',
            'ul': 'margin: 5px 0; padding-left: 20px; list-style-type: none;',
            'ol': 'margin: 5px 0; padding-left: 20px; list-style-type: none;',
            'li': 'margin: 2px 0; line-height: 1.6; color: #3f3f3f; font-size: 15px; list-style-type: none;'
        }
        for tag, style in styles.items():
            # 处理没有其他属性的标签（如 <tag>）
            html = html.replace(f'<{tag}>', f'<{tag} style="{style}">')
            # 处理带有其他属性的标签（如 <tag attr="value">）
            html = re.sub(rf'<{tag}\s', f'<{tag} style="{style}" ', html)

        # 4. 关键词高亮（确保不引入额外空白）
        keywords = {
            '涨停': '#e84118',
            '跌停': '#4cd137',
            '炸板': '#fa8231',
            '龙虎榜': '#07C160',
            '北向资金': '#1890ff',
            '主力资金': '#fa8c16'
        }
        for word, color in keywords.items():
            pattern = re.compile(re.escape(word))
            html = pattern.sub(f'<span style="color: {color}; font-weight: bold;">{word}</span>', html)

        # 5. 清理HTML：移除空标签，压缩标签间空白
        html = self._clean_wechat_html(html)

        # 6. 外壳封装
        final_html = f"""
        <div style="font-family: -apple-system-font, system-ui, sans-serif; letter-spacing: 0.5px; padding: 15px;">
            {html}
            <p style="color:#999; font-size:12px; text-align:center; margin-top:25px; padding-top:10px; border-top:1px solid #eee;">
                数据来源：AKShare | 发布时间：{date}<br>
                ⚠️ 投资有风险，入市需谨慎。本分析仅供参考，不构成投资建议。
            </p>
        </div>
        """

        # 7. 再次压缩标签间空白（移除外壳与内部之间的换行）
        final_html = re.sub(r'>\s+<', '><', final_html)

        return final_html

    def _clean_wechat_html(self, html: str) -> str:
        """Clean HTML by removing empty tags, extra whitespace, and compressing blank lines"""
        # 1. 移除空的 <li>, <p>, <div> 标签
        html = re.sub(r'<(li|p|div)[^>]*>\s*</\1>', '', html, flags=re.DOTALL)
        
        # 2. 移除连续多个 <br> 标签，保留最多两个（确保不会完全删除有用换行）
        html = re.sub(r'(<br\s*/?>\s*){3,}', '<br><br>', html, flags=re.IGNORECASE)
        
        # 3. 移除标签之间的空白（包括换行和空格），避免产生多余空白节点
        #    注意：这可能会影响 <pre> 或代码块，但微信草稿一般不会放复杂代码，暂时安全
        html = re.sub(r'>\s+<', '><', html)
        
        # 4. 将连续的多个换行符压缩为两个（美化代码，非必要）
        # html = re.sub(r'\n\s*\n', '\n\n', html)
        
        # 5. 可选：将 <p></p> 之间的空白段落彻底删除
        # html = re.sub(r'<p[^>]*>\s*</p>', '', html)
        
        return html
    
    def _get_access_token(self) -> Optional[str]:
        """Get access token from WeChat API"""
        app_id = self.config.wechat_app_id
        app_secret = self.config.wechat_app_secret
        
        if not app_id or not app_secret:
            self.logger.error("WeChat app_id or app_secret not configured")
            return None
        
        url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={app_id}&secret={app_secret}"
        
        try:
            self.logger.info("Requesting WeChat access token...")
            response = requests.get(url, timeout=10)
            result = response.json()
            
            if 'access_token' in result:
                token = result['access_token']
                self.logger.info("✅ Access token obtained successfully")
                return token
            else:
                self.logger.error(f"❌ Failed to get access token: {result}")
                return None
        except Exception as e:
            self.logger.error(f"Access token request failed: {e}")
            return None
    
    def _upload_image_as_thumb(self, access_token: str, image_path: str) -> Optional[str]:
        """
        Upload image as thumbnail and return media_id
            Args:
                access_token: WeChat API access token
                image_path: path to the image file
            
            Returns:
                media_id if upload successful, None otherwise
        """
        if not os.path.exists(image_path):
            self.logger.error(f"Cover image not found: {image_path}")
            return None
        
        url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={access_token}&type=image"
        
        try:
            self.logger.info(f"Uploading cover image: {image_path}")
            
            with open(image_path, 'rb') as f:
                files = {'media': f}
                response = requests.post(url, files=files, timeout=30)
                result = response.json()
            
            media_id = result.get("media_id")
            if media_id:
                self.logger.info(f"✅ Cover image uploaded: {media_id}")
                return media_id
            else:
                self.logger.error(f"❌ Cover image upload failed: {result}")
                return None
                
        except Exception as e:
            self.logger.error(f"Cover image upload failed: {e}")
            return None
    
    def _generate_digest(self, content_html: str, max_length: int = 120) -> str:
        """
        Generate article digest from HTML content with strict length control
        
        WeChat limits digest to 120 characters
        """
        # 移除 HTML 标签
        text = re.sub(r'<[^>]+>', '', content_html)
        # 移除多余空白
        text = re.sub(r'\s+', ' ', text).strip()
        # 移除特殊符号
        text = re.sub(r'[#*_`•·●]', '', text)
        
        # 如果内容太长，取前100字加上关键信息
        if len(text) > max_length:
            # 尝试找到段落开头
            sentences = re.split(r'[。.!?！？]', text)
            digest = sentences[0] if sentences else ""
            
            # 如果第一句就超长，强制截断
            if len(digest) > max_length - 3:
                digest = digest[:max_length-3]
            elif len(digest) < 30 and len(sentences) > 1:
                # 第一句太短，加上第二句的一部分
                second_part = sentences[1][:30]
                digest = digest + "，" + second_part
            
            # 如果还是太短，补充日期信息
            if len(digest) < 20:
                import datetime
                today = datetime.datetime.now().strftime('%m月%d日')
                digest = f"{today} A股市场复盘分析"
        else:
            digest = text
        
        # 最终截断检查
        if len(digest) > max_length:
            digest = digest[:max_length-3] + '...'
        
        # 确保不是空字符串
        if not digest or digest.isspace():
            digest = "A股市场深度复盘分析"
        
        self.logger.debug(f"Generated digest ({len(digest)} chars)")
        return digest
    
    def _get_default_thumb_media_id(self) -> str:
        """Get default cover image media_id"""
        # 可以返回一个固定的封面图 ID，或者上传一个默认图片
        # 这里返回空字符串，微信会使用默认封面
        return ""
    

def main():
    """Test WeChatPoster"""
    import os
    from pathlib import Path
    import sys
    import argparse
    from config import Settings
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--date', type=str, help='Date for the article with format YYYYMMDD, e.g. 20260312')
    parser.add_argument('--market-summary-file', type=str, default=None, help='Markdown file path')
    parser.add_argument('--ai-analysis-file', type=str, default=None, help='Markdown file path')
    parser.add_argument('--cover-file', type=str, default="skills/stock_review/cover.jpg", help='Cover image path')
    parser.add_argument('--title', type=str, default="Test Article", help='Article title')
    args = parser.parse_args()
    
    config = Settings()
    
    # 创建 WeChatPoster 实例
    poster = WeChatPoster(config)
    
    # 准备测试数据
    date = args.date or "20260312"
    
    # 如果指定了 Markdown 文件，从文件读取
    if args.market_summary_file and Path(args.market_summary_file).exists():
        with open(args.market_summary_file, 'r', encoding='utf-8') as f:
            market_summary = f.read()
        print(f"✅ 从文件读取 Markdown: {args.market_summary_file}")
    else:
        print(f"❗️ 未指定 Markdown 文件")
    
    # 如果指定了 Markdown 文件，从文件读取
    if args.ai_analysis_file and Path(args.ai_analysis_file).exists():
        with open(args.ai_analysis_file, 'r', encoding='utf-8') as f:
            ai_analysis = f.read()
        print(f"✅ 从文件读取 Markdown: {args.ai_analysis_file}")
    else:
        print(f"❗️ 未指定 Markdown 文件")

    # 封面图片路径
    cover_image = args.cover_file
    if not cover_image:
        # 尝试查找默认封面
        possible_covers = [
            Path.cwd() / "cover.jpg",
            Path(__file__).parent / "cover.jpg",
            Path(__file__).parent.parent / "cover.jpg",
            Path(__file__).parent.parent.parent / "cover.jpg",
        ]
        for p in possible_covers:
            if p.exists():
                cover_image = str(p)
                print(f"✅ 使用默认封面: {cover_image}")
                break
    
    # 标题
    title = args.title or f"A股全市场复盘：{date} 深度解析及AI洞察"
    
    print(f"\n📝 开始测试微信发布...")
    print(f"   日期: {date}")
    print(f"   标题: {title}")
    print(f"   封面图片: {cover_image or '无'}")
    print("-" * 50)
    
    # 执行发布
    media_id = poster.create_draft(
        market_summary=market_summary,
        ai_analysis=ai_analysis,
        date=date,
        title=title,
        cover_image_path=cover_image
    )
    
    if media_id:
        print(f"\n✅ 测试成功！")
        print(f"   media_id: {media_id}")
        print(f"   请登录微信公众号后台查看草稿")
    else:
        print(f"\n❌ 测试失败！")
        print(f"   请检查日志以获取详细错误信息")


if __name__ == "__main__":
    main()