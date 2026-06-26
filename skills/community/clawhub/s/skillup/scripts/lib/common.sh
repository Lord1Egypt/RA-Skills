#!/bin/sh

set -eu

SKILLUP_ROOT=${SKILLUP_ROOT:-$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)}
SKILLUP_DEFAULT_CONFIG="$SKILLUP_ROOT/config.example.toml"
SKILLUP_DEFAULT_ARTIFACT_DIR="$SKILLUP_ROOT/.skillup-artifacts"
SKILLUP_RESULTS=""
SKILLUP_FAIL_FAST=0
SKILLUP_RETRY_COUNT=0
SKILLUP_REDACT_MODE="strict"
SKILLUP_MODE="publish"
SKILLUP_RESULT_FILE=""
SKILLUP_FAILED=0
SKILLUP_CONTINUE_ON_ERROR=1
SKILLUP_BUMP_PART=""
SKILLUP_INSTALL_TARGET=""
SKILLUP_ROLLBACK_VERSION=""
SKILLUP_PARALLEL_PUBLISH=1

usage() {
  cat <<'EOF'
Usage: publish.sh [publish|check|package|bump|status|doctor|redact-check|install-local|rollback] --source <path> [options]

Modes:
  publish                Validate, package, and publish skills (default)
  check                  Validate skills and platform requirements only
  package                Validate and package skills without publishing
  bump                   Update the skill version in SKILL.md and manifest.toml
  status                 Show local and remote publishing status
  doctor                 Check local environment readiness
  redact-check           Scan skill files for sensitive content before upload
  install-local          Install local skill into codex/openclaw skill directories
  rollback               Restore local skill files from a published GitHub release

Options:
  --source <path>        Single skill directory or repository root
  --platforms <csv>      github,xiaping,openclaw,clawhub
  --config <path>        Config file path
  --artifact-dir <path>  Artifact output directory
  --result-file <path>   JSON result file path
  --dry-run              Validate and package without remote publishing
  --fail-fast            Stop after the first failure
  --continue-on-error    Continue processing after failures
  --retry <n>            Retry failed publishes up to n additional times
  --redact-mode <mode>   strict, warn, off
  --parallel-publish     Publish platforms concurrently when possible
  --sequential-publish   Disable concurrent platform publishing
  --only-validate        Alias for check mode
  --only-package         Alias for package mode
  --help                 Show this message
EOF
}

main() {
  SOURCE=""
  PLATFORMS=""
  CONFIG_PATH=""
  ARTIFACT_DIR=""
  DRY_RUN=0

  if [ "$#" -gt 0 ]; then
    case "$1" in
      publish|check|package|status|doctor|redact-check)
        SKILLUP_MODE=$1
        shift
        ;;
      bump)
        SKILLUP_MODE=$1
        shift
        [ "$#" -gt 0 ] || {
          echo "bump requires patch, minor, or major" >&2
          exit 1
        }
        SKILLUP_BUMP_PART=$1
        shift
        ;;
      install-local)
        SKILLUP_MODE=$1
        shift
        [ "$#" -gt 0 ] || {
          echo "install-local requires codex, openclaw, or both" >&2
          exit 1
        }
        SKILLUP_INSTALL_TARGET=$1
        shift
        ;;
      rollback)
        SKILLUP_MODE=$1
        shift
        [ "$#" -gt 0 ] || {
          echo "rollback requires a version like 0.1.7" >&2
          exit 1
        }
        SKILLUP_ROLLBACK_VERSION=$1
        shift
        ;;
    esac
  fi

  while [ "$#" -gt 0 ]; do
    case "$1" in
      --source)
        SOURCE=$2
        shift 2
        ;;
      --platforms)
        PLATFORMS=$2
        shift 2
        ;;
      --config)
        CONFIG_PATH=$2
        shift 2
        ;;
      --artifact-dir)
        ARTIFACT_DIR=$2
        shift 2
        ;;
      --result-file)
        SKILLUP_RESULT_FILE=$2
        shift 2
        ;;
      --dry-run)
        DRY_RUN=1
        shift
        ;;
      --fail-fast)
        SKILLUP_FAIL_FAST=1
        SKILLUP_CONTINUE_ON_ERROR=0
        shift
        ;;
      --continue-on-error)
        SKILLUP_FAIL_FAST=0
        SKILLUP_CONTINUE_ON_ERROR=1
        shift
        ;;
      --retry)
        SKILLUP_RETRY_COUNT=$2
        shift 2
        ;;
      --redact-mode)
        SKILLUP_REDACT_MODE=$2
        shift 2
        ;;
      --parallel-publish)
        SKILLUP_PARALLEL_PUBLISH=1
        shift
        ;;
      --sequential-publish)
        SKILLUP_PARALLEL_PUBLISH=0
        shift
        ;;
      --only-validate)
        SKILLUP_MODE="check"
        shift
        ;;
      --only-package)
        SKILLUP_MODE="package"
        shift
        ;;
      --help)
        usage
        exit 0
        ;;
      *)
        echo "Unknown argument: $1" >&2
        usage >&2
        exit 1
        ;;
    esac
  done

  [ -n "$SOURCE" ] || {
    echo "--source is required" >&2
    usage >&2
    exit 1
  }

  [ -d "$SOURCE" ] || {
    echo "Source directory not found: $SOURCE" >&2
    exit 1
  }

  if [ -z "$CONFIG_PATH" ] && [ -f "$SKILLUP_DEFAULT_CONFIG" ]; then
    CONFIG_PATH=$SKILLUP_DEFAULT_CONFIG
  fi

  if [ -z "$PLATFORMS" ]; then
    PLATFORMS=$(config_get "$CONFIG_PATH" defaults platforms "github,xiaping,openclaw,clawhub")
  fi

  if [ -z "$ARTIFACT_DIR" ]; then
    ARTIFACT_DIR=$(config_get "$CONFIG_PATH" defaults artifact_dir "$SKILLUP_DEFAULT_ARTIFACT_DIR")
  fi
  ARTIFACT_DIR=$(resolve_path "$ARTIFACT_DIR" "$SKILLUP_ROOT")
  mkdir -p "$ARTIFACT_DIR"

  if [ -z "$SKILLUP_RESULT_FILE" ]; then
    SKILLUP_RESULT_FILE=$(config_get "$CONFIG_PATH" defaults result_file "$ARTIFACT_DIR/publish-result.json")
  fi
  SKILLUP_RESULT_FILE=$(resolve_path "$SKILLUP_RESULT_FILE" "$SKILLUP_ROOT")

  SKILLS=$(discover_skills "$SOURCE")
  if [ -z "$SKILLS" ]; then
    echo "No skills found under $SOURCE" >&2
    exit 1
  fi

  OLD_IFS=$IFS
  IFS='
