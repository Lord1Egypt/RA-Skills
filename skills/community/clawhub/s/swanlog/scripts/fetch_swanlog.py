"""从 SwanLab 云端拉取一次训练的全部指标 + 完整 profile（config / metadata / requirements / run_info）到本地。

输出目录结构::

    swanlog_<YYYY-MM-DD_HH-MM-SS>/     # 默认按 run.created_at 命名
    ├── metrics.csv         # 全部 scalar 指标（按 step 对齐）
    ├── config.yaml         # 当次实验的 resolved config
    ├── metadata.json       # SwanLab 采集的系统/硬件/git 信息
    ├── requirements.txt    # 训练环境的 pip freeze
    └── run_info.json       # 实验名/id/状态/时间戳

用法::

    # 默认：自动列举该 run 的所有 scalar metric 并全量拉取
    python fetch_swanlog.py --latest --project MyProject
    python fetch_swanlog.py --exp-id <experiment_id> --project MyProject

    # 仅拉指定 keys（白名单覆盖自动列举）
    python fetch_swanlog.py --latest --project MyProject --keys "train/loss,val/auc"

    # 自定义输出位置和时区
    python fetch_swanlog.py --latest --project MyProject -o /tmp/exp_dump --tz Asia/Shanghai

要求：
    - swanlab>=0.7.15
    - pandas, omegaconf
    - 本地已 ``swanlab login``（凭据落在 ``~/.swanlab/.netrc``）

设计：
    - 默认行为 = 自动列举所有 scalar key 并全拉，用户无需提前知道有哪些 metric
    - 通过 SwanLab 内部 ``/experiment/{id}/column`` 端点列举；列举失败会 fallback 到
      一组通用 key 并打 warning
    - 单 key 拉取 + 跳 404，兼容缺失字段的实验（不会因一个 key 不存在而整体失败）
    - 不依赖任何调用方项目代码，可作为独立工具使用
"""

from __future__ import annotations

import argparse
import json
import logging
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from zoneinfo import ZoneInfo
except ImportError:  # Python < 3.9 fallback
    ZoneInfo = None  # type: ignore

import pandas as pd
import swanlab
from omegaconf import OmegaConf
from swanlab.error import ApiError

logger = logging.getLogger(__name__)


# 列举失败时的兜底 key 列表，覆盖最常见的训练循环命名。
# 不存在的 key 会被 404 跳过，所以多列无害。
FALLBACK_KEYS: list[str] = [
    "train/loss",
    "train/lr",
    "epoch/avg_loss",
    "epoch/lr",
    "epoch/time_s",
    "val/loss",
    "val/loss_mean",
    "val/acc",
    "val/auc",
]

# SwanLab 把 metric 标记为 scalar 的两种 type；其它（IMAGE / AUDIO / TEXT 等）
# 在 metrics.csv 里没有合适的呈现方式，跳过。
SCALAR_TYPES: set[str] = {"FLOAT", "INTEGER"}


def _format_created_at(created_at: Any, tz: Any) -> str:
    """把 SwanLab 的 created_at（UTC ISO8601 字符串或 datetime）转成
    指定时区下文件系统安全、字典序即时间序的时间戳，形如
    ``YYYY-MM-DD_HH-MM-SS``。
    """
    if isinstance(created_at, datetime):
        dt = created_at
    else:
        s = str(created_at).rstrip("Z").split(".")[0]
        dt = datetime.fromisoformat(s)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)  # SwanLab 时间戳统一视作 UTC
    if tz is not None:
        dt = dt.astimezone(tz)
    else:
        dt = dt.astimezone()  # 系统本地时区
    return dt.strftime("%Y-%m-%d_%H-%M-%S")


def _enumerate_run_keys(client: Any, exp_id: str) -> list[str]:
    """通过 ``/experiment/{exp_id}/column`` 列出该 run 实际记录过的所有 scalar key。

    SwanLab 0.7.x 的公开 SDK 没有暴露这个端点，需要走 ``api._client`` 的内部 HTTP。
    服务端 ``size`` 上限实测 ≤ 100，因此使用 100 作为分页大小并循环拉到取完。
    若端点返回结构变化或鉴权失败，调用方应 fallback 到默认 key 列表。
    """
    page_size = 100
    items: list[dict] = []
    page = 1
    while True:
        data, _ = client.get(
            f"/experiment/{exp_id}/column",
            params={"page": page, "size": page_size},
        )
        chunk = data.get("list", []) or []
        items.extend(chunk)
        total_pages = data.get("pages", 1)
        if page >= total_pages or not chunk:
            break
        page += 1

    keys = [it["key"] for it in items if it.get("type") in SCALAR_TYPES]
    skipped_non_scalar = len(items) - len(keys)
    if skipped_non_scalar:
        logger.info(
            "skipped %d non-scalar columns (IMAGE / AUDIO / TEXT etc.)",
            skipped_non_scalar,
        )
    return keys


