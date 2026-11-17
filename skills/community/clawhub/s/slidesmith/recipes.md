# slidesmith recipes

Copy-paste task recipes. Replace `$ID` with the presentation id (or paste the
full URL). Every recipe ends by previewing with `diff` before `push` — keep that
habit. `slidesmith` here means the installed CLI (`.venv/bin/slidesmith` in a
dev checkout).

## 0. Setup / sanity
```bash
slidesmith auth doctor
ID=<presentation-id-or-url>
slidesmith pull "$ID" -o .        # creates ./<id>/
D=./<id>                          # the pulled folder
```

## 0a. Start a new deck without gog
```bash
slidesmith create --title "Launch plan" --dir . \
  --share teammate@example.com --role writer
ID=<printed-presentation-id>
D=./$ID
slidesmith diff "$D" --summary
```
`create` prints the deck URL and materializes a pristine local workspace. The
optional `--share` list is comma-separated and applies only to the newly
created deck; there is deliberately no standalone share command because
`drive.file` does not reliably authorize sharing arbitrary existing decks.

## 1. Deck-wide restyle by role (the ID-scripting killer)
Tag once, restyle forever.
```bash
# tag a role taxonomy (adjust selectors to the deck)
slidesmith apply "$D" 'text$=/ 06'                      --set-role footer
slidesmith apply "$D" 'tag=Rect AND h>60 AND slide in 2..6' --set-role title
slidesmith apply "$D" 'role=title' --add-class text-color-#f2ede2 --add-class font-family-montserrat
# preview + push
slidesmith diff "$D" --summary
slidesmith push "$D"
```

## 2. Bulk color/font swap across the whole deck
```bash
slidesmith replace-class "$D" \
  --swap text-color-#ffffff=text-color-#f2ede2 \
  --swap bold\ font-family-arial=bold\ font-family-montserrat \
  --dry-run                       # shows per-slide counts, writes nothing
slidesmith replace-class "$D" --swap text-color-#ffffff=text-color-#f2ede2
slidesmith diff "$D" --summary && slidesmith push "$D"
```

## 3. Add a row of cards with the layout engine (no coordinate math)
Append inside a slide's `content.sml`, before `</Slide>`:
```xml
<Stack id="mrow" x="56" y="440" w="848" h="72" direction="row" gap="24" align="stretch">
  <TextBox id="m1" flex="1" class="fill-#0a111d stroke-#5df2b2/36 stroke-solid content-align-middle text-align-center"><P class="bold text-size-13 text-color-#5df2b2">SHIP</P></TextBox>
  <TextBox id="m2" flex="1" class="fill-#0a111d stroke-#5df2b2/36 stroke-solid content-align-middle text-align-center"><P class="bold text-size-13 text-color-#5df2b2">SCALE</P></TextBox>
  <TextBox id="m3" flex="1" class="fill-#0a111d stroke-#d9b36c/54 stroke-solid content-align-middle text-align-center"><P class="bold text-size-13 text-color-#d9b36c">PROFIT</P></TextBox>
</Stack>
```
```bash
slidesmith diff "$D" --summary     # confirms 3 CREATEs at computed x-positions
slidesmith push "$D"
```

## 4. Repeat a card via a component
`$D/components.sml`:
```xml
<Components>
  <Component name="stat">
    <Rect id="box" x="0" y="0" w="200" h="96" class="fill-#0a111d stroke-{{accent|#5df2b2}}/40 stroke-solid content-align-middle text-align-center">
      <P class="bold font-family-montserrat text-size-28 text-color-{{accent|#5df2b2}}">{{value}}</P>
      <P class="font-family-arial text-size-9 text-color-#bdc5d4">{{label}}</P>
    </Rect>
  </Component>
</Components>
```
In a slide, inside a Stack:
```xml
<Use component="stat" flex="1" value="90d" label="TO LAUNCH" accent="#d9b36c"/>
```
```bash
slidesmith components "$D" --show stat     # inspect body + slots
slidesmith diff "$D" --summary && slidesmith push "$D"
```

