#!/bin/bash
# 一括レンダリングスクリプト
# Usage: bash render-all.sh [composition]
# 引数なしで全コンポジションをレンダリング

set -e

OUTPUT_DIR="out"
mkdir -p "$OUTPUT_DIR"

render_composition() {
  local name=$1
  local width=$2
  local height=$3
  local suffix=$4

  echo "--- Rendering: ${name} (${width}x${height}) ---"
  npx remotion render src/index.ts "$name" \
    "${OUTPUT_DIR}/${name}${suffix}.mp4" \
    --width "$width" \
    --height "$height" \
    --codec h264
  echo "Done: ${OUTPUT_DIR}/${name}${suffix}.mp4"
}

if [ -n "$1" ]; then
  # 特定のコンポジションのみ
  COMP=$1
  case $COMP in
    Promo)
      render_composition "Promo" 1920 1080 ""
      ;;
    FeatureIntro)
      render_composition "FeatureIntro" 1080 1080 "-square"
      render_composition "FeatureIntro" 1080 1920 "-reel"
      ;;
    SnsShort)
      render_composition "SnsShort" 1080 1920 "-reel"
      ;;
    Tutorial)
      render_composition "Tutorial" 1920 1080 ""
      ;;
    *)
      echo "Unknown composition: $COMP"
      echo "Available: Promo, FeatureIntro, SnsShort, Tutorial"
      exit 1
      ;;
  esac
else
  # 全コンポジション
  render_composition "Promo" 1920 1080 ""
  render_composition "FeatureIntro" 1080 1080 "-square"
  render_composition "FeatureIntro" 1080 1920 "-reel"
  render_composition "SnsShort" 1080 1920 "-reel"
  render_composition "Tutorial" 1920 1080 ""
fi

echo ""
echo "=== All renders complete ==="
ls -lh "$OUTPUT_DIR"/*.mp4
