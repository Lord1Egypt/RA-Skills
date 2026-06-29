#!/usr/bin/env bash
# workspace-git-setup/scripts/setup.sh
# 为任意工作区初始化 Git 版本追踪，预置通用安全 .gitignore 规则
# 幂等设计：可重复运行，已有配置不破坏
#
# 用法:
#   bash setup.sh [WORKSPACE_PATH] [PROJECT_NAME]   初始化/对齐配置
#   bash setup.sh --audit [WORKSPACE_PATH]          巡检模式（只读，不改动）
#   bash setup.sh --dry-run [WORKSPACE_PATH] [PROJECT_NAME]  预览将做的改动
#
# 工作区路径优先级：命令行参数 > 环境变量 WORKSPACE_DIR > 当前目录
# Git 身份优先级：环境变量 GIT_AUTHOR_NAME/EMAIL > 已有 git config > 手动输入

set -euo pipefail

# ─── 颜色 ────────────────────────────────────────────────────────────────────
GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; BLUE='\033[0;34m'; NC='\033[0m'
ok()   { echo -e "${GREEN}✅ $*${NC}"; }
warn() { echo -e "${YELLOW}⚠️  $*${NC}"; }
info() { echo -e "${BLUE}ℹ️  $*${NC}"; }
err()  { echo -e "${RED}❌ $*${NC}"; exit 1; }

# ─── 通用安全 .gitignore 规则（通用安全规则）────────────────
read -r -d '' DEFAULT_GITIGNORE <<'GITIGNORE_EOF' || true
# ── Workspace Git Ignore · 通用安全实践 ──────────────────────────────────────