'
  for skill_dir in $SKILLS; do
    IFS=$OLD_IFS
    if ! process_skill "$skill_dir" "$PLATFORMS" "$CONFIG_PATH" "$ARTIFACT_DIR" "$DRY_RUN"; then
      SKILLUP_FAILED=1
      if [ "$SKILLUP_FAIL_FAST" -eq 1 ]; then
        break
      fi
    fi
    IFS='
'
  done
  IFS=$OLD_IFS

  print_summary
  write_results_json "$SKILLUP_RESULT_FILE"

  if [ "$SKILLUP_FAILED" -ne 0 ]; then
    exit 1
  fi
}

config_get() {
  config_path=$1
  section=$2
  key=$3
  default_value=$4

  if [ -z "$config_path" ] || [ ! -f "$config_path" ]; then
    printf '%s\n' "$default_value"
    return
  fi

  value=$(awk -v target_section="[$section]" -v target_key="$key" '
    BEGIN { in_section = 0 }
    /^\[[^]]+\]$/ { in_section = ($0 == target_section); next }
    in_section && $0 ~ "^[[:space:]]*" target_key "[[:space:]]*=" {
      sub(/^[^=]*=[[:space:]]*/, "", $0)
      gsub(/^[[:space:]]*"/, "", $0)
      gsub(/"[[:space:]]*$/, "", $0)
      gsub(/\\"/, "\"", $0)
      print
      exit
    }
  ' "$config_path")

  if [ -n "$value" ]; then
    printf '%s\n' "$value"
  else
    printf '%s\n' "$default_value"
  fi
}

resolve_path() {
  input_path=$1
  base_dir=$2

  case "$input_path" in
    /*)
      printf '%s\n' "$input_path"
      ;;
    *)
      printf '%s\n' "$base_dir/$input_path"
      ;;
  esac
}

command_exists() {
  command -v "$1" >/dev/null 2>&1
}

manifest_get() {
  skill_dir=$1
  key=$2
  manifest_path="$skill_dir/manifest.toml"

  if [ ! -f "$manifest_path" ]; then
    return 1
  fi

  awk -v target_key="$key" '
    $0 ~ "^[[:space:]]*" target_key "[[:space:]]*=" {
      sub(/^[^=]*=[[:space:]]*/, "", $0)
      gsub(/^[[:space:]]*"/, "", $0)
      gsub(/"[[:space:]]*$/, "", $0)
      gsub(/\\"/, "\"", $0)
      print
      exit
    }
  ' "$manifest_path"
}

manifest_section_get() {
  skill_dir=$1
  section=$2
  key=$3
  manifest_path="$skill_dir/manifest.toml"

  if [ ! -f "$manifest_path" ]; then
    return 1
  fi

  awk -v target_section="[$section]" -v target_key="$key" '
    BEGIN { in_section = 0 }
    /^\[[^]]+\]$/ { in_section = ($0 == target_section); next }
    in_section && $0 ~ "^[[:space:]]*" target_key "[[:space:]]*=" {
      sub(/^[^=]*=[[:space:]]*/, "", $0)
      gsub(/^[[:space:]]*"/, "", $0)
      gsub(/"[[:space:]]*$/, "", $0)
      gsub(/\\"/, "\"", $0)
      print
      exit
    }
  ' "$manifest_path"
}

manifest_section_enabled() {
  skill_dir=$1
  section=$2
  raw_value=$(manifest_section_get "$skill_dir" "$section" enabled 2>/dev/null || true)

  if [ -z "$raw_value" ]; then
    printf '%s\n' "true"
    return
  fi

  printf '%s\n' "$raw_value" | tr '[:upper:]' '[:lower:]'
}

frontmatter_get() {
  skill_dir=$1
  key=$2
  skill_md="$skill_dir/SKILL.md"

  awk -v target_key="$key" '
    NR == 1 && $0 != "---" { exit }
    NR == 1 && $0 == "---" { in_frontmatter = 1; next }
    in_frontmatter && $0 == "---" { exit }
    in_frontmatter && $0 ~ "^[[:space:]]*" target_key ":" {
      sub(/^[^:]*:[[:space:]]*/, "", $0)
      gsub(/^[[:space:]]*"/, "", $0)
      gsub(/"[[:space:]]*$/, "", $0)
      print
      exit
    }
  ' "$skill_md"
}

slugify() {
  printf '%s\n' "$1" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g; s/-\{2,\}/-/g; s/^-//; s/-$//'
}

discover_skills() {
  source_dir=$1

  if [ -f "$source_dir/SKILL.md" ]; then
    printf '%s\n' "$source_dir"
    return
  fi

  find "$source_dir" -mindepth 1 -maxdepth 2 -type f -name 'SKILL.md' | while read -r skill_file; do
    dirname "$skill_file"
  done | sort -u
}

skill_slug() {
  skill_dir=$1
  slug=$(manifest_get "$skill_dir" slug 2>/dev/null || true)
  if [ -z "$slug" ]; then
    slug=$(frontmatter_get "$skill_dir" name 2>/dev/null || true)
  fi
  if [ -z "$slug" ]; then
    slug=$(basename "$skill_dir")
  fi
  slugify "$slug"
}

skill_version() {
  skill_dir=$1
  version=$(manifest_get "$skill_dir" version 2>/dev/null || true)
  if [ -z "$version" ]; then
    version=$(frontmatter_get "$skill_dir" version 2>/dev/null || true)
  fi
  printf '%s\n' "$version"
}

skill_name() {
  skill_dir=$1
  name=$(manifest_get "$skill_dir" name 2>/dev/null || true)
  if [ -z "$name" ]; then
    name=$(frontmatter_get "$skill_dir" name 2>/dev/null || true)
  fi
  if [ -z "$name" ]; then
    name=$(basename "$skill_dir")
  fi
  printf '%s\n' "$name"
}

platform_text_preference() {
  platform=$1
  field_base=$2
  skill_dir=$3

  case "$platform" in
    xiaping|openclaw)
      value=$(manifest_section_get "$skill_dir" "$platform" "${field_base}_zh" 2>/dev/null || true)
      if [ -n "$value" ]; then
        printf '%s\n' "$value"
        return 0
      fi
      ;;
    clawhub)
      value=$(manifest_section_get "$skill_dir" "$platform" "${field_base}_en" 2>/dev/null || true)
      if [ -n "$value" ]; then
        printf '%s\n' "$value"
        return 0
      fi
      ;;
  esac

  value=$(manifest_section_get "$skill_dir" "$platform" "$field_base" 2>/dev/null || true)
  if [ -n "$value" ]; then
    printf '%s\n' "$value"
    return 0
  fi

  case "$field_base" in
    title)
      skill_name "$skill_dir"
      ;;
    description|summary)
      value=$(manifest_get "$skill_dir" description 2>/dev/null || true)
      if [ -z "$value" ]; then
        value=$(frontmatter_get "$skill_dir" description 2>/dev/null || true)
      fi
      printf '%s\n' "$value"
      ;;
    *)
      printf '\n'
      ;;
  esac
}

