# Caption Styles Reference

## Preset Categories & IDs

### Viral
| ID | Name | Key Feature |
|----|------|-------------|
| `viral-center` | Viral Center | Golden highlight, lift animation, center position |
| `hormozi-style` | Hormozi Style | Bold yellow bg on active word, punch animation |
| `mr-beast-style` | MrBeast Style | Hot pink bg, bounce animation, comic font |
| `comic-pop` | Comic Pop | Speech bubble style, white bg, black border |

### Clean
| ID | Name | Key Feature |
|----|------|-------------|
| `classic-subtitle` | Classic Subtitle | Simple white + black stroke, no active word |
| `clean-highlight` | Clean Highlight | Golden bg on active word, lift animation |
| `sky-word` | Sky Word | Blue bg on active word, bounce animation |
| `paper-classic` | Paper Classic | White bg bar, blue active word color |
| `clean-minimal-pro` | Clean Minimal Pro | Wide letter-spacing, glow active word |
| `netflix-bold` | Netflix Bold | Black bg bar, bold, streaming style |
| `full-sentence` | Full Sentence | Static reveal, gold active word color |

### Social
| ID | Name | Key Feature |
|----|------|-------------|
| `highlighter-pro` | Highlighter Pro | Yellow highlighter on active word |
| `pill-pop` | Pill Pop | Rounded pill bg (indigo) on active word |
| `karaoke-style` | Karaoke Style | Gray→cyan color change, no bg highlight |
| `single-word-focus` | Single Word Focus | One word at a time, pop animation |
| `single-word-instant` | Single Word Instant | One word at a time, no animation |

### Cinematic
| ID | Name | Key Feature |
|----|------|-------------|
| `editorial-luxe` | Editorial Luxe | Serif (Fraunces), no active word highlight |
| `cinema-minimal` | Cinema Minimal | Garamond serif, elegant film subtitle |
| `documentary` | Documentary | Dark bg bar, gold active word glow |
| `cinematic-film` | Cinematic Film | Playfair Display serif, classic movie |
| `minimal-style` | Minimal Style | Small Garamond, no highlight, low position |

### Modern
| ID | Name | Key Feature |
|----|------|-------------|
| `studio-sans` | Studio Sans | Space Grotesk, indigo bg, elastic animation |
| `gradient-style` | Gradient Style | Purple→pink gradient text |
| `gradient-word` | Gradient Word | Purple bg on active word, glow animation |
| `glass-blur` | Glass Blur | Frosted glass bg, white border |
| `ethereal-glow` | Ethereal Glow | Multi-layer white glow, dreamy |
| `sunset-gradient` | Sunset Gradient | Gold→coral gradient text |
| `metallic-pro` | Metallic Pro | Cyan→magenta gradient text |
| `metallic-silver` | Metallic Silver | White→gray gradient text |

### Expressive
| ID | Name | Key Feature |
|----|------|-------------|
| `mono-studio` | Mono Studio | IBM Plex Mono, emerald bg, punch |
| `neon-glow` | Neon Glow | Orbitron font, cyan 4-layer neon glow |
| `retro-stack` | Retro Stack | Oswald, 3D offset shadows, gold text |
| `brush-stroke` | Brush Stroke | Emerald bg, elastic animation |
| `typewriter-script` | Typewriter Script | Caveat handwriting, typewriter reveal |

---

## CaptionStyleSettings Schema

### Typography
| Field | Type | Description |
|-------|------|-------------|
| `fontSize` | number | Font size in pixels (38–56 typical) |
| `fontFamily` | string | Font name (Inter, Anton, Bangers, Poppins, etc.) |
| `fontWeight` | string | Weight: "400"–"900" |
| `color` | string | Text color (hex or rgba) |
| `letterSpacing` | number | Letter spacing in px |
| `wordSpacingPx` | number | Space between words |
| `lineHeight` | number | Line height multiplier |
| `textAlign` | string | "center" | "left" | "right" |

### Text Fill & Gradient
| Field | Type | Description |
|-------|------|-------------|
| `textFillStyle` | string | "solid" or "gradient" |
| `textGradientFrom` | string | Start color for gradient text |
| `textGradientTo` | string | End color for gradient text |
| `textGradientAngleDeg` | number | Gradient angle in degrees |
| `textGradientColorSpace` | string | "oklch" for smooth gradients |
| `shadowMode` | string | null or "drop-shadow" (required for gradient text shadows) |

