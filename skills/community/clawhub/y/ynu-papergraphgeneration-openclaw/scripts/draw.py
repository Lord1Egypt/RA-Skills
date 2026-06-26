"""
paper-diagram-skill / draw.py
=============================
重构后的标准化流程：

  Step 1  扫描  ── 读取论文文本，识别可视化部分
  Step 2  排序  ── 以表格形式展示，按优先级排列
  Step 3  选图  ── 用户选择要生成的图片
  Step 4  生成  ── 逐一生成图片
  Step 5  校验  ── 检查图片结构是否与原文逻辑冲突
  Step 6  重生  ── 有偏差则询问是否调整描述词重生成
"""

import os, json, sys, argparse, textwrap
from pathlib import Path

# ── 内置模块 ──────────────────────────────────────────────
from pdf_to_text import extract_text
from image_generator import generate_image, build_academic_prompt
from self_checker import check_figure_logical_consistency

_SCRIPT_DIR = Path(__file__).parent.resolve()
_SKILL_DIR  = _SCRIPT_DIR.parent
sys.path.insert(0, str(_SCRIPT_DIR))

# ─────────────────────────────────────────────────────────
# Step 1：扫描论文，识别可可视化部分
# ─────────────────────────────────────────────────────────
def scan_paper(raw_text: str) -> list[dict]:
    """
    分析论文文本，识别所有可生成 figure 的章节，
    返回结构化列表。
    每个条目：
      {
        "id":        int,          # 序号
        "priority":  str,          # High / Medium / Low
        "type":      str,          # 图类型
        "title":     str,          # 中英双语标题
        "source":    str,          # 原文出处（图号/章节号）
        "description": str,        # 中文描述（供 LLM 生图用）
        "topology":  str,          # topology 字符串（供 build_academic_prompt 用）
        "user_req":  str,          # user_requirement 字符串
      }
    """
    items = []

    # ── 启发式关键词扫描 ────────────────────────────────
    lines = raw_text.split("\n")
    full_lower = raw_text.lower()

    def add(id_, priority, fig_type, title_cn, title_en, source, desc_cn, topology, user_req=""):
        items.append({
            "id": id_,
            "priority": priority,
            "type": fig_type,
            "title_cn": title_cn,
            "title_en": title_en,
            "source": source,
            "description": desc_cn,
            "topology": topology,
            "user_req": user_req,
        })

    # ── 通用段落匹配 ────────────────────────────────
    # 如果论文内已有 figure 引用，优先提取
    fig_patterns = [
        (r"图\s*1[:：]?\s*(.{10,80})", "图1"),
        (r"Figure\s*1[:.]?\s*(.{10,80})", "Figure 1"),
        (r"图\s*2[:：]?\s*(.{10,80})", "图2"),
        (r"Figure\s*2[:.]?\s*(.{10,80})", "Figure 2"),
    ]

    found_figures = []
    for pat, label in fig_patterns:
        import re
        for m in re.finditer(pat, raw_text):
            found_figures.append((label, m.group(0)[:120]))

    # ── 根据论文内容，手动构建优先级列表 ─────────────
    # 这里用关键词匹配来自动判断哪些章节有可视化价值

    # 1. 架构总览图（最高优先）
    if any(k in full_lower for k in ["架构", "architecture", "framework", "overview"]):
        add(1, "High", "架构图",
            "模型架构总览",
            "Architecture Overview",
            "Section 3 / 图4",
            "展示整个模型的完整架构流程，从输入到输出，包含所有主要模块和连接关系",
            "Clean academic architecture diagram, left-to-right hierarchical layout showing all modules and connections")

    # 2. 损失函数 / 训练流程
    if any(k in full_lower for k in ["损失", "loss", "loss function", "objective"]):
        add(2, "High", "公式/流程图",
            "训练目标与损失函数",
            "Training Objective & Loss",
            "Section 3.1-3.3 / 公式1-2",
            "展示模型的损失函数构成，包括对比损失、自监督损失等的组合方式",
            "Academic diagram showing mathematical formulation, loss components and their combination")

    # 3. 数据效率对比
    if any(k in full_lower for k in ["数据高效", "data efficient", "zero-shot", "数据效率"]):
        add(3, "High", "对比折线图",
            "数据效率对比（DeCLIP vs CLIP）",
            "Data Efficiency Comparison",
            "图1 / Section 4.3",
            "X轴为训练数据量（12M/29M/56M/88M），Y轴为ImageNet零样本Top-1精度，绘制DeCLIP和CLIP两条对比曲线，标注关键节点数据",
            "Line chart, grid background, two curves (CLIP vs DeCLIP), annotated data points, clean academic style")

    # 4. 三种监督信号详解
    if any(k in full_lower for k in ["自监督", "多视角", "最近邻", "self-supervision", "multi-view", "nearest neighbor"]):
        add(4, "High", "多面板图",
            "三种监督信号详解",
            "Three Supervision Signals",
            "图4(b) / Section 3.3",
            "三栏并排布局：(a)自监督 (b)多视角监督 (c)最近邻监督，每栏有独立标题和颜色区分",
            "Three-panel figure, distinct background colors per panel, labeled subcomponents, clean academic style")

    # 5. 下游任务迁移效果
    if any(k in full_lower for k in ["下游", "迁移", "transfer", "linear probe", "下游任务"]):
        add(5, "High", "对比柱状图",
            "下游任务迁移效果对比",
            "Downstream Task Transfer",
            "表3 / Section 4.3",
            "11个下游数据集的线性探针精度对比柱状图，DeCLIP vs CLIP，标注胜出数据集",
            "Grouped bar chart, 11 datasets, CLIP vs DeCLIP bars, clean academic style")

    # 6. 最近邻检索示例
    if any(k in full_lower for k in ["最近邻", "nearest neighbor", "nn", "neighbor"]):
        add(6, "Medium", "示例图",
            "最近邻文本检索示例",
            "Nearest Neighbor Retrieval Examples",
            "图3 / Section 3.3",
            "展示原始图像-文本对与检索到的最近邻对的对比，标注语义相似性",
            "Side-by-side image-text pairs showing original and retrieved nearest neighbors, clean academic style")

    # 7. 消融实验
    if any(k in full_lower for k in ["消融", "ablation", "ablation study"]):
        add(7, "Medium", "消融图/表格",
            "各监督信号消融实验",
            "Ablation Study",
            "表4 / Section 4.4",
            "展示SS、MVS、NNS各监督信号的消融结果，标注每项的贡献度",
            "Table or grouped bar chart, showing ablation results for SS/MVS/NNS components")

    # 8. 零样本学习曲线
    if any(k in full_lower for k in ["zero-shot", "零样本"]):
        add(8, "Medium", "折线图",
            "ImageNet零样本学习曲线",
            "Zero-Shot Learning Curve on ImageNet",
            "图1 / Section 4.3",
            "展示随训练数据量增加，零样本精度变化的曲线，标注关键转折点",
            "Line chart showing zero-shot accuracy vs data size, annotated key points")

    # 9. CAM 可视化
    if any(k in full_lower for k in ["cam", "class activation", "激活图", "可视化"]):
        add(9, "Medium", "热力图",
            "类激活图（CAM）可视化",
            "Class Activation Map (CAM) Visualization",
            "图8 / Section 4.5",
            "CLIP vs DeCLIP 的 CAM 对比，展示模型关注区域的差异",
            "CAM heatmap comparison, CLIP vs DeCLIP side by side, clean academic style")

    # 10. 数据集样本
    if any(k in full_lower for k in ["数据集", "dataset", "sample", "样本"]):
        add(10, "Low", "样本展示",
            "预训练数据集样本",
            "Pretraining Dataset Samples",
            "Section 4.1 / 图3",
            "展示预训练数据集中选取的图像-文本对样本",
            "Grid of image-text pairs from pretraining dataset, clean academic style")

    # 11. CLIP baseline 回顾
    if any(k in full_lower for k in ["clip", "align", "对比学习"]):
        add(11, "Low", "架构图",
            "CLIP/ALIGN 基线方法回顾",
            "CLIP/ALIGN Baseline Overview",
            "图4(a) / Section 3.1",
            "展示原始 CLIP 的双塔架构（图像编码器 + 文本编码器 + 对比损失）",
            "Clean architecture diagram of CLIP baseline, dual-tower structure, minimal academic style")

    # 12. 模型扩展性
    if any(k in full_lower for k in ["扩展", "scale", "scaling", "regnet", "vit"]):
        add(12, "Low", "扩展曲线图",
            "模型规模扩展性分析",
            "Model Scaling Analysis",
            "Section 4.3 / 表2",
            "展示不同模型规模（ResNet50/ViT-B32/RegNetY-64GF）的零样本性能对比",
            "Bar chart or line chart showing scaling trends across different model architectures")

    # 按优先级排序：High > Medium > Low，同级别按 id 排序
    prio_order = {"High": 0, "Medium": 1, "Low": 2}
    items.sort(key=lambda x: (prio_order[x["priority"]], x["id"]))

    # 重新编号
    for i, item in enumerate(items, 1):
        item["id"] = i

    return items


