---
name: travel-safety-etiquette
description: >-
  Generate a visually rich, card-based HTML info page covering city safety overview, local taboos & legal etiquette,
  emergency contacts, and transportation tips for a given travel destination.
  Use when the user mentions travel safety, cultural taboos, local etiquette, travel risks, destination tips,
  or asks "去XX要注意什么""旅行禁忌""安全提示""出行注意事项""当地法律""交通安全" etc.
---

# Travel Safety & Etiquette Companion v2

Generate a single-file HTML info card (card-based dashboard) with four modules for a specified destination.

## Compliance Rules (MUST follow)

**Strictly forbidden outputs:**
- Specific geographic coordinates, street names, or "how to visit" guides for slums, shanty towns, or so-called "most dangerous neighborhoods"
- Voyeuristic or sensationalist framing of poverty or vulnerable communities
- Content that could be used to plan unauthorized entry into restricted or high-risk zones

**Allowed outputs:**
- General safety zoning using neutral language ("tourist-friendly area" vs "area requiring extra caution")
- Night-time and situational safety reminders
- Cultural, religious, and legal taboos
- Emergency contacts, consular info, and practical travel tools
- Transportation safety advice and common scam awareness

**Tone:** Use hedging language ("may / it is advisable / not recommended / exercise caution"); avoid alarmist or fear-mongering phrasing. Present information as helpful awareness, not warnings of danger.

**Zoning language guidelines:**
- Instead of "贫民窟 / slum / favela" → use "非主要旅游区域" or "游客较少到达的区域"
- Instead of "高风险街区 / dangerous neighborhood" → use "夜间建议结伴的区域" or "需额外留意的区域"
- Instead of "热门街区" → use "游客常去的区域" or "适合步行游览的区域"

## Input Variables

Collect from the user before generating. If unspecified, use defaults.

| Variable | Description | Default |
|---|---|---|
| `place` | Country / city / region | *(required)* |
| `time_of_day` | Primary travel time window | 全天 |
| `travel_party` | Travel style (solo / couple / family / group) | 结伴 |
| `pref` | Interest tags | 文化/美食 |

## Content Variables (Four Modules)

Research and populate all variables for the given `place`:

### Module 1: 城市安全概览与分区建议

| Variable | Count | Notes |
|---|---|---|
| `friendly_zone_1..4` | 3–4 | Tourist-friendly zones; use neutral "适合步行游览" framing |
| `caution_zone_1..3` | 3 | Situations/areas requiring caution; NO slum positioning or entry routes |
| `safety_tip` | 1 | One-line overall safety impression of the destination |

### Module 2: 当地禁忌与法律礼仪

| Variable | Count | Notes |
|---|---|---|
| `taboo_religion` | 1 | Religious / sacred site etiquette |
| `taboo_dress` | 1 | Dress code expectations |
| `taboo_public` | 1 | Public behavior norms |
| `taboo_law` | 1 | Legal prohibitions; use "may be illegal" hedging |
| `taboo_photo` | 1 | Photography restrictions and social norms |
| `taboo_topic` | 1 | Sensitive conversation topics to avoid |
| `taboo_tipping` | 1 | Tipping / service charge customs |

### Module 3: 紧急联系与实用信息

| Variable | Count | Notes |
|---|---|---|
| `emergency_police` | 1 | Local police number |
| `emergency_ambulance` | 1 | Ambulance / medical emergency number |
| `emergency_fire` | 1 | Fire department number |
| `embassy_info` | 1 | Chinese embassy / consulate contact (phone + address summary) |
| `useful_app_1..3` | 3 | Recommended local apps (ride-hailing, maps, translation, etc.) |
| `medical_tip` | 1 | Healthcare/pharmacy access tip |

### Module 4: 交通与出行安全提示

| Variable | Count | Notes |
|---|---|---|
| `transport_taxi` | 1 | Taxi / ride-hailing safety advice |
| `transport_public` | 1 | Public transport tips |
| `transport_walk` | 1 | Pedestrian safety notes |
| `scam_1..3` | 3 | Common tourist scams or schemes to watch for |

## Workflow

1. **Collect inputs** — Ask the user for `place` (required); infer or confirm the other variables.
2. **Research content** — Populate all content variables with accurate, balanced information. Cross-check facts where possible.
3. **Fill template** — Read `template.html` in this skill directory. Replace every `{placeholder}` with generated content.
   - For `{friendly_zone_4_optional}`: if a 4th zone exists, output `<li>content</li>`; otherwise output empty string.
4. **Output** — Save completed HTML as `.html` file and provide the link.

## Handling Edge Cases

- **Slum / danger zone requests:** If the user asks for specific slum locations or "most dangerous block" routes, redirect: explain how to stay safe by avoiding unfamiliar non-tourist areas at night, and suggest legitimate cultural alternatives (museums, exhibitions, certified community programs).
- **Overly broad destination:** If the destination is too broad (e.g. "Europe", "Southeast Asia"), ask the user to narrow down to a specific city.
- **Politically sensitive destinations:** Stick to factual travel safety information; avoid political commentary.

## Template

The full HTML template is in [template.html](template.html). Read it at generation time and fill in placeholders.
