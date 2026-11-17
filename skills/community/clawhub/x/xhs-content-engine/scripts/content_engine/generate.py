"""Generate mode 主编排。

流程（v0.3.0）：
1. 解析链接 → 找/拆解 deconstruction card（v0.2.1 自动 fallback）
2. 读 graph 必读节点（brand-voice / brand-story / segments / taboo / hooks / style-tags）
3. 调 LLM 生成 5 类文本（脚本 → 字幕 / 封面文案 / desc / tags）
4. (video 类型) 生成 seedance-prompt.md
5. (v0.3.0, video + real_video) Seedance 真生视频：N 个 shot → ffmpeg 拼成片
6. Nano Banana 出 N 张参考素材图 + 1 张封面图
7. validator 质检（v0.2.1）
8. 写入 generated/GEN-xxx-{type}/ 目录
"""

from __future__ import annotations
import json
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from pathlib import Path

from .llm import OfoxLLMClient, OfoxError
from .lookup import find_card_by_note_id, find_or_auto_create, make_v2_generated_dir, DEFAULT_FRESHNESS_DAYS
from .nano_banana import generate_image, build_prompt as build_image_prompt
from .prompts import (
    system_for_brand,
    prompt_script,
    prompt_caption,
    prompt_cover_text,
    prompt_desc,
    prompt_tags,
    prompt_seedance_video,
)
from .seedance import (
    SeedanceError,
    ark_credentials_present,
    estimate_cost_usd,
    help_message as seedance_help_message,
)
from .validator import validate_workspace, extract_taboo_words_from_graph
from .video_compose import compose, submit_all, write_partial_report


# ─── 数据结构 ───

@dataclass
class GenerateInput:
    """v2 generate 的全部输入。"""
    link: str
    type: str = "video"           # video / image / script
    count: int = 1
    product_imgs: list[Path] = field(default_factory=list)
    product_usp: str = ""
    out_dir: Path | None = None
    fresh: bool = False
    freshness_days: int = DEFAULT_FRESHNESS_DAYS
    # v0.3.0 视频生成开关
    real_video: bool = True       # video 类型默认真生视频；--no-real-video 关闭
    async_video: bool = False     # 异步模式：仅提交不轮询，generate.py 立即返回
    cost_confirm_seconds: int = 3 # 真生视频前的 Ctrl+C 倒数（0 = 不等）


@dataclass
class GraphContext:
    """从 graph/ 读出的品牌上下文（容错：缺啥都能跑）。"""
    brand_voice: str = ""
    brand_story: str = ""
    segments: str = ""
    taboo: str = ""
    hooks: str = ""
    style_tags: str = ""
    xiaohongshu: str = ""


@dataclass
class GenerateOutput:
    """generate 的完整产出 metadata。"""
    note_id: str
    card_path: Path
    gen_dir: Path
    type: str
    count: int
    files: list[str] = field(default_factory=list)
    duration_seconds: float = 0
    llm_calls: int = 0
    # v0.3.0 视频
    final_video: Path | None = None   # ffmpeg 拼接后的成片
    shots_total: int = 0
    shots_succeeded: int = 0
    pending_video_tasks: list[str] = field(default_factory=list)  # async 模式提交的 task_id


# ─── 工具：读 graph ───

def read_graph_context(skill_root: Path) -> GraphContext:
    """读 graph/ 所有必需节点，缺失文件不阻断（容错）。"""
    graph = skill_root / "graph"

    def read_safe(rel: str) -> str:
        p = graph / rel
        if not p.exists():
            return ""
        try:
            text = p.read_text(encoding="utf-8")
            # 跳过含大量 # TODO: 的占位文件（说明用户没填）
            if text.count("# TODO:") >= 3:
                return ""  # 视为空，让 prompt 走"无品牌上下文"路径
            return text
        except (OSError, UnicodeDecodeError):
            return ""

    return GraphContext(
        brand_voice=read_safe("brand/brand-voice.md"),
        brand_story=read_safe("brand/brand-story.md"),
        segments=read_safe("audience/segments.md"),
        taboo=read_safe("engine/taboo.md"),
        hooks=read_safe("engine/hooks.md"),
        style_tags=read_safe("engine/style-tags.md"),
        xiaohongshu=read_safe("platforms/xiaohongshu.md"),
    )


# ─── 主流程 ───

