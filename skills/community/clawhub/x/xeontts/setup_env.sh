#!/usr/bin/env bash
set -euo pipefail

export HF_ENDPOINT=https://hf-mirror.com
export HF_HUB_ENABLE_HF_TRANSFER=0

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }
log_step() { echo -e "${BLUE}[STEP]${NC} $1"; }

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SKILL_DIR"

BASE_MODEL_PATH="${BASE_MODEL_PATH:-~/model/Qwen3-TTS-12Hz-0.6B-Base-OpenVINO-INT8}"
CUSTOM_MODEL_PATH="${CUSTOM_MODEL_PATH:-~/model/Qwen3-TTS-12Hz-0.6B-CustomVoice-OpenVINO-INT8}"
BASE_CHECKPOINT_PATH="${BASE_CHECKPOINT_PATH:-}"
BASE_MODEL_REPO="${BASE_MODEL_REPO:-aurora2035/Qwen3-TTS-12Hz-0.6B-Base-OpenVINO-INT8}"
CUSTOM_MODEL_REPO="${CUSTOM_MODEL_REPO:-aurora2035/Qwen3-TTS-12Hz-0.6B-CustomVoice-OpenVINO-INT8}"
BASE_CHECKPOINT_REPO="${BASE_CHECKPOINT_REPO:-}"
TTS_PIP_SPEC="${XDP_TTS_PIP_SPEC:-xdp-tts-service}"
FORCE=0
SKIP_DEPS=0

usage() {
  cat <<EOF
用法: $0 [--force] [--skip-deps]

环境变量覆盖：
  XDP_TTS_PIP_SPEC       Python 包安装源，默认 xdp-tts-service
  BASE_MODEL_PATH        Base OV 模型目录
  CUSTOM_MODEL_PATH      Custom OV 模型目录
  BASE_CHECKPOINT_PATH   可选：Base 原始 checkpoint 目录（旧导出兼容）
  BASE_MODEL_REPO        Base OV 模型 HF 仓库名
  CUSTOM_MODEL_REPO      Custom OV 模型 HF 仓库名
  BASE_CHECKPOINT_REPO   可选：Base checkpoint HF 仓库名（旧导出兼容）
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --force) FORCE=1; shift ;;
    --skip-deps) SKIP_DEPS=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) log_error "未知参数: $1"; usage; exit 1 ;;
  esac
done

expand_path() {
  local value="$1"
  if [[ "$value" == ~* ]]; then
    value="${value/#\~/$HOME}"
  fi
  printf '%s\n' "$value"
}

detect_os() {
  if [[ -f /etc/os-release ]]; then
    . /etc/os-release
    printf '%s\n' "$ID"
    return 0
  fi
  printf '%s\n' unknown
}

check_sudo() {
  if [[ "$EUID" -eq 0 ]]; then
    SUDO=""
  elif command -v sudo >/dev/null 2>&1; then
    SUDO="sudo"
  else
    SUDO=""
  fi
}

install_system_deps() {
  [[ "$SKIP_DEPS" -eq 1 ]] && return 0
  check_sudo
  local os_id
  os_id="$(detect_os)"
  case "$os_id" in
    ubuntu|debian)
      log_step "安装系统依赖 (Debian/Ubuntu)"
      $SUDO apt-get update -qq >/dev/null 2>&1 || true
      $SUDO apt-get install -y wget curl git lsof net-tools unzip bzip2 ca-certificates ffmpeg >/dev/null 2>&1 || \
        $SUDO apt-get install -y wget curl git lsof net-tools unzip bzip2 ca-certificates ffmpeg
      ;;
    centos|rhel|fedora|rocky|almalinux|ol|alibabacloud|alios)
      log_step "安装系统依赖 (RHEL/CentOS)"
      local pkg_mgr="yum"
      command -v dnf >/dev/null 2>&1 && pkg_mgr="dnf"
      $SUDO "$pkg_mgr" install -y wget curl git lsof net-tools unzip bzip2 ca-certificates ffmpeg which >/dev/null 2>&1 || \
        $SUDO "$pkg_mgr" install -y wget curl git lsof net-tools unzip bzip2 ca-certificates ffmpeg which
      ;;
    *)
      log_warn "未知系统，跳过系统依赖自动安装"
      ;;
  esac
}

