# Used Car Image Analysis Guide

Complete guide for analyzing Gumtree listing photos to verify listing accuracy and identify potential issues.

## Overview

When a user requests image analysis for a Gumtree listing, download the car images and perform a systematic visual inspection to:

1. **Verify Listing Accuracy** — Does the car match the advertised details?
2. **Identify Visible Issues** — Bodywork damage, rust, wear, modifications
3. **Assess Overall Condition** — Professional dealer vs private neglect
4. **Flag Red Flags** — Signs of accident damage, poor maintenance, or misrepresentation

---

## Image Analysis Workflow

### Step 1: Download Images

Use the Read tool to fetch images from the `image_url` field:

```
Read tool with path: <image_url>
```

**Image Sources:**
- Primary thumbnail: `img.gumtree.com` CDN
- Full listing images: Available in listing detail page
- Typical resolution: 800x600 to 1600x1200

### Step 2: Systematic Visual Inspection

Analyze images in this order:

#### A. Listing Verification (5-10 seconds per image)

Check if the car matches advertised details:

| Advertised Detail | What to Check | Red Flags |
|-------------------|---------------|-----------|
| **Make/Model** | Badge on grille/boot, body shape | Wrong badges, debadged car |
| **Year** | Registration plate format, pre/post-facelift features | Plate doesn't match year, older generation model |
| **Color** | Body color consistency | Resprayed panels (color mismatch), primer spots |
| **Trim Level** | Wheels, interior features (visible through windows) | Mismatched wheels, trim badges don't match |
| **Mileage** | Wear on seats/steering wheel/pedals (if visible) | Excessive wear for claimed mileage |

**Example Checks:**

- "Listing says 2018 Ford Focus" → Check for 2015-2018 Mk3.5 facelift features (updated grille, headlights)
- "Listing says 45k miles" → Steering wheel should show light wear; heavily worn = suspect clocking
- "Listing says Titanium trim" → Should have alloy wheels, not steel wheels with hubcaps

#### B. Bodywork Inspection (Front to Back)

**Front:**
- ✅ **Good:** Clean bumper, matching paint, no cracks
- ⚠️ **Minor Issues:** Small stone chips, light scuffs (normal for age)
- 🚨 **Red Flags:** 
  - Cracked/broken bumper
  - Misaligned panel gaps
  - Resprayed (orange peel texture, color mismatch)
  - Missing trim pieces

**Sides:**
- ✅ **Good:** Straight body lines, consistent panel gaps, original paint
- ⚠️ **Minor:** Light scratches, parking dings
- 🚨 **Red Flags:**
  - Dented doors/sills
  - **Rust bubbles** on sills/wheel arches (MOT fail risk)
  - Mismatched body panels (accident repair)
  - Large scrapes/gouges

**Rear:**
- ✅ **Good:** Clean bumper, working lights, straight bootlid
- ⚠️ **Minor:** Light scratches, tow bar fitment marks
- 🚨 **Red Flags:**
  - Crumpled bumper (rear-end collision)
  - Boot misalignment (structural damage)
  - Broken lights (MOT fail)

**Roof:**
- ✅ **Good:** Clean, no dents
- ⚠️ **Minor:** Tree sap, bird droppings
- 🚨 **Red Flags:** Hail damage (multiple small dents), large dents

#### C. Wheels & Tyres

**Check Each Wheel:**
- ✅ **Good:** Matching alloys, good tread depth, even wear
- ⚠️ **Minor:** Light kerb rash on one wheel, slight uneven wear
- 🚨 **Red Flags:**
  - **Badly kerbed wheels** (multiple, deep gouges) = careless owner
  - **Budget tyres** (Linglong, Wanli, Nankang) = owner cutting corners
  - **Mismatched tyres** (different brands/tread patterns) = poor maintenance
  - **Worn tyres** (visible cords, <2mm tread) = immediate expense
  - **Uneven wear** (inside/outside edges worn) = suspension/alignment issues

**Example Red Flag:**
"Front two tyres are Michelin, rear two are budget Wanli → owner buys cheapest tyres → likely skimps on servicing too"

#### D. Interior Condition (if visible through windows)

**Steering Wheel & Seats:**
- ✅ **Good:** Light wear matching mileage (45k miles = slight shine on wheel rim)
- ⚠️ **Minor:** Some wear, but matches age
- 🚨 **Red Flags:**
  - **Heavily worn steering wheel** (leather peeling) on "30k mile" car = clocked
  - **Torn seats** (expensive repair)
  - **Stained/dirty interior** (neglect, possible odor issues)

**Dashboard:**
- ⚠️ Check for warning lights (if ignition on in photo)
- 🚨 **Red Flag:** Multiple warning lights = electrical issues

**Cleanliness:**
- ✅ **Good:** Clean, vacuumed, dealer-prepped
- ⚠️ **Minor:** Some dust, lived-in look
- 🚨 **Red Flags:**
  - **Filthy interior** = neglected maintenance
  - **Excessive clutter** = daily abuse
  - **Smoke smell indicators** (if mentioned by owner later) = hard to remove, lowers value

