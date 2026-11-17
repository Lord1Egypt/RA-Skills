#!/bin/sh
# Shared help and structured environment diagnostics for CLI-backed skills.

cli_usage() {
  cat <<'EOF'
Usage:
  sh scripts/run-cli.sh [--help | <command> [args...]]
  sh scripts/run-cli.sh help                 # Current CLI command reference
  sh scripts/cli-state.sh [status]           # JSON environment diagnostics
  sh scripts/cli-state.sh [help | -h | --help]

Help works without installing the CLI or configuring an API key.
Business queries require tencent-news-cli and a user-configured API key.
See references/installation-guide.md and references/env-setup-guide.md.
Diagnostics may exit 0 with success:false; this does not mean a query succeeded.
EOF
}

cli_run_help() {
  if [ "$#" -eq 0 ]; then cli_usage; exit 0; fi
  if [ "$#" -eq 1 ]; then
    case "$1" in
      -h|--help) cli_usage; exit 0 ;;
      help) CLI_HELP_REQUEST=true ;;
    esac
  fi
}

# Do not include raw errors or credential values in agent-facing diagnostics.
fail() {
  case "$1" in
    "cli not found"*)
      if [ "${CLI_HELP_REQUEST:-false}" = true ]; then cli_usage; exit 0; fi
      cli_result_fields CLI_NOT_INSTALLED
      ;;
    *) cli_result_fields INVALID_ARGUMENT ;;
  esac
  printf '{%s}\n' "$CLI_RESULT_FIELDS"
  exit 1
}

cli_result_fields() {
  case "$1" in
    CLI_NOT_INSTALLED)
      message='Tencent News CLI is not installed or could not be found.'
      next_steps='["Follow references/installation-guide.md, then run cli-state status again."]'
      ;;
    API_KEY_MISSING)
      message='No API key was detected in the current CLI environment.'
      next_steps='["Check the shell configuration as described in SKILL.md before setting a new key.","If missing, obtain a key at https://news.qq.com/exchange?scene=appkey and configure it locally."]'
      ;;
    ENVIRONMENT_CHECK_FAILED)
      message='The CLI environment could not be verified.'
      next_steps='["Follow references/env-setup-guide.md; do not share credentials or raw logs."]'
      ;;
    API_KEY_UNAUTHORIZED)
      message='The API key is invalid, expired, or unauthorized.'
      next_steps='["Obtain an authorized key at https://news.qq.com/exchange?scene=appkey and configure it locally."]'
      ;;
    INVALID_ARGUMENT)
      message='Invalid script arguments or skill metadata. Read --help and check SKILL.md.'
      next_steps='["Run the script with --help."]'
      ;;
    READY)
      CLI_RESULT_FIELDS='"success":true,"status":"ready","data":null,"error":null,"nextSteps":[]'
      return
      ;;
  esac
  result_status=environment_not_ready
  [ "$1" != INVALID_ARGUMENT ] || result_status=invalid_request
  CLI_RESULT_FIELDS="\"success\":false,\"status\":\"$result_status\",\"data\":null,\"error\":{\"code\":\"$1\",\"message\":\"$message\"},\"nextSteps\":$next_steps"
}

cli_state_fields() {
  if [ "$CLI_EXISTS" != true ]; then
    cli_result_fields CLI_NOT_INSTALLED
  elif [ "$APIKEY_STATUS" = missing ]; then
    cli_result_fields API_KEY_MISSING
  elif [ "$APIKEY_STATUS" != configured ]; then
    if printf '%s' "$APIKEY_ERROR" | grep -qiE 'invalid api key|unauthorized|401|403|API Key 无效|鉴权|认证失败'; then
      cli_result_fields API_KEY_UNAUTHORIZED
    else
      cli_result_fields ENVIRONMENT_CHECK_FAILED
    fi
  else
    cli_result_fields READY
  fi
  [ "$APIKEY_ERROR" = null ] || APIKEY_ERROR='"Unable to verify API key state; see error.code and the setup guide."'
  [ "$UPDATE_ERROR" = null ] || UPDATE_ERROR='"Unable to check CLI updates."'
  CLI_RESULT_FIELDS="$CLI_RESULT_FIELDS,"
}
