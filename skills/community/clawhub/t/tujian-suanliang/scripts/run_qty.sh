#!/usr/bin/env bash
# 统一入口：contract-only。正式链路 cad-file-reader → lis-skill-bus → 本技能。
# 可选 bus 接线：--bus-pull --project 项目 [--building 楼栋] [--floor 楼层] -o 输出目录
# 命中契约后自动把 qty_core 的输入换成拉取到的 contract.json；
# 缺依赖由入口闸门统一返回 20/21；未命中/拉取失败 exit 1，不回退“本机解图”。
set -euo pipefail
_HERE="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
source "$_HERE/runtime_env.sh"
: "${CAD_MEM_LIMIT_MB:=4096}"; export CAD_MEM_LIMIT_MB

A=("$@")
COUNT=$#
BUS=0; BUS_PROJECT=""; BUS_BUILDING=""; BUS_FLOOR=""; BUS_OUT=""
OUT_TOKEN=()
FWD=()
for ((i=0; i<COUNT; i++)); do
  a="${A[$i]}"
  case "$a" in
    --bus-pull) BUS=1;;
    --project)  [[ $((i+1)) -lt $COUNT ]] && BUS_PROJECT="${A[$((i+1))]}"; ((i+=1));;
    --building) [[ $((i+1)) -lt $COUNT ]] && BUS_BUILDING="${A[$((i+1))]}"; ((i+=1));;
    --floor)    [[ $((i+1)) -lt $COUNT ]] && BUS_FLOOR="${A[$((i+1))]}"; ((i+=1));;
    --out|-o)   [[ $((i+1)) -lt $COUNT ]] && { BUS_OUT="${A[$((i+1))]}"; OUT_TOKEN=("$a" "${A[$((i+1))]}"); ((i+=1)); };;
    *) FWD+=("$a");;
  esac
done

SUB="${FWD[0]:-}"
# -o 只属于 floor/advanced/pipeline；floors/index 不接受，且 --bus-pull 时它就是契约落盘目录。
case "$SUB" in
  floor|advanced|pipeline) [[ ${#OUT_TOKEN[@]} -gt 0 ]] && FWD+=("${OUT_TOKEN[@]}");;
esac

# --check-deps 由核心打印完整状态（缺依赖 exit 20/21 + 安装命令），不要求底座已就位
for x in "${FWD[@]:-}"; do
  if [[ "$x" == "--check-deps" ]]; then
    exec "${PYTHON_BIN}" "${SKILL_DIR}/scripts/qty_core.py" "${FWD[@]}"
  fi
done

if [[ "$BUS" -eq 1 ]]; then
  if [[ -z "${BUS_PROJECT:-}" || -z "${BUS_OUT:-}" ]]; then
    echo "[run_qty] --bus-pull 需要同时给出 --project 与 -o/--out" >&2
    exit 1
  fi
  PULL=(--project "$BUS_PROJECT" --out-dir "$BUS_OUT" --cad-skill-dir "$CAD_SKILL_DIR")
  [[ -n "${BUS_BUILDING:-}" ]] && PULL+=(--building "$BUS_BUILDING")
  [[ -n "${BUS_FLOOR:-}" ]] && PULL+=(--floor "$BUS_FLOOR")
  mkdir -p "$BUS_OUT"
  if ! "${PYTHON_BIN}" "${SKILL_DIR}/scripts/qty_statesync.py" "${PULL[@]}"; then
    echo "[run_qty] bus 契约拉取失败，已停止（不回退本机解图）。" >&2
    # 依赖缺失统一映射 20/21，不把闸门错误覆盖成 1。
    set +e
    "${PYTHON_BIN}" "${SKILL_DIR}/scripts/qty_core.py" --check-deps >/dev/null 2>&1
    _gate_rc=$?
    set -e
    case "$_gate_rc" in
      20|21) exit "$_gate_rc";;
    esac
    exit 1
  fi
  # 把拉到的契约 JSON 作为 qty_core 的 positional dwg 参数追加。
  # 不能覆盖 FWD[1]：floor 子命令的 FWD[1] 可能是 --floor-label 等选项值。
  FWD+=("$BUS_OUT/contract.json")
fi

if [[ "${FWD[0]:-}" == "advanced" || "${FWD[0]:-}" == "pipeline" ]]; then
  exec "${PYTHON_BIN}" "${SKILL_DIR}/scripts/cad_quantity_pipeline.py" "${FWD[@]:1}"
fi
exec "${PYTHON_BIN}" "${SKILL_DIR}/scripts/qty_core.py" "${FWD[@]}"
