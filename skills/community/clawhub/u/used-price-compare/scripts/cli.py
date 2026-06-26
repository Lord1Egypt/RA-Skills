"""Used Price Compare CLI — multi-platform price comparison via bb-browser.

Output: JSON (ensure_ascii=False)
Exit codes: 0=success, 2=error
"""

from __future__ import annotations

import argparse
import json
import logging
import sys

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger("used-price-compare")


def _output(data: dict, exit_code: int = 0) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))
    sys.exit(exit_code)


def cmd_compare(args: argparse.Namespace) -> None:
    """Compare prices across platforms."""
    from used_price_compare.compare import compare_prices, format_comparison_table

    platforms = args.platforms.split(",") if args.platforms else None

    result = compare_prices(
        keyword=args.keyword,
        city=args.city,
        country=args.country,
        platforms=platforms,
        top_n=args.top,
    )

    output = format_comparison_table(result)
    _output(output)


def cmd_platforms(args: argparse.Namespace) -> None:
    """List available platforms."""
    from used_price_compare.platforms import PLATFORMS

    platforms = []
    for name, plat in PLATFORMS.items():
        platforms.append({
            "name": name,
            "display_name": plat.display_name,
            "adapter": plat.adapter,
            "domain": plat.domain,
            "enabled": plat.enabled,
        })

    _output({"success": True, "platforms": platforms})


def cmd_fetch_detail(args: argparse.Namespace) -> None:
    """Fetch detail page for a single item URL."""
    from used_price_compare.fetcher import fetch_detail
    from dataclasses import asdict

    item = fetch_detail(args.url)
    _output({"success": True, **asdict(item)})


def _build_vision_cfg(args: argparse.Namespace):
    """Build VisionConfig from CLI args, falling back to config file / env."""
    from used_price_compare.evaluator import load_vision_config

    model = getattr(args, "vision_model", None)
    # Always load config; model_override=None means "use config file value"
    return load_vision_config(model_override=model)


def cmd_evaluate(args: argparse.Namespace) -> None:
    """Fetch and evaluate one or more item URLs."""
    from used_price_compare.fetcher import fetch_details
    from used_price_compare.evaluator import evaluate_items, format_eval_results
    from used_price_compare.models import ItemDetail

    urls = [u.strip() for u in args.urls.split(",") if u.strip()]
    if not urls:
        _output({"success": False, "error": "No URLs provided"}, exit_code=2)

    raw_results = fetch_details(urls)
    items: list[ItemDetail] = []
    errors: list[dict] = []
    for r in raw_results:
        if isinstance(r, ItemDetail):
            items.append(r)
        else:
            errors.append(r)

    if not items:
        _output({"success": False, "error": "All fetches failed", "details": errors}, exit_code=2)

    vision_cfg = _build_vision_cfg(args)
    eval_results = evaluate_items(items, vision_cfg=vision_cfg)
    output = format_eval_results(eval_results)
    if errors:
        output["fetch_errors"] = errors
    _output(output)


def cmd_summarize(args: argparse.Namespace) -> None:
    """Full pipeline: fetch all items, evaluate, and produce comparative summary."""
    from used_price_compare.fetcher import fetch_details
    from used_price_compare.evaluator import evaluate_items, format_eval_results
    from used_price_compare.models import ItemDetail

    urls = [u.strip() for u in args.urls.split(",") if u.strip()]
    if not urls:
        _output({"success": False, "error": "No URLs provided"}, exit_code=2)

    raw_results = fetch_details(urls)
    items: list[ItemDetail] = []
    errors: list[dict] = []
    for r in raw_results:
        if isinstance(r, ItemDetail):
            items.append(r)
        else:
            errors.append(r)

    if not items:
        _output({"success": False, "error": "All fetches failed", "details": errors}, exit_code=2)

    vision_cfg = _build_vision_cfg(args)
    eval_results = evaluate_items(items, vision_cfg=vision_cfg)
    output = format_eval_results(eval_results)

    # Add summary section
    best = eval_results[0] if eval_results else None
    summary_parts = [f"共评估 {len(eval_results)} 件商品"]
    if best:
        summary_parts.append(
            f"最佳推荐: {best.item.title[:50]} ({best.item.price}, {best.item.platform}) "
            f"— {best.verdict_label}, 综合 {best.scores.overall}/10"
        )
    recommended = [r for r in eval_results if r.verdict in ("highly_recommended", "recommended")]
    caution = [r for r in eval_results if r.verdict == "caution"]
    avoid = [r for r in eval_results if r.verdict == "avoid"]
    summary_parts.append(
        f"推荐 {len(recommended)} 件, 谨慎 {len(caution)} 件, 不建议 {len(avoid)} 件"
    )

    output["summary"] = "。".join(summary_parts) + "。"
    if errors:
        output["fetch_errors"] = errors
    _output(output)


