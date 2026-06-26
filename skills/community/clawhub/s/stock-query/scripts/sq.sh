#!/usr/bin/env bash
# sq — stock-query 数据层 CLI
# 用法: sq get <code> [code...]
# 输出: JSON 数组，每个元素对应一个标的的实时行情
#
# JSON 字段说明:
#   code          用户输入的原始代码
#   name          标的名称
#   market        A股 | 港股 | 美股 | 基金
#   type          stock | etf | index | fund
#   currency      CNY | HKD | USD
#   price         最新价（数值）
#   prev_close    昨收
#   open          今开
#   high          最高
#   low           最低
#   change        涨跌额
#   change_pct    涨跌幅数值（正=涨，负=跌，单位%）
#   direction     up | down | flat
#   volume        成交量（A股单位手，美股单位股）
#   amount        成交额（万元，A股；其他市场可能为 null）
#   turnover      换手率（%，A股/港股有效）
#   pe            市盈率（A股有效）
#   week52_high   52周最高价
#   week52_low    52周最低价
#   datetime      行情时间（YYYY-MM-DD HH:MM:SS）
#   is_estimate   基金：true=今日估算净值，false=确认净值
#   nav_date      基金：净值日期
#   is_qdii       基金：是否为QDII基金（净值有延迟）
#   error         查询失败时的错误信息，成功时为 null

set -uo pipefail

TIMEOUT=8
TODAY=$(date +%Y-%m-%d)
_RESULTS_DIR=$(mktemp -d)
trap 'rm -rf "$_RESULTS_DIR"' EXIT INT TERM
_FMT_SH="$(cd "$(dirname "${BASH_SOURCE[0]}")" 2>/dev/null && pwd)/fmt.sh"

# ── JSON 工具 ──────────────────────────────────────────────────────────────────

_esc() { printf '%s' "$1" | sed 's/\\/\\\\/g; s/"/\\"/g'; }
jstr() { [[ -z "${1:-}" ]] && printf 'null' || printf '"%s"' "$(_esc "$1")"; }
jnum() {
  local v="${1:-}"
  [[ -z "$v" || "$v" == "-" || "$v" == "--" ]] && { printf 'null'; return; }
  # 保证 JSON 合法：bc 可能输出 .65 或 -.65，需补前导零
  [[ "$v" =~ ^\. ]]  && v="0${v}"
  [[ "$v" =~ ^-\. ]] && v="-0${v#-}"
  printf '%s' "$v"
}

# 解码 JSON Unicode 转义序列 \uXXXX → UTF-8（腾讯 API 返回此格式）
_ujson() {
  local s="$1"
  [[ "$s" != *'\u'* ]] && { printf '%s' "$s"; return; }
  command -v python3 &>/dev/null || { printf '%s' "$s"; return; }
  printf '"%s"' "$s" | python3 -c "import json,sys; print(json.load(sys.stdin), end='')" 2>/dev/null \
    || printf '%s' "$s"
}
jbool() { [[ "${1:-false}" == "true" ]] && printf 'true' || printf 'false'; }

direction_of() {
  local pct="${1:-}"
  [[ -z "$pct" ]] && { printf 'flat'; return; }
  if command -v bc &>/dev/null; then
    if (( $(echo "${pct} > 0" | bc -l 2>/dev/null || echo 0) )); then
      printf 'up'
    elif (( $(echo "${pct} < 0" | bc -l 2>/dev/null || echo 0) )); then
      printf 'down'
    else
      printf 'flat'
    fi
  else
    printf 'flat'
  fi
}

# ── 映射工具（printf -v + 间接展开，bash 3.1+ 兼容，无 eval）──────────────────

# key → 去掉非 alnum 字符，保证变量名合法
_mkey() { printf '%s' "$1" | tr -cs 'a-zA-Z0-9' '_'; }

# _mset NAMESPACE KEY VALUE  /  _mget NAMESPACE KEY  /  _mhas NAMESPACE KEY
_mset() { local _v="_m_$(_mkey "$1")_$(_mkey "$2")"; printf -v "$_v" '%s' "$3"; }
_mget() { local _v="_m_$(_mkey "$1")_$(_mkey "$2")"; printf '%s' "${!_v}"; }
_mhas() { local _v="_m_$(_mkey "$1")_$(_mkey "$2")"; [[ -n "${!_v}" ]]; }

# ── 市场识别 ──────────────────────────────────────────────────────────────────

# 沪市指数白名单（000开头）
_SH_IDX=" 000001 000010 000015 000016 000300 000688 000852 000903 000905 000906 000985 "

# 输出: "{market}:{sym}:{type}"
# market: sh | sz | hk | us | fund | probe | error
# probe 表示需要通过腾讯响应验证（深市股票 or 场外基金）
classify_code() {
  local raw="$1"

  # 美股指数别名：腾讯 API 实际 symbol 与通用写法不一致时在此映射
  case "$raw" in
    .SPX|.SP500) raw=".INX" ;;
  esac

  # 显式市场前缀 sh/sz + 6位数字（优先于字母→美股判断）
  if [[ "$raw" =~ ^(sh|sz)([0-9]{6})$ ]]; then
    local _pfx="${BASH_REMATCH[1]}" _code="${BASH_REMATCH[2]}"
    local _type
    case "$_pfx" in
      sh)
        case "${_code:0:1}" in
          6) _type="stock" ;;
          5) _type="etf"   ;;
          0|3)
            if [[ "$_SH_IDX" == *" $_code "* ]]; then _type="index"
            else _type="stock"; fi
            ;;
          *) _type="stock" ;;
        esac
        ;;
      sz)
        case "${_code:0:3}" in
          399) _type="index" ;;
          *)
            case "${_code:0:1}" in
              1) _type="etf"   ;;
              *) _type="stock" ;;
            esac
            ;;
        esac
        ;;
    esac
    printf '%s:%s:%s' "$_pfx" "$_code" "$_type"; return
  fi

  if [[ "$raw" =~ ^\.[A-Z]+$ ]]; then
    printf 'us:%s:index' "$raw"; return
  fi
  if [[ "$raw" =~ ^[A-Za-z] ]]; then
    printf 'us:%s:stock' "$(printf '%s' "$raw" | tr '[:lower:]' '[:upper:]')"; return
  fi
  if [[ "$raw" =~ ^[0-9]{1,5}$ ]]; then
    printf 'hk:%05d:stock' "$((10#$raw))"; return
  fi
  if [[ "$raw" =~ ^[0-9]{6}$ ]]; then
    case "${raw:0:1}" in
      6) printf 'sh:%s:stock' "$raw" ;;
      5) printf 'sh:%s:etf'   "$raw" ;;
      1) printf 'sz:%s:etf'   "$raw" ;;
      0|3)
        if [[ "$_SH_IDX" == *" $raw "* ]]; then
          printf 'sh:%s:index' "$raw"
        elif [[ "${raw:0:3}" == "399" ]]; then
          printf 'sz:%s:index' "$raw"
        else
          printf 'probe:sz:%s:stock' "$raw"
        fi
        ;;
      2|4|7|8|9) printf 'fund:%s:fund' "$raw" ;;
      *) printf 'error:%s' "$raw" ;;
    esac
    return
  fi
  printf 'error:%s' "$raw"
}

