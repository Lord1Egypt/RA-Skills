#!/usr/bin/env bash
# yotta-code-quality 多智能体安装脚本（YottaSkills）
# 用法:
#   bash install.sh --agent <name>  # 按智能体默认用户级目录安装
#   bash install.sh --dir <path>    # 装到指定目录（用户改过目录的智能体）
#   bash install.sh -g              # 装到全部已知智能体用户级目录
#   bash install.sh                 # 检测并安装到已存在的项目级目录
#   bash install.sh --list          # 列出智能体 -> 默认目录
#   bash install.sh --dry-run       # 只显示将写入的目标，不写文件
#   bash install.sh --version       # 显示版本
#   bash install.sh --help          # 显示帮助
# 退出码: 0 成功 / 1 安装失败 / 2 用法错误 / 4 目标错误
set -euo pipefail

SKILL_NAME="yotta-code-quality"
SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
_IS_WINDOWS=0
case "$(uname -s)" in
  MINGW*|MSYS*)
    SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -W)"
    _IS_WINDOWS=1
    ;;
  CYGWIN*) _IS_WINDOWS=1 ;;
esac

# 智能体 -> 用户级默认目录（--agent 装到第一个）
# .agents/skills 并非通用目录：OpenCode / Cursor / Cline / Amp / Kimi / Gemini CLI / GitHub Copilot 读取。
dirs_for() {
  case "$1" in
    claude)     echo ".claude/skills" ;;
    cursor)     echo ".cursor/skills .agents/skills" ;;
    codex)      echo "__CODEX__" ;;
    gemini)     echo ".gemini/skills .agents/skills" ;;
    goose)      echo ".config/goose/skills .agents/skills" ;;
    amp)        echo ".config/agents/skills .agents/skills" ;;
    opencode)   echo "__OPENCODE__" ;;
    windsurf)   echo ".codeium/windsurf/skills" ;;
    workbuddy)  echo ".workbuddy/skills" ;;
    kiro)       echo ".kiro/skills" ;;
    trae)       echo ".traecli/skills" ;;
    trae-cn)    echo ".trae-cn/skills" ;;
    qwen)       echo ".qwen/skills" ;;
    comate)     echo ".comate/skills" ;;
    codebuddy)  echo ".codebuddy/skills" ;;
    kimi)       echo ".kimi/skills" ;;
    agents)     echo ".agents/skills" ;;
    *)          return 1 ;;
  esac
}

codex_dir() {
  if [ -n "${CODEX_HOME:-}" ]; then printf '%s' "$CODEX_HOME/skills"; else printf '%s' "$HOME/.codex/skills"; fi
}
opencode_dir() {
  if [ -n "${XDG_CONFIG_HOME:-}" ]; then printf '%s' "$XDG_CONFIG_HOME/opencode/skills"; else printf '%s' "$HOME/.config/opencode/skills"; fi
}
resolve_user() {
  case "$1" in
    __CODEX__)    codex_dir ;;
    __OPENCODE__) opencode_dir ;;
    *)            printf '%s' "$HOME/$1" ;;
  esac
}

skill_version() {
  local pkg="$SOURCE_DIR/package.json" v=""
  [ -f "$pkg" ] || return 0
  if command -v awk >/dev/null 2>&1; then
    v="$(awk -F'"' '{for (i=1;i<=NF;i++) if ($i=="version") {print $(i+2); exit}}' "$pkg" 2>/dev/null || true)"
  fi
  if [ -z "$v" ]; then
    v="$(sed -n 's/.*"version"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' "$pkg" 2>/dev/null | head -n 1 || true)"
  fi
  printf '%s' "$v"
}

