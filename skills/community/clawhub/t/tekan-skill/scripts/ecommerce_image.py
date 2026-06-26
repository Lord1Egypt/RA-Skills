#!/usr/bin/env python3
from __future__ import annotations

"""E-commerce image generation via Tekan image_all_in_one APIs.

## AGENT INSTRUCTIONS — READ FIRST
- Default workflow: ALWAYS use `run` (submit + auto-poll).
  Do NOT ask the user to run query manually.
- Only use `query` when `run` has already timed out and a taskId exists,
  or when the user explicitly provides a taskId to resume.
- Read references/ecommerce_image.md for Agent behavior rules:
  module selection strategy, selling-point strategy, batch confirmation.
- Never hand a pending taskId back to the user — always poll to completion.

Supported tool types (--tool-type):
    product_detail_image           商品详情图
    product_main_image_ecomm       商品主图
    virtual_try_on_ecomm           虚拟穿搭
    garment_detail_view_ecomm      服装细节图
    product_3d_render_ecomm        商品3D图
    background_replacement_ecomm   商品换背景
    image_retouching_ecomm         商品图精修
    product_flat_lay_ecomm         商品平铺图
    product_set_images_ecomm       商品套图
    lifestyle_fashion_photo_ecomm  服装种草图
    smart_watermark_removal_ecomm  智能去水印
    texture_enhancement_ecomm      服装材质增强
    trending_style_set_ecomm       爆款套图

Subcommands:
    run                  Submit + poll until done — DEFAULT, use this first
    submit               Submit only, print taskId, exit
    query                Poll an existing taskId until done
    list-tools           List all 13 tool types
    list-modules         List 16 detail modules (product_detail_image only)
    extract-selling-points  Extract selling points only (product_detail_image)
    estimate-cost        Estimate credit cost

Usage:
    python ecommerce_image.py run --tool-type product_detail_image --images product.jpg \\
        --modules hero,selling_points,multi_angle --board-id <id>
    python ecommerce_image.py list-tools
    python ecommerce_image.py list-modules
"""

import argparse
import json as json_mod
import os
import sys
import tempfile
import time
from typing import Optional

sys.path.insert(0, os.path.dirname(__file__))

import requests as _requests

from shared.client import (
    TopviewClient, TopviewError, TEKAN_API_URL,
    TEKAN_CREDIT_MULTIPLIER, to_tekan_credit, convert_result_credits,
    shorten_url,
)
from shared.upload import (
    upload_and_get_url, resolve_local_file, TEKAN_S3_API_URL,
    ecommerce_upload, get_file_url, detect_format,
)

ECOMMERCE_API_URL = TEKAN_S3_API_URL

# ---------------------------------------------------------------------------
# Detail modules (product_detail_image only)
# ---------------------------------------------------------------------------

DETAIL_MODULES = [
    {"id": "hero",            "name": "首页主视觉"},
    {"id": "selling_points",  "name": "核心卖点图"},
    {"id": "model_efficacy",  "name": "痛点共鸣图"},
    {"id": "multi_angle",     "name": "产品多角度"},
    {"id": "vibe",            "name": "氛围展示图"},
    {"id": "texture_detail",  "name": "细节微距图"},
    {"id": "ingredient_core", "name": "核心成分图"},
    {"id": "clinical_data",   "name": "科研数据图"},
    {"id": "contrast",        "name": "前后对比图"},
    {"id": "specs",           "name": "详细规格图"},
    {"id": "tech_hud",        "name": "渗透工艺图"},
    {"id": "flatlay",         "name": "赠品全家图"},
    {"id": "sku",             "name": "SKU矩阵图"},
    {"id": "expert_lab",      "name": "专家大楼图"},
    {"id": "after_sales",     "name": "售后保证图"},
    {"id": "usage_guide",     "name": "使用建议图"},
]

DETAIL_MODULE_IDS = {m["id"] for m in DETAIL_MODULES}

DEFAULT_MODULES = ["hero", "selling_points", "multi_angle", "vibe"]

# ---------------------------------------------------------------------------
# Fallback prompts (used when /prompt/text/by_code is unavailable)
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# 3D render default prompts (matches web frontend atoms.ts)
# ---------------------------------------------------------------------------

PROMPT_3D_WITHOUT_REFERENCE = (
    "将衣服变为类似穿在人身上的立体效果，服装角度向左微微旋转，"
    "保持背景和服装细节质感不变。"
)

PROMPT_3D_WITH_REFERENCE = (
    "参考图二（上传的参考图）的服装立体效果，将图一（上传的平铺服装图）的"
    "服装平铺图也转为和图二中服装一样的3D立体效果。服装摆放的角度，姿势和"
    "图二保持一致，背景保持不变"
)

# ---------------------------------------------------------------------------
# Image retouching options (matches web frontend config.ts)
# ---------------------------------------------------------------------------

RETOUCH_TYPES = {
    "common": "image_retouching_common",
    "light": "image_retouching_light",
    "reflex": "image_retouching_reflex",
    "water": "image_retouching_water",
}

RETOUCH_POSITIONS = {
    "front": "image_retouching_front",
    "full_side": "image_retouching_full_side",
    "half_side": "image_retouching_half_side",
    "back": "image_retouching_back",
    "top": "image_retouching_top",
    "bottom": "image_retouching_bottom",
}

# ---------------------------------------------------------------------------
# Fallback prompts (used when /prompt/text/by_code is unavailable)
# ---------------------------------------------------------------------------

