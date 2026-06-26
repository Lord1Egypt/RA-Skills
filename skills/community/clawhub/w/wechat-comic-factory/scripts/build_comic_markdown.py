from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from common import SkillError, ensure_directory, normalize_display_text, read_json_file, setup_logger  # noqa: E402


def build_comic_markdown(manifest_path: str | Path, output_dir: str | Path) -> dict:
    output_dir = ensure_directory(output_dir)
    logger = setup_logger("wechat_comic_factory", output_dir)
    manifest = read_json_file(manifest_path)

    title = normalize_display_text(manifest.get("title", ""))
    intro = normalize_display_text(manifest.get("intro", ""))
    ending = normalize_display_text(manifest.get("ending", ""))
    images = manifest.get("images", [])
    if not title or not images:
        raise SkillError("build_markdown", "manifest.json 缺少 title 或 images")

    lines = [f"# {title}", ""]
    if intro:
        lines.extend([intro, ""])

    for image in images:
        caption = normalize_display_text(image.get("caption", ""))
        image_path = str(image.get("image_path", "")).strip()
        if not image_path:
            raise SkillError("build_markdown", "manifest 中存在缺少 image_path 的图片项", details=image)
        lines.extend(
            [
                f"![{caption}]({image_path})",
                "",
            ]
        )
        if caption:
            lines.extend([caption, ""])

    if ending:
        lines.extend([ending, ""])

    markdown_content = "\n".join(lines).strip() + "\n"
    md_path = Path(output_dir) / "article.md"
    md_path.write_text(markdown_content, encoding="utf-8")
    logger.info("Markdown 文章已生成，md_path=%s", md_path)
    return {
        "success": True,
        "stage": "build_comic_markdown",
        "title": title,
        "md_path": str(md_path),
        "output_dir": str(output_dir),
    }


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="根据 manifest.json 构建 Markdown 文章")
    parser.add_argument("--manifest_path", required=True, help="manifest.json 路径")
    parser.add_argument("--output_dir", required=True, help="输出目录")
    return parser


def main() -> None:
    parser = build_arg_parser()
    args = parser.parse_args()
    try:
        result = build_comic_markdown(args.manifest_path, args.output_dir)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except SkillError as exc:
        print(json.dumps({"success": False, **exc.to_dict()}, ensure_ascii=False, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