replace_frontmatter_field() {
  skill_md_path=$1
  key=$2
  new_value=$3

  python3 - "$skill_md_path" "$key" "$new_value" <<'PY'
from pathlib import Path
import sys

path = Path(sys.argv[1])
key = sys.argv[2]
new_value = sys.argv[3]
lines = path.read_text(encoding="utf-8").splitlines()
in_frontmatter = False
replaced = False
for idx, line in enumerate(lines):
    if idx == 0 and line == "---":
        in_frontmatter = True
        continue
    if in_frontmatter and line == "---":
        if not replaced:
            lines.insert(idx, f"{key}: {new_value}")
        break
    if in_frontmatter and line.startswith(f"{key}:"):
        lines[idx] = f"{key}: {new_value}"
        replaced = True
path.write_text("\n".join(lines) + "\n", encoding="utf-8")
PY
}

replace_manifest_field() {
  manifest_path=$1
  key=$2
  new_value=$3
  [ -f "$manifest_path" ] || return 0

  python3 - "$manifest_path" "$key" "$new_value" <<'PY'
from pathlib import Path
import sys

path = Path(sys.argv[1])
key = sys.argv[2]
new_value = sys.argv[3]
lines = path.read_text(encoding="utf-8").splitlines()
for idx, line in enumerate(lines):
    if line.startswith(f"{key} = "):
        lines[idx] = f'{key} = "{new_value}"'
        break
path.write_text("\n".join(lines) + "\n", encoding="utf-8")
PY
}

prepare_platform_skill_dir() {
  skill_dir=$1
  platform=$2

  localized_name=$(platform_text_preference "$platform" title "$skill_dir")
  localized_description=$(platform_text_preference "$platform" description "$skill_dir")

  if [ -z "$localized_name" ] && [ -z "$localized_description" ]; then
    printf '%s\n' "$skill_dir"
    return 0
  fi

  temp_root=$(mktemp -d "/tmp/skillup-${platform}.XXXXXX")
  skill_copy="$temp_root/$(basename "$skill_dir")"
  cp -R "$skill_dir" "$skill_copy"

  if [ -n "$localized_name" ]; then
    replace_frontmatter_field "$skill_copy/SKILL.md" name "$localized_name"
    replace_manifest_field "$skill_copy/manifest.toml" name "$localized_name"
  fi

  if [ -n "$localized_description" ]; then
    replace_frontmatter_field "$skill_copy/SKILL.md" description "$localized_description"
    replace_manifest_field "$skill_copy/manifest.toml" description "$localized_description"
  fi

  printf '%s\n' "$skill_copy"
}

json_quote() {
  python3 -c 'import json,sys; print(json.dumps(sys.argv[1]))' "$1"
}

json_array_contains() {
  json_value=$1
  needle=$2
  python3 - "$json_value" "$needle" <<'PY'
import json
import sys
try:
    values = json.loads(sys.argv[1])
except Exception:
    sys.exit(2)
sys.exit(0 if sys.argv[2] in values else 1)
PY
}

json_array_each() {
  json_value=$1
  python3 - "$json_value" <<'PY'
import json
import sys
values = json.loads(sys.argv[1])
for item in values:
    print(item)
PY
}

ensure_skill_version() {
  skill_dir=$1
  version=$(skill_version "$skill_dir")
  if [ -z "$version" ]; then
    echo "Missing version metadata for $skill_dir; add version to SKILL.md frontmatter or manifest.toml" >&2
    return 1
  fi
}

bump_version_value() {
  current_version=$1
  bump_part=$2

  python3 - "$current_version" "$bump_part" <<'PY'
import sys
version = sys.argv[1]
part = sys.argv[2]
major, minor, patch = [int(x) for x in version.split(".")]
if part == "patch":
    patch += 1
elif part == "minor":
    minor += 1
    patch = 0
elif part == "major":
    major += 1
    minor = 0
    patch = 0
else:
    raise SystemExit(1)
print(f"{major}.{minor}.{patch}")
PY
}

replace_version_in_skill() {
  skill_dir=$1
  new_version=$2
  python3 - "$skill_dir/SKILL.md" "$new_version" <<'PY'
from pathlib import Path
import sys
path = Path(sys.argv[1])
new_version = sys.argv[2]
text = path.read_text(encoding="utf-8")
lines = text.splitlines()
in_frontmatter = False
for idx, line in enumerate(lines):
    if idx == 0 and line == "---":
        in_frontmatter = True
        continue
    if in_frontmatter and line == "---":
        break
    if in_frontmatter and line.startswith("version:"):
        lines[idx] = f"version: {new_version}"
path.write_text("\n".join(lines) + "\n", encoding="utf-8")
PY
}

