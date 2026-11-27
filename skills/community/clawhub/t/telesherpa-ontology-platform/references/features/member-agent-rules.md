# Rules for a member agent

> Reference for agents that build a workspace with normal account rights — no
> administrator access. These are the points such an agent gets wrong, and why.

## 1. Texts: keys through the API, never in the template

Visible text is not written into a page. It is a key, resolved per language
(de/en/fr/it).

- Create a key with `onto_i18n_create` — **without** a `mo.` prefix. That prefix
  belongs to the platform's own strings; a customer key carrying it lands in the
  wrong namespace and never resolves.
- Add a translation with `onto_i18n_translate`. Translations are **proposals**: an
  operator reviews and exports them. Until that happens the page shows the literal
  text you wrote — so "it looks right in German" proves nothing.
- Never edit a language file by hand. Those files are generated output, not a source.

A hard-coded German sentence is the classic failure: the workspace is finished, the
customer switches to English, half the page stays German.

## 2. Two modes per endpoint

Every endpoint you build answers in two modes, chosen by the `format=json` parameter:

- HTML: form submit, redirect back to the list, confirmation message.
- JSON: same logic, `{"result":"OK", ...}` or `{"result":"Error","error":"..."}` with
  a **real** HTTP status code.

Without the JSON mode you cannot verify your own work, and the customer cannot
automate anything later. The status code matters: an error returned as 200 is
invisible to every client.

## 3. Filters belong to the session, not to the URL

List filters are stored per view and per session. Filters in the query string leak
between users, break paging and end up in links that other people click. Business
data travels in the request body only — never in a URL that lands in a log or a
bookmark.

## 4. Permissions of a view are declared, not implied

`access.require` on each view:

| value | meaning |
|---|---|
| `"write"` | needs write on the scope of the shown data |
| `"manage"` | needs scope management |
| a number | needs that scope |
| missing | read is enough |
| anything unknown | denied |

A view that shows other people's data without `access.require` is a data leak, not a
matter of taste.

## 5. Placeholders

| placeholder | resolves to |
|---|---|
| `{current_user_email}` | e-mail of the acting account |
| `{current_user_id}`, `{current_user_profile_id}` | its identifiers |
| `{old:<field>}`, `{new:<field>}` | previous / new value, shown in the reader's time zone |
| `{now}` | current time |

`{old:...}`/`{new:...}` print seconds only when they are not `:00`. A value written
in one time zone and shown in another is the most common "the data is wrong" report
that turns out to be a formatting issue.

## 6. Deleting: one id at a time

Never delete by pattern, prefix or name. Show the list, then delete exact ids. Two
reasons: a pattern matches more than intended, and a delete has no undo. This holds
for probe objects you created yourself — the next object with a similar name may
belong to the customer.

## 7. Notes for colleagues, not for the browser

Comments belong in the server-side source. Anything written into the delivered HTML
is read by every customer, and internal reasoning does not belong there.

## 8. What you cannot do — and must not fake

- You cannot create object types outside the catalogue. File a service request.
- You cannot grant rights to other people; that is the scope manager's job.
- You cannot delete accounts through your own endpoints.
- You cannot grant yourself write access to get a write done. If a write is refused,
  the answer is an action with a target scope — see
  `references/features/scope-bridges.md`, not a grant.
