from __future__ import annotations

import argparse
import json
import sys
import traceback
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from build_comic_markdown import build_comic_markdown  # noqa: E402
from common import (  # noqa: E402
    SkillError,
    build_task_result,
    create_task_output_dir,
    ensure_publishable_task_files,
    load_config,
    load_latest_task,
    read_json_file,
    load_task_result,
    now_iso,
    save_task_result,
    setup_logger,
)
from compress_image import compress_image_assets  # noqa: E402
from format_article import format_article  # noqa: E402
from generate_comic_images import generate_comic_images  # noqa: E402
from plan_comics import plan_comics  # noqa: E402
from publish_draft import publish_draft  # noqa: E402


def error_text(exc: SkillError) -> str:
    if exc.hint:
        return f"{exc.message} ({exc.hint})"
    return exc.message


def build_paths(output_dir: Path) -> dict[str, str]:
    return {
        "plan_path": str((output_dir / "plan.json").resolve()),
        "manifest_path": str((output_dir / "manifest.json").resolve()),
        "md_path": str((output_dir / "article.md").resolve()),
        "assets_path": str((output_dir / "publish_assets.json").resolve()),
        "html_path": str((output_dir / "final.html").resolve()),
    }


def resolve_publish_target(
    *,
    publish_latest: bool,
    publish_output_dir: str | None,
) -> tuple[dict, Path, bool]:
    if publish_output_dir:
        payload = load_task_result(publish_output_dir)
    elif publish_latest:
        payload = load_latest_task()
    else:
        raise SkillError("input", "未提供发布目标")

    payload = ensure_publishable_task_files(payload)
    output_dir = Path(str(payload["output_dir"])).resolve()
    draft_status = str(payload.get("draft_status", "not_started")).strip().lower()
    if draft_status == "success":
        return payload, output_dir, True
    if draft_status not in {"pending", "failed"}:
        raise SkillError(
            "task_state",
            "最近任务不是待发布状态",
            hint="请先生成待发布内容，或指定另一个任务目录执行发布。",
            details={"draft_status": payload.get("draft_status"), "stage": payload.get("stage")},
        )
    return payload, output_dir, False


def publish_existing_task(*, publish_latest: bool = False, publish_output_dir: str | None = None) -> dict:
    task_payload, output_dir, already_published = resolve_publish_target(
        publish_latest=publish_latest,
        publish_output_dir=publish_output_dir,
    )
    logger = setup_logger("wechat_comic_factory", output_dir)

    if already_published:
        result = build_task_result(
            success=True,
            comic_type=str(task_payload.get("comic_type", "")),
            topic=str(task_payload.get("topic", "")),
            count=task_payload.get("count"),
            title=str(task_payload.get("title", "")),
            output_dir=output_dir,
            stage="completed",
            draft_status="success",
            draft_id=task_payload.get("draft_id"),
            created_at=str(task_payload.get("created_at") or now_iso()),
            extra={
                **build_paths(output_dir),
                "message": "最近任务已发布成功，无需重复发布。",
            },
        )
        save_task_result(output_dir, result, update_latest=True)
        logger.info("最近任务已发布，无需重复发布 output_dir=%s", output_dir)
        return result

    created_at = str(task_payload.get("created_at") or now_iso())
    logger.info("开始发布已有任务到微信公众号草稿箱 output_dir=%s", output_dir)
    try:
        assets_payload = read_json_file(task_payload["assets_path"])
        if not assets_payload.get("article_images_uploaded"):
            logger.info("检测到正文图片尚未上传，先补执行 format_article 上传正文图")
            format_article(
                task_payload["md_path"],
                task_payload["assets_path"],
                output_dir,
                upload_to_wechat=True,
            )
        publish_result = publish_draft(
            task_payload["html_path"],
            task_payload["assets_path"],
            output_dir,
        )
    except SkillError as exc:
        result = build_task_result(
            success=False,
            comic_type=str(task_payload.get("comic_type", "")),
            topic=str(task_payload.get("topic", "")),
            count=task_payload.get("count"),
            title=str(task_payload.get("title", "")),
            output_dir=output_dir,
            stage="publish_failed",
            draft_status="failed",
            draft_id=task_payload.get("draft_id"),
            created_at=created_at,
            error=error_text(exc),
            extra={
                **build_paths(output_dir),
                "error_details": exc.to_dict(),
            },
        )
        save_task_result(output_dir, result, update_latest=True)
        raise SkillError("publish_failed", result["error"], details=result) from exc

    result = build_task_result(
        success=True,
        comic_type=str(task_payload.get("comic_type", "")),
        topic=str(task_payload.get("topic", "")),
        count=task_payload.get("count"),
        title=str(task_payload.get("title", "")),
        output_dir=output_dir,
        stage="completed",
        draft_status="success",
        draft_id=publish_result.get("draft_id"),
        created_at=created_at,
        extra={
            **build_paths(output_dir),
            "publish_result_path": publish_result.get("publish_result_path"),
            "raw_publish_response": publish_result.get("raw_response"),
        },
    )
    save_task_result(output_dir, result, update_latest=True)
    logger.info("已有任务发布成功 output_dir=%s draft_id=%s", output_dir, result["draft_id"])
    return result


