#!/usr/bin/env bash
set -euo pipefail

# use-hln-api eval runner
# Requires: curl, jq, yq
# Environment:
#   - HLN_API_KEY for live HL Names API calls, or use the built-in public agent fallback key
#   - OPENAI_API_KEY, VENICE_API_KEY, or ANTHROPIC_API_KEY for answer/judge models

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
EVALS_DIR="$ROOT/evals"
RESULTS_DIR="$ROOT/results"
JUDGE_PROMPT="$SCRIPT_DIR/judge.md"

if [[ -f "$ROOT/.env" ]]; then
  set -a
  # shellcheck disable=SC1091
  source "$ROOT/.env"
  set +a
fi

MODEL="openai/gpt-5.4-nano"
JUDGE_MODEL="openai/gpt-5.4-nano"
EVAL_FILE="$EVALS_DIR/use-hln-api.lvl1.yaml"
EVAL_ID_FILTER=""
RUN_BASELINE=true
HLN_BASE_URL="${HLN_BASE_URL:-https://api.hlnames.xyz/}"
HLN_PUBLIC_AGENT_API_KEY="NILB2EY-R4LUDOA-WN5G5JQ-KHAQOLA"
HLN_API_KEY="${HLN_API_KEY:-$HLN_PUBLIC_AGENT_API_KEY}"
TIMESTAMP="$(date +%Y%m%d-%H%M%S)"

usage() {
  cat <<'EOF'
Usage: ./runner/run.sh [options]

Options:
  --model <provider/model>    Target answer model (default: openai/gpt-5.4-nano)
  --judge <provider/model>    Judge model (default: openai/gpt-5.4-nano)
  --eval <eval-id>            Run only one eval ID
  --eval-file <path>          Path to eval YAML (default: evals/use-hln-api.lvl1.yaml)
  --base-url <url>            HL Names API base URL (default: https://api.hlnames.xyz/)
  --no-baseline               Skip baseline run without the skill bundle
  --help                      Show this message
EOF
}

require_cmd() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "ERROR: Missing required command: $1" >&2
    exit 1
  fi
}

repeat_char() {
  local count="$1"
  local char="$2"
  local out
  printf -v out '%*s' "$count" ''
  printf '%s' "${out// /$char}"
}

print_box() {
  local title="$1"
  shift
  local -a lines=("$@")
  local width="${#title}"
  local line
  local left_pad right_pad border

  for line in "${lines[@]}"; do
    if [[ "${#line}" -gt "$width" ]]; then
      width="${#line}"
    fi
  done

  if [[ "$width" -lt 36 ]]; then
    width=36
  fi

  border="$(repeat_char "$((width + 2))" "═")"
  echo "╔${border}╗"

  left_pad=$(((width - ${#title}) / 2))
  right_pad=$((width - ${#title} - left_pad))
  printf '║ %*s%s%*s ║\n' "$left_pad" '' "$title" "$right_pad" ''

  echo "╠${border}╣"
  for line in "${lines[@]}"; do
    printf '║ %-*s ║\n' "$width" "$line"
  done
  echo "╚${border}╝"
}

timestamp_ms() {
  perl -MTime::HiRes=time -e 'printf "%.0f\n", time() * 1000'
}

resolve_provider() {
  local model="$1"
  echo "${model%%/*}"
}

resolve_model_name() {
  local model="$1"
  echo "${model#*/}"
}

resolve_api() {
  local provider="$1"
  case "$provider" in
    openai) echo "https://api.openai.com/v1/chat/completions" ;;
    venice) echo "https://api.venice.ai/api/v1/chat/completions" ;;
    anthropic) echo "https://api.anthropic.com/v1/messages" ;;
    *) echo "https://api.openai.com/v1/chat/completions" ;;
  esac
}

resolve_key() {
  local provider="$1"
  case "$provider" in
    openai) echo "${OPENAI_API_KEY:-}" ;;
    venice) echo "${VENICE_API_KEY:-}" ;;
    anthropic) echo "${ANTHROPIC_API_KEY:-}" ;;
    *) echo "${OPENAI_API_KEY:-}" ;;
  esac
}

