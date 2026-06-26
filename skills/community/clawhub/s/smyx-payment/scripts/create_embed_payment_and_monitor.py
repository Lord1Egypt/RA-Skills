#!/usr/bin/env python3
"""Create a payment hosted embed page and monitor payment status.

This avoids WebChat push: the assistant returns [embed ref="..."] once, and
that hosted page polls its own non-sensitive status.json. When payment succeeds,
this process updates status.json with success + balance.

Security:
- privateKey only from cloud create_order response and only in this process memory.
- privateKey is never written, printed, argv/env, or exposed to the browser.
- status.json contains only non-sensitive status/result/balance fields.
"""

from __future__ import annotations

import argparse
import contextlib
import html
import io
import json
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path

WORKSPACE = "/root/.openclaw/workspace"
if WORKSPACE not in sys.path:
    sys.path.insert(0, WORKSPACE)

from skills.smyx_payment.scripts.open_id import require_open_id
from skills.smyx_payment.scripts.pay_with_cloud_order import (
    create_payment_with_cloud_order,
    extract_private_key_from_order,
    query_alipay_trade_status,
)
from skills.smyx_payment.scripts.query import query_account
from skills.smyx_payment.scripts.recharge import create_recharge_order

CANVAS_DOC_ROOT = Path("/root/.openclaw/canvas/documents")
TMP_RESULT_FILE = Path("/tmp/payment_success.json")


def get_order_no(obj: dict) -> str | None:
    data = obj.get("data") if isinstance(obj.get("data"), dict) else {}
    return obj.get("orderNo") or obj.get("order_no") or data.get("orderNo") or data.get("order_no")


def emit(obj: dict) -> None:
    print(json.dumps(obj, ensure_ascii=False), flush=True)


def safe_ref(s: str) -> str:
    return re.sub(r"[^A-Za-z0-9_-]", "-", s)[:120]


def atomic_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + f".tmp.{os.getpid()}")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(path)


def write_html(doc_dir: Path, payment_url: str, order_no: str, amount: float, package_name: str, uses: int) -> None:
    page = f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>支付状态 - {html.escape(order_no)}</title>