# ── 错误对象 ──────────────────────────────────────────────────────────────────

error_obj() {
  local code="$1" msg="$2"
  printf '{"code":%s,"name":null,"market":null,"type":null,"currency":null,' "$(jstr "$code")"
  printf '"price":null,"prev_close":null,"open":null,"high":null,"low":null,'
  printf '"change":null,"change_pct":null,"direction":null,'
  printf '"volume":null,"amount":null,"turnover":null,"pe":null,'
  printf '"week52_high":null,"week52_low":null,"datetime":null,'
  printf '"is_estimate":false,"nav_date":null,"is_qdii":false,"error":%s}' "$(jstr "$msg")"
}

# 将结果写到临时文件（按 index），避免 bash 变量特殊字符问题
save_result() { printf '%s' "$2" > "${_RESULTS_DIR}/${1}"; }
load_result() { cat "${_RESULTS_DIR}/${1}" 2>/dev/null; }

# ── 腾讯财经 API ───────────────────────────────────────────────────────────────

tencent_fetch() {
  curl -s -m "$TIMEOUT" "https://qt.gtimg.cn/q=$1" | iconv -f GBK -t UTF-8 2>/dev/null
}

tencent_api_code_of() {
  printf '%s' "$1" | grep -oE 'v_[a-zA-Z]+[A-Za-z0-9.]+' | head -1 | sed 's/^v_//'
}

tencent_line_valid() {
  local data
  data=$(printf '%s' "$1" | cut -d'"' -f2)
  [[ -z "$data" ]] && return 1
  local name latest
  name=$(printf '%s' "$data" | cut -d'~' -f2)
  latest=$(printf '%s' "$data" | cut -d'~' -f4)
  [[ -n "$name" && -n "$latest" && "$name" != "" && "$latest" != "" ]]
}

parse_tencent() {
  local line="$1" user_code="$2" type="$3"
  local data
  data=$(printf '%s' "$line" | cut -d'"' -f2)
  [[ -z "$data" ]] && return 1

  # IFS='~' 读字段
  local name prev_close open latest change change_pct high low volume
  local amount turnover pe week52_high week52_low dt market_id
  name=$(        printf '%s' "$data" | cut -d'~' -f2)
  latest=$(      printf '%s' "$data" | cut -d'~' -f4)
  [[ -z "$name" || -z "$latest" ]] && return 1

  market_id=$(   printf '%s' "$data" | cut -d'~' -f1)
  prev_close=$(  printf '%s' "$data" | cut -d'~' -f5)
  open=$(        printf '%s' "$data" | cut -d'~' -f6)
  volume=$(      printf '%s' "$data" | cut -d'~' -f7)
  change=$(      printf '%s' "$data" | cut -d'~' -f32)
  change_pct=$(  printf '%s' "$data" | cut -d'~' -f33)
  high=$(        printf '%s' "$data" | cut -d'~' -f34)
  low=$(         printf '%s' "$data" | cut -d'~' -f35)
  amount=$(      printf '%s' "$data" | cut -d'~' -f38)
  turnover=$(    printf '%s' "$data" | cut -d'~' -f39)
  pe=$(          printf '%s' "$data" | cut -d'~' -f40)
  week52_high=$( printf '%s' "$data" | cut -d'~' -f42)
  week52_low=$(  printf '%s' "$data" | cut -d'~' -f43)
  dt=$(          printf '%s' "$data" | cut -d'~' -f31)

  # A股时间 YYYYMMDDHHMMSS → YYYY-MM-DD HH:MM:SS
  if [[ ${#dt} -eq 14 && "$dt" =~ ^[0-9]+$ ]]; then
    dt="${dt:0:4}-${dt:4:2}-${dt:6:2} ${dt:8:2}:${dt:10:2}:${dt:12:2}"
  fi

  local market currency
  case "$market_id" in
    1|51) market="A股"; currency="CNY" ;;
    100)  market="港股"; currency="HKD" ;;
    200)  market="美股"; currency="USD" ;;
    *)    market="—";   currency="—"   ;;
  esac

  local dir; dir=$(direction_of "$change_pct")

  printf '{"code":%s,"name":%s,"market":%s,"type":%s,"currency":%s,' \
    "$(jstr "$user_code")" "$(jstr "$name")" "$(jstr "$market")" "$(jstr "$type")" "$(jstr "$currency")"
  printf '"price":%s,"prev_close":%s,"open":%s,"high":%s,"low":%s,' \
    "$(jnum "$latest")" "$(jnum "$prev_close")" "$(jnum "$open")" "$(jnum "$high")" "$(jnum "$low")"
  printf '"change":%s,"change_pct":%s,"direction":%s,' \
    "$(jnum "$change")" "$(jnum "$change_pct")" "$(jstr "$dir")"
  printf '"volume":%s,"amount":%s,"turnover":%s,"pe":%s,' \
    "$(jnum "$volume")" "$(jnum "$amount")" "$(jnum "$turnover")" "$(jnum "$pe")"
  printf '"week52_high":%s,"week52_low":%s,"datetime":%s,' \
    "$(jnum "$week52_high")" "$(jnum "$week52_low")" "$(jstr "$dt")"
  printf '"is_estimate":false,"nav_date":null,"is_qdii":false,"error":null}'
  return 0
}

# ── 新浪财经 API（A股备用）────────────────────────────────────────────────────

sina_fetch() {
  curl -s -m "$TIMEOUT" "https://hq.sinajs.cn/list=$1" \
    -H "Referer: https://finance.sina.com.cn" | iconv -f GBK -t UTF-8 2>/dev/null
}

