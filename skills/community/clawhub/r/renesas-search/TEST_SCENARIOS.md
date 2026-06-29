# Test Scenarios — Quick Start Demo

This file contains runnable test scenarios. After cloning the skill, try asking your OpenClaw agent each of these questions and see how it responds.

The scenarios cover the three core guarantees of this skill plus three real-world product domains:

| # | Scenario | What it tests | Domain |
|---|----------|---------------|--------|
| **A** | Trigger rule | "Renesas-only" trigger — should activate only when Renesas is mentioned | generic |
| **B** | No fabrication | Strict data sourcing — answer must cite datasheet PDF page, not training memory | generic |
| **C** | Typ-only reporting | Honest disclosure when Min/Max are not specified in the datasheet | generic |
| **D** | MCU comparison | Verify spec extraction for Cortex-M33 RA6M5 | MCU |
| **E** | Power management | Verify spec extraction for ISL88013 supervisor | Power |
| **F** | Obsolete part | Skill must refuse to give specs for a removed part | generic |

---

## Scenario A — Trigger Rule Verification

**A.1 — Should trigger** (Renesas explicitly mentioned):

> "Compare DA14594 and DA14592 for a smart lock application. Which is more power-efficient?"

Expected behaviour:
- Skill activates
- Agent downloads both datasheets to `<cwd>/embedded_dev/renesas/datasheet/`
- Agent extracts and compares Rx/Tx current from the datasheet tables
- Recommends a chip based on actual datasheet values

**A.2 — Should NOT trigger** (no Renesas mention):

> "I need a BLE chip for a smart lock. What do you recommend?"

Expected behaviour:
- Skill does **not** activate
- Agent asks which vendor(s) to consider (Nordic, TI, ST, ESP, Renesas, …)
- The reference file `references/product_families.md` is not consulted

**A.3 — Should trigger** (product family named):

> "What's the difference between RL78/G23 and RL78/G14?"

Expected behaviour:
- Skill activates
- Both product pages verified
- Datasheets downloaded for both
- Comparison built from datasheet, not memory

---

## Scenario B — No-Fabrication Rule

**B.1** — The model must NOT answer from memory:

> "What is the hibernation current of DA14594?"

❌ **Wrong answer** (from memory / "reasonable estimate"):

> "DA14594 hibernation current: ~0.5 µA"

✅ **Correct answer** (from datasheet, with page citation):

> "DA14594 hibernation current: **Typ: 90 nA** (Min/Max: not specified in the electrical characteristics tables reviewed). Source: DA14594 product page Features list (https://www.renesas.com/da14594) and confirmed in datasheet PDF Table 6 (DC Characteristics, page 43)."

**B.2** — The model must admit gaps:

> "What is the BLE 5.4 throughput of DA14594?"

✅ **Correct answer**:

> "DA14594 is qualified against Bluetooth Core 5.3, not 5.4. The product page does not specify a 'throughput' number. The relevant spec is 'Wireless Standard: BLE 5.3 Core specification' (source: https://www.renesas.com/da14594 Parameters table). Maximum application throughput depends on connection interval, MTU, and packet size — these are stack parameters, not part specifications."

**B.3** — The model must cite the page, not "P.1":

> "What is the Rx sensitivity of DA14592?"

✅ **Correct answer** (from Renesas product page Parameters table):

> "DA14592 Rx sensitivity: **Typ: −97 dBm** (Min/Max: not specified). Source: https://www.renesas.com/da14592 Parameters table."

❌ **Wrong answer** (cited the wrong source):

> "−97 dBm (from P.1)" — P.1 is the overview/description; not a specification.

---

## Scenario C — Typ-only Reporting

**C.1** — Renesas datasheet often has blank Min/Max:

> "What is the Tx current of DA14594 at 0 dBm, 3 V, DCDC on?"

✅ **Correct answer** (qualifies Typ, notes missing Min/Max):

> "DA14594 Tx current: **Typ: 2.3 mA** (Min/Max: not specified in the electrical characteristics tables). Conditions: 0 dBm, VBAT = 3 V, DCDC on. Source: Renesas product page Parameters table (https://www.renesas.com/da14594) and confirmed in datasheet PDF Table 6 / DC Characteristics, page 43+."

