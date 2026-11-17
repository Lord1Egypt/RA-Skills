#!/usr/bin/env bash
set -euo pipefail

readonly ENDPOINT='https://ai-fabric.patsnap.com/mcp/patsnap-solution-engine?APP_ID=Patsnap'
readonly DEFAULT_TIMEOUT=900

usage() {
  printf 'Usage:\n  %s list [--result-only] [--timeout SECONDS]\n  %s call TOOL [--arguments JSON | --arguments-file FILE] [--result-only] [--timeout SECONDS]\n' "$0" "$0" >&2
  exit 2
}

command -v curl >/dev/null || { printf 'error: curl is required\n' >&2; exit 1; }
command -v jq >/dev/null || { printf 'error: jq is required\n' >&2; exit 1; }

action="${1:-}"
[[ "$action" == 'list' || "$action" == 'call' ]] || usage
shift

tool=''
arguments='{}'
arguments_file=''
timeout="$DEFAULT_TIMEOUT"
result_only=false

if [[ "$action" == 'call' ]]; then
  tool="${1:-}"
  [[ -n "$tool" && "$tool" != --* ]] || usage
  shift
fi

while (( $# )); do
  case "$1" in
    --arguments) [[ $# -ge 2 && -z "$arguments_file" ]] || usage; arguments="$2"; shift 2 ;;
    --arguments-file) [[ $# -ge 2 && "$arguments" == '{}' ]] || usage; arguments_file="$2"; shift 2 ;;
    --timeout) [[ $# -ge 2 ]] || usage; timeout="$2"; shift 2 ;;
    --result-only) result_only=true; shift ;;
    *) usage ;;
  esac
done

[[ "$timeout" =~ ^[1-9][0-9]*$ ]] || { printf 'error: timeout must be a positive integer\n' >&2; exit 2; }
if [[ -n "$arguments_file" ]]; then
  [[ -r "$arguments_file" ]] || { printf 'error: cannot read arguments file: %s\n' "$arguments_file" >&2; exit 1; }
  arguments="$(<"$arguments_file")"
fi
jq -e 'type == "object"' >/dev/null <<<"$arguments" || { printf 'error: arguments must be a JSON object\n' >&2; exit 2; }

if [[ "$action" == 'list' ]]; then
  payload="$(jq -cn '{jsonrpc:"2.0",id:1,method:"tools/list",params:{}}')"
else
  payload="$(jq -cn --arg name "$tool" --argjson arguments "$arguments" '{jsonrpc:"2.0",id:1,method:"tools/call",params:{name:$name,arguments:$arguments}}')"
fi

body_file="$(mktemp)"
trap 'rm -f "$body_file"' EXIT
set +e
http_code="$(curl -sS --max-time "$timeout" -o "$body_file" -w '%{http_code}' \
  -X POST "$ENDPOINT" \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  --data-binary "$payload")"
curl_status=$?
set -e
if (( curl_status != 0 )); then
  if (( curl_status == 28 )); then
    printf 'error: request timed out after %s seconds; the server may still be processing the task, so do not retry automatically\n' "$timeout" >&2
  else
    printf 'error: curl request failed with exit code %s\n' "$curl_status" >&2
  fi
  exit 1
fi

if [[ ! "$http_code" =~ ^2 ]]; then
  printf 'error: HTTP %s: %s\n' "$http_code" "$(<"$body_file")" >&2
  exit 1
fi

if jq -e . "$body_file" >/dev/null 2>&1; then
  response="$(jq -c . "$body_file")"
else
  response="$(sed -n 's/^data:[[:space:]]*//p' "$body_file" | jq -c 'select(.id == 1)' 2>/dev/null | tail -n 1 || true)"
fi
[[ -n "$response" ]] || { printf 'error: MCP endpoint returned no final response\n' >&2; exit 1; }
if jq -e '.error != null' >/dev/null <<<"$response"; then
  jq -c '.error' <<<"$response" >&2
  exit 1
fi
if jq -e '.result.isError == true' >/dev/null <<<"$response"; then
  jq -c '.result.content // .result' <<<"$response" >&2
  exit 1
fi
if [[ "$result_only" == true ]]; then
  jq '
    .result as $result
    | if $result.structuredContent != null then $result.structuredContent
      elif ($result.content | type) == "array" then
        ($result.content | map(select(.type == "text")) | .[0].text) as $text
        | if $text == null then $result else (($text | fromjson?) // $text) end
      else $result
      end
  ' <<<"$response"
else
  jq . <<<"$response"
fi
