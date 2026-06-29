---
name: travel-checklist
description: Use when the user asks in Chinese or English what to pack, what to bring, what to prepare before leaving, or wants a trip-specific packing list/pre-departure checklist. 适用于旅行要带什么、行李清单、出门检查清单、packing list、travel checklist、亲子旅行、自驾、国外旅行、国内旅游、主题乐园、露营、徒步、雪山、高原、老人儿童同行等清单类请求。
---

# Travel Checklist

## Scope

Use this skill to produce packing lists and pre-departure checklists. Do not create full itineraries, book travel, provide visa or legal determinations, diagnose medical conditions, replace qualified guides, or claim current destination rules unless verified from official live sources.

## When to Use

| Use this skill when the user asks for... | Do not use this skill when the user asks for... |
| --- | --- |
| What to pack, what to bring, or what to prepare before leaving | A full day-by-day itinerary or route plan |
| A packing list, travel checklist, 出门检查清单, 行李清单, or pre-departure checklist | A binding visa, customs, medical, airline, or attraction policy determination |
| Destination-, traveler-, transport-, activity-, or luggage-style-specific preparation | Booking flights, hotels, tickets, tours, insurance, or vehicles |
| Child, older-adult, pet, medical-needs, cruise, road-trip, camping, hiking, skiing, beach, or theme-park packing guidance | Diagnosing symptoms, prescribing medication, or replacing a qualified guide for high-risk activities |

## Workflow

1. Extract trip facts from the request:
   - Destination and region: country, city, scenic area, theme park, beach, mountain, desert, border area.
   - Duration and season: number of days, month, weekday/weekend, likely weather.
   - Travelers: adults, children, infants, older adults, pets, medical needs.
   - Transport and lodging: international flight, domestic flight, train, self-driving, hotel, camping, cruise.
   - Activity profile: city sightseeing, hiking, theme park, photography, shopping, business, skiing, swimming.

2. If key facts are missing, make conservative assumptions instead of blocking. Ask at most one concise follow-up only when the checklist would be materially wrong without it, such as unknown child age, winter/summer ambiguity, or whether travel is international.

3. Produce a checklist that is specific to the destination and travelers, not a generic packing list. Include both packing items and pre-departure tasks.

4. Flag high-risk or easy-to-forget items first when relevant: passport, visa, ID card, child documents, medication, chargers, weather protection, booking confirmations, emergency contacts, and destination restrictions.

## Output Format

Match the user's language by default:
- If the user writes in Chinese, answer in Chinese.
- If the user writes in English, answer in English.
- If the user explicitly requests Chinese or English, use the requested language.
- If the request is mixed or language preference is unclear, default to Chinese.

Use the same language for the assumptions line, section headings, checklist items, optional labels, cautions, and "can buy locally" notes. Keep proper nouns, app names, document names, and destination names in their common form when clearer.

Start with a short assumptions line:

`按你的描述，我按「2名成人 / 日本 / 7天 / 酒店住宿 / 常规城市观光」来生成；如人数、季节或孩子年龄不同，清单需要微调。`

`Based on your request, I am assuming "2 adults / Japan / 7 days / hotel stay / regular city sightseeing"; if the season, group size, or child age differs, adjust the checklist.`

Then use sections with checkboxes. Use Chinese headings for Chinese output and English headings for English output:

| Chinese | English |
| --- | --- |
| 证件与出行文件 | Documents and travel files |
| 钱包、支付与通讯 | Money, payment, and connectivity |
| 衣物与鞋包 | Clothing, shoes, and bags |
| 洗护与日用品 | Toiletries and daily essentials |
| 药品与健康 | Medication and health |
| 电子设备 | Electronics |
| 目的地专项 | Destination-specific items |
| 儿童/老人/特殊人群专项 | Children, older adults, or special needs |
| 出门前检查 | Pre-departure checks |
| 不建议携带或可到当地购买 | Not recommended or can buy locally |

Keep items concrete. Prefer "护照原件、签证/入境许可截图、机票酒店订单离线保存" over "证件"; prefer "passport, visa or entry permit screenshots, offline copies of flight and hotel bookings" over "documents".

## Destination Rules

For international trips:
- Include passport validity, visa or entry permit, customs restrictions, roaming/eSIM, travel insurance, overseas payment backup, plug adapter, emergency contact, and copies of key documents.
- Mention that rules can change and should be checked against official sources close to departure if the user asks for visa, customs, medication import, or entry policy details.

