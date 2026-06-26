#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 图片生成模块
根据文章内容生成封面图
"""

import os
import io
import time
import requests
from pathlib import Path
from typing import Optional, List
import logging
from PIL import Image

logger = logging.getLogger(__name__)


class ImageGenerator:
    """AI 图片生成器"""
    
    def __init__(self, config: Optional[Dict] = None):
        """
        初始化图片生成器
        
        Args:
            config: 配置字典（从 config.yaml 读取）
        """
        self.config = config or {}
        
        # 输出配置
        self.output_width = self.config.get('output_width', 900)
        self.output_height = self.config.get('output_height', 383)
        self.output_format = self.config.get('output_format', 'JPEG')
        self.output_quality = self.config.get('output_quality', 85)
        
        # 配图策略配置
        self.provider_priority = self.config.get('provider_priority', [
            'unsplash', 'tongyi-wanxiang', 'baidu-yige', 'dall-e-3', 'placeholder'
        ])
        self.auto_switch = self.config.get('auto_switch', True)
        self.max_retries = self.config.get('max_retries', 2)
        
        # 读取各图片源详细配置
        providers_config = self.config.get('providers', {})
        
        # 加载环境变量（支持 .env 文件）
        from dotenv import load_dotenv
        load_dotenv()
        
        # Unsplash 配置
        unsplash_cfg = providers_config.get('unsplash', {})
        self.unsplash_enabled = unsplash_cfg.get('enabled', True)
        self.unsplash_access_key = unsplash_cfg.get('access_key', '') or os.environ.get("UNSPLASH_ACCESS_KEY", "")
        self.unsplash_orientation = unsplash_cfg.get('orientation', 'landscape')
        self.unsplash_per_page = unsplash_cfg.get('per_page', 5)
        self.unsplash_monthly_limit = unsplash_cfg.get('monthly_limit')
        
        # 通义万相配置
        tongyi_cfg = providers_config.get('tongyi-wanxiang', {})
        self.tongyi_enabled = tongyi_cfg.get('enabled', True)
        self.tongyi_api_key = tongyi_cfg.get('api_key', '') or os.environ.get("DASHSCOPE_API_KEY", "")
        self.tongyi_api_url = tongyi_cfg.get('api_url', 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image-generation/generation')
        self.tongyi_model = tongyi_cfg.get('model', 'wanx-v1')
        self.tongyi_size = tongyi_cfg.get('size', '1024*1024')
        self.tongyi_style = tongyi_cfg.get('style', '<auto>')
        self.tongyi_num_images = tongyi_cfg.get('num_images', 1)
        self.tongyi_monthly_limit = tongyi_cfg.get('monthly_limit', 100)
        
        # 阿里百炼配置
        bailian_cfg = providers_config.get('bailian', {})
        self.bailian_enabled = bailian_cfg.get('enabled', True)
        self.bailian_api_key = bailian_cfg.get('api_key', '') or os.environ.get("BAILIAN_API_KEY", "")
        self.bailian_api_url = bailian_cfg.get('api_url', 'https://bailian.aliyuncs.com/api/v1/services/aigc/image-generation/generation')
        self.bailian_model = bailian_cfg.get('model', 'wanx-v1')
        self.bailian_size = bailian_cfg.get('size', '1024*1024')
        self.bailian_style = bailian_cfg.get('style', '<auto>')
        self.bailian_num_images = bailian_cfg.get('num_images', 1)
        self.bailian_monthly_limit = bailian_cfg.get('monthly_limit', 100)
        
        # 火山方舟配置
        volc_cfg = providers_config.get('volcengine', {})
        self.volcengine_enabled = volc_cfg.get('enabled', True)
        self.volcengine_api_key = volc_cfg.get('api_key', '') or os.environ.get("VOLCENGINE_API_KEY", "")
        self.volcengine_api_secret = volc_cfg.get('api_secret', '') or os.environ.get("VOLCENGINE_API_SECRET", "")
        self.volcengine_api_url = volc_cfg.get('api_url', 'https://ark.cn-beijing.volces.com/api/v3/images/generations')
        self.volcengine_model = volc_cfg.get('model', 'doubao-image-alpha')
        self.volcengine_size = volc_cfg.get('size', '1024x1024')
        self.volcengine_style = volc_cfg.get('style', 'realistic')
        self.volcengine_num_images = volc_cfg.get('num_images', 1)
        self.volcengine_monthly_limit = volc_cfg.get('monthly_limit', 100)
        
        # 文心一格配置
        baidu_cfg = providers_config.get('baidu-yige', {})
        self.baidu_enabled = baidu_cfg.get('enabled', True)
        self.baidu_api_key = baidu_cfg.get('api_key', '') or os.environ.get("BAIDU_API_KEY", "")
        self.baidu_secret_key = baidu_cfg.get('secret_key', '') or os.environ.get("BAIDU_SECRET_KEY", "")
        self.baidu_api_url = baidu_cfg.get('api_url', 'https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/text2image/sd_xl')
        self.baidu_size = baidu_cfg.get('size', '1024,1024')
        self.baidu_style = baidu_cfg.get('style', 'Base')
        self.baidu_monthly_limit = baidu_cfg.get('monthly_limit', 100)
        
        # DALL-E 3 配置
        dalle_cfg = providers_config.get('dall-e-3', {})
        self.dalle_enabled = dalle_cfg.get('enabled', True)
        self.dalle_api_key = dalle_cfg.get('api_key', '') or os.environ.get("DALL_E_API_KEY", "")
        self.dalle_model = dalle_cfg.get('model', 'dall-e-3')
        self.dalle_size = dalle_cfg.get('size', '1024x1024')
        self.dalle_quality = dalle_cfg.get('quality', 'standard')
        self.dalle_api_url = dalle_cfg.get('api_url', 'https://api.openai.com/v1/images/generations')
        self.dalle_monthly_limit = dalle_cfg.get('monthly_limit')
        
        # 占位图配置（始终启用）
        placeholder_cfg = providers_config.get('placeholder', {})
        self.placeholder_enabled = placeholder_cfg.get('enabled', True)
        self.placeholder_monthly_limit = placeholder_cfg.get('monthly_limit')
        
        # 免费额度重置配置
        free_quota = self.config.get('free_quota', {})
        self.reset_day = free_quota.get('reset_day', 1)
        
        # 初始化使用计数器
        from usage_counter import get_counter
        self.counter = get_counter()
        
        # 设置计数器限额（从配置读取）
        self.counter.data["providers"]["unsplash"]["limit"] = self.unsplash_monthly_limit
        self.counter.data["providers"]["tongyi-wanxiang"]["limit"] = self.tongyi_monthly_limit
        self.counter.data["providers"]["baidu-yige"]["limit"] = self.baidu_monthly_limit
        self.counter.data["providers"]["dall-e-3"]["limit"] = self.dalle_monthly_limit
        self.counter.data["providers"]["placeholder"]["limit"] = self.placeholder_monthly_limit
        
        self.output_dir = Path("generated_images")
        self.output_dir.mkdir(exist_ok=True)
        
        logger.info(f"配图策略初始化完成 - 优先级：{self.provider_priority}")
        logger.info(f"图片源状态：Unsplash={self.unsplash_enabled}, 通义={self.tongyi_enabled}, 百度={self.baidu_enabled}, DALL-E={self.dalle_enabled}")
    
    def extract_keywords(self, content: str, max_keywords: int = 20, context: str = "") -> List[str]:
        """
        从文章内容提取关键词（至少 20 个）
        
        Args:
            content: 文章内容
            max_keywords: 最大关键词数量（默认至少 20 个）
            context: 上下文（段落或章节标题）
            
        Returns:
            关键词列表
        """
        # 从文章内容中提取关键场景和元素（至少 20 个）
        return self._extract_keywords_from_content(content, max(20, max_keywords), context)
    
    def _extract_keywords_with_llm(self, content: str, context: str, max_keywords: int) -> List[str]:
        """
        使用 LLM 提取关键词和场景描述
        
        Args:
            content: 文章内容
            context: 上下文
            max_keywords: 最大关键词数量
            
        Returns:
            关键词列表
        """
        # 截取前 1000 字作为分析样本
        sample = content[:1000] if len(content) > 1000 else content
        
        # 构建提示词
        prompt = f"""