replace_version_in_manifest() {
  skill_dir=$1
  new_version=$2
  manifest_path="$skill_dir/manifest.toml"
  [ -f "$manifest_path" ] || return 0
  python3 - "$manifest_path" "$new_version" <<'PY'
from pathlib import Path
import sys
path = Path(sys.argv[1])
new_version = sys.argv[2]
lines = path.read_text(encoding="utf-8").splitlines()
for idx, line in enumerate(lines):
    if line.startswith("version = "):
        lines[idx] = f'version = "{new_version}"'
        break
path.write_text("\n".join(lines) + "\n", encoding="utf-8")
PY
}

run_bump() {
  skill_dir=$1
  current_version=$(skill_version "$skill_dir")
  [ -n "$current_version" ] || {
    echo "Missing version metadata for $skill_dir" >&2
    return 1
  }

  case "$SKILLUP_BUMP_PART" in
    patch|minor|major)
      ;;
    *)
      echo "bump requires patch, minor, or major" >&2
      return 1
      ;;
  esac

  new_version=$(bump_version_value "$current_version" "$SKILLUP_BUMP_PART")
  replace_version_in_skill "$skill_dir" "$new_version"
  replace_version_in_manifest "$skill_dir" "$new_version"
  record_result "bump" "$skill_dir" "updated" "version bumped from $current_version to $new_version" "" "$(skill_slug "$skill_dir")" "$new_version" ""
  printf '[bump] %s -> %s\n' "$current_version" "$new_version"
  return 0
}

run_doctor() {
  skill_dir=$1

  has_git=$(command_exists git && printf yes || printf no)
  has_gh=$(command_exists gh && printf yes || printf no)
  has_claw=$(command_exists claw && printf yes || printf no)
  has_clawhub=$(command_exists clawhub && printf yes || printf no)
  has_zip=$(command_exists zip && printf yes || printf no)
  has_python=$(command_exists python3 && printf yes || printf no)

  record_result "doctor" "$skill_dir" "ok" "environment checked" "" "$(skill_slug "$skill_dir")" "$(skill_version "$skill_dir")" ""
  printf '[doctor] git=%s gh=%s claw=%s clawhub=%s zip=%s python3=%s\n' \
    "$has_git" "$has_gh" "$has_claw" "$has_clawhub" "$has_zip" "$has_python"
  return 0
}

run_status() {
  skill_dir=$1
  platforms_csv=$2
  config_path=$3

  local_version=$(skill_version "$skill_dir")
  record_result "status" "$skill_dir" "local" "local version $local_version" "" "$(skill_slug "$skill_dir")" "$local_version" ""
  printf '[status] %s local=%s\n' "$skill_dir" "$local_version"

  OLD_IFS=$IFS
  IFS=','
  for platform in $platforms_csv; do
    IFS=$OLD_IFS
    trimmed_platform=$(trim "$platform")
    if [ -n "$trimmed_platform" ]; then
      if ! status_platform "$trimmed_platform" "$skill_dir" "$config_path" "$local_version"; then
        SKILLUP_FAILED=1
      fi
    fi
    IFS=','
  done
  IFS=$OLD_IFS

  print_status_summary "$skill_dir" "$local_version"
}

validate_skill_dir() {
  skill_dir=$1
  [ -f "$skill_dir/SKILL.md" ] || {
    echo "Missing SKILL.md in $skill_dir" >&2
    return 1
  }
}

validate_skill_slug() {
  skill_dir=$1
  slug=$(skill_slug "$skill_dir")
  printf '%s' "$slug" | grep -E '^[a-z0-9][a-z0-9-]*$' >/dev/null 2>&1 || {
    echo "Invalid slug '$slug' for $skill_dir" >&2
    return 1
  }
}

validate_skill_metadata() {
  skill_dir=$1
  if ! validate_skill_dir "$skill_dir"; then
    return 1
  fi
  if ! ensure_skill_version "$skill_dir"; then
    return 1
  fi
  if ! validate_skill_slug "$skill_dir"; then
    return 1
  fi
  return 0
}

package_skill() {
  skill_dir=$1
  artifact_dir=$2
  slug=$(skill_slug "$skill_dir")
  artifact_path="$artifact_dir/$slug.zip"
  parent_dir=$(dirname "$skill_dir")
  skill_name_local=$(basename "$skill_dir")

  rm -f "$artifact_path"
  (
    cd "$parent_dir"
    zip -qr "$artifact_path" "$skill_name_local"
  )
  printf '%s\n' "$artifact_path"
}

validate_artifact() {
  artifact_path=$1
  [ -f "$artifact_path" ] || {
    echo "Artifact not found: $artifact_path" >&2
    return 1
  }

  artifact_size=$(wc -c < "$artifact_path")
  if [ "$artifact_size" -gt 52428800 ]; then
    echo "Artifact exceeds 50MB limit: $artifact_path" >&2
    return 1
  fi
}

run_redact_check() {
  skill_dir=$1
  mode=$2
  findings_file=${3:-/tmp/skillup-redact-findings.txt}

  case "$mode" in
    off)
      record_result "redact-check" "$skill_dir" "skipped" "redaction scan disabled" "" "$(skill_slug "$skill_dir")" "$(skill_version "$skill_dir")" ""
      return 0
      ;;
    strict|warn)
      ;;
    *)
      record_result "redact-check" "$skill_dir" "failed" "invalid redact mode: $mode" "" "$(skill_slug "$skill_dir")" "$(skill_version "$skill_dir")" ""
      return 1
      ;;
  esac

  python3 - "$skill_dir" "$findings_file" <<'PY'
from pathlib import Path
import fnmatch
import re
import sys

root = Path(sys.argv[1]).resolve()
findings_file = Path(sys.argv[2])
ignore_file = root / ".skillup-ignore"
ignore_patterns = []
if ignore_file.exists():
    ignore_patterns = [
        line.strip() for line in ignore_file.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]

def ignored(path: Path) -> bool:
    rel = path.relative_to(root).as_posix()
    for part in rel.split("/"):
        if part in {".git", ".skillup-artifacts"}:
            return True
    for pattern in ignore_patterns:
        if fnmatch.fnmatch(rel, pattern) or fnmatch.fnmatch(path.name, pattern):
            return True
    return False

