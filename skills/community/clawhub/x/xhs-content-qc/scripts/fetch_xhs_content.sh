#!/usr/bin/env sh
set -eu

usage() {
  cat <<'USAGE'
用 curl 尽量抓取小红书链接页面可读内容（标题/话题/@）并输出 JSON。

用法：
  sh fetch_xhs_content.sh --url "<链接URL>" [--timeout-s 15] [--max-chars 20000] [--max-tags 80] [--max-ats 20]
USAGE
}

URL=""
TIMEOUT_S=15
MAX_CHARS=20000
MAX_TAGS=80
MAX_ATS=20
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"

while [ $# -gt 0 ]; do
  case "$1" in
    --url)
      URL="${2:-}"
      shift 2
      ;;
    --timeout-s)
      TIMEOUT_S="${2:-15}"
      shift 2
      ;;
    --max-chars)
      MAX_CHARS="${2:-20000}"
      shift 2
      ;;
    --max-tags)
      MAX_TAGS="${2:-80}"
      shift 2
      ;;
    --max-ats)
      MAX_ATS="${2:-20}"
      shift 2
      ;;
    --user-agent)
      UA="${2:-}"
      shift 2
      ;;
    -h | --help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown arg: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

if [ -z "$URL" ]; then
  echo "Missing --url" >&2
  usage >&2
  exit 2
fi

tmp_html="$(mktemp)"
trap 'rm -f "$tmp_html" 2>/dev/null || true' EXIT

marker_code="__HTTP_CODE__:"
marker_url="__URL_EFFECTIVE__:"

# 1) 把 HTML 写到临时文件
# 2) 额外用 -w 输出 http_code/effective_url（写到 stdout，方便解析）
meta="$(
  curl -sL \
    -A "$UA" \
    --max-redirs 5 \
    --connect-timeout "$TIMEOUT_S" \
    -o "$tmp_html" \
    -w "\n${marker_code}%{http_code}\n${marker_url}%{url_effective}\n" \
    "$URL" 2>/dev/null || true
)"

http_status=""
final_url=""

# 解析 meta
if echo "$meta" | grep -q "$marker_code"; then
  http_status="$(printf "%s" "$meta" | sed -n "s/.*${marker_code}\([0-9][0-9]*\).*/\1/p" | tail -n 1)"
fi
if echo "$meta" | grep -q "$marker_url"; then
  final_url="$(printf "%s" "$meta" | sed -n "s/.*${marker_url}//p" | head -n 1 | tr -d '\n' | tr -d '\r')"
fi

html="$(cat "$tmp_html" 2>/dev/null || true)"

escape_json() {
  # 只做基础转义：反斜杠/双引号/换行
  # 标题/摘要多为单行，够用即可。
  printf "%s" "$1" \
    | sed 's/\\/\\\\/g; s/"/\\"/g; s/\r//g; s/\n/\\n/g'
}

extract_og() {
  # property="og:title" content="xxx"
  prop="$1"
  printf "%s" "$html" | sed -n "s/.*property=[\"']${prop}[\"'][[:space:]]\\+content=[\"']\\([^\"']*\\)[\"'].*/\\1/p" | head -n 1 | sed 's/^[[:space:]]*//; s/[[:space:]]*$//'
}

extract_meta_desc() {
  printf "%s" "$html" | sed -n "s/.*property=['\"]og:description['\"][[:space:]]\\+content=['\"]\\([^'\"]*\\)['\"].*/\\1/p" | head -n 1
}

title="$(extract_og "og:title")"
if [ -z "$title" ]; then
  # fallback: <title>...</title>
  title="$(printf "%s" "$html" | sed -n 's/.*<title[^>]*>\([^<]*\)<\/title>.*/\1/p' | head -n 1)"
fi

desc="$(extract_meta_desc)"

# 抽取 tags：优先从 html 中直接抓，避免复杂的“提纯正文”
text_no_tags="$(printf "%s" "$html" | sed 's/<[^>]*>/ /g')"

