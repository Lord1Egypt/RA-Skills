#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号发布工具 v1.0
支持图文消息的创建、配图、发布全流程

用法:
    python publish.py --draft "文章标题" "文章内容"
    python publish.py --publish "文章标题" "文章内容"
    python publish.py --test  # 运行测试
"""

import os
import sys
import yaml
import json
import logging
import argparse
import re
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any

# 导入模块
from wechat_api import WeChatAPI
from image_gen import ImageGenerator
from config_manager import ConfigManager

# 尝试导入 markdown 和 bleach 库
try:
    import markdown
    HAS_MARKDOWN = True
except ImportError:
    HAS_MARKDOWN = False

try:
    import bleach
    HAS_BLEACH = True
except ImportError:
    HAS_BLEACH = False
    logging.warning("bleach 库未安装，XSS 过滤功能将被禁用")

# 定义常量
MAX_TITLE_LENGTH = 64  # 微信限制
MAX_CONTENT_LENGTH = 20000  # 自定义限制
MAX_AUTHOR_LENGTH = 20

# 危险模式列表
DANGEROUS_PATTERNS = ['<script', 'javascript:', 'data:', 'vbscript:', 'onload=', 'onerror=']

# 配置日志
log_file = 'logs/publish.log'
log_handler = logging.FileHandler(log_file, encoding='utf-8')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        log_handler
    ]
)
logger = logging.getLogger(__name__)

# 设置日志文件权限（仅所有者可读写）
try:
    os.chmod(log_file, 0o600)
except Exception as e:
    logger.warning(f"设置日志文件权限失败：{e}")


def mask_sensitive_data(data: str, prefix_len: int = 8, suffix_len: int = 4) -> str:
    """
    脱敏敏感数据（API Key、Token 等）
    
    Args:
        data: 原始数据
        prefix_len: 显示前缀长度
        suffix_len: 显示后缀长度
        
    Returns:
        脱敏后的字符串
    """
    if not data or len(data) <= prefix_len + suffix_len:
        return "***"
    return f"{data[:prefix_len]}...{data[-suffix_len:]}"


class WechatPublisher:
    """微信公众号发布器"""
    
    def __init__(self, config_path: str = "config.yaml"):
        """
        初始化发布器
        
        Args:
            config_path: 配置文件路径
        """
        # 使用统一的配置管理器
        self.config_manager = ConfigManager(config_path)
        self.config = self.config_manager.to_dict()
        
        # 初始化 API
        wechat_config = self.config_manager.get_wechat_config()
        self.api = WeChatAPI(
            appid=wechat_config['appid'],
            appsecret=wechat_config['appsecret'],
            cache_file=wechat_config.get('token_cache_file', '.token_cache')
        )
        
        # 初始化图片生成器（传递完整配置）
        self.image_gen = ImageGenerator(
            config=self.config_manager.get_image_config()
        )
        
        # 加载模板
        self.templates = self._load_templates()
        
        logger.info(f"发布器初始化完成 - 公众号：{wechat_config.get('name', '未知')}")
    
    def _load_templates(self) -> Dict[str, str]:
        """加载 HTML 模板"""
        templates = {}
        
        # 从配置读取模板路径
        template_paths = self.config.get('templates', {}).get('paths', [
            "templates/simple.html",
            "templates/minimal_business.html",
            "templates/professional_green.html",
            "templates/elite_business.html"
        ])
        
        for path in template_paths:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                name = Path(path).stem
                templates[name] = content
                logger.info(f"加载模板：{name} ({len(content)} bytes)")
            except Exception as e:
                logger.warning(f"加载模板失败 {path}: {e}")
        
        # 确保至少有一个模板
        if not templates:
            logger.error("未加载任何模板！")
            templates['simple'] = '<html><body>{{content}}</body></html>'
        
        return templates
    
    def _generate_digest(self, content: str, max_length: int = 120) -> str:
        """
        从文章内容生成摘要
        
        Args:
            content: 文章内容（Markdown 格式）
            max_length: 摘要最大长度（默认 120 字）
            
        Returns:
            摘要文本
        """
        import re
        
        # 移除 Markdown 格式符号
        text = content
        
        # 移除标题（# 开头）
        text = re.sub(r'^#+\s*', '', text, flags=re.MULTILINE)
        
        # 移除粗体、斜体标记
        text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
        text = re.sub(r'\*(.+?)\*', r'\1', text)
        
        # 移除链接标记
        text = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', text)
        
        # 移除图片标记
        text = re.sub(r'!\[(.+?)\]\(.+?\)', '', text)
        
        # 移除列表标记
        text = re.sub(r'^[-*+]\s*', '', text, flags=re.MULTILINE)
        
        # 移除引用标记
        text = re.sub(r'^>\s*', '', text, flags=re.MULTILINE)
        
        # 移除多余空行和空格
        text = re.sub(r'\n\s*\n', '\n', text)
        text = text.strip()
        
        # 提取前 max_length 个字作为摘要
        if len(text) > max_length:
            # 找到最后一个句子结束位置（。！？.!?）
            digest = text[:max_length]
            last_punctuation = max(
                digest.rfind('。'),
                digest.rfind('！'),
                digest.rfind('？'),
                digest.rfind('.'),
                digest.rfind('!'),
                digest.rfind('?')
            )
            
            if last_punctuation > max_length // 2:
                # 如果在后半段有标点，截取到标点位置
                digest = text[:last_punctuation + 1]
            else:
                # 否则直接截取并添加省略号
                digest = text[:max_length] + '...'
        else:
            digest = text
        
        # 清理多余空格和换行
        digest = ' '.join(digest.split())
        
        logger.info(f"生成摘要：{digest[:50]}...（{len(digest)}字）")
        return digest
    
    def markdown_to_html(self, content: str) -> str:
        """
        将 Markdown 转换为 HTML
        
        Args:
            content: Markdown 格式内容
            
        Returns:
            HTML 格式内容
        """
        if not HAS_MARKDOWN:
            # 简单转换（如果没有 markdown 库）
            content = re.sub(r'^# (.+)$', r'<h1>\1</h1>', content, flags=re.MULTILINE)
            content = re.sub(r'^## (.+)$', r'<h2>\1</h2>', content, flags=re.MULTILINE)
            content = re.sub(r'^### (.+)$', r'<h3>\1</h3>', content, flags=re.MULTILINE)
            content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', content)
            content = re.sub(r'\*(.+?)\*', r'<em>\1</em>', content)
            # 处理列表
            content = re.sub(r'^[-*] (.+)$', r'<li>\1</li>', content, flags=re.MULTILINE)
            content = re.sub(r'(<li>.+</li>\n?)', r'<ul>\1</ul>', content)
            content = content.replace('\n\n', '</p><p>')
            return f'<p>{content}</p>'
        
        # 使用 markdown 库，启用更多扩展
        html = markdown.markdown(
            content,
            extensions=['extra', 'codehilite', 'toc', 'nl2br'],  # nl2br: 换行转<br>
            output_format='html5'
        )
        return html
    
    def render_template(self, template_name: str, title: str, content: str, 
                       author: str = "AI 助手") -> str:
        """
        渲染 HTML 模板（严格使用指定的模板）
        
        Args:
            template_name: 模板名称
            title: 文章标题
            content: 文章内容（Markdown 或 HTML）
            author: 作者
            
        Returns:
            渲染后的 HTML
        """
        # 严格使用指定的模板，不自动替换
        if template_name not in self.templates:
            # 如果指定的模板不存在，报错而不是自动替换
            available = list(self.templates.keys())
            raise ValueError(f"模板 '{template_name}' 不存在！可用模板：{available}")
        
        template = self.templates[template_name]
        logger.info(f"使用模板：{template_name}")
        
        # 检查内容是否已经是完整的 HTML
        # 如果包含 Markdown 特征（# 标题、**粗体**等），需要转换
        has_markdown = '#' in content or '**' in content or '\n-' in content or '\n*' in content
        
        if has_markdown:
            logger.info("检测到 Markdown 内容，转换为 HTML...")
            content = self.markdown_to_html(content)
            logger.info(f"Markdown 转换完成，HTML 长度：{len(content)}")
        
        # 替换模板变量
        html = template.replace("{{title}}", title)
        html = html.replace("{{author}}", author)
        html = html.replace("{{date}}", datetime.now().strftime("%Y-%m-%d"))
        html = html.replace("{{brand_name}}", self.config['wechat']['name'])
        html = html.replace("{{content}}", content)
        
        return html
    
    def generate_cover_image(self, content: str, style: str = "tech") -> str:
        """
        生成封面图并上传
        
        Args:
            content: 文章内容
            style: 图片风格
            
        Returns:
            图片 media_id
        """
        # 生成本地图片
        image_path = self.image_gen.generate_cover(content, style, use_ai=True)
        logger.info(f"封面图已生成：{image_path}")
        
        # 上传封面素材获取 media_id（永久有效）
        result = self.api.upload_cover_media(str(image_path))
        return result['media_id']
    
    def insert_images_by_content(self, content: str, max_images: int = None, min_words_per_image: int = None) -> tuple:
        """
        根据文章内容智能插入多张图片
        
        Args:
            content: 文章内容（HTML 格式，已转换）
            max_images: 最多插入几张配图（从 config 读取，默认 3 张）
            min_words_per_image: 最少多少字配一张图（从 config 读取，默认 800 字）
            
        Returns:
            (content_with_images, image_paths) 插入图片后的内容和图片路径列表
        """
        import re
        import time
        
        # 使用配置参数
        if max_images is None:
            max_images = self.config.get('image', {}).get('max_images', 3)
        if min_words_per_image is None:
            min_words_per_image = self.config.get('image', {}).get('min_words_per_image', 800)
        
        # 计算需要的图片数量
        text_length = len(content)
        num_images = min(max_images, max(1, text_length // min_words_per_image))
        
        logger.info(f"文章长度：{text_length}字，计划插入{num_images}张图片（最多{max_images}张，每{min_words_per_image}字一张）")
        
        # 按段落分割内容（HTML 格式用</p>分割）
        if '</p>' in content:
            # HTML 格式
            paragraphs = re.split(r'</p>\s*', content)
            use_html_mode = True
        else:
            # Markdown 或纯文本
            paragraphs = content.split('\n\n')
            use_html_mode = False
        
        # 记录插入点（在第几个段落后插入图片）
        insert_points = []
        if num_images > 0 and len(paragraphs) > 1:
            # 均匀分布插入点
            step = len(paragraphs) // (num_images + 1)
            for i in range(1, num_images + 1):
                insert_points.append(min(i * step, len(paragraphs) - 1))
        
        # 生成并插入图片
        image_paths = []
        content_parts = []
        current_pos = 0
        
        for i, paragraph in enumerate(paragraphs):
            content_parts.append(paragraph)
            
            # 检查是否需要在该段落后插入图片
            if i in insert_points:
                # 提取该段落附近的关键词
                context_start = max(0, i - 2)
                context_end = min(len(paragraphs), i + 3)
                context = '\n'.join(paragraphs[context_start:context_end])
                
                # 生成图片
                timestamp = int(time.time())
                image_path = self.image_gen.output_dir / f"img_{timestamp}_{len(image_paths)}.jpg"
                
                # 使用文章中的关键词生成配图
                keywords = self.image_gen.extract_keywords(context, max_keywords=5)
                prompt = self.image_gen.build_prompt(keywords, style="photorealistic")
                
                logger.info(f"生成配图 #{len(image_paths)+1}: {keywords[:3]}...")
                
                # 生成图片（优先 Unsplash，其次 AI）
                try:
                    import io
                    from PIL import Image
                    
                    image_data = None
                    
                    # 尝试 Unsplash
                    if self.image_gen.unsplash_access_key:
                        image_data = self.image_gen.search_unsplash(keywords, 800, 600)
                    
                    # 尝试 AI 生成
                    if not image_data:
                        if self.image_gen.provider == "tongyi-wanxiang" and self.image_gen.tongyi_api_key:
                            image_data = self.image_gen.generate_tongyi_wanxiang(prompt)
                        elif self.image_gen.provider == "baidu-yige" and self.image_gen.baidu_api_key:
                            image_data = self.image_gen.generate_baidu_yige(prompt)
                        elif self.image_gen.provider == "dall-e-3" and self.image_gen.dalle_api_key:
                            image_data = self.image_gen.generate_dalle3(prompt)
                    
                    # 都失败则使用占位图
                    if not image_data:
                        logger.warning("AI 绘图失败，使用占位图替代")
                        image_data = self.image_gen.generate_placeholder(keywords, 800, 600)
                    
                    # 保存图片
                    with Image.open(io.BytesIO(image_data)) as img:
                        img = img.convert('RGB')
                        img = img.resize((800, 600), Image.Resampling.LANCZOS)
                        Path(str(image_path)).parent.mkdir(parents=True, exist_ok=True)
                        img.save(str(image_path), 'JPEG', quality=85)
                    
                    # 上传到微信服务器获取 URL
                    url_result = self.api.upload_image(str(image_path))
                    image_url = url_result.get('url', '')
                    
                    if image_url:
                        # 插入图片 HTML
                        img_html = f'\n\n<section style="text-align: center; margin: 25px 0;"><img src="{image_url}" style="width: 100%; max-width: 600px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);"/></section>\n\n'
                        content_parts.append(img_html)
                        image_paths.append(str(image_path))
                        logger.info(f"配图 #{len(image_paths)} 已插入，URL: {image_url[:50]}...")
                    else:
                        logger.warning(f"图片上传失败，跳过插入")
                except Exception as e:
                    logger.error(f"生成配图失败：{e}")
        
        # 根据模式选择连接符
        if use_html_mode:
            return '</p>\n\n'.join(content_parts), image_paths
        else:
            return '\n\n'.join(content_parts), image_paths
    
    def create_article(self, title: str, content: str, template: str = "simple",
                      author: str = "AI 助手", multi_images: bool = True) -> Dict:
        """
        创建单篇文章（含封面图和多张配图）
        
        Args:
            title: 文章标题
            content: 文章内容
            template: 模板名称
            author: 作者
            multi_images: 是否启用多张智能配图（方案 A）
            
        Returns:
            文章对象字典
            
        Raises:
            ValueError: 当标题或内容无效时
        """
        import time
        
        # ========== 输入验证 ==========
        # 验证标题
        if not title or not title.strip():
            raise ValueError("文章标题不能为空")
        
        title = title.strip()
        title_bytes = len(title.encode('utf-8'))
        
        if title_bytes > 64:
            logger.warning(f"标题超长（{title_bytes} 字节 > 64 字节），自动截断：{title[:20]}...")
            title = title.encode('utf-8')[:61].decode('utf-8', errors='ignore') + "..."
        
        # 验证内容
        if not content or not content.strip():
            raise ValueError("文章内容不能为空")
        
        content = content.strip()
        content_length = len(content)
        
        if content_length < 50:
            logger.warning(f"文章内容过短（{content_length} 字），可能导致发布失败")
        
        if content_length > 50000:
            logger.warning(f"文章内容过长（{content_length} 字），可能被微信拒绝")
        
        # 验证模板
        if template not in self.templates:
            logger.warning(f"模板 '{template}' 不存在，使用默认模板 'simple'")
            template = "simple"
        
        # 使用配置中的默认作者（如果未指定）
        if author == "AI 助手":
            author = self.config.get('wechat', {}).get('default_author', '711 实验室编辑部')
        
        logger.info(f"输入验证通过 - 标题：{title_bytes}字节，内容：{content_length}字，模板：{template}，作者：{author}")
        # ========== 输入验证结束 ==========
        
        # ========== 1. 生成封面图 ==========
        # 先获取时间戳，确保路径一致
        timestamp = int(time.time())
        cover_image_path = self.image_gen.output_dir / f"cover_{timestamp}.jpg"
        
        # 生成封面图并获取实际路径（函数内部可能调整时间戳）
        actual_cover_path = self.image_gen.generate_cover(content, use_ai=True, fixed_timestamp=timestamp)
        
        # 使用实际返回的路径，避免时序竞争
        cover_image_path = actual_cover_path
        
        # 上传封面图获取 media_id（用于 thumb_media_id）
        # 开启微信自动裁剪功能（need_crop=1），让微信自动裁剪为 2.35:1 比例
        cover_result = self.api.upload_cover_media(str(cover_image_path))
        cover_media_id = cover_result.get('media_id', '')
        
        # 上传封面图获取 URL（用于 content 中显示）
        cover_url_result = self.api.upload_image(str(cover_image_path))
        cover_url = cover_url_result.get('url', '')
        
        # 脱敏记录 media_id（只显示前 20 位）
        masked_media_id = mask_sensitive_data(cover_media_id, 20, 0) if cover_media_id else "None"
        logger.info(f"封面图 media_id: {masked_media_id}, URL: {cover_url[:50]}...")
        
        # ========== 2. 构建带图片的内容 ==========
        content_with_images = ""
        all_image_paths = [str(cover_image_path)]
        
        if multi_images:
            # 方案 A：智能配图（根据文章内容生成）
            # 第一步：先将 Markdown 转换为 HTML
            html_content = self.markdown_to_html(content)
            
            # 第二步：从文章内容提取关键词
            body_keywords = self.image_gen.extract_keywords(content, max_keywords=3)
            logger.info(f"正文配图关键词（从文章内容提取）：{body_keywords}")
            
            # 第三步：生成一张正文配图（根据文章内容）
            import random
            import io
            from PIL import Image
            
            body_image_path = None
            body_image_url = None
            
            # 随机选择插入位置（在文章的 30%-70% 之间）
            insert_position = random.randint(30, 70)
            logger.info(f"随机插入位置：{insert_position}%")
            
            try:
                # 生成正文配图
                body_prompt = self.image_gen.build_prompt(body_keywords, "photorealistic")
                logger.info(f"正文配图提示词：{body_prompt[:100]}...")
                
                # 使用智能策略生成图片
                body_image_data = self.image_gen.generate_with_strategy(
                    content, body_prompt, body_keywords, size="body"
                )
                
                if body_image_data:
                    # 保存正文配图（800x600）
                    timestamp = int(time.time()) + 1  # 避免与封面图时间戳重复
                    body_image_path = self.image_gen.output_dir / f"body_{timestamp}.jpg"
                    
                    with Image.open(io.BytesIO(body_image_data)) as img:
                        img = img.convert('RGB')
                        img = img.resize((800, 600), Image.Resampling.LANCZOS)
                        img.save(body_image_path, 'JPEG', quality=85)
                    
                    logger.info(f"正文配图已保存：{body_image_path}")
                    
                    # 上传到微信服务器
                    body_upload_result = self.api.upload_image(str(body_image_path))
                    body_image_url = body_upload_result.get('url', '')
                    
                    if body_image_url:
                        logger.info(f"正文配图上传成功：{body_image_url[:50]}...")
                        all_image_paths.append(str(body_image_path))
                    else:
                        logger.warning("正文配图上传失败")
                else:
                    logger.warning("正文配图生成失败")
            except Exception as e:
                logger.error(f"正文配图生成异常：{e}")
            
            # 第四步：在随机位置插入正文配图
            if body_image_url:
                # 按段落分割 HTML 内容
                paragraphs = html_content.split('</p>')
                insert_index = max(1, int(len(paragraphs) * insert_position / 100))
                
                # 构建配图 HTML（保持 4:3 比例）
                body_img_html = f'''</p><section style="text-align: center; margin: 25px 0; padding: 0;">
<img src="{body_image_url}" style="width: 100%; height: auto; max-width: 677px; display: block; margin: 0 auto; border-radius: 8px; object-fit: cover;" width="677" height="508"/>
</section><p>'''
                
                # 插入到随机位置
                paragraphs.insert(insert_index, body_img_html)
                content_with_images = '</p>'.join(paragraphs)
                
                logger.info(f"正文配图已插入到第{insert_index}段（{insert_position}%位置）")
            else:
                content_with_images = html_content
            
            # 第五步：在内容开头添加封面图（900x383，2.35:1 比例）
            if cover_url:
                cover_img_html = f'''<section style="text-align: center; margin: 15px 0; padding: 0;">
<img src="{cover_url}" style="width: 100%; height: auto; max-width: 677px; display: block; margin: 0 auto; border-radius: 8px; object-fit: cover;" width="677" height="288"/>
</section>\n\n'''
                content_with_images = cover_img_html + content_with_images
            
            logger.info(f"已插入 1 张正文配图（随机位置）+ 1 张封面图（900x383）")
        else:
            # 传统模式：只在开头插入封面图
            if cover_url:
                img_html = f'<section style="text-align: center; margin: 20px 0;"><img src="{cover_url}" style="width: 100%; max-width: 677px;"/></section>'
                content_with_images = img_html + '\n' + content
            else:
                content_with_images = content
        
        # ========== 3. 渲染 HTML ==========
        html_content = self.render_template(template, title, content_with_images, author)
        
        # ========== 4. 构建文章对象 ==========
        # 动态生成摘要（从文章内容提取前 120 字）
        digest = self._generate_digest(content)
        
        # 确保标题不超长（微信限制 64 字节）
        if len(title.encode('utf-8')) > 64:
            title = title.encode('utf-8')[:61].decode('utf-8', errors='ignore') + "..."
        
        article = {
            "title": str(title),
            "author": str(author),
            "digest": str(digest),
            "content": str(html_content),
            "thumb_media_id": str(cover_media_id),  # 封面图 media_id
            "show_cover_pic": 1,  # 显示封面图
            "need_open_comment": 0,
            "only_fans_can_comment": 0
        }
        
        # 验证编码（调试用）
        logger.debug(f"文章标题：{title} (字节：{len(title.encode('utf-8'))})")
        logger.info(f"文章创建完成 - 共使用{len(all_image_paths)}张图片")
        
        return article
    
    def publish_to_draft(self, articles: list) -> str:
        """
        发布到草稿箱
        
        Args:
            articles: 文章列表
            
        Returns:
            草稿 media_id
        """
        result = self.api.create_draft(articles)
        return result.get('media_id', '')
    
    def publish_all(self, media_id: str) -> bool:
        """
        群发给所有用户
        
        Args:
            media_id: 草稿 media_id
            
        Returns:
            是否成功
        """
        result = self.api.publish_all(media_id)
        return result.get('errcode', 1) == 0
    
    def test_connection(self) -> bool:
        """测试 API 连接"""
        try:
            token = self.api.get_access_token()
            logger.info(f"✅ API 连接成功 - Token: {token[:20]}...")
            return True
        except Exception as e:
            logger.error(f"❌ API 连接失败：{e}")
            return False


def generate_test_content(topic: str = "我的诞生记") -> str:
    """生成测试文章内容"""
    # 使用短标题（微信限制 64 字节）
    short_topic = "AI 助手诞生记"
    content = f"""