patterns = [
    ("private_key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("bearer", re.compile(r"Authorization:\s*Bearer\s+[A-Za-z0-9._\-]{16,}", re.IGNORECASE)),
    ("token_assignment", re.compile(r"(token|api[_-]?key|secret)\s*[:=]\s*[\"']?[A-Za-z0-9_\-]{16,}", re.IGNORECASE)),
    ("openai_key", re.compile(r"\bsk-[A-Za-z0-9]{20,}\b")),
    ("github_token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b")),
    ("google_api_key", re.compile(r"\bAIza[0-9A-Za-z\-_]{20,}\b")),
    ("slack_token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b")),
    ("jwt", re.compile(r"\beyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}\b")),
]

findings = []
for path in root.rglob("*"):
    if not path.is_file() or ignored(path):
        continue
    if path.suffix.lower() in {".zip", ".png", ".jpg", ".jpeg", ".gif", ".webp", ".pdf", ".ico"}:
        continue
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        continue
    rel = path.relative_to(root).as_posix()
    for line_no, line in enumerate(text.splitlines(), start=1):
        for name, pattern in patterns:
            if pattern.search(line):
                findings.append(f"{rel}:{line_no}:{name}")
                break

findings_file.write_text("\n".join(findings) + ("\n" if findings else ""), encoding="utf-8")
sys.exit(1 if findings else 0)
PY
  scan_status=$?

  if [ "$scan_status" -eq 0 ]; then
    record_result "redact-check" "$skill_dir" "clean" "no sensitive content detected" "" "$(skill_slug "$skill_dir")" "$(skill_version "$skill_dir")" ""
    return 0
  fi

  findings=$(cat "$findings_file" 2>/dev/null || true)
  first_finding=$(printf '%s' "$findings" | head -n 1)
  detail="sensitive content detected"
  if [ -n "$first_finding" ]; then
    detail="$detail: $first_finding"
  fi

  if [ "$mode" = "warn" ]; then
    record_result "redact-check" "$skill_dir" "warning" "$detail" "" "$(skill_slug "$skill_dir")" "$(skill_version "$skill_dir")" ""
    printf '[redact-check] %s warning %s\n' "$skill_dir" "$detail"
    return 0
  fi

  record_result "redact-check" "$skill_dir" "failed" "$detail" "" "$(skill_slug "$skill_dir")" "$(skill_version "$skill_dir")" ""
  printf '[redact-check] %s failed %s\n' "$skill_dir" "$detail"
  return 1
}

trim() {
  printf '%s' "$1" | awk '{ gsub(/^[[:space:]]+|[[:space:]]+$/, ""); print }'
}

record_result() {
  platform=$1
  skill_dir=$2
  status=$3
  detail=$4
  url=${5:-}
  resource_id=${6:-}
  version=${7:-}
  review_state=${8:-}

  SKILLUP_RESULTS="${SKILLUP_RESULTS}${platform}|${skill_dir}|${status}|${detail}|${url}|${resource_id}|${version}|${review_state}
"
}

template_render() {
  template=$1
  slug=$2
  version=$3

  printf '%s\n' "$template" | sed \
    -e "s/{slug}/$slug/g" \
    -e "s/{version}/$version/g"
}

platform_requires_command() {
  platform=$1
  case "$platform" in
    github)
      printf '%s\n' "git"
      ;;
    xiaping)
      printf '%s\n' "curl"
      ;;
    openclaw)
      printf '%s\n' "claw"
      ;;
    clawhub)
      printf '%s\n' "clawhub"
      ;;
    *)
      printf '\n'
      ;;
  esac
}

check_platform() {
  platform=$1
  skill_dir=$2
  config_path=$3

  if ! platform_enabled_for_skill "$platform" "$skill_dir"; then
    record_result "$platform" "$skill_dir" "skipped" "platform disabled in manifest" "" "$(skill_slug "$skill_dir")" "$(skill_version "$skill_dir")" ""
    return 0
  fi

  case "$platform" in
    github)
      check_github "$skill_dir" "$config_path"
      ;;
    xiaping)
      check_xiaping "$skill_dir" "$config_path"
      ;;
    openclaw)
      check_openclaw "$skill_dir" "$config_path"
      ;;
    clawhub)
      check_clawhub "$skill_dir" "$config_path"
      ;;
    *)
      record_result "$platform" "$skill_dir" "skipped" "unknown platform"
      return 0
      ;;
  esac
}

platform_enabled_for_skill() {
  platform=$1
  skill_dir=$2
  enabled=$(manifest_section_enabled "$skill_dir" "$platform")

  case "$enabled" in
    true|1|yes|on)
      return 0
      ;;
    false|0|no|off)
      return 1
      ;;
    *)
      return 0
      ;;
  esac
}

check_common_platform_requirement() {
  platform=$1
  skill_dir=$2
  required_command=$(platform_requires_command "$platform")

  if [ -n "$required_command" ] && ! command_exists "$required_command"; then
    record_result "$platform" "$skill_dir" "failed" "missing command: $required_command"
    return 1
  fi

  return 0
}

run_with_retries() {
  platform=$1
  skill_dir=$2
  artifact_path=$3
  config_path=$4
  dry_run=$5

  attempt=0
  while :; do
    if publish_one "$platform" "$skill_dir" "$artifact_path" "$config_path" "$dry_run"; then
      return 0
    fi
    if [ "$attempt" -ge "$SKILLUP_RETRY_COUNT" ]; then
      return 1
    fi
    attempt=$((attempt + 1))
  done
}

platform_blocking_status() {
  status=$1
  case "$status" in
    failed|failed_platform_bug)
      printf 'true\n'
      ;;
    *)
      printf 'false\n'
      ;;
  esac
}

platform_adjusted_status() {
  status=$1
  detail=$2
  case "$status" in
    platform-version-adjusted)
      printf 'true\n'
      ;;
    *)
      case "$detail" in
        *"platform adjusted version"*|*"auto-adjusted patch version"*)
          printf 'true\n'
          ;;
        *)
          printf 'false\n'
          ;;
      esac
      ;;
  esac
}