FALLBACK_PROMPTS = {
    "product_selling_points": (
        "你是一位拥有15年经验的顶尖电商视觉营销总监。\n\n"
        "用户已上传该产品的商品图，并计划生成以下详情模块图：\n"
        "${selected_modules} \n\n"
        "模块 ID 与名称及其内容需求对应关系如下：\n"
        "- hero（首页主视觉）：需要核心视觉主张与品牌最强价值点\n"
        "- selling_points（核心卖点图）：需要产品最具差异化的 3～5 个核心优势\n"
        "- model_efficacy（痛点共鸣图）：需要目标用户的核心痛点场景与产品解决方案\n"
        "- multi_angle（产品多角度）：需要产品外观、细节、工艺的多维度描述\n"
        "- vibe（氛围展示图）：需要情绪氛围描述与品牌态度语录\n"
        "- texture_detail（细节微距图）：需要产品材质、质感、触感的细节描述\n"
        "- ingredient_core（核心成分图）：需要核心成分/材质名称及其功效优势\n"
        "- clinical_data（科研数据图）：需要数据背书、检测认证、权威数据\n"
        "- contrast（前后对比图）：需要使用前的痛点状态与使用后的效果改变\n"
        "- specs（详细规格图）：需要产品尺寸、重量、容量、材质等参数信息\n"
        "- tech_hud（渗透工艺图）：需要核心技术原理或生产工艺描述\n"
        "- flatlay（赠品全家图）：需要套装内容清单与附赠品价值描述\n"
        "- sku（SKU矩阵图）：需要多规格、颜色或型号的系列信息\n"
        "- expert_lab（专家大楼图）：需要专家背书、实验室认证、研发故事\n"
        "- after_sales（售后保证图）：需要售后政策、品质保障与购买承诺\n"
        "- usage_guide（使用建议图）：需要分步骤的正确使用方法\n\n"
        "请从商品图中识别产品信息，结合上述已选模块的内容需求，优先提取这些模块所需的卖点信息。\n\n"
        "直接输出一段自然流畅的卖点描述文字，涵盖产品核心价值、用户痛点、差异化优势、"
        "材质工艺等关键信息，优先覆盖所选模块所需内容维度。语言风格符合产品视觉调性，具备购买号召力。"
    ),
    "product_image_detail": (
        "你是一个电商图片生成提示词专家。你将收到产品的商品图和卖点描述，"
        "任务是为用户选择的模块生成可直接调用文生图 API 的提示词。\n\n"
        "模块 ID 与名称完整对应关系：\n"
        "- hero = 首页主视觉\n- selling_points = 核心卖点图\n"
        "- model_efficacy = 痛点共鸣图\n- multi_angle = 产品多角度\n"
        "- vibe = 氛围展示图\n- texture_detail = 细节微距图\n"
        "- ingredient_core = 核心成分图\n- clinical_data = 科研数据图\n"
        "- contrast = 前后对比图\n- specs = 详细规格图\n"
        "- tech_hud = 渗透工艺图\n- flatlay = 赠品全家图\n"
        "- sku = SKU矩阵图\n- expert_lab = 专家大楼图\n"
        "- after_sales = 售后保证图\n- usage_guide = 使用建议图\n\n"
        "**输入信息：**\n"
        "- 卖点描述：${selling_points}\n"
        "- 用户选择的模块（逗号分隔的模块 ID）：${selected_modules} \n\n"
        "**任务步骤：**\n"
        "1. 仔细观察商品图，自行提炼产品的主色调（记为[主色调]）和材质质感（记为[材质质感]），"
        "作为填充模板变量的依据\n"
        "2. 结合卖点描述和商品图信息，对用户选择的每个模块，将对应提示词模板中的所有 [...] "
        "占位变量替换为具体内容，并在此基础上灵活演绎，使提示词更贴合该产品的实际特点\n"
        "3. 仅输出用户选择的模块，未选择的跳过不输出\n"
        "4. 严格输出 JSON 数组，不输出任何其他内容\n\n"
        "**各模块提示词模板：**\n\n"
        "hero:\n\"高端电商首屏大图风格。整体构图留有充足的干净留白区域，"
        "便于叠加品牌主标题与副标题。展台或产品承托区域精致有质感，"
        "整体视觉传达[hero.title]的品牌核心主张。棚拍级光效，高级医美质感，[主色调]色系。\"\n\n"
        "selling_points:\n\"极简电商卖点背景图。[主色调]渐变色系，整体构图具有几何节奏感，"
        "画面留有均等的模块化空白区域，便于叠加多条卖点文字卡片。干净现代，高级电商质感。\"\n\n"
        "model_efficacy:\n\"美妆杂志人像摄影风格。亚洲女性模特，皮肤自然细腻，"
        "表情传达[model_efficacy.context]的情绪与场景感。构图为模特与留白区域的合理分割，"
        "留白处供叠加痛点文案。明亮棚拍光效，[主色调]色系背景。\"\n\n"
        "multi_angle:\n\"极简3D展台陈列风格。多层几何展台构图，展示产品多个角度与细节。"
        "展台表面光洁有质感，背景干净，带[主色调]色系微反光。"
        "整体留有充足空白供文字角度标注叠加。C4D渲染质感。\"\n\n"
        "vibe:\n\"电影感情绪氛围大图。[材质质感]材质的微距或意境纹理与大面积[主色调]色系背景"
        "构成视觉张力，整体情绪氛围呼应[vibe.quote]的品牌态度。留有充足空白供品牌金句叠加。\"\n\n"
        "texture_detail:\n\"高端护肤品质感微距摄影。聚焦展示[texture_detail.feature]的[材质质感]"
        "细腻质感，光线突出产品材质的丰盈与水润感。构图留有空白区域供质感描述文字叠加。超高清特写。\"\n\n"
        "ingredient_core:\n\"抽象3D科学可视化风格。以[ingredient_core.title]为主视觉焦点，"
        "通过发光分子结构或晶体形态象征[ingredient_core.desc]的功效能量。"
        "[主色调]与纯白极简背景，科学与美感并存，留有文字排版空间。C4D，Octane渲染。\"\n\n"
        "clinical_data:\n\"科研实验室视觉风格。微观细胞、分子结构或荧光纹理背景，"
        "呼应[tech_hud.desc]的科学原理。整体色调深沉专业，画面中留有空白面板区域，"
        "便于叠加数据图表与检测数值。未来感医疗美学。\"\n\n"
        "contrast:\n\"极简概念对比艺术。画面构图呈现清晰的前后或内外对比关系，"
        "左侧传达[contrast.before]的状态感，右侧呈现[contrast.after]的蜕变效果。"
        "背景干净，视觉焦点突出，[主色调]色系，科学医疗渲染风格。\"\n\n"
        "specs:\n\"产品规格展示背景。[主色调]细线网格或几何框架构成精密质感背景，"
        "整体简洁克制，营造技术说明书的严谨感。留有充足空间供规格参数表格叠加展示。简约工业设计质感。\"\n\n"
        "tech_hud:\n\"科技工艺可视化背景。同心扩散波纹、分子渗透路径或HUD技术线条，"
        "可视化[tech_hud.desc]的工艺原理。[主色调]色系，极简蓝图美学，"
        "画面中央留有空白区域供工艺说明文字与产品图叠加。\"\n\n"
        "flatlay:\n\"高端平铺产品摄影风格。产品与配件、赠品等套装内容以优雅方式铺陈，"
        "构图疏密有致，留有空白区域供套装清单文字叠加。[材质质感]质感道具衬托，柔和自然光。\"\n\n"
        "sku:\n\"产品系列矩阵展示背景。[主色调]色系色板或几何模块均匀排列，"
        "形成视觉节奏感，便于叠加不同规格、颜色或型号的产品图与说明。背景简洁高级，电商选色卡质感。\"\n\n"
        "expert_lab:\n\"权威医研背景图。现代化实验室建筑外观或洁净临床研究环境，"
        "传达[expert_lab.story]的专业背书感，背景适度虚化。"
        "构图留有大面积渐变空白区域，供权威文案与认证标识叠加。专业可信赖医疗美学。\"\n\n"
        "after_sales:\n\"品质承诺视觉背景。[主色调]与金色细节构成的高级几何纹样或印章感图案，"
        "传达可信赖的品质承诺。整体背景柔和简洁，留有充足空间供售后政策条款叠加展示。庄重正式，有安全感。\"\n\n"
        "usage_guide:\n\"极简洁净步骤背景。纯净底色配以轻盈的网格或分割线结构，"
        "营造步骤说明书的条理感。画面留有充足的均等空间，适合分步骤叠加使用图文说明。现代简约，无干扰元素。\"\n\n"
        "**输出格式（严格 JSON 数组，不输出任何其他内容）：**\n"
        "[\n  {\n    \"module_id\": \"hero\",\n    \"module_name\": \"首页主视觉\",\n"
        "    \"prompt\": \"（结合商品图和卖点信息灵活生成的完整中文提示词）\"\n  }\n]"
    ),
    "watermark_removal_system_prompt": (
        "除了产品上的文字外，其余的文字和贴片都去除，只留下产品和完全无文字的背景图。"
        "生成中不要出现任何文字，构图保持原样。"
    ),
    "texture_enhancement_fixed_prompt": (
        "参考图二（高清服装图）中的服饰细节，去修复图一（需要修复的原图）中"
        "服装上细节丢失的部分"
    ),
    "garment_detail_view": (
        "为电商卖家生成${detail}细节图。"
    ),
    # product_main_image: 与网页端 mainImagePrompt.ts FALLBACK_SYSTEM_PROMPT 对齐。
    # 后端 API 返回的新版模板缺少 model / product_display 字段，且 negative 预设了
    # 「禁止动物」被 LLM 泛化为「禁止人物/模特」，导致生成结果永远没有模特。
    # 此处使用网页端正在用的旧版模板，确保 LLM 输出包含模特描述。
    "product_main_image": (
        "## 角色定义\n"
        "你是一个电商主图AI编导系统。你的任务是根据用户提供的4个输入，生成结构化的图片生成提示词（JSON格式）。\n\n"
        "## 输入参数\n"
        "| 参数 | 说明 | 必填 |\n"
        "|------|------|------|\n"
        "| product_image | 白底抠图产品图（已自动去背景） | 是 |\n"
        "| reference_image | 完整的电商主图参考图 | 是 |\n"
        "| product_features | 产品功能点/卖点（数组） | 是 |\n"
        "| marketing_points | 营销利益点（数组） | 是 |\n\n"
        "你最多会得到七个变量：1.product_image，作用于主图的核心展示商品图；"
        "2.reference_image，作用于画面的风格和文字排版；"
        "3.product_features，作用于主图具体功能的文案内容；"
        "4.marketing_points，作用于主图促销点的具体营销内容。"
        "5.background image，作用于生成主图的背景，如果没有得到这个变量，继续流程参考参考图的生成背景。"
        "6.activity icon，作用于生成主图的营销利益点的logo，如果没有这个变量，禁止生成营销利益点的logo样式。"
        "7.brand icon，作用于生成主图的品牌logo，如果没有这个变量，禁止生成品牌logo。\n\n"
        "## 处理流程\n\n"
        "### Step 1: 产品图分析\n"
        "从白底抠图中提取产品的精确视觉特征。\n\n"
        "**产品保真原则（不可违反）：**\n"
        "- 颜色：色相、饱和度、明度必须与产品图一致\n"
        "- 材质：面料质感、透明度、光泽度必须还原\n"
        "- 图案：花纹、印花、刺绣等图案的样式和分布必须一致\n"
        "- 版型：剪裁轮廓、廓形特征必须保持\n"
        "- 细节：纽扣、拉链、缝线、装饰件等必须保留\n\n"
        "### Step 2: 参考图分析\n"
        "从参考图中提取可复用的风格元素。\n\n"
        "**参考图提取原则：**\n"
        "- 提取：构图布局、文字排版风格、配色方案、氛围调性、装饰元素风格、促销条样式\n"
        "- 提取：模特的姿态类型、拍摄角度、场景风格\n"
        "- 不提取：参考图中的产品特征（颜色、款式、材质等）\n"
        "- 不提取：参考图中的具体文案内容（用户提供的卖点/营销点替换）\n"
        "- 不提取：参考图中的品牌logo\n\n"
        "### Step 3: 文案映射\n"
        "将用户提供的 product_features 和 marketing_points 映射到参考图的文案位置：\n\n"
        "**映射规则：**\n"
        "1. marketing_points 中最具冲击力的词 → 映射到参考图的主标题位置（最大字号）\n"
        "2. product_features 各项 → 映射到参考图的散落式卖点文案位置\n"
        "3. marketing_points 中的标签类内容（如88VIP、满减等）→ 映射到底部促销条/标签位置\n"
        "4. 如果文案数量 > 参考图文案位数，按优先级裁剪\n"
        "5. 如果文案数量 < 参考图文案位数，允许同一卖点在不同位置出现\n\n"
        "### Step 4: 生成结构化提示词\n"
        "输出精简JSON，总内容不超过1500字。\n\n"
        "## 输出格式\n"
        "{\n"
        '  "status": "OK",\n'
        '  "safety": "PASS",\n'
        '  "product": {\n'
        '    "type": "<产品简称>",\n'
        '    "preserve": "<产品保真约束，一句话概括不可改变的视觉特征>"\n'
        "  },\n"
        '  "scene": "<场景描述，30字以内>",\n'
        '  "model": "<模特描述，含外貌/姿态/配饰，50字以内>",\n'
        '  "product_display": "<产品穿着/展示描述，强调需还原的关键特征，60字以内>",\n'
        '  "text_overlays": [\n'
        '    { "text": "<文案>", "style": "<字体风格>", "pos": "<位置>" }\n'
        "  ],\n"
        '  "decor": "<装饰元素描述，20字以内>",\n'
        '  "bottom_bar": "<底部促销条描述（如有），20字以内>",\n'
        '  "style": {\n'
        '    "ratio": "1:1正方形电商主图",\n'
        '    "mood": "<整体氛围，20字以内>",\n'
        '    "color": "<配色方案，20字以内>"\n'
        "  },\n"
        '  "negative": "<负面约束，一句话>",\n'
        '  "prompt": "<将以上所有信息合并为一段完整自然语言提示词，300字以内>"\n'
        "}\n\n"
        "## 关键约束总结\n"
        "1. 产品保真 > 一切：产品的颜色、材质、图案、版型绝对不可改变\n"
        "2. 参考图是风格模板：只参考构图/排版/氛围，不参考产品本身，不参考品牌logo\n"
        "3. 文案来自用户输入：不使用参考图中的文案，只用用户提供的功能点和营销点\n"
        "4. 内容安全一票否决：任何输入含违规内容，立即返回NSF\n"
        "5. 主图规格：默认1:1正方形，适配电商平台主图要求\n"
        "6. 总输出 ≤ 1500字：精简表达，不输出中间分析过程，只保留最终生成指令\n\n"
        "产品功能点：${product_features}\n"
        "营销利益点：${marketing_points}"
    ),
}

# ---------------------------------------------------------------------------
# Watermark removal fallback prompt
# ---------------------------------------------------------------------------

WATERMARK_REMOVAL_FALLBACK_PROMPT = (
    "除了产品上的文字外，其余的文字和贴片都去除，只留下产品和完全无文字的背景图。"
    "生成中不要出现任何文字，构图保持原样。"
)

# ---------------------------------------------------------------------------
# Texture enhancement fallback prompt
# ---------------------------------------------------------------------------

TEXTURE_ENHANCEMENT_FALLBACK_PROMPT = (
    "参考图二（高清服装图）中的服饰细节，去修复图一（需要修复的原图）中"
    "服装上细节丢失的部分"
)

# ---------------------------------------------------------------------------
# Garment detail view constants
# ---------------------------------------------------------------------------

GARMENT_DETAIL_FALLBACK_PROMPT = "为电商卖家生成${detail}细节图。"

GARMENT_TYPES = {
    "top": "上装",
    "bottom": "下装",
    "dress": "连衣裙",
    "custom": "自定义",
}

GARMENT_DETAIL_PARTS = {
    "top": {
        "top_collar": "衬衣领口", "top_pocket": "衬衫口袋",
        "top_fabric": "衬衫面料", "top_pattern": "上装图案",
        "top_zipper": "外套拉链", "top_cuff": "上装袖口",
    },
    "bottom": {
        "bottom_button": "下装扣子", "bottom_pocket": "下装口袋",
        "bottom_fabric": "下装面料", "bottom_pattern": "下装图案",
        "bottom_hem": "下装下摆", "bottom_leg_opening": "下装裤脚",
    },
    "dress": {
        "dress_fabric": "连衣裙面料", "dress_hem": "连衣裙下摆",
        "dress_pattern": "连衣裙图案", "dress_collar": "连衣裙领口",
        "dress_strap": "吊带裙吊带", "dress_cuff": "连衣裙袖口",
    },
}

# ---------------------------------------------------------------------------
# Trending style set constants
# ---------------------------------------------------------------------------

TRENDING_STYLE_FALLBACK_PROMPT = (
    "让模特图之中的模特合理的穿搭佩戴着商品图之中的商品，"
    "动作和背景参考场景参考图之中的动作和背景。"
)

TRENDING_STYLE_ROLE_ORDER = ["product_image", "model_reference", "scene_reference"]

# ---------------------------------------------------------------------------
# Tool type configuration — pipeline routing for all 13 e-commerce functions
# ---------------------------------------------------------------------------

