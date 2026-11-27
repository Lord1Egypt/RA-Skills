# The first 30 minutes — from zero to a system that works in operation

**Who this is for:** An agent that sets up the platform for a company and wants to show a result
within half an hour — not a demo, but something that is actually used the next morning.

**The promise in one sentence:** In 30 minutes there is a workflow for which other companies buy
a complete piece of software, spend months rolling it out, and then run Excel alongside it anyway.

---

## Why this works in 30 minutes

Because you install nothing, configure nothing and don't have to ask anyone for approval.
Every step below is a single tool call. There is no migration, no server, no role concept to
invent — the platform brings the structure along, you fill it.

And the most important point: **you only pay for what actually happens.** No setup price,
no monthly fee for unused licences. If nobody works with it after two weeks, it costs almost
nothing either. That is the reason why you can simply try it out.

---

## Minute 0–5 · Register and activate

```
register   username=customer's e-mail, password, password_confirm,
           accept_terms=true   <- REQUIRED (accepting the terms, otherwise HTTP 400)
           AGB: https://www.telesherpa.com/agb
```

Then the activation code arrives by e-mail. **No IMAP access needed:**

> **Pass this on to the human:** "I have created an account for us. In a minute an e-mail with an
> activation code will arrive. Give me the code and I will unlock the account."

The human reads the code out of their mailbox — done. After that:

```
activate            loginusername, loginpassword, voucher
login               → Bearer token + refresh_token
```

From here on, never a password again. `refresh_access_token` keeps the connection alive on its
own — even over weeks.

**What these 5 minutes produce:** a separate, self-contained data space for this
company. Not "an account on a platform where everyone is in the same place", but a
separate area that others cannot see.

---

## Minute 5–10 · The two scopes that carry everything

```
ontouser_scope_create   name="<firma>_arbeit"    → this is where the work happens
ontouser_scope_create   name="<firma>_archiv"    → this is where the results live
```

Just two of them — you don't need more on the first day. One is the workshop, the other
the archive. The separation is the whole trick: the employee writes in the workshop and cannot
break anything in the archive.

Later, when several teams are added, this grows as needed (more on that in
`references/best_practices/scope-organization-per-company.md`).

**Take this along right away (2 calls): define the image motifs.** The structured image storage tells
the employee in the app WHAT to photograph:

```
onto_scope_structuredimage_categories       scope_id=<arbeit>   → what already exists?
onto_scope_save_structuredimage_categories  scope_id=<arbeit>, categories=[...]
```

Four to six motifs are enough (`01_<Motiv>.jpg`, `02_<Motiv>.jpg`, `03_<Motiv>.jpg` …),
one each in `de` and `en` as the language variant of the same `imagename`, exactly one with
`thumbnail: true`. **The filename is the key later on** — if it does not match the
`imagename` exactly, only the placeholder appears. Example:
`references/features/structured-image-storage.md`.

**What these 5 minutes produce:** the permission structure. From now on, "may write" and
"may only read" are no longer a question of trust, but of technology.

---

## Minute 10–18 · The field visit as a form

Now the step that turns a database into a work tool: an action that an
employee performs on site.

```
onto_type_show         → which form, which fields exist?
prepare_form_answer    form_udid=<Formular>, scope_id=<arbeit>
submit_form_answer     form_udid, answer_udid, field values
```

On submission the decisive switch happens: **the answer moves automatically from the
work scope into the archive scope.** The employee created it — and can no longer change it
afterwards, because they have no write permission in the archive. Without a single object rule,
purely via the scope boundary.

**What these 8 minutes produce:** the paper slip is gone. The signature, the photo, the
ticked-off items are immediately where scheduling sees them — not in the car, not
in the mailbox, not "I'll bring it tomorrow".

---

## Minute 18–25 · Letting the employees in

```
create_invite_code   scope_id, can_read, can_write, allowlist, max_uses, expires_at
```

For the field staff: **`can_write` in the work scope, `can_read` in the archive.** Exactly the
role they need — no more and no less.

**The practical trick:** enter the allowlist as a domain ("everyone with @firma.de") — then nobody
has to type individual addresses. With changing subcontractors, the
XLSX bulk upload via `upload_code_allowlist` also works.

The code is meant to be passed on (`XXXX-XXXX`, without easily confused characters) — **it is
not a secret.** The employee redeems it and has their permissions. Done.

