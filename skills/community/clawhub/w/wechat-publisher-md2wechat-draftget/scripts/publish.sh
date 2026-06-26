#!/usr/bin/env bash
# wechat-publisher: 使用 md2wechat create_draft 正式推送微信公众号草稿并核验
# Usage: ./publish.sh <article.md|article.html> <cover-image> [title] [author] [digest]

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

usage() {
  cat <<'EOF'
Usage:
  publish.sh <article.md|article.html> <cover-image> [title] [author] [digest]

正式链路：
  md2wechat inspect/preview/convert(若输入 Markdown)
  -> md2wechat upload_image cover
  -> 生成 draft.json
  -> md2wechat create_draft draft.json
  -> 微信 draft/get 后台核验

Examples:
  ./scripts/publish.sh article.html cover.png "文章标题" "野哥" "摘要"
  ./scripts/publish.sh article.md cover.png "文章标题" "野哥"

Notes:
  - 输入 HTML 时默认认为它已经是公众号兼容 HTML。
  - 输入 Markdown 时脚本会先用 md2wechat 转 HTML；AI 模式生成的 HTML应由外层 Agent 先落盘后再传入本脚本。
EOF
}

fail() { echo -e "${RED}❌ $*${NC}" >&2; exit 1; }
info() { echo -e "${YELLOW}$*${NC}"; }
ok() { echo -e "${GREEN}$*${NC}"; }

