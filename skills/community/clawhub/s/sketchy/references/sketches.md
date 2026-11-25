# Sketches

Small pencil drawings of things, used instead of icons, clip art or emoji. Each one draws the object itself in 5 to 14 strokes, with at most one colored fill, inside a 140 x 110 viewBox. They boil with the rest of the page and trace themselves in when `data-draw` is set.

```html
<svg data-sketch="lightbulb-idea" viewBox="0 0 140 110" style="width:220px" aria-hidden="true"></svg>
<svg data-sketch="truck" data-draw viewBox="0 0 140 110" role="img" aria-label="A delivery truck"></svg>
```

- Size it with CSS width; the height follows. 120 to 320 px on pages, 240 to 700 px on slides.
- Decorative sketches get `aria-hidden="true"`. A sketch that carries meaning gets `role="img"` and an `aria-label`.
- `data-seed="2"` draws the same sketch with a different wobble, for when it appears twice on one page.
- Browse them all: open `dev/sketch-gallery.html` in this skill folder (search, family filter, day and night).

## Choosing

Pick the object the sentence is about, not an abstract symbol of it. "Costs fell" is `coin-stack`, not an arrow. "We hired three people" is `team-of-three`, not a plus sign. If nothing fits, draw a new one (below) rather than forcing a near miss; a wrong picture is worse than none.

## Catalog

### Business

| Name | Picture | Fits |
|---|---|---|
| `piggy-bank` | piggy bank with a coin | savings, budget |
| `coin-stack` | two coin stacks | cost, price, revenue |
| `handshake` | two hands shaking | deal, partner, agreement |
| `target-arrow` | arrow in a target | goal, target, accuracy |
| `trophy` | cup with a star | win, award, best result |
| `rocket` | rocket with sparkles | launch, release, growth spurt |
| `megaphone` | megaphone and sound waves | announcement, marketing |
| `briefcase` | briefcase | job, client, business trip |
| `receipt` | receipt with a torn edge | bill, expense, invoice |
| `invoice-stamp` | invoice with a stamp | approved, paid |
| `price-tag` | price tag | price, plan tier |
| `shop-front` | shop with an awning | retail, store, local business |
| `factory` | factory with chimneys | production, supply |
| `truck` | delivery truck | logistics, shipping |
| `pie-slice-hand` | hand holding a pie slice | market share, our part |
| `growth-plant` | plant in a pot | growth, early stage |
| `ladder-up` | ladder | career, steps up, progress |
| `bridge` | bridge | integration, transition, gap closed |
| `scale-balance` | balance scales | trade-off, fairness, compare |
| `hourglass` | hourglass | deadline, waiting, time left |
| `calendar-page` | calendar page | date, schedule |
| `signpost` | signpost | direction, options |
| `crossroads` | road fork | decision, two paths |
| `flag-summit` | flag on a mountain top | milestone reached |

### People and communication

| Name | Picture | Fits |
|---|---|---|
| `person` | one person | user, customer, owner |
| `two-people-talk` | two people talking | interview, meeting, support |
| `team-of-three` | three people | team, hiring |
| `speech-bubbles` | two speech bubbles | conversation, chat |
| `lightbulb-idea` | light bulb | idea, insight |
| `thought-cloud` | thought cloud | assumption, belief |
| `raised-hand` | raised hand | question, volunteer |
| `heart` | heart | care, loyalty, favorite |
| `eye` | eye | visibility, review |
| `ear-listen` | ear | listening, feedback |

### Tech

| Name | Picture | Fits |
|---|---|---|
| `laptop` | laptop | app, work, device |
| `phone` | phone | mobile, call |
| `server-rack` | server rack | infrastructure, hosting |
| `database-cylinders` | database cylinders | data, storage |
| `cloud-upload` | cloud with an up arrow | upload, cloud, backup |
| `lock` | padlock | security, privacy |
| `key` | key | access, credentials |
| `shield-check` | shield with a check | protected, compliant |
| `gear-pair` | two gears | process, automation |
| `robot-head` | robot head | AI, agent, bot |
| `chip` | microchip | hardware, compute |
| `plug-socket` | plug and socket | integration, connect |
| `wifi-waves` | wifi waves | network, signal |
| `bug` | beetle | bug, defect |
| `terminal-prompt` | terminal window with a prompt | command line, developer |
| `api-plugs` | two plugs joining | API, interface |
| `magnifier-doc` | document under a magnifier | audit, research, review |