def cmd_vision_config(args: argparse.Namespace) -> None:
    """Show or initialize vision model configuration."""
    from used_price_compare.evaluator import load_vision_config, _CONFIG_SEARCH_PATHS
    from dataclasses import asdict
    from pathlib import Path

    action = getattr(args, "action", "show")

    if action == "init":
        target = _CONFIG_SEARCH_PATHS[0]
        if target.exists() and not getattr(args, "force", False):
            _output({
                "success": False,
                "error": f"Config already exists at {target}. Use --force to overwrite.",
            }, exit_code=2)

        template = {
            "model": "qwen-vl-max",
            "api_base": "https://dashscope.aliyuncs.com/compatible-mode/v1",
            "api_key": "",
            "max_images": 5,
            "timeout": 60,
        }
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(template, indent=2, ensure_ascii=False) + "\n",
                          encoding="utf-8")
        _output({
            "success": True,
            "message": f"Config written to {target}. Edit api_key before use.",
            "path": str(target),
        })
    else:
        cfg = load_vision_config()
        safe = asdict(cfg)
        safe["api_key"] = ("***" + safe["api_key"][-4:]) if len(safe["api_key"]) > 4 else "(unset)"
        safe["enabled"] = cfg.enabled

        config_path = None
        for p in _CONFIG_SEARCH_PATHS:
            if p.is_file():
                config_path = str(p)
                break

        _output({
            "success": True,
            "config_file": config_path,
            "resolved": safe,
        })


def cmd_install(args: argparse.Namespace) -> None:
    """Install bb-browser adapters to ~/.bb-browser/sites/.

    Walks all subdirectories under adapters/, copying *.js files
    (excluding _template files and build scripts) to ~/.bb-browser/sites/.
    """
    import shutil
    from pathlib import Path

    adapter_dir = Path(__file__).resolve().parent.parent / "adapters"
    installed = []

    for sub_dir in sorted(adapter_dir.iterdir()):
        if not sub_dir.is_dir():
            continue

        target_dir = Path.home() / ".bb-browser" / "sites" / sub_dir.name
        target_dir.mkdir(parents=True, exist_ok=True)

        for js_file in sorted(sub_dir.glob("*.js")):
            if js_file.name.startswith("_") or js_file.name == "build.js":
                continue
            target = target_dir / js_file.name
            shutil.copy2(js_file, target)
            installed.append(f"{sub_dir.name}/{js_file.name}")

    _output({"success": True, "installed": installed, "message": f"Installed {len(installed)} adapter(s)"})


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="used-price-compare",
        description="Multi-platform second-hand price comparison (via bb-browser)",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # compare
    sub = subparsers.add_parser("compare", help="Compare prices across platforms")
    sub.add_argument("--keyword", required=True, help="Product to search for")
    sub.add_argument("--city", default="los-angeles", help="City (default: los-angeles)")
    sub.add_argument("--country", default=None, help="Country code (default: auto-detect from city)")
    sub.add_argument("--platforms", default="", help="Comma-separated platform names (default: all)")
    sub.add_argument("--top", type=int, default=5, help="Top N cheapest per platform (default: 5)")
    sub.set_defaults(func=cmd_compare)

    # fetch-detail
    sub = subparsers.add_parser("fetch-detail", help="Fetch detail page for a single item URL")
    sub.add_argument("--url", required=True, help="Item listing URL")
    sub.set_defaults(func=cmd_fetch_detail)

    # evaluate
    sub = subparsers.add_parser("evaluate", help="Fetch and evaluate item URLs")
    sub.add_argument("--urls", required=True, help="Comma-separated item URLs")
    sub.add_argument("--vision-model", default=None,
                     help="Vision model name for image analysis (e.g. qwen-vl-max). "
                          "Requires VISION_API_BASE and VISION_API_KEY env vars")
    sub.set_defaults(func=cmd_evaluate)

    # summarize
    sub = subparsers.add_parser("summarize", help="Full evaluation pipeline with comparative summary")
    sub.add_argument("--urls", required=True, help="Comma-separated item URLs")
    sub.add_argument("--vision-model", default=None,
                     help="Vision model name for image analysis (e.g. qwen-vl-max). "
                          "Requires VISION_API_BASE and VISION_API_KEY env vars")
    sub.set_defaults(func=cmd_summarize)

    # vision-config
    sub = subparsers.add_parser("vision-config",
                                help="Show or initialize vision model configuration")
    sub.add_argument("action", nargs="?", default="show", choices=["show", "init"],
                     help="'show' (default) displays resolved config; "
                          "'init' creates a template config file")
    sub.add_argument("--force", action="store_true",
                     help="Overwrite existing config file (for 'init')")
    sub.set_defaults(func=cmd_vision_config)

    # platforms
    sub = subparsers.add_parser("platforms", help="List available platforms")
    sub.set_defaults(func=cmd_platforms)

    # install
    sub = subparsers.add_parser("install", help="Install bb-browser adapters")
    sub.set_defaults(func=cmd_install)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    try:
        args.func(args)
    except Exception as e:
        logger.error("Failed: %s", e, exc_info=True)
        _output({"success": False, "error": str(e)}, exit_code=2)


if __name__ == "__main__":
    main()
