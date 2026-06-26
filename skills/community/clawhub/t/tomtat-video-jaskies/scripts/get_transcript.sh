#!/bin/bash
# Script để lấy transcript từ YouTube video dùng yt-dlp

URL=$1
if [ -z "$URL" ]; then
    echo "Lỗi: Vui lòng cung cấp URL video YouTube."
    exit 1
fi

# Tải transcript (ưu tiên tiếng Việt, sau đó là tiếng Anh)
# Lưu vào file tạm
OUTPUT_DIR=$(mktemp -d)
yt-dlp --skip-download --write-auto-subs --sub-lang "vi,en" --convert-subs vtt -o "$OUTPUT_DIR/sub" "$URL" > /dev/null 2>&1

if [ -f "$OUTPUT_DIR/sub.vi.vtt" ]; then
    cat "$OUTPUT_DIR/sub.vi.vtt"
elif [ -f "$OUTPUT_DIR/sub.en.vtt" ]; then
    cat "$OUTPUT_DIR/sub.en.vtt"
else
    echo "Lỗi: Không tìm thấy transcript cho video này."
    rm -rf "$OUTPUT_DIR"
    exit 1
fi

rm -rf "$OUTPUT_DIR"