### Teaching and science

| Name | Picture | Fits |
|---|---|---|
| `open-book` | open book | reading, lesson, docs |
| `graduation-cap` | graduation cap | course, certificate |
| `pencil` | pencil | write, draft, homework |
| `ruler-triangle` | ruler and set square | measure, geometry |
| `microscope` | microscope | detail, biology, investigate |
| `flask` | lab flask | experiment, chemistry |
| `atom` | atom | physics, science |
| `brain` | brain | thinking, memory |
| `globe-stand` | globe on a stand | geography, world |
| `compass` | compass | direction, navigation |
| `map-pin` | map pin | location, place |
| `light-switch` | light switch | on and off, toggle |
| `abacus` | abacus | counting, math |
| `chalkboard` | chalkboard | class, teaching |

### Health and life science

| Name | Picture | Fits |
|---|---|---|
| `syringe` | syringe with a dose and a drop | vaccine, injection, shot |
| `virus` | ball with round-tipped spikes | virus, infection, pathogen |
| `bacterium` | capsule with flagella and fine hairs | bacteria, microbe, germ |
| `cell` | animal cell with nucleus and organelles | cell biology, tissue, organism |
| `antibody` | Y-shaped antibody meeting two antigens | immune response, immunity |
| `dna-helix` | double helix with rungs | genes, heredity, genome |
| `pill-capsule` | capsule and two tablets | medicine, dose, treatment |
| `stethoscope` | stethoscope | doctor, checkup, diagnosis |
| `thermometer` | thermometer with a red column | fever, temperature |
| `bandage` | two crossed adhesive bandages | first aid, healing |
| `plant-cell` | plant cell with wall, vacuole and chloroplasts | plant biology, photosynthesis |
| `leaf` | leaf with veins | plants, nature, photosynthesis |

### Postal and space

| Name | Picture | Fits |
|---|---|---|
| `envelope` | envelope | message, letter, email |
| `parcel-string` | parcel tied with string | delivery, package, gift |
| `postage-stamp` | perforated stamp | covers, postcards, the house motif |
| `postcard` | postcard | summary, greeting |
| `mailbox` | mailbox | inbox, receiving |
| `planet-ringed` | ringed planet | far goal, space |
| `satellite` | satellite | remote, monitoring |
| `telescope` | telescope | vision, looking ahead |
| `star-sparkle` | sparkle star | highlight, new |
| `comet` | comet | fast, one-off event |
| `moon-phases` | moon in phases | cycles, phases, stages |

### Decision board set (from sketch-board)

`bug-button` (report a problem), `people-risk` (risk scoring), `cloud-person` (cloud accounts), `clock-waves` (scheduling in waves), `folder-watch` (periodic check), `notebook-check` (verification), `key-speech` (ownership), `mail-checklist` (review request), `dead-stop-button` (switch without effect), `linked-folders` (built-in link), `crossed-slip` (obsolete setting), `globe-search` (web search), `calendar-checks` (recurring check), `moving-box` (move, transfer), `four-eyes` (approval), `globe-download` (update feed), `mail-bell` (notification), `speech-tag` (labels, titles), `two-servers-crown` (failover leader), `gear-clock` (background jobs), `laptop-wrench` (developer mode).

## Drawing a new sketch

Register it in a script after `sketches.js` (or in your own file loaded after it):

```js
Sketchy.register('safe-box', function (p, C, parts) {
  p.rect(30, 30, 80, 60, { fill: C.yellow });        // body, one colored fill
  p.circle(70, 60, 26);                               // dial
  p.line(70, 60, 80, 52);
  p.text(70, 104, 'vault', { anchor: 'middle' });     // at most two or three words
});
```

Rules: stay inside 140 x 110; 5 to 14 primitives; one accent fill from `C` (never a raw color); green only for checks, red only for stop, wrong or the one thing; no arrow chains or flows; name it after the picture, not the feature; use `p.random()` and never `Math.random()`. Parts you can reuse: `parts.person`, `magnifier`, `envelope`, `globe`, `clock`, `check`, `planet`, `box3d`, `gear`, `cloud`, `star`, `lines`, `bubble` (signatures in `engine/sketches.js` and `engine/sketchy.js`).