请从以下文章内容中提取 {max_keywords} 个最适合用于配图的关键词或短语。

要求：
1. 提取具体的场景、物体或概念（如"服务器机房"、"数据可视化"、"网络安全"）
2. 避免抽象词汇（如"科技"、"未来"）
3. 优先选择可以视觉化的内容
4. 用英文输出，逗号分隔

文章内容：
{sample}

关键词：
"""
        
        # 调用 DALL-E API（复用连接）
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 100,
            "temperature": 0.7
        }
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            result = response.json()
            
            if "choices" in result and len(result["choices"]) > 0:
                keywords_text = result["choices"][0]["message"]["content"]
                keywords = [kw.strip() for kw in keywords_text.split(',')]
                logger.info(f"LLM 提取关键词：{keywords}")
                return keywords[:max_keywords]
        except Exception as e:
            logger.warning(f"LLM 调用失败：{e}")
        
        return []
    
    def _extract_keywords_from_content(self, content: str, max_keywords: int = 20, context: str = "") -> List[str]:
        """
        从文章内容提取关键词（至少 20 个）
        
        Args:
            content: 文章内容
            max_keywords: 最大关键词数量（默认至少 20 个）
            context: 上下文（段落或章节标题）
            
        Returns:
            关键词列表（至少 20 个）
        """
        import re
        
        # 确保至少提取 20 个关键词
        max_keywords = max(20, max_keywords)
        
        # 1. 提取文章中的关键名词和场景
        keywords = []
        
        # 2. 从标题/章节名提取（如果有）
        if context:
            keywords.append(context)
        
        # 3. 提取文章中的关键场景词（根据内容类型）
        content_lower = content.lower()
        
        # 检测文章类型并提取相应关键词
        if any(word in content_lower for word in ['科技', '技术', 'AI', '人工智能', '数据']):
            # 科技类文章 - 扩展词库
            tech_keywords = {
                '服务器': 'server room, data center',
                '网络': 'network topology, connected nodes',
                '安全': 'cybersecurity shield, digital protection',
                '数据': 'data visualization, digital information flow',
                'AI': 'artificial intelligence, neural network',
                '算法': 'algorithm flowchart, code visualization',
                '云': 'cloud computing, distributed systems',
                '系统': 'computer system, software interface',
                '技术': 'modern technology, innovation',
                '智能': 'smart technology, automation',
                '数字': 'digital transformation, technology',
                '信息': 'information technology, data',
                '软件': 'software development, coding',
                '硬件': 'computer hardware, equipment',
                '互联网': 'internet, web technology',
                '移动': 'mobile technology, smartphone',
                '设备': 'electronic devices, gadgets',
                '平台': 'digital platform, ecosystem',
                '应用': 'mobile app, application',
                '编程': 'programming, software development',
                '代码': 'source code, programming',
                '数据库': 'database, data storage',
                '接口': 'API, interface design',
                '前端': 'frontend design, UI',
                '后端': 'backend system, server',
            }
            for cn, en in tech_keywords.items():
                if cn.lower() in content_lower and en not in keywords:
                    keywords.append(en)
        
        elif any(word in content_lower for word in ['商业', '企业', '市场', '经济']):
            # 商业类文章 - 扩展词库
            business_keywords = {
                '会议': 'business meeting, conference room',
                '办公': 'modern office, workspace',
                '团队': 'teamwork, collaboration',
                '报告': 'business report, analytics dashboard',
                '分析': 'data analysis, charts and graphs',
                '金融': 'financial district, trading floor',
                '市场': 'market analysis, business',
                '经济': 'economic growth, finance',
                '企业': 'corporate business, company',
                '管理': 'business management, leadership',
                '战略': 'business strategy, planning',
                '营销': 'marketing, advertising',
                '销售': 'sales, business development',
                '客户': 'customer service, client',
                '产品': 'product design, innovation',
                '服务': 'business service, professional',
                '投资': 'investment, finance',
                '财务': 'financial report, accounting',
                '人力资源': 'HR, human resources',
                '培训': 'training, professional development',
            }
            for cn, en in business_keywords.items():
                if cn.lower() in content_lower and en not in keywords:
                    keywords.append(en)
        
        # 4. 从文章中提取高频词（确保达到 20 个关键词）
        words = re.findall(r'[\u4e00-\u9fa5]{2,}', content)
        word_freq = {}
        for word in words:
            if len(word) >= 2 and word not in ['这个', '那个', '我们', '他们', '可以', '应该', '可能', '一个', '一些', '很多']:
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # 取频率最高的词，确保达到 20 个
        top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        for word, freq in top_words:
            if len(keywords) >= max_keywords:
                break
            # 将中文词转换为英文描述
            english_desc = f"{word}, professional photography, high quality, detailed"
            if english_desc not in keywords:
                keywords.append(english_desc)
        
        # 5. 确保至少 20 个关键词
        while len(keywords) < 20:
            generic_keywords = [
                "professional photography, high quality",
                "modern design, clean background",
                "detailed image, sharp focus",
                "business style, professional",
                "high resolution, 8k quality"
            ]
            for kw in generic_keywords:
                if len(keywords) >= 20:
                    break
                if kw not in keywords:
                    keywords.append(kw)
        
        logger.info(f"从文章内容提取{len(keywords)}个关键词：{keywords[:5]}...")
        return keywords[:max_keywords]
    
    def _extract_keywords_basic(self, content: str, context: str, max_keywords: int) -> List[str]:
        """
        基于规则和词频提取关键词（备用方案）
        
        Args:
            content: 文章内容
            context: 上下文
            max_keywords: 最大关键词数量
            
        Returns:
            关键词列表
        """
        import re
        
        # 更详细的场景词库
        scene_keywords = {
            # 科技/数据
            "数据": "data visualization, digital information flow",
            "网络": "network topology, connected nodes",
            "安全": "cybersecurity shield, digital protection",
            "服务器": "server room, data center",
            "云计算": "cloud computing, distributed systems",
            "AI": "artificial intelligence, neural network",
            "算法": "algorithm flowchart, code visualization",
            
            # 办公/商业
            "办公": "modern office, workspace",
            "会议": "business meeting, conference room",
            "团队": "teamwork, collaboration",
            "报告": "business report, analytics dashboard",
            "分析": "data analysis, charts and graphs",
            
            # 行业场景
            "金融": "financial district, trading floor",
            "医疗": "hospital, medical technology",
            "教育": "classroom, online learning",
            "电商": "e-commerce, online shopping",
            "物流": "logistics, warehouse automation",
            
            # 抽象概念
            "隐私": "privacy protection, data encryption",
            "泄露": "data breach warning, security alert",
            "黑客": "hacker silhouette, cyber attack",
            "监控": "surveillance, security monitoring",
            "权限": "access control, authentication"
        }
        
        keywords = []
        content_lower = content.lower()
        
        # 优先使用上下文（段落主题）
        if context:
            for kw, desc in scene_keywords.items():
                if kw.lower() in context.lower():
                    keywords.append(desc)
        
        # 再从全文提取
        for kw, desc in scene_keywords.items():
            if kw.lower() in content_lower and desc not in keywords:
                keywords.append(desc)
        
        # 如果关键词不足，添加通用科技场景
        if len(keywords) < max_keywords:
            default_scenes = [
                "modern technology background, clean and professional",
                "abstract digital pattern, blue gradient",
                "futuristic interface, data visualization"
            ]
            keywords.extend(default_scenes)
        
        return keywords[:max_keywords]
    
    def build_prompt(self, keywords: List[str], style: str = "photorealistic", context: str = "") -> str:
        """
        构建专业的 AI 绘图提示词（使用所有关键词）
        
        Args:
            keywords: 关键词列表（至少 20 个）
            style: 风格 (tech, abstract, minimal, photorealistic)
            context: 上下文描述
            
        Returns:
            英文提示词（包含所有关键词）
        """
        # 风格定义
        style_prompts = {
            "tech": "futuristic technology background, clean and modern, professional photography, studio lighting",
            "abstract": "abstract digital art, flowing data streams, artistic composition, dramatic lighting",
            "minimal": "minimalist design, clean lines, solid colors, simple composition",
            "photorealistic": "photorealistic, high detail, 8k resolution, professional photography, depth of field",
            "business": "business and technology, corporate environment, professional setting, modern office"
        }
        
        # 质量增强词
        quality_enhancers = [
            "ultra high quality",
            "extremely detailed",
            "sharp focus",
            "professional composition",
            "balanced lighting",
            "8k resolution",
            "masterpiece"
        ]
        
        # 使用所有关键词（至少 20 个）
        if keywords and len(keywords) >= 20:
            # 将所有关键词组合成详细的提示词
            base_prompt = ", ".join(keywords)
            logger.info(f"使用{len(keywords)}个关键词构建提示词")
        else:
            base_prompt = ", ".join(keywords) if keywords else style_prompts.get(style, style_prompts['tech'])
            logger.warning(f"关键词数量不足{len(keywords)}个，提示词可能不够详细")
        
        # 添加风格描述
        style_desc = style_prompts.get(style, style_prompts['photorealistic'])
        
        # 添加上下文（如果有）
        context_part = ""
        if context:
            context_part = f", {context}"
        
        # 组合完整提示词（包含所有关键词）
        full_prompt = f"{base_prompt}{context_part}, {style_desc}, {', '.join(quality_enhancers)}"
        
        # 添加负面提示
        negative = "no text, no words, no letters, no watermark, no signature, no blur, no distortion, no noise"
        
        logger.info(f"提示词长度：{len(full_prompt)}字符")
        return f"{full_prompt}, {negative}"
    
    def generate_dalle3(self, prompt: str, size: Optional[str] = None) -> Optional[bytes]:
        """
        使用 DALL-E 3 生成图片
        
        Args:
            prompt: 提示词
            size: 图片尺寸（从 config 读取默认值）
            
        Returns:
            图片二进制数据
        """
        if not self.dalle_api_key:
            logger.error("DALL-E API key 未配置")
            return None
        
        url = self.dalle_api_url
        headers = {
            "Authorization": f"Bearer {self.dalle_api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.dalle_model,
            "prompt": prompt,
            "n": 1,
            "size": size or self.dalle_size,
            "quality": self.dalle_quality,
            "response_format": "b64_json"
        }
        
        logger.info(f"调用 DALL-E 3 生成图片：{prompt[:50]}...")
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=60)
            response.raise_for_status()
            result = response.json()
            
            if "data" in result and len(result["data"]) > 0:
                import base64
                image_data = base64.b64decode(result["data"][0]["b64_json"])
                logger.info("DALL-E 3 图片生成成功")
                return image_data
            else:
                logger.error(f"DALL-E 3 返回异常：{result}")
                return None
                
        except Exception as e:
            logger.error(f"DALL-E 3 调用失败：{e}")
            return None
    
    def generate_tongyi_wanxiang(self, prompt: str, size: Optional[str] = None) -> Optional[bytes]:
        """
        使用通义万相生成图片（阿里云 DashScope）
        
        Args:
            prompt: 提示词
            size: 图片尺寸（从 config 读取默认值）
            
        Returns:
            图片二进制数据
            
        文档：https://help.aliyun.com/zh/dashscope/developer-reference/image-generation-api
        """
        if not self.tongyi_api_key:
            logger.error("通义万相 API key 未配置")
            return None
        
        url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/image-generation/generation"
        headers = {
            "Authorization": f"Bearer {self.tongyi_api_key}",
            "Content-Type": "application/json"
        }
        
        size = size or self.tongyi_size
        prompt_text = f"{prompt}"
        
        data = {
            "model": "wanx-v1",
            "input": {
                "prompt": prompt_text
            },
            "parameters": {
                "size": size,
                "n": 1
            }
        }
        
        logger.info(f"调用通义万相生成图片：{prompt_text[:50]}...")
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=60)
            response.raise_for_status()
            result = response.json()
            
            if "output" in result and "results" in result["output"]:
                img_url = result["output"]["results"][0]["url"]
                logger.info(f"图片 URL: {img_url}")
                
                img_response = requests.get(img_url, timeout=30)
                img_response.raise_for_status()
                logger.info("通义万相图片生成成功")
                return img_response.content
            else:
                logger.error(f"通义万相返回异常：{result}")
                return None
                
        except Exception as e:
            logger.error(f"通义万相调用失败：{e}")
            return None
    
    def generate_bailian(self, prompt: str, size: Optional[str] = None) -> Optional[bytes]:
        """
        使用阿里百炼 qwen-image-plus 生成图片
        
        Args:
            prompt: 提示词
            size: 图片尺寸
            
        Returns:
            图片二进制数据
            
        文档：https://help.aliyun.com/zh/bailian
        """
        if not self.bailian_api_key:
            logger.error("阿里百炼 API key 未配置")
            return None
        
        url = self.bailian_api_url
        headers = {
            "Authorization": f"Bearer {self.bailian_api_key}",
            "Content-Type": "application/json"
        }
        
        size = size or self.bailian_size
        
        # qwen-image-plus 需要使用 messages 格式
        data = {
            "model": self.bailian_model,
            "input": {
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {"text": f"生成一张图片：{prompt}"}
                        ]
                    }
                ]
            },
            "parameters": {
                "size": size
            }
        }
        
        logger.info(f"调用阿里百炼生成图片：{prompt[:50]}...")
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=60)
            response.raise_for_status()
            result = response.json()
            
            # qwen-image-plus 返回格式
            if "output" in result and "choices" in result["output"]:
                message = result["output"]["choices"][0]["message"]
                content = message.get("content", [])
                
                if content and len(content) > 0:
                    img_url = content[0].get("image", "")
                    
                    if img_url:
                        logger.info(f"图片 URL: {img_url[:100]}...")
                        
                        img_response = requests.get(img_url, timeout=30)
                        img_response.raise_for_status()
                        logger.info("阿里百炼图片生成成功")
                        return img_response.content
                    else:
                        logger.error(f"阿里百炼返回中没有图片 URL: {result}")
                        return None
                else:
                    logger.error(f"阿里百炼返回格式异常：{result}")
                    return None
            else:
                logger.error(f"阿里百炼返回异常：{result}")
                return None
                
        except Exception as e:
            logger.error(f"阿里百炼调用失败：{e}")
            return None
    
    def generate_volcengine(self, prompt: str, size: Optional[str] = None, target_size: Optional[tuple] = None) -> Optional[bytes]:
        """
        使用火山方舟生成图片
        
        Args:
            prompt: 提示词
            size: 图片尺寸（字符串格式，如 "2048x2048"）
            target_size: 目标尺寸（元组格式，如 (1080, 1080)，用于后续缩放）
            
        Returns:
            图片二进制数据
            
        文档：https://www.volcengine.com/docs/82379
        """
        if not self.volcengine_api_key or not self.volcengine_api_secret:
            logger.error("火山方舟 API key 未配置")
            return None
        
        url = self.volcengine_api_url
        headers = {
            "Authorization": f"Bearer {self.volcengine_api_key}",
            "Content-Type": "application/json"
        }
        
        # 确定 API 请求尺寸（火山方舟要求最小 3686400 像素，约 1920x1920）
        api_size = size or self.volcengine_size
        
        # 检查尺寸是否满足火山方舟要求
        if api_size:
            try:
                w, h = map(int, api_size.lower().split('x'))
                if w * h < 3686400:
                    logger.warning(f"火山方舟要求最小 3686400 像素，{api_size} 不满足，使用 2048x2048")
                    api_size = "2048x2048"
            except:
                pass
        
        logger.info(f"火山方舟 API 请求尺寸：{api_size}")
        if target_size:
            logger.info(f"生成后将缩放到：{target_size[0]}x{target_size[1]}")
        
        # 火山方舟请求格式
        data = {
            "model": self.volcengine_model,
            "prompt": prompt,
            "size": size,
            "num_images": self.volcengine_num_images,
            "style": self.volcengine_style
        }
        
        logger.info(f"调用火山方舟生成图片：{prompt[:50]}...")
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=60)
            response.raise_for_status()
            result = response.json()
            
            # 火山方舟返回格式
            if "data" in result:
                # 新格式：data 是数组，每个元素有 url 字段
                if isinstance(result["data"], list) and len(result["data"]) > 0:
                    img_url = result["data"][0].get("url", "")
                # 旧格式：data.images 数组
                elif "images" in result["data"]:
                    img_url = result["data"]["images"][0]["url"]
                else:
                    logger.error(f"火山方舟返回格式异常：{result}")
                    return None
                
                if img_url:
                    logger.info(f"图片 URL: {img_url[:100]}...")
                    
                    img_response = requests.get(img_url, timeout=30)
                    img_response.raise_for_status()
                    
                    # 如果需要缩放
                    if target_size:
                        from PIL import Image
                        import io
                        
                        img = Image.open(io.BytesIO(img_response.content))
                        img = img.resize((target_size[0], target_size[1]), Image.Resampling.LANCZOS)
                        
                        output = io.BytesIO()
                        img.save(output, format='JPEG', quality=90)
                        output.seek(0)
                        
                        logger.info(f"图片已缩放到 {target_size[0]}x{target_size[1]}")
                        return output.getvalue()
                    else:
                        logger.info("火山方舟图片生成成功")
                        return img_response.content
                else:
                    logger.error(f"火山方舟返回中没有图片 URL: {result}")
                    return None
            else:
                logger.error(f"火山方舟返回异常：{result}")
                return None
                
        except Exception as e:
            logger.error(f"火山方舟调用失败：{e}")
            return None
    
    def generate_baidu_yige(self, prompt: str, size: Optional[str] = None) -> Optional[bytes]:
        """
        使用文心一格生成图片（百度）
        
        Args:
            prompt: 提示词
            size: 图片尺寸（从 config 读取默认值）
            
        Returns:
            图片二进制数据
            
        文档：https://cloud.baidu.com/doc/WENXINWORKSHOP/s/3l0q8v17t
        """
        if not self.baidu_api_key or not self.baidu_secret_key:
            logger.error("文心一格 API key 未配置")
            return None
        
        # 第一步：获取 access_token
        token_url = "https://aip.baidubce.com/oauth/2.0/token"
        token_params = {
            "grant_type": "client_credentials",
            "client_id": self.baidu_api_key,
            "client_secret": self.baidu_secret_key
        }
        
        try:
            token_response = requests.post(token_url, params=token_params, timeout=30)
            token_response.raise_for_status()
            token_result = token_response.json()
            access_token = token_result.get("access_token")
            
            if not access_token:
                logger.error("文心一格 access_token 获取失败")
                return None
            
            # 第二步：调用文心一格 API
            url = f"{self.baidu_api_url}?access_token={access_token}"
            headers = {
                "Content-Type": "application/json"
            }
            
            size = size or self.baidu_size
            style = self.baidu_style
            
            # 文心一格支持中文提示词
            prompt_text = f"{prompt}, 高质量，精美，专业"
            
            data = {
                "prompt": prompt_text,
                "size": size,
                "style": style,
                "num": 1
            }
            
            logger.info(f"调用文心一格生成图片：{prompt_text[:50]}...")
            
            response = requests.post(url, headers=headers, json=data, timeout=60)
            response.raise_for_status()
            result = response.json()
            
            # 文心一格返回格式
            if "data" in result and "img_urls" in result["data"]:
                img_url = result["data"]["img_urls"][0]
                
                # 下载图片
                img_response = requests.get(img_url, timeout=30)
                img_response.raise_for_status()
                logger.info("文心一格图片生成成功")
                return img_response.content
            else:
                logger.error(f"文心一格返回异常：{result}")
                return None
                
        except Exception as e:
            logger.error(f"文心一格调用失败：{e}")
            return None
    
    def generate_placeholder(self, keywords: List[str], width: int = 900, height: int = 383) -> bytes:
        """
        生成占位图（当 AI 绘图不可用时）
        
        Args:
            keywords: 关键词（用于生成颜色）
            width: 宽度
            height: 高度
            
        Returns:
            图片二进制数据
        """
        # 根据关键词生成渐变色
        colors = {
            "AI": (0, 123, 255),
            "科技": (0, 188, 212),
            "未来": (155, 89, 182),
            "数据": (46, 204, 113),
            "默认": (52, 152, 219)
        }
        
        # 选择主色
        main_color = colors.get("默认")
        for kw in keywords:
            if kw in colors:
                main_color = colors[kw]
                break
        
        # 创建渐变图片
        img = Image.new('RGB', (width, height))
        pixels = img.load()
        
        for y in range(height):
            # 垂直渐变
            ratio = y / height
            r = int(main_color[0] * (1 - ratio) + 255 * ratio)
            g = int(main_color[1] * (1 - ratio) + 255 * ratio)
            b = int(main_color[2] * (1 - ratio) + 255 * ratio)
            
            for x in range(width):
                pixels[x, y] = (r, g, b)
        
        # 保存为 JPEG
        buffer = io.BytesIO()
        img.save(buffer, format='JPEG', quality=85)
        return buffer.getvalue()
    
    def search_unsplash(self, keywords: List[str], width: int = 900, height: int = 383) -> Optional[bytes]:
        """
        从 Unsplash 搜索并下载图片
        
        Args:
            keywords: 搜索关键词
            width: 图片宽度
            height: 图片高度
            
        Returns:
            图片二进制数据
        """
        # Unsplash API 需要 Access Key
        if not self.unsplash_access_key:
            logger.warning("Unsplash Access Key 未配置，跳过图库搜索")
            return None
        
        # 构建搜索查询
        query = "+".join(keywords[:3]) if keywords else "technology"
        url = f"https://api.unsplash.com/search/photos"
        params = {
            "query": query,
            "per_page": self.unsplash_per_page,
            "orientation": self.unsplash_orientation,
            "content_filter": "high"
        }
        headers = {
            "Authorization": f"Client-ID {self.unsplash_access_key}"
        }
        
        try:
            logger.info(f"搜索 Unsplash 图库：{query}")
            response = requests.get(url, params=params, headers=headers, timeout=30)
            response.raise_for_status()
            result = response.json()
            
            if "results" in result and len(result["results"]) > 0:
                # 选择第一张图片
                photo = result["results"][0]
                photo_url = photo["urls"]["regular"]
                
                # 下载图片
                logger.info(f"下载 Unsplash 图片：{photo_url}")
                img_response = requests.get(photo_url, timeout=30)
                img_response.raise_for_status()
                
                # 调整尺寸
                with Image.open(io.BytesIO(img_response.content)) as img:
                    img = img.convert('RGB')
                    img = img.resize((width, height), Image.Resampling.LANCZOS)
                    
                    buffer = io.BytesIO()
                    img.save(buffer, format='JPEG', quality=85)
                    logger.info("Unsplash 图片下载并调整尺寸完成")
                    return buffer.getvalue()
            
            logger.warning("Unsplash 未找到匹配图片")
            return None
            
        except Exception as e:
            logger.error(f"Unsplash 搜索失败：{e}")
            return None
    
    def generate_cover(self, content: str, style: str = "photorealistic", 
                       use_ai: bool = True, fixed_timestamp: Optional[int] = None) -> Path:
        """
        生成封面图（根据文章内容生成，使用 1:1 正方形避免微信裁剪变形）
        
        Args:
            content: 文章内容
            style: 风格（默认 photorealistic 更真实）
            use_ai: 是否使用 AI 生成
            fixed_timestamp: 固定时间戳（避免时序竞争）
            
        Returns:
            生成的图片路径
        """
        from PIL import Image
        
        # 从文章内容提取关键词（20+ 个）
        cover_keywords = self.extract_keywords(content, max_keywords=20)
        logger.info(f"封面图关键词（从文章内容提取，{len(cover_keywords)}个）：{cover_keywords[:5]}...")
        
        # 构建提示词（使用所有关键词）
        prompt = self.build_prompt(cover_keywords, style)
        logger.info(f"封面图提示词长度：{len(prompt)}字符")
        
        # 使用智能策略生成图片（使用 1:1 正方形，避免微信裁剪变形）
        # 微信会将封面图裁剪为 1:1 或 4:3，所以我们直接生成 1:1
        image_data = self.generate_with_strategy(content, prompt, cover_keywords, size="cover")
        
        if not image_data:
            logger.error("封面图生成失败，使用占位图")
            # 生成占位图
            image_data = self.generate_placeholder(cover_keywords, 1080, 1080)
        
        # 保存封面图
        timestamp = fixed_timestamp if fixed_timestamp is not None else int(time.time())
        image_path = self.output_dir / f"cover_{timestamp}.jpg"
        
        with Image.open(io.BytesIO(image_data)) as img:
            img = img.convert('RGB')
            # 调整为 1:1 正方形（1080x1080），避免微信裁剪变形
            img = img.resize((1080, 1080), Image.Resampling.LANCZOS)
            img.save(image_path, 'JPEG', quality=85)
        
        logger.info(f"封面图已保存：{image_path}（1080x1080，1:1）")
        logger.info(f"文件大小：{image_path.stat().st_size / 1024:.1f} KB")
        
        # 打印使用统计
        logger.info(self.counter.get_summary())
        
        return image_path
    
    def generate_image_with_ai(self, prompt: str, output_path: str, 
                                width: int = 800, height: int = 600,
                                keywords: List[str] = None) -> Path:
        """
        使用 AI 生成配图（正文插图）
        
        Args:
            prompt: 绘图提示词
            output_path: 输出路径
            width: 图片宽度
            height: 图片高度
            keywords: 关键词列表（用于 Unsplash 搜索）
            
        Returns:
            生成的图片路径
        """
        image_data = None
        
        # 优先级 1：尝试 Unsplash 图库（真实照片）
        if keywords:
            image_data = self.search_unsplash(keywords, width, height)
        
        # 优先级 2：AI 生成
        if not image_data and self.api_key:
            image_data = self.generate_dalle3(prompt, size="1024x1024")
        
        # 优先级 3：占位图
        if not image_data:
            logger.warning("AI 绘图失败，使用占位图替代")
            # 从提示词提取简单关键词
            kws = [w.strip() for w in prompt.split(',')[:3]] if prompt else []
            image_data = self.generate_placeholder(kws, width, height)
        
        # 保存并调整尺寸
        with Image.open(io.BytesIO(image_data)) as img:
            img = img.convert('RGB')
            img = img.resize((width, height), Image.Resampling.LANCZOS)
            
            # 确保目录存在
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            img.save(output_path, 'JPEG', quality=85)
        
        logger.info(f"配图已保存：{output_path}")
        return Path(output_path)
    
    def get_best_provider(self) -> str:
        """
        根据优先级和额度选择最佳图片源
        
        Returns:
            最佳服务提供商名称
        """
        logger.info("开始选择最佳图片源...")
        
        for provider in self.provider_priority:
            # 检查是否配置了 API Key
            if not self._is_provider_configured(provider):
                logger.debug(f"{provider} 未配置 API Key，跳过")
                continue
            
            # 检查额度是否充足
            if not self.counter.should_use_provider(provider):
                usage = self.counter.get_usage(provider)
                if not usage.get("unlimited", False):
                    logger.warning(f"{provider} 额度不足（已用{usage['count']}/{usage['limit']}），跳过")
                    continue
            
            # 检查服务是否可用（简单 ping）
            if not self._is_provider_available(provider):
                logger.warning(f"{provider} 服务不可用，跳过")
                continue
            
            logger.info(f"选择图片源：{provider}")
            return provider
        
        # 所有服务都不可用，返回占位图
        logger.warning("所有图片源都不可用，使用占位图")
        return "placeholder"
    
    def _is_provider_configured(self, provider: str) -> bool:
        """
        检查服务提供商是否已配置并启用
        
        Args:
            provider: 服务提供商名称
            
        Returns:
            True 如果已配置并启用
        """
        # 首先检查开关状态
        if not self._is_provider_enabled(provider):
            logger.debug(f"{provider} 已禁用（开关=OFF）")
            return False
        
        # 然后检查 API Key 配置
        if provider == "unsplash":
            return bool(self.unsplash_access_key and self.unsplash_access_key != "your-unsplash-access-key-here")
        elif provider == "tongyi-wanxiang":
            return bool(self.tongyi_api_key and self.tongyi_api_key != "sk-your-dashscope-api-key-here")
        elif provider == "bailian":
            return bool(self.bailian_api_key and self.bailian_api_key != "sk-your-bailian-api-key-here")
        elif provider == "volcengine":
            return bool(self.volcengine_api_key and self.volcengine_api_key != "your-volcengine-api-key-here")
        elif provider == "baidu-yige":
            return bool(self.baidu_api_key and self.baidu_secret_key and 
                       self.baidu_api_key != "your-baidu-api-key-here")
        elif provider == "dall-e-3":
            return bool(self.dalle_api_key and self.dalle_api_key != "sk-your-dalle-api-key-here")
        elif provider == "placeholder":
            return True  # 占位图总是可用
        
        return False
    
    def _is_provider_enabled(self, provider: str) -> bool:
        """
        检查服务提供商开关状态
        
        Args:
            provider: 服务提供商名称
            
        Returns:
            True 如果开关为 ON
        """
        if provider == "unsplash":
            return self.unsplash_enabled
        elif provider == "tongyi-wanxiang":
            return self.tongyi_enabled
        elif provider == "bailian":
            return self.bailian_enabled
        elif provider == "volcengine":
            return self.volcengine_enabled
        elif provider == "baidu-yige":
            return self.baidu_enabled
        elif provider == "dall-e-3":
            return self.dalle_enabled
        elif provider == "placeholder":
            return self.placeholder_enabled
        
        return False
    
    def _is_provider_available(self, provider: str) -> bool:
        """
        检查服务提供商是否可用（简单检查）
        
        Args:
            provider: 服务提供商名称
            
        Returns:
            True 如果可用
        """
        # 这里可以做简单的健康检查
        # 目前只检查是否配置，实际调用时再检查连通性
        return self._is_provider_configured(provider)
    
    def generate_with_strategy(self, content: str, prompt: str, 
                               keywords: List[str], size: str = "cover") -> Optional[bytes]:
        """
        使用智能策略生成图片
        
        Args:
            content: 文章内容（用于关键词提取）
            prompt: 绘图提示词
            keywords: 关键词列表
            size: 图片尺寸类型（cover 或 body）
            
        Returns:
            图片二进制数据
        """
        # 选择最佳图片源
        best_provider = self.get_best_provider()
        logger.info(f"使用图片源：{best_provider}")
        
        image_data = None
        retry_count = 0
        
        # 尝试生成图片
        while retry_count < self.max_retries:
            try:
                if best_provider == "unsplash":
                    width, height = (900, 383) if size == "cover" else (800, 600)
                    image_data = self.search_unsplash(keywords, width, height)
                
                elif best_provider == "tongyi-wanxiang":
                    image_data = self.generate_tongyi_wanxiang(prompt)
                
                elif best_provider == "bailian":
                    image_data = self.generate_bailian(prompt)
                
                elif best_provider == "volcengine":
                    # 封面图使用 1:1 正方形，火山方舟要求最小 3686400 像素（1920x1920）
                    # 生成 2048x2048，然后缩放到 1080x1080
                    if size == "cover":
                        logger.info("封面图：使用火山方舟生成 2048x2048，然后缩放到 1080x1080")
                        # 先生成 2048x2048（满足火山方舟最小尺寸要求）
                        image_data = self.generate_volcengine(prompt, size="2048x2048", target_size=(1080, 1080))
                    else:
                        logger.info(f"正文配图：使用默认尺寸 {self.volcengine_size}")
                        image_data = self.generate_volcengine(prompt, size=self.volcengine_size, target_size=None)
                
                elif best_provider == "baidu-yige":
                    image_data = self.generate_baidu_yige(prompt)
                
                elif best_provider == "dall-e-3":
                    image_data = self.generate_dalle3(prompt)
                
                elif best_provider == "placeholder":
                    width, height = (900, 383) if size == "cover" else (800, 600)
                    image_data = self.generate_placeholder(keywords, width, height)
                
                # 生成成功
                if image_data:
                    # 记录使用量
                    self.counter.increment(best_provider)
                    logger.info(f"{best_provider} 图片生成成功")
                    break
                
            except Exception as e:
                logger.warning(f"{best_provider} 生成失败（尝试 {retry_count + 1}/{self.max_retries}）: {e}")
                retry_count += 1
                
                # 自动切换到下一个可用服务
                if self.auto_switch:
                    old_provider = best_provider
                    best_provider = self.get_best_provider()
                    if best_provider == old_provider:
                        logger.warning(f"无法切换到其他服务，继续使用 {best_provider}")
                    else:
                        logger.info(f"自动切换：{old_provider} → {best_provider}")
        
        # 最终降级方案
        if not image_data:
            logger.warning("所有服务都失败，使用占位图")
            width, height = (900, 383) if size == "cover" else (800, 600)
            image_data = self.generate_placeholder(keywords, width, height)
            self.counter.increment("placeholder")
        
        return image_data


def test_generator():
    """测试图片生成"""
    generator = ImageGenerator()
    
    test_content = """
    我是一名 AI 助手，从诞生的那一刻起就开始学习成长。
    在科技的海洋中，我不断探索人工智能的边界。
    数据是我的养分，算法是我的思维。
    """
    
    print("🧪 测试图片生成")
    print("=" * 50)
    
    try:
        image_path = generator.generate_cover(test_content, use_ai=False)
        print(f"✅ 图片生成成功：{image_path}")
        print(f"   尺寸：900x383px")
    except Exception as e:
        print(f"❌ 图片生成失败：{e}")


if __name__ == "__main__":
    test_generator()