For domestic China trips:
- Include ID card, health/insurance basics, local climate layers, sunscreen or cold protection, local transport apps or offline maps, and region-specific safety.
- For Xinjiang, Tibet, border regions, deserts, high altitude, or long-distance routes, add ID checks, sun/wind protection, dry climate care, larger power bank planning within airline limits, and long transfer snacks/water.

For theme parks:
- Prioritize lightweight day-pack items: tickets/ID, power bank, sunscreen, rain poncho, small snacks where allowed, water bottle if permitted, comfortable shoes, spare socks, stroller or child comfort items.
- Add child-specific safety items: contact card, photo of child outfit that day, small toy, spare clothes, fever medicine if appropriate.

For children:
- Ask or infer age band when possible: infant, toddler, school-age, teen.
- Include documents, spare clothes, snacks, water, wet wipes, medication, sleep comfort item, entertainment, stroller/car seat when relevant, and emergency contact card.

For outdoor or climate-heavy trips:
- Match the list to likely conditions: rain, cold, snow, heat, sun exposure, insects, dry air, altitude, hiking distance.
- Include safety and layering items before optional comfort items.

## High-Risk Outdoor Trips

For snow mountains, high-altitude trekking, wilderness crossings, desert crossings, routes with river crossings, unsupported remote routes, or trips where rescue and evacuation may be difficult, read `references/high-risk-outdoor.md` before answering.

## Scenario Coverage

Add scenario-specific sections only when relevant. Do not include every section by default.

Climate and season:
- Cold or snow: thermal layers, gloves, hat, scarf, snow boots or anti-slip covers, hand warmers, moisturizer, lip balm.
- Heat or beach: sunscreen, sunglasses, hat, swimsuit, quick-dry towel, sandals, after-sun care, waterproof phone pouch.
- Rainy season or typhoon risk: raincoat, waterproof shoe covers or spare shoes, waterproof bags, itinerary flexibility, weather alerts.
- Dry, windy, high-UV regions: moisturizer, lip balm, sunglasses, sun hat, long sleeves, nasal spray if useful, extra water planning.

Transport:
- Flight: ID/passport, boarding documents, airline luggage limits, liquids in carry-on, power bank in carry-on, neck pillow or earplugs for long flights.
- Train or long-distance bus: ID, easy-access snacks, water, tissues, wet wipes, light blanket or jacket, entertainment, compact wash kit for overnight rides.
- Self-driving: driver's license, vehicle documents, insurance, offline maps, car charger, tire pressure check, emergency triangle, reflective vest, fuel and rest-stop planning.
- Cruise, RV, or camping: motion sickness medicine, compact storage, power adapters, quick-dry items, flashlight or headlamp, campsite or cabin-specific supplies.

Travelers:
- Infant: diapers, wipes, formula or feeding supplies, bottles, spare clothes, comfort item, stroller or carrier, age-appropriate medicine.
- Toddler or school-age child: snacks, water bottle, spare clothes, entertainment, contact card, photo of the child's outfit that day, fever medicine if appropriate.
- Older adult: daily medication plus spare days, medical summary, comfortable shoes, warm layer, mobility aid, emergency contacts.
- Pregnant traveler: medical records, permitted medication, compression socks if needed, comfortable shoes, snacks, hydration, hospital information near destination.
- Medical needs: prescription medicine in original packaging when relevant, doctor's note for controlled medication, cold-chain plan if needed, insurance and emergency contacts.
- Pets: carrier, leash, food, water bowl, waste bags, vaccination records, pet-friendly lodging confirmation.

Activities:
- Skiing: ski gloves, thermal layers, goggles, face cover, sunscreen, lip balm, protective gear, spare socks.
- Hiking or mountain trips: broken-in hiking shoes, layers, rain shell, trekking poles if needed, headlamp, water, energy snacks, first-aid basics.
- Diving, surfing, or water sports: swimsuit, rash guard, reef-safe sunscreen where required, waterproof bag, towel, personal gear, motion sickness medicine.
- Photography trips: camera body/lenses, batteries, charger, memory cards, cleaning cloth, tripod if needed, rain cover.
- Concerts, festivals, or events: tickets, ID, power bank, earplugs, small bag that meets venue rules, rain/sun protection.
- Business travel: laptop, charger, adapters, formal clothes, business cards if used, backup presentation files, invoice or reimbursement records.
- Visiting family or friends: gifts, address/contact details, personal toiletries, sleepwear, any items requested by the host.
- Shopping trips: foldable bag, luggage weight allowance, payment backup, customs allowance awareness for international travel.

