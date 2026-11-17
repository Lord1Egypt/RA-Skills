#!/usr/bin/env python3
"""为 weipaiban 交互作品提供可选的随机视觉方向（流派驱动 + 本地历史反重复）。

LLM 自行按主题挑流派会塌回「清新手账 + 满版封面 + 日夜 clickSwitch + 浅灰清单」。
本脚本只在用户要求随机方向或主创需要灵感时使用；输出是建议，不是强制模板。

与旧版的区别——**先定流派，其余维度在该流派的兼容集内抽**。全维独立随机会抽出
「奢侈品质感 + 粉彩马卡龙 + 黏土3D」这种内部打架的组合；优秀设计的前提是内在一致。
每个流派另带一份可执行的版面规格（字体 / 字重 / 字号 / 字距 / 边距 / 圆角 / 图片处理），
把视觉词翻译成坐标层能落地的数值；最终仍以所选 format 的规则为准。

- school / paletteStrategy / hue / techniques / coverComposition / motion 是视觉维；
- climaxMechanic / imageMedium / takeawayForm / colorRoute 是交互作品维；
- 兼容集外的抽签会标 `contrast`（题材外流派）/ `paletteContrast` / `mediumContrast`；
- 历史默认 ~/.cache/weipaiban/direction-history.jsonl，排除最近几次的
  school / paletteStrategy / 色相桶 / coverComposition / climaxMechanic / imageMedium /
  takeawayForm / colorRoute。

用法示例：

    python3 pick_direction.py --format layered-scroll
    python3 pick_direction.py --format layered-scroll --category 开学季
    python3 pick_direction.py --format layered-scroll --school 报纸社论
    python3 pick_direction.py --self-check
"""

from __future__ import annotations

import argparse
import json
import os
import random
import sys
import time

# ---- 与 design-inspiration.md 第 1/2/3/6/7 层同步 ----

SCHOOLS = [
    "极简留白",
    "杂志编辑风",
    "国潮/新中式",
    "孟菲斯",
    "莫兰迪高级灰",
    "极繁装饰",
    "瑞士网格",
    "复古印刷",
    "赛博科技冷感",
    "清新手账",
    "商务简报",
    "奢侈品质感",
    "报纸社论",
    "自然清透",
    "暖阳节庆",
    "Y2K/酸性",
    "波普拼贴",
    "暗黑霓虹",
    "法式浪漫",
    "蒸汽波",
    "黑白高对比",
]

PALETTE_STRATEGIES = [
    "单色系深浅渐进",
    "互补撞色",
    "高饱和双色撞色",
    "深色底+荧光强调",
    "大地色系",
    "粉彩马卡龙",
    "黑白灰+单强调色",
    "三色分割(60-30-10)",
    "复古褪色调",
    "金属点缀",
    "邻近色和谐",
    "渐变主导",
]

TECHNIQUES = [
    "非对称留白",
    "大小字号强对比",
    "首字/引号放大",
    "序号/角标锚点",
    "分割线节奏",
    "层叠造纵深",
    "字距呼吸感",
    "边角描边点缀",
    "色块错位",
    "满版色底反白",
    "超大数字压屏",
    "竖排文字意象",
    "密集重复节奏",
]

COMPOSITIONS = [
    "中心聚焦",
    "层叠纵深",
    "对角动线",
    "四角点缀",
    "散点漂浮",
    "错位叠压",
    "左右分栏",
    "上下堆叠",
    "满版铺底",
]

MOTIONS = [
    "依次入场",
    "主图循环",
    "强调脉冲",
    "入场+氛围",
    "盖章定格",
    "组合变换",
    "克制点睛",
]

IMAGE_MEDIUMS = [
    "胶片纪实摄影",
    "杂志棚拍",
    "纸本拼贴",
    "水墨工笔",
    "扁平贴纸插画",
    "黏土3D",
    "印刷网纹",
    "手绘线稿上色",
    "木刻版画",
    "水彩淡彩",
]

# 色彩路线：决定整篇的明暗与浓烈度，见 references/wechat-dark-color.md
COLOR_ROUTES = ["light-airy", "chromatic-dark", "photo-led"]

CATEGORIES = [
    "春节",
    "建党节",
    "儿童节",
    "妇女节",
    "劳动节",
    "重阳节",
    "母亲节",
    "端午节",
    "中秋节",
    "情人节",
    "万圣节",
    "清明节",
    "安全日",
    "节气",
    "开学季",
    "毕业季",
    "医疗健康",
    "教育",
    "党政",
    "科技",
    "电商",
    "母婴",
    "金融",
    "婚庆",
    "媒体",
    "制造业",
    "餐饮",
    "娱乐",
    "环保",
    "慈善",
    "招聘",
    "报告",
    "人物",
    "邀请函",
    "文学",
    "会议",
]