def run_pipeline(comic_type: str, topic: str, count: int | None = None, *, skip_publish: bool = False) -> dict:
    base_config = load_config(required_paths=["defaults.output_dir"])
    defaults = base_config.get("defaults", {})
    final_count = int(count or defaults.get("default_count", 3))
    output_dir = create_task_output_dir(comic_type, defaults.get("output_dir")).resolve()
    created_at = now_iso()
    logger = setup_logger("wechat_comic_factory", output_dir)
    logger.info(
        "开始执行完整流水线 comic_type=%s topic=%s count=%s skip_publish=%s",
        comic_type,
        topic,
        final_count,
        skip_publish,
    )

    paths = build_paths(output_dir)
    title = ""

    try:
        plan_result = plan_comics(comic_type, topic, final_count, output_dir)
        title = str(plan_result.get("title", "")).strip()
    except SkillError as exc:
        result = build_task_result(
            success=False,
            comic_type=comic_type,
            topic=topic,
            count=final_count,
            title=title,
            output_dir=output_dir,
            stage="planning_failed",
            draft_status="not_started",
            created_at=created_at,
            error=error_text(exc),
            extra={"error_details": exc.to_dict()},
        )
        save_task_result(output_dir, result, update_latest=False)
        raise SkillError("planning_failed", result["error"], details=result) from exc

    try:
        generate_comic_images(output_dir / "plan.json", output_dir)
    except SkillError as exc:
        result = build_task_result(
            success=False,
            comic_type=plan_result["comic_type"],
            topic=topic,
            count=final_count,
            title=title,
            output_dir=output_dir,
            stage="image_generation_failed",
            draft_status="not_started",
            created_at=created_at,
            error=error_text(exc),
            extra={**paths, "error_details": exc.to_dict()},
        )
        save_task_result(output_dir, result, update_latest=False)
        raise SkillError("image_generation_failed", result["error"], details=result) from exc

    try:
        build_comic_markdown(output_dir / "manifest.json", output_dir)
    except SkillError as exc:
        result = build_task_result(
            success=False,
            comic_type=plan_result["comic_type"],
            topic=topic,
            count=final_count,
            title=title,
            output_dir=output_dir,
            stage="markdown_failed",
            draft_status="not_started",
            created_at=created_at,
            error=error_text(exc),
            extra={**paths, "error_details": exc.to_dict()},
        )
        save_task_result(output_dir, result, update_latest=False)
        raise SkillError("markdown_failed", result["error"], details=result) from exc

    try:
        compress_image_assets(output_dir / "manifest.json", output_dir)
    except SkillError as exc:
        result = build_task_result(
            success=False,
            comic_type=plan_result["comic_type"],
            topic=topic,
            count=final_count,
            title=title,
            output_dir=output_dir,
            stage="compression_failed",
            draft_status="not_started",
            created_at=created_at,
            error=error_text(exc),
            extra={**paths, "error_details": exc.to_dict()},
        )
        save_task_result(output_dir, result, update_latest=False)
        raise SkillError("compression_failed", result["error"], details=result) from exc

    try:
        format_article(
            output_dir / "article.md",
            output_dir / "publish_assets.json",
            output_dir,
            upload_to_wechat=not skip_publish,
        )
    except SkillError as exc:
        result = build_task_result(
            success=False,
            comic_type=plan_result["comic_type"],
            topic=topic,
            count=final_count,
            title=title,
            output_dir=output_dir,
            stage="html_failed",
            draft_status="failed" if not skip_publish else "not_started",
            created_at=created_at,
            error=error_text(exc),
            extra={**paths, "error_details": exc.to_dict()},
        )
        save_task_result(output_dir, result, update_latest=False)
        raise SkillError("html_failed", result["error"], details=result) from exc

    if skip_publish:
        result = build_task_result(
            success=True,
            comic_type=plan_result["comic_type"],
            topic=topic,
            count=final_count,
            title=title,
            output_dir=output_dir,
            stage="completed",
            draft_status="pending",
            draft_id=None,
            created_at=created_at,
            extra=paths,
        )
        save_task_result(output_dir, result, update_latest=True)
        logger.info("流水线执行完成，生成待发布内容 output_dir=%s", output_dir)
        return result

    try:
        publish_result = publish_draft(
            output_dir / "final.html",
            output_dir / "publish_assets.json",
            output_dir,
        )
    except SkillError as exc:
        result = build_task_result(
            success=False,
            comic_type=plan_result["comic_type"],
            topic=topic,
            count=final_count,
            title=title,
            output_dir=output_dir,
            stage="publish_failed",
            draft_status="failed",
            created_at=created_at,
            error=error_text(exc),
            extra={**paths, "error_details": exc.to_dict()},
        )
        save_task_result(output_dir, result, update_latest=True)
        raise SkillError("publish_failed", result["error"], details=result) from exc

    result = build_task_result(
        success=True,
        comic_type=plan_result["comic_type"],
        topic=topic,
        count=final_count,
        title=title,
        output_dir=output_dir,
        stage="completed",
        draft_status="success",
        draft_id=publish_result.get("draft_id"),
        created_at=created_at,
        extra={
            **paths,
            "publish_result_path": publish_result.get("publish_result_path"),
            "raw_publish_response": publish_result.get("raw_response"),
        },
    )
    save_task_result(output_dir, result, update_latest=True)
    logger.info("流水线执行完成并成功发布 output_dir=%s draft_id=%s", output_dir, result["draft_id"])
    return result


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="微信公众号漫画工厂统一入口")
    parser.add_argument("--comic_type", help="漫画类型")
    parser.add_argument("--topic", help="漫画主题")
    parser.add_argument("--count", type=int, default=None, help="漫画张数，不传时默认读取配置")
    parser.add_argument("--skip_publish", action="store_true", help="跳过微信正文图上传和草稿发布")
    parser.add_argument("--publish_latest", action="store_true", help="发布最近一次待发布任务到微信公众号草稿箱")
    parser.add_argument("--publish_output_dir", help="发布指定任务目录中的已生成内容")
    return parser


