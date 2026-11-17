# Rainwater Harvesting — Rules & Reference

## 1. Catchment math
- US: `gallons = area_ft² × rain_in × 0.623 × coeff`. Metric: `liters = m² × mm × coeff`.
- Runoff coefficients: metal 0.95, membrane 0.95, asphalt 0.90, tile 0.80, gravel/built-up 0.70, thatch 0.60, green roof 0.40.
- Measure roof area in **plan view** (footprint), not along the slope — rain falls on the plan projection. Only roof planes plumbed to the barrel count; a downspout usually serves half the roof.
- Quick anchors: 1,000 ft² × 1 inch ≈ 623 gal × coeff. 100 m² × 1 mm ≈ 85–95 L.

## 2. Irrigation demand bands (dry season, per week)
| Planting | L/m²/week |
|---|---|
| Vegetables (productive) | 15–20 |
| New trees/shrubs (yr 1) | 20–30 |
| Lawn (cool-season) | 20–25 |
| Lawn (warm-season) | 15–20 |
| Xeric / native beds | 5–8 |
| Containers (exposed) | 30–50 (small areas) |

Advanced: `ET₀ × Kc × area` (landscape coefficient method) — ET₀ from local ag extension; Kc 0.8 vegetables, 0.75 lawn, 0.5 xeric. The L/m² bands above are ET-season averages for temperate summers.

## 3. Storage sizing doctrine
- Storage exists to **bridge dry spells**, not to store the year. Rule of thumb: 3–6 weeks of demand, or until the next typical rain interval.
- 200 L per 10–15 m² of bed is the working heuristic. A 200 L barrel serves ~10 m² of vegetables for one dry week.
- Mass-balance monthly sim is the honest method (the `storage` command): track overflow and shortfall separately; optimize capacity until marginal 100 L adds <5% used.
- Multiple barrels: connect at the **bottom** for equal level (daisy-chain top-overflow only for cascade filling), one shared first-flush.

## 4. First-flush & water quality
- Discard the first 0.5–1 mm of each storm: 0.2–0.5 L per m² of roof (a 150 m² roof → 40–75 L diverter!). Practical compromise: 20–40 L diverter for residential roofs.
- Screen every inlet/outlet (1 mm mesh mosquito screen); sealed lid.
- Asphalt shingle harvest: fine for ornamental beds; many extension services suggest avoiding it for leafy vegetables eaten raw. Metal/tile roofs are the cleanest catchments.
- Never harvest from: lead flashing, asbestos cement, copper-moss-treated roofs (zinc strips), heavily mossed shingles without cleaning.

## 5. Plumbing reality
- Gravity head: 1 m of water column ≈ 0.1 bar. A barrel on 1 m stand gives ~0.1–0.15 bar at the spigot — enough to fill a watering can fast, **not** enough for standard drip (needs ~0.7–1 bar). Use gravity-rated drip kits (0.1–0.5 bar) or a small 12 V pump.
- Stand must carry 1 kg/L (a 400 L IBC = 400 kg + tote): pavers or concrete blocks, level, on firm ground.
- Overflow: pipe ≥ downspout diameter, routed ≥3 m (10 ft) from the foundation, ideally to a soakaway/rain garden. Winter: drain barrel, redirect downspout to ground, reconnect in spring.
- Freeze: water expands ~9%; any trapped water splits plastic. Drain ALL fittings, leave spigot open.

## 6. Economics honesty
- US municipal water averages $8–15/kgal (+sewer on top where metered together — rain barrels typically reduce the combined bill only if sewer is charged on water volume).
- A 2×200 L system (~$250–350 DIY) using 4,000–6,000 gal/yr saves $50–120/yr → payback 3–7 yr where sewer counts; 10–20+ yr where it doesn't. Rebates ($25–100/barrel, e.g. many municipal programs) usually halve that.
- The non-economic case is real: soft chlorine-free water (better for acid-loving plants and epiphytes), zero-carbon irrigation, drought/outage resilience, stormwater reduction (many cities pay stormwater fee credits for detention).
- Used ≠ harvested: only count gallons that actually replaced municipal use.

## 7. Legality snapshot (verify locally; rules change)
- US: largely legal and encouraged; Colorado historically capped residential collection (2 barrels ≤110 gal total, HB16-1005); Utah permits up to 2,500 gal with registration. Most states + municipalities offer rebates.
- EU/UK: legal and encouraged; Germany requires attenuation on new builds in many Länder.
- Australia: actively promoted (mandatory in some councils for new builds); rebates common.
- Always check: barrel subsidies, stormwater-fee credits, and HOA/deed restrictions before install.

## 8. Troubleshooting quick table
| Symptom | Likely cause | Fix |
|---|---|---|
| Barrel always empty | demand >> catchment, or leaf-jam at inlet | add barrels, clean gutter screens |
| Barrel always full/overflowing | demand too small | expand irrigated beds; this is a good problem |
| Water smells/gray | anaerobic organics, no first-flush | flush barrel, add diverter, use within 2 wk |
| Mosquitoes | unscreened opening | 1 mm mesh every opening; mosquito dunks (Bti) |
| Spigot trickles | insufficient head or 3/4" restriction | raise stand, 1" or 25 mm minimum plumbing |
| Green water / algae | light entering barrel | opaque barrel or paint; algae need light |