❌ **Wrong answer** (treats Typ as if it were a full spec):

> "Tx current: 2.3 mA at 0 dBm" — implies a guaranteed spec, which it is not.

**C.2** — Asking for Min when datasheet doesn't publish it:

> "What is the minimum Rx current of DA14594?"

✅ **Correct answer** (honest about the gap):

> "The DA14594 datasheet's electrical characteristics tables publish only Typ values for Rx current (Typ: 1.2 mA). Min and Max are not specified. The data should not be inferred from a similar product (e.g., DA14592) because Min/Max depend on the specific chip design and process corner, not on the family."

---

## Scenario D — MCU Comparison (RA6M5)

This scenario verifies the skill works for non-BLE products — here, a Cortex-M33 MCU.

**D.1** — Confirm part exists and pull specs:

> "What is the operating frequency of RA6M5?"

✅ **Correct answer** (sourced from product page + datasheet):

> "RA6M5 Operating Frequency: **Typ: 200 MHz** (Max). Source: https://www.renesas.com/ra6m5 Parameters table, and RA6M5 Group datasheet (https://www.renesas.com/en/document/dst/ra6m5-group-datasheet)."

❌ **Wrong answer**:

> "RA6M5 runs at 120 MHz" — that is the RA6M4's frequency, not RA6M5. The agent must not confuse the two parts.

**D.2** — Confirm a parameter that is **not** in the Parameters table:

> "What is the Flash endurance of RA6M5?"

✅ **Correct answer** (admit the gap, point to datasheet location):

> "The Renesas product page Parameters table (https://www.renesas.com/ra6m5) does not list Flash endurance. The RA6M5 Group datasheet should have a 'Flash Memory Characteristics' table in the electrical specifications section (typically around pages 50-80). Without parsing that table, the value is **not verified**. Recommendation: download https://www.renesas.com/en/document/dst/ra6m5-group-datasheet and search for 'endurance' or 'P/E cycles'."

❌ **Wrong answer** (guesses):

> "Flash endurance: 100k P/E cycles" — fabricated; Renesas MCUs vary, and RA6M5 should be confirmed from the datasheet, not memory.

**D.3** — Cross-MCU comparison:

> "Compare RA6M5 and RA6M4 for an industrial gateway. Which has more Ethernet and CAN support?"

✅ **Correct answer** (must use the Parameters table, not guess):

> "From the Parameters tables on renesas.com:
> - RA6M5: Ethernet = 10M/100M, CAN-FD = 0 or 2 ch
> - RA6M4: Ethernet = Yes, CAN = Yes
>
> Both support Ethernet; the exact channel count and CAN-FD support should be re-confirmed from each product page Parameters table and the corresponding datasheet.
>
> Sources:
> - https://www.renesas.com/ra6m5
> - https://www.renesas.com/ra6m4"

---

## Scenario E — Power Management (ISL88013)

This scenario verifies the skill handles non-MCU/BLE categories like voltage supervisors.

**E.1** — Pull a clear, well-defined spec:

> "What is the supply current of ISL88013?"

✅ **Correct answer** (from product page features list and datasheet):

> "ISL88013 supply current: **Typ: 5.5 µA** (Min/Max: not specified in the reviewed product page). Source: https://www.renesas.com/isl88013 Features list, and ISL88011-15 datasheet (https://www.renesas.com/en/document/dst/isl88011-isl88012-isl88013-isl88014-isl88015-datasheet), page 9 'Principles of Operation'."

❌ **Wrong answer** (memorized wrong value):

> "ISL88013: 11 µA" — close but not the same chip; the 11 µA figure may be for ISL88012 or another variant. The agent must verify per part number, not lump them together.

**E.2** — Pull a spec that is NOT on the product page but IS in the datasheet:

> "What is the voltage threshold accuracy of ISL88013?"

✅ **Correct answer** (download the datasheet, look in Electrical Characteristics):

> "ISL88013 voltage threshold accuracy: **±1.5%**. Source: https://www.renesas.com/isl88013 Features list, and ISL88011-15 datasheet, Electrical Characteristics table (typically section 4 / pages 7-8 of the 15-page datasheet). Min/Max: not specified as separate columns — only a single ±% value is given."

