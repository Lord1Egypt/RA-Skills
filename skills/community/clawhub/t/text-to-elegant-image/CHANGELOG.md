# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.1] - 2026-07-28

### Security

- **Removed remote-URL rendering branch** in `export_image.js`: the renderer previously accepted any `http(s)://` input and navigated a headless browser to it, effectively turning a local text/Markdown-to-image tool into a general-purpose web fetcher (SSRF / internal-network probing surface). It now only accepts local HTML file paths; remote URLs are rejected with a clear error. Normal usage (write content to a local `.html`, then render) is unchanged.
- **Dependency install is no longer silent**: `setup.sh` dropped `--silent` on `npm install`, so the puppeteer-core installation is now visible. SKILL.md wording updated from "silently auto-installs, no confirmation" to "prompts and installs with visible output", removing the undocumented-side-effect concern. Behavior is otherwise identical.

## [1.2.0] - 2026-07-27

### Added

- **Card-style backgrounds on every style**: all 18 styles' `.container` now ship a themed card background (background color + border + radius/shadow, matching each style's own palette — neon-outlined for cyberpunk, paper-textured hairline for ink-scroll, etc.), giving a consistent "card floating on canvas" look paired with the frame padding. On by default, no flag required.
- **`--flat` flag**: opt out of the card background to restore the previous flat, edge-to-edge look (`node scripts/export_image.js <html> <output.png> 560 --flat`). Not recommended for the glassmorphism style, whose frosted-glass card *is* the core visual effect.

## [1.1.0] - 2026-07-27

### Added

- **Per-style resource files**: the single `resources/styles_reference.md` is split into 18 standalone style files under `resources/styles/` (`01_cyberpunk.md` … `18_vivid.md`), each bundling complete CSS, an HTML structure example, component color-variable mapping, optional font injection and signature decorations; shared skeleton and typography rules moved to `resources/styles/_BASE.md`. The old path remains as a 9-line pointer stub for backward compatibility.
- **Visualization component library** (`resources/components.css`): KPI cards, progress bars, comparison bars, donut charts, flow steps, timelines and more — themed per style through `--t2e-*` CSS variables.
- **Signature web-font injection**: 6 curated display fonts (public Google Fonts CDN) wired into matching styles, with system-font fallback so rendering never blocks.
- **Frame padding** (`--frame <px>`): uniform 32px canvas frame on all four edges by default in long-image mode; customizable or disabled with `--frame 0`.
- **Poster & cover layouts** (`--fixed-height <px>`): fixed 3:4 (600×800) quote-poster and cover-card modes with centered flex layout, alongside the default long-image mode.
- **Adaptive screenshot height**: the export script measures the real `.container` height and crops trailing whitespace precisely.
- **Scripted emoji check** (`scripts/check_emoji.py`): mandatory pre-screenshot gate that reports offending characters with line numbers (headless Chrome renders emoji as tofu boxes).
- **Style templates**: ready-made 3:4 poster / cover-card HTML examples under `resources/templates/`.

### Changed

- `SKILL.md` workflow expanded: visualization-opportunity scanning, per-style read discipline (only read the chosen style file + `_BASE.md`), low-cost style switching (swap CSS + class prefixes instead of regenerating HTML).
- `scripts/export_image.js`: web-font wait (up to 8s, non-blocking on CDN failure), frame padding, fixed-height mode, footer injection/removal.

## [1.0.0] - 2026-07-13

### Added

- Initial public release: 18 visual styles, high-DPI (2×) headless-Chrome rendering, auto height cropping, cross-platform Chrome detection, configurable output directory (`T2EI_OUTPUT_DIR`, default `./output`), footer control (`--author` / `--no-footer`).
