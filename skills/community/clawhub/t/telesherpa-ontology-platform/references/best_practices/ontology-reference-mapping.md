# Reference Ontologies and Standard Mapping

**Who this is for:** An agent that configures object types and properties for a company — and
needs to know how the platform's data model relates to established standards.

**Why:** Customers come from SAP, ServiceNow, Planon, Salesforce. If a term is recognizable,
that shortens the migration. This file is the translation table.

**Important — schema changes:** creating object types, property sets and property
definitions is the platform operator's job. A customer agent **reads** the schema and uses the
**existing** types and properties to the full extent; a type it needs is a service request.

---

## 1. The Catalog Idea

The platform provides a **large, standards-conformant catalog** from which the customer
chooses — instead of every customer inventing their own model. That is the difference from
SAP/ServiceNow: there you get a model that you first have to adapt at considerable effort. Here,
the selection is the configuration.

**When configuring, therefore:** before you suggest a custom type, check whether the catalog
already has a standards-conformant one. A self-invented type is the second-worst solution;
the worst is two similar types side by side.

---

## 2. What the platform's model looks like

**The catalog comprises two inventories:**
- **Legacy types** — object types that have grown organically
- **Catalog types (space/location family)** — added in a standards-conformant way:
  `site`, `floor`, `zone`, `space`, `outdoorArea`, `land`

| Object type | Corresponds to (standard) |
| --- | --- |
| `building` | Brick `Building` · REC `Building` · ISA-95 `Site` level |
| `site` | Brick `Site` · ISA-95 `Site` · REC `RealEstate` |
| `room` | Brick `Space` · REC `Room` · ISA-95 `Work Center` |
| `space` | Brick `Space` · REC `Space` |
| `floor` | Brick `Floor` (**storey**) · REC `Level` |
| `zone` | Brick `Zone` (HVAC/Lighting/Energy/Fire) |
| `outdoorArea` | Brick `Outdoor_Area` · REC `OutdoorSpace` |
| `land` | REC `Land` |
| `machine` | Brick `Equipment` · REC `Device` · ISA-95 `Equipment` |
| `tool` | ISA-95 `Equipment` (tool) |
| `person` | Brick `Occupant` · REC `Agent`/`Person` · ISA-95 `Personnel` |
| `car` | ISA-95 `Equipment` (vehicle) · FIWARE `Vehicle` |
| `aed` | Brick **`Automated_External_Defibrillator`** (its own class!) |
| `baseStation` | TM Forum `Resource` · SAREF4CITY |
| `radioTower` | TM Forum `Resource` · SAREF4CITY |
| `serviceVisit` | FIWARE `Service` · TM Forum `Service` |
| `serviceOrder` | TM Forum `Order` · ISA-95 `Process Segment` |
| `inspection` | TM Forum `Service` (inspection) |
| `changeRequest` | OSLC Change Management |
| `orderItem` | ISA-95 `Material` · TM Forum `Product` |
| `file` | REC `Information` |
| `comment` | — |
| `form`, `function`, `trigger`, `actiondef` | Platform mechanics, no standard counterpart |

**Documented:** Brick carries **`Automated_External_Defibrillator`** (class `Safety_Equipment`) —
the platform is already standards-conformant on this point. That is a sales argument,
not a coincidence. **Note:** the class is **not** called `AED` — that short name does not exist
in Brick. In ODTB (REC 3.3) a defibrillator class is entirely missing.

---

## 3. What exists in the standards and is (still) missing here

**The space/location family has been created.**
`site` · `floor` · `zone` · `space` · `outdoorArea` · `land` — with property sets and
standards-conformant labels (`mo.Site`, `mo.Floor_Level`, `mo.Zone`, `mo.Space`,
`mo.OutdoorArea`, `mo.Land`).

**i18n trap with the labels (important):**

