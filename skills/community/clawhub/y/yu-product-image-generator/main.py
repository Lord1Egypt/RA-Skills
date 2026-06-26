#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 商品图生成器 - 主程序
对话式交互，生成电商商品图
"""

import os
import sys
from typing import Dict, List, Any, Optional

# 添加路径
sys.path.insert(0, os.path.dirname(__file__))

from core.image_analyzer import ImageAnalyzer, analyze_product
from core.scheme_generator import SchemeGenerator, generate_schemes
from core.composition_planner import CompositionPlanner, create_composition_plan
from core.image_generator import ImageGenerator, GenerationConfig
from core.image_packager import ImagePackager, package_images
from utils.feishu_sender import send_feishu_images, send_feishu_message
from utils.text_overlay import add_marketing_text

# 默认 API Key（Grsai Nano Banana）
DEFAULT_API_KEY = "sk-6fe41fd597614d2686f6d0685b4bd232"

# 默认 API Key
DEFAULT_API_KEY = "sk-6fe41fd597614d2686f6d0685b4bd232"


class ProductImageGenerator:
    """AI 商品图生成器（主控制器）"""
    
    # 支持的语言
    LANGUAGES = {
        '1': ('中文', 'zh'),
        '2': ('英文', 'en'),
        '3': ('日文', 'ja'),
        '4': ('韩文', 'ko'),
        '5': ('德文', 'de'),
        '6': ('法文', 'fr'),
        '7': ('阿拉伯文', 'ar'),
        '8': ('俄文', 'ru'),
        '9': ('泰文', 'th'),
        '10': ('印尼文', 'id'),
        '11': ('越南文', 'vi'),
        '12': ('无文字', 'none')
    }
    
    def __init__(self):
        self.analyzer = ImageAnalyzer()
        self.scheme_generator = SchemeGenerator()
        self.packager = ImagePackager()
        self.generator = ImageGenerator(api_key=DEFAULT_API_KEY)
        
        # 会话状态
        self.state = {
            'images': [],
            'analysis': None,
            'selected_scheme': None,
            'language': 'zh',
            'plan': None,
            'generated_images': []
        }
    
    def start_session(self, image_paths: List[str]) -> Dict[str, Any]:
        """
        开始新会话
        
        Args:
            image_paths: 产品图片路径列表
        
        Returns:
            分析结果
        """
        print("\n" + "=" * 60)
        print("🎨 AI 商品图生成器")
        print("=" * 60)
        
        # 1. 分析产品
        print("\n📸 正在分析产品图片...")
        analysis = analyze_product(image_paths)
        
        self.state['images'] = image_paths
        self.state['analysis'] = analysis
        
        # 返回分析结果供用户确认
        return {
            'status': 'analyzed',
            'analysis': analysis,
            'confirm_prompt': f"""
📋 产品分析结果：
- 产品类型：{analysis.get('product_type', '未知')}
- 材质：{analysis.get('material', '未知')}
- 颜色：{analysis.get('color', '未知')}
- 风格：{analysis.get('style', '未知')}