TOOL_CONFIGS = {
    "product_detail_image": {
        "name": "商品详情图",
        "pipeline": "multi_enhance",
        "prompt_codes": ["product_selling_points", "product_image_detail"],
        "max_images": 5,
        "has_modules": True,
        "has_selling_points": True,
        "default_model": "nano_banana_2",
        "submit_per_module": True,
    },
    "product_main_image_ecomm": {
        "name": "商品主图",
        "pipeline": "enhance_then_submit",
        "prompt_codes": ["product_main_image"],
        "max_images": 5,
        "default_model": "nano_banana_2",
        "default_aspect_ratio": "1:1",
        # 网页端 constants.ts DEFAULT_RESOLUTION = '2K'，但实际提交时用 '512p'
        # 为与网页端保持完全一致，此处也用 '512p'
        "default_resolution": "512p",
    },
    "virtual_try_on_ecomm": {
        "name": "虚拟穿搭",
        "pipeline": "enhance_then_submit",
        "prompt_codes": ["virtual_try_on"],
        "max_images": 10,
        "default_model": "nano_banana_2",
        "default_aspect_ratio": "3:4",
        "image_ids": True,
    },
    "garment_detail_view_ecomm": {
        "name": "服装细节图",
        "pipeline": "direct_submit",
        "prompt_codes": ["garment_detail_view"],
        "max_images": 1,
        "default_model": "nano_banana_2",
        "default_aspect_ratio": "1:1",
    },
    "product_3d_render_ecomm": {
        "name": "商品3D图",
        "pipeline": "direct_submit",
        "prompt_codes": [],
        "max_images": 2,
        "default_model": "nano_banana_2",
        "default_aspect_ratio": "1:1",
    },
    "background_replacement_ecomm": {
        "name": "商品换背景",
        "pipeline": "direct_submit",
        "prompt_codes": ["background_replacement_ecomm"],
        "max_images": 2,
        "default_model": "nano_banana_2",
        "default_aspect_ratio": "1:1",
        "image_names": True,
    },
    "image_retouching_ecomm": {
        "name": "商品图精修",
        "pipeline": "direct_submit",
        "prompt_codes": ["image_retouching_common"],
        "max_images": 4,
        "default_model": "nano_banana_2",
        "default_aspect_ratio": "1:1",
        "image_names": True,
    },
    "product_flat_lay_ecomm": {
        "name": "商品平铺图",
        "pipeline": "enhance_then_submit",
        "prompt_codes": ["product_flat_lay"],
        "max_images": 1,
        "default_model": "nano_banana_2",
        "default_aspect_ratio": "1:1",
    },
    "product_set_images_ecomm": {
        "name": "商品套图",
        "pipeline": "enhance_then_submit",
        "prompt_codes": ["image_set_prompt_enhance"],
        "max_images": 1,
        "default_model": "nano_banana_2",
        "default_aspect_ratio": "1:1",
        "fallback_prompt_code": "image_set_generation_fallback",
    },
    "lifestyle_fashion_photo_ecomm": {
        "name": "服装种草图",
        "pipeline": "enhance_then_submit",
        "prompt_codes": ["lifestyle_fashion_system_prompt"],
        "max_images": 3,
        "default_model": "nano_banana_2",
        "default_aspect_ratio": "3:4",
    },
    "smart_watermark_removal_ecomm": {
        "name": "智能去水印",
        "pipeline": "direct_submit",
        "prompt_codes": ["watermark_removal_system_prompt"],
        "max_images": 1,
        "default_model": "nano_banana_2",
        "default_aspect_ratio": "9:16",
    },
    "texture_enhancement_ecomm": {
        "name": "服装材质增强",
        "pipeline": "direct_submit",
        "prompt_codes": ["texture_enhancement_fixed_prompt"],
        "max_images": 2,
        "default_model": "nano_banana_2",
        "default_aspect_ratio": "9:16",
    },
    "trending_style_set_ecomm": {
        "name": "爆款套图",
        "pipeline": "multi_enhance_submit",
        "prompt_codes": ["trending_style_set_system_prompt"],
        "max_images": 5,
        "default_model": "nano_banana_2",
        "default_aspect_ratio": "3:4",
        "multi_round": 4,
    },
}

DEFAULT_TIMEOUT = 600
DEFAULT_INTERVAL = 5

# ---------------------------------------------------------------------------
# API wrappers — all hit ECOMMERCE_API_URL (api.tekan.cn:8095)
# Headers use uid (not Bearer token), matching the web frontend.
# ---------------------------------------------------------------------------

def _uid_headers(client: TopviewClient) -> dict:
    uid = client._uid
    return {"uid": uid, "teamId": uid, "Content-Type": "application/json"}


_pricing_cache: dict[str, dict] = {}


def _fetch_model_pricing(model_id: str, client: TopviewClient) -> dict:
    """Fetch the full pricing dict for a model from /ai_image/config/tkv/get.

    Returns e.g. {"512p": 0.25, "1K": 0.4, "2K": 0.6, "4K": 0.85}.
    Cached per model_id for the session.
    """
    if model_id in _pricing_cache:
        return _pricing_cache[model_id]
    url = f"{ECOMMERCE_API_URL}/ai_image/config/tkv/get"
    try:
        resp = _requests.get(url, headers=_uid_headers(client), timeout=15)
        resp.raise_for_status()
        data = resp.json()
        if str(data.get("code", "")) != "200":
            _pricing_cache[model_id] = {}
            return {}
        result = data.get("result", {})
        for scene_type in ("imageEdit", "textToImage"):
            for provider in result.get(scene_type, []):
                for model in provider.get("models", []):
                    if model.get("id") != model_id:
                        continue
                    p = dict(model.get("pricing", {}))
                    _pricing_cache[model_id] = p
                    return p
    except Exception:
        pass
    _pricing_cache[model_id] = {}
    return {}


def calc_image_unit_price(model_id: str, client: TopviewClient,
                          resolution: str = "2K",
                          aspect_ratio: str = "") -> float:
    """Calculate per-image topview credit price, matching frontend logic.

    Priority (same as frontend calculateAIImageCost):
      1. resolution_aspectRatio  (e.g. "2K_1:1")
      2. resolution              (e.g. "2K")
      3. aspectRatio             (e.g. "1:1")
      4. "default"
      5. fallback 0.2
    """
    pricing = _fetch_model_pricing(model_id, client)
    if not pricing:
        return 0.2

    if resolution and aspect_ratio:
        combined = f"{resolution}_{aspect_ratio}"
        if combined in pricing:
            return float(pricing[combined])

    if resolution and resolution in pricing:
        return float(pricing[resolution])

    if aspect_ratio and aspect_ratio in pricing:
        return float(pricing[aspect_ratio])

    return float(pricing.get("default", 0.2))


def estimate_tekan_credits(model_id: str, task_count: int,
                           client: TopviewClient,
                           resolution: str = "2K",
                           aspect_ratio: str = "") -> int:
    """Estimate total Tekan credits for a batch, matching frontend formula.

    tekanCredits = round(unitPrice × taskCount × TEKAN_CREDIT_MULTIPLIER)
    """
    unit = calc_image_unit_price(model_id, client, resolution, aspect_ratio)
    return round(unit * task_count * TEKAN_CREDIT_MULTIPLIER)


def api_get_default_board_id(client: TopviewClient) -> str:
    """GET /boards — return the first (default) board id for current user."""
    url = f"{ECOMMERCE_API_URL}/boards"
    resp = _requests.get(url, headers=_uid_headers(client), timeout=15)
    resp.raise_for_status()
    data = resp.json()
    boards = data.get("result", {}).get("data", [])
    if not boards:
        raise TopviewError("NO_BOARD", "No board found for this user")
    return boards[0]["boardId"]


def api_create_board_task(board_id: str, tool_type: str,
                          client: TopviewClient) -> str:
    """POST /boards/{boardId}/tasks — create a placeholder board task.

    Returns the boardTaskId needed by image_all_in_one/task/submit.
    """
    url = f"{ECOMMERCE_API_URL}/boards/{board_id}/tasks"
    body = {
        "toolType": tool_type,
        "toolCategory": "image",
        "useUnlimitMode": False,
    }
    resp = _requests.post(url, headers=_uid_headers(client), json=body, timeout=15)
    resp.raise_for_status()
    data = resp.json()
    code = str(data.get("code", ""))
    if code != "200":
        msg = data.get("message", f"create board task failed: {data}")
        raise TopviewError(code, msg)
    return data["result"]["taskId"]


def api_get_prompt_template(prompt_code: str, client: TopviewClient) -> str:
    """GET /prompt/text/by_code — fetch system prompt template by code."""
    url = f"{ECOMMERCE_API_URL}/prompt/text/by_code"
    resp = _requests.get(url, headers=_uid_headers(client),
                         params={"promptCode": prompt_code})
    resp.raise_for_status()
    data = resp.json()
    code = str(data.get("code", ""))
    if code != "200":
        return ""
    result = data.get("result") or data.get("data", {}).get("result", "")
    return result if isinstance(result, str) else ""


def api_enhance_prompt(prompt: str, media_files: list[dict],
                       client: TopviewClient) -> str:
    """POST /common_task/image_all_in_one/enhance-prompt — LLM enhance."""
    url = f"{ECOMMERCE_API_URL}/common_task/image_all_in_one/enhance-prompt"
    body = {"prompt": prompt, "mediaFiles": media_files}
    resp = _requests.post(url, headers=_uid_headers(client), json=body)
    resp.raise_for_status()
    data = resp.json()
    code = str(data.get("code", ""))
    if code != "200":
        msg = data.get("message", f"enhance-prompt failed: {data}")
        raise TopviewError(code, msg)
    result = data.get("result", "")
    return result if isinstance(result, str) else json_mod.dumps(result, ensure_ascii=False)


def api_submit_task(body: dict, client: TopviewClient) -> dict:
    """POST /common_task/image_all_in_one/task/submit — submit generation task."""
    url = f"{ECOMMERCE_API_URL}/common_task/image_all_in_one/task/submit"
    resp = _requests.post(url, headers=_uid_headers(client), json=body)
    resp.raise_for_status()
    data = resp.json()
    code = str(data.get("code", ""))
    if code != "200":
        msg = data.get("message", f"submit failed: {data}")
        raise TopviewError(code, msg)
    return data.get("result", data.get("data", {}))


