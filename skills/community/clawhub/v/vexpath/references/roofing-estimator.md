# VexPath — Roofing Contractor Automation Module

> Full workflow: address in → roof measurements → waste calculations → material estimate → cold outreach → reply triage → CRM → calendar booking.

---

## 1. Roof Measurement via Google Solar API

### Step 1 — Geocode Address → Lat/Lng

```
GET https://maps.googleapis.com/maps/api/geocode/json
  ?address=<URL_ENCODED_ADDRESS>
  &key=<GOOGLE_MAPS_API_KEY>
```

**Parse:** `results[0].geometry.location` → `{ lat, lng }`

### Step 2 — Pull Building Insights

```
GET https://solar.googleapis.com/v1/buildingInsights:findClosest
  ?location.latitude=<LAT>
  &location.longitude=<LNG>
  &requiredQuality=HIGH
  &key=<GOOGLE_MAPS_API_KEY>
```

**Key response fields:**

| Field | Description |
|---|---|
| `roofSegmentStats[]` | Array of roof segments (area, pitch, azimuth) |
| `roofSegmentStats[].stats.areaMeters2` | Segment area in m² |
| `roofSegmentStats[].pitchDegrees` | Pitch in degrees |
| `roofSegmentStats[].azimuthDegrees` | Facing direction |
| `wholeRoofStats.areaMeters2` | Total roof area in m² |
| `solarPotential.panelsCount` | Panel count (use for validation) |

**Convert m² to ft²:** `area_ft2 = area_m2 × 10.7639`

---

## 2. Waste Calculation Engine

### Base Waste by Complexity

| Segments | Roof Type | Base Waste |
|---|---|---|
| 1–2 | Simple gable | 7% |
| 3–4 | Hip roof | 12% |
| 5–8 | Complex | 17% |
| 9+ | Very complex | 22% |

### Adjustments

| Condition | Adjustment |
|---|---|
| Pitch > 6/12 | +1% per pitch unit above 6/12 |
| Each segment beyond 4 | +1.5% per segment |
| Minimum waste | 5% (floor) |
| Maximum waste | 30% (cap) |

### Pitch Conversion (degrees → x/12)

`pitch_ratio = tan(pitch_degrees × π/180) × 12`

### Final Formula

```
waste = base_waste
      + max(0, pitch_ratio - 6) × 1
      + max(0, num_segments - 4) × 1.5
waste = clamp(waste, 5, 30)
```

---

## 3. Material Calculator

**Input:** `total_area_ft2`, `waste_percent`, `num_segments`

```
roof_squares       = (total_area_ft2 × (1 + waste_percent/100)) / 100
shingle_bundles    = ceil(roof_squares × 3)
underlayment_rolls = ceil(roof_squares × 1.1)
ridge_cap_bundles  = ceil(est_perimeter_ft × 0.15 / 33)   # 33 ln ft/bundle
drip_edge_sections = ceil(est_perimeter_ft / 10)           # 10 ft sections
starter_strip_ft   = est_perimeter_ft
nails_lbs          = ceil(roof_squares × 2.5)
ice_water_rolls    = num_valleys × 2                       # 2 rolls per valley
```

**Perimeter Estimate:** `est_perimeter_ft ≈ sqrt(total_area_ft2) × 4 × 0.85`
**Valleys Estimate:** `num_valleys ≈ max(0, num_segments - 2)`

---

## 4. Cost Estimation

| Material | Unit | Low | Mid | High |
|---|---|---|---|---|
| Architectural shingles | /bundle | $30 | $40 | $50 |
| Underlayment | /roll | $45 | $55 | $65 |
| Ridge cap | /bundle | $35 | $45 | $55 |
| Drip edge | /10ft section | $8 | $10 | $12 |
| Labor | /square | $75 | $100 | $125 |
| Tear-off (if needed) | /square | $25 | $37 | $50 |

### Total Estimate Formula

