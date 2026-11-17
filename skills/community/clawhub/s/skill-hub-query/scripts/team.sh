#!/usr/bin/env bash
# skill-hub-query/scripts/team.sh
# Team management: search teams / list members / add / remove.
#
# Usage:
#   team.sh search <keyword>                            # search teams (get teamId)
#   team.sh my                                          # my teams (with myRole)
#   team.sh info <teamId>                               # team detail
#   team.sh list <teamId> [--role R] [--all] [--json]   # members (full pagination)
#   team.sh member <teamId> <email>                     # is this email in the team?
#   team.sh add <teamId> <email> [email...] [--role member|admin|viewer] [--yes]
#   team.sh remove <teamId> <email> [email...] [--yes]
#
# Endpoints (optional -- see references/api.md §5). A Hub without them should
# expose SKILL_HUB_DISABLE_TEAM=1 so this script refuses to run instead of
# producing confusing errors (same convention as edit.sh):
#   GET    <team prefix>/team/search?keyword=&current=&size=
#   GET    <team prefix>/team/my?current=&size=
#   GET    <team prefix>/team/{teamId}
#   GET    <team prefix>/team/{teamId}/members?current=&size=
#   POST   <team prefix>/team/{teamId}/members/add     body {"members":[{userEmail,role}]}
#   DELETE <team prefix>/team/{teamId}/members/remove  body {"userEmails":["..."]}
#
# ⚠️ Field-tested pitfalls (all verified against a live Hub, do not "fix" by
# intuition):
#   1. add returns 200 success for a NON-EXISTENT email too, and writes a
#      dangling record (user.handle == userEmail) -> the response cannot be
#      trusted; this script always re-verifies against the member list.
#   2. add is idempotent-success for members already in the team -> we
#      de-duplicate before submitting and report the existing role instead.
#   3. the pagination parameter is current= (page= is silently ignored and
#      forever returns page 1).
#   4. valid roles: member / admin / viewer (owner / guest / editor -> 400).
#   5. remove returns silent 200 for emails not in the team -> verified after.
#   6. team-not-found: HTTP 200 + code=400 (fake-200, same family as the
#      download endpoint) -> always check the business envelope, not just HTTP.
#
# Safety guardrails (same conventions as edit.sh):
#   1. add / remove are write ops: show the target team + roster, wait for a
#      y/N answer (--yes must be user-authorized; an agent must never pass it).
#   2. email format is validated client-side (the server does not validate;
#      garbage strings get written as dangling records).
#   3. full de-dup before add (never silently change an existing member's role).
#   4. post-write verification: re-pull the member list and check each email.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=_lib.sh
source "${SCRIPT_DIR}/_lib.sh"

# Team endpoints live under the Hub's API root but outside the skill path
# family (see references/api.md §5). Default mirrors the edit.sh convention:
# an overridable prefix with a sane default.
TEAM_PREFIX="${SKILL_HUB_TEAM_PREFIX:-/api/team}"

# ---------- constants ----------
PAGE_SIZE=200          # members per page (size=200 verified working)
MAX_PAGES=200           # pagination runaway defense (200 * 200 = 40k members cap)
VALID_ROLES="member admin viewer"

if [[ "${SKILL_HUB_DISABLE_TEAM:-0}" == "1" ]]; then
  echo "[error] team management is disabled on this Hub (SKILL_HUB_DISABLE_TEAM=1)" >&2
  exit 1
fi

