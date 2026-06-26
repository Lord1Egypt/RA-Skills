"""
style_presets.py - 学术插图风格预设库
为不同顶会/期刊场景提供标准化的配色和风格模板
"""

# ============================================================
# 风格预设
# ============================================================

PRESETS = {
    "cvpr": {
        "label": "CVPR (Computer Vision) — Flat 2D Schematic",
        "style": (
            "flat 2D schematic, solid color blocks with no gradients, "
            "no shadows, no 3D, no shading, no perspective, "
            "clean layer separation by color coding, "
            "thin straight arrows for data flow left-to-right or top-to-bottom, "
            "concrete input examples at entry points, "
            "loss modules in purple and larger than other blocks"
        ),
        "background": "pure white",
        "primary_colors": {
            "frozen":  "#3B82F6",     # 蓝 - frozen/teacher 模块
            "module":  "#3B82F6",     # 蓝 - 核心模块 (shared)
            "image":   "#F97316",     # 橙 - image student/分支
            "text":    "#22C55E",     # 绿 - text student/分支
            "loss":    "#8B5CF6",     # 紫 - 损失函数 (醒目)
            "input":   "#60A5FA",     # 浅蓝 - 输入层
            "queue":   "#8B5CF6",     # 紫 - 队列/缓存
            "baseline": "#9CA3AF",    # 灰 - 基线/对比方法
        },
        "font": "Arial or Helvetica, sans-serif",
        "stroke": "1.5px black, thin straight lines only",
        "corner_radius": "8px",
        "dpi": 300,
        "negative_keywords": (
            "photorealistic, 3D render, watercolor, hand-drawn, gradients, "
            "shadow, depth, perspective, decorative background, comic, blurry, "
            "rounded 3D, bevel, emboss, glow, soft edges, texture, noise, "
            "isometric, drop shadow, inner shadow, outer glow"
        ),
    },
    "neurips": {
        "label": "NeurIPS (Machine Learning)",
        "style": "minimalist schematic, thin lines, clear hierarchy",
        "background": "pure white",
        "primary_colors": {
            "module": "#7570B3",      # 紫 - 核心模块
            "secondary": "#E7298A",   # 粉 - 次级模块
            "highlight": "#D95F02",   # 橙 - 强调
            "input": "#66A61E",       # 绿 - 输入
            "output": "#E6AB02",      # 黄 - 输出
            "loss": "#A6761D",        # 棕 - 损失
            "baseline": "#CCCCCC",    # 浅灰 - 基线
        },
        "font": "Times New Roman or Computer Modern, serif",
        "stroke": "1px dark gray",
        "corner_radius": "4px",
        "dpi": 300,
        "negative_keywords": "photorealistic, 3D render, watercolor, hand-drawn, heavy borders, "
                             "shadow, bold colors, decorative, blurry",
    },
    "icml": {
        "label": "ICML (Machine Learning)",
        "style": "clean block diagram, consistent spacing, academic vector",
        "background": "pure white",
        "primary_colors": {
            "module": "#1F77B4",      # 蓝
            "secondary": "#FF7F0E",   # 橙
            "highlight": "#D62728",   # 红
            "input": "#2CA02C",       # 绿
            "output": "#9467BD",      # 紫
            "loss": "#8C564B",        # 棕
            "baseline": "#BCBD22",    # 黄绿 - 基线
        },
        "font": "Arial, sans-serif",
        "stroke": "1.5px black",
        "corner_radius": "6px",
        "dpi": 300,
        "negative_keywords": "photorealistic, 3D render, watercolor, hand-drawn, gradients, "
                             "shadow, depth, decorative, blurry",
    },
    "nature": {
        "label": "Nature / Science",
        "style": "elegant minimalist, soft colors, high clarity, publication quality",
        "background": "pure white",
        "primary_colors": {
            "module": "#4472C4",      # 柔蓝
            "secondary": "#5B9BD5",   # 浅蓝
            "highlight": "#C00000",   # 深红
            "input": "#70AD47",       # 柔绿
            "output": "#ED7D31",      # 柔橙
            "loss": "#7030A0",        # 柔紫
            "baseline": "#A5A5A5",    # 灰
        },
        "font": "Helvetica, sans-serif",
        "stroke": "1px #333333",
        "corner_radius": "10px",
        "dpi": 300,
        "negative_keywords": "photorealistic, 3D render, watercolor, hand-drawn, heavy lines, "
                             "shadow, bright neon colors, decorative, blurry",
    },
    "default": "cvpr",   # 默认使用 CVPR 风格
}