```
materials_low  = (bundles×30) + (underlayment×45) + (ridge_cap×35) + (drip_edge×8)
materials_mid  = (bundles×40) + (underlayment×55) + (ridge_cap×45) + (drip_edge×10)
materials_high = (bundles×50) + (underlayment×65) + (ridge_cap×55) + (drip_edge×12)

labor_low  = roof_squares × 75
labor_mid  = roof_squares × 100
labor_high = roof_squares × 125

total_low  = materials_low  + labor_low
total_mid  = materials_mid  + labor_mid
total_high = materials_high + labor_high
```

---

## 5. Storm Damage / Hail Outreach

### Identifying Affected Areas

| Source | URL | What to Pull |
|---|---|---|
| NOAA Storm Events API | `https://www.ncdc.noaa.gov/stormevents/` | Hail events by county/zip, date range |
| NWS Alerts | `https://api.weather.gov/alerts/active` | Active severe weather alerts |
| Local news / storm trackers | weather.com, spotter network | Ground truth verification |
| Hail maps | hailTrace.com, iri.columbia.edu | Visual storm path overlay |

### NOAA API Query

```
GET https://www.ncdc.noaa.gov/stormevents/csv
  ?eventType=Hail
  &beginDate_mm=MM&beginDate_dd=DD&beginDate_yyyy=YYYY
  &endDate_mm=MM&endDate_dd=DD&endDate_yyyy=YYYY
  &county=COUNTY_NAME&statefips=STATE_FIPS
```

### Building Address Lists

1. **County Assessor Data** — Most counties publish public property records with owner name, mailing address, and parcel data. Search `[county name] assessor property search public records`.
2. **USPS ZIP+4 Lookup** — Validate and normalize addresses before outreach.
3. **Public records aggregators** — PACER, county GIS portals, OpenAddresses.io.

---

## 6. Cold Email Templates

> ⚠️ **CAN-SPAM Compliance (required for all templates):**
> - Include your physical mailing address in every email
> - Provide a clear unsubscribe mechanism
> - Never use deceptive subject lines
> - Honor unsubscribe requests within 10 business days
> - Keep a suppression list and never re-contact opt-outs

---

### Template 1: Post-Storm Outreach

**Subject:** Quick question about your roof at [ADDRESS]

**Body:**
```
Hi [HOMEOWNER_NAME],

[NEIGHBORHOOD/CITY] was recently hit by [STORM_TYPE] on [STORM_DATE].
Based on storm reports, your area at [ADDRESS] may have sustained roof damage.

Many homeowners don't realize they have damage until it leads to leaks or
costly interior repairs — and most storm damage is covered by insurance.

We're offering free roof inspections for homeowners in [NEIGHBORHOOD] this week.
No cost, no pressure, no obligation.

If you'd like us to take a look and document any damage for a potential
insurance claim, reply to this email or call us at [PHONE].

[COMPANY_NAME]
[PHYSICAL_ADDRESS]
[CITY, STATE ZIP]
[PHONE] | [WEBSITE]

To unsubscribe from future emails, reply with "unsubscribe" in the subject line.
```

---

### Template 2: Aging Roof

**Subject:** Homes in [NEIGHBORHOOD] built in [YEAR_RANGE] — heads up

**Body:**
```
Hi [HOMEOWNER_NAME],

Roofs on homes in [NEIGHBORHOOD] built between [YEAR_RANGE] are reaching
the end of their typical lifespan (20–25 years for asphalt shingles).

We've been inspecting roofs in your area and wanted to give you a heads up
before small issues turn into expensive problems. Early signs of wear —
granule loss, curling edges, or soft spots — are easy to miss but important
to catch early.

We offer free inspections with no obligation. If everything looks good,
we'll tell you. If there's an issue, we'll walk you through your options.

Interested? Reply here or call [PHONE] to schedule a quick look.

[COMPANY_NAME]
[PHYSICAL_ADDRESS]
[CITY, STATE ZIP]
[PHONE] | [WEBSITE]

To unsubscribe, reply with "unsubscribe" in the subject.
```

---

### Template 3: Insurance Claim Help

**Subject:** [HOMEOWNER_NAME], your neighbor just got a new roof (insurance paid)