setup_miniconda() {
  log_step "准备 Miniconda Python 3.10"
  local conda_dir="$HOME/miniconda3"
  local conda_url="https://repo.anaconda.com/miniconda/Miniconda3-py310_23.11.0-2-Linux-x86_64.sh"
  if [[ "$FORCE" -eq 1 && -d "$conda_dir" ]]; then
    rm -rf "$conda_dir"
  fi
  if [[ ! -d "$conda_dir" ]]; then
    wget --timeout=120 -q "$conda_url" -O /tmp/miniconda.sh || curl -fsSL --connect-timeout 120 "$conda_url" -o /tmp/miniconda.sh
    bash /tmp/miniconda.sh -b -p "$conda_dir" >/dev/null 2>&1
    rm -f /tmp/miniconda.sh
  fi
  PYTHON_CMD="$conda_dir/bin/python"
  [[ -x "$PYTHON_CMD" ]] || { log_error "Miniconda 安装失败"; exit 1; }
  log_info "Python 就绪: $($PYTHON_CMD --version 2>&1)"
}

setup_venv() {
  if [[ "$FORCE" -eq 1 && -d venv ]]; then
    rm -rf venv
  fi
  if [[ ! -d venv ]]; then
    log_step "创建虚拟环境"
    "$PYTHON_CMD" -m venv venv
  fi
  source venv/bin/activate
  pip install -q --upgrade pip
}

install_python_packages() {
  log_step "安装 Python TTS 服务包"
  if ! pip install -q --upgrade "$TTS_PIP_SPEC"; then
    log_error "安装失败: $TTS_PIP_SPEC"
    log_error "如果包尚未发布，请设置 XDP_TTS_PIP_SPEC=/path/to/xdp_tts_service.whl 后重试"
    exit 1
  fi
  log_info "已安装: $TTS_PIP_SPEC"
}

verify_python_runtime() {
  log_step "校验 Python TTS 运行时"
  [[ -x venv/bin/xdp-tts-service ]] || {
    log_error "安装后仍未生成 venv/bin/xdp-tts-service"
    log_error "请检查 XDP_TTS_PIP_SPEC 是否指向包含 console entry point 的有效包"
    exit 1
  }

  venv/bin/python <<'PYEOF'
import importlib.util
import sys

required = [
    'xdp_tts_service',
    'qwen_tts',
]
missing = []
for name in required:
    if importlib.util.find_spec(name) is None:
        missing.append(name)

if missing:
    print('missing python modules:', ', '.join(missing), file=sys.stderr)
    sys.exit(1)
PYEOF
}

copy_node_config() {
  if [[ -f config.json && "$FORCE" -ne 1 ]]; then
    log_info "config.json 已存在，跳过"
    return 0
  fi
  cp config.example.json config.json
  log_info "已生成 config.json"
}

generate_tts_config() {
  if [[ -f tts_config.json && "$FORCE" -ne 1 ]]; then
    log_info "tts_config.json 已存在，跳过"
    return 0
  fi
  if [[ -x venv/bin/xdp-tts-init-config ]]; then
    venv/bin/xdp-tts-init-config --output ./tts_config.json >/dev/null
  else
    cp tts_config.example.json tts_config.json
  fi
  log_info "已生成 tts_config.json"
}

resolve_hf_cli() {
  export PATH="$HOME/miniconda3/bin:$HOME/.local/bin:$PATH"
  if command -v hf >/dev/null 2>&1; then
    printf '%s\n' "$(command -v hf)"
    return 0
  fi
  if command -v huggingface-cli >/dev/null 2>&1; then
    printf '%s\n' "$(command -v huggingface-cli)"
    return 0
  fi
  if pip install -q 'huggingface_hub[cli]' >/dev/null 2>&1 || pip install -q huggingface_hub >/dev/null 2>&1; then
    export PATH="$HOME/miniconda3/bin:$HOME/.local/bin:$PATH"
    if command -v hf >/dev/null 2>&1; then
      printf '%s\n' "$(command -v hf)"
      return 0
    fi
    if command -v huggingface-cli >/dev/null 2>&1; then
      printf '%s\n' "$(command -v huggingface-cli)"
      return 0
    fi
  fi
  return 1
}

download_model_if_missing() {
  local repo_id="$1"
  local target_path
  [[ -n "$repo_id" ]] || return 0
  [[ -n "${2:-}" ]] || return 0
  target_path="$(expand_path "$2")"
  if [[ -d "$target_path" ]] && [[ -n "$(ls -A "$target_path" 2>/dev/null || true)" ]]; then
    log_info "模型目录已存在: $target_path"
    return 0
  fi
  local hf_cli
  if ! hf_cli="$(resolve_hf_cli)"; then
    log_warn "未找到 Hugging Face CLI，跳过自动下载: $repo_id"
    return 0
  fi
  mkdir -p "$target_path"
  log_step "尝试下载模型: $repo_id -> $target_path"
  if [[ "$(basename "$hf_cli")" == "hf" ]]; then
    "$hf_cli" download "$repo_id" --local-dir "$target_path" || log_warn "下载失败，请后续手工补齐: $repo_id"
  else
    "$hf_cli" download "$repo_id" --local-dir "$target_path" --local-dir-use-symlinks False || log_warn "下载失败，请后续手工补齐: $repo_id"
  fi
}

