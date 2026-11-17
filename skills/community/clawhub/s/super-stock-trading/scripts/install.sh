#!/usr/bin/env bash
#=============================================================================
# install.sh — 超级股票交易 Skill 一键安装脚本
#-----------------------------------------------------------------------------
# 功能:
#   1. 检查前置环境(git / python3 / node / npx / clawhub)
#   2. 创建 Python 虚拟环境
#   3. 安装 16 个 GitHub 开源 Skill(git clone 到 ~/.claude/skills/)
#   4. 安装 Wind AIFin Market skills(npx skills add)
#   5. 安装 Python 依赖(akshare / tushare / pandas)
#   6. 配置 API Key(交互式或从 config.json 读取)
#   7. 安装验证 + 汇总报告
#
# 用法:
#   chmod +x install.sh
#   ./install.sh                # 交互式安装
#   ./install.sh --non-interactive   # 非交互(从 config.json 读取)
#   ./install.sh --skip-github       # 跳过 GitHub Skill 安装
#   ./install.sh --skip-wind         # 跳过 Wind Skill 安装
#
# 说明: 用户在需求中表述为"18 个 GitHub 开源 Skill",实际列出的 GitHub 仓库为 16 个
#       (另有 stock-watcher 走 ClawHub、guosen-securities 未开源走跳过),本脚本按
#       用户明确给出的 16 个 GitHub 仓库实现,加上 Wind AIFin Market Skills。
#=============================================================================
set -euo pipefail

# ----------------------------------------------------------------------------
# 配置区(可通过环境变量覆盖,或从 config.json 读取)
# ----------------------------------------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
CONFIG_FILE="${CONFIG_FILE:-$PROJECT_DIR/config.json}"

SKILLS_DIR="${SKILLS_DIR:-$HOME/.claude/skills}"
VENV_DIR="${VENV_DIR:-$HOME/.claude/stock-skills-venv}"
TMP_DIR="${TMP_DIR:-/tmp/stock-skills-install}"

# 运行参数
NON_INTERACTIVE=false
SKIP_GITHUB=false
SKIP_WIND=false

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# 计数器
TOTAL=0
SUCCESS=0
FAILED=0
SKIPPED=0

# 日志函数
log_info()  { echo -e "${BLUE}[INFO]${NC}  $1"; }
log_ok()    { echo -e "${GREEN}[OK]${NC}    $1"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC}  $1"; }
log_err()   { echo -e "${RED}[ERROR]${NC} $1"; }
log_step()  { echo -e "${CYAN}[STEP]${NC}  $1"; }

#=============================================================================
# 解析命令行参数
#=============================================================================
parse_args() {
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --non-interactive|-y)
        NON_INTERACTIVE=true
        shift
        ;;
      --skip-github)
        SKIP_GITHUB=true
        shift
        ;;
      --skip-wind)
        SKIP_WIND=true
        shift
        ;;
      --help|-h)
        sed -n '2,20p' "${BASH_SOURCE[0]}"
        exit 0
        ;;
      *)
        log_warn "未知参数: $1 (已忽略)"
        shift
        ;;
    esac
  done
}

