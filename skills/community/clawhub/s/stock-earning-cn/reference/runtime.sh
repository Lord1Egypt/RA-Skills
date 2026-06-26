#!/bin/bash

se_get_file_perm() {
  local file="$1"
  local perm=""
  if stat -f "%Lp" "$file" >/dev/null 2>&1; then
    perm="$(stat -f "%Lp" "$file" 2>/dev/null || true)"
  elif stat -c "%a" "$file" >/dev/null 2>&1; then
    perm="$(stat -c "%a" "$file" 2>/dev/null || true)"
  fi
  echo "$perm"
}

se_try_load_env_file() {
  local file="$1"
  [ -f "$file" ] || return 1
  local perm
  perm="$(se_get_file_perm "$file")"
  if [ -n "$perm" ] && [ "$perm" != "600" ] && [ "$perm" != "400" ]; then
    echo "⚠️ WARNING: API Key 文件权限不是 600/400（当前: $perm）。建议执行: chmod 600 \"$file\""
  fi
  source "$file"
  return 0
}

se_load_api_key() {
  if [ -n "$STOCK_API_KEY" ]; then
    return 0
  fi

  local candidates=(
    "$STOCKEARNING_ENV_FILE"
    "$HOME/.openclaw/stockearning.env"
    "$HOME/.config/openclaw/stockearning.env"
    "$HOME/.config/hermes/stockearning.env"
    "$HOME/.hermes/stockearning.env"
  )

  local f
  for f in "${candidates[@]}"; do
    if se_try_load_env_file "$f"; then
      break
    fi
  done

  if [ -z "$STOCK_API_KEY" ]; then
    cat >&2 <<'EOF'
⚠️ 尚未配置 StockEarning 的 API Key（STOCK_API_KEY），无法调用 mystockearning.cn 的接口。

【如何获取】
  1) 打开 https://www.mystockearning.cn 注册账号；
  2) 等待管理员审核通过后，在控制台获取您的 API Key。

【如何配置（仅需一次）】
  mkdir -p ~/.config/stockearning
  (umask 077; printf 'export STOCK_API_KEY="sk_您的API_Key"\n' > ~/.config/stockearning/stockearning.env)
  source ~/.config/stockearning/stockearning.env

  或者直接在当前终端临时设置：
  export STOCK_API_KEY="sk_您的API_Key"

配置完成后，重新运行本命令即可。
EOF
    return 1
  fi

  return 0
}

se_require_trusted_base_url() {
  STOCK_BASE_URL="${STOCK_BASE_URL%/}"

  if [[ "$STOCK_BASE_URL" != https://* ]]; then
    echo "Error: STOCK_BASE_URL must start with https://"
    return 1
  fi

  if [ -n "$DEFAULT_STOCK_BASE_URL" ] && [ "$STOCK_BASE_URL" != "$DEFAULT_STOCK_BASE_URL" ]; then
    if [ "${STOCKEARNING_TRUST_BASE_URL:-0}" != "1" ]; then
      echo "Error: STOCK_BASE_URL is customized. Refusing to send API key to an untrusted endpoint."
      echo "If you trust this endpoint, set STOCKEARNING_TRUST_BASE_URL=1 and try again."
      return 1
    fi

    if ! curl -sS --max-time 5 -I "$STOCK_BASE_URL" >/dev/null 2>&1; then
      echo "Error: Cannot verify custom STOCK_BASE_URL is reachable."
      return 1
    fi
  fi

  return 0
}

se_request() {
  local method="$1"
  local path="$2"
  local json_data="$3"

  if ! se_load_api_key; then
    return 1
  fi

  if ! se_require_trusted_base_url; then
    return 1
  fi

  local url="${STOCK_BASE_URL}${path}"
  local tmp_body
  tmp_body="$(mktemp 2>/dev/null || echo "/tmp/stockearning_body.$$")"

  local http_code=""
  local curl_exit=0

  if [ "$method" = "GET" ]; then
    http_code="$(curl -sS -o "$tmp_body" -w "%{http_code}" -H "X-API-Key: $STOCK_API_KEY" "$url")"
    curl_exit=$?
  elif [ "$method" = "POST" ] || [ "$method" = "PUT" ]; then
    if [ -n "$json_data" ]; then
      http_code="$(curl -sS -o "$tmp_body" -w "%{http_code}" -X "$method" -H "Content-Type: application/json" -H "X-API-Key: $STOCK_API_KEY" -d "$json_data" "$url")"
      curl_exit=$?
    else
      http_code="$(curl -sS -o "$tmp_body" -w "%{http_code}" -X "$method" -H "X-API-Key: $STOCK_API_KEY" "$url")"
      curl_exit=$?
    fi
  else
    echo "Error: Unsupported HTTP method $method" >&2
    rm -f "$tmp_body" >/dev/null 2>&1 || true
    return 1
  fi

  local body
  body="$(cat "$tmp_body" 2>/dev/null || true)"
  rm -f "$tmp_body" >/dev/null 2>&1 || true

  if [ $curl_exit -ne 0 ]; then
    echo "网络错误：curl exit=$curl_exit" >&2
    [ -n "$body" ] && echo "$body" >&2
    return $curl_exit
  fi

  if [[ "$http_code" =~ ^2 ]]; then
    printf '%s' "$body"
    return 0
  fi

  if [ "$http_code" = "401" ]; then
    echo "授权出现问题（401 Unauthorized）。请检查：" >&2
    echo "1) 是否已正确设置 STOCK_API_KEY" >&2
    echo "2) API Key 是否有效/未过期" >&2
    echo "3) STOCK_BASE_URL 是否指向正确的后端地址" >&2
    [ -n "$body" ] && echo "服务器返回: $body" >&2
    return 1
  fi

  if [ "$http_code" = "403" ]; then
    echo "权限/订阅出现问题（403 Forbidden）。可能原因：" >&2
    echo "1) 账号未通过管理员审批或被禁用" >&2
    echo "2) 没有有效订阅或订阅已过期" >&2
    [ -n "$body" ] && echo "服务器返回: $body" >&2
    return 1
  fi

  if [ "$http_code" = "429" ]; then
    echo "请求频率/配额超限（429 Too Many Requests）。请稍后重试或升级订阅。" >&2
    [ -n "$body" ] && echo "服务器返回: $body" >&2
    return 1
  fi

  echo "请求失败（HTTP $http_code）。" >&2
  [ -n "$body" ] && echo "服务器返回: $body" >&2
  return 1
}
