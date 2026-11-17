# video-skill-router — AI Video & Animation Skill Router

Want to make a video but don't know which tool to use? Want an AI agent that can **find a skill → install it → produce the video → clean up after itself**? **video-skill-router** is an AI video skill / animation skill meta-skill — the capability discovery & orchestration layer for video/animation creation. You just describe what you need ("turn the Pythagorean theorem into an explainer animation", "make a promo video for my app", "trim the mistakes and silences in this talking-head footage") and it automatically: detects the video category (commercial promo / educational explainer / other) → matches locally installed skills first → discovers and installs from category-specific channels when nothing local fits (built-in curated catalog → live GitHub search → web search) → orchestrates the installed skill to produce the final edited video → then tells you what was installed, what each skill does, and asks whether to keep or uninstall.

The entire install/uninstall lifecycle follows a safety protocol: git snapshot rollback, strict frontmatter validation, explicit choice when multiple packs match, and no `rm -rf`. Built for: content creators, educational YouTubers, e-commerce video teams, and complete beginners who want to make videos with AI and zero pre-installed skills.

[中文说明](./README.md) · **Live docs:** https://guipi888.github.io/video-skill-router/

## The problem it solves

- **Don't know which skill to use for a video**: ships a curated catalog of 11 GitHub-verified skill packs (manim_skill 1201★, motion-design-skill 2441★, OpenMontage 70908★, herk-edit-kit 2017★ …), auto-matched by video category — zero network cost
- **No local capability**: different channels per category — commercial promo packs motion/template/ad skills, educational packs math-animation/data-viz skills, other packs editing/subtitle/voiceover skills, with GitHub + web search as dual fallbacks
- **Can't orchestrate after installing**: reads and drives the installed skill according to its own workflow, fills gaps with FFmpeg, and outputs a finished video directly
- **Skills piling up**: after every run it prints an install manifest (skill / purpose / source) and offers one-command uninstall via `git rm` or trash — rollback-safe, zero residue

Unlike single-engine skills (Manim-only or Remotion-only), this router covers the full pipeline: category detection → discovery → install → orchestration → output.

## Use cases

| Scenario | Example request | Channel |
|----------|----------------|---------|
| Math/science explainer animation | "Turn the Pythagorean theorem proof into an explainer animation" | Educational → manim_skill etc. |
| Product demo & promo video | "Make a product demo promo video for my app" | Commercial → motion-design template skills |
| Talking-head editing | "Trim the mistakes and silences in this talking-head footage" | Other → herk-edit-kit etc. |
| Data visualization video | "Turn this sales data into an animated chart video" | Educational → data animation skills |
| Subtitle & whiteboard animation | "Turn this SRT subtitle into a whiteboard hand-drawn animation" | Other → subtitle animation skills |
| E-commerce short video | "Make a selling video for this product" | Commercial → ad template skills |
| Lottie web animation | "Load a lottie animation on the webpage" | Commercial → motion-design-skill |

## Installation

### WorkBuddy skill market (recommended)

Search "视频创作技能路由器" in WorkBuddy for one-click install.

### Manual

```bash
git clone https://github.com/guipi888/video-skill-router.git \
  ~/.workbuddy/skills/video-skill-router
```

### Requirements

- Python 3.8+ (pure standard library, zero third-party dependencies)
- git (install/uninstall via git snapshots; falls back to a trash mechanism in non-git environments)
- FFmpeg (optional, used as a fallback for missing pipeline steps)

## Usage

After installing, just describe your need to the agent, e.g.:

- "Turn the Pythagorean theorem proof into an explainer animation"
- "Make a product demo promo video for my app"
- "Trim the mistakes and silences in this talking-head footage"

The router handles category detection → matching → download → execution → follow-up automatically — no manual skill selection.

You can also call the three scripts directly:

```bash
# 1. Match (locally installed skills + built-in curated catalog, merged scoring)
python3 scripts/match_skill.py --query "math explainer animation"

# 2. Discover (category-based GitHub channel)
python3 scripts/search_anim.py --category education --query "math animation"

# 3. Install / list / uninstall
python3 scripts/manage_skill.py install --repo shuyicc/MathLens --reason "math explainer"
python3 scripts/manage_skill.py list
python3 scripts/manage_skill.py uninstall --name MathLens
```

## Output

- **Final video**: video files under `video-output/<date>-<topic>/`
- **Follow-up report**: an install manifest table (skill / purpose / source) plus an interactive prompt — reply `1` to keep, `2` to uninstall

## Project structure

```
SKILL.md                          # Router orchestration (5-step pipeline)
data/curated-catalog.json         # Built-in curated catalog (11 packs + 11 engines, GitHub API verified)
references/
  categories.md                   # Video category → channel matrix
  catalog.md                      # Animation capability taxonomy & local registry
  sources.md                      # External channel list + GitHub search syntax + candidate pool
  repos.md                        # 34 local video skills → upstream repo traceability table
  install-protocol.md             # Install/uninstall safety protocol
scripts/
  match_skill.py                  # Request → skill matching (local + catalog)
  search_anim.py                  # Multi-channel animation skill search (GitHub API)
  manage_skill.py                 # Install/list/uninstall (snapshot + validation + rollback)
docs/
  index.html                      # Landing page (GitHub Pages)
  images/social-preview.png       # Social preview source of truth (1280×640)
```

## About the author

**桂皮 Guipi** — AI agent developer · solo-founder practitioner
Focused on AI efficiency tools and one-person-company methodology.

| Platform | Account |
|----------|---------|
| 🐙 GitHub | [guipi888](https://github.com/guipi888) |
| 🌟 知识星球 | [AI超级个体](https://t.zsxq.com/guSUk) |
| 📱 小红书 | [桂皮AI实战](https://www.xiaohongshu.com/user/profile/5a409dda44363b313b9d7e15) |

## License

MIT License — see [LICENSE](./LICENSE)
