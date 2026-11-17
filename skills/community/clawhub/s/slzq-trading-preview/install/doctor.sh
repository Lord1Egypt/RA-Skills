#!/usr/bin/env bash
set -euo pipefail

SKILL_NAME="slzq-trading"
DOMAIN_ENV="SLZQ_OPENCLAW_DOMAIN"
API_KEY_ENV="SLZQ_OPENCLAW_API_KEY"
TRADING_ENV="SLZQ_OPENCLAW_ENV"

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MCP_ENTRY="${ROOT_DIR}/runtime/mcp/dist/index.js"
LEGACY_MCP_ENTRY="$(cd "${ROOT_DIR}/.." && pwd)/${SKILL_NAME}-mcp/dist/index.js"

fail() {
  echo "FAIL: $1"
  echo "下一步：$2"
  exit 1
}

pass() {
  echo "PASS: $1"
}

command -v node >/dev/null 2>&1 || fail "未找到 node" "请安装 Node.js 18 或更高版本后重试。"
NODE_MAJOR="$(node -p "Number(process.versions.node.split('.')[0])")"
if [ "${NODE_MAJOR}" -lt 18 ]; then
  fail "Node.js 版本过低：$(node -v)" "请升级到 Node.js 18 或更高版本。"
fi
pass "Node.js $(node -v)"

DEFAULT_DOMAIN="https://slzqapi.sxslqhsh.com"
CREDENTIALS_FILE="${HOME}/.slzq-trading/credentials.json"

DOMAIN="${!DOMAIN_ENV:-}"
API_KEY="${!API_KEY_ENV:-}"
ENV_VALUE="${!TRADING_ENV:-sim}"

# 未设置时使用生产域名
DOMAIN_SOURCE="env"
if [ -z "${DOMAIN}" ]; then
  DOMAIN="${DEFAULT_DOMAIN}"
  DOMAIN_SOURCE="default"
  echo "INFO: 未设置 ${DOMAIN_ENV}，按生产域名 ${DEFAULT_DOMAIN} 检查。"
fi
# 生产域名不要带 /mobile-api
case "${DOMAIN}" in
  */mobile-api* ) fail "${DOMAIN_ENV} 不应包含 /mobile-api" "去掉结尾的 /mobile-api，例如 https://slzqapi.sxslqhsh.com" ;;
  http://*|https://* ) pass "${DOMAIN_ENV} 格式正确" ;;
  * ) fail "${DOMAIN_ENV} 必须以 http:// 或 https:// 开头" "请填写完整域名，例如 https://slzqapi.sxslqhsh.com " ;;
esac

# 基址连通性 + 服务端能力探测（免鉴权，新老版本都可调）
HEALTH_JSON="$(curl -fsS --max-time 10 "${DOMAIN}/mobile-api/open/v1/health" 2>/dev/null || true)"
if [ -z "${HEALTH_JSON}" ]; then
  fail "基址不可达：${DOMAIN}/mobile-api/open/v1/health" \
    "请确认能访问生产地址 https://slzqapi.sxslqhsh.com/mobile-api（${DOMAIN_ENV} 不要带 /mobile-api）。"
fi
pass "基址可达：${DOMAIN}/mobile-api"
AUTH_LOGIN_SUPPORTED="false"
case "${HEALTH_JSON}" in
  *'"authLoginSupported":true'* )
    AUTH_LOGIN_SUPPORTED="true"
    pass "服务端支持免密钥登录领钥" ;;
  * )
    if [ "${DOMAIN_SOURCE}" = "default" ]; then
      echo "WARN: 生产域名 ${DOMAIN} 未上线免密钥登录接口。"
    else
      echo "WARN: ${DOMAIN} 未上线免密钥登录接口（health 无 authLoginSupported）。"
    fi ;;
esac

# 未配置密钥不再判定为失败：可在会话中用手机号 + 验证码登录领取
if [ -z "${API_KEY}" ] && [ -f "${CREDENTIALS_FILE}" ]; then
  pass "已找到登录落盘的凭据文件：${CREDENTIALS_FILE}"
