#!/usr/bin/env bash

set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  robot_send.sh text --robot-id <robot_id> --robot-key <robot_key> --content <text> [options]
  robot_send.sh file --robot-id <robot_id> --robot-key <robot_key> --file <path> [options]

Required:
  --robot-id <value>   Target robot id
  --robot-key <value>  Robot key used to sign /robot/send

Text mode:
  --content <value>    Text content to send

File mode:
  --file <path>        File to upload by multipart/form-data
  --content <value>    Optional text content attached to the file

Options:
  --base-url <value>       /robot/send URL. Default: http://localhost:8093/robot/send
  --cvs-id <value>         Optional conversation id. If omitted, server may use the robot owner P2P conversation
  --refer-msg-id <value>   Optional referenced message id
  --msg-id <value>         Optional message id. Default: generated automatically
  --noncestr <value>       Optional nonce. Default: generated automatically
  --timestamp <value>      Optional unix timestamp in seconds. Default: current time
  --at <uid1,uid2>         Optional comma-separated at_uid_list for text JSON body
  --mentioned <uid1,uid2>  Optional comma-separated mentioned_list for text JSON body
  --dry-run                Print request details without sending
  --help                   Show this help message

Examples:
  ./shell/robot_send.sh text \
    --robot-id robot_xxx \
    --robot-key rk_xxx \
    --content "hello robot"

  ./shell/robot_send.sh file \
    --robot-id robot_xxx \
    --robot-key rk_xxx \
    --content "please handle this file" \
    --file ./demo.pdf
EOF
}

require_command() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "missing required command: $1" >&2
    exit 1
  fi
}

urlencode() {
  python3 -c 'import sys, urllib.parse; print(urllib.parse.quote_plus(sys.argv[1]))' "$1"
}

uuid_hex() {
  python3 -c 'import uuid; print(uuid.uuid4().hex)'
}

json_body() {
  python3 - "$msg_id" "$cvs_id" "$refer_msg_id" "$content" "$at_uid_list" "$mentioned_list" <<'PY'
import json
import sys

msg_id, cvs_id, refer_msg_id, content, at_uid_list, mentioned_list = sys.argv[1:]

def split_csv(value):
    return [item.strip() for item in value.split(",") if item.strip()]

head = {"msg_id": msg_id}
if cvs_id:
    head["cvs_id"] = cvs_id
if refer_msg_id:
    head["refer_msg_id"] = refer_msg_id

body = {}
if content:
    body["content"] = content
if at_uid_list:
    body["at_uid_list"] = split_csv(at_uid_list)
if mentioned_list:
    body["mentioned_list"] = split_csv(mentioned_list)

print(json.dumps({"cmd": "msg", "head": head, "body": body}, ensure_ascii=False, separators=(",", ":")))
PY
}

mode="${1:-}"
if [[ "${mode}" == "text" || "${mode}" == "file" ]]; then
  shift
else
  mode=""
fi

base_url="http://localhost:8093/robot/send"
robot_id=""
robot_key=""
cvs_id=""
refer_msg_id=""
msg_id=""
noncestr=""
timestamp=""
content=""
file_path=""
at_uid_list=""
mentioned_list=""
dry_run=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --mode)
      mode="${2:-}"
      shift 2
      ;;
    --base-url)
      base_url="${2:-}"
      shift 2
      ;;
    --robot-id)
      robot_id="${2:-}"
      shift 2
      ;;
    --robot-key)
      robot_key="${2:-}"
      shift 2
      ;;
    --cvs-id)
      cvs_id="${2:-}"
      shift 2
      ;;
    --refer-msg-id)
      refer_msg_id="${2:-}"
      shift 2
      ;;
    --msg-id)
      msg_id="${2:-}"
      shift 2
      ;;
    --noncestr)
      noncestr="${2:-}"
      shift 2
      ;;
    --timestamp)
      timestamp="${2:-}"
      shift 2
      ;;
    --content)
      content="${2:-}"
      shift 2
      ;;
    --file)
      file_path="${2:-}"
      shift 2
      ;;
    --at)
      at_uid_list="${2:-}"
      shift 2
      ;;
    --mentioned)
      mentioned_list="${2:-}"
      shift 2
      ;;
    --dry-run)
      dry_run=true
      shift
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      echo "unknown argument: $1" >&2
      usage
      exit 1
      ;;
  esac
done

require_command curl
require_command openssl
require_command python3

if [[ "${mode}" != "text" && "${mode}" != "file" ]]; then
  echo "mode must be text or file" >&2
  usage
  exit 1
fi

if [[ -z "${robot_id}" || -z "${robot_key}" ]]; then
  echo "robot_id and robot_key are required" >&2
  usage
  exit 1
fi

if [[ "${mode}" == "text" && -z "${content}" ]]; then
  echo "text mode requires --content" >&2
  exit 1
fi

if [[ "${mode}" == "file" ]]; then
  if [[ -z "${file_path}" ]]; then
    echo "file mode requires --file" >&2
    exit 1
  fi
  if [[ ! -f "${file_path}" ]]; then
    echo "file does not exist: ${file_path}" >&2
    exit 1
  fi
fi

timestamp="${timestamp:-$(date +%s)}"
msg_id="${msg_id:-msg_${timestamp}_$(uuid_hex)}"
noncestr="${noncestr:-nonce_${timestamp}_$(uuid_hex)}"

# Keep this signing text aligned with talk-robots/common.RobotSendSignPayload:
# sorted keys and URL-encoded values.
signing_text="msg_id=$(urlencode "${msg_id}")&noncestr=$(urlencode "${noncestr}")&robot_id=$(urlencode "${robot_id}")&timestamp=$(urlencode "${timestamp}")"
sign="$(printf '%s' "${signing_text}" | openssl dgst -sha256 -hmac "${robot_key}" | awk '{print $2}')"
request_url="${base_url}?robot_id=$(urlencode "${robot_id}")&noncestr=$(urlencode "${noncestr}")&timestamp=$(urlencode "${timestamp}")&msg_id=$(urlencode "${msg_id}")&sign=$(urlencode "${sign}")"

echo "mode=${mode}"
echo "request_url=${request_url}"
echo "msg_id=${msg_id}"
echo "noncestr=${noncestr}"
echo "timestamp=${timestamp}"
echo "signing_text=${signing_text}"
echo "sign=${sign}"

if [[ "${dry_run}" == true ]]; then
  if [[ "${mode}" == "text" ]]; then
    echo "json_body=$(json_body)"
  else
    echo "file=${file_path}"
    [[ -n "${content}" ]] && echo "content=${content}"
  fi
  exit 0
fi

if [[ "${mode}" == "text" ]]; then
  body="$(json_body)"
  curl -sS -X POST "${request_url}" \
    -H "Content-Type: application/json" \
    --data-binary "${body}" \
    -w '\nHTTP_STATUS=%{http_code}\n'
else
  curl_args=(
    -sS
    -X POST "${request_url}"
    -F "msg_id=${msg_id}"
    -F "file=@${file_path}"
    -w $'\nHTTP_STATUS=%{http_code}\n'
  )
  [[ -n "${cvs_id}" ]] && curl_args+=(-F "cvs_id=${cvs_id}")
  [[ -n "${refer_msg_id}" ]] && curl_args+=(-F "refer_msg_id=${refer_msg_id}")
  [[ -n "${content}" ]] && curl_args+=(-F "content=${content}")
  curl "${curl_args[@]}"
fi