usage() {
  echo "$SKILL_NAME 安装脚本（YottaSkills）"
  echo ""
  echo "用法:"
  echo "  bash install.sh --agent <name>   按智能体默认用户级目录安装（推荐）"
  echo "  bash install.sh --dir <path>     装到指定目录（用户改了目录的智能体）"
  echo "  bash install.sh -g               安装到全部已知智能体用户级目录"
  echo "  bash install.sh                  安装到检测到的项目级目录"
  echo ""
  echo "参数:"
  echo "  --agent <name>  智能体键名，见 --list"
  echo "  --dir <path>    自定义技能目录"
  echo "  -g, --global    安装到全部已知用户级目录"
  echo "  --list, -l      列出支持的智能体目录"
  echo "  --dry-run       只显示将写入的目标，不写文件"
  echo "  --version, -v   显示版本"
  echo "  --help, -h      显示帮助"
  echo "  --yes, -y       兼容参数（-g 不再强制要求）"
  echo ""
  echo "退出码: 0 成功 / 1 安装失败 / 2 用法错误 / 4 目标错误"
}

resolve_path() {
  # 与 SOURCE_DIR 同一风格（Windows Git Bash 用 pwd -W），供路径包含判断使用
  local p="$1"
  if [ "$_IS_WINDOWS" = "1" ]; then
    (cd "$p" 2>/dev/null && pwd -W)
  else
    (cd "$p" 2>/dev/null && pwd -P)
  fi
}