**Body:**
```
Hi [HOMEOWNER_NAME],

We recently helped several homeowners in [NEIGHBORHOOD] get full roof
replacements covered by their homeowner's insurance after storm damage —
at little to no out-of-pocket cost.

If your roof is 10+ years old or your area has had hail or wind events in
the past few years, there's a chance your insurance policy covers damage
you might not even see from the ground.

We specialize in helping homeowners navigate the claims process — from
inspection and documentation to working directly with your adjuster.

We'd love to do a free inspection and walk you through what we find. No
cost, no pressure. If there's no claim-worthy damage, we'll tell you.

Reply here or call [PHONE] to get on our schedule this week.

[COMPANY_NAME]
[PHYSICAL_ADDRESS]
[CITY, STATE ZIP]
[PHONE] | [WEBSITE]

To unsubscribe, reply with "unsubscribe" in the subject.
```

---

## 7. CRM Structure (Google Sheets)

### Column Headers

```
Address | Homeowner Name | Email | Phone | Roof Area (sq ft) | Segments |
Avg Pitch | Waste % | Est Cost Low | Est Cost High | Status |
Date Added | Last Contact | Next Follow-Up | Notes
```

### Status Values

| Status | Meaning |
|---|---|
| `New Lead` | Added to CRM, not yet contacted |
| `Contacted` | Initial email sent |
| `Replied` | Homeowner responded |
| `Inspection Scheduled` | Appointment booked |
| `Quote Sent` | Estimate delivered |
| `Closed Won` | Job awarded |
| `Closed Lost` | No sale, no follow-up |
| `Suppressed` | Unsubscribed / do not contact |

---

## 8. Calendar Integration

### When to Create an Event

Triggered when a reply is classified as **"Interested / wants inspection"**.

### Google Calendar Event Template

```
Title:    [COMPANY] Roof Inspection – [ADDRESS]
Location: [ADDRESS]
Duration: 1 hour (default)
Description:
  Homeowner: [HOMEOWNER_NAME]
  Phone: [PHONE]
  Email: [EMAIL]
  Est. Roof Area: [AREA] sq ft
  Notes: [REPLY_SUMMARY]
```

**Booking flow:**
1. VEX drafts event for approval
2. Human approves → create via Google Calendar API or manual entry
3. Send confirmation email to homeowner with time slot
4. Update CRM status → `Inspection Scheduled`

---

## 9. Email Reply Triage

| Reply Signal | Classification | Action |
|---|---|---|
| "interested", "yes", "schedule", "when can you come" | Interested | Draft inspection booking email → update CRM → create calendar event |
| "how much", "quote", "estimate", "cost" | Wants Quote | Generate estimate from Solar API → draft quote email |
| "not interested", "no thanks", "pass" | Not Interested | Mark `Closed Lost` → remove from follow-up queue |
| "already have", "using someone else" | Has Contractor | Mark `Closed Lost` |
| "insurance", "claim", "adjuster" | Insurance Question | Draft claims process explanation → offer free inspection |
| "remove", "unsubscribe", "stop", "DO NOT CONTACT" | Opt-Out | Mark `Suppressed` → add to suppression list immediately |
| Hostile / threatening language | Angry | Mark `Suppressed` → escalate to human review |

---

## 10. Full Workflow Summary

```
1. Identify storm-affected area (zip code / city)
2. Pull addresses (public records / assessor data)
3. For each address:
   a. Geocode address → lat/lng
   b. Hit Solar API → roof data
   c. Calculate waste + materials + cost estimate
   d. Add to CRM sheet (status: New Lead)
4. Batch cold outreach emails → HUMAN APPROVAL GATE → send
5. Monitor inbox for replies (VexPath email triage)
6. Classify replies → route:
   - Interested        → schedule inspection (calendar)
   - Wants quote       → generate + send estimate
   - Not interested    → Closed Lost + suppress
   - Insurance Q       → draft helpful response
   - Unsubscribe       → Suppressed immediately
7. Follow-up sequence for non-responders:
   - Day 3:  Gentle check-in
   - Day 7:  Value-add (tip or stat)
   - Day 14: Final attempt + close
8. Track all activity in CRM sheet
9. Weekly: review pipeline, move stale leads, update forecasts
```
