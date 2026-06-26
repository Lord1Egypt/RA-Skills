---
name: recursive-maths-animator
description: Recursive maths animator — Manim-based technical animations with optional voiceover (manim-voiceover), git scene versioning, pinned requirements, asset folders, GIF approval previews, and a vision verification loop (frame extract, multimodal review in Cursor/Claude Code, VERIFICATION_FEEDBACK.md, iterate). Brief-first workflow: pitch a digestible animation plan and design options, get user approval, then code; lock theme in DESIGN_THEME.md.
---

# Recursive maths animator (Manim + voiceover + verification)

This skill ships helper code under `references/` (palette, optional Gemini TTS adapter, `manim_versioning.ManimProject`) and utilities under `scripts/`. Agents should point users at those paths when generating projects.

## Brief-first workflow (do this before any scene code)

Many users want something **cool, shareable, and minimal** — not a wall of technical detail. **Do not** jump straight to `project.init()` + a full scene unless the user explicitly says “just build it.”

1. **Digestible pitch first** — In chat, give a **short** animation brief: one-line takeaway, 3–5 **beats** (what appears, in order, rough seconds each), and why it fits Manim (motion, not static slides). Keep it skimmable; no long tables of API names unless they ask.
2. **Offer choices** — Present **2–3 palette options** from the built-in design systems (see below). Use letter labels the user can reply with:

   - **A — Swiss grid** (Inter, clinical, data-forward)
   - **B — Bauhaus primary** (Space Grotesk, geometric, educational)
   - **C — Braun minimal** (Work Sans, warm gray, product)
   - **D — Editorial bold** (Playfair + Inter, dramatic, storytelling)
   - **E — Apple precision** (DM Sans, cool, tech)
   - **F — Soft enterprise** (Roboto, warm cream — existing default)

   Also offer **aspect ratio** (16:9, 1:1, 9:16) and **tone** (calm / punchy). Let the user pick or mix.
3. **Wait for approval** — Only after the user confirms (or says “use A + 1:1 + calm”) do you: write **`ANIMATION_BRIEF.md`** (filled) + **`DESIGN_THEME.md`** (locked), then implement the scene.
4. **Use the maths engine** — Prefer Manim-native motion: `MathTex` / `Tex`, `NumberPlane`, `ParametricFunction`, `Transform` / `ReplacementTransform`, `Indicate`, `ShowPassingFlash`, `LaggedStart`, updaters. Avoid “generic UI explainer” unless that is what they asked for. See **`references/manim_guide.md`** for patterns.
5. **Shareable quality** — **MP4 at `-qh` / `--quality h`** is the default deliverable for “looks good.” GIF is for **layout checks** only; re-encoding with aggressive `ffmpeg` **crushes** gradients and dark minimal palettes. If they need a small GIF, render a **short** clip, limit colors in the scene, or share **MP4** / link instead.

`ManimProject.init()` seeds **`ANIMATION_BRIEF.md`** with a template; agents replace “DRAFT” content after approval.

## Operating principles (do these every time)

1. **Design theme + brief** — After the user approves the pitch, record mood, light/dark, chosen **design system** (swiss / bauhaus / braun / editorial / apple / soft), typography, motion, deliverable size, and brand assets in `DESIGN_THEME.md`. Keep the approved story in `ANIMATION_BRIEF.md`.
2. **Pinned dependencies** — Every project keeps a root **`requirements.txt`** (seeded on `init()` from this skill’s template). When you add imports or optional stacks (e.g. Gemini), **update `requirements.txt`** and tell the user to `pip install -r requirements.txt`. For reproducible CI, suggest `pip freeze > requirements.lock.txt` after upgrades.
3. **Assets live in `assets/`** — Put images, SVGs, and custom fonts under `assets/images`, `assets/svgs`, `assets/fonts`. Keep `scenes/` for Python only so diffs stay readable.
4. **Optional GIF before final MP4** — When stakeholders need a quick motion check in chat, produce a **low-quality GIF** (`ManimProject.render_approval_gif("scene_1")` or `render(..., output_format="gif", export_approval_copy=True)`). If the user prefers to go straight to MP4 (e.g. silent cut with voiceover added later), **skip the GIF** and render MP4 directly. After any GIF sign-off, render **`output_format="movie"`** (MP4; see Rendering — Manim uses `--format mp4`).
5. **Verify with vision, then iterate** — After each substantive render, run the **verification loop** below: slice frames, review with the host model’s **vision**, write `VERIFICATION_FEEDBACK.md`, fix Manim code, re-render. Prefer **MP4** for final verification passes; **GIF** is acceptable for quick layout checks.