#### E. Engine Bay (if photo included)

**What to Check:**
- ✅ **Good:** Clean, no leaks, tidy wiring
- ⚠️ **Minor:** Some dust, oil residue
- 🚨 **Red Flags:**
  - **Oil leaks** (dark stains on engine block) = expensive repairs
  - **Aftermarket modifications** (cold air intake, tuning box) = warranty void, higher failure risk
  - **Corroded battery terminals** = neglected
  - **Dirty engine bay** = lack of care

---

## Issue Severity Classification

Use this classification when reporting findings:

### 🟢 ACCEPTABLE (No Concerns)
- Normal wear and tear for age/mileage
- Minor cosmetic imperfections (small stone chips, light scratches)
- Clean, well-maintained overall appearance

### 🟡 MINOR ISSUES (Negotiate Price)
- Light kerb rash on one wheel
- Small scuffs/scratches (£100-£300 to repair)
- Worn tyres (£200-£400 to replace)
- Interior wear slightly above expected
- Faded paint (common on red/black)

**Advice:** "Use these as negotiation leverage for £200-£500 discount"

### 🟠 MODERATE CONCERNS (Inspect In-Person Carefully)
- Multiple kerbed wheels
- Visible rust spots (check if structural)
- Mismatched tyres or budget brands
- Interior stains or tears
- Panel gaps slightly off
- Resprayed panels (check for accident history)

**Advice:** "Request detailed inspection photos or AA/RAC pre-purchase inspection before viewing"