CATEGORY_HUE_HINTS = {
    "春节": "暖红/金为传统主场，也可反套路用黛青底衬红",
    "建党节": "正红+金黄，庄重",
    "儿童节": "高饱和糖果色，蓝黄粉绿都行",
    "妇女节": "粉紫/玫红常见，也可用高级紫罗兰",
    "劳动节": "橙红活力或工装蓝",
    "重阳节": "秋色系：橙黄/枫红/暖棕",
    "母亲节": "康乃馨粉/暖珊瑚",
    "端午节": "粽叶绿/艾草青，配米黄",
    "中秋节": "月白桂黄配黛青夜色，或暖金圆月；反套路可用青瓷绿衬月白",
    "情人节": "玫红/酒红/粉，也可黑金反差",
    "万圣节": "橙黑紫经典组合",
    "清明节": "青绿/灰绿，素净",
    "安全日": "警示黄/红+深灰",
    "节气": "随节气取自然色：春青夏碧秋橙冬灰蓝",
    "开学季": "校园蓝/活力黄/黑板绿",
    "毕业季": "学士蓝/落日橙/纪念册米色",
    "医疗健康": "洁净蓝绿，也可暖橙传递关怀",
    "教育": "蓝/绿稳重或马卡龙活泼皆可",
    "党政": "正红+金/深蓝，庄重规整",
    "科技": "蓝紫/青，可反套路用暖橙",
    "电商": "促销暖橙/品红/大红",
    "母婴": "奶油黄/婴儿粉蓝/浅豆绿",
    "金融": "藏青/墨绿/月金",
    "婚庆": "香槟金/雾粉/酒红",
    "媒体": "黑白灰+单强调，报纸感",
    "制造业": "钢灰/工业蓝/安全橙",
    "餐饮": "食欲暖色：番茄红/芥末黄/焦糖棕",
    "娱乐": "霓虹/撞色/高饱和",
    "环保": "草木绿/大地棕/天空蓝",
    "慈善": "温暖橙黄/柔和蓝绿",
    "招聘": "企业蓝/活力橙",
    "报告": "红黑/蓝灰等严整商务色",
    "人物": "黑白灰突出人物，或单一情绪色",
    "邀请函": "黑金/香槟/深绿绒感/宝蓝",
    "文学": "米黄纸感/墨色/黛青",
    "会议": "深蓝/深灰+亮色强调",
}

# school → 适配题材（倾向不是规定）。短名单由此反查。
SCHOOL_CATEGORIES = {
    "极简留白": ["科技", "报告", "人物", "会议", "招聘", "金融", "制造业", "安全日", "医疗健康", "环保", "中秋节"],
    "杂志编辑风": ["媒体", "文学", "人物", "邀请函", "开学季", "毕业季", "教育"],
    "国潮/新中式": ["春节", "建党节", "党政", "文学", "节气", "端午节", "清明节", "重阳节", "中秋节"],
    "孟菲斯": ["儿童节", "娱乐", "电商", "母婴", "开学季", "教育"],
    "莫兰迪高级灰": ["婚庆", "母婴", "文学", "邀请函", "母亲节", "妇女节", "医疗健康", "慈善"],
    "极繁装饰": ["邀请函", "婚庆", "春节", "会议", "建党节"],
    "瑞士网格": ["报告", "制造业", "金融", "科技", "招聘", "安全日", "教育", "劳动节"],
    "复古印刷": ["文学", "人物", "媒体", "餐饮", "清明节", "重阳节", "毕业季", "端午节", "环保", "中秋节"],
    "赛博科技冷感": ["科技", "娱乐", "金融", "电商", "万圣节"],
    "清新手账": ["开学季", "教育", "母婴", "儿童节", "节气", "母亲节"],
    "商务简报": ["金融", "制造业", "招聘", "会议", "报告", "安全日", "劳动节", "医疗健康"],
    "奢侈品质感": ["婚庆", "邀请函", "金融", "人物", "情人节", "中秋节"],
    "报纸社论": ["媒体", "报告", "党政", "会议", "建党节", "人物", "毕业季"],
    "自然清透": ["环保", "医疗健康", "慈善", "节气", "清明节", "重阳节", "端午节", "母亲节", "中秋节"],
    "暖阳节庆": ["电商", "餐饮", "春节", "劳动节", "儿童节", "开学季", "端午节", "重阳节", "慈善", "中秋节"],
    "Y2K/酸性": ["娱乐", "电商", "科技", "开学季", "毕业季"],
    "波普拼贴": ["娱乐", "电商", "儿童节", "媒体", "妇女节", "情人节", "餐饮", "劳动节"],
    "暗黑霓虹": ["娱乐", "科技", "电商", "万圣节"],
    "法式浪漫": ["婚庆", "母婴", "餐饮", "情人节", "妇女节", "母亲节", "慈善"],
    "蒸汽波": ["娱乐", "科技", "毕业季", "文学", "万圣节"],
    "黑白高对比": ["人物", "媒体", "报告", "招聘", "党政", "安全日"],
}

VERSATILE_SCHOOLS = ["杂志编辑风", "极简留白", "瑞士网格", "复古印刷", "报纸社论"]

# ---- 流派规格表：兼容维 + 可执行版面规格 ----
#
# palettes / mediums / motions / routes：该流派的兼容集，抽签默认在集内取。
# titleFont：sans-serif（黑体）/ serif（宋体）/ monospace（等宽）——编辑器仅这三档。
# titleWeight：`<text>` 不解析 font-weight，恒为 400。≥600 的标题必须用
#   `<foreignObject>` 承载（titleCarrier 由脚本据此推出），最终服从 format 规则。
# titleSize / titleTracking：封面主标题字号与字距，正负 4px / 1px 内可按字数微调。
# safeMargin / gutter / cornerRadius：390 画布的左右安全边距、元素间距、圆角。
# imageTreatment：full-bleed 满幅出血 / inset-card 内缩圆角卡 / cutout 去底剪影 / framed 细边框。
# texture：版面质感词，只用于排版（边框、字距、栏线），不写进 styleAnchor。
#   图像质感走 IMAGE_TEXTURES。lighting：选图时的光线与质地锚。