# ─────────────────────────────────────────────────────────
# Step 2：格式化表格输出
# ─────────────────────────────────────────────────────────
def print_visualization_table(items: list[dict]):
    """打印带优先级的可视化清单表格"""
    header = f"{'#':<3} {'优先级':<8} {'类型':<10} {'标题':<20} {'来源':<15}"
    sep    = "─" * 60
    print("\n" + "═" * 70)
    print("  📊 论文可视化扫描结果")
    print("═" * 70)
    print(header)
    print(sep)

    prio_emoji = {"High": "🔴", "Medium": "🟡", "Low": "⚪"}
    type_emoji = {
        "架构图": "🏗", "对比折线图": "📈", "多面板图": "🗂",
        "对比柱状图": "📊", "公式/流程图": "🔢", "示例图": "🖼",
        "消融图/表格": "🔬", "折线图": "📈", "热力图": "🔥",
        "样本展示": "📦", "扩展曲线图": "📐",
    }

    for item in items:
        emoji_p = prio_emoji.get(item["priority"], "⚪")
        emoji_t = type_emoji.get(item["type"], "•")
        title   = (item["title_cn"] + " / " + item["title_en"])[:28]
        print(
            f"{emoji_p} {item['id']:<2} {item['priority']:<8} "
            f"{emoji_t}{item['type']:<9} {title:<30} {item['source']:<15}"
        )

    print(sep)
    print(f"共识别 {len(items)} 个可可视化部分\n")