## Requirements

- **Python** 3.9+
- **manim** — `pip install manim` (versions pinned in project `requirements.txt`)
- **manim-voiceover** with a TTS backend — e.g. `pip install "manim-voiceover[gtts]"` (uses network for gTTS unless you switch engine)
- **ffmpeg** and **ffprobe** — with `libx264` and `libass` if you burn subtitles (see `scripts/run_pipeline.py`); **ffprobe** is required for `extract_verification_frames.py`
- **git** — for `ManimProject` versioning commands

Optional:

- **google-genai** — only if using `references/gemini_tts_service.py` (set `GEMINI_API_KEY`); uncomment in `requirements.txt` when used.

## Using `references/` from your project

The installable skill is the **directory that contains `SKILL.md`** (often `.../recursive-maths-animator/` inside a Git clone), not the repository root above it. If the host says “unknown skill,” confirm that path ends with `recursive-maths-animator/SKILL.md`.

The Quick Start imports `ManimProject` from `manim_versioning`. Add this skill’s `references` directory to `sys.path` (or copy the files into your repo).

```python
from pathlib import Path
import sys

# Path to the installed skill’s references/ folder (adjust if you symlink or copy the skill).
# Cursor (user-wide): ~/.cursor/skills/recursive-maths-animator/references
# Claude Code (user-wide): ~/.claude/skills/recursive-maths-animator/references
SKILL_REF = Path.home() / ".cursor/skills/recursive-maths-animator/references"
# SKILL_REF = Path("path/to/recursive-maths-animator/references")

sys.path.insert(0, str(SKILL_REF.resolve()))
from manim_versioning import ManimProject
```

Scene files should use the same pattern so `soft_enterprise_palette` and optional `gemini_tts_service` resolve:

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "references"))
```

(Adjust the relative path if your layout differs.)

## Quick Start

```python
from pathlib import Path
import sys

REF = Path("/path/to/recursive-maths-animator/references").resolve()
sys.path.insert(0, str(REF))
from manim_versioning import ManimProject

project = ManimProject("my_animation")
project.init()  # Creates git repo, scenes/ folder, structure

# Create Scene 1
project.create_scene("scene_1", """
class Scene1(Scene):
    def construct(self):
        # Your animation code
        pass
""")

# Render and commit
project.render("scene_1")  # Auto-commits as "scene_1 v1"

# Make changes, create new version
project.update_scene("scene_1", "# updated code...")
project.render("scene_1")  # Auto-commits as "scene_1 v2"

# Rollback if needed
project.rollback("scene_1", version=1)  # Restores v1

# Create provisional branch for review
project.branch("scene_1", "review-alice")  # Creates branch, doesn't affect main
```

## Project structure

After `ManimProject.init()`, the layout includes dependency and theme files plus asset and approval folders:

```
my_animation/
├── .git/
├── requirements.txt       # Pinned Manim / voiceover; extend when you add packages
├── ANIMATION_BRIEF.md     # Short pitch + beats + approved choices (before / while coding)
├── DESIGN_THEME.md        # User’s theme answers — fill after approval, before heavy code
├── assets/
│   ├── README.md
│   ├── images/
│   ├── svgs/
│   └── fonts/
├── VERIFICATION_FEEDBACK.md   # Latest multimodal review output (agent-written; optional until first review)
├── exports/
│   ├── approvals/         # GIF (or other) previews for sign-off
│   └── verification/    # Frame slices + manifest.json per run (see extract script)
├── scenes/
│   ├── scene_1/
│   │   ├── scene_1.py
│   │   ├── versions/
│   │   │   ├── v1.py
│   │   │   └── v2.py
│   │   └── branches/
│   │       └── review-alice/
│   ├── scene_2/
│   └── shared/
│       ├── palette.py
│       └── utils.py
├── media/
│   ├── scene_1_v2.mp4
│   └── scene_1_v2.gif     # when you render GIF previews
└── project.json
```

## Versioning commands

| Action | Command | Result |
|--------|---------|--------|
| Initialize project | `project.init()` | Git repo + folder structure |
| Create scene | `project.create_scene(name, code)` | Scene file + initial commit |
| Update scene | `project.update_scene(name, code)` | New version committed |
| Render | `project.render(name)` | Video + auto-commit |
| List versions | `project.versions(name)` | Shows v1, v2, v3... |
| Rollback | `project.rollback(name, version)` | Restores code to version |
| Create branch | `project.branch(name, branch_name)` | Provisional copy |
| Merge branch | `project.merge(name, branch_name)` | Merges into main |
| Compare | `project.diff(name, v1, v2)` | Shows code differences |
| Tag approved | `project.tag(name, version, "approved")` | Marks final version |

## Provisional branch workflow

```python
project.update_scene("scene_1", "# version 1 code")
project.render("scene_1")

