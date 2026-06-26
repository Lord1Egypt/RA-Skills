#!/usr/bin/env bash
# List available Smallest AI voices and their characteristics

cat << 'EOF'
╔══════════════════════════════════════════════════════════════╗
║              Smallest AI — Available Voices                  ║
║              Lightning TTS Model                             ║
╚══════════════════════════════════════════════════════════════╝

ENGLISH VOICES
──────────────
  emily      Female │ Neutral, clear        │ Best for: general use, announcements
  jasmine    Female │ Warm, expressive       │ Best for: storytelling, greetings
  arman      Male   │ Professional, deep     │ Best for: reports, news, briefings
  arnav      Male   │ Conversational         │ Best for: casual updates, reminders

HINDI VOICES
────────────
  mithali    Female │ Native Hindi, natural  │ Best for: Hindi content, code-switching

USAGE
─────
  # In tts.sh
  tts.sh "Hello" --voice emily

  # In tts.py
  python3 tts.py "Hello" --voice arman

  # Code-switching (auto-detected)
  tts.sh "Hey, मुझे remind कर दो" --voice emily --lang hi

NOTES
─────
  • Voice cloning available on Basic plan ($5/mo) and above
  • New voices added regularly — check https://waves-docs.smallest.ai
  • For voice cloning, use the Smallest AI console at https://waves.smallest.ai

EOF