print_publish_diff_summary() {
  skill_dir=$1
  local_version=$2
  summary=$(SKILLUP_RESULTS_DATA=$SKILLUP_RESULTS python3 - "$skill_dir" "$local_version" <<'PY'
import os
import sys

skill_dir = sys.argv[1]
rows = []
for line in os.environ.get("SKILLUP_RESULTS_DATA", "").splitlines():
    if not line.strip():
        continue
    parts = line.split("|")
    parts += [""] * (8 - len(parts))
    if parts[1] != skill_dir:
        continue
    if parts[0] not in {"github", "xiaping", "openclaw", "clawhub"}:
        continue
    rows.append(parts)

parts_out = []
for platform, _, status, detail, _, _, version, review_state in rows:
    if status in {"in-sync"}:
        action = "无变更"
    elif status in {"platform-version-adjusted"}:
        action = f"平台版本已前进到 {version or 'unknown'}"
    elif status in {"out-of-sync"}:
        action = f"将发布到 {platform}"
    elif status in {"status-review"}:
        action = "状态待确认"
    elif status in {"status-unknown"}:
        action = "远端状态未知"
    else:
        continue
    label = {
        "github": "GitHub",
        "xiaping": "虾评",
        "openclaw": "OpenClaw 中文社区",
        "clawhub": "ClawHub",
    }.get(platform, platform)
    parts_out.append(f"{label}:{action}")

print("，".join(parts_out))
PY
)
  [ -n "$summary" ] || summary="未获取到平台差异"
  record_result "publish-diff" "$skill_dir" "summary" "$summary" "" "$(skill_slug "$skill_dir")" "$local_version" ""
  printf '[publish-diff] %s\n' "$summary"
}

run_platform_status_checks() {
  skill_dir=$1
  platforms_csv=$2
  config_path=$3
  local_version=$4

  OLD_IFS=$IFS
  IFS=','
  for platform in $platforms_csv; do
    IFS=$OLD_IFS
    trimmed_platform=$(trim "$platform")
    if [ -n "$trimmed_platform" ]; then
      status_platform "$trimmed_platform" "$skill_dir" "$config_path" "$local_version" >/dev/null 2>&1 || true
    fi
    IFS=','
  done
  IFS=$OLD_IFS
}

run_publish_parallel() {
  skill_dir=$1
  platforms_csv=$2
  artifact_path=$3
  config_path=$4
  dry_run=$5
  skill_failed=0
  worker_dir=$(mktemp -d "/tmp/skillup-publish.XXXXXX")

  OLD_IFS=$IFS
  IFS=','
  index=0
  for platform in $platforms_csv; do
    IFS=$OLD_IFS
    trimmed_platform=$(trim "$platform")
    if [ -n "$trimmed_platform" ]; then
      if ! platform_enabled_for_skill "$trimmed_platform" "$skill_dir"; then
        record_result "$trimmed_platform" "$skill_dir" "skipped" "platform disabled in manifest" "" "$(skill_slug "$skill_dir")" "$(skill_version "$skill_dir")" ""
      else
        result_file="$worker_dir/$index.results"
        status_file="$worker_dir/$index.status"
        (
          SKILLUP_RESULTS=""
          if run_with_retries "$trimmed_platform" "$skill_dir" "$artifact_path" "$config_path" "$dry_run"; then
            printf '0\n' > "$status_file"
          else
            printf '1\n' > "$status_file"
          fi
          printf '%s' "$SKILLUP_RESULTS" > "$result_file"
        ) &
        eval "worker_pid_$index=$!"
        eval "worker_result_$index='$result_file'"
        eval "worker_status_$index='$status_file'"
        index=$((index + 1))
      fi
    fi
    IFS=','
  done
  IFS=$OLD_IFS

  current=0
  while [ "$current" -lt "$index" ]; do
    eval "wait \$worker_pid_$current"
    eval "result_file=\$worker_result_$current"
    eval "status_file=\$worker_status_$current"
    if [ -f "$result_file" ]; then
      worker_results=$(cat "$result_file")
      if [ -n "$worker_results" ]; then
        SKILLUP_RESULTS="${SKILLUP_RESULTS}${worker_results}
"
      fi
    fi
    if [ -f "$status_file" ] && [ "$(cat "$status_file")" != "0" ]; then
      skill_failed=1
    fi
    current=$((current + 1))
  done

  rm -rf "$worker_dir"
  [ "$skill_failed" -eq 0 ]
}

install_local_skill() {
  skill_dir=$1
  install_target=$2
  skill_name_local=$(basename "$skill_dir")
  backup_root=$(mktemp -d "/tmp/skillup-install.XXXXXX")
  installed_any=0

  for target in $(printf '%s\n' "$install_target" | tr ',' ' '); do
    case "$target" in
      codex)
        install_root="$HOME/.codex/skills"
        ;;
      openclaw)
        install_root="$HOME/.openclaw/skills"
        ;;
      both)
        for sub_target in codex openclaw; do
          install_local_skill "$skill_dir" "$sub_target"
        done
        rm -rf "$backup_root"
        return 0
        ;;
      *)
        record_result "install-local" "$skill_dir" "failed" "unknown install target: $target" "" "$(skill_slug "$skill_dir")" "$(skill_version "$skill_dir")" ""
        rm -rf "$backup_root"
        return 1
        ;;
    esac

    mkdir -p "$install_root"
    destination="$install_root/$skill_name_local"
    if [ -d "$destination" ]; then
      mv "$destination" "$backup_root/${skill_name_local}.${target}.backup"
    fi
    cp -R "$skill_dir" "$destination"
    record_result "install-local" "$skill_dir" "installed" "installed to $destination" "$destination" "$(skill_slug "$skill_dir")" "$(skill_version "$skill_dir")" "$target"
    installed_any=1
  done

  [ "$installed_any" -eq 1 ]
}