project.branch("scene_1", "alt-animation")
project.update_scene("scene_1", "# alternative code", branch="alt-animation")
project.render("scene_1", branch="alt-animation")

# Review outputs, then merge or delete_branch as needed
project.merge("scene_1", "alt-animation")
```

## Scene templates

### Using a built-in design system (recommended)

```python
"""
SCENE {N}: {TITLE}
{Description}
~{duration}s, {orientation}
Design system: {scheme}
"""

import sys
sys.path.insert(0, '{project_path}/references')

from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService

# Import the chosen design system (example: swiss)
from design_systems.swiss_international import SwissScene, SwissColors, EASE_SWISS_SNAP


class Scene{N}_{Title}(SwissScene):
    """{Description}"""

    def __init__(self, **kwargs):
        config.pixel_width = {width}
        config.pixel_height = {height}
        config.frame_width = {frame_w}
        config.frame_height = {frame_h}
        config.frame_rate = 60

        super().__init__(**kwargs)

        self.set_speech_service(GTTSService(lang='en', slow=True))

    def construct(self):
        self.setup_swiss_background()

        section_title = self.make_heading("{SECTION_TITLE}")
        section_title.to_edge(UP, buff=0.5)
        self.add(section_title)

        with self.voiceover(
            text="{VOICEOVER_LINE_1}"
        ) as tracker:
            pass

        self.wait(0.5)


if __name__ == "__main__":
    config.quality = "high_quality"
    scene = Scene{N}_{Title}()
    scene.render()
```

### Legacy: voiceover + soft palette (no design system)

```python
"""
SCENE {N}: {TITLE}
{Description}
~{duration}s, {orientation}
"""

import sys
sys.path.insert(0, '{project_path}/references')

from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService
from default_typography import DEFAULT_FONT
from soft_enterprise_palette import SoftColors, EASE_GAS_SPRING


class Scene{N}_{Title}(VoiceoverScene):
    """{Description}"""

    def __init__(self, **kwargs):
        config.pixel_width = {width}
        config.pixel_height = {height}
        config.frame_width = {frame_w}
        config.frame_height = {frame_h}
        config.frame_rate = 60

        super().__init__(**kwargs)

        self.set_speech_service(GTTSService(lang='en', slow=True))

    def construct(self):
        bg = Rectangle(
            width=config.frame_width,
            height=config.frame_height,
            fill_color=SoftColors.BACKGROUND,
            fill_opacity=1
        )
        self.add(bg)

        section_title = Text(
            "{SECTION_TITLE}",
            font=DEFAULT_FONT,
            font_size=14,
            color=SoftColors.TEXT_SECONDARY
        )
        section_title.to_edge(UP, buff=0.5)
        self.add(section_title)

        with self.voiceover(
            text="{VOICEOVER_LINE_1}"
        ) as tracker:
            pass

        self.wait(0.5)

    def create_token(self, text, is_active=False):
        token = Text(
            text,
            font=DEFAULT_FONT,
            font_size=24,
            color=SoftColors.TEXT_PRIMARY if is_active else SoftColors.TEXT_SECONDARY,
            weight=MEDIUM
        )

        if is_active:
            bg = RoundedRectangle(
                corner_radius=0.12,
                width=token.width + 0.35,
                height=token.height + 0.25,
                fill_color=SoftColors.CONTAINER,
                fill_opacity=0.85,
                stroke_color=SoftColors.BORDER,
                stroke_width=1
            )
            bg.move_to(token.get_center())
            token = VGroup(bg, token)

        return token


if __name__ == "__main__":
    config.quality = "high_quality"
    scene = Scene{N}_{Title}()
    scene.render()