- The type label is `mo.X`, the **translation key is `X` — without prefix.** Whoever creates the
  key with `mo.` produces an entry that nobody finds — the type then shows
  the raw key in the dropdown.
- **`Site` is already taken** (German „Gelände", from an earlier model). `create`
  rejects an existing key. The object type `site` therefore uses the **existing**
  value; if it is to be called „Liegenschaft", that is a **change** to the existing key (with
  side effects on existing data) — to be decided deliberately, not on the side.
- `Zone`, `Space`, `OutdoorArea`, `Land`, `Floor_Level` were free.

**Status:** Types are `active` and fully retrievable via `onto_type_show`. The German
texts are in the DB; the 15 translations (en/fr/it) are waiting for `review` + `export` —
those are **human steps**, not agent steps.

**Still open:**

| Gap | Standard term | Current state |
| --- | --- | --- |
| **Facility as generic term** | Brick `Equipment`, REC `Device` | only `machine`/`tool` — no shared generic term |
| **Sensor** | REC `Sensor`, Brick `Point` | missing (`machine` is a facility, not a measurement point) |
| **Measured value** | Brick `Point`/`Setpoint`, REC `Observation` | `samples`, `range` as properties on `radioTower` |
| **Zone** | Brick `Zone` | **created** (catalog type, must be enabled per customer) |

**Consequence for configuration:** Floors and zones now exist as catalog types — but they
must be **enabled** per customer (see section 4b). They are not
automatically visible in every customer.

---

## 4. The geodata pattern (mandatory for locations)

**This is the trap that catches every agent.** A location without coordinates is not
map-capable — and the UI only offers a geocoding button when the data is there.

**For every map-capable type, these five properties belong to it:**

```
latitude · longitude · city · postalCode · street
```

Present and visible via `onto_type_show` for: `building`, `car`, `person`, `radioTower`,
`aed` (fixed).

**Tools:** `onto_object_geocode` with `direction: geocode` (address → coordinates) or
`direction: reverse` (coordinates → address). With `apply: true` it writes directly.

**Rule:** Address first, then geocode, then check whether `latitude`/`longitude` were actually
written. Do not assume — `apply: true` can silently do nothing.

---

## 4b. Enabling catalog types — PRESETS

**The problem:** Object types are defined **globally**. A large catalog would show everything
to every customer.

**The solution: presets.** The customer chooses **bundles**, not individual types.

```
Preset-DEFINITION (global, maintained by Telesherpa):
  Name + list of the contained object types

Preset-SELECTION (per customer):
  Selection of the preset names for one's own scope
```

**Multiple presets are possible** — the type sets are **unioned**. That allows the
platform to be used for several business cases at the same time (e.g. radio network **and** fleet).

**Available presets:**

| Preset (internal name) | Types |
| --- | --- |
| `basis` | building, room, person, file |
| `gebaeudeverwaltung` | building, room, floor, zone, space, site, land, outdoorArea, machine, aed, person, file |
| `funknetz` | radioTower, baseStation, site, person, file |
| `feldservice` | machine, tool, aed, person, serviceOrder, building, room, file |
| `fuhrpark` | car, person, file, serviceOrder |
| `vollstaendig` | all 18 domain types (without platform mechanics) |

**Value format of the preset definition:** `{"label":"mo.Preset_X","types":[...]}`.
A plain array (legacy form) is still read — the label then falls back to the
internal name. The internal name (`funknetz`) is stable; only the label is
translatable.

**Labels are i18n keys — and need `export`.** If the label of a type is, for example,
`mo.Preset_Telecom`, then the i18n key is `Preset_Telecom` **without prefix** (see
section 3, i18n trap). As long as the translations are not exported, the
interface shows the raw key (`mo.Preset_Telecom`) instead of the translation — that is not an
error, but the open export step.

**Behavior:**
- **No entry** for a scope → **all** active types visible (existing behavior).
  That is intentional: the feature cannot cripple an existing installation. A customer
  who selects nothing notices nothing.