rollback_skill_from_github() {
  skill_dir=$1
  config_path=$2
  rollback_version=$3

  repo_name=$(config_get "$config_path" github repo "")
  slug=$(skill_slug "$skill_dir")
  tag="${slug}-v${rollback_version}"
  [ -n "$repo_name" ] || {
    record_result "rollback" "$skill_dir" "failed" "github.repo is required for rollback" "" "$slug" "$rollback_version" "github"
    return 1
  }
  command_exists gh || {
    record_result "rollback" "$skill_dir" "failed" "gh CLI is required for rollback" "" "$slug" "$rollback_version" "github"
    return 1
  }

  rollback_dir=$(mktemp -d "/tmp/skillup-rollback.XXXXXX")
  backup_dir=$(mktemp -d "/tmp/skillup-rollback-backup.XXXXXX")
  artifact_pattern="${slug}.zip"

  cp -R "$skill_dir" "$backup_dir/$(basename "$skill_dir")"
  if ! gh release download "$tag" --repo "$repo_name" --pattern "$artifact_pattern" --dir "$rollback_dir" >/tmp/skillup-rollback.log 2>&1; then
    record_result "rollback" "$skill_dir" "failed" "unable to download release asset for $tag" "" "$slug" "$rollback_version" "github"
    rm -rf "$rollback_dir" "$backup_dir"
    return 1
  fi

  rm -rf "$skill_dir"
  mkdir -p "$(dirname "$skill_dir")"
  if ! unzip -q "$rollback_dir/$artifact_pattern" -d "$rollback_dir/unpacked"; then
    record_result "rollback" "$skill_dir" "failed" "unable to extract release asset for $tag" "" "$slug" "$rollback_version" "github"
    rm -rf "$rollback_dir"
    cp -R "$backup_dir/$(basename "$skill_dir")" "$skill_dir"
    rm -rf "$backup_dir"
    return 1
  fi
  mv "$rollback_dir/unpacked/$(basename "$skill_dir")" "$skill_dir"
  record_result "rollback" "$skill_dir" "rolled-back" "restored local files from GitHub release $tag" "https://github.com/$repo_name/releases/tag/$tag" "$slug" "$rollback_version" "github"
  rm -rf "$rollback_dir" "$backup_dir"
  return 0
}

process_skill() {
  skill_dir=$1
  platforms_csv=$2
  config_path=$3
  artifact_dir=$4
  dry_run=$5
  skill_failed=0

  if [ "$SKILLUP_MODE" = "bump" ]; then
    run_bump "$skill_dir"
    return
  fi

  if [ "$SKILLUP_MODE" = "doctor" ]; then
    run_doctor "$skill_dir"
    return
  fi

  if [ "$SKILLUP_MODE" = "install-local" ]; then
    validate_skill_metadata "$skill_dir"
    install_local_skill "$skill_dir" "$SKILLUP_INSTALL_TARGET"
    return
  fi

  if [ "$SKILLUP_MODE" = "rollback" ]; then
    validate_skill_metadata "$skill_dir"
    rollback_skill_from_github "$skill_dir" "$config_path" "$SKILLUP_ROLLBACK_VERSION"
    return
  fi

  if [ "$SKILLUP_MODE" = "status" ]; then
    validate_skill_metadata "$skill_dir"
    run_status "$skill_dir" "$platforms_csv" "$config_path"
    return
  fi

  if ! validate_skill_metadata "$skill_dir"; then
    record_result "check" "$skill_dir" "failed" "skill validation failed"
    return 1
  fi

  record_result "check" "$skill_dir" "validated" "skill metadata passed validation" "" "$(skill_slug "$skill_dir")" "$(skill_version "$skill_dir")" ""

  redact_mode=$(config_get "$config_path" defaults redact_mode "$SKILLUP_REDACT_MODE")
  if ! run_redact_check "$skill_dir" "$redact_mode"; then
    return 1
  fi

  if [ "$SKILLUP_MODE" = "redact-check" ]; then
    return
  fi

  local_version=$(skill_version "$skill_dir")
  run_platform_status_checks "$skill_dir" "$platforms_csv" "$config_path" "$local_version"
  print_publish_diff_summary "$skill_dir" "$local_version"

  OLD_IFS=$IFS
  IFS=','
  for platform in $platforms_csv; do
    IFS=$OLD_IFS
    trimmed_platform=$(trim "$platform")
    if [ -n "$trimmed_platform" ]; then
      if ! check_platform "$trimmed_platform" "$skill_dir" "$config_path"; then
        skill_failed=1
        if [ "$SKILLUP_FAIL_FAST" -eq 1 ]; then
          IFS=','
          break
        fi
      fi
    fi
    IFS=','
  done
  IFS=$OLD_IFS

  if [ "$SKILLUP_MODE" = "check" ]; then
    [ "$skill_failed" -eq 0 ]
    return
  fi

  artifact_path=$(package_skill "$skill_dir" "$artifact_dir")
  if ! validate_artifact "$artifact_path"; then
    record_result "package" "$skill_dir" "failed" "artifact validation failed" "" "$(skill_slug "$skill_dir")" "$(skill_version "$skill_dir")" ""
    return 1
  fi
  record_result "package" "$skill_dir" "packaged" "artifact created" "$artifact_path" "$(skill_slug "$skill_dir")" "$(skill_version "$skill_dir")" ""

  if [ "$SKILLUP_MODE" = "package" ]; then
    [ "$skill_failed" -eq 0 ]
    return
  fi

  if [ "$SKILLUP_PARALLEL_PUBLISH" -eq 1 ] && [ "$SKILLUP_FAIL_FAST" -eq 0 ]; then
    if ! run_publish_parallel "$skill_dir" "$platforms_csv" "$artifact_path" "$config_path" "$dry_run"; then
      skill_failed=1
    fi
  else
    OLD_IFS=$IFS
    IFS=','
    for platform in $platforms_csv; do
      IFS=$OLD_IFS
      trimmed_platform=$(trim "$platform")
      if [ -n "$trimmed_platform" ]; then
        if ! platform_enabled_for_skill "$trimmed_platform" "$skill_dir"; then
          record_result "$trimmed_platform" "$skill_dir" "skipped" "platform disabled in manifest" "" "$(skill_slug "$skill_dir")" "$(skill_version "$skill_dir")" ""
          IFS=','
          continue
        fi
        if ! run_with_retries "$trimmed_platform" "$skill_dir" "$artifact_path" "$config_path" "$dry_run"; then
          skill_failed=1
          if [ "$SKILLUP_FAIL_FAST" -eq 1 ]; then
            IFS=','
            break
          fi
        fi
      fi
      IFS=','
    done
    IFS=$OLD_IFS
  fi

  [ "$skill_failed" -eq 0 ]
}