def ask_user_selection(items: list[dict]) -> list[int]:
    """询问用户选择要生成哪些图片，返回 id 列表"""
    print("请输入要生成的图片编号（支持：1 或 1,3,5 或 1-5 或 all）：")
    choice = input("> ").strip().lower()

    if choice in ("all", "全部", ""):
        return [item["id"] for item in items]

    ids = set()
    parts = choice.replace("，", ",").split(",")
    for part in parts:
        part = part.strip()
        if "-" in part:
            start, end = part.split("-", 1)
            ids.update(range(int(start), int(end) + 1))
        elif part.isdigit():
            ids.add(int(part))

    return sorted(ids)


# ─────────────────────────────────────────────────────────
# Step 5：校验图片逻辑一致性
# ─────────────────────────────────────────────────────────
def verify_figure(item: dict, generated_path: str) -> tuple[bool, str]:
    """
    调用 self_checker 检查图片逻辑一致性。
    返回 (passed, message)。
    """
    try:
        result = check_figure_logical_consistency(
            figure_path=generated_path,
            paper_text="",  # 可传原文用于更深层比对
            figure_type=item["type"],
        )
        passed = result.get("passed", True)
        issues = result.get("issues", [])
        msg = "\n".join(issues) if issues else "未发现明显偏差 ✓"
        return passed, msg
    except Exception as e:
        return False, f"校验过程出错：{e}"


