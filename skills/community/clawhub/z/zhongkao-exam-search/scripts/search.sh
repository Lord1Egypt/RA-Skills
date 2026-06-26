#!/usr/bin/env bash
# search.sh — 从多个免费来源搜索中考真题下载链接
# 用法: ./search.sh "湖南长沙" "英语" 2021
# 输出: JSON格式的搜索结果

set -euo pipefail

REGION="${1:?用法: search.sh <省份城市> <科目> <年份>}"
SUBJECT="${2:?用法: search.sh <省份城市> <科目> <年份>}"
YEAR="${3:?用法: search.sh <省份城市> <科目> <年份>}"

UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
RESULTS=()
RESULT_JSON="[]"

log() { echo "[search] $*" >&2; }

# --- 来源1: 中考网 zhongkao.com ---
search_zhongkao() {
  log "搜索中考网 (zhongkao.com)..."
  
  # 提取省份和城市
  PROVINCE=$(echo "$REGION" | sed 's/省\|市//g' | cut -c1-2)
  CITY=$(echo "$REGION" | grep -oE '[^\s]+$' | sed 's/市//g')
  
  # 搜索下载版页面
  DOWNLOAD_URL="https://m.zhongkao.com/e/search/result/"
  
  # 用web搜索找中考网页面
  local search_query="${CITY}+中考${SUBJECT}+真题+下载版+${YEAR}"
  local search_url="https://www.zhongkao.com/e/search/result/?searchid=0&keyboard=${search_query}"
  
  # 直接构建可能的URL模式
  # 已知中考网URL模式: m.zhongkao.com/e/{日期}/{ID}.shtml
  # 下载链接模式: files.eduuu.com/ohr/{年}/{月}/{日}/{文件名}.zip|.rar
  
  echo '{"source":"zhongkao","status":"needs_web_search","query":"'"${CITY} 中考${SUBJECT} 真题 下载版 ${YEAR}"'","url_pattern":"m.zhongkao.com/e/{date}/{id}.shtml","download_pattern":"files.eduuu.com/ohr/{year}/{month}/{day}/{filename}.zip|.rar"}'
}

# --- 来源2: 中学英语网 trjlseng.com (仅英语) ---
search_trjlseng() {
  if [[ "$SUBJECT" != "英语" ]]; then
    echo '{"source":"trjlseng","status":"skipped","reason":"仅支持英语科目"}'
    return
  fi
  
  log "搜索中学英语网 (trjlseng.com)..."
  echo '{"source":"trjlseng","status":"needs_web_search","query":"'"${REGION} 中考英语 真题 ${YEAR}"'","url_pattern":"trjlseng.com/zkst/{id}.html","download_pattern":"trjlseng.com/uploads/ueditor/file/{date}/{filename}.zip","note":"可能需要注册登录"}'
}

# --- 来源3: 第一试卷网 shijuan1.com ---
search_shijuan1() {
  log "搜索第一试卷网 (shijuan1.com)..."
  
  # 科目分类编码
  local subject_code
  case "$SUBJECT" in
    语文)   subject_code="sjywzk" ;;
    数学)   subject_code="sjshxzk" ;;
    英语)   subject_code="sjyyzk" ;;
    物理)   subject_code="sjwlzk" ;;
    化学)   subject_code="sjhxzk" ;;
    历史)   subject_code="sjlszk" ;;
    道法|道德与法治) subject_code="sjzzzk" ;;
    生物)   subject_code="sjswwk" ;;
    地理)   subject_code="sjdlzk" ;;
    *)      subject_code="sjyyzk" ;;  # 默认英语
  esac
  
  echo '{"source":"shijuan1","status":"needs_web_search","query":"'"${REGION} ${YEAR} 中考${SUBJECT}"'","url_pattern":"shijuan1.com/a/'"${subject_code}"'/{id}.html","download_pattern":"shijuan1.com/uploads/soft/{category}/'"${subject_code}"'/中考/{filename}.rar","subject_code":"'"${subject_code}"'"}'
}

# --- 来源4: 中学学科网 zxzyw.cn ---
search_zxzyw() {
  log "搜索中学学科网 (zxzyw.cn)..."
  echo '{"source":"zxzyw","status":"needs_web_search","query":"'"${REGION} 中考${SUBJECT} 真题 ${YEAR} 免费下载"'","note":"部分资源需积分"}'
}

# --- 来源5: 五一考网 51test.net ---
search_51test() {
  log "搜索无忧考网 (51test.net)..."
  echo '{"source":"51test","status":"needs_web_search","query":"'"${REGION} ${YEAR} 中考${SUBJECT} 试题 答案 Word"'","note":"Word版需VIP"}'
}

# --- 汇总输出 ---
main() {
  log "搜索: ${REGION} ${YEAR}年中考${SUBJECT}真题"
  log "================================"
  
  R1=$(search_zhongkao)
  R2=$(search_trjlseng)
  R3=$(search_shijuan1)
  R4=$(search_zxzyw)
  R5=$(search_51test)
  
  # 输出JSON数组
  python3 -c "
import json, sys
results = [
  json.loads('''$R1'''),
  json.loads('''$R2'''),
  json.loads('''$R3'''),
  json.loads('''$R4'''),
  json.loads('''$R5'''),
]
print(json.dumps(results, ensure_ascii=False, indent=2))
"
  
  log "================================"
  log "搜索完成。下一步：使用web_search工具按query字段搜索，获取具体下载页面URL"
  log "然后使用download.sh下载文件"
}

main