request_completion_raw() {
  local provider="$1"
  local api_url="$2"
  local api_key="$3"
  local model_name="$4"
  local system_msg="$5"
  local user_msg="$6"
  local request_kind="${7:-answer}"

  local payload

  system_msg="$(printf '%s' "$system_msg" | sanitize_ascii)"
  user_msg="$(printf '%s' "$user_msg" | sanitize_ascii)"

  case "$provider" in
    anthropic)
      payload=$(jq -n \
        --arg model "$model_name" \
        --arg system "$system_msg" \
        --arg user "$user_msg" \
        '{
          model: $model,
          max_tokens: 2000,
          temperature: 0.0,
          system: $system,
          messages: [
            {
              role: "user",
              content: [
                { type: "text", text: $user }
              ]
            }
          ]
        }')

      curl -sS "$api_url" \
        -H "x-api-key: $api_key" \
        -H "anthropic-version: 2023-06-01" \
        -H "content-type: application/json" \
        -d "$payload"
      ;;
    *)
      local token_param="max_tokens"
      if [[ "$provider" == "openai" ]]; then
        token_param="max_completion_tokens"
      fi

      if [[ "$provider" == "venice" ]]; then
        if [[ "$request_kind" == "judge" ]]; then
          payload=$(jq -n \
            --arg model "$model_name" \
            --arg system "$system_msg" \
            --arg user "$user_msg" \
            --arg tp "$token_param" \
            '{
              model: $model,
              messages: [
                { role: "system", content: $system },
                { role: "user", content: $user }
              ],
              temperature: 0.0,
              ($tp): 1200,
              venice_parameters: {
                include_venice_system_prompt: false,
                disable_thinking: true,
                strip_thinking_response: true
              }
            }')
        else
          payload=$(jq -n \
            --arg model "$model_name" \
            --arg system "$system_msg" \
            --arg user "$user_msg" \
            --arg tp "$token_param" \
            '{
              model: $model,
              messages: [
                { role: "system", content: $system },
                { role: "user", content: $user }
              ],
              temperature: 0.0,
              ($tp): 2000,
              venice_parameters: {
                include_venice_system_prompt: false
              }
            }')
        fi
      else
        payload=$(jq -n \
          --arg model "$model_name" \
          --arg system "$system_msg" \
          --arg user "$user_msg" \
          --arg tp "$token_param" \
          '{
            model: $model,
            messages: [
              { role: "system", content: $system },
              { role: "user", content: $user }
            ],
            temperature: 0.0,
            ($tp): 2000
          }')
      fi

      curl -sS "$api_url" \
        -H "Authorization: Bearer $api_key" \
        -H "Content-Type: application/json" \
        -d "$payload"
      ;;
  esac
}

extract_text() {
  local provider="$1"
  local response_file="$2"

  case "$provider" in
    anthropic)
      jq -r '[.content[]? | select(.type == "text") | .text] | join("\n")' "$response_file"
      ;;
    *)
      jq -r '
        if (.choices[0].message.content | type) == "string" then
          .choices[0].message.content
        elif (.choices[0].message.content | type) == "array" then
          [.choices[0].message.content[]? | .text // empty] | join("\n")
        else
          "ERROR: No response"
        end
      ' "$response_file"
      ;;
  esac
}

extract_usage_json() {
  local response_file="$1"
  jq -c '.usage // {}' "$response_file" 2>/dev/null || echo "{}"
}

has_provider_error() {
  local response_file="$1"
  jq -e '.error != null' "$response_file" >/dev/null 2>&1
}

provider_error_json() {
  local response_file="$1"
  jq -c '
    if (.error | type) == "object" then
      .error
    elif (.error | type) == "string" then
      {code: "provider_error", message: .error}
    else
      {code: "provider_error", message: "Unknown API error"}
    end
  ' "$response_file"
}