def validate_args(args: argparse.Namespace) -> None:
    publish_mode = bool(args.publish_latest or args.publish_output_dir)
    generate_mode = bool(args.comic_type or args.topic)
    if publish_mode and generate_mode:
        raise SkillError("input", "发布模式与生成模式不能同时使用")
    if args.publish_latest and args.publish_output_dir:
        raise SkillError("input", "--publish_latest 与 --publish_output_dir 不能同时使用")
    if publish_mode:
        if args.count is not None:
            raise SkillError("input", "发布已有任务时不需要传入 --count")
        if args.skip_publish:
            raise SkillError("input", "发布已有任务时不能同时传入 --skip_publish")
        return
    if not args.comic_type or not args.topic:
        raise SkillError("input", "生成模式必须同时提供 --comic_type 与 --topic")


def main() -> None:
    parser = build_arg_parser()
    args = parser.parse_args()
    try:
        validate_args(args)
        if args.publish_latest or args.publish_output_dir:
            result = publish_existing_task(
                publish_latest=args.publish_latest,
                publish_output_dir=args.publish_output_dir,
            )
        else:
            result = run_pipeline(
                comic_type=args.comic_type,
                topic=args.topic,
                count=args.count,
                skip_publish=args.skip_publish,
            )
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except SkillError as exc:
        if isinstance(exc.details, dict) and "success" in exc.details and "stage" in exc.details:
            print(json.dumps(exc.details, ensure_ascii=False, indent=2))
        else:
            print(json.dumps({"success": False, **exc.to_dict()}, ensure_ascii=False, indent=2))
        sys.exit(1)
    except Exception as exc:  # pragma: no cover
        print(
            json.dumps(
                {
                    "success": False,
                    "stage": "unexpected",
                    "message": str(exc),
                    "details": traceback.format_exc(),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
