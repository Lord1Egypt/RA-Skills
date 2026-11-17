# ffmpeg Recipes: Probe, Encode Ladders, Size Math

## Probe first

    ffprobe -v error -show_format -show_streams -of json input.mov

Key fields: codec_name, width/height, r_frame_rate vs avg_frame_rate (differ → VFR), pix_fmt, color_transfer (smpte2084/arib-std-b67 → HDR), bit_rate, duration, size.

## The three paths

**Passthrough** (already compliant): do nothing, deliver as-is.

**Remux** (right codecs, wrong container — seconds, zero quality loss):

    ffmpeg -i input.mkv -c copy -movflags +faststart output.mp4

**Re-encode** (safe default for any upload target):

    ffmpeg -i input.mov -c:v libx264 -profile:v high -pix_fmt yuv420p \
      -crf 21 -preset slow -c:a aac -b:a 160k -ar 48000 \
      -movflags +faststart output.mp4

## Size-budget math

    total_kbps = size_cap_MB × 8192 ÷ duration_s
    video_kbps = total_kbps − audio_kbps (× ~0.98 for container overhead)

CRF vs two-pass:

- **Headroom** (estimated CRF output well under cap) → CRF 20-23, simpler and better quality
- **Tight cap** → two-pass bitrate targeting:


    ffmpeg -y -i in.mp4 -c:v libx264 -b:v 470k -pass 1 -an -f null /dev/null
    ffmpeg -i in.mp4 -c:v libx264 -b:v 470k -pass 2 -c:a aac -b:a 128k out.mp4

## Quality floors (H.264, 30fps)

| Resolution | Floor | Comfortable |
|---|---|---|
| 1080p | ~1.5 Mbps | 4-8 Mbps |
| 720p | ~0.8 Mbps | 2-4 Mbps |
| 480p | ~0.5 Mbps | 1-2 Mbps |

If the budget falls below the floor for the current resolution, step down one rung instead of starving it. Screen-content/tutorial video tolerates ~30-40% lower bitrates than camera footage; fast motion (sports, gaming) needs ~50% more.

## Common transforms

Downscale to 1080p (keep aspect):

    -vf "scale=1920:-2:flags=lanczos"

Force constant frame rate (fix VFR):

    -vsync cfr -r 30

10-bit HEVC → 8-bit SDR H.264:

    -c:v libx264 -pix_fmt yuv420p

HDR (PQ/HLG) → SDR tone-map:

    -vf "zscale=t=linear:npl=100,tonemap=hable,zscale=p=bt709:t=bt709:m=bt709,format=yuv420p"

Strip audio / replace audio:

    -an                    # strip
    -i music.m4a -map 0:v -map 1:a -shortest   # replace

Trim without re-encoding (keyframe-aligned, fast):

    ffmpeg -ss 00:00:05 -to 00:00:35 -i in.mp4 -c copy out.mp4

Tiny looping clip for email/web:

    ffmpeg -ss 12 -t 8 -i in.mp4 -vf "scale=640:-2" -c:v libx264 -crf 28 -an -movflags +faststart loop.mp4

## Speed vs quality

`-preset` slow > medium > fast trades encode time for compression efficiency (~10-20% size per step). Batch jobs on a deadline: medium. Tight size caps: slow/slower. Never use ultrafast for delivery files.