```

## Design systems

Five built-in designer-inspired aesthetic systems live under `references/design_systems/`. Each is a complete module (colors, typography, motion, containers, background, base scene) following the same API as `soft_enterprise_palette.SoftEnterpriseScene`.

| Key | Name | Designer / Movement | Primary Font | Mood |
|-----|------|---------------------|--------------|------|
| `swiss` | Swiss International | Josef Müller-Brockmann | Inter | Strict grid, clinical precision, black/white + restrained red |
| `bauhaus` | Bauhaus Modern | Herbert Bayer | Space Grotesk | Geometric, primary colors, functional art |
| `braun` | Braun Minimal | Dieter Rams | Work Sans | Warm light grays, systematic, "less but better" |
| `editorial` | Editorial Bold | Paula Scher / Pentagram | Playfair Display + Inter | Dramatic scale contrast, deep navy + warm cream |
| `apple` | Apple Precision | Jony Ive | DM Sans | Cool neutrals, generous whitespace, sleek motion |
| `soft` | Soft Enterprise | Skill default | Roboto | Warm cream, dot grid, gas-spring easing |

**Import a system directly:**

```python
import sys
sys.path.insert(0, 'path/to/references')
from design_systems.swiss_international import SwissScene, SwissColors, EASE_SWISS_SNAP
```

**Or use the registry:**

```python
from design_systems import get_scheme, get_scene_class
SceneClass = get_scene_class("swiss")   # -> SwissScene
```

**Fonts are downloaded on demand:**

```python
from design_systems.font_catalog import install_fonts
install_fonts("swiss", target_dir="assets/fonts")
```

All fonts are SIL Open Font License (OFL) 1.1 and freely redistributable. `ManimProject.init(scheme="swiss", install_fonts=True)` can download fonts automatically at project creation.

## Soft enterprise palette

Defined in `references/soft_enterprise_palette.py` — import `SoftColors` and `EASE_GAS_SPRING` after adding `references` to `sys.path`.

**Default font:** `references/default_typography.py` defines `DEFAULT_FONT` (**Roboto**) for all `Text()` unless the user overrides in `DESIGN_THEME.md`.

## Rendering

Manim Community expects **`--format mp4`** (or `gif`, `webm`, etc.), not `movie`. The word “movie” in docs means “video file”; `ManimProject.render(..., output_format="movie")` maps to `--format mp4` internally.

For **shareable, high-quality** output, prefer **`--quality h`** (or `-qh`) MP4. Post-processing GIF with heavy palette reduction often looks **worse** than the source MP4 — especially dark or gradient minimal styles.

```bash
# Draft MP4
manim -ql scene.py SceneClass --format mp4 --disable_caching

# Stakeholder approval GIF (small, easy to share)
manim -ql scene.py SceneClass --format gif --disable_caching

# High quality final MP4
manim -qh scene.py SceneClass --format mp4 --disable_caching

# Versioning helper — final pass (still uses output_format="movie" in Python = MP4 on CLI)
project.render("scene_1", quality="high", output_format="movie")

# Versioning helper — approval GIF into exports/approvals/ (no auto-commit)
project.render_approval_gif("scene_1")
```

If your Manim build errors on `--format`, upgrade Manim (Community ≥ 0.18) or use a two-step pipeline: render draft MP4, then `ffmpeg` to GIF (document in project README if needed).

## Verification loop (required after substantive renders)

This skill does **not** call cloud LLM APIs from Python. **Cursor** or **Claude Code** performs multimodal review using extracted stills.

### When to run

- After any render that changes **layout, copy, colors, or story beats** (including a new GIF approval cut).
- **Final checks** should use a **full-quality MP4** when possible; GIFs are fine for early layout passes.

### Step 1 — Extract frames

From the **animation project root** (or pass `--cwd`), run:

```bash
python3 path/to/recursive-maths-animator/scripts/extract_verification_frames.py path/to/render.mp4
```

Optional: `--count 10`, `--format png`, `--output-dir exports/verification/my_run`.

This writes a timestamped folder under `exports/verification/` with JPEG/PNG frames and **`manifest.json`** (`t_seconds`, `pct`, `filename` per frame).

### Step 2 — Multimodal review (host agent)

1. Read **`manifest.json`** and open **every** extracted frame (vision).
2. Read **`DESIGN_THEME.md`** and the agreed **storyboard / scene plan** (what each beat must prove).
3. Apply [`references/video_verification_rubric.md`](references/video_verification_rubric.md): padding and safe margins, typography (including font vs `DESIGN_THEME.md`), **text alignment and overlap**, theme colors, **logical progression** vs plan, motion hints between samples, glitches.

### Step 3 — Write `VERIFICATION_FEEDBACK.md` (project root)

Use this structure:

```markdown
# Verification feedback