def _load_user_keys(args: argparse.Namespace) -> list[str]:
    """合并 ``--keys`` 与 ``--keys-file`` 的输入；都没传时返回空列表。"""
    keys: list[str] = []
    if args.keys:
        keys.extend(k.strip() for k in args.keys.split(",") if k.strip())
    if args.keys_file:
        text = Path(args.keys_file).read_text()
        keys.extend(
            k.strip() for k in text.splitlines() if k.strip() and not k.startswith("#")
        )
    # 去重保序
    seen: set[str] = set()
    deduped: list[str] = []
    for k in keys:
        if k not in seen:
            seen.add(k)
            deduped.append(k)
    return deduped


def _resolve_keys(
    args: argparse.Namespace, api: Any, run: Any
) -> tuple[list[str], str]:
    """决定本次要拉哪些 key，并返回 (keys, source_label) 用于日志。

    优先级：
      1. 用户显式 ``--keys`` / ``--keys-file`` → 白名单
      2. 默认 → 自动列举 run 的所有 scalar key
      3. 列举失败 → 退回 FALLBACK_KEYS（带 warning）
    """
    user_keys = _load_user_keys(args)
    if user_keys:
        return user_keys, "user-provided"

    try:
        auto_keys = _enumerate_run_keys(api._client, run.id)
        if auto_keys:
            return auto_keys, "auto-enumerated"
        logger.warning("no scalar keys found via enumeration; falling back to defaults")
    except Exception as exc:  # noqa: BLE001 — broad on purpose; we want a clean fallback
        logger.warning(
            "could not enumerate keys (%s: %s); falling back to defaults",
            type(exc).__name__, exc,
        )
    return list(FALLBACK_KEYS), "fallback-defaults"


def _fetch_metrics(run: Any, keys: list[str]) -> pd.DataFrame:
    """按 key 逐个拉取 metrics，遇到 404（该 key 不存在）就跳过。

    单次批量请求若包含任何不存在的 key 会整体失败，所以这里逐 key 请求并合并。
    """
    frames: list[pd.DataFrame] = []
    missing: list[str] = []
    for key in keys:
        try:
            df = run.metrics(keys=[key], x_axis="step")
        except ApiError as exc:
            if "404" in str(exc):
                missing.append(key)
                continue
            raise
        if df is not None and not df.empty:
            frames.append(df)
    if missing:
        logger.info("skipped %d missing keys: %s", len(missing), missing)
    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, axis=1)


def _resolve_run(
    api: "swanlab.Api",
    user: str,
    project: str,
    exp_id: str | None,
    latest: bool,
):
    if exp_id:
        return api.run(path=f"{user}/{project}/{exp_id}")
    runs = list(api.runs(path=f"{user}/{project}"))
    if not runs:
        raise RuntimeError(f"No experiments in {user}/{project}.")
    if latest:
        return max(runs, key=lambda r: r.created_at)
    raise ValueError("Must pass --exp-id or --latest.")


def _write_brief(
    out_dir: Path,
    run: Any,
    df: pd.DataFrame,
    keys_source: str,
) -> Path:
    """生成一份人类（与 LLM）友好的简报 ``brief.md``。

    动机：调用方拉完数据后想 1 秒内知道 "这个 run 现在跑成什么样了"。
    让脚本一次产出固定格式的简报，调用方（包括 Claude skill）就不必每次发明
    awk / Python one-liner 去 grep CSV，行为一致 + 不易出错。

    简报内容：
      - run 元信息（name / id / state / 时间 / url）
      - 每个 scalar 的最新非空值 + 对应 step
      - metrics.csv 形态（行 × 列）
    """
    lines: list[str] = []
    name = run.name or "(unnamed)"
    lines.append(f"# {name}")
    lines.append("")
    lines.append(f"- **id**: `{run.id}`")
    lines.append(f"- **state**: {run.state}")
    lines.append(f"- **created_at**: {run.created_at}")
    lines.append(
        f"- **finished_at**: {run.finished_at if run.finished_at else '(still running)'}"
    )
    lines.append(f"- **url**: {run.url}")
    lines.append("")

    # metrics.csv 的列形如 ``key`` 与 ``key_timestamp``；只展示非 timestamp 列
    if not df.empty:
        value_cols = [c for c in df.columns if not c.endswith("_timestamp")]
        lines.append("## Latest scalars")
        lines.append("")
        lines.append("| metric | step | value |")
        lines.append("|---|---:|---:|")
        for col in value_cols:
            series = df[col].dropna()
            if series.empty:
                continue
            last_step = series.index[-1]
            last_val = series.iloc[-1]
            # float 保留 6 位有效位；非 float 直接 str
            try:
                last_str = f"{float(last_val):.6g}"
            except (TypeError, ValueError):
                last_str = str(last_val)
            lines.append(f"| `{col}` | {last_step} | {last_str} |")
        lines.append("")
        lines.append("## Counts")
        lines.append("")
        lines.append(f"- metrics.csv: {len(df)} rows × {len(df.columns)} cols")
        lines.append(f"- scalar metrics: {len(value_cols)} ({keys_source})")
    else:
        lines.append("_No metrics rows yet — the run may not have logged any step._")

    brief_path = out_dir / "brief.md"
    brief_path.write_text("\n".join(lines) + "\n")
    return brief_path


