#!/usr/bin/env bash
#
# orient.sh - structured project state dump for AI agents and humans.
#
# Run from anywhere inside a Forge project. Walks up to find forge.toml,
# then prints sections that replace the standard "read five files at session
# start" routine.
#
# Sections (each starts with "## NAME"):
#   PROJECT, ENVIRONMENT, SQLX CACHE, MAIN.RS, FUNCTIONS/MOD.RS, SCHEMA/MOD.RS,
#   HANDLERS, MIGRATIONS, REACTIVITY-ENABLED TABLES, NEXT
#
# Designed to be cheap to run. macOS + Linux compatible. No GNU-only flags.

set -u

# Pick the best available grep-with-globs implementation.
if command -v rg >/dev/null 2>&1; then
  HAS_RG=1
else
  HAS_RG=0
fi

# --- find project root (walk up) -------------------------------------------
find_root() {
  local dir
  dir="$(pwd -P)"
  while :; do
    if [ -f "$dir/forge.toml" ]; then
      printf '%s\n' "$dir"
      return 0
    fi
    if [ "$dir" = "/" ]; then
      return 1
    fi
    dir="$(dirname "$dir")"
  done
}

ROOT="$(find_root)" || {
  echo "orient.sh: not in a Forge project (no forge.toml found walking up from $(pwd))" >&2
  exit 1
}
cd "$ROOT" || exit 1

section() { printf '\n## %s\n' "$1"; }
unavailable() { printf '(unavailable: %s)\n' "$1"; }