SCHOOL_SPECS: dict[str, dict] = {
    "极简留白": {
        "palettes": ["黑白灰+单强调色", "单色系深浅渐进", "邻近色和谐", "三色分割(60-30-10)"],
        "mediums": ["胶片纪实摄影", "杂志棚拍", "手绘线稿上色", "印刷网纹"],
        "motions": ["克制点睛", "依次入场"],
        "routes": ["light-airy", "photo-led"],
        "titleFont": "sans-serif",
        "titleWeight": 400,
        "titleSize": 30,
        "titleTracking": 2,
        "bodyLineHeight": 1.9,
        "safeMargin": 36,
        "gutter": 20,
        "cornerRadius": 2,
        "imageTreatment": "inset-card",
        "texture": ["大量负空间", "细线分隔", "单一强调色"],
        "lighting": "均匀柔光，背景干净到近乎空白，主体小而精准，大面积留白",
    },
    "杂志编辑风": {
        "palettes": ["黑白灰+单强调色", "三色分割(60-30-10)", "复古褪色调", "大地色系", "金属点缀"],
        "mediums": ["胶片纪实摄影", "杂志棚拍", "印刷网纹"],
        "motions": ["依次入场", "克制点睛", "盖章定格"],
        "routes": ["photo-led", "light-airy"],
        "titleFont": "serif",
        "titleWeight": 700,
        "titleSize": 32,
        "titleTracking": 1,
        "bodyLineHeight": 1.75,
        "safeMargin": 24,
        "gutter": 16,
        "cornerRadius": 0,
        "imageTreatment": "full-bleed",
        "texture": ["大小字号强对比", "栏线", "英文小标"],
        "lighting": "杂志封面级布光，自然侧光或棚拍柔光，构图留出压标题的净空",
    },
    "国潮/新中式": {
        "palettes": ["金属点缀", "单色系深浅渐进", "互补撞色", "大地色系", "复古褪色调"],
        "mediums": ["水墨工笔", "木刻版画", "纸本拼贴", "印刷网纹"],
        "motions": ["依次入场", "克制点睛", "盖章定格"],
        "routes": ["light-airy", "chromatic-dark"],
        "titleFont": "serif",
        "titleWeight": 400,
        "titleSize": 30,
        "titleTracking": 4,
        "bodyLineHeight": 1.9,
        "safeMargin": 32,
        "gutter": 18,
        "cornerRadius": 0,
        "imageTreatment": "framed",
        "texture": ["朱红黛青", "留白与印章", "竖排意象"],
        "lighting": "宣纸质地，墨色晕染，大面积留白，边缘自然洇开",
    },
    "孟菲斯": {
        "palettes": ["高饱和双色撞色", "互补撞色", "粉彩马卡龙", "三色分割(60-30-10)"],
        "mediums": ["扁平贴纸插画", "黏土3D", "纸本拼贴"],
        "motions": ["依次入场", "入场+氛围", "强调脉冲"],
        "routes": ["light-airy", "chromatic-dark"],
        "titleFont": "sans-serif",
        "titleWeight": 800,
        "titleSize": 34,
        "titleTracking": 0,
        "bodyLineHeight": 1.7,
        "safeMargin": 20,
        "gutter": 14,
        "cornerRadius": 14,
        "imageTreatment": "cutout",
        "texture": ["撞色几何", "圆点波浪装饰", "活泼错位"],
        "lighting": "平光无阴影，纯色高饱和背景，形状边缘干脆",
    },
    "莫兰迪高级灰": {
        "palettes": ["邻近色和谐", "单色系深浅渐进", "复古褪色调", "渐变主导"],
        "mediums": ["杂志棚拍", "水彩淡彩", "黏土3D", "手绘线稿上色"],
        "motions": ["克制点睛", "主图循环"],
        "routes": ["light-airy"],
        "titleFont": "serif",
        "titleWeight": 400,
        "titleSize": 28,
        "titleTracking": 3,
        "bodyLineHeight": 1.9,
        "safeMargin": 32,
        "gutter": 18,
        "cornerRadius": 10,
        "imageTreatment": "inset-card",
        "texture": ["低饱和灰调", "同色系过渡", "温柔无对比"],
        "lighting": "阴天漫射光，低对比，边缘柔和，色彩蒙一层灰",
    },
    "极繁装饰": {
        "palettes": ["金属点缀", "单色系深浅渐进", "互补撞色", "复古褪色调"],
        "mediums": ["印刷网纹", "木刻版画", "纸本拼贴", "水墨工笔"],
        "motions": ["依次入场", "入场+氛围", "组合变换"],
        "routes": ["chromatic-dark", "light-airy"],
        "titleFont": "serif",
        "titleWeight": 700,
        "titleSize": 30,
        "titleTracking": 3,
        "bodyLineHeight": 1.8,
        "safeMargin": 30,
        "gutter": 14,
        "cornerRadius": 4,
        "imageTreatment": "framed",
        "texture": ["边框套边框", "繁复描边", "对称仪式感"],
        "lighting": "华丽布光，严格对称构图，繁复纹样铺满边缘",
    },
    "瑞士网格": {
        "palettes": ["黑白灰+单强调色", "三色分割(60-30-10)", "互补撞色"],
        "mediums": ["印刷网纹", "杂志棚拍", "胶片纪实摄影"],
        "motions": ["依次入场", "克制点睛"],
        "routes": ["light-airy", "photo-led"],
        "titleFont": "sans-serif",
        "titleWeight": 800,
        "titleSize": 34,
        "titleTracking": -0.5,
        "bodyLineHeight": 1.7,
        "safeMargin": 24,
        "gutter": 16,
        "cornerRadius": 0,
        "imageTreatment": "full-bleed",
        "texture": ["严整对齐", "粗黑标题", "功能主义"],
        "lighting": "平实纪实光，几何化构图，元素与画面边缘严格对齐",
    },
    "复古印刷": {
        "palettes": ["复古褪色调", "大地色系", "金属点缀", "单色系深浅渐进"],
        "mediums": ["印刷网纹", "木刻版画", "纸本拼贴", "手绘线稿上色"],
        "motions": ["盖章定格", "依次入场", "克制点睛"],
        "routes": ["light-airy"],
        "titleFont": "serif",
        "titleWeight": 700,
        "titleSize": 30,
        "titleTracking": 1,
        "bodyLineHeight": 1.8,
        "safeMargin": 26,
        "gutter": 16,
        "cornerRadius": 2,
        "imageTreatment": "framed",
        "texture": ["米黄纸感", "暗红墨绿", "做旧"],
        "lighting": "半调网点，油墨轻微错位，纸张纤维纹理，暖黄泛旧",
    },
    "赛博科技冷感": {
        "palettes": ["深色底+荧光强调", "互补撞色", "单色系深浅渐进", "金属点缀"],
        "mediums": ["杂志棚拍", "胶片纪实摄影", "黏土3D", "印刷网纹"],
        "motions": ["入场+氛围", "组合变换", "强调脉冲"],
        "routes": ["chromatic-dark"],
        "titleFont": "monospace",
        "titleWeight": 700,
        "titleSize": 30,
        "titleTracking": 2,
        "bodyLineHeight": 1.75,
        "safeMargin": 24,
        "gutter": 16,
        "cornerRadius": 2,
        "imageTreatment": "full-bleed",
        "texture": ["几何切角", "荧光青/品红点缀", "冷硬材质"],
        "lighting": "冷调霓虹补光，深色背景，主体边缘一道亮边光",
    },
    "清新手账": {
        "palettes": ["粉彩马卡龙", "邻近色和谐", "三色分割(60-30-10)", "单色系深浅渐进"],
        "mediums": ["扁平贴纸插画", "水彩淡彩", "手绘线稿上色", "纸本拼贴"],
        "motions": ["入场+氛围", "依次入场", "主图循环"],
        "routes": ["light-airy"],
        "titleFont": "sans-serif",
        "titleWeight": 700,
        "titleSize": 28,
        "titleTracking": 1,
        "bodyLineHeight": 1.8,
        "safeMargin": 26,
        "gutter": 14,
        "cornerRadius": 18,
        "imageTreatment": "cutout",
        "texture": ["马卡龙浅色", "圆角贴纸感", "轻盈"],
        "lighting": "明亮平光，浅色背景，柔和短投影，边缘圆润",
    },
    "商务简报": {
        "palettes": ["黑白灰+单强调色", "三色分割(60-30-10)", "单色系深浅渐进", "邻近色和谐"],
        "mediums": ["杂志棚拍", "胶片纪实摄影", "印刷网纹"],
        "motions": ["依次入场", "克制点睛"],
        "routes": ["light-airy", "photo-led"],
        "titleFont": "sans-serif",
        "titleWeight": 700,
        "titleSize": 30,
        "titleTracking": 0,
        "bodyLineHeight": 1.75,
        "safeMargin": 28,
        "gutter": 16,
        "cornerRadius": 6,
        "imageTreatment": "inset-card",
        "texture": ["藏青钢灰", "图表式秩序", "克制强调"],
        "lighting": "干净商务布光，中性色调，构图克制不炫技",
    },
    "奢侈品质感": {
        "palettes": ["金属点缀", "黑白灰+单强调色", "单色系深浅渐进"],
        "mediums": ["杂志棚拍", "胶片纪实摄影"],
        "motions": ["克制点睛", "盖章定格"],
        "routes": ["chromatic-dark", "light-airy"],
        "titleFont": "serif",
        "titleWeight": 400,
        "titleSize": 30,
        "titleTracking": 6,
        "bodyLineHeight": 2.0,
        "safeMargin": 40,
        "gutter": 20,
        "cornerRadius": 0,
        "imageTreatment": "framed",
        "texture": ["极窄边框线", "超大字距", "留白撑场"],
        "lighting": "低调侧光，深色背景，材质高光细腻，暗部有层次",
    },
    "报纸社论": {
        "palettes": ["黑白灰+单强调色", "复古褪色调", "三色分割(60-30-10)"],
        "mediums": ["胶片纪实摄影", "印刷网纹", "木刻版画"],
        "motions": ["克制点睛", "依次入场"],
        "routes": ["light-airy", "photo-led"],
        "titleFont": "serif",
        "titleWeight": 800,
        "titleSize": 34,
        "titleTracking": 0,
        "bodyLineHeight": 1.7,
        "safeMargin": 22,
        "gutter": 14,
        "cornerRadius": 0,
        "imageTreatment": "full-bleed",
        "texture": ["粗横线", "大标题压边", "双栏感"],
        "lighting": "纪实黑白，高对比硬光，可见颗粒，抓拍瞬间感",
    },
    "自然清透": {
        "palettes": ["邻近色和谐", "单色系深浅渐进", "三色分割(60-30-10)", "粉彩马卡龙"],
        "mediums": ["水彩淡彩", "胶片纪实摄影", "手绘线稿上色", "扁平贴纸插画"],
        "motions": ["主图循环", "入场+氛围", "克制点睛"],
        "routes": ["light-airy", "photo-led"],
        "titleFont": "sans-serif",
        "titleWeight": 400,
        "titleSize": 28,
        "titleTracking": 2,
        "bodyLineHeight": 1.9,
        "safeMargin": 30,
        "gutter": 18,
        "cornerRadius": 16,
        "imageTreatment": "inset-card",
        "texture": ["草木绿天空蓝", "有机圆角", "呼吸感"],
        "lighting": "逆光自然光，通透，浅景深，叶隙光斑",
    },
    "暖阳节庆": {
        "palettes": ["互补撞色", "三色分割(60-30-10)", "高饱和双色撞色", "金属点缀", "大地色系"],
        "mediums": ["扁平贴纸插画", "黏土3D", "纸本拼贴", "水彩淡彩"],
        "motions": ["入场+氛围", "强调脉冲", "依次入场"],
        "routes": ["light-airy", "chromatic-dark"],
        "titleFont": "sans-serif",
        "titleWeight": 800,
        "titleSize": 32,
        "titleTracking": 1,
        "bodyLineHeight": 1.75,
        "safeMargin": 24,
        "gutter": 14,
        "cornerRadius": 14,
        "imageTreatment": "cutout",
        "texture": ["橙红金暖调", "圆润饱满", "热闹点缀"],
        "lighting": "暖金光，喜庆氛围，柔和投影，色彩饱满",
    },
    "Y2K/酸性": {
        "palettes": ["渐变主导", "高饱和双色撞色", "深色底+荧光强调", "互补撞色"],
        "mediums": ["黏土3D", "扁平贴纸插画", "印刷网纹"],
        "motions": ["组合变换", "入场+氛围", "强调脉冲"],
        "routes": ["chromatic-dark", "light-airy"],
        "titleFont": "sans-serif",
        "titleWeight": 800,
        "titleSize": 36,
        "titleTracking": -1,
        "bodyLineHeight": 1.7,
        "safeMargin": 20,
        "gutter": 12,
        "cornerRadius": 20,
        "imageTreatment": "cutout",
        "texture": ["金属银质感", "扭曲错位", "千禧未来感"],
        "lighting": "金属反光，高光溢出，色相偏移，边缘发亮",
    },
    "波普拼贴": {
        "palettes": ["高饱和双色撞色", "互补撞色", "三色分割(60-30-10)"],
        "mediums": ["纸本拼贴", "印刷网纹", "木刻版画", "扁平贴纸插画"],
        "motions": ["依次入场", "强调脉冲", "组合变换"],
        "routes": ["light-airy", "chromatic-dark"],
        "titleFont": "sans-serif",
        "titleWeight": 900,
        "titleSize": 36,
        "titleTracking": 0,
        "bodyLineHeight": 1.7,
        "safeMargin": 20,
        "gutter": 12,
        "cornerRadius": 4,
        "imageTreatment": "cutout",
        "texture": ["大色块拼贴", "波点网纹", "漫画感"],
        "lighting": "硬光高对比，半调网点，剪纸般的硬边缘",
    },
    "暗黑霓虹": {
        "palettes": ["深色底+荧光强调", "互补撞色", "单色系深浅渐进"],
        "mediums": ["胶片纪实摄影", "杂志棚拍", "黏土3D"],
        "motions": ["入场+氛围", "强调脉冲", "组合变换"],
        "routes": ["chromatic-dark"],
        "titleFont": "sans-serif",
        "titleWeight": 800,
        "titleSize": 34,
        "titleTracking": 2,
        "bodyLineHeight": 1.75,
        "safeMargin": 24,
        "gutter": 14,
        "cornerRadius": 8,
        "imageTreatment": "full-bleed",
        "texture": ["霓虹描边", "近黑深底", "夜店气质"],
        "lighting": "霓虹边缘光，深夜街头，湿地面反光，紫青洋红光源",
    },
    "法式浪漫": {
        "palettes": ["邻近色和谐", "粉彩马卡龙", "复古褪色调", "单色系深浅渐进"],
        "mediums": ["水彩淡彩", "杂志棚拍", "手绘线稿上色", "胶片纪实摄影"],
        "motions": ["克制点睛", "主图循环"],
        "routes": ["light-airy"],
        "titleFont": "serif",
        "titleWeight": 400,
        "titleSize": 30,
        "titleTracking": 4,
        "bodyLineHeight": 1.95,
        "safeMargin": 34,
        "gutter": 18,
        "cornerRadius": 12,
        "imageTreatment": "inset-card",
        "texture": ["奶油白雾粉", "纤细字重", "慵懒优雅"],
        "lighting": "晨间柔光，纱帘散射，低饱和，画面轻微过曝",
    },
    "蒸汽波": {
        "palettes": ["渐变主导", "深色底+荧光强调", "互补撞色"],
        "mediums": ["印刷网纹", "黏土3D", "杂志棚拍", "胶片纪实摄影"],
        "motions": ["组合变换", "入场+氛围", "主图循环"],
        "routes": ["chromatic-dark"],
        "titleFont": "monospace",
        "titleWeight": 700,
        "titleSize": 32,
        "titleTracking": 4,
        "bodyLineHeight": 1.8,
        "safeMargin": 24,
        "gutter": 16,
        "cornerRadius": 6,
        "imageTreatment": "full-bleed",
        "texture": ["粉紫青色阶", "日落地平线", "梦核氛围"],
        "lighting": "日落渐层天空，紫粉洋红，复古噪点，低角度地平线",
    },
    "黑白高对比": {
        "palettes": ["黑白灰+单强调色", "互补撞色"],
        "mediums": ["胶片纪实摄影", "木刻版画", "印刷网纹", "杂志棚拍"],
        "motions": ["盖章定格", "克制点睛", "依次入场"],
        "routes": ["photo-led", "light-airy"],
        "titleFont": "sans-serif",
        "titleWeight": 900,
        "titleSize": 40,
        "titleTracking": -1,
        "bodyLineHeight": 1.7,
        "safeMargin": 20,
        "gutter": 12,
        "cornerRadius": 0,
        "imageTreatment": "full-bleed",
        "texture": ["超粗字重", "大面积对撞", "海报感"],
        "lighting": "高对比黑白，硬光，强烈明暗分界，几乎无中间调",
    },
}

