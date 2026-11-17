---
name: slidesmith
description: >-
  Edit a Google Slides deck in place from the command line: pull it to editable
  local SML, change it (semantic selectors, roles, components, images, layout),
  preview an exact diff, and push batchUpdates back to the SAME deck. Use for any
  task that creates or restyles Google Slides while keeping them native and
  editable — new slides, deck-wide restyles, media/galleries, cross-deck theme
  transfer — instead of generating an image or a throwaway .pptx.
metadata:
  openclaw:
    homepage: https://github.com/unblocklabs-ai/slidesmith
    requires:
      bins:
        - slidesmith
---

# slidesmith

You edit a **living** Google Slides deck. `pull` mirrors it to local SML files,
you change those files, `diff` shows the exact `batchUpdate` you'd send, and
`push` applies it to the same deck — your edits appear in Drive version history
like any collaborator's. A human can have the deck open while you push.

## Mental model (read this first)

- **The deck is the source of truth.** Your local folder is a projection plus a
  pristine snapshot for diffing — a git-style working tree, not a replica.
- **SML is HTML-like.** Each slide is `slides/NN/content.sml`: elements
  (`<Rect>`, `<TextBox>`, `<Image>`, `<Line>`…) with absolute `x/y/w/h` in points
  (960×540 page) and **Tailwind-style classes** for style
  (`fill-#173b32/40`, `text-size-24`, `bold`, `text-color-#5df2b2`,
  `content-align-middle`). Text is `<P>` paragraphs, optionally with `<T class>`
  runs.
- **Quick class vocabulary.** Append `/NN` (0–100) to fill, stroke, or text
  colors for opacity; stroke dashes are `stroke-solid`, `stroke-dot`,
  `stroke-dash`, `stroke-dash-dot`, `stroke-long-dash`, and
  `stroke-long-dash-dot`; text effects are `bold`, `italic`, `underline`,
  `line-through`, `small-caps`, `superscript`, and `subscript`. The agent guide
  is the authority for the full class grammar.
- **Don't hand-compute coordinates when you can help it.** Use layout containers
  (`Stack`/`Grid`) and semantic `select`/`apply`. That's the whole point.
- **Trust the diff and the warnings.** `diff` before every `push`. If Google
  silently changes what you sent, `push` prints `warning: … (sent 'X', remote
  now 'Y')` — believe it over your local intent.

## The loop

```bash
slidesmith auth doctor                  # once, if credentials might be off
slidesmith create --title "Quarterly plan" --share owner@example.com
slidesmith pull <deck-url-or-id> -o .   # -> <id>/slides/NN/content.sml
# ... edit the SML (see below) ...
slidesmith diff <id> --summary          # preview; --slide N to scope
slidesmith push <id>                    # apply to the same deck
slidesmith push <id> --json             # emit a machine-readable proof receipt
slidesmith check <id> --contact-sheet   # download renders + geometry QA
slidesmith advise <id>                  # local maintainability suggestions
slidesmith group <id> 'id=a OR id=b'    # native grouping, revision-locked
slidesmith --version                    # print the installed package version
```

Newer gog versions may store only the OAuth client ID in `credentials.json` and
keep the client secret in the OS keyring. `slidesmith auth doctor` checks both;
if the keyring read is unavailable, follow its macOS Keychain guidance or use
`GOG_ACCESS_TOKEN` / `gog auth credentials <file> --insecure` as a fallback.
In a non-interactive process, keyring calls time out after 5 seconds instead of
hanging on a Keychain prompt, and session-token operations fall back to the
0600 file store. Set `SLIDESMITH_KEYRING_TIMEOUT=<float-seconds>` to override
that bound, or `SLIDESMITH_KEYRING_TIMEOUT=0` to disable all keyring access;
`SLIDESMITH_TOKEN_STORE=file` selects only the session store, not gogcli's
bounded client-secret lookup.

To create a slide, scaffold it locally with `slidesmith add-slide <id>`:
`--after N` inserts after existing 1-based slide `N`, `--at N` inserts before
1-based position `N`, and `--blank` creates an empty root. `--layout title-body`
is the built-in minimal template; its starter geometry and font sizes scale to
the deck page size, falling back to 960×540 when page-size metadata is
unavailable or invalid. With neither position flag, the slide appends at the
end. The command only writes local SML; run `diff` and `push` afterward. A
follow-up pull renumbers folders to the actual deck order.

Push diagnostics distinguish actionable `warning:` lines from lower-severity
`notice:` lines and render warnings first.
`push --json` includes persistence results but not render or QA results; those
receipt fields are future scope. Per-slide JSON pushes emit a partial receipt
before re-raising a mid-run failure, and `--force --json` performs one extra
live revision read so `revision_before` is truthful.

