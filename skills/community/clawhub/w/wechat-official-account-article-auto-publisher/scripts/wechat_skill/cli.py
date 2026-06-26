from __future__ import annotations

import argparse
from pathlib import Path

from .config import load_config
from .utils import ensure_dir, slugify, write_json


def build_parser() -> argparse.ArgumentParser:
    cover_templates = ["insight", "magazine", "minimal"]
    default_config = Path(__file__).resolve().parent.parent.parent / "config.json"
    parser = argparse.ArgumentParser(description="WeChat article publisher skill")
    parser.add_argument("--config", default=str(default_config), help="Path to config.json")
    parser.add_argument("--timeout", type=int, default=30, help="HTTP timeout seconds")

    subparsers = parser.add_subparsers(dest="command", required=True)

    install = subparsers.add_parser("install", help="Install Python dependencies")
    install.add_argument("--upgrade", action="store_true", help="Upgrade dependencies")

    create = subparsers.add_parser("create", help="Prepare creation prompt, outline, and checks")
    create.add_argument("title", help="Article title")
    create.add_argument("--mode", choices=["title_to_article", "rewrite"], default="title_to_article", help="Creation mode")
    create.add_argument("--request", default="", help="One-sentence user request")
    create.add_argument("--request-file", default="", help="File containing user request")
    create.add_argument("--audience", default="", help="Target audience")
    create.add_argument("--angle", default="", help="Article angle")
    create.add_argument("--tone", choices=["professional", "sharp", "warm"], default="professional", help="Writing tone")
    create.add_argument("--key-point", action="append", default=[], help="Key point that must be covered")
    create.add_argument("--constraint", action="append", default=[], help="Fact or boundary that must be preserved")
    create.add_argument("--source-summary", default="", help="Reference article summary")
    create.add_argument("--source-file", default="", help="Local markdown file used as rewrite reference")
    create.add_argument("--heading-count", type=int, default=4, help="Desired number of H2 headings")
    create.add_argument("--article-file", default="", help="Existing markdown article to validate")
    create.add_argument("--output-dir", default="", help="Directory for generated creation assets")

    write = subparsers.add_parser("write", help="Generate article markdown from creation assets")
    write.add_argument("input", help="Creation asset directory or brief.json path")
    write.add_argument("--heading-count", type=int, default=4, help="Desired number of H2 headings")
    write.add_argument("--output", default="", help="Output markdown path")

    workflow = subparsers.add_parser("workflow", help="Run create -> write -> preview -> draft in one command")
    workflow.add_argument("title", help="Article title")
    workflow.add_argument("--request", default="", help="One-sentence user request")
    workflow.add_argument("--request-file", default="", help="File containing user request")
    workflow.add_argument("--mode", choices=["title_to_article", "rewrite"], default="title_to_article", help="Creation mode")
    workflow.add_argument("--audience", default="", help="Target audience")
    workflow.add_argument("--angle", default="", help="Article angle")
    workflow.add_argument("--tone", choices=["professional", "sharp", "warm"], default="professional", help="Writing tone")
    workflow.add_argument("--key-point", action="append", default=[], help="Key point that must be covered")
    workflow.add_argument("--constraint", action="append", default=[], help="Fact or boundary that must be preserved")
    workflow.add_argument("--source-summary", default="", help="Reference article summary")
    workflow.add_argument("--source-file", default="", help="Local markdown file used as rewrite reference")
    workflow.add_argument("--source-url", default="", help="URL used as rewrite reference and content source url")
    workflow.add_argument("--heading-count", type=int, default=4, help="Desired number of H2 headings")
    workflow.add_argument("--output-dir", default="", help="Directory for generated workflow assets")
    workflow.add_argument("--template", choices=["standard", "business", "story"], default="", help="Article template")
    workflow.add_argument("--author", default="", help="Override author")
    workflow.add_argument("--cover-image", default="", help="Local cover image path")
    workflow.add_argument("--cover-provider", choices=["doubao", "qwen"], default="", help="Provider used when generating cover")
    workflow.add_argument("--cover-template", choices=cover_templates, default="magazine", help="Cover template")
    workflow.add_argument("--cover-subtitle", default="", help="Cover subtitle")
    workflow.add_argument("--dry-run", action="store_true", help="Generate article and preview without calling WeChat API")
    workflow.add_argument("--publish", action="store_true", help="Submit draft for publish after creation")
    workflow.add_argument("--status", action="store_true", help="Query publish status once")

    extract = subparsers.add_parser("extract", help="Extract article to markdown")
    extract.add_argument("input", help="mp.weixin URL, generic URL, or markdown file")
    extract.add_argument("--output", default="", help="Output markdown path")

    cover = subparsers.add_parser("cover", help="Generate a cover image")
    cover.add_argument("title", help="Article title")
    cover.add_argument("--subtitle", default="", help="Cover subtitle")
    cover.add_argument("--provider", choices=["doubao", "qwen"], default="", help="Image provider override")
    cover.add_argument("--template", choices=cover_templates, default="magazine", help="Cover template")
    cover.add_argument("--output", default="", help="Output image path")

    material = subparsers.add_parser("material", help="Upload local material to WeChat")
    material.add_argument("file", help="Local file path")
    material.add_argument("--type", default="image", choices=["image", "voice", "video", "thumb"], help="WeChat material type")

    draft = subparsers.add_parser("draft", help="Create draft from URL or markdown")
    draft.add_argument("input", help="mp.weixin URL, generic URL, or markdown file")
    draft.add_argument("--template", choices=["standard", "business", "story"], default="", help="Article template")
    draft.add_argument("--author", default="", help="Override author")
    draft.add_argument("--source-url", default="", help="Override source URL")
    draft.add_argument("--cover-image", default="", help="Local cover image path")
    draft.add_argument("--cover-provider", choices=["doubao", "qwen"], default="", help="Provider used when generating cover")
    draft.add_argument("--cover-template", choices=cover_templates, default="magazine", help="Cover template")
    draft.add_argument("--cover-subtitle", default="", help="Cover subtitle")
    draft.add_argument("--dry-run", action="store_true", help="Render article without calling WeChat API")
    draft.add_argument("--publish", action="store_true", help="Submit draft for publish after creation")
    draft.add_argument("--status", action="store_true", help="Query publish status once")

    publish = subparsers.add_parser("publish", help="Publish an existing draft media_id")
    publish.add_argument("media_id", help="WeChat draft media_id")
    publish.add_argument("--status", action="store_true", help="Query publish status once")

    return parser


