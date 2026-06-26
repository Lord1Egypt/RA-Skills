#!/usr/bin/env bash
# UniFi OS skill shared library — sourced by all scripts

CACHE_DIR="${HOME}/.clawdbot/cache/unifi"
CONFIG_FILE="${UNIFI_CONFIG_FILE:-${HOME}/.clawdbot/credentials/unifi/config.json}"

TTL_INVENTORY=3600   # devices, networks, wlans, port profiles, port forwards
TTL_OPERATIONAL=300  # health, clients, dpi
TTL_ALERTS=60        # alerts always near-fresh

load_config() {
  if [[ -z "${UNIFI_URL}" || -z "${UNIFI_API_KEY}" ]]; then
    [[ ! -f "${CONFIG_FILE}" ]] && { echo "ERROR: Set UNIFI_URL+UNIFI_API_KEY or create ${CONFIG_FILE}" >&2; exit 1; }
    UNIFI_URL=$(jq -r '.url' "${CONFIG_FILE}")
    UNIFI_API_KEY=$(jq -r '.api_key' "${CONFIG_FILE}")
    UNIFI_SITE=$(jq -r '.site // "default"' "${CONFIG_FILE}")
  fi
  UNIFI_SITE="${UNIFI_SITE:-default}"
}

api_get() {
  curl -s --fail-with-body \
    -H "X-API-Key: ${UNIFI_API_KEY}" \
    -H "Accept: application/json" \
    "${UNIFI_URL}${1}"
}

cache_get() {
  local file="${CACHE_DIR}/${1}.json" ttl="${2}"
  [[ ! -f "${file}" ]] && return 1
  local age=$(( $(date +%s) - $(stat -c %Y "${file}") ))
  (( age < ttl )) && { cat "${file}"; return 0; }
  return 1
}

cache_set() {
  mkdir -p "${CACHE_DIR}"
  cat > "${CACHE_DIR}/${1}.json"
}

# Fetch with cache. Args: cache_key api_path ttl
# Set UNIFI_FORCE=1 to bypass cache for all calls
cached_api() {
  local key="$1" path="$2" ttl="$3" data http_out
  if [[ -z "${UNIFI_FORCE}" ]] && data=$(cache_get "${key}" "${ttl}"); then
    echo "${data}"
  else
    http_out=$(api_get "${path}")
    local rc=$?
    if (( rc != 0 )); then
      echo "ERROR: API failed (exit ${rc}): ${path}" >&2
      [[ -n "${http_out}" ]] && echo "Response: ${http_out}" >&2
      exit 1
    fi
    echo "${http_out}" | cache_set "${key}"
    echo "${http_out}"
  fi
}

cache_age() {
  local file="${CACHE_DIR}/${1}.json"
  [[ ! -f "${file}" ]] && { echo "no cache"; return; }
  local age=$(( $(date +%s) - $(stat -c %Y "${file}") ))
  echo "${age}s ago"
}

invalidate() {
  rm -f "${CACHE_DIR}/${1}.json"
}