usage() {
  cat <<'EOF'
skill-hub-query/scripts/team.sh - Skill Hub team member management

Usage:
  team.sh search <keyword>                             # search teams (get teamId)
  team.sh my                                           # my teams (with myRole)
  team.sh info <teamId>                                # team detail
  team.sh list <teamId> [--role R] [--all] [--json]    # members (first 30 + total by default)
  team.sh member <teamId> <email>                      # is this email in the team, what role
  team.sh add <teamId> <email> [email...] [--role R]   # add members (--role default member)
  team.sh remove <teamId> <email> [email...] [--yes]   # remove members

Options:
  --role member|admin|viewer    role for add (default member; owner/guest/editor are rejected server-side)
  --all                         list: show everything (default first 30)
  --json                        list: raw JSON array output (for agents / pipes)
  --yes                         skip the interactive confirmation (user-authorized only; agents must not pass it)
  -h, --help                    show this help

Exit codes:
  0 = success (including idempotent "already in team")
  1 = failure (bad args / team not found / verification failed)
  2 = member query: email not in team

Safety guardrails:
  1. add / remove show the target team + full roster and wait for confirmation (--yes requires user authorization)
  2. email format validated client-side (the server does not validate; garbage becomes a dangling record)
  3. full de-dup before add; existing members are skipped with their current role reported
  4. after every write the member list is re-pulled and verified; failures are reported honestly
EOF
  exit "${1:-0}"
}

# ---------- HTTP wrapper (team endpoints; token attached when configured) ----------
# stdout: response body (JSON)
# failure: non-200 HTTP, or business envelope code != 200 -> error + exit 1
team_http() {
  local method="$1" path="$2" body="${3:-}"
  local endpoint
  endpoint="$(load_endpoint)"

  local tmp_body tmp_code
  tmp_body="$(shq_mktemp)"
  tmp_code="$(shq_mktemp)"

  local -a curl_opts=(-sS --max-time 30 -o "$tmp_body" -w "%{http_code}" -X "$method")
  local token=""
  if token="$(load_token 2>/dev/null)"; then
    curl_opts+=(-H "Authorization: Bearer ${token}")
  fi
  if [[ -n "$body" ]]; then
    curl_opts+=(-H "Content-Type: application/json" -d "$body")
  fi

  if ! curl "${curl_opts[@]}" "${endpoint}${path}" > "$tmp_code" 2>/dev/null; then
    echo "[error] network failure: ${method} ${path} (check connectivity)" >&2
    rm -f "$tmp_body" "$tmp_code"
    exit 1
  fi

  local http
  http="$(cat "$tmp_code")"
  if [[ "$http" != "200" ]]; then
    echo "[error] HTTP ${http}: ${method} ${path}" >&2
    [[ -s "$tmp_body" ]] && head -c 300 "$tmp_body" >&2
    rm -f "$tmp_body" "$tmp_code"
    exit 1
  fi

  # Business envelope check (fake-200: team-not-found / invalid role are both
  # HTTP 200 + code=400).
  local biz_code
  biz_code="$(jq -r '.code // empty' "$tmp_body" 2>/dev/null || echo "")"
  if [[ -z "$biz_code" ]]; then
    echo "[error] response is not valid JSON (or missing code field): ${method} ${path}" >&2
    head -c 300 "$tmp_body" >&2
    rm -f "$tmp_body" "$tmp_code"
    exit 1
  fi
  if [[ "$biz_code" != "200" ]]; then
    local msg
    msg="$(jq -r '.message // .error // ""' "$tmp_body" 2>/dev/null || echo "")"
    echo "[error] business error code=${biz_code}: ${msg}" >&2
    rm -f "$tmp_body" "$tmp_code"
    exit 1
  fi

  cat "$tmp_body"
  rm -f "$tmp_body" "$tmp_code"
}

team_get()    { team_http GET "$1"; }
team_post()   { team_http POST "$1" "$2"; }
team_delete() { team_http DELETE "$1" "$2"; }

# ---------- argument validation ----------
validate_team_id() {
  local id="$1"
  if [[ ! "$id" =~ ^[0-9]+$ ]]; then
    echo "[error] team id must be a positive integer (got: ${id}; if you don't know the id, run: team.sh search <keyword>)" >&2
    exit 1
  fi
}

validate_email() {
  local email="$1"
  # The server does not validate email format (garbage becomes a dangling
  # record), so the client must.
  if [[ ! "$email" =~ ^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$ ]]; then
    echo "[error] invalid email format: ${email}" >&2
    exit 1
  fi
}

