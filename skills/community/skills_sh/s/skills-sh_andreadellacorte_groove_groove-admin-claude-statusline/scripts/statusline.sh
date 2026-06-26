#!/bin/bash
# Single line: Model | repo@branch (+N -N) | tokens | %used | effort | 5h bar @reset | 7d bar @reset | loops

set -f  # disable globbing

input=$(cat)

if [ -z "$input" ]; then
    printf "Claude"
    exit 0
fi

# ANSI colors
blue='\033[38;2;0;153;255m'
orange='\033[38;2;255;176;85m'
green='\033[38;2;0;160;0m'
cyan='\033[38;2;46;149;153m'
red='\033[38;2;255;85;85m'
yellow='\033[38;2;230;200;0m'
white='\033[38;2;220;220;220m'
dim='\033[2m'
reset='\033[0m'

format_tokens() {
    local num=$1
    if [ "$num" -ge 1000000 ]; then
        awk "BEGIN {printf \"%.1fm\", $num / 1000000}"
    elif [ "$num" -ge 1000 ]; then
        awk "BEGIN {printf \"%.0fk\", $num / 1000}"
    else
        printf "%d" "$num"
    fi
}

usage_color() {
    local pct=$1
    if [ "$pct" -ge 90 ]; then echo "$red"
    elif [ "$pct" -ge 70 ]; then echo "$orange"
    elif [ "$pct" -ge 50 ]; then echo "$yellow"
    else echo "$green"
    fi
}

# ===== Extract data from JSON =====
model_name=$(echo "$input" | jq -r '.model.display_name // "Claude"')

size=$(echo "$input" | jq -r '.context_window.context_window_size // 200000')
[ "$size" -eq 0 ] 2>/dev/null && size=200000

input_tokens=$(echo "$input" | jq -r '.context_window.current_usage.input_tokens // 0')
cache_create=$(echo "$input" | jq -r '.context_window.current_usage.cache_creation_input_tokens // 0')
cache_read=$(echo "$input" | jq -r '.context_window.current_usage.cache_read_input_tokens // 0')
current=$(( input_tokens + cache_create + cache_read ))

used_tokens=$(format_tokens $current)
total_tokens=$(format_tokens $size)

if [ "$size" -gt 0 ]; then
    pct_used=$(( current * 100 / size ))
else
    pct_used=0
fi

# Check effort level — prefer the live session value from stdin JSON,
# then env override, then static settings.json as a last resort.
settings_path="$HOME/.claude/settings.json"
effort_level="high"
effort_live=$(echo "$input" | jq -r '.effort.level // empty')
if [ -n "$effort_live" ]; then
    effort_level="$effort_live"
elif [ -n "$CLAUDE_CODE_EFFORT_LEVEL" ]; then
    effort_level="$CLAUDE_CODE_EFFORT_LEVEL"
elif [ -f "$settings_path" ]; then
    effort_val=$(jq -r '.effortLevel // empty' "$settings_path" 2>/dev/null)
    [ -n "$effort_val" ] && effort_level="$effort_val"
fi

# ===== Build output =====
out=""
out+="${blue}${model_name}${reset}"

cwd=$(echo "$input" | jq -r '.cwd // empty')
if [ -n "$cwd" ]; then
    display_dir="${cwd##*/}"
    git_branch=$(git -C "${cwd}" rev-parse --abbrev-ref HEAD 2>/dev/null)
    out+=" ${dim}|${reset} "
    out+="${cyan}${display_dir}${reset}"
    if [ -n "$git_branch" ]; then
        out+="${dim}@${reset}${green}${git_branch}${reset}"
        git_stat=$(git -C "${cwd}" diff --numstat 2>/dev/null | awk '{a+=$1; d+=$2} END {if (a+d>0) printf "+%d -%d", a, d}')
        [ -n "$git_stat" ] && out+=" ${dim}(${reset}${green}${git_stat%% *}${reset} ${red}${git_stat##* }${reset}${dim})${reset}"
    fi
fi

sep=" ${dim}|${reset} "

out+="${sep}"
out+="${orange}${used_tokens}/${total_tokens}${reset} ${dim}(${reset}${green}${pct_used}%${reset}${dim})${reset}"
out+="${sep}"
out+="effort: "
case "$effort_level" in
    low)    out+="${dim}low${reset}" ;;
    medium) out+="${orange}med${reset}" ;;
    high)   out+="${green}high${reset}" ;;
    xhigh)  out+="${cyan}xhigh${reset}" ;;
    max)    out+="${cyan}max${reset}" ;;
    *)      out+="${green}${effort_level}${reset}" ;;
esac

