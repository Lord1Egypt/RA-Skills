#!/usr/bin/env python3
"""ClawHub 独立数据采集与报告生成程序 —— 不依赖任何 LLM API。

工作方式（二选一）：
  1. API 模式：从 Convex API 抓取最新 skill 列表（推荐，数据最新）
  2. 文件模式：读取最近缓存的 skill_list.json

无论哪种模式，都会自动读入最近的 metrics 和 snapshot 来计算变化量，
最终生成格式化文本报告和 JSON 指标文件，供后续 cron/agent 直接使用。

用法：
  python3 clawhub_report.py --handle harrylabsj --out-dir ../reports
  python3 clawhub_report.py --handle harrylabsj --from-file data/raw/harrylabsj_skill_list.json --stdout

输出：
  reports/clawhub-report-YYYY-MM-DD.txt     ← 格式化报告（可直接发送）
  reports/clawhub-report-latest.txt         ← 最新报告副本
  reports/clawhub-metrics-YYYY-MM-DD.json   ← 指标 JSON（供下次 delta 计算）
"""

from __future__ import annotations

import argparse
import json
import os
import ssl
import subprocess
import sys
import time
import urllib.error
import urllib.request
from collections import defaultdict
from datetime import datetime, date, timezone
from pathlib import Path
from typing import Any

CONVEX_QUERY_URL = "https://wry-manatee-359.convex.cloud/api/query"
USER_AGENT = "clawhub-report/1.0"


# ── helpers ──────────────────────────────────────────────────────────────


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def to_int(v: Any) -> int:
    try:
        return int(float(v)) if v not in (None, "", "None") else 0
    except (ValueError, TypeError):
        return 0


def beijing_now() -> str:
    """返回北京时间 YYYY-MM-DD HH:MM 字符串"""
    bj = datetime.now(timezone.utc).astimezone()
    # 手动偏移 +8h
    from datetime import timedelta
    bj = datetime.now(timezone.utc) + timedelta(hours=8)
    return bj.strftime("%Y-%m-%d %H:%M")


def beijing_date() -> str:
    from datetime import timedelta
    return (datetime.now(timezone.utc) + timedelta(hours=8)).strftime("%Y-%m-%d")


# ── Convex API ───────────────────────────────────────────────────────────


def convex_query(path: str, args: list[Any], *, retries: int = 3) -> Any:
    """调用 Convex query API，支持 SSL fallback。"""
    body = {"path": path, "format": "convex_encoded_json", "args": args}
    data = json.dumps(body, separators=(",", ":")).encode("utf-8")
    headers = {
        "User-Agent": USER_AGENT,
        "Content-Type": "application/json",
        "Convex-Client": "npm-1.40.0",
        "Accept": "application/json",
    }

    # 准备 SSL context（尝试多种配置）
    ctx = ssl.create_default_context()

    last_error: Exception | None = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(
                CONVEX_QUERY_URL, data=data, headers=headers, method="POST"
            )
            with urllib.request.urlopen(req, timeout=60, context=ctx) as resp:
                result = json.loads(resp.read().decode("utf-8"))
            if result.get("status") != "success":
                raise RuntimeError(f"Convex query failed: {result}")
            return result.get("value")
        except (urllib.error.URLError, urllib.error.HTTPError, ssl.SSLError) as e:
            last_error = e
            if attempt < retries - 1:
                wait = 2.0 * (attempt + 1)
                print(f"  ⚠️  API 请求失败，{wait:.0f}s 后重试 ({attempt+2}/{retries}): {e}", file=sys.stderr)
                time.sleep(wait)
                continue
        except Exception as e:
            last_error = e
            if attempt < retries - 1:
                time.sleep(2.0 * (attempt + 1))
                continue
            raise

    raise RuntimeError(
        f"Convex API 全部 {retries} 次重试均失败: {last_error}"
    )


def fetch_skill_list(handle: str) -> list[dict[str, Any]]:
    """通过 Convex 分页获取完整的 skill 列表（不含 detail，速度快）。"""
    all_skills: list[dict[str, Any]] = []
    cursor: str | None = None
    page = 0

    while True:
        page += 1
        args = {
            "handle": handle,
            "kind": "skill",
            "sort": "downloads",
            "paginationOpts": {"cursor": cursor, "numItems": 500},
        }
        value = convex_query("publishers:listPublishedPage", [args])
        if not isinstance(value, dict):
            raise RuntimeError(f"Unexpected page response: {value!r}")
        page_skills = value.get("page") or []
        all_skills.extend(page_skills)
        print(
            f"  📄 第{page}页: {len(page_skills)} 个, 累计 {len(all_skills)}",
            file=sys.stderr,
        )
        if value.get("isDone"):
            break
        cursor = value.get("continueCursor")
        if cursor in (None, ""):
            raise RuntimeError(f"分页未完成但无cursor: {value}")
        time.sleep(0.3)

    return all_skills


