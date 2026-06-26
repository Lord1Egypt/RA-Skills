# Caption Templates — Instagram Reels Style

10 ready-to-use caption templates that mimic real Instagram Reels caption aesthetics.
Each template provides the full `drawtext` filter string. Replace placeholder values.

## Common Variables (customize these)

| Variable       | Description                  | Example                    |
|----------------|------------------------------|----------------------------|
| `TEXT`         | Caption text                 | `Your text here`           |
| `START`        | Start time (seconds)         | `1`                        |
| `END`          | End time (seconds)           | `8`                        |
| `FONTFILE`     | Path to font                 | `/usr/share/fonts/...`     |
| `FONTSIZE`     | Font size in pixels          | `56`                       |

**Font setup** — run before using templates:
```bash
apt-get install -y fonts-noto fonts-liberation fonts-dejavu fontconfig
# Useful font paths:
# /usr/share/fonts/truetype/noto/NotoSans-Bold.ttf
# /usr/share/fonts/truetype/noto/NotoSans-Regular.ttf
# /usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf
# /usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf
```

---

## Template 1: Classic Center Bottom (Instagram Default)

White bold text with black outline, centered at bottom.

```
drawtext=text='YOUR TEXT HERE':
  fontfile=/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf:
  fontsize=56:fontcolor=white:
  borderw=3:bordercolor=black:
  x=(w-tw)/2:y=h-th-250:
  enable='between(t,START,END)'
```

**Preview:** Clean, minimal, works on any background.

---

## Template 2: Highlighted Box (TikTok/Reels Popular)

White text on a semi-transparent black rounded box.

```
drawbox=x=(w-tw-40)/2:y=h-th-290:w=tw+40:h=th+20:
  color=black@0.65:t=fill:enable='between(t,START,END)',
drawtext=text='YOUR TEXT HERE':
  fontfile=/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf:
  fontsize=52:fontcolor=white:
  x=(w-tw)/2:y=h-th-280:
  enable='between(t,START,END)'
```

**Preview:** High contrast, readable on any background. Most popular Reels style.

---

## Template 3: Karaoke / Word-by-Word Highlight

Shows words one at a time — great for music reels. Generate multiple drawtext lines:

```python
# Python generator for karaoke-style captions
words = [("Hello", 0, 0.5), ("World", 0.5, 1.0), ("This", 1.0, 1.5), ("Is", 1.5, 2.0), ("Amazing", 2.0, 3.0)]
filters = []
for word, start, end in words:
    filters.append(
        f"drawtext=text='{word}':"
        f"fontfile=/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf:"
        f"fontsize=72:fontcolor=yellow:"
        f"borderw=4:bordercolor=black:"
        f"x=(w-tw)/2:y=(h-th)/2:"
        f"enable='between(t,{start},{end})'"
    )
print(",".join(filters))
```

**Preview:** Dynamic, attention-grabbing. Perfect for lyric/music reels.

---

## Template 4: Top + Bottom Split Text

Title at top, subtitle at bottom — storytelling format.

```
drawtext=text='MAIN TITLE':
  fontfile=/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf:
  fontsize=64:fontcolor=white:
  borderw=4:bordercolor=black:
  x=(w-tw)/2:y=180:
  enable='between(t,START,END)',
drawtext=text='subtitle text here':
  fontfile=/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf:
  fontsize=40:fontcolor=white@0.9:
  borderw=2:bordercolor=black:
  x=(w-tw)/2:y=h-th-200:
  enable='between(t,START,END)'
```

**Preview:** Cinematic, used for recipe/tutorial reels.

---

## Template 5: Neon Glow Text

Bright colored text with a glowing shadow effect.

```
drawtext=text='YOUR TEXT':
  fontfile=/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf:
  fontsize=60:fontcolor=0x00FFFF:
  shadowcolor=0x00FFFF@0.5:shadowx=0:shadowy=0:
  borderw=2:bordercolor=0x00FFFF@0.3:
  x=(w-tw)/2:y=(h-th)/2:
  enable='between(t,START,END)',
drawtext=text='YOUR TEXT':
  fontfile=/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf:
  fontsize=60:fontcolor=white:
  x=(w-tw)/2:y=(h-th)/2:
  enable='between(t,START,END)'
```

**Colors:** Cyan `0x00FFFF`, Pink `0xFF00FF`, Green `0x00FF00`, Orange `0xFF6600`

**Preview:** Nightlife/party aesthetic. Double-layered for glow effect.

---

## Template 6: Gradient Background Bar

Text on a full-width gradient bar.

```
drawbox=x=0:y=h-200:w=w:h=120:color=black@0.7:t=fill:
  enable='between(t,START,END)',
drawtext=text='YOUR TEXT HERE':
  fontfile=/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf:
  fontsize=48:fontcolor=white:
  x=(w-tw)/2:y=h-180:
  enable='between(t,START,END)'
```

**Preview:** Clean lower-third style. Professional look.

---

## Template 7: Typewriter Reveal

Text appears character by character. Use Python to generate:

