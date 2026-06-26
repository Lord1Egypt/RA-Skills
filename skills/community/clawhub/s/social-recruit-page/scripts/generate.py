#!/usr/bin/env python3
"""
recruit-page 生成脚本
用法：
  python3 generate.py                          # 用默认配置生成
  python3 generate.py --config config.json     # 用 JSON 配置生成
  python3 generate.py --output /tmp/out.png    # 指定输出路径
  python3 generate.py --send-feishu --receive-id ou_xxx --app-id xxx --app-secret xxx
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


def build_html(c: dict) -> str:
    brand     = c.get("brand_name", "私人圈子")
    tagline   = c.get("tagline", "AI 时代的企业家私人智囊团")
    badge     = c.get("badge", "PRIVATE CIRCLE · 私人圈子")
    hero_intro = c.get("hero_intro", "你不缺信息，你缺的是<strong>一个真正懂你的人</strong>在身边。")
    f_name    = c.get("founder_name", "谢导")
    f_emoji   = c.get("founder_emoji", "🔍")
    f_intro   = c.get("founder_intro", "")
    f_tags    = c.get("founder_tags", [])
    price     = c.get("price", "9,980")
    unit      = c.get("price_unit", "¥")
    quota     = c.get("quota", "30")
    footer_q  = c.get("footer_quote", "真正的价值，不在于你认识多少人。")
    year      = c.get("year", "2026")
    services  = c.get("services", [])
    for_who   = c.get("for_who", [])
    perks     = c.get("perks", [])

    tags_html = "".join(f'<span class="tag">{t}</span>' for t in f_tags)

    services_html = ""
    for i, s in enumerate(services, 1):
        services_html += f"""
        <div class="service-item">
          <div class="service-num">0{i}</div>
          <div class="service-content">
            <h3>{s['title']}</h3>
            <span class="service-tag">{s.get('tag','')}</span>
            <p>{s['desc']}</p>
          </div>
        </div>"""

    who_html = ""
    for w in for_who:
        who_html += f"""
        <div class="who-item">
          <div class="icon">{w['icon']}</div>
          <h4>{w['title']}</h4>
          <p>{w['desc']}</p>
        </div>"""

    perks_html = "".join(f"<li>{p}</li>" for p in perks)

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{brand}</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600;700;900&family=Noto+Sans+SC:wght@300;400;500;700&display=swap');
  *{{margin:0;padding:0;box-sizing:border-box}}
  body{{background:#0a0a0a;color:#e8d5b0;font-family:'Noto Sans SC',sans-serif;width:750px;margin:0 auto}}
  .hero{{background:linear-gradient(160deg,#1a1208 0%,#0d0d0d 40%,#0a0a0a 100%);padding:80px 60px 60px;text-align:center;border-bottom:1px solid #2a2010;position:relative;overflow:hidden}}
  .hero::before{{content:'';position:absolute;top:-100px;left:-100px;right:-100px;height:300px;background:radial-gradient(ellipse at center,rgba(212,175,55,.12) 0%,transparent 70%)}}
  .hero-badge{{display:inline-block;border:1px solid #c9a227;color:#c9a227;font-size:13px;letter-spacing:4px;padding:6px 20px;margin-bottom:36px;font-family:'Noto Serif SC',serif}}
  .hero-title{{font-family:'Noto Serif SC',serif;font-size:52px;font-weight:900;color:#f0e0a0;line-height:1.2;margin-bottom:16px;text-shadow:0 0 40px rgba(212,175,55,.3)}}
  .hero-title span{{color:#c9a227}}
  .hero-subtitle{{font-size:18px;color:#9a8060;letter-spacing:2px;margin-bottom:48px;font-weight:300}}
  .hero-divider{{width:60px;height:2px;background:linear-gradient(90deg,transparent,#c9a227,transparent);margin:0 auto 48px}}
  .hero-intro{{font-size:16px;line-height:2;color:#c8b080;max-width:560px;margin:0 auto;font-weight:300}}
  .hero-intro strong{{color:#e8d070;font-weight:500}}
  .founder{{padding:64px 60px;background:#080808;border-bottom:1px solid #1e1810}}
  .section-label{{font-size:11px;letter-spacing:5px;color:#6a5830;text-transform:uppercase;margin-bottom:40px;text-align:center}}
  .founder-card{{display:flex;gap:36px;align-items:flex-start}}
  .founder-avatar{{width:100px;height:100px;border-radius:50%;border:2px solid #c9a227;background:linear-gradient(135deg,#2a1f08,#1a1408);display:flex;align-items:center;justify-content:center;font-size:36px;flex-shrink:0;box-shadow:0 0 20px rgba(201,162,39,.2)}}
  .founder-info h3{{font-family:'Noto Serif SC',serif;font-size:24px;color:#f0e0a0;margin-bottom:8px}}
  .founder-info .title-tags{{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:20px}}
  .tag{{background:rgba(201,162,39,.1);border:1px solid rgba(201,162,39,.3);color:#c9a227;font-size:12px;padding:4px 12px;border-radius:2px;letter-spacing:1px}}
  .founder-info p{{font-size:15px;color:#9a8060;line-height:1.9;font-weight:300}}
  .founder-info p strong{{color:#c8b080}}
  .for-who{{padding:64px 60px;background:linear-gradient(180deg,#0a0a0a 0%,#0d0b08 100%);border-bottom:1px solid #1e1810}}
  .section-title{{font-family:'Noto Serif SC',serif;font-size:30px;color:#f0e0a0;text-align:center;margin-bottom:12px}}
  .section-title span{{color:#c9a227}}
  .section-desc{{text-align:center;color:#7a6840;font-size:14px;margin-bottom:48px;letter-spacing:1px}}
  .who-grid{{display:grid;grid-template-columns:1fr 1fr;gap:16px}}
  .who-item{{background:rgba(201,162,39,.04);border:1px solid rgba(201,162,39,.15);padding:24px 28px;border-radius:2px}}
  .who-item .icon{{font-size:24px;margin-bottom:12px}}
  .who-item h4{{font-size:15px;color:#e8d5b0;margin-bottom:8px;font-weight:500}}
  .who-item p{{font-size:13px;color:#7a6840;line-height:1.7}}
  .services{{padding:64px 60px;background:#080808;border-bottom:1px solid #1e1810}}
  .service-item{{display:flex;gap:28px;margin-bottom:48px;padding-bottom:48px;border-bottom:1px solid #1a1408}}
  .service-item:last-child{{margin-bottom:0;padding-bottom:0;border-bottom:none}}
  .service-num{{font-family:'Noto Serif SC',serif;font-size:48px;color:rgba(201,162,39,.15);line-height:1;flex-shrink:0;width:60px;font-weight:900}}
  .service-content h3{{font-family:'Noto Serif SC',serif;font-size:22px;color:#f0e0a0;margin-bottom:8px}}
  .service-content .service-tag{{display:inline-block;background:rgba(201,162,39,.12);color:#c9a227;font-size:11px;padding:3px 10px;margin-bottom:16px;letter-spacing:2px}}
  .service-content p{{font-size:15px;color:#8a7050;line-height:1.9;font-weight:300}}
  .service-content p strong{{color:#c8b080}}
  .pricing{{padding:64px 60px;background:linear-gradient(160deg,#0f0c04 0%,#0a0a0a 100%);border-bottom:1px solid #1e1810;text-align:center}}
  .price-box{{border:1px solid rgba(201,162,39,.4);padding:56px 40px;max-width:480px;margin:0 auto 40px;position:relative;background:rgba(201,162,39,.03)}}
  .price-box::before{{content:'首期限定';position:absolute;top:-1px;right:32px;background:#c9a227;color:#0a0a0a;font-size:11px;letter-spacing:2px;padding:4px 14px;font-weight:700}}
  .price-amount{{font-family:'Noto Serif SC',serif;font-size:72px;font-weight:900;color:#c9a227;line-height:1;margin-bottom:8px}}
  .price-amount .currency{{font-size:32px;vertical-align:top;margin-top:14px;display:inline-block}}
  .price-period{{font-size:14px;color:#6a5830;letter-spacing:2px;margin-bottom:36px}}
  .price-divider{{width:40px;height:1px;background:rgba(201,162,39,.3);margin:0 auto 36px}}
  .price-perks{{list-style:none;text-align:left}}
  .price-perks li{{font-size:15px;color:#9a8060;padding:10px 0;border-bottom:1px solid rgba(201,162,39,.08);display:flex;align-items:center;gap:12px}}
  .price-perks li:last-child{{border-bottom:none}}
  .price-perks li::before{{content:'✦';color:#c9a227;font-size:10px;flex-shrink:0}}
  .quota-note{{font-size:14px;color:#5a4820;letter-spacing:1px}}
  .quota-note strong{{color:#c9a227;font-size:20px;font-family:'Noto Serif SC',serif}}
  .filter{{padding:64px 60px;background:#080808;border-bottom:1px solid #1e1810}}
  .filter-steps{{margin-top:40px}}
  .filter-step{{display:flex;gap:24px;margin-bottom:32px;align-items:flex-start}}
  .step-num{{width:40px;height:40px;border:1px solid #c9a227;display:flex;align-items:center;justify-content:center;font-family:'Noto Serif SC',serif;font-size:16px;color:#c9a227;flex-shrink:0}}
  .step-content h4{{font-size:16px;color:#e8d5b0;margin-bottom:6px;padding-top:8px;font-weight:500}}
  .step-content p{{font-size:13px;color:#6a5830;line-height:1.7}}
  .footer{{padding:56px 60px;background:linear-gradient(180deg,#0a0a0a 0%,#050503 100%);text-align:center}}
  .footer-quote{{font-family:'Noto Serif SC',serif;font-size:20px;color:#8a7050;line-height:1.8;margin-bottom:48px;font-style:italic}}
  .footer-quote strong{{color:#c9a227}}
  .cta-btn{{display:inline-block;border:1px solid #c9a227;color:#0a0a0a;background:#c9a227;font-size:15px;letter-spacing:4px;padding:16px 60px;margin-bottom:24px;font-weight:700}}
  .cta-note{{font-size:12px;color:#4a3818;letter-spacing:1px;margin-bottom:48px}}
  .footer-brand{{font-size:12px;color:#3a2c12;letter-spacing:3px}}
  .footer-brand span{{color:#5a4820}}
</style>
</head>
<body>

<div class="hero">
  <div class="hero-badge">{badge}</div>
  <div class="hero-title">{brand}</div>
  <div class="hero-subtitle">{tagline}</div>
  <div class="hero-divider"></div>
  <div class="hero-intro">{hero_intro}</div>
</div>

<div class="founder">
  <div class="section-label">FOUNDER · 发起人</div>
  <div class="founder-card">
    <div class="founder-avatar">{f_emoji}</div>
    <div class="founder-info">
      <h3>{f_name}</h3>
      <div class="title-tags">{tags_html}</div>
      <p>{f_intro}</p>
    </div>
  </div>
</div>

<div class="for-who">
  <div class="section-label">FOR WHO · 为谁设计</div>
  <div class="section-title">这个圈子，<span>不是为所有人</span>准备的</div>
  <div class="section-desc">以下四种人，你至少占一条</div>
  <div class="who-grid">{who_html}</div>
</div>

<div class="services">
  <div class="section-label">SERVICES · 核心服务</div>
  <div class="section-title" style="margin-bottom:48px">三件事，<span>真正有用</span></div>
  {services_html}
</div>

<div class="pricing">
  <div class="section-label">PRICING · 年费</div>
  <div class="section-title" style="margin-bottom:48px"><span>一个决定</span>，改变一年的质量</div>
  <div class="price-box">
    <div class="price-amount"><span class="currency">{unit}</span>{price}</div>
    <div class="price-period">/ 年 · PER YEAR</div>
    <div class="price-divider"></div>
    <ul class="price-perks">{perks_html}</ul>
  </div>
  <div class="quota-note">首期仅招募 <strong>{quota}</strong> 人 · 名额满即关闭</div>
</div>

<div class="filter">
  <div class="section-label">PROCESS · 入圈流程</div>
  <div class="section-title" style="margin-bottom:8px">不是<span>所有人</span>都能进</div>
  <div class="section-desc">谢导亲自面试，确保每一位成员都值得认识</div>
  <div class="filter-steps">
    <div class="filter-step"><div class="step-num">01</div><div class="step-content"><h4>提交申请</h4><p>填写简单表格：你是谁、你在做什么、你希望从圈子里得到什么</p></div></div>
    <div class="filter-step"><div class="step-num">02</div><div class="step-content"><h4>谢导审阅</h4><p>谢导亲自阅读每一份申请，3 个工作日内给出回复</p></div></div>
    <div class="filter-step"><div class="step-num">03</div><div class="step-content"><h4>一对一面谈</h4><p>30 分钟视频通话，谢导想了解你，也给你机会了解圈子</p></div></div>
    <div class="filter-step"><div class="step-num">04</div><div class="step-content"><h4>正式入圈</h4><p>双向确认后完成年费，正式成为成员，立即享受所有权益</p></div></div>
  </div>
</div>

<div class="footer">
  <div class="footer-quote">{footer_q}</div>
  <div class="cta-btn">申请入圈</div>
  <div class="cta-note">提交申请 · 无需付费 · 双向选择</div>
  <div class="footer-brand">{brand} <span>© {year}</span></div>
</div>

</body>
</html>"""