def _project_root() -> Path:
    return Path(__file__).resolve().parent.parent.parent


def _output_dir(config) -> Path:
    return ensure_dir(config.resolve_output_dir(_project_root()))


def _install_dependencies(upgrade: bool) -> int:
    import subprocess
    import sys

    req = Path(__file__).resolve().parent.parent / "requirements.txt"
    command = [sys.executable, "-m", "pip", "install"]
    if upgrade:
        command.append("--upgrade")
    command.extend(["-r", str(req)])
    subprocess.check_call(command)
    write_json({"success": True, "installed": True, "requirements": str(req)})
    return 0


def _handle_extract(args, config) -> int:
    from .extractors import load_article

    article = load_article(args.input, timeout=args.timeout)
    output = Path(args.output).resolve() if args.output else _output_dir(config) / f"{slugify(article.title)}.md"
    output.write_text(article.markdown, encoding="utf-8")
    write_json({"success": True, "title": article.title, "source_url": article.source_url, "author": article.author, "markdown_path": str(output), "digest": article.digest})
    return 0


def _handle_create(args, config) -> int:
    import json

    from .creation import (
        CreationSpec,
        WritingBrief,
        build_creation_prompt,
        build_outline_template,
        infer_brief_from_request,
        validate_article,
    )

    output_dir = Path(args.output_dir).resolve() if args.output_dir else _output_dir(config) / f"{slugify(args.title)}-creation"
    ensure_dir(output_dir)

    request_text = args.request
    if args.request_file:
        request_path = Path(args.request_file).resolve()
        if not request_path.exists():
            raise RuntimeError(f"需求文件不存在: {request_path}")
        request_text = request_path.read_text(encoding="utf-8").strip()

    source_summary = args.source_summary
    if args.source_file:
        source_path = Path(args.source_file).resolve()
        if not source_path.exists():
            raise RuntimeError(f"参考文件不存在: {source_path}")
        source_summary = source_path.read_text(encoding="utf-8")
        source_summary = source_summary[:4000].strip()

    inferred = infer_brief_from_request(args.title, request_text, tone=args.tone) if request_text else None
    mode = args.mode if args.mode != "title_to_article" or not inferred else inferred.mode
    angle = args.angle.strip() or (inferred.angle if inferred else "") or ("从一个更适合公众号传播的角度重写主题" if mode == "rewrite" else "找到一个清晰、有传播性的切口来展开")
    audience = args.audience.strip() or (inferred.audience if inferred else "") or "关注行业趋势的微信公众号读者"
    key_points = tuple(args.key_point) if args.key_point else (inferred.key_points if inferred else ())
    brief = WritingBrief(
        title=args.title,
        mode=mode,
        audience=audience,
        angle=angle,
        key_points=key_points,
        source_summary=source_summary,
        source_constraints=tuple(args.constraint),
        tone=args.tone,
    )
    spec = CreationSpec(mode=mode, tone=args.tone)

    prompt_text = build_creation_prompt(brief, spec)
    outline_text = build_outline_template(args.title, heading_count=args.heading_count)

    brief_path = output_dir / "brief.json"
    prompt_path = output_dir / "prompt.md"
    outline_path = output_dir / "outline.md"
    guide_path = output_dir / "guide.md"
    request_path = output_dir / "request.md"

    brief_payload = {
        "title": brief.title,
        "mode": brief.mode,
        "audience": brief.audience,
        "angle": brief.angle,
        "tone": brief.tone,
        "key_points": list(brief.key_points),
        "source_constraints": list(brief.source_constraints),
        "source_summary": brief.source_summary,
        "target_words_min": spec.target_words_min,
        "target_words_max": spec.target_words_max,
        "target_headings_min": spec.target_headings_min,
        "target_headings_max": spec.target_headings_max,
    }
    brief_path.write_text(json.dumps(brief_payload, ensure_ascii=False, indent=2), encoding="utf-8")
    prompt_path.write_text(prompt_text, encoding="utf-8")
    outline_path.write_text(outline_text, encoding="utf-8")
    if request_text:
        request_path.write_text(request_text, encoding="utf-8")
    guide_path.write_text(
        "\n".join(
            [
                "使用建议：",
                "0. 如果 request.md 存在，先读用户原始需求，再读 brief.json。",
                "1. 先阅读 prompt.md，把它交给 Skill 或模型生成初稿。",
                "2. 用 outline.md 检查结构是否完整。",
                "3. 写完后把最终 Markdown 传回 create --article-file 做质量检查。",
            ]
        ),
        encoding="utf-8",
    )

    result = {
        "success": True,
        "title": args.title,
        "mode": brief.mode,
        "audience": brief.audience,
        "angle": brief.angle,
        "brief_path": str(brief_path),
        "prompt_path": str(prompt_path),
        "outline_path": str(outline_path),
        "guide_path": str(guide_path),
    }
    if request_text:
        result["request_path"] = str(request_path)

    if args.article_file:
        article_path = Path(args.article_file).resolve()
        if not article_path.exists():
            raise RuntimeError(f"待检查文章不存在: {article_path}")
        article_markdown = article_path.read_text(encoding="utf-8")
        check = validate_article(article_markdown, spec)
        check_path = output_dir / "check.json"
        check_payload = {
            "passes": check.passes,
            "word_count": check.word_count,
            "heading_count": check.heading_count,
            "warnings": check.warnings,
        }
        check_path.write_text(json.dumps(check_payload, ensure_ascii=False, indent=2), encoding="utf-8")
        result["check_path"] = str(check_path)
        result["passes"] = check.passes
        result["word_count"] = check.word_count
        result["heading_count"] = check.heading_count
        result["warnings"] = check.warnings

    write_json(result)
    return 0


