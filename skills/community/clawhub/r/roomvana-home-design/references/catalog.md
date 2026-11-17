# Roomvana catalog snapshot

Fallback for when `scripts/studio_link.py` can't reach the live catalog (`https://api.roomvana.co/options`). The live list wins whenever it's reachable. Regenerate with `python3 scripts/studio_link.py catalog-md > references/catalog.md`.

## Indoor rooms

Modes: `redesign`, `stage` (furnish an empty room), `declutter`, `surface`.

- `kitchen` — kitchen
- `living-room` — living room
- `bedroom` — bedroom
- `bathroom` — bathroom
- `dining-room` — dining room
- `home-office` — home office
- `kids-room` — kids' room
- `nursery` — nursery
- `basement` — basement
- `attic` — attic bedroom
- `entryway` — entryway
- `laundry-room` — laundry room
- `closet` — walk-in closet
- `home-theater` — home theater
- `home-gym` — home gym
- `wine-cellar` — wine cellar
- `basement-bar` — basement bar
- `staircase` — staircase and stairwell

## House exterior

Modes: `redesign`, `surface`.

- `exterior` — house exterior (facade)

## Yard and outdoor spaces

Mode: `redesign` only.

- `garden` — garden
- `backyard` — backyard
- `landscape` — yard and surrounding landscape
- `patio` — patio and outdoor seating area
- `deck` — deck
- `porch` — porch
- `balcony` — balcony

## Styles

Used by `redesign` and `stage`.

- `modern` — clean lines, uncluttered surfaces, neutral palette with bold accents
- `minimalist` — essential furniture only, calm neutral tones, hidden storage
- `scandinavian` — light woods, white walls, cozy textiles, functional simplicity
- `japandi` — Japanese-Scandinavian fusion, warm woods, low-profile furniture, serene neutrals
- `mid-century-modern` — walnut and teak furniture, organic curves, retro accents
- `industrial` — exposed brick and metal, dark tones, raw finishes
- `bohemian` — layered patterns and textures, plants, warm eclectic decor
- `modern-farmhouse` — shiplap accents, warm woods, black fixtures, rustic-meets-clean
- `coastal` — airy whites and blues, natural fibers, beach-house freshness
- `traditional` — classic furniture silhouettes, rich woods, elegant symmetry
- `contemporary` — current-day polish, mixed materials, comfortable sophistication
- `rustic` — reclaimed wood, stone textures, warm cabin comfort
- `french-country` — soft pastels, carved wood, linen fabrics, Provencal charm
- `mediterranean` — terracotta, wrought iron, warm plaster walls, arched details
- `art-deco` — geometric patterns, brass and velvet, glamorous jewel tones
- `modern-luxury` — marble, brass details, statement lighting, hotel-suite polish
- `vintage` — curated second-hand furniture, nostalgic colors, timeless character
- `dark-academia` — moody deep tones, wood paneling, library-inspired warmth
- `tropical` — lush green plants, rattan and bamboo, resort-like brightness
- `cottagecore` — floral patterns, soft vintage furniture, whimsical countryside coziness
- `transitional` — traditional silhouettes with contemporary lines, soft neutral palette
- `spanish-colonial-revival` — white stucco, dark carved wood beams, terracotta tile, arched openings
- `2026-trends` — organic curved furniture, earthy color-drenched walls, sculptural lighting

## Indoor surfaces

Surface mode. The finish goes in the link's `style` parameter. Where a finish has a closest real paint color, it's in brackets.