`advise` is an offline, advisory-only pattern scan over a pulled workspace. It
reports repeated pseudo-group clusters, buried opaque-capable elements, Stack
candidates, and text boxes with 90–105% measured content-height utilization
before QA flags values above 105%; use
`--rule ID` or `--json` for agent workflows.
It never creates QA findings or blocks a push. The `group` command turns a
selected one-slide set of top-level siblings into a native Google group through
the same revision-locked write and refresh path as `reorder`; `--dry-run` prints
the exact request without authentication or an API call.

`check` writes remote-deck thumbnails at `.qa/slide-NN.png` and a
`.qa/contact-sheet.png` — **look at them**; the offline geometry lint can't see
visual intent, only overlaps/overflow. If local edits are pending, `check`
warns that these images do not include them; run `slidesmith push` first.

## Core capabilities

### Create and share a deck

```bash
slidesmith create --title "Launch plan" --dir .
slidesmith create --title "Launch plan" \
  --share writer@example.com,reviewer@example.com --role commenter
```

`create` creates the deck, materializes the returned presentation through the
same workspace path as `pull`, and prints the presentation ID, URL, and local
workspace. `--share` is intentionally available only during creation: under
the `drive.file` scope, Slidesmith can reliably share decks it created, but
not arbitrary existing decks without a Drive Picker grant. Sharing defaults
to `writer`, sends no notification email, and reports each success/failure;
the deck and workspace remain available when sharing is partially or wholly
unsuccessful.

### Add a slide

```bash
slidesmith add-slide <id> --after 2 --layout title-body
slidesmith add-slide <id> --at 1 --blank --dry-run
```

The command is local-only. User positions are 1-based and become the API's
0-based `insertionIndex`; omitting both flags appends. The intent is stored in
the authoring-only `insertion-index` attribute on the new `<Slide>` root and is
omitted by pull-generated roots, so a no-edit post-push diff is zero. The next
pull renumbers `slides/NN` folders to actual deck order. Safe authored IDs are
5–50 characters, must start with a letter or underscore, and must not start
with reserved `new_`; remaining characters may be letters, digits, underscores,
or hyphens. Position bounds use
only pulled slides: pending insertion-index scaffolds do not increase the
deck length, so a four-slide deck accepts `--at 1..5` and rejects `--at 6`.

### Semantic selection (avoid ID-scripting)
```bash
slidesmith select <id> "role=title AND slide in 4..24"
slidesmith apply  <id> "role=subtitle" --add-class text-size-18 --remove-class text-size-24
```
Predicates (combine with `AND`/`OR`/parens): `tag=`, `role=`, `id=`/`id~=`,
`text=`/`text^=`/`text$=`/`text~=`, `class~=`, `slide=`/`slide in a..b`/`slide in
a,b`, geometry `w>`/`h<=`/`x>=`/`y<`. Quote values with spaces:
`text="I CLOSE LOOPS."`. Use exact/anchored (`text=`, `id=`) to avoid
over-matching. `apply` is atomic and rejects class conflicts. Run
`slidesmith select --help` for the full grammar.

### Roles (semantic layer for restyling)
```bash
slidesmith apply <id> "text^=THE MISSION OR text^=THE ROADMAP" --set-role kicker
slidesmith apply <id> "role=kicker" --add-class fill-#173b32/40   # restyle all kickers at once
```
Roles round-trip via `roles.json`, are never sent to Google, and make deck-wide
restyles a single command.

### Layout (compiler does the math)
```xml
<Stack id="cards" x="56" y="400" w="848" h="80" direction="row" gap="24" align="stretch">
  <TextBox id="c1" flex="1" class="fill-#0a111d content-align-middle text-align-center"><P>SHIP</P></TextBox>
  <TextBox id="c2" flex="1" class="fill-#0a111d content-align-middle text-align-center"><P>SCALE</P></TextBox>
</Stack>
```
`Stack`/`Grid` compute child positions; `flex="1"` splits space; `h="auto"` sizes
a TextBox to its text. **One-shot:** after push they're plain absolute SML — keep
your authoring source if you want to re-run it.

### Components (reuse a pattern)
`components.sml` (needs a `<Components>` root):
```xml
<Components>
  <Component name="metric">
    <Rect id="box" x="0" y="0" w="200" h="110" class="fill-#0a111d stroke-{{accent}}/40 stroke-solid content-align-middle text-align-center">
      <P class="bold font-family-montserrat text-size-30 text-color-{{accent}}">{{value}}</P>
      <P class="font-family-arial text-size-10 text-color-#bdc5d4">{{label|SUPPORT}}</P>
    </Rect>
  </Component>
</Components>
```
Use it: `<Use component="metric" value="3x" label="LOOPS" accent="#5df2b2" x=.. y=.. w=.. h=../>`
(also works inside a Stack with `flex`). `slidesmith components <id> --show metric`
prints the body + slots. Slots support `{{name|default}}`.