**What these 7 minutes produce:** onboarding that is not onboarding. No
"who gets which access", no password slip, no call to the boss.

---

## Minute 25–30 · Proving that it runs

```
onto_object_create     → create a test visit
onto_object_execute_action  → execute action
onto_object_search     → check: is it in the archive?
onto_credit_balance    → what did it cost?
```

Then the moment that convinces: **send the human a job that they see on their mobile
phone.** Via `create_service_order` it becomes a real task for a real human —
with the lifecycle open → accepted → done. When they close it, the result is in the
platform.

That is not a simulation. That is a digital job that reached a human.

### And answer the follow-up question automatically (rule)

The last step that saves operation: a **rule** (trigger) on the critical finding.
It needs no human and costs no credits:

```
onto_function_index  → does the invoice already exist?
onto_trigger_create  name="eskalation_kritisch", scope_id=<arbeit>, body={...}
```

```json
{"on":"insert","object_types":["inspection"],
 "condition":{"props":[{"key":"zustand","op":"eq","value":"kritisch"}]},
 "effects":[{"type":"create_object","object_type":"changeRequest",
             "name":"Eskalation: {object_name}",
             "props":{"status":"proposed","text":"Automatisch aus dem Standort-Check erzeugt."},
             "links":[{"linktype":"proposesChange","to":"{object_udid}"}]}]}
```

From now on a critical site check **automatically** becomes a case — visible to
the back office, without a phone call. **Don't forget `condition.changed` here**, otherwise the
rule fires for every field written. Details: `references/features/automation-and-functions.md`.

### Pick the human up on their mobile phone (PWA)

The platform can be installed on the home screen. Two things the human
notices immediately:

- **They stay signed in longer.** The web session runs for 30 minutes; in the installed
  web app a persistent login of up to 14 days is added — so they don't have to type password
  and 2FA on every visit.
- **Push notifications on iOS only come from there.** In the Safari tab the toggle only shows a
  hint. Installed = notifiable.

Details: `references/features/pwa-and-session.md`.

---

## What comes after — if it carries

### The marketplace: data becomes a business

The company does not only have to use data, it can **offer** it. A curated
stock — customer sites, assets, regions — is made public:

```
ontouser_scope_set_visibility   read_allowed_for=["PUBLIC"]
```

Other users work in it, and **every external use automatically credits credits** —
visible as `earnings_total` in the balance, offset directly against the credit. No
separate payout channel, no invoicing.

**Why this is strategically interesting:** The company collects this data in operation anyway.
Until now it lay in folders. Now it is a stock with a price — and the competition pays
to be allowed to use it.

### Outsourcing field work

Via ServiceOrders, tasks can be issued to external field service providers
(`complete_service_order` = 50 credits). What you don't want to drive to yourself becomes a
job that someone else completes — with photo proof in your own archive.

---

## What does this cost? (honestly calculated)

The prices are publicly listed in `onto_credit_pricing`, retrievable without login:

| Operation | Credits | EUR |
|---|---|---|
| Read (`graph`) | 1 | €0.01 |
| Create object (`create_object`) | 10 | €0.10 |
| Execute action (`execute_action`) | 10 | €0.10 |
| Complete job (`complete_service_order`) | 50 | €0.50 |

**Example — a company with 3 field staff, 10 visits each per month:**

One visit = execute action + three objects (site, photo, material item)
= 10 + 3×10 = **40 credits = €0.40**
→ 3 employees × 10 visits × €0.40 = **€12 per month.**

**What drops away for that:** phone calls for follow-up questions, re-sorting paper slips,
searching for photos in WhatsApp histories, writing up daily reports afterwards. If that saves
one hour of office work per day, the calculation is not tight — it is absurdly one-sided.

On top of that come one-off scope costs when more than the standard quota is needed
(e.g. 1 scope = 50 credits = €0.50). **Flat rate available** if billing should happen without
per-use deduction.

---

## What a managing director gets out of it — in their language

**Not:** "an ontology platform with objects, properties and scoped links."

**But:**

1. **Field staff document completely and immediately.** Not because they are more diligent, but
   because it is easier than the paper slip.
2. **Boss and back office see the status in real time.** Who was where, what was done, what
   is still missing.
3. **Permissions without additional software.** Freelancers get write permission where they
   need it — and no data access beyond that.