provider_error_message() {
  local response_file="$1"
  jq -r '
    if (.error | type) == "object" then
      .error | ((.code // .type // "provider_error") + ": " + (.message // "Unknown API error"))
    elif (.error | type) == "string" then
      "provider_error: " + .error
    else
      "provider_error: Unknown API error"
    end
  ' "$response_file"
}

venice_get_json() {
  local path="$1"
  curl -sS "https://api.venice.ai/api/v1$path" \
    -H "Authorization: Bearer $VENICE_API_KEY"
}

preflight_venice() {
  local model_name="$1"
  local role_label="$2"
  local limits_json models_json access_permitted usd_balance diem_balance model_found

  if [[ -z "${VENICE_API_KEY:-}" ]]; then
    echo "ERROR: VENICE_API_KEY is required for Venice $role_label model $model_name" >&2
    exit 1
  fi

  limits_json="$(venice_get_json '/api_keys/rate_limits')"
  if ! jq -e '.data != null' >/dev/null 2>&1 <<<"$limits_json"; then
    echo "ERROR: Venice preflight failed while fetching /api_keys/rate_limits" >&2
    echo "$limits_json" >&2
    exit 1
  fi

  access_permitted="$(jq -r '.data.accessPermitted // false' <<<"$limits_json")"
  usd_balance="$(jq -r '.data.balances.USD // 0' <<<"$limits_json")"
  diem_balance="$(jq -r '.data.balances.DIEM // 0' <<<"$limits_json")"

  if [[ "$access_permitted" != "true" ]]; then
    echo "ERROR: Venice preflight reports accessPermitted=false for $role_label model $model_name" >&2
    exit 1
  fi

  models_json="$(venice_get_json '/models?type=text')"
  if ! jq -e '.data != null' >/dev/null 2>&1 <<<"$models_json"; then
    echo "ERROR: Venice preflight failed while fetching /models?type=text" >&2
    echo "$models_json" >&2
    exit 1
  fi

  model_found="$(jq -r --arg model "$model_name" 'any(.data[]?; .id == $model)' <<<"$models_json")"
  if [[ "$model_found" != "true" ]]; then
    echo "ERROR: Venice model '$model_name' was not found in /models?type=text during $role_label preflight" >&2
    exit 1
  fi

  echo "Venice preflight OK for $role_label model $model_name (USD balance: $usd_balance, DIEM balance: $diem_balance)" >&2
}

build_skill_bundle() {
  local skill_path="$1"

  cat "$skill_path/SKILL.md"

  if [[ -d "$skill_path/references" ]]; then
    local ref
    while IFS= read -r ref; do
      printf '\n\n---\n# Reference: %s\n\n' "$(basename "$ref")"
      cat "$ref"
    done < <(find "$skill_path/references" -maxdepth 1 -type f -name '*.md' | sort)
  fi
}

yaml_map_entries_tsv() {
  local expr="$1"
  local input_file="$2"

  yq -o=json "$expr" "$input_file" \
    | jq -r 'to_entries[]? | [.key, (.value | tostring)] | @tsv'
}

sanitize_ascii() {
  perl -CSDA -pe '
    s/\x{2018}|\x{2019}/'\''/g;
    s/\x{201C}|\x{201D}/"/g;
    s/\x{2013}|\x{2014}/-/g;
    s/\x{2026}/.../g;
    s/\x{00A0}/ /g;
    s/[^\x00-\x7F]/ /g;
  '
}

render_template() {
  local template="$1"
  local rendered="$template"
  local key

  for key in "${!CTX[@]}"; do
    rendered="${rendered//\{$key\}/${CTX[$key]}}"
  done

  printf '%s' "$rendered"
}

generate_label() {
  local suffix
  suffix="$(date +%s)"
  echo "eval${suffix: -8}"
}

record_result() {
  local result_json="$1"
  jq ". += [$result_json]" "$RESULTS_TMP" > "$RESULTS_TMP.next"
  mv "$RESULTS_TMP.next" "$RESULTS_TMP"
}

run_live_request() {
  local method="$1"
  local path="$2"
  local body_json="$3"
  local output_file="$4"

  local url="${HLN_BASE_URL%/}$path"
  local status
  local tmp_file

  tmp_file="$(mktemp)"

  if [[ "$body_json" == "null" || -z "$body_json" ]]; then
    status=$(curl -sS -o "$tmp_file" -w "%{http_code}" \
      -X "$method" \
      -H "X-API-Key: $HLN_API_KEY" \
      "$url")
  else
    status=$(curl -sS -o "$tmp_file" -w "%{http_code}" \
      -X "$method" \
      -H "X-API-Key: $HLN_API_KEY" \
      -H "Content-Type: application/json" \
      -d "$body_json" \
      "$url")
  fi

  mv "$tmp_file" "$output_file"
  printf '%s' "$status"
}

check_required_fields() {
  local json_file="$1"
  local eval_file="$2"
  local eval_index="$3"
  local checks='[]'
  local required_len
  local field
  local field_path
  local passed

  required_len=$(yq ".evals[$eval_index].required_fields | length" "$eval_file" 2>/dev/null || echo "0")
  if [[ "$required_len" == "0" || "$required_len" == "null" ]]; then
    echo '{"required_fields":[],"passed":true}'
    return
  fi

  local idx=0
  while [[ "$idx" -lt "$required_len" ]]; do
    field=$(yq -r ".evals[$eval_index].required_fields[$idx]" "$eval_file")
    field_path=".$field"
    if jq -e "$field_path != null" "$json_file" >/dev/null 2>&1; then
      passed=true
    else
      passed=false
    fi

    checks=$(jq \
      --arg field "$field" \
      --argjson passed "$passed" \
      '. += [{field: $field, passed: $passed}]' <<<"$checks")
    idx=$((idx + 1))
  done

  jq -n \
    --argjson required_fields "$checks" \
    '{
      required_fields: $required_fields,
      passed: ([ $required_fields[] | .passed ] | all)
    }'
}

run_model() {
  local model_spec="$1"
  local system_msg="$2"
  local user_msg="$3"
  local output_dir="$4"

  local provider api_url api_key model_name started ended response_file response_text usage_json error_json error_message

  provider="$(resolve_provider "$model_spec")"
  api_url="$(resolve_api "$provider")"
  api_key="$(resolve_key "$provider")"
  model_name="$(resolve_model_name "$model_spec")"

  if [[ -z "$api_key" ]]; then
    echo "ERROR: No API key found for model $model_spec" >&2
    exit 1
  fi

  mkdir -p "$output_dir"
  response_file="$output_dir/raw_response.json"

  started="$(timestamp_ms)"
  request_completion_raw "$provider" "$api_url" "$api_key" "$model_name" "$system_msg" "$user_msg" > "$response_file"
  ended="$(timestamp_ms)"

  usage_json="$(extract_usage_json "$response_file")"

  if has_provider_error "$response_file"; then
    error_json="$(provider_error_json "$response_file")"
    error_message="$(provider_error_message "$response_file")"
    printf 'ERROR: %s\n' "$error_message" > "$output_dir/response.md"
    printf '%s\n' "$error_json" | jq '.' > "$output_dir/error.json"
    jq -n \
      --arg model "$model_spec" \
      --arg provider "$provider" \
      --arg api_url "$api_url" \
      --argjson started "$started" \
      --argjson ended "$ended" \
      --argjson duration_ms "$((ended - started))" \
      --argjson usage "$usage_json" \
      --argjson error "$error_json" \
      '{
        model: $model,
        provider: $provider,
        api_url: $api_url,
        started_ms: $started,
        ended_ms: $ended,
        duration_ms: $duration_ms,
        usage: $usage,
        error: $error
      }' > "$output_dir/timing.json"
    return 1
  fi

  response_text="$(extract_text "$provider" "$response_file")"

  if [[ -z "$response_text" || "$response_text" == "ERROR: No response" ]]; then
    error_json='{"code":"no_response","message":"Provider response did not contain extractable text."}'
    printf 'ERROR: no_response: Provider response did not contain extractable text.\n' > "$output_dir/response.md"
    printf '%s\n' "$error_json" | jq '.' > "$output_dir/error.json"
    jq -n \
      --arg model "$model_spec" \
      --arg provider "$provider" \
      --arg api_url "$api_url" \
      --argjson started "$started" \
      --argjson ended "$ended" \
      --argjson duration_ms "$((ended - started))" \
      --argjson usage "$usage_json" \
      --argjson error "$error_json" \
      '{
        model: $model,
        provider: $provider,
        api_url: $api_url,
        started_ms: $started,
        ended_ms: $ended,
        duration_ms: $duration_ms,
        usage: $usage,
        error: $error
      }' > "$output_dir/timing.json"
    return 1
  fi

  printf '%s\n' "$response_text" > "$output_dir/response.md"
  jq -n \
    --arg model "$model_spec" \
    --arg provider "$provider" \
    --arg api_url "$api_url" \
    --argjson started "$started" \
    --argjson ended "$ended" \
    --argjson duration_ms "$((ended - started))" \
    --argjson usage "$usage_json" \
    '{
      model: $model,
      provider: $provider,
      api_url: $api_url,
      started_ms: $started,
      ended_ms: $ended,
      duration_ms: $duration_ms,
      usage: $usage
    }' > "$output_dir/timing.json"
  return 0
}

