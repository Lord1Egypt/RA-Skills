#!/bin/sh

clawhub_remote_version_from_file() {
  status_file=$1
  [ -f "$status_file" ] || return 1

  python3 - "$status_file" <<'PY'
import json
import sys

path = sys.argv[1]
try:
    payload = json.load(open(path, encoding='utf-8'))
except Exception:
    raise SystemExit(1)

version = (
    payload.get("latestVersion", {}).get("version")
    or payload.get("skill", {}).get("tags", {}).get("latest")
    or ""
)
if not version:
    raise SystemExit(1)
print(version)
PY
}

clawhub_remote_summary_from_file() {
  status_file=$1
  [ -f "$status_file" ] || return 1

  python3 - "$status_file" <<'PY'
import json
import sys

path = sys.argv[1]
try:
    payload = json.load(open(path, encoding='utf-8'))
except Exception:
    raise SystemExit(1)

summary = payload.get("skill", {}).get("summary", "")
if not summary:
    raise SystemExit(1)
print(summary)
PY
}

check_clawhub() {
  skill_dir=$1
  config_path=$2

  if ! check_common_platform_requirement "clawhub" "$skill_dir"; then
    return 1
  fi

  record_result "clawhub" "$skill_dir" "validated" "ClawHub publish command is available"
  return 0
}

status_clawhub() {
  skill_dir=$1
  config_path=$2
  local_version=$3
  _unused=$config_path
  slug=$(skill_slug "$skill_dir")

  if command_exists clawhub; then
    if clawhub inspect "$slug" --json >/tmp/skillup-clawhub-status.json 2>/tmp/skillup-clawhub-status.log; then
      remote_version=$(clawhub_remote_version_from_file /tmp/skillup-clawhub-status.json 2>/dev/null || true)
      remote_summary=$(clawhub_remote_summary_from_file /tmp/skillup-clawhub-status.json 2>/dev/null || true)
      if [ -n "$remote_version" ] && [ "$remote_version" = "$local_version" ]; then
        record_result "clawhub" "$skill_dir" "in-sync" "ClawHub version matches local${remote_summary:+; summary: $remote_summary}" "https://clawhub.ai/skills/$slug" "$slug" "$remote_version" ""
        printf '[clawhub] %s remote=%s status=in-sync\n' "$skill_dir" "$remote_version"
      elif [ -n "$remote_version" ]; then
        record_result "clawhub" "$skill_dir" "status-review" "ClawHub remote version is $remote_version${remote_summary:+; summary: $remote_summary}" "https://clawhub.ai/skills/$slug" "$slug" "$remote_version" ""
        printf '[clawhub] %s remote=%s status=review\n' "$skill_dir" "$remote_version"
      else
        record_result "clawhub" "$skill_dir" "status-review" "ClawHub skill exists; inspect output for exact version details" "https://clawhub.ai/skills/$slug" "$slug" "$local_version" ""
        printf '[clawhub] %s remote=exists status=review\n' "$skill_dir"
      fi
    elif grep -E "security scan is pending|hidden while security scan is pending" /tmp/skillup-clawhub-status.log >/dev/null 2>&1; then
      record_result "clawhub" "$skill_dir" "status-review" "ClawHub security scan pending" "" "$slug" "$local_version" "security_scan_pending"
      printf '[clawhub] %s remote=pending status=review\n' "$skill_dir"
    else
      record_result "clawhub" "$skill_dir" "out-of-sync" "ClawHub skill not found" "" "$slug" "" ""
      printf '[clawhub] %s remote=missing status=out-of-sync\n' "$skill_dir"
    fi
  else
    record_result "clawhub" "$skill_dir" "status-unknown" "clawhub CLI unavailable" "" "$slug" "" ""
    printf '[clawhub] %s remote=unknown\n' "$skill_dir"
  fi
  return 0
}

