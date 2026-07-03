#!/usr/bin/env bash
################################################################################
# yyqdata skill — 自动更新脚本
#
# 用法：
#   bash update.sh                  # 默认：检查 + 提示 + 自动安装（如果有新版）
#   bash update.sh --check          # 只检查，不安装（exit 0=最新 / 10=有新版 / 非零=错误）
#   bash update.sh --apply          # 强制重装（不论版本）
#   bash update.sh --dry-run        # 打印将要做的事但不真改文件
#   bash update.sh --install-dir DIR # 指定 skill 安装父目录（默认自动探测）
#
# 环境变量：
#   SKILL_UPDATE_URL       zip 下载 URL，默认 https://static.yyqyx.com/skill/yyqdata-stock-skill.zip
#   SKILL_MANIFEST_URL     manifest URL，默认 https://static.yyqyx.com/skill/yyqdata.manifest.json
#   SKILL_INSTALL_DIR      skill 安装父目录（最终路径 = $SKILL_INSTALL_DIR/yyqdata）
#                          默认自动探测：~/.openclaw/skills/ → ~/.hermes/skills/ →
#                                       ~/.claude/skills/  → ./
#
# 退出码：
#   0   一切正常（最新 / 已更新）
#   10  --check 模式下发现可更新
#   1   网络错误 / manifest 解析失败
#   2   sha256 校验失败
#   3   安装目录不可写
#   4   缺依赖（curl / unzip）
################################################################################

set -euo pipefail

DEFAULT_MANIFEST_URL="https://static.yyqyx.com/skill/yyqdata.manifest.json"
DEFAULT_ZIP_URL="https://static.yyqyx.com/skill/yyqdata-stock-skill.zip"

MANIFEST_URL="${SKILL_MANIFEST_URL:-$DEFAULT_MANIFEST_URL}"
ZIP_URL="${SKILL_UPDATE_URL:-$DEFAULT_ZIP_URL}"
INSTALL_DIR="${SKILL_INSTALL_DIR:-}"

MODE="auto"          # auto | check | apply
DRY_RUN="false"

# ── 解析参数 ─────────────────────────────────────────────────────────────────
while [[ $# -gt 0 ]]; do
    case "$1" in
        --check)         MODE="check";   shift ;;
        --apply)         MODE="apply";   shift ;;
        --dry-run)       DRY_RUN="true"; shift ;;
        --install-dir)   INSTALL_DIR="$2"; shift 2 ;;
        --manifest-url)  MANIFEST_URL="$2"; shift 2 ;;
        --zip-url)       ZIP_URL="$2"; shift 2 ;;
        -h|--help)
            sed -n '/^# 用法/,/^####/p' "$0" | head -25
            exit 0
            ;;
        *) echo "[ERR] 未知参数：$1" >&2; exit 1 ;;
    esac
done

# ── 颜色 ────────────────────────────────────────────────────────────────────
if [[ -t 1 ]]; then
    RED=$'\033[0;31m'; GREEN=$'\033[0;32m'; YELLOW=$'\033[1;33m'; BLUE=$'\033[0;34m'; NC=$'\033[0m'
else
    RED=''; GREEN=''; YELLOW=''; BLUE=''; NC=''
fi
info()  { echo "${GREEN}[INFO]${NC}  $*"; }
warn()  { echo "${YELLOW}[WARN]${NC}  $*" >&2; }
error() { echo "${RED}[ERROR]${NC} $*" >&2; exit "${2:-1}"; }
step()  { echo "${BLUE}$*${NC}"; }

# ── 依赖检查 ────────────────────────────────────────────────────────────────
command -v curl  >/dev/null 2>&1 || error "需要 curl 命令" 4
command -v unzip >/dev/null 2>&1 || error "需要 unzip 命令" 4

# ── 探测安装目录（按优先级试 4 个候选） ────────────────────────────────────
auto_detect_install_dir() {
    local cands=(
        "$HOME/.openclaw/skills"
        "$HOME/.hermes/skills"
        "$HOME/.claude/skills"
        "$HOME/.config/skills"
    )
    # 已存在 yyqdata 子目录的优先
    for d in "${cands[@]}"; do
        if [[ -d "$d/yyqdata" ]]; then
            echo "$d"; return 0
        fi
    done
    # 否则用第一个存在的父目录
    for d in "${cands[@]}"; do
        if [[ -d "$d" ]]; then
            echo "$d"; return 0
        fi
    done
    # 都不存在 → 返回脚本所在目录的上一级
    local self_dir
    self_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    # 如果脚本本身就在 yyqdata/ 里，往上一级算父目录
    if [[ "$(basename "$self_dir")" == "yyqdata" ]]; then
        echo "$(dirname "$self_dir")"
    else
        echo "$self_dir"
    fi
}

[[ -n "$INSTALL_DIR" ]] || INSTALL_DIR="$(auto_detect_install_dir)"
SKILL_DIR="$INSTALL_DIR/yyqdata"

# ── 读 manifest ──────────────────────────────────────────────────────────────
fetch_manifest() {
    local tmp
    tmp=$(mktemp)
    if ! curl -fsSL --max-time 10 "$MANIFEST_URL" -o "$tmp"; then
        rm -f "$tmp"
        error "拉 manifest 失败：$MANIFEST_URL（网络 / 服务不可达）" 1
    fi
    echo "$tmp"
}

