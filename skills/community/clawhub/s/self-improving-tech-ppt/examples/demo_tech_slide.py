#!/usr/bin/env python3
"""
Full-Page High-Density Executive Technical Architecture Template (v1.1.0).
Serves as the canonical structural reference for ALL LLMs (ChatGPT, DeepSeek, Claude, Gemini)
so models NEVER drift into sparse 12-node "Gamma/Keynote blog slides" or teal+orange AI-slop.

Demonstrates:
  - Default locked `executive-blue` palette (switchable via CLI arg: `slate-minimal` / `steel-teal` / `academic-indigo`)
  - Compact 48pt executive header (zero giant hero whitespace)
  - Top Problem -> Goal band with anti-circular `forbid_terms=("DSL",)`
  - Left 3 Split-Card Challenges (abstract technical mini-schematics + numbered points) + Bottom Core Concept card
  - Right 3-Swimlane Technical Architecture (micro-chip modules + diamonds + petite white cylinders + Spec cards)
  - Bottom Evolution Strip with orthogonal feedback loop
  - Passes strict `run_self_check(scene, mode="tech-arch")` with 100+ nodes & 20+ orthogonal edges!
"""
import os
import sys
import tempfile

SCRIPT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts")
sys.path.insert(0, SCRIPT_DIR)

from ppt_engine import (
    DEFAULT_THEME_NAME,
    Scene,
    TextRun,
    add_arch_header,
    add_chip_module,
    add_header_strip_module,
    add_labeled_box,
    add_problem_goal_band,
    add_swimlane_shell,
    export_pptx,
    render_quicklook_and_crop,
    run_self_check,
)