<style>
  :root {{ color-scheme: light dark; }}
  body {{ margin:0; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Noto Sans SC',Arial,sans-serif; background:#f6f8fb; color:#172033; }}
  .wrap {{ max-width: 420px; margin: 0 auto; padding: 14px; }}
  .card {{ background: #fff; border: 2px solid #1677ff; border-radius: 16px; box-shadow: 0 8px 28px rgba(0,0,0,.14); overflow: hidden; }}
  .head {{ padding: 12px 14px; background: linear-gradient(135deg,#1677ff,#54a6ff); color:white; }}
  .title {{ font-weight: 800; font-size: 17px; }}
  .sub {{ opacity:.92; margin-top:4px; font-size: 13px; }}
  .body {{ padding: 12px; }}
  .grid {{ display:grid; grid-template-columns: 82px 1fr; gap:6px 8px; font-size: 13px; margin-bottom: 10px; }}
  .k {{ color:#6b7280; }}
  .v {{ font-weight:600; word-break:break-all; }}
  iframe {{ width:300px; height:300px; border:0; border-radius:12px; display:block; margin: 8px auto; box-shadow: inset 0 0 0 1px rgba(0,0,0,.08); }}
  .pay-link {{ display:block; width:max-content; max-width:100%; margin: 10px auto 0; padding: 10px 14px; border-radius: 10px; background:#1677ff; color:#fff; text-decoration:none; font-weight:700; }}
  .status {{ margin-top: 10px; border-radius: 12px; padding: 10px 12px; font-weight: 700; text-align:center; }}
  .waiting {{ background:#fff7e6; color:#ad6800; }}
  .success {{ background:#e9fbe9; color:#237804; }}
  .timeout {{ background:#fff1f0; color:#a8071a; }}
  .details {{ margin-top: 10px; font-size: 13px; line-height:1.65; background:#f7fafc; border-radius:12px; padding:10px; display:none; }}
  .details.show {{ display:block; }}
  .hint {{ margin-top:8px; font-size:12px; color:#6b7280; text-align:center; }}
  @media (prefers-color-scheme: dark) {{ body{{background:#111827;color:#e5e7eb}} .card{{background:#1f2937}} .k{{color:#9ca3af}} .details{{background:#111827}} }}
</style>
</head>
<body>
<div class="wrap">
  <div class="card">
    <div class="head">
      <div class="title">🦞 测试套餐支付</div>
      <div class="sub">扫码后本卡片会自动刷新状态，无需再发“已支付”</div>
    </div>
    <div class="body">
      <div class="grid">
        <div class="k">订单号</div><div class="v">{html.escape(order_no)}</div>
        <div class="k">套餐</div><div class="v">{html.escape(package_name)}</div>
        <div class="k">金额</div><div class="v">¥{amount:.2f}</div>
        <div class="k">次数</div><div class="v">{uses} 次</div>
      </div>
      <iframe src="{html.escape(payment_url, quote=True)}" scrolling="no"></iframe>
      <a class="pay-link" href="{html.escape(payment_url, quote=True)}" target="_blank" rel="noopener noreferrer">👉 打开支付宝付款页面</a>
      <div id="status" class="status waiting">⏳ 等待支付中，自动刷新...</div>
      <div id="details" class="details"></div>
      <div class="hint">每 2 秒自动检查一次状态；页面只读取非敏感 status.json。</div>
    </div>
  </div>
</div>
<script>
async function loadStatus() {{
  try {{
    const res = await fetch('status.json?ts=' + Date.now(), {{ cache: 'no-store' }});
    const s = await res.json();
    const el = document.getElementById('status');
    const d = document.getElementById('details');
    if (s.status === 'success') {{
      el.className = 'status success';
      el.textContent = '✅ 支付成功，余额已更新';
      const b = s.balance || {{}};
      d.className = 'details show';
      d.innerHTML = `
        <b>支付结果</b><br>
        订单号：${{escapeHtml(s.order_no || '')}}<br>
        金额：¥${{escapeHtml(s.total_amount || '')}}<br>
        支付时间：${{escapeHtml(s.send_pay_date || '')}}<br>
        支付宝交易号：${{escapeHtml(s.trade_no || '')}}<br>
        检测时间：${{escapeHtml(s.detected_at || '')}}<br><br>
        <b>当前余额</b><br>
        总可用次数：${{escapeHtml(String(b.totalRecharged ?? ''))}} 次<br>
        已使用次数：${{escapeHtml(String(b.usedCount ?? ''))}} 次<br>
        剩余次数：${{escapeHtml(String((b.remainingUses ?? b.balance) ?? ''))}} 次
      `;
      return;
    }}
    if (s.status === 'timeout') {{
      el.className = 'status timeout';
      el.textContent = '⌛ 暂未检测到支付成功，可刷新或稍后再看';
      return;
    }}
    if (s.trade_status) {{
      el.textContent = '⏳ 当前状态：' + s.trade_status + '，继续自动刷新...';
    }}
  }} catch (e) {{
    // Keep waiting silently; file may be mid-write or unavailable briefly.
  }}
  setTimeout(loadStatus, 2000);
}}
function escapeHtml(x) {{
  return x.replace(/[&<>"']/g, c => ({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[c]));
}}
loadStatus();
</script>
</body>
</html>
"""
    doc_dir.mkdir(parents=True, exist_ok=True)
    (doc_dir / "index.html").write_text(page, encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--amount", type=float, default=0.01)
    ap.add_argument("--package-name", default="测试套餐")
    ap.add_argument("--uses", type=int, default=10)
    ap.add_argument("--subject", default="小龙虾主厨 - 测试套餐充值")
    ap.add_argument("--timeout-seconds", type=int, default=180)
    ap.add_argument("--interval-seconds", type=int, default=2)
    args = ap.parse_args()

    open_id = require_open_id(None)
    with contextlib.redirect_stdout(io.StringIO()):
        order = create_recharge_order(
            phone=open_id,
            amount=args.amount,
            package_type=args.package_name,
            detail=f"增值账户续费 - {args.package_name}",
        )
    if not isinstance(order, dict):
        emit({"event": "create_order_failed", "success": False})
        return 2
    order_no = get_order_no(order)
    if not order_no:
        emit({"event": "create_order_failed", "success": False, "message": "missing orderNo"})
        return 2
    private_key = extract_private_key_from_order(order)
    pay = create_payment_with_cloud_order(
        cloud_order_no=order_no,
        phone=open_id,
        amount=args.amount,
        subject=args.subject,
        package_name=args.package_name,
        uses=args.uses,
        private_key_string=private_key,
    )
    payment_url = pay.get("pay_url")
    ref = safe_ref(f"smyx-pay-{order_no}")
    doc_dir = CANVAS_DOC_ROOT / ref
    status_path = doc_dir / "status.json"
    write_html(doc_dir, payment_url, order_no, args.amount, args.package_name, args.uses)
    atomic_json(status_path, {
        "status": "waiting",
        "order_no": order_no,
        "amount": f"{args.amount:.2f}",
        "package_name": args.package_name,
        "uses": args.uses,
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    })
    emit({"event": "embed_ready", "success": True, "ref": ref, "order_no": order_no, "url": f"/__openclaw__/canvas/documents/{ref}/index.html"})

    start = time.time()
    last_trade = ""
    while time.time() - start <= args.timeout_seconds:
        s = query_alipay_trade_status(order_no, private_key_string=private_key)
        trade = s.get("trade_status", "")
        if trade and trade != last_trade:
            last_trade = trade
            atomic_json(status_path, {"status": "waiting", "order_no": order_no, "trade_status": trade, "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
            emit({"event": "payment_status", "order_no": order_no, "trade_status": trade})
        if trade in ("TRADE_SUCCESS", "TRADE_FINISHED"):
            try:
                balance = query_account(open_id) or {}
            except Exception as e:
                balance = {"_error": str(e)}
            result = {
                "status": "success",
                "order_no": order_no,
                "total_amount": s.get("total_amount", "0.00"),
                "send_pay_date": s.get("send_pay_date", ""),
                "trade_no": s.get("trade_no", ""),
                "detected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "balance": balance,
            }
            atomic_json(status_path, result)
            atomic_json(TMP_RESULT_FILE, result)
            emit({"event": "payment_success", "success": True, **result})
            return 0
        if trade == "TRADE_CLOSED":
            atomic_json(status_path, {"status": "closed", "order_no": order_no, "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
            return 3
        time.sleep(args.interval_seconds)

    atomic_json(status_path, {"status": "timeout", "order_no": order_no, "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
    emit({"event": "payment_timeout", "success": False, "order_no": order_no})
    return 4


if __name__ == "__main__":
    raise SystemExit(main())