def _handle_cover(args, config) -> int:
    from .covers import generate_cover

    output = Path(args.output).resolve() if args.output else _output_dir(config) / f"{slugify(args.title)}-cover.jpg"
    path = generate_cover(
        config.image_generation,
        title=args.title,
        output_path=output,
        provider_name=args.provider,
        template_name=args.template,
        subtitle=args.subtitle,
    )
    write_json({"success": True, "cover_path": str(path), "provider": args.provider or config.image_generation.provider, "template": args.template})
    return 0


def _resolve_creation_paths(input_value: str) -> tuple[Path, Path]:
    path = Path(input_value).resolve()
    if not path.exists():
        raise RuntimeError(f"创作资产不存在: {path}")
    if path.is_dir():
        brief_path = path / "brief.json"
        base_dir = path
    else:
        brief_path = path
        base_dir = path.parent
    if not brief_path.exists():
        raise RuntimeError(f"未找到 brief.json: {brief_path}")
    return base_dir, brief_path


def _handle_write(args, config) -> int:
    import json

    from .creation import CreationSpec, WritingBrief, generate_article_markdown, validate_article

    base_dir, brief_path = _resolve_creation_paths(args.input)
    brief_payload = json.loads(brief_path.read_text(encoding="utf-8"))
    brief = WritingBrief(
        title=brief_payload["title"],
        mode=brief_payload["mode"],
        audience=brief_payload["audience"],
        angle=brief_payload["angle"],
        key_points=tuple(brief_payload.get("key_points") or []),
        source_summary=brief_payload.get("source_summary") or "",
        source_constraints=tuple(brief_payload.get("source_constraints") or []),
        tone=brief_payload.get("tone") or "professional",
    )
    spec = CreationSpec(
        mode=brief.mode,
        tone=brief.tone,
        target_words_min=int(brief_payload.get("target_words_min", 1200)),
        target_words_max=int(brief_payload.get("target_words_max", 1500)),
        target_headings_min=int(brief_payload.get("target_headings_min", 3)),
        target_headings_max=int(brief_payload.get("target_headings_max", 5)),
    )

    article_markdown = generate_article_markdown(brief, spec=spec, heading_count=args.heading_count)
    article_path = Path(args.output).resolve() if args.output else base_dir / "article.md"
    article_path.write_text(article_markdown, encoding="utf-8")

    check = validate_article(article_markdown, spec)
    check_path = base_dir / "generated_check.json"
    check_payload = {
        "passes": check.passes,
        "word_count": check.word_count,
        "heading_count": check.heading_count,
        "warnings": check.warnings,
    }
    check_path.write_text(json.dumps(check_payload, ensure_ascii=False, indent=2), encoding="utf-8")

    write_json(
        {
            "success": True,
            "title": brief.title,
            "article_path": str(article_path),
            "check_path": str(check_path),
            "passes": check.passes,
            "word_count": check.word_count,
            "heading_count": check.heading_count,
            "warnings": check.warnings,
        }
    )
    return 0


