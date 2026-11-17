#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
查重复核工单渲染器 v4.5.0

将一条复核工单渲染为「移动端可读」的自包含 HTML：
- 两张原始凭证缩略图左右对照（数电票渲染首页 / 纸票用扫描图）
- 差异字段标注表
- 渲染失败（无预览图）时仅展示要素差异表，不影响查阅

设计约束（死规则 #9 / #13）：
- 第三方库（pdf2image / pypdf）缺失时降级跳过缩略图，仅出要素差异表
- 不生成任何 .bat/.ps1 等受限文件
"""

import base64
import io
import json
from pathlib import Path
from typing import Dict, Any, Optional


_MIME = {
    ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
    ".bmp": "image/bmp", ".gif": "image/gif",
}

_FIELD_LABELS = {
    "invoice_number": "发票号码",
    "seller_name": "销售方",
    "amount": "金额",
    "billing_date": "开票日期",
}


def _thumb_data_uri(path: Optional[str]) -> Optional[str]:
    """把原始凭证文件转为内联 base64 缩略图；不可渲染返回 None"""
    if not path:
        return None
    p = Path(path)
    if not p.exists():
        return None
    suf = p.suffix.lower()
    try:
        if suf in _MIME:
            data = p.read_bytes()
            return f"data:{_MIME[suf]};base64," + base64.b64encode(data).decode("ascii")
        if suf == ".pdf":
            # 尝试渲染首页为 PNG
            try:
                from pdf2image import convert_from_path
                imgs = convert_from_path(str(p), first_page=1, last_page=1, dpi=90)
                if imgs:
                    buf = io.BytesIO()
                    imgs[0].save(buf, "PNG")
                    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode("ascii")
            except Exception:
                return None
    except Exception:
        return None
    return None


def render_review_html(review: Dict[str, Any], output_html: str) -> str:
    """
    渲染工单为移动端可读 HTML。

    Args:
        review: ledger_db.list_reviews() 返回的工单 dict（含 members / diff_fields）
        output_html: 输出文件路径
    Returns:
        输出文件路径
    """
    members = review.get("members", []) or []
    diff_fields = review.get("diff_fields", []) or []
    signal = review.get("signal", "")
    confidence = review.get("confidence", 0) or 0

    out = Path(output_html)
    out.parent.mkdir(parents=True, exist_ok=True)

    # 缩略图卡片
    cards = []
    for m in members:
        uri = _thumb_data_uri(m.get("source_file"))
        if uri:
            thumb = f'<img class="thumb" src="{uri}" alt="原始凭证"/>'
        else:
            thumb = '<div class="nothumb">无预览图<br/><small>请在桌面端打开原文件</small></div>'
        cards.append(f"""
        <div class="card">
          {thumb}
          <div class="meta">
            <div><b>票号</b> {_esc(m.get('invoice_number'))}</div>
            <div><b>销售方</b> {_esc(m.get('seller_name'))}</div>
            <div><b>金额</b> {_fmt_money(m.get('amount'))}</div>
            <div><b>日期</b> {_esc(m.get('billing_date'))}</div>
            <div><b>来源</b> {_esc(m.get('source_file'))}</div>
          </div>
        </div>""")

    # 差异表
    diff_rows = ""
    if diff_fields:
        head = "".join(f"<th>{_FIELD_LABELS.get(f, f)}</th>" for f in diff_fields)
        body_rows = []
        for m in members:
            tds = "".join(f"<td>{_esc(m.get(f))}</td>" for f in diff_fields)
            body_rows.append(f"<tr>{tds}</tr>")
        diff_rows = f"""
        <h3>差异标注</h3>
        <table class="diff">
          <thead><tr>{head}</tr></thead>
          <tbody>{''.join(body_rows)}</tbody>
        </table>"""
    else:
        diff_rows = '<p class="nodiff">无差异字段（疑似原样重复）</p>'

    signal_label = "精确重复" if signal == "exact" else ("近似重复（疑似改抬头）" if signal == "fuzzy" else signal)

    html = f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>查重复核工单 #{review.get('id')}</title>
<style>
  * {{ box-sizing: border-box; }}
  body {{ font-family: -apple-system, "PingFang SC", "Microsoft YaHei", sans-serif;
         margin: 0; padding: 14px; background: #f5f6f8; color: #222; }}
  .head {{ background: #fff; border-radius: 10px; padding: 14px; margin-bottom: 12px;
          box-shadow: 0 1px 3px rgba(0,0,0,.08); }}
  .badge {{ display: inline-block; padding: 2px 10px; border-radius: 12px; font-size: 13px;
           background: #fff1f0; color: #cf1322; font-weight: 600; }}
  .row {{ display: flex; gap: 10px; overflow-x: auto; }}
  .card {{ flex: 1 1 0; min-width: 140px; background: #fff; border-radius: 10px; padding: 8px;
          box-shadow: 0 1px 3px rgba(0,0,0,.08); }}
  .thumb {{ width: 100%; height: 150px; object-fit: contain; background: #fafafa;
           border: 1px solid #eee; border-radius: 6px; }}
  .nothumb {{ width: 100%; height: 150px; display: flex; flex-direction: column;
             align-items: center; justify-content: center; color: #999; font-size: 13px;
             background: #fafafa; border: 1px dashed #ddd; border-radius: 6px; }}
  .meta {{ font-size: 13px; line-height: 1.7; margin-top: 6px; }}
  .meta b {{ color: #888; font-weight: 500; margin-right: 4px; }}
  h3 {{ font-size: 15px; margin: 16px 0 8px; }}
  table.diff {{ width: 100%; border-collapse: collapse; background: #fff; border-radius: 8px;
               overflow: hidden; font-size: 13px; }}
  table.diff th, table.diff td {{ border: 1px solid #eee; padding: 8px 6px; text-align: left; }}
  table.diff th {{ background: #fafafa; color: #666; }}
  .nodiff {{ color: #cf1322; font-size: 14px; }}
  .foot {{ margin-top: 16px; font-size: 12px; color: #999; }}
</style></head>
<body>
  <div class="head">
    <div><span class="badge">{signal_label}</span></div>
    <h2 style="margin:8px 0 4px;">查重复核工单 #{review.get('id')}</h2>
    <div>置信度：{confidence:.0%} ｜ 状态：{review.get('status','pending')}</div>
    <div style="font-size:13px;color:#888;">财务确认重复后相关票据不进台账；误报请标记豁免并沉淀规则</div>
  </div>
  <div class="row">{''.join(cards)}</div>
  {diff_rows}
  <div class="foot">本工单由 receipt-compliance v4.5.0 生成 ｜ 处置请使用 ledger_db.py --resolve-review</div>
</body></html>"""

    out.write_text(html, encoding="utf-8")
    return str(out)


def _esc(v: Any) -> str:
    if v is None:
        return "—"
    s = str(v)
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def _fmt_money(v: Any) -> str:
    if v is None:
        return "—"
    try:
        return f"¥{float(v):,.2f}"
    except (TypeError, ValueError):
        return _esc(v)


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("用法: python review_render.py <review_json> <output.html>")
        sys.exit(1)
    review = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    print(render_review_html(review, sys.argv[2]))