update_tts_model_paths() {
  local base_model_abs custom_model_abs base_ckpt_abs
  base_model_abs="$(expand_path "$BASE_MODEL_PATH")"
  custom_model_abs="$(expand_path "$CUSTOM_MODEL_PATH")"
  base_ckpt_abs=""
  if [[ -n "$BASE_CHECKPOINT_PATH" ]]; then
    base_ckpt_abs="$(expand_path "$BASE_CHECKPOINT_PATH")"
  fi

  log_step "写入 TTS 模型路径到 tts_config.json"
  venv/bin/python <<PYEOF
import json
from pathlib import Path

config_path = Path("tts_config.json")
config = json.loads(config_path.read_text(encoding="utf-8"))

legacy_base = config.pop("qwen3_tts_base", None) or {}
legacy_custom = config.pop("qwen3_tts_custom", None) or {}

base_cfg = config.setdefault("qwen3_tts_0.6b_base_openvino", {})
custom_cfg = config.setdefault("qwen3_tts_0.6b_custom_openvino", {})

if legacy_base and not base_cfg.get("model_dir"):
  base_cfg["model_dir"] = legacy_base.get("model") or legacy_base.get("model_dir") or ""
if legacy_custom and not custom_cfg.get("model_dir"):
  custom_cfg["model_dir"] = legacy_custom.get("model") or legacy_custom.get("model_dir") or ""

base_cfg["model_dir"] = r"$base_model_abs"
base_cfg.setdefault("label", "Qwen3-TTS-0.6B-Base(OpenVINO)")
base_cfg.setdefault("model_type", "Qwen3_TTS_OpenVINO")
base_cfg.setdefault("tts_model_type", "voice_clone")
base_cfg.setdefault("force_cpu", False)
base_cfg.setdefault("default_mode", "voice_clone_xvector")
base_cfg.setdefault("modes", ["voice_clone", "voice_clone_xvector"])
base_cfg.setdefault("device", "CPU")
base_cfg.setdefault("default_language", "Chinese")
base_cfg.setdefault("prompt_text", "")
base_cfg.setdefault("prompt_audio", "")

custom_cfg["model_dir"] = r"$custom_model_abs"
custom_cfg.setdefault("label", "Qwen3-TTS-0.6B-CustomVoice(OpenVINO)")
custom_cfg.setdefault("model_type", "Qwen3_TTS_OpenVINO")
custom_cfg.setdefault("tts_model_type", "custom_voice")
custom_cfg.setdefault("force_cpu", False)
custom_cfg.setdefault("default_mode", "custom_voice")
custom_cfg.setdefault("modes", ["custom_voice"])
custom_cfg.setdefault("device", "CPU")
custom_cfg.setdefault("default_language", "Chinese")
custom_cfg.setdefault("default_speaker", "Vivian")
custom_cfg.setdefault("speakers", ["Vivian", "Serena", "Uncle_Fu", "Dylan", "Eric", "Ryan", "Aiden", "Ono_Anna", "Sohee"])

base_ckpt = r"$base_ckpt_abs".strip()
if base_ckpt:
  base_cfg["checkpoint_path"] = base_ckpt
else:
  base_cfg.pop("checkpoint_path", None)

config_path.write_text(json.dumps(config, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
PYEOF
}

repair_base_checkpoint_hint() {
  local base_model_abs hint_file resolved_hint
  base_model_abs="$(expand_path "$BASE_MODEL_PATH")"
  hint_file="$base_model_abs/checkpoint_path.txt"
  [[ -f "$hint_file" ]] || return 0

  resolved_hint="$(tr -d '\r' < "$hint_file" | head -n 1 | xargs)"
  if [[ -z "$resolved_hint" || ! -e "$(expand_path "$resolved_hint")" ]]; then
    printf '%s\n' "$base_model_abs" > "$hint_file"
    log_info "已修复 Base 模型 checkpoint_path.txt: $hint_file"
  fi
}

main() {
  echo "========================================"
  echo "  Xeon TTS Skill 环境准备"
  echo "========================================"
  install_system_deps
  setup_miniconda
  setup_venv
  install_python_packages
  verify_python_runtime
  copy_node_config
  generate_tts_config
  download_model_if_missing "$BASE_MODEL_REPO" "$BASE_MODEL_PATH"
  download_model_if_missing "$CUSTOM_MODEL_REPO" "$CUSTOM_MODEL_PATH"
  download_model_if_missing "$BASE_CHECKPOINT_REPO" "$BASE_CHECKPOINT_PATH"
  update_tts_model_paths
  repair_base_checkpoint_hint
  mkdir -p runtime outputs references
  log_info "Xeon TTS 环境准备完成"
}

main "$@"