- `walls`: `warm-white` [Sherwin-Williams Alabaster SW 7008], `greige` [Sherwin-Williams Agreeable Gray SW 7029], `sage-green` [Sherwin-Williams Clary Sage SW 6178], `olive-green` [Sherwin-Williams Ripe Olive SW 6209], `navy-blue` [Benjamin Moore Hale Navy HC-154], `light-blue` [Benjamin Moore Breath of Fresh Air 806], `charcoal` [Benjamin Moore Kendall Charcoal HC-166], `terracotta` [Sherwin-Williams Cavern Clay SW 7701], `dusty-pink` [Benjamin Moore First Light 2102-70], `cream` [Benjamin Moore White Dove OC-17], `mustard` [Benjamin Moore Spicy Mustard 2154-20], `forest-green` [Benjamin Moore Hunter Green 2041-10]
- `flooring`: `light-oak`, `natural-oak`, `walnut`, `dark-wood`, `herringbone-oak`, `whitewashed-wood`, `gray-lvp`, `polished-concrete`, `terrazzo`, `large-format-tile`
- `wallpaper`: `botanical`, `vintage-floral`, `geometric`, `grasscloth`, `subtle-stripes`, `landscape-mural`, `damask`, `kids-clouds`
- `cabinets`: `white-shaker` [Benjamin Moore White Dove OC-17], `cream` [Benjamin Moore White Dove OC-17], `sage-green` [Sherwin-Williams Clary Sage SW 6178], `forest-green` [Benjamin Moore Hunter Green 2041-10], `navy-blue` [Benjamin Moore Hale Navy HC-154], `black-matte` [Sherwin-Williams Tricorn Black SW 6258], `natural-oak`, `walnut`, `two-tone`, `greige` [Sherwin-Williams Agreeable Gray SW 7029]
- `backsplash`: `white-subway-tile`, `white-zellige-tile`, `green-zellige-tile`, `marble-slab`, `herringbone-tile`, `hex-tile`, `terracotta-tile`
- `countertop`: `white-quartz`, `calacatta-marble`, `carrara-marble`, `butcher-block`, `black-granite`, `soapstone`, `concrete`, `waterfall-quartz`
- `wainscoting`: `white-beadboard` [Sherwin-Williams Alabaster SW 7008], `board-and-batten` [Sherwin-Williams Alabaster SW 7008], `raised-panel` [Sherwin-Williams Alabaster SW 7008], `shaker-panel` [Sherwin-Williams Alabaster SW 7008], `wood-slat`
- `molding`: `crown-molding` [Sherwin-Williams Alabaster SW 7008], `picture-frame-molding` [Sherwin-Williams Alabaster SW 7008], `coffered-ceiling` [Sherwin-Williams Alabaster SW 7008], `wood-ceiling-beams`, `white-trim` [Sherwin-Williams Alabaster SW 7008], `black-trim` [Sherwin-Williams Tricorn Black SW 6258]

## Exterior surfaces

Surface mode. The finish goes in the link's `style` parameter. Where a finish has a closest real paint color, it's in brackets.

- `siding`: `white` [Sherwin-Williams Pure White SW 7005], `cream` [Benjamin Moore White Dove OC-17], `greige` [Sherwin-Williams Agreeable Gray SW 7029], `sage-green` [Sherwin-Williams Clary Sage SW 6178], `navy-blue` [Benjamin Moore Hale Navy HC-154], `charcoal` [Benjamin Moore Kendall Charcoal HC-166], `black` [Sherwin-Williams Tricorn Black SW 6258], `natural-cedar`, `white-painted-brick` [Sherwin-Williams Pure White SW 7005], `stone-veneer`
- `front-door`: `black` [Sherwin-Williams Tricorn Black SW 6258], `navy-blue` [Benjamin Moore Hale Navy HC-154], `forest-green` [Benjamin Moore Hunter Green 2041-10], `classic-red` [Benjamin Moore Caliente AF-290], `teal`, `mustard` [Benjamin Moore Spicy Mustard 2154-20], `natural-wood`, `white` [Sherwin-Williams Pure White SW 7005], `sage-green` [Sherwin-Williams Clary Sage SW 6178]
- `garage-door`: `white` [Sherwin-Williams Pure White SW 7005], `black` [Sherwin-Williams Tricorn Black SW 6258], `charcoal` [Benjamin Moore Kendall Charcoal HC-166], `natural-wood`, `navy-blue` [Benjamin Moore Hale Navy HC-154], `sage-green` [Sherwin-Williams Clary Sage SW 6178]
- `shutters`: `black` [Sherwin-Williams Tricorn Black SW 6258], `navy-blue` [Benjamin Moore Hale Navy HC-154], `forest-green` [Benjamin Moore Hunter Green 2041-10], `charcoal` [Benjamin Moore Kendall Charcoal HC-166], `white` [Sherwin-Williams Pure White SW 7005], `sage-green` [Sherwin-Williams Clary Sage SW 6178]
- `roof`: `charcoal-shingle`, `black-shingle`, `weathered-wood-shingle`, `slate-gray-shingle`, `black-standing-seam`, `terracotta-tile`
- `deck-boards`: `natural-cedar`, `warm-brown-stain`, `gray-composite-decking`, `whitewashed-wood`, `charcoal-stain`