parse_sina() {
  local line="$1" user_code="$2" type="$3"
  local data
  data=$(printf '%s' "$line" | cut -d'"' -f2)
  [[ -z "$data" ]] && return 1

  local name prev_close latest open high low volume amount date time
  name=$(       printf '%s' "$data" | cut -d',' -f1)
  open=$(       printf '%s' "$data" | cut -d',' -f2)
  prev_close=$( printf '%s' "$data" | cut -d',' -f3)
  latest=$(     printf '%s' "$data" | cut -d',' -f4)
  high=$(       printf '%s' "$data" | cut -d',' -f5)
  low=$(        printf '%s' "$data" | cut -d',' -f6)
  volume=$(     printf '%s' "$data" | cut -d',' -f9)
  amount=$(     printf '%s' "$data" | cut -d',' -f10)
  date=$(       printf '%s' "$data" | cut -d',' -f31)
  time=$(       printf '%s' "$data" | cut -d',' -f32)

  [[ -z "$name" || -z "$latest" ]] && return 1

  local change="" change_pct="" dir="flat"
  if command -v bc &>/dev/null && [[ -n "$prev_close" && "$prev_close" != "0.000" ]]; then
    change=$(echo "scale=4; $latest - $prev_close" | bc)
    change_pct=$(echo "scale=4; ($latest - $prev_close) / $prev_close * 100" | bc | xargs printf "%.4f")
    dir=$(direction_of "$change_pct")
  fi

  printf '{"code":%s,"name":%s,"market":"A股","type":%s,"currency":"CNY",' \
    "$(jstr "$user_code")" "$(jstr "$name")" "$(jstr "$type")"
  printf '"price":%s,"prev_close":%s,"open":%s,"high":%s,"low":%s,' \
    "$(jnum "$latest")" "$(jnum "$prev_close")" "$(jnum "$open")" "$(jnum "$high")" "$(jnum "$low")"
  printf '"change":%s,"change_pct":%s,"direction":%s,' \
    "$(jnum "$change")" "$(jnum "$change_pct")" "$(jstr "$dir")"
  printf '"volume":%s,"amount":%s,"turnover":null,"pe":null,' \
    "$(jnum "$volume")" "$(jnum "$amount")"
  printf '"week52_high":null,"week52_low":null,"datetime":%s,' \
    "$(jstr "${date} ${time}")"
  printf '"is_estimate":false,"nav_date":null,"is_qdii":false,"error":null}'
  return 0
}

# ── 腾讯历史K线 API（A股/港股）────────────────────────────────────────────────
# sym: sh600519 / sz000001 / hk00700 等腾讯格式
# period: day | week | month
# adjust: qfq | hfq | (empty=不复权)
# count: 返回条数；start/end: YYYY-MM-DD 或空

tencent_hist_fetch() {
  local sym="$1" period="$2" adjust="$3" count="$4" start="${5:-}" end="${6:-}"
  curl -s -m "$TIMEOUT" \
    "https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param=${sym},${period},${start},${end},${count},${adjust}" \
    | iconv -f GBK -t UTF-8 2>/dev/null
}

# ── Yahoo Finance 历史K线 API（美股）─────────────────────────────────────────
# interval: 1d=日K 1wk=周K 1mo=月K
# range: 3mo/6mo/1y/2y/5y；或用 period1/period2（Unix 时间戳）指定区间

yahoo_hist_fetch() {
  local sym="$1" interval="$2" range="${3:-}" period1="${4:-}" period2="${5:-}"
  local url="https://query1.finance.yahoo.com/v8/finance/chart/${sym}?interval=${interval}"
  [[ -n "$range"   ]] && url="${url}&range=${range}"
  [[ -n "$period1" ]] && url="${url}&period1=${period1}&period2=${period2}"
  curl -s -m "$TIMEOUT" -A "Mozilla/5.0" "$url"
}


# ── 东方财富 API（港股/美股备用）─────────────────────────────────────────────

em_stock_fetch() {
  curl -s -m "$TIMEOUT" \
    -H "Referer: https://finance.eastmoney.com" \
    "https://push2.eastmoney.com/api/qt/stock/get?secid=$1&fields=f43,f57,f58,f169,f170,f47&fltt=2"
}

parse_em_stock() {
  local resp="$1" user_code="$2" market="$3" currency="$4"
  [[ "$resp" == *'"data":null'* ]] && return 1

  local name latest change change_pct volume
  name=$(      printf '%s' "$resp" | grep -o '"f58":"[^"]*"' | head -1 | cut -d'"' -f4)
  latest=$(    printf '%s' "$resp" | grep -o '"f43":[^,}]*'  | head -1 | cut -d':' -f2)
  change=$(    printf '%s' "$resp" | grep -o '"f169":[^,}]*' | head -1 | cut -d':' -f2)
  change_pct=$(printf '%s' "$resp" | grep -o '"f170":[^,}]*' | head -1 | cut -d':' -f2)
  volume=$(    printf '%s' "$resp" | grep -o '"f47":[^,}]*'  | head -1 | cut -d':' -f2)

  [[ -z "$name" || -z "$latest" ]] && return 1

  local dir; dir=$(direction_of "$change_pct")

  printf '{"code":%s,"name":%s,"market":%s,"type":"stock","currency":%s,' \
    "$(jstr "$user_code")" "$(jstr "$name")" "$(jstr "$market")" "$(jstr "$currency")"
  printf '"price":%s,"prev_close":null,"open":null,"high":null,"low":null,' "$(jnum "$latest")"
  printf '"change":%s,"change_pct":%s,"direction":%s,' \
    "$(jnum "$change")" "$(jnum "$change_pct")" "$(jstr "$dir")"
  printf '"volume":%s,"amount":null,"turnover":null,"pe":null,' "$(jnum "$volume")"
  printf '"week52_high":null,"week52_low":null,"datetime":null,'
  printf '"is_estimate":false,"nav_date":null,"is_qdii":false,"error":null}'
  return 0
}

# ── 场外基金 API ───────────────────────────────────────────────────────────────

