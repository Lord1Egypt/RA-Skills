#!/bin/sh

openclaw_status_via_cli() {
  if ! command_exists claw; then
    return 1
  fi

  NODE_TLS_REJECT_UNAUTHORIZED=0 claw skill my >/tmp/skillup-openclaw-status.out 2>/tmp/skillup-openclaw-status.log || true
  return 0
}

check_openclaw() {
  skill_dir=$1
  config_path=$2

  if ! check_common_platform_requirement "openclaw" "$skill_dir"; then
    return 1
  fi

  record_result "openclaw" "$skill_dir" "validated" "OpenClaw 中文社区 publish command is available"
  return 0
}

status_openclaw() {
  skill_dir=$1
  config_path=$2
  local_version=$3
  _unused=$config_path
  slug=$(skill_slug "$skill_dir")

  if command_exists claw; then
    openclaw_status_via_cli
    if grep -F "Client network socket disconnected before secure TLS connection was established" /tmp/skillup-openclaw-status.log >/dev/null 2>&1; then
      record_result "openclaw" "$skill_dir" "status-review" "OpenClaw 中文社区 CLI hit TLS connection issue while fetching skill list" "" "$slug" "$local_version" "tls_error"
      printf '[openclaw] %s remote=unknown status=review\n' "$skill_dir"
    elif grep -E "Spread syntax requires|forEach is not a function|unparsable" /tmp/skillup-openclaw-status.log >/dev/null 2>&1; then
      record_result "openclaw" "$skill_dir" "status-review" "OpenClaw 中文社区 CLI returned unparsable skill list" "" "$slug" "$local_version" "cli_parse_error"
      printf '[openclaw] %s remote=unknown status=review\n' "$skill_dir"
    else
      record_result "openclaw" "$skill_dir" "status-review" "OpenClaw 中文社区 requires CLI or community-side inspection for exact version status" "" "$slug" "$local_version" ""
      printf '[openclaw] %s remote=unknown status=review\n' "$skill_dir"
    fi
  else
    record_result "openclaw" "$skill_dir" "status-unknown" "claw CLI unavailable" "" "$slug" "" ""
    printf '[openclaw] %s remote=unknown\n' "$skill_dir"
  fi
  return 0
}

publish_openclaw() {
  skill_dir=$1
  artifact_path=$2
  config_path=$3
  dry_run=$4
  publish_skill_dir=$(prepare_platform_skill_dir "$skill_dir" openclaw)

  token=$(env_or_config "SKILLUP_OPENCLAW_TOKEN" "$config_path" openclaw token "")
  base_url=$(config_get "$config_path" openclaw base_url "")
  upload_path=$(config_get "$config_path" openclaw upload_path "")
  cli_bin=$(config_get "$config_path" openclaw cli_bin "claw")
  publish_args=$(config_get "$config_path" openclaw publish_args "")

  if [ "$dry_run" -eq 1 ]; then
    if command_exists "$cli_bin"; then
      record_result "openclaw" "$skill_dir" "dry-run" "would run $cli_bin skill publish for $publish_skill_dir"
    else
      record_result "openclaw" "$skill_dir" "dry-run" "would publish artifact $artifact_path"
    fi
    [ "$publish_skill_dir" = "$skill_dir" ] || rm -rf "$(dirname "$publish_skill_dir")"
    return
  fi

  if command_exists "$cli_bin"; then
    if [ -n "$token" ]; then
      SKILLUP_OPENCLAW_TOKEN=$token
      export SKILLUP_OPENCLAW_TOKEN
    fi

    if [ -n "$publish_args" ]; then
      if (cd "$publish_skill_dir" && "$cli_bin" skill publish $publish_args >/tmp/skillup-openclaw-cli.log 2>&1); then
        publish_id=$(python3 - <<'PY'
import re
try:
    text = open('/tmp/skillup-openclaw-cli.log', 'r', encoding='utf-8').read()
except Exception:
    text = ''
match = re.search(r'Skill published:\s*([^\s(]+)', text)
print(match.group(1) if match else '')
PY
        )
        review_state=$(python3 - <<'PY'
try:
    text = open('/tmp/skillup-openclaw-cli.log', 'r', encoding='utf-8').read().lower()
except Exception:
    text = ''
print('pending_review' if 'pending review' in text else '')
PY
        )
        record_result "openclaw" "$skill_dir" "published" "published through $cli_bin skill publish" "" "$publish_id" "$(skill_version "$skill_dir")" "$review_state"
        [ "$publish_skill_dir" = "$skill_dir" ] || rm -rf "$(dirname "$publish_skill_dir")"
        return
      fi
    else
      if (cd "$publish_skill_dir" && "$cli_bin" skill publish >/tmp/skillup-openclaw-cli.log 2>&1); then
        publish_id=$(python3 - <<'PY'
import re
try:
    text = open('/tmp/skillup-openclaw-cli.log', 'r', encoding='utf-8').read()
except Exception:
    text = ''
match = re.search(r'Skill published:\s*([^\s(]+)', text)
print(match.group(1) if match else '')
PY
        )
        review_state=$(python3 - <<'PY'
try:
    text = open('/tmp/skillup-openclaw-cli.log', 'r', encoding='utf-8').read().lower()
except Exception:
    text = ''
print('pending_review' if 'pending review' in text else '')
PY
        )
        record_result "openclaw" "$skill_dir" "published" "published through $cli_bin skill publish" "" "$publish_id" "$(skill_version "$skill_dir")" "$review_state"
        [ "$publish_skill_dir" = "$skill_dir" ] || rm -rf "$(dirname "$publish_skill_dir")"
        return
      fi
    fi
  fi

  if [ -z "$base_url" ] || [ -z "$upload_path" ]; then
    if command_exists "$cli_bin"; then
      record_result "openclaw" "$skill_dir" "failed" "community CLI publish failed and no endpoint is configured"
      [ "$publish_skill_dir" = "$skill_dir" ] || rm -rf "$(dirname "$publish_skill_dir")"
      return 1
    else
      record_result "openclaw" "$skill_dir" "skipped" "endpoint not configured; artifact ready at $artifact_path"
    fi
    [ "$publish_skill_dir" = "$skill_dir" ] || rm -rf "$(dirname "$publish_skill_dir")"
    return
  fi

  auth_header=""
  if [ -n "$token" ]; then
    auth_header="-H Authorization: Bearer $token"
  fi

  if [ -n "$auth_header" ]; then
    http_code=$(curl -sS -o /tmp/skillup-openclaw-response.json -w '%{http_code}' \
      -X POST "$base_url$upload_path" \
      -H "Authorization: Bearer $token" \
      -F "file=@$artifact_path")
  else
    http_code=$(curl -sS -o /tmp/skillup-openclaw-response.json -w '%{http_code}' \
      -X POST "$base_url$upload_path" \
      -F "file=@$artifact_path")
  fi

  if [ "$http_code" -ge 200 ] && [ "$http_code" -lt 300 ]; then
    record_result "openclaw" "$skill_dir" "published" "upload accepted by $base_url$upload_path"
  else
    record_result "openclaw" "$skill_dir" "failed" "HTTP $http_code from $base_url$upload_path"
    [ "$publish_skill_dir" = "$skill_dir" ] || rm -rf "$(dirname "$publish_skill_dir")"
    return 1
  fi

  [ "$publish_skill_dir" = "$skill_dir" ] || rm -rf "$(dirname "$publish_skill_dir")"

  return 0
}
