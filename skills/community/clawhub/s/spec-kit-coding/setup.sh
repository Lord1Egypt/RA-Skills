#!/usr/bin/env bash
# ============================================================================
# spec-kit-coding setup.sh — Dependency Check & Auto-Install
# ============================================================================
# Usage:
#   bash setup.sh              # Check all dependencies and install missing ones
#   bash setup.sh --check-only # Only check, don't install anything
#   bash setup.sh --force      # Force reinstall everything
#   bash setup.sh --help       # Show this help
#
# This script checks for and installs:
#   1. `specify` CLI (GitHub Spec-Kit)
#   2. speckit-* skills
#   3. CodingGuidance files (TopLevelCodingGuidance + DesignPattern)
#   4. External auxiliary skills (ECC, superpowers, mattpocock, ui-ux-pro-max)
# ============================================================================

set -euo pipefail

WORKSPACE="${HOME}/.openclaw/workspace"
SKILLS_DIR="${WORKSPACE}/skills"
SPEC_KIT_DIR="${SKILLS_DIR}/spec-kit-coding"
EXTERNAL_DIR="${SPEC_KIT_DIR}/external-skills"

MODE=""
FORCE=false

usage() {
    cat <<EOF
Usage: bash setup.sh [OPTIONS]

Options:
  --check-only    Only check, don't install anything
  --force         Force reinstall everything
  --help          Show this help
EOF
    exit 0
}

for arg in "$@"; do
    case "$arg" in
        --check-only) MODE="--check-only" ;;
        --force)      FORCE=true ;;
        --help)       usage ;;
        *)            echo "Unknown option: $arg"; usage ;;
    esac
done

# Mutual exclusion: --force and --check-only conflict
if [ "$FORCE" = "true" ] && [ "$MODE" = "--check-only" ]; then
    echo "Error: --force and --check-only cannot be used together."
    echo "  --check-only: only report status, don't install"
    echo "  --force: reinstall everything"
    exit 1
fi

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

ok()   { echo -e "${GREEN}[✓]${NC} $1"; }
warn() { echo -e "${YELLOW}[!]${NC} $1"; }
fail() { echo -e "${RED}[✗]${NC} $1"; }
info() { echo -e "    $1"; }

# Helper: git clone with retry (works with set -e)
git_clone_with_retry() {
    local repo="$1" dest="$2" max_retries="${3:-3}" delay="${4:-3}"
    local attempt=1 last_err
    while [ $attempt -le $max_retries ]; do
        last_err=$(git clone --depth 1 "$repo" "$dest" 2>&1) && return 0
        if [ $attempt -lt $max_retries ]; then
            warn "git clone attempt $attempt/$max_retries failed, retrying in ${delay}s..."
            sleep "$delay"
        fi
        attempt=$((attempt + 1))
    done
    echo "$last_err" >&2
    return 1
}

# Helper: write standardized SOURCE.md for a third-party skill directory
# Args: $1 = dest_dir (absolute path to skill directory)
#       $2 = source_url (full URL or repo path; used verbatim in "Source:" field)
#       $3 = date_str (optional — defaults to today; use "unknown" for pre-existing)
write_source_md() {
    local dest_dir="$1"
    local source_url="$2"
    local date_str="${3:-$(date +%Y-%m-%d)}"
    cat > "${dest_dir}/SOURCE.md" <<EOF
Source: $source_url
Downloaded: $date_str
Unmodified third-party skill.
EOF
}