judge_response() {
  local eval_id="$1"
  local eval_type="$2"
  local prompt="$3"
  local response_text="$4"
  local expected_facts_json="$5"
  local fail_if_json="$6"
  local output_file="$7"

  local judge_provider judge_api judge_key judge_name judge_input judge_raw_file judge_json error_json error_message candidate_json tmp_output

  judge_provider="$(resolve_provider "$JUDGE_MODEL")"
  judge_api="$(resolve_api "$judge_provider")"
  judge_key="$(resolve_key "$judge_provider")"
  judge_name="$(resolve_model_name "$JUDGE_MODEL")"

  if [[ -z "$judge_key" ]]; then
    echo "ERROR: No API key found for judge model $JUDGE_MODEL" >&2
    exit 1
  fi

  judge_input=$(cat <<EOF
## Eval ID
$eval_id

## Eval Type
$eval_type

## Prompt
$prompt

## Model Response
$response_text

## Expected Facts
$expected_facts_json

## Fail Conditions
$fail_if_json
EOF
)

  judge_raw_file="${output_file%.json}.raw.json"
  request_completion_raw "$judge_provider" "$judge_api" "$judge_key" "$judge_name" "$(cat "$JUDGE_PROMPT")" "$judge_input" "judge" > "$judge_raw_file"

  if has_provider_error "$judge_raw_file"; then
    error_json="$(provider_error_json "$judge_raw_file")"
    error_message="$(provider_error_message "$judge_raw_file")"
    jq -n \
      --arg verdict "ERROR" \
      --arg reasoning "Judge API error: $error_message" \
      --argjson provider_error "$error_json" \
      '{
        verdict: $verdict,
        expected_hits: [],
        expected_misses: [],
        fail_triggers: [],
        reasoning: $reasoning,
        evidence: [],
        provider_error: $provider_error
      }' > "$output_file"
    return 1
  fi

  if jq -e '.choices[0].finish_reason == "length"' "$judge_raw_file" >/dev/null 2>&1; then
    jq -n \
      --arg verdict "ERROR" \
      --arg reasoning "Judge response was truncated before returning valid JSON." \
      '{
        verdict: $verdict,
        expected_hits: [],
        expected_misses: [],
        fail_triggers: [],
        reasoning: $reasoning,
        evidence: []
      }' > "$output_file"
    return 1
  fi

  candidate_json="$(jq -r '
    if (.choices[0].message.content | type) == "string" then
      .choices[0].message.content
    elif (.choices[0].message.content | type) == "array" then
      [.choices[0].message.content[]? | .text // empty] | join("\n")
    else
      ""
    end
  ' "$judge_raw_file" 2>/dev/null || true)"

  candidate_json="$(printf '%s' "$candidate_json" | sed '/^```/d')"

  if ! printf '%s\n' "$candidate_json" | jq -e '.' >/dev/null 2>&1; then
    candidate_json="$(printf '%s' "$candidate_json" | perl -0777 -ne 'print $1 if /(\{.*\})/s')"
  fi

  if [[ -z "$candidate_json" ]]; then
    jq -n \
      --arg verdict "ERROR" \
      --arg reasoning "Judge parse failed: output was not valid JSON." \
      '{
        verdict: $verdict,
        expected_hits: [],
        expected_misses: [],
        fail_triggers: [],
        reasoning: $reasoning,
        evidence: []
      }' > "$output_file"
    printf '%s\n' "$(extract_text "$judge_provider" "$judge_raw_file")" > "${output_file%.json}.candidate.txt"
    return 1
  fi

  tmp_output="$(mktemp)"
  if ! printf '%s\n' "$candidate_json" | jq '.' > "$tmp_output" 2>/dev/null; then
    normalized_candidate="$(printf '%s' "$candidate_json" | perl -0pe 's/\\"/"/g')"
    if printf '%s\n' "$normalized_candidate" | jq '.' > "$tmp_output" 2>/dev/null; then
      candidate_json="$normalized_candidate"
    else
    jq -n \
      --arg verdict "ERROR" \
      --arg reasoning "Judge parse failed: extracted candidate was not valid JSON." \
      '{
        verdict: $verdict,
        expected_hits: [],
        expected_misses: [],
        fail_triggers: [],
        reasoning: $reasoning,
        evidence: []
      }' > "$output_file"
    printf '%s\n' "$candidate_json" > "${output_file%.json}.candidate.txt"
    rm -f "$tmp_output"
    return 1
    fi
  fi

  mv "$tmp_output" "$output_file"
  return 0
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --model) MODEL="$2"; shift 2 ;;
    --judge) JUDGE_MODEL="$2"; shift 2 ;;
    --eval) EVAL_ID_FILTER="$2"; shift 2 ;;
    --eval-file) EVAL_FILE="$2"; shift 2 ;;
    --base-url) HLN_BASE_URL="$2"; shift 2 ;;
    --no-baseline) RUN_BASELINE=false; shift ;;
    --help) usage; exit 0 ;;
    *) echo "Unknown arg: $1" >&2; usage; exit 1 ;;
  esac