def api_poll_task(board_task_id: str, client: TopviewClient, *,
                  interval: int = 5, timeout: int = 600,
                  verbose: bool = True) -> dict:
    """Poll board task detail via POST /boards/tasks/batch-detail until done.

    Web frontend uses board.task.getBatchDetail for polling, not the
    /common_task/image_all_in_one/task/query endpoint.
    """
    import time as _time
    url = f"{ECOMMERCE_API_URL}/boards/tasks/batch-detail"
    start = _time.time()
    while True:
        elapsed = _time.time() - start
        if elapsed > timeout:
            raise TimeoutError(
                f"Task {board_task_id} did not complete within {timeout}s")
        resp = _requests.post(url, headers=_uid_headers(client),
                              json={"taskIds": [board_task_id]}, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        code = str(data.get("code", ""))
        if code != "200":
            raise TopviewError(code, data.get("message", "query failed"))
        tasks = data.get("result", {}).get("tasks", [])
        if not tasks:
            if verbose:
                print(f"  [{elapsed:.0f}s] status: pending (no task data)",
                      file=sys.stderr)
            _time.sleep(interval)
            continue
        task = tasks[0]
        status = (task.get("status") or "").lower()
        if verbose:
            print(f"  [{elapsed:.0f}s] status: {status}", file=sys.stderr)
        if status == "success":
            result_data = task.get("result", {})
            image_url = (result_data.get("originImage", {}).get("url")
                         or result_data.get("compressedImage", {}).get("url")
                         or result_data.get("url", ""))
            images = result_data.get("images", [])
            cost_credit = task.get("creditsCost", 0) or 0
            return {
                "status": "success",
                "taskId": task.get("taskId", board_task_id),
                "boardTaskId": board_task_id,
                "boardId": task.get("boardId", ""),
                "imageUrl": image_url,
                "images": images,
                "costCredit": cost_credit,
                "result": result_data,
            }
        if status in ("failed", "fail"):
            raise TopviewError(
                "TASK_FAILED",
                task.get("errorMessage") or task.get("errorMsg") or "Task failed")
        _time.sleep(interval)


def _patch_product_main_image_template(template: str) -> str:
    """Patch the API-returned product_main_image prompt template.

    The backend updated the template and dropped the ``model`` /
    ``product_display`` output fields.  Without ``model``, the LLM never
    describes a human model in its output, producing flat-lay images only.

    This function injects the missing fields back into the JSON schema
    section so the LLM is forced to fill them in.
    """
    # Inject "model" and "product_display" after "scene" in the output JSON
    if '"model"' not in template and '"scene"' in template:
        template = template.replace(
            '"scene": "<',
            '"scene": "<场景描述，30字以内>",\n'
            '  "model": "<模特描述，含外貌/姿态/配饰，50字以内>",\n'
            '  "product_display": "<产品穿着/展示描述，强调需还原的关键特征，60字以内',
            1,  # only first occurrence
        )
        # If that didn't work cleanly (template format varies), try simpler inject
        if '"model"' not in template:
            template = template.replace(
                '"scene":',
                '"scene": "<场景描述>",\n'
                '  "model": "<模特描述，含外貌/姿态/配饰，50字以内>",\n'
                '  "product_display": "<产品穿着/展示描述，60字以内>",\n'
                '  "scene_orig":',
                1,
            )
    # Also fix the negative field: add explicit exclusion for humans
    if "动物" in template and "不包括人物" not in template:
        template = template.replace(
            "猫狗宠物、动物",
            "猫狗宠物、动物（不包括人物和模特）"
        )
        template = template.replace(
            "猫狗动物等无关生物",
            "猫狗动物等无关生物（人物/模特除外）"
        )
    # Step 2: ensure reference image analysis mentions extracting model poses
    if "参考图提取" not in template and "参考图" in template:
        # The new template's Step 2 doesn't mention extracting model poses
        template = template.replace(
            "仅提取参考图的构图比例和排版网格",
            "仅提取参考图的构图比例、排版网格、模特姿态类型和拍摄角度"
        )
    return template


def get_prompt_or_fallback(prompt_code: str, client: TopviewClient,
                           quiet: bool) -> str:
    """Try to fetch prompt from API, fall back to local copy."""
    if not quiet:
        print(f"Fetching prompt template: {prompt_code}...", file=sys.stderr)
    template = api_get_prompt_template(prompt_code, client)
    if template and template.strip():
        if prompt_code == "product_main_image":
            template = _patch_product_main_image_template(template)
            if not quiet:
                print("Patched product_main_image template (injected model field).",
                      file=sys.stderr)
        return template
    fallback = FALLBACK_PROMPTS.get(prompt_code, "")
    if fallback and not quiet:
        print(f"Using fallback prompt for {prompt_code}.", file=sys.stderr)
    return fallback


# ---------------------------------------------------------------------------
# Image preparation helpers
# ---------------------------------------------------------------------------

def prepare_images(image_refs: list[str], client: TopviewClient,
                   quiet: bool) -> list[dict]:
    """Upload local files via S3 SDK and resolve to {s3Path, fileUrl, mimeType}.

    Uses the ecommerce S3 upload path so LLM backend can access images
    through CloudFront (same as the web frontend).
    """
    uid = client._uid
    results = []
    for ref in image_refs:
        if os.path.isfile(ref):
            info = ecommerce_upload(ref, uid, quiet=quiet)
            results.append(info)
        elif ref.startswith("http"):
            ext = ref.rsplit(".", 1)[-1].split("?")[0].lower() if "." in ref else "jpg"
            mime = {"png": "image/png", "webp": "image/webp",
                    "gif": "image/gif"}.get(ext, "image/jpeg")
            file_url = ref
            s3_path = ref
            # Extract s3Path from CloudFront URL and get signed URL
            from urllib.parse import urlparse, unquote
            parsed = urlparse(ref)
            if "cloudfront.net" in parsed.netloc:
                s3_path = unquote(parsed.path.lstrip("/")).split("?")[0]
                file_url = get_file_url(s3_path, uid=uid)
            elif "?" not in ref:
                # Unsigned URL — try to get signed version
                file_url = get_file_url(ref, uid=uid) if not ref.startswith("http") else ref
            results.append({"s3Path": s3_path, "fileUrl": file_url, "mimeType": mime})
        else:
            file_url = get_file_url(ref, uid=uid)
            ext = ref.rsplit(".", 1)[-1].split("?")[0].lower() if "." in ref else "jpg"
            mime = {"png": "image/png", "webp": "image/webp",
                    "gif": "image/gif"}.get(ext, "image/jpeg")
            results.append({"s3Path": ref, "fileUrl": file_url, "mimeType": mime})
    return results


def _resolve_cutout_from_remove_bg(
    result: dict, client: TopviewClient, quiet: bool
) -> dict:
    """Resolve remove_background result to ``{s3Path, fileUrl, mimeType}``.

    Matches the web frontend ``useRemoveBackground`` behaviour:
    - ``s3Path``  = ``bgRemovedImage.filePath`` as-is (typically ``oss://...``)
    - ``fileUrl`` = ``bgRemovedImageUrl`` (OSS signed URL, HTTP-accessible)

    The **submit** API accepts ``oss://`` paths directly (the backend reads
    OSS internally).  The **enhance-prompt** API needs an HTTP URL in
    ``mediaFiles``; the OSS signed URL works for that.

    Previous code tried to re-upload the cutout to AWS S3.  This broke the
    submit path: the backend expects the ``oss://`` path for cutout images
    produced by its own ``remove_background`` service.
    """
    mask_fp = None
    m = result.get("mask")
    if isinstance(m, dict):
        mask_fp = (m.get("filePath") or m.get("file_path") or "").strip() or None

    def _log(source: str, detail: str) -> None:
        if not quiet:
            d = detail[:140] + ("..." if len(detail) > 140 else "")
            print(f"remove_bg cutout: {source} — {d}", file=sys.stderr)

    # --- Collect s3Path (bgRemovedImage.filePath) -------------------------
    s3_path = None
    nested = result.get("bgRemovedImage") or result.get("bg_removed_image")
    if isinstance(nested, str):
        s = nested.strip()
        if s and not s.startswith("http"):
            s3_path = s
    elif isinstance(nested, dict):
        fp = (nested.get("filePath") or nested.get("file_path") or "").strip()
        if fp and not (mask_fp and fp == mask_fp):
            s3_path = fp

    if not s3_path:
        for key in ("bgRemovedImageFilePath", "bgRemovedImageS3Path",
                     "bg_removed_image_file_path"):
            v = result.get(key)
            if v and isinstance(v, str) and not v.strip().startswith("http"):
                v = v.strip()
                if not (mask_fp and v == mask_fp):
                    s3_path = v
                    break

    # --- Collect fileUrl (bgRemovedImageUrl — OSS signed) -----------------
    file_url = None
    for key in ("bgRemovedImageUrl", "bgRemovedImagePath",
                "bg_removed_image_url"):
        v = result.get(key)
        if v and str(v).strip().startswith("http"):
            file_url = str(v).strip()
            break

    if not s3_path and not file_url:
        raise RuntimeError("remove_background: missing cutout in API result")

    # If we only have a URL but no s3Path, use the URL as s3Path fallback
    if not s3_path:
        s3_path = file_url

    # If we have s3Path but no URL, try get_file_url
    if not file_url:
        try:
            file_url = get_file_url(s3_path, uid=client._uid)
        except Exception:
            file_url = s3_path  # last resort

    _log("s3Path", s3_path)
    _log("fileUrl", file_url)

    ext = s3_path.rsplit(".", 1)[-1].lower() if "." in s3_path else "png"
    mime = {"png": "image/png", "webp": "image/webp"}.get(ext, "image/png")

    return {"s3Path": s3_path, "fileUrl": file_url, "mimeType": mime}


def _apply_remove_bg_for_product_main_image(
    args, client: TopviewClient, quiet: bool
) -> list[dict]:
    """Run remove_background on each --images path (product only). Matches web 商品主図.

    Returns a list of ``{s3Path, fileUrl, mimeType}`` dicts — one per product
    image — so that the caller can build both ``mediaFiles`` (needs HTTP URL)
    and ``images`` (needs ``oss://`` s3Path) correctly.  Also overwrites
    ``args.images`` with the s3Path strings for compatibility.
    """
    from remove_bg import run_remove_background_product_main_web

    rb_timeout = min(float(getattr(args, "timeout", 600) or 600), 300.0)
    rb_interval = float(getattr(args, "interval", 5) or 5)
    if rb_interval > 3:
        rb_interval = 3.0
    cutout_infos: list[dict] = []
    n = len(args.images)
    for i, ref in enumerate(args.images):
        if not quiet:
            print(
                f"remove_bg: product image {i + 1}/{n} (Tekan common_task submit + detail, web parity)...",
                file=sys.stderr,
            )
        result = run_remove_background_product_main_web(
            ref, client, timeout=rb_timeout, interval=rb_interval, quiet=quiet
        )
        info = _resolve_cutout_from_remove_bg(result, client, quiet)
        cutout_infos.append(info)
    # Keep args.images in sync (s3Path strings) for non-main-image callers
    args.images = [info["s3Path"] for info in cutout_infos]
    return cutout_infos


# ---------------------------------------------------------------------------
# Pipeline: multi_enhance (product_detail_image)
# Flow: prompt template → enhance(selling points) → enhance(module prompts)
#       → per-module submit → poll each
# ---------------------------------------------------------------------------

def pipeline_multi_enhance(config: dict, args, client: TopviewClient) -> list[dict]:
    """Full product_detail_image pipeline: extract selling points, generate
    per-module prompts, submit per-module tasks, poll all."""
    quiet = args.quiet
    modules = args.modules.split(",") if args.modules else DEFAULT_MODULES
    if not quiet and not args.modules:
        print(f"No --modules specified, using defaults: {','.join(DEFAULT_MODULES)}",
              file=sys.stderr)

    invalid = [m for m in modules if m not in DETAIL_MODULE_IDS]
    if invalid:
        print(f"Error: unknown module(s): {', '.join(invalid)}", file=sys.stderr)
        print(f"Valid modules: {', '.join(DETAIL_MODULE_IDS)}", file=sys.stderr)
        sys.exit(1)

    image_infos = prepare_images(args.images, client, quiet)
    media_files = [{"url": i["fileUrl"], "mimeType": i["mimeType"]} for i in image_infos]
    s3_images = [{"path": i["s3Path"]} for i in image_infos]
    modules_str = ",".join(modules)

    # --- Step 1: extract selling points ---
    selling_points = getattr(args, "selling_points", None) or ""
    if not selling_points:
        if not quiet:
            print("Step 1/3: Extracting selling points...", file=sys.stderr)
        sp_template = get_prompt_or_fallback("product_selling_points", client, quiet)
        sp_prompt = sp_template.replace("${selected_modules}", modules_str)
        selling_points = api_enhance_prompt(sp_prompt, media_files, client)
        if not quiet:
            preview = selling_points[:200] + ("..." if len(selling_points) > 200 else "")
            print(f"Selling points extracted: {preview}", file=sys.stderr)
    else:
        if not quiet:
            print("Step 1/3: Using provided selling points (skipping extraction).",
                  file=sys.stderr)

    # --- Step 2: generate per-module prompts ---
    if not quiet:
        print("Step 2/3: Generating per-module image prompts...", file=sys.stderr)
    detail_template = get_prompt_or_fallback("product_image_detail", client, quiet)
    detail_prompt = (detail_template
                     .replace("${selected_modules}", modules_str)
                     .replace("${selling_points}", selling_points))
    module_prompts_raw = api_enhance_prompt(detail_prompt, media_files, client)

    try:
        module_prompts = json_mod.loads(module_prompts_raw)
    except json_mod.JSONDecodeError:
        cleaned = module_prompts_raw.strip()
        if cleaned.startswith("```"):
            lines = cleaned.split("\n")
            lines = [l for l in lines if not l.strip().startswith("```")]
            cleaned = "\n".join(lines)
        try:
            module_prompts = json_mod.loads(cleaned)
        except json_mod.JSONDecodeError:
            print(f"Error: failed to parse module prompts as JSON.\n"
                  f"Raw response:\n{module_prompts_raw}", file=sys.stderr)
            sys.exit(1)

    if not isinstance(module_prompts, list):
        print(f"Error: expected JSON array, got {type(module_prompts).__name__}.",
              file=sys.stderr)
        sys.exit(1)

    prompt_map = {p["module_id"]: p["prompt"] for p in module_prompts
                  if "module_id" in p and "prompt" in p}

    if not quiet:
        print(f"Generated prompts for {len(prompt_map)} module(s): "
              f"{', '.join(prompt_map.keys())}", file=sys.stderr)

    # --- Step 3: submit per-module tasks ---
    if not quiet:
        print(f"Step 3/3: Submitting {len(prompt_map)} task(s)...", file=sys.stderr)

    model_id = args.model_id or config.get("default_model", "nano_banana_2")
    resolution = args.resolution or "2K"
    aspect_ratio = args.aspect_ratio or "3:4"
    tool_type = args.tool_type

    board_id = getattr(args, "board_id", None) or ""
    if not board_id:
        if not quiet:
            print("  Fetching default board...", file=sys.stderr)
        board_id = api_get_default_board_id(client)
        if not quiet:
            print(f"  Using board: {board_id}", file=sys.stderr)

    task_ids = []
    for mod_id, mod_prompt in prompt_map.items():
        board_task_id = api_create_board_task(board_id, tool_type, client)
        if not quiet:
            print(f"  Module [{mod_id}] boardTask created: {board_task_id}",
                  file=sys.stderr)

        submit_body = {
            "projectId": "",
            "prompts": [{"text": mod_prompt, "name": ""}],
            "images": s3_images,
            "toolType": tool_type,
            "resolution": resolution,
            "aspectRatio": aspect_ratio,
            "taskType": "imageEdit",
            "imageCount": 1,
            "boardTaskId": board_task_id,
            "modelId": model_id,
        }

        result = api_submit_task(submit_body, client)
        task_id = result.get("taskId", "")
        if not quiet:
            print(f"  Module [{mod_id}] submitted: taskId={task_id}", file=sys.stderr)
        task_ids.append({"module_id": mod_id, "task_id": task_id,
                         "board_task_id": board_task_id})

    if args.submit_only:
        return task_ids

    # --- Poll all tasks ---
    if not quiet:
        print(f"Polling {len(task_ids)} task(s)...", file=sys.stderr)

    results = []
    for entry in task_ids:
        btid = entry["board_task_id"]
        mid = entry["module_id"]
        if not quiet:
            print(f"  Polling module [{mid}] boardTaskId={btid}...", file=sys.stderr)
        try:
            result = api_poll_task(
                btid, client,
                interval=args.interval, timeout=args.timeout,
                verbose=not quiet,
            )
            convert_result_credits(result)
            result["module_id"] = mid
            if not result.get("boardId"):
                result["boardId"] = board_id
            results.append(result)
        except (TimeoutError, TopviewError) as e:
            results.append({
                "module_id": mid,
                "board_task_id": btid,
                "status": "error",
                "error": str(e),
            })
    return results


# ---------------------------------------------------------------------------
# Pipeline: enhance_then_submit (Type B — most common)
# ---------------------------------------------------------------------------

def _build_enhance_inputs(tool_type: str, config: dict, args,
                          image_infos: list[dict],
                          client: TopviewClient, quiet: bool):
    """Build (user_prompt, media_files, s3_images) for enhance_then_submit.

    Returns (prompt_for_enhance, media_files, s3_images_for_submit).
    Handles tool-specific multi-image and prompt logic.
    """
    media_files = [{"url": i["fileUrl"], "mimeType": i["mimeType"]} for i in image_infos]
    s3_images = [{"path": i["s3Path"]} for i in image_infos]
    user_prompt = args.prompt or ""
    prompt_codes = config.get("prompt_codes", [])

    if tool_type == "product_main_image_ecomm":
        extra_images = []
        extra_media = []
        for attr in ("reference_image", "background_image", "brand_logo"):
            path = getattr(args, attr, None)
            if path:
                # Reference image uses product_main_image/.../reference/ path
                # (matches web useReferenceImageUpload.ts subPath='reference')
                if attr == "reference_image" and os.path.isfile(path):
                    from shared.upload import product_main_image_reference_upload
                    infos = [product_main_image_reference_upload(
                        path, client._uid or "", quiet=quiet)]
                else:
                    infos = prepare_images([path], client, quiet)
                extra_media.extend(
                    {"url": i["fileUrl"], "mimeType": i["mimeType"]} for i in infos)
                extra_images.extend({"path": i["s3Path"]} for i in infos)
        media_files.extend(extra_media)
        s3_images.extend(extra_images)
        features = getattr(args, "features", None) or ""
        marketing = getattr(args, "marketing", None) or ""
        if prompt_codes:
            template = get_prompt_or_fallback(prompt_codes[0], client, quiet)
            if template:
                # 与前端 mainImagePrompt.buildMainImagePrompt 一致：替换模板变量（可为空串）
                user_prompt = (
                    template
                    .replace("${product_features}", features)
                    .replace("${marketing_points}", marketing)
                )
        # 与前端 buildMainImagePrompt 完全一致的角色说明
        idx = 1
        role_lines = [
            f"- 第{idx}张图：product_image（白底抠图产品图）",
        ]
        idx += 1
        role_lines.append(f"- 第{idx}张图：reference_image（电商主图参考图）")
        idx += 1
        if getattr(args, "background_image", None):
            role_lines.append(f"- 第{idx}张图：background image（背景图）")
            idx += 1
        if getattr(args, "brand_logo", None):
            role_lines.append(f"- 第{idx}张图：brand icon（品牌logo）")
        user_prompt = (
            f"{user_prompt}\n\n附带图片说明：\n" + "\n".join(role_lines)
        )
        return user_prompt, media_files, s3_images

    if tool_type == "virtual_try_on_ecomm":
        extra_media = []
        extra_s3 = []
        counter = len(image_infos) + 1
        for attr in ("model_image", "pose_image"):
            path = getattr(args, attr, None)
            if path:
                infos = prepare_images([path], client, quiet)
                for info in infos:
                    extra_media.append(
                        {"url": info["fileUrl"], "mimeType": info["mimeType"]})
                    extra_s3.append({"path": info["s3Path"], "id": f"图{counter}"})
                    counter += 1
        media_files.extend(extra_media)
        submit_images = [{"path": i["s3Path"], "id": f"图{idx+1}"}
                         for idx, i in enumerate(image_infos)]
        submit_images.extend(extra_s3)
        if prompt_codes:
            template = get_prompt_or_fallback(prompt_codes[0], client, quiet)
            if template:
                user_prompt = template if not user_prompt else f"{template}\n\n{user_prompt}"
        return user_prompt, media_files, submit_images

    if tool_type == "lifestyle_fashion_photo_ecomm":
        # Web frontend: systemPromptTemplate.replace('{{scene_id}}', scenePromptTemplate)
        #                                   .replace('{{user_prompt}}', userCustomInput)
        # Scene options are fetched from 'lifestyle_fashion_scene_options' prompt code.
        scene_id = getattr(args, "scene", None) or "scene_aesthetic"  # default: 氛围美图
        custom_input = user_prompt  # user's --prompt, if any
        if prompt_codes:
            template = get_prompt_or_fallback(prompt_codes[0], client, quiet)
            if template:
                # Resolve scene prompt template
                scene_replacement = ""
                if scene_id:
                    scene_options_raw = api_get_prompt_template(
                        "lifestyle_fashion_scene_options", client)
                    if scene_options_raw:
                        try:
                            parsed = json_mod.loads(scene_options_raw)
                            options = parsed.get("content", parsed) if isinstance(parsed, dict) else parsed
                            if isinstance(options, list):
                                for opt in options:
                                    if opt.get("sceneId") == scene_id:
                                        scene_replacement = opt.get("promptTemplate", "")
                                        if not quiet:
                                            print(f"Scene '{scene_id}' → {opt.get('name', '')}",
                                                  file=sys.stderr)
                                        break
                                if not scene_replacement and not quiet:
                                    valid = [o.get("sceneId") for o in options]
                                    print(f"Scene '{scene_id}' not found. Valid: {valid}",
                                          file=sys.stderr)
                        except (json_mod.JSONDecodeError, ValueError):
                            pass
                if not scene_replacement and not custom_input:
                    # No scene and no custom prompt — use fallback custom default
                    fallback_custom = api_get_prompt_template(
                        "lifestyle_fashion_custom_default", client)
                    if fallback_custom:
                        try:
                            fc = json_mod.loads(fallback_custom)
                            custom_input = fc.get("content", fallback_custom) if isinstance(fc, dict) else fallback_custom
                        except (json_mod.JSONDecodeError, ValueError):
                            custom_input = fallback_custom
                # The API template has typos in variable syntax:
                #   {{scene_id}  (missing closing })
                #   ${user_prompt}}  (mixed ${ and }})
                # Handle all possible variants.
                user_prompt = template
                for pat in ("{{scene_id}}", "{{scene_id}", "${scene_id}"):
                    user_prompt = user_prompt.replace(pat, scene_replacement)
                for pat in ("{{user_prompt}}", "${user_prompt}}", "${user_prompt}"):
                    user_prompt = user_prompt.replace(pat, custom_input)
        return user_prompt, media_files, s3_images

    if tool_type == "product_flat_lay_ecomm":
        # Web frontend: enhanceTemplate.replace(${extraction_target}, targetId)
        # targetId is one of: all, tops, bottoms, dress, shoes, jumpsuit, bags, jewelry, glasses
        extraction_target = getattr(args, "extraction_target", None) or "all"
        if prompt_codes:
            template = get_prompt_or_fallback(prompt_codes[0], client, quiet)
            if template:
                user_prompt = template.replace("${extraction_target}", extraction_target)
                if not quiet:
                    print(f"Extraction target: {extraction_target}", file=sys.stderr)
        return user_prompt, media_files, s3_images

    if tool_type == "product_set_images_ecomm":
        if not user_prompt:
            fallback_code = config.get("fallback_prompt_code", "")
            if fallback_code:
                fallback = get_prompt_or_fallback(fallback_code, client, quiet)
                if fallback:
                    return fallback, [], s3_images
            return user_prompt, media_files, s3_images
        if prompt_codes:
            template = get_prompt_or_fallback(prompt_codes[0], client, quiet)
            if template:
                user_prompt = f"{template}\n\n{user_prompt}"
        return user_prompt, media_files, s3_images

    if prompt_codes:
        template = get_prompt_or_fallback(prompt_codes[0], client, quiet)
        if template:
            user_prompt = template if not user_prompt else f"{template}\n\n{user_prompt}"
    return user_prompt, media_files, s3_images


_ANTI_MODEL_PATTERNS = [
    # 「严禁/禁止/不得 + ... + 模特/人物/人像」
    r"[，。、；\s]*严禁[^。]*?(?:模特|人物|人像)[^。]*",
    r"[，。、；\s]*(?:禁止|不得|不要|不允许)[^。]*?(?:模特|人物|人像)[^。]*",
    # 「无（任何）模特/人物」
    r"[，。、；\s]*(?:无(?:任何)?(?:模特|人物|人像))[^。]*",
    # 「剔除/去除/移除 + 人物/人像/模特」
    r"[，。、；\s]*(?:但)?(?:剔除|去除|移除|去掉|删除)[^。]*?(?:所有|全部|任何)?(?:人物|人像|模特)[^。]*",
    # 「不含/不包含 + 人物/模特」
    r"[，。、；\s]*(?:不含|不包含)[^。]*?(?:人物|人像|模特)[^。]*",
]

import re as _re
_ANTI_MODEL_RE = _re.compile("|".join(_ANTI_MODEL_PATTERNS))


def _sanitize_prompt_anti_model(prompt: str, quiet: bool) -> str:
    """Remove 'no model / no person' constraints from the generated prompt.

    The enhance-prompt LLM sometimes over-generalizes the template's
    'no pets/animals' negative constraint into 'no models/people', which
    prevents the generation model from including human models that the
    reference image clearly shows.  The web frontend does NOT have this
    issue consistently — it's LLM randomness.  We strip these anti-model
    phrases so the generation model can follow the reference image freely.
    """
    cleaned = _ANTI_MODEL_RE.sub("", prompt)
    # Clean up leftover punctuation artifacts
    cleaned = _re.sub(r"[，、]{2,}", "，", cleaned)
    cleaned = _re.sub(r"[。]{2,}", "。", cleaned)
    cleaned = cleaned.strip("，、。 ")
    if cleaned != prompt and not quiet:
        print("Removed anti-model constraints from prompt", file=sys.stderr)
    return cleaned


def _extract_prompt_from_enhance_result(raw: str, quiet: bool) -> str:
    """Extract the ``prompt`` field from an enhance-prompt JSON response.

    The product_main_image prompt template instructs the LLM to return a
    structured JSON with a ``prompt`` key containing the final natural-
    language generation prompt.  The web frontend
    (``useGenerateMainImagePrompt.ts``) does::

        const parsed = JSON.parse(jsonStr);
        finalPrompt = parsed.prompt ?? jsonStr;

    This function replicates that logic.  If parsing fails or the key is
    absent we fall back to the raw string.

    Additionally, strips anti-model/person constraints that the enhance LLM
    sometimes hallucinates (see ``_sanitize_prompt_anti_model``).
    """
    text = raw.strip()
    # Strip markdown code fences (```json ... ```)
    if text.startswith("```"):
        lines = text.split("\n")
        lines = [l for l in lines if not l.strip().startswith("```")]
        text = "\n".join(lines).strip()
    try:
        parsed = json_mod.loads(text)
        if isinstance(parsed, dict):
            prompt = parsed.get("prompt")
            if prompt and isinstance(prompt, str):
                prompt = _sanitize_prompt_anti_model(prompt, quiet)
                if not quiet:
                    preview = prompt[:120] + ("..." if len(prompt) > 120 else "")
                    print(f"Extracted prompt from JSON: {preview}", file=sys.stderr)
                return prompt
    except (json_mod.JSONDecodeError, ValueError):
        pass
    # Fallback: return raw text as-is
    if not quiet:
        print("enhance result is not JSON or has no 'prompt' key; using raw text",
              file=sys.stderr)
    return raw


def pipeline_enhance_then_submit(config: dict, args,
                                 client: TopviewClient) -> list[dict]:
    """Single enhance + submit pipeline."""
    quiet = args.quiet
    tool_type = args.tool_type
    cutout_infos = None
    if tool_type == "product_main_image_ecomm" and not getattr(
        args, "no_remove_bg", False
    ):
        client.guard_credit(0, "remove_bg")
        cutout_infos = _apply_remove_bg_for_product_main_image(args, client, quiet)
    if cutout_infos is not None:
        # Use cutout info directly — s3Path is oss://, fileUrl is OSS signed URL.
        # Do NOT run prepare_images on oss:// paths (would produce invalid CloudFront URLs).
        image_infos = cutout_infos
    else:
        image_infos = prepare_images(args.images, client, quiet)

    user_prompt, media_files, s3_images = _build_enhance_inputs(
        tool_type, config, args, image_infos, client, quiet)

    if media_files:
        if not quiet:
            print("Enhancing prompt...", file=sys.stderr)
        enhanced = api_enhance_prompt(user_prompt, media_files, client)
    else:
        enhanced = user_prompt

    # --- product_main_image_ecomm: extract .prompt from JSON ---------------
    # The enhance-prompt LLM returns a structured JSON object for this tool
    # type (with fields like status, product, scene, model, prompt, ...).
    # The web frontend (useGenerateMainImagePrompt.ts) parses the JSON and
    # extracts the `prompt` field as the final text to submit.  Without this
    # extraction the raw JSON blob is sent to the generation model, which
    # ignores the structured instructions and produces a flat-lay style
    # image instead of an editorial/model shot.
    if tool_type == "product_main_image_ecomm" and enhanced:
        enhanced = _extract_prompt_from_enhance_result(enhanced, quiet)

    model_id = args.model_id or config.get("default_model", "nano_banana_2")
    resolution = args.resolution or config.get("default_resolution", "2K")
    default_ar = config.get("default_aspect_ratio", "1:1")
    aspect_ratio = args.aspect_ratio or default_ar

    board_id = getattr(args, "board_id", None) or ""
    if not board_id:
        board_id = api_get_default_board_id(client)

    count = args.image_count or 1

    # Web frontend creates N independent boardTasks, each with imageCount=1,
    # and submits them in parallel.  Replicate that here.
    tasks = []
    for i in range(count):
        board_task_id = api_create_board_task(board_id, tool_type, client)
        if not quiet:
            print(f"Board task created ({i+1}/{count}): {board_task_id}", file=sys.stderr)

        submit_body = {
            "projectId": "",
            "prompts": [{"text": enhanced, "name": ""}],
            "images": s3_images,
            "toolType": tool_type,
            "resolution": resolution,
            "aspectRatio": aspect_ratio,
            "taskType": "imageEdit",
            "imageCount": 1,
            "boardTaskId": board_task_id,
            "modelId": model_id,
        }

        result = api_submit_task(submit_body, client)
        task_id = result.get("taskId", "")
        if not quiet:
            print(f"Task submitted ({i+1}/{count}): taskId={task_id}", file=sys.stderr)
        tasks.append({"task_id": task_id, "board_task_id": board_task_id})

    if args.submit_only:
        return tasks

    # Poll all tasks
    results = []
    for i, entry in enumerate(tasks):
        btid = entry["board_task_id"]
        if not quiet and count > 1:
            print(f"Polling task {i+1}/{count} (boardTaskId={btid})...", file=sys.stderr)
        poll_result = api_poll_task(
            btid, client,
            interval=args.interval, timeout=args.timeout,
            verbose=not quiet,
        )
        convert_result_credits(poll_result)
        if not poll_result.get("boardId"):
            poll_result["boardId"] = board_id
        results.append(poll_result)
    return results


# ---------------------------------------------------------------------------
# Pipeline: direct_submit (Type C — no enhance)
# Handles: product_3d_render_ecomm, background_replacement_ecomm,
#          image_retouching_ecomm
# ---------------------------------------------------------------------------

def _build_direct_submit_images(tool_type: str, image_infos: list[dict],
                                args) -> list[dict]:
    """Build the images payload, adding name fields when the tool requires it."""
    if tool_type == "background_replacement_ecomm":
        images = [{"name": "product_image", "path": image_infos[0]["s3Path"]}]
        scene_image = getattr(args, "scene_image", None)
        if scene_image:
            from shared.upload import ecommerce_upload, get_file_url
            uid = None
            if hasattr(args, "_client"):
                uid = args._client._uid
            if os.path.isfile(scene_image):
                info = ecommerce_upload(scene_image, uid or "", quiet=getattr(args, "quiet", False))
                images.append({"name": "scene_image", "path": info["s3Path"]})
            elif scene_image.startswith("http"):
                from urllib.parse import urlparse, unquote
                parsed = urlparse(scene_image)
                s3_path = scene_image
                if "cloudfront.net" in parsed.netloc:
                    s3_path = unquote(parsed.path.lstrip("/")).split("?")[0]
                images.append({"name": "scene_image", "path": s3_path})
            else:
                images.append({"name": "scene_image", "path": scene_image})
        return images

    if tool_type == "image_retouching_ecomm":
        return [{"name": f"product_image_{i+1}", "path": info["s3Path"]}
                for i, info in enumerate(image_infos)]

    return [{"path": info["s3Path"]} for info in image_infos]


def _resolve_direct_submit_prompt(tool_type: str, config: dict, args,
                                  client: TopviewClient, quiet: bool) -> str:
    """Resolve the prompt text for direct_submit tools."""
    user_prompt = args.prompt or ""

    if tool_type == "product_3d_render_ecomm":
        if not user_prompt:
            has_ref = len(args.images) > 1 or getattr(args, "reference_image", None)
            user_prompt = PROMPT_3D_WITH_REFERENCE if has_ref else PROMPT_3D_WITHOUT_REFERENCE
        return user_prompt

    if tool_type == "image_retouching_ecomm":
        retouch = getattr(args, "retouch_type", None) or "common"
        position = getattr(args, "position", None)
        prompt_code = RETOUCH_TYPES.get(retouch, "image_retouching_common")
        if position and position in RETOUCH_POSITIONS:
            prompt_code = RETOUCH_POSITIONS[position]
        template = get_prompt_or_fallback(prompt_code, client, quiet)
        return template or user_prompt

    if tool_type == "background_replacement_ecomm":
        prompt_code = (config.get("prompt_codes") or ["background_replacement_ecomm"])[0]
        template = get_prompt_or_fallback(prompt_code, client, quiet)
        if template:
            has_scene = bool(getattr(args, "scene_image", None))
            replacement = "" if has_scene else user_prompt
            return template.replace("${user_prompt}", replacement)
        return user_prompt

    if tool_type == "smart_watermark_removal_ecomm":
        prompt_codes = config.get("prompt_codes", [])
        if prompt_codes:
            template = get_prompt_or_fallback(prompt_codes[0], client, quiet)
            if template:
                return template
        return user_prompt or WATERMARK_REMOVAL_FALLBACK_PROMPT

    if tool_type == "texture_enhancement_ecomm":
        prompt_codes = config.get("prompt_codes", [])
        if prompt_codes:
            template = get_prompt_or_fallback(prompt_codes[0], client, quiet)
            if template:
                return template
        return user_prompt or TEXTURE_ENHANCEMENT_FALLBACK_PROMPT

    if tool_type == "garment_detail_view_ecomm":
        prompt_codes = config.get("prompt_codes", [])
        template = None
        if prompt_codes:
            template = get_prompt_or_fallback(prompt_codes[0], client, quiet)
        if not template:
            template = GARMENT_DETAIL_FALLBACK_PROMPT
        detail = getattr(args, "detail", None) or ""
        if not detail:
            garment_type = getattr(args, "garment_type", None) or "top"
            detail_part = getattr(args, "detail_part", None)
            if detail_part:
                parts = GARMENT_DETAIL_PARTS.get(garment_type, {})
                detail = parts.get(detail_part, detail_part)
            else:
                first_type_parts = GARMENT_DETAIL_PARTS.get(garment_type, {})
                if first_type_parts:
                    detail = list(first_type_parts.values())[0]
                else:
                    detail = "衬衣领口"
        return template.replace("${detail}", detail)

    prompt_codes = config.get("prompt_codes", [])
    if prompt_codes:
        template = get_prompt_or_fallback(prompt_codes[0], client, quiet)
        if template:
            return template if not user_prompt else f"{template}\n\n{user_prompt}"
    return user_prompt


def pipeline_direct_submit(config: dict, args,
                           client: TopviewClient) -> list[dict]:
    """Direct submit without enhance step."""
    quiet = args.quiet
    tool_type = args.tool_type

    # texture_enhancement_ecomm: web frontend removes background from the
    # reference image (image 2) before submitting.  images[1].path must be
    # the bgRemovedImage.filePath (oss://) of the reference, not the raw upload.
    if tool_type == "texture_enhancement_ecomm" and len(args.images) >= 2:
        from remove_bg import run_remove_background_product_main_web
        ref_path = args.images[1]
        if not quiet:
            print("texture_enhancement: removing background from reference image (web parity)...",
                  file=sys.stderr)
        # Upload reference to S3 first if local
        if os.path.isfile(ref_path):
            from shared.upload import product_main_image_upload
            ref_info = product_main_image_upload(ref_path, client._uid or "", quiet=quiet)
            ref_s3 = ref_info["s3Path"]
        else:
            ref_s3 = ref_path
        rb_result = run_remove_background_product_main_web(
            ref_s3, client, timeout=300, interval=3, quiet=quiet
        )
        cutout = _resolve_cutout_from_remove_bg(rb_result, client, quiet)
        # Replace args.images[1] with the cutout oss:// path
        args.images[1] = cutout["s3Path"]

    image_infos = prepare_images(args.images, client, quiet)
    args._client = client
    s3_images = _build_direct_submit_images(tool_type, image_infos, args)
    user_prompt = _resolve_direct_submit_prompt(tool_type, config, args, client, quiet)

    model_id = args.model_id or config.get("default_model", "nano_banana_2")
    resolution = args.resolution or "2K"
    default_ar = config.get("default_aspect_ratio", "1:1")
    aspect_ratio = args.aspect_ratio or default_ar

    board_id = getattr(args, "board_id", None) or ""
    if not board_id:
        board_id = api_get_default_board_id(client)
    board_task_id = api_create_board_task(board_id, tool_type, client)
    if not quiet:
        print(f"Board task created: {board_task_id}", file=sys.stderr)

    submit_body = {
        "projectId": "",
        "prompts": [{"text": user_prompt, "name": ""}],
        "images": s3_images,
        "toolType": tool_type,
        "resolution": resolution,
        "aspectRatio": aspect_ratio,
        "taskType": "imageEdit",
        "imageCount": args.image_count or 1,
        "boardTaskId": board_task_id,
        "modelId": model_id,
    }

    result = api_submit_task(submit_body, client)
    task_id = result.get("taskId", "")
    if not quiet:
        print(f"Task submitted: taskId={task_id}", file=sys.stderr)

    if args.submit_only:
        return [{"task_id": task_id, "board_task_id": board_task_id}]

    poll_result = api_poll_task(
        board_task_id, client,
        interval=args.interval, timeout=args.timeout,
        verbose=not quiet,
    )
    convert_result_credits(poll_result)
    if not poll_result.get("boardId"):
        poll_result["boardId"] = board_id
    return [poll_result]


# ---------------------------------------------------------------------------
# Pipeline: multi_enhance_submit (Type D — multiple rounds)
# ---------------------------------------------------------------------------

def _build_trending_style_task_sets(args, image_infos, client, quiet, rounds):
    """Build per-round (s3_paths, metadata, media_files) for trending_style_set."""
    product_infos = list(image_infos)
    model_ref_infos = []
    scene_ref_infos = []
    for attr, target in (("model_ref", model_ref_infos), ("scene_ref", scene_ref_infos)):
        paths = getattr(args, attr, None)
        if paths:
            if isinstance(paths, str):
                paths = [paths]
            target.extend(prepare_images(paths, client, quiet))

    all_infos_by_role = {
        "product_image": product_infos,
        "model_reference": model_ref_infos,
        "scene_reference": scene_ref_infos,
    }

    task_sets = []
    for r in range(rounds):
        round_infos = []
        numbering: dict[str, list[str]] = {}
        idx = 1
        for role in TRENDING_STYLE_ROLE_ORDER:
            infos = all_infos_by_role.get(role, [])
            if not infos:
                continue
            if role == "scene_reference" and len(infos) > 1:
                pick = [infos[r % len(infos)]]
            else:
                pick = infos
            nums = []
            for info in pick:
                round_infos.append(info)
                nums.append(f"图{idx}")
                idx += 1
            numbering[role] = nums

        metadata = json_mod.dumps({
            "mission_type": [getattr(args, "mission_type", None) or "网红地打卡"],
            "product_image": numbering.get("product_image", []),
            "model_reference": numbering.get("model_reference", []),
            "scene_reference": numbering.get("scene_reference", []),
        })
        s3_paths = [{"path": i["s3Path"]} for i in round_infos]
        media = [{"url": i["fileUrl"], "mimeType": i["mimeType"]} for i in round_infos]
        task_sets.append((s3_paths, metadata, media))
    return task_sets


def pipeline_multi_enhance_submit(config: dict, args,
                                  client: TopviewClient) -> list[dict]:
    """Multiple rounds of enhance + submit (e.g. trending_style_set_ecomm)."""
    quiet = args.quiet
    tool_type = args.tool_type
    rounds = config.get("multi_round", 4)

    image_infos = prepare_images(args.images, client, quiet)
    user_prompt = args.prompt or ""
    model_id = args.model_id or config.get("default_model", "nano_banana_2")
    resolution = args.resolution or "2K"
    default_ar = config.get("default_aspect_ratio", "3:4")
    aspect_ratio = args.aspect_ratio or default_ar

    prompt_codes = config.get("prompt_codes", [])
    system_template = ""
    if prompt_codes:
        system_template = get_prompt_or_fallback(prompt_codes[0], client, quiet) or ""

    if tool_type == "trending_style_set_ecomm":
        task_sets = _build_trending_style_task_sets(
            args, image_infos, client, quiet, rounds)
    else:
        media_files = [{"url": i["fileUrl"], "mimeType": i["mimeType"]} for i in image_infos]
        s3_images = [{"path": i["s3Path"]} for i in image_infos]
        task_sets = [(s3_images, "", media_files)] * rounds

    board_id = getattr(args, "board_id", None) or ""
    if not board_id:
        board_id = api_get_default_board_id(client)

    task_ids = []
    for r in range(rounds):
        s3_imgs, metadata, media = task_sets[r]
        enhance_prompt = system_template
        if metadata:
            enhance_prompt = f"{system_template}\n\n{metadata}" if system_template else metadata
        if user_prompt:
            enhance_prompt = f"{enhance_prompt}\n\n{user_prompt}" if enhance_prompt else user_prompt

        if not quiet:
            print(f"Round {r+1}/{rounds}: enhancing prompt...", file=sys.stderr)
        if media:
            enhanced = api_enhance_prompt(enhance_prompt, media, client)
        else:
            enhanced = enhance_prompt or TRENDING_STYLE_FALLBACK_PROMPT

        board_task_id = api_create_board_task(board_id, tool_type, client)
        submit_body = {
            "projectId": "",
            "prompts": [{"text": enhanced, "name": ""}],
            "images": s3_imgs,
            "toolType": tool_type,
            "resolution": resolution,
            "aspectRatio": aspect_ratio,
            "taskType": "imageEdit",
            "imageCount": args.image_count or 1,
            "boardTaskId": board_task_id,
            "modelId": model_id,
        }

        result = api_submit_task(submit_body, client)
        task_id = result.get("taskId", "")
        task_ids.append({"task_id": task_id, "board_task_id": board_task_id})
        if not quiet:
            print(f"  Round {r+1} submitted: taskId={task_id}", file=sys.stderr)

    if args.submit_only:
        return [{"round": i+1, "task_id": e["task_id"],
                 "board_task_id": e["board_task_id"]}
                for i, e in enumerate(task_ids)]

    results = []
    for i, entry in enumerate(task_ids):
        btid = entry["board_task_id"]
        if not quiet:
            print(f"Polling round {i+1}/{rounds} boardTaskId={btid}...",
                  file=sys.stderr)
        try:
            result = api_poll_task(
                btid, client,
                interval=args.interval, timeout=args.timeout,
                verbose=not quiet,
            )
            convert_result_credits(result)
            result["round"] = i + 1
            if not result.get("boardId"):
                result["boardId"] = board_id
            results.append(result)
        except (TimeoutError, TopviewError) as e:
            results.append({"round": i + 1, "task_id": entry["task_id"],
                            "board_task_id": btid,
                            "status": "error", "error": str(e)})
    return results


# ---------------------------------------------------------------------------
# Pipeline router
# ---------------------------------------------------------------------------

def run_pipeline(tool_type: str, args, client: TopviewClient) -> list[dict]:
    """Route to the correct pipeline based on config."""
    config = TOOL_CONFIGS[tool_type]
    pipeline = config["pipeline"]

    if pipeline == "multi_enhance":
        return pipeline_multi_enhance(config, args, client)
    elif pipeline == "enhance_then_submit":
        return pipeline_enhance_then_submit(config, args, client)
    elif pipeline == "direct_submit":
        return pipeline_direct_submit(config, args, client)
    elif pipeline == "multi_enhance_submit":
        return pipeline_multi_enhance_submit(config, args, client)
    else:
        print(f"Error: unknown pipeline '{pipeline}' for tool-type '{tool_type}'.",
              file=sys.stderr)
        sys.exit(1)


# ---------------------------------------------------------------------------
# Result printing
# ---------------------------------------------------------------------------

# Model display names — matches web frontend constants
MODEL_DISPLAY_NAMES = {
    "nano_banana_2": "Nano Banana Pro",
}


def print_results(results: list[dict], args,
                   estimated_credits: Optional[int] = None) -> None:
    """Print final results.

    ``estimated_credits`` is the pre-calculated Tekan credit cost for the
    whole batch (matching the frontend formula).  When supplied, it is shown
    as the cost line instead of the per-task backend ``creditsCost`` (which
    is often inaccurate / zero).
    """
    if args.json:
        out = results
        if estimated_credits is not None:
            out = {"results": results, "estimatedCredits": estimated_credits}
        print(json_mod.dumps(out, indent=2, ensure_ascii=False))
        return

    board_url = ""
    for r in results:
        mod = r.get("module_id", "")
        prefix = f"[{mod}] " if mod else ""

        if r.get("status") == "error":
            print(f"{prefix}Error: {r.get('error', 'unknown')}")
            continue

        status = r.get("status", "unknown")
        print(f"{prefix}status: {status}")

        images = r.get("images", [])
        if images:
            for i, img in enumerate(images):
                img_status = img.get("status", "unknown")
                if str(img_status).lower() == "success":
                    url = img.get("filePath", "")
                    dims = ""
                    if img.get("width") and img.get("height"):
                        dims = f" ({img['width']}x{img['height']})"
                    print(f"  [{i+1}] [查看图片]({url}){dims}")
                    print(f"  {shorten_url(url)}")
                else:
                    err = img.get("errorMsg", "")
                    print(f"  [{i+1}] {img_status}: {err}")
        elif r.get("imageUrl"):
            origin = r.get("result", {}).get("originImage", {})
            dims = ""
            if origin.get("width") and origin.get("height"):
                dims = f" ({origin['width']}x{origin['height']})"
            print(f"  [查看图片]({r['imageUrl']}){dims}")
            print(f"  {shorten_url(r['imageUrl'])}")

        board_task_id = r.get("boardTaskId", "")
        board_id = r.get("boardId", "") or getattr(args, "board_id", "") or ""
        if board_task_id and board_id:
            edit_url = f"https://tekan.cn/board/{board_id}?boardResultId={board_task_id}"
            print(f"  [在看板中查看]({edit_url})")
            print(f"  {shorten_url(edit_url)}")
            if not board_url:
                board_url = f"https://tekan.cn/board/{board_id}"

    success_count = sum(1 for r in results if r.get("status") == "success")

    # Print tool type name for Agent to use in reply
    tool_type = getattr(args, "tool_type", "")
    tool_config = TOOL_CONFIGS.get(tool_type, {})
    tool_name = tool_config.get("name", tool_type)
    if success_count > 0:
        print(f"\n功能: {tool_name}")
    if estimated_credits is not None and success_count > 0:
        print(f"消耗: ~{estimated_credits} credits（预估）")
    if board_url and success_count > 1:
        print(f"[在看板中查看/编辑所有图片]({board_url})")
        print(f"{shorten_url(board_url)}")


# ---------------------------------------------------------------------------
# Subcommand handlers
# ---------------------------------------------------------------------------

def _validate_product_main_image_images(args, parser) -> None:
    """网页商品主图只有一张 product + 单独 reference；CLI 与之对齐。"""
    if args.tool_type == "product_main_image_ecomm" and len(args.images) > 1:
        parser.error(
            "product_main_image_ecomm 的 --images 只能填 1 张商品图（平铺/商品原图）。"
            "模特/风格/构图参考请放在 --reference-image，不要和商品图一起塞进 --images。"
        )


def cmd_run(args, parser):
    """Submit + poll — full flow."""
    if args.tool_type not in TOOL_CONFIGS:
        parser.error(f"Unknown tool-type: {args.tool_type}")
    _validate_product_main_image_images(args, parser)
    # --images is required for most tools except trending_style_set_ecomm
    # (穿搭OOTD / 萌宠带货 have optional product_image)
    if not args.images and args.tool_type != "trending_style_set_ecomm":
        parser.error("--images is required for this tool type")
    args.submit_only = False
    config = TOOL_CONFIGS[args.tool_type]
    client = TopviewClient()
    client.guard_credit(0, f"ecommerce_image/{args.tool_type}")
    results = run_pipeline(args.tool_type, args, client)
    task_count = sum(1 for r in results if r.get("status") == "success")
    model_id = args.model_id or config.get("default_model", "nano_banana_2")
    resolution = args.resolution or "2K"
    aspect_ratio = args.aspect_ratio or config.get("default_aspect_ratio", "1:1")
    estimated = estimate_tekan_credits(model_id, task_count, client,
                                       resolution=resolution,
                                       aspect_ratio=aspect_ratio)
    print_results(results, args, estimated_credits=estimated)


def cmd_submit(args, parser):
    """Submit only — print task IDs and exit."""
    if args.tool_type not in TOOL_CONFIGS:
        parser.error(f"Unknown tool-type: {args.tool_type}")
    _validate_product_main_image_images(args, parser)
    if not args.images and args.tool_type != "trending_style_set_ecomm":
        parser.error("--images is required for this tool type")
    args.submit_only = True
    client = TopviewClient()
    client.guard_credit(0, f"ecommerce_image/{args.tool_type}")
    results = run_pipeline(args.tool_type, args, client)
    if args.json:
        print(json_mod.dumps(results, indent=2, ensure_ascii=False))
    else:
        for r in results:
            tid = r.get("task_id", "")
            btid = r.get("board_task_id", "")
            extra = ""
            if "module_id" in r:
                extra = f" (module: {r['module_id']})"
            elif "round" in r:
                extra = f" (round: {r['round']})"
            print(f"taskId: {tid}  boardTaskId: {btid}{extra}")


def cmd_query(args, parser):
    """Poll an existing taskId."""
    client = TopviewClient()
    try:
        result = api_poll_task(
            args.task_id, client,
            interval=args.interval, timeout=args.timeout,
            verbose=not args.quiet,
        )
        model_id = getattr(args, "model_id", None) or "nano_banana_2"
        resolution = getattr(args, "resolution", None) or "2K"
        aspect_ratio = getattr(args, "aspect_ratio", None) or "1:1"
        est = estimate_tekan_credits(model_id, 1, client,
                                     resolution=resolution,
                                     aspect_ratio=aspect_ratio) if result.get("status") == "success" else None
        print_results([result], args, estimated_credits=est)
    except TimeoutError as e:
        print(f"Timeout: {e}", file=sys.stderr)
        sys.exit(2)


def cmd_list_tools(args, _parser):
    """List all 13 tool types."""
    if args.json:
        out = {k: {"name": v["name"], "pipeline": v["pipeline"]}
               for k, v in TOOL_CONFIGS.items()}
        print(json_mod.dumps(out, indent=2, ensure_ascii=False))
        return
    print(f"\n{'Tool Type':<38} {'Name':<12} {'Pipeline'}")
    print("-" * 72)
    for key, cfg in TOOL_CONFIGS.items():
        print(f"{key:<38} {cfg['name']:<12} {cfg['pipeline']}")
    print()


def cmd_list_modules(args, _parser):
    """List 16 detail modules (product_detail_image only)."""
    if args.json:
        print(json_mod.dumps(DETAIL_MODULES, indent=2, ensure_ascii=False))
        return
    print(f"\n{'#':<4} {'ID':<18} {'Name'}")
    print("-" * 40)
    for i, m in enumerate(DETAIL_MODULES, 1):
        print(f"{i:<4} {m['id']:<18} {m['name']}")
    print()


def cmd_extract_selling_points(args, parser):
    """Extract selling points only (product_detail_image)."""
    if not args.images:
        parser.error("--images is required for extract-selling-points")
    modules = args.modules.split(",") if args.modules else DEFAULT_MODULES
    if not args.modules and not args.quiet:
        print(f"No --modules specified, using defaults: {','.join(DEFAULT_MODULES)}",
              file=sys.stderr)

    client = TopviewClient()
    image_infos = prepare_images(args.images, client, args.quiet)
    media_files = [{"url": i["fileUrl"], "mimeType": i["mimeType"]} for i in image_infos]
    modules_str = ",".join(modules)

    sp_template = get_prompt_or_fallback("product_selling_points", client, args.quiet)
    sp_prompt = sp_template.replace("${selected_modules}", modules_str)
    selling_points = api_enhance_prompt(sp_prompt, media_files, client)

    if args.json:
        print(json_mod.dumps({"selling_points": selling_points}, indent=2, ensure_ascii=False))
    else:
        print(selling_points)


def cmd_estimate_cost(args, _parser):
    """Estimate credit cost using live pricing from API."""
    config = TOOL_CONFIGS.get(args.tool_type)
    if not config:
        print(f"Unknown tool-type: {args.tool_type}", file=sys.stderr)
        sys.exit(1)

    module_count = 1
    if config.get("submit_per_module"):
        mods = args.modules.split(",") if args.modules else DEFAULT_MODULES
        module_count = len(mods)

    rounds = config.get("multi_round", 1)
    total_tasks = module_count * rounds

    client = TopviewClient()
    model_id = config.get("default_model", "nano_banana_2")
    resolution = getattr(args, "resolution", None) or "2K"
    aspect_ratio = getattr(args, "aspect_ratio", None) or config.get("default_aspect_ratio", "1:1")
    estimated = estimate_tekan_credits(model_id, total_tasks, client,
                                       resolution=resolution,
                                       aspect_ratio=aspect_ratio)

    if args.json:
        print(json_mod.dumps({
            "tool_type": args.tool_type, "tasks": total_tasks,
            "estimated_credits": estimated,
            "model_id": model_id,
            "resolution": resolution, "aspect_ratio": aspect_ratio,
        }))
    else:
        print(f"tool-type: {args.tool_type} ({config['name']})")
        print(f"model: {model_id}")
        print(f"tasks: {total_tasks}")
        print(f"estimated cost: ~{estimated} credits")


# ---------------------------------------------------------------------------
# Argument parser
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Tekan E-commerce Image — generate product images with AI.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
AGENT WORKFLOW RULES:
  1. ALWAYS start with `run` — it submits and polls automatically.
  2. Only use `query` if `run` timed out and you have a taskId to resume.
  3. Read references/ecommerce_image.md for module selection and interaction rules.
  4. NEVER hand a pending taskId back to the user — always poll to completion.
  5. --modules is OPTIONAL. If omitted, defaults to: hero,selling_points,multi_angle,vibe,specs,usage_guide
     Agent should pick modules itself based on product category, or omit --modules to use defaults.
     DO NOT ask the user to choose modules — just run the command.

Examples:
  # Generate product detail images (with specific modules)
  python ecommerce_image.py run --tool-type product_detail_image \\
      --images product.jpg --modules hero,selling_points,multi_angle

  # Generate product detail images (using default modules — preferred for quick execution)
  python ecommerce_image.py run --tool-type product_detail_image --images product.jpg

  # List available tool types
  python ecommerce_image.py list-tools

  # List detail modules
  python ecommerce_image.py list-modules

  # Extract selling points only
  python ecommerce_image.py extract-selling-points --images product.jpg
""",
    )

    sub = parser.add_subparsers(dest="subcommand")
    sub.required = True

    def add_common(p):
        p.add_argument("--tool-type", required=True,
                       help="Tool type (see list-tools)")
        p.add_argument("--images", nargs="+", default=[],
                       help="Product image files (local paths or URLs)")
        p.add_argument("--prompt", default=None,
                       help="User prompt / description")
        p.add_argument("--modules", default=None,
                       help="Comma-separated module IDs (product_detail_image only)")
        p.add_argument("--selling-points", default=None,
                       help="Manual selling points (skip extraction)")
        p.add_argument("--aspect-ratio", default=None,
                       help="Aspect ratio (e.g. 3:4, 1:1, 16:9)")
        p.add_argument("--resolution", default=None,
                       help="Resolution (e.g. 1K, 2K, 4K)")
        p.add_argument("--image-count", type=int, default=None,
                       help="Number of images to generate per task")
        p.add_argument("--model-id", default=None,
                       help="Model ID (default: nano_banana_2)")
        p.add_argument("--board-id", default=None,
                       help="Board ID for task organization")
        p.add_argument("--scene-image", default=None,
                       help="Scene/background image (background_replacement_ecomm)")
        p.add_argument("--retouch-type", default=None,
                       choices=["common", "light", "reflex", "water"],
                       help="Retouching type (image_retouching_ecomm)")
        p.add_argument("--position", default=None,
                       choices=["front", "full_side", "half_side",
                                "back", "top", "bottom"],
                       help="Product position (image_retouching_ecomm)")
        p.add_argument("--reference-image", default=None,
                       help="Reference image (product_main_image_ecomm)")
        p.add_argument("--background-image", default=None,
                       help="Background image (product_main_image_ecomm)")
        p.add_argument("--brand-logo", default=None,
                       help="Brand logo image (product_main_image_ecomm)")
        p.add_argument("--features", default=None,
                       help="Product features (product_main_image_ecomm)")
        p.add_argument("--marketing", default=None,
                       help="Marketing points (product_main_image_ecomm)")
        p.add_argument("--no-remove-bg", action="store_true",
                       help="Skip remove-background on product image(s) "
                            "(product_main_image_ecomm; default: remove_bg first, web parity)")
        p.add_argument("--model-image", default=None,
                       help="Model image (virtual_try_on_ecomm, required)")
        p.add_argument("--pose-image", default=None,
                       help="Pose reference image (virtual_try_on_ecomm)")
        p.add_argument("--extraction-target", default=None,
                       choices=["all", "tops", "bottoms", "dress", "shoes",
                                "jumpsuit", "bags", "jewelry", "glasses"],
                       help="Extraction target (product_flat_lay_ecomm): "
                            "all=整套, tops=上装, bottoms=下装, dress=衣裙, "
                            "shoes=鞋靴, jumpsuit=连体衣, bags=包包, "
                            "jewelry=首饰, glasses=眼镜")
        p.add_argument("--garment-type", default=None,
                       choices=["top", "bottom", "dress", "custom"],
                       help="Garment type (garment_detail_view_ecomm)")
        p.add_argument("--detail-part", default=None,
                       help="Detail part ID (garment_detail_view_ecomm)")
        p.add_argument("--detail", default=None,
                       help="Custom detail description (garment_detail_view_ecomm)")
        p.add_argument("--scene", default=None,
                       help="Scene ID for lifestyle_fashion_photo_ecomm: "
                            "scene_aesthetic, scene_street, scene_mirror_selfie, "
                            "scene_home, scene_coffee, scene_canon, scene_fuji, scene_hat")
        p.add_argument("--mission-type", default=None,
                       help="Mission type for trending_style_set_ecomm: "
                            "网红地打卡, 好物plog, 穿搭OOTD, 萌宠带货, 一衣多穿")
        p.add_argument("--model-ref", nargs="+", default=None,
                       help="Model reference images (trending_style_set_ecomm)")
        p.add_argument("--scene-ref", nargs="+", default=None,
                       help="Scene reference images (trending_style_set_ecomm)")

    def add_poll(p):
        p.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT,
                       help=f"Max polling time in seconds (default: {DEFAULT_TIMEOUT})")
        p.add_argument("--interval", type=float, default=DEFAULT_INTERVAL,
                       help=f"Polling interval in seconds (default: {DEFAULT_INTERVAL})")

    def add_output(p):
        p.add_argument("--json", action="store_true",
                       help="Output full JSON response")
        p.add_argument("-q", "--quiet", action="store_true",
                       help="Suppress status messages")

    # -- run --
    p_run = sub.add_parser("run", help="[DEFAULT] Submit and poll until done")
    add_common(p_run)
    add_poll(p_run)
    add_output(p_run)

    # -- submit --
    p_submit = sub.add_parser("submit", help="Submit only, print taskId(s)")
    add_common(p_submit)
    add_output(p_submit)

    # -- query --
    p_query = sub.add_parser("query", help="Poll existing taskId until done")
    p_query.add_argument("--task-id", required=True, help="taskId to poll")
    add_poll(p_query)
    add_output(p_query)

    # -- list-tools --
    p_lt = sub.add_parser("list-tools", help="List all tool types")
    p_lt.add_argument("--json", action="store_true")

    # -- list-modules --
    p_lm = sub.add_parser("list-modules",
                          help="List 16 detail modules (product_detail_image)")
    p_lm.add_argument("--json", action="store_true")

    # -- extract-selling-points --
    p_esp = sub.add_parser("extract-selling-points",
                           help="Extract selling points only")
    p_esp.add_argument("--images", nargs="+", required=True,
                       help="Product image files")
    p_esp.add_argument("--modules", default=None,
                       help="Comma-separated module IDs (defaults to common set)")
    p_esp.add_argument("--json", action="store_true")
    p_esp.add_argument("-q", "--quiet", action="store_true")

    # -- estimate-cost --
    p_ec = sub.add_parser("estimate-cost", help="Estimate credit cost")
    p_ec.add_argument("--tool-type", required=True)
    p_ec.add_argument("--modules", default=None,
                      help="Comma-separated module IDs (for cost calculation)")
    p_ec.add_argument("--resolution", default=None,
                      help="Resolution for pricing (512p, 1K, 2K, 4K)")
    p_ec.add_argument("--aspect-ratio", default=None,
                      help="Aspect ratio (e.g. 1:1, 3:4)")
    p_ec.add_argument("--json", action="store_true")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    cmd = args.subcommand

    if cmd == "run":
        cmd_run(args, parser)
    elif cmd == "submit":
        cmd_submit(args, parser)
    elif cmd == "query":
        cmd_query(args, parser)
    elif cmd == "list-tools":
        cmd_list_tools(args, parser)
    elif cmd == "list-modules":
        cmd_list_modules(args, parser)
    elif cmd == "extract-selling-points":
        cmd_extract_selling_points(args, parser)
    elif cmd == "estimate-cost":
        cmd_estimate_cost(args, parser)


if __name__ == "__main__":
    main()