validate_role() {
  local role="$1"
  local r
  local ok=0
  for r in $VALID_ROLES; do
    if [[ "$r" == "$role" ]]; then ok=1; fi
  done
  if [[ "$ok" != "1" ]]; then
    echo "[error] invalid role: ${role} (valid: ${VALID_ROLES}; the server rejects the rest too)" >&2
    exit 1
  fi
}

# ---------- team info ----------
# stdout: team detail JSON (the data part)
fetch_team_detail() {
  local team_id="$1"
  team_get "${TEAM_PREFIX}/${team_id}" | jq '.data'
}

# ---------- member list (full pagination) ----------
# stdout: all pages' records merged into one JSON array (temp files keep large
# JSON out of argv / here-strings)
fetch_all_members() {
  local team_id="$1"
  local tmp_all tmp_resp
  tmp_all="$(shq_mktemp shq-members)"
  tmp_resp="$(shq_mktemp shq-page)"
  echo '[]' > "$tmp_all"
  local page=1 got=0
  while :; do
    team_get "${TEAM_PREFIX}/${team_id}/members?current=${page}&size=${PAGE_SIZE}" > "$tmp_resp"
    jq 'if has("data") and (.data | has("records")) then .data.records else [] end' "$tmp_resp" > "${tmp_resp}.records"
    jq -s '.[0] + .[1]' "$tmp_all" "${tmp_resp}.records" > "${tmp_all}.new"
    mv "${tmp_all}.new" "$tmp_all"
    got="$(jq 'length' "${tmp_resp}.records")"
    rm -f "${tmp_resp}.records"
    if (( got < PAGE_SIZE )); then
      break
    fi
    if (( page >= MAX_PAGES )); then
      echo "[error] pagination anomaly: ${MAX_PAGES} pages without an end, aborting (runaway defense)" >&2
      rm -f "$tmp_all" "$tmp_resp"
      return 1
    fi
    page=$((page + 1))
  done
  cat "$tmp_all"
  rm -f "$tmp_all" "$tmp_resp"
}

# Find one email in the members array. Input: file path + email. Output: the
# member record (empty string when not found).
find_member() {
  local members_file="$1" email="$2"
  jq -r --arg e "$email" '[.[] | select((.user.email // "") == $e)][0] // empty' "$members_file"
}