def _handle_workflow(args, config) -> int:
    import json

    from .creation import (
        CreationSpec,
        WritingBrief,
        build_creation_prompt,
        build_outline_template,
        generate_article_markdown,
        infer_brief_from_request,
        validate_article,
    )
    from .extractors import load_article
    from .renderer import optimize_for_wechat_html
    from .wechat_api import WeChatClient

    output_dir = Path(args.output_dir).resolve() if args.output_dir else _output_dir(config) / f"{slugify(args.title)}-workflow"
    ensure_dir(output_dir)

    request_text = args.request
    if args.request_file:
        input_request_path = Path(args.request_file).resolve()
        if not input_request_path.exists():
            raise RuntimeError(f"需求文件不存在: {input_request_path}")
        request_text = input_request_path.read_text(encoding="utf-8").strip()

    source_summary = args.source_summary
    source_url = args.source_url.strip()
    source_markdown_path = ""
    if args.source_file:
        source_path = Path(args.source_file).resolve()
        if not source_path.exists():
            raise RuntimeError(f"参考文件不存在: {source_path}")
        source_summary = source_path.read_text(encoding="utf-8")[:4000].strip()
        source_markdown_path = str(source_path)
    elif source_url:
        source_article = load_article(source_url, timeout=args.timeout)
        source_summary = source_article.markdown[:4000].strip()
        extracted_source_path = output_dir / "source.md"
        extracted_source_path.write_text(source_article.markdown, encoding="utf-8")
        source_markdown_path = str(extracted_source_path)

    inferred = infer_brief_from_request(args.title, request_text, tone=args.tone) if request_text else None
    mode = args.mode
    if mode == "title_to_article" and (source_summary or source_markdown_path):
        mode = "rewrite"
    if mode == "title_to_article" and inferred and inferred.mode == "rewrite":
        mode = inferred.mode

    angle = args.angle.strip() or (inferred.angle if inferred else "") or ("从一个更适合公众号传播的角度重写主题" if mode == "rewrite" else "找到一个清晰、有传播性的切口来展开")
    audience = args.audience.strip() or (inferred.audience if inferred else "") or "关注行业趋势的微信公众号读者"
    key_points = tuple(args.key_point) if args.key_point else (inferred.key_points if inferred else ())
    brief = WritingBrief(
        title=args.title,
        mode=mode,
        audience=audience,
        angle=angle,
        key_points=key_points,
        source_summary=source_summary,
        source_constraints=tuple(args.constraint),
        tone=args.tone,
    )
    spec = CreationSpec(mode=mode, tone=args.tone)

    brief_path = output_dir / "brief.json"
    prompt_path = output_dir / "prompt.md"
    outline_path = output_dir / "outline.md"
    guide_path = output_dir / "guide.md"
    request_path = output_dir / "request.md"
    article_path = output_dir / "article.md"
    check_path = output_dir / "generated_check.json"

    brief_payload = {
        "title": brief.title,
        "mode": brief.mode,
        "audience": brief.audience,
        "angle": brief.angle,
        "tone": brief.tone,
        "key_points": list(brief.key_points),
        "source_constraints": list(brief.source_constraints),
        "source_summary": brief.source_summary,
        "target_words_min": spec.target_words_min,
        "target_words_max": spec.target_words_max,
        "target_headings_min": spec.target_headings_min,
        "target_headings_max": spec.target_headings_max,
    }
    brief_path.write_text(json.dumps(brief_payload, ensure_ascii=False, indent=2), encoding="utf-8")
    prompt_path.write_text(build_creation_prompt(brief, spec), encoding="utf-8")
    outline_path.write_text(build_outline_template(args.title, heading_count=args.heading_count), encoding="utf-8")
    if request_text:
        request_path.write_text(request_text, encoding="utf-8")
    guide_path.write_text(
        "\n".join(
            [
                "workflow 已自动完成：",
                "1. 生成 brief / prompt / outline",
                "2. 生成 article.md",
                "3. 执行结构与字数检查",
                "4. 生成预览并按需创建草稿",
            ]
        ),
        encoding="utf-8",
    )

    article_markdown = generate_article_markdown(brief, spec=spec, heading_count=args.heading_count)
    article_path.write_text(article_markdown, encoding="utf-8")

    generated_check = validate_article(article_markdown, spec)
    generated_check_payload = {
        "passes": generated_check.passes,
        "word_count": generated_check.word_count,
        "heading_count": generated_check.heading_count,
        "warnings": generated_check.warnings,
    }
    check_path.write_text(json.dumps(generated_check_payload, ensure_ascii=False, indent=2), encoding="utf-8")

    article = load_article(str(article_path), timeout=args.timeout)
    if source_url:
        article.source_url = source_url
    article.html = optimize_for_wechat_html(
        article.html,
        template=(args.template or config.wechat.default_template or "standard").strip().lower(),
    )
    preview_path = output_dir / f"{slugify(article.title)}-wechat-preview.html"
    preview_path.write_text(article.html, encoding="utf-8")

    result = {
        "success": True,
        "title": article.title,
        "mode": brief.mode,
        "audience": brief.audience,
        "angle": brief.angle,
        "brief_path": str(brief_path),
        "prompt_path": str(prompt_path),
        "outline_path": str(outline_path),
        "guide_path": str(guide_path),
        "article_path": str(article_path),
        "check_path": str(check_path),
        "preview_html": str(preview_path),
        "passes": generated_check.passes,
        "word_count": generated_check.word_count,
        "heading_count": generated_check.heading_count,
        "warnings": generated_check.warnings,
    }
    if request_text:
        result["request_path"] = str(request_path)
    if source_markdown_path:
        result["source_markdown_path"] = source_markdown_path

    if args.dry_run:
        result["mode_detail"] = "workflow-dry-run"
        write_json(result)
        return 0

    client = WeChatClient(config.wechat, timeout=args.timeout)
    token = client.get_token()
    if args.cover_image:
        local_path = Path(args.cover_image).resolve()
        if not local_path.exists():
            raise RuntimeError(f"封面文件不存在: {local_path}")
        upload = client.upload_material(token, local_path, material_type="image")
        thumb_media_id = upload["media_id"]
        cover_path = str(local_path)
    else:
        from .covers import generate_cover

        generated_cover_path = output_dir / f"{slugify(article.title)}-cover.jpg"
        cover_file = generate_cover(
            config.image_generation,
            title=article.title,
            output_path=generated_cover_path,
            provider_name=args.cover_provider,
            template_name=args.cover_template,
            subtitle=args.cover_subtitle,
        )
        upload = client.upload_material(token, cover_file, material_type="image")
        thumb_media_id = upload["media_id"]
        cover_path = str(cover_file)

    media_id = client.create_draft(
        token=token,
        title=article.title,
        author=args.author or config.wechat.author,
        digest=article.digest,
        content_html=article.html,
        source_url=article.source_url,
        thumb_media_id=thumb_media_id,
    )
    result["cover_path"] = cover_path
    result["draft_media_id"] = media_id

    if args.publish:
        publish_id = client.submit_publish(token, media_id)
        result["publish_id"] = publish_id
        if args.status:
            result["status"] = client.get_publish_status(token, publish_id)

    write_json(result)
    return 0


