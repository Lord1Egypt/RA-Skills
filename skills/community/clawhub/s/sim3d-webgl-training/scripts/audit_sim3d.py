#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
audit_sim3d.py — 3D虚拟仿真实训单文件HTML静态审核脚本
用法: python audit_sim3d.py <成品.html> [--report 审核报告.md]
评分: P0项一票否决；满分100，三档判定：≥85 优（可直接交付）/ 80-84 良（补齐失败P1后交付）/ <80 不可交付
校准基准：9 个已验证样本（WebGL 系 + Canvas2D 软渲染系均应 ≥85；
引用 three.js CDN 的旧版大疆无人机属反面教材，应不通过）
"""
import sys
import re
import argparse
from pathlib import Path


def audit(path: str):
    html = Path(path).read_text(encoding="utf-8", errors="ignore")
    lines = html.splitlines()
    n_lines = len(lines)
    low = html.lower()
    checks = []  # (level, name, passed, detail, weight)

    def add(level, name, passed, detail="", weight=5):
        checks.append((level, name, passed, detail, weight))

    # ---------- 渲染架构识别 ----------
    has_webgl = bool(re.search(r'getContext\s*\(\s*["\']webgl2?["\']', html)) or ("WebGLRenderer" in html)
    # Canvas2D 软渲染系：project3D + 三角形深度排序
    has_sw_raster = ("project3D" in html or "projectPoint" in html) and \
                    re.search(r'sort\s*\(\s*\(\s*\w\s*,\s*\w\s*\)\s*=>\s*\w\.depth\s*-', html) is not None
    has_canvas3d = has_webgl or has_sw_raster

    # ---------- P0 一票否决 ----------
    tail = html.rstrip()[-80:]
    add("P0", "HTML完整闭合(</html>)", tail.endswith("</html>"),
        "文件末尾必须是 </body></html>，截断会导致静默失败" if not tail.endswith("</html>") else "")

    add("P0", "<script>标签闭合", html.count("<script") == html.count("</script>"),
        f"script标签数不匹配: {html.count('<script')}/{html.count('</script>')}"
        if html.count("<script") != html.count("</script>") else "")

    # 外链仅指 <script src> / <link href>（<a href> 政策原文链接不阻断渲染）
    ext_scripts = re.findall(r'<script[^>]+src\s*=\s*["\'](?!data:)[^"\']+["\']', html)
    ext_links = re.findall(r'<link[^>]+href\s*=\s*["\'](?!data:)[^"\']+["\']', html)
    add("P0", "零外部CDN依赖(离线可用)", len(ext_scripts) + len(ext_links) == 0,
        f"发现外链脚本/样式 {len(ext_scripts) + len(ext_links)} 处（three.js/tailwind/fonts 等会断网白屏）——严禁！"
        if ext_scripts or ext_links else "全程序化自包含")

    add("P0", "3D引擎(WebGL或Canvas2D软渲染)", has_canvas3d,
        "必须含 getContext('webgl2'|'webgl') 或 project3D+深度排序软渲染管线"
        if not has_canvas3d else ("WebGL 硬件渲染" if has_webgl else "Canvas2D 软件光栅化"))

    has_shaders = has_webgl and (("VERTEX_SHADER" in html or "PBR_VS" in html or "VS_SRC" in html or
                                  "#version 300 es" in html or "gl_Position" in html or "attribute vec" in html))
    add("P0" if has_webgl else "P2", "顶点/片元着色器定义", has_shaders,
        "WebGL 项目必须有着色器源码" if (has_webgl and not has_shaders) else "",
        5)

    add("P0", "requestAnimationFrame主循环", "requestAnimationFrame" in html, "", 5)

    add("P0", "中文界面(≥150汉字)", len(re.findall(r'[\u4e00-\u9fff]', html)) >= 150, "", 5)

    # ---------- P1 结构必需 ----------
    # 双画布或等价 overlay 机制
    has_overlay = ("hud-canvas" in html) or ("overlay-canvas" in html) or \
                  ("overlay" in low) or ("hotspot-layer" in html) or (html.count("<canvas") >= 2) or \
                  ("spatial-label" in html)
    add("P1", "3D视图+2D叠加层分离", has_overlay, "建议双画布或 DOM/Canvas overlay 层承载数据标注", 4)

    # 交互：拖拽/缩放
    has_orbit = ("mousedown" in html or "pointerdown" in html) and ("wheel" in html or "deltaY" in html)
    add("P1", "轨道相机交互(拖拽+滚轮缩放)", has_orbit, "", 5)

    # 点选联动（宽松匹配各项目命名风格）
    has_select = bool(re.search(r'function\s+select\w*\(', html)) or \
                 bool(re.search(r'selected(?:Part|Hotspot|Comp|Module|Entity)', html)) or \
                 ("hotspotDomMap" in html) or ("activeJobId" in html)
    add("P1", "点选部件→详情联动", has_select, "必须有点选部件/工位弹出工程详情的联动", 5)

    # 部件数据库
    has_db = bool(re.search(r'(?:COMPONENTS|SIM_CONFIG|HOTSPOTS_DATA|TRAINING_MODULES|PARTS|POSTS|SCENE_POSTS|ENTITIES|POST_DATA|CASES|BAGS|PASSENGERS|SOP_STEPS|KNOWLEDGE|TASKS|PARTS_DB|STEPS)\w*\s*[:=]\s*[\[{]', html))
    add("P1", "结构化部件/工位数据库", has_db, "需要 COMPONENTS[]/HOTSPOTS_DATA/SOP_STEPS 等结构化数据驱动", 5)

    # 相机预设或镜头聚焦
    has_cam_preset = ("setCameraPreset" in html) or ("animateCameraTo" in html) or ("flyCamera" in html) or \
                     ("resetCameraView" in html) or ("data-cam" in html) or ("goalYaw" in html) or \
                     ("focusPos" in html) or ("focusTarget" in html) or ("camGoal" in html) or \
                     ("cameraPreset" in html)
    add("P1", "相机预设位/镜头聚焦", has_cam_preset, "部件聚焦或视角预设至少其一", 3)

    # 教学闭环：任一形态
    teach_signals = sum(1 for kw in ["sop", "工卡", "步骤", "知识卡", "kpi", "考核", "教学", "实训", "模块", "步骤卡"]
                        if kw in low or kw in html)
    add("P1", "教学闭环要素(SOP/KPI/知识卡/模块)", teach_signals >= 3, f"检测到 {teach_signals}/10 类教学要素", 5)

    # 防呆：h 遮蔽热点循环（真实 bug 模式）
    h_loop = re.findall(r'for\s*\(\s*(?:const|let)\s+h\s+of|\.forEach\(\s*h\s*[,)]', html)
    add("P1", "无 h 变量热点循环遮蔽", len(h_loop) == 0,
        "发现 for(const h of ...) / forEach(h) 模式——热点循环变量必须改名 item/hs，防止与视口高度 h 遮蔽"
        if h_loop else "", 4)

    # 深度/遮挡处理（WebGL: depthMask 双通道；Canvas2D: painter 排序）
    depth_ok = (html.count("depthMask") >= 2) or has_sw_raster or ("DEPTH_TEST" in html and "depth" in low)
    add("P1", "遮挡处理(depthMask双通道或深度排序)", depth_ok,
        "半透明件需 depthMask 切换；软渲染需 back-to-front 排序" if not depth_ok else "", 4)

    # 法线处理（WebGL 系）
    if has_webgl:
        normal_ok = ("normalize(vNormal)" in html) or ("normalize(mat3(" in html) or \
                    ("normalize(uModel[0].xyz)" in html) or ("N = -N" in html) or ("N = -N;" in html)
        add("P1", "法线归一化(防非均匀缩放畸变)", normal_ok,
            "需 normalize(vNormal) 或顶点着色器法线矩阵重归一化写法" if not normal_ok else "", 4)

    # ---------- P1 教学闭环深化（按类型条件判定）----------
    is_sop_type = ("checkFn" in html) or ("工卡" in html) or bool(re.search(r'steps\s*:\s*\[', html)) or \
                  bool(re.search(r'SOP_STEPS|sopSteps|sop', low))
    is_exam_capable = ("deduct" in low) or ("score" in low and ("考核" in html or "评分" in html or "扣" in html or "PTS" in html))
    is_principle_type = ("kpi" in low) or bool(re.search(r'pv-canvas|chart-canvas|wave-canvas|示功|波形', html))

    if is_sop_type:
        add("P1", "SOP步骤完成判据(checkFn)", "checkFn" in html or "completedSteps" in html or
            re.search(r'completed\w*\[', html) is not None or "triggerSopStep" in html or
            ("step" in low and ("done" in low or "完成" in html)), "SOP 步骤卡需完成判据实时校验", 4)
    if is_exam_capable or ("考核" in html):
        has_score_ui = re.search(r'score|得分|PTS', low) and ("deduct" in low or "扣分" in html or "违规" in html
                                                              or "taskPts" in html or "quizPts" in html
                                                              or "quiz" in low)
        add("P1", "考核评分联动", has_score_ui, "考核型系统需要 score + 扣分/答题分机制", 4)

    # ---------- 内容密度块（仅对 SIM_CONFIG 数据驱动架构生效，旧样本不受影响）----------
    # 新架构自声明：采用 SIM_CONFIG 单源数据 → 强制领域内容密度基线（SKILL.md 品质红线）
    is_config_driven = "SIM_CONFIG" in html
    if is_config_driven:
        has_testpoints = (("vNorm" in html and "vFault" in html) or
                          ("ohmNorm" in html and "ohmFault" in html) or
                          ("mohmNorm" in html and "mohmFault" in html))
        add("P1", "可测数值体系(testPoints正常/故障双值)", has_testpoints,
            "SIM_CONFIG.components 每项需 testPoints 8 值（契约见 domain-data.md §1）", 4)

        dmm_btns = len(re.findall(r'data-dmm\s*=', html)) + len(re.findall(r'dmm-mode-btn', html))
        add("P1", "虚拟万用表≥3档位(V/Ω/MΩ/A)", dmm_btns >= 3,
            f"检测到 {dmm_btns} 个档位按钮；需 ≥3（含表笔选择 sel-probe）", 3)

        has_quiz = (("quizQuestion" in html and "answerIdx" in html) or
                    ("options" in html and "answerIdx" in html))
        add("P1", "故障盲考选择题库", has_quiz,
            "每个故障需 quizQuestion + options + answerIdx（症状→测量→决策闭环）", 3)

        tele_count = len(re.findall(r'id="tele-', html))
        add("P1", "底部遥测条(≥3项实时指标)", tele_count >= 3,
            f"检测到 {tele_count} 项 tele- 指标；需 ≥3（坐标/电流/电压/误差…）", 3)

        comp_count = len(re.findall(r'code\s*:', html))
        add("P1", "部件总数≥8", comp_count >= 8, f"检测到 {comp_count} 个部件 code", 3)

        has_std = bool(re.search(r'GB[/T]?\s*\d|ISO\s*\d|IEC\s*\d', html))
        add("P2", "标准引用(GB/ISO/IEC真实标准号)", has_std, "标题徽章或 SOP 引用 ≥1 个真实标准", 2)

        specs_blocks = len(re.findall(r'specs\s*:\s*\[', html))
        add("P2", "部件规格表(specs≥4行/件)", specs_blocks >= 1,
            f"检测到 {specs_blocks} 个 specs 块；每件需 ≥4 行真实工程数值", 2)

        cond_signals = len(re.findall(r'data-wcond|workCond\s*===', html))
        add("P2", "工况模式(≥2种可切换)", cond_signals >= 2,
            f"检测到 {cond_signals} 处工况切换；需 ≥2 种典型工况", 2)

        has_jog = ("jog-slider" in html) or ("data-jidx" in html) or ("示教" in html and "slider" in low)
        add("P2", "示教点动/关节控制台", has_jog, "机械臂类需 J1~J6 滑块（真实行程限位）", 2)

    # ---------- P2 质感 ----------
    has_pbr = ("uMetallic" in html or "metallic" in low or "specPower" in html or "Phong" in html or
               ("spec" in low and "light" in low))
    add("P2", "PBR/高光材质工作流", has_pbr, "", 3)

    cad_pats = ["addTubeSection", "addHelicalSpring", "addExtrudedPolygon", "buildTubeMesh",
                "buildSphereMesh", "MeshBuilder", "buildCylinderMesh", "buildChamferBox", "addCylinder",
                "addCylinderY", "addCylinderZ", "addCylinderX", "buildLoftedShell",
                "addSphere", "addWheel", "addTri", "addQuad", "CylinderGeometry", "SphereGeometry",
                "ConeGeometry", "TorusGeometry", "createBeveledBoxMesh", "createCylinderMesh",
                "createSphereMesh", "addBox", "addQuadFlat", "buildFace", "pushQuad", "pushTri",
                "makeBox", "makeCylinder", "addPrism", "faces.push", "emitFace", "addPolygon"]
    cad_types = sum(1 for pat in cad_pats if pat in html)
    add("P2", "程序化CAD曲面生成(≥3类)", cad_types >= 3, f"检测到 {cad_types}/35 类曲面生成器", 4)

    has_particles = ("POINTS" in html) or ("particle" in low) or ("pushMeshToQueue" in html) or \
                    ("ShadowDisk" in html) or ("drawGlow" in html)
    add("P2", "粒子/光效/动态元素", has_particles, "", 2)

    has_2danno = ("moveTo" in html and "lineTo" in html and ("fillText" in html or "hotspot" in low
                                                               or "spatial-label" in html or "updateSpatialLabels" in html))
    if not has_2danno:
        # DOM 热点 Pin 方案（A320 式：DOM 元素随 3D 投影定位）
        has_2danno = "hotspot-pin" in html or ("hotspotDomMap" in html) or ("hotspot-layer" in html)
    add("P2", "2D引线标注/热点Pin", has_2danno, "", 3)

    has_explode = ("explode" in low) and re.search(r'explode\w*\s*\*', low) is not None
    add("P2", "爆炸视图/剖切模式", has_explode or "cutaway" in low or "剖面" in html or "剖切" in html
        or "xray" in low or "半剖" in html or "透视模式" in html,
        "结构认知需爆炸/剖切/X光透视其一", 2)

    has_inst = any(kw in html or kw in low for kw in
                   ["万用表", "multimeter", "示波器", "scope", "obd", "仪表", "x光", "xray", "判图", "验电"])
    add("P2", "虚拟仪器(表/镜/终端)", has_inst, "实操型建议配置虚拟仪表", 2)

    has_audio = "AudioContext" in html or "audioCtx" in html
    add("P2", "Web Audio音效", has_audio, "", 1)

    has_person = any(kw in html for kw in ["技师", "乘务员", "安检员", "人物", "Technician", "avatar"])
    add("P2", "3D人物角色", has_person, "", 2)

    add("P2", "代码量级(≥1500行)", n_lines >= 1500, f"当前 {n_lines} 行；对标样本 2500-3900 行", 3)

    # ---------- 评分 ----------
    total_weight = 0
    earned = 0
    p0_failed = []
    for level, name, passed, detail, weight in checks:
        if level == "P0":
            if not passed:
                p0_failed.append(name)
        else:
            total_weight += weight
            if passed:
                earned += weight

    score = round(earned / total_weight * 100) if total_weight else 0
    if p0_failed:
        score = min(score, 45)

    if 85 <= score <= 100:
        grade = "可交付"
    elif 80 <= score < 85:
        grade = "良（需补齐失败P1后交付）"
    else:
        grade = "不可交付"

    return {
        "file": path,
        "lines": n_lines,
        "score": score,
        "grade": grade,
        "arch": "WebGL" if has_webgl else ("Canvas2D软渲染" if has_sw_raster else "未知"),
        "p0_failed": p0_failed,
        "checks": checks,
        "passed": (score >= 80) and (len(p0_failed) == 0),
    }


def render_report(r) -> str:
    out = []
    out.append("# 3D虚拟仿真实训系统审核报告\n")
    out.append(f"- **文件**: `{r['file']}`")
    out.append(f"- **渲染架构**: {r['arch']}")
    out.append(f"- **代码行数**: {r['lines']}")
    out.append(f"- **得分**: **{r['score']} / 100**")
    if r["passed"] and r["score"] >= 85:
        verdict = "✅ **通过（优）**（≥85 且无P0失败，可直接交付）"
    elif r["passed"]:
        verdict = "🟡 **通过（良）**（80-84 分，补齐失败P1项后交付）"
    else:
        verdict = "❌ **未通过**（<80 分或存在P0失败，不可交付）"
    out.append(f"- **结论**: {verdict}\n")

    if r["p0_failed"]:
        out.append("## ⛔ P0 一票否决项失败\n")
        for name in r["p0_failed"]:
            out.append(f"- {name}")
        out.append("")

    out.append("## 检查明细\n")
    out.append("| 级别 | 检查项 | 结果 | 权重 | 说明 |")
    out.append("|---|---|---|---|---|")
    for level, name, passed, detail, weight in r["checks"]:
        mark = "✅" if passed else "❌"
        out.append(f"| {level} | {name} | {mark} | {weight} | {detail} |")

    failed = [(lv, nm, dt) for lv, nm, ps, dt, _ in r["checks"] if not ps]
    if failed:
        out.append("\n## 修复优先级建议\n")
        for prio, title in [("P1", "P1 结构必需（优先修复）"), ("P2", "P2 质感提升")]:
            items = [f for f in failed if f[0] == prio]
            if items:
                out.append(f"### {title}\n")
                for lv, nm, dt in items:
                    out.append(f"- **{nm}** {dt}")
                out.append("")

    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description="3D虚拟仿真实训HTML静态审核")
    ap.add_argument("html", help="待审核的 HTML 文件路径")
    ap.add_argument("--report", help="输出 Markdown 报告路径（可选）")
    args = ap.parse_args()

    r = audit(args.html)
    report = render_report(r)
    print(report)
    if args.report:
        Path(args.report).write_text(report, encoding="utf-8")
        print(f"\n报告已写入: {args.report}")
    sys.exit(0 if r["passed"] else 1)


if __name__ == "__main__":
    main()
