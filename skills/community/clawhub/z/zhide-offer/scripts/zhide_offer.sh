#!/usr/bin/env bash
set -euo pipefail
BASE_DIR="$(cd "$(dirname "$0")" && pwd)"

# Let users keep the key in the environment or a local config file.
if [[ -z "${ZHIDE_OFFER_KEY:-}" && -f "$BASE_DIR/config.json" ]]; then
  :
fi

cmd="${1:-}"
shift || true

case "$cmd" in
  jobs-search)
    exec node "$BASE_DIR/jobs_search.js" "$@"
    ;;
  job-get)
    exec node "$BASE_DIR/jobs_get.js" "$@"
    ;;
  interviews-search)
    exec node "$BASE_DIR/interviews_search.js" "$@"
    ;;
  interview-get)
    exec node "$BASE_DIR/interviews_get.js" "$@"
    ;;
  quota)
    exec node "$BASE_DIR/account_entitlements.js" "$@"
    ;;
  help|--help|-h|"")
    cat <<'EOF'
Usage:
  zhide_offer.sh jobs-search <keyword> [--company 公司] [--city 城市] [--size 数量]
  zhide_offer.sh job-get <岗位ID>
  zhide_offer.sh interviews-search <关键词> [--company 公司] [--city 城市] [--tag 校招|实习|社招] [--limit 数量]
  zhide_offer.sh interview-get <面经ID>
  zhide_offer.sh quota
EOF
    ;;
  *)
    echo "未知命令: $cmd" >&2
    echo >&2
    "$0" help >&2
    exit 1
    ;;
esac