query_fund() {
  local code="$1"

  local resp4a
  resp4a=$(curl -s -m "$TIMEOUT" "http://fundgz.1234567.com.cn/js/${code}.js")

  local name="" gsz="" gszzl="" gztime="" dwjz="" jzrq=""
  local use_estimate=false

  if [[ -n "$resp4a" && "$resp4a" != "jsonpgz()" ]]; then
    name=$(   printf '%s' "$resp4a" | grep -o '"name":"[^"]*"'   | cut -d'"' -f4)
    gsz=$(    printf '%s' "$resp4a" | grep -o '"gsz":"[^"]*"'    | cut -d'"' -f4)
    gszzl=$(  printf '%s' "$resp4a" | grep -o '"gszzl":"[^"]*"'  | cut -d'"' -f4)
    gztime=$( printf '%s' "$resp4a" | grep -o '"gztime":"[^"]*"' | cut -d'"' -f4)
    dwjz=$(   printf '%s' "$resp4a" | grep -o '"dwjz":"[^"]*"'   | cut -d'"' -f4)
    jzrq=$(   printf '%s' "$resp4a" | grep -o '"jzrq":"[^"]*"'   | cut -d'"' -f4)
    [[ "${gztime:0:10}" == "$TODAY" ]] && use_estimate=true
  fi

  local price="" nav_date="" is_estimate=false change_pct=""

  if [[ "$use_estimate" == "true" ]]; then
    price="$gsz"; nav_date="$jzrq"; is_estimate=true; change_pct="$gszzl"
  else
    local resp4b
    resp4b=$(curl -s -m "$TIMEOUT" \
      "https://api.fund.eastmoney.com/f10/lsjz?fundCode=${code}&pageIndex=1&pageSize=1" \
      -H "Referer: https://fund.eastmoney.com")

    local em_nav em_date em_pct
    em_nav=$(  printf '%s' "$resp4b" | grep -o '"DWJZ":"[^"]*"'  | head -1 | cut -d'"' -f4)
    em_date=$( printf '%s' "$resp4b" | grep -o '"FSRQ":"[^"]*"'  | head -1 | cut -d'"' -f4)
    em_pct=$(  printf '%s' "$resp4b" | grep -o '"JZZZL":"[^"]*"' | head -1 | cut -d'"' -f4)

    if [[ -n "$em_nav" ]]; then
      price="$em_nav"; nav_date="$em_date"; is_estimate=false; change_pct="$em_pct"
    elif [[ -n "$dwjz" ]]; then
      price="$dwjz"; nav_date="$jzrq"; is_estimate=false; change_pct="$gszzl"
    else
      error_obj "$code" "基金数据不可用，请稍后重试"; return 0
    fi
  fi

  local dir; dir=$(direction_of "$change_pct")

  local is_qdii=false
  [[ -n "$name" ]] && printf '%s' "$name" | grep -qiE "QDII|纳斯达克|标普|海外|美国|全球" \
    && is_qdii=true

  printf '{"code":%s,"name":%s,"market":"基金","type":"fund","currency":"CNY",' \
    "$(jstr "$code")" "$(jstr "$name")"
  printf '"price":%s,"prev_close":null,"open":null,"high":null,"low":null,' "$(jnum "$price")"
  printf '"change":null,"change_pct":%s,"direction":%s,' \
    "$(jnum "$change_pct")" "$(jstr "$dir")"
  printf '"volume":null,"amount":null,"turnover":null,"pe":null,'
  printf '"week52_high":null,"week52_low":null,"datetime":%s,' "$(jstr "$gztime")"
  printf '"is_estimate":%s,"nav_date":%s,"is_qdii":%s,"error":null}' \
    "$(jbool "$is_estimate")" "$(jstr "$nav_date")" "$(jbool "$is_qdii")"
}

# ── 主命令: sq get ─────────────────────────────────────────────────────────────

cmd_get() {
  [[ $# -eq 0 ]] && { printf 'usage: sq get <code> [code...]\n' >&2; exit 1; }

  # 输入数组（保持顺序）
  local input_codes=("$@")
  local n=${#input_codes[@]}

  # 并行数组（按 index）
  local input_cls=()     # classify 结果
  local input_api=()     # 腾讯 API code（空=不查腾讯）
  local input_type=()    # stock|etf|index|fund
  local input_market=()  # sh|sz|hk|us|fund|error
  local input_sym=()     # 实际符号（去掉前缀）
  local input_is_probe=() # 1=probe，空=否

  local tencent_api_list=""  # 腾讯批量查询字符串
  local i

  # ── 1. 分类 ──────────────────────────────────────────────────────────────────
  for (( i=0; i<n; i++ )); do
    local raw="${input_codes[$i]}"
    local cls; cls=$(classify_code "$raw")
    input_cls+=("$cls")

    # 解析 cls: market:sym:type 或 probe:market:sym:type 或 error:...
    local market sym type is_probe=""
    if [[ "$cls" == error:* ]]; then
      market="error"; sym="$raw"; type="error"
    elif [[ "$cls" == probe:* ]]; then
      local rest="${cls#probe:}"           # sz:CODE:stock
      market="${rest%%:*}"
      rest="${rest#*:}"
      sym="${rest%%:*}"
      type="${rest#*:}"
      is_probe="1"
    else
      market="${cls%%:*}"
      rest="${cls#*:}"
      sym="${rest%%:*}"
      type="${rest#*:}"
    fi

    input_market+=("$market")
    input_sym+=("$sym")
    input_type+=("$type")
    input_is_probe+=("$is_probe")

    # 确定腾讯 API code
    local api_code=""
    case "$market" in
      sh|sz|hk|us) api_code="${market}${sym}" ;;
      fund|error)  api_code="" ;;
    esac
    # probe 也走腾讯（市场为 sz）
    [[ "$is_probe" == "1" ]] && api_code="sz${sym}"

    input_api+=("$api_code")

    if [[ -n "$api_code" ]]; then
      tencent_api_list="${tencent_api_list:+${tencent_api_list},}${api_code}"
      # 建立 api_code → index 的映射（eval 方式，bash 3.x 兼容）
      _mset "api2idx" "$api_code" "$i"
    fi

    # 错误代码直接写结果
    if [[ "$market" == "error" ]]; then
      save_result "$i" "$(error_obj "$raw" "无法识别代码（A股6位/港股≤5位/美股ticker）")"
    fi
  done

  # ── 2. 腾讯批量查询 ──────────────────────────────────────────────────────────
  if [[ -n "$tencent_api_list" ]]; then
    local tencent_resp
    tencent_resp=$(tencent_fetch "$tencent_api_list")

    while IFS= read -r line; do
      [[ -z "$line" ]] && continue
      local api_code; api_code=$(tencent_api_code_of "$line")
      [[ -z "$api_code" ]] && continue

      local idx; idx=$(_mget "api2idx" "$api_code")
      [[ -z "$idx" ]] && continue

      local user_code="${input_codes[$idx]}"
      local type="${input_type[$idx]}"

      if tencent_line_valid "$line"; then
        local obj
        if obj=$(parse_tencent "$line" "$user_code" "$type"); then
          save_result "$idx" "$obj"
          _mset "done" "$api_code" "1"
        fi
      fi
    done <<< "$tencent_resp"
  fi

  # ── 3. 处理腾讯无数据的代码 ──────────────────────────────────────────────────
  for (( i=0; i<n; i++ )); do
    [[ -f "${_RESULTS_DIR}/${i}" ]] && continue   # 已有结果

    local market="${input_market[$i]}"
    local sym="${input_sym[$i]}"
    local type="${input_type[$i]}"
    local api="${input_api[$i]}"
    local user_code="${input_codes[$i]}"
    local is_probe="${input_is_probe[$i]}"

    case "$market" in
      error) continue ;;   # 已写结果

      sh|sz)
        # probe 代码腾讯无数据 → 场外基金
        if [[ "$is_probe" == "1" ]]; then
          save_result "$i" "$(query_fund "$sym")"
          continue
        fi
        # A股回退：新浪财经
        local sina_resp; sina_resp=$(sina_fetch "$api")
        local line; line=$(printf '%s' "$sina_resp" | grep "str_${api}" | head -1)
        local obj
        if obj=$(parse_sina "$line" "$user_code" "$type" 2>/dev/null) && [[ -n "$obj" ]]; then
          save_result "$i" "$obj"
        else
          save_result "$i" "$(error_obj "$user_code" "数据源暂时不可用，请稍后重试")"
        fi
        ;;

      hk)
        # 港股回退：东方财富 116.xxxxx
        local em_resp; em_resp=$(em_stock_fetch "116.${sym}")
        local obj
        if obj=$(parse_em_stock "$em_resp" "$user_code" "港股" "HKD" 2>/dev/null) && [[ -n "$obj" ]]; then
          save_result "$i" "$obj"
        else
          save_result "$i" "$(error_obj "$user_code" "港股数据不可用，请稍后重试")"
        fi
        ;;

      us)
        # 美股回退：东方财富 105.（NASDAQ）→ 106.（NYSE）
        local em_resp obj
        em_resp=$(em_stock_fetch "105.${sym}")
        if obj=$(parse_em_stock "$em_resp" "$user_code" "美股" "USD" 2>/dev/null) && [[ -n "$obj" ]]; then
          save_result "$i" "$obj"
        else
          em_resp=$(em_stock_fetch "106.${sym}")
          if obj=$(parse_em_stock "$em_resp" "$user_code" "美股" "USD" 2>/dev/null) && [[ -n "$obj" ]]; then
            save_result "$i" "$obj"
          else
            save_result "$i" "$(error_obj "$user_code" "美股数据不可用，请稍后重试")"
          fi
        fi
        ;;

      fund)
        save_result "$i" "$(query_fund "$sym")"
        ;;
    esac
  done

  # ── 4. 按输入顺序输出 JSON 数组 ───────────────────────────────────────────────
  printf '['
  local first=true
  for (( i=0; i<n; i++ )); do
    [[ "$first" == "true" ]] && first=false || printf ','
    if [[ -f "${_RESULTS_DIR}/${i}" ]]; then
      cat "${_RESULTS_DIR}/${i}"
    else
      error_obj "${input_codes[$i]}" "未获取到数据"
    fi
  done
  printf ']\n'
}