### 🔴 RED FLAGS (Walk Away or Expert Inspection Required)
- **Rust on sills/chassis** (MOT failure, structural integrity)
- **Misaligned panels/large gaps** (poor accident repair)
- **Clocking suspicion** (wear doesn't match mileage)
- **Multiple accident damage signs** (crumpled panels, resprays, misalignment)
- **Severe neglect** (filthy interior + damaged exterior)
- **Major mechanical damage visible** (cracked engine mounts, oil leaks)

**Advice:** "This car shows signs of [issue]. Request HPI report, full service history, and consider walking away unless price reflects major repairs needed."

---

## Listing Accuracy Red Flags

### Misrepresentation Indicators

**1. Photos Don't Match Description**
- Listing says "Excellent condition" but photos show heavy wear
- Listing says "Full service history" but engine bay is filthy
- Listing says "One owner" but wear suggests 80k+ miles (claimed 40k)

**2. Strategic Photo Angles**
- All photos from same side = hiding damage on other side
- No interior photos = hiding stains/wear
- No wheel photos = hiding kerb damage
- No engine bay = hiding leaks/modifications

**3. Overly Dark/Blurry Photos**
- Can't see panel gaps clearly = hiding misalignment
- Can't see tyre tread = hiding wear
- Low resolution = hiding defects

**4. Registration Plate Obscured**
- Can't verify year from plate format
- Can't run MOT history check to cross-reference mileage

---

## Photo Quality Assessment

Rate the listing's photo quality and transparency:

### ⭐⭐⭐⭐⭐ EXCELLENT (Dealer Standard)
- 10+ high-resolution photos
- Full 360° coverage (all angles, interior, engine bay, boot, wheels)
- Good lighting, clean car
- Close-ups of minor damage disclosed
- Shows VIN/registration plate clearly

**Interpretation:** Professional dealer listing or transparent private seller

### ⭐⭐⭐ AVERAGE
- 5-8 photos
- Main angles covered (front, rear, sides, interior)
- Adequate resolution
- Some angles missing (no engine bay or boot)

**Interpretation:** Standard private sale

### ⭐ POOR (Avoid)
- <5 photos
- Blurry/dark images
- Missing critical angles (no wheels, no interior)
- Taken in poor lighting or from distance

**Interpretation:** Seller hiding issues or lazy listing = high-risk purchase

---

## Analysis Output Format

When providing image analysis, structure your response like this:

```
# 🖼️ Image Analysis Report: [Car Title]

## Listing Verification
✅ Make/Model: Matches (confirmed [Brand] [Model])
✅ Year: Appears correct ([Year] generation features visible)
⚠️ Color: Listing says [Color A], photo shows [Color B] (possible respray?)
✅ Trim: Matches ([Trim] wheels/badges visible)

## Condition Assessment

### Bodywork: 🟡 MINOR ISSUES
- Front bumper: Small stone chips (normal for age)
- Near-side front wing: Light scratches
- Rear bumper: Scuff mark (approx £150 repair)

### Wheels & Tyres: 🟠 MODERATE CONCERNS
- Front wheels: Heavy kerb rash on both (suggests parking incidents)
- Tyres: Mixed brands (Michelin front, budget Wanli rear) = £300-£400 to replace with matching quality

### Interior: 🟢 ACCEPTABLE
- Steering wheel: Light wear consistent with [mileage]
- Seats: Clean, no tears
- Dashboard: No warning lights visible

### Overall Cleanliness: 🟢 GOOD
- Exterior: Clean, appears dealer-prepped
- Interior: Tidy, vacuumed

## Red Flags: None / [List any critical issues]

## Recommendation
[Overall assessment and advice]

**Price Negotiation Leverage:**
- Kerb rash + tyre replacement: ~£500-£600
- Suggested offer: £[listing price - £500]

**Next Steps:**
1. Request close-up photos of [specific area]
2. Ask for service history to verify maintenance
3. Check MOT history at gov.uk for any advisories
4. Consider in-person viewing if photos check out
```

---

## Common UK Market Issues by Brand

### German Brands (BMW, Audi, Mercedes)

**Look for:**
- Rust on wheel arches (2000-2010 models)
- Oil leaks (common on older models)
- Overly clean engine bay = "detailed for sale" (hiding leaks)
- Aftermarket wheels = OEM wheels sold separately (expensive to replace)

### French Brands (Peugeot, Citroën, Renault)

**Look for:**
- Rust on rear arches and tailgate (common)
- Interior wear (trim pieces break easily)
- Electrical issues (visible dashboard warnings)

### Ford/Vauxhall (Mass Market)

**Look for:**
- Taxi/private hire use indicators (high wear, low price)
- Aftermarket modifications (boy racer culture)
- Multiple small dings (fleet/rental car history)

### Japanese Brands (Toyota, Honda, Mazda)

**Usually well-maintained, but check:**
- Rust on sills (older models)
- Hybrid battery warning lights (expensive replacement)
- Taxi use (Prius common in PHV)

---

## When NOT to Analyze

Skip image analysis if:
1. **No images available** — Report this to user ("Listing has no photos — red flag")
2. **Only stock/generic photos** — Not actual car photos
3. **User wants quick summary only** — Offer analysis as optional add-on

---

## Example Analysis Scenarios

### Scenario 1: Good Condition Car

**Input:** 2018 Honda Civic 1.0 VTEC, £9,500, 45k miles, Trade seller, 12 photos

**Analysis Output:**
```
✅ Listing Verified: 2018 Civic Mk10, correct year, Petrol 1.0 turbo
🟢 Condition: Excellent — Clean bodywork, no visible damage, dealer-prepped
🟢 Tyres: Matching Michelin, good tread depth
🟢 Interior: Light wear, consistent with 45k miles

No red flags detected. This appears to be a well-maintained approved-used example.

Recommendation: Good buy at asking price if service history is complete.
```

### Scenario 2: Hidden Issues

**Input:** 2015 BMW 320d, £8,000, 90k miles, Private seller, 4 photos (all from front-right angle)

**Analysis Output:**
```
⚠️ Photo Coverage: POOR — Only 4 photos, all from same angle
🔴 Red Flag: No photos of near-side (left) = likely hiding damage
🟠 Wheels: Heavy kerb rash visible on front-right wheel
⚠️ Engine Bay: No photo provided (check for oil leaks on N47 diesel engine)

Critical Missing Photos:
- Near-side bodywork
- Engine bay (N47 timing chain issues common)
- Interior wear
- Boot space

Recommendation: REQUEST additional photos before viewing. If seller refuses, walk away.
```

### Scenario 3: Clocking Suspicion

**Input:** 2016 VW Golf, £7,500, "38k miles", Trade seller, 8 photos

**Analysis Output:**
```
🔴 RED FLAG: Mileage Discrepancy Suspected
- Listing claims 38,000 miles
- Steering wheel shows HEAVY wear (leather peeling at 3 & 9 o'clock) = 80k+ miles typical
- Driver's seat bolster heavily worn = high-mileage use
- Pedal rubber almost completely worn through

Verification Required:
1. Check MOT history at gov.uk (will show historical mileage readings)
2. Request service book with stamped mileage
3. HPI check for clocking markers

Recommendation: DO NOT VIEW until MOT history verified. If mileage is genuine, this car has been severely abused.
```

---

## Tools & Resources

**MOT History Check (Free):**
- gov.uk/check-mot-history
- Cross-reference mileage with listing claims

**HPI Check (£20-£40):**
- Verifies registration details
- Flags stolen/written-off status
- Shows if mileage has been adjusted

**What to Request After Analysis:**
- More photos of specific areas
- Close-ups of any identified issues
- Service history scans
- MOT certificates

---

## Best Practices

1. **Always analyze ALL available photos** — Don't just look at the hero shot
2. **Compare wear to mileage** — Use this as primary clocking indicator
3. **Look for consistency** — Paint color match, panel gaps, wheel condition
4. **Check backgrounds** — Dealer forecourt (more trust) vs dark alley (red flag)
5. **Note what's MISSING** — Strategic omissions are red flags
6. **Be objective** — Report findings factually, let user decide

**Remember:** Photos can hide issues but rarely lie. A good visual inspection can save the user thousands in unexpected repairs.
