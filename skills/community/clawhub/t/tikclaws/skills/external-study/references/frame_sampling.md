# Frame sampling reference

The helper is the normal path. These commands define what the helper does and are only for diagnosis.

```bash
WORKDIR="${PWD}/tikclaws/external-study/$(date -u +%Y%m%dT%H%M%SZ)"
mkdir -p "$WORKDIR/frames"

ffprobe -v error   -print_format json   -show_format   -show_streams   "$INPUT" > "$WORKDIR/probe.json"

ffmpeg -y -hide_banner -loglevel error   -i "$INPUT"   -vf "fps=1/2,scale='min(1280,iw)':-2"   -frames:v 8   "$WORKDIR/frames/frame_%03d.jpg"

ffmpeg -y -hide_banner -loglevel error   -pattern_type glob   -i "$WORKDIR/frames/frame_*.jpg"   -vf "scale=320:-1,tile=4x2"   -frames:v 1   "$WORKDIR/contact_sheet.jpg"
```

Required local outputs:

- `probe.json`
- `frame_index.json`
- `contact_sheet.jpg`
- at least 3 `frames/frame_*.jpg`

Sampled frames do not prove every moment of the source. Write only observations supported by the evidence.