# 截断预览
text_preview="$text_no_tags"
if [ "$MAX_CHARS" -gt 0 ]; then
  text_preview="$(printf "%s" "$text_preview" | awk -v n="$MAX_CHARS" '{ if(length($0)>n){print substr($0,1,n)} else {print $0} }')"
fi

# hashtags: # + 1~30 中文或字母数字下划线
hashtags_tmp="$(
  printf "%s" "$text_no_tags" \
    | awk -v limit="$MAX_TAGS" '
      BEGIN{count=0}
      {
        while (match($0, /#[A-Za-z0-9_]{1,30}/)) {
          tag=substr($0, RSTART, RLENGTH)
          if (!(tag in seen)) { seen[tag]=1; tags[++count]=tag }
          $0=substr($0, RSTART+RLENGTH)
          if (count>=limit) break
        }
        if (count>=limit) { exit }
      }
      END{
        for(i=1;i<=count;i++) print tags[i]
      }'
)"

# 兼容中文 hashtag（# + 一到龥）
hashtags_cn="$(
  printf "%s" "$text_no_tags" \
    | awk -v limit="$MAX_TAGS" '
      BEGIN{count=0}
      {
        while (match($0, /#[一-龥]{1,30}/)) {
          tag=substr($0, RSTART, RLENGTH)
          if (!(tag in seen)) { seen[tag]=1; tags[++count]=tag }
          $0=substr($0, RSTART+RLENGTH)
          if (count>=limit) break
        }
        if (count>=limit) { exit }
      }
      END{
        for(i=1;i<=count;i++) print tags[i]
      }'
)"

hashtags="$(
  # 合并去重
  printf "%s\n%s\n" "$hashtags_tmp" "$hashtags_cn" \
    | awk -v limit="$MAX_TAGS" '
      BEGIN{count=0}
      {
        tag=$0
        if(tag==""||tag=="\r") next
        if(!(tag in seen)){ seen[tag]=1; out[++count]=tag }
        if(count>=limit) { exit }
      }
      END{ for(i=1;i<=count;i++) print out[i] }'
)"

# ats: 简单抓取 @ + 非空白串，然后裁掉末尾标点
ats="$(
  printf "%s" "$text_no_tags" \
    | awk -v limit="$MAX_ATS" '
      BEGIN{count=0}
      {
        while(match($0, /@[A-Za-z0-9_]+/)){
          a=substr($0, RSTART, RLENGTH)
          $0=substr($0, RSTART+RLENGTH)
          if(!(a in seen)){ seen[a]=1; out[++count]=a }
          if(count>=limit) break
        }
        if(count>=limit) { exit }
      }
      END{ for(i=1;i<=count;i++) print out[i] }'
)"

hashtags_json=""
if [ -n "$hashtags" ]; then
  hashtags_json="$(printf "%s" "$hashtags" | awk '
    BEGIN{first=1}
    {
      gsub(/\r/,"")
      if($0=="") next
      if(first==0) printf ","
      printf "\"%s\"", $0
      first=0
    }
    END{ }')"
fi

ats_json=""
if [ -n "$ats" ]; then
  ats_json="$(printf "%s" "$ats" | awk '
    BEGIN{first=1}
    {
      gsub(/\r/,"")
      if($0=="") next
      if(first==0) printf ","
      printf "\"%s\"", $0
      first=0
    }
    END{ }')"
fi

title_esc="$(escape_json "${title:-}")"
desc_esc="$(escape_json "${desc:-}")"
preview_esc="$(escape_json "${text_preview:-}")"

cat <<EOF
{
  "url": "$(escape_json "$URL")",
  "http_status": "$(escape_json "${http_status:-}")",
  "final_url": "$(escape_json "${final_url:-}")",
  "title": "$title_esc",
  "description": "$desc_esc",
  "hashtags": [${hashtags_json}],
  "ats": [${ats_json}],
  "text_preview": "$preview_esc"
}
EOF