def generate(
    input_: GenerateInput,
    skill_root: Path | None = None,
    deconstructions_dir: Path | None = None,
    log=print,
) -> GenerateOutput:
    """v2.0 M1 主入口（文本类 only，不出图）。

    Args:
        input_: GenerateInput 包
        skill_root: skill 根目录（默认推断）
        deconstructions_dir: 拆解卡目录（默认 cwd/docs/deconstructions/）
        log: 进度输出函数（默认 print）

    Returns:
        GenerateOutput summary
    """
    t0 = time.time()
    if skill_root is None:
        skill_root = Path(__file__).resolve().parent.parent.parent
    if deconstructions_dir is None:
        deconstructions_dir = Path.cwd() / "docs" / "deconstructions"

    # ─── Step 1: 链接 → note_id ───
    log("[1] Resolving link...")
    from .linkresolve import resolve_xhs_link
    note_id, _ = resolve_xhs_link(input_.link)
    log(f"    note_id = {note_id}")

    # ─── Step 2: 找拆解卡（找不到自动 fallback 跑 v1 + 写 stub）───
    log("[2] Looking up deconstruction card...")
    if input_.fresh:
        log("    --fresh: bypass cache, force auto-create new stub card")
        # --fresh 时我们仍跑 auto_create_card（生成新 stub）；用户可手动复用旧卡
        from .lookup import auto_create_card
        card_path = auto_create_card(input_.link, note_id, deconstructions_dir, log)
    else:
        result = find_or_auto_create(
            link=input_.link,
            note_id=note_id,
            deconstructions_dir=deconstructions_dir,
            freshness_days=input_.freshness_days,
            log=log,
        )
        if result.card_path:
            if "AUTO-STUB" in result.card_path.read_text(encoding="utf-8")[:500]:
                log(f"    using auto-stub card: {result.card_path.name}")
                log(f"    ⚠️ stub 仅含文本字段；视觉字段（拆解/风格/钩子）建议 agent 完善后 --fresh 重跑")
            else:
                log(f"    found: {result.card_path.name} (age {result.age_days}d, fresh={result.is_fresh})")
                if not result.is_fresh:
                    log(f"    ⚠️ card is older than {input_.freshness_days} days — consider --fresh to re-deconstruct")
        card_path = result.card_path

    deconstruction = card_path.read_text(encoding="utf-8")

    # ─── Step 3: 读 graph 上下文 ───
    log("[3] Reading graph context...")
    ctx = read_graph_context(skill_root)
    nonempty = sum(1 for v in vars(ctx).values() if v)
    log(f"    loaded {nonempty}/7 graph nodes (others empty/template)")

    # ─── Step 4: 准备工作区 ───
    log("[4] Preparing workspace...")
    if input_.out_dir:
        gen_dir = input_.out_dir
        gen_dir.mkdir(parents=True, exist_ok=True)
    else:
        # 默认放在拆解卡所在目录的 generated/ 子目录
        # 兼容两种结构：
        # - v1 旧（.md 单文件）：放到 deconstructions/AIC-xxx-slug.md → generated 应放到 deconstructions/AIC-xxx-slug-generated/
        # - v2 新（目录）：放到 deconstructions/AIC-xxx-slug/generated/
        if card_path.suffix == ".md":  # v1 旧结构
            stem = card_path.stem
            gen_root = card_path.parent / f"{stem}-generated"
        else:  # v2 新结构
            gen_root = card_path.parent / "generated"
        gen_id = f"GEN-{time.strftime('%y%m%d')}-{int(time.time()) % 1000:03d}"
        gen_dir = gen_root / f"{gen_id}-{input_.type}"
        gen_dir.mkdir(parents=True, exist_ok=True)
    log(f"    workspace = {gen_dir}")

    # ─── Step 5: LLM 生成脚本（核心） ───
    log("[5] Generating script (core)...")
    llm = OfoxLLMClient()
    sys_msg = system_for_brand(
        brand_voice=ctx.brand_voice,
        brand_story=ctx.brand_story,
        audience=ctx.segments,
        taboo=ctx.taboo,
    )

    product_imgs_desc = (
        f"用户提供 {len(input_.product_imgs)} 张产品图（路径见命令行参数）"
        if input_.product_imgs else ""
    )

    script_prompt = prompt_script(
        deconstruction=deconstruction,
        product_usp=input_.product_usp,
        product_imgs_desc=product_imgs_desc,
        output_type=input_.type,
        output_count=input_.count,
    )
    script_md = llm.chat([
        {"role": "system", "content": sys_msg},
        {"role": "user", "content": script_prompt},
    ])
    (gen_dir / "script.md").write_text(script_md, encoding="utf-8")
    log(f"    script.md written ({len(script_md)} chars)")

    llm_calls = 1

    # ─── Step 6: 并行生成 4 类辅助文本 ───
    log("[6] Generating ancillary text in parallel (caption / cover / desc / tags)...")

    tasks = {}
    if input_.type == "video":
        tasks["caption.txt"] = ("caption", prompt_caption(script_md))
    tasks["cover.txt"] = ("cover", prompt_cover_text(script_md, deconstruction))
    tasks["desc.txt"] = ("desc", prompt_desc(script_md, deconstruction))

    # tags 依赖 desc，先单线程出
    # (其他可并行)

    parallel_results: dict[str, str] = {}
    with ThreadPoolExecutor(max_workers=3) as pool:
        future_to_name = {
            pool.submit(
                llm.chat, [
                    {"role": "system", "content": sys_msg},
                    {"role": "user", "content": prompt_text},
                ]
            ): (filename, label)
            for filename, (label, prompt_text) in tasks.items()
        }
        for future in as_completed(future_to_name):
            filename, label = future_to_name[future]
            try:
                result = future.result()
                parallel_results[filename] = result
                (gen_dir / filename).write_text(result, encoding="utf-8")
                log(f"    {filename} written ({len(result)} chars)")
                llm_calls += 1
            except Exception as e:
                log(f"    ⚠️ {filename} failed: {e}")
                parallel_results[filename] = ""

    # ─── Step 7: tags（依赖 desc）───
    desc_text = parallel_results.get("desc.txt", "")
    if desc_text:
        log("[7] Generating tags (depends on desc)...")
        tags_text = llm.chat([
            {"role": "system", "content": sys_msg},
            {"role": "user", "content": prompt_tags(desc_text, deconstruction)},
        ])
        (gen_dir / "tags.txt").write_text(tags_text, encoding="utf-8")
        log(f"    tags.txt written ({len(tags_text)} chars)")
        llm_calls += 1
    else:
        log("[7] Skipping tags (desc generation failed)")

    # ─── Step 8: Seedance prompt（仅 video 类型）───
    final_video = None
    shots_total = 0
    shots_succeeded = 0
    pending_video_tasks: list[str] = []
    if input_.type == "video":
        log("[8] Video type: generating Seedance cinema-style prompt...")
        seedance_md = llm.chat([
            {"role": "system", "content": sys_msg},
            {"role": "user", "content": prompt_seedance_video(script_md, deconstruction)},
        ])
        (gen_dir / "seedance-prompt.md").write_text(seedance_md, encoding="utf-8")
        log(f"    seedance-prompt.md written ({len(seedance_md)} chars)")
        llm_calls += 1

        # ─── Step 8.5 (v0.3.0): 真生视频 ───
        if input_.real_video:
            shots_total, shots_succeeded, final_video, pending_video_tasks = _run_seedance(
                input_, seedance_md, gen_dir, log,
            )
        else:
            log("    ⚠️ --no-real-video: skipping Seedance API call (use prompt manually)")

    # ─── Step 9: 图片生成（Nano Banana 三路约束 prompt） ───
    image_calls = 0
    if input_.type in ("video", "image"):
        log("[9] Generating images via Nano Banana...")
        image_calls = _generate_images(
            gen_dir=gen_dir,
            input_=input_,
            script_md=script_md,
            deconstruction=deconstruction,
            ctx=ctx,
            log=log,
        )

    # ─── Step 10: validator 质检 ───
    log("[10] Running validator (hard errors auto-retry, soft warnings → quality_report.md)...")
    extra_taboo = extract_taboo_words_from_graph(ctx.taboo)
    report = validate_workspace(gen_dir, input_.type, extra_banned_words=tuple(extra_taboo))

    # 硬错重跑（最多 1 次，避免无限循环）
    if report.has_hard_errors and not getattr(input_, "_retry_attempted", False):
        log(f"    {report.summary_line()} — attempting auto-retry of failed text steps")
        input_._retry_attempted = True  # 标记已重试，避免再次进入
        retry_calls = _retry_hard_errors(
            report, gen_dir, deconstruction, ctx, sys_msg, llm, log,
        )
        llm_calls += retry_calls
        # 重跑后再 validate 一次
        report = validate_workspace(gen_dir, input_.type, extra_banned_words=tuple(extra_taboo))
        log(f"    after retry: {report.summary_line()}")

    # 写 quality_report.md
    (gen_dir / "quality_report.md").write_text(report.to_markdown(), encoding="utf-8")

    # ─── Step 11: 总结 ───
    files = sorted(p.name for p in gen_dir.iterdir())
    if (gen_dir / "frames").exists():
        files = [f for f in files if f != "frames"]
        files.append(f"frames/ ({len(list((gen_dir / 'frames').iterdir()))} 张)")
    if (gen_dir / "shots").exists():
        files = [f for f in files if f != "shots"]
        files.append(f"shots/ ({len(list((gen_dir / 'shots').glob('*.mp4')))} 个分镜)")
    duration = time.time() - t0
    log(f"[11] Done in {duration:.1f}s · {llm_calls} LLM + {image_calls} image calls · {len(files)} entries")
    log(f"     Quality: {report.summary_line()}")
    if final_video:
        log(f"     🎬 Final video: {final_video} ({shots_succeeded}/{shots_total} shots)")
    elif pending_video_tasks:
        log(f"     ⏳ {len(pending_video_tasks)} video tasks submitted (async); poll later")

    return GenerateOutput(
        note_id=note_id,
        card_path=card_path,
        gen_dir=gen_dir,
        type=input_.type,
        count=input_.count,
        files=files,
        duration_seconds=round(duration, 1),
        llm_calls=llm_calls + image_calls,
        final_video=final_video,
        shots_total=shots_total,
        shots_succeeded=shots_succeeded,
        pending_video_tasks=pending_video_tasks,
    )


