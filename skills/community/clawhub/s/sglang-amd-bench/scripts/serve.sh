#!/bin/bash
#
# General sglang server launcher for benchmarking
#
# Usage:
#   MODEL_PATH=/data/models/DeepSeek-R1 CONFIG=DP8EP8 bash serve.sh
#   MODEL_PATH=/data/models/Llama-70B CONFIG=TP8 bash serve.sh
#
# CONFIG format (case-insensitive):
#   TP8          - pure TP (dense models)
#   DP8EP8       - DP-attention + EP (MoE, all-reduce EP)
#   DP8EP8_A2A   - DP-attention + EP (MoE, all-to-all EP via mori)
#   TP4EP4       - TP + EP (MoE, all-reduce EP)
#   TP4EP4_A2A   - TP + EP (MoE, all-to-all EP via mori)
#   DP4TP4       - DP-attention + TP for MoE
#
# Env vars:
#   MODEL_PATH  - (required) model weights path
#   CONFIG      - (required) parallel config
#   LOG_DIR     - log directory (default: .)
#   PORT        - server port (default: 30000)
#   MTP         - MTP speculative decoding steps: 0=off, N>0=mtp with N steps (default: 0)
#   MTP_ALGO    - speculative algorithm: NEXTN|EAGLE (required when MTP>0)
#   LOAD_DUMMY  - use dummy weights for fast startup: 0|1 (default: 1)
#   DISABLE_RADIX_CACHE - disable radix cache: 0|1 (default: 1)
#   BACKGROUND  - run server in background: 0|1 (default: 0)
#   DRY_RUN     - print command without running: 0|1 (default: 0)
#   EXTRA_ARGS  - additional sglang flags
#

set -eu

export SGLANG_USE_AITER=1

# ── Auto-detect PYTHONPATH for aiter/mori/sglang ──────────────────────
# When launched via non-interactive shells (e.g. docker exec -d), .bashrc
# may not be sourced, causing PYTHONPATH to be missing paths needed for
# editable installs of aiter, mori, and sglang. Auto-add them if present.
for p in /sgl-workspace/aiter /sgl-workspace/mori /sgl-workspace/sglang/python; do
  [[ -d "$p" && ":${PYTHONPATH:-}:" != *":$p:"* ]] && export PYTHONPATH="${p}:${PYTHONPATH:-}"
done

: "${MODEL_PATH:?Error: MODEL_PATH must be set}"
: "${CONFIG:?Error: CONFIG must be set (e.g. TP8, DP8EP8, DP8EP8_A2A)}"

PORT="${PORT:-30000}"
LOG_DIR="${LOG_DIR:-.}"
MTP="${MTP:-0}"
LOAD_DUMMY="${LOAD_DUMMY:-1}"
DISABLE_RADIX_CACHE="${DISABLE_RADIX_CACHE:-1}"
DRY_RUN="${DRY_RUN:-0}"
EXTRA_ARGS="${EXTRA_ARGS:-}"

# ── Parse CONFIG ─────────────────────────────────────────────────────
CFG=$(echo "$CONFIG" | tr '[:lower:]' '[:upper:]')

A2A=0
if [[ "$CFG" == *_A2A ]]; then
  A2A=1
  CFG="${CFG%_A2A}"
fi

DP_SIZE=1
EP_SIZE=1

if [[ "$CFG" =~ ^DP([0-9]+)EP([0-9]+)$ ]]; then
  DP_SIZE="${BASH_REMATCH[1]}"
  EP_SIZE="${BASH_REMATCH[2]}"
elif [[ "$CFG" =~ ^TP([0-9]+)EP([0-9]+)$ ]]; then
  EP_SIZE="${BASH_REMATCH[2]}"
elif [[ "$CFG" =~ ^DP([0-9]+)TP([0-9]+)$ ]]; then
  DP_SIZE="${BASH_REMATCH[1]}"
elif [[ "$CFG" =~ ^TP([0-9]+)$ ]]; then
  :
