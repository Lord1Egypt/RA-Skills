#!/usr/bin/env bash
# YouTube Music Skill - Demo Script
# Shows off the features of the new YouTube Music skill

set -e

SKILL_DIR="/home/oki/.openclaw/workspace/skills/youtube-music"

echo "🎵 YouTube Music Skill Demo"
echo "==========================="
echo ""
echo "Skill created successfully! Here's what you can do:"
echo ""
echo "1️⃣  PLAY MUSIC"
echo "   ./scripts/youtube-music.sh play \"Ye Tune Kya Kiya\""
echo ""
echo "2️⃣  PLAYBACK CONTROLS"
echo "   ./scripts/youtube-music.sh pause"
echo "   ./scripts/youtube-music.sh skip"
echo "   ./scripts/youtube-music.sh previous"
echo ""
echo "3️⃣  VOLUME CONTROL"
echo "   ./scripts/youtube-music.sh volume 75"
echo ""
echo "4️⃣  SEARCH"
echo "   ./scripts/youtube-music.sh search \"Arijit Singh\""
echo ""
echo "5️⃣  GET INFO"
echo "   ./scripts/youtube-music.sh now-playing"
echo ""
echo "==========================="
echo ""
echo "Or use natural language with OpenClaw:"
echo '  "play Ye Tune Kya Kiya"'
echo '  "pause the music"'
echo '  "skip to next track"'
echo '  "set volume to 75%"'
echo ""
echo "==========================="
echo ""
echo "📁 Skill Location: $SKILL_DIR"
echo "📚 Documentation: $SKILL_DIR/README.md"
echo "📖 Usage Guide: $SKILL_DIR/USAGE.md"
echo ""
echo "Ready to use! 🎵🔥"