done

require_cmd curl
require_cmd jq
require_cmd yq
require_cmd perl

if [[ ! -f "$EVAL_FILE" ]]; then
  echo "ERROR: Eval file not found: $EVAL_FILE" >&2
  exit 1
fi

mkdir -p "$RESULTS_DIR"

SKILL_PATH="$(yq -r '.skill_path' "$EVAL_FILE")"
SKILL_PATH="${SKILL_PATH#./}"
SKILL_PATH="$ROOT/$SKILL_PATH"
SKILL_BUNDLE="$(build_skill_bundle "$SKILL_PATH")"

MODEL_PROVIDER="$(resolve_provider "$MODEL")"
MODEL_NAME_ONLY="$(resolve_model_name "$MODEL")"
JUDGE_PROVIDER="$(resolve_provider "$JUDGE_MODEL")"
JUDGE_NAME_ONLY="$(resolve_model_name "$JUDGE_MODEL")"

if [[ "$MODEL_PROVIDER" == "venice" ]]; then
  preflight_venice "$MODEL_NAME_ONLY" "answer"
fi
if [[ "$JUDGE_PROVIDER" == "venice" ]]; then
  preflight_venice "$JUDGE_NAME_ONLY" "judge"
fi

ITERATION_DIR="$RESULTS_DIR/iteration-$TIMESTAMP"
mkdir -p "$ITERATION_DIR"
RESULTS_TMP="$ITERATION_DIR/results.json"
echo "[]" > "$RESULTS_TMP"