else
  echo "Error: unrecognized CONFIG format: $CONFIG"
  echo "Examples: TP8, DP8EP8, DP8EP8_A2A, TP4EP4, DP4TP4"
  exit 1
fi

# ── Derive world size from CONFIG ────────────────────────────────────
# In sglang, --tp-size is the world size (total GPUs).
# The numbers in CONFIG represent the parallelism degree = world size.
# e.g. TP8 → 8, DP4EP4 → 4, DP8EP8 → 8
WORLD_SIZE=$(echo "$CFG" | grep -oE '[0-9]+' | head -1)

CMD="python3 -m sglang.launch_server"
CMD="$CMD --model-path $MODEL_PATH"
CMD="$CMD --tp-size $WORLD_SIZE"
CMD="$CMD --port $PORT"
CMD="$CMD --trust-remote-code"

[[ "$DISABLE_RADIX_CACHE" == "1" ]] && CMD="$CMD --disable-radix-cache"
[[ "$LOAD_DUMMY" == "1" ]] && CMD="$CMD --load-format dummy"
[[ $DP_SIZE -gt 1 ]] && CMD="$CMD --dp-size $DP_SIZE --enable-dp-attention --enable-dp-lm-head"
[[ $EP_SIZE -gt 1 ]] && CMD="$CMD --ep-size $EP_SIZE"
[[ $A2A -eq 1 ]] && CMD="$CMD --moe-a2a-backend mori"
if [[ "$MTP" -gt 0 ]]; then
  : "${MTP_ALGO:?Error: MTP_ALGO must be set when MTP>0 (e.g. NEXTN, EAGLE)}"
  CMD="$CMD --speculative-algorithm $MTP_ALGO"
  CMD="$CMD --speculative-num-steps $MTP"
  CMD="$CMD --speculative-eagle-topk 1"
  CMD="$CMD --speculative-num-draft-tokens $(( MTP + 1 ))"
fi
[[ -n "$EXTRA_ARGS" ]] && CMD="$CMD $EXTRA_ARGS"

# ── Log ──────────────────────────────────────────────────────────────
if [[ "$MTP" -gt 0 ]]; then
  MTP_LABEL="mtp${MTP}"
else
  MTP_LABEL="mtp0"
fi
if [[ $A2A -eq 1 ]]; then
  LOG_LABEL="${CFG}_A2A_${MTP_LABEL}"
else
  LOG_LABEL="${CFG}_${MTP_LABEL}"
fi
LOG_FILE="${LOG_DIR}/server_${LOG_LABEL}.log"

# ── Print ────────────────────────────────────────────────────────────
echo "======================================================================"
echo "SGLang Server Launch"
echo "  Model:      ${MODEL_PATH}"
echo "  Config:     ${CONFIG}"
echo "  World size: ${WORLD_SIZE}"
echo "  DP:         ${DP_SIZE}"
echo "  EP:         ${EP_SIZE}"
echo "  All-to-All: ${A2A}"
echo "  MTP:        ${MTP}"
echo "  Port:       ${PORT}"
echo "  Dummy load: ${LOAD_DUMMY}"
echo "  Log:        ${LOG_FILE}"
echo "======================================================================"
echo ""
# Print copy-pasteable command with \ continuations
echo "$CMD" \
  | tr ' ' '\n' \
  | awk '
    BEGIN { line="" }
    /^--/ { if (line != "") print "  " line " \\"; line=$0; next }
    { if (line != "") line=line " " $0; else line=$0 }
    END { print "  " line " \\" }
  '
echo "  2>&1 | tee ${LOG_FILE}"
echo ""

if [[ "$DRY_RUN" == "1" ]]; then
  echo "[DRY RUN] Remove DRY_RUN=1 to execute."
  exit 0
fi

mkdir -p "$LOG_DIR"

if [[ "${BACKGROUND:-0}" == "1" ]]; then
  nohup $CMD > "$LOG_FILE" 2>&1 &
  echo "Server launched in background (PID: $!). Log: ${LOG_FILE}"
else
  exec $CMD 2>&1 | tee "$LOG_FILE"
fi
