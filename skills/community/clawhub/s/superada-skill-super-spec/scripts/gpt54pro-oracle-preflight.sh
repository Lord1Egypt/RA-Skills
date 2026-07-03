#!/usr/bin/env bash
set -euo pipefail

# Fast fail/route gate for product-spec oracle work.
# This checks the direct Azure OpenAI Responses route before a spec job burns time on it.

BASE_URL="${GPT54PRO_BASE_URL:-${AZURE_OPENAI_BASE_URL:-${OPENAI_BASE_URL:-http://127.0.0.1:4000/v1}}}"
PRIMARY_MODEL="${GPT54PRO_PRIMARY_MODEL:-gpt-5.4-pro}"
FALLBACK_MODELS_CSV="${GPT54PRO_FALLBACK_MODELS:-gpt-5.4,gpt-chat-latest}"
TIMEOUT_SECONDS="${GPT54PRO_TIMEOUT_SECONDS:-20}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
DEFAULT_STATE_DIR="${REPO_ROOT}/output/reliability"
if ! mkdir -p "${DEFAULT_STATE_DIR}" 2>/dev/null; then
  DEFAULT_STATE_DIR="${TMPDIR:-/tmp}/clawd-reliability"
  mkdir -p "${DEFAULT_STATE_DIR}"
fi
STATE_FILE="${GPT54PRO_STATE_FILE:-${DEFAULT_STATE_DIR}/gpt54pro-oracle-health.jsonl}"
PROMPT_MARKER="GPT54PRO_ORACLE_PREFLIGHT_OK"

if [[ -z "${OPENAI_API_KEY:-}" ]]; then
  if [[ -n "${AZURE_OPENAI_API_KEY:-}" ]]; then
    OPENAI_API_KEY="${AZURE_OPENAI_API_KEY}"
  else
    echo "ERROR: set AZURE_OPENAI_API_KEY or OPENAI_API_KEY" >&2
    exit 2
  fi
fi

API_KEY="${OPENAI_API_KEY}"
mkdir -p "$(dirname "${STATE_FILE}")"

probe_model() {
  local model="$1"
  local started ended elapsed response http_code body tmp
  started="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
  tmp="$(mktemp)"

  set +e
  http_code="$(
    curl -sS \
      --max-time "${TIMEOUT_SECONDS}" \
      -o "${tmp}" \
      -w "%{http_code}" \
      "${BASE_URL%/}/responses" \
      -H "Authorization: Bearer ${API_KEY}" \
      -H "Content-Type: application/json" \
      --data "{\"model\":\"${model}\",\"input\":\"Return exactly ${PROMPT_MARKER}\",\"max_output_tokens\":32}" \
      2>/dev/null
  )"
  local rc=$?
  set -e

  ended="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
  body="$(cat "${tmp}" 2>/dev/null || true)"
  rm -f "${tmp}"

  if [[ "${rc}" -ne 0 ]]; then
    printf '{"ts":"%s","route":"%s","model":"%s","ok":false,"http_code":null,"error":"curl_failed","started":"%s","ended":"%s"}\n' \
      "${ended}" "${BASE_URL}" "${model}" "${started}" "${ended}" >> "${STATE_FILE}"
    return 1
  fi

  if [[ "${http_code}" != "200" ]]; then
    printf '{"ts":"%s","route":"%s","model":"%s","ok":false,"http_code":%s,"error":"non_200","started":"%s","ended":"%s"}\n' \
      "${ended}" "${BASE_URL}" "${model}" "${http_code}" "${started}" "${ended}" >> "${STATE_FILE}"
    return 1
  fi

  if [[ "${body}" != *"${PROMPT_MARKER}"* ]]; then
    printf '{"ts":"%s","route":"%s","model":"%s","ok":false,"http_code":200,"error":"marker_missing","started":"%s","ended":"%s"}\n' \
      "${ended}" "${BASE_URL}" "${model}" "${started}" "${ended}" >> "${STATE_FILE}"
    return 1
  fi

  printf '{"ts":"%s","route":"%s","model":"%s","ok":true,"http_code":200,"started":"%s","ended":"%s"}\n' \
    "${ended}" "${BASE_URL}" "${model}" "${started}" "${ended}" >> "${STATE_FILE}"
  printf '%s\n' "${model}"
  return 0
}

if chosen="$(probe_model "${PRIMARY_MODEL}")"; then
  printf '{"status":"ok","primary":"%s","chosen":"%s","state_file":"%s"}\n' "${PRIMARY_MODEL}" "${chosen}" "${STATE_FILE}"
  exit 0
fi

IFS=',' read -r -a fallback_models <<< "${FALLBACK_MODELS_CSV}"
for model in "${fallback_models[@]}"; do
  model="$(printf '%s' "${model}" | xargs)"
  [[ -z "${model}" ]] && continue
  if chosen="$(probe_model "${model}")"; then
    printf '{"status":"degraded","primary":"%s","chosen":"%s","state_file":"%s"}\n' "${PRIMARY_MODEL}" "${chosen}" "${STATE_FILE}"
    exit 0
  fi
done

printf '{"status":"failed","primary":"%s","chosen":null,"state_file":"%s"}\n' "${PRIMARY_MODEL}" "${STATE_FILE}"
exit 1