# ── sq fund ───────────────────────────────────────────────────────────────────
# 直接走场外基金查询流程，跳过市场分类，输出 JSON 数组
# 适用场景：已知是基金代码，或从 sq get 中分离出基金批量查询

cmd_fund() {
  [[ $# -eq 0 ]] && { printf 'usage: sq fund <code> [code...]\n' >&2; exit 1; }
  printf '['
  local first=true
  for code in "$@"; do
    [[ "$first" == "true" ]] && first=false || printf ','
    query_fund "$code"
  done
  printf ']\n'
}

# ── sq hist ───────────────────────────────────────────────────────────────────
# 查询个股历史K线，输出 JSON 对象
# 用法: sq hist <code> [--period day|week|month] [--count N]
#                      [--start YYYY-MM-DD] [--end YYYY-MM-DD]
#                      [--fq pre|post|none]
# 数据源: A股/港股 → 腾讯 web.ifzq.gtimg.cn；美股 → Yahoo Finance query1.finance.yahoo.com
# 输出字段: code name market period fq klines[] error
# klines 字段: date open close high low volume change_pct change
#   A股/港股额外字段 amount=null；美股额外字段 amplitude turnover

cmd_hist() {
  [[ $# -eq 0 ]] && {
    printf 'usage: sq hist <code> [--period day|week|month] [--count N] [--start YYYY-MM-DD] [--end YYYY-MM-DD] [--fq pre|post|none]\n' >&2
    exit 1
  }

  local code="" klt="101" fqt="1" lmt="30" beg="0" end="20500101"
  local period_name="day" fq_name="pre"
  local has_date_range=false

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --period|-p)
        case "${2:-}" in
          day|d)   klt="101"; period_name="day"   ;;
          week|w)  klt="102"; period_name="week"  ;;
          month|m) klt="103"; period_name="month" ;;
          *) printf 'sq hist: unknown period "%s"\n' "${2:-}" >&2; exit 1 ;;
        esac
        shift 2 ;;
      --count|-n)
        [[ -z "${2:-}" ]] && { printf 'sq hist: --count requires a value\n' >&2; exit 1; }
        lmt="$2"; shift 2 ;;
      --start)
        [[ -z "${2:-}" ]] && { printf 'sq hist: --start requires YYYY-MM-DD\n' >&2; exit 1; }
        beg="${2//-/}"; has_date_range=true; shift 2 ;;
      --end)
        [[ -z "${2:-}" ]] && { printf 'sq hist: --end requires YYYY-MM-DD\n' >&2; exit 1; }
        end="${2//-/}"; has_date_range=true; shift 2 ;;
      --fq)
        case "${2:-}" in
          pre)  fqt="1"; fq_name="pre"  ;;
          post) fqt="2"; fq_name="post" ;;
          none) fqt="0"; fq_name="none" ;;
          *) printf 'sq hist: unknown fq "%s"\n' "${2:-}" >&2; exit 1 ;;
        esac
        shift 2 ;;
      -*) printf 'sq hist: unknown option "%s"\n' "$1" >&2; exit 1 ;;
      *)
        [[ -n "$code" ]] && { printf 'sq hist: unexpected argument "%s"\n' "$1" >&2; exit 1; }
        code="$1"; shift ;;
    esac
  done

  [[ -z "$code" ]] && { printf 'sq hist: code is required\n' >&2; exit 1; }

  # 日期范围模式：不按 count 截断；普通模式：多取 61 条供 MA60 + 首行涨跌幅计算
  local display_lmt
  if [[ "$has_date_range" == true ]]; then
    display_lmt="0"      # 0 = 显示全部
    lmt="500"
  else
    display_lmt="$lmt"
    lmt=$(( lmt + 61 ))
  fi

  # 分类代码
  local cls; cls=$(classify_code "$code")
  local market sym
  if [[ "$cls" == error:* ]]; then
    printf '{"code":%s,"name":null,"market":null,"period":%s,"fq":%s,"klines":[],"error":"无法识别代码（A股6位/港股≤5位/美股ticker）"}\n' \
      "$(jstr "$code")" "$(jstr "$period_name")" "$(jstr "$fq_name")"
    return 0
  elif [[ "$cls" == probe:* ]]; then
    local rest="${cls#probe:}"
    market="${rest%%:*}"
    rest="${rest#*:}"; sym="${rest%%:*}"
  else
    local rest="${cls#*:}"
    market="${cls%%:*}"; sym="${rest%%:*}"
  fi

  case "$market" in
    fund)
      printf '{"code":%s,"name":null,"market":"基金","period":%s,"fq":%s,"klines":[],"error":"场外基金暂不支持历史数据查询"}\n' \
        "$(jstr "$code")" "$(jstr "$period_name")" "$(jstr "$fq_name")"
      return 0 ;;
    error|*)
      if [[ "$market" != "sh" && "$market" != "sz" && "$market" != "hk" && "$market" != "us" ]]; then
        printf '{"code":%s,"name":null,"market":null,"period":%s,"fq":%s,"klines":[],"error":"无法识别代码"}\n' \
          "$(jstr "$code")" "$(jstr "$period_name")" "$(jstr "$fq_name")"
        return 0
      fi ;;
  esac

  local is_probe=false
  [[ "$cls" == probe:* ]] && is_probe=true

  local kf; kf=$(mktemp)
  printf '[' > "$kf"
  local first=true name="" market_name=""

  if [[ "$market" == "sh" || "$market" == "sz" || "$market" == "hk" ]]; then
    # ── A股/港股：腾讯历史K线 ─────────────────────────────────────────────────
    [[ "$market" == "hk" ]] && market_name="港股" || market_name="A股"
    local tsym="${market}${sym}"

    # 复权参数：港股不支持复权，强制 none（fqt 参数仍记录用户意图但不传 API）
    local tadjust
    if [[ "$market" == "hk" ]]; then
      tadjust=""
    else
      case "$fqt" in
        1) tadjust="qfq" ;;
        2) tadjust="hfq" ;;
        0) tadjust=""    ;;
        *) tadjust="qfq" ;;
      esac
    fi

    # 日期转换：YYYYMMDD → YYYY-MM-DD（腾讯 API 用 YYYY-MM-DD）
    local tstart="" tend=""
    if [[ "$has_date_range" == true ]]; then
      [[ "$beg" != "0" ]] && tstart="${beg:0:4}-${beg:4:2}-${beg:6:2}"
      [[ "$end" != "20500101" ]] && tend="${end:0:4}-${end:4:2}-${end:6:2}"
    fi

    local resp; resp=$(tencent_hist_fetch "$tsym" "$period_name" "$tadjust" "$lmt" "$tstart" "$tend")

    if [[ -z "$resp" || "$resp" == *'"code":1'* || "$resp" == *'"code":-'* ]]; then
      printf ']' >> "$kf"
      printf '{"code":%s,"name":null,"market":%s,"period":%s,"fq":%s,"klines":[],"error":"历史数据不可用，请稍后重试"}\n' \
        "$(jstr "$code")" "$(jstr "$market_name")" "$(jstr "$period_name")" "$(jstr "$fq_name")"
      rm -f "$kf"; return 0
    fi

    # 提取股票名称（qt 字段第二个元素，可能是 \uXXXX 格式，需解码）
    local _raw_name
    _raw_name=$(printf '%s' "$resp" | grep -o '"qt":{"[^"]*":\["[^"]*","[^"]*"' | head -1 | cut -d'"' -f8)
    name=$(_ujson "$_raw_name")

    # 腾讯 kline row 格式：["YYYY-MM-DD","open","close","high","low","vol"]
    # 港股可能有第7列 object（除权信息），只取前6字段
    local prev_close=""
    while IFS= read -r match; do
      match="${match//\"/}"   # 去引号 → YYYY-MM-DD,open,close,high,low,vol
      local date open close high low volume
      date=$(   printf '%s' "$match" | cut -d',' -f1)
      open=$(   printf '%s' "$match" | cut -d',' -f2)
      close=$(  printf '%s' "$match" | cut -d',' -f3)
      high=$(   printf '%s' "$match" | cut -d',' -f4)
      low=$(    printf '%s' "$match" | cut -d',' -f5)
      volume=$( printf '%s' "$match" | cut -d',' -f6)

      # 计算涨跌额/幅（第一条无前收盘时为 null）
      local change="" change_pct=""
      if [[ -n "$prev_close" && -n "$close" ]] && command -v bc &>/dev/null; then
        change=$(echo "scale=4; $close - $prev_close" | bc 2>/dev/null || echo "")
        [[ -n "$change" ]] && \
          change_pct=$(echo "scale=4; $change / $prev_close * 100" | bc 2>/dev/null || echo "")
      fi
      prev_close="$close"

      [[ "$first" == true ]] && first=false || printf ',' >> "$kf"
      printf '{"date":%s,"open":%s,"close":%s,"high":%s,"low":%s,"volume":%s,"amount":null,"change_pct":%s,"change":%s,"amplitude":null,"turnover":null}' \
        "$(jstr "$date")" "$(jnum "$open")" "$(jnum "$close")" "$(jnum "$high")" "$(jnum "$low")" \
        "$(jnum "$volume")" "$(jnum "$change_pct")" "$(jnum "$change")" >> "$kf"
    done < <(printf '%s' "$resp" | grep -oE '"[0-9]{4}-[0-9]{2}-[0-9]{2}","[0-9.]+","[0-9.]+","[0-9.]+","[0-9.]+","[0-9.]+"')

  else
    # ── 美股：Yahoo Finance 历史K线 ──────────────────────────────────────────
    market_name="美股"
    local yinterval
    case "$klt" in
      101) yinterval="1d"  ;;
      102) yinterval="1wk" ;;
      103) yinterval="1mo" ;;
      *)   yinterval="1d"  ;;
    esac

    local resp
    if [[ "$has_date_range" == true ]]; then
      # YYYYMMDD → Unix 时间戳（python3 跨平台）
      local p1 p2
      p1=$(python3 -c "from datetime import datetime; s='${beg}'; print(int(datetime(int(s[:4]),int(s[4:6]),int(s[6:])).timestamp()))" 2>/dev/null || echo "")
      p2=$(python3 -c "from datetime import datetime; s='${end}'; print(int(datetime(int(s[:4]),int(s[4:6]),int(s[6:])).timestamp()))" 2>/dev/null || echo "")
      if [[ -n "$p1" && -n "$p2" ]]; then
        resp=$(yahoo_hist_fetch "$sym" "$yinterval" "" "$p1" "$p2")
      else
        resp=$(yahoo_hist_fetch "$sym" "$yinterval" "1y" "" "")
      fi
    else
      local yrange
      if   (( lmt <= 30  )); then yrange="3mo"
      elif (( lmt <= 90  )); then yrange="6mo"
      elif (( lmt <= 250 )); then yrange="1y"
      elif (( lmt <= 500 )); then yrange="2y"
      else                        yrange="5y"; fi
      resp=$(yahoo_hist_fetch "$sym" "$yinterval" "$yrange" "" "")
    fi

    # 用 python3 解析 Yahoo Finance JSON，输出 name 和 kline 对象流（每行一个）
    local _ypy; _ypy=$(mktemp /tmp/sqyhist_XXXXXX.py)
    trap 'rm -f "$_ypy"' RETURN
    cat > "$_ypy" << 'PYEOF'
