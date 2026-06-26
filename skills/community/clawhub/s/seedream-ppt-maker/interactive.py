#!/usr/bin/env python3
"""
baoyu-seedream-ppt - 交互式分步生成入口
优化后的工作流程：
1. 分析内容 → 推荐布局×风格×比例 → 请用户确认
2. 用户确认方案 → 生成每页提示词 → 可选请用户确认
3. 提示词确认 → 逐页生成图片 → 整合PPT

目的：减少反复修改，节省API配额
"""

import argparse
import json
import os
import sys
import time
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from baoyu_seedream_ppt import (
    get_api_key, generate_image, download_image, create_ppt,
    DEFAULT_MODEL, BASE_URL
)


class InteractivePPTCreator:
    """交互式分步PPT创建器"""
    
    def __init__(self):
        """初始化"""
        self.skill_root = Path(__file__).parent
        self.baoyu_root = self.skill_root.parent / "baoyu-infographic"
        
        # 检查baoyu-infographic依赖
        if not self.baoyu_root.exists():
            print(f"❌ 未找到 baoyu-infographic 布局库，请先安装:")
            print(f"   位置: {self.baoyu_root}")
            raise FileNotFoundError("baoyu-infographic not found")
        
        self.api_key = get_api_key()
        if not self.api_key:
            raise ValueError("❌ 未找到火山方舟API Key，请配置 ~/.openclaw/config.json")
    
    def get_available_layouts(self) -> List[str]:
        """获取所有可用布局"""
        layouts_dir = self.baoyu_root / "references" / "layouts"
        return sorted([f.stem for f in layouts_dir.glob("*.md")])
    
    def get_available_styles(self) -> List[str]:
        """获取所有可用风格"""
        styles_dir = self.baoyu_root / "references" / "styles"
        return sorted([f.stem for f in styles_dir.glob("*.md")])
    
    def step1_analyze_content(self, content_path: str) -> Dict:
        """
        第一步：分析内容，推荐方案
        
        Args:
            content_path: 内容文件路径
        
        Returns:
            分析结果，包含内容分页、推荐方案
        """
        print(f"📖 [步骤1] 分析内容文件: {content_path}")
        
        with open(content_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 拆分内容为多页（每页一个#标题分隔）
        pages = []
        current_page = []
        for line in content.split('\n'):
            if line.startswith('# ') and current_page:
                pages.append('\n'.join(current_page))
                current_page = []
            current_page.append(line)
        if current_page:
            pages.append('\n'.join(current_page))
        
        print(f"   检测到 {len(pages)} 页内容")
        
        # 内容分析，推荐布局和风格
        recommendations = self._recommend_layout_style(pages)
        
        result = {
            "content_path": content_path,
            "total_pages": len(pages),
            "pages": pages,
            "recommendations": recommendations
        }
        
        # 保存分析结果
        return result
    
    def _recommend_layout_style(self, pages: List[str]) -> Dict:
        """根据内容推荐布局和风格"""
        # 简单规则推荐，可以后续用AI优化
        content_text = ' '.join(pages).lower()
        recommendations = []
        
        # 布局推荐规则
        if any(k in content_text for k in ['对比', 'vs', '比较', '区别']):
            recommendations.append({
                "layout": "binary-comparison",
                "style": "chalkboard",
                "reason": "内容包含对比分析，使用二分对比布局 + 黑板风格清晰易读"
            })
        
        if any(k in content_text for k in ['时间', '流程', '发展', '历史', '历程']):
            recommendations.append({
                "layout": "linear-progression",
                "style": "craft-handmade",
                "reason": "内容包含时间线/流程，使用线性递进布局 + 手绘纸艺风格自然流畅"
            })
        
        if any(k in content_text for k in ['多个', '分类', '汇总', '概览', '介绍']):
            recommendations.append({
                "layout": "bento-grid",
                "style": "corporate-memphis",
                "reason": "多主题概览，使用便当网格布局 + 扁平化活力风格清爽美观"
            })
        
        if any(k in content_text for k in ['数据', '指标',kpi,'dashboard']):
            recommendations.append({
                "layout": "dashboard",
                "style": "technical-schematic",
                "reason": "数据指标展示，使用仪表盘布局 + 工程蓝图风格专业清晰"
            })
        
        if len(recommendations) < 3:
            # 默认推荐
            recommendations.append({
                "layout": "bento-grid",
                "style": "morandi-journal",
                "reason": "通用多主题布局 + 莫兰迪手绘风格，适配大多数内容"
            })
        
        if len(recommendations) < 3:
            recommendations.append({
                "layout": "dense-modules",
                "style": "bold-graphic",
                "reason": "高密度信息模块 + 粗线漫画风格，信息密度高且视觉冲击力强"
            })
        
        # 只推荐前3个
        return recommendations[:3]
    
    def format_scheme_for_user(self, analysis: Dict, aspect: str = "landscape") -> str:
        """格式化方案给用户确认"""
        total_pages = analysis["total_pages"]
        recs = analysis["recommendations"]
        
        text = f"""🎯 **内容分析完成 - 推荐方案**

📄 **内容信息**:
- 总页数: {total_pages} 页
- 建议比例: **{self._format_aspect(aspect)}**

---

💡 **推荐组合（选择一个或告诉我你的想法）**:

"""
        
        for i, rec in enumerate(recs, 1):
            text += f"**方案{i}**\n"
            text += f"- 布局: `{rec['layout']}`\n"
            text += f"- 风格: `{rec['style']}`\n"
            text += f"- 原因: {rec['reason']}\n\n"
        
        text += """---

请确认：
1. 选择哪个推荐方案，还是要使用其他布局/风格？
2. 比例是否需要调整？（可选 landscape 16:9 / portrait 9:16 / square 1:1）
3. 确认后，是否需要我先把每页提示词列出来给你确认再生成？（推荐复杂内容确认一下）

修改请直接告诉我，比如：
- "选方案1，比例不变，需要确认提示词"
- "用 bento-grid + claymation，16:9，不需要确认提示词直接生成"
"""
        return text
    
    def _format_aspect(self, aspect: str) -> str:
        if aspect == "landscape":
            return "landscape (16:9)"
        elif aspect == "portrait":
            return "portrait (9:16)"
        elif aspect == "square":
            return "square (1:1)"
        return aspect
    
    def _read_template(self, layout: str, style: str) -> Tuple[str, str, str]:
        """读取布局、风格、基础prompt模板"""
        layout_path = self.baoyu_root / "references" / "layouts" / f"{layout}.md"
        style_path = self.baoyu_root / "references" / "styles" / f"{style}.md"
        base_prompt_path = self.baoyu_root / "references" / "base-prompt.md"
        
        with open(layout_path, 'r', encoding='utf-8') as f:
            layout_def = f.read()
        
        with open(style_path, 'r', encoding='utf-8') as f:
            style_def = f.read()
        
        with open(base_prompt_path, 'r', encoding='utf-8') as f:
            base_prompt = f.read()
        
        return layout_def, style_def, base_prompt
    
    def step2_generate_prompts(
        self,
        analysis: Dict,
        layout: str,
        style: str,
        aspect: str,
        project_name: Optional[str] = None,
        output_dir: str = "./output"
    ) -> Dict:
        """
        第二步：生成所有页面的提示词
        
        Args:
            analysis: 第一步的分析结果
            layout: 用户选定的布局
            style: 用户选定的风格
            aspect: 用户选定的比例
            project_name: 项目名称（默认从内容文件提取）
            output_dir: 输出目录
        
        Returns:
            生成的提示词列表和项目信息
        """
        print(f"\n💭 [步骤2] 生成每页提示词...")
        
        if not project_name:
            content_path = analysis["content_path"]
            project_name = os.path.splitext(os.path.basename(content_path))[0]
        
        # 创建输出目录
        output_path = Path(output_dir) / project_name
        images_dir = output_path / "images"
        prompts_dir = output_path / "prompts"
        output_path.mkdir(parents=True, exist_ok=True)
        images_dir.mkdir(parents=True, exist_ok=True)
        prompts_dir.mkdir(parents=True, exist_ok=True)
        
        # 读取模板
        layout_def, style_def, base_prompt = self._read_template(layout, style)
        
        # 为每页生成prompt
        prompts = []
        for page_idx, page_content in enumerate(analysis["pages"]):
            page_num = page_idx + 1
            page_title = page_content.splitlines()[0].strip('# ')
            
            # 构建完整prompt
            full_prompt = base_prompt
            full_prompt = full_prompt.replace("{{LAYOUT}}", layout)
            full_prompt = full_prompt.replace("{{STYLE}}", style)
            full_prompt = full_prompt.replace("{{ASPECT_RATIO}}", aspect)
            full_prompt = full_prompt.replace("{{LANGUAGE}}", "Chinese")
            full_prompt = full_prompt.replace("{{LAYOUT_GUIDELINES}}", layout_def)
            full_prompt = full_prompt.replace("{{STYLE_GUIDELINES}}", style_def)
            full_prompt = full_prompt.replace("{{CONTENT}}", page_content)
            full_prompt = full_prompt.replace("{{TEXT_LABELS}}", "")
            
            prompts.append({
                "page_num": page_num,
                "page_title": page_title,
                "content": page_content,
                "prompt": full_prompt
            })
            
            # 保存prompt
            prompt_file = prompts_dir / f"page_{page_num:02d}.md"
            with open(prompt_file, 'w', encoding='utf-8') as f:
                f.write(full_prompt)
        
        # 保存项目配置
        config = {
            "project_name": project_name,
            "layout": layout,
            "style": style,
            "aspect": aspect,
            "total_pages": len(prompts),
            "content_path": analysis["content_path"]
        }
        with open(output_path / "config.json", 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        
        print(f"   已生成 {len(prompts)} 个提示词，保存在: {prompts_dir}")
        
        return {
            "project_name": project_name,
            "output_dir": str(output_path),
            "images_dir": str(images_dir),
            "prompts_dir": str(prompts_dir),
            "layout": layout,
            "style": style,
            "aspect": aspect,
            "prompts": prompts,
            "config": config
        }
    
    def format_prompts_for_user(self, prompt_info: Dict) -> str:
        """格式化提示词给用户确认"""
        prompts = prompt_info["prompts"]
        project = prompt_info["project_name"]
        layout = prompt_info["layout"]
        style = prompt_info["style"]
        
        text = f"""📋 **提示词预览 - {project}**

**配置**: 布局=`{layout}`, 风格=`{style}`

---

"""
        for p in prompts:
            text += f"**第{p['page_num']}页**: {p['page_title']}\n"
            text += f"> ```\n> {p['prompt'][:200]}...\n> ```\n\n"
        
        text += f"""---

共 {len(prompts)} 页。请确认：
- 是否需要修改哪些页面的提示词？
- 确认无误后，我将开始逐页生成图片。
"""
        return text
    
    def step3_generate_images(
        self,
        prompt_info: Dict,
        model: str = DEFAULT_MODEL,
        interval: int = 10
    ) -> Dict:
        """
        第三步：提示词确认后，生成所有图片
        
        Args:
            prompt_info: 第二步的结果
            model: Seedream模型ID
            interval: 生成间隔（秒），避免限流
        
        Returns:
            生成结果
        """
        print(f"\n🖼️  [步骤3] 开始生成图片...")
        
        prompts = prompt_info["prompts"]
        images_dir = Path(prompt_info["images_dir"])
        aspect = prompt_info["aspect"]
        
        success_count = 0
        results = []
        
        for p in prompts:
            page_num = p["page_num"]
            page_title = p["page_title"]
            prompt = p["prompt"]
            
            print(f"\n[{page_num}/{len(prompts)}] 生成: {page_title}")
            
            # 生成图片
            image_url = generate_image(prompt, aspect, self.api_key, model)
            if not image_url:
                print(f"   ❌ 生成失败")
                results.append({
                    "page_num": page_num,
                    "page_title": page_title,
                    "status": "failed",
                    "error": "API返回空"
                })
                continue
            
            # 下载图片
            image_path = images_dir / f"page_{page_num:02d}.png"
            if download_image(image_url, str(image_path)):
                success_count += 1
                results.append({
                    "page_num": page_num,
                    "page_title": page_title,
                    "status": "success",
                    "path": str(image_path)
                })
            else:
                results.append({
                    "page_num": page_num,
                    "page_title": page_title,
                    "status": "failed",
                    "error": "下载失败"
                })
            
            # 间隔避免限流
            if page_num != len(prompts):
                print(f"   ⏳ 等待 {interval} 秒后生成下一页...")
                time.sleep(interval)
        
        print(f"\n✅ 图片生成完成: {success_count}/{len(prompts)} 页成功")
        
        return {
            "total": len(prompts),
            "success": success_count,
            "failed": len(prompts) - success_count,
            "results": results,
            "prompt_info": prompt_info
        }
    
    def step4_create_ppt(self, generation_result: Dict) -> str:
        """
        第四步：整合所有图片到PPT
        
        Args:
            generation_result: 第三步的结果
        
        Returns:
            最终PPT路径
        """
        print(f"\n📦 [步骤4] 整合PPT...")
        
        prompt_info = generation_result["prompt_info"]
        images_dir = Path(prompt_info["images_dir"])
        output_dir = Path(prompt_info["output_dir"])
        project_name = prompt_info["project_name"]
        layout = prompt_info["layout"]
        style = prompt_info["style"]
        aspect = prompt_info["aspect"]
        
        output_ppt = output_dir / f"{project_name}_{layout}_{style}.pptx"
        
        if generation_result["success"] == 0:
            print(f"❌ 没有成功生成任何图片，无法创建PPT")
            return ""
        
        create_ppt(str(images_dir), str(output_ppt), aspect)
        
        print(f"\n🎉 全部完成! 最终PPT: {output_ppt}")
        return str(output_ppt)
    
    def get_summary(self, generation_result: Dict, ppt_path: str) -> str:
        """生成总结给用户"""
        res = generation_result
        pi = res["prompt_info"]
        
        text = f"""✅ **生成完成**

| 项目 | 信息 |
|------|------|
| **项目名称** | {pi['project_name']} |
| **布局** | {pi['layout']} |
| **风格** | {pi['style']} |
| **比例** | {pi['aspect']} |
| **总页数** | {res['total']} |
| **成功生成** | {res['success']} |
| **失败** | {res['failed']} |
| **最终PPT** | `{ppt_path}` |

你可以使用上述路径打开PPT文件。
"""
        return text


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description='baoyu-seedream-ppt 交互式分步生成'
    )
    parser.add_argument('content_file', nargs='?', help='内容文件路径')
    parser.add_argument('--step', '-s', 
                       choices=["analyze", "prompts", "generate", "full"],
                       default="analyze",
                       help="执行步骤: analyze(分析内容推荐方案), prompts(生成提示词), generate(生成图片), full(完整流程测试)")
    parser.add_argument('--layout', '-l', help='选定的布局 (prompts/generate步骤使用)')
    parser.add_argument('--style', help='选定的风格 (prompts/generate步骤使用)')
    parser.add_argument('--aspect', default='landscape', 
                       choices=['landscape', 'portrait', 'square'],
                       help='宽高比')
    parser.add_argument('--config', '-c', help='项目配置JSON文件 (generate步骤使用)')
    parser.add_argument('--output-dir', '-o', default='./output', help='输出目录')
    parser.add_argument('--model', default=DEFAULT_MODEL, help='Seedream模型ID')
    parser.add_argument('--interval', '-i', type=int, default=10, help='生成间隔(秒)')
    
    args = parser.parse_args()
    
    creator = InteractivePPTCreator()
    
    if args.step == "analyze":
        if not args.content_file or not os.path.exists(args.content_file):
            print("❌ 请提供有效的内容文件路径")
            sys.exit(1)
        
        result = creator.step1_analyze_content(args.content_file)
        print("\n" + "="*70)
        print(creator.format_scheme_for_user(result, args.aspect))
        print("="*70)
    
    elif args.step == "prompts":
        if not args.content_file or not os.path.exists(args.content_file):
            print("❌ 请提供有效的内容文件路径")
            sys.exit(1)
        if not args.layout or not args.style:
            print("❌ 请提供 --layout 和 --style 参数")
            sys.exit(1)
        
        # 先分析内容
        analysis = creator.step1_analyze_content(args.content_file)
        # 生成提示词
        prompt_info = creator.step2_generate_prompts(
            analysis, args.layout, args.style, args.aspect,
            output_dir=args.output_dir
        )
        print("\n" + "="*70)
        print(creator.format_prompts_for_user(prompt_info))
        print("="*70)
        print(f"\n💾 提示词已保存到: {prompt_info['prompts_dir']}")
    
    elif args.step == "generate":
        # 从配置文件读取信息
        if not args.config or not os.path.exists(args.config):
            print("❌ 请提供 --config 参数（项目config.json路径）")
            sys.exit(1)
        
        with open(args.config, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # 需要重新分析内容获取pages
        analysis = creator.step1_analyze_content(config["content_path"])
        
        # 重新生成提示词（用户可能修改过）
        prompt_info = creator.step2_generate_prompts(
            analysis,
            config["layout"],
            config["style"],
            config["aspect"],
            config["project_name"],
            args.output_dir
        )
        
        # 生成图片
        result = creator.step3_generate_images(prompt_info, args.model, args.interval)
        
        # 创建PPT
        if result["success"] > 0:
            ppt_path = creator.step4_create_ppt(result)
            print("\n" + "="*70)
            print(creator.get_summary(result, ppt_path))
            print("="*70)
        else:
            print("\n❌ 没有成功生成任何图片")
            sys.exit(1)
    
    elif args.step == "full":
        # 完整流程（测试用）
        if not args.content_file or not os.path.exists(args.content_file):
            print("❌ 请提供有效的内容文件路径")
            sys.exit(1)
        if not args.layout or not args.style:
            print("❌ 请提供 --layout 和 --style 参数")
            sys.exit(1)
        
        print("🚀 执行完整流程（测试用，实际使用应分步确认）")
        
        # 1. 分析内容
        analysis = creator.step1_analyze_content(args.content_file)
        print(f"   分析完成，{analysis['total_pages']} 页")
        
        # 2. 生成提示词
        prompt_info = creator.step2_generate_prompts(
            analysis, args.layout, args.style, args.aspect,
            output_dir=args.output_dir
        )
        print(f"   提示词生成完成，{len(prompt_info['prompts'])} 页")
        
        # 3. 生成图片
        result = creator.step3_generate_images(prompt_info, args.model, args.interval)
        
        # 4. 创建PPT
        if result["success"] > 0:
            ppt_path = creator.step4_create_ppt(result)
            print("\n" + "="*70)
            print(creator.get_summary(result, ppt_path))
            print("="*70)
        else:
            print("\n❌ 没有成功生成任何图片")
            sys.exit(1)


if __name__ == "__main__":
    main()