def build_full_arch_slide(theme_name: str = DEFAULT_THEME_NAME) -> Scene:
    s = Scene("full-tech-arch-template", theme_name=theme_name)
    t = s.theme

    # 1. Compact Header (y=0..50)
    add_arch_header(s, "规则表达编译与校验技术：将业务语义表达为机器可计算、可执行、可复用的规则本体")

    # 2. Top Problem -> Goal Band (y=56..107) — ZERO mention of 'DSL' in Problems!
    add_problem_goal_band(
        s,
        problems=[
            ("规则停留在文本描述，无法计算与执行", "条件阈值、单位换算与步骤依赖混在纯文本中，检索与运行层无法直接调用。"),
            ("生成缺少规范与标准约束，质量不可控", "自由抽取结构易变，跨场景术语口径难对齐，单靠模型打分难核验逻辑原意。"),
        ],
        goal_title="表达为机器可理解、可执行、可复用的规则本体",
        goal_sub="引入声明式规则 DSL，实现受限编译、标准标识演进与双重质量核验",
        forbid_terms=("DSL",),
    )

    # 3. Left Column: 3 Technical Challenges (y=114..384) + Core Concept Card (y=390..526)
    s.add_node("rrect", 16, 114, 24, 270, fill=t["blue_main"], radius=4.0,
               text="技\n术\n挑\n战", font_size=9.5, font_color=t["white"], bold=True, line_spacing=1.72, pad_x=1)

    lx, lw = 45, 307
    s.add_node("rrect", lx, 114, lw, 20, fill=t["blue_pale"], stroke=t["border"], stroke_w=0.8, radius=3.5,
               text="语义输入 → 标准规则本体 三个核心技术挑战", font_size=7.6, font_color=t["navy"], bold=True,
               single_line_each_para=True, forbid_terms=("DSL",))
    s.add_node("chevron_r", 355, 119.5, 14, 9, fill=t["border"])

    challenges = [
        ("挑战 1", t["blue_mid"], "自然语义如何稳定转为可计算、可执行结构？",
         "1、同一定义须兼顾对外匹配契约与内部步骤依赖，且必须剥离底层接口。",
         "2、阈值、公式计算与多目标权衡混在文本中，自由抽取每次结构不一。",
         [("条件", t["white"]), ("单位", t["white"]), ("步骤", t["white"])], "文本混写 ≠ 接口未剥离"),
        ("挑战 2", t["blue_mid"], "跨场景要素如何对齐口径并支持持续演进？",
         "1、对象、属性、关系与单位说法不一，同名概念在不同领域含义不同。",
         "2、新业务持续出现未收录项，直接覆盖破坏存量，各自新建又难复用。",
         [("同词异义", t["amber_bg"]), ("多套单位", t["amber_bg"])], "统一标识 · 分域隔离"),
        ("挑战 3", t["navy_deep"], "格式合规的产物如何准确核验逻辑与原意？",
         "1、语法合法仍可能出现引用失效、单位冲突、缺前置输入或依赖成环。",
         "2、单靠大模型综合打分不稳定，难以发现漏掉否定词或条件正反写反。",
         [("格式合规", t["blue_pale"]), ("逻辑冲突", t["amber_bg"])], "格式对 ≠ 逻辑原意对"),
    ]
    cy, ch = 139, 78.5
    for idx, (badge, bcol, ctitle, cp1, cp2, tags, cap) in enumerate(challenges):
        s.add_node("rrect", lx, cy, lw, ch, fill=t["white"], stroke=t["border"], stroke_w=0.85, radius=4.5)
        mx, my, mw, mh = lx + 6, cy + 6, 108, ch - 12
        s.add_node("rrect", mx, my, mw, mh, fill=t["panel_bg"], stroke=t["border_lt"], stroke_w=0.75, radius=3.5)
        tw = (mw - 10 - 3 * (len(tags) - 1)) / len(tags)
        for ti, (ttxt, tbg) in enumerate(tags):
            is_amb = (tbg == t["amber_bg"])
            s.add_node("rrect", mx + 5 + ti * (tw + 3), my + 12, tw, 17, fill=tbg,
                       stroke=t["amber_bdr"] if is_amb else t["border"], stroke_w=0.75, radius=2.5,
                       text=ttxt, font_size=5.2, font_color=t["amber"] if is_amb else t["navy"], bold=True,
                       pad_x=0, single_line_each_para=True, forbid_terms=("DSL",))
        s.add_node("rrect", mx + 5, my + 39, mw - 10, 17, fill=t["white"], stroke=t["border"], stroke_w=0.7, radius=2.5,
                   text=cap, font_size=5.0, font_color=t["muted"], bold=True, pad_x=0,
                   single_line_each_para=True, forbid_terms=("DSL",))
        rx_c, rw_c = mx + mw + 7, lw - mw - 19
        s.add_node("rrect", rx_c, cy + 5, 42, 14.5, fill=bcol, radius=3.0,
                   text=badge, font_size=6.6, font_color=t["white"], bold=True, pad_x=0, single_line_each_para=True)
        s.add_node("rect", rx_c, cy + 21, rw_c, 13, align="left", text=ctitle, font_size=7.0,
                   font_color=t["navy"], bold=True, pad_x=0, single_line_each_para=True, forbid_terms=("DSL",))
        s.add_node("rect", rx_c, cy + 34.5, rw_c, 20, align="left", text=cp1, font_size=6.3,
                   font_color=t["text"], pad_x=0, line_spacing=1.15, forbid_terms=("DSL",))
        s.add_node("rect", rx_c, cy + 55, rw_c, 20, align="left", text=cp2, font_size=6.3,
                   font_color=t["text"], pad_x=0, line_spacing=1.15, forbid_terms=("DSL",))
        cy += ch + 5

    # Bottom-Left Core Concept Card: 规则 DSL (y=390..526)
    s.add_node("rrect", 16, 390, 24, 136, fill=t["navy_deep"], radius=4.0,
               text="规\n则\nD\nS\nL", font_size=9.2, font_color=t["white"], bold=True, line_spacing=1.42, pad_x=1)
    dx, dy, dw, dh = lx, 390, lw, 136
    s.add_node("rrect", dx, dy, dw, dh, fill=t["panel_bg"], stroke=t["blue_mid"], stroke_w=0.95, radius=4.5)
    s.add_node("rrect", dx + 5, dy + 5, dw - 10, 20, fill=t["navy_deep"], radius=3.0, align="left",
               text="DSL ＝ Domain-Specific Language · 领域特定语言", font_size=7.3, font_color=t["white"],
               bold=True, pad_x=6, single_line_each_para=True)
    s.add_node("rrect", dx + 5, dy + 28, dw - 10, 54, fill=t["white"], stroke=t["border_lt"], stroke_w=0.75, radius=3.0)
    s.add_node("rect", dx + 5, dy + 31, 2.3, 48, fill=t["blue_main"], stroke_w=0)
    s.add_node("rect", dx + 11, dy + 29, dw - 20, 52, align="left", pad_x=1, pad_y=0, line_spacing=1.18,
               runs=[
                   [TextRun("定位与价值：", color=t["navy"], bold=True, size=6.5),
                    TextRun("面向规则表达的声明式语言。比纯文本有严格语法，可约束生成与静态检查；相比硬编码剥离接口，支持跨场景复用。", color=t["text"], size=6.3)],
                   [TextRun("产出与运行形态：", color=t["navy"], bold=True, size=6.5),
                    TextRun("生成标准定义文件，供匹配检索直接计算；运行时可编译为可执行代码，或配合运行层绑定外部接口资源。", color=t["text"], size=6.3)],
               ])
    for si, (stitle, sflds, sdesc) in enumerate([
        ("对外契约 · 供匹配与复用计算", "subject / scope / io / effect", "对象 · 范围 · 输入输出 · 规则树"),
        ("执行逻辑 · 编译代码或接运行层", "steps / dag / gov / trace", "步骤依赖图 · 治理点 · 剥离接口"),
    ]):
        sx_c = dx + 5 + si * 151.5
        s.add_node("rrect", sx_c, dy + 86, 145.5, 44, fill=t["white"], stroke=t["blue_line"], stroke_w=0.8, radius=3.0)
        s.add_node("rrect", sx_c + 1, dy + 87, 143.5, 13.5, fill=t["blue_pale"], radius=2.2,
                   text=stitle, font_size=6.1, font_color=t["blue_main"], bold=True, pad_x=1, single_line_each_para=True)
        s.add_node("rect", sx_c + 5, dy + 102, 136, 25, align="left", pad_x=1, line_spacing=1.16,
                   runs=[
                       [TextRun(sflds, color=t["navy"], bold=True, size=6.0)],
                       [TextRun(sdesc, color=t["muted"], size=5.7)],
                   ])

    # Tapered soft transition wedge
    s.add_node("wedge_r", 355, 165, 14, 306, grad_fill=(t["panel_bg"], t["blue_soft"], 0))

    # 4. Right Panel: Solution Pipeline + 3 Horizontal Swimlanes (1:1 with Left Challenges!) + Bottom Strip
    rx, rw = 373, 571
    s.add_node("rrect", rx, 114, rw, 412, fill=t["white"], stroke=t["border"], stroke_w=0.95, radius=5.0)

    # Top Solution Pipeline Strip
    s.add_node("rrect", rx + 7, 119, 62, 19, fill=t["blue_pale"], stroke=t["border"], stroke_w=0.75, radius=3.0,
               text="技术解决方案", font_size=7.0, font_color=t["navy"], bold=True, single_line_each_para=True)
    s.add_node("rrect", rx + 75, 119, 80, 19, fill=t["panel_bg"], stroke=t["border"], stroke_w=0.75, radius=3.0,
               text="已确认业务语义", font_size=6.9, font_color=t["navy"], bold=True, single_line_each_para=True)
    s.add_edge([(rx + 155, 128.5), (rx + 166, 128.5)], stroke=t["blue_main"])
    s.add_node("rrect", rx + 166, 119, 238, 19, fill=t["blue_main"], radius=3.0,
               text="规则 DSL 引擎：受限解码 · 实体对齐 · 双重核验", font_size=7.0, font_color=t["white"],
               bold=True, single_line_each_para=True)
    s.add_edge([(rx + 404, 128.5), (rx + 415, 128.5)], stroke=t["blue_main"])
    s.add_node("rrect", rx + 415, 119, 149, 19, fill=t["blue_soft"], stroke=t["blue_line"], stroke_w=0.8, radius=3.0,
               text="正式规则本体 DSL · 供匹配执行", font_size=6.8, font_color=t["navy"], bold=True, single_line_each_para=True)

    sx, sw = rx + 7, rw - 14
    d1x, spec_x, spec_w = sx + 31, sx + 379, 173
    lh = 109

    # Swimlane 1: 结构编译技术
    y1 = 143
    add_swimlane_shell(s, sx, y1, sw, lh, "结\n构\n编\n译\n技\n术")
    add_labeled_box(s, d1x, y1 + 14, 48, 29, "输入语义", "条件/步骤")
    s.add_edge([(d1x + 48, y1 + 28.5), (d1x + 58, y1 + 28.5)], stroke=t["blue_main"])
    add_labeled_box(s, d1x + 58, y1 + 14, 72, 29, "JSON Schema\n受限解码", "约束输出·建追踪表",
                    fill=t["blue_main"], stroke="none", title_color=t["white"], sub_color=t["sub_white"], title_size=6.0)
    s.add_node("can", d1x + 62, y1 + 57, 64, 33, fill=t["white"], stroke=t["blue_line"], stroke_w=0.85,
               text="DSL 语法规范库\nSchema · 算子", font_size=5.4, font_color=t["navy"], bold=True, pad_x=2, pad_y=1)
    s.add_edge([(d1x + 94, y1 + 57), (d1x + 94, y1 + 43)], stroke=t["blue_line"])
    s.add_edge([(d1x + 130, y1 + 28.5), (d1x + 149, y1 + 28.5)], stroke=t["blue_main"])
    s.add_edge([(d1x + 140, y1 + 28.5), (d1x + 140, y1 + 74), (d1x + 149, y1 + 74)], stroke=t["blue_main"])
    add_chip_module(s, d1x + 149, y1 + 12.5, 122, 32, "ExprAST 规则树编译", ["比较节点", "纯函数", "权衡边界"], cols=3)
    add_chip_module(s, d1x + 149, y1 + 58, 122, 32, "端口推演与 DAG 构建", ["op1/op2→op3", "剥离外部接口"], cols=2)
    s.add_edge([(d1x + 271, y1 + 28.5), (d1x + 278, y1 + 28.5), (d1x + 278, y1 + 51.5), (d1x + 286, y1 + 51.5)], stroke=t["blue_main"])
    s.add_edge([(d1x + 271, y1 + 74), (d1x + 278, y1 + 74), (d1x + 278, y1 + 51.5)], stroke=t["blue_main"], arrow_end=False)
    s.add_node("stadium", d1x + 286, y1 + 39.5, 58, 24, fill=t["blue_main"],
               text="本体 DSL\n编译初稿", font_size=6.1, font_color=t["white"], bold=True, pad_x=2, line_spacing=1.10)
    # Spec Card 1
    s.add_node("rrect", spec_x, y1 + 5, spec_w, lh - 10, fill=t["white"], stroke=t["blue_line"], stroke_w=0.8, dashed=True, radius=3.5)
    s.add_node("rrect", spec_x + 4, y1 + 8, spec_w - 8, 16, fill=t["blue_mid"], radius=2.5,
               text="核心编译技术｜结构与可计算性", font_size=6.4, font_color=t["white"], bold=True, single_line_each_para=True)
    add_labeled_box(s, spec_x + 5, y1 + 27, spec_w - 10, 24, "可计算 ExprAST 规则树", "禁用任意脚本 · 内置单位换算", fill=t["panel_bg"], stroke=t["border"])
    add_labeled_box(s, spec_x + 5, y1 + 54, spec_w - 10, 24, "契约与执行逻辑解耦", "具体接口交由运行层绑定或生成代码", fill=t["blue_pale"], stroke=t["blue_line"])
    s.add_node("rrect", spec_x + 4, y1 + 82, spec_w - 8, 17, fill=t["blue_soft"], radius=2.5,
               text="生成语义项 ↔ AST 双向追踪表", font_size=6.0, font_color=t["navy"], bold=True, single_line_each_para=True)

    # Swimlane 2: 归一演进技术
    y2 = 258
    add_swimlane_shell(s, sx, y2, sw, lh, "归\n一\n演\n进\n技\n术")
    add_labeled_box(s, d1x, y2 + 12, 46, 27, "候选要素", "对象/指标")
    s.add_edge([(d1x + 46, y2 + 25.5), (d1x + 54, y2 + 25.5)], stroke=t["blue_main"])
    add_labeled_box(s, d1x + 54, y2 + 12, 64, 27, "多维实体对齐", "向量·Jaccard\n关系·单位", fill=t["blue_pale"])
    s.add_edge([(d1x + 118, y2 + 25.5), (d1x + 126, y2 + 25.5)], stroke=t["blue_main"])
    s.add_node("diamond", d1x + 126, y2 + 10.5, 62, 30, fill=t["white"], stroke=t["blue_main"], stroke_w=0.85,
               text="口径一致?", font_size=5.7, font_color=t["navy"], bold=True, pad_x=0)
    s.add_edge([(d1x + 188, y2 + 25.5), (d1x + 201, y2 + 25.5)], stroke=t["blue_main"])
    add_labeled_box(s, d1x + 201, y2 + 12, 58, 27, "绑定标准标识", "统一基准单位",
                    fill=t["blue_main"], stroke="none", title_color=t["white"], sub_color=t["sub_white"], title_size=5.9)
    s.add_edge([(d1x + 259, y2 + 25.5), (d1x + 281, y2 + 25.5)], stroke=t["blue_main"])
    add_labeled_box(s, d1x + 281, y2 + 12, 63, 27, "口径与版本", "标识 · 单位基准")
    s.add_edge([(d1x + 312.5, y2 + 51), (d1x + 312.5, y2 + 39)], stroke=t["blue_line"])
    s.add_edge([(d1x + 157, y2 + 40.5), (d1x + 157, y2 + 49), (d1x + 30, y2 + 49), (d1x + 30, y2 + 62)],
               stroke=t["amber_bdr"], dashed=True)
    add_labeled_box(s, d1x, y2 + 62, 60, 27, "未收录或差异", "新增与歧义分流",
                    fill=t["amber_bg"], stroke=t["amber_bdr"], title_color=t["amber"], title_size=5.9)
    s.add_edge([(d1x + 60, y2 + 75.5), (d1x + 70, y2 + 75.5)], stroke=t["amber_bdr"], dashed=True)
    s.add_node("diamond", d1x + 70, y2 + 60.5, 56, 30, fill=t["white"], stroke=t["blue_main"], stroke_w=0.85,
               text="口径冲突?", font_size=5.8, font_color=t["navy"], bold=True, pad_x=0)
    s.add_edge([(d1x + 126, y2 + 75.5), (d1x + 136, y2 + 75.5), (d1x + 136, y2 + 63.5), (d1x + 145, y2 + 63.5)], stroke=t["blue_main"])
    s.add_edge([(d1x + 136, y2 + 75.5), (d1x + 136, y2 + 88), (d1x + 145, y2 + 88)], stroke=t["blue_main"])
    s.add_node("rrect", d1x + 145, y2 + 54.5, 120, 18, fill=t["blue_pale"], stroke=t["blue_line"], stroke_w=0.75, radius=2.8,
               text="无冲突：建基类或 is-a 派生子类", font_size=5.8, font_color=t["navy"], bold=True, single_line_each_para=True)
    s.add_node("rrect", d1x + 145, y2 + 79, 120, 18, fill=t["white"], stroke=t["blue_line"], stroke_w=0.75, radius=2.8,
               text="有冲突：分行业域独立建类隔离", font_size=5.8, font_color=t["navy"], bold=True, single_line_each_para=True)
    s.add_edge([(d1x + 265, y2 + 63.5), (d1x + 281, y2 + 63.5)], stroke=t["blue_main"])
    s.add_edge([(d1x + 265, y2 + 88), (d1x + 281, y2 + 88)], stroke=t["blue_main"])
    s.add_node("can", d1x + 281, y2 + 51, 63, 47, fill=t["white"], stroke=t["blue_main"], stroke_w=0.9,
               text="标准业务\n对象库\n属性 · 关系", font_size=5.6, font_color=t["navy"], bold=True, pad_x=2, pad_y=0)
    # Spec Card 2
    s.add_node("rrect", spec_x, y2 + 5, spec_w, lh - 10, fill=t["white"], stroke=t["blue_line"], stroke_w=0.8, dashed=True, radius=3.5)
    s.add_node("rrect", spec_x + 4, y2 + 8, spec_w - 8, 16, fill=t["blue_mid"], radius=2.5,
               text="五类标准对齐与分类演进", font_size=6.4, font_color=t["white"], bold=True, single_line_each_para=True)
    for idx, st in enumerate(["标准对象", "属性类型", "关联关系"]):
        s.add_node("rrect", spec_x + 5 + idx * 55, y2 + 27, 52, 15, fill=t["panel_bg"], stroke=t["border"], stroke_w=0.65,
                   radius=2.0, text=st, font_size=6.0, font_color=t["navy"], bold=True, single_line_each_para=True)
    s.add_node("rrect", spec_x + 5, y2 + 45, 80, 15, fill=t["panel_bg"], stroke=t["border"], stroke_w=0.65, radius=2.0,
               text="指标口径分域隔离", font_size=5.8, font_color=t["navy"], bold=True, single_line_each_para=True)
    s.add_node("rrect", spec_x + 89, y2 + 45, 79, 15, fill=t["panel_bg"], stroke=t["border"], stroke_w=0.65, radius=2.0,
               text="统一基准单位换算", font_size=5.8, font_color=t["navy"], bold=True, single_line_each_para=True)
    s.add_node("rrect", spec_x + 5, y2 + 64, spec_w - 10, 16, fill=t["blue_pale"], stroke=t["blue_line"], stroke_w=0.65, radius=2.0,
               text="同源 is-a 按域剪枝 · 冲突分域隔离", font_size=5.8, font_color=t["navy"], bold=True, single_line_each_para=True)
    s.add_node("rrect", spec_x + 4, y2 + 83, spec_w - 8, 17, fill=t["blue_soft"], radius=2.5,
               text="产出：标准标识对齐的候选本体 DSL", font_size=5.9, font_color=t["navy"], bold=True, single_line_each_para=True)

    # Swimlane 3: 质量校验技术
    y3 = 373
    add_swimlane_shell(s, sx, y3, sw, lh, "质\n量\n校\n验\n技\n术", dark=True)
    add_labeled_box(s, d1x, y3 + 16, 46, 28, "候选本体\nDSL")
    s.add_edge([(d1x + 46, y3 + 30), (d1x + 55, y3 + 30)], stroke=t["blue_main"])
    add_chip_module(s, d1x + 55, y3 + 8, 118, 44, "一、规则内核静态检查",
                    ["Schema · 引用", "单位换算", "Kahn 拓扑判环", "无接口硬编码"], cols=2, stroke=t["blue_main"])
    s.add_edge([(d1x + 173, y3 + 30), (d1x + 182, y3 + 30)], stroke=t["blue_main"])
    s.add_node("diamond", d1x + 182, y3 + 15, 54, 30, fill=t["white"], stroke=t["blue_main"], stroke_w=0.85,
               text="静态通过?", font_size=5.8, font_color=t["navy"], bold=True, pad_x=0)
    s.add_edge([(d1x + 236, y3 + 30), (d1x + 247, y3 + 30)], stroke=t["blue_main"])
    add_header_strip_module(s, d1x + 247, y3 + 8, 97, 44, "二、完备与还原复核",
                            ["查追踪表 · 条款无漏无增", "还原中文 · 独立模型核原意"])
    s.add_edge([(d1x + 209, y3 + 45), (d1x + 209, y3 + 80), (d1x + 156, y3 + 80)], stroke=t["amber_bdr"], dashed=True)
    add_labeled_box(s, d1x, y3 + 66.5, 156, 27, "按语义项↔AST 映射定位修正", "避免大模型自由改写 · 精准回溯根因",
                    fill=t["amber_bg"], stroke=t["amber_bdr"], title_color=t["amber"], title_size=6.0)
    s.add_edge([(d1x + 295.5, y3 + 52), (d1x + 295.5, y3 + 68)], stroke=t["navy_deep"], stroke_w=1.05)
    s.add_node("stadium", d1x + 247, y3 + 68, 97, 24, fill=t["navy_deep"],
               text="正式规则本体 DSL", font_size=6.7, font_color=t["white"], bold=True, pad_x=2, single_line_each_para=True)
    # Spec Card 3
    s.add_node("rrect", spec_x, y3 + 5, spec_w, lh - 10, fill=t["white"], stroke=t["navy_deep"], stroke_w=0.85, dashed=True, radius=3.5)
    s.add_node("rrect", spec_x + 4, y3 + 8, spec_w - 8, 16, fill=t["navy_deep"], radius=2.5,
               text="校验准出保障与下游使用形态", font_size=6.4, font_color=t["white"], bold=True, single_line_each_para=True)
    for idx, ct in enumerate(["Schema与引用有效", "单位换算·无环", "语义条款无漏无增", "否定与极性一致"]):
        r, c = idx // 2, idx % 2
        s.add_node("rrect", spec_x + 5 + c * 83, y3 + 28 + r * 24, 80, 20, fill=t["panel_bg"], stroke=t["border"],
                   stroke_w=0.7, radius=2.2, text=ct, font_size=5.9, font_color=t["navy"], bold=True, single_line_each_para=True)
    s.add_node("rrect", spec_x + 4, y3 + 81, spec_w - 8, 19, fill=t["blue_soft"], radius=2.5,
               text="供匹配复用计算 · 交运行层编译执行", font_size=6.0, font_color=t["navy_deep"], bold=True, single_line_each_para=True)

    # 5. Bottom Evolution Strip + Right-Edge Feedback Arrow (y=490..519)
    by = 490
    s.add_node("rrect", sx, by, sw, 29, fill=t["panel_bg"], stroke=t["border"], stroke_w=0.85, radius=4.0)
    s.add_node("rrect", sx + 4, by + 4, 92, 21, fill=t["blue_main"], radius=3.0,
               text="标准演进与回归", font_size=6.8, font_color=t["white"], bold=True, single_line_each_para=True)
    ex_cur = sx + 104
    evo_steps = [("验收与评测集归因", 88), ("更新对象与编译规则", 92), ("沿引用图增量定位", 88), ("自动回归重检", 76), ("升版发布", 63)]
    for idx, (st, ew) in enumerate(evo_steps):
        s.add_node("rrect", ex_cur, by + 4.5, ew, 20, fill=t["white"], stroke=t["border"], stroke_w=0.75, radius=3.0,
                   text=st, font_size=6.0, font_color=t["navy"], bold=True, single_line_each_para=True)
        if idx < len(evo_steps) - 1:
            s.add_edge([(ex_cur + ew, by + 14.5), (ex_cur + ew + 8, by + 14.5)], stroke=t["blue_line"])
        ex_cur += ew + 8
    s.add_edge([(sx + sw, by + 14.5), (rx + rw - 2.5, by + 14.5), (rx + rw - 2.5, y2 + 54), (sx + sw, y2 + 54)],
               stroke=t["blue_main"], stroke_w=1.0)

    return s


if __name__ == "__main__":
    chosen = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_THEME_NAME
    scene = build_full_arch_slide(theme_name=chosen)
    run_self_check(scene, mode="tech-arch", extra_banned_words=("URI",))
    with tempfile.TemporaryDirectory() as td:
        pptx_p = os.path.join(td, f"arch_{chosen}.pptx")
        export_pptx(scene, pptx_p)
        outs = render_quicklook_and_crop(pptx_p, td, crops={"lanes": (0.38, 0.21, 0.99, 0.91)})
        print(f"Verified theme={chosen} PPTX:", os.path.getsize(pptx_p), "bytes; PNGs:", {k: os.path.getsize(v) for k, v in outs.items()})