#=============================================================================
# 从 config.json 读取配置项(依赖 python3)
# 用法: config_get "api_keys.tushare_token"
#=============================================================================
config_get() {
  local key="$1"
  local default="${2:-}"
  if [[ ! -f "$CONFIG_FILE" ]]; then
    echo "$default"
    return 0
  fi
  python3 - "$CONFIG_FILE" "$key" "$default" <<'PYEOF' 2>/dev/null || echo "$default"
import json, sys
cfg_path, key, default = sys.argv[1], sys.argv[2], sys.argv[3]
try:
    with open(cfg_path, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    node = cfg
    for part in key.split("."):
        if isinstance(node, dict) and part in node:
            node = node[part]
        else:
            node = None
            break
    val = "" if node is None else str(node)
    # 占位符检测: 含 YOUR_ 或 PLACEHOLDER 视为未配置,返回默认值
    if val and ("YOUR_" in val or "PLACEHOLDER" in val):
        val = ""
    print(val if val != "" else default)
except Exception:
    print(default)
PYEOF
}

#=============================================================================
# 16 个 GitHub 开源 Skill 定义表
# 格式: "目录名|GitHub URL|Python依赖文件|备注"
#=============================================================================
declare -a GITHUB_SKILLS=(
  "finance-quant-skills|https://github.com/lzwme/finance-quant-skills.git|requirements.txt|A股量化交易 akquant+akshare+backtrader"
  "stock-analysis-skill|https://github.com/tigersking520/stock-analysis-skill.git||专业个股投研 Skill"
  "openclaw-stock-data-skill|https://github.com/1018466411/openclaw-stock-data-skill.git|requirements.txt|A股股票信息和分钟级数据"
  "daily-stock-analysis-openclaw-skill|https://github.com/tel9980/daily-stock-analysis-openclaw-skill.git|requirements.txt|OpenClaw 股票智能分析 A股/港股/美股"
  "stock-analytics-skill|https://github.com/belos-street/stock-analytics-skill.git||24 个技能股市分析集 bun 运行"
  "a-stock-picker|https://github.com/tel9980/a-stock-picker.git||A股 AI 选股与资讯推送"
  "Stock-Analysis-Skill|https://github.com/liusai0820/Stock-Analysis-Skill.git||Claude 扮演专业股票分析师 akshare+yfinance"
  "short-term-stock-picker|https://github.com/online0001/short-term-stock-picker.git||短线强势股筛选工具"
  "stock-picker|https://github.com/tel9980/stock-picker.git|requirements.txt|周线爆发选股策略"
  "industry-analysis|https://github.com/0xsline/industry-analysis.git||麦肯锡框架行业分析"
  "daily_stock_analysis|https://github.com/ZhuLinsen/daily_stock_analysis.git|requirements.txt|AI 股票智能分析系统原版"
  "TradingAgents|https://github.com/hiowenluke/TradingAgents.git|requirements.txt|多 Agent LLM 金融交易框架"
  "FalconSignals|https://github.com/ironcladgeek/FalconSignals.git|pyproject.toml|AI 多 Agent 投资信号系统 5 个专业 Agent"
  "GeniusInStock|https://github.com/EveryFine/GeniusInStock.git|requirements.txt|全链条股票投资工具"
  "stock_trading|https://github.com/MilleXi/stock_trading.git|pyproject.toml|LSTM 预测 + 强化学习交易 AI"
  "quant-trading|https://github.com/amirzadeh20/quant-trading.git||均线交叉策略(无依赖文件)"
)

#=============================================================================
# 前置环境检查
#=============================================================================
check_prerequisites() {
  log_step "=== [1/7] 前置环境检查 ==="
  local missing=0

  # git(必需)
  if ! command -v git &>/dev/null; then
    log_err "未找到 git,请先安装: sudo apt install git / brew install git"
    missing=$((missing + 1))
  else
    log_ok "git: $(git --version 2>&1 | head -1)"
  fi

  # python3(必需)
  if ! command -v python3 &>/dev/null; then
    log_err "未找到 python3,请先安装: sudo apt install python3 python3-venv"
    missing=$((missing + 1))
  else
    log_ok "python3: $(python3 --version 2>&1)"
  fi

  # node(建议)
  if command -v node &>/dev/null; then
    log_ok "node: $(node --version 2>&1)"
  else
    log_warn "未找到 node,建议安装 Node.js v22+ 以使用 skills CLI 与 Wind Skill"
  fi

  # npx(建议)
  if command -v npx &>/dev/null; then
    log_ok "npx: $(npx --version 2>&1)"
  else
    log_warn "未找到 npx,Wind AIFin Market Skill 将跳过。安装: curl -fsSL https://fnm.vercel.app/install | bash"
  fi

  # clawhub(可选)
  if command -v clawhub &>/dev/null; then
    log_ok "clawhub: 已安装"
  else
    log_warn "未找到 clawhub CLI(可选)。安装: npm i -g clawhub"
  fi

  if [[ $missing -gt 0 ]]; then
    log_err "前置环境缺少必需组件($missing 个),请补齐后重试。"
    exit 1
  fi
  echo ""
}

#=============================================================================
# 创建 Python 虚拟环境
#=============================================================================
create_venv() {
  log_step "=== [2/7] 创建 Python 虚拟环境 ==="
  if [[ ! -d "$VENV_DIR" ]]; then
    python3 -m venv "$VENV_DIR"
    log_ok "虚拟环境已创建: $VENV_DIR"
  else
    log_info "虚拟环境已存在: $VENV_DIR"
  fi
  # shellcheck disable=SC1091
  source "$VENV_DIR/bin/activate" 2>/dev/null || true
  if command -v pip &>/dev/null; then
    pip install --upgrade pip -q
    log_ok "虚拟环境已激活且 pip 已就绪"
  fi
  echo ""
}

#=============================================================================
# 为缺少 SKILL.md 的仓库自动生成基础 SKILL.md
#=============================================================================
generate_skill_md() {
  local dest="$1"
  local name="$2"
  local note="$3"
  cat > "$dest/SKILL.md" << EOF
---
name: ${name}
description: ${note}。Use when the user asks for stock analysis, stock picking, or financial data analysis related to this skill's domain.
---

# ${name}

## Description
${note}

## When to use
当用户需要进行股票分析、选股、量化交易或金融数据处理时使用此 Skill。

## Instructions
1. 查看本目录下的 README.md 或主脚本文件了解具体功能
2. 按照仓库文档的说明运行相应脚本
3. 确保 Python 依赖已安装(见 requirements.txt 或 pyproject.toml)

## Source
原始仓库: 见 git remote origin
EOF
  log_ok "已自动生成 SKILL.md: $dest/SKILL.md"
}

#=============================================================================
# 安装单个 GitHub Skill
#=============================================================================
install_github_skill() {
  local entry="$1"
  IFS='|' read -r name url req_file note <<< "$entry"
  TOTAL=$((TOTAL + 1))

  echo ""
  log_step "[$TOTAL] 安装: $name"
  log_info "描述: $note"

  local dest="$SKILLS_DIR/$name"

  if [[ -d "$dest/.git" ]]; then
    log_info "目录已存在,尝试更新: $dest"
    if git -C "$dest" pull --ff-only 2>/dev/null; then
      log_ok "已更新: $name"
    else
      log_warn "更新失败,保留现有版本"
    fi
    SUCCESS=$((SUCCESS + 1))
  else
    if git clone --depth 1 "$url" "$dest" 2>/dev/null; then
      log_ok "克隆成功: $name → $dest"
      SUCCESS=$((SUCCESS + 1))
    else
      log_err "克隆失败: $name ($url)"
      FAILED=$((FAILED + 1))
      return 1
    fi
  fi

  # 安装 Python 依赖
  if [[ -n "$req_file" && -f "$dest/$req_file" ]]; then
    log_info "安装 Python 依赖: $req_file"
    if command -v pip &>/dev/null; then
      pip install -r "$dest/$req_file" -q 2>/dev/null && log_ok "依赖安装完成" || log_warn "部分依赖安装失败(可稍后手动处理)"
    else
      log_warn "pip 不可用,请手动安装: pip install -r $dest/$req_file"
    fi
  fi

  # 检查 SKILL.md
  if [[ -f "$dest/SKILL.md" || -f "$dest/skill.md" ]]; then
    log_ok "检测到 SKILL.md — 标准 Agent Skill 格式"
  else
    log_warn "未找到 SKILL.md,自动生成基础版本"
    generate_skill_md "$dest" "$name" "$note"
  fi
}

#=============================================================================
# 批量安装 GitHub Skill
#=============================================================================
install_github_skills() {
  if [[ "$SKIP_GITHUB" = true ]]; then
    log_warn "已通过 --skip-github 跳过 GitHub Skill 安装"
    echo ""
    return 0
  fi
  log_step "=== [3/7] 安装 $(echo "${#GITHUB_SKILLS[@]}") 个 GitHub 开源 Skill ==="
  log_info "目标目录: $SKILLS_DIR"
  mkdir -p "$SKILLS_DIR" "$TMP_DIR"

  for entry in "${GITHUB_SKILLS[@]}"; do
    install_github_skill "$entry" || true
  done
  echo ""
}

#=============================================================================
# 安装 Wind AIFin Market Skills(npx skills add)
#=============================================================================
install_wind_skills() {
  if [[ "$SKIP_WIND" = true ]]; then
    log_warn "已通过 --skip-wind 跳过 Wind AIFin Market Skill 安装"
    echo ""
    return 0
  fi
  log_step "=== [4/7] 安装 Wind AIFin Market Skills ==="
  log_info "Wind AIFin Market 提供 34 个金融数据 Skill(基于 MCP 协议)"
  log_info "GitHub 仓库: Wind-Information-Co-Ltd/wind-skills"

  if ! command -v npx &>/dev/null; then
    log_warn "npx 不可用,跳过 Wind Skill 安装。可稍后手动执行:"
    log_info "  npx skills add Wind-Information-Co-Ltd/wind-skills --skill wind-mcp-skill"
    echo ""
    return 0
  fi

  # 核心数据 Skill
  local wind_skills=(
    "wind-mcp-skill"
    "wind-find-finance-skill"
  )
  for skill in "${wind_skills[@]}"; do
    if npx skills add "Wind-Information-Co-Ltd/wind-skills" --skill "$skill" -y 2>/dev/null; then
      log_ok "$skill 安装成功"
      SUCCESS=$((SUCCESS + 1))
    else
      log_warn "$skill 安装失败(可稍后手动安装)"
      FAILED=$((FAILED + 1))
    fi
    TOTAL=$((TOTAL + 1))
  done

  log_info "请前往 https://aifinmarket.wind.com.cn 获取 API Key (ak_xxx)"
  log_info "配置方式: export WIND_API_KEY=ak_your_key_here 或写入 config.json"
  echo ""
}

#=============================================================================
# 安装核心 Python 依赖(akshare / tushare / pandas)
#=============================================================================
install_python_deps() {
  log_step "=== [5/7] 安装核心 Python 依赖 ==="
  if ! command -v pip &>/dev/null; then
    log_warn "pip 不可用,跳过 Python 依赖安装"
    echo ""
    return 0
  fi

  local deps=("akshare" "tushare" "pandas" "requests" "python-dotenv")
  log_info "安装: ${deps[*]}"
  if pip install "${deps[@]}" -q 2>/dev/null; then
    log_ok "核心 Python 依赖安装完成"
  else
    log_warn "部分依赖安装失败,尝试逐个安装..."
    for dep in "${deps[@]}"; do
      pip install "$dep" -q 2>/dev/null && log_ok "$dep 安装成功" || log_warn "$dep 安装失败"
    done
  fi
  echo ""
}

#=============================================================================
# 配置 API Key(交互式或从 config.json 读取)
#=============================================================================
configure_api_keys() {
  log_step "=== [6/7] 配置 API Key ==="

  # 从 config.json 读取已有值
  local cfg_wind cfg_tushare cfg_alpha
  cfg_wind="$(config_get 'api_keys.wind_api_key')"
  cfg_tushare="$(config_get 'api_keys.tushare_token')"
  cfg_alpha="$(config_get 'api_keys.alphavantage_api_key')"

  if [[ "$NON_INTERACTIVE" = true ]]; then
    log_info "非交互模式: 从 config.json / 环境变量读取 API Key"
    # 优先用 config.json,其次环境变量
    [[ -z "$cfg_wind" ]] && cfg_wind="${WIND_API_KEY:-}"
    [[ -z "$cfg_tushare" ]] && cfg_tushare="${TUSHARE_TOKEN:-}"
    [[ -z "$cfg_alpha" ]] && cfg_alpha="${ALPHAVANTAGE_API_KEY:-}"
  else
    # 交互式询问
    local input
    echo ""
    log_info "将交互式收集 API Key(直接回车则保留 config.json / 环境变量中的现有值)"
    read -r -p "  Wind AIFin Market API Key [${cfg_wind:+已配置}]: " input
    [[ -n "$input" ]] && cfg_wind="$input"
    read -r -p "  Tushare Token [${cfg_tushare:+已配置}]: " input
    [[ -n "$input" ]] && cfg_tushare="$input"
    read -r -p "  AlphaVantage API Key(FalconSignals 需要)[${cfg_alpha:+已配置}]: " input
    [[ -n "$input" ]] && cfg_alpha="$input"
  fi

  # 写回 config.json
  if [[ -f "$CONFIG_FILE" ]] && command -v python3 &>/dev/null; then
    python3 - "$CONFIG_FILE" "$cfg_wind" "$cfg_tushare" "$cfg_alpha" <<'PYEOF' 2>/dev/null && log_ok "API Key 已写入 config.json" || log_warn "config.json 写入失败(可手动编辑)"
import json, sys
cfg_path, wind, tushare, alpha = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
with open(cfg_path, "r", encoding="utf-8") as f:
    cfg = json.load(f)
cfg.setdefault("api_keys", {})
cfg["api_keys"]["wind_api_key"] = wind
cfg["api_keys"]["tushare_token"] = tushare
cfg["api_keys"]["alphavantage_api_key"] = alpha
with open(cfg_path, "w", encoding="utf-8") as f:
    json.dump(cfg, f, ensure_ascii=False, indent=2)
PYEOF
  fi

  # 同时导出到当前 shell 环境(便于后续脚本读取)
  export WIND_API_KEY="$cfg_wind"
  export TUSHARE_TOKEN="$cfg_tushare"
  export ALPHAVANTAGE_API_KEY="$cfg_alpha"

  # 提示如何持久化
  cat << EOF

  持久化 API Key(可选,写入 shell 配置):
    echo 'export WIND_API_KEY="$cfg_wind"'           >> ~/.bashrc
    echo 'export TUSHARE_TOKEN="$cfg_tushare"'       >> ~/.bashrc
    echo 'export ALPHAVANTAGE_API_KEY="$cfg_alpha"'  >> ~/.bashrc
EOF
  echo ""
}

#=============================================================================
# 安装验证
#=============================================================================
verify_installation() {
  log_step "=== [7/7] 安装验证 ==="
  local found=0

  if [[ "$SKIP_GITHUB" = false ]]; then
    for entry in "${GITHUB_SKILLS[@]}"; do
      IFS='|' read -r name _ _ _ <<< "$entry"
      if [[ -d "$SKILLS_DIR/$name" ]]; then
        local has_skill="否"
        [[ -f "$SKILLS_DIR/$name/SKILL.md" ]] && has_skill="是"
        [[ -f "$SKILLS_DIR/$name/skill.md" ]] && has_skill="是"
        printf "  ${GREEN}v${NC} %-40s SKILL.md: %s\n" "$name" "$has_skill"
        found=$((found + 1))
      fi
    done
  fi

  echo ""
  log_info "Skill 目录: $SKILLS_DIR"
  log_info "共找到 $found 个 GitHub Skill 目录"

  # Python 依赖验证
  if command -v python3 &>/dev/null; then
    echo ""
    log_info "Python 依赖检查:"
    for mod in akshare tushare pandas; do
      if python3 -c "import $mod" 2>/dev/null; then
        printf "  ${GREEN}v${NC} %-10s 已安装\n" "$mod"
      else
        printf "  ${RED}x${NC} %-10s 未安装\n" "$mod"
      fi
    done
  fi

  echo ""
  cat << 'EOF'
  验证方式:
  +-----------------------------------------------------------+
  | Claude Code:  在对话中问 "What Skills are available?"      |
  | TRAE IDE:     Settings > Skills & Commands 查看列表        |
  | OpenClaw:     clawhub list  或  重启会话后自动加载          |
  | 通用:         ls ~/.claude/skills/*/SKILL.md               |
  +-----------------------------------------------------------+
EOF
}

#=============================================================================
# 汇总报告
#=============================================================================
print_summary() {
  echo ""
  echo "============================================================"
  echo -e "${CYAN}              一键安装汇总报告${NC}"
  echo "============================================================"
  echo -e "  总计处理 Skill: $TOTAL"
  echo -e "  ${GREEN}成功安装:       $SUCCESS${NC}"
  echo -e "  ${RED}安装失败:       $FAILED${NC}"
  echo -e "  ${YELLOW}跳过:           $SKIPPED${NC}"
  echo "============================================================"
  echo ""
  echo "  下一步:"
  echo "  1. 检查各 Skill 目录下的 README.md 了解具体用法"
  echo "  2. 确认 API Key 已配置(config.json / 环境变量)"
  echo "     - Wind:    export WIND_API_KEY=ak_xxx  (https://aifinmarket.wind.com.cn)"
  echo "     - Tushare: export TUSHARE_TOKEN=xxx    (https://tushare.pro)"
  echo "     - AlphaVantage: export ALPHAVANTAGE_API_KEY=xxx"
  echo "  3. 运行日常 Pipeline:"
  echo "     python3 $SCRIPT_DIR/daily_pipeline.py --phase morning --stock 600519"
  echo "  4. 查阅全球财富报告:"
  echo "     open $SCRIPT_DIR/../references/wealth_reports/BCG_2026全球财富报告_中文版.html"
  echo ""
}

#=============================================================================
# 主流程
#=============================================================================
main() {
  parse_args "$@"

  echo ""
  echo "================================================================"
  echo -e "${CYAN}   超级股票交易 Skill — 一键安装${NC}"
  echo "================================================================"
  echo "  项目目录: $PROJECT_DIR"
  echo "  Skill 目录: $SKILLS_DIR"
  echo "  虚拟环境: $VENV_DIR"
  echo "  配置文件: $CONFIG_FILE"
  echo "  日期: $(date '+%Y-%m-%d %H:%M:%S')"
  echo "  交互模式: $([[ "$NON_INTERACTIVE" = true ]] && echo '否' || echo '是')"
  echo "================================================================"
  echo ""

  mkdir -p "$SKILLS_DIR" "$TMP_DIR"

  check_prerequisites
  create_venv
  install_github_skills
  install_wind_skills
  install_python_deps
  configure_api_keys
  verify_installation
  print_summary

  if [[ $FAILED -gt 0 ]]; then
    log_warn "存在 $FAILED 个失败项,请根据上方日志排查后重试。"
    exit 1
  fi
  log_ok "安装流程全部完成!"
}

main "$@"
