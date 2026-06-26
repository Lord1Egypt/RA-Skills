# Naming: ubiquitous language, bounded context, and length

**Do this:** Put domain **nouns** on exported types, models, and public APIs. Inside a function or module, use **short names** when the parent (`function`, class, file path) already carries context—do **not** repeat that context on every local. If a name keeps growing, **extract** a smaller function or type instead of stacking words.

**Ubiquitous language** (DDD) is the vocabulary for *this* product—not “more English words per identifier.” **Bounded context** means readers resolve meaning from folder, type, and enclosing name; locals don’t need to restate it.

---

Good names come from the domain, not from universal English. Ubiquitous language is what domain experts and developers share for *this* product—it is **not** a universal rule that every variable must spell out full phrases.

## Ubiquitous language vs. repetition

- **Use domain terms** (`Shipment`, `LineItem`, `allocate`) where they encode business meaning—types, public APIs, aggregates.
- **Do not** repeat module or parent names on every inner identifier to sound “explicit”; that **noise** hides real domain words.

## Bounded context shortens safe names

A name is read with its context: sub-domain folder, file, enclosing type, function, or block.

- Prefer **`status` inside `finalizeShipment`** over `finalizedShipmentDeliveryStatus` when the function already implies shipment.
- Prefer **`items` inside `buildInvoicePreview`** over `invoicePreviewLineItems` when types document the rest.

Narrow scope → shorter locals often read **better** with their parent name.

## When verbosity is a smell

Treat long or stacked identifiers as a signal to **narrow scope** or **extract**:

- Repeated **prefixes** on locals → parent function/module may be doing too much; extract a unit whose **name** holds context once.
- **Colliding** concepts → split code paths or narrow types; don’t invent `userUserAccountProfile`-style names.

Long names to avoid refactoring make **renames** expensive for humans and agents (same strings repeated across lines and diffs without adding disambiguation).

## Checklist

- Domain vocabulary on **exports** and **models**; short **inside** when parent scope is obvious.
- If a local **restates** the function or file name, shorten it or fix the boundary.
- If names **grow** while nesting, **extract**—don’t compound identifiers.