# Dangling-record detection: handle/displayName both equal to the email and no
# avatar -> the account probably does not exist (the server writes such a
# record even for non-existent emails).
is_dangling_member() {
  local flag
  flag="$(jq -r 'if ((.user.handle // "") == (.user.email // "")) and
                  ((.user.displayName // "") == (.user.email // "")) and
                  ((.user.avatar // null) == null)
                then "yes" else "no" end')"
  [[ "$flag" == "yes" ]]
}

# ---------- display ----------
# My role in a team (GET /team/{id} does not return myRole; page through /team/my).
fetch_my_role() {
  local team_id="$1" page=1
  while :; do
    local resp role records_n total
    resp="$(team_get "${TEAM_PREFIX}/my?current=${page}&size=100")" || return 1
    role="$(jq -r --arg id "$team_id" 'first(.data.records[] | select((.id|tostring) == $id) | .myRole) // empty' <<<"$resp")"
    if [[ -n "$role" ]]; then
      echo "$role"
      return 0
    fi
    records_n="$(jq '.data.records | length' <<<"$resp")"
    total="$(jq -r '.data.total // 0' <<<"$resp")"
    if (( records_n < 100 )) || (( page * 100 >= total )); then
      return 1
    fi
    page=$((page + 1))
  done
}

print_team_summary() {
  local detail="$1"
  local id name role members skills
  id="$(jq -r '.id' <<<"$detail")"
  name="$(jq -r '.teamName // "?"' <<<"$detail")"
  members="$(jq -r '.memberCount // "?"' <<<"$detail")"
  skills="$(jq -r '.skillCount // "?"' <<<"$detail")"
  role="$(jq -r '.myRole // empty' <<<"$detail")"
  if [[ -z "$role" || "$role" == "null" ]]; then
    role="$(fetch_my_role "$id" 2>/dev/null || true)"
  fi
  [[ -z "$role" ]] && role="not a member"
  echo "  target team: ${name} (ID ${id}, my role: ${role}, ${members} members, ${skills} skills)"
}

# Interactive confirmation; non-interactive (stdin closed) fails loudly
# instead of hanging.
confirm_or_die() {
  local prompt="$1"
  if [[ "$YES" != "1" ]]; then
    local ans=""
    if ! read -r -p "${prompt} [y/N] " ans; then
      echo "[abort] non-interactive session without --yes; nothing was changed." >&2
      exit 1
    fi
    if [[ "${ans,,}" != "y" && "${ans,,}" != "yes" ]]; then
      echo "[abort] cancelled by user; nothing was changed."
      exit 0
    fi
  fi
}

# ---------- subcommands ----------
cmd_search() {
  local keyword="$1"
  local resp
  resp="$(team_get "${TEAM_PREFIX}/search?keyword=$(jq -rn --arg k "$keyword" '$k|@uri')&size=20")"
  local total
  total="$(jq -r '.data.total // 0' <<<"$resp")"
  if [[ "$total" == "0" ]]; then
    echo "no teams match \"${keyword}\""
    return 0
  fi
  echo "teams matching \"${keyword}\" (${total} total):"
  jq -r '.data.records[] | "  [\(.id)] \(.teamName) — my role: \(.myRole // "not a member") · \(.memberCount) members · \(.skillCount) skills\n      \(.teamDescription // "")"' <<<"$resp"
}

cmd_my() {
  local resp
  resp="$(team_get "${TEAM_PREFIX}/my?size=100")"
  local total
  total="$(jq -r '.data.total // 0' <<<"$resp")"
  if [[ "$total" == "0" ]]; then
    echo "you are not in any team"
    return 0
  fi
  echo "my teams (${total} total):"
  jq -r '.data.records[] | "  [\(.id)] \(.teamName) — my role: \(.myRole // "?") · \(.memberCount) members · \(.skillCount) skills"' <<<"$resp"
}

cmd_info() {
  local team_id="$1"
  validate_team_id "$team_id"
  local detail
  detail="$(fetch_team_detail "$team_id")"
  jq '{id, teamName, teamEmail, teamDescription, visibility, status, myRole, memberCount, skillCount, createdBy: .createdBy.email, createdAt}' <<<"$detail"
}

cmd_list() {
  local team_id="$1" role_filter="${ROLE_FILTER:-}" show_all="${SHOW_ALL:-0}" as_json="${AS_JSON:-0}"
  validate_team_id "$team_id"
  local members_file
  members_file="$(shq_mktemp shq-members)"
  fetch_all_members "$team_id" > "$members_file"

  if [[ -n "$role_filter" ]]; then
    jq --arg r "$role_filter" '[.[] | select(.role == $r)]' "$members_file" > "${members_file}.f"
    mv "${members_file}.f" "$members_file"
  fi

  if [[ "$as_json" == "1" ]]; then
    jq '.' "$members_file"
    rm -f "$members_file"
    return 0
  fi

  local total
  total="$(jq 'length' "$members_file")"
  echo "team ${team_id} members (${total} total$([[ -n "$role_filter" ]] && echo ", role=${role_filter}")):"
  if [[ "$total" == "0" ]]; then
    rm -f "$members_file"
    return 0
  fi

  local shown_file="$members_file"
  if [[ "$show_all" != "1" ]]; then
    shown_file="${members_file}.shown"
    jq '.[0:30]' "$members_file" > "$shown_file"
  fi
  jq -r '.[] | "  \(.user.email)  \(.user.displayName // "?")  [\(.role)]  joined \(.createdAt // "?")"' "$shown_file"
  local shown_n
  shown_n="$(jq 'length' "$shown_file")"
  if [[ "$show_all" != "1" && "$total" -gt "$shown_n" ]]; then
    echo "  ... ($((total - shown_n)) more omitted; --all for everything, --json for raw data)"
  fi
  rm -f "$members_file" "${members_file}.shown"
}

cmd_member() {
  local team_id="$1" email="$2"
  validate_team_id "$team_id"
  validate_email "$email"
  local members_file rec_file
  members_file="$(shq_mktemp shq-members)"
  fetch_all_members "$team_id" > "$members_file"
  rec_file="$(shq_mktemp shq-rec)"
  find_member "$members_file" "$email" > "$rec_file"
  if [[ ! -s "$rec_file" ]]; then
    echo "[error] ${email} is not in team ${team_id}" >&2
    rm -f "$members_file" "$rec_file"
    exit 2
  fi
  # stdout carries JSON only (pipeable to jq); human-readable notes go to stderr
  echo "ok: ${email} is in team ${team_id}:" >&2
  jq '{email: .user.email, displayName: .user.displayName, handle: .user.handle, role, grantedBy: .grantedBy.email, grantedByName: .grantedBy.displayName, joinedAt: .createdAt}' "$rec_file"
  if is_dangling_member < "$rec_file"; then
    echo "[warn] this record's handle/displayName equal the email and it has no avatar -- probably a non-existent account (the server writes such records for non-existent emails too)" >&2
  fi
  rm -f "$members_file" "$rec_file"
}

cmd_add() {
  local team_id="$1"; shift
  local emails=("$@")
  local role="${ROLE:-member}"

  # [1/6] argument validation
  validate_team_id "$team_id"
  local e
  for e in "${emails[@]}"; do
    validate_email "$e"
  done
  validate_role "$role"

  # input de-duplication (order-preserving)
  local -a uniq_emails=()
  local seen=" "
  for e in "${emails[@]}"; do
    if [[ "$seen" != *" ${e} "* ]]; then
      uniq_emails+=("$e")
      seen="${seen}${e} "
    fi
  done

  # [2/6] team detail (confirm it exists + show the user exactly what they touch)
  echo "[1/5] fetching team detail..."
  local detail
  detail="$(fetch_team_detail "$team_id")"
  print_team_summary "$detail"

  # [3/6] full de-dup
  echo "[2/5] de-duplicating against the full member list..."
  local members_file
  members_file="$(shq_mktemp shq-members)"
  fetch_all_members "$team_id" > "$members_file"
  local -a to_add=()
  local -a already=()
  for e in "${uniq_emails[@]}"; do
    if [[ -n "$(find_member "$members_file" "$e")" ]]; then
      already+=("${e} (current role: $(jq -r --arg e2 "$e" '[.[] | select((.user.email // "") == $e2)][0].role // "unset"' "$members_file"))")
    else
      to_add+=("$e")
    fi
  done
  rm -f "$members_file"

  if [[ "${#already[@]}" -gt 0 ]]; then
    echo "already in team, skipping ${#already[@]}:"
    for e in "${already[@]}"; do echo "   - ${e}"; done
  fi
  if [[ "${#to_add[@]}" == "0" ]]; then
    echo "ok: all emails are already in team ${team_id}; nothing to add (idempotent exit)."
    exit 0
  fi

  # [4/5] show roster + confirm
  echo ""
  echo "adding ${#to_add[@]} member(s) to the team (role: ${role}):"
  for e in "${to_add[@]}"; do echo "   - ${e}"; done
  echo ""
  confirm_or_die "confirm adding the ${#to_add[@]} member(s) above to team ${team_id}?"

  # [5/5] POST + verify
  echo ""
  echo "[3/5] submitting add request..."
  local body
  body="$(jq -n --arg r "$role" --args '{members: [$ARGS.positional[] | {userEmail: ., role: $r}]}' -- "${to_add[@]}")"
  team_post "${TEAM_PREFIX}/${team_id}/members/add" "$body" >/dev/null
  echo "      ok: endpoint returned success (note: it also returns success for non-existent emails; the verification below is the source of truth)"

  echo "[4/5] verifying (re-pulling the member list)..."
  local verify_file
  verify_file="$(shq_mktemp shq-members)"
  fetch_all_members "$team_id" > "$verify_file"
  local -a ok_list=() fail_list=() dangling_list=()
  for e in "${to_add[@]}"; do
    local rec_file
    rec_file="$(shq_mktemp shq-rec)"
    find_member "$verify_file" "$e" > "$rec_file"
    if [[ -s "$rec_file" ]]; then
      ok_list+=("$e")
      if is_dangling_member < "$rec_file"; then
        dangling_list+=("$e")
      fi
    else
      fail_list+=("$e")
    fi
    rm -f "$rec_file"
  done
  rm -f "$verify_file"

  echo "[5/5] result:"
  if [[ "${#ok_list[@]}" -gt 0 ]]; then
    echo "   added (${#ok_list[@]}):"
    for e in "${ok_list[@]}"; do echo "      - ${e}"; done
  fi
  if [[ "${#dangling_list[@]}" -gt 0 ]]; then
    echo "   [warn] probably non-existent accounts (${#dangling_list[@]}; the server wrote records anyway):"
    for e in "${dangling_list[@]}"; do echo "      - ${e}"; done
    echo "      to clean up a mistake: bash $0 remove ${team_id} ${dangling_list[*]}"
  fi
  if [[ "${#fail_list[@]}" -gt 0 ]]; then
    echo "   [error] verification failed (endpoint said success but the member list disagrees, ${#fail_list[@]}):"
    for e in "${fail_list[@]}"; do echo "      - ${e}"; done
    exit 1
  fi
  echo ""
  echo "done: ${#ok_list[@]} member(s) added to team ${team_id} (role ${role})."
}

cmd_remove() {
  local team_id="$1"; shift
  local emails=("$@")
  local e

  validate_team_id "$team_id"
  for e in "${emails[@]}"; do
    validate_email "$e"
  done

  echo "[1/4] fetching team detail..."
  local detail
  detail="$(fetch_team_detail "$team_id")"
  print_team_summary "$detail"

  echo "[2/4] cross-checking (confirm these emails are really in the team)..."
  local members_file
  members_file="$(shq_mktemp shq-members)"
  fetch_all_members "$team_id" > "$members_file"
  local -a in_team=() not_in=()
  for e in "${emails[@]}"; do
    local rec_file
    rec_file="$(shq_mktemp shq-rec)"
    find_member "$members_file" "$e" > "$rec_file"
    if [[ -s "$rec_file" ]]; then
      in_team+=("$e ($(jq -r '.user.displayName // "?"' "$rec_file"), role $(jq -r '.role' "$rec_file"))")
    else
      not_in+=("$e")
    fi
    rm -f "$rec_file"
  done
  rm -f "$members_file"
  if [[ "${#not_in[@]}" -gt 0 ]]; then
    echo "not in team, skipping ${#not_in[@]}:"
    for e in "${not_in[@]}"; do echo "   - ${e}"; done
  fi
  if [[ "${#in_team[@]}" == "0" ]]; then
    echo "ok: none of the emails are in team ${team_id}; nothing to remove (idempotent exit)."
    exit 0
  fi

  echo ""
  echo "removing ${#in_team[@]} member(s) from the team:"
  for e in "${in_team[@]}"; do echo "   - ${e}"; done
  echo ""
  confirm_or_die "confirm removing the ${#in_team[@]} member(s) above from team ${team_id}?"

  echo ""
  echo "[3/4] submitting remove request..."
  local body
  # Submit only the emails that are actually in the team (semantic precision;
  # the remove endpoint silently 200s unknown emails, but do not rely on it).
  local -a in_team_emails=()
  for e in "${emails[@]}"; do
    local hit=""
    for it in "${in_team[@]}"; do
      if [[ "$it" == "$e"* ]]; then hit="$e"; break; fi
    done
    [[ -n "$hit" ]] && in_team_emails+=("$e")
  done
  body="$(jq -n --args '{userEmails: $ARGS.positional}' -- "${in_team_emails[@]}")"
  team_delete "${TEAM_PREFIX}/${team_id}/members/remove" "$body" >/dev/null
  echo "      ok: endpoint returned success (it also returns success for emails not in the team; the verification below is the source of truth)"

  echo "[4/4] verifying (re-pulling the member list)..."
  local verify_file
  verify_file="$(shq_mktemp shq-members)"
  fetch_all_members "$team_id" > "$verify_file"
  local -a still=()
  for e in "${emails[@]}"; do
    if [[ -n "$(find_member "$verify_file" "$e")" ]]; then
      still+=("$e")
    fi
  done
  rm -f "$verify_file"
  if [[ "${#still[@]}" -gt 0 ]]; then
    echo "   [error] verification failed: still in the list (${#still[@]}):"
    for e in "${still[@]}"; do echo "      - ${e}"; done
    exit 1
  fi
  echo "done: ${#in_team[@]} member(s) no longer in team ${team_id}."
}

# ---------- argument parsing ----------
CMD=""
ROLE=""
ROLE_FILTER=""
SHOW_ALL=0
AS_JSON=0
YES=0
declare -a POSITIONAL=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    search|my|info|list|member|add|remove)
      if [[ -z "$CMD" ]]; then CMD="$1"; else echo "[error] duplicate subcommand: $1" >&2; exit 1; fi
      shift;;
    --role)
      if [[ -z "${2:-}" || "${2:-}" == -* ]]; then
        echo "[error] --role requires a value (valid: ${VALID_ROLES})" >&2
        exit 1
      fi
      if [[ "$CMD" == "list" ]]; then ROLE_FILTER="$2"; else ROLE="$2"; fi
      shift 2;;
    --all)      SHOW_ALL=1; shift;;
    --json)     AS_JSON=1; shift;;
    --yes)      YES=1; shift;;
    -h|--help)  usage 0;;
    --*)        echo "[error] unknown option: $1 (see --help)" >&2; exit 1;;
    *)          POSITIONAL+=("$1"); shift;;
  esac