if [[ $# -lt 1 || "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

ARTICLE_PATH="$1"
COVER_PATH="${2:-}"
TITLE="${3:-}"
AUTHOR="${4:-野哥}"
DIGEST="${5:-}"

[[ -f "$ARTICLE_PATH" ]] || fail "文章文件不存在: $ARTICLE_PATH"
[[ -n "$COVER_PATH" ]] || fail "必须提供封面图片路径"
[[ -f "$COVER_PATH" ]] || fail "封面图片不存在: $COVER_PATH"
command -v md2wechat >/dev/null 2>&1 || fail "md2wechat CLI 未安装或不在 PATH"
command -v python3 >/dev/null 2>&1 || fail "python3 不可用"

WORKDIR="$(cd "$(dirname "$ARTICLE_PATH")" && pwd)"
ARTICLE_ABS="$(cd "$(dirname "$ARTICLE_PATH")" && pwd)/$(basename "$ARTICLE_PATH")"
COVER_ABS="$(cd "$(dirname "$COVER_PATH")" && pwd)/$(basename "$COVER_PATH")"
BASE_NAME="$(basename "$ARTICLE_PATH")"
STEM="${BASE_NAME%.*}"
HTML_PATH="$ARTICLE_ABS"
DRAFT_JSON="$WORKDIR/${STEM}.md2wechat-create-draft.json"
CREATE_RESULT="$WORKDIR/${STEM}.md2wechat-create-draft-result.json"
VERIFY_JSON="$WORKDIR/${STEM}.md2wechat-create-draft-verify.json"
UPLOAD_JSON="$WORKDIR/${STEM}.md2wechat-cover-upload.json"

info "🔎 校验 md2wechat 配置..."
md2wechat config validate --json >/dev/null

if [[ "$ARTICLE_ABS" =~ \.md$|\.markdown$ ]]; then
  info "🔎 inspect / preview Markdown..."
  (cd "$WORKDIR" && md2wechat inspect "$ARTICLE_ABS" --json > "$WORKDIR/${STEM}.md2wechat-inspect.json")
  (cd "$WORKDIR" && md2wechat preview "$ARTICLE_ABS" --json > "$WORKDIR/${STEM}.md2wechat-preview.json")
  HTML_PATH="$WORKDIR/${STEM}.md2wechat-layout.html"
  info "🧩 转换 Markdown 为 HTML: $HTML_PATH"
  (cd "$WORKDIR" && md2wechat convert "$ARTICLE_ABS" --output "$HTML_PATH" --json > "$WORKDIR/${STEM}.md2wechat-convert.json")
fi

[[ -f "$HTML_PATH" ]] || fail "HTML 产物不存在: $HTML_PATH"

info "🖼️ 上传封面..."
(cd "$WORKDIR" && md2wechat upload_image "$COVER_ABS" --json > "$UPLOAD_JSON")

info "🧾 生成 draft.json..."
python3 - "$HTML_PATH" "$UPLOAD_JSON" "$DRAFT_JSON" "$TITLE" "$AUTHOR" "$DIGEST" <<'PY'
import json, pathlib, re, sys
html_path=pathlib.Path(sys.argv[1])
upload_json=pathlib.Path(sys.argv[2])
out=pathlib.Path(sys.argv[3])
title=sys.argv[4].strip()
author=sys.argv[5].strip() or '野哥'
digest=sys.argv[6].strip()
html=html_path.read_text(encoding='utf-8')
upload=json.loads(upload_json.read_text(encoding='utf-8'))
media_id=(upload.get('data') or {}).get('media_id')
if not media_id:
    raise SystemExit('封面上传结果中没有 media_id')
if not title:
    m=re.search(r'<h1[^>]*>(.*?)</h1>', html, flags=re.I|re.S)
    if m:
        title=re.sub(r'<[^>]+>','',m.group(1)).strip()
if not title:
    title=html_path.stem
if len(title)>32:
    title=title[:32]
if len(author)>16:
    author=author[:16]
if not digest:
    text=re.sub(r'(?is)<(script|style)[^>]*>.*?</\\1>',' ',html)
    text=re.sub(r'<[^>]+>',' ',text)
    text=' '.join(text.split())
    digest=text[:120]
if len(digest)>128:
    digest=digest[:128]
draft={'articles':[{'title':title,'author':author,'digest':digest,'content':html,'thumb_media_id':media_id,'show_cover_pic':0}]}
out.write_text(json.dumps(draft,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'draft_json':str(out),'title':title,'author':author,'digest_len':len(digest),'content_len':len(html),'thumb_media_id':media_id},ensure_ascii=False,indent=2))
PY

info "🚀 create_draft 推送草稿..."
(cd "$WORKDIR" && md2wechat create_draft "$DRAFT_JSON" --json > "$CREATE_RESULT")
cat "$CREATE_RESULT"

info "✅ draft/get 后台核验..."
python3 - "$CREATE_RESULT" "$DRAFT_JSON" "$VERIFY_JSON" <<'PY'
import json, os, pathlib, sys, urllib.parse, urllib.request, yaml
create_result=pathlib.Path(sys.argv[1])
draft_json=pathlib.Path(sys.argv[2])
out=pathlib.Path(sys.argv[3])
created=json.loads(create_result.read_text(encoding='utf-8'))
media_id=(created.get('data') or {}).get('media_id')
if not media_id:
    raise SystemExit('create_draft 结果中没有 media_id')
draft_req=json.loads(draft_json.read_text(encoding='utf-8'))
expected=(draft_req.get('articles') or [{}])[0]
cfg_path=pathlib.Path.home()/'.config/md2wechat/config.yaml'
cfg=yaml.safe_load(cfg_path.read_text(encoding='utf-8')) or {}
appid=(cfg.get('wechat') or {}).get('appid') or os.getenv('WECHAT_APPID')
secret=(cfg.get('wechat') or {}).get('secret') or os.getenv('WECHAT_SECRET')
if not appid or not secret:
    raise SystemExit('缺少 WECHAT_APPID / WECHAT_SECRET 或 md2wechat config wechat 配置')
url='https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid='+urllib.parse.quote(appid)+'&secret='+urllib.parse.quote(secret)
with urllib.request.urlopen(url, timeout=20) as r:
    token_resp=json.loads(r.read().decode())
result={'target_media_id':media_id,'token_response':{k:('***' if k=='access_token' else v) for k,v in token_resp.items()}}
if 'access_token' not in token_resp:
    result.update({'passed':False,'error':'no access_token'})
else:
    req=urllib.request.Request('https://api.weixin.qq.com/cgi-bin/draft/get?access_token='+urllib.parse.quote(token_resp['access_token']), data=json.dumps({'media_id':media_id},ensure_ascii=False).encode(), headers={'Content-Type':'application/json'}, method='POST')
    with urllib.request.urlopen(req, timeout=20) as r:
        draft_resp=json.loads(r.read().decode())
    item=(draft_resp.get('news_item') or [{}])[0] if isinstance(draft_resp.get('news_item'), list) else {}
    content=item.get('content','') or ''
    checks={
        'errcode_ok': draft_resp.get('errcode') in (None,0),
        'title': item.get('title'),
        'title_ok': item.get('title')==expected.get('title'),
        'author': item.get('author'),
        'author_ok': item.get('author')==expected.get('author'),
        'digest': item.get('digest'),
        'thumb_media_id_present': bool(item.get('thumb_media_id')),
        'content_length': len(content),
        'content_has_local_path': '/home/ye/' in content or 'content-factory/' in content,
        'content_has_inline_style': 'style=' in content,
        'url_present': bool(item.get('url')),
        'thumb_url_present': bool(item.get('thumb_url')),
    }
    result.update({'draft_get_response':draft_resp,'checks':checks,'passed':checks['errcode_ok'] and checks['title_ok'] and checks['author_ok'] and checks['thumb_media_id_present'] and not checks['content_has_local_path']})
out.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
if not result.get('passed'):
    raise SystemExit(1)
PY

ok "🎉 草稿推送并核验通过"
echo "create_result: $CREATE_RESULT"
echo "verify_json:   $VERIFY_JSON"
