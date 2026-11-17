# Ready-to-run requests

Shapes come from the SchoolPass Swagger spec and `docs/SCHOOLPASS-API.md`. Run
the live check (`node --env-file=.env scripts/live-check.mjs`) once to confirm
the auth-response fields on your account before trusting the `jq` recipes below.

## Helper — source this first

```bash
: "${SCHOOLPASS_SCHOOL_CODE:?export SCHOOLPASS_SCHOOL_CODE first}"
: "${SCHOOLPASS_EMAIL:?}"; : "${SCHOOLPASS_PASSWORD:?}"
SP_HOST="${SCHOOLPASS_API_HOST:-busapi-east16-ss.school-pass.net}"
SP_BASE="https://${SP_HOST}/api"
# Token cache for this skill (NOT the MCP server's store — the server keeps none
# on disk, but keep this skill's state self-contained regardless).
SP_SESSION="${SCHOOLPASS_CURL_SESSION:-$HOME/.schoolpass-mcp/curl-token.json}"

# sp_curl <method> <path> [body-json] [-- extra-curl-args...]
# Adds the AppCode header, Authorization (if $SP_TOKEN set), and JSON accept.
sp_curl() {
  local method="$1" path="$2" body="${3:-}"
  shift 2; [ $# -gt 0 ] && shift
  [ "${1:-}" = "--" ] && shift
  curl -sS -X "$method" "${SP_BASE}/${path}" \
    -H "AppCode: ${SCHOOLPASS_SCHOOL_CODE}" \
    -H "accept: application/json" \
    -H "content-type: application/json" \
    ${SP_TOKEN:+-H "Authorization: Bearer ${SP_TOKEN}"} \
    ${body:+--data "$body"} "$@"
}

# sp_login: Auth/users -> pick Parent identity -> Auth/token -> export SP_TOKEN.
# Verify the response field names against your account once (live-check) — the
# access-token field is `access_token`; adjust the jq path if yours differs.
sp_login() {
  local users uid utype token
  users=$(sp_curl POST Auth/users "$(jq -nc \
    --argjson sc "$SCHOOLPASS_SCHOOL_CODE" --arg em "$SCHOOLPASS_EMAIL" --arg pw "$SCHOOLPASS_PASSWORD" \
    '{schoolCode:$sc,email:$em,password:$pw,ssoToken:null,authType:"Credentials"}')") || return 1
  # Pick the Parent identity (userType 3), else the sole identity. Field names
  # vary (userId|id, userType|type) — normalize.
  uid=$(echo "$users" | jq -r '(if type=="array" then . else (.users // .data // [.]) end)
      | map({id:(.userId // .id), t:(.userType // .type)})
      | (map(select(.t==3))[0] // .[0]) | .id')
  utype=$(echo "$users" | jq -r '(if type=="array" then . else (.users // .data // [.]) end)
      | map({id:(.userId // .id), t:(.userType // .type)})
      | (map(select(.t==3))[0] // .[0]) | .t')
  token=$(sp_curl POST Auth/token "$(jq -nc \
    --argjson sc "$SCHOOLPASS_SCHOOL_CODE" --argjson uid "$uid" --argjson ut "$utype" --arg pw "$SCHOOLPASS_PASSWORD" \
    '{schoolCode:$sc,userId:$uid,userType:$ut,password:$pw,ssoToken:null,authType:"Credentials"}')" \
    | jq -r '.access_token // .payload.access_token // .accessToken')
  [ -n "$token" ] && [ "$token" != "null" ] || { echo "login failed" >&2; return 1; }
  export SP_TOKEN="$token" SP_MEMBER_ID="$uid"
  mkdir -p "$(dirname "$SP_SESSION")" && chmod 700 "$(dirname "$SP_SESSION")"
  printf '{"memberId":%s}\n' "$uid" > "$SP_SESSION"   # never write the token to disk
}
```

## Reachability (no auth)

```bash
sp_curl GET "version?schoolCode=${SCHOOLPASS_SCHOOL_CODE}"
# -> "Host:…,Version:5.0.4.7602,…,School:SprAPiServer 1183 Scholars Academy"
```