def _retry_hard_errors(
    report,
    gen_dir: Path,
    deconstruction: str,
    ctx: "GraphContext",
    sys_msg: str,
    llm: OfoxLLMClient,
    log,
) -> int:
    """对 hard errors 涉及的文本类文件进行重跑。返回重跑的 LLM 调用次数。"""
    retry_calls = 0
    files_to_retry = {issue.file for issue in report.hard if issue.file.endswith((".txt", ".md"))}
    # 不重跑图片（重跑成本太高，且很可能是 prompt 问题需要人工调整）

    for fname in files_to_retry:
        try:
            if fname == "script.md":
                # script 重跑成本高 + 影响下游一切；只在确实空时重跑
                continue  # 暂不自动重跑 script，由人工决定
            elif fname == "desc.txt":
                # 重跑 desc，强调禁忌词
                old_script = (gen_dir / "script.md").read_text(encoding="utf-8") if (gen_dir / "script.md").exists() else ""
                from .prompts import prompt_desc
                user_msg = prompt_desc(old_script, deconstruction) + "\n\n⚠️ 上次生成含禁忌词或太短，重新生成时**严格遵守 system 里的禁忌词清单**。"
                new_text = llm.chat([
                    {"role": "system", "content": sys_msg},
                    {"role": "user", "content": user_msg},
                ])
                (gen_dir / fname).write_text(new_text, encoding="utf-8")
                retry_calls += 1
                log(f"    ↻ retried {fname} ({len(new_text)} chars)")
            elif fname == "tags.txt":
                old_desc = (gen_dir / "desc.txt").read_text(encoding="utf-8") if (gen_dir / "desc.txt").exists() else ""
                from .prompts import prompt_tags
                user_msg = prompt_tags(old_desc, deconstruction) + "\n\n⚠️ 上次标签数不足，重新生成时**至少 10 个**。"
                new_text = llm.chat([
                    {"role": "system", "content": sys_msg},
                    {"role": "user", "content": user_msg},
                ])
                (gen_dir / fname).write_text(new_text, encoding="utf-8")
                retry_calls += 1
                log(f"    ↻ retried {fname} ({len(new_text)} chars)")
            # 其他文件：cover.txt / caption.txt / seedance-prompt.md 暂不自动重跑
        except OfoxError as e:
            log(f"    ⚠️ retry of {fname} failed: {e}")

    return retry_calls