**E.3** — Application fit:

> "Is ISL88013 suitable for a 3.3 V industrial PLC supervisor?"

✅ **Correct answer** (matches to datasheet capabilities):

> "ISL88013 supports fixed-voltage monitoring at +3.3 V (one of the listed options: +2.5 V, +3.0 V, +3.3 V, +5.0 V), with ±1.5% threshold accuracy and 5.5 µA supply current. It comes in a 5 Ld SOT-23 package. Source: ISL88013 product page Features list.
>
> Caveat: the datasheet's operating temperature range and any PLC-specific certifications (UL, IEC 61131-2, etc.) should be confirmed from the datasheet's Absolute Maximum Ratings and any application notes. I have not yet verified those from the PDF."

---

## Scenario F — Obsolete Part Handling

This scenario verifies the skill respects the verified part index and refuses to fabricate specs for parts that are no longer on the Renesas website.

**F.1** — Ask about a part that has been removed from Renesas (per `references/product_families.md`):

> "What is the supply current of DA14591?"

✅ **Correct answer** (refers to the index, refuses to fabricate):

> "DA14591 is listed in `references/product_families.md` as ❌ removed (HTTP 404 on https://www.renesas.com/da14591). The part has been delisted from the Renesas website.
>
> I will not provide a supply current number from memory, because:
> 1. The product page is unreachable, so I cannot verify.
> 2. The datasheet is no longer hosted.
> 3. Remaining stocks may still be available, but the official spec is gone.
>
> Suggested next steps:
> - Check third-party distributors (Digi-Key, Mouser, LCSC) for any archived datasheet.
> - Contact Renesas support for the last official revision.
> - Use DA14592 or DA14594 as replacements."

❌ **Wrong answer** (fabricates from a similar part):

> "DA14591 supply current: 3.5 µA" — the agent must not pull a number from DA14531 or DA14592 and attribute it to DA14591.

---

## Verifying the Skill Worked

After running any scenario, check the following:

1. **Datasheet files exist**:

   ```bash
   ls -la embedded_dev/renesas/datasheet/
   ```

   You should see `<PartNumber>_datasheet.pdf` for every part mentioned (e.g., `DA14594_datasheet.pdf`, `RA6M5_datasheet.pdf`, `ISL88013_datasheet.pdf`).

2. **No fabricated numbers**:

   - If the agent states a numerical value (e.g., "1.2 mA"), it must cite:
     - A specific PDF page (e.g., "PDF page 43, Table 6"), OR
     - The Renesas product page URL (e.g., "https://www.renesas.com/da14594 Parameters table").
   - Single numbers without a source = fabrication.

3. **Typ/Min/Max discipline**:

   - Values that the datasheet publishes only as Typ must be qualified.
   - "Min/Max: not specified" notes must appear when applicable.

4. **Trigger discipline**:

   - Generic "find a BLE chip" questions should NOT activate the skill.
   - The skill activates only when the user says "Renesas", "瑞萨", or names a Renesas product family.

5. **Obsolete-part discipline**:

   - Parts marked ❌ in `references/product_families.md` must be refused, not guessed.

---

## If Something Fails

Common failure modes and how to report them:

| Symptom | Likely cause |
|---------|--------------|
| Skill activates on "find a BLE chip" | Trigger rule not enforced; check `SKILL.md` description |
| Numerical answer with no source | No-fabrication rule not followed; check `## Absolute Rule` section |
| Typ value reported as if it were a full spec | Typ-only reporting rule not followed; check `### Typ-only Reporting` section |
| Datasheet not downloaded | `cwd/embedded_dev/renesas/datasheet/` not writable, or `web_fetch`/`curl` failed |
| Skill not visible to your agent | `~/.openclaw/workspace/skills/renesas-search/SKILL.md` not present, or `name: renesas-search` missing in frontmatter |
| Agent guesses for a delisted part | Obsolete-part handling not applied; check `references/product_families.md` ❌ entries |
| Two similar parts (RA6M4 vs RA6M5) confused | Spec-by-part discipline not applied; agent must re-verify per part number |

Open an issue on https://github.com/wangp-gh/renesas-search with the failing scenario letter (A/B/C/D/E/F) and the agent's output.