publish_one() {
  raw_platform=$1
  skill_dir=$2
  artifact_path=$3
  config_path=$4
  dry_run=$5
  platform=$(trim "$raw_platform")

  case "$platform" in
    github)
      publish_github "$skill_dir" "$artifact_path" "$config_path" "$dry_run"
      ;;
    xiaping)
      publish_xiaping "$skill_dir" "$artifact_path" "$config_path" "$dry_run"
      ;;
    openclaw)
      publish_openclaw "$skill_dir" "$artifact_path" "$config_path" "$dry_run"
      ;;
    clawhub)
      publish_clawhub "$skill_dir" "$artifact_path" "$config_path" "$dry_run"
      ;;
    "")
      return 0
      ;;
    *)
      record_result "$platform" "$skill_dir" "skipped" "unknown platform"
      return 0
      ;;
  esac
}

status_platform() {
  platform=$1
  skill_dir=$2
  config_path=$3
  local_version=$4

  case "$platform" in
    github)
      status_github "$skill_dir" "$config_path" "$local_version"
      ;;
    xiaping)
      status_xiaping "$skill_dir" "$config_path" "$local_version"
      ;;
    openclaw)
      status_openclaw "$skill_dir" "$config_path" "$local_version"
      ;;
    clawhub)
      status_clawhub "$skill_dir" "$config_path" "$local_version"
      ;;
    *)
      record_result "$platform" "$skill_dir" "skipped" "unknown platform"
      ;;
  esac
}

print_status_summary() {
  skill_dir=$1
  local_version=$2
  summary=$(SKILLUP_RESULTS_DATA=$SKILLUP_RESULTS python3 - "$skill_dir" "$local_version" <<'PY'
import os
import sys

skill_dir = sys.argv[1]
local_version = sys.argv[2]
rows = []
for line in os.environ.get("SKILLUP_RESULTS_DATA", "").splitlines():
    if not line.strip():
        continue
    parts = line.split("|")
    parts += [""] * (8 - len(parts))
    if parts[1] != skill_dir:
        continue
    rows.append(parts)

parts_out = []
for platform, _, status, detail, _, _, version, review_state in rows:
    if platform == "github":
        parts_out.append("GitHub已同步" if status == "in-sync" else "GitHub未同步")
    elif platform == "xiaping":
        if status == "in-sync":
            parts_out.append("虾评已同步")
        elif status == "platform-version-adjusted":
            parts_out.append("虾评已同步")
        else:
            parts_out.append("虾评未同步")
    elif platform == "openclaw":
        if status == "in-sync":
            parts_out.append("OpenClaw 中文社区已同步")
        elif status == "status-review":
            parts_out.append("OpenClaw 中文社区待确认")
        else:
            parts_out.append("OpenClaw 中文社区未同步")
    elif platform == "clawhub":
        if status == "in-sync":
            parts_out.append("ClawHub已同步")
        elif status == "status-review":
            if review_state == "security_scan_pending" or "scan pending" in detail.lower():
                parts_out.append("ClawHub扫描中")
            else:
                parts_out.append("ClawHub待确认")
        elif status == "out-of-sync":
            parts_out.append("ClawHub未发布")
        else:
            parts_out.append("ClawHub待确认")

summary = "，".join(parts_out) if parts_out else f"本地版本 {local_version}"
print(summary)
PY
)
  record_result "status-summary" "$skill_dir" "summary" "$summary" "" "$(skill_slug "$skill_dir")" "$local_version" ""
  printf '[status-summary] %s\n' "$summary"
}

print_summary() {
  printf '%s' "$SKILLUP_RESULTS" | awk -F'|' 'NF >= 4 {
    extra = ""
    if ($5 != "") extra = " " $5
    printf "[%s] %s -> %s (%s)%s\n", $1, $2, $3, $4, extra
  }'
}

write_results_json() {
  result_file=$1
  result_dir=$(dirname "$result_file")
  mkdir -p "$result_dir"

  SKILLUP_RESULTS_DATA=$SKILLUP_RESULTS python3 - "$result_file" <<'PY'
import json
import os
import sys
from pathlib import Path

def local_version_for(skill_dir: str) -> str:
    path = Path(skill_dir)
    manifest = path / "manifest.toml"
    if manifest.exists():
        for line in manifest.read_text(encoding="utf-8").splitlines():
            if line.startswith("version = "):
                return line.split("=", 1)[1].strip().strip('"')
    skill_md = path / "SKILL.md"
    if skill_md.exists():
        in_frontmatter = False
        for idx, line in enumerate(skill_md.read_text(encoding="utf-8").splitlines()):
            if idx == 0 and line == "---":
                in_frontmatter = True
                continue
            if in_frontmatter and line == "---":
                break
            if in_frontmatter and line.startswith("version:"):
                return line.split(":", 1)[1].strip()
    return ""

rows = []
raw = os.environ.get("SKILLUP_RESULTS_DATA", "")
for line in raw.splitlines():
    if not line.strip():
        continue
    parts = line.split("|")
    parts.extend([""] * (8 - len(parts)))
    status = parts[2]
    detail = parts[3]
    version = parts[6]
    local_version = local_version_for(parts[1]) if parts[1] else ""
    remote_version = ""
    if status in {"in-sync", "platform-version-adjusted", "status-review", "published", "rolled-back", "out-of-sync"}:
        remote_version = version
    platform_adjusted = status == "platform-version-adjusted" or "platform adjusted version" in detail or "auto-adjusted patch version" in detail
    blocking = status in {"failed", "failed_platform_bug"}
    rows.append(
        {
            "platform": parts[0],
            "skill_dir": parts[1],
            "status": status,
            "detail": detail,
            "url": parts[4],
            "id": parts[5],
            "version": version,
            "local_version": local_version,
            "remote_version": remote_version,
            "platform_adjusted": platform_adjusted,
            "blocking": blocking,
            "review_state": parts[7],
        }
    )

with open(sys.argv[1], "w", encoding="utf-8") as handle:
    json.dump(rows, handle, ensure_ascii=False, indent=2)
PY
}

env_or_config() {
  env_name=$1
  config_path=$2
  section=$3
  key=$4
  default_value=$5

  eval "env_value=\${$env_name:-}"
  if [ -n "$env_value" ]; then
    printf '%s\n' "$env_value"
    return
  fi

  config_get "$config_path" "$section" "$key" "$default_value"
}