# ── 敏感信息 / 凭证（安全核心，绝不可入 git）──────────────────────────────
.env
.env.*
*.pem
secrets/
.credentials/
*token*.json
*secret*.json
# TLS / SSH 私钥（仅排除 certs 目录下的 .key，避免误伤其它合法 .key 文件）
**/certs/*.key
id_rsa
id_dsa
id_ecdsa
id_ed25519
*.p12
*.keystore

# ── 临时文件 / 缓存 ────────────────────────────────────────────────────────
tmp/
*.tmp
*.cache
*.log
*.pid
.DS_Store
._*
._.DS_Store
Thumbs.db

# ── 编辑器 / IDE ──────────────────────────────────────────────────────────
.vscode/
.idea/
*.swp
*.swo
*~

# ── 依赖 ──────────────────────────────────────────────────────────────────
node_modules/
__pycache__/
*.pyc
*.pyo
.venv/
venv/
.pytest_cache/

# ── 构建 / 生成物目录 ─────────────────────────────────────────────────────
output/
dist/
build/
out/
*.egg-info/
GITIGNORE_EOF

# ─── 敏感文件检测模式（巡检用，匹配已 tracked 的危险文件）────────────────────
# 匹配已被 git 跟踪的危险文件（私钥 / 凭证 / token），用于 --audit 巡检
SENSITIVE_PATTERNS='(^|/)\.env($|\.)|\.pem$|(^|/)secrets/|token.*\.json$|secret.*\.json$|(^|/)certs/.*\.key$|(^|/)id_rsa$|(^|/)id_dsa$|(^|/)id_ecdsa$|(^|/)id_ed25519$|\.p12$|\.keystore$|(^|/)\.credentials/'

# ─── 大文件阈值（字节）：>10MB 提示 ───────────────────────────────────────────
BIG_FILE_BYTES=$((10 * 1024 * 1024))

# ─── 环境检测：git ────────────────────────────────────────────────────────────
if ! command -v git &>/dev/null; then
  err "未检测到 git，请参考官方文档安装后重试：https://git-scm.com/downloads"
fi

# ─── 参数解析（支持 --audit / --dry-run 标志，位置无关）──────────────────────
MODE="setup"           # setup | audit | dry-run
WORKSPACE_PATH=""
PROJECT_NAME=""
for arg in "$@"; do
  case "$arg" in
    --audit)   MODE="audit" ;;
    --dry-run) MODE="dry-run" ;;
    -h|--help)
      # 只打印文件头注释块（从第 2 行起，遇到第一个非 # 开头的行即停）
      awk 'NR==1{next} /^#/{sub(/^# ?/,""); print; next} {exit}' "$0"
      exit 0 ;;
    *)
      if [[ -z "$WORKSPACE_PATH" ]]; then WORKSPACE_PATH="$arg"
      elif [[ -z "$PROJECT_NAME" ]]; then PROJECT_NAME="$arg"
      fi ;;
  esac
done

info "git 已就绪：$(git --version)"

# ─── 1. 确定 workspace 路径 ───────────────────────────────────────────────────
# 优先级：命令行参数 > 环境变量 WORKSPACE_DIR > 当前目录
if [[ -z "$WORKSPACE_PATH" ]]; then
  if [[ -n "${WORKSPACE_DIR:-}" ]]; then
    WORKSPACE_PATH="$WORKSPACE_DIR"
    info "使用环境变量 WORKSPACE_DIR：$WORKSPACE_PATH"
  else
    WORKSPACE_PATH="$PWD"
    info "未指定路径，使用当前目录：$WORKSPACE_PATH"
  fi
fi
[[ -d "$WORKSPACE_PATH" ]] || err "路径不存在：$WORKSPACE_PATH"
# realpath 在 macOS BSD 默认不存在；缺失时降级用 cd+pwd 兜底
if command -v realpath &>/dev/null; then
  WORKSPACE_PATH="$(realpath "$WORKSPACE_PATH")"
else
  WORKSPACE_PATH="$(cd "$WORKSPACE_PATH" && pwd)"
fi

# ─── 2. 推断项目名称（默认用工作区目录名）────────────────────────────────────
if [[ -z "$PROJECT_NAME" ]]; then
  PROJECT_NAME="$(basename "$WORKSPACE_PATH")"
  [[ -z "$PROJECT_NAME" || "$PROJECT_NAME" == "/" ]] && PROJECT_NAME="(当前工作区)"
fi

# ════════════════════════════════════════════════════════════════════════════
# 巡检模式（只读，不改动任何文件 / git 状态）
# ════════════════════════════════════════════════════════════════════════════
if [[ "$MODE" == "audit" ]]; then
  echo ""
  echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
  echo -e "${BLUE}   Workspace Git 巡检（只读模式）${NC}"
  echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
  info "项目  : $PROJECT_NAME"
  info "路径   : $WORKSPACE_PATH"
  echo ""

  if [[ ! -d "$WORKSPACE_PATH/.git" ]]; then
    warn "该 workspace 尚未 git init，建议先运行：bash setup.sh"
    exit 0
  fi
  cd "$WORKSPACE_PATH"

  # A) 已 tracked 的敏感文件
  echo -e "${BLUE}[1/3] 敏感文件检测（已被 git 跟踪的危险文件）${NC}"
  SENSITIVE_HITS=$(git ls-files | grep -E "$SENSITIVE_PATTERNS" || true)
  if [[ -n "$SENSITIVE_HITS" ]]; then
    warn "发现 $(echo "$SENSITIVE_HITS" | wc -l | tr -d ' ') 个疑似敏感文件已进 git，存在泄露风险："
    echo "$SENSITIVE_HITS" | sed 's/^/    🔴 /' | head -40
    echo ""
    warn "建议人工核实后从版本管理中移除（本工具不自动改动）。"
  else
    ok "未发现已 tracked 的敏感文件"
  fi
  echo ""

  # B) 漏跟踪检测（未被 git 跟踪、也未被 ignore 的文件）
  echo -e "${BLUE}[2/3] 漏跟踪检测（磁盘有但 git 未跟踪）${NC}"
  TRACKED=$(git ls-files | wc -l | tr -d ' ')
  UNTRACKED=$(git status -s 2>/dev/null | grep -c '^??' || true)
  ok "  已跟踪文件：$TRACKED"
  if [[ "$UNTRACKED" -gt 0 ]]; then
    warn "  发现 $UNTRACKED 个未跟踪文件（未 add 且未被 .gitignore 排除）："
    git status -s 2>/dev/null | grep '^??' | sed 's/^?? /    ❔ /' | head -20
    [[ "$UNTRACKED" -gt 20 ]] && info "    ...（仅显示前 20 个，共 $UNTRACKED 个）"
    warn "  如确认应纳入版本管理，运行：git add <文件>；如应忽略，加进 .gitignore"
  else
    ok "  无未跟踪文件，工作区干净"
  fi
  echo ""

  # C) 关键配置检测
  echo -e "${BLUE}[3/3] 关键 git 配置检测${NC}"
  AC=$(git config --get core.autocrlf || echo '(未设置)')
  if [[ "$AC" == "input" || "$AC" == "false" ]]; then
    ok "  core.autocrlf=$AC（推荐值）"
  else
    warn "  core.autocrlf=$AC（建议设为 input，统一换行符避免 CRLF 假 diff）"
  fi
  [[ -f "$WORKSPACE_PATH/.gitignore" ]] && ok "  .gitignore 存在" || warn "  .gitignore 缺失"
  echo ""
  info "巡检完成（未对仓库做任何修改）。如需修复配置/规则，运行：bash setup.sh"
  exit 0
fi

# ════════════════════════════════════════════════════════════════════════════
# 初始化 / 对齐模式（setup & dry-run 共用主流程）
# ════════════════════════════════════════════════════════════════════════════
DRY=false
[[ "$MODE" == "dry-run" ]] && DRY=true

echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
if $DRY; then
  echo -e "${BLUE}   Workspace Git Setup — 预览模式（dry-run，不落地）${NC}"
else
  echo -e "${BLUE}   Workspace Git Setup — 通用安全实践版${NC}"
fi
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo ""
info "项目  : $PROJECT_NAME"
info "路径   : $WORKSPACE_PATH"
echo ""

# ─── 3. 读取 user.name / user.email ──────────────────────────────────────────
GIT_USER=""
GIT_EMAIL=""

# 优先：环境变量 GIT_AUTHOR_NAME / GIT_AUTHOR_EMAIL（git 原生约定，CI/CD 友好）
if [[ -n "${GIT_AUTHOR_EMAIL:-}" ]]; then
  GIT_EMAIL="$GIT_AUTHOR_EMAIL"
  info "从环境变量 GIT_AUTHOR_EMAIL 读取到邮箱：$GIT_EMAIL"
fi
if [[ -n "${GIT_AUTHOR_NAME:-}" ]]; then
  GIT_USER="$GIT_AUTHOR_NAME"
fi
# 邮箱有但用户名缺失时，用邮箱前缀兜底，避免静默落入交互
if [[ -n "$GIT_EMAIL" && -z "$GIT_USER" ]]; then
  GIT_USER="${GIT_EMAIL%@*}"
  info "未提供用户名，按邮箱前缀推断：$GIT_USER（可后续 git config 修改）"
fi

# 已有 git config 作为备用
if [[ -z "$GIT_EMAIL" ]]; then
  EXISTING_EMAIL=$(git -C "$WORKSPACE_PATH" config user.email 2>/dev/null || true)
  EXISTING_NAME=$(git -C "$WORKSPACE_PATH" config user.name 2>/dev/null || true)
  [[ -n "$EXISTING_EMAIL" ]] && GIT_EMAIL="$EXISTING_EMAIL"
  [[ -n "$EXISTING_NAME" ]] && GIT_USER="$EXISTING_NAME"
fi

# 手动输入兜底（dry-run 下若读不到则用占位，不交互）
if $DRY; then
  [[ -z "$GIT_USER" ]]  && GIT_USER="(将提示手动输入；非交互场景请预设 GIT_AUTHOR_NAME)"
  [[ -z "$GIT_EMAIL" ]] && GIT_EMAIL="(将提示手动输入；非交互场景请预设 GIT_AUTHOR_EMAIL)"
else
  if [[ -z "$GIT_USER" ]]; then
    read -rp "$(echo -e "${YELLOW}请输入 git user.name（示例：Jane Doe）: ${NC}")" GIT_USER
  fi
  if [[ -z "$GIT_EMAIL" ]]; then
    read -rp "$(echo -e "${YELLOW}请输入 git user.email（示例：jane@example.com）: ${NC}")" GIT_EMAIL
  fi
  [[ -z "$GIT_USER" ]]  && err "user.name 不能为空"
  [[ -z "$GIT_EMAIL" ]] && err "user.email 不能为空"
fi

# ─── 4. Git Init ──────────────────────────────────────────────────────────────
IS_NEW_REPO=false
if [[ ! -d "$WORKSPACE_PATH/.git" ]]; then
  if $DRY; then
    info "[dry-run] 将执行 git init（当前无仓库，默认分支 main）"
    IS_NEW_REPO=true
  else
    # 默认分支用 main（git 2.28+ 支持 -b；老版本回退后手动改名）
    if ! git -C "$WORKSPACE_PATH" init -q -b main 2>/dev/null; then
      git -C "$WORKSPACE_PATH" init -q
      git -C "$WORKSPACE_PATH" symbolic-ref HEAD refs/heads/main 2>/dev/null || true
    fi
    ok "git init 完成（默认分支 main）"
    IS_NEW_REPO=true
  fi
else
  info "已存在 git 仓库，跳过 init"
fi

if $DRY; then
  info "[dry-run] 将设置 user.name=$GIT_USER  user.email=$GIT_EMAIL  core.autocrlf=input"
else
  git -C "$WORKSPACE_PATH" config user.name  "$GIT_USER"
  git -C "$WORKSPACE_PATH" config user.email "$GIT_EMAIL"
  # 推荐 input：提交时转 LF、检出不转，统一换行符避免 CRLF 假 diff
  git -C "$WORKSPACE_PATH" config core.autocrlf input
  ok "git config：name=$GIT_USER  email=$GIT_EMAIL  core.autocrlf=input"
fi

# ─── 5. .gitignore ────────────────────────────────────────────────────────────
GITIGNORE_PATH="$WORKSPACE_PATH/.gitignore"

if [[ -f "$GITIGNORE_PATH" ]]; then
  DIFF=$(diff <(echo "$DEFAULT_GITIGNORE") "$GITIGNORE_PATH" || true)
  if [[ -z "$DIFF" ]]; then
    ok ".gitignore 已是最新，无需变更"
  else
    warn ".gitignore 已存在，与通用安全规则有差异："
    echo ""
    diff <(echo "$DEFAULT_GITIGNORE") "$GITIGNORE_PATH" || true
    echo ""
    if $DRY; then
      info "[dry-run] 将询问是否覆盖为通用安全规则（此处不落地）"
    else
      warn "提示：现有 .gitignore 可能含本 workspace 的个性化规则，覆盖会丢失。"
      read -rp "$(echo -e "${YELLOW}是否覆盖为通用安全规则？[y/N] ${NC}")" OVERWRITE
      if [[ "${OVERWRITE,,}" == "y" ]]; then
        echo "$DEFAULT_GITIGNORE" > "$GITIGNORE_PATH"
        ok ".gitignore 已覆盖为通用安全规则"
      else
        info "保留现有 .gitignore，未做修改"
      fi
    fi
  fi
else
  if $DRY; then
    info "[dry-run] 将写入通用安全规则 .gitignore"
  else
    echo "$DEFAULT_GITIGNORE" > "$GITIGNORE_PATH"
    ok ".gitignore 已写入（通用安全规则）"
  fi
fi

# ─── 6. 大文件扫描（首次 commit 前预警）───────────────────────────────────────
cd "$WORKSPACE_PATH"
info "扫描将被纳入跟踪的大文件（>10MB）..."
# 列出 git 会跟踪（未被 ignore）且 >10MB 的文件
BIG_FILES=$(git ls-files --others --cached --exclude-standard 2>/dev/null \
  | while IFS= read -r f; do
      [[ -f "$f" ]] || continue
      sz=$(stat -c%s "$f" 2>/dev/null || echo 0)
      if [[ "$sz" -gt "$BIG_FILE_BYTES" ]]; then
        printf '%s\t%s\n' "$(numfmt --to=iec "$sz" 2>/dev/null || echo "${sz}B")" "$f"
      fi
    done | sort -rh || true)

if [[ -n "$BIG_FILES" ]]; then
  warn "检测到以下大文件（>10MB），将被纳入 git，可能导致仓库膨胀："
  echo "$BIG_FILES" | sed 's/^/    📦 /' | head -20
  echo ""
  if $DRY; then
    info "[dry-run] 建议将其加入 .gitignore 或改走 CDN/Hub 重新拉取"
  else
    warn "如需排除，请先 Ctrl+C 退出，把它们加进 .gitignore 后重跑。"
    read -rp "$(echo -e "${YELLOW}仍要把这些大文件纳入 commit？[y/N] ${NC}")" BIGOK
    if [[ "${BIGOK,,}" != "y" ]]; then
      info "已中止首次 commit。请处理大文件后重新运行。"
      exit 0
    fi
  fi
else
  ok "未发现 >10MB 的待跟踪大文件"
fi

# ─── 7. 首次 Commit ───────────────────────────────────────────────────────────
if $DRY; then
  STAGED_PREVIEW=$(git add -A --dry-run 2>/dev/null | wc -l | tr -d ' ')
  info "[dry-run] git add -A 将影响约 $STAGED_PREVIEW 个文件（未真正暂存）"
  echo ""
  info "[dry-run] 预览结束，未对仓库做任何修改。去掉 --dry-run 即可正式执行。"
  exit 0
fi

git add -A 2>/dev/null || true
STAGED=$(git diff --cached --name-only 2>/dev/null | wc -l | tr -d ' ')

if [[ "$STAGED" -gt 0 ]]; then
  if $IS_NEW_REPO; then
    COMMIT_MSG="chore: init workspace git tracking (workspace-git-setup)"
  else
    COMMIT_MSG="chore: apply workspace-git-setup defaults"
  fi
  git commit -q -m "$COMMIT_MSG" 2>/dev/null || true
  COMMIT_HASH=$(git rev-parse --short HEAD 2>/dev/null || echo "n/a")
  ok "已提交 $STAGED 个文件  [$COMMIT_HASH] $COMMIT_MSG"
else
  info "无新变更需要提交"
fi

# ─── 8. 汇总 ─────────────────────────────────────────────────────────────────
echo ""
echo -e "${GREEN}═══════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}   ✅ 设置完成${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════${NC}"
echo ""
echo -e "  项目     : ${BLUE}$PROJECT_NAME${NC}"
echo -e "  工作区   : ${BLUE}$WORKSPACE_PATH${NC}"
echo -e "  Git user : ${BLUE}$GIT_USER <$GIT_EMAIL>${NC}"
echo -e "  分支     : ${BLUE}$(git -C "$WORKSPACE_PATH" branch --show-current 2>/dev/null || echo 'main')${NC}"
echo ""
info "已为 [$PROJECT_NAME] 配置 Git 追踪。"
info "巡检漏跟踪 / 敏感文件：${YELLOW}bash setup.sh --audit${NC}"
info "为其它工作区配置：${YELLOW}bash setup.sh /path/to/other-workspace \"ProjectName\"${NC}"
echo ""
info "提示：当前为纯本地 Git，无远程仓库。如需备份，可配置 remote："
echo -e "  ${YELLOW}git remote add origin <your-repo-url>${NC}"
echo ""
