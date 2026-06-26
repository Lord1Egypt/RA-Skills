#!/usr/bin/env python3
"""
微信公众号 Markdown 转 HTML 工具
支持多种主题样式，严格按照微信规范生成 HTML
"""

import re
import html as html_module


class ThemePresets:
    """主题预设样式集合"""
    
    # ========== 主题 1: 极简商务风 ==========
    MINIMAL_BUSINESS = {
        "name": "极简商务",
        "description": "干净专业，适合商业、职场、管理类文章",
        "body": {
            "font_size": "16px",
            "line_height": "1.75",
            "color": "#333333",
            "letter_spacing": "0.5px",
            "padding": "0 16px",
            "margin": "0 0 16px 0"  # 只保留底部边距，避免叠加
        },
        "h1": {
            "font_size": "20px",
            "font_weight": "bold",
            "color": "#1a1a2e",
            "margin": "24px 0 16px 0",  # 减小上下边距
            "padding": "0 16px",
            "border_bottom": "2px solid #1a1a2e",
            "padding_bottom": "8px",
            "letter_spacing": "0.5px"
        },
        "h2": {
            "font_size": "17px",
            "font_weight": "bold",
            "color": "#2d3436",
            "margin": "20px 0 12px 0",  # 减小边距
            "padding": "0 16px",
            "border_left": "3px solid #0984e3",
            "padding_left": "10px"
        },
        "h3": {
            "font_size": "16px",
            "font_weight": "bold",
            "color": "#2d3436",
            "margin": "16px 0 10px 0",  # 减小边距
            "padding": "0 16px"
        },
        "blockquote": {
            "font_size": "15px",
            "background_color": "#f5f5f5",
            "border_left": "3px solid #0984e3",
            "padding": "12px 16px",  # 减小内边距
            "margin": "16px 0",  # 减小边距
            "color": "#555555",
            "font_style": "normal",  # 不用斜体，更易读
            "line_height": "1.7"
        },
        "code_inline": {
            "font_size": "14px",
            "background_color": "#f0f0f0",
            "padding": "1px 4px",  # 更紧凑
            "border_radius": "3px",
            "color": "#e74c3c",
            "font_family": "'SF Mono', 'Courier New', monospace"
        },
        "code_block": {
            "font_size": "13px",  # 稍小一点
            "background_color": "#f8f8f8",
            "padding": "12px 16px",  # 减小内边距
            "border_radius": "6px",
            "margin": "16px 0",  # 减小边距
            "border": "1px solid #e8e8e8",
            "line_height": "1.6",
            "color": "#333333"
        },
        "list": {
            "font_size": "16px",
            "margin": "12px 0",  # 减小边距
            "padding": "0 16px",
            "line_height": "1.75",
            "bullet_color": "#0984e3"
        },
        "link": {
            "color": "#0984e3",
            "text_decoration": "none",
            "border_bottom": "1px solid #0984e3"
        },
        "strong": {
            "font_weight": "bold",
            "color": "#1a1a2e"
        },
        "separator": {
            "border_top": "1px solid #e0e0e0",
            "margin": "24px 15%"  # 减小边距
        },
        "image": {
            "border_radius": "6px",
            "box_shadow": "none"  # 不用阴影，更简洁
        }
    }
    
    # ========== 主题 2: 温暖文艺风 ==========
    WARM_ARTISTIC = {
        "name": "温暖文艺",
        "description": "柔和有温度，适合生活、情感、读书类文章",
        "body": {
            "font_size": "16px",
            "line_height": "1.8",
            "color": "#4a4a4a",
            "letter_spacing": "0.5px",
            "padding": "0 16px",
            "margin": "0 0 16px 0"
        },
        "h1": {
            "font_size": "21px",
            "font_weight": "normal",
            "color": "#8b6914",
            "margin": "24px 0 16px 0",
            "padding": "0 16px",
            "text_align": "center",
            "border_bottom": "1px solid #d4c4a8",
            "padding_bottom": "10px"
        },
        "h2": {
            "font_size": "17px",
            "font_weight": "normal",
            "color": "#9c7c2e",
            "margin": "20px 0 12px 0",
            "padding": "0 16px",
            "border_left": "none",
            "text_align": "center"
        },
        "h3": {
            "font_size": "16px",
            "font_weight": "bold",
            "color": "#6b5b3d",
            "margin": "16px 0 10px 0",
            "padding": "0 16px"
        },
        "blockquote": {
            "font_size": "15px",
            "background_color": "#faf8f5",
            "border_left": "none",
            "border_top": "1px solid #e8dcc8",
            "border_bottom": "1px solid #e8dcc8",
            "padding": "14px 16px",  # 减小内边距
            "margin": "16px 0",
            "color": "#6b5b3d",
            "font_style": "normal",
            "text_align": "center",
            "line_height": "1.75"
        },
        "code_inline": {
            "font_size": "14px",
            "background_color": "#f5f0e8",
            "padding": "1px 4px",
            "border_radius": "3px",
            "color": "#8b6914",
            "font_family": "'SF Mono', 'Courier New', monospace"
        },
        "code_block": {
            "font_size": "13px",
            "background_color": "#faf8f5",
            "padding": "12px 16px",
            "border_radius": "8px",
            "margin": "16px 0",
            "border": "1px solid #e8dcc8",
            "line_height": "1.6",
            "color": "#5a4a3d"
        },
        "list": {
            "font_size": "16px",
            "margin": "12px 0",
            "padding": "0 16px",
            "line_height": "1.8",
            "bullet_color": "#c9a86c"
        },
        "link": {
            "color": "#8b6914",
            "text_decoration": "none",
            "border_bottom": "1px solid #d4c4a8"
        },
        "strong": {
            "font_weight": "bold",
            "color": "#5a4a2d"
        },
        "separator": {
            "border_top": "1px dashed #d4c4a8",
            "margin": "24px 20%"
        },
        "image": {
            "border_radius": "8px",
            "box_shadow": "none"
        }
    }
    
    # ========== 主题 3: 科技现代风（高对比度浅色）===========
    TECH_MODERN = {
        "name": "科技现代 Pro",
        "description": "高对比度浅色科技风，专业清晰，适合技术、编程、AI类文章",
        "body": {
            "font_size": "16px",
            "line_height": "1.8",
            "color": "#0f172a",  # 深蓝灰，高对比度
            "letter_spacing": "0.3px",
            "padding": "0 20px",
            "margin": "0 0 18px 0",
            "background_color": "#f8fafc"  # 极浅灰背景
        },
        "h1": {
            "font_size": "24px",
            "font_weight": "700",
            "color": "#0f172a",  # 深蓝灰
            "margin": "32px 0 20px 0",
            "padding": "0 20px 12px 20px",
            "border_bottom": "3px solid #2563eb"  # 科技蓝底边
        },
        "h2": {
            "font_size": "19px",
            "font_weight": "600",
            "color": "#1e293b",  # 深色文字
            "margin": "28px 0 16px 0",
            "padding": "10px 16px",
            "border_left": "4px solid #2563eb",  # 科技蓝左边框
            "background_color": "#f1f5f9",  # 浅灰背景
            "border_radius": "0 8px 8px 0"
        },
        "h3": {
            "font_size": "17px",
            "font_weight": "600",
            "color": "#1e293b",  # 深色文字
            "margin": "24px 0 12px 0",
            "padding": "0 20px",
            "border_left": "3px solid #7c3aed",  # 电紫左边框
            "padding_left": "12px"
        },
        "blockquote": {
            "font_size": "15px",
            "background_color": "#eff6ff",  # 浅蓝背景
            "border_left": "4px solid #2563eb",
            "padding": "16px 20px",
            "margin": "20px 0",
            "color": "#334155",  # 深色文字
            "line_height": "1.75",
            "border_radius": "0 8px 8px 0"
        },
        "code_inline": {
            "font_size": "14px",
            "background_color": "#e0e7ff",  # 浅紫蓝背景
            "padding": "3px 8px",
            "border_radius": "4px",
            "color": "#3730a3",  # 深紫色
            "font_weight": "500",
            "font_family": "'SF Mono', 'Fira Code', monospace"
        },
        "code_block": {
            "font_size": "14px",
            "background_color": "#1e293b",  # 深色代码块（专业感）
            "padding": "18px 20px",
            "margin": "24px 0",
            "border_radius": "10px",
            "border": "1px solid #334155",
            "line_height": "1.7",
            "color": "#e2e8f0"  # 浅色代码文字
        },
        "list": {
            "font_size": "16px",
            "margin": "16px 0",
            "padding": "0 20px 0 36px",
            "line_height": "1.8",
            "bullet_color": "#2563eb"
        },
        "link": {
            "color": "#2563eb",  # 科技蓝
            "text_decoration": "none",
            "border_bottom": "1px dashed #2563eb"
        },
        "strong": {
            "font_weight": "600",
            "color": "#0f172a"  # 深色强调
        },
        "separator": {
            "border_top": "2px solid #e2e8f0",  # 浅色分隔线
            "margin": "32px 20%"
        },
        "image": {
            "border_radius": "8px",
            "border": "1px solid #e2e8f0"
        }
    }
    
    # ========== 主题 4: 活泼清新风 ==========
    FRESH_LIVELY = {
        "name": "活泼清新",
        "description": "明亮年轻，适合生活方式、美食、旅行类文章",
        "body": {
            "font_size": "16px",
            "line_height": "1.75",
            "color": "#3d3d3d",
            "letter_spacing": "0.3px",
            "padding": "0 16px",
            "margin": "0 0 16px 0"
        },
        "h1": {
            "font_size": "22px",
            "font_weight": "bold",
            "color": "#ff6b6b",
            "margin": "24px 0 16px 0",
            "padding": "0 16px",
            "text_align": "center"
        },
        "h2": {
            "font_size": "17px",
            "font_weight": "bold",
            "color": "#4ecdc4",
            "margin": "20px 0 12px 0",
            "padding": "0 16px",
            "border_left": "3px solid #4ecdc4",
            "padding_left": "10px"
        },
        "h3": {
            "font_size": "16px",
            "font_weight": "bold",
            "color": "#45b7d1",
            "margin": "16px 0 10px 0",
            "padding": "0 16px"
        },
        "blockquote": {
            "font_size": "15px",
            "background_color": "#fff9e6",
            "border_left": "3px solid #ffd93d",
            "padding": "12px 16px",
            "margin": "16px 0",
            "color": "#5a5a5a",
            "font_style": "normal",
            "line_height": "1.75",
            "border_radius": "0 10px 10px 0"
        },
        "code_inline": {
            "font_size": "14px",
            "background_color": "#e8f4f8",
            "padding": "1px 4px",
            "border_radius": "4px",
            "color": "#45b7d1",
            "font_family": "'SF Mono', 'Courier New', monospace"
        },
        "code_block": {
            "font_size": "13px",
            "background_color": "#f0f7fa",
            "padding": "12px 16px",
            "border_radius": "10px",
            "margin": "16px 0",
            "border": "1px solid #e0f0f5",
            "line_height": "1.6"
        },
        "list": {
            "font_size": "16px",
            "margin": "12px 0",
            "padding": "0 16px",
            "line_height": "1.75",
            "bullet_color": "#ff6b6b"
        },
        "link": {
            "color": "#4ecdc4",
            "text_decoration": "none",
            "border_bottom": "1px solid rgba(78, 205, 196, 0.3)"
        },
        "strong": {
            "font_weight": "bold",
            "color": "#ff6b6b"
        },
        "separator": {
            "border_top": "1px dashed #ffd93d",
            "margin": "24px 20%"
        },
        "image": {
            "border_radius": "10px",
            "box_shadow": "none"
        }
    }
    
    # ========== 主题 5: 杂志高级风 ==========
    MAGAZINE_PREMIUM = {
        "name": "杂志高级",
        "description": "精致设计感，适合时尚、艺术、深度阅读类文章",
        "body": {
            "font_size": "16px",
            "line_height": "1.8",
            "color": "#2c2c2c",
            "letter_spacing": "0.3px",
            "padding": "0 20px",
            "margin": "0 0 16px 0"
        },
        "h1": {
            "font_size": "22px",
            "font_weight": "300",
            "color": "#1a1a1a",
            "margin": "24px 0 16px 0",
            "padding": "0 20px",
            "text_align": "center",
            "letter_spacing": "1px"
        },
        "h2": {
            "font_size": "17px",
            "font_weight": "400",
            "color": "#3d3d3d",
            "margin": "20px 0 12px 0",
            "padding": "0 20px",
            "border_left": "none",
            "border_bottom": "1px solid #c0a080",
            "padding_bottom": "8px"
        },
        "h3": {
            "font_size": "16px",
            "font_weight": "500",
            "color": "#4a4a4a",
            "margin": "16px 0 10px 0",
            "padding": "0 20px",
            "font_style": "italic"
        },
        "blockquote": {
            "font_size": "15px",
            "background_color": "transparent",
            "border_left": "none",
            "border_top": "1px solid #d0c0a0",
            "border_bottom": "1px solid #d0c0a0",
            "padding": "16px 20px",
            "margin": "16px 0",
            "color": "#5a5a5a",
            "font_style": "italic",
            "text_align": "center",
            "line_height": "1.8"
        },
        "code_inline": {
            "font_size": "14px",
            "background_color": "#f5f3f0",
            "padding": "1px 4px",
            "border_radius": "3px",
            "color": "#8b7355",
            "font_family": "'SF Mono', 'Courier New', monospace"
        },
        "code_block": {
            "font_size": "13px",
            "background_color": "#faf8f5",
            "padding": "12px 16px",
            "border_radius": "4px",
            "margin": "16px 0",
            "border": "1px solid #e8e4e0",
            "line_height": "1.7"
        },
        "list": {
            "font_size": "16px",
            "margin": "12px 0",
            "padding": "0 20px",
            "line_height": "1.8",
            "bullet_color": "#c0a080"
        },
        "link": {
            "color": "#8b7355",
            "text_decoration": "none",
            "border_bottom": "1px solid #d0c0a0"
        },
        "strong": {
            "font_weight": "600",
            "color": "#1a1a1a"
        },
        "separator": {
            "border_top": "none",
            "border_bottom": "1px solid #e0d8d0",
            "margin": "24px 25%",
            "height": "1px"
        },
        "image": {
            "border_radius": "4px",
            "box_shadow": "none"
        }
    }
    # ========== 主题 6: 学术专业风 ==========
    ACADEMIC_PROFESSIONAL = {
        "name": "学术专业",
        "description": "严谨学术风格，适合论文、研究报告、学术分析类文章",
        "body": {
            "font_size": "15px",
            "line_height": "1.8",
            "color": "#2c3e50",
            "letter_spacing": "0.3px",
            "padding": "0 20px",
            "margin": "0 0 16px 0"
        },
        "h1": {
            "font_size": "20px",
            "font_weight": "bold",
            "color": "#1a365d",
            "margin": "28px 0 16px 0",
            "padding": "0 20px",
            "border_bottom": "2px solid #2c5282",
            "padding_bottom": "8px"
        },
        "h2": {
            "font_size": "17px",
            "font_weight": "bold",
            "color": "#2d3748",
            "margin": "22px 0 12px 0",
            "padding": "0 20px",
            "border_left": "4px solid #4299e1",
            "padding_left": "12px"
        },
        "h3": {
            "font_size": "15px",
            "font_weight": "bold",
            "color": "#4a5568",
            "margin": "18px 0 10px 0",
            "padding": "0 20px"
        },
        "blockquote": {
            "font_size": "14px",
            "background_color": "#f7fafc",
            "border_left": "4px solid #4299e1",
            "padding": "12px 16px",
            "margin": "16px 0",
            "color": "#4a5568",
            "font_style": "italic",
            "line_height": "1.7"
        },
        "code_inline": {
            "font_size": "13px",
            "background_color": "#edf2f7",
            "padding": "2px 5px",
            "border_radius": "3px",
            "color": "#2b6cb0",
            "font_family": "'Consolas', 'Courier New', monospace"
        },
        "code_block": {
            "font_size": "13px",
            "background_color": "#f7fafc",
            "padding": "14px 16px",
            "border_radius": "4px",
            "margin": "16px 0",
            "border": "1px solid #e2e8f0",
            "line_height": "1.6",
            "color": "#2d3748"
        },
        "list": {
            "font_size": "15px",
            "margin": "12px 0",
            "padding": "0 20px",
            "line_height": "1.8",
            "bullet_color": "#4299e1"
        },
        "link": {
            "color": "#2b6cb0",
            "text_decoration": "none",
            "border_bottom": "1px solid #4299e1"
        },
        "strong": {
            "font_weight": "bold",
            "color": "#1a365d"
        },
        "separator": {
            "border_top": "1px solid #e2e8f0",
            "margin": "24px 20%"
        },
        "image": {
            "border_radius": "4px",
            "box_shadow": "none"
        }
    }
    
    # ========== 主题 7: 复古经典风 ==========
    RETRO_CLASSIC = {
        "name": "复古经典",
        "description": "怀旧复古风格，适合历史、传统文化、回忆录类文章",
        "body": {
            "font_size": "16px",
            "line_height": "1.85",
            "color": "#3d2914",
            "letter_spacing": "0.5px",
            "padding": "0 16px",
            "margin": "0 0 16px 0"
        },
        "h1": {
            "font_size": "22px",
            "font_weight": "normal",
            "color": "#5c3d2e",
            "margin": "24px 0 16px 0",
            "padding": "0 16px",
            "text_align": "center",
            "letter_spacing": "2px"
        },
        "h2": {
            "font_size": "18px",
            "font_weight": "normal",
            "color": "#6b4423",
            "margin": "20px 0 12px 0",
            "padding": "0 16px",
            "border_bottom": "1px solid #c9a86c",
            "padding_bottom": "6px"
        },
        "h3": {
            "font_size": "16px",
            "font_weight": "bold",
            "color": "#5c3d2e",
            "margin": "16px 0 10px 0",
            "padding": "0 16px"
        },
        "blockquote": {
            "font_size": "15px",
            "background_color": "#faf6f0",
            "border_left": "none",
            "border_top": "1px solid #c9a86c",
            "border_bottom": "1px solid #c9a86c",
            "padding": "14px 16px",
            "margin": "16px 0",
            "color": "#6b4423",
            "font_style": "italic",
            "line_height": "1.8",
            "text_align": "center"
        },
        "code_inline": {
            "font_size": "14px",
            "background_color": "#f5ede0",
            "padding": "1px 4px",
            "border_radius": "2px",
            "color": "#8b6914",
            "font_family": "'Courier New', monospace"
        },
        "code_block": {
            "font_size": "13px",
            "background_color": "#faf6f0",
            "padding": "12px 16px",
            "border_radius": "4px",
            "margin": "16px 0",
            "border": "1px solid #e8dcc8",
            "line_height": "1.6",
            "color": "#5c3d2e"
        },
        "list": {
            "font_size": "16px",
            "margin": "12px 0",
            "padding": "0 16px",
            "line_height": "1.85",
            "bullet_color": "#c9a86c"
        },
        "link": {
            "color": "#8b6914",
            "text_decoration": "none",
            "border_bottom": "1px solid #c9a86c"
        },
        "strong": {
            "font_weight": "bold",
            "color": "#5c3d2e"
        },
        "separator": {
            "border_top": "none",
            "border_bottom": "2px solid #c9a86c",
            "margin": "24px 30%"
        },
        "image": {
            "border_radius": "4px",
            "box_shadow": "none"
        }
    }
    
    # ========== 主题 8: 极客科技风 ==========
    GEEK_TECH = {
        "name": "极客科技",
        "description": "极客风格科技主题，适合游戏、二次元、数码类文章",
        "body": {
            "font_size": "16px",
            "line_height": "1.8",
            "color": "#1e293b",  # 深蓝灰，高对比度
            "letter_spacing": "0.3px",
            "padding": "0 16px",
            "margin": "0 0 16px 0",
            "background_color": "#fafbfc"  # 极浅灰背景
        },
        "h1": {
            "font_size": "22px",
            "font_weight": "700",
            "color": "#7c3aed",  # 电紫
            "margin": "28px 0 18px 0",
            "padding": "0 16px",
            "text_align": "center"
        },
        "h2": {
            "font_size": "18px",
            "font_weight": "600",
            "color": "#1e293b",  # 深色文字
            "margin": "24px 0 14px 0",
            "padding": "8px 14px",
            "border_left": "4px solid #8b5cf6",  # 紫色左边框
            "background_color": "#f3f4f6",  # 浅灰背景
            "border_radius": "0 6px 6px 0"
        },
        "h3": {
            "font_size": "16px",
            "font_weight": "600",
            "color": "#374151",  # 深灰文字
            "margin": "20px 0 10px 0",
            "padding": "0 16px",
            "border_left": "3px solid #a78bfa",  # 浅紫左边框
            "padding_left": "10px"
        },
        "blockquote": {
            "font_size": "15px",
            "background_color": "#f5f3ff",  # 浅紫背景
            "border_left": "4px solid #8b5cf6",
            "padding": "14px 16px",
            "margin": "18px 0",
            "color": "#4c1d95",  # 深紫文字
            "line_height": "1.75",
            "border_radius": "0 8px 8px 0"
        },
        "code_inline": {
            "font_size": "14px",
            "background_color": "#ede9fe",  # 浅紫背景
            "padding": "2px 6px",
            "border_radius": "4px",
            "color": "#6d28d9",  # 深紫文字
            "font_family": "'Fira Code', 'Consolas', monospace"
        },
        "code_block": {
            "font_size": "14px",
            "background_color": "#1e293b",  # 深色代码块
            "padding": "16px 18px",
            "border_radius": "8px",
            "margin": "20px 0",
            "border": "1px solid #374151",
            "line_height": "1.65",
            "color": "#e2e8f0"  # 浅色代码文字
        },
        "list": {
            "font_size": "16px",
            "margin": "14px 0",
            "padding": "0 16px 0 32px",
            "line_height": "1.8",
            "bullet_color": "#8b5cf6"
        },
        "link": {
            "color": "#7c3aed",  # 电紫
            "text_decoration": "none",
            "border_bottom": "1px dashed #a78bfa"
        },
        "strong": {
            "font_weight": "600",
            "color": "#1e293b"  # 深色强调
        },
        "separator": {
            "border_top": "2px solid #e5e7eb",
            "margin": "24px 20%"
        },
        "image": {
            "border_radius": "8px",
            "border": "1px solid #e5e7eb"
        }
    }
    
    # ========== 主题 9: 马卡龙粉色 ==========
    MACARON_PINK = {
        "name": "马卡龙粉",
        "description": "甜美温柔的马卡龙粉色系，适合情感、生活、女性向文章",
        "body": {
            "font_size": "16px",
            "line_height": "1.8",
            "color": "#5d4e60",
            "letter_spacing": "0.3px",
            "padding": "0 16px",
            "margin": "0 0 16px 0",
            "background_color": "#fef6f9"
        },
        "h1": {
            "font_size": "20px",
            "font_weight": "bold",
            "color": "#d4859a",
            "margin": "24px 0 16px 0",
            "padding": "0 16px",
            "text_align": "center"
        },
        "h2": {
            "font_size": "17px",
            "font_weight": "bold",
            "color": "#c76b8a",
            "margin": "20px 0 12px 0",
            "padding": "12px 16px",
            "background_color": "#fce4ec",
            "border_radius": "8px"
        },
        "h3": {
            "font_size": "16px",
            "font_weight": "bold",
            "color": "#ad5c7d",
            "margin": "16px 0 10px 0",
            "padding": "0 16px"
        },
        "blockquote": {
            "font_size": "15px",
            "background_color": "#fce4ec",
            "border_left": "4px solid #f8bbd9",
            "padding": "12px 16px",
            "margin": "16px 0",
            "color": "#6d5a6e",
            "line_height": "1.7"
        },
        "code_inline": {
            "font_size": "14px",
            "background_color": "#f8bbd9",
            "padding": "2px 6px",
            "border_radius": "4px",
            "color": "#ad5c7d"
        },
        "code_block": {
            "font_size": "13px",
            "background_color": "#fef6f9",
            "padding": "12px 16px",
            "border_radius": "8px",
            "margin": "16px 0",
            "border": "1px solid #f8bbd9",
            "line_height": "1.6",
            "color": "#5d4e60"
        },
        "list": {
            "font_size": "16px",
            "margin": "12px 0",
            "padding": "0 16px",
            "line_height": "1.8",
            "bullet_color": "#f8bbd9"
        },
        "link": {
            "color": "#c76b8a",
            "text_decoration": "none"
        },
        "strong": {
            "font_weight": "bold",
            "color": "#ad5c7d"
        },
        "separator": {
            "border_top": "2px solid #f8bbd9",
            "margin": "24px 20%"
        },
        "image": {
            "border_radius": "12px",
            "box_shadow": "0 4px 12px rgba(200, 100, 130, 0.15)"
        }
    }
    
    # ========== 主题 10: 马卡龙蓝色 ==========
    MACARON_BLUE = {
        "name": "马卡龙蓝",
        "description": "清新宁静的马卡龙蓝色系，适合旅行、自然、放松向文章",
        "body": {
            "font_size": "16px",
            "line_height": "1.8",
            "color": "#4a5568",
            "letter_spacing": "0.3px",
            "padding": "0 16px",
            "margin": "0 0 16px 0",
            "background_color": "#f0f9ff"
        },
        "h1": {
            "font_size": "20px",
            "font_weight": "bold",
            "color": "#4299e1",
            "margin": "24px 0 16px 0",
            "padding": "0 16px",
            "text_align": "center"
        },
        "h2": {
            "font_size": "17px",
            "font_weight": "bold",
            "color": "#3182ce",
            "margin": "20px 0 12px 0",
            "padding": "12px 16px",
            "background_color": "#dbeafe",
            "border_radius": "8px"
        },
        "h3": {
            "font_size": "16px",
            "font_weight": "bold",
            "color": "#2b6cb0",
            "margin": "16px 0 10px 0",
            "padding": "0 16px"
        },
        "blockquote": {
            "font_size": "15px",
            "background_color": "#dbeafe",
            "border_left": "4px solid #93c5fd",
            "padding": "12px 16px",
            "margin": "16px 0",
            "color": "#4a5568",
            "line_height": "1.7"
        },
        "code_inline": {
            "font_size": "14px",
            "background_color": "#bfdbfe",
            "padding": "2px 6px",
            "border_radius": "4px",
            "color": "#2b6cb0"
        },
        "code_block": {
            "font_size": "13px",
            "background_color": "#f0f9ff",
            "padding": "12px 16px",
            "border_radius": "8px",
            "margin": "16px 0",
            "border": "1px solid #bfdbfe",
            "line_height": "1.6",
            "color": "#4a5568"
        },
        "list": {
            "font_size": "16px",
            "margin": "12px 0",
            "padding": "0 16px",
            "line_height": "1.8",
            "bullet_color": "#93c5fd"
        },
        "link": {
            "color": "#3182ce",
            "text_decoration": "none"
        },
        "strong": {
            "font_weight": "bold",
            "color": "#2b6cb0"
        },
        "separator": {
            "border_top": "2px solid #bfdbfe",
            "margin": "24px 20%"
        },
        "image": {
            "border_radius": "12px",
            "box_shadow": "0 4px 12px rgba(59, 130, 246, 0.15)"
        }
    }
    
    # ========== 主题 11: 马卡龙薄荷 ==========
    MACARON_MINT = {
        "name": "马卡龙薄荷",
        "description": "清爽自然的马卡龙薄荷色系，适合健康、环保、清新向文章",
        "body": {
            "font_size": "16px",
            "line_height": "1.8",
            "color": "#3d5a5a",
            "letter_spacing": "0.3px",
            "padding": "0 16px",
            "margin": "0 0 16px 0",
            "background_color": "#f0fdfa"
        },
        "h1": {
            "font_size": "20px",
            "font_weight": "bold",
            "color": "#14b8a6",
            "margin": "24px 0 16px 0",
            "padding": "0 16px",
            "text_align": "center"
        },
        "h2": {
            "font_size": "17px",
            "font_weight": "bold",
            "color": "#0d9488",
            "margin": "20px 0 12px 0",
            "padding": "12px 16px",
            "background_color": "#ccfbf1",
            "border_radius": "8px"
        },
        "h3": {
            "font_size": "16px",
            "font_weight": "bold",
            "color": "#0f766e",
            "margin": "16px 0 10px 0",
            "padding": "0 16px"
        },
        "blockquote": {
            "font_size": "15px",
            "background_color": "#ccfbf1",
            "border_left": "4px solid #5eead4",
            "padding": "12px 16px",
            "margin": "16px 0",
            "color": "#3d5a5a",
            "line_height": "1.7"
        },
        "code_inline": {
            "font_size": "14px",
            "background_color": "#99f6e4",
            "padding": "2px 6px",
            "border_radius": "4px",
            "color": "#0f766e"
        },
        "code_block": {
            "font_size": "13px",
            "background_color": "#f0fdfa",
            "padding": "12px 16px",
            "border_radius": "8px",
            "margin": "16px 0",
            "border": "1px solid #99f6e4",
            "line_height": "1.6",
            "color": "#3d5a5a"
        },
        "list": {
            "font_size": "16px",
            "margin": "12px 0",
            "padding": "0 16px",
            "line_height": "1.8",
            "bullet_color": "#5eead4"
        },
        "link": {
            "color": "#0d9488",
            "text_decoration": "none"
        },
        "strong": {
            "font_weight": "bold",
            "color": "#0f766e"
        },
        "separator": {
            "border_top": "2px solid #99f6e4",
            "margin": "24px 20%"
        },
        "image": {
            "border_radius": "12px",
            "box_shadow": "0 4px 12px rgba(20, 184, 166, 0.15)"
        }
    }
    
    # ========== 主题 12: 马卡龙薰衣草 ==========
    MACARON_LAVENDER = {
        "name": "马卡龙薰衣草",
        "description": "浪漫优雅的马卡龙薰衣草色系，适合情感、文艺、浪漫向文章",
        "body": {
            "font_size": "16px",
            "line_height": "1.8",
            "color": "#5b4b6a",
            "letter_spacing": "0.3px",
            "padding": "0 16px",
            "margin": "0 0 16px 0",
            "background_color": "#faf5ff"
        },
        "h1": {
            "font_size": "20px",
            "font_weight": "bold",
            "color": "#a78bfa",
            "margin": "24px 0 16px 0",
            "padding": "0 16px",
            "text_align": "center"
        },
        "h2": {
            "font_size": "17px",
            "font_weight": "bold",
            "color": "#8b5cf6",
            "margin": "20px 0 12px 0",
            "padding": "12px 16px",
            "background_color": "#ede9fe",
            "border_radius": "8px"
        },
        "h3": {
            "font_size": "16px",
            "font_weight": "bold",
            "color": "#7c3aed",
            "margin": "16px 0 10px 0",
            "padding": "0 16px"
        },
        "blockquote": {
            "font_size": "15px",
            "background_color": "#ede9fe",
            "border_left": "4px solid #c4b5fd",
            "padding": "12px 16px",
            "margin": "16px 0",
            "color": "#5b4b6a",
            "line_height": "1.7"
        },
        "code_inline": {
            "font_size": "14px",
            "background_color": "#ddd6fe",
            "padding": "2px 6px",
            "border_radius": "4px",
            "color": "#7c3aed"
        },
        "code_block": {
            "font_size": "13px",
            "background_color": "#faf5ff",
            "padding": "12px 16px",
            "border_radius": "8px",
            "margin": "16px 0",
            "border": "1px solid #ddd6fe",
            "line_height": "1.6",
            "color": "#5b4b6a"
        },
        "list": {
            "font_size": "16px",
            "margin": "12px 0",
            "padding": "0 16px",
            "line_height": "1.8",
            "bullet_color": "#c4b5fd"
        },
        "link": {
            "color": "#8b5cf6",
            "text_decoration": "none"
        },
        "strong": {
            "font_weight": "bold",
            "color": "#7c3aed"
        },
        "separator": {
            "border_top": "2px solid #ddd6fe",
            "margin": "24px 20%"
        },
        "image": {
            "border_radius": "12px",
            "box_shadow": "0 4px 12px rgba(139, 92, 246, 0.15)"
        }
    }
    
    # ========== 主题 13: 马卡龙蜜桃 ==========
    MACARON_PEACH = {
        "name": "马卡龙蜜桃",
        "description": "温暖甜美的马卡龙蜜桃色系，适合美食、生活、甜品向文章",
        "body": {
            "font_size": "16px",
            "line_height": "1.8",
            "color": "#6d5a5a",
            "letter_spacing": "0.3px",
            "padding": "0 16px",
            "margin": "0 0 16px 0",
            "background_color": "#fff7ed"
        },
        "h1": {
            "font_size": "20px",
            "font_weight": "bold",
            "color": "#f97316",
            "margin": "24px 0 16px 0",
            "padding": "0 16px",
            "text_align": "center"
        },
        "h2": {
            "font_size": "17px",
            "font_weight": "bold",
            "color": "#ea580c",
            "margin": "20px 0 12px 0",
            "padding": "12px 16px",
            "background_color": "#ffedd5",
            "border_radius": "8px"
        },
        "h3": {
            "font_size": "16px",
            "font_weight": "bold",
            "color": "#c2410c",
            "margin": "16px 0 10px 0",
            "padding": "0 16px"
        },
        "blockquote": {
            "font_size": "15px",
            "background_color": "#ffedd5",
            "border_left": "4px solid #fdba74",
            "padding": "12px 16px",
            "margin": "16px 0",
            "color": "#6d5a5a",
            "line_height": "1.7"
        },
        "code_inline": {
            "font_size": "14px",
            "background_color": "#fed7aa",
            "padding": "2px 6px",
            "border_radius": "4px",
            "color": "#c2410c"
        },
        "code_block": {
            "font_size": "13px",
            "background_color": "#fff7ed",
            "padding": "12px 16px",
            "border_radius": "8px",
            "margin": "16px 0",
            "border": "1px solid #fed7aa",
            "line_height": "1.6",
            "color": "#6d5a5a"
        },
        "list": {
            "font_size": "16px",
            "margin": "12px 0",
            "padding": "0 16px",
            "line_height": "1.8",
            "bullet_color": "#fdba74"
        },
        "link": {
            "color": "#ea580c",
            "text_decoration": "none"
        },
        "strong": {
            "font_weight": "bold",
            "color": "#c2410c"
        },
        "separator": {
            "border_top": "2px solid #fed7aa",
            "margin": "24px 20%"
        },
        "image": {
            "border_radius": "12px",
            "box_shadow": "0 4px 12px rgba(249, 115, 22, 0.15)"
        }
    }
    
    # ========== 主题 14: 马卡龙柠檬 ==========
    MACARON_LEMON = {
        "name": "马卡龙柠檬",
        "description": "明亮活力的马卡龙柠檬色系，适合励志、正能量、活力向文章",
        "body": {
            "font_size": "16px",
            "line_height": "1.8",
            "color": "#5a5a3d",
            "letter_spacing": "0.3px",
            "padding": "0 16px",
            "margin": "0 0 16px 0",
            "background_color": "#fefce8"
        },
        "h1": {
            "font_size": "20px",
            "font_weight": "bold",
            "color": "#eab308",
            "margin": "24px 0 16px 0",
            "padding": "0 16px",
            "text_align": "center"
        },
        "h2": {
            "font_size": "17px",
            "font_weight": "bold",
            "color": "#ca8a04",
            "margin": "20px 0 12px 0",
            "padding": "12px 16px",
            "background_color": "#fef9c3",
            "border_radius": "8px"
        },
        "h3": {
            "font_size": "16px",
            "font_weight": "bold",
            "color": "#a16207",
            "margin": "16px 0 10px 0",
            "padding": "0 16px"
        },
        "blockquote": {
            "font_size": "15px",
            "background_color": "#fef9c3",
            "border_left": "4px solid #fde047",
            "padding": "12px 16px",
            "margin": "16px 0",
            "color": "#5a5a3d",
            "line_height": "1.7"
        },
        "code_inline": {
            "font_size": "14px",
            "background_color": "#fef08a",
            "padding": "2px 6px",
            "border_radius": "4px",
            "color": "#a16207"
        },
        "code_block": {
            "font_size": "13px",
            "background_color": "#fefce8",
            "padding": "12px 16px",
            "border_radius": "8px",
            "margin": "16px 0",
            "border": "1px solid #fef08a",
            "line_height": "1.6",
            "color": "#5a5a3d"
        },
        "list": {
            "font_size": "16px",
            "margin": "12px 0",
            "padding": "0 16px",
            "line_height": "1.8",
            "bullet_color": "#fde047"
        },
        "link": {
            "color": "#ca8a04",
            "text_decoration": "none"
        },
        "strong": {
            "font_weight": "bold",
            "color": "#a16207"
        },
        "separator": {
            "border_top": "2px solid #fef08a",
            "margin": "24px 20%"
        },
        "image": {
            "border_radius": "12px",
            "box_shadow": "0 4px 12px rgba(234, 179, 8, 0.15)"
        }
    }
    
    # ========== 主题 15: 马卡龙珊瑚 ==========
    MACARON_CORAL = {
        "name": "马卡龙珊瑚",
        "description": "热情温暖的马卡龙珊瑚色系，适合情感、热情、活力向文章",
        "body": {
            "font_size": "16px",
            "line_height": "1.8",
            "color": "#5a4a4a",
            "letter_spacing": "0.3px",
            "padding": "0 16px",
            "margin": "0 0 16px 0",
            "background_color": "#fff5f5"
        },
        "h1": {
            "font_size": "20px",
            "font_weight": "bold",
            "color": "#f87171",
            "margin": "24px 0 16px 0",
            "padding": "0 16px",
            "text_align": "center"
        },
        "h2": {
            "font_size": "17px",
            "font_weight": "bold",
            "color": "#ef4444",
            "margin": "20px 0 12px 0",
            "padding": "12px 16px",
            "background_color": "#fee2e2",
            "border_radius": "8px"
        },
        "h3": {
            "font_size": "16px",
            "font_weight": "bold",
            "color": "#dc2626",
            "margin": "16px 0 10px 0",
            "padding": "0 16px"
        },
        "blockquote": {
            "font_size": "15px",
            "background_color": "#fee2e2",
            "border_left": "4px solid #fca5a5",
            "padding": "12px 16px",
            "margin": "16px 0",
            "color": "#5a4a4a",
            "line_height": "1.7"
        },
        "code_inline": {
            "font_size": "14px",
            "background_color": "#fecaca",
            "padding": "2px 6px",
            "border_radius": "4px",
            "color": "#dc2626"
        },
        "code_block": {
            "font_size": "13px",
            "background_color": "#fff5f5",
            "padding": "12px 16px",
            "border_radius": "8px",
            "margin": "16px 0",
            "border": "1px solid #fecaca",
            "line_height": "1.6",
            "color": "#5a4a4a"
        },
        "list": {
            "font_size": "16px",
            "margin": "12px 0",
            "padding": "0 16px",
            "line_height": "1.8",
            "bullet_color": "#fca5a5"
        },
        "link": {
            "color": "#ef4444",
            "text_decoration": "none"
        },
        "strong": {
            "font_weight": "bold",
            "color": "#dc2626"
        },
        "separator": {
            "border_top": "2px solid #fecaca",
            "margin": "24px 20%"
        },
        "image": {
            "border_radius": "12px",
            "box_shadow": "0 4px 12px rgba(248, 113, 113, 0.15)"
        }
    }
    
    # ========== 主题 16: 马卡龙鼠尾草 ==========
    MACARON_SAGE = {
        "name": "马卡龙鼠尾草",
        "description": "自然清新的马卡龙鼠尾草色系，适合自然、环保、健康向文章",
        "body": {
            "font_size": "16px",
            "line_height": "1.8",
            "color": "#4a5a4a",
            "letter_spacing": "0.3px",
            "padding": "0 16px",
            "margin": "0 0 16px 0",
            "background_color": "#f0fdf4"
        },
        "h1": {
            "font_size": "20px",
            "font_weight": "bold",
            "color": "#4ade80",
            "margin": "24px 0 16px 0",
            "padding": "0 16px",
            "text_align": "center"
        },
        "h2": {
            "font_size": "17px",
            "font_weight": "bold",
            "color": "#22c55e",
            "margin": "20px 0 12px 0",
            "padding": "12px 16px",
            "background_color": "#dcfce7",
            "border_radius": "8px"
        },
        "h3": {
            "font_size": "16px",
            "font_weight": "bold",
            "color": "#16a34a",
            "margin": "16px 0 10px 0",
            "padding": "0 16px"
        },
        "blockquote": {
            "font_size": "15px",
            "background_color": "#dcfce7",
            "border_left": "4px solid #86efac",
            "padding": "12px 16px",
            "margin": "16px 0",
            "color": "#4a5a4a",
            "line_height": "1.7"
        },
        "code_inline": {
            "font_size": "14px",
            "background_color": "#bbf7d0",
            "padding": "2px 6px",
            "border_radius": "4px",
            "color": "#16a34a"
        },
        "code_block": {
            "font_size": "13px",
            "background_color": "#f0fdf4",
            "padding": "12px 16px",
            "border_radius": "8px",
            "margin": "16px 0",
            "border": "1px solid #bbf7d0",
            "line_height": "1.6",
            "color": "#4a5a4a"
        },
        "list": {
            "font_size": "16px",
            "margin": "12px 0",
            "padding": "0 16px",
            "line_height": "1.8",
            "bullet_color": "#86efac"
        },
        "link": {
            "color": "#22c55e",
            "text_decoration": "none"
        },
        "strong": {
            "font_weight": "bold",
            "color": "#16a34a"
        },
        "separator": {
            "border_top": "2px solid #bbf7d0",
            "margin": "24px 20%"
        },
        "image": {
            "border_radius": "12px",
            "box_shadow": "0 4px 12px rgba(74, 222, 128, 0.15)"
        }
    }
    
    # ========== 主题 17: 马卡龙丁香 ==========
    MACARON_LILAC = {
        "name": "马卡龙丁香",
        "description": "优雅浪漫的马卡龙丁香色系，适合情感、文艺、优雅向文章",
        "body": {
            "font_size": "16px",
            "line_height": "1.8",
            "color": "#5a4a5a",
            "letter_spacing": "0.3px",
            "padding": "0 16px",
            "margin": "0 0 16px 0",
            "background_color": "#fdf4ff"
        },
        "h1": {
            "font_size": "20px",
            "font_weight": "bold",
            "color": "#d946ef",
            "margin": "24px 0 16px 0",
            "padding": "0 16px",
            "text_align": "center"
        },
        "h2": {
            "font_size": "17px",
            "font_weight": "bold",
            "color": "#c026d3",
            "margin": "20px 0 12px 0",
            "padding": "12px 16px",
            "background_color": "#fae8ff",
            "border_radius": "8px"
        },
        "h3": {
            "font_size": "16px",
            "font_weight": "bold",
            "color": "#a21caf",
            "margin": "16px 0 10px 0",
            "padding": "0 16px"
        },
        "blockquote": {
            "font_size": "15px",
            "background_color": "#fae8ff",
            "border_left": "4px solid #e879f9",
            "padding": "12px 16px",
            "margin": "16px 0",
            "color": "#5a4a5a",
            "line_height": "1.7"
        },
        "code_inline": {
            "font_size": "14px",
            "background_color": "#f5d0fe",
            "padding": "2px 6px",
            "border_radius": "4px",
            "color": "#a21caf"
        },
        "code_block": {
            "font_size": "13px",
            "background_color": "#fdf4ff",
            "padding": "12px 16px",
            "border_radius": "8px",
            "margin": "16px 0",
            "border": "1px solid #f5d0fe",
            "line_height": "1.6",
            "color": "#5a4a5a"
        },
        "list": {
            "font_size": "16px",
            "margin": "12px 0",
            "padding": "0 16px",
            "line_height": "1.8",
            "bullet_color": "#e879f9"
        },
        "link": {
            "color": "#c026d3",
            "text_decoration": "none"
        },
        "strong": {
            "font_weight": "bold",
            "color": "#a21caf"
        },
        "separator": {
            "border_top": "2px solid #f5d0fe",
            "margin": "24px 20%"
        },
        "image": {
            "border_radius": "12px",
            "box_shadow": "0 4px 12px rgba(217, 70, 239, 0.15)"
        }
    }
    
    # ========== 主题 18: 马卡龙奶油 ==========
    MACARON_CREAM = {
        "name": "马卡龙奶油",
        "description": "柔和温暖的马卡龙奶油色系，适合温馨、治愈、生活向文章",
        "body": {
            "font_size": "16px",
            "line_height": "1.8",
            "color": "#5a5550",
            "letter_spacing": "0.3px",
            "padding": "0 16px",
            "margin": "0 0 16px 0",
            "background_color": "#fffbeb"
        },
        "h1": {
            "font_size": "20px",
            "font_weight": "bold",
            "color": "#d4a574",
            "margin": "24px 0 16px 0",
            "padding": "0 16px",
            "text_align": "center"
        },
        "h2": {
            "font_size": "17px",
            "font_weight": "bold",
            "color": "#c4956a",
            "margin": "20px 0 12px 0",
            "padding": "12px 16px",
            "background_color": "#fef3c7",
            "border_radius": "8px"
        },
        "h3": {
            "font_size": "16px",
            "font_weight": "bold",
            "color": "#b8860b",
            "margin": "16px 0 10px 0",
            "padding": "0 16px"
        },
        "blockquote": {
            "font_size": "15px",
            "background_color": "#fef3c7",
            "border_left": "4px solid #fcd34d",
            "padding": "12px 16px",
            "margin": "16px 0",
            "color": "#5a5550",
            "line_height": "1.7"
        },
        "code_inline": {
            "font_size": "14px",
            "background_color": "#fde68a",
            "padding": "2px 6px",
            "border_radius": "4px",
            "color": "#b8860b"
        },
        "code_block": {
            "font_size": "13px",
            "background_color": "#fffbeb",
            "padding": "12px 16px",
            "border_radius": "8px",
            "margin": "16px 0",
            "border": "1px solid #fde68a",
            "line_height": "1.6",
            "color": "#5a5550"
        },
        "list": {
            "font_size": "16px",
            "margin": "12px 0",
            "padding": "0 16px",
            "line_height": "1.8",
            "bullet_color": "#fcd34d"
        },
        "link": {
            "color": "#c4956a",
            "text_decoration": "none"
        },
        "strong": {
            "font_weight": "bold",
            "color": "#b8860b"
        },
        "separator": {
            "border_top": "2px solid #fde68a",
            "margin": "24px 20%"
        },
        "image": {
            "border_radius": "12px",
            "box_shadow": "0 4px 12px rgba(212, 165, 116, 0.15)"
        }
    }
    
    # ========== 主题 19: 马卡龙天空 ==========
    MACARON_SKY = {
        "name": "马卡龙天空",
        "description": "清新明亮的马卡龙天空色系，适合旅行、自由、梦想向文章",
        "body": {
            "font_size": "16px",
            "line_height": "1.8",
            "color": "#4a5060",
            "letter_spacing": "0.3px",
            "padding": "0 16px",
            "margin": "0 0 16px 0",
            "background_color": "#f0f9ff"
        },
        "h1": {
            "font_size": "20px",
            "font_weight": "bold",
            "color": "#38bdf8",
            "margin": "24px 0 16px 0",
            "padding": "0 16px",
            "text_align": "center"
        },
        "h2": {
            "font_size": "17px",
            "font_weight": "bold",
            "color": "#0ea5e9",
            "margin": "20px 0 12px 0",
            "padding": "12px 16px",
            "background_color": "#e0f2fe",
            "border_radius": "8px"
        },
        "h3": {
            "font_size": "16px",
            "font_weight": "bold",
            "color": "#0284c7",
            "margin": "16px 0 10px 0",
            "padding": "0 16px"
        },
        "blockquote": {
            "font_size": "15px",
            "background_color": "#e0f2fe",
            "border_left": "4px solid #7dd3fc",
            "padding": "12px 16px",
            "margin": "16px 0",
            "color": "#4a5060",
            "line_height": "1.7"
        },
        "code_inline": {
            "font_size": "14px",
            "background_color": "#bae6fd",
            "padding": "2px 6px",
            "border_radius": "4px",
            "color": "#0284c7"
        },
        "code_block": {
            "font_size": "13px",
            "background_color": "#f0f9ff",
            "padding": "12px 16px",
            "border_radius": "8px",
            "margin": "16px 0",
            "border": "1px solid #bae6fd",
            "line_height": "1.6",
            "color": "#4a5060"
        },
        "list": {
            "font_size": "16px",
            "margin": "12px 0",
            "padding": "0 16px",
            "line_height": "1.8",
            "bullet_color": "#7dd3fc"
        },
        "link": {
            "color": "#0ea5e9",
            "text_decoration": "none"
        },
        "strong": {
            "font_weight": "bold",
            "color": "#0284c7"
        },
        "separator": {
            "border_top": "2px solid #bae6fd",
            "margin": "24px 20%"
        },
        "image": {
            "border_radius": "12px",
            "box_shadow": "0 4px 12px rgba(56, 189, 248, 0.15)"
        }
    }
    
    # ========== 主题 20: 马卡龙玫瑰 ==========
    MACARON_ROSE = {
        "name": "马卡龙玫瑰",
        "description": "浪漫精致的马卡龙玫瑰色系，适合情感、浪漫、精致向文章",
        "body": {
            "font_size": "16px",
            "line_height": "1.8",
            "color": "#5a4a50",
            "letter_spacing": "0.3px",
            "padding": "0 16px",
            "margin": "0 0 16px 0",
            "background_color": "#fdf2f8"
        },
        "h1": {
            "font_size": "20px",
            "font_weight": "bold",
            "color": "#ec4899",
            "margin": "24px 0 16px 0",
            "padding": "0 16px",
            "text_align": "center"
        },
        "h2": {
            "font_size": "17px",
            "font_weight": "bold",
            "color": "#db2777",
            "margin": "20px 0 12px 0",
            "padding": "12px 16px",
            "background_color": "#fce7f3",
            "border_radius": "8px"
        },
        "h3": {
            "font_size": "16px",
            "font_weight": "bold",
            "color": "#be185d",
            "margin": "16px 0 10px 0",
            "padding": "0 16px"
        },
        "blockquote": {
            "font_size": "15px",
            "background_color": "#fce7f3",
            "border_left": "4px solid #f9a8d4",
            "padding": "12px 16px",
            "margin": "16px 0",
            "color": "#5a4a50",
            "line_height": "1.7"
        },
        "code_inline": {
            "font_size": "14px",
            "background_color": "#fbcfe8",
            "padding": "2px 6px",
            "border_radius": "4px",
            "color": "#be185d"
        },
        "code_block": {
            "font_size": "13px",
            "background_color": "#fdf2f8",
            "padding": "12px 16px",
            "border_radius": "8px",
            "margin": "16px 0",
            "border": "1px solid #fbcfe8",
            "line_height": "1.6",
            "color": "#5a4a50"
        },
        "list": {
            "font_size": "16px",
            "margin": "12px 0",
            "padding": "0 16px",
            "line_height": "1.8",
            "bullet_color": "#f9a8d4"
        },
        "link": {
            "color": "#db2777",
            "text_decoration": "none"
        },
        "strong": {
            "font_weight": "bold",
            "color": "#be185d"
        },
        "separator": {
            "border_top": "2px solid #fbcfe8",
            "margin": "24px 20%"
        },
        "image": {
            "border_radius": "12px",
            "box_shadow": "0 4px 12px rgba(236, 72, 153, 0.15)"
        }
    }
    
    # 主题关键词映射 - 用于自动推荐
    THEME_KEYWORDS = {
        "minimal_business": [
            "商业", "职场", "管理", "战略", "分析", "数据", "行业", "市场",
            "企业", "创业", "投资", "金融", "经济", "报告", "趋势", "business",
            "management", "strategy", "analysis", "职场", "干货", "方法论"
        ],
        "warm_artistic": [
            "生活", "情感", "读书", "文学", "散文", "随笔", "故事", "人生",
            "感悟", "思考", "阅读", "书籍", "电影", "音乐", "艺术", "美学",
            "生活方式", "慢生活", "治愈", "温暖", "柔软", "细腻"
        ],
        "tech_modern": [
            "技术", "编程", "代码", "开发", "算法", "AI", "人工智能", "机器学习",
            "深度学习", "Python", "JavaScript", "前端", "后端", "架构", "系统",
            "教程", "指南", "工具", "软件", "数码", "科技", "互联网", "产品"
        ],
        "fresh_lively": [
            "美食", "旅行", "探店", "打卡", "穿搭", "时尚", "护肤", "美妆",
            "健身", "运动", "瑜伽", "跑步", "咖啡", "甜品", "餐厅", "景点",
            "攻略", "推荐", "种草", "生活方式", "日常", "Vlog", "Plog"
        ],
        "magazine_premium": [
            "时尚", "奢侈品", "设计", "建筑", "摄影", "艺术", "展览", "博物馆",
            "深度", "长文", "专访", "人物", "品牌", "文化", "历史", "哲学",
            "思考", "观察", "评论", "批评", "审美", "品味", "格调"
        ],
        "academic_professional": [
            "论文", "学术", "研究", "分析", "报告", "学位", "毕业", "科研",
            "大学", "学院", "教授", "博士", "硕士", "论文", "期刊", "发表",
            "实验", "数据", "方法", "结论", "参考文献", "citation", "research"
        ],
        "retro_classic": [
            "历史", "传统", "文化", "复古", "怀旧", "经典", "回忆", "年代",
            "老照片", "往事", "记忆", "童年", "故乡", "民俗", "古风", "传承",
            "岁月", "时光", "纪念", "回顾", "heritage", "vintage", "classic"
        ],
        "geek_tech": [
            "游戏", "电竞", "二次元", "动漫", "极客", "赛博",
            "科幻", "未来", "虚拟", "电子", "像素", "独立游戏", "手游", "端游",
            "steam", "switch", "playstation", "xbox", "gaming", "esports"
        ],
        # ===== 马卡龙主题关键词 =====
        "macaron_pink": [
            "女性", "少女", "甜美", "温柔", "粉色", "浪漫", "恋爱", "情感",
            "闺蜜", "美妆", "护肤", "穿搭", "约会", "心情", "日记", "pink",
            "sweet", "gentle", "romance", "少女心", "温柔风"
        ],
        "macaron_blue": [
            "清新", "宁静", "放松", "旅行", "自然", "海洋", "天空", "平静",
            "治愈", "清新", "海边", "度假", "慢生活", "蓝天", "大海", "blue",
            "calm", "peaceful", "relax", "清新风"
        ],
        "macaron_mint": [
            "健康", "环保", "清新", "自然", "植物", "绿茶", "瑜伽", "养生",
            "有机", "绿色", "生态", "环保生活", "健康饮食", "清新感", "mint",
            "fresh", "nature", "healthy", "清新自然"
        ],
        "macaron_lavender": [
            "浪漫", "优雅", "文艺", "梦幻", "紫色", "薰衣草", "法式", "田园",
            "诗意", "优雅感", "浪漫风", "文艺风", "梦幻感", "lavender",
            "elegant", "dreamy", "romantic", "浪漫优雅"
        ],
        "macaron_peach": [
            "美食", "甜品", "下午茶", "温暖", "甜美", "柔和", "温馨", "家庭",
            "烘焙", "甜点", "温暖感", "治愈系", "蜜桃", "peach", "warm",
            "sweet", "cozy", "温暖甜美"
        ],
        "macaron_lemon": [
            "活力", "正能量", "励志", "阳光", "明亮", "清新", "能量", "积极",
            "奋斗", "希望", "快乐", "青春", "柠檬", "lemon", "energy",
            "positive", "bright", "sunny", "活力满满"
        ],
        "macaron_coral": [
            "热情", "活力", "夏日", "海滩", "热带", "激情", "运动", "活泼",
            "珊瑚", "暖色", "热情风", "活力风", "coral", "passion",
            "tropical", "vibrant", "热情活力"
        ],
        "macaron_sage": [
            "自然", "环保", "户外", "植物", "森林", "田园", "质朴", "简约",
            "鼠尾草", "森系", "自然风", "环保生活", "sage", "natural",
            "organic", "forest", "自然清新"
        ],
        "macaron_lilac": [
            "优雅", "浪漫", "文艺", "精致", "女性", "轻奢", "优雅感", "品味",
            "丁香", "紫调", "优雅风", "精致生活", "lilac", "refined",
            "sophisticated", "优雅浪漫"
        ],
        "macaron_cream": [
            "温馨", "治愈", "柔和", "家庭", "生活", "简单", "舒适", "日常",
            "奶油", "暖调", "温馨感", "治愈系", "cream", "warm",
            "comfortable", "cozy", "温馨治愈"
        ],
        "macaron_sky": [
            "旅行", "自由", "梦想", "天空", "飞行", "希望", "开阔", "蓝天",
            "云朵", "自由感", "梦想家", "旅行者", "sky", "freedom",
            "dream", "horizon", "清新明亮"
        ],
        "macaron_rose": [
            "浪漫", "爱情", "精致", "女性", "优雅", "玫瑰", "约会", "纪念日",
            "情侣", "表白", "浪漫风", "精致感", "rose", "love",
            "romantic", "elegant", "浪漫精致"
        ]
    }
    
    @classmethod
    def get_all_themes(cls):
        """获取所有可用主题"""
        return {
            # 原有 8 个主题
            "minimal_business": cls.MINIMAL_BUSINESS,
            "warm_artistic": cls.WARM_ARTISTIC,
            "tech_modern": cls.TECH_MODERN,
            "fresh_lively": cls.FRESH_LIVELY,
            "magazine_premium": cls.MAGAZINE_PREMIUM,
            "academic_professional": cls.ACADEMIC_PROFESSIONAL,
            "retro_classic": cls.RETRO_CLASSIC,
            "geek_tech": cls.GEEK_TECH,
            # 马卡龙主题 12 个
            "macaron_pink": cls.MACARON_PINK,
            "macaron_blue": cls.MACARON_BLUE,
            "macaron_mint": cls.MACARON_MINT,
            "macaron_lavender": cls.MACARON_LAVENDER,
            "macaron_peach": cls.MACARON_PEACH,
            "macaron_lemon": cls.MACARON_LEMON,
            "macaron_coral": cls.MACARON_CORAL,
            "macaron_sage": cls.MACARON_SAGE,
            "macaron_lilac": cls.MACARON_LILAC,
            "macaron_cream": cls.MACARON_CREAM,
            "macaron_sky": cls.MACARON_SKY,
            "macaron_rose": cls.MACARON_ROSE
        }
    
    @classmethod
    def get_theme(cls, theme_name):
        """获取指定主题"""
        themes = cls.get_all_themes()
        return themes.get(theme_name, cls.MINIMAL_BUSINESS)
    
    @classmethod
    def list_themes(cls):
        """列出所有主题名称和描述"""
        themes = cls.get_all_themes()
        return {k: {"name": v["name"], "description": v["description"]} 
                for k, v in themes.items()}
    
    @classmethod
    def recommend_theme(cls, content: str, title: str = "") -> tuple:
        """
        根据内容自动推荐主题
        
        Returns:
            (theme_id, confidence, reason)
        """
        text = (title + " " + content).lower()
        scores = {}
        
        for theme_id, keywords in cls.THEME_KEYWORDS.items():
            score = 0
            matched_keywords = []
            for keyword in keywords:
                count = text.count(keyword.lower())
                if count > 0:
                    score += count
                    matched_keywords.append(keyword)
            scores[theme_id] = {
                "score": score,
                "keywords": matched_keywords
            }
        
        # 排序找最高分
        sorted_themes = sorted(scores.items(), key=lambda x: x[1]["score"], reverse=True)
        
        if sorted_themes[0][1]["score"] == 0:
            # 没有匹配到关键词，默认用极简商务
            return "minimal_business", 0.3, "未检测到明确主题特征，默认使用极简商务风格"
        
        best_theme = sorted_themes[0]
        theme_id = best_theme[0]
        score = best_theme[1]["score"]
        keywords = best_theme[1]["keywords"][:3]  # 最多显示3个匹配词
        
        # 计算置信度
        total_score = sum(s["score"] for s in scores.values())
        confidence = score / total_score if total_score > 0 else 0
        
        theme_name = cls.get_theme(theme_id)["name"]
        reason = f"检测到关键词：{', '.join(keywords)}，适合{theme_name}风格"
        
        return theme_id, confidence, reason