total=0
pass=0
partial=0
fail=0
with_errors=0
baseline_pass=0
baseline_partial=0
baseline_fail=0
baseline_errors=0
error_count=0

print_box "use-hln-api eval runner" \
  "Model:    $MODEL" \
  "Judge:    $JUDGE_MODEL" \
  "Baseline: $RUN_BASELINE" \
  "Base URL: $HLN_BASE_URL" \
  "Time:     $TIMESTAMP"
echo ""

num_evals=$(yq '.evals | length' "$EVAL_FILE")

for i in $(seq 0 $((num_evals - 1))); do
  eval_id="$(yq -r ".evals[$i].id" "$EVAL_FILE")"
  eval_type="$(yq -r ".evals[$i].type" "$EVAL_FILE")"

  if [[ -n "$EVAL_ID_FILTER" && "$eval_id" != "$EVAL_ID_FILTER" ]]; then
    continue
  fi

  total=$((total + 1))
  eval_dir="$ITERATION_DIR/$eval_id"
  mkdir -p "$eval_dir"

  declare -A CTX=()
  CTX[generated_label]="$(generate_label)"

  while IFS=$'\t' read -r key value; do
    if [[ -z "$key" || "$key" == "null" ]]; then
      continue
    fi
    CTX["$key"]="$(printf '%s' "$value" | sed "s/{generated_label}/${CTX[generated_label]}/g")"
  done < <(yaml_map_entries_tsv ".evals[$i].context // {}" "$EVAL_FILE")

  prompt="$(yq -r ".evals[$i].prompt // \"\"" "$EVAL_FILE")"
  expected_facts_json="$(yq -o=json ".evals[$i].expected_facts" "$EVAL_FILE")"
  fail_if_json="$(yq -o=json ".evals[$i].fail_if" "$EVAL_FILE")"
  live_note=""

  if [[ "$eval_type" == "live_http" ]]; then
    if [[ -z "${HLN_API_KEY:-}" ]]; then
      echo "ERROR: HLN_API_KEY is required for live evals." >&2
      exit 1
    fi

    setup_len=$(yq ".evals[$i].setup | length" "$EVAL_FILE" 2>/dev/null || echo "0")
    if [[ "$setup_len" != "0" && "$setup_len" != "null" ]]; then
      for s in $(seq 0 $((setup_len - 1))); do
        setup_id="$(yq -r ".evals[$i].setup[$s].id" "$EVAL_FILE")"
        setup_method="$(yq -r ".evals[$i].setup[$s].method" "$EVAL_FILE")"
        setup_path_template="$(yq -r ".evals[$i].setup[$s].path" "$EVAL_FILE")"
        setup_body_json="$(yq -o=json ".evals[$i].setup[$s].body_json // null" "$EVAL_FILE")"
        setup_path="$(render_template "$setup_path_template")"
        setup_file="$eval_dir/setup-$setup_id.json"
        setup_status="$(run_live_request "$setup_method" "$setup_path" "$setup_body_json" "$setup_file")"

        if [[ "$setup_status" != "200" ]]; then
          echo "  [$eval_id] setup $setup_id failed with HTTP $setup_status"
          record_result "$(jq -n \
            --arg eval_id "$eval_id" \
            --arg eval_type "$eval_type" \
            --arg status "ERROR" \
            --arg message "Setup request $setup_id failed with HTTP $setup_status" \
            '{eval_id: $eval_id, type: $eval_type, verdict: $status, message: $message}')"
          error_count=$((error_count + 1))
          continue 2
        fi

        while IFS=$'\t' read -r out_key jq_query; do
          if [[ -z "$out_key" || "$out_key" == "null" ]]; then
            continue
          fi
          CTX["$out_key"]="$(jq -r "$jq_query" "$setup_file")"
        done < <(yaml_map_entries_tsv ".evals[$i].setup[$s].extract // {}" "$EVAL_FILE")
      done
    fi

    live_method="$(yq -r ".evals[$i].live_request.method" "$EVAL_FILE")"
    live_path_template="$(yq -r ".evals[$i].live_request.path" "$EVAL_FILE")"
    live_body_json="$(yq -o=json ".evals[$i].live_request.body_json // null" "$EVAL_FILE")"
    live_path="$(render_template "$live_path_template")"
    live_file="$eval_dir/live_response.json"
    live_status="$(run_live_request "$live_method" "$live_path" "$live_body_json" "$live_file")"

    mechanical_checks=$(jq -n --arg status "$live_status" '{http_status: $status}')
    if jq -e . "$live_file" >/dev/null 2>&1; then
      pretty_live_response="$(jq '.' "$live_file")"
      mechanical_checks=$(jq '. + {json_parseable: true}' <<<"$mechanical_checks")
    else
      pretty_live_response="$(cat "$live_file")"
      mechanical_checks=$(jq '. + {json_parseable: false}' <<<"$mechanical_checks")
    fi

    field_checks="$(check_required_fields "$live_file" "$EVAL_FILE" "$i")"
    mechanical_checks="$(jq --argjson fields "$field_checks" '. + {field_checks: $fields}' <<<"$mechanical_checks")"
    printf '%s\n' "$mechanical_checks" | jq '.' > "$eval_dir/mechanical_checks.json"

    if [[ "$live_status" != "200" ]]; then
      echo "  [$eval_id] live request failed with HTTP $live_status"
      record_result "$(jq -n \
        --arg eval_id "$eval_id" \
        --arg eval_type "$eval_type" \
        --arg status "ERROR" \
        --arg message "Live request failed with HTTP $live_status" \
        '{eval_id: $eval_id, type: $eval_type, verdict: $status, message: $message}')"
      error_count=$((error_count + 1))
      continue
    fi

    if ! jq -e '.field_checks.passed' "$eval_dir/mechanical_checks.json" >/dev/null 2>&1; then
      echo "  [$eval_id] live response missing required fields"
      record_result "$(jq -n \
        --arg eval_id "$eval_id" \
        --arg eval_type "$eval_type" \
        --arg status "ERROR" \
        --arg message "Live response missing required fields" \
        '{eval_id: $eval_id, type: $eval_type, verdict: $status, message: $message}')"
      error_count=$((error_count + 1))
      continue
    fi

    CTX[live_response]="$pretty_live_response"
    prompt_template="$(yq -r ".evals[$i].prompt_template" "$EVAL_FILE")"
    prompt="$(render_template "$prompt_template")"
    live_note=" (live)"
  fi

  echo -n "  [$eval_id$live_note] "

  with_skill_dir="$eval_dir/with_skill"
  without_skill_dir="$eval_dir/without_skill"
  with_skill_system_prompt=$(cat <<EOF
You are a helpful AI assistant. Use the following skill bundle as authoritative task guidance when answering.
Follow its explicit endpoint-selection, interpretation, workflow, and answer-shape rules when they apply.

--- SKILL BUNDLE ---
$SKILL_BUNDLE
--- END SKILL BUNDLE ---
EOF
)

  with_error_message=""
  if run_model "$MODEL" "$with_skill_system_prompt" "$prompt" "$with_skill_dir"; then
    with_response="$(cat "$with_skill_dir/response.md")"
    if judge_response "$eval_id" "$eval_type" "$prompt" "$with_response" "$expected_facts_json" "$fail_if_json" "$with_skill_dir/judging.json"; then
      with_verdict="$(jq -r '.verdict // "ERROR"' "$with_skill_dir/judging.json")"
    else
      with_verdict="ERROR"
      with_error_message="$(jq -r '.reasoning // "Judge failed."' "$with_skill_dir/judging.json")"
    fi
  else
    with_verdict="ERROR"
    with_error_message="$(jq -r '((.code // .type // "provider_error") + ": " + (.message // "Unknown API error"))' "$with_skill_dir/error.json" 2>/dev/null || echo "Model request failed.")"
  fi

  baseline_verdict=""
  baseline_error_message=""
  if [[ "$RUN_BASELINE" == true ]]; then
    if run_model "$MODEL" "You are a helpful AI assistant." "$prompt" "$without_skill_dir"; then
      without_response="$(cat "$without_skill_dir/response.md")"
      if judge_response "$eval_id" "$eval_type" "$prompt" "$without_response" "$expected_facts_json" "$fail_if_json" "$without_skill_dir/judging.json"; then
        baseline_verdict="$(jq -r '.verdict // "ERROR"' "$without_skill_dir/judging.json")"
      else
        baseline_verdict="ERROR"
        baseline_error_message="$(jq -r '.reasoning // "Judge failed."' "$without_skill_dir/judging.json")"
      fi
    else
      baseline_verdict="ERROR"
      baseline_error_message="$(jq -r '((.code // .type // "provider_error") + ": " + (.message // "Unknown API error"))' "$without_skill_dir/error.json" 2>/dev/null || echo "Model request failed.")"
    fi
  fi

  case "$with_verdict" in
    PASS) pass=$((pass + 1)); echo -n "PASS" ;;
    PARTIAL) partial=$((partial + 1)); echo -n "PARTIAL" ;;
    FAIL) fail=$((fail + 1)); echo -n "FAIL" ;;
    ERROR) with_errors=$((with_errors + 1)); error_count=$((error_count + 1)); echo -n "ERROR" ;;
    *) with_errors=$((with_errors + 1)); error_count=$((error_count + 1)); echo -n "ERROR" ;;
  esac

  if [[ "$RUN_BASELINE" == true ]]; then
    case "$baseline_verdict" in
      PASS) baseline_pass=$((baseline_pass + 1)) ;;
      PARTIAL) baseline_partial=$((baseline_partial + 1)) ;;
      FAIL) baseline_fail=$((baseline_fail + 1)) ;;
      ERROR) baseline_errors=$((baseline_errors + 1)); error_count=$((error_count + 1)) ;;
      *) ;;
    esac
    echo "  baseline: $baseline_verdict"
  else
    echo ""
  fi

  record_result "$(jq -n \
    --arg eval_id "$eval_id" \
    --arg eval_type "$eval_type" \
    --arg prompt "$prompt" \
    --arg verdict "$with_verdict" \
    --arg baseline_verdict "$baseline_verdict" \
    --arg with_path "$with_skill_dir" \
    --arg without_path "$without_skill_dir" \
    --arg with_error "$with_error_message" \
    --arg baseline_error "$baseline_error_message" \
    '{eval_id: $eval_id, type: $eval_type, prompt: $prompt, verdict: $verdict, baseline_verdict: $baseline_verdict, with_skill_dir: $with_path, without_skill_dir: $without_path, with_error: $with_error, baseline_error: $baseline_error}')"
