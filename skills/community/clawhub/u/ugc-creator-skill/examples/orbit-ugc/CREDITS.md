# Credits

Footage courtesy of NASA. This project is not endorsed by NASA. No person appears in any video in
this folder: the creator's half of every video is a labelled placeholder ("your recording goes
here"), because the skill never generates a person and this demo has no real creator.

## NASA sources (no people on screen)

| Source | NASA page | Used for |
|---|---|---|
| "Artemis I Launch (Press Site)", Marshall Space Flight Center, 16 Nov 2022, `~medium.mp4` | https://images.nasa.gov/details/Artemis%20I%20Launch%202022%20CU%20tracking%20from%20Press%20Site_compressed | 0:44 to 0:52 in `orbit-footage.mp4` |
| "Earth Views from the ISS - No Music", NASA Headquarters, 21 Dec 2020, `~medium.mp4` | https://images.nasa.gov/details/NHQ_2020_1221_Earth%20Views | 25:00 to 25:06 in `orbit-footage.mp4`; stills at 5:00, 20:00 and 35:00 in `takes/screen.mp4` |

The downloads themselves are not in this repo. `tools/make_inputs.py` rebuilds both input files from
them, byte for byte.

## Files in this folder and their SHA-256

| File | What it is | SHA-256 |
|---|---|---|
| `orbit-footage.mp4` | the made-up brand's "supplied footage": the two NASA clips above, 640x568, no sound | `fbafe06d71d2d7ea6f4248599c7c7a9c289729691f64b99f5b4106c5162d578f` |
| `takes/screen.mp4` | a mock screen recording of the made-up "Example Orbit" app, drawn by `tools/make_inputs.py` around three NASA Earth stills | `dc2b9270e349953ee6e61f9ccdac6af9a788e45d35f5fd4eeb726b37d75b592e` |
| `videos/tiktok.mp4` | `make_video.py --placeholder --width 540`: split screen, opens with hook h1 | `8175e9d2b69bcf3448e9613941a10e70b40f59b7401ab7dc44b6a3d21c0ad1c9` |
| `videos/reels.mp4` | the same, opens with hook h2, footage from 4 s in | `d3ff1d44edaf61a26c928822ddfe4b723adc037584d194d20036f45c04ab8bbf` |
| `videos/shorts.mp4` | face plus screen recording, opens with hook h3 | `6d7b8f3e9a8afc63d36badca19bc30cc71d508d72d34ad70bf55c66fd721f90a` |
| `videos/*-cover.jpg`, `videos/contact-sheet.jpg` | frames of those videos, written by `make_video.py` | |

`../showcase.png` is a screenshot of `plan.html` in dark mode. `videos/uploaded.json`, `media.json` and
the ids in `requests/` are made up: nothing in this folder was ever uploaded.

NASA material is generally not subject to copyright in the United States (NASA media usage
guidelines: https://www.nasa.gov/nasa-brand-center/images-and-media/). NASA endorses nothing here,
and nothing here is an ad for NASA or by NASA.

## Made up

"Example Orbit", the app, its campaign, the marketplace, the brief, the accounts (`@example.creator`,
`@example.orbit`), every id, link, confirmation and number in this folder are made up for the
example. No real campaign, brand, creator or post is shown. The on-screen line reads "EXAMPLE ONLY:
not a real ad", and every number in `after-posting/` is marked EXAMPLE ONLY.
