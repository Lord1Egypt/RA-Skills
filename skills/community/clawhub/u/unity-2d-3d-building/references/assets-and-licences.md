# Assets you are allowed to ship, and where to get them online

This page is guidance, not code. It names public hosts your own agent may fetch art from, after the
licence gate below. No script ships with this skill, so nothing here fetches, uploads, posts or
reports anything by itself: every download described here is a command your agent runs, under your
own permissions.

Licence first, download second. Nothing gets pulled until it is clear it can ship, because a game built
on the wrong source cannot be published - and rewriting the art later costs more than sourcing it right.

## The licence gate, in order

1. **CC0 is the target.** Public domain: publishable, sellable, remixable, no attribution, no review.
   When a source is CC0 the licence conversation is over, and its files can live in a public repo.
2. **A free kit's art can be CC0 while its code is not.** Asset Store starters often carry the standard
   Extension Asset EULA for the code and CC0 for the art (their attribution block names the CC0
   upstream). Take the art, write the logic yourself, and the kit is never a runtime dependency.
3. **Free to use is not free to redistribute.** A service can allow the asset in a shipped build while
   forbidding the raw files in a repo. Keep your own local copies and never commit those files.
4. **A GitHub game repo needs a real licence at the file.** No LICENSE, or "for educational purposes"
   wording, is not permission to ship. MIT/Apache only, and read it at the file rather than in a README.
5. **Record the licence per source in the project notes.** "Everything is CC0" has to survive the next
   session; write down which source each used asset came from.

## Sources worth using (verify the licence at the source, per file)

| Source | Best for | Licence | Format |
|---|---|---|---|
| **Kenney** - https://kenney.nl/assets | 2D sprites, UI, icons, tilesets, small 3D kits, sound | **CC0** | PNG, plus OBJ/FBX/glTF for 3D kits |
| **Quaternius** - https://quaternius.com | low-poly 3D characters, creatures, props, 250+ animation clips | **CC0** | FBX, OBJ, glTF, Blender |
| **Poly Haven** - https://polyhaven.com | PBR textures, HDRIs, a few models; a documented file API for scripted pulls | **CC0** | JPG/PNG, EXR/HDR, FBX/glTF |
| **KayKit** - https://kaylousberg.itch.io | stylised character + dungeon/prop packs that read well in a flat-lit scene | **CC0** | glTF, FBX |
| **Poly Pizza** - https://poly.pizza | quick low-poly props, filtered by licence | **CC0 / CC-BY** (per model) | glTF |
| **Sonniss GDC bundles** - https://sonniss.com/gameaudiogdc | large royalty-free sound libraries (tens of GB) | royalty-free, per bundle terms | WAV |
| **Freesound** - https://freesound.org | single sounds, ambiences, foley | **per file** (CC0 / CC-BY / CC-BY-NC) | WAV, MP3, OGG |
| **Unity Asset Store** - https://assetstore.unity.com | free-tier art packs, tools, templates | Extension Asset EULA (read the licence per package; "free" is not CC0) | package |
| **Mixamo** - https://mixamo.com | rigged character animation, auto-rigging | free for commercial use, **redistribution of raw files forbidden** | FBX |

Notes that matter in practice:

- **Kenney's *Starter Kits* are Godot, not Unity.** His CC0 *assets* import into Unity happily; his
  *kits* cannot. Do not chase them.
- **Check the pack's own attribution block for its CC0 upstream** - it frequently names a cleaner source
  than the page you found first.
- **Sound libraries are the classic gap** in a model-heavy library. Name the gap and pull audio from a
  second source rather than implying the library is complete.
- **Watch the format against the engine**: a glTF-binary mirror needs a glTF importer in the project,
  while an FBX/OBJ pack imports natively. Downloaded packs arrive *staged* - expect `Blends/ FBX/ OBJ/`
  (or `Textures/` beside models) and pick the folder the engine wants instead of importing all three.

## Never source from these

"Free download" aggregators that redistribute paid Asset Store packages without a licence
(`unityassetpack.com`, `unityassetcollection.com`, `opengameasset.net`, "50 Unity Source Codes" and
similar bundles). A game built on them cannot be published, and the licence problem surfaces exactly
when the project is ready to release. Free *art* for a theme does not make a free *framework*: if a
genre's kit is paid, say so instead of searching longer.

## Fetching efficiently

- **Enumerate before fetching.** Prefer an organised mirror or a machine-readable index (`kits.tsv`,
  an API) over scraping a vendor's site. A JavaScript-rendered catalogue can return zero links to
  `curl` while a browser shows dozens - treat "curl found nothing" as a property of the site, not proof
  the packs do not exist.
- **When a download hides behind a widget, read the button.** A `drive.google.com/drive/folders/<id>`
  href is scriptable; a login-gated or itch.io flow is not. Report which packs resolved rather than
  assuming they all behave the same.
- **Keep one library directory outside the project**, so a later title reuses the same kits with no
  second download.
- **Import selectively.** Importing thousands of models inflates the project, slows every import, and
  inflates the shipped build with assets nobody sees. Import the kits the levels actually call for.
- **A bulk download outlives the tool call.** Launch large pulls in the background and poll the
  filesystem for growing directories; relaunching a live job races the first copy.
- **Count what arrived, per category, and report those numbers.** A claimed total that was never
  counted is not a result.