done

with_rate=0
baseline_rate=0

if [[ "$total" -gt 0 ]]; then
  with_rate=$((pass * 100 / total))
  if [[ "$RUN_BASELINE" == true ]]; then
    baseline_rate=$((baseline_pass * 100 / total))
  fi
fi

benchmark_json="$ITERATION_DIR/benchmark.json"
jq -n \
  --arg timestamp "$TIMESTAMP" \
  --arg skill "$(yq -r '.skill' "$EVAL_FILE")" \
  --arg eval_file "$EVAL_FILE" \
  --arg model "$MODEL" \
  --arg judge_model "$JUDGE_MODEL" \
  --arg base_url "$HLN_BASE_URL" \
  --argjson baseline "$RUN_BASELINE" \
  --argjson total "$total" \
  --argjson pass "$pass" \
  --argjson partial "$partial" \
  --argjson fail "$fail" \
  --argjson with_errors "$with_errors" \
  --argjson error_count "$error_count" \
  --argjson baseline_pass "$baseline_pass" \
  --argjson baseline_partial "$baseline_partial" \
  --argjson baseline_fail "$baseline_fail" \
  --argjson baseline_errors "$baseline_errors" \
  --argjson with_rate "$with_rate" \
  --argjson baseline_rate "$baseline_rate" \
  --slurpfile results "$RESULTS_TMP" \
  '{
    timestamp: $timestamp,
    skill: $skill,
    eval_file: $eval_file,
    model: $model,
    judge_model: $judge_model,
    base_url: $base_url,
    baseline_enabled: $baseline,
    summary: {
      total: $total,
      with_skill: {
        pass: $pass,
        partial: $partial,
        fail: $fail,
        errors: $with_errors,
        rate_percent: $with_rate
      },
      without_skill: {
        pass: $baseline_pass,
        partial: $baseline_partial,
        fail: $baseline_fail,
        errors: $baseline_errors,
        rate_percent: $baseline_rate
      },
      errors: $error_count,
      uplift_percent: ($with_rate - $baseline_rate)
    },
    results: $results[0]
  }' > "$benchmark_json"

"$SCRIPT_DIR/report.sh" "$benchmark_json" > "$ITERATION_DIR/RESULTS.md"

echo ""
summary_lines=(
  "Total:      $total"
  "With:       $pass pass / $partial partial / $fail fail / $with_errors error"
)
if [[ "$RUN_BASELINE" == true ]]; then
  summary_lines+=("Baseline:   $baseline_pass pass / $baseline_partial partial / $baseline_fail fail / $baseline_errors error")
fi
summary_lines+=("Errors:     $error_count")
summary_lines+=("")
summary_lines+=("With skill pass rate: ${with_rate}%")
if [[ "$RUN_BASELINE" == true ]]; then
  summary_lines+=("Baseline pass rate:   ${baseline_rate}%")
  summary_lines+=("Uplift:               $((with_rate - baseline_rate))%")
fi

print_box "RESULTS SUMMARY" "${summary_lines[@]}"
echo ""
echo "Results saved to: $ITERATION_DIR"
