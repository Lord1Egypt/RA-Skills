#!/usr/bin/env bash
# resize_photo.sh — 把生成的简历照裁剪/缩放到标准证件照尺寸（不拉伸变形）。
#
# 用法:
#   resize_photo.sh <输入图> <预设|宽x高> [输出图]
# 例:
#   resize_photo.sh photo.jpg 二寸
#   resize_photo.sh photo.jpg 413x579 out.jpg
set -euo pipefail

in="${1:-}"; target="${2:-}"; out="${3:-}"
if [ -z "$in" ] || [ -z "$target" ]; then
  echo "用法: resize_photo.sh <输入图> <预设|宽x高> [输出图]" >&2
  echo "预设: 小一寸 一寸 大一寸 小二寸 二寸 美签 方图 3x4" >&2
  exit 2
fi
[ -f "$in" ] || { echo "找不到输入文件: $in" >&2; exit 1; }

case "$target" in
  小一寸|small1) dims=260x378 ;;
  一寸|1寸|1inch) dims=295x413 ;;
  大一寸|big1) dims=390x567 ;;
  小二寸|small2) dims=413x531 ;;
  二寸|2寸|2inch) dims=413x579 ;;
  美签|us|passport|2x2) dims=600x600 ;;
  方图|square|1x1) dims=1200x1200 ;;
  3x4|简历) dims=1200x1600 ;;
  *[xX]*) dims="$target" ;;
  *) echo "未知预设: $target" >&2; exit 2 ;;
esac
w="${dims%[xX]*}"; h="${dims##*[xX]}"
case "$w$h" in (*[!0-9]*) echo "尺寸必须是 宽x高 数字: $dims" >&2; exit 2 ;; esac

if [ -z "$out" ]; then
  case "$target" in
    小一寸|small1) slug=1in-small ;; 一寸|1寸|1inch) slug=1in ;;
    大一寸|big1) slug=1in-big ;; 小二寸|small2) slug=2in-small ;;
    二寸|2寸|2inch) slug=2in ;; 美签|us|passport|2x2) slug=passport ;;
    方图|square|1x1) slug=square ;; 3x4|简历) slug=3x4 ;;
    *) slug="$target" ;;
  esac
  slug="${slug//[^A-Za-z0-9._-]/}"
  [ -n "$slug" ] || slug=idphoto
  base="${in%.*}"; out="${base}_${slug}.jpg"
fi

if command -v magick >/dev/null 2>&1; then
  magick "$in" -auto-orient -resize "${w}x${h}^" -gravity center -extent "${w}x${h}" -quality 92 "$out"
elif command -v convert >/dev/null 2>&1; then
  convert "$in" -auto-orient -resize "${w}x${h}^" -gravity center -extent "${w}x${h}" -quality 92 "$out"
elif command -v ffmpeg >/dev/null 2>&1; then
  ffmpeg -hide_banner -loglevel error -y -i "$in" \
    -vf "scale=${w}:${h}:force_original_aspect_ratio=increase,crop=${w}:${h}" -pix_fmt yuvj444p -q:v 2 "$out"
elif command -v sips >/dev/null 2>&1; then
  sw=$(sips -g pixelWidth "$in" | awk '/pixelWidth/{print $2}')
  sh=$(sips -g pixelHeight "$in" | awk '/pixelHeight/{print $2}')
  read -r nw nh < <(awk -v sw="$sw" -v sh="$sh" -v w="$w" -v h="$h" \
    'BEGIN{nw=w; nh=int(sh*w/sw+0.5); if(nh<h){nh=h; nw=int(sw*h/sh+0.5)}; print nw, nh}')
  tmp="${out%.*}.tmp.${out##*.}"
  sips -s format jpeg -z "$nh" "$nw" "$in" --out "$tmp" >/dev/null
  sips -s format jpeg -c "$h" "$w" "$tmp" --out "$out" >/dev/null
  rm -f "$tmp"
else
  echo "需要 magick / convert / ffmpeg / sips 之一来完成缩放。" >&2
  exit 3
fi

echo "已输出: $out (${w}x${h})"