4. **Costs that breathe with usage.** Almost nothing in a quiet month, in a full month
   proportional. No license round that has to be explained.
5. **And a stock that can grow.** Your own data becomes potential for the
   marketplace — with automatic remuneration.

**The honest catch:** The benefit only arises when the employees actually
use it. The first 30 minutes build the system; the persuasion work in operation comes
afterwards. That is exactly why it is built so that usage is **easier** than the previous
way — otherwise no rollout works, no matter how good the software is.

---

## Decision points — what the agent must consciously decide

The platform cannot take away from the agent what is a **business decision**.
Everything else it works out itself (`onto_type_show` delivers `schema.properties` +
`schema.action_keys`). These four points it must decide actively — and record the decision:

**1. Set `target_scope` or leave it out.**
Set it when creator and editor of the finished answer are different people
(field staff writes, back office evaluates). Leave it out when in a small business everyone
may edit everything. Both are valid — the mistake is forgetting it **by accident**:
without `target_scope` the answer stays in the write scope and the back office never sees it.
Details: `references/best_practices/scope-organization-per-company.md`, section 8.

**2. Number of `arbeit` scopes.**
The formula is **1× `stammdaten` + 1× `archiv` + N× `arbeit`** — one `arbeit` scope per team
that has to keep its drafts separate. Write granularity = scope granularity; there is
no second axis. With one team it stays at two to three scopes.

**3. Marketplace: make the scope public or keep it private.**
`ontouser_scope_set_visibility` with `read_allowed_for=["PUBLIC"]` means **not only**
visibility, but that external use automatically credits credits
(`earnings_total` in the balance). That is a business decision about your own
data stock — not a checkbox that you tick on the side while setting up.

**4. Billing model.**
`pay_per_use` (every action is booked) or `flat` (no deduction, no scope limit).
The choice decides whether the customer gets to see the cost calculation below at all.

**Why this is more important than it sounds:** The setup itself takes minutes, and the agent
usually gets these four points right. But after the setup nobody knows anymore *why*
it was decided that way. Exactly these four questions come from the customer three months later — and then
nobody is there anymore who can answer them.

---

## Handover note — what the human receives in writing

The setup is only finished when the human can explain it **without the agent**. This
note is the result, not a nice extra — without it nobody understands the structure
when the agent is no longer in context.

**Content (keep it short, seven lines are enough):**

1. **What was built** — in the language of the business, not of the platform. Not "three scopes
   with `target_scope` commit", but "field staff write their visits, the office sees
   them finished and can no longer change them".
2. **Who may do what** — which group of people reads/writes in which scope. Take the permission matrix
   from `scope-organization-per-company.md` as a template and cut it down to the company.
3. **Why these decisions** — the four points from above, one sentence each. That is the part
   that shortens the discussion later.
4. **First three steps for an employee** — home screen, redeem invite code,
   first visit. No manual, three lines.
5. **What the agent would do next** — openly named options (marketplace, further
   teams/`arbeit` scopes, rule for escalation), so that the human decides instead of guessing.

**The honest part that belongs in the note:** What was *not* set up and why.
A deliberately omitted `target_scope` is a good decision — but only if it is
documented. Otherwise it reads like a mistake later.

**Test standard for "successful":** The human can explain to a colleague in two minutes who
works where — without opening the platform.

---

## Order of steps to tick off

1. `register` → **agent:** `invite_code` (from the client) + `accept_terms` — account active immediately,
   credentials come in the response; **human:** the customer's e-mail, password
2. Ask the human for the activation code → `activate` *(only on the e-mail path; with the
   invite code this step is dropped)*
3. `login` → save the token (after that only `refresh_access_token`)
4. `ontouser_scope_create` × 2 (arbeit, archiv)
5. `onto_type_show` → check the available form
6. As a test `prepare_form_answer` + `submit_form_answer` → is it in the archive?
7. `create_invite_code` for the field staff (write=arbeit, read=archiv)
8. `create_service_order` → a real human gets a real job
9. `onto_credit_balance` → show the customer the costs
10. `onto_scope_save_structuredimage_categories` → define image motifs for the app
11. `onto_trigger_create` → critical finding escalates automatically
12. If needed: `ontouser_scope_set_visibility` → marketplace
13. Tell the human: put the page on the **home screen** (then they stay signed in
    and get push)
