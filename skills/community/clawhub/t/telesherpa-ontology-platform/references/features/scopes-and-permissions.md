# Scopes: how access is organised

> Reference for agents building a workspace. It describes what you configure and
> what you can observe — not how the platform is implemented.

## 1. The model

A **scope** groups data *and* the people who may work with it. There is no second
permission system: what an account may see or change is decided by its grant on a
scope.

Practical consequence: if a person must not see something, put the data in a
different scope. Hiding it in a view is convenience, not a boundary.

## 2. Three levels per grant

| Level | What it allows |
|---|---|
| read | see objects of the scope in lists, views and details |
| write | create and change objects in the scope |
| manage | administer the scope: grants for other people, its interfaces, action definitions, start cards |

The levels are independent: `manage` does not imply `write`, and not `read`.
Grant what the person actually needs.

## 3. Empty means empty

An account without a grant does not "see everything by default", and it inherits
nothing from another scope. A list without a grant is an empty list.

Two practical rules follow:

- Check the real account, not just your own. A manager who sees a page does not
  prove that a staff account sees it.
- After changing a grant, verify with the affected account: sign in (or call the
  API) as that account and confirm the expected result **and** the expected refusal.

## 4. A public area for new accounts

Every new account automatically gets read access to the public scope, so the first
screen is not empty. Treat it as read-only: do not build a customer's work area
there, and do not give it write access.

## 5. Where access is enforced

| Place | How you declare it |
|---|---|
| a view | `access.require` in the view configuration: `"write"`, `"manage"` or a scope id; missing means read is enough; an unknown value is denied |
| an action | the action carries the scope it runs in; the executing account needs write there |
| a form | `guards` in the form definition — `[{"type": "linked_to_user", "linktype": "concerns"}]` binds the submission to the person it concerns; without it the form behaves as before |
| your own endpoint | check the scope in the endpoint as well, even if the menu already hides the page |
| the sidebar | `required_role` and `require_scope_manage` — a menu entry can be hidden per account |

**A hidden menu entry is not a lock.** Both doors belong together: hide the entry
*and* check inside the page. A page that only disappears from the menu is still
reachable by URL.

### Forms and the person binding

An action can be guarded so that it only runs on the person's own row. A form had no such
guard: an account that could read a colleague could fill in a form **for** them — an
absence in someone else's name.

```json
"guards": [{"type": "linked_to_user", "linktype": "concerns"}]
```

The submission is checked against the object the answer concerns — for an absence, the
person. If that object is the signed-in person's own person, the binding holds. Anything
else is refused before the first write, and a refusal is logged with account and address.
No exception for administrators. Without `guards` a form behaves as before, so existing
forms are untouched.

## 6. A layout that works for shift planning

Three scopes per customer, one tree:

| Scope | Content | Staff | Managers |
|---|---|---|---|
| master data | people, stations, qualifications, contract data | no access | read + write |
| planning | shifts, absences, demands, periods | **no access** — own objects only, through the person link | read + write |
| team | the staff's own doors: my shifts, swap requests, clock in/out | read, and write only where a door needs it | read |

Why staff get **no** grant on planning: a grant is per scope, not per row. Whoever
may read the planning scope reads every colleague's shifts, absences and
corrections — filtering in a view does not change that, because the list and the API
follow the grant.

The door for staff is **the person link**, not a grant: an object that hangs on the
person's own person (the shift they work, the absence they filed) is reachable for
them — the page opens, the actions on it run. Everything else in planning stays
locked, and a foreign object answers exactly like a nonexistent one.

Consequences for the design:

- Every staff door is an object **linked to the person**, and the action is guarded
  so that only that person's row can be changed
  (`references/features/scope-bridges.md`).
- Nothing that colleagues must not see goes into planning anyway — the person link
  opens a row, not a redacted view of it. Put payroll rates and free-text notes for
  managers in a scope of their own.
- A team view therefore lists what is reachable for that person; it does not "read
  planning" and hide the rest.

## 7. Hand-over checklist

1. For every scope, write down who reads, who writes, who manages.
2. Remove grants nobody needs — look at the staff accounts, not only the managers.
3. Set `access.require` on every view that shows personal data.
4. Give every own endpoint its own scope check.
5. Walk through the workspace once with a real staff account: menus, direct URLs,
   calls against a foreign scope.
6. Confirm the public scope is read-only for everybody.