# 给 styleAnchor 的图像质感词，描述照片/插画本身的质地。
# 与 SCHOOL_SPECS 的 texture 严格分开：texture 讲的是版面（边框、字距、留白、栏线），
# 把它写进 styleAnchor，版面上会出现不该有的边框和文字感。
IMAGE_TEXTURES: dict[str, list[str]] = {
    "极简留白": ["主体单一", "静谧克制"],
    "杂志编辑风": ["时尚大片质感", "环境细节真实"],
    "国潮/新中式": ["东方意境", "传统器物细节"],
    "孟菲斯": ["几何形状鲜明", "玩具般轻快"],
    "莫兰迪高级灰": ["哑光质地", "静物般安静"],
    "极繁装饰": ["纹样繁复", "华丽厚重"],
    "瑞士网格": ["理性克制", "画面干净"],
    "复古印刷": ["旧海报质感", "岁月痕迹"],
    "赛博科技冷感": ["精密工业质感", "金属玻璃材质"],
    "清新手账": ["轻盈通透", "柔软可亲"],
    "商务简报": ["专业整洁", "真实可信"],
    "奢侈品质感": ["低调奢华", "材质纹理考究"],
    "报纸社论": ["新闻现场感", "未经修饰"],
    "自然清透": ["自然生机", "水润清透"],
    "暖阳节庆": ["圆润饱满", "热闹亲切"],
    "Y2K/酸性": ["液态金属质感", "千禧塑料感"],
    "波普拼贴": ["拼贴剪纸感", "大色块并置"],
    "暗黑霓虹": ["潮湿夜色", "冷硬都市感"],
    "法式浪漫": ["柔焦朦胧", "慵懒优雅"],
    "蒸汽波": ["石膏像与塑料质感", "怀旧失真"],
    "黑白高对比": ["粗粝有力", "轮廓分明"],
}