# 极简 JSON 字段提取（不依赖 jq；只支持顶层 string / number）
json_get() {
    local key="$1"
    local file="$2"
    # 匹配 "key":"value" 或 "key":number；允许任意空白
    grep -oE "\"$key\"[[:space:]]*:[[:space:]]*(\"[^\"]*\"|[0-9]+)" "$file" \
        | head -1 \
        | sed -E 's/^"[^"]+"[[:space:]]*:[[:space:]]*"?//; s/"$//'
}

# 读本地 SKILL.md 的 version（frontmatter）
local_version() {
    local skill_md="$SKILL_DIR/SKILL.md"
    if [[ ! -f "$skill_md" ]]; then
        echo "0.0.0"
        return 0
    fi
    grep -m1 '^version:' "$skill_md" | sed -E 's/^version:[[:space:]]*//; s/["'"'"']//g' | head -1
}

# ── 安装 zip ─────────────────────────────────────────────────────────────────
download_and_install() {
    local expected_sha256="$1"
    local tmpdir
    tmpdir=$(mktemp -d)
    local zip_path="$tmpdir/skill.zip"

    info "下载：$ZIP_URL"
    if [[ "$DRY_RUN" == "true" ]]; then
        info "[DRY] 跳过下载 / 校验 / 解压"
        rm -rf "$tmpdir"
        return 0
    fi
    curl -fsSL --max-time 60 "$ZIP_URL" -o "$zip_path" \
        || { rm -rf "$tmpdir"; error "下载失败：$ZIP_URL" 1; }

    # sha256 校验
    if [[ -n "$expected_sha256" && "$expected_sha256" != "null" ]]; then
        local actual_sha256
        if command -v sha256sum >/dev/null 2>&1; then
            actual_sha256=$(sha256sum "$zip_path" | awk '{print $1}')
        elif command -v shasum >/dev/null 2>&1; then
            actual_sha256=$(shasum -a 256 "$zip_path" | awk '{print $1}')
        else
            warn "无 sha256sum / shasum 命令，跳过校验"
            actual_sha256=""
        fi
        if [[ -n "$actual_sha256" && "$actual_sha256" != "$expected_sha256" ]]; then
            rm -rf "$tmpdir"
            error "sha256 不匹配：期望 $expected_sha256 实际 $actual_sha256（可能 zip 损坏 / 中间人篡改）" 2
        fi
        [[ -n "$actual_sha256" ]] && info "✓ sha256 校验通过"
    fi

    # 目标父目录可写
    mkdir -p "$INSTALL_DIR" || error "安装目录不可写：$INSTALL_DIR" 3
    [[ -w "$INSTALL_DIR" ]] || error "安装目录不可写：$INSTALL_DIR（chmod +w 或换路径）" 3

    # 备份旧的（如果存在）
    if [[ -d "$SKILL_DIR" ]]; then
        local bak="${SKILL_DIR}.bak-$(date +%Y%m%d%H%M%S)"
        info "备份旧版：$SKILL_DIR → $bak"
        mv "$SKILL_DIR" "$bak"
    fi

    info "解压到：$INSTALL_DIR/"
    unzip -oq "$zip_path" -d "$INSTALL_DIR/" \
        || { rm -rf "$tmpdir"; error "解压失败（zip 格式可能损坏）" 1; }

    rm -rf "$tmpdir"
    info "✓ 安装完成：$SKILL_DIR"
}

# ── main ────────────────────────────────────────────────────────────────────
main() {
    step "yyqdata skill 自动更新"
    info "manifest URL：$MANIFEST_URL"
    info "zip URL：     $ZIP_URL"
    info "安装目录：    $INSTALL_DIR （目标：$SKILL_DIR）"
    info "模式：        $MODE （dry-run=$DRY_RUN）"
    echo

    # --apply：强制重装
    if [[ "$MODE" == "apply" ]]; then
        local manifest
        manifest=$(fetch_manifest)
        local remote_sha256 remote_version
        remote_sha256=$(json_get "sha256" "$manifest")
        remote_version=$(json_get "version" "$manifest")
        rm -f "$manifest"
        info "强制安装远端 v${remote_version}"
        download_and_install "$remote_sha256"
        return 0
    fi

    # check / auto：先比对版本
    local manifest local_v remote_v remote_sha
    manifest=$(fetch_manifest)
    remote_v=$(json_get "version" "$manifest")
    remote_sha=$(json_get "sha256" "$manifest")
    local_v=$(local_version)
    info "本地版本：$local_v"
    info "远端版本：$remote_v"

    # 版本比较：字面值不同就算 stale（不做语义比较，避免误判）
    if [[ "$local_v" == "$remote_v" ]]; then
        info "${GREEN}✓ 已是最新版${NC}"
        rm -f "$manifest"
        return 0
    fi

    # 显示 changelog
    local changelog
    changelog=$(json_get "changelog_summary" "$manifest")
    if [[ -n "$changelog" ]]; then
        echo
        info "更新说明：$changelog"
        echo
    fi

    if [[ "$MODE" == "check" ]]; then
        warn "有可用更新：$local_v → $remote_v（用 bash update.sh --apply 升级）"
        rm -f "$manifest"
        exit 10
    fi

    # auto 模式：直接装
    download_and_install "$remote_sha"
    rm -f "$manifest"
}

main
