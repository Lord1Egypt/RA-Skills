#!/bin/bash
# Video Watcher - Analyze a video URL
# Usage: ./analyze.sh "https://youtube.com/watch?v=..."

set -e

URL="$1"
OUTPUT_DIR="${2:-./outputs}"
FRAME_INTERVAL="${3:-30}"
WHISPER_MODEL="${4:-medium}"

if [ -z "$URL" ]; then
    echo "❌ URL gerekli!"
    echo "Kullanım: $0 <video-url> [output-dir] [frame-interval] [whisper-model]"
    exit 1
fi

# Klasörleri oluştur
mkdir -p "$OUTPUT_DIR/frames"

echo "🎬 Video Watcher"
echo "================"
echo "URL: $URL"
echo "Output: $OUTPUT_DIR"
echo ""

# 1. Video indir
echo "📥 Video indiriliyor..."
yt-dlp -f 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4' \
    -o "$OUTPUT_DIR/video.%(ext)s" \
    --no-playlist \
    "$URL" 2>/dev/null || {
    # Sadece audio dene
    echo "📥 Sadece audio indiriliyor..."
    yt-dlp -f 'bestaudio' \
        -x --audio-format mp3 \
        -o "$OUTPUT_DIR/audio.%(ext)s" \
        --no-playlist \
        "$URL"
}

# Video veya audio bul
VIDEO_FILE=$(find "$OUTPUT_DIR" -maxdepth 1 -name "video.*" | head -1)
AUDIO_FILE=$(find "$OUTPUT_DIR" -maxdepth 1 -name "audio.*" | head -1)

if [ -n "$VIDEO_FILE" ]; then
    echo "✅ Video indirildi: $VIDEO_FILE"
    
    # 2. Audio çıkar
    echo "🔊 Audio çıkarılıyor..."
    ffmpeg -i "$VIDEO_FILE" -vn -acodec libmp3lame -q:a 2 "$OUTPUT_DIR/audio.mp3" -y 2>/dev/null
    AUDIO_FILE="$OUTPUT_DIR/audio.mp3"
    
    # 3. Frameler al
    echo "📸 Frameler alınıyor (her ${FRAME_INTERVAL}s)..."
    DURATION=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$VIDEO_FILE" 2>/dev/null | cut -d. -f1)
    
    for i in $(seq 0 $FRAME_INTERVAL $DURATION); do
        TIMESTAMP=$(printf "%02d_%02d_%02d" $((i/3600)) $(((i%3600)/60)) $((i%60)))
        ffmpeg -ss $i -i "$VIDEO_FILE" -vframes 1 -q:v 2 "$OUTPUT_DIR/frames/${TIMESTAMP}.jpg" -y 2>/dev/null
    done
    FRAME_COUNT=$(ls "$OUTPUT_DIR/frames/" | wc -l | tr -d ' ')
    echo "✅ $FRAME_COUNT frame alındı"
fi

# 4. Transcript
if [ -n "$AUDIO_FILE" ]; then
    echo "🎙️ Transcript çıkarılıyor (model: $WHISPER_MODEL)..."
    whisper "$AUDIO_FILE" \
        --model "$WHISPER_MODEL" \
        --output_format txt \
        --output_format srt \
        --output_dir "$OUTPUT_DIR" \
        2>/dev/null
    
    # Dosya isimlerini düzenle
    mv "$OUTPUT_DIR/audio.txt" "$OUTPUT_DIR/transcript.txt" 2>/dev/null || true
    mv "$OUTPUT_DIR/audio.srt" "$OUTPUT_DIR/transcript.srt" 2>/dev/null || true
    
    echo "✅ Transcript hazır"
fi

echo ""
echo "🎉 Tamamlandı!"
echo ""
echo "Çıktılar:"
ls -la "$OUTPUT_DIR"
echo ""
echo "Frameler:"
ls "$OUTPUT_DIR/frames/" | head -5
[ $(ls "$OUTPUT_DIR/frames/" | wc -l) -gt 5 ] && echo "... ve daha fazlası"