assert_safe_target() {
  local dest="$1" src_real dest_real parent
  src_real="$(resolve_path "$SOURCE_DIR")" || return 0
  if [ -d "$dest" ]; then
    dest_real="$(resolve_path "$dest")" || return 0
  else
    parent="$(dirname "$dest")"
    dest_real="$(resolve_path "$parent")" || return 0
    dest_real="$dest_real/$(basename "$dest")"
  fi
  case "$dest_real" in
    "$src_real"|"$src_real"/*)
      echo "安装失败：目标目录不能在技能源目录内（防止自装自毁）" >&2
      return 1
      ;;
  esac
  return 0
}

is_managed_hub_link() {
  local p="$1" real parent
  [ -L "$p" ] || return 1
  real="$(resolve_path "$p")" || return 1
  [ "$(basename "$real")" = "$SKILL_NAME" ] || return 1
  parent="$(dirname "$real")"
  [ -f "$parent/.yotta-hub.json" ] || [ -f "$parent/.yotta-links.json" ]
}

assert_no_nested_links() {
  local dest="$1"
  [ -d "$dest" ] || return 0
  if find "$dest" -mindepth 1 -type l -print -quit 2>/dev/null | grep -q .; then
    echo "安装失败：目标目录包含符号链接，拒绝写入：$dest" >&2
    return 1
  fi
  return 0
}

# 清理旧版安装残留（fail-closed 白名单）：仅在目标目录已存在且含 SKILL.md 时触发；
# 只删顶层开发项 + 任意层级缓存；不整目录删除、不跟随符号链接。
DEV_SKIP="package.json package-lock.json bin lib test .github .git .gitignore .npmignore .gitattributes .yotta .tmp install.sh node_modules"
clean_residue() {
  local dest="$1" name p
  [ -d "$dest" ] || return 0
  [ -f "$dest/SKILL.md" ] || return 0
  for name in $DEV_SKIP; do
    p="$dest/$name"
    [ -L "$p" ] && continue
    if [ -e "$p" ]; then
      rm -rf -- "$p"
      echo "已清理残留: $name"
    fi
  done
  find "$dest" -type d \( -name '__pycache__' -o -name '.pytest_cache' -o -name '.mypy_cache' \) -prune -exec rm -rf -- {} + 2>/dev/null || true
  find "$dest" -type f \( -name '*.pyc' -o -name '*.pyo' \) -delete 2>/dev/null || true
}

# 复制技能本体：顶层跳过开发件与运行时不相关目录（嵌套同名保留）；
# 任意层级跳过缓存（__pycache__ / .pytest_cache / .mypy_cache / *.pyc / *.pyo）。
copy_tree() {
  local src="$1" dst="$2" top="$3" entry base
  if [ "$top" != "1" ] && [ -L "$dst" ]; then
    echo "安装失败：目标目录包含符号链接，拒绝写入：$dst" >&2
    return 1
  fi
  mkdir -p "$dst" || return 1
  if [ "$top" != "1" ] && [ -L "$dst" ]; then
    echo "安装失败：目标目录包含符号链接，拒绝写入：$dst" >&2
    return 1
  fi
  for entry in "$src"/* "$src"/.[!.]* "$src"/..?*; do
    [ -e "$entry" ] || [ -L "$entry" ] || continue
    base="$(basename "$entry")"
    case "$base" in
      __pycache__|.pytest_cache|.mypy_cache) continue ;;
    esac
    if [ "$top" = "1" ]; then
      case " $DEV_SKIP " in
        *" $base "*) continue ;;
      esac
    fi
    if [ -d "$entry" ] && [ ! -L "$entry" ]; then
      if [ -L "$dst/$base" ]; then
        echo "安装失败：目标目录包含符号链接，拒绝写入：$dst/$base" >&2
        return 1
      fi
      copy_tree "$entry" "$dst/$base" 0 || return 1
    else
      case "$base" in
        *.pyc|*.pyo) continue ;;
      esac
      if [ -L "$dst/$base" ]; then
        echo "安装失败：目标文件是符号链接，拒绝写入：$dst/$base" >&2
        return 1
      fi
      cp -RP "$entry" "$dst/$base" || return 1
    fi
  done
}

install_to() {
  local base="$1" dry="$2" dest
  dest="$base/$SKILL_NAME"
  if [ -L "$base" ]; then
    echo "安装失败：目标目录是符号链接，拒绝跟随：$base" >&2
    return 1
  fi
  if [ -e "$base" ] && [ ! -d "$base" ]; then
    echo "安装失败：目标路径已存在且不是目录：$base" >&2
    return 1
  fi
  if [ -L "$dest" ] && ! is_managed_hub_link "$dest"; then
    echo "安装失败：技能目录是符号链接，拒绝跟随：$dest" >&2
    return 1
  fi
  if [ -e "$dest" ] && [ ! -d "$dest" ]; then
    echo "安装失败：技能路径已存在且不是目录：$dest" >&2
    return 1
  fi
  assert_safe_target "$dest" || return 1
  assert_no_nested_links "$dest" || return 1
  if [ "$dry" = "1" ]; then
    echo "[dry-run] 将安装到 -> $dest"
    return 0
  fi
  clean_residue "$dest"
  mkdir -p "$dest" || return 1
  if [ -L "$dest" ] && ! is_managed_hub_link "$dest"; then
    echo "安装失败：技能目录在安装期间变成了链接，拒绝写入：$dest" >&2
    return 1
  fi
  copy_tree "$SOURCE_DIR" "$dest" 1 || return 1
  if [ ! -f "$dest/SKILL.md" ]; then
    echo "安装失败：结果缺少 SKILL.md" >&2
    return 1
  fi
  echo "installed -> $dest"
}

list() {
  echo "智能体 -> 默认技能目录（--agent <name> 装到第一个，用户级）:"
  local a dirs first
  for a in claude cursor codex gemini goose amp opencode windsurf workbuddy kiro trae trae-cn qwen comate codebuddy kimi agents; do
    dirs="$(dirs_for "$a")"
    first="${dirs%% *}"
    case "$first" in
      __CODEX__)    first=".codex/skills" ;;
      __OPENCODE__) first=".config/opencode/skills" ;;
    esac
    if [ "$_IS_WINDOWS" = "1" ]; then
      first="%USERPROFILE%\\${first//\//\\}"
    else
      first="~/$first"
    fi
    printf '  %-10s %s\n' "$a" "$first"
  done
  echo '说明：Windows 用 %USERPROFILE%，Linux/macOS 用 ~；仅收录有官方默认目录的智能体。'
  echo '改了目录的请用 --dir <路径>，不要依赖默认位置；若设置了 CODEX_HOME / XDG_CONFIG_HOME，安装自动以该变量为准。'
}

main() {
  local agent="" dir="" global=0 show_list=0 show_help=0 show_version=0 dry=0
  while [ $# -gt 0 ]; do
    case "$1" in
      --help|-h) show_help=1 ;;
      --version|-v) show_version=1 ;;
      --list|-l) show_list=1 ;;
      -g|--global) global=1 ;;
      --dry-run) dry=1 ;;
      --yes|-y) : ;;
      --agent)
        shift
        if [ $# -eq 0 ] || [ -z "${1:-}" ]; then
          echo "用法错误: --agent 需要一个非空名称" >&2
          exit 2
        fi
        agent="$1"
        ;;
      --dir)
        shift
        if [ $# -eq 0 ] || [ -z "${1:-}" ]; then
          echo "用法错误: --dir 需要一个非空路径" >&2
          exit 2
        fi
        dir="$1"
        ;;
      *) echo "未知参数: $1" >&2; exit 2 ;;
    esac
    shift
  done

  if [ "$show_help" = "1" ]; then usage; return 0; fi
  if [ "$show_version" = "1" ]; then
    local v
    v="$(skill_version)"
    if [ -z "$v" ]; then
      echo "$SKILL_NAME 版本未知（未找到 package.json）" >&2
      exit 1
    fi
    echo "$SKILL_NAME v$v"
    return 0
  fi
  if [ "$show_list" = "1" ]; then list; return 0; fi

  local selected=0
  [ -n "$dir" ] && selected=$((selected + 1))
  [ -n "$agent" ] && selected=$((selected + 1))
  [ "$global" = "1" ] && selected=$((selected + 1))
  if [ "$selected" -gt 1 ]; then
    echo "用法错误: --dir / --agent / -g 只能选一个" >&2
    exit 2
  fi

  if [ -n "$dir" ]; then
    install_to "$dir" "$dry" || exit 1
    [ "$dry" = "1" ] || echo "完成。"
    return 0
  fi
  if [ -n "$agent" ]; then
    local dirs first
    if ! dirs="$(dirs_for "$agent")"; then
      echo "未收录智能体: $agent。可用 --list 查看，或 --dir <路径> 指定。" >&2
      exit 2
    fi
    first="${dirs%% *}"
    install_to "$(resolve_user "$first")" "$dry" || exit 1
    [ "$dry" = "1" ] || echo "完成。"
    return 0
  fi
  if [ "$global" = "1" ]; then
    local a dirs rel seen=" "
    for a in claude cursor codex gemini goose amp opencode windsurf workbuddy kiro trae trae-cn qwen comate codebuddy kimi agents; do
      dirs="$(dirs_for "$a")" || continue
      for rel in $dirs; do
        case "$seen" in
          *" $rel "*) continue ;;
        esac
        seen="$seen$rel "
        install_to "$(resolve_user "$rel")" "$dry" || exit 1
      done
    done
    [ "$dry" = "1" ] || echo "完成。"
    return 0
  fi
  local installed=0 d
  for d in .claude/skills .cursor/skills .codex/skills .config/goose/skills .config/agents/skills .opencode/skills .codeium/windsurf/skills .workbuddy/skills .kiro/skills .traecli/skills .gemini/skills .trae-cn/skills .qwen/skills .comate/skills .codebuddy/skills .kimi/skills .agents/skills; do
    if [ -d "$d" ]; then
      install_to "$d" "$dry" || exit 1
      installed=1
    fi
  done
  if [ "$installed" = "0" ]; then
    echo "目标错误: 未检测到项目级智能体目录。可用 --agent <name> 装到用户级，或用 --dir <路径> 指定目录。" >&2
    exit 4
  fi
  [ "$dry" = "1" ] || echo "完成。"
}

main "$@"