done

if [[ -z "$CMD" ]]; then
  echo "[error] missing subcommand" >&2
  usage 1
fi

case "$CMD" in
  search)
    [[ "${#POSITIONAL[@]}" -lt 1 ]] && { echo "[error] usage: team.sh search <keyword>" >&2; exit 1; }
    cmd_search "${POSITIONAL[0]}";;
  my)
    cmd_my;;
  info)
    [[ "${#POSITIONAL[@]}" -lt 1 ]] && { echo "[error] usage: team.sh info <teamId>" >&2; exit 1; }
    cmd_info "${POSITIONAL[0]}";;
  list)
    [[ "${#POSITIONAL[@]}" -lt 1 ]] && { echo "[error] usage: team.sh list <teamId> [--role R] [--all] [--json]" >&2; exit 1; }
    cmd_list "${POSITIONAL[0]}";;
  member)
    [[ "${#POSITIONAL[@]}" -lt 2 ]] && { echo "[error] usage: team.sh member <teamId> <email>" >&2; exit 1; }
    cmd_member "${POSITIONAL[0]}" "${POSITIONAL[1]}";;
  add)
    [[ "${#POSITIONAL[@]}" -lt 2 ]] && { echo "[error] usage: team.sh add <teamId> <email> [email...] [--role member|admin|viewer]" >&2; exit 1; }
    cmd_add "${POSITIONAL[0]}" "${POSITIONAL[@]:1}";;
  remove)
    [[ "${#POSITIONAL[@]}" -lt 2 ]] && { echo "[error] usage: team.sh remove <teamId> <email> [email...]" >&2; exit 1; }
    cmd_remove "${POSITIONAL[0]}" "${POSITIONAL[@]:1}";;
esac
