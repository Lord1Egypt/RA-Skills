#!/bin/bash
set -euo pipefail

AUDIO_INFO="$(system_profiler SPAudioDataType)"

default_output="$(
  printf '%s\n' "$AUDIO_INFO" | awk '
    /^[[:space:]]{8}[^:]+:$/ {
      name = $0
      gsub(/^[[:space:]]+/, "", name)
      sub(/:$/, "", name)
      current = name
    }
    /Default Output Device: Yes/ {
      print current
      exit
    }
  '
)"

echo "Scanning audio devices..."
echo
printf '%s\n' "$AUDIO_INFO" | sed -n '1,240p'
echo

if printf '%s\n' "$AUDIO_INFO" | grep -q "BlackHole 2ch"; then
  echo "BlackHole 2ch detected."
  echo
  echo "Current default output: ${default_output:-unknown}"
  echo
  case "${default_output:-}" in
    "BlackHole 2ch"|"多输出设备"|"Multi-Output Device")
      ;;
    *)
    echo "BlackHole is installed, but macOS is still playing audio through another output."
    echo "Until the default output is switched to a Multi-Output Device or BlackHole directly,"
    echo "system-audio capture will be silent."
    echo
      ;;
  esac
  echo "Next steps:"
  echo "1. Open Audio MIDI Setup."
  echo "2. Create a Multi-Output Device."
  echo "3. Add your headphones or speakers and BlackHole 2ch."
  echo "4. Set the Multi-Output Device as the macOS output device."
  echo "5. Run validate_system_audio_loopback.sh to confirm BlackHole is receiving real audio."
  echo "6. Start the realtime interpreter with start_system_bilingual_subtitles.sh."
else
  echo "BlackHole 2ch not detected."
  echo
  echo "If you just installed it, reboot macOS first."
  echo "Then run this script again."
fi