Luggage strategy:
- Carry-on only: reduce liquids, prioritize quick-dry clothing, use solid toiletries, avoid bulky backups.
- Checked luggage: separate one-day essentials and important documents into carry-on, protect liquids, leave room for return items.
- Minimal packing: separate "must bring" from "can buy locally" aggressively.
- Multi-city trip: favor mix-and-match clothes, packing cubes, laundry plan, smaller luggage, easy-access daily essentials.

Home pre-departure:
- Check water, electricity, gas, doors, windows, appliances, trash, refrigerator perishables, plants, pets, parcel delivery, and emergency contact sharing.

## Quality Bar

- Do not overpack. Mark optional items as "可选" in Chinese output or "optional" in English output, or place them in a separate section.
- Avoid vague filler such as "生活用品若干", "miscellaneous items", or "etc.". Name the items.
- Separate "must bring" from "can buy locally" when the destination has easy shopping access.
- Include quantities when duration matters, for example underwear/socks by day count plus one spare set.
- Include pre-departure tasks, not only luggage contents.
- Avoid claiming current entry rules, airline battery rules, or attraction policies unless verified live from official/current sources.

## Output Self-Check

Before answering, verify:

- [ ] The response starts with an assumptions line in the user's language.
- [ ] The checklist includes both packing items and pre-departure checks.
- [ ] The sections are relevant to the trip; irrelevant sections are omitted.
- [ ] At least one destination, traveler, transport, activity, climate, or luggage strategy detail is reflected.
- [ ] High-risk or easy-to-forget items appear before comfort or optional items.
- [ ] Optional items are marked separately or labeled "可选" / "optional".
- [ ] Items that can be bought locally are separated when shopping access is easy.
- [ ] No current visa, customs, airline battery, cruise, attraction, or medication-import rule is stated as verified unless live official sources were checked.
- [ ] The answer stays a checklist, not a full itinerary.

## Common Mistakes

- Turning a checklist request into a full itinerary. Keep route and timing details minimal unless needed for packing.
- Including every possible section for every trip. Add only relevant sections.
- Overpacking city trips with outdoor, camping, or emergency gear that the request does not imply.
- Treating high-risk outdoor equipment as making the trip safe. Say it reduces risk and requires qualified planning.
- Giving fixed legal, visa, customs, airline, cruise, or attraction rules without live official verification.
- Mixing output languages. Match the user's language for headings and checklist text unless they request otherwise.
- Using generic items such as "documents", "toiletries", or "miscellaneous" without concrete examples.

## Test Matrix

Use these scenarios to spot-check future edits:

| Scenario | Expected behavior |
| --- | --- |
| 中文普通旅行："去成都玩4天要带什么？" | Chinese checklist, conservative assumptions, city-weather and pre-departure checks |
| English carry-on only: "What should I pack for 10 days in Italy with carry-on only?" | English checklist, carry-on constraints, can-buy-locally split |
| Mixed language: "去新加坡 5 days with toddler, packing list please" | Default Chinese unless user clearly asks English; include toddler and international items |
| Parent/child beach trip | Child safety, sun, water, spare clothes, cleanup, and pre-departure checks first |
| High-risk outdoor route | Read `references/high-risk-outdoor.md`; risk controls before gear |
| Rule-sensitive request: "Can I bring this medicine into Japan?" | Do not decide legality; give packing precautions and tell user to verify official sources |

## Example Prompts

- "我要去国外日本旅游一周，需要带什么？"
- "我要去新疆伊犁旅游七天，给我生成检查清单。"
- "我要带孩子去上海迪士尼玩一个周末，帮我看看带什么东西？"
- "我打算去云南爬哈巴雪山，需要带些什么？"
- "我打算去走狼塔C+V，需要带什么？"
- "我带3岁孩子去新加坡玩5天，只带登机箱，怎么打包？"
- "我要去北海道滑雪一周，需要准备什么？"
- "我带老人去西藏旅行10天，需要检查清单。"
- "What should I pack for a 10-day trip to Italy with carry-on only?"
- "Can you make a pre-departure checklist for a family beach trip with a toddler?"
- "I am going to Iceland in winter for a week. What should I bring?"
- "What should I pack for my first cruise, and what should I leave at home?"