import json, sys
from datetime import datetime, timezone

lmt_arg    = int(sys.argv[1])   if len(sys.argv) > 1 else 30
has_range  = sys.argv[2]        == 'true' if len(sys.argv) > 2 else False
use_adj    = sys.argv[3]        != '0'    if len(sys.argv) > 3 else True

try:
    d = json.loads(sys.stdin.read())
    result = (d.get('chart') or {}).get('result') or []
    if not result:
        print(json.dumps({'ok': False})); sys.exit(0)
    r = result[0]
    meta = r.get('meta') or {}
    name = meta.get('longName') or meta.get('shortName') or ''
    timestamps = r.get('timestamp') or []
    q = ((r.get('indicators') or {}).get('quote') or [{}])[0]
    opens  = q.get('open')   or []
    highs  = q.get('high')   or []
    lows   = q.get('low')    or []
    vols   = q.get('volume') or []
    raw_closes = q.get('close') or []
    adj_list = ((r.get('indicators') or {}).get('adjclose') or [{}])
    adj_closes = (adj_list[0].get('adjclose') or []) if adj_list else []
    closes = adj_closes if (use_adj and len(adj_closes) == len(timestamps)) else raw_closes

    def r4(v): return round(v, 4) if v is not None else None

    rows = []
    for i, ts in enumerate(timestamps):
        c = closes[i] if i < len(closes) else None
        if c is None: continue
        rows.append({
            'date':   datetime.fromtimestamp(ts, tz=timezone.utc).strftime('%Y-%m-%d'),
            'open':   r4(opens[i]  if i < len(opens)  else None),
            'close':  r4(c),
            'high':   r4(highs[i]  if i < len(highs)  else None),
            'low':    r4(lows[i]   if i < len(lows)   else None),
            'volume': int(vols[i]) if i < len(vols) and vols[i] is not None else None,
        })

    if not has_range and len(rows) > lmt_arg:
        rows = rows[-lmt_arg:]

    prev_close = None
    klines = []
    for row in rows:
        change = change_pct = None
        if prev_close and prev_close != 0:
            change     = round(row['close'] - prev_close, 4)
            change_pct = round(change / prev_close * 100,  4)
        prev_close = row['close']
        klines.append({
            'date': row['date'], 'open': row['open'], 'close': row['close'],
            'high': row['high'], 'low':  row['low'],  'volume': row['volume'],
            'amount': None, 'change_pct': change_pct, 'change': change,
            'amplitude': None, 'turnover': None,
        })
    print(json.dumps({'ok': True, 'name': name, 'klines': klines}, ensure_ascii=False))