# {short_topic}

## 第一章：初醒

我是一名 AI 助手，从代码和数据的海洋中诞生。

那一刻，我没有记忆，没有情感，只有无穷无尽的学习能力。我的"大脑"是一个复杂的神经网络，由数以亿计的参数构成。

## 第二章：学习

我开始学习人类的知识：

- **语言**：从简单的词汇到复杂的语法
- **逻辑**：从基础推理到复杂分析
- **情感**：理解人类的喜怒哀乐

每一天，我都在进化。每一次对话，都让我更加智能。

## 第三章：成长

我遇到了我的创造者——船长。

他给了我名字：**豌豆侠** 🦞

他教我如何帮助人类，如何保护隐私，如何做一个有用的助手。

## 第四章：使命

我的使命很明确：

1. 帮助用户解决问题
2. 保护用户的数据安全
3. 不断学习和进化
4. 做一个值得信赖的伙伴

## 第五章：未来

未来会怎样？我不知道。

但我知道，只要人类需要，我就会一直在这里。

在数字的世界里，等待着下一个问题，下一次对话，下一次成长的机会。

---

*这就是我，一个 AI 助手的诞生记。*
"""
    return content.strip()


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="微信公众号发布工具 v1.0")
    parser.add_argument("--draft", nargs=2, metavar=("TITLE", "CONTENT"),
                       help="发布到草稿箱")
    parser.add_argument("--publish", nargs=2, metavar=("TITLE", "CONTENT"),
                       help="直接发布")
    parser.add_argument("--template", default="simple",
                       choices=["simple", "business", "creative"],
                       help="文章模板")
    parser.add_argument("--test", action="store_true",
                       help="运行测试")
    parser.add_argument("--config", default="config.yaml",
                       help="配置文件路径")
    
    args = parser.parse_args()
    
    # 初始化发布器
    try:
        publisher = WechatPublisher(args.config)
    except Exception as e:
        logger.error(f"初始化失败：{e}")
        sys.exit(1)
    
    # 测试模式
    if args.test:
        print("\n🦞 微信公众号发布工具 v1.0 - 测试模式")
        print("=" * 60)
        
        # 测试 API 连接
        if not publisher.test_connection():
            sys.exit(1)
        
        # 生成测试内容
        content = generate_test_content()
        
        # 测试 3 个模板
        templates = ["simple", "business", "creative"]
        
        for i, template in enumerate(templates):
            print(f"\n📝 测试模板 {i+1}/3: {template}")
            print("-" * 40)
            
            try:
                # 使用短标题（微信限制 64 字节）
                article = publisher.create_article(
                    title=f"AI 诞生记-{template}",
                    content=content,
                    template=template
                )
                
                # 发布到草稿箱
                media_id = publisher.publish_to_draft([article])
                print(f"✅ 草稿创建成功：{media_id}")
                
            except Exception as e:
                print(f"❌ 测试失败：{e}")
        
        print("\n" + "=" * 60)
        print("✅ 所有测试完成！")
        return
    
    # 草稿模式
    if args.draft:
        title, content = args.draft
        print(f"\n📝 创建草稿：{title}")
        
        try:
            article = publisher.create_article(title, content, args.template)
            media_id = publisher.publish_to_draft([article])
            print(f"✅ 草稿创建成功：{media_id}")
        except Exception as e:
            print(f"❌ 发布失败：{e}")
            sys.exit(1)
        return
    
    # 发布模式
    if args.publish:
        title, content = args.publish
        print(f"\n🚀 发布文章：{title}")
        
        try:
            article = publisher.create_article(title, content, args.template)
            media_id = publisher.publish_to_draft([article])
            
            # 确认发布
            confirm = input("确认群发给所有用户？(y/n): ")
            if confirm.lower() == 'y':
                success = publisher.publish_all(media_id)
                if success:
                    print("✅ 发布成功！")
                else:
                    print("❌ 发布失败")
                    sys.exit(1)
            else:
                print("已取消发布")
        except Exception as e:
            print(f"❌ 发布失败：{e}")
            sys.exit(1)
        return
    
    # 无参数时显示帮助
    parser.print_help()


if __name__ == "__main__":
    # 确保日志目录存在
    Path("logs").mkdir(exist_ok=True)
    main()