- **Entry present** → only the types of the selected presets appear.
- Multiple scopes of a user are unioned (additive).

**Where it takes effect:** in the object view (type filter) and in the app on type
selection. Filtered via the server-side type resolution or the app counterpart.

**Two paths, the same function — human and agent are on equal footing:**

| Path | Endpoint |
| --- | --- |
| **Human** (browser) | in the web interface: catalog selection with checkboxes and save |
| **Agent** (MCP) | `onto_catalog_presets`, `onto_catalog_index`, `onto_catalog_apply`, `onto_catalog_clear` |

Rights: **scope-based** (`can_manage_scope`), FAIL-CLOSED — whoever manages a scope sets
its presets, and nobody gets in without that right.

**Where the entry sits in the menu:** under **Settings** (not in the user menu) — it is a
configuration of the customer for their own scope, not daily work. The menu is configuration, not code.
An entry is `{"label":"mo.Catalog","url":"<path>","required_role":"..."}`.

**Terms (binding):**

- **Menu label:** `mo.Catalog` → „Katalog" (short, so that the sidebar stays calm)
- **Page title:** `mo.Catalog_Title` → „Objekttypen-Katalog" (precise, its own i18n key!)
- **Page headings:** `mo.Catalog_Presets`, `mo.Catalog_Selection`, `mo.Catalog_Hint`

Why **not** „Ontologie-Katalog": the platform uses „Ontologie" only as a header/title,
never as the customer's working term. And „Katalog" alone is unspecific — there are also
link definitions, property definitions and property sets alongside it. „Objekttypen-Katalog" is
unambiguous and lines up cleanly next to „Typen verwalten".

**Type names in the catalog are shown as a label**, not technically: `Gebäude (building)`,
`Person (person)`, `Funkmast (radioTower)`. Otherwise the catalog contradicts the
type list of the platform, which likewise shows label + code. The helper provides
`types_detail` (array of `{name,label}`) in addition to `types` (array of names) for this purpose.

**Visibility:** The menu entry is visible to everyone with the role `member` — which is
practically every customer. That is defensible because the rights are checked per scope:
without `can_manage_scope` the page is **readable**, but not changeable.

**Honest about it:** Whoever does not manage a scope sees a page on which they cannot change
anything. For a genuine self-service customer that is right (they manage their scope).
For third-party customers without their own scope the entry is noise — then `required_role`
or a scope condition in the menu would be the lever, not the controller.

**The presets are maintained by Telesherpa, not the customer.** New presets are a product decision.
The customer only chooses from what is there.

**Properties are NOT filtered separately.** Whoever enables a type gets its
properties along with it — they hang off the type. The filter dropdown of the object list continues to show all
defs: an object can carry properties that are not in the schema at all (form
fields are written as properties, without a def). A filtering would make these values
invisible.

### i18n review in the UI: hit areas