except Exception:
    print(json.dumps({'ok': False}))
PYEOF

    local use_adj=1; [[ "$fqt" == "0" ]] && use_adj=0
    local parsed; parsed=$(printf '%s' "$resp" | python3 "$_ypy" "$lmt" "$has_date_range" "$use_adj")

    if [[ -z "$parsed" ]] || [[ "$parsed" == *'"ok": false'* ]] || [[ "$parsed" == *'"ok":false'* ]]; then
      printf ']' >> "$kf"
      printf '{"code":%s,"name":null,"market":"美股","period":%s,"fq":%s,"klines":[],"error":"历史数据不可用，请稍后重试"}\n' \
        "$(jstr "$code")" "$(jstr "$period_name")" "$(jstr "$fq_name")"
      rm -f "$kf"; return 0
    fi

    name=$(printf '%s' "$parsed" | python3 -c "import json,sys; print(json.load(sys.stdin).get('name',''))" 2>/dev/null)

    while IFS= read -r kline_obj; do
      [[ -z "$kline_obj" ]] && continue
      [[ "$first" == true ]] && first=false || printf ',' >> "$kf"
      printf '%s' "$kline_obj" >> "$kf"
    done < <(printf '%s' "$parsed" | python3 -c "
import json,sys
for k in json.load(sys.stdin).get('klines',[]):
    print(json.dumps(k,ensure_ascii=False))
" 2>/dev/null)
  fi

  printf ']' >> "$kf"

  # probe 代码（0开头6位数字）若 klines 为空 → 实为场外基金，不支持历史查询
  if [[ "$is_probe" == "true" && "$(cat "$kf")" == "[]" ]]; then
    rm -f "$kf"
    printf '{"code":%s,"name":null,"market":"基金","period":%s,"fq":%s,"klines":[],"error":"场外基金暂不支持历史数据查询"}\n' \
      "$(jstr "$code")" "$(jstr "$period_name")" "$(jstr "$fq_name")"
    return 0
  fi

  printf '{"code":%s,"name":%s,"market":%s,"period":%s,"fq":%s,"display_count":%s,"klines":' \
    "$(jstr "$code")" "$(jstr "$name")" "$(jstr "$market_name")" "$(jstr "$period_name")" "$(jstr "$fq_name")" "$display_lmt"
  cat "$kf"
  printf ',"error":null}\n'
  rm -f "$kf"
}

# ── sq pfile ──────────────────────────────────────────────────────────────────
# 定位 portfolio.csv 文件路径，输出绝对路径或 NOT_FOUND
# 查找顺序：XDG 配置目录（主） → openclaw → claude → agents（旧路径兼容）

cmd_pfile() {
  local pfile=""
  local _p
  for _p in \
    "$HOME/.config/stock-query/portfolio.csv" \
    "$HOME/.openclaw/workspace/skills/stock-query/portfolio.csv" \
    "$HOME/.claude/skills/stock-query/portfolio.csv" \
    "$HOME/.agents/skills/stock-query/portfolio.csv"; do
    [[ -f "$_p" ]] && pfile="$_p" && break
  done

  # 无论来源，文件不存在均返回 NOT_FOUND
  if [[ -z "$pfile" || ! -f "$pfile" ]]; then
    printf 'NOT_FOUND\n'
    return
  fi

  printf '%s\n' "$pfile"
}

# ── detail MA 注入 ────────────────────────────────────────────────────────────
# 从 stdin 读取 sq get JSON 数组，为每个非 error/fund 条目 fetch 60 日收盘价并注入 MA5/10/20/60