### Stroke
| Field | Type | Description |
|-------|------|-------------|
| `textStrokeEnabled` | boolean | Enable text outline |
| `textStrokeColor` | string | Stroke color |
| `textStrokeWidthPx` | number | Stroke width (1–5 typical) |
| `textStrokeBlurPx` | number | Stroke blur |

### Background & Position
| Field | Type | Description |
|-------|------|-------------|
| `backgroundColor` | string | Caption box background |
| `borderRadius` | number | Corner rounding in px |
| `border` | string | CSS border (e.g., "3px solid #000") |
| `position` | string | "top" | "bottom" |
| `customPositionY` | number | Y position as % (50=center, 75=lower) |
| `paddingPx` | number | Padding inside caption box |
| `backgroundGlowColor` | string | Glow behind caption box |
| `backgroundGlowBlurPx` | number | Glow blur radius |

### Active Word Highlighting
| Field | Type | Description |
|-------|------|-------------|
| `showActiveWord` | boolean | Enable active word highlight |
| `activeWordColor` | string | Text color of active word |
| `activeWordBackgroundColor` | string | Background color of active word |
| `activeWordAnimation` | enum | Animation on active word (see below) |
| `activeWordHoldMs` | number | Hold duration in ms after word ends |

### Reveal & Layout
| Field | Type | Description |
|-------|------|-------------|
| `wordRevealAnimation` | enum | How words appear (see below) |
| `revealMode` | string | "sequential" | "single" | "static" |
| `wordsPerLineLimit` | number | Max words per line |
| `maxLinesPerCaption` | number | Max lines shown at once (1–2) |
| `pageCombineMs` | number | Group words within this window into one page |

### Emphasis System
| Field | Type | Description |
|-------|------|-------------|
| `emphasisEnabled` | boolean | Enable auto-emphasis |
| `autoEmphasisDetection` | boolean | Auto-detect emphasis words |
| `emphasisPatterns` | string[] | Detection patterns: "numbers", "caps", "exclamations" |
| `emphasisScale` | number | Scale multiplier (1.1–1.2 typical) |
| `emphasisColor` | string | Override color for emphasis words |
| `emphasisFontWeight` | string | Override font weight |
| `emphasisRotationDeg` | number | Slight rotation for emphasis |
| `emphasisBackgroundColor` | string | Override background |

---

## Active Word Animations

`highlight` · `scale` · `glow` · `lift` · `bounce` · `punch` · `slam` · `elastic` · `shake` · `none`

## Word Reveal Animations

`none` · `fade` · `scale` · `slide-up` · `pop` · `drop` · `slam` · `typewriter` · `glitch` · `mask-reveal` · `bounce-up` · `split-reveal`

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/projects/{id}/captions/style` | Get current caption style |
| PATCH | `/projects/{id}/captions/style` | Update caption style settings |
| POST | `/projects/{id}/captions` | Apply preset by `style_id` |
| GET | `/projects/{id}/captions` | List caption blocks |
| GET | `/projects/{id}/captions/{captionId}` | Get one caption block with words |
| PATCH | `/projects/{id}/captions/{captionId}` | Replace caption block text |
| GET | `/projects/{id}/captions/words` | List caption words, optionally filtered by `timeline_item_id` or `match_text` |
| POST | `/projects/{id}/captions/words/text` | Update one caption word by `word_id` |
| POST | `/projects/{id}/captions/words/delete` | Delete caption words |
| POST | `/projects/{id}/captions/words/merge` | Merge contiguous caption words |
| POST | `/projects/{id}/captions/words/split` | Split a caption word |
| POST | `/projects/{id}/captions/words/emphasis` | Set emphasis on specific words |
| POST | `/projects/{id}/captions/words/style` | Set per-word style overrides |

Caption-block CRUD is project-scoped. Do not call guessed global routes such as `/captions/{captionId}` or guessed preset routes such as `/projects/{id}/captions/presets`. Use project context to find the caption timeline item and its `captionId`, then patch `/projects/{id}/captions/{captionId}` or list/update words by `timeline_item_id` and `word_id`.