## Verdict
PASS | PASS_WITH_ISSUES | FAIL

## Summary
2–4 sentences. Must include at least one sentence on **text alignment** (e.g. columns, baselines, multi-line blocks) and one on **overlap / clutter** (text vs arrows/shapes, cramped `buff=`).

## Layout (alignment & overlap)
- Alignment: …
- Overlap / clutter: …

## Issues
### P0 — (title)
- Evidence: frame `frame_03_...jpg` — t=…s, pct=…%
- Expected: …
- Observed: …
- Suggested fix: … (Manim: e.g. `buff=`, `to_edge`, `shift`, color constant, reorder `play`)

### P1 — …

## Next iteration
Ordered list of edits to the scene file(s), then re-render and re-run extraction.
```

### Step 4 — Iterate

1. Implement **P0** then **P1** (then P2) in Manim source.
2. Re-render the same deliverable type you are validating.
3. Re-run **`extract_verification_frames.py`** on the new file (new output folder preserves history).
4. Repeat until **Verdict is PASS** or **PASS_WITH_ISSUES** with only acceptable P2 items.

**Round cap:** default **3** full verify cycles unless the user explicitly asks for more.

## Pipeline helper (optional)

`scripts/run_pipeline.py` wraps render + optional subtitle burn-in. `scripts/check_environment.py` verifies common dependencies.

## Output locations

- **Draft**: `media/videos/scene_1/480p15/Scene1.mp4`
- **Final**: `media/videos/scene_1/1080p60/Scene1.mp4`
- **Versioned**: `media/scene_1_v{N}.mp4` (when using `ManimProject`; see implementation)

## Best practices

1. **Theme in writing** — `DESIGN_THEME.md` should reflect what the user agreed to; link palette choices to the chosen design system (e.g. `SwissColors`, `BauhausColors`) or a project palette module under `scenes/shared/`.
2. **Requirements drift** — Any new `pip` dependency must appear in `requirements.txt` the same change set.
3. Version deliberately: use commits per meaningful **final** render; GIF previews may skip auto-commit (see `render_approval_gif`).
4. Use branches for experiments before merging to main line.
5. Tag approvals when a cut is final (`project.tag(...)`).
6. Keep scenes independently renderable.
7. Shared utilities live under `scenes/shared/`; binaries only under `assets/`.
8. Keep voiceover text TTS-friendly (plain punctuation, avoid noisy symbols).
9. Target ~10–15s per scene for short-form vertical if that is the deliverable.
10. **Close the verification loop** — Do not treat a render as done until frames are extracted and `VERIFICATION_FEEDBACK.md` records a PASS (or user accepts PASS_WITH_ISSUES).
11. **Pitch before pixels** — For creative or “explainer” requests, use the **Brief-first workflow** so palette and story match what the user considers “cool” before you invest in a long scene file.

## Automated sandbox reports (VirusTotal Zenbox, etc.)

If a **dynamic** scan of the skill zip shows subprocesses, `python.exe`, `cmd.exe`, **non-standard ports**, or **URLs** such as `http://192.168.x.x:…/v1/…`, treat the overall **verdict and score** first: this package is **documentation + optional Manim helpers**; it does **not** embed a C2 server or obfuscated payloads. Strings like **`/v1/chat/completions`** in memory usually come from **the analyzer environment** (local model proxy), not from files in this skill. Heuristic “injection” or “non-standard port” flags are common for **any** stack that runs `subprocess` + Python + optional HTTP clients (e.g. gTTS). Compare the zip to this repository when in doubt.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Git not initialized | Run `project.init()` first |
| Import errors for helpers | Add this skill’s `references/` to `sys.path` or copy files into your project |
| Branch merge conflict | Resolve in scene file, then commit via project helpers |
| Cache issues | Use `--disable_caching` |
| TTS / API limits | Fall back to gTTS or another `SpeechService` |
| `ffprobe` / frame extract fails | Install full `ffmpeg` package; ensure `ffprobe` is on `PATH` |
| Empty or black frames | Re-sample with higher `--count` or inspect source video; check `-ss` timing |
| GIF looks muddy / banded after `ffmpeg` | Deliver **MP4** for final share; shorten the clip, simplify palette in Manim, or use gentler GIF settings — do not treat crushed GIF as the only artifact |

## Optional follow-on

- **Remotion** or other compositors for captions, UI chrome, or multi-track polish.
- **General video editing** (FFmpeg, DaVinci, etc.) for final assembly.