CLIMAX_MECHANICS = {
    "clickSwitch-真假": "clickSwitch",
    "clickSwitch-误区正解": "clickSwitch",
    "clickSwitch-前后": "clickSwitch",
    "clickSwitch-日夜": "clickSwitch",
    "details-满幅翻页": "details",
    "animationGroup-特写": "svg",
    "static-数字压屏": "svg",
    "static-金句压屏": "svg",
}

TAKEAWAY_FORMS = ["金句卡", "清单", "步骤条", "引用卡", "CTA胶囊"]

# 作品壳，不参与随机。与 references/formats/index.md 已落地项同步。
ARTICLE_FORMATS = [
    "layered-scroll",
    "parallax-scroll",
    "coloring-scroll",
    "quiz",
    "choice-expand",
    "scene-transition",
]

SATURATIONS = ["低", "中", "高"]
DESATURATE_STRATEGIES = {"深色底+荧光强调", "高饱和双色撞色"}

DEFAULT_HISTORY_FILE = os.path.expanduser(
    "~/.cache/weipaiban/direction-history.jsonl"
)
RECENT_WINDOW = 8
EXCLUDE_RECENT = 3
HUE_BUCKET_SIZE = 30
WILDCARD_RATE = 0.2
OFF_SPEC_RATE = 0.15
BOLD_WEIGHT_FLOOR = 600