The accept/reject buttons of the review queue were `btn-xs` with **icon only** — around 22×18 px,
directly next to each other. On the phone that leads to mis-taps (actually happened: „Ablehnen"
instead of „Annehmen" for `Catalog_Title`/fr_FR). Rule for mobile actions:

- **Always text in addition to the icon** — an icon alone is no label.
- **At least 44 px hit height** (here `padding:12px; font-size:15px`).
- **Stacked on narrow screens** (`flex-direction:column`, full width, `gap:10px`),
  so that two opposing actions are never side by side.
- The labels come from existing keys (`mo.Accept` = „Akzeptieren",
  `mo.Reject` = „Ablehnen") — do not invent new keys for existing terms.

**Rejecting is not data loss:** a rejected suggestion remains as a row with
`status='rejected'`, the approved inventory is not touched. A renewed `translate` with
the same key/locale creates a new `pending` suggestion (the review endpoint accepts only
`pending`). So it is repairable — but only if you notice it.

**Trap with `i18n create`:** The endpoint rejects taken keys (`Key existiert bereits`) and
there is **no** update endpoint. Whoever wants to change menu label and page title therefore needs
**two separate keys** (`mo.Catalog` for the menu, `mo.Catalog_Title` for the page) —
not the same key occupied twice.

**Important for the agent:** If a catalog type is missing from the dropdown although it has
`status='active'`, its preset is not enabled for this customer. That is configuration, not a bug —
do not work around it by creating a second, similar type. Enable the matching preset
instead.

---

## 5. Sets and schema are two sources — the most important trap

The platform shows properties in **two** ways, and historically they were not congruent:

| Path | Source | Who sees it |
| --- | --- | --- |
| **Schema introspection** | `onto_property_def_index` | the **agent** via `onto_type_show` |
| **Object view** | `onto_property_set_index` (+ `onto_property_def_index`) | the **human** in the UI |

**Two states that need to be understood:**

- **`display_mode='auto'`** — the set is shown automatically, grouped, in the object view
- **`display_mode='manual'`** — visible only in interfaces/cards
- **Properties in no set** — appear in the UI as a flat list below the sets
  (in the interface: „nicht zugeordnete Felder")

**Important (has occurred before):** Properties can be visible in the interface
but missing from the agent schema — then an agent creates objects without these values.

**Rule:** If a property appears in the UI but is missing in `onto_type_show` (or
vice versa), that is a **mapping error** — report it, do not work around it by guessing.

---

## 6. Property types and what they can do

The UI offers: `string` · `int` · `float` · `datetime` · `bool` ·
`options`.

- **`options`** needs JSON: `[{"value":"1","label":"Ja"},{"value":"0","label":"Nein"}]`
- **`datetime`** knows relative defaults: `0` (today), `+30`, `-365` (days)
- **`computed`** makes a field calculated instead of manual (JSON formula).
  Example from the existing inventory: `serviceStatusComputed`, `maintenanceOverdue`
- **`required`** is currently rarely set — most fields are optional

**Labels** are `mo.*` keys: they run via the server's language files (4 languages),
**not** via the platform's i18n management. Creating new labels: `create` + `translate`
(agent), `review` + `export` (human).

---

## 7. Standard provenance and license (important for compatibility statements)

Verified against the LICENSE files of the repositories or the ontology files:

| Standard | License | Usable as |
| --- | --- | --- |
| **Brick Schema** | **BSD-3-Clause** (Brick Consortium, Inc.) | adopt classes/properties, attribution |
| **RealEstateCore** | **BSD-3-Clause** (RealEstateCore Consortium) | adopt classes/properties, attribution |
| **Azure opendigitaltwins-building** | **MIT** (Microsoft Corporation) | adopt classes, attribution |
| **FIWARE Smart Data Models** | **CC BY 4.0** — evidenced via the group repos and the FIWARE organisation's `contribution-agreement.md` (not part of this skill). **Restriction:** the individual `dataModel.*` repos have no LICENSE.md of their own (GitHub reports `NOASSERTION`), and the badge in the umbrella README is commented out in the HTML | adopt entities, **attribution required** |
| **SAREF (ETSI)** | **ETSI Software License = BSD-3-Clause** — via `dcterms:license` in every TTL. **Note:** the normative specification text (TS 103 264 PDF) is **not** covered by it („© ETSI 2025. All rights reserved."), no license term appears there | ontology IRIs/serializations free, **specification text not** |
| **ISA-95 (IEC 62264)** | **proprietary** (standard 454–470 USD). **Free:** the B2MML XSDs from MESA International (attribution suffices) | not the standard text, yes the XSD schemas |
| **TM Forum SID** | **proprietary** for the Models Suite (members only). **Free:** ITU-T M.3190 (freely accessible) and the **Open APIs (Apache 2.0)** | SID terms via ITU/Open APIs, not the Models Suite |
| **OSLC** | **CC BY 4.0 + Apache 2.0** (OASIS OSLC Open Project) | free, no login |
| ServiceNow CSDM · SAP ODM · Planon | proprietary | read as reference only, **not** adopt |
| Deloitte `sap-ontology` | **CC BY-SA 4.0** | **Caution:** ShareAlike — derivative works must be licensed the same way |

**Rule:** For any outward compatibility statement, always check the license. „We are
compatible with X" is a different statement than „we have adopted X". For Brick and REC,
name the consortia explicitly — attribution is a license condition.

---

## 7b. Order of magnitude of the standards (for expectation management)

| Standard | Scope | Version |
| --- | --- | --- |
| Brick Schema | **1,469 classes**, 82 ObjectProperties + 8 DatatypeProperties | 1.5.0 |
| RealEstateCore | **270 own interfaces** (+ 1,094 embedded Brick) | 4.1 |
| Azure opendigitaltwins-building | **766 interfaces** | REC 3.3 (older state) |
| FIWARE Smart Data Models | **82 repos, 1,118 entity types** | as of 2026-07-19 |
| SAREF Core | 30 classes · 62 ObjectProperties | 4.1.1 (TS 103 264) |
| SAREF4BLDG | 65 classes · 81 DatatypeProperties | 2.1.1 |
| ISA-95 / IEC 62264 | 8 parts + TR95.01 | — |

**This is the most important number in this file:** Brick alone has 1,469 classes. A 1:1 mapping
is therefore **not** a viable path — it would make the catalog unusable. The catalog picks out
specifically the classes that carry a real use case.

---

## 7c. Naming traps (check before creating!)

**`floor` — the most dangerous trap:**

| Standard | `Floor` means |
| --- | --- |
| **Brick** | **Storey** (`Floor` under `Location`, with `Basement`, `Parking_Level`, `Rooftop`) |
| **Azure ODTB** | **Floor slab** (`Floor` under `BuildingComponent`) — **not** the storey! |
| **RealEstateCore** | does not know `Floor` at all — there it is called **`Level`** (`levelNumber`) |

Whoever says „Floor" and means storey must create `floor` and declare it **explicitly** as a storey
in the docs. Whoever does not do that inherits the ODTB ambiguity.

**Further divergences between the standards:**

- `Wing` (building wing) exists **only in Brick** — not in REC, not in ODTB
- `Outdoor_Area` only in Brick; REC/ODTB call it **`OutdoorSpace`**
- `Site` is missing in ODTB (present in Brick and REC 4.1)
- `Land` only in REC 4.1, not in ODTB
- **Measured values are modeled fundamentally differently:** Brick uses `Point` objects
  (`Sensor`, `Setpoint`, `Command`, `Status`, `Alarm`, `Parameter`) with an external
  timeseries reference; REC/ODTB use **`Capability`** as a capability plus separate
  **`ObservationEvent`** objects. A catalog that maps only one of the two paths is
  not connectable for the other standard.

**Telecom gap:** For `baseStation`/`radioTower` **both** standards deliver almost nothing —
only `ICT_Equipment` (Brick) or `ICTEquipment` (ODTB) with `Server`, `Gateway`, `Router`,
`WirelessAccessPoint`. Mobile-radio-specific classes are missing. That is **not** an oversight of the
catalog, but a gap in the standards — name it as such externally.

---

## 8. Sources

- Brick Schema — `github.com/BrickSchema/Brick`, `bricksrc/location.py`, `bricksrc/equipment.py`
- RealEstateCore — `github.com/RealEstateCore/rec`, docs `doc.realestatecore.io/3.2/core.html`
- Azure open digital twins building — `github.com/Azure/opendigitaltwins-building` (MIT)
- FIWARE Smart Data Models — `fiware.org/smart-data-models`
- SAREF — `saref.etsi.org`
- ISA-95 / IEC 62264 · TM Forum SID · OSLC — standard documentation
