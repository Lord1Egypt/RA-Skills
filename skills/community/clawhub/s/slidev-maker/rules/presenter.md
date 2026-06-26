# Slidev Presenter Mode

Presenter view, speaker notes, and timer.

## Accessing Presenter Mode

Press `P` during presentation or navigate to:
```
http://localhost:3030/presenter
```

Presenter view shows:
- Current slide
- Next slide preview
- Speaker notes
- Timer
- Slide navigation

## Speaker Notes

Add notes using HTML comments at the end of a slide:
```markdown
---
layout: default
---

# My Slide

Slide content here.

<!--
These are speaker notes.

They support **Markdown** formatting.

- Bullet points work
- Multiple lines supported
-->
```

Notes MUST be at the end of the slide content, after all other elements.

### Notes Position Matters
```markdown
---

# Slide Title

<!-- This is NOT a note - it's in the middle -->

Content here.

<!-- This IS a note - it's at the end -->
```

Only the last comment block is treated as notes.

## Click Markers in Notes

Highlight sections of notes based on click progress:
```markdown
---

# My Slide

<v-click>Point one</v-click>
<v-click>Point two</v-click>

<!--
Introduction to the topic.

[click] Now explain point one in detail.

[click] Move on to point two.

[click:3] This shows after 3 clicks.
-->
```

The notes panel auto-scrolls and highlights the relevant section.

## Timer

The presenter view includes a built-in timer showing:
- Elapsed time
- Current time

### Timer Controls

- Click timer to pause/resume
- Right-click to reset

### Configure Timer

Set expected duration in headmatter:
```yaml
---
presenter: true
---
```

## Presenter Mode Options

Enable/disable presenter mode:
```yaml
---
presenter: true       # Always enabled (default)
presenter: dev        # Only in development
presenter: build      # Only in production build
presenter: false      # Disabled
---
```

## Remote Control

Access presentation remotely on the same network:
```bash
slidev --remote
```

This displays a QR code and URL for remote access.

### Remote with Password
```bash
slidev --remote=mypassword
```

## Recording

Built-in recording feature for screen and camera:

1. Press `R` or click record button
2. Select screen/camera to record
3. Press `R` again to stop
4. Download recording

Enable/disable recording:
```yaml
---
record: true          # Enabled (default)
record: dev           # Only in development
record: build         # Only in production
record: false         # Disabled
---
```

## Drawing Mode

Press `D` to toggle drawing mode during presentation.

Configure in headmatter:
```yaml
---
drawings:
  enabled: true
  persist: false      # Keep drawings between sessions
  presenterOnly: false # Only presenter can draw
  syncAll: true       # Sync across all clients
---
```

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Space` / `→` / `↓` | Next animation/slide |
| `←` / `↑` | Previous animation/slide |
| `P` | Toggle presenter mode |
| `O` | Toggle overview |
| `D` | Toggle drawing mode |
| `R` | Toggle recording |
| `F` | Toggle fullscreen |
| `G` | Show go-to dialog |
| `Escape` | Exit current mode |

## Dual Screen Setup

1. Open presentation in browser on main display
2. Open `/presenter` URL on secondary display
3. Presenter view syncs automatically with main view

Both views stay synchronized - navigation on either updates both.