class WeChatHTMLConverter:
    """微信公众号 HTML 转换器 - 支持多主题"""
    
    # 微信安全标签白名单
    SAFE_TAGS = {
        'p', 'br', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
        'strong', 'b', 'em', 'i', 'span', 'a', 'img',
        'ul', 'ol', 'li', 'section', 'blockquote',
        'pre', 'code'
    }
    
    # 支持的 CSS 属性
    SAFE_CSS = {
        'color', 'font-size', 'font-weight', 'font-family',
        'text-align', 'line-height', 'background-color',
        'padding', 'margin', 'border', 'border-radius',
        'border-left', 'border-right', 'border-top', 'border-bottom',
        'display', 'max-width', 'height', 'overflow-x', 'white-space', 
        'word-wrap', 'text-decoration', 'letter-spacing', 'text-shadow',
        'text-transform', 'font-style', 'padding-left', 'padding-right',
        'padding-top', 'padding-bottom', 'position'
    }
    
    def __init__(self, theme="minimal_business"):
        self.toc = []  # 目录
        self.heading_counter = 0
        self.theme = ThemePresets.get_theme(theme)
    
    def set_theme(self, theme_name):
        """切换主题"""
        self.theme = ThemePresets.get_theme(theme_name)
    
    def _style_to_str(self, style_dict):
        """将样式字典转换为 CSS 字符串"""
        if not style_dict:
            return ""
        return "; ".join([f"{k.replace('_', '-')}: {v}" for k, v in style_dict.items()])
    
    def escape_html(self, text):
        """转义 HTML 特殊字符"""
        return html_module.escape(text, quote=False)
    
    def convert(self, markdown_text):
        """
        将 Markdown 转换为微信安全的 HTML
        """
        html_content = markdown_text
        
        # 1. 处理代码块（优先处理，避免内部内容被转换）
        html_content = self._process_code_blocks(html_content)
        
        # 2. 处理标题
        html_content = self._process_headings(html_content)
        
        # 3. 处理粗体和斜体
        html_content = self._process_emphasis(html_content)
        
        # 4. 处理行内代码
        html_content = self._process_inline_code(html_content)
        
        # 5. 处理链接
        html_content = self._process_links(html_content)
        
        # 6. 处理图片
        html_content = self._process_images(html_content)
        
        # 7. 处理列表
        html_content = self._process_lists(html_content)
        
        # 8. 处理表格（在引用块之前处理）
        html_content = self._process_tables(html_content)
        
        # 9. 处理引用块
        html_content = self._process_blockquotes(html_content)
        
        # 9. 处理分隔线
        html_content = self._process_hr(html_content)
        
        # 10. 处理段落
        html_content = self._process_paragraphs(html_content)
        
        # 11. 清理空标签和多余换行
        html_content = self._cleanup(html_content)
        
        return html_content
    
    def _process_code_blocks(self, text):
        """处理代码块 - 使用主题样式"""
        pattern = r'```(\w+)?\n(.*?)```'
        style = self._style_to_str(self.theme.get("code_block", {}))
        
        def replace_code_block(match):
            lang = match.group(1) or ''
            code = match.group(2)
            code_escaped = self.escape_html(code)
            
            return f'''<pre style="{style}; overflow-x: auto; font-family: 'Courier New', monospace;">
<code style="display: block;">{code_escaped}</code>
</pre>'''
        
        return re.sub(pattern, replace_code_block, text, flags=re.DOTALL)
    
    def _process_headings(self, text):
        """处理标题 - 使用主题样式"""
        h1_style = self._style_to_str(self.theme.get("h1", {}))
        h2_style = self._style_to_str(self.theme.get("h2", {}))
        h3_style = self._style_to_str(self.theme.get("h3", {}))
        
        # H1
        text = re.sub(
            r'^# (.+)$',
            lambda m: f'<h1 style="{h1_style}">{self.escape_html(m.group(1))}</h1>',
            text,
            flags=re.MULTILINE
        )
        
        # H2
        text = re.sub(
            r'^## (.+)$',
            lambda m: f'<h2 style="{h2_style}">{self.escape_html(m.group(1))}</h2>',
            text,
            flags=re.MULTILINE
        )
        
        # H3
        text = re.sub(
            r'^### (.+)$',
            lambda m: f'<h3 style="{h3_style}">{self.escape_html(m.group(1))}</h3>',
            text,
            flags=re.MULTILINE
        )
        
        # H4-H6 使用 H3 样式
        text = re.sub(
            r'^#### (.+)$',
            lambda m: f'<h4 style="{h3_style}">{self.escape_html(m.group(1))}</h4>',
            text,
            flags=re.MULTILINE
        )
        
        return text
    
    def _process_emphasis(self, text):
        """处理粗体和斜体 - 使用主题样式"""
        strong_style = self._style_to_str(self.theme.get("strong", {}))
        
        # 粗体 **text**
        text = re.sub(
            r'\*\*(.+?)\*\*',
            lambda m: f'<strong style="{strong_style}">{self.escape_html(m.group(1))}</strong>',
            text
        )
        
        # 斜体 *text* - 使用主题文字颜色
        text_color = self.theme.get("body", {}).get("color", "#4a4a4a")
        text = re.sub(
            r'\*(.+?)\*',
            lambda m: f'<em style="font-style: italic; color: {text_color};">{self.escape_html(m.group(1))}</em>',
            text
        )
        
        return text
    
    def _process_inline_code(self, text):
        """处理行内代码 - 使用主题样式"""
        style = self._style_to_str(self.theme.get("code_inline", {}))
        return re.sub(
            r'`(.+?)`',
            lambda m: f'<code style="{style}">{self.escape_html(m.group(1))}</code>',
            text
        )
    
    def _process_links(self, text):
        """处理链接 - 使用主题样式"""
        style = self._style_to_str(self.theme.get("link", {}))
        return re.sub(
            r'\[([^\]]+)\]\(([^)]+)\)',
            lambda m: f'<a href="{m.group(2)}" style="{style}">{self.escape_html(m.group(1))}</a>',
            text
        )
    
    def _process_images(self, text):
        """处理图片 - 优化移动端显示"""
        # ![alt](url)
        # 根据主题获取图片样式
        img_border_radius = self.theme.get("image", {}).get("border_radius", "8px")
        img_shadow = self.theme.get("image", {}).get("box_shadow", "none")
        
        shadow_style = f"box-shadow: {img_shadow};" if img_shadow != "none" else ""
        
        return re.sub(
            r'!\[([^\]]*)\]\(([^)]+)\)',
            lambda m: f'<p style="text-align: center; margin: 20px 0; padding: 0 16px;"><img src="{m.group(2)}" alt="{self.escape_html(m.group(1))}" style="max-width: 100%; height: auto; display: block; margin: 0 auto; border-radius: {img_border_radius}; {shadow_style}"></p>',
            text
        )
    
    def _process_lists(self, text):
        """处理列表 - 使用主题样式"""
        lines = text.split('\n')
        result = []
        in_ul = False
        in_ol = False
        
        list_style = self.theme.get("list", {})
        list_style_str = self._style_to_str(list_style)
        bullet_color = list_style.get("bullet_color", "#4a90d9")
        font_size = list_style.get("font_size", "15px")
        line_height = list_style.get("line_height", "1.75")
        text_color = self.theme.get("body", {}).get("color", "#333")
        
        for line in lines:
            ul_match = re.match(r'^[\s]*[-\*] (.+)$', line)
            ol_match = re.match(r'^[\s]*(\d+)\. (.+)$', line)
            
            if ul_match:
                if not in_ul:
                    if in_ol:
                        result.append('</ol>')
                        in_ol = False
                    result.append(f'<ul style="{list_style_str}; list-style: none;">')
                    in_ul = True
                content = ul_match.group(1)
                result.append(f'<li style="margin: 6px 0; line-height: {line_height}; color: {text_color}; padding-left: 20px; position: relative;"><span style="position: absolute; left: 0; color: {bullet_color}; font-size: {font_size};">·</span>{content}</li>')
            
            elif ol_match:
                if not in_ol:
                    if in_ul:
                        result.append('</ul>')
                        in_ul = False
                    result.append(f'<ol style="{list_style_str}; list-style: none; counter-reset: item;">')
                    in_ol = True
                content = ol_match.group(2)
                num = ol_match.group(1)
                result.append(f'<li style="margin: 6px 0; line-height: {line_height}; color: {text_color}; padding-left: 30px; position: relative;"><span style="position: absolute; left: 0; color: {bullet_color}; font-weight: bold; font-size: {font_size};">{num}.</span>{content}</li>')
            
            else:
                if in_ul:
                    result.append('</ul>')
                    in_ul = False
                if in_ol:
                    result.append('</ol>')
                    in_ol = False
                result.append(line)
        
        if in_ul:
            result.append('</ul>')
        if in_ol:
            result.append('</ol>')
        
        return '\n'.join(result)
    
    def _process_blockquotes(self, text):
        """处理引用块 - 使用主题样式"""
        lines = text.split('\n')
        result = []
        in_quote = False
        quote_content = []
        
        style = self._style_to_str(self.theme.get("blockquote", {}))
        
        for line in lines:
            quote_match = re.match(r'^[\s]*> (.+)$', line)
            
            if quote_match:
                if not in_quote:
                    in_quote = True
                    quote_content = []
                quote_content.append(quote_match.group(1))
            else:
                if in_quote:
                    content = '<br>'.join(quote_content)
                    result.append(f'<blockquote style="{style}">{content}</blockquote>')
                    in_quote = False
                    quote_content = []
                result.append(line)
        
        if in_quote:
            content = '<br>'.join(quote_content)
            result.append(f'<blockquote style="{style}">{content}</blockquote>')
        
        return '\n'.join(result)
    
    def _process_hr(self, text):
        """处理分隔线 - 使用主题样式"""
        style = self._style_to_str(self.theme.get("separator", {}))
        return re.sub(
            r'^[\s]*[-\*_]{3,}[\s]*$',
            f'<section style="{style}"></section>',
            text,
            flags=re.MULTILINE
        )
    
    def _process_tables(self, text):
        """处理 Markdown 表格 - 微信不支持table，转换为更美观的列表形式"""
        lines = text.split('\n')
        result = []
        i = 0
        
        while i < len(lines):
            line = lines[i].strip()
            
            # 检测表格开始（包含 | 的行，且不是引用块）
            if '|' in line and not line.startswith('>'):
                # 收集表格所有行
                table_lines = []
                while i < len(lines) and '|' in lines[i]:
                    table_lines.append(lines[i].strip())
                    i += 1
                
                # 解析表格
                if len(table_lines) >= 2:  # 至少需要表头和分隔行
                    # 过滤掉分隔行（包含 --- 的行）
                    content_rows = [row for row in table_lines if not re.match(r'^\|?[\s\-:|]+\|?$', row)]
                    
                    if content_rows and len(content_rows) >= 2:
                        # 获取表头
                        header_cells = [cell.strip() for cell in content_rows[0].split('|') if cell.strip()]
                        
                        # 将表格转换为更美观的列表形式展示
                        html_list = []
                        
                        # 添加一个小标题说明
                        html_list.append('<p style="font-size: 15px; margin: 16px 0; line-height: 1.75; color: #333; text-align: justify; letter-spacing: 1px; padding: 0 16px;"><strong style="font-weight: bold; color: #1a1a1a;">排版参数：</strong></p>')
                        
                        html_list.append('<ul style="font-size: 15px; margin: 16px 0; padding-left: 0; list-style: none; line-height: 1.75; letter-spacing: 1px; padding: 0 16px;">')
                        
                        # 数据行（跳过表头，从第二行开始）
                        for row in content_rows[1:]:
                            cells = [cell.strip() for cell in row.split('|') if cell.strip()]
                            if cells:
                                # 将每行数据格式化为 参数 → 数值 的形式
                                if len(cells) >= 2:
                                    param = cells[0]
                                    value = cells[1]
                                    formatted = f"<strong style='color: #4a90d9;'>{self.escape_html(param)}</strong>：{self.escape_html(value)}"
                                else:
                                    formatted = self.escape_html(" | ".join(cells))
                                html_list.append(f'<li style="margin: 6px 0; line-height: 1.75; color: #333; padding-left: 20px; position: relative; letter-spacing: 1px;"><span style="position: absolute; left: 0; color: #4a90d9; font-size: 15px;">·</span>{formatted}</li>')
                        
                        html_list.append('</ul>')
                        result.append('\n'.join(html_list))
                    elif content_rows and len(content_rows) == 1:
                        # 只有一行，作为普通文本
                        result.append(content_rows[0])
                continue
            
            result.append(lines[i])
            i += 1
        
        return '\n'.join(result)
    
    def _process_paragraphs(self, text):
        """处理段落 - 使用主题样式"""
        lines = text.split('\n')
        result = []
        paragraph = []
        
        style = self._style_to_str(self.theme.get("body", {}))
        
        for line in lines:
            stripped = line.strip()
            
            # 如果已经是 HTML 标签，直接添加
            if stripped.startswith('<') and stripped.endswith('>'):
                if paragraph:
                    content = ' '.join(paragraph)
                    if content:
                        result.append(f'<p style="{style}">{content}</p>')
                    paragraph = []
                result.append(line)
            elif stripped:
                paragraph.append(stripped)
            else:
                # 空行，结束段落
                if paragraph:
                    content = ' '.join(paragraph)
                    result.append(f'<p style="{style}">{content}</p>')
                    paragraph = []
        
        # 处理最后一个段落
        if paragraph:
            content = ' '.join(paragraph)
            result.append(f'<p style="{style}">{content}</p>')
        
        return '\n'.join(result)
    
    def _cleanup(self, text):
        """清理空标签和多余内容 - 只保留一个空行"""
        # 移除空的 p 标签
        text = re.sub(r'<p[^>]*>[\s]*</p>', '', text)
        
        # 合并多个换行为一个
        text = re.sub(r'\n{2,}', '\n', text)
        
        # 移除行首行尾空白
        lines = text.split('\n')
        lines = [line.strip() for line in lines]
        text = '\n'.join(lines)
        
        return text.strip()