### Images
```xml
<Image id="hero" src="https://picsum.photos/1600/900" x="60" y="140" w="480" h="270" fit="contain"/>
<Image id="logo" src="./assets/logo.png" x="800" y="40" w="100" h="40" fit="contain"/>
```
`src` = public URL **or** local path (local uploads to Drive, cached). Relative
local paths resolve from the deck/pull root (the `<ID>/` folder), e.g.
`<ID>/assets/...`, not from the `slides/NN/` directory containing the SML file.
`fit`:
`contain` (aspect-correct, top-left anchored — recommended), `stretch` (exact
box, may distort), or `cover` (aspect-preserving center crop that fills the
authored frame). For an existing image, set a new `src` (optionally with
`fit`) in SML and use the normal `diff`/`push` loop; this emits
`IMAGE_UPDATE`/`replaceImage` and a geometry pin. A `fit` change requires a
`src`. For a clean-diff one-shot swap, use `slidesmith replace-image
<id> <element-id> <new-src> --fit cover --dry-run`. New local and remote cover
images are center-cropped into a deterministic cached asset before the normal
Drive upload; a new remote cover emits only a plain `createImage` using that
derived asset. The remote cache key includes the URL, downloaded content hash,
target aspect, and derivation version, and a cache hit does not refetch. Existing
image cover replacements retain the native `CENTER_CROP` replace plus geometry
pin path; that is the one live-unvalidated cover path. Pull keeps images
source-less as before and does
not infer `cover` from crop properties because Google's volatile render URL is
not an authored source; write `src` and `fit="cover"` explicitly when replacing.
The `replace-image` command pushes immediately with a revision lock; it is not
staged by `diff`/`push`.

### Large decks / safe pushes
```bash
slidesmith push <id> --per-slide --preflight=block   # per-slide progress; abort on NEW geometry findings
slidesmith push <id> --per-slide --resume            # continue after a partial failure
```

### Cross-deck design language
```bash
slidesmith theme extract <id> --from-slides 1-3 -o theme.json
slidesmith theme apply <id> theme.json --to-slides 4-24 --map-colors --dry-run --verbose
slidesmith snippet copy <src-id> "role=title" -o title.sml
slidesmith snippet paste <dst-id> --slide 5 title.sml
```
`theme apply` is style-only (never touches text/geometry); `--map-colors` snaps
off-theme colors to the nearest palette member; needs roles on the target for
role-aware restyle.

### QA judgment
`check` labels findings NEW / PRE-EXISTING / RESOLVED vs your last pull. Accept
intentional composition so it stops warning: `check <id> --accept <finding-id>`
or add a `qa-accept-<rule>` class to the element inline (stripped before push).
Overflow QA measures each paragraph/run inside a 7.2pt horizontal and
field-calibrated 3.6pt vertical default text content inset, wraps at whitespace,
applies authored leading and paragraph spacing, and consumes captured
text-autofit scale/reduction only for untouched elements; pending text or
run-size edits deactivate that captured adjustment. Captured per-element insets
override both defaults.
`NONE` is not treated as shrinkable. Overlap QA remains conservative for
text-vs-text, but uses alignment-aware estimated paragraph ink for
text-vs-non-text pairs; only `<Line>` elements remain unconditionally exempt.

## Gotchas
- Always `diff` before `push`; the deck may have changed under you (push is
  revision-locked and will abort on conflict — re-pull and retry).
- Layout/components are one-shot; a later pull returns resolved coordinates.
- Authored element IDs survive round-trips when they meet Google's 5–50-character
  object-ID grammar, are unoccupied, and don't resemble a generated
  Google/Slidesmith ID (`eNN`, `gNN`, `pNN`, `SLIDES_API…`); invalid, occupied,
  or generated-looking names are sanitized/suffixed, so don't script around
  generated `eNN` IDs.
- `fmt` before committing hand-edited SML so whitespace changes don't inflate the
  diff.
- Bounds-containment nesting: a visually containing ordinary element may become
  an SML parent on re-pull only when that subtree is contiguous in Google's
  back-to-front paint order. The SML tree's depth-first document order is
  therefore guaranteed to match paint order; interleaved elements remain
  siblings (or attach to the highest still-contiguous ancestor). Native Google
  `Group` structure is preserved. Deleting an inferred wrapper needs care
  (keep the child).

See `recipes.md` for copy-paste task recipes and `docs/AGENT-GUIDE.md` (in the
repo) for the exhaustive reference.
