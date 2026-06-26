# ASS Subtitle Effects Reference

Quick reference for ASS override tags used in the subtitle generation script.

## Color System

ASS uses **BGR** format (not RGB): `&HBBGGRR&`

| Color Name | ASS Code     | Visual  |
|-----------|-------------|---------|
| White     | `&HFFFFFF&` | Default text |
| Yellow    | `&H00FFFF&` | Primary highlight |
| Red       | `&H0000FF&` | Strong emphasis |
| Cyan      | `&HFFFF00&` | Secondary highlight |
| Green     | `&H00FF00&` | Positive/success |
| Orange    | `&H0080FF&` | Warning |
| Blue      | `&HFF0000&` | Cool tone |

## Override Tags

### Text Styling
```
{\b1}         Bold on
{\b0}         Bold off
{\i1}         Italic on
{\fs48}       Font size 48
{\fn字体名}    Font face
{\c&H00FFFF&} Primary text color (yellow in BGR)
{\c}          Reset to default color
{\3c&H000000&} Outline color
{\4c&H000000&} Shadow color
```

### Border & Shadow
```
{\bord3}      Outline width 3px
{\shad2}      Shadow depth 2px
{\xbord3}     X-axis outline
{\ybord3}     Y-axis outline
{\xshad2}     X-axis shadow
{\yshad2}     Y-axis shadow
```

### Position & Alignment
```
{\an2}        Bottom center (default for subtitles)
{\an5}        Middle center
{\an8}        Top center
{\pos(x,y)}   Exact position
```

Alignment numpad layout:
```
7  8  9   ← top
4  5  6   ← middle
1  2  3   ← bottom
```

### Animation & Effects

#### Fade
```
{\fad(fadein_ms, fadeout_ms)}
{\fad(150,0)}           Fade in 150ms, no fade out
{\fad(200,200)}         Fade in/out 200ms each
```

#### Scale Bounce (keyword emphasis)
```
{\t(0,150,\fscx130\fscy130)\t(150,300,\fscx100\fscy100)}
```
This scales text to 130% over 150ms, then back to 100% over the next 150ms.

#### Typewriter / Character Reveal
```
{\alphaFF\t(0,500,\alpha00)}
```
Fades from invisible to visible over 500ms.

#### Shake Effect
```
{\t(0,50,\shad5)\t(50,100,\shad2)}
```

#### Rotation
```
{\frz10\t(0,300,\frz0)}     Rotate from 10° to 0° over 300ms
```

### Karaoke (Word-by-word reveal)
```
{\k50}       Highlight word for 500ms (unit = 10ms)
{\kf50}      Smooth fill from left to right
{\ko50}      Outline highlight
```

## Recommended Effect Combinations

### Normal Subtitle
```
{\fad(150,0)\an2\bord3\shad1}Text here
```

### Highlighted Keyword
```
{\fad(150,0)\an2\bord3\shad1}Normal text {\c&H00FFFF&\t(0,150,\fscx125\fscy125)\t(150,300,\fscx100\fscy100)}keyword{\c} more text
```

### Strong Emphasis (Red + Bounce)
```
{\c&H0000FF&\t(0,100,\fscx140\fscy140)\t(100,250,\fscx100\fscy100)\bord4}IMPORTANT{\c\bord3}
```

### Two-Line Subtitle with Break
```
{\fad(150,0)\an2\bord3}First line of text\NSecond line of text
```

## Timing Format

ASS uses `H:MM:SS.CC` (centiseconds, not milliseconds):
- 1.5 seconds = `0:00:01.50`
- 65.3 seconds = `0:01:05.30`
- 3723.99 seconds = `1:02:03.99`

## Style Definition Template

```
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Heiti SC,48,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,3,1,2,20,20,280,1
```

Key fields:
- PrimaryColour: Main text color
- OutlineColour: Border color (usually black)
- BackColour: Shadow color (with alpha, e.g., `&H80000000` = 50% transparent black)
- Bold: -1 = true
- BorderStyle: 1 = outline + shadow
- Outline: outline width in px
- Shadow: shadow depth in px
- Alignment: 2 = bottom center
- MarginV: vertical margin from bottom (280 for 1280 height = ~78% from top)