# ---------------------------------------------------------------------------
# 1. Check `specify` CLI
# ---------------------------------------------------------------------------
check_specify() {
    echo ""
    echo "=== 1. Checking specify CLI ==="

    if [ "$FORCE" != "true" ]; then
        if command -v specify &>/dev/null; then
            local ver
            ver=$(specify version 2>/dev/null || echo "unknown")
            ok "specify CLI found: $ver"
            return 0
        fi
    else
        warn "--force: will reinstall specify CLI"
    fi

    if [ "$MODE" = "--check-only" ]; then
        if command -v specify &>/dev/null; then
            ok "specify CLI found"
            return 0
        fi
        fail "specify CLI not found"
        info "Run without --check-only to install."
        return 1
    fi

    info "Installing specify CLI via uv..."
    if command -v uv &>/dev/null; then
        uv tool install specify-cli --from git+https://github.com/github/spec-kit.git@latest --force
        ok "specify CLI installed via uv"
    elif command -v pipx &>/dev/null; then
        pipx install --force git+https://github.com/github/spec-kit.git@latest
        ok "specify CLI installed via pipx"
    else
        fail "Neither uv nor pipx found. Please install one of them first."
        info "  uv:  https://docs.astral.sh/uv/"
        info "  pipx: https://pipx.pypa.io/"
        return 1
    fi
    return 0
}