def _ensure_cover(client: WeChatClient, token: str, args, config, article) -> tuple[str, str]:
    from .covers import generate_cover

    if args.cover_image:
        local_path = Path(args.cover_image).resolve()
        if not local_path.exists():
            raise RuntimeError(f"封面文件不存在: {local_path}")
        upload = client.upload_material(token, local_path, material_type="image")
        return upload["media_id"], str(local_path)

    generated_path = _output_dir(config) / f"{slugify(article.title)}-cover.jpg"
    path = generate_cover(
        config.image_generation,
        title=article.title,
        output_path=generated_path,
        provider_name=args.cover_provider,
        template_name=args.cover_template,
        subtitle=args.cover_subtitle,
    )
    upload = client.upload_material(token, path, material_type="image")
    return upload["media_id"], str(path)


def _handle_material(args, config) -> int:
    from .wechat_api import WeChatClient

    file_path = Path(args.file).resolve()
    if not file_path.exists():
        raise RuntimeError(f"素材文件不存在: {file_path}")
    client = WeChatClient(config.wechat, timeout=args.timeout)
    token = client.get_token()
    result = client.upload_material(token, file_path, material_type=args.type)
    result["success"] = True
    result["file"] = str(file_path)
    write_json(result)
    return 0


def _handle_draft(args, config) -> int:
    from .extractors import load_article
    from .renderer import optimize_for_wechat_html
    from .wechat_api import WeChatClient

    article = load_article(args.input, timeout=args.timeout)
    if args.source_url:
        article.source_url = args.source_url
    template = (args.template or config.wechat.default_template or "standard").strip().lower()
    article.html = optimize_for_wechat_html(article.html, template=template)

    output_dir = _output_dir(config)
    preview_path = output_dir / f"{slugify(article.title)}-wechat-preview.html"
    markdown_path = output_dir / f"{slugify(article.title)}.md"
    preview_path.write_text(article.html, encoding="utf-8")
    markdown_path.write_text(article.markdown, encoding="utf-8")

    if args.dry_run:
        write_json(
            {
                "success": True,
                "mode": "dry-run",
                "title": article.title,
                "author": args.author or article.author or config.wechat.author,
                "digest": article.digest,
                "template": template,
                "markdown_path": str(markdown_path),
                "preview_html": str(preview_path),
            }
        )
        return 0

    client = WeChatClient(config.wechat, timeout=args.timeout)
    token = client.get_token()
    thumb_media_id, cover_path = _ensure_cover(client, token, args, config, article)
    media_id = client.create_draft(
        token=token,
        title=article.title,
        author=args.author or article.author or config.wechat.author,
        digest=article.digest,
        content_html=article.html,
        source_url=article.source_url,
        thumb_media_id=thumb_media_id,
    )

    result = {
        "success": True,
        "title": article.title,
        "template": template,
        "draft_media_id": media_id,
        "preview_html": str(preview_path),
        "markdown_path": str(markdown_path),
        "cover_path": cover_path,
    }
    if args.publish:
        publish_id = client.submit_publish(token, media_id)
        result["publish_id"] = publish_id
        if args.status:
            result["status"] = client.get_publish_status(token, publish_id)
    write_json(result)
    return 0