publish_clawhub() {
  skill_dir=$1
  artifact_path=$2
  config_path=$3
  dry_run=$4
  publish_skill_dir=$(prepare_platform_skill_dir "$skill_dir" clawhub)
  skill_dir_abs=$(CDPATH= cd -- "$publish_skill_dir" && pwd)

  token=$(env_or_config "SKILLUP_CLAWHUB_TOKEN" "$config_path" clawhub token "")
  if [ -z "$token" ]; then
    token=$(env_or_config "CLAWHUB_TOKEN" "$config_path" clawhub token "")
  fi
  base_url=$(config_get "$config_path" clawhub base_url "https://clawhub.ai")
  upload_path=$(config_get "$config_path" clawhub upload_path "/api/v1/skills")
  cli_bin=$(config_get "$config_path" clawhub cli_bin "clawhub")
  site_url=$(config_get "$config_path" clawhub site_url "https://clawhub.ai")
  registry_url=$(config_get "$config_path" clawhub registry_url "https://clawhub.ai")
  version=$(skill_version "$skill_dir")

  if [ "$dry_run" -eq 1 ]; then
    if command_exists "$cli_bin"; then
      record_result "clawhub" "$skill_dir" "dry-run" "would run $cli_bin publish $skill_dir_abs --version $version"
    else
      record_result "clawhub" "$skill_dir" "dry-run" "would publish artifact $artifact_path"
    fi
    [ "$publish_skill_dir" = "$skill_dir" ] || rm -rf "$(dirname "$publish_skill_dir")"
    return
  fi

  if command_exists "$cli_bin"; then
    if [ -n "$token" ]; then
      CLAWHUB_TOKEN=$token
      export CLAWHUB_TOKEN
      "$cli_bin" login --token "$token" --site "$site_url" --registry "$registry_url" --no-input >/tmp/skillup-clawhub-login.log 2>&1 || true
    fi

    if "$cli_bin" publish "$skill_dir_abs" --version "$version" --site "$site_url" --registry "$registry_url" --no-input >/tmp/skillup-clawhub-cli.log 2>&1; then
      record_result "clawhub" "$skill_dir" "published" "published through $cli_bin publish" "https://clawhub.ai/skills/$(skill_slug "$skill_dir")" "$(skill_slug "$skill_dir")" "$version" ""
      [ "$publish_skill_dir" = "$skill_dir" ] || rm -rf "$(dirname "$publish_skill_dir")"
      return
    fi
  fi

  if [ -z "$token" ]; then
    if grep -F "multiple paginated queries" /tmp/skillup-clawhub-cli.log >/dev/null 2>&1; then
      record_result "clawhub" "$skill_dir" "failed_platform_bug" "ClawHub server bug while creating publisher/search digests"
    else
      record_result "clawhub" "$skill_dir" "failed" "ClawHub CLI publish failed and no API token is available for HTTP fallback"
    fi
    [ "$publish_skill_dir" = "$skill_dir" ] || rm -rf "$(dirname "$publish_skill_dir")"
    return 1
  fi

  if [ -z "$base_url" ] || [ -z "$upload_path" ]; then
    if command_exists "$cli_bin"; then
      if grep -F "multiple paginated queries" /tmp/skillup-clawhub-cli.log >/dev/null 2>&1; then
        record_result "clawhub" "$skill_dir" "failed_platform_bug" "ClawHub server bug while creating publisher/search digests"
      else
        record_result "clawhub" "$skill_dir" "failed" "clawhub CLI publish failed and no endpoint is configured"
      fi
      [ "$publish_skill_dir" = "$skill_dir" ] || rm -rf "$(dirname "$publish_skill_dir")"
      return 1
    else
      record_result "clawhub" "$skill_dir" "skipped" "endpoint not configured; artifact ready at $artifact_path"
    fi
    [ "$publish_skill_dir" = "$skill_dir" ] || rm -rf "$(dirname "$publish_skill_dir")"
    return
  fi

  if [ -n "$token" ]; then
    http_code=$(curl -sS -o /tmp/skillup-clawhub-response.json -w '%{http_code}' \
      -X POST "$base_url$upload_path" \
      -H "Authorization: Bearer $token" \
      -F "file=@$artifact_path")
  else
    http_code=$(curl -sS -o /tmp/skillup-clawhub-response.json -w '%{http_code}' \
      -X POST "$base_url$upload_path" \
      -F "file=@$artifact_path")
  fi

  if [ "$http_code" -ge 200 ] && [ "$http_code" -lt 300 ]; then
    record_result "clawhub" "$skill_dir" "published" "upload accepted by $base_url$upload_path"
  else
    record_result "clawhub" "$skill_dir" "failed" "HTTP $http_code from $base_url$upload_path"
    [ "$publish_skill_dir" = "$skill_dir" ] || rm -rf "$(dirname "$publish_skill_dir")"
    return 1
  fi

  [ "$publish_skill_dir" = "$skill_dir" ] || rm -rf "$(dirname "$publish_skill_dir")"

  return 0
}