def ask_regenerate(item: dict, issue_msg: str) -> bool:
    """询问用户是否要调整描述重新生成"""
    print("\n" + "!" * 60)
    print(f"  ⚠️  发现潜在偏差（图片 #{item['id']}：{item['title_cn']}）")
    print("!" * 60)
    print(f"  问题描述：{issue_msg}")
    print()
    print("  是否重新生成？（输入 y 重新生成，输入 n 保留当前版本）")
    choice = input("> ").strip().lower()
    return choice in ("y", "yes", "是", "重新生成", "1", "ok")


# ─────────────────────────────────────────────────────────
# Step 4：生成单张图片（带重生成循环）
# ─────────────────────────────────────────────────────────
def generate_single_figure(
    item: dict,
    api_url: str,
    api_key: str,
    model: str,
    output_dir: str,
    timeout: int = 300,
    auto_retry: bool = False,
) -> tuple[bool, str]:
    """
    生成单张图片，包含：
      - build_academic_prompt（基于拓扑+描述）
      - generate_image
      - verify_figure
      - ask_regenerate（循环直到用户满意或跳过）
    """

    print(f"\n{'─'*60}")
    print(f"  🔄 生成 #{item['id']}：{item['title_cn']} / {item['title_en']}")
    print(f"  来源：{item['source']}")
    print(f"{'─'*60}")

    # 构造 prompt
    prompt_dict = build_academic_prompt(
        topology=item.get("topology", ""),
        figure_type=item["type"],
        user_requirement=item.get("user_req", ""),
        style_name="cvpr",
    )

    filename = f"fig_{item['id']:02d}_{item['title_en'].replace(' ','_').replace('/','_')[:20]}.png"
    output_path = os.path.join(output_dir, filename)

    attempt = 0
    while True:
        attempt += 1
        print(f"\n  [{attempt}] 调用生图 API...")

        success, path, err = generate_image(
            prompt_dict=prompt_dict,
            api_url=api_url,
            api_key=api_key,
            model=model,
            output_filename=filename,
            output_dir=output_dir,
            timeout=timeout,
        )

        if not success:
            print(f"\n  ❌ 生成失败：{err}")
            if auto_retry:
                print("  [auto] 重试...")
                continue
            print("  是否重试？（输入 y 重试，输入 n 跳过）")
            if input("> ").strip().lower() not in ("y", "yes", "是", "1"):
                return False, ""
            continue

        print(f"\n  ✅ 生成完成：{path}")

        # Step 5：校验
        passed, issue_msg = verify_figure(item, path)
        print(f"\n  🔍 逻辑校验结果：{'通过 ✓' if passed else '有偏差 ⚠️'}")
        if not passed:
            print(f"     {issue_msg}")

        if not passed:
            if auto_retry or ask_regenerate(item, issue_msg):
                if auto_retry:
                    print("\n  [auto] 重新生成...")
                else:
                    print("\n  请描述你希望如何调整（直接回车使用默认调整）：")
                    adjustment = input("> ").strip()
                if adjustment:
                    # 将用户调整追加到 topology
                    item["topology"] = item["topology"] + "\n用户补充要求: " + adjustment
                    prompt_dict = build_academic_prompt(
                        topology=item.get("topology", ""),
                        figure_type=item["type"],
                        user_requirement=item.get("user_req", ""),
                        style_name="cvpr",
                    )
                continue  # 重新生成
            else:
                print("  保留当前版本，继续下一张。")
                return True, path
        else:
            print("  图片通过校验，无需调整。")
            return True, path