def load_history(path: str) -> list[dict]:
    if not os.path.isfile(path):
        return []
    records: list[dict] = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    item = json.loads(line)
                    if isinstance(item, dict):
                        records.append(item)
                except json.JSONDecodeError:
                    continue
    except OSError:
        return []
    return records[-RECENT_WINDOW:]


def append_history(path: str, record: dict) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def pick_excluding(pool: list[str], recent_values: list[str]) -> str:
    recent = recent_values[-EXCLUDE_RECENT:]
    candidates = [x for x in pool if x not in recent]
    if not candidates:
        candidates = [x for x in pool if x not in recent_values[-1:]] or pool
    return random.choice(candidates)


def pick_in_spec(
    fit_pool: list[str], full_pool: list[str], recent: list[str]
) -> tuple[str, bool]:
    """默认在流派兼容集内抽；小概率越界，越界记为 off-spec（有意反差）。"""
    off_pool = [x for x in full_pool if x not in fit_pool]
    off_spec = bool(off_pool) and random.random() < OFF_SPEC_RATE
    pool = off_pool if off_spec else fit_pool
    return pick_excluding(pool, recent), off_spec


def pick_hue_seed(recent_buckets: list[int]) -> int:
    avoid = set(recent_buckets[-EXCLUDE_RECENT:])
    for _ in range(50):
        seed = random.randrange(360)
        if seed // HUE_BUCKET_SIZE not in avoid:
            return seed
    return random.randrange(360)


