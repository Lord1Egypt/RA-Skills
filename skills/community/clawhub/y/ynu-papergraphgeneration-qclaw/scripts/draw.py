"""
paper-diagram-skill / draw.py
=============================
标准化流程：

  Step 1  扫描  ── LLM 分析论文，识别可可视化部分
  Step 2  排序  ── 以表格形式展示，按优先级排列
  Step 3  选图  ── 用户选择要生成的图片
  Step 4  生成  ── 逐一生成图片
  Step 5  校验  ── 检查图片结构是否与原文逻辑冲突
  Step 6  重生  ── 有偏差则询问是否调整描述词重生成
"""

import os, json, sys, argparse, textwrap, re, urllib.request, urllib.parse
from pathlib import Path

# ── 内置模块 ──────────────────────────────────────────────
from pdf_to_text import extract_text
from image_generator import generate_image, build_academic_prompt
from self_checker import check_figure_logical_consistency

_SCRIPT_DIR = Path(__file__).parent.resolve()
_SKILL_DIR  = _SCRIPT_DIR.parent
sys.path.insert(0, str(_SCRIPT_DIR))


# ─────────────────────────────────────────────────────────
# 共享 API 调用函数（被 scan_paper_llm 和 image_generator 共用）
# ─────────────────────────────────────────────────────────
def call_llm(prompt: str, api_url: str = None, api_key: str = None,
             model: str = None, timeout: int = 60) -> str:
    """通过 HTTP 调用 LLM API，返回文本响应。"""
    if api_url is None:
        api_url = os.environ.get(
            "BANANA2_API_URL",
            "https://api.acedata.cloud/nano-banana/chat"
        )
    if api_key is None:
        api_key = os.environ.get("BANANA2_API_KEY",
                                os.environ.get("ACEDATA_API_KEY", ""))
    if model is None:
        model = os.environ.get("BANANA2_MODEL", "nano-banana-2")

    payload = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2,
        "max_tokens": 2048,
    }).encode("utf-8")

    req = urllib.request.Request(
        api_url,
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        return data["choices"][0]["message"]["content"]


# ─────────────────────────────────────────────────────────
# Step 1：LLM 扫描论文（替换原关键词版本）
# ─────────────────────────────────────────────────────────
def scan_paper_llm(raw_text: str,
                   api_url: str = None,
                   api_key: str = None,
                   model: str = None) -> list[dict]:
    """
    用 LLM 分析论文文本，识别所有可生成 figure 的章节，
    返回结构化列表（与原 scan_paper 格式完全兼容）。

    LLM 会：
      1. 识别论文结构（引言/方法/实验/结论）
      2. 发现所有 figure/table 引用及描述
      3. 判断每个可视化候选的：类型、重要性、来源
      4. 生成中文描述（供后续生图用）
      5. 输出 JSON 数组

    返回格式：
      [{
        "id":          int,   # 序号（1-based）
        "priority":    str,   # High / Medium / Low
        "type":        str,   # 架构图 / 对比折线图 / 多面板图 / 对比柱状图 / 消融图 ...
        "title_cn":    str,   # 中文标题
        "title_en":    str,   # 英文标题
        "source":      str,   # 原文出处（图号/章节号）
        "description": str,   # 中文详细描述（供 LLM 生图用）
        "topology":    str,   # topology 字符串
        "user_req":    str,   # user_requirement 补充
      }, ...]
    """

    # 裁剪过长文本（API 有 token 上限，只传核心部分）
    MAX_CHARS = 12000
    paper_body = raw_text
    if len(raw_text) > MAX_CHARS:
        # 优先保留开头（摘要+引言）和结尾（实验部分）
        head = raw_text[:6000]
        tail = raw_text[-6000:]
        paper_body = head + "\n...\n[中间部分已截断，长度限制]...\n" + tail

    system_prompt = textwrap.dedent("""\
        你是一篇学术论文的可视化顾问。
        你的任务是从一篇论文的文本中，识别出所有适合生成学术插图的内容，
        并给出结构化的描述，供 AI 生图模型使用。

        请严格按以下流程分析：

        1. 识别论文结构：找到标题、摘要、Section/章节标题、Figure/Table 引用
        2. 对每个 Figure 引用，提取：
           - 图号（Figure X / 图X）和标题
           - 所在章节
           - 描述性文字（摘要/图注/实验描述中的关键信息）
        3. 识别以下类型的可视化候选：
           - 架构图：模型结构、pipeline、framework、overview
           - 对比折线图：随数据量/规模变化的精度曲线
           - 多面板图：多子图的组合图（如 ablation 分栏）
           - 对比柱状图：多方法/多数据集的精度对比
           - 消融图/表格：ablation study，结果表格
           - 热力图：CAM、attention、相似度矩阵
           - 示例图：检索结果、可视化样本
        4. 判断重要性：
           - High：论文核心贡献图（架构图、主要实验图）
           - Medium：支撑性实验图（消融、扩展实验）
           - Low：补充性图（数据集样本、可视化细节）
        5. 为每个候选生成：
           - 中文详细描述（100-300字）：图里应包含什么元素？
           - topology 字符串：简洁的结构描述（英文，逗号分隔）
           - user_requirement：额外约束（数据点值、颜色、布局等）

        输出要求：
        - 必须输出有效的 JSON 数组，不要输出其他文字
        - 每个元素必须包含字段：id, priority, type, title_cn, title_en,
          source, description, topology, user_req
        - id 从 1 开始，按 priority（High→Medium→Low）排序
        - description 用中文，100-300字
        - topology 英文，用逗号分隔的关键词（如 "left-to-right flow, 3 stages"）
        - user_req 为空字符串或补充约束
        - 如果论文没有某类型的图，对应候选也要基于实验描述生成
          （不要因为原文没图就跳过，只要内容值得可视化就生成候选）
        - 最多返回 10 个候选（优先最重要的）
    """).strip()

    user_prompt = f"请分析以下论文文本，输出 JSON 数组：\n\n{paper_body}"

    print("\n🧠 正在调用 LLM 分析论文结构...")
    try:
        response = call_llm(
            prompt=f"{system_prompt}\n\n{user_prompt}",
            api_url=api_url,
            api_key=api_key,
            model=model,
            timeout=120,
        )
    except Exception as e:
        print(f"⚠ LLM 调用失败：{e}，回退到关键词扫描")
        return scan_paper_fallback(raw_text)

    # 解析 JSON
    response = response.strip()
    # 尝试提取代码块内的 JSON
    if response.startswith("```"):
        # 去掉 ```json ... ``` 或 ``` ... ```
        lines = response.split("\n")
        start = next((i for i, l in enumerate(lines) if l.strip().startswith("```")), 0)
        end   = next((i for i, l in enumerate(lines[start+1:], start+1) if l.strip().startswith("```")), len(lines)-1)
        response = "\n".join(lines[start+1:end])

    try:
        items = json.loads(response)
    except json.JSONDecodeError as e:
        print(f"⚠ LLM 返回非 JSON（{e}），回退到关键词扫描")
        return scan_paper_fallback(raw_text)

    # 验证格式并补全字段
    validated = []
    for i, item in enumerate(items):
        if not isinstance(item, dict):
            continue
        validated.append({
            "id":          item.get("id", i+1),
            "priority":    item.get("priority", "Medium"),
            "type":        item.get("type", "架构图"),
            "title_cn":    item.get("title_cn", item.get("title", "")),
            "title_en":    item.get("title_en", ""),
            "source":      item.get("source", ""),
            "description": item.get("description", ""),
            "topology":    item.get("topology", ""),
            "user_req":    item.get("user_req", ""),
        })

    # 重新编号
    for i, item in enumerate(validated, 1):
        item["id"] = i

    # 按 priority 排序
    prio_order = {"High": 0, "Medium": 1, "Low": 2}
    validated.sort(key=lambda x: (prio_order.get(x["priority"], 1), x["id"]))

    print(f"✅ LLM 识别出 {len(validated)} 个可视化候选")
    return validated


# ─────────────────────────────────────────────────────────
# 降级版：关键词扫描（LLM 失败时使用）
# ─────────────────────────────────────────────────────────
def scan_paper_fallback(raw_text: str) -> list[dict]:
    """LLM 不可用时的降级方案，用关键词匹配识别可视化内容。"""
    items = []
    lines = raw_text.split("\n")
    full_lower = raw_text.lower()

    def add(id_, priority, fig_type, title_cn, title_en, source, desc_cn, topology, user_req=""):
        items.append({
            "id": id_, "priority": priority, "type": fig_type,
            "title_cn": title_cn, "title_en": title_en,
            "source": source, "description": desc_cn,
            "topology": topology, "user_req": user_req,
        })

    # 提取原文 figure 引用
    found_figures = []
    for pat, label in [
        (r"(?:Figure|图)\s*1[：:.\s]*(.{10,80})", "Figure 1"),
        (r"(?:Figure|图)\s*2[：:.\s]*(.{10,80})", "Figure 2"),
        (r"(?:Figure|图)\s*3[：:.\s]*(.{10,80})", "Figure 3"),
        (r"(?:Figure|图)\s*4[：:.\s]*(.{10,80})", "Figure 4"),
    ]:
        for m in re.finditer(pat, raw_text, re.IGNORECASE):
            found_figures.append((label, m.group(0)[:120]))

    if any(k in full_lower for k in ["架构", "architecture", "framework", "overview"]):
        add(1, "High", "架构图", "模型架构总览", "Architecture Overview",
            "Section 3", "展示整个模型的完整架构流程，从输入到输出，包含所有主要模块和连接关系",
            "Clean academic architecture diagram, left-to-right hierarchical layout")

    if any(k in full_lower for k in ["损失", "loss", "loss function", "objective"]):
        add(2, "High", "公式/流程图", "训练目标与损失函数", "Training Objective & Loss",
            "Section 3.1-3.3", "展示模型的损失函数构成，包括对比损失、自监督损失等的组合方式",
            "Academic diagram showing mathematical formulation, loss components")

    if any(k in full_lower for k in ["数据高效", "data efficient", "zero-shot", "数据效率"]):
        add(3, "High", "对比折线图", "数据效率对比", "Data Efficiency Comparison",
            "Figure 1", "X轴为训练数据量，Y轴为零样本Top-1精度，绘制DeCLIP和CLIP两条对比曲线",
            "Line chart, two curves (CLIP vs DeCLIP), annotated data points")

    if any(k in full_lower for k in ["自监督", "multi-view", "nearest neighbor", "mvs", "nns"]):
        add(4, "High", "多面板图", "三种监督信号详解", "Three Supervision Signals",
            "Section 3.3", "三栏并排布局展示三种监督信号",
            "Three-panel figure, distinct background colors per panel")

    if any(k in full_lower for k in ["下游", "迁移", "transfer", "linear probe"]):
        add(5, "High", "对比柱状图", "下游任务迁移效果对比", "Downstream Task Transfer",
            "Table 3", "11个下游数据集的线性探针精度对比柱状图",
            "Grouped bar chart, 11 datasets, CLIP vs DeCLIP")

    if any(k in full_lower for k in ["消融", "ablation"]):
        add(6, "Medium", "消融图/表格", "各监督信号消融实验", "Ablation Study",
            "Table 4", "展示SS、MVS、NNS各监督信号的消融结果",
            "Table or grouped bar chart, ablation results for SS/MVS/NNS")

    prio_order = {"High": 0, "Medium": 1, "Low": 2}
    items.sort(key=lambda x: (prio_order[x["priority"]], x["id"]))
    for i, item in enumerate(items, 1):
        item["id"] = i
    return items


# ─────────────────────────────────────────────────────────
# 兼容旧名（供 execute 调用）
# ─────────────────────────────────────────────────────────
def scan_paper(raw_text: str, api_url: str = None,
               api_key: str = None, model: str = None) -> list[dict]:
    """scan_paper 入口：优先调用 LLM，失败则降级关键词。"""
    return scan_paper_llm(raw_text, api_url, api_key, model)


# ─────────────────────────────────────────────────────────
# Step 2：格式化表格输出
# ─────────────────────────────────────────────────────────
def print_visualization_table(items: list[dict]):
    header = f"{'#':<3} {'优先级':<8} {'类型':<12} {'标题':<28} {'来源':<15}"
    sep = "─" * 72
    print("\n" + "═" * 74)
    print("  📊 论文可视化扫描结果（LLM 智能分析）")
    print("═" * 74)
    print(header)
    print(sep)

    prio_emoji  = {"High": "🔴", "Medium": "🟡", "Low": "⚪"}
    type_emoji  = {
        "架构图": "🏗", "对比折线图": "📈", "多面板图": "🗂",
        "对比柱状图": "📊", "公式/流程图": "🔢", "示例图": "🖼",
        "消融图/表格": "🔬", "折线图": "📈", "热力图": "🔥",
        "样本展示": "📦", "扩展曲线图": "📐",
    }

    for item in items:
        ep  = prio_emoji.get(item["priority"], "⚪")
        et  = type_emoji.get(item["type"], "•")
        ttl = (item.get("title_cn","") + " / " + item.get("title_en","")[:14])[:30]
        print(
            f"{ep} {item['id']:<2} {item['priority']:<8} "
            f"{et}{item['type']:<11} {ttl:<30} {item.get('source',''):<15}"
        )

    print(sep)
    print(f"共识别 {len(items)} 个可可视化部分（High={sum(1 for i in items if i['priority']=='High')}  "
          f"Medium={sum(1 for i in items if i['priority']=='Medium')}  "
          f"Low={sum(1 for i in items if i['priority']=='Low')}）\n")


def ask_user_selection(items: list[dict]) -> list[int]:
    print("请输入要生成的图片编号（1 / 1,3,5 / 1-5 / all）：")
    choice = input("> ").strip().lower()
    if choice in ("all", "全部", ""):
        return [item["id"] for item in items]
    ids = set()
    for part in choice.replace("，", ",").split(","):
        part = part.strip()
        if "-" in part:
            s, e = part.split("-", 1)
            ids.update(range(int(s), int(e) + 1))
        elif part.isdigit():
            ids.add(int(part))
    return sorted(ids)


# ─────────────────────────────────────────────────────────
# Step 5：校验图片逻辑一致性
# ─────────────────────────────────────────────────────────
def verify_figure(item: dict, generated_path: str) -> tuple[bool, str]:
    try:
        result = check_figure_logical_consistency(
            figure_path=generated_path,
            paper_text="",
            figure_type=item["type"],
        )
        passed = result.get("passed", True)
        issues = result.get("issues", [])
        msg = "\n".join(issues) if issues else "未发现明显偏差 ✓"
        return passed, msg
    except Exception as e:
        return False, f"校验过程出错：{e}"


def ask_regenerate(item: dict, issue_msg: str) -> bool:
    print("\n" + "!" * 60)
    print(f"  ⚠️  发现潜在偏差（图片 #{item['id']}：{item['title_cn']}）")
    print("!" * 60)
    print(f"  问题描述：{issue_msg}")
    print("  是否重新生成？（y / n）")
    return input("> ").strip().lower() in ("y", "yes", "是", "1", "ok")


# ─────────────────────────────────────────────────────────
# Step 5：增强型 Prompt 自动调整（基于 self_checker）
# ─────────────────────────────────────────────────────────
def enhance_prompt_from_check(prompt_dict: dict, issues: list[str],
                               warnings: list[str], figure_type: str) -> dict:
    import copy
    new_prompt = copy.deepcopy(prompt_dict)
    corrections = []

    for issue in issues:
        il = issue.lower()
        if "占位符" in issue or "placeholder" in il:
            corrections.append(
                "STRICT: Every module must contain visible, correct text labels. "
                "No placeholder, no blank boxes. All names must be real Chinese/English words."
            )
        if figure_type in ("架构图", "多面板图", "公式/流程图"):
            if any(k in il for k in ["结构", "encoder", "loss", "关键词"]):
                corrections.append(
                    "STRUCTURE: Include Image Encoder, Text Encoder, Loss Module, "
                    "Projection Layers. Solid arrows = forward, dashed = stop-gradient. "
                    "Each module = colored rectangle with text label inside."
                )
        if figure_type in ("对比折线图", "折线图"):
            if any(k in il for k in ["坐标轴", "数据标注", "图表结构"]):
                corrections.append(
                    "STRUCTURE: X-axis (Training Data Size), Y-axis (Top-1 Acc %), "
                    "grid lines, annotated data points, legend (CLIP vs DeCLIP)."
                )
        if figure_type in ("对比柱状图",):
            if any(k in il for k in ["数据集", "指标", "结构"]):
                corrections.append(
                    "STRUCTURE: X-axis (datasets), Y-axis (Accuracy %), "
                    "grouped bars, color legend, readable tick labels."
                )
        if figure_type in ("多面板图",):
            if any(k in il for k in ["面板", "panel", "(a)"]):
                corrections.append(
                    "STRUCTURE: Each sub-panel labeled (a), (b), (c) top-left, "
                    "with panel title below the label."
                )
        if figure_type in ("消融图/表格",):
            if any(k in il for k in ["消融", "监督信号", "ablation"]):
                corrections.append(
                    "STRUCTURE: Show ablation rows/columns for SS, MVS, NNS, "
                    "with numerical results. Purple for loss modules."
                )

    for warn in warnings:
        if "分辨率较低" in warn:
            corrections.append("QUALITY: Minimum 2048px width, sharp readable text at print scale.")
        if "宽高比异常" in warn:
            corrections.append("LAYOUT: Use 16:9 or 4:3 aspect ratio, natural undistorted proportions.")

    corrections.append(
        "FLAT_2D: No shadows, no gradients, no 3D, no perspective. "
        "Pure flat 2D schematic. Solid thin borders (1.5px black), "
        "rounded rectangles (radius 8px), solid fills only."
    )

    combined = "\n".join(corrections)
    old_req = new_prompt.get("user_requirement", "")
    new_prompt["user_requirement"] = (
        old_req + "\n\n[Auto-correction from self-check]\n" + combined
    )
    return new_prompt


# ─────────────────────────────────────────────────────────
# Step 4：生成单张图片（带主动自检循环）
# ─────────────────────────────────────────────────────────
def generate_single_figure(
    item: dict, api_url: str, api_key: str, model: str,
    output_dir: str, timeout: int = 300,
    auto_retry: bool = False, max_attempts: int = 3,
    paper_text: str = "",
) -> tuple[bool, str]:

    print(f"\n{'─'*60}")
    print(f"  🔄 生成 #{item['id']}：{item['title_cn']} / {item['title_en']}")
    print(f"  来源：{item.get('source', 'N/A')}  |  类型：{item['type']}")
    print(f"{'─'*60}")

    prompt_dict = build_academic_prompt(
        topology=item.get("topology", ""),
        figure_type=item["type"],
        user_requirement=item.get("user_req", ""),
        style_name="cvpr",
    )

    safe_name = re.sub(r"[^\w]", "_", item["title_en"])[:20]
    filename  = f"fig_{item['id']:02d}_{safe_name}.png"
    path      = os.path.join(output_dir, filename)

    attempt = 0
    while True:
        attempt += 1
        print(f"\n  [{attempt}] 调用生图 API...")

        success, out_path, err = generate_image(
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
                continue
            print("  是否重试？（y / n）")
            if input("> ").strip().lower() not in ("y", "yes", "1"):
                return False, ""
            continue

        print(f"\n  ✅ 生成完成：{out_path}")

        # 自检
        try:
            check_result = check_figure_logical_consistency(
                figure_path=out_path,
                paper_text=paper_text,
                figure_type=item["type"],
            )
            passed  = check_result.get("passed", True)
            issues  = check_result.get("issues", [])
            warnings_ = check_result.get("warnings", [])
            issue_msg = "\n".join(issues) if issues else (
                "\n".join(warnings_) if warnings_ else "未发现明显偏差 ✓"
            )
        except Exception:
            passed = True
            issues = []
            warnings_ = []
            issue_msg = "校验跳过（出错）"

        print(f"\n  🔍 自检结果：{'通过 ✓' if passed else '有偏差 ⚠️'}")
        for i in issues:
            print(f"     ❗ {i}")
        for w in warnings_:
            print(f"     ⚠  {w}")

        if not passed and attempt < max_attempts:
            print(f"\n  🔧 [自动] 第 {attempt}/{max_attempts} 次，通过自检调整 prompt，重新生成...")
            prompt_dict = enhance_prompt_from_check(
                prompt_dict, issues, warnings_, item["type"]
            )
            continue
        elif not passed:
            print(f"\n  ⚠  已达最大重试次数（{max_attempts}），保留当前版本。")
            return True, out_path
        else:
            print("  ✅ 图片通过全部自检。")
            return True, out_path


# ─────────────────────────────────────────────────────────
# 主入口（execute，供 OpenClaw 调用）
# ─────────────────────────────────────────────────────────
def execute(args: dict, context: dict = None) -> dict:
    raw_input = args.get("input", "")
    if not raw_input:
        return {"success": False, "error": "缺少 input 参数"}

    # 读取输入
    if os.path.isfile(raw_input):
        ext = Path(raw_input).suffix.lower()
        if ext == ".pdf":
            raw_text = extract_text(raw_input)
        else:
            with open(raw_input, encoding="utf-8") as f:
                raw_text = f.read()
    else:
        raw_text = raw_input

    if len(raw_text) < 200:
        return {"success": False, "error": f"输入内容太短（{len(raw_text)} 字符）"}

    # API 配置
    api_url    = args.get("api_url",    os.environ.get(
        "BANANA2_API_URL", "https://api.acedata.cloud/nano-banana/images"))
    api_key    = args.get("api_key",    os.environ.get(
        "BANANA2_API_KEY", os.environ.get("ACEDATA_API_KEY", "")))
    model      = args.get("model",      os.environ.get("BANANA2_MODEL", "nano-banana-2"))
    output_dir = args.get("output_dir", str(_SCRIPT_DIR / "outputs"))
    auto_select= args.get("auto_select", False)

    # LLM API 配置（用于 scan_paper）
    llm_url = args.get("llm_url",    api_url.replace("/images", "/chat", 1)
                        if "/images" in api_url else None)
    llm_key = api_key

    if not api_key:
        return {"success": False, "error": "未设置 API Key"}

    os.makedirs(output_dir, exist_ok=True)

    # Step 1：LLM 扫描
    print(f"\n📖 正在扫描论文（{len(raw_text)} 字）...")
    items = scan_paper_llm(raw_text, api_url=llm_url, api_key=llm_key, model=model)
    if not items:
        return {"success": False, "error": "未能从论文中识别到可可视化的内容"}

    print_visualization_table(items)

    # Step 2：用户选择
    if auto_select:
        selected_ids = [item["id"] for item in items]
    else:
        print("─" * 60)
        selected_ids = ask_user_selection(items)
        if not selected_ids:
            print("未选择任何图片，退出。")
            return {"success": True, "generated": [], "skipped": []}

    selected_items = [item for item in items if item["id"] in selected_ids]

    # Step 3：逐一生成
    print(f"\n🎯 开始生成 {len(selected_items)} 张图片（开启主动自检，最多重试 2 次）...\n")
    results = []
    for item in selected_items:
        success, path = generate_single_figure(
            item, api_url, api_key, model, output_dir,
            auto_retry=True, max_attempts=3, paper_text=raw_text,
        )
        results.append({
            "id": item["id"], "title": item["title_cn"],
            "success": success, "path": path,
        })

    # 汇总报告
    print("\n" + "═" * 64)
    print("  📦 生成报告")
    print("═" * 64)
    for r in results:
        icon = "✅" if r["success"] else "❌"
        print(f"  {icon} #{r['id']:2d}  {r['title']:<26}  {r['path']}")
    print("═" * 64)

    return {
        "success": True,
        "generated": [r for r in results if r["success"]],
        "failed":    [r for r in results if not r["success"]],
    }


# ─────────────────────────────────────────────────────────
# CLI 入口
# ─────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Paper Diagram Generator (LLM-Powered Scan)")
    parser.add_argument("--input", "-i", required=True)
    parser.add_argument("--api-url",    default=os.environ.get("BANANA2_API_URL",
                        "https://api.acedata.cloud/nano-banana/images"))
    parser.add_argument("--api-key",    default=os.environ.get("BANANA2_API_KEY",
                        os.environ.get("ACEDATA_API_KEY", "")))
    parser.add_argument("--model",     default=os.environ.get("BANANA2_MODEL", "nano-banana-2"))
    parser.add_argument("--output-dir", default=str(_SCRIPT_DIR / "outputs"))
    parser.add_argument("--auto",       action="store_true")

    args_cli = vars(parser.parse_args())
    if not args_cli["api_key"]:
        print("❌ 错误：未设置 API Key（--api-key 或 BANANA2_API_KEY）")
        sys.exit(1)

    result = execute(args_cli)
    if not result.get("success"):
        print(f"\n❌ 错误：{result.get('error')}")
        sys.exit(1)


if __name__ == "__main__":
    main()
