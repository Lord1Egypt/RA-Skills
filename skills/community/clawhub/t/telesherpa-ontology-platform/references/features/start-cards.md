# Start cards: the team's front page, configured once

> Reference for agents. Status: available today, not a preview.

## 1. What a start card is

A start card is a saved link to an interface, published for a scope. Every member
who can read that scope finds it on the start page in the panel **"Startkarten fürs
Team"** — a panel of its own, deliberately not mixed with the personal favourites.

Two different things:

| | personal favourites | start cards |
|---|---|---|
| who configures | each user, for themselves | whoever manages the scope |
| visible to | that one account | everyone who reads the scope |
| MCP tools | `onto_favorite_*` | `onto_startcard_*` |

## 2. Visibility — both conditions, always

A card is shown to a user only if **both** hold:

1. the user can read the card's scope, and
2. the target interface is in that user's interface list, including the interface's
   own `access.require` gate.

Condition 2 is not cosmetic: without it the card would be a dead link for part of
the team, and a dead link on the front page is worse than no card.

There are **no roles on a card**. A card is for members, full stop.

## 3. Who may configure

Configuration requires managing at least one scope. An account that manages no scope
does not get the page at all — it answers with an access error, no table and no
"add" button, and the same holds for the endpoints behind it.

The menu entry sits under the settings and is hidden for accounts without that
right. A hidden menu entry is not a lock, though: the page and every endpoint check
again.

## 4. The page

The configuration page follows the platform pattern: a "+" button in the header, one
dialog for creating and editing, one for deleting, pencil and bin in each row, a
real form submit with a confirmation message. The same endpoints answer with JSON
when `format=json` is passed, so an agent can drive them.

## 5. Tools

| Tool | Purpose |
|---|---|
| `onto_startcard_index` | list the cards you may see |
| `onto_startcard_save` | create or change (`id` optional) |
| `onto_startcard_move` | `id` plus `dir` = `up` / `down` |
| `onto_startcard_delete` | `id` |

None of them takes a `roles` argument. Order is maintained by the move call.

## 6. "My area"

Do not build a special page for it. An interface can carry the **blocks** element and
inside it several building blocks (tables, cards), each with its own filters. That is
the supported way to give a workspace its own front page — and a start card can point
at it like at any other interface.
