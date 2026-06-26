#!/usr/bin/env bash
set -euo pipefail

# Optional comma-separated input names via env:
# export OBS_AUDIO_INPUTS="Mic/Aux,Desktop Audio"
INPUTS_CSV="${OBS_AUDIO_INPUTS:-}"
MIC_DB="${MIC_DB:--6}"
DESKTOP_DB="${DESKTOP_DB:--12}"

if [[ -z "$INPUTS_CSV" ]]; then
  echo "No OBS_AUDIO_INPUTS provided; skipping explicit input tuning."
  echo "Tip: export OBS_AUDIO_INPUTS='Mic/Aux,Desktop Audio'"
  exit 0
fi

IFS=',' read -r -a INPUTS <<< "$INPUTS_CSV"
for i in "${!INPUTS[@]}"; do
  name="$(echo "${INPUTS[$i]}" | xargs)"
  [[ -z "$name" ]] && continue
  target_db="$MIC_DB"
  [[ "$i" -gt 0 ]] && target_db="$DESKTOP_DB"
  mcporter call "obs.set_input_volume(input_name: \"$name\", db: $target_db)" >/dev/null || true
  mcporter call "obs.get_input_mute(input_name: \"$name\")" >/dev/null || true
  echo "Tuned input '$name' to ${target_db}dB"
done