# ---------------------------------------------------------------------------
# 2. Check speckit-* skills
# ---------------------------------------------------------------------------
check_speckit_skills() {
    echo ""
    echo "=== 2. Checking speckit-* skills ==="

    local SPEKKIT_SKILLS=(
        speckit-constitution
        speckit-specify
        speckit-clarify
        speckit-checklist
        speckit-plan
        speckit-tasks
        speckit-analyze
        speckit-implement
    )

    local missing=()
    for skill in "${SPEKKIT_SKILLS[@]}"; do
        if [ -f "${EXTERNAL_DIR}/${skill}/SKILL.md" ] && [ "$FORCE" != "true" ]; then
            :  # present — count later
        elif [ "$FORCE" = "true" ]; then
            missing+=("$skill")
        else
            missing+=("$skill")
        fi
    done

    if [ ${#missing[@]} -eq 0 ]; then
        ok "All speckit skills present (${#SPEKKIT_SKILLS[@]} total)"
        return 0
    fi

    if [ "$FORCE" = "true" ]; then
        warn "--force: will regenerate all ${#SPEKKIT_SKILLS[@]} speckit skills"
    else
        for skill in "${missing[@]}"; do
            fail "$skill"
        done
    fi

    if [ "$MODE" = "--check-only" ]; then
        info "Missing speckit skills. Run without --check-only to generate them."
        return 1
    fi

    info "Generating speckit-* skills via specify init..."
    mkdir -p "$EXTERNAL_DIR"
    local tmpdir
    tmpdir=$(mktemp -d -t speckit-init.XXXXXX)
    register_cleanup "$tmpdir"
    local _orig_dir="$PWD"
    cd "$tmpdir"

    if ! command -v specify &>/dev/null; then
        fail "specify CLI not available — cannot generate speckit skills"
        cd "$_orig_dir"
        return 1
    fi

    # Clean old skill directories before regeneration (--force: prevent stale files)
    for skill in "${missing[@]}"; do
        rm -rf "${EXTERNAL_DIR}/${skill}"
    done

    specify init --here --integration claude --force --ignore-agent-tools --script sh --no-git 2>/dev/null
    # Guard: glob may fail if specify CLI changes output structure
    # NOTE: compgen is a bash builtin — this script requires bash, not POSIX sh
    if compgen -G ".claude/skills/speckit-*" > /dev/null 2>&1; then
        cp -r .claude/skills/speckit-* "${EXTERNAL_DIR}/"
    else
        fail "speckit-* skills not found (specify CLI may have changed output structure)"
        cd "$_orig_dir"
        return 1
    fi

    # Verify
    local gen_ok=0 gen_fail=0
    for skill in "${missing[@]}"; do
        if [ -f "${EXTERNAL_DIR}/${skill}/SKILL.md" ]; then
            gen_ok=$((gen_ok + 1))
        else
            fail "$skill (generation failed)"
            gen_fail=$((gen_fail + 1))
        fi
    done
    if [ "$gen_fail" -eq 0 ]; then
        ok "All speckit skills generated (${gen_ok} total)"
    fi
    cd "$_orig_dir"
    return $gen_fail
}

# ---------------------------------------------------------------------------
# 3. Check CodingGuidance files
# ---------------------------------------------------------------------------
check_coding_guidance() {
    echo ""
    echo "=== 3. Checking CodingGuidance ==="

    local GUIDANCE_DIR="${SPEC_KIT_DIR}/CodingGuidance"

    local ALL_OK=true

    # Check TopLevelCodingGuidance.md
    if [ -f "${GUIDANCE_DIR}/TopLevelCodingGuidance.md" ]; then
        ok "TopLevelCodingGuidance.md"
    else
        fail "TopLevelCodingGuidance.md (missing — bundled with the skill, not downloadable)"
        ALL_OK=false
    fi

    # Check CppCodingStyle.md
    if [ -f "${GUIDANCE_DIR}/CppCodingStyle.md" ]; then
        ok "CppCodingStyle.md"
    else
        fail "CppCodingStyle.md (missing — bundled with the skill, not downloadable)"
        ALL_OK=false
    fi

    # Check CppEngineeringFrameworkReference directory
    if [ -d "${GUIDANCE_DIR}/CppEngineeringFrameworkReference" ]; then
        ok "CppEngineeringFrameworkReference"
    else
        fail "CppEngineeringFrameworkReference (missing — bundled with the skill, not downloadable)"
        ALL_OK=false
    fi

    # Check DesignPattern directory
    if [ -d "${GUIDANCE_DIR}/DesignPattern" ]; then
        ok "DesignPattern"
    else
        fail "DesignPattern (missing — bundled with the skill, not downloadable)"
        ALL_OK=false
    fi

    if $ALL_OK; then
        ok "All CodingGuidance files present"
        return 0
    else
        return 1
    fi
}

# ---------------------------------------------------------------------------
# 4. Check external auxiliary skills
# ---------------------------------------------------------------------------
check_external_skills() {
    echo ""
    echo "=== 4. Checking external auxiliary skills ==="

    mkdir -p "$EXTERNAL_DIR"

    local ALL_OK=true

    # --- 3a. ECC language skills ---
    echo ""
    info "ECC language skills:"
    if ! check_ecc_skills; then ALL_OK=false; fi

    # --- 3b. superpowers skills ---
    echo ""
    info "superpowers skills:"
    # These are small standalone SKILL.md files — fetch from raw GitHub
    local SP_SKILLS=(
        "superpowers-requesting-code-review=https://raw.githubusercontent.com/obra/superpowers/main/skills/requesting-code-review/SKILL.md"
        "superpowers-systematic-debugging=https://raw.githubusercontent.com/obra/superpowers/main/skills/systematic-debugging/SKILL.md"
    )

    for entry in "${SP_SKILLS[@]}"; do
        local name="${entry%%=*}"
        local url="${entry#*=}"
        check_single_file_skill "$name" "$url" "obra/superpowers" || ALL_OK=false
    done

    # --- 3c. mattpocock skills ---
    echo ""
    info "mattpocock skills:"
    local MP_SKILLS=(
        "mattpocock-diagnose=https://raw.githubusercontent.com/mattpocock/skills/main/skills/engineering/diagnose/SKILL.md"
        "mattpocock-improve-codebase-architecture=https://raw.githubusercontent.com/mattpocock/skills/main/skills/engineering/improve-codebase-architecture/SKILL.md"
    )

    for entry in "${MP_SKILLS[@]}"; do
        local name="${entry%%=*}"
        local url="${entry#*=}"
        check_single_file_skill "$name" "$url" "mattpocock/skills" || ALL_OK=false
    done

    # --- 3c2. mattpocock multi-file skills (directory-level) ---
    echo ""
    info "mattpocock multi-file skills:"
    check_mattpocock_dir_skills || ALL_OK=false

    # --- 3d. ui-ux-pro-max entire repo ---
    echo ""
    info "ui-ux-pro-max skill:"
    check_uipro_skill || ALL_OK=false

    if $ALL_OK; then
        ok "All external skills present"
        generate_skill_manifest
        return 0
    else
        return 1
    fi
}

# Helper: generate a manifest of all installed external skills
generate_skill_manifest() {
    local manifest="${EXTERNAL_DIR}/MANIFEST.md"
    local now
    now=$(date '+%Y-%m-%d %H:%M')

    # Run in subshell to isolate shopt changes from the caller
    (
        shopt -s nullglob 2>/dev/null || true
        {
            echo "# External Skills Manifest"
            echo ""
            echo "Generated: $now"
            echo ""
            echo "| Skill | Source | Downloaded |"
            echo "|-------|--------|------------|"
            for skill_dir in "${EXTERNAL_DIR}"/*/; do
                name=$(basename "$skill_dir")
                source=""
                downloaded="unknown"
                if [ -f "${skill_dir}/SOURCE.md" ]; then
                    source=$(grep '^Source:' "${skill_dir}/SOURCE.md" | head -1 | sed 's/^Source: //')
                    downloaded=$(grep '^Downloaded:' "${skill_dir}/SOURCE.md" | head -1 | sed 's/^Downloaded: //')
                fi
                [ -z "$source" ] && source="—"
                echo "| $name | $source | $downloaded |"
            done
            echo ""
            echo "Total: $(find "${EXTERNAL_DIR}" -name SKILL.md | wc -l | tr -d ' ') skills"
        } > "$manifest"
    )
    ok "Skill manifest written: external-skills/MANIFEST.md"
}

# Helper: download a single-file skill from a raw URL
check_single_file_skill() {
    local name="$1"
    local url="$2"
    local source="$3"
    local dest_dir="${EXTERNAL_DIR}/${name}"

    if [ -f "${dest_dir}/SKILL.md" ] && [ "$FORCE" != "true" ]; then
        ok "$name (found in external-skills/)"
        # Ensure SOURCE.md exists for skills downloaded before SOURCE.md was introduced
        if [ ! -f "${dest_dir}/SOURCE.md" ]; then
            write_source_md "$dest_dir" "https://github.com/$source" "unknown (pre-existing)"
        fi
        return 0
    fi

    if [ "$MODE" = "--check-only" ]; then
        fail "$name (not found)"
        return 1
    fi

    warn "$name not found, downloading from $source..."
    mkdir -p "$dest_dir"

    if curl -fsSL --retry 3 --retry-delay 2 "$url" -o "${dest_dir}/SKILL.md"; then
        # Validate: file must be non-empty and look like a Markdown skill file
        if [ ! -s "${dest_dir}/SKILL.md" ]; then
            fail "$name (downloaded file is empty — check URL: $url)"
            rm -f "${dest_dir}/SKILL.md"
            return 1
        fi
        # Reject HTML error pages and non-markdown content
        local first_line
        first_line=$(head -1 "${dest_dir}/SKILL.md")
        if echo "$first_line" | grep -qiE '^<(!DOCTYPE|html|head)'; then
            fail "$name (downloaded HTML instead of Markdown — URL may be invalid: $url)"
            rm -f "${dest_dir}/SKILL.md"
            return 1
        fi
        if ! echo "$first_line" | grep -qE '^(#|---|[A-Za-z])'; then
            fail "$name (downloaded file doesn't look like Markdown — may be an error page)"
            rm -f "${dest_dir}/SKILL.md"
            return 1
        fi
        write_source_md "$dest_dir" "https://github.com/$source"
        ok "$name (downloaded)"
    else
        fail "$name (download failed)"
        return 1
    fi
}

# Helper: check multi-file mattpocock skills (entire skill directories from cloned repo)
check_mattpocock_dir_skills() {
    local MP_REPO="https://github.com/mattpocock/skills.git"

    # Map: local-name=repo-path
    local MP_DIR_SKILLS=(
        "mattpocock-grill-with-docs=skills/engineering/grill-with-docs"
    )

    local need_download=false
    for entry in "${MP_DIR_SKILLS[@]}"; do
        local name="${entry%%=*}"
        if [ ! -f "${EXTERNAL_DIR}/${name}/SKILL.md" ] || [ "$FORCE" = "true" ]; then
            need_download=true
            break
        fi
    done

    if ! $need_download; then
        ok "All multi-file mattpocock skills present (${#MP_DIR_SKILLS[@]} total)"
        for entry in "${MP_DIR_SKILLS[@]}"; do
            local name="${entry%%=*}"
            local srcfile="${EXTERNAL_DIR}/${name}/SOURCE.md"
            if [ ! -f "$srcfile" ]; then
                write_source_md "${EXTERNAL_DIR}/${name}" "https://github.com/mattpocock/skills/tree/main/${entry#*=}"
            fi
        done
        return 0
    fi

    if [ "$MODE" = "--check-only" ]; then
        local count=0
        for entry in "${MP_DIR_SKILLS[@]}"; do
            local name="${entry%%=*}"
            if [ ! -f "${EXTERNAL_DIR}/${name}/SKILL.md" ]; then
                fail "$name (not found)"
                count=$((count + 1))
            fi
        done
        if [ "$count" -gt 0 ]; then
            info "$count/${#MP_DIR_SKILLS[@]} multi-file mattpocock skills missing"
            return 1
        fi
        return 0
    fi

    warn "Downloading multi-file mattpocock skills from GitHub..."
    local MP_TMP
    MP_TMP=$(mktemp -d -t mp-skills.XXXXXX)
    register_cleanup "$MP_TMP"

    if ! git_clone_with_retry "$MP_REPO" "$MP_TMP"; then
        fail "Failed to clone mattpocock/skills repo after retries"
        return 1
    fi

    local mp_ok=0 mp_fail=0
    for entry in "${MP_DIR_SKILLS[@]}"; do
        local name="${entry%%=*}"
        local repo_path="${entry#*=}"
        local src="$MP_TMP/$repo_path"
        local dest="${EXTERNAL_DIR}/${name}"
        if [ -d "$src" ] && [ -f "${src}/SKILL.md" ]; then
            rm -rf "$dest" && cp -r "$src" "$dest"
            write_source_md "$dest" "https://github.com/mattpocock/skills/tree/main/$repo_path"
            mp_ok=$((mp_ok + 1))
        else
            fail "$name (SKILL.md not found at $repo_path — repo structure may have changed)"
            mp_fail=$((mp_fail + 1))
        fi
    done

    rm -rf "$MP_TMP"
    if [ "$mp_fail" -gt 0 ]; then
        info "$mp_ok downloaded, $mp_fail failed (out of ${#MP_DIR_SKILLS[@]} total)"
        return 1
    fi
    ok "All multi-file mattpocock skills downloaded (${#MP_DIR_SKILLS[@]} total)"
    return 0
}

# Helper: check ECC skills (entire skill directories from cloned repo)
check_ecc_skills() {
    local ECC_REPO="https://github.com/affaan-m/ECC.git"

    local ECC_SKILL_LIST=(
        "cpp-coding-standards" "cpp-testing"
        "python-patterns" "python-testing" "pytorch-patterns"
        "dart-flutter-patterns" "flutter-dart-code-review"
        "java-coding-standards"
        "kotlin-patterns" "kotlin-testing"
        "golang-patterns" "golang-testing"
        "rust-patterns" "rust-testing"
        "coding-standards" "api-design" "error-handling" "git-workflow" "accessibility"
        "security-scan"
        # --- Additional skills documented in SKILL.md §9 ---
        "swiftui-patterns" "swift-protocol-di-testing"
        "dotnet-patterns" "csharp-testing" "fsharp-testing"
        "fastapi-patterns" "nestjs-patterns" "nuxt4-patterns"
        "frontend-patterns" "docker-patterns" "deployment-patterns"
        "springboot-patterns" "springboot-security" "springboot-tdd" "springboot-verification"
        "postgres-patterns" "redis-patterns"
    )

    local need_download=false
    for skill in "${ECC_SKILL_LIST[@]}"; do
        if [ ! -f "${EXTERNAL_DIR}/ecc-${skill}/SKILL.md" ] || [ "$FORCE" = "true" ]; then
            need_download=true
            break
        fi
    done

    if ! $need_download; then
        ok "All ECC skills present (${#ECC_SKILL_LIST[@]} total)"
        # Ensure SOURCE.md exists for pre-existing skills (earlier setup runs may
        # not have created them)
        for skill in "${ECC_SKILL_LIST[@]}"; do
            local srcfile="${EXTERNAL_DIR}/ecc-${skill}/SOURCE.md"
            if [ ! -f "$srcfile" ]; then
                write_source_md "${EXTERNAL_DIR}/ecc-${skill}" "https://github.com/affaan-m/ECC/tree/main/skills/$skill"
            fi
        done
        return 0
    fi

    if [ "$MODE" = "--check-only" ]; then
        local count=0
        for skill in "${ECC_SKILL_LIST[@]}"; do
            if [ ! -f "${EXTERNAL_DIR}/ecc-${skill}/SKILL.md" ]; then
                fail "ecc-$skill (not found)"
                count=$((count + 1))
            fi
        done
        if [ "$count" -gt 0 ]; then
            info "$count/${#ECC_SKILL_LIST[@]} ECC skills missing"
            return 1
        fi
        return 0
    fi

    warn "Downloading ECC skills from GitHub..."
    local ECC_TMP
    ECC_TMP=$(mktemp -d -t ecc-skills.XXXXXX)
    register_cleanup "$ECC_TMP"

    if ! git_clone_with_retry "$ECC_REPO" "$ECC_TMP"; then
        fail "Failed to clone ECC repo after retries"
        return 1
    fi

    local ecc_ok=0 ecc_fail=0
    for skill in "${ECC_SKILL_LIST[@]}"; do
        local src="$ECC_TMP/skills/$skill"
        local dest="${EXTERNAL_DIR}/ecc-${skill}"
        if [ -d "$src" ]; then
            rm -rf "$dest" && cp -r "$src" "$dest"
            write_source_md "$dest" "https://github.com/affaan-m/ECC/tree/main/skills/$skill"
            ecc_ok=$((ecc_ok + 1))
        else
            fail "ecc-$skill (not found in ECC repo — may have been renamed or removed)"
            ecc_fail=$((ecc_fail + 1))
        fi
    done

    rm -rf "$ECC_TMP"
    if [ "$ecc_fail" -gt 0 ]; then
        info "$ecc_ok downloaded, $ecc_fail failed (out of ${#ECC_SKILL_LIST[@]} total)"
        return 1
    fi
    ok "All ECC skills downloaded (${#ECC_SKILL_LIST[@]} total)"
    return 0
}

# Helper: check ui-ux-pro-max skill (entire repo)
check_uipro_skill() {
    local dest="${EXTERNAL_DIR}/ui-ux-pro-max-skill"
    local repo="https://github.com/nextlevelbuilder/ui-ux-pro-max-skill.git"

    if [ -f "${dest}/SKILL.md" ] || [ -f "${dest}/.claude/skills/ui-ux-pro-max/SKILL.md" ]; then
        if [ "$FORCE" != "true" ]; then
            ok "ui-ux-pro-max-skill (found)"
            return 0
        fi
    fi

    if [ "$MODE" = "--check-only" ]; then
        fail "ui-ux-pro-max-skill (not found)"
        return 1
    fi

    warn "Downloading ui-ux-pro-max-skill entire repo..."
    local uipro_tmp
    uipro_tmp=$(mktemp -d -t uipro.XXXXXX)
    register_cleanup "$uipro_tmp"

    if git_clone_with_retry "$repo" "$uipro_tmp"; then
        rm -rf "$uipro_tmp/.git"
        rm -rf "$dest"
        mv "$uipro_tmp" "$dest"
        # Verify SKILL.md is reachable (repo structure may vary)
        if [ -f "${dest}/SKILL.md" ] || [ -f "${dest}/.claude/skills/ui-ux-pro-max/SKILL.md" ] || find "$dest" -name SKILL.md -maxdepth 3 | grep -q .; then
            write_source_md "$dest" "https://github.com/nextlevelbuilder/ui-ux-pro-max-skill"
            ok "ui-ux-pro-max-skill (cloned)"
        else
            fail "ui-ux-pro-max-skill (SKILL.md not found after clone — repo structure may have changed)"
            return 1
        fi
    else
        fail "ui-ux-pro-max-skill (clone failed after retries)"
        return 1
    fi
}

# ---------------------------------------------------------------------------
# 0. Check system prerequisites (git, curl)
# ---------------------------------------------------------------------------
check_system_tools() {
    echo ""
    echo "=== 0. Checking system tools ==="

    local missing=()

    if command -v git &>/dev/null; then
        ok "git: $(git --version 2>/dev/null | head -1)"
    else
        fail "git (not found — required for cloning external skill repos)"
        missing+=("git")
    fi

    if command -v curl &>/dev/null; then
        ok "curl: $(curl --version 2>/dev/null | head -1)"
    else
        fail "curl (not found — required for downloading individual skill files)"
        missing+=("curl")
    fi

    # Network connectivity check (only if we'll need to download)
    if [ "$MODE" != "--check-only" ] && [ ${#missing[@]} -eq 0 ]; then
        if ! curl -fsSL --connect-timeout 5 -o /dev/null https://github.com 2>/dev/null; then
            warn "Cannot reach github.com — network downloads may fail"
            info "If running offline, use --check-only to verify local state."
        else
            ok "Network: github.com reachable"
        fi
    fi

    if [ ${#missing[@]} -gt 0 ]; then
        # git and curl are critical — abort immediately
        local critical=()
        for tool in "${missing[@]}"; do
            case "$tool" in git|curl) critical+=("$tool") ;;
            esac
        done
        if [ ${#critical[@]} -gt 0 ]; then
            echo ""
            fail "Critical system tools missing: ${critical[*]}"
            info "Please install them first:"
            info "  macOS:  brew install ${critical[*]}"
            info "  Debian/Ubuntu: sudo apt install ${critical[*]}"
            info "  RHEL/Fedora: sudo dnf install ${critical[*]}"
            exit 1
        fi
        return 1
    fi
    return 0
}

# ---------------------------------------------------------------------------
# Cleanup: remove temp directories on exit/interrupt
# ---------------------------------------------------------------------------
# Declare BEFORE any function that uses it -- bash 3.2 requires explicit
# declaration prior to set -u array access, and `:-` fallback ensures
# compatibility with set -o nounset on empty arrays.
_CLEANUP_DIRS=()

register_cleanup() {
    _CLEANUP_DIRS+=("$1")
}

cleanup_temp_dirs() {
    if [ ${#_CLEANUP_DIRS[@]} -eq 0 ]; then
        return 0
    fi
    for dir in "${_CLEANUP_DIRS[@]}"; do
        [ -d "$dir" ] && rm -rf "$dir"
    done
}

trap cleanup_temp_dirs EXIT INT TERM

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
main() {
    echo ""
    echo "╔══════════════════════════════════════════════════╗"
    echo "║  spec-kit-coding — Dependency Setup              ║"
    echo "╚══════════════════════════════════════════════════╝"

    local exit_code=0

    check_system_tools || exit_code=1
    check_specify || exit_code=1
    check_speckit_skills || exit_code=1
    check_coding_guidance || exit_code=1
    check_external_skills || exit_code=1

    echo ""
    if [ $exit_code -eq 0 ]; then
        echo -e "${GREEN}╔══════════════════════════════════════╗${NC}"
        echo -e "${GREEN}║  All dependencies ready.            ║${NC}"
        echo -e "${GREEN}╚══════════════════════════════════════╝${NC}"
    else
        echo -e "${YELLOW}╔══════════════════════════════════════╗${NC}"
        echo -e "${YELLOW}║  Some dependencies are missing.     ║${NC}"
        echo -e "${YELLOW}║  Run without --check-only to fix.   ║${NC}"
        echo -e "${YELLOW}╚══════════════════════════════════════╝${NC}"
    fi

    exit $exit_code
}

main