def shortlist_for(category: str) -> list[str]:
    hits = [school for school, cats in SCHOOL_CATEGORIES.items() if category in cats]
    if len(hits) < 4:
        for school in VERSATILE_SCHOOLS:
            if school not in hits:
                hits.append(school)
            if len(hits) >= 4:
                break
    return hits or list(SCHOOLS)


def pick_school(category: str | None, recent: list[str]) -> tuple[str, bool]:
    if not category:
        return pick_excluding(SCHOOLS, recent), False
    fit = shortlist_for(category)
    contrast_pool = [school for school in SCHOOLS if school not in fit]
    use_wildcard = bool(contrast_pool) and random.random() < WILDCARD_RATE
    pool = contrast_pool if use_wildcard else fit
    return pick_excluding(pool, recent), use_wildcard


def wechat_adapt(school: str, strategy: str, route: str) -> list[str]:
    notes: list[str] = []
    if route == "chromatic-dark":
        notes.append("canvas-chromatic-dark")
    if route == "photo-led":
        notes.append("text-on-photo-safe")
    if school == "黑白高对比":
        notes.append("high-contrast-gray-plus-accent")
    if strategy in DESATURATE_STRATEGIES:
        notes.append("desaturate-for-wechat")
    return notes


def build_typography(spec: dict) -> dict:
    weight = spec["titleWeight"]
    return {
        "titleFont": spec["titleFont"],
        "titleWeight": weight,
        # <text> 不解析 font-weight（恒 400），粗标题只能走 foreignObject
        "titleCarrier": "foreignObject" if weight >= BOLD_WEIGHT_FLOOR else "text",
        "titleSize": spec["titleSize"],
        "titleTracking": spec["titleTracking"],
        "bodySize": 15,
        "bodyLineHeight": spec["bodyLineHeight"],
        "captionSize": 12,
    }


def build_layout(spec: dict) -> dict:
    return {
        "safeMargin": spec["safeMargin"],
        "gutter": spec["gutter"],
        "cornerRadius": spec["cornerRadius"],
        "imageTreatment": spec["imageTreatment"],
    }


def self_check() -> int:
    """校验流派规格表与各清单的一致性。"""
    problems: list[str] = []
    for school in SCHOOLS:
        spec = SCHOOL_SPECS.get(school)
        if spec is None:
            problems.append(f"SCHOOL_SPECS 缺少流派：{school}")
            continue
        for value in spec["palettes"]:
            if value not in PALETTE_STRATEGIES:
                problems.append(f"{school}: 配色策略「{value}」不在清单内")
        for value in spec["mediums"]:
            if value not in IMAGE_MEDIUMS:
                problems.append(f"{school}: 图像介质「{value}」不在清单内")
        for value in spec["motions"]:
            if value not in MOTIONS:
                problems.append(f"{school}: 动效方案「{value}」不在清单内")
        for value in spec["routes"]:
            if value not in COLOR_ROUTES:
                problems.append(f"{school}: 色彩路线「{value}」不在清单内")
    for school in SCHOOL_SPECS:
        if school not in SCHOOLS:
            problems.append(f"SCHOOL_SPECS 多出流派：{school}")
    for school in SCHOOLS:
        if school not in IMAGE_TEXTURES:
            problems.append(f"IMAGE_TEXTURES 缺少流派：{school}")
    for school in IMAGE_TEXTURES:
        if school not in SCHOOLS:
            problems.append(f"IMAGE_TEXTURES 多出流派：{school}")
    for category in CATEGORIES:
        if category not in CATEGORY_HUE_HINTS:
            problems.append(f"CATEGORY_HUE_HINTS 缺少题材：{category}")

    if problems:
        for line in problems:
            print(f"✗ {line}", file=sys.stderr)
        return 1
    print(f"✓ {len(SCHOOLS)} 个流派规格完整，各维词条与清单一致")
    return 0


def die(flag: str, value: str, allowed: list[str]) -> int:
    print(
        f"错误：{flag}「{value}」不在合法清单内：{'、'.join(allowed)}",
        file=sys.stderr,
    )
    return 2