def convert_markdown_to_wechat_html(markdown_text, theme="minimal_business"):
    """
    便捷函数：将 Markdown 转换为微信 HTML
    
    Args:
        markdown_text: Markdown 文本
        theme: 主题名称，可选：minimal_business, warm_artistic, tech_modern, fresh_lively, magazine_premium
    """
    converter = WeChatHTMLConverter(theme=theme)
    return converter.convert(markdown_text)


def list_available_themes():
    """列出所有可用主题"""
    return ThemePresets.list_themes()


# 测试
if __name__ == "__main__":
    test_md = """
# 测试文章

这是一段普通文字，**加粗**，*斜体*。

## 代码示例

```python
print("Hello, World!")
```

### 列表

- 项目1
- 项目2
- 项目3

> 这是一段引用

[链接](https://example.com)

---

分隔线测试
"""
    
    print("=" * 60)
    print("可用主题列表：")
    print("=" * 60)
    for theme_id, info in list_available_themes().items():
        print(f"\n🎨 {theme_id}")
        print(f"   名称: {info['name']}")
        print(f"   描述: {info['description']}")
    
    print("\n" + "=" * 60)
    print("各主题预览（H1标题样式）：")
    print("=" * 60)
    
    for theme_id in list_available_themes().keys():
        converter = WeChatHTMLConverter(theme=theme_id)
        html = converter.convert("# 主题预览\n\n这是一段测试文字**加粗显示**")
        print(f"\n--- {theme_id} ---")
        print(html[:300] + "...")
