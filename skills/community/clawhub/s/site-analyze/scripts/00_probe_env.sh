#!/bin/bash
# 探测当前节点网络环境，结果写入 ~/.site-analyzer-env.json
# 用法: bash 00_probe_env.sh [--force]

ENV_FILE="$HOME/.site-analyzer-env.json"

if [[ -f "$ENV_FILE" && "$1" != "--force" ]]; then
  echo "[env] Already probed. Use --force to re-probe."
  cat "$ENV_FILE"
  exit 0
fi

echo "[env] Probing network environment..." >&2

# 本机出口 IP
MY_IP=$(curl -s --max-time 5 https://api.ipify.org 2>/dev/null || \
        curl -s --max-time 5 http://ip-api.com/json 2>/dev/null | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('query',''))" 2>/dev/null)

# 出口 IP 归属
IP_INFO=$(curl -s --max-time 5 "http://ip-api.com/json/${MY_IP}" 2>/dev/null)

# 默认 DNS
DEFAULT_DNS=$(cat /etc/resolv.conf 2>/dev/null | grep '^nameserver' | awk '{print $2}' | head -3 | tr '\n' ',')

# 测试 dig 是否可用
DIG_OK=$(which dig >/dev/null 2>&1 && echo true || echo false)
TRACEROUTE_OK=$(which traceroute >/dev/null 2>&1 && echo true || echo false)
PING_OK=$(which ping >/dev/null 2>&1 && echo true || echo false)
WHOIS_OK=$(which whois >/dev/null 2>&1 && echo true || echo false)

COUNTRY=$(echo "$IP_INFO" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('country','unknown'))" 2>/dev/null)
CITY=$(echo "$IP_INFO" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('city','unknown'))" 2>/dev/null)
ISP=$(echo "$IP_INFO" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('isp','unknown'))" 2>/dev/null)
AS=$(echo "$IP_INFO" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('as','unknown'))" 2>/dev/null)

python3 -c "
import json
data = {
  'my_ip': '$MY_IP',
  'country': '$COUNTRY',
  'city': '$CITY',
  'isp': '$ISP',
  'as': '$AS',
  'default_dns': '$DEFAULT_DNS'.strip(','),
  'tools': {
    'dig': '$DIG_OK' == 'true',
    'traceroute': '$TRACEROUTE_OK' == 'true',
    'ping': '$PING_OK' == 'true',
    'whois': '$WHOIS_OK' == 'true'
  }
}
print(json.dumps(data, ensure_ascii=False, indent=2))
" | tee "$ENV_FILE"

echo "[env] Saved to $ENV_FILE" >&2