# --- helpers ---------------------------------------------------------------
toml_string() {
  # toml_string <file> <section> <key>
  # Bash regex extraction. Handles "key = \"value\"" within [section] blocks.
  awk -v section="$2" -v key="$3" '
    /^\[/ {
      cur=$0; sub(/^\[/, "", cur); sub(/\].*$/, "", cur)
      next
    }
    cur == section {
      line=$0
      sub(/^[ \t]*/, "", line)
      idx=index(line, "=")
      if (idx == 0) next
      k=substr(line, 1, idx-1); sub(/[ \t]+$/, "", k)
      if (k != key) next
      v=substr(line, idx+1); sub(/^[ \t]+/, "", v); sub(/[ \t]+$/, "", v)
      gsub(/^"/, "", v); gsub(/"$/, "", v)
      print v
      exit
    }
  ' "$1"
}

# --- PROJECT ---------------------------------------------------------------
section "PROJECT"
printf 'root: %s\n' "$ROOT"
project_name=$(toml_string forge.toml project name 2>/dev/null)
printf 'name: %s\n' "${project_name:-(not set)}"

auth_mode=""
if [ -f forge.toml ]; then
  if grep -q "^\[auth\]" forge.toml 2>/dev/null; then
    if grep -qE "rsa_(public|private)_key" forge.toml 2>/dev/null; then
      auth_mode="rs256"
    elif grep -qE "jwt_secret" forge.toml 2>/dev/null; then
      auth_mode="hs256"
    elif grep -qE "oauth|provider" forge.toml 2>/dev/null; then
      auth_mode="oauth"
    else
      auth_mode="custom"
    fi
  else
    auth_mode="none"
  fi
fi
printf 'auth_mode: %s\n' "${auth_mode:-unknown}"

frontend="none"
if [ -f frontend/package.json ]; then frontend="svelte"; fi
if [ -f frontend/Cargo.toml ] || [ -f frontend/Dioxus.toml ]; then frontend="dioxus"; fi
printf 'frontend: %s\n' "$frontend"

# --- ENVIRONMENT -----------------------------------------------------------
section "ENVIRONMENT"
if [ "${SQLX_OFFLINE:-}" = "true" ] || [ "${SQLX_OFFLINE:-}" = "1" ]; then
  printf 'SQLX_OFFLINE: set\n'
else
  printf 'SQLX_OFFLINE: not set (raw cargo check will misbehave; eval "$(forge env)")\n'
fi

if [ -n "${DATABASE_URL:-}" ]; then
  host=$(printf '%s\n' "$DATABASE_URL" | sed -E 's|.*@([^:/]+).*|\1|')
  printf 'DATABASE_URL: set (host=%s)\n' "${host:-?}"
else
  printf 'DATABASE_URL: not set\n'
fi

if command -v cargo-sqlx >/dev/null 2>&1; then
  printf 'cargo-sqlx: installed\n'
else
  printf 'cargo-sqlx: missing (cargo install sqlx-cli --no-default-features --features postgres)\n'
fi

if [ -f docker-compose.yml ] || [ -f compose.yml ] || [ -f compose.yaml ]; then
  if command -v docker >/dev/null 2>&1 && docker info >/dev/null 2>&1; then
    printf 'docker: running\n'
  else
    printf 'docker: not running\n'
  fi
else
  printf 'docker: not used\n'
fi

# --- SQLX CACHE ------------------------------------------------------------
section "SQLX CACHE"
if [ -d .sqlx ]; then
  count=$(find .sqlx -name 'query-*' -type f 2>/dev/null | wc -l | tr -d ' ')
  printf '.sqlx/: present (%s entries)\n' "$count"
  if [ -d src ]; then
    newer=$(find src -name '*.rs' -newer .sqlx 2>/dev/null | wc -l | tr -d ' ')
    if [ "$newer" -gt 0 ]; then
      printf 'stale: yes (%s source files newer than cache; run forge check or forge migrate prepare)\n' "$newer"
    else
      printf 'stale: no\n'
    fi
  fi
else
  printf '.sqlx/: missing (run forge migrate prepare)\n'
fi

# --- MAIN.RS ---------------------------------------------------------------
section "MAIN.RS"
if [ -f src/main.rs ]; then
  cat src/main.rs
else
  unavailable "src/main.rs not found"
fi

# --- FUNCTIONS/MOD.RS ------------------------------------------------------
section "FUNCTIONS/MOD.RS"
if [ -f src/functions/mod.rs ]; then
  cat src/functions/mod.rs
elif [ -d src/functions ]; then
  unavailable "src/functions/ exists but mod.rs is missing"
else
  unavailable "no src/functions/ yet"
fi

# --- SCHEMA/MOD.RS ---------------------------------------------------------
section "SCHEMA/MOD.RS"
if [ -f src/schema/mod.rs ]; then
  cat src/schema/mod.rs
elif [ -d src/schema ]; then
  unavailable "src/schema/ exists but mod.rs is missing"
else
  unavailable "no src/schema/ yet"
fi

# --- HANDLERS --------------------------------------------------------------
section "HANDLERS"
extract_fn_name() {
  # Args: file, attribute_line. Looks ahead for the first `pub async fn NAME`.
  # Window of 20 lines covers multi-line attribute blocks like
  # #[forge::workflow(... over several lines ...)] pub async fn ...
  # Portable across BSD/GNU awk (no third-arg match()).
  awk -v target="$2" '
    NR > target && NR <= target + 20 {
      line=$0
      if (line ~ /pub[ \t]+async[ \t]+fn[ \t]+/) {
        sub(/.*pub[ \t]+async[ \t]+fn[ \t]+/, "", line)
        sub(/[ \t(<].*/, "", line)
        if (length(line) > 0) { print line; exit }
      }
    }
  ' "$1" 2>/dev/null
}

list_handlers() {
  # Args: kind, attribute regex.
  local kind="$1" attr="$2" any=0
  if [ "$HAS_RG" -eq 1 ]; then
    while IFS=: read -r file line _; do
      [ -z "$file" ] && continue
      fn_name=$(extract_fn_name "$file" "$line")
      [ -z "$fn_name" ] && fn_name="(unnamed)"
      printf '  - %s (%s:%s)\n' "$fn_name" "$file" "$line"
      any=1
    done < <(rg --line-number --no-heading --regexp="$attr" src 2>/dev/null)
  else
    while IFS= read -r match; do
      file=$(printf '%s' "$match" | cut -d: -f1)
      line=$(printf '%s' "$match" | cut -d: -f2)
      [ -z "$file" ] && continue
      fn_name=$(extract_fn_name "$file" "$line")
      [ -z "$fn_name" ] && fn_name="(unnamed)"
      printf '  - %s (%s:%s)\n' "$fn_name" "$file" "$line"
      any=1
    done < <(grep -rn -E "$attr" src 2>/dev/null || true)
  fi
  if [ "$any" -eq 0 ]; then
    printf '  (none)\n'
  fi
}

for kind in query mutation job cron workflow daemon webhook mcp_tool; do
  printf '%ss:\n' "$kind"
  list_handlers "$kind" "#\[forge::${kind}([(\"]|\$|[ \t])"
done

# --- MIGRATIONS ------------------------------------------------------------
section "MIGRATIONS"
if [ -d migrations ]; then
  files=$(find migrations -maxdepth 1 -name '*.sql' 2>/dev/null | sort)
  if [ -z "$files" ]; then
    printf '(empty)\n'
  else
    count=$(printf '%s\n' "$files" | wc -l | tr -d ' ')
    printf 'file count: %s\n' "$count"
    printf 'files:\n'
    printf '%s\n' "$files" | sed 's/^/  - /'
    latest=$(printf '%s\n' "$files" | tail -n 1)
    printf '\nlatest (%s):\n' "$latest"
    cat "$latest"
  fi
else
  unavailable "no migrations/ directory"
fi

# --- REACTIVITY-ENABLED TABLES --------------------------------------------
section "REACTIVITY-ENABLED TABLES"
if [ -d migrations ]; then
  if [ "$HAS_RG" -eq 1 ]; then
    rg --no-heading --no-filename -o "forge_enable_reactivity\('([^']+)'" -r '$1' migrations 2>/dev/null | sort -u | sed 's/^/  - /' || printf '  (none)\n'
  else
    grep -rho "forge_enable_reactivity('[^']*'" migrations 2>/dev/null \
      | sed -E "s/.*'([^']+)'.*/\1/" | sort -u | sed 's/^/  - /' || printf '  (none)\n'
  fi
else
  unavailable "no migrations/ directory"
fi

# --- NEXT ------------------------------------------------------------------
section "NEXT"
hints=0
if [ "${SQLX_OFFLINE:-}" != "true" ] && [ "${SQLX_OFFLINE:-}" != "1" ]; then
  printf '  - eval "$(forge env)" — sets SQLX_OFFLINE=true and shell completions\n'
  hints=1
fi
if ! command -v cargo-sqlx >/dev/null 2>&1; then
  printf '  - run `forge doctor` (cargo-sqlx missing)\n'
  hints=1
fi
if [ ! -d .sqlx ] || [ ! -f .sqlx/.gitkeep -a -z "$(ls .sqlx 2>/dev/null)" ]; then
  if [ -d src ] && grep -rqE "sqlx::query!?_?(as|scalar)?!" src 2>/dev/null; then
    printf '  - run `forge migrate prepare` (.sqlx looks empty/missing)\n'
    hints=1
  fi
fi
if [ "$hints" -eq 0 ]; then
  printf '  - You are oriented. Proceed.\n'
fi
