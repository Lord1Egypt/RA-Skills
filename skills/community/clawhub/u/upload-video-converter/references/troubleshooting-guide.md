# Troubleshooting Rejected or Broken Uploads

Symptom-first guide. Probe the file before guessing.

## "Unsupported format" / rejected at upload

1. Container not on whitelist → remux to MP4 (`-c copy`) if codecs comply
2. Codec not accepted (HEVC, VP9, AV1, ProRes on strict targets) → re-encode to H.264
3. Pixel format exotic (yuv444p, 10-bit) → add `-pix_fmt yuv420p`
4. Audio codec odd (PCM, FLAC, Opus in MP4) → `-c:a aac -b:a 160k`
5. Profile too high (H.264 4:4:4 / High10) → `-profile:v high`

## Upload succeeds but processing fails / stalls

- moov atom at end of file → re-run with `-movflags +faststart`
- Extremely high bitrate spikes → cap with `-maxrate`/`-bufsize` (e.g., `-maxrate 8M -bufsize 16M`)
- Broken metadata/timestamps from screen recorders → `-fflags +genpts` or full re-encode
- Zero-byte or truncated file from interrupted export → re-export source

## Looks washed out / gray after upload

HDR footage (iPhone HLG/Dolby Vision, PQ) uploaded to SDR pipeline. Tone-map:

    -vf "zscale=t=linear:npl=100,tonemap=hable,zscale=p=bt709:t=bt709:m=bt709,format=yuv420p"

Verify `color_transfer` in the output probe is bt709.

## Stutter / audio drift after conversion or in editor

Variable frame rate source (phones, OBS, screen recorders). Force CFR:

    -vsync cfr -r 30

Check drift at the END of long files — VFR drift accumulates.

## Green/pink artifacts or half-height garbage

Pixel-format or interlacing mismatch:

- `-pix_fmt yuv420p` for playback compatibility
- Interlaced source (1080i) → deinterlace: `-vf yadif=1`

## Audio out of sync only after trimming

Keyframe-misaligned `-c copy` trim. Either accept the nearest-keyframe cut, or re-encode the trim:

    ffmpeg -ss 5 -to 35 -i in.mp4 -c:v libx264 -crf 21 -c:a aac out.mp4

## File plays locally but not in browser/preview

- Missing faststart (see above)
- H.264 level too high for the player → `-level 4.1` is a safe ceiling for 1080p60
- Audio in a second language track / multiple streams → map explicitly: `-map 0:v:0 -map 0:a:0`

## Size cap met but quality is unacceptable

- Preset too fast → slow/slower buys 10-20% efficiency
- Resolution too high for the budget → step down one rung (see quality floors in ffmpeg-recipes.md)
- Grain/noise eating bitrate → light denoise `-vf hqdn3d=1.5:1.5:6:6` before encoding
- Screen content: try `-tune animation` variants; camera content: never use stillimage tunes

## Escalation rules

- Duration over the destination cap → route to cutting, never silently truncate
- Aspect ratio mismatch → route to resizer, never stretch
- Source already heavily compressed and target cap is tiny → warn about visible quality loss before converting, and say what cap WOULD preserve quality
