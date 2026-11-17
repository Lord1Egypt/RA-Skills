"""命令行入口：将 Agent 整理的 review-input JSON 渲染为 Markdown，并可选生成辅助图表."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from charts import write_charts
from report import ReportBuilder


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="周度复盘渲染器：review-input JSON → Markdown（可生成辅助图表 SVG）"
    )
    parser.add_argument(
        "--input",
        "-i",
        required=True,
        help="review-input JSON 路径（见 schema/review-input.example.json）",
    )
    parser.add_argument("--output", "-o", help="输出 markdown 文件路径")
    parser.add_argument(
        "--charts-dir",
        help="辅助图表输出目录；不传且指定了 -o 时，默认写到报告同目录",
    )
    parser.add_argument(
        "--no-charts",
        action="store_true",
        help="不生成/不嵌入辅助图表",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="原样输出校验后的 JSON（不做 Markdown 渲染）",
    )
    args = parser.parse_args(argv)

    path = Path(args.input).expanduser()
    if not path.exists():
        print(f"输入文件不存在: {path}", file=sys.stderr)
        return 1

    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        print("review-input 必须是 JSON 对象", file=sys.stderr)
        return 1
    if not (data.get("period") or {}).get("start"):
        print("缺少 period.start", file=sys.stderr)
        return 1

    # 始终按定稿样式生成 SVG（横向时间分布 + 双栏归因/Token）
    if not args.no_charts and not args.json:
        charts_dir: Path | None = None
        if args.charts_dir:
            charts_dir = Path(args.charts_dir).expanduser()
        elif args.output:
            charts_dir = Path(args.output).expanduser().resolve().parent
        if charts_dir is not None:
            names = write_charts(data, charts_dir)
            dash = data.setdefault("dashboard", {})
            if args.output:
                out_parent = Path(args.output).expanduser().resolve().parent
                rels = []
                for n in names:
                    full = (charts_dir / n).resolve()
                    try:
                        rels.append(str(full.relative_to(out_parent)).replace("\\", "/"))
                    except ValueError:
                        rels.append(str(full).replace("\\", "/"))
                dash["charts"] = rels
            else:
                dash["charts"] = names


    if args.json:
        text = json.dumps(data, ensure_ascii=False, indent=2)
    else:
        text = ReportBuilder(data).build()

    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(text, encoding="utf-8")
        try:
            print(f"报告已保存：{args.output}")
        except UnicodeEncodeError:
            print(f"Saved: {args.output}")
    else:
        try:
            print(text)
        except UnicodeEncodeError:
            sys.stdout.buffer.write(text.encode("utf-8"))
            sys.stdout.buffer.write(b"\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
