from __future__ import annotations

import argparse
import html
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPORT_GLOB = "data/tiktok_hotspot_analysis/tiktok_hotspot_analysis_*.json"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "data" / "tiktok_hotspot_analysis"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render a TikTok hotspot analysis JSON report as static HTML.")
    parser.add_argument("--report", type=Path, default=None, help="Analysis JSON report. Defaults to the latest report.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args()


def resolve_path(path: Path) -> Path:
    return path if path.is_absolute() else PROJECT_ROOT / path


def latest_report() -> Path:
    paths = sorted(PROJECT_ROOT.glob(DEFAULT_REPORT_GLOB), key=lambda path: path.stat().st_mtime, reverse=True)
    if not paths:
        raise ValueError("No TikTok hotspot analysis report found")
    return paths[0]


def load_report(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as file:
        report = json.load(file)
    if not isinstance(report, dict):
        raise ValueError(f"Report is not a JSON object: {path}")
    return report


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def text(value: Any) -> str:
    if value is None:
        return "—"
    return html.escape(str(value))


def short_number(value: Any) -> str:
    if value is None:
        return "—"
    try:
        number = float(value)
    except (TypeError, ValueError):
        return text(value)
    abs_value = abs(number)
    if abs_value >= 1_000_000_000:
        return f"{number / 1_000_000_000:.1f}B"
    if abs_value >= 1_000_000:
        return f"{number / 1_000_000:.1f}M"
    if abs_value >= 1_000:
        return f"{number / 1_000:.1f}K"
    return f"{number:,.0f}"


def percent(value: Any) -> str:
    if value is None:
        return "—"
    try:
        return f"{float(value) * 100:.1f}%"
    except (TypeError, ValueError):
        return text(value)


def metric(label: str, value: Any, unit: str = "") -> str:
    return f"""
    <div class=\"metric\">
      <div class=\"metric-label\">{html.escape(label)}</div>
      <div class=\"metric-value\">{text(value)}<span>{html.escape(unit)}</span></div>
    </div>
    """


def stat(label: str, value: Any, class_name: str = "") -> str:
    return f"<div class=\"stat-row {class_name}\"><span>{html.escape(label)}</span><strong>{text(value)}</strong></div>"


def chips(values: list[Any], limit: int = 5) -> str:
    items = values[:limit]
    if not items:
        return "<span class=\"chip muted\">暂无标签</span>"
    return "".join(f"<span class=\"chip\">#{text(item)}</span>" for item in items)


def timeliness_label_text(label: str | None) -> str:
    return {
        "within_1d": "近一天",
        "within_3d": "近三天",
        "within_7d": "近七天",
        "within_14d": "近两周",
        "older_than_14d": "两周以前",
        "age_unknown": "发布时间未知",
        "fresh_rising": "新近起量",
        "rising_existing_video": "存量回升",
        "flat_or_declining": "持平或回落",
        "not_seen_in_previous_snapshot": "前序未命中",
    }.get(label or "", "状态未知")


def label_class(label: str | None) -> str:
    return {
        "within_1d": "status-hot",
        "within_3d": "status-hot",
        "within_7d": "status-warm",
        "within_14d": "status-warm",
        "older_than_14d": "status-muted",
        "age_unknown": "status-unknown",
        "fresh_rising": "status-hot",
        "rising_existing_video": "status-warm",
        "flat_or_declining": "status-muted",
        "not_seen_in_previous_snapshot": "status-unknown",
    }.get(label or "", "status-unknown")


def emerging_status_text(status: str | None) -> str:
    return {
        "new_emerging": "新冒出",
        "spreading": "正在扩散",
        "single_signal": "单点信号",
        "cooling": "已冷却",
        "mature_or_flat": "成熟或持平",
    }.get(status or "", "状态未知")


def hashtag_timeliness_text(label: str | None) -> str:
    return {
        "established_still_hot": "早已出现仍火",
        "new_within_7d": "近一周冒出",
        "new_within_3d": "近三天冒出",
        "new_within_1d": "一天内冒出",
        "established_first_seen": "本轮首次命中",
        "new_without_upload_time": "新标签待确认",
    }.get(label or "", "状态未知")


def hashtag_status_class(label: str | None) -> str:
    return {
        "new_within_1d": "status-hot",
        "new_within_3d": "status-hot",
        "new_within_7d": "status-warm",
        "established_still_hot": "status-warm",
        "established_first_seen": "status-unknown",
        "new_without_upload_time": "status-unknown",
    }.get(label or "", "status-unknown")


def age_hours(value: Any) -> str:
    if value is None:
        return "—"
    try:
        hours = float(value)
    except (TypeError, ValueError):
        return text(value)
    if hours < 24:
        return f"{hours:.1f} 小时"
    return f"{hours / 24:.1f} 天"


def source_type_text(source_type: Any) -> str:
    return {
        "keyword": "关键词",
        "hashtag": "话题标签",
        "creator": "达人",
        "music": "音乐",
    }.get(str(source_type or ""), text(source_type))


def video_card(video: dict[str, Any], index: int, mode: str) -> str:
    growth = video.get("growth") if isinstance(video.get("growth"), dict) else {}
    music = video.get("music") if isinstance(video.get("music"), dict) else {}
    label = growth.get("timeliness_label")
    is_rising = mode == "rising"
    primary_value = short_number(growth.get("views_delta")) if is_rising else short_number(video.get("view_count"))
    primary_label = "新增播放" if is_rising else "总播放"
    score = short_number(growth.get("trend_score")) if is_rising else short_number(video.get("hot_score"))
    score_label = "趋势分" if is_rising else "热度分"
    href = html.escape(str(video.get("url") or "#"), quote=True)
    return f"""
    <a href="{href}" target="_blank" rel="noreferrer" class="video-card-link">
    <article class=\"video-card\">
      <div class=\"rank\">{index:02d}</div>
      <div class=\"video-main\">
        <div class=\"video-topline\">
          <span class=\"source\">{source_type_text(video.get('source_type'))} / {text(video.get('source_value'))}</span>
          <span class=\"status {label_class(label)}\">{timeliness_label_text(label)}</span>
        </div>
        <h3>{text(video.get('title'))}</h3>
        <span class="creator">@{text(video.get('creator'))}</span>
        <div class=\"chip-row\">{chips(video.get('hashtags') or [])}</div>
      </div>
      <div class=\"video-data\">
        {stat(primary_label, primary_value, 'emphasis')}
        {stat(score_label, score)}
        {stat('视频年龄', f"{growth.get('video_age_hours')} 小时" if growth.get('video_age_hours') is not None else '—')}
        {stat('互动率', percent(video.get('engagement_rate')))}
        {stat('音乐', f"{music.get('track') or '—'} — {music.get('artist') or '—'}")}
      </div>
    </article>
    </a>
    """


def ranked_list(title: str, items: list[dict[str, Any]], value_label: str = "热度分") -> str:
    rows = []
    descriptions = {
        "热门音乐": "热度分 = 使用该音乐的样本视频热度分累加。单条视频热度分按播放量、点赞、评论、分享和收藏加权计算，因此这里更偏累计热度，不等同于当前增速。",
        "热门达人": "热度分 = 该达人在样本中命中的视频热度分累加。单条视频热度分按播放量、点赞、评论、分享和收藏加权计算，因此这里更偏累计热度，不等同于当前增速。",
    }
    description = descriptions.get(title)
    description_html = f'<p class="panel-note">{html.escape(description)}</p>' if description else ""
    for index, item in enumerate(items[:8], start=1):
        rows.append(
            f"""
            <tr>
              <td>{index:02d}</td>
              <td>{text(item.get('name'))}</td>
              <td>{short_number(item.get('video_count'))}</td>
              <td>{short_number(item.get('views'))}</td>
              <td>{short_number(item.get('score'))}</td>
            </tr>
            """
        )
    return f"""
    <section class=\"panel\">
      <div class=\"section-label\">{html.escape(title)}</div>
      {description_html}
      <table>
        <thead><tr><th>#</th><th>名称</th><th>视频数</th><th>播放量</th><th>{html.escape(value_label)}</th></tr></thead>
        <tbody>{''.join(rows)}</tbody>
      </table>
    </section>
    """


def hashtag_timeliness_table(items: list[dict[str, Any]]) -> str:
    rows = []
    for index, item in enumerate(items[:8], start=1):
        label = item.get("timeliness_label")
        rows.append(
            f"""
            <tr>
              <td>{index:02d}</td>
              <td>{text(item.get('name'))}</td>
              <td><span class=\"status {hashtag_status_class(label)}\">{hashtag_timeliness_text(label)}</span></td>
              <td>{short_number(item.get('video_count'))}</td>
              <td>{short_number(item.get('views'))}</td>
              <td>{age_hours(item.get('oldest_video_age_hours'))}</td>
              <td>{age_hours(item.get('newest_video_age_hours'))}</td>
            </tr>
            """
        )
    if not rows:
        rows.append('<tr><td colspan="7">暂无标签信号</td></tr>')
    return f"""
    <section class=\"panel\">
      <div class=\"section-label\">长期热门标签 / 时效性</div>
      <table>
        <thead><tr><th>#</th><th>标签</th><th>状态</th><th>视频数</th><th>播放量</th><th>最早视频年龄</th><th>最新视频年龄</th></tr></thead>
        <tbody>{''.join(rows)}</tbody>
      </table>
    </section>
    """
def recent_video_groups(groups: list[dict[str, Any]]) -> str:
    sections = []
    for group in groups:
        items = group.get("items") if isinstance(group.get("items"), list) else []
        cards = "".join(video_card(video, index, "cumulative") for index, video in enumerate(items[:5], start=1))
        if not cards:
            cards = "<div class=\"empty\">这个时间段暂无命中热视频。</div>"
        sections.append(
            f"""
            <section class=\"bucket-panel\">
              <div class=\"section-label\">{text(group.get('label'))} / 最多 5 条</div>
              <div class=\"video-stack\">{cards}</div>
            </section>
            """
        )
    return "".join(sections)


def novelty_badge(novelty: str | None) -> str:
    if novelty == "first_seen":
        return '<span class="novelty-badge first-seen">新见</span>'
    return ""


def signal_card(item: dict[str, Any], index: int) -> str:
    return f"""
    <article class="signal-card">
      <div class="signal-rank">{index:02d}</div>
      <div class="signal-main">
        <div class="signal-name">{text(item.get('name'))}{novelty_badge(item.get('novelty'))}</div>
        <div class="signal-age">最早 {age_hours(item.get('oldest_video_age_hours'))} / 最新 {age_hours(item.get('newest_video_age_hours'))}</div>
      </div>
      <div class="signal-metrics">
        <span>视频 {short_number(item.get('video_count'))}</span>
        <span>播放 {short_number(item.get('views'))}</span>
        <span>热度 {short_number(item.get('score'))}</span>
        <span>覆盖 {short_number(item.get('coverage_score'))}</span>
      </div>
    </article>
    """


def signal_list(title: str, items: list[dict[str, Any]], empty_text: str) -> str:
    cards = "".join(signal_card(item, index) for index, item in enumerate(items[:5], start=1))
    if not cards:
        cards = f'<div class="empty signal-empty">{html.escape(empty_text)}</div>'
    return f"""
    <div class="signal-group">
      <div class="section-label">{html.escape(title)}</div>
      <div class="signal-list">{cards}</div>
    </div>
    """


def recent_signals_groups(groups: list[dict[str, Any]]) -> str:
    sections = []
    for group in groups:
        heat_items = group.get("content_terms") if isinstance(group.get("content_terms"), list) else []
        cov_items = group.get("content_terms_coverage") if isinstance(group.get("content_terms_coverage"), list) else []
        ht_heat = group.get("hashtags") if isinstance(group.get("hashtags"), list) else []
        ht_cov = group.get("hashtags_coverage") if isinstance(group.get("hashtags_coverage"), list) else []
        sections.append(
            f"""
            <section class="panel signal-bucket">
              <div class="section-label">{text(group.get('label'))} / 趋势信号</div>
              <div class="signal-columns">
                {signal_list('内容关键词 · 热度排行', heat_items, '这个时间段暂无新近内容关键词')}
                {signal_list('内容关键词 · 覆盖排行', cov_items, '这个时间段暂无新近内容关键词')}
                {signal_list('TikTok 标签 · 热度排行', ht_heat, '这个时间段暂无新近 TikTok 标签')}
                {signal_list('TikTok 标签 · 覆盖排行', ht_cov, '这个时间段暂无新近 TikTok 标签')}
              </div>
            </section>
            """
        )
    return "".join(sections)


def established_terms_table(items: list[dict[str, Any]], title: str = "长期热门关键词 / 扩散监控", empty_text: str = "暂无长期热词扩散信号") -> str:
    rows = []
    for index, item in enumerate(items[:8], start=1):
        rows.append(
            f"""
            <tr>
              <td>{index:02d}</td>
              <td>{text(item.get('name'))}</td>
              <td><span class=\"status status-warm\">{emerging_status_text(item.get('status'))}</span></td>
              <td>{short_number(item.get('video_count'))}</td>
              <td>{short_number(item.get('sample_video_delta'))}</td>
              <td>{short_number(item.get('recent_24h_video_delta'))}</td>
              <td>{short_number(item.get('recent_7d_video_delta'))}</td>
              <td>{short_number(item.get('coverage_score'))}</td>
              <td>{short_number(item.get('score'))}</td>
              <td>{age_hours(item.get('oldest_video_age_hours'))}</td>
              <td>{age_hours(item.get('newest_video_age_hours'))}</td>
            </tr>
            """
        )
    if not rows:
        rows.append(f'<tr><td colspan="11">{html.escape(empty_text)}</td></tr>')
    return f"""
    <section class=\"panel wide-panel\">
      <div class=\"section-label\">{html.escape(title)}</div>
      <p class=\"panel-note\">这里只放最早命中的样本视频已经超过一个月的长期信号。扩散状态不再依赖前序快照是否命中，而是看当前快照内的视频年龄分布：近 7 天视频占比达到 10% 且最新视频在 7 天内才算“正在扩散”；最新视频在 7-30 天内为“成熟或持平”；最新视频超过 30 天为“已冷却”。覆盖分（video_count × log(1 + avg_score_per_video)）用于衡量一个词出现在多少视频中且每条都有基础互动。</p>
      <table>
        <thead><tr><th>#</th><th>名称</th><th>扩散状态</th><th>视频数</th><th>样本视频数</th><th>近24h视频</th><th>近7d视频</th><th>覆盖分</th><th>热度分</th><th>最早视频年龄</th><th>最新视频年龄</th></tr></thead>
        <tbody>{''.join(rows)}</tbody>
      </table>
    </section>
    """



def render_html(report: dict[str, Any]) -> str:
    top_videos = report.get("top_videos") or []
    hero = top_videos[0] if top_videos else {}
    hero_growth = hero.get("growth") if isinstance(hero.get("growth"), dict) else {}
    window = report.get("analysis_window") if isinstance(report.get("analysis_window"), dict) else {}
    cm = report.get("crawl_metrics") or {}
    source_counts = report.get("source_counts") if isinstance(report.get("source_counts"), dict) else {}
    source_summary = " / ".join(f"{source_type_text(key)} {value}" for key, value in source_counts.items()) or "暂无来源"
    recent_video_cards = recent_video_groups(report.get("recent_videos_by_age") or [])
    recent_signals = recent_signals_groups(report.get("recent_signals_by_age") or [])
    established_terms = established_terms_table(report.get("established_terms") or [], title="长期热门内容关键词 / 扩散监控")
    established_hashtags = established_terms_table(report.get("established_hashtags") or [], title="长期热门 TikTok 标签 / 扩散监控", empty_text="暂无长期热门标签扩散信号")
    cumulative_cards = "".join(video_card(video, index, "cumulative") for index, video in enumerate(top_videos[:6], start=1))

    return f"""<!doctype html>
<html lang=\"zh-CN\">
<head>
  <meta charset=\"utf-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
  <title>TikTok 热点分析报告</title>
  <link rel=\"preconnect\" href=\"https://fonts.googleapis.com\">
  <link rel=\"preconnect\" href=\"https://fonts.gstatic.com\" crossorigin>
  <link href=\"https://fonts.googleapis.com/css2?family=Doto:wght@400..700&family=Space+Grotesk:wght@300;400;500;700&family=Space+Mono:wght@400;700&display=swap\" rel=\"stylesheet\">
  <style>
    :root {{
      --black:#000; --surface:#111; --surface-raised:#1A1A1A; --border:#222; --border-visible:#333;
      --text-disabled:#666; --text-secondary:#999; --text-primary:#E8E8E8; --text-display:#FFF;
      --accent:#D71921; --success:#4A9E5C; --warning:#D4A843;
      --space-sm:8px; --space-md:16px; --space-lg:24px; --space-xl:32px; --space-2xl:48px; --space-3xl:64px;
    }}
    * {{ box-sizing:border-box; }}
    body {{
      margin:0; background:var(--black); color:var(--text-primary); font-family:'Space Grotesk', system-ui, sans-serif;
      background-image:radial-gradient(circle, var(--border) .5px, transparent .5px); background-size:12px 12px;
    }}
    a {{ color:var(--text-display); text-decoration:none; }}
    .page {{ max-width:1440px; margin:0 auto; padding:40px clamp(20px,4vw,56px) 72px; }}
    header {{ display:grid; grid-template-columns:1.2fr .8fr; gap:var(--space-2xl); align-items:end; min-height:360px; }}
    .eyebrow,.section-label,.metric-label,.source,.status,th,.stat-row span,.chip,.meta {{
      font-family:'Space Mono', monospace; font-size:11px; letter-spacing:.08em; text-transform:uppercase; color:var(--text-secondary);
    }}
    h1 {{ margin:12px 0 0; font-family:'Doto','Space Mono',monospace; font-size:clamp(54px,8vw,112px); line-height:.9; letter-spacing:-.04em; color:var(--text-display); font-weight:700; }}
    .hero-subtitle {{ max-width:680px; margin-top:var(--space-lg); color:var(--text-secondary); font-size:18px; line-height:1.45; }}
    .hero-metric {{ border-left:2px solid var(--accent); padding-left:var(--space-lg); }}
    .hero-number {{ font-family:'Space Mono',monospace; font-size:clamp(44px,6vw,84px); line-height:1; color:var(--text-display); letter-spacing:-.05em; }}
    .hero-label {{ margin-top:var(--space-sm); font-family:'Space Mono',monospace; font-size:12px; letter-spacing:.08em; color:var(--accent); text-transform:uppercase; }}
    .grid-metrics {{ display:grid; grid-template-columns:repeat(4,1fr); gap:1px; background:var(--border); border:1px solid var(--border); margin:var(--space-3xl) 0; }}
    .metric {{ background:var(--black); padding:var(--space-lg); min-height:132px; display:flex; flex-direction:column; justify-content:space-between; }}
    .metric-value {{ font-family:'Space Mono',monospace; color:var(--text-display); font-size:32px; letter-spacing:-.04em; }}
    .metric-value span {{ margin-left:4px; font-size:11px; color:var(--text-secondary); letter-spacing:.08em; }}
    .section-head {{ display:flex; justify-content:space-between; gap:var(--space-lg); align-items:end; margin:var(--space-3xl) 0 var(--space-lg); }}
    .section-head h2 {{ margin:0; color:var(--text-display); font-size:32px; line-height:1.1; letter-spacing:-.02em; }}
    .section-head p {{ margin:0; max-width:460px; color:var(--text-secondary); line-height:1.5; }}
    .video-stack {{ display:grid; gap:var(--space-md); }}
    .video-card {{ display:grid; grid-template-columns:72px 1fr 360px; gap:var(--space-lg); padding:var(--space-lg); background:rgba(17,17,17,.92); border:1px solid var(--border); border-radius:16px; }}
    .bucket-panel {{ margin-top:var(--space-lg); }}
    .rank {{ font-family:'Space Mono',monospace; color:var(--text-disabled); font-size:28px; letter-spacing:-.05em; }}
    .video-topline {{ display:flex; flex-wrap:wrap; gap:var(--space-sm); margin-bottom:var(--space-md); }}
    .status {{ border:1px solid var(--border-visible); border-radius:999px; padding:3px 9px; display:inline-flex; align-items:center; white-space:nowrap; }}
    .status-hot {{ color:var(--accent); border-color:var(--accent); }}
    .status-warm {{ color:var(--warning); border-color:var(--warning); }}
    .status-muted {{ color:var(--text-disabled); }}
    .status-unknown {{ color:var(--text-secondary); }}
    .video-main {{ min-width:0; }}
    h3 {{ margin:0 0 var(--space-md); font-size:22px; line-height:1.25; color:var(--text-display); font-weight:500; overflow-wrap:anywhere; word-break:break-word; }}
    .chip-row {{ display:flex; flex-wrap:wrap; gap:var(--space-sm); margin-top:var(--space-lg); }}
    .chip {{ border:1px solid var(--border-visible); border-radius:999px; padding:4px 10px; color:var(--text-secondary); }}
    .muted {{ color:var(--text-disabled); border-color:var(--border); }}
    .video-data {{ display:grid; align-content:start; border-top:1px solid var(--border); }}
    .stat-row {{ display:flex; justify-content:space-between; gap:var(--space-md); padding:12px 0; border-bottom:1px solid var(--border); }}
    .stat-row strong {{ font-family:'Space Mono',monospace; color:var(--text-primary); font-size:13px; text-align:right; font-weight:400; max-width:210px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }}
    .stat-row.emphasis strong {{ color:var(--accent); font-size:18px; }}
    .lower-grid {{ display:grid; grid-template-columns:1fr; gap:var(--space-lg); margin-top:var(--space-lg); }}
    .wide-panel {{ margin-top:var(--space-lg); }}
    .panel {{ background:rgba(17,17,17,.92); border:1px solid var(--border); border-radius:16px; padding:var(--space-lg); overflow:auto; }}
    .panel-note {{ margin:10px 0 20px; max-width:860px; color:var(--text-secondary); line-height:1.5; }}
    .signal-bucket {{ margin-top:var(--space-lg); overflow:visible; }}
    .signal-columns {{ display:grid; grid-template-columns:minmax(0,1fr) minmax(0,1fr); gap:var(--space-lg); margin-top:var(--space-md); }}
    .signal-group {{ display:grid; gap:var(--space-md); }}
    .signal-list {{ display:grid; gap:10px; }}
    .signal-card {{ display:grid; grid-template-columns:40px minmax(0,1fr); gap:var(--space-md); align-items:start; padding:14px 0; border-top:1px solid var(--border); }}
    .signal-card:first-child {{ border-top:1px solid var(--border-visible); }}
    .video-card-link {{ display:block; color:inherit; text-decoration:none; }}
    .video-card-link:hover article {{ border-color:var(--accent); }}
    .signal-rank {{ font-family:'Space Mono',monospace; color:var(--text-disabled); font-size:16px; }}
    .signal-main {{ min-width:0; }}
    .signal-name {{ color:var(--text-display); font-size:18px; line-height:1.25; overflow-wrap:anywhere; word-break:break-word; }}
    .signal-age {{ margin-top:4px; font-family:'Space Mono',monospace; color:var(--text-secondary); font-size:11px; letter-spacing:.04em; }}
    .signal-metrics {{ grid-column:2; display:flex; flex-wrap:wrap; justify-content:flex-start; gap:8px; margin-top:8px; }}
    .signal-metrics span {{ border:1px solid var(--border-visible); border-radius:999px; padding:4px 9px; font-family:'Space Mono',monospace; color:var(--text-secondary); font-size:11px; white-space:nowrap; }}
    .novelty-badge {{ border-radius:999px; padding:2px 8px; font-size:10px; font-family:'Space Mono',monospace; letter-spacing:.06em; margin-left:8px; vertical-align:middle; display:inline-block; }}
    .novelty-badge.first-seen {{ background:var(--accent); color:#FFF; border:1px solid var(--accent); }}
    .signal-empty {{ padding:var(--space-lg); }}
    table {{ width:100%; border-collapse:collapse; min-width:760px; }}
    th {{ text-align:left; padding:0 12px 12px; border-bottom:1px solid var(--border-visible); font-weight:400; }}
    td {{ padding:14px 12px; border-bottom:1px solid var(--border); color:var(--text-primary); }}
    td:nth-child(2) {{ max-width:420px; overflow-wrap:anywhere; word-break:break-word; }}
    td:first-child, td:nth-child(n+3) {{ font-family:'Space Mono',monospace; color:var(--text-secondary); }}
    td:nth-child(n+3), th:nth-child(n+3) {{ text-align:right; }}
    .empty {{ border:1px solid var(--border-visible); border-radius:16px; padding:var(--space-2xl); color:var(--text-secondary); font-family:'Space Mono',monospace; font-size:12px; letter-spacing:.04em; }}
    footer {{ margin-top:var(--space-3xl); padding-top:var(--space-lg); border-top:1px solid var(--border); color:var(--text-disabled); font-family:'Space Mono',monospace; font-size:11px; letter-spacing:.06em; text-transform:uppercase; }}
    @media (max-width:1100px) {{ header,.video-card,.lower-grid,.signal-columns {{ grid-template-columns:1fr; }} .video-data {{ margin-top:var(--space-md); }} }}
    @media (max-width:760px) {{ .grid-metrics {{ grid-template-columns:1fr 1fr; }} .page {{ padding-top:24px; }} header {{ min-height:auto; }} .signal-card {{ grid-template-columns:36px 1fr; }} .signal-metrics {{ grid-column:2; justify-content:flex-start; }} }}
  </style>
</head>
<body>
  <main class=\"page\">
    <header>
      <div>
        <div class=\"eyebrow\">TIKTOK 热点分析 / 美区女装</div>
        <h1>热点<br>此刻</h1>
        <p class=\"hero-subtitle\">这是一份静态热点报告，用发布时间分桶识别新近热点，用长期热词区块观察老词是否仍在扩散。</p>
      </div>
      <div class=\"hero-metric\">
        <div class=\"hero-number\">{short_number(hero.get('view_count'))}</div>
        <div class=\"hero-label\">累计播放最高</div>
        <p class=\"meta\">{text(hero.get('creator'))} / 视频年龄 {text(hero_growth.get('video_age_hours'))} 小时 / {timeliness_label_text(hero_growth.get('timeliness_label'))}</p>
      </div>
    </header>

    <section class=\"grid-metrics\">
      {metric('有效视频数', short_number(report.get('unique_video_count')))}
      {metric('前序命中数', short_number(window.get('matched_previous_video_count')))}
      {metric('分析窗口', f"{float(window.get('interval_hours') or 0):.2f}", '小时')}
      {metric('重复率', percent(cm.get('duplicate_rate')))}
      {metric('计划运行数', short_number(cm.get('planned_run_count')))}
      {metric('失败窗口', short_number(cm.get('failed_run_count')))}
      {metric('请求总量', short_number(cm.get('requested_total_limit')))}
      {metric('数据来源', source_summary)}
    </section>
    {f'<p class="panel-note" style="margin:-24px 0 24px;font-size:11px;">{html.escape(cm.get("cost_model_note", ""))}</p>' if cm.get("cost_model_note") else ''}

    <section>
      <div class=\"section-head\">
        <div>
          <div class=\"section-label\">新近视频 / 发布时间分桶</div>
          <h2>按发布时间分级的热点视频</h2>
        </div>
        <p>这里不依赖前后两轮是否抓到同一条视频，而是直接按视频发布时间分成近一天、三天、七天和两周，每个分级最多展示 5 条热视频。</p>
      </div>
      {recent_video_cards}
    </section>

    <section>
      <div class=\"section-head\">
        <div>
          <div class=\"section-label\">累计热度 / 总量排行</div>
          <h2>累计热视频</h2>
        </div>
        <p>这一部分按总播放和互动加权排序，可能包含早就已经很热的长尾视频，需要结合视频年龄和时效状态一起判断。</p>
      </div>
      <div class=\"video-stack\">{cumulative_cards}</div>
    </section>

    <section>
      <div class=\"section-head\">
        <div>
          <div class=\"section-label\">新晋趋势信号 / 发布时间分桶</div>
          <h2>新晋关键词与 TikTok 标签</h2>
        </div>
        <p>按一天、三天、七天、两周和一个月分桶；每个时间段分热度排行和覆盖排行两列展示。带有<span style=\"color:var(--accent)\">新见</span>标记的词在该时间段出现，但在更长时间段（如近七天 / 近两周 / 近一个月）的样本中未出现，代表它可能是本轮新冒出的信号。覆盖分（video_count × log(1 + avg_score_per_video)）用于衡量一个词出现在多少视频中且有基础互动。</p>
      </div>
      {recent_signals}
    </section>

    <section>
      <div class=\"section-head\">
        <div>
          <div class=\"section-label\">长期热词 / 扩散监控</div>
          <h2>长期热门关键词</h2>
        </div>
        <p>长期热词与新近关键词分开：只有长期热词才看“是否仍在扩散”，新近词优先看出现时间和短期热度。</p>
      </div>
      {established_terms}
      {established_hashtags}
    </section>

    <section class=\"lower-grid\">
      {ranked_list('热门音乐', report.get('top_music') or [])}
      {ranked_list('热门达人', report.get('top_creators') or [])}
    </section>

    <footer>
      生成时间 {text(report.get('generated_at'))} / 当前快照 {text(window.get('current_snapshot_time'))} / 前序快照 {text(window.get('previous_snapshot_time'))}
    </footer>
  </main>
</body>
</html>
"""


def write_html(content: str, output_dir: Path) -> Path:
    output_dir = output_dir if output_dir.is_absolute() else PROJECT_ROOT / output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"tiktok_hotspot_report_{utc_timestamp()}.html"
    path.write_text(content, encoding="utf-8")
    return path


def main() -> int:
    args = parse_args()
    try:
        report_path = resolve_path(args.report) if args.report else latest_report()
        report = load_report(report_path)
        output_path = write_html(render_html(report), args.output_dir)
    except ValueError as exc:
        print(f"render error: {exc}")
        return 2
    print(f"html_report: {output_path}")
    print(f"source_report: {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