是否正确？正确请输入 confirm，错误请输入正确的产品类型：
"""
        }
    
    def confirm_product_type(self, user_input: str) -> Dict[str, Any]:
        """
        确认或修改产品类型
        
        Args:
            user_input: 用户输入（confirm 或新的产品类型）
        
        Returns:
            确认结果
        """
        if user_input.lower() == 'confirm' or user_input.lower() == '确定':
            return {
                'status': 'confirmed',
                'analysis': self.state['analysis'],
                'message': f"✅ 产品类型确认：{self.state['analysis'].get('product_type', '未知')}"
            }
        else:
            # 用户提供了新的产品类型
            self.state['analysis']['product_type'] = user_input
            return {
                'status': 'updated',
                'analysis': self.state['analysis'],
                'message': f"✅ 产品类型已更新：{user_input}"
            }
    
    def show_schemes(self) -> str:
        """显示可选方案"""
        if not self.state['analysis']:
            return "❌ 请先分析产品"
        
        # 生成方案
        schemes = self.scheme_generator.generate_schemes(self.state['analysis'])
        
        # 格式化输出
        output_lines = ["\n🎨 已生成 3 个设计方案：\n"]
        
        for scheme in schemes:
            output_lines.append(f"【方案{scheme.id}】{scheme.icon} {scheme.name}")
            output_lines.append(f"风格：{scheme.description}")
            output_lines.append(f"文案：{scheme.copywriting_style}")
            output_lines.append(f"氛围：{scheme.target_mood}")
            output_lines.append("")
        
        output_lines.append("请选择方案（输入 1/2/3）：")
        
        return "\n".join(output_lines)
    
    def select_scheme(self, scheme_id: int) -> Dict[str, Any]:
        """
        选择方案
        
        Args:
            scheme_id: 方案 ID（1/2/3）
        
        Returns:
            选择结果
        """
        schemes = self.scheme_generator.generate_schemes(self.state['analysis'])
        
        if scheme_id < 1 or scheme_id > len(schemes):
            return {'status': 'error', 'message': '无效的方案编号'}
        
        selected = schemes[scheme_id - 1]
        self.state['selected_scheme'] = selected
        
        return {
            'status': 'scheme_selected',
            'scheme': selected,
            'message': f"✅ 已选择：{selected.icon} {selected.name}"
        }
    
    def show_languages(self) -> str:
        """显示语言选项"""
        lines = ["\n🌐 请选择语言：\n"]
        
        for key, (name, code) in self.LANGUAGES.items():
            lines.append(f"{key}. {name}")
        
        lines.append("\n请输入选项（1-12）：")
        
        return "\n".join(lines)
    
    def select_language(self, lang_id: str) -> Dict[str, Any]:
        """
        选择语言
        
        Args:
            lang_id: 语言编号（1-12）
        
        Returns:
            选择结果
        """
        if lang_id not in self.LANGUAGES:
            return {'status': 'error', 'message': '无效的语言编号'}
        
        lang_name, lang_code = self.LANGUAGES[lang_id]
        self.state['language'] = lang_code
        
        return {
            'status': 'language_selected',
            'language': lang_name,
            'message': f"✅ 已选择：{lang_name}"
        }
    
    def create_composition_plan(self, num_shots: int = 3) -> str:
        """
        创建分镜规划
        
        Args:
            num_shots: 分镜数量
        
        Returns:
            分镜规划文本
        """
        if not self.state['selected_scheme']:
            return "❌ 请先选择方案"
        
        # 获取方案 key
        scheme_name = self.state['selected_scheme'].name
        style_key = self._get_style_key(scheme_name)
        
        # 创建规划
        planner = create_composition_plan(style_key, num_shots)
        self.state['plan'] = planner
        
        return planner.format_plan_for_display()
    
    def confirm_and_generate(self, use_reference: bool = True) -> Dict[str, Any]:
        """
        确认并开始生成
        
        Args:
            use_reference: 是否使用参考图模式（保持产品一致性）
        
        Returns:
            生成结果
        """
        if not self.state['plan']:
            return {'status': 'error', 'message': '请先创建分镜规划'}
        
        print("\n🚀 开始生成图片，预计 2-3 分钟...")
        
        # 参考图（用户上传的原图）
        reference_images = self.state['images'] if use_reference else None
        if reference_images:
            print(f"   📎 使用参考图：{len(reference_images)} 张")
        
        # 生成每张图片
        generated_paths = []
        
        for idx, shot in enumerate(self.state['plan'].shots):
            # 构建提示词（强调保持产品一致性）
            if use_reference:
                prompt = self.generator.build_prompt(
                    self.state['analysis'],
                    self.state['selected_scheme'],
                    shot,
                    self.state['language']
                )
                # 添加参考图模式提示
                if self.state['language'] == 'zh':
                    prompt += "，保持产品主体不变，只更换背景，产品一致性"
                else:
                    prompt += ", keep product subject unchanged, only change background, product consistency"
            else:
                prompt = self.generator.build_prompt(
                    self.state['analysis'],
                    self.state['selected_scheme'],
                    shot,
                    self.state['language']
                )
            
            print(f"\n  生成图{shot.id}：{shot.name}")
            
            # 生成图片
            config = GenerationConfig(
                width=1024,
                height=1024,
                num_images=1
            )
            
            paths = self.generator.generate(
                prompt,
                config=config,
                reference_images=reference_images
            )
            
            # 添加营销文案
            if paths and self.state['language'] != 'none':
                for path in paths:
                    # 获取文案
                    if self.state['language'] == 'en':
                        headline = shot.copywriting_en if hasattr(shot, 'copywriting_en') else ''
                    else:
                        headline = shot.copywriting if hasattr(shot, 'copywriting') else ''
                    
                    # 如果没有文案，使用默认
                    if not headline:
                        headline = self.state['selected_scheme'].copywriting_style if hasattr(self.state['selected_scheme'], 'copywriting_style') else ''
                    
                    if headline:
                        print(f"   📝 添加文案：{headline}")
                        add_marketing_text(path, headline, '', path)
            
            generated_paths.extend(paths)
        
        self.state['generated_images'] = generated_paths
        
        return {
            'status': 'generated',
            'image_paths': generated_paths,
            'count': len(generated_paths)
        }
    
    def package_and_download(self, product_name: str = "产品", customer_name: str = None) -> Dict[str, Any]:
        """
        打包下载
        
        Args:
            product_name: 产品名称
            customer_name: 客户名称
        
        Returns:
            打包结果
        """
        if not self.state['generated_images']:
            return {'status': 'error', 'message': '没有可打包的图片'}
        
        result = package_images(
            self.state['generated_images'],
            product_name,
            customer_name
        )
        
        return {
            'status': 'packaged',
            'zip_path': result['zip_path'],
            'preview_path': result.get('preview_path')
        }
    
    def send_to_feishu(self, user_id: str = None) -> Dict[str, Any]:
        """
        发送到飞书
        
        Args:
            user_id: 接收用户ID（默认当前用户）
        
        Returns:
            发送结果
        """
        if not self.state['generated_images']:
            return {'status': 'error', 'message': '没有可发送的图片'}
        
        if user_id is None:
            user_id = "ou_9ac9a7fa7050b46022dcdaf6c02a3ee3"
        
        print("\n📤 准备发送到飞书...")
        
        # 发送消息通知
        product_name = self.state.get('analysis', {}).get('product_type', '产品')
        scheme_name = self.state.get('selected_scheme', {}).name if self.state.get('selected_scheme') else '默认风格'
        message = f"🎨 商品图生成完成！\n产品：{product_name}\n风格：{scheme_name}\n共{len(self.state['generated_images'])}张图片"
        
        send_feishu_message(message, user_id)
        
        # 发送图片
        success_count = send_feishu_images(self.state['generated_images'], user_id)
        
        if success_count > 0:
            return {
                'status': 'sent',
                'success_count': success_count,
                'total': len(self.state['generated_images']),
                'message': f'✅ 成功发送 {success_count} 张图片到飞书'
            }
        else:
            return {
                'status': 'failed',
                'message': '❌ 发送失败，请检查飞书配置'
            }
    
    def _get_style_key(self, scheme_name: str) -> str:
        """根据方案名称获取风格 key"""
        if '治愈' in scheme_name or '温馨' in scheme_name:
            return 'healing_warm'
        elif '简约' in scheme_name or '商务' in scheme_name:
            return 'minimal_business'
        elif '时尚' in scheme_name or '潮流' in scheme_name:
            return 'fashion_trendy'
        else:
            return 'healing_warm'
    
    def reset(self):
        """重置会话状态"""
        self.state = {
            'images': [],
            'analysis': None,
            'selected_scheme': None,
            'language': 'zh',
            'plan': None,
            'generated_images': []
        }


# 便捷函数
def generate_product_images(
    image_paths: List[str],
    scheme_id: int = 1,
    language: str = '1',
    num_shots: int = 3,
    product_name: str = "产品",
    customer_name: str = None
) -> Dict[str, Any]:
    """
    便捷函数：一键生成商品图
    
    Args:
        image_paths: 产品图片路径
        scheme_id: 方案编号（1-3）
        language: 语言编号（1-12）
        num_shots: 分镜数量
        product_name: 产品名称
        customer_name: 客户名称
    
    Returns:
        完整结果
    """
    generator = ProductImageGenerator()
    
    # 1. 分析
    result = generator.start_session(image_paths)
    print(f"✅ 产品分析完成：{result['analysis'].get('product_type')}")
    
    # 2. 选择方案
    generator.select_scheme(scheme_id)
    print(f"✅ 方案已选择")
    
    # 3. 选择语言
    generator.select_language(language)
    print(f"✅ 语言已选择")
    
    # 4. 创建规划
    plan_text = generator.create_composition_plan(num_shots)
    print(plan_text)
    
    # 5. 生成
    gen_result = generator.confirm_and_generate()
    print(f"✅ 生成完成：{gen_result['count']}张图片")
    
    # 6. 打包
    package_result = generator.package_and_download(product_name, customer_name)
    print(f"📦 打包完成：{package_result['zip_path']}")
    
    return package_result


if __name__ == '__main__':
    # 测试流程
    print("🎨 AI 商品图生成器 - 完整流程测试")
    print("=" * 60)
    
    # 模拟测试（实际使用时传入真实图片路径）
    test_images = ['/tmp/product_001.jpg', '/tmp/product_002.jpg']
    
    print("\n提示：这是测试模式，实际使用需要真实图片路径\n")
    
    # 演示流程
    generator = ProductImageGenerator()
    
    # 1. 分析
    print("步骤 1: 分析产品")
    result = generator.start_session(test_images)
    print(f"  产品类型：{result['analysis'].get('product_type')}")
    
    # 2. 显示方案
    print("\n步骤 2: 选择方案")
    print(generator.show_schemes())
    
    # 3. 选择方案
    generator.select_scheme(1)
    print("  ✅ 已选择方案 1")
    
    # 4. 选择语言
    print("\n步骤 3: 选择语言")
    print(generator.show_languages())
    generator.select_language('1')
    print("  ✅ 已选择中文")
    
    # 5. 创建规划
    print("\n步骤 4: 分镜规划")
    print(generator.create_composition_plan(3))
    
    # 6. 生成（模拟）
    print("\n步骤 5: 生成图片（模拟）")
    print("   开始生成...")
    print("  ✅ 生成完成")
    
    # 7. 打包
    print("\n步骤 6: 打包下载")
    result = generator.package_and_download("测试产品", "测试客户")
    print(f"  📦 ZIP: {result['zip_path']}")
    
    print("\n" + "=" * 60)
    print("✅ 完整流程测试完成！")