```python
text = "This is typewriter effect"
fps = 30
chars_per_sec = 12
filters = []
for i in range(1, len(text) + 1):
    start = (i - 1) / chars_per_sec
    end = i / chars_per_sec
    partial = text[:i].replace("'", "'\\\\\\''")
    if i == len(text):
        end = 10  # total display end time
    filters.append(
        f"drawtext=text='{partial}':"
        f"fontfile=/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf:"
        f"fontsize=52:fontcolor=white:"
        f"borderw=3:bordercolor=black:"
        f"x=(w-tw)/2:y=h-th-250:"
        f"enable='between(t,{start:.3f},{end:.3f})'"
    )
print(",\n".join(filters))
```

**Preview:** Engaging, builds suspense. Great for quotes and hooks.

---

## Template 8: Pop-Up Bouncy (Animated Scale)

Text pops in with a scale animation. Uses `fontsize` expression:

```
drawtext=text='YOUR TEXT':
  fontfile=/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf:
  fontsize='if(between(t,START,START+0.3),56*(1+0.5*sin(2*PI*(t-START)/0.3)),56)':
  fontcolor=white:
  borderw=3:bordercolor=black:
  x=(w-tw)/2:y=(h-th)/2:
  enable='between(t,START,END)'
```

**Preview:** Fun, energetic. Great for comedy/lifestyle reels.

---

## Template 9: Stacked Multi-Line with Background

Multiple lines centered with a rounded-look background panel.

```
drawbox=x=(w-700)/2:y=(h-250)/2:w=700:h=250:
  color=0x1a1a2e@0.85:t=fill:
  enable='between(t,START,END)',
drawtext=text='LINE ONE':
  fontfile=/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf:
  fontsize=52:fontcolor=0xE94560:
  x=(w-tw)/2:y=(h-250)/2+30:
  enable='between(t,START,END)',
drawtext=text='LINE TWO':
  fontfile=/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf:
  fontsize=40:fontcolor=white:
  x=(w-tw)/2:y=(h-250)/2+100:
  enable='between(t,START,END)',
drawtext=text='LINE THREE':
  fontfile=/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf:
  fontsize=36:fontcolor=white@0.7:
  x=(w-tw)/2:y=(h-250)/2+160:
  enable='between(t,START,END)'
```

**Preview:** Presentation/quote style. Branded aesthetic.

---

## Template 10: Cinematic Letterbox + Subtitle

Black letterbox bars top/bottom with subtitle text — movie feel.

```
drawbox=x=0:y=0:w=w:h=160:color=black:t=fill,
drawbox=x=0:y=h-160:w=w:h=160:color=black:t=fill,
drawtext=text='YOUR CINEMATIC TEXT':
  fontfile=/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf:
  fontsize=44:fontcolor=white@0.95:
  borderw=2:bordercolor=black:
  x=(w-tw)/2:y=h-280:
  enable='between(t,START,END)'
```

**Preview:** Film/trailer aesthetic. Great for dramatic/travel reels.

---

## Using Captions with SRT Subtitles (Auto-Generated)

```bash
# Template 1 style (clean white)
ffmpeg -i video.mp4 -vf "subtitles=captions.srt:force_style='FontName=Noto Sans,FontSize=24,PrimaryColour=&Hffffff,OutlineColour=&H000000,Outline=2,Shadow=1,Alignment=2,MarginV=250'" OUTPUT_FLAGS output.mp4

# Template 2 style (box background)
ffmpeg -i video.mp4 -vf "subtitles=captions.srt:force_style='FontName=Noto Sans,FontSize=22,PrimaryColour=&Hffffff,BackColour=&H80000000,BorderStyle=4,Outline=0,Shadow=0,Alignment=2,MarginV=250'" OUTPUT_FLAGS output.mp4

# Template 5 style (neon)
ffmpeg -i video.mp4 -vf "subtitles=captions.srt:force_style='FontName=Noto Sans Bold,FontSize=26,PrimaryColour=&H00FFFF,OutlineColour=&H00FFFF80,Outline=3,Shadow=2,ShadowColour=&H00FFFF40,Alignment=2,MarginV=200'" OUTPUT_FLAGS output.mp4

# Template 10 style (cinematic)
ffmpeg -i video.mp4 -vf "subtitles=captions.srt:force_style='FontName=Noto Sans,FontSize=22,PrimaryColour=&Hffffff,OutlineColour=&H000000,Outline=2,Shadow=0,Alignment=2,MarginV=180,Italic=1'" OUTPUT_FLAGS output.mp4
```

---

## Combining Caption Templates

Stack multiple drawtext filters for rich multi-element captions:

```
drawtext=text='RECIPE':fontsize=72:fontcolor=yellow:borderw=4:bordercolor=black:x=(w-tw)/2:y=150:enable='between(t,0,3)',
drawtext=text='Pasta Carbonara':fontsize=48:fontcolor=white:borderw=2:bordercolor=black:x=(w-tw)/2:y=240:enable='between(t,0.5,3)',
drawtext=text='Step 1 of 5':fontsize=32:fontcolor=white@0.7:x=(w-tw)/2:y=h-200:enable='between(t,0,5)'
```