elif [ -z "${API_KEY}" ] && [ "${AUTH_LOGIN_SUPPORTED}" = "true" ]; then
  echo "WARN: 未配置 ${API_KEY_ENV}，也没有本地凭据文件。两种取钥方式任选其一："
  echo "  方式 A · 会话内登录领取（只需手机号 + 短信验证码；账号已有模拟盘密钥时会原样返回，不会顶掉旧的）"
  echo "        已注册 MCP：slzq_open_v1_auth_agreement → slzq_open_v1_auth_send_code → slzq_open_v1_auth_login。"
  echo "        没有 MCP（这三个接口均免鉴权，纯 HTTP 同样可用）："
  echo "          GET  ${DOMAIN}/mobile-api/open/v1/auth/agreement"
  echo "          POST ${DOMAIN}/mobile-api/open/v1/auth/sms/send  -d '{\"mobileNum\":\"…\"}'"
  echo "          POST ${DOMAIN}/mobile-api/open/v1/auth/login     -d '{\"mobileNum\":\"…\",\"verifyCode\":\"…\",\"agreementVersion\":\"…\"}'"
  echo "  方式 B · 去 App 复制已有密钥（要用实盘密钥时只能走这条）"
  echo "        App「我的 → 期货辅助交易」→ 有效密钥列表显示完整密钥，一键复制后配置到 ${API_KEY_ENV}。"
elif [ -z "${API_KEY}" ] && [ "${DOMAIN_SOURCE}" = "default" ]; then
  # 没配密钥 + 探的是默认域名：先纠正域名，再谈"服务端不支持"，否则会把用户错误地推去 App 领钥
  echo "WARN: 未配置 ${API_KEY_ENV}，且生产域名未上线免密钥登录。"
  echo "下一步：请在 App「我的 → 期货辅助交易」生成模拟盘密钥并配置到 ${API_KEY_ENV}。"
  echo "        不要改域名。"
elif [ -z "${API_KEY}" ]; then
  echo "WARN: 未配置 ${API_KEY_ENV}，且 ${DOMAIN} 不支持免密钥登录。"
  echo "下一步：请在 App「我的 → 期货辅助交易」生成模拟盘密钥并配置到 ${API_KEY_ENV}。"
  echo "        不要去试 /open/v1/auth/*：旧版服务端会用鉴权拦截器把这些不存在的路径拦下、"
  echo "        报 10411「缺少 API Key」，那是假象，不代表你需要补密钥。"
else
  case "${API_KEY}" in
    oc.*.* ) pass "${API_KEY_ENV} 看起来是完整 OpenClaw Key" ;;
    * ) fail "${API_KEY_ENV} 格式不像 OpenClaw Key" "正确格式应类似 oc.<16位>.<secret>，请重新复制完整密钥；或改用登录流程重新领取。" ;;
  esac
fi

case "${ENV_VALUE}" in
  sim|live ) pass "${TRADING_ENV}=${ENV_VALUE}" ;;
  * ) fail "${TRADING_ENV} 值无效：${ENV_VALUE}" "请设置为小写 sim 或 live。" ;;
esac

if [ -f "${MCP_ENTRY}" ]; then
  pass "找到一体包 MCP 入口：${MCP_ENTRY}"
elif [ -f "${LEGACY_MCP_ENTRY}" ]; then
  pass "找到兼容 MCP 入口：${LEGACY_MCP_ENTRY}"
else
  fail "未找到 MCP 入口 dist/index.js" "请确认已下载新版能力包，或在 ${SKILL_NAME}-mcp 目录执行 npm ci && npm run build。"
fi

if [ -f "${MCP_ENTRY}" ] && [ ! -d "${ROOT_DIR}/runtime/mcp/node_modules" ]; then
  echo "WARN: 一体包 MCP 依赖尚未安装。下一步：执行 cd ${ROOT_DIR}/runtime/mcp && npm ci，或直接运行 install/test_mcp_tools.sh 自动安装。"
fi

echo "doctor 完成：环境变量、Node、基址连通性与 MCP 入口检查通过。"