## 5. Image gallery, mixed aspect ratios
```xml
<Image id="hero"  src="https://picsum.photos/seed/a/1600/900" x="56"  y="150" w="480" h="270" fit="contain"/>
<Image id="tall"  src="https://picsum.photos/seed/b/800/1200" x="560" y="150" w="140" h="210" fit="contain"/>
<Image id="sq"    src="./assets/logo.png"                     x="720" y="150" w="150" h="150" fit="contain"/>
<!-- Use fit="cover" when the frame must be filled with a center crop. -->
```
Relative local paths such as `./assets/...` resolve from the deck root, not the
slide folder.
```bash
slidesmith diff "$D" --summary
slidesmith push "$D"
slidesmith check "$D" --contact-sheet        # verify the render visually
# swap one later, geometry pinned:
slidesmith replace-image "$D" hero https://picsum.photos/seed/c/1200/675 --dry-run
```

## 6. Big deck: safe, resumable push
```bash
slidesmith push "$D" --per-slide --preflight=block   # QA-gate + per-slide progress
# if it stops mid-deck on a failure:
slidesmith push "$D" --per-slide --resume            # continues from the first unfinished slide
```

## 7. Apply one deck's design language to another
```bash
slidesmith theme extract "$SRC" --from-slides 1-3 -o theme.json
# on the target deck, assign roles first if you want role-aware restyle (recipe 1), then:
slidesmith theme apply "$DST" theme.json --to-slides 4-24 --map-colors --dry-run --verbose
slidesmith theme apply "$DST" theme.json --to-slides 4-24 --map-colors
slidesmith diff "$DST" --summary && slidesmith push "$DST"
```

## 8. Silence intentional decorative bleed in QA
```bash
slidesmith check "$D" --no-thumbnails            # see finding ids
slidesmith check "$D" --accept OUT_OF_BOUNDS:1:e3
# or inline: add class "qa-accept-out-of-bounds" to element e3 in the SML
```

## 9. Normalize hand-edited SML before diffing
```bash
slidesmith fmt "$D"                # canonical formatting, semantics unchanged
slidesmith diff "$D" --summary     # now shows only real changes
```

## 10. Add a new slide
Scaffold locally, choose a real deck position, then preview and push:
```bash
slidesmith add-slide "$D" --after 2 --layout title-body
slidesmith diff "$D" --summary
slidesmith push "$D"
```
Use `--at N` to insert before the 1-based slide position `N`, or `--blank` for
an empty `<Slide>` root. With neither `--after` nor `--at`, the new slide
appends at the end, preserving the historical implicit-folder behavior.
`--dry-run` prints the folder, safe authored slide ID, and intended API
`insertionIndex` without writing. IDs must use Google's 5–50 character
authored-ID grammar, must start with a letter or underscore, and may not start
with reserved `new_`. The `title-body` starter scales its geometry and font
sizes to the deck page size, falling back to 960×540 when page-size metadata is
unavailable or invalid.

The command writes `slides/NN/content.sml` and records a requested position in
the authoring-only root attribute `insertion-index`; it never pushes by itself.
The API index is 0-based: `--after 2` records `2`, while `--at 3` records `2`.
Bounds are checked against the original pulled deck, not other pending
scaffolds: with four original slides, `--at 1..5` is valid and `--at 6` is
rejected. The stored index remains in original-deck coordinates; only the
single request generator shifts later indices for earlier inserts in one push.
When one push creates several positioned slides, requests are ordered by their
requested original-deck position and each later index is shifted right for
earlier insertions at or before it. A subsequent pull renumbers `slides/NN`
folders to the actual deck order and removes the authoring-only intent, so a
clean post-push diff is zero.

## 11. Send a background to back
`reorder` changes live top-level z-order; preview first, then apply:
```bash
slidesmith reorder "$D" 'id=background' --op send-to-back --dry-run
slidesmith reorder "$D" 'id=background' --op send-to-back
```
The four operations are `bring-to-front`, `bring-forward`, `send-backward`,
and `send-to-back`.

## 12. Accept an intentional overlap in QA
```bash
slidesmith check "$D" --no-thumbnails       # inspect stable finding IDs
slidesmith check "$D" --no-thumbnails \
  --accept OVERLAP:1:card_a,card_b
```
For committed intent, add `qa-accept-overlap` to an involved element's class;
the class is stripped before requests are generated.

## 13. Authoring guardrails
- Authored IDs meeting the 5–50 character and charset constraints survive
  push/pull round trips verbatim. IDs outside those constraints are still
  accepted, but slidesmith sanitizes them into generated object IDs before
  sending, so the authored name is not preserved.
  `new_` is reserved; see the agent guide for the full ID rules.
- A new `<Group>` cannot be created through the API. Keep or copy a pulled
  group's ID instead; request generation fails with `Group elements cannot be created via the API; keep or copy pulled groups instead`.