# ── 文件加载 ──────────────────────────────────────────────────────────────


def load_previous_metrics(metrics_dir: Path) -> dict[str, Any] | None:
    """加载前一天的指标 JSON 用于 delta 计算。"""
    if not metrics_dir.exists():
        return None
    candidates = sorted(metrics_dir.glob("clawhub-metrics-*.json"))
    if not candidates:
        return None
    for p in reversed(candidates):
        try:
            return json.loads(p.read_text("utf-8"))
        except Exception:
            continue
    return None


def load_latest_snapshot_installs(
    snapshot_dir: Path,
) -> tuple[dict[str, int], int]:
    """从最新 snapshot 中提取 installs_all_time 数据。"""
    latest_path = snapshot_dir / "latest.json"
    if not latest_path.exists():
        return {}, 0
    try:
        data = json.loads(latest_path.read_text("utf-8"))
        skills = data.get("skills", [])
        installs_map: dict[str, int] = {}
        total = 0
        for s in skills:
            slug = s.get("slug", "")
            inst = to_int(s.get("installs_all_time", 0))
            if slug:
                installs_map[slug] = inst
                total += inst
        return installs_map, total
    except Exception as e:
        print(f"  ⚠️  snapshot 读取失败: {e}", file=sys.stderr)
        return {}, 0


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text("utf-8"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


# ── 指标计算 ──────────────────────────────────────────────────────────────


def compute_metrics(
    skills: list[dict[str, Any]],
    prev_metrics: dict[str, Any] | None,
    installs_map: dict[str, int],
    total_installs_snapshot: int,
) -> dict[str, Any]:
    """计算所有报告指标。"""
    now = utc_now()
    today = beijing_date()

    # 当前汇总
    total_skills = len(skills)
    total_downloads = sum(to_int(s.get("downloads", 0)) for s in skills)
    total_stars = sum(to_int(s.get("stars", 0)) for s in skills)

    # 安装数据：优先用 snapshot，其次 prev_metrics
    total_installs = total_installs_snapshot if total_installs_snapshot > 0 else (
        prev_metrics.get("total_installs", 0) if prev_metrics else 0
    )

    # 按下载排序
    sorted_by_dl = sorted(
        skills,
        key=lambda s: to_int(s.get("downloads", 0)),
        reverse=True,
    )

    # TOP 下载
    top_downloads = [
        {
            "slug": s.get("slug", ""),
            "display_name": s.get("displayName", s.get("slug", "")),
            "downloads": to_int(s.get("downloads", 0)),
            "stars": to_int(s.get("stars", 0)),
        }
        for s in sorted_by_dl[:15]
    ]

    # 高星标
    top_stars = [
        {
            "slug": s.get("slug", ""),
            "display_name": s.get("displayName", s.get("slug", "")),
            "downloads": to_int(s.get("downloads", 0)),
            "stars": to_int(s.get("stars", 0)),
        }
        for s in sorted(skills, key=lambda s: -to_int(s.get("stars", 0)))
        if to_int(s.get("stars", 0)) > 0
    ]

    # 增量计算
    delta_downloads = 0
    delta_installs = 0
    delta_stars = 0
    new_skills: list[dict[str, Any]] = []
    top_new_downloads: list[dict[str, Any]] = []
    install_changes: list[dict[str, Any]] = []

    if prev_metrics:
        prev_dl = prev_metrics.get("total_downloads", 0)
        prev_inst = prev_metrics.get("total_installs", 0)
        prev_stars = prev_metrics.get("total_stars", 0)
        delta_downloads = total_downloads - prev_dl
        delta_installs = total_installs - prev_inst
        delta_stars = total_stars - prev_stars

        # 新技能
        prev_slugs = set(prev_metrics.get("all_slugs", []))
        new_skills = [
            {
                "slug": s.get("slug", ""),
                "display_name": s.get("displayName", s.get("slug", "")),
                "downloads": to_int(s.get("downloads", 0)),
            }
            for s in skills
            if s.get("slug", "") not in prev_slugs
        ]
        new_skills.sort(key=lambda x: -x["downloads"])

        # 下载增长 TOP
        prev_dl_map = prev_metrics.get("downloads_map", {})
        changes = []
        for s in skills:
            slug = s.get("slug", "")
            current_dl = to_int(s.get("downloads", 0))
            prev_dl_ = prev_dl_map.get(slug, 0)
            diff = current_dl - prev_dl_
            if diff > 0:
                changes.append({
                    "slug": slug,
                    "display_name": s.get("displayName", slug),
                    "new_downloads": diff,
                    "current_downloads": current_dl,
                })
        changes.sort(key=lambda x: -x["new_downloads"])
        top_new_downloads = changes[:15]

        # 安装增长 TOP
        prev_inst_map = prev_metrics.get("installs_map", {})
        install_changes = []
        for slug, current_inst in installs_map.items():
            prev_inst_ = prev_inst_map.get(slug, 0)
            diff = max(0, current_inst - prev_inst_)
            if diff > 0:
                # 找 display_name
                display_name = slug
                for s in skills:
                    if s.get("slug", "") == slug:
                        display_name = s.get("displayName", slug)
                        break
                install_changes.append({
                    "slug": slug,
                    "display_name": display_name,
                    "new_installs": diff,
                    "current_installs": current_inst,
                })
        install_changes.sort(key=lambda x: -x["new_installs"])

    return {
        "generated_at": now.isoformat(),
        "generated_at_date": today,
        "total_skills": total_skills,
        "total_downloads": total_downloads,
        "total_installs": total_installs,
        "total_stars": total_stars,
        "delta_downloads": delta_downloads,
        "delta_installs": delta_installs,
        "delta_stars": delta_stars,
        "new_skills_count": len(new_skills),
        "new_skills": new_skills[:10],
        "top_new_downloads": top_new_downloads,
        "top_downloads": top_downloads,
        "top_stars": top_stars,
        "top_new_installs": install_changes[:15],
        "all_slugs": [s.get("slug", "") for s in skills],
        "downloads_map": {
            s.get("slug", ""): to_int(s.get("downloads", 0)) for s in skills
        },
        "installs_map": installs_map,
    }


def assess_data_quality(
    metrics: dict[str, Any],
    skills: list[dict[str, Any]],
    *,
    data_source: str,
    data_dir: Path,
    handle: str,
) -> dict[str, Any]:
    raw_dir = data_dir / "raw"
    collection_summary = read_json(raw_dir / f"{handle}_collection_summary.json")
    profile = read_json(raw_dir / f"{handle}_profile.json")
    profile_stats = profile.get("stats") if isinstance(profile.get("stats"), dict) else {}

    warnings: list[str] = []
    if not data_source.startswith("API (实时)"):
        warnings.append(f"using non-live data source: {data_source}")

    total_skills = to_int(metrics.get("total_skills"))
    total_downloads = to_int(metrics.get("total_downloads"))
    total_stars = to_int(metrics.get("total_stars"))
    zero_download_count = sum(1 for skill in skills if to_int(skill.get("downloads")) == 0)
    zero_download_rate = round(zero_download_count / total_skills, 4) if total_skills else 0.0

    detail_error_count = to_int(collection_summary.get("detail_error_count"))
    detail_success_count = to_int(collection_summary.get("detail_success_count"))
    detail_total = detail_error_count + detail_success_count
    detail_error_rate = round(detail_error_count / detail_total, 4) if detail_total else 0.0

    profile_skill_count = to_int(profile_stats.get("skills") or collection_summary.get("profile_skill_count"))
    profile_downloads = to_int(profile_stats.get("downloads"))
    profile_stars = to_int(profile_stats.get("stars"))

    if detail_error_count:
        warnings.append(f"detail fetch failed for {detail_error_count}/{detail_total or total_skills} skills")
    if profile_skill_count and profile_skill_count != total_skills:
        warnings.append(f"profile skill count {profile_skill_count} differs from report count {total_skills}")
    if profile_downloads:
        diff = abs(profile_downloads - total_downloads)
        if diff / max(1, profile_downloads) >= 0.03:
            warnings.append(f"profile downloads {profile_downloads} differ from report downloads {total_downloads}")
    if profile_stars and profile_stars != total_stars:
        warnings.append(f"profile stars {profile_stars} differ from report stars {total_stars}")
    if zero_download_rate >= 0.2 and (detail_error_count or profile_downloads):
        warnings.append(f"zero-download rows are high: {zero_download_count}/{total_skills}")
    if to_int(metrics.get("delta_downloads")) < 0:
        warnings.append(f"negative download delta: {metrics.get('delta_downloads')}")
    if to_int(metrics.get("delta_stars")) < 0:
        warnings.append(f"negative star delta: {metrics.get('delta_stars')}")

    status = "partial" if warnings else "ok"
    return {
        "status": status,
        "warnings": warnings,
        "destructive_actions_allowed": status == "ok",
        "cleanup_actions_allowed": status == "ok",
        "data_source": data_source,
        "detail_error_count": detail_error_count,
        "detail_error_rate": detail_error_rate,
        "zero_download_count": zero_download_count,
        "zero_download_rate": zero_download_rate,
        "profile_downloads": profile_downloads,
        "reported_downloads": total_downloads,
        "profile_stars": profile_stars,
        "reported_stars": total_stars,
    }


# ── 报告格式化 ────────────────────────────────────────────────────────────


def format_report(metrics: dict[str, Any]) -> str:
    """生成专注新增下载和新增安装的简明报告。"""
    now_str = beijing_now()
    date_str = metrics.get("generated_at_date", beijing_date())

    lines: list[str] = []
    lines.append(f"📊 ClawHub 每日新增报告（{date_str}）")
    lines.append("═" * 50)
    data_quality = metrics.get("data_quality") if isinstance(metrics.get("data_quality"), dict) else {}
    if data_quality and data_quality.get("status") != "ok":
        lines.append(f"⚠️ 数据质量：{data_quality.get('status', 'partial')}")
        for warning in data_quality.get("warnings", [])[:4]:
            lines.append(f"  - {warning}")
        lines.append("  本报告仅用于趋势观察；不要据此隐藏、合并或删除 skill。")
        lines.append("─" * 50)

    d_dl = metrics["delta_downloads"]
    d_inst = metrics["delta_installs"]
    d_stars = metrics["delta_stars"]
    new_cnt = metrics["new_skills_count"]

    d_dl_str = f"+{d_dl:,}" if d_dl >= 0 else str(d_dl)
    d_inst_str = f"+{d_inst}" if d_inst >= 0 else str(d_inst)

    lines.append(f"📥 新增下载：{d_dl_str}")
    lines.append(f"💾 新增安装：{d_inst_str}")
    if d_stars != 0:
        d_stars_str = f"+{d_stars}" if d_stars >= 0 else str(d_stars)
        lines.append(f"⭐ 新增星标：{d_stars_str}")
    if new_cnt > 0:
        lines.append(f"🆕 新技能：+{new_cnt}")
    lines.append("─" * 50)

    # 新增下载 TOP 10
    lines.append("")
    lines.append("🔥 新增下载 TOP 10")
    top_new = metrics.get("top_new_downloads", [])
    if top_new:
        for i, s in enumerate(top_new[:10], 1):
            name = s["display_name"][:40]
            lines.append(f" {i:2d}. {name:40s} +{s['new_downloads']:>4d}")
    else:
        lines.append(" （首次运行或缺对比数据）")

    # 新增安装 TOP 10（如有数据）
    top_new_inst = metrics.get("top_new_installs", [])
    if top_new_inst:
        lines.append("")
        lines.append("💾 新增安装 TOP 10")
        for i, s in enumerate(top_new_inst[:10], 1):
            name = s["display_name"][:40]
            lines.append(f" {i:2d}. {name:40s} +{s['new_installs']:>4d}")

    lines.append("")
    lines.append("─" * 50)
    lines.append(f"⏰ 报告时间：{now_str}")

    return "\n".join(lines)


# ── main ─────────────────────────────────────────────────────────────────


def find_cached_skill_list(data_dir: Path, handle: str) -> Path | None:
    """在 data/raw/ 下找最近的 skill_list 缓存。"""
    candidates = sorted(data_dir.glob(f"{handle}_skill_list.json"))
    return candidates[-1] if candidates else None


def find_default_paths(
    handle: str,
) -> tuple[Path, Path, Path]:
    """根据脚本所在目录推断默认数据路径。"""
    script_dir = Path(__file__).resolve().parent
    data_dir = script_dir.parent / "data"
    out_dir = script_dir.parent / "reports"
    snapshot_dir = data_dir / "snapshots" / handle
    return data_dir, out_dir, snapshot_dir


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--handle", default="harrylabsj", help="ClawHub handle")
    parser.add_argument(
        "--out-dir", type=Path, default=None, help="报告输出目录"
    )
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=None,
        help="数据目录（含 raw/ snapshots/）",
    )
    parser.add_argument(
        "--from-file",
        type=Path,
        default=None,
        help="跳过 API 直接从已有 JSON 文件读取 skill list",
    )
    parser.add_argument(
        "--stdout", action="store_true", help="同时输出报告到 stdout"
    )
    parser.add_argument(
        "--skip-api",
        action="store_true",
        help="跳过 API 抓取，使用最近缓存",
    )
    args = parser.parse_args()

    # ── 路径 ─────────────────────────────────────────────────
    data_dir, default_out, default_snapshot = find_default_paths(args.handle)
    if args.data_dir:
        data_dir = args.data_dir.resolve()
    out_dir = (args.out_dir or default_out).resolve()
    snapshot_dir = data_dir / "snapshots" / args.handle
    raw_dir = data_dir / "raw"

    out_dir.mkdir(parents=True, exist_ok=True)

    # ── 加载/获取数据 ─────────────────────────────────────────
    skills: list[dict[str, Any]] = []
    data_source = ""

    if args.from_file:
        # 从指定文件加载
        fp = args.from_file.resolve()
        if not fp.exists():
            print(f"❌ 文件不存在: {fp}", file=sys.stderr)
            return 1
        skills = json.loads(fp.read_text("utf-8"))
        data_source = f"文件: {fp}"
        print(f"📂 从文件加载: {len(skills)} skills", file=sys.stderr)
    elif args.skip_api:
        # 用最近缓存
        cached = find_cached_skill_list(raw_dir, args.handle)
        if cached:
            skills = json.loads(cached.read_text("utf-8"))
            data_source = f"缓存: {cached}"
            print(f"📂 使用缓存: {len(skills)} skills ({cached.name})", file=sys.stderr)
        else:
            print("❌ 无缓存数据且跳过 API", file=sys.stderr)
            return 1
    else:
        # API 模式
        print(f"🌐 从 API 抓取 @{args.handle} 的 skill 列表...", file=sys.stderr)
        try:
            skills = fetch_skill_list(args.handle)
            data_source = "API (实时)"
            print(f"✅ API 成功: {len(skills)} skills", file=sys.stderr)
        except Exception as e:
            print(f"⚠️  API 抓取失败: {e}", file=sys.stderr)
            # fallback: 用最近缓存
            cached = find_cached_skill_list(raw_dir, args.handle)
            if cached:
                skills = json.loads(cached.read_text("utf-8"))
                data_source = f"缓存(API失败回退): {cached.name}"
                print(f"📂 回退到缓存: {len(skills)} skills", file=sys.stderr)
            else:
                print("❌ API 失败且无缓存", file=sys.stderr)
                return 1

    if not skills:
        print("❌ 无数据", file=sys.stderr)
        return 1

    # ── 加载历史数据用于 delta ────────────────────────────────
    prev_metrics = load_previous_metrics(out_dir)
    installs_map, total_installs_snapshot = load_latest_snapshot_installs(
        snapshot_dir
    )

    if prev_metrics:
        print(
            f"📊 上次指标日期: {prev_metrics.get('generated_at_date', '?')}",
            file=sys.stderr,
        )
    else:
        print("📊 首次运行，无历史对比", file=sys.stderr)

    if installs_map:
        print(
            f"📊 从 snapshot 获取安装数据: {total_installs_snapshot} 安装",
            file=sys.stderr,
        )
    else:
        print("📊 snapshot 中无安装数据", file=sys.stderr)

    # ── 计算指标 ──────────────────────────────────────────────
    metrics = compute_metrics(
        skills, prev_metrics, installs_map, total_installs_snapshot
    )
    metrics["_data_source"] = data_source
    metrics["data_quality"] = assess_data_quality(
        metrics,
        skills,
        data_source=data_source,
        data_dir=data_dir,
        handle=args.handle,
    )

    # ── 生成报告 ──────────────────────────────────────────────
    report = format_report(metrics)
    print("", file=sys.stderr)
    print(report, file=sys.stderr)

    # ── 写输出文件 ────────────────────────────────────────────
    today = date.today().isoformat()

    report_path = out_dir / f"clawhub-report-{today}.txt"
    report_path.write_text(report, encoding="utf-8")
    print(f"\n📝 报告: {report_path}", file=sys.stderr)

    latest_path = out_dir / "clawhub-report-latest.txt"
    latest_path.write_text(report, encoding="utf-8")
    print(f"📝 最新: {latest_path}", file=sys.stderr)

    metrics_path = out_dir / f"clawhub-metrics-{today}.json"
    metrics_path.write_text(
        json.dumps(metrics, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"📊 指标: {metrics_path}", file=sys.stderr)

    # ── stdout ────────────────────────────────────────────────
    if args.stdout:
        print()
        print(report)

    return 0


if __name__ == "__main__":
    sys.exit(main())