def _handle_publish(args, config) -> int:
    from .wechat_api import WeChatClient

    client = WeChatClient(config.wechat, timeout=args.timeout)
    token = client.get_token()
    publish_id = client.submit_publish(token, args.media_id)
    result = {"success": True, "media_id": args.media_id, "publish_id": publish_id}
    if args.status:
        result["status"] = client.get_publish_status(token, publish_id)
    write_json(result)
    return 0


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        if args.command == "install":
            return _install_dependencies(args.upgrade)

        config = load_config(Path(args.config).resolve())

        if args.command == "extract":
            return _handle_extract(args, config)
        if args.command == "create":
            return _handle_create(args, config)
        if args.command == "write":
            return _handle_write(args, config)
        if args.command == "workflow":
            return _handle_workflow(args, config)
        if args.command == "cover":
            return _handle_cover(args, config)
        if args.command == "material":
            return _handle_material(args, config)
        if args.command == "draft":
            return _handle_draft(args, config)
        if args.command == "publish":
            return _handle_publish(args, config)
        raise RuntimeError(f"未知命令: {args.command}")
    except ModuleNotFoundError as exc:
        write_json(
            {
                "success": False,
                "error": f"缺少运行依赖: {exc}. 请先执行 `python scripts/publish_wechat.py install`",
                "type": type(exc).__name__,
            }
        )
        return 1
    except Exception as exc:
        write_json({"success": False, "error": str(exc), "type": type(exc).__name__})
        return 1