# ===== OAuth token =====
get_oauth_token() {
    local token=""
    if [ -n "$CLAUDE_CODE_OAUTH_TOKEN" ]; then echo "$CLAUDE_CODE_OAUTH_TOKEN"; return 0; fi
    if command -v security >/dev/null 2>&1; then
        local blob
        blob=$(security find-generic-password -s "Claude Code-credentials" -w 2>/dev/null)
        if [ -n "$blob" ]; then
            token=$(echo "$blob" | jq -r '.claudeAiOauth.accessToken // empty' 2>/dev/null)
            if [ -n "$token" ] && [ "$token" != "null" ]; then echo "$token"; return 0; fi
        fi
    fi
    local creds_file="${HOME}/.claude/.credentials.json"
    if [ -f "$creds_file" ]; then
        token=$(jq -r '.claudeAiOauth.accessToken // empty' "$creds_file" 2>/dev/null)
        if [ -n "$token" ] && [ "$token" != "null" ]; then echo "$token"; return 0; fi
    fi
    if command -v secret-tool >/dev/null 2>&1; then
        local blob
        blob=$(timeout 2 secret-tool lookup service "Claude Code-credentials" 2>/dev/null)
        if [ -n "$blob" ]; then
            token=$(echo "$blob" | jq -r '.claudeAiOauth.accessToken // empty' 2>/dev/null)
            if [ -n "$token" ] && [ "$token" != "null" ]; then echo "$token"; return 0; fi
        fi
    fi
    echo ""
}

# ===== Usage limits (cached 60s) =====
cache_file="/tmp/claude/statusline-usage-cache.json"
cache_max_age=60
mkdir -p /tmp/claude

needs_refresh=true
usage_data=""

if [ -f "$cache_file" ]; then
    cache_mtime=$(stat -c %Y "$cache_file" 2>/dev/null || stat -f %m "$cache_file" 2>/dev/null)
    now=$(date +%s)
    cache_age=$(( now - cache_mtime ))
    if [ "$cache_age" -lt "$cache_max_age" ]; then
        needs_refresh=false
        usage_data=$(cat "$cache_file" 2>/dev/null)
    fi
fi

if $needs_refresh; then
    token=$(get_oauth_token)
    if [ -n "$token" ] && [ "$token" != "null" ]; then
        response=$(curl -s --max-time 10 \
            -H "Accept: application/json" \
            -H "Content-Type: application/json" \
            -H "Authorization: Bearer $token" \
            -H "anthropic-beta: oauth-2025-04-20" \
            -H "User-Agent: claude-code/2.1.34" \
            "https://api.anthropic.com/api/oauth/usage" 2>/dev/null)
        if [ -n "$response" ] && echo "$response" | jq . >/dev/null 2>&1; then
            usage_data="$response"
            echo "$response" > "$cache_file"
        fi
    fi
    if [ -z "$usage_data" ] && [ -f "$cache_file" ]; then
        usage_data=$(cat "$cache_file" 2>/dev/null)
    fi
fi

iso_to_epoch() {
    local iso_str="$1"
    local epoch
    epoch=$(date -d "${iso_str}" +%s 2>/dev/null)
    if [ -n "$epoch" ]; then echo "$epoch"; return 0; fi
    local stripped="${iso_str%%.*}"
    stripped="${stripped%%Z}"
    stripped="${stripped%%+*}"
    stripped="${stripped%%-[0-9][0-9]:[0-9][0-9]}"
    if [[ "$iso_str" == *"Z"* ]] || [[ "$iso_str" == *"+00:00"* ]] || [[ "$iso_str" == *"-00:00"* ]]; then
        epoch=$(env TZ=UTC date -j -f "%Y-%m-%dT%H:%M:%S" "$stripped" +%s 2>/dev/null)
    else
        epoch=$(date -j -f "%Y-%m-%dT%H:%M:%S" "$stripped" +%s 2>/dev/null)
    fi
    if [ -n "$epoch" ]; then echo "$epoch"; return 0; fi
    return 1
}

format_reset_time() {
    local iso_str="$1"
    local style="$2"
    [ -z "$iso_str" ] || [ "$iso_str" = "null" ] && return
    local epoch
    epoch=$(iso_to_epoch "$iso_str")
    [ -z "$epoch" ] && return
    case "$style" in
        time)
            date -j -r "$epoch" +"%l:%M%p" 2>/dev/null | sed 's/^ //' | tr '[:upper:]' '[:lower:]' || \
            date -d "@$epoch" +"%l:%M%P" 2>/dev/null | sed 's/^ //'
            ;;
        datetime)
            date -j -r "$epoch" +"%b %-d, %l:%M%p" 2>/dev/null | sed 's/  / /g; s/^ //' | tr '[:upper:]' '[:lower:]' || \
            date -d "@$epoch" +"%b %-d, %l:%M%P" 2>/dev/null | sed 's/  / /g; s/^ //'
            ;;
        *)
            date -j -r "$epoch" +"%b %-d" 2>/dev/null | tr '[:upper:]' '[:lower:]' || \
            date -d "@$epoch" +"%b %-d" 2>/dev/null
            ;;
    esac
}

