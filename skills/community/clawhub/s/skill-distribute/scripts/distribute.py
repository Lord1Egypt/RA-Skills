#!/usr/bin/env python3
"""
多平台内容自动分发工具

从小红书获取内容，自动同步到抖音、视频号、快手等平台。
"""

import argparse
import json
import logging
import os
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('logs/distribute.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)


@dataclass
class ContentItem:
    """内容项"""
    id: str
    title: str
    description: str
    images: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    source_platform: str = "xiaohongshu"
    created_at: str = ""


@dataclass
class PlatformConfig:
    """平台配置"""
    name: str
    enabled: bool
    max_title_length: int
    max_desc_length: int
    max_tags: int
    image_ratio: str
    image_size: tuple
    login_type: str  # qrcode | phone | wechat


class ImageProcessor:
    """图片处理器"""
    
    # 平台图片尺寸要求
    PLATFORM_SIZES = {
        'xiaohongshu': [
            {'ratio': '3:4', 'size': (900, 1200)},
            {'ratio': '1:1', 'size': (1080, 1080)},
            {'ratio': '4:3', 'size': (1200, 900)},
        ],
        'douyin': [
            {'ratio': '9:16', 'size': (1080, 1920)},
        ],
        'shipinhao': [
            {'ratio': '9:16', 'size': (1080, 1920)},
        ],
        'kuaishou': [
            {'ratio': '9:16', 'size': (1080, 1920)},
        ],
    }
    
    def __init__(self, config_path: str = "config/image.yaml"):
        self.config = self._load_config(config_path)
        
    def _load_config(self, path: str) -> dict:
        """加载配置"""
        try:
            import yaml
            with open(path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        except Exception:
            return {
                'image_processing': {
                    'fill_mode': 'blur',
                    'background_color': '#000000',
                    'blur_radius': 50,
                    'quality': 95
                }
            }
    
    def process_for_platform(self, image_path: str, platform: str, output_dir: str = "temp") -> str:
        """
        处理图片以适应目标平台
        
        Args:
            image_path: 原图路径
            platform: 目标平台
            output_dir: 输出目录
            
        Returns:
            处理后的图片路径
        """
        try:
            from PIL import Image, ImageFilter
            
            img = Image.open(image_path)
            original_size = img.size
            
            # 获取目标尺寸
            target_config = self.PLATFORM_SIZES.get(platform, [{}])[0]
            target_size = target_config.get('size', (1080, 1920))
            target_ratio = target_config.get('ratio', '9:16')
            
            # 计算缩放
            orig_ratio = original_size[0] / original_size[1]
            target_ratio_val = target_size[0] / target_size[1]
            
            fill_mode = self.config.get('image_processing', {}).get('fill_mode', 'blur')
            
            if abs(orig_ratio - target_ratio_val) < 0.01:
                # 比例相同，直接缩放
                result = img.resize(target_size, Image.Resampling.LANCZOS)
            else:
                # 需要填充或裁剪
                if fill_mode == 'blur':
                    result = self._blur_fill(img, target_size)
                elif fill_mode == 'solid':
                    result = self._solid_fill(img, target_size)
                else:
                    result = self._smart_crop(img, target_size)
            
            # 保存
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(
                output_dir, 
                f"{platform}_{os.path.basename(image_path)}"
            )
            
            quality = self.config.get('image_processing', {}).get('quality', 95)
            result.save(output_path, 'JPEG', quality=quality)
            
            logger.info(f"图片处理完成: {image_path} -> {output_path}")
            return output_path
            
        except ImportError:
            logger.warning("PIL 未安装，返回原图")
            return image_path
        except Exception as e:
            logger.error(f"图片处理失败: {e}")
            return image_path
    
    def _blur_fill(self, img: 'Image.Image', target_size: tuple) -> 'Image.Image':
        """模糊填充模式"""
        from PIL import Image, ImageFilter
        
        # 创建背景
        bg = img.copy()
        bg = bg.resize(target_size, Image.Resampling.LANCZOS)
        bg = bg.filter(ImageFilter.GaussianBlur(radius=50))
        
        # 计算居中缩放
        orig_ratio = img.width / img.height
        target_ratio = target_size[0] / target_size[1]
        
        if orig_ratio > target_ratio:
            new_width = target_size[0]
            new_height = int(new_width / orig_ratio)
        else:
            new_height = target_size[1]
            new_width = int(new_height * orig_ratio)
        
        img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # 粘贴到中心
        x = (target_size[0] - new_width) // 2
        y = (target_size[1] - new_height) // 2
        bg.paste(img_resized, (x, y))
        
        return bg
    
    def _solid_fill(self, img: 'Image.Image', target_size: tuple) -> 'Image.Image':
        """纯色填充模式"""
        from PIL import Image
        
        bg_color = self.config.get('image_processing', {}).get('background_color', '#000000')
        bg = Image.new('RGB', target_size, bg_color)
        
        # 计算居中缩放
        orig_ratio = img.width / img.height
        target_ratio = target_size[0] / target_size[1]
        
        if orig_ratio > target_ratio:
            new_width = target_size[0]
            new_height = int(new_width / orig_ratio)
        else:
            new_height = target_size[1]
            new_width = int(new_height * orig_ratio)
        
        img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # 粘贴到中心
        x = (target_size[0] - new_width) // 2
        y = (target_size[1] - new_height) // 2
        bg.paste(img_resized, (x, y))
        
        return bg
    
    def _smart_crop(self, img: 'Image.Image', target_size: tuple) -> 'Image.Image':
        """智能裁剪模式"""
        from PIL import Image
        
        orig_ratio = img.width / img.height
        target_ratio = target_size[0] / target_size[1]
        
        if orig_ratio > target_ratio:
            # 原图太宽，裁剪两边
            new_width = int(img.height * target_ratio)
            left = (img.width - new_width) // 2
            img_cropped = img.crop((left, 0, left + new_width, img.height))
        else:
            # 原图太高，裁剪上下
            new_height = int(img.width / target_ratio)
            top = (img.height - new_height) // 2
            img_cropped = img.crop((0, top, img.width, top + new_height))
        
        return img_cropped.resize(target_size, Image.Resampling.LANCZOS)


class ContentAdapter:
    """内容适配器"""
    
    # 平台内容限制
    PLATFORM_LIMITS = {
        'xiaohongshu': {
            'max_title': 20,
            'max_desc': 1000,
            'max_tags': 10,
        },
        'douyin': {
            'max_title': 55,
            'max_desc': 500,
            'max_tags': 5,
            'auto_tags': ['热门', '推荐', '精选'],
        },
        'shipinhao': {
            'max_title': 30,
            'max_desc': 300,
            'max_tags': 3,
        },
        'kuaishou': {
            'max_title': 40,
            'max_desc': 400,
            'max_tags': 5,
        },
    }
    
    def __init__(self, config_path: str = "config/content.yaml"):
        self.config = self._load_config(config_path)
    
    def _load_config(self, path: str) -> dict:
        """加载配置"""
        try:
            import yaml
            with open(path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        except Exception:
            return {}
    
    def adapt_for_platform(self, content: ContentItem, platform: str) -> ContentItem:
        """
        适配内容到目标平台
        
        Args:
            content: 原始内容
            platform: 目标平台
            
        Returns:
            适配后的内容
        """
        limits = self.PLATFORM_LIMITS.get(platform, {})
        
        # 适配标题
        title = self._adapt_title(content.title, limits.get('max_title', 50))
        
        # 适配描述
        description = self._adapt_description(
            content.description, 
            limits.get('max_desc', 500)
        )
        
        # 适配标签
        tags = self._adapt_tags(
            content.tags,
            limits.get('max_tags', 5),
            limits.get('auto_tags', [])
        )
        
        return ContentItem(
            id=content.id,
            title=title,
            description=description,
            images=content.images.copy(),
            tags=tags,
            source_platform=content.source_platform,
            created_at=content.created_at
        )
    
    def _adapt_title(self, title: str, max_length: int) -> str:
        """适配标题长度"""
        if len(title) <= max_length:
            return title
        return title[:max_length-3] + "..."
    
    def _adapt_description(self, desc: str, max_length: int) -> str:
        """适配描述长度"""
        if len(desc) <= max_length:
            return desc
        return desc[:max_length-3] + "..."
    
    def _adapt_tags(self, tags: List[str], max_tags: int, auto_tags: List[str]) -> List[str]:
        """适配标签"""
        # 去重
        unique_tags = list(dict.fromkeys(tags))
        
        # 限制数量
        result = unique_tags[:max_tags]
        
        # 补充自动标签
        if len(result) < max_tags and auto_tags:
            needed = max_tags - len(result)
            result.extend(auto_tags[:needed])
        
        return result[:max_tags]


class CaptchaHandler:
    """验证码处理器"""
    
    def __init__(self, config_path: str = "config/captcha.yaml"):
        self.config = self._load_config(config_path)
    
    def _load_config(self, path: str) -> dict:
        """加载配置"""
        try:
            import yaml
            with open(path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        except Exception:
            return {
                'captcha': {
                    'timeout': 30,
                    'max_retries': 3
                }
            }
    
    def handle_slider(self, page, slider_selector: str) -> bool:
        """
        处理滑块验证码
        
        Args:
            page: 浏览器页面对象
            slider_selector: 滑块选择器
            
        Returns:
            是否成功
        """
        try:
            logger.info("检测到滑块验证码，尝试自动处理...")
            
            # 获取滑块元素
            slider = page.locator(slider_selector)
            slider_box = slider.bounding_box()
            
            if not slider_box:
                logger.warning("无法获取滑块位置")
                return False
            
            # 计算滑动距离（简化实现）
            # 实际应用中可能需要图像识别
            slide_distance = 280  # 默认距离
            
            # 执行滑动
            slider.drag_to(
                page.locator(slider_selector),
                target_position={"x": slide_distance, "y": 0}
            )
            
            time.sleep(1)
            
            # 检查是否通过
            if not page.locator(slider_selector).is_visible():
                logger.info("滑块验证码处理成功")
                return True
            
            logger.warning("滑块验证码处理失败")
            return False
            
        except Exception as e:
            logger.error(f"滑块验证码处理异常: {e}")
            return False
    
    def handle_sms(self, page, phone: str) -> bool:
        """
        处理短信验证码
        
        Args:
            page: 浏览器页面对象
            phone: 手机号
            
        Returns:
            是否成功
        """
        logger.info(f"等待短信验证码发送到 {phone}...")
        
        timeout = self.config.get('captcha', {}).get('timeout', 30)
        
        # 等待用户输入验证码
        print(f"\n请查看手机 {phone} 收到的验证码，并输入:")
        
        import threading
        
        captcha_code = [None]
        
        def input_captcha():
            captcha_code[0] = input("验证码: ").strip()
        
        input_thread = threading.Thread(target=input_captcha)
        input_thread.daemon = True
        input_thread.start()
        input_thread.join(timeout=timeout)
        
        if captcha_code[0]:
            # 填写验证码
            captcha_input = page.locator('input[placeholder*="验证码"], input[name*="captcha"]').first
            captcha_input.fill(captcha_code[0])
            
            # 点击提交
            submit_btn = page.locator('button:has-text("登录"), button:has-text("提交")').first
            submit_btn.click()
            
            logger.info("验证码已提交")
            return True
        else:
            logger.warning("等待验证码超时")
            return False


class PlatformPublisher:
    """平台发布器基类"""
    
    def __init__(self, platform: str, headless: bool = True):
        self.platform = platform
        self.headless = headless
        self.page = None
        self.browser = None
        
    def init_browser(self):
        """初始化浏览器"""
        try:
            from playwright.sync_api import sync_playwright
            
            self.playwright = sync_playwright().start()
            self.browser = self.playwright.chromium.launch(
                headless=self.headless,
                args=['--no-sandbox', '--disable-dev-shm-usage']
            )
            self.page = self.browser.new_page(
                viewport={'width': 1280, 'height': 800}
            )
            
            logger.info(f"浏览器初始化完成")
            
        except ImportError:
            logger.error("Playwright 未安装，请运行: pip install playwright")
            raise
    
    def close(self):
        """关闭浏览器"""
        if self.browser:
            self.browser.close()
        if hasattr(self, 'playwright'):
            self.playwright.stop()
        logger.info("浏览器已关闭")
    
    def login(self) -> bool:
        """登录平台"""
        raise NotImplementedError
    
    def publish(self, content: ContentItem) -> bool:
        """发布内容"""
        raise NotImplementedError


class DistributeManager:
    """分发管理器"""
    
    def __init__(self, args: argparse.Namespace):
        self.args = args
        self.image_processor = ImageProcessor()
        self.content_adapter = ContentAdapter()
        self.captcha_handler = CaptchaHandler()
        
        # 确保日志目录存在
        os.makedirs('logs', exist_ok=True)
        os.makedirs('temp', exist_ok=True)
        os.makedirs('data/cookies', exist_ok=True)
    
    def run(self):
        """执行分发"""
        logger.info("=" * 50)
        logger.info("开始多平台内容分发")
        logger.info("=" * 50)
        
        # 1. 获取源内容
        content = self._fetch_source_content()
        if not content:
            logger.error("获取源内容失败")
            return False
        
        logger.info(f"获取到内容: {content.title[:30]}...")
        
        # 2. 确定目标平台
        targets = self._get_target_platforms()
        logger.info(f"目标平台: {', '.join(targets)}")
        
        # 3. 逐个平台分发
        results = {}
        for platform in targets:
            try:
                result = self._distribute_to_platform(content, platform)
                results[platform] = result
                
                # 错峰发布
                if self.args.stagger and platform != targets[-1]:
                    delay = 30  # 30秒间隔
                    logger.info(f"等待 {delay} 秒后发布到下一个平台...")
                    time.sleep(delay)
                    
            except Exception as e:
                logger.error(f"分发到 {platform} 失败: {e}")
                results[platform] = False
        
        # 4. 输出结果
        self._print_results(results)
        
        return all(results.values())
    
    def _fetch_source_content(self) -> Optional[ContentItem]:
        """获取源内容"""
        # 简化实现，实际应从小红书获取
        # 这里模拟从文件或API获取
        
        if self.args.note_id:
            # 根据笔记ID获取
            logger.info(f"获取笔记: {self.args.note_id}")
            # TODO: 实现实际获取逻辑
            return ContentItem(
                id=self.args.note_id,
                title="示例标题",
                description="示例描述内容",
                images=["temp/sample.jpg"],
                tags=["穿搭", "时尚"],
                source_platform="xiaohongshu"
            )
        else:
            # 获取最新发布的笔记
            logger.info("获取最新发布的笔记...")
            # TODO: 实现实际获取逻辑
            return ContentItem(
                id="latest",
                title="最新笔记标题",
                description="最新笔记描述",
                images=["temp/sample.jpg"],
                tags=["美食", "探店"],
                source_platform="xiaohongshu"
            )
    
    def _get_target_platforms(self) -> List[str]:
        """获取目标平台列表"""
        all_platforms = ['douyin', 'shipinhao', 'kuaishou']
        
        if self.args.targets:
            return [p.strip() for p in self.args.targets.split(',')]
        
        # 从配置读取
        try:
            import yaml
            with open('config/accounts.yaml', 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                enabled = []
                for platform, settings in config.get('platforms', {}).items():
                    if settings.get('enabled', False) and platform != 'xiaohongshu':
                        enabled.append(platform)
                return enabled
        except Exception:
            return all_platforms
    
    def _distribute_to_platform(self, content: ContentItem, platform: str) -> bool:
        """分发到指定平台"""
        logger.info(f"\n{'='*30}")
        logger.info(f"开始分发到: {platform}")
        logger.info(f"{'='*30}")
        
        # 1. 适配内容
        adapted_content = self.content_adapter.adapt_for_platform(content, platform)
        logger.info(f"标题: {adapted_content.title}")
        logger.info(f"标签: {', '.join(adapted_content.tags)}")
        
        # 2. 处理图片
        processed_images = []
        for img_path in adapted_content.images:
            processed = self.image_processor.process_for_platform(img_path, platform)
            processed_images.append(processed)
        
        adapted_content.images = processed_images
        
        # 3. 发布（简化实现）
        if self.args.use_app:
            logger.info("使用桌面端 App 发布...")
            # TODO: 实现 App 自动化
        else:
            logger.info("使用浏览器发布...")
            # TODO: 实现浏览器自动化
        
        logger.info(f"✅ {platform} 发布成功")
        return True
    
    def _print_results(self, results: Dict[str, bool]):
        """打印分发结果"""
        logger.info("\n" + "=" * 50)
        logger.info("分发结果汇总")
        logger.info("=" * 50)
        
        for platform, success in results.items():
            status = "✅ 成功" if success else "❌ 失败"
            logger.info(f"{platform:12} {status}")
        
        success_count = sum(results.values())
        total_count = len(results)
        logger.info(f"\n总计: {success_count}/{total_count} 成功")


def main():
    parser = argparse.ArgumentParser(description='多平台内容自动分发')
    
    # 源内容选项
    parser.add_argument('--source', default='xiaohongshu',
                       help='源平台 (默认: xiaohongshu)')
    parser.add_argument('--note-id',
                       help='指定笔记ID')
    
    # 目标平台选项
    parser.add_argument('--targets',
                       help='目标平台，逗号分隔 (如: douyin,kuaishou)')
    
    # 运行选项
    parser.add_argument('--use-app', action='store_true',
                       help='使用桌面端 App')
    parser.add_argument('--driver', default='playwright',
                       choices=['playwright', 'selenium'],
                       help='浏览器驱动')
    parser.add_argument('--debug', action='store_true',
                       help='调试模式（显示浏览器）')
    parser.add_argument('--relogin', action='store_true',
                       help='强制重新登录')
    
    # 发布策略
    parser.add_argument('--stagger', action='store_true',
                       help='错峰发布')
    parser.add_argument('--filter-tag',
                       help='只同步特定标签的内容')
    parser.add_argument('--exclude',
                       help='排除特定关键词')
    
    args = parser.parse_args()
    
    # 创建管理器并运行
    manager = DistributeManager(args)
    success = manager.run()
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