def screenshot(html_content: str, output_path: str) -> bool:
    with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
        f.write(html_content)
        tmp = f.name
    try:
        r = subprocess.run(
            ["playwright", "screenshot", "--browser", "chromium",
             "--full-page", "--viewport-size", "750,900",
             f"file://{tmp}", output_path],
            capture_output=True, text=True, timeout=60
        )
        if r.returncode != 0:
            print(f"[错误] Playwright: {r.stderr}", file=sys.stderr)
            return False
        print(f"[✅] 图片: {output_path}")
        return True
    finally:
        os.unlink(tmp)


def send_feishu(image_path: str, receive_id: str, app_id: str, app_secret: str,
                receive_id_type: str = "open_id") -> bool:
    import urllib.request
    # token
    req = urllib.request.Request(
        "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        data=json.dumps({"app_id": app_id, "app_secret": app_secret}).encode(),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=15) as r:
        token = json.loads(r.read()).get("tenant_access_token", "")
    if not token:
        print("[错误] 获取飞书 token 失败", file=sys.stderr); return False

    # 上传图片
    up = subprocess.run(
        ["curl", "-s", "-X", "POST", "https://open.feishu.cn/open-apis/im/v1/images",
         "-H", f"Authorization: Bearer {token}",
         "-F", "image_type=message", "-F", f"image=@{image_path}"],
        capture_output=True, text=True, timeout=30
    )
    image_key = json.loads(up.stdout).get("data", {}).get("image_key", "")
    if not image_key:
        print(f"[错误] 上传失败: {up.stdout}", file=sys.stderr); return False

    # 发消息
    req2 = urllib.request.Request(
        f"https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type={receive_id_type}",
        data=json.dumps({"receive_id": receive_id, "msg_type": "image",
                         "content": json.dumps({"image_key": image_key})}).encode(),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req2, timeout=15) as r:
        resp = json.loads(r.read())
    if resp.get("code") == 0:
        print(f"[✅] 飞书发送成功"); return True
    print(f"[错误] 发送失败: {resp}", file=sys.stderr); return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", help="JSON 配置文件")
    parser.add_argument("--output", default="/tmp/recruit_output.png")
    parser.add_argument("--send-feishu", action="store_true")
    parser.add_argument("--receive-id")
    parser.add_argument("--receive-id-type", default="open_id")
    parser.add_argument("--app-id")
    parser.add_argument("--app-secret")
    args = parser.parse_args()

    config = {}
    if args.config:
        with open(args.config, encoding="utf-8") as f:
            config = json.load(f)

    html = build_html(config)
    if not screenshot(html, args.output):
        sys.exit(1)

    if args.send_feishu:
        send_feishu(args.output, args.receive_id, args.app_id, args.app_secret,
                    args.receive_id_type)


if __name__ == "__main__":
    main()
