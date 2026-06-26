#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

python3 - <<'PY' "$SKILL_DIR/SKILL.md"
from pathlib import Path
import sys

path = Path(sys.argv[1])
text = path.read_text(encoding="utf-8")
assert text.startswith("---\n"), "SKILL.md must start with frontmatter"
assert "\n---\n" in text[4:], "SKILL.md frontmatter must close"
for needle in ["name: senseaudio-floating-audio-assistant", "description:", "metadata:"]:
    assert needle in text, f"missing {needle}"
for needle in [
    "start-senseaudio-floating-audio-assistant.sh",
    "stop-senseaudio-floating-audio-assistant.sh",
    "check-senseaudio-floating-audio-assistant-setup.sh",
    "AudioClaw agent",
    "BlackHole 2ch",
    "Multi-Output Device",
    "SenseAudio API key",
]:
    assert needle in text, f"missing launch contract item: {needle}"
print("manifest ok")
PY

for required in \
  start-senseaudio-floating-audio-assistant.sh \
  stop-senseaudio-floating-audio-assistant.sh \
  status-senseaudio-floating-audio-assistant.sh \
  check-senseaudio-floating-audio-assistant-setup.sh \
  open-senseaudio-floating-audio-assistant-runs.sh; do
  test -f "$SKILL_DIR/scripts/$required"
done
echo "launcher wrappers ok"

if find "$SKILL_DIR/scripts" -maxdepth 1 -type f -name '*realtime_subtitle*' | grep -q .; then
  echo "legacy realtime_subtitle wrapper names remain under scripts/" >&2
  exit 1
fi
echo "launcher namespace ok"

for script in "$SKILL_DIR"/scripts/*.sh; do
  bash -n "$script"
done
echo "shell entrypoints ok"

find "$SKILL_DIR/runtime/realtime_interpreter" -name '*.sh' -type f -print0 | while IFS= read -r -d '' script; do
  bash -n "$script"
done
echo "runtime shell sources ok"

python3 -m py_compile "$SKILL_DIR/scripts/senseaudio_api_smoke.py"
find "$SKILL_DIR/runtime/realtime_interpreter" -name '*.py' -type f -print0 | while IFS= read -r -d '' script; do
  python3 -m py_compile "$script"
done
diagnostics_json="$(mktemp)"
python3 "$SKILL_DIR/scripts/senseaudio_api_smoke.py" >"$diagnostics_json"
python3 -m json.tool "$diagnostics_json" >/dev/null
rm -f "$diagnostics_json"
find "$SKILL_DIR" -name '__pycache__' -type d -prune -exec rm -rf {} +
echo "SenseAudio probe ok"

test -f "$SKILL_DIR/README.md"
test -f "$SKILL_DIR/references/quickstart.md"
test -f "$SKILL_DIR/references/operator_notes.md"
test -f "$SKILL_DIR/references/senseaudio_integration.md"
test -f "$SKILL_DIR/references/troubleshooting.md"
echo "operator notes ok"

test -f "$SKILL_DIR/presets/meeting-digest-template.md"
test -f "$SKILL_DIR/presets/lofi-study-music.json"
test -f "$SKILL_DIR/runtime/realtime_interpreter/subtitle_overlay.swift"
test -f "$SKILL_DIR/runtime/realtime_interpreter/mic_pcm_stream.swift"
test -f "$SKILL_DIR/runtime/realtime_interpreter/runner.py"
test -f "$SKILL_DIR/runtime/realtime_interpreter/requirements.txt"
test -f "$SKILL_DIR/runtime/realtime_interpreter/start_system_subtitle_overlay.sh"
test -f "$SKILL_DIR/runtime/realtime_interpreter/stop_system_subtitle_overlay.sh"
test -f "$SKILL_DIR/runtime/realtime_interpreter/enter_subtitle_mode.sh"
test -f "$SKILL_DIR/runtime/realtime_interpreter/exit_subtitle_mode.sh"
test -f "$SKILL_DIR/runtime/realtime_interpreter/cross_platform_overlay/index.html"
test -f "$SKILL_DIR/runtime/realtime_interpreter/cross_platform_overlay/overlay_host.py"
echo "bundled runtime ok"
home_path_marker="/$(printf 'Users')/"
workspace_marker="~$(printf '.')audioclaw"
env_assignment_marker="[A-Z][A-Z0-9_]{2,}="
if grep -R -E "sk-[A-Za-z0-9]{20,}|${home_path_marker}|${workspace_marker}|${env_assignment_marker}" "$SKILL_DIR/presets" "$SKILL_DIR/references" "$SKILL_DIR/SKILL.md" >/dev/null 2>&1; then
  echo "upload package contains a local path, key-like token, or environment assignment" >&2
  exit 1
fi
echo "presets ok"
