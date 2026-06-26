#!/usr/bin/env python3
"""Build WeChat article HTML and create/update draft."""
import json, sys, os

# Read vars
with open('/tmp/wechat_vars.sh') as f:
    lines = f.read().strip().split('\n')
for line in lines:
    k, v = line.split('=', 1)
    os.environ[k] = v

BANNER_URL = os.environ['BANNER_URL']
DIVIDER_URL = os.environ['DIVIDER_URL']
COVER_MEDIA_ID = os.environ['COVER_MEDIA_ID']
TOKEN = os.environ['TOKEN']

def p(text, accent=False, em=False):
    """Create a paragraph with optional accent/highlight spans."""
    p_style = 'font-size:15px;line-height:2;color:#333;margin:0 0 22px;letter-spacing:1px;word-break:normal;white-space:normal;'
    if accent:
        text = text.replace('{{A}}', '<span style="color:#d4a574;font-weight:500;">').replace('{{/A}}', '</span>')
    return f'<p style="{p_style}">{text}</p>'

def hr():
    return '<section style="text-align:center;padding:6px 20px;word-break:normal;white-space:normal;"><span style="display:inline-block;width:32px;height:1px;background:#d4a574;"></span></section>'

def highlight_card(text, prefix="毕竟——"):
    return f'''<section style="padding:4px 20px;word-break:normal;white-space:normal;">
<div style="margin:16px 0;padding:24px;background:#f8f6f3;text-align:center;">
  <p style="font-size:14px;color:#999;margin:0 0 10px;letter-spacing:2px;">{prefix}</p>
  <p style="font-size:22px;font-weight:400;color:#1a1a2e;margin:0;letter-spacing:3px;line-height:1.8;">{text}</p>
</div>
</section>'''

# Build article text as paragraphs
# Read the article
with open('/mnt/d/openclaw-workspace/skills/wechat-mp-editor/功利主义推文稿.md') as f:
    article_text = f.read()

# Split by double newlines (paragraphs)
paragraphs = article_text.strip().split('\n\n')

body_parts = []
for para in paragraphs:
    line = para.strip()
    if not line:
        continue
    if line == '---':
        body_parts.append(hr())
    elif line.startswith('> '):
        # Blockquote
        quote_text = line[2:]
        body_parts.append(
            f'<div style="margin:16px 20px;padding:16px 20px;background:#f8f6f3;border-left:3px solid #d4a574;word-break:normal;white-space:normal;">'
            f'<p style="font-size:15px;line-height:2;color:#333;margin:0;letter-spacing:1px;">{quote_text}</p></div>'
        )
    else:
        body_parts.append(p(line))

body_html = '\n'.join(body_parts)

# Build full HTML
full_html = f'''<section style="padding:0;margin:0;background:#fff;word-break:normal;white-space:normal;">

<!-- Banner -->
<section style="width:100%;margin:0;padding:0;">
  <img src="{BANNER_URL}" style="width:100%;display:block;" />
</section>

<!-- Header -->
<section style="padding:44px 20px 16px;text-align:center;word-break:normal;white-space:normal;">
  <p style="font-size:13px;color:#b8b8b8;letter-spacing:4px;margin:0 0 18px;font-weight:300;">I N S I G H T</p>
  <p style="font-size:22px;font-weight:400;color:#1a1a2e;margin:0 0 8px;letter-spacing:2px;">我们活成了一台不停计算的机器</p>
  <p style="font-size:13px;color:#aaa;margin:0;">2026 · 05 · 21</p>
</section>

{hr()}

<!-- Body -->
<section style="padding:32px 20px 8px;word-break:normal;white-space:normal;">
{body_html}
</section>

{hr()}

<!-- Highlight card -->
{highlight_card(
  '没有什么，比「没有为什么」更有用。',
  '毕竟——'
)}

<!-- Footer -->
<div style="padding:36px 0 40px;text-align:center;">
  <p style="font-size:11px;color:#888;letter-spacing:2px;margin:0;">巡梦人</p>
  <p style="font-size:10px;color:#a09080;margin:8px 0 0;">从一颗星星开始，温暖整个宇宙</p>
</div>

</section>'''

# Check content length
print(f"HTML content length: {len(full_html)} chars")

# Create draft
api_url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={TOKEN}"
payload = {
    "articles": [{
        "title": "我们活成了一台不停计算的机器",
        "author": "巡梦人",
        "digest": "你有没有发现，我们每天都在算账？每一个选择都被拆解成收益和风险，我们活成了一张不停更新的损益表。但看完《给阿嬷的情书》之后，我总觉得有什么东西算漏了。",
        "content": full_html,
        "thumb_media_id": COVER_MEDIA_ID,
        "need_open_comment": 0,
        "only_fans_can_comment": 0
    }]
}

# Save for inspection
with open('/tmp/draft_payload.json', 'w') as f:
    json.dump(payload, f, ensure_ascii=False)

print("Draft payload saved to /tmp/draft_payload.json")

# Submit to API
import urllib.request
req = urllib.request.Request(
    api_url,
    data=json.dumps(payload, ensure_ascii=False).encode('utf-8'),
    headers={'Content-Type': 'application/json'}
)
try:
    resp = urllib.request.urlopen(req)
    result = json.loads(resp.read())
    print(f"API Response: {json.dumps(result, ensure_ascii=False, indent=2)}")
    if 'media_id' in result:
        print(f"✅ Draft created! media_id: {result['media_id']}")
    else:
        print(f"❌ Error: {result}")
except Exception as e:
    print(f"❌ API Error: {e}")