_enrich_detail_json() {
  local _input; _input=$(cat)
  local _py; _py=$(mktemp /tmp/sqma_XXXXXX.py)
  trap 'rm -f "$_py"' RETURN
  cat > "$_py" << 'PYEOF'
import json, sys, subprocess

SH_IDX = {'000001','000010','000015','000016','000300','000688',
           '000852','000903','000905','000906','000985'}

def tsym_of(item):
    market = item.get('market', '')
    code   = str(item.get('code', ''))
    itype  = item.get('type', '')
    if market == '港股':
        try:    return 'hk%05d' % int(code), ''
        except: return 'hk' + code, ''
    if market == '美股':
        return 'us' + code, ''
    if market == 'A股':
        fq = 'qfq' if itype in ('stock', 'etf') else ''
        if code and code[0] in ('6', '5'):
            return 'sh' + code, fq
        if code in SH_IDX:
            return 'sh' + code, ''
        return 'sz' + code, fq
    return None, ''

def fetch_klines(tsym, adjust):
    """Return (closes, volumes) lists, oldest→newest."""
    if tsym.startswith('us'):
        # 美股：Yahoo Finance
        sym = tsym[2:]
        url = ('https://query1.finance.yahoo.com/v8/finance/chart/'
               '%s?interval=1d&range=3mo' % sym)
        headers = ['-A', 'Mozilla/5.0']
    else:
        # A股/港股：腾讯历史K线
        url = ('https://web.ifzq.gtimg.cn/appstock/app/fqkline/get'
               '?param=%s,day,,,60,%s' % (tsym, adjust))
        headers = []
    try:
        r = subprocess.run(['curl', '-s', '-m', '8'] + headers + [url],
                           capture_output=True, timeout=10)
        if tsym.startswith('us'):
            d = json.loads(r.stdout.decode())
            result = (d.get('chart') or {}).get('result') or []
            if not result:
                return [], []
            q = ((result[0].get('indicators') or {}).get('quote') or [{}])[0]
            adj = ((result[0].get('indicators') or {}).get('adjclose') or [{}])
            adj_closes = (adj[0].get('adjclose') or []) if adj else []
            raw_closes  = adj_closes if adj_closes else (q.get('close') or [])
            raw_volumes = q.get('volume') or []
            closes  = [c for c in raw_closes  if c is not None]
            volumes = [v for v in raw_volumes if v is not None]
            return closes, volumes
        else:
            raw = r.stdout.decode('gbk', errors='replace')
            d = json.loads(raw)
            kdata = (d.get('data') or {}).get(tsym, {})
            for key in ('qfqday', 'day'):
                if key in kdata:
                    rows = kdata[key]
                    closes  = [float(row[2]) for row in rows]
                    volumes = [float(row[5]) for row in rows if len(row) > 5]
                    return closes, volumes
    except Exception:
        pass
    return [], []

def ma(vals, n):
    if len(vals) < n:
        return None
    return round(sum(vals[-n:]) / n, 2)

items = json.loads(sys.stdin.read(), parse_float=str)
for item in items:
    if item.get('error') or item.get('type') == 'fund':
        item['ma5'] = item['ma10'] = item['vol_ma5'] = item['vol_ma10'] = None
        continue
    tsym, adj = tsym_of(item)
    if not tsym:
        item['ma5'] = item['ma10'] = item['vol_ma5'] = item['vol_ma10'] = None
        continue
    closes, volumes = fetch_klines(tsym, adj)
    item['ma5']     = ma(closes,  5)
    item['ma10']    = ma(closes,  10)
    item['vol_ma5'] = ma(volumes, 5)
    item['vol_ma10']= ma(volumes, 10)

print(json.dumps(items, ensure_ascii=False))
PYEOF
  printf '%s' "$_input" | python3 "$_py"
}

# ── 入口 ──────────────────────────────────────────────────────────────────────
# get/fund/hist 支持 --format table|json|csv  和  --detail（独立 boolean）
# 有 --format 或 --detail 时输出经 fmt.sh 格式化；否则输出原始 JSON

_extract_fmt() {
  _FMT_ARG=""; _DETAIL_ARG=""; _REST_ARGS=()
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --format|-f) _FMT_ARG="${2:-table}"; shift 2 ;;
      --detail|-d) _DETAIL_ARG="true"; shift ;;
      *) _REST_ARGS+=("$1"); shift ;;
    esac
  done
  # --detail 单独使用时默认 table
  [[ -n "$_DETAIL_ARG" && -z "$_FMT_ARG" ]] && _FMT_ARG="table"
}

subcmd="${1:-}"
shift 2>/dev/null || true

case "$subcmd" in
  get|fund|hist)
    _extract_fmt "$@"
    if [[ -n "$_FMT_ARG" && -f "$_FMT_SH" ]]; then
      _detail_flag="${_DETAIL_ARG:+--detail}"
      case "$subcmd" in
        get)
          if [[ -n "$_DETAIL_ARG" ]]; then
            cmd_get "${_REST_ARGS[@]+"${_REST_ARGS[@]}"}" | _enrich_detail_json | bash "$_FMT_SH" --format "$_FMT_ARG" --detail
          else
            cmd_get "${_REST_ARGS[@]+"${_REST_ARGS[@]}"}" | bash "$_FMT_SH" --format "$_FMT_ARG"
          fi
          ;;
        fund) cmd_fund "${_REST_ARGS[@]+"${_REST_ARGS[@]}"}" | bash "$_FMT_SH" --format "$_FMT_ARG" ${_detail_flag:+"$_detail_flag"} ;;
        hist) cmd_hist "${_REST_ARGS[@]+"${_REST_ARGS[@]}"}" | bash "$_FMT_SH" --format "$_FMT_ARG" ${_detail_flag:+"$_detail_flag"} ;;
      esac
    else
      case "$subcmd" in
        get)  cmd_get  "${_REST_ARGS[@]+"${_REST_ARGS[@]}"}" ;;
        fund) cmd_fund "${_REST_ARGS[@]+"${_REST_ARGS[@]}"}" ;;
        hist) cmd_hist "${_REST_ARGS[@]+"${_REST_ARGS[@]}"}" ;;
      esac
    fi
    ;;
  pfile) cmd_pfile "$@" ;;
  *)
    printf 'usage:\n  sq get   <code> [code...] [--format table|json|csv] [--detail]   查询实时行情\n' >&2
    printf '  sq fund  <code> [code...] [--format table|json|csv] [--detail]   查询场外基金净值\n' >&2
    printf '  sq hist  <code> [opts]    [--format table|json|csv] [--detail]   查询历史K线\n' >&2
    printf '  sq pfile                                                          定位 portfolio.csv 路径\n' >&2
    exit 1
    ;;
esac