# ─────────────────────────────────────────────────────────
# 主入口（execute，供 OpenClaw 调用）
# ─────────────────────────────────────────────────────────
def execute(args: dict, context: dict = None) -> dict:
    """
    OpenClaw skill 主入口。
    args 包含：
      input       : str，论文文本或文件路径（.txt / .pdf）
      api_url     : str（可选，默认 acedata）
      api_key     : str（可选，从环境变量读取）
      model       : str（可选）
      output_dir  : str（可选）
      auto_select : bool，是否自动选择全部（跳过交互，默认 False）
    """
    # 1. 读取输入
    raw_input = args.get("input", "")
    if not raw_input:
        return {"success": False, "error": "缺少 input 参数，请提供论文文本或文件路径"}

    # 支持文件路径
    if os.path.isfile(raw_input):
        ext = Path(raw_input).suffix.lower()
        if ext == ".pdf":
            raw_text = extract_text_from_pdf(raw_input)
        else:
            with open(raw_input, encoding="utf-8") as f:
                raw_text = f.read()
    else:
        raw_text = raw_input

    if len(raw_text) < 200:
        return {"success": False, "error": f"输入内容太短（{len(raw_text)} 字符），请确认论文内容正确"}

    # 2. 扫描论文
    print(f"\n📖 正在扫描论文（{len(raw_text)} 字）...")
    items = scan_paper(raw_text)
    if not items:
        return {"success": False, "error": "未能从论文中识别到可可视化的内容"}

    # 3. 打印表格
    print_visualization_table(items)

    # 4. 读取配置
    api_url    = args.get("api_url",    os.environ.get("BANANA2_API_URL",    "https://api.acedata.cloud/nano-banana/images"))
    api_key    = args.get("api_key",    os.environ.get("BANANA2_API_KEY",    os.environ.get("ACEDATA_API_KEY", "")))
    model      = args.get("model",      "nano-banana-2")
    output_dir = args.get("output_dir", str(_SCRIPT_DIR / "outputs"))
    auto_select= args.get("auto_select", False)

    if not api_key:
        return {"success": False, "error": "未设置 API Key，请通过参数 api_key 或环境变量 BANANA2_API_KEY 提供"}

    os.makedirs(output_dir, exist_ok=True)

    # 5. 交互选择（auto_select=True 时跳过）
    if auto_select:
        selected_ids = [item["id"] for item in items]
    else:
        print("─" * 60)
        selected_ids = ask_user_selection(items)
        if not selected_ids:
            print("未选择任何图片，退出。")
            return {"success": True, "generated": [], "skipped": []}

    selected_items = [item for item in items if item["id"] in selected_ids]

    # 6. 逐一生成
    print(f"\n🎯 开始生成 {len(selected_items)} 张图片...\n")
    results = []
    for item in selected_items:
        success, path = generate_single_figure(item, api_url, api_key, model, output_dir)
        results.append({
            "id": item["id"],
            "title": item["title_cn"],
            "success": success,
            "path": path,
        })

    # 7. 汇总报告
    print("\n" + "═" * 60)
    print("  📦 生成报告")
    print("═" * 60)
    for r in results:
        icon = "✅" if r["success"] else "❌"
        print(f"  {icon} #{r['id']:2d}  {r['title']:<25}  {r['path']}")
    print("═" * 60)

    return {
        "success": True,
        "generated": [r for r in results if r["success"]],
        "failed":   [r for r in results if not r["success"]],
    }


# ─────────────────────────────────────────────────────────
# CLI 入口（供 draw.py --scan 使用）
# ─────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="DeCLIP Paper Diagram Generator (New Workflow)")
    parser.add_argument("--input", "-i", required=True, help="论文文本或文件路径")
    parser.add_argument("--api-url",   default=os.environ.get("BANANA2_API_URL",    "https://api.acedata.cloud/nano-banana/images"))
    parser.add_argument("--api-key",   default=os.environ.get("BANANA2_API_KEY",    os.environ.get("ACEDATA_API_KEY", "")))
    parser.add_argument("--model",     default="nano-banana-2")
    parser.add_argument("--output-dir",default=str(_SCRIPT_DIR / "outputs"))
    parser.add_argument("--auto",       action="store_true", help="自动选择全部图片，跳过交互")

    args_cli = parser.parse_args()
    args_dict = vars(args_cli)

    if not args_dict["api_key"]:
        print("❌ 错误：未设置 API Key")
        print("   请设置环境变量 BANANA2_API_KEY 或通过 --api-key 参数传递")
        sys.exit(1)

    result = execute(args_dict)
    if not result.get("success"):
        print(f"\n❌ 错误：{result.get('error', '未知错误')}")
        sys.exit(1)


if __name__ == "__main__":
    main()
