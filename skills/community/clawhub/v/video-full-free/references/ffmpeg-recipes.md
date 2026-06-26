# FFmpeg — وصفات جاهزة للفيديوهات القصيرة

## دمج فيديو + صوت (أساسي)

```bash
ffmpeg -y \
  -i scene_01.mp4 \
  -i vo_01.mp3 \
  -c:v copy \
  -c:a aac -b:a 192k \
  -shortest \
  -map 0:v:0 -map 1:a:0 \
  merged_01.mp4
```

## دمج كل المشاهد (concat)

```bash
# أنشئ ملف القائمة أولاً:
echo "file 'merged_01.mp4'" >> concat_list.txt
echo "file 'merged_02.mp4'" >> concat_list.txt
# ... إلخ

# ثم الدمج:
ffmpeg -y \
  -f concat -safe 0 \
  -i concat_list.txt \
  -c:v libx264 -crf 23 \
  -c:a aac -b:a 192k \
  -preset fast \
  -movflags +faststart \
  final_video.mp4
```

## ضغط للإرسال على Telegram (إذا كان الحجم كبيراً)

```bash
# الحد الأقصى على Telegram = 50MB
ffmpeg -y \
  -i final_video.mp4 \
  -c:v libx264 -crf 28 \
  -c:a aac -b:a 128k \
  -preset fast \
  final_video_compressed.mp4
```

## إضافة subtitles مدمجة (اختياري)

```bash
# أنشئ ملف SRT:
# 1
# 00:00:00,000 --> 00:00:10,000
# هل تعلم أن كيلو من اليورانيوم يعادل 3 ملايين كيلو فحم؟

ffmpeg -y \
  -i final_video.mp4 \
  -vf "subtitles=subtitles.srt:force_style='FontName=Cairo,FontSize=18,PrimaryColour=&HFFFFFF,OutlineColour=&H000000,Outline=2'" \
  final_with_subs.mp4
```

## فحص مدة الفيديو

```bash
ffprobe -v error \
  -show_entries format=duration \
  -of default=noprint_wrappers=1:nokey=1 \
  final_video.mp4
```

## فحص مزامنة الصوت والصورة

```bash
ffprobe -v error \
  -select_streams v:0 \
  -show_entries stream=codec_name,duration,r_frame_rate \
  -of default=noprint_wrappers=1 \
  merged_01.mp4
```

## تصحيح مشكلة out-of-sync

```bash
# إذا الصوت قبل الفيديو:
ffmpeg -y -i scene_01.mp4 -i vo_01.mp3 \
  -itsoffset 0.5 -i vo_01.mp3 \
  -c:v copy -c:a aac \
  -map 0:v:0 -map 2:a:0 \
  merged_01_fixed.mp4

# إضافة -async 1 للمزامنة التلقائية:
ffmpeg -y -i merged_all.mp4 -async 1 output.mp4
```
