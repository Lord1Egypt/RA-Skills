# Tool traps — warehouse logistics

Read the platform list first:
[tool-traps.md](../../../telesherpa-ontology-platform/references/features/tool-traps.md).
This file only adds traps that showed up while describing warehouse labels and
stock bookings.

1. **The label code is not the UDID.** Inventing a code, or printing a QR that
   encodes the object id, builds a sticker the scan page will not bind the way
   this skill describes. Let the platform assign `code`. Verify Crockford Base32
   (12 characters plus a check digit, no `I`/`L`/`O`/`U`) on the read-back.
2. **Quantity lives on the package.** Writing `menge` onto the label, or treating
   a bind as a goods receipt, creates a second source of truth. Bind only sets
   `identifies` and `labelStatus`. Change `menge` only through the stock actions.
3. **Do not rename `frei` / `gebunden` / `gesperrt`.** `label_bind` and
   `label_rebind` are proven against those values. English values look neater and
   break the condition.
4. **A function in the wrong scope looks like a rights problem.** If
   `stock_putaway` (or pick, relocate, count) returns HTTP 403 with the message
   that the function is not allowed in this scope, the function's `scopes` list
   does not include the package's scope. Align the function; do not grant extra
   account rights.
5. **The platform scan chapter also describes other scan recipes.** Use that
   chapter for the HTTP contract, `ein_code`, prompts and `require`. Use this
   skill for labels and for the single-scan stock actions.
6. **Checkpoint codes and warehouse codes are different features.** Checkpoint
   rounds still document a QR that contains a raw UDID. Warehouse stickers print
   `/q/<code>`. Do not mix the two.
7. **Do not keep a second "current place" next to the movement.** The booking
   records the place on `movesTo`. Leave the package field `place` alone; do not
   also write a `concerns` slot link as a second truth.
8. **A reprint of the same charge must not be treated as "print more labels".**
   Count first, print, count again.
9. **A second bind is a rejected precondition, not a bug.** To hang the sticker
   on another package, use `label_rebind`. Do not delete `identifies` by hand
   to "fix" a second bind.
10. **Scan is HTTP, not MCP.** There is no `tools/list` entry for
    `match_actions`. Driving the scan only through `onto_object_execute_action`
    skips the page that staff will actually use — still run one real scan.
11. **The short URL hides the name before sign-in on purpose.** Do not try to
    "fix" that with a public scope or an unauthenticated view.
12. **Staff 404 on a warehouse label is fail-closed, not a failed bind.** Check
    the graph as manager before you grant extra rights.
13. **`remove: true` is still the general unlink trap.** If you ever detach a
    link, use `remove: "pair"`. `label_rebind` already replaces the edge.
14. **Prices come from `onto_credit_pricing` today.** A table in another skill
    or in yesterday's log is not the price. Quote the live key and the number
    you read; do not copy a figure from this skill.
15. **`ontouser_scope_types_set` replaces the list.** Activating `label` or
    `stockMovement` without including the types already on the scope will drop
    them.
16. **Relocate still needs a quantity input for the function.** The sign is
    zero, so `menge` on the package stays the same; the movement stores the
    quantity you passed. Pass the current book quantity (or another agreed
    figure) and read both values back.
17. **Count sets the book quantity absolutely.** There is no second correction
    row. The gap is the difference between the previous movement's resulting
    stock and the new `menge`. Put the reason in `grund`.