def main() -> int:
    parser = argparse.ArgumentParser(description="为交互作品抽取一个可选视觉方向")
    parser.add_argument("--category", help="题材类别（缺省不按题材收短名单）")
    parser.add_argument("--school", help="指定流派，跳过该维抽签")
    parser.add_argument("--palette-strategy", help="指定配色策略")
    parser.add_argument("--color-route", help="指定色彩路线：light-airy / chromatic-dark / photo-led")
    parser.add_argument("--cover-composition", help="指定封面构图")
    parser.add_argument("--climax-mechanic", help="指定高潮机制")
    parser.add_argument("--motion", help="指定动效方案")
    parser.add_argument("--image-medium", help="指定图像介质")
    parser.add_argument("--takeaway-form", help="指定收口形态")
    parser.add_argument(
        "--format",
        dest="article_format",
        help="作品 format；layered-scroll、parallax-scroll、coloring-scroll、quiz、choice-expand 或 scene-transition",
    )
    parser.add_argument("--history-file", default=DEFAULT_HISTORY_FILE, help="历史 jsonl 路径")
    parser.add_argument("--no-history", action="store_true", help="不读不写历史（调试用）")
    parser.add_argument("--self-check", action="store_true", help="只校验规格表一致性后退出")
    args = parser.parse_args()

    if args.self_check:
        return self_check()

    if args.category and args.category not in CATEGORIES:
        return die("--category", args.category, CATEGORIES)
    if args.school and args.school not in SCHOOLS:
        return die("--school", args.school, SCHOOLS)
    if args.palette_strategy and args.palette_strategy not in PALETTE_STRATEGIES:
        return die("--palette-strategy", args.palette_strategy, PALETTE_STRATEGIES)
    if args.color_route and args.color_route not in COLOR_ROUTES:
        return die("--color-route", args.color_route, COLOR_ROUTES)
    if args.cover_composition and args.cover_composition not in COMPOSITIONS:
        return die("--cover-composition", args.cover_composition, COMPOSITIONS)
    if args.climax_mechanic and args.climax_mechanic not in CLIMAX_MECHANICS:
        return die("--climax-mechanic", args.climax_mechanic, list(CLIMAX_MECHANICS))
    if args.motion and args.motion not in MOTIONS:
        return die("--motion", args.motion, MOTIONS)
    if args.image_medium and args.image_medium not in IMAGE_MEDIUMS:
        return die("--image-medium", args.image_medium, IMAGE_MEDIUMS)
    if args.takeaway_form and args.takeaway_form not in TAKEAWAY_FORMS:
        return die("--takeaway-form", args.takeaway_form, TAKEAWAY_FORMS)
    if args.article_format and args.article_format not in ARTICLE_FORMATS:
        return die("--format", args.article_format, ARTICLE_FORMATS)

    history = [] if args.no_history else load_history(args.history_file)

    def recent_of(key: str) -> list[str]:
        return [r[key] for r in history if isinstance(r.get(key), str)]

    recent_buckets = [r["hueBucket"] for r in history if isinstance(r.get("hueBucket"), int)]

    contrast = False
    if args.school:
        school = args.school
    else:
        school, contrast = pick_school(args.category, recent_of("school"))

    spec = SCHOOL_SPECS[school]

    palette_off_spec = False
    if args.palette_strategy:
        strategy = args.palette_strategy
    else:
        strategy, palette_off_spec = pick_in_spec(
            spec["palettes"], PALETTE_STRATEGIES, recent_of("paletteStrategy")
        )

    medium_off_spec = False
    if args.image_medium:
        image_medium = args.image_medium
    else:
        image_medium, medium_off_spec = pick_in_spec(
            spec["mediums"], IMAGE_MEDIUMS, recent_of("imageMedium")
        )

    color_route = args.color_route or pick_excluding(spec["routes"], recent_of("colorRoute"))
    motion = args.motion or pick_excluding(spec["motions"], recent_of("motion"))
    cover_composition = args.cover_composition or pick_excluding(
        COMPOSITIONS, recent_of("coverComposition")
    )
    climax_mechanic = args.climax_mechanic or pick_excluding(
        list(CLIMAX_MECHANICS), recent_of("climaxMechanic")
    )
    takeaway_form = args.takeaway_form or pick_excluding(
        TAKEAWAY_FORMS, recent_of("takeawayForm")
    )
    hue_seed = pick_hue_seed(recent_buckets)
    techniques = random.sample(TECHNIQUES, k=random.choice([1, 2]))
    saturation = random.choice(SATURATIONS)
    tone = "深底" if color_route == "chromatic-dark" else "浅底"

    typography = build_typography(spec)
    image_texture_words = "，".join(IMAGE_TEXTURES[school])

    direction = {
        "category": args.category,
        "school": school,
        "contrast": contrast,
        "paletteStrategy": strategy,
        "paletteOffSpec": palette_off_spec,
        "colorRoute": color_route,
        "hue": {
            "seed": hue_seed,
            "saturation": saturation,
            "tone": tone,
        },
        "huePriority": random.choice(["seed", "category"]) if args.category else "seed",
        "categoryHueHint": CATEGORY_HUE_HINTS.get(args.category or "", ""),
        "techniques": techniques,
        "coverComposition": cover_composition,
        "climaxMechanic": climax_mechanic,
        "climaxKind": CLIMAX_MECHANICS[climax_mechanic],
        "motion": motion,
        "imageMedium": image_medium,
        "imageMediumOffSpec": medium_off_spec,
        "takeawayForm": takeaway_form,
        "format": args.article_format or "layered-scroll",
        "typography": typography,
        "layout": build_layout(spec),
        "wechatAdapt": wechat_adapt(school, strategy, color_route),
        "styleAnchorHint": f"{school}，{image_medium}，{image_texture_words}",
        "styleAnchorNote": (
            "落 asset-request 时在 styleAnchor 末尾补一句具体色调词（如「暖金与深棕色调」），"
            "取自 palette 主色。不要把 paletteStrategy 的策略名写进去。"
        ),
        "lightingHint": spec["lighting"],
    }

    if not args.no_history:
        append_history(
            args.history_file,
            {
                "ts": int(time.time()),
                "category": args.category,
                "school": school,
                "contrast": contrast,
                "paletteStrategy": strategy,
                "colorRoute": color_route,
                "hueBucket": hue_seed // HUE_BUCKET_SIZE,
                "coverComposition": cover_composition,
                "climaxMechanic": climax_mechanic,
                "motion": motion,
                "imageMedium": image_medium,
                "takeawayForm": takeaway_form,
            },
        )

    print(json.dumps(direction, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