if [ -n "$usage_data" ] && echo "$usage_data" | jq -e . >/dev/null 2>&1; then
    five_hour_pct=$(echo "$usage_data" | jq -r '.five_hour.utilization // 0' | awk '{printf "%.0f", $1}')
    five_hour_reset_iso=$(echo "$usage_data" | jq -r '.five_hour.resets_at // empty')
    five_hour_reset=$(format_reset_time "$five_hour_reset_iso" "time")
    five_hour_color=$(usage_color "$five_hour_pct")

    out+="${sep}${white}5h${reset} ${five_hour_color}${five_hour_pct}%${reset}"
    [ -n "$five_hour_reset" ] && out+=" ${dim}@${five_hour_reset}${reset}"

    seven_day_pct=$(echo "$usage_data" | jq -r '.seven_day.utilization // 0' | awk '{printf "%.0f", $1}')
    seven_day_reset_iso=$(echo "$usage_data" | jq -r '.seven_day.resets_at // empty')
    seven_day_reset=$(format_reset_time "$seven_day_reset_iso" "datetime")
    seven_day_color=$(usage_color "$seven_day_pct")

    out+="${sep}${white}7d${reset} ${seven_day_color}${seven_day_pct}%${reset}"
    [ -n "$seven_day_reset" ] && out+=" ${dim}@${seven_day_reset}${reset}"

    extra_enabled=$(echo "$usage_data" | jq -r '.extra_usage.is_enabled // false')
    if [ "$extra_enabled" = "true" ]; then
        extra_pct=$(echo "$usage_data" | jq -r '.extra_usage.utilization // 0' | awk '{printf "%.0f", $1}')
        extra_used=$(echo "$usage_data" | jq -r '.extra_usage.used_credits // 0' | LC_NUMERIC=C awk '{printf "%.2f", $1/100}')
        extra_limit=$(echo "$usage_data" | jq -r '.extra_usage.monthly_limit // 0' | LC_NUMERIC=C awk '{printf "%.2f", $1/100}')
        if [ -n "$extra_used" ] && [ -n "$extra_limit" ] && [[ "$extra_used" != *'* ]] && [[ "$extra_limit" != *'* ]]; then
            extra_color=$(usage_color "$extra_pct")
            out+="${sep}${white}extra${reset} ${extra_color}${extra_used}/${extra_limit}${reset}"
        else
            out+="${sep}${white}extra${reset} ${green}enabled${reset}"
        fi
    fi
fi

# ===== Loop info =====
loops_file="/tmp/claude/loops.json"
if [ -f "$loops_file" ]; then
    file_mtime=$(stat -f %m "$loops_file" 2>/dev/null || stat -c %Y "$loops_file" 2>/dev/null)
    now_ts=$(date +%s)
    file_age=$(( now_ts - file_mtime ))

    if [ "$file_age" -lt 14400 ]; then
        loop_count=$(jq 'length' "$loops_file" 2>/dev/null || echo 0)

        if [ -n "$loop_count" ] && [ "$loop_count" -gt 0 ]; then
            loop_info=$(LOOP_JOBS=$(cat "$loops_file") python3 -c "
import os, json, sys
from datetime import datetime, timedelta

def matches(field, value):
    if field == '*': return True
    if '/' in field:
        b, s = field.split('/', 1)
        start = 0 if b == '*' else int(b.split('-')[0])
        return (value - start) % int(s) == 0
    if ',' in field: return value in [int(x) for x in field.split(',')]
    if '-' in field:
        a, b2 = field.split('-')
        return int(a) <= value <= int(b2)
    try: return value == int(field)
    except: return False

def next_fire(cron_expr):
    parts = cron_expr.split()
    if len(parts) != 5: return None, ''
    m, h, dom, mon, dow = parts
    t = datetime.now().replace(second=0, microsecond=0) + timedelta(minutes=1)
    for _ in range(10080):
        if matches(m, t.minute) and matches(h, t.hour) and matches(mon, t.month) and matches(dom, t.day):
            return t, t.strftime('%-I:%M%p').lower()
        t += timedelta(minutes=1)
    return None, ''

jobs = json.loads(os.environ.get('LOOP_JOBS', '[]'))
if not jobs: sys.exit(0)

best_dt, best_prompt, best_time = None, '', ''
for job in jobs:
    dt, ts = next_fire(job.get('schedule', ''))
    if dt and (best_dt is None or dt < best_dt):
        best_dt, best_time = dt, ts
        best_prompt = job.get('prompt', '')[:25]

if best_prompt:
    print(f'{best_prompt}|{best_time}')
" 2>/dev/null)

            loop_label="loop"
            [ "$loop_count" -gt 1 ] && loop_label="loops"

            out+="${sep}${cyan}${loop_count} ${loop_label}${reset}"
            if [ -n "$loop_info" ]; then
                next_prompt="${loop_info%%|*}"
                next_time="${loop_info##*|}"
                out+=" ${dim}|${reset} ${white}${next_prompt}${reset}"
                [ -n "$next_time" ] && out+=" ${dim}@${next_time}${reset}"
            fi
        fi
    fi
fi

printf "%b" "$out"
exit 0