def get_preset(style_name: str = None) -> dict:
    """获取风格预设，未指定则返回默认"""
    if not style_name:
        style_name = PRESETS["default"]
    preset = PRESETS.get(style_name.lower())
    if not preset:
        preset = PRESETS[PRESETS["default"]]
    return preset


def list_presets() -> list:
    """列出所有可用风格"""
    return [{"name": k, "label": v["label"]} for k, v in PRESETS.items() if isinstance(v, dict)]


def build_style_prompt(preset: dict) -> str:
    """将预设转为 Prompt 中的风格描述片段"""
    colors = preset["primary_colors"]
    color_desc = ", ".join([f"{k}={v}" for k, v in colors.items()])
    return (
        f"Style: {preset['style']}. "
        f"Background: {preset['background']}. "
        f"Color scheme: {color_desc}. "
        f"Font: {preset['font']}. "
        f"Stroke: {preset['stroke']}, corner radius: {preset['corner_radius']}. "
        f"ABSOLUTELY NO shadows, NO 3D, NO gradients, NO perspective. "
        f"Print-ready {preset['dpi']}dpi quality."
    )


def build_negative_prompt(preset: dict) -> str:
    """从预设构建 negative prompt"""
    base = preset.get("negative_keywords", PRESETS["cvpr"]["negative_keywords"])
    # 统一追加 flat 2D 强约束
    flat_guard = "shadow, gradient, 3D, perspective, isometric, bevel, glow, blur, depth of field"
    return f"{base}, {flat_guard}"


def build_latex_caption(figure_type: str, figure_label: str, section_ref: str = "",
                         description: str = "") -> str:
    """
    生成 LaTeX 格式的图注
    Args:
        figure_type: 图类型 (architecture/flowchart/teaser/environment/results)
        figure_label: 中文标签
        section_ref: 对应论文章节 (如 "Section 3.1")
        description: 补充描述
    """
    caption_map = {
        "teaser":      "Overview and motivation of the proposed method",
        "architecture": "Architecture of the proposed framework",
        "flowchart":   "Algorithmic pipeline and procedure",
        "environment": "Experimental environment and interaction setup",
        "results":     "Experimental results and comparison",
    }
    caption_text = caption_map.get(figure_type, figure_label)

    if description:
        caption_text += f". {description}"

    if section_ref:
        section_line = f"  % Corresponds to {section_ref}\n"
    else:
        section_line = ""

    latex = (
        f"{section_line}"
        f"\\begin{{figure}}[t]\n"
        f"  \\centering\n"
        f"  \\includegraphics[width=\\linewidth]{{figures/{figure_type}_diagram.png}}\n"
        f"  \\caption{{{caption_text}}}\n"
        f"  \\label{{fig:{figure_type}}}\n"
        f"\\end{{figure}}"
    )
    return latex


def build_word_caption(figure_type: str, figure_label: str, section_ref: str = "",
                        description: str = "") -> str:
    """生成 Word 文档用的图注"""
    caption_map = {
        "teaser":      "Overview and motivation of the proposed method",
        "architecture": "Architecture of the proposed framework",
        "flowchart":   "Algorithmic pipeline and procedure",
        "environment": "Experimental environment and interaction setup",
        "results":     "Experimental results and comparison",
    }
    caption_text = caption_map.get(figure_type, figure_label)
    if description:
        caption_text += f". {description}"

    ref_line = f" [Ref: {section_ref}]" if section_ref else ""
    return f"Figure: {caption_text}.{ref_line}"