def _dump_profile(profile: Any, out_dir: Path) -> list[str]:
    """把 profile 里的各块分别落到 out_dir；返回已写文件名列表。

    SwanLab 0.7.x 的 ``run.profile`` 是 ``Profile`` 对象（不是 dict），
    暴露 ``config`` / ``metadata`` / ``requirements`` 属性。
    """
    def _get(key: str) -> Any:
        if profile is None:
            return None
        if isinstance(profile, dict):
            return profile.get(key)
        return getattr(profile, key, None)

    written: list[str] = []
    if config := _get("config"):
        cfg_path = out_dir / "config.yaml"
        cfg_path.write_text(OmegaConf.to_yaml(OmegaConf.create(config)))
        written.append(cfg_path.name)
    if metadata := _get("metadata"):
        meta_path = out_dir / "metadata.json"
        meta_path.write_text(
            json.dumps(metadata, indent=2, ensure_ascii=False, default=str)
        )
        written.append(meta_path.name)
    if requirements := _get("requirements"):
        req_text = (
            "\n".join(requirements)
            if isinstance(requirements, list)
            else str(requirements)
        )
        req_path = out_dir / "requirements.txt"
        req_path.write_text(req_text)
        written.append(req_path.name)
    return written


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Fetch a SwanLab cloud run (all metrics + profile) to a local directory. "
            "By default enumerates every scalar metric the run logged."
        )
    )
    parser.add_argument(
        "--user", default=None,
        help="SwanLab username; defaults to the locally-logged-in account.",
    )
    parser.add_argument(
        "--project", default=None,
        help="SwanLab project name. Required unless SWANLAB_PROJECT env var is set.",
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--exp-id", help="Experiment ID (copyable from the WebUI URL).")
    group.add_argument(
        "--latest", action="store_true",
        help="Pick the project's most recent experiment by created_at.",
    )
    parser.add_argument(
        "--keys", default=None,
        help=(
            "Comma-separated metric keys to fetch (e.g. 'train/loss,val/auc'). "
            "When set, this acts as a whitelist and overrides auto-enumeration. "
            "Missing keys are skipped automatically."
        ),
    )
    parser.add_argument(
        "--keys-file", default=None,
        help="Path to a text file with one metric key per line (# comments allowed).",
    )
    parser.add_argument(
        "--tz", default=None,
        help=(
            "Timezone name for the output dir timestamp (e.g. 'Asia/Shanghai'). "
            "Default: system local timezone."
        ),
    )
    parser.add_argument(
        "-o", "--output", default=None,
        help="Output directory; default ./swanlog_<YYYY-MM-DD_HH-MM-SS>/",
    )
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(message)s")

    project = args.project or os.environ.get("SWANLAB_PROJECT")
    if not project:
        parser.error("--project is required (or set SWANLAB_PROJECT env var).")

    tz = None
    if args.tz:
        if ZoneInfo is None:
            parser.error("--tz requires Python 3.9+ (zoneinfo).")
        tz = ZoneInfo(args.tz)

    api = swanlab.Api()
    user = args.user or api.user().username
    run = _resolve_run(api, user, project, args.exp_id, args.latest)
    logger.info(
        "run: %s id=%s state=%s url=%s",
        run.name, run.id, run.state, run.url,
    )

    out_dir = (
        Path(args.output)
        if args.output
        else Path.cwd() / f"swanlog_{_format_created_at(run.created_at, tz)}"
    )
    out_dir.mkdir(parents=True, exist_ok=True)

    keys, source = _resolve_keys(args, api, run)
    logger.info("metric keys: %d (%s)", len(keys), source)
    df = _fetch_metrics(run, keys)
    metrics_path = out_dir / "metrics.csv"
    df.to_csv(metrics_path, index=True)
    logger.info(
        "metrics: %d rows × %d cols -> %s",
        len(df), len(df.columns), metrics_path.name,
    )

    (out_dir / "run_info.json").write_text(
        json.dumps(
            {
                "id": run.id,
                "name": run.name,
                "description": run.description,
                "state": run.state,
                "created_at": run.created_at,
                "finished_at": run.finished_at,
                "url": run.url,
                "user": getattr(run.user, "username", str(run.user)),
            },
            indent=2, ensure_ascii=False, default=str,
        )
    )

    written = _dump_profile(run.profile or {}, out_dir)
    logger.info("profile files: %s", written or "(profile is empty)")

    brief_path = _write_brief(out_dir, run, df, source)
    logger.info("brief: %s", brief_path.name)
    logger.info("output dir: %s", out_dir)


if __name__ == "__main__":
    main()