## Reads (after `sp_login`)

```bash
# Students — id, name, grade, home dismissal location.
sp_curl GET "parent/getstudents?memberId=${SP_MEMBER_ID}" \
  | jq '.[] | {id, name:"\(.firstName) \(.lastName)", gradeId, dismissalLocationId, aftercare}'

# Parent profile.
sp_curl GET "parent/profile?memberId=${SP_MEMBER_ID}"

# Authorized drivers, with carpools.
sp_curl GET "parent/parentdrivers?memberId=${SP_MEMBER_ID}&includeCarpool=true"

# Dismissal locations — the vocabulary a change refers to.
sp_curl GET "dismissal/getDismissalLocations" \
  | jq '.[] | {id, name, locationTypeId, dismissalSessionTimeId}'

# A student's arrival/dismissal calendar for a date range.
STU=12345; TODAY=$(date +%F); IN2W=$(date -v+14d +%F 2>/dev/null || date -d '+14 days' +%F)
sp_curl GET "Student/StudentCalendar?schoolCode=${SCHOOLPASS_SCHOOL_CODE}&studentId=${STU}&startDate=${TODAY}&endDate=${IN2W}"

# Pickup / dismissal changes for a student today.
sp_curl GET "PickupChange/GetChanges?studentId=${STU}&date=${TODAY}"

# School info + config.
sp_curl GET "SchoolInfo/GetBasicSchoolInfo?schoolCode=${SCHOOLPASS_SCHOOL_CODE}"
sp_curl GET "Config/configsettings?schoolCode=${SCHOOLPASS_SCHOOL_CODE}"
```

## Notes

- A `403` on any read means your parent token cannot reach that route (it is
  admin-only). Expected — not a login problem.
- The `jq` field paths above follow the Swagger shapes; if the live check shows a
  different envelope on your account, adjust the paths and update this file.

## Writes (verified live)

Submit a dismissal/arrival change — `POST studentchange`. The body must match the
app exactly: `dateSet.dates` EMPTY, `daysOfWeek` as NUMERIC ids (Monday=1…Sunday=7),
`modifiedBy` = your parent member id (= `parentMemberId`), `changeType` from the E2
enum (Absent=1, LateArrival=2, EarlyDismissal=3, Carpool=4, Activity=5, Bus=6).

```bash
STU=11278; DATE=2026-09-14; DOW=1   # DOW: Mon=1..Sun=7 for $DATE
sp_curl POST "studentchange?schoolCode=${SCHOOLPASS_SCHOOL_CODE}&parentMemberId=${SP_MEMBER_ID}" "$(jq -nc \
  --argjson sid "$STU" --arg date "$DATE" --argjson dow "$DOW" --argjson mid "$SP_MEMBER_ID" '{
    studentId:$sid, moveToId:null, busStopId:null,
    dateSet:{dates:[], daysOfWeek:[$dow], startDate:$date, endDate:$date, recurringWeeks:0},
    notes:"", pickupDropoffPerson:null, willReturn:false, timeOfDay:null,
    changeSeriesId:0, changeType:1, adType:3, userType:3, modifiedBy:$mid }')"
# Verify: re-read the calendar; a non-default entry (isDefault:false, changeSeriesId set) appears.
sp_curl GET "Student/StudentCalendar?schoolCode=${SCHOOLPASS_SCHOOL_CODE}&studentId=${STU}&startDate=${DATE}&endDate=${DATE}" | jq '.dailyList'
```

Cancel a change — `DELETE studentchange/DeleteMobileChange`, keyed on the
`changeSeriesId` from the calendar:

```bash
CSID=27074   # from the calendar entry's changeSeriesId
sp_curl DELETE "studentchange/DeleteMobileChange?schoolCode=${SCHOOLPASS_SCHOOL_CODE}&ChangeSeriesId=${CSID}&ChangeType=1&ADType=4&dt=${DATE}"
```

- `moveToId` for a Carpool move (changeType 4) is a **carpool id**; moving to the
  carpool the student is already in returns 500.
- A 2xx is not proof — re-read the calendar to confirm the change (or its removal).
