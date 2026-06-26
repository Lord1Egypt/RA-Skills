# Seamless Looper — Tips & Use Cases

## Best Crossfade Durations by Footage Type

| Footage Type | Crossfade | Why |
|---|---|---|
| Fast cuts / high motion | 0.5s | Longer causes ghosting on motion |
| Default ambient / lofi | 1s | Works for most backgrounds |
| Slow pan / nature | 2s | Smooth enough to not notice |
| Very slow drift / clouds | 3s | Seamless for slow-moving content |

## Input Requirements

- Format: `.mp4` (H.264 recommended)
- Duration: ≥2 seconds (shorter files skipped)
- Size: No hard limit, but longer = longer processing
- Audio: Not preserved in looped output (visual only)

## Common Workflows

**Batch loop all ambient videos in a folder:**
```bash
bash loop.sh ~/Downloads/ambient ~/Videos/looped 1
```

**Quick 2s crossfade for nature footage:**
```bash
bash loop.sh ./forest_footage ./output 2
```

**Preview before processing (dry run):**
```bash
for f in ~/Videos/*.mp4; do
  dur=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$f")
  echo "$(basename "$f"): ${dur}s"
done
```

## Output Notes

- Output is 2x the input duration (two copies joined at crossfade)
- File naming: `original_looped.mp4`
- CRF 18 = high quality, reasonable file size
- Preset `fast` = quick encoding

## Use Cases

- **Twitch/YouTube ambient backgrounds** — seamless 10-30min loops
- **Social media** — looped product reveal clips
- **Projection mapping** — continuous ambient backgrounds
- **Website hero video** — seamless background loops
- **Podcast video** — looped intro/outro bumper
