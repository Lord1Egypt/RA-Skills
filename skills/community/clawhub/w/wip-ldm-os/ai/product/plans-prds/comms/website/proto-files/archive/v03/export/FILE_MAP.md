# File map — WIP Computer Homepage prototype

Five files. That's everything.

```
Homepage.html       Entry point. Loads React 18 + ReactDOM + Babel Standalone from
                    unpkg, then components.jsx, then mounts <App />.

styles.css          All visual styles. Vanilla CSS, no framework.
                    Token block at the top (--accent, --fg, --content, --font-*).
                    Sections labelled: Header / Hero / Letter / Products / Footer /
                    Bucky readout (debug). Keyframes for hero caret + caption.

components.jsx      All UI. JSX, transpiled in-browser by Babel. Five sections:
                    1. Header()           — Fixed top bar. Logo left, CTA right.
                                            CTA opacity is scroll-tied to hero CTA.
                    2. Hero()             — Bucky bg cycler + headline + CTAs.
                    3. HeroTitle()        — Typewriter loop. Top + bottom lines.
                    4. Letter()           — Editorial founder letter.
                    5. Products()         — "Architecture" reveal section.
                    6. Footer()           — Brand + Tools + Connect + bottom row.
                    Plus BUCKY_PRESETS at top: hand-curated bg placements.
                    SOCIAL_ICONS map: inline SVG for X + GitHub.

assets/
  wip-logo.png        WIP triangle mark.
  bucky-patent-1.gif  R. B. Fuller US Patent 2,393,676, sheet 1
  bucky-patent-2.gif  …sheet 2
  bucky-patent-3.gif  …sheet 3
  bucky-patent-4.gif  …sheet 4
  bucky-patent-5.gif  …sheet 5
```

## External dependencies (CDN, pinned + SRI)

- React 18.3.1 + ReactDOM 18.3.1
- Babel Standalone 7.29.0
- Google Fonts: Inter Tight (400/500/600). Loaded by `styles.css`.

## What's NOT in the export

This prototype was built with React + in-browser Babel for design iteration
speed. Production likely wants vanilla JS (no framework runtime) to match the
deploy spec. Port boundary is clean: every component is self-contained, no
shared state outside React.useState/useRef and one tiny pub-sub
(`_archState` / `useArchOpen`) for the architecture reveal.

The font stack assumes Inter Tight is available. Embed locally for production.