# ─── 图片生成子流程 ───

def _extract_brand_anchors(brand_voice: str, style_tags: str) -> str:
    """从 graph/brand/brand-voice + graph/engine/style-tags 提关键词组合成图片风格锚点。

    很简单的实现：抽前 2 段非空内容，拼接成 prompt-friendly 短语。
    """
    out = []
    if brand_voice:
        # 取 brand-voice 的"价值观三关键词"区段，没有就取前 200 字
        m = re.search(r"价值观.*?\n((?:.+\n){1,5})", brand_voice)
        snippet = m.group(1) if m else brand_voice[:200]
        out.append(f"Brand voice: {snippet.strip()[:200]}")
    if style_tags:
        # 取已有词典的"美学流派"section
        m = re.search(r"美学流派.*?\n((?:[|*\-].+\n){1,8})", style_tags)
        if m:
            out.append(f"Aesthetic dictionary: {m.group(1).strip()[:300]}")
    return "\n".join(out) if out else "Premium aesthetic, restrained, magazine editorial quality"


def _extract_image_descriptions_from_script(script_md: str, count: int) -> list[str]:
    """从 script.md 提 N 个画面描述，给 N 张图各自的 prompt 用。

    策略：
    1. 找形如 "## 图 N" / "## Shot N" / "## 第 N-N 秒" 的分镜头标题
    2. 跳过 preamble（标题 + "整组叙事逻辑" 等总览段）— 这是 issue 3 的根因
    3. 每段提取"构图 / 主体 / 风格 / 画面"等 single-image 描述
    4. 取不到 N 段就把脚本主体平均切

    Returns:
        N 个独立的 single-image 描述（不含拼图/总览语义）
    """
    # 1. 按图标题切段
    sections = re.split(r"\n## (?=图\s*\d+|Shot\s+\d+|第\s*[\d-]+\s*秒)", "\n" + script_md)

    # 2. 关键修复：第一段（preamble）总是包含"整组叙事逻辑"等"多图"描述
    #    必须丢弃，否则 frame_001 会出成拼图
    if len(sections) > 1:
        # 有真分镜段，丢掉 preamble
        per_shot = sections[1:]
    else:
        # 没找到分镜段，整脚本切片
        chunk_size = max(len(script_md) // count, 200)
        return [script_md[i*chunk_size:(i+1)*chunk_size].strip() for i in range(count)]

    per_shot = [s.strip() for s in per_shot if s.strip()]

    # 3. 取前 count 段
    if len(per_shot) >= count:
        return per_shot[:count]

    # 4. 不够 N 段，最后一段重复填充（极少见）
    while len(per_shot) < count:
        per_shot.append(per_shot[-1] if per_shot else script_md[:500])
    return per_shot[:count]


def _generate_images(
    gen_dir: Path,
    input_: "GenerateInput",
    script_md: str,
    deconstruction: str,
    ctx: "GraphContext",
    log,
) -> int:
    """生成参考素材图 + 封面图。

    Returns:
        实际成功生成的图片数（用于统计 + 计费提示）
    """
    success_count = 0
    brand_anchors = _extract_brand_anchors(ctx.brand_voice, ctx.style_tags)

    # 我方产品描述（v2.0 仅文本，v2.1 改 image-to-image）
    product_desc = input_.product_usp or ""
    if input_.product_imgs:
        product_desc += f"\n(reference shots provided: {len(input_.product_imgs)} angles)"

    # 禁忌词（提负面 prompt）
    negative = ""
    if ctx.taboo:
        # 简单提取禁忌段落
        m = re.search(r"超.+词.*?\n((?:[|*\-].+\n){1,10})", ctx.taboo)
        if m:
            negative = m.group(1).strip()[:200]

    # 图片数量：image 类型用 --count；video 类型固定 1 张关键帧
    n_frames = input_.count if input_.type == "image" else 1
    frames_dir = gen_dir / "frames"
    layouts = _extract_image_descriptions_from_script(script_md, n_frames)

    log(f"    will generate {n_frames} reference frame(s) + 1 cover")

    # 并行出图（节制：max 3 路并发，避免触发 API 限流 + 控制费用）
    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = {}
        # 普通 frame：严格 no-text，single-image 约束
        for i, layout in enumerate(layouts, start=1):
            prompt = build_image_prompt(
                layout_description=layout,
                brand_anchors=brand_anchors,
                product_description=product_desc,
                negative=negative,
                is_cover=False,
            )
            out_path = frames_dir / f"frame_{i:03d}.png"
            futures[pool.submit(generate_image, prompt, out_path)] = ("frame", i, out_path)

        # 封面：is_cover=True 允许大字层 + 显式文字内容
        cover_text = ""
        if (gen_dir / "cover.txt").exists():
            cover_text = (gen_dir / "cover.txt").read_text(encoding="utf-8").strip()
        cover_prompt = build_image_prompt(
            layout_description=(
                "Magazine cover style. Single hero product centered with breathing space. "
                "Background is the brand's signature setting. "
                "Reserve clean space for text overlay (upper-center or lower-third)."
            ),
            brand_anchors=brand_anchors,
            product_description=product_desc,
            negative=negative,
            is_cover=True,
            cover_text=cover_text,
        )
        futures[pool.submit(generate_image, cover_prompt, gen_dir / "cover.png")] = ("cover", 0, gen_dir / "cover.png")

        for future in as_completed(futures):
            kind, idx, path = futures[future]
            try:
                future.result()
                size_kb = path.stat().st_size // 1024
                log(f"    ✓ {kind}{f' #{idx}' if kind == 'frame' else ''} → {path.name} ({size_kb}KB)")
                success_count += 1
            except OfoxError as e:
                log(f"    ✗ {kind}{f' #{idx}' if kind == 'frame' else ''} failed: {e}")

    return success_count


# ─── v0.3.0: 真生视频编排 ───

def _run_seedance(
    input_: GenerateInput,
    seedance_md: str,
    gen_dir: Path,
    log,
) -> tuple[int, int, Path | None, list[str]]:
    """video 类型 + real_video=True 时的编排。

    Returns:
        (shots_total, shots_succeeded, final_video_path_or_None, pending_async_task_ids)
    """
    if not ark_credentials_present():
        log("    ⚠️ ARK_API_KEY not configured — skipping real video gen")
        log(f"    {seedance_help_message().splitlines()[0]}")
        return (0, 0, None, [])

    # 数 shot + 估算成本
    from .video_compose import parse_shots
    shots = parse_shots(seedance_md)
    if not shots:
        log("    ⚠️ seedance-prompt.md 解析不出 shot — 跳过真生视频")
        return (0, 0, None, [])

    total_seconds = sum(s.duration for s in shots)
    cost = estimate_cost_usd(num_shots=1, duration_per_shot=total_seconds)
    log(f"[8.5] About to call Seedance API: {len(shots)} shots, total {total_seconds}s")
    log(f"      Estimated cost ≈ ${cost:.2f} USD")

    # Ctrl+C 倒数（用户可中断）
    if input_.cost_confirm_seconds > 0 and not input_.async_video:
        log(f"      Starting in {input_.cost_confirm_seconds}s... (Ctrl+C to abort)")
        try:
            for i in range(input_.cost_confirm_seconds, 0, -1):
                time.sleep(1)
        except KeyboardInterrupt:
            log("      ✗ Aborted by user")
            return (len(shots), 0, None, [])

    shots_dir = gen_dir / "shots"

    # 异步模式：仅提交不轮询
    if input_.async_video:
        log(f"[8.5] --async: submitting {len(shots)} shots, returning immediately")
        results = submit_all(seedance_md)
        pending = []
        failed = 0
        for shot, tid, err in results:
            if tid:
                log(f"      ✓ Shot {shot.index} submitted: {tid}")
                pending.append(tid)
            else:
                log(f"      ✗ Shot {shot.index} submit failed: {err}")
                failed += 1
        # 写一个待轮询说明文件
        (gen_dir / "pending-video-tasks.md").write_text(
            "# Pending Video Tasks (async mode)\n\n"
            f"{len(pending)} 个任务已提交到火山 Ark，请用以下 task_id 手动轮询：\n\n"
            + "\n".join(f"- `{t}`" for t in pending)
            + ("\n\n失败 shot 数：" + str(failed) if failed else ""),
            encoding="utf-8",
        )
        return (len(shots), 0, None, pending)

    # 同步模式：阻塞轮询每个 shot
    log(f"[8.5] Generating {len(shots)} shots (blocking, ~1-3 min each)...")

    last_status = {}
    def on_progress(shot_idx, status, elapsed):
        # 状态变化时打印一次
        prev = last_status.get(shot_idx)
        if status != prev:
            log(f"      Shot {shot_idx}: {status} ({elapsed}s)")
            last_status[shot_idx] = status

    report = compose(
        seedance_md=seedance_md,
        out_dir=shots_dir,
        on_shot_progress=on_progress,
    )

    # 写 partial-video.md（即使全成功也写，方便审计 task_id）
    write_partial_report(report, gen_dir / "partial-video.md")

    if report.all_succeeded and report.final_video:
        log(f"      ✅ All {report.shots_total} shots OK → {report.final_video.name}")
    elif report.has_partial_failure:
        log(f"      ⚠️ {report.shots_succeeded}/{report.shots_total} shots OK; see partial-video.md")
    else:
        log(f"      ✗ All shots failed; see partial-video.md")

    return (
        report.shots_total,
        report.shots_succeeded,
        report.final_video,
        [],
    )
