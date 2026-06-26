---
name: opentable-booking
description: "Book restaurant tables on OpenTable via the browser tool. Handles hidden time slots and terms checkboxes with JS evaluate fallbacks. Works with a logged-in session and card on file — no manual card entry needed."
version: 1.0.0
metadata:
  openclaw:
    emoji: "🍽️"
    requires:
      config:
        - browser.enabled
---

# OpenTable Booking (Browser Tool)

Use the **OpenClaw browser tool** to book restaurants via OpenTable.

> **Why this skill exists:** OpenTable's widget hides critical UI elements
> (time-slot links, terms checkboxes) from the accessibility/aria tree.
> This skill encodes the JS evaluation patterns that reliably find them.
> See [browser-snippets.md](browser-snippets.md) for the full snippet reference.

## When to Use

- Any request to book or reserve a restaurant table on OpenTable.
- Works globally — opentable.com, opentable.co.uk, opentable.de, and all other OpenTable domains.

Do **not** use for SevenRooms, Resy, Tock, TheFork, or other booking platforms.

## Prerequisites

1. OpenClaw browser is running with `profile="openclaw"` (headed, not headless — Cloudflare blocks headless on OpenTable).
2. User is already logged into OpenTable (session cookie present).
3. A payment card is on file in the OpenTable account (auto-loaded at checkout).

**First-time setup:** If not yet logged in, navigate to the OpenTable sign-in page manually, authenticate via email + verification code, and ensure a card is saved. This only needs to be done once — the session persists.

## Core Loop (MANDATORY)

1. **browser.navigate** to target URL.
2. **browser.snapshot (interactive)**.
3. **Decide action using refs** from snapshot.
4. **browser.act** (click/fill).
5. **Re-snapshot** after every significant action.

Never guess selectors. Never reuse old refs after navigation.

## Booking Flow

### 1) Parse request

Extract from the user's message:
- Restaurant name (required).
- Date (required).
- Time (default: 20:30).
- Party size (default: 2).
- Location (default: London).
- OpenTable domain (default: opentable.co.uk — use opentable.com for US, opentable.de for Germany, etc.).
- Seating preference (default: standard).
- Special request (default: none).

### 2) Navigate to restaurant page

Use slug URL:

```
https://www.{domain}/r/{restaurant-slug}-{location}?covers={partySize}&dateTime={YYYY-MM-DD}T{HH:MM}
```

If you don't know the slug, use search:

```
https://www.{domain}/s?covers={party_size}&dateTime={date}T{time}&term={restaurant}+{location}
```

Where `{domain}` is the appropriate OpenTable domain (e.g. `opentable.co.uk`, `opentable.com`).

### 3) Dismiss cookie banner

If a cookie banner appears, click the Accept/Close button by ref. Re-snapshot.

```
browser.act(click ref for "Accept" / "Accept All" / close button)
browser.snapshot(interactive=true)
```

### 4) Confirm/Set date, time, party size

Check the widget bar at the top of the restaurant page. If the pre-filled values don't match the request, click the relevant widget and update:

- **Date picker:** click the date field ref → navigate to correct month → click day.
- **Time picker:** click time dropdown ref → select correct time.
- **Covers:** click covers dropdown ref → select number.

Re-snapshot after each change. Then click "Find a Table" / "Search" if needed.

### 5) Select time slot (⚠️ JS required)

The time-slot buttons are NOT reliably in the aria tree. Run this JS evaluation to find them:

```javascript
(() => {
  const links = [...document.querySelectorAll('a')];
  const timeSlots = links.filter(a => {
    const text = a.textContent.trim();
    return /^\d{1,2}:\d{2}$/.test(text) && a.offsetParent !== null;
  });
  return timeSlots.map(a => ({
    time: a.textContent.trim(),
    id: a.id || '',
    href: a.href || '',
    rect: a.getBoundingClientRect().toJSON()
  }));
})()
```

This returns visible `<a>` elements whose text matches HH:MM.

To click the desired slot:

```javascript
(() => {
  const links = [...document.querySelectorAll('a')];
  const target = links.find(a =>
    a.textContent.trim() === '{TARGET_TIME}' && a.offsetParent !== null
  );
  if (target) { target.click(); return 'clicked ' + target.textContent.trim(); }
  return 'not found';
})()
```

Replace `{TARGET_TIME}` with the exact HH:MM string (e.g. `"20:30"`).

If the exact time isn't available, pick the nearest available slot. Re-snapshot after clicking.

### 6) Choose booking type

If options like **Standard reservation** vs tasting menus appear, select **Standard** unless user specified otherwise. Click its Select button by ref. Re-snapshot.

### 7) Verify pre-filled details

Because we're logged in, OpenTable should pre-fill:
- First name, Last name, Email, Phone number.
- Card on file (e.g. "Visa ending 0184").

Verify these are present in the snapshot. If guest details are empty, fill them in step 8. If **no card on file** is shown, **stop and inform the user** — they need to add a card to their OpenTable account before this skill can complete a booking.

### 8) Manually fill guest details ONLY if they aren't pre-filled

Use `browser.act` fill on the fields (from refs):
- First name, Last name, Email, Phone.

Re-snapshot.

### 9) Accept terms checkbox (⚠️ JS required)

The terms checkbox is often NOT in the aria tree. Find and check it via JS:

```javascript
(() => {
  const checkboxes = [...document.querySelectorAll('input[type="checkbox"]')];
  const terms = checkboxes.find(cb => {
    const label = cb.closest('label') || document.querySelector('label[for="' + cb.id + '"]');
    return label && /terms|conditions|policy|agree/i.test(label.textContent);
  });
  if (terms && !terms.checked) {
    terms.click();
    return 'checked terms';
  }
  if (terms && terms.checked) return 'already checked';
  return 'not found';
})()
```

Re-snapshot to verify it's checked.

### 10) Complete booking

Find and click the "Complete reservation" / "Confirm" button by ref.

```
browser.act(click ref={confirm_button_ref})
```

Re-snapshot.

### 11) Handle 3DS

If a 3DS authentication iframe or redirect appears:
- **Screenshot** the page so the user can see the challenge.
- **Inform the user** they need to approve the 3DS challenge on their device / banking app.
- Wait for user confirmation, then re-snapshot to check for the confirmation page.

### 12) Report result

Return confirmation number and summary:
- Restaurant, date, time, party size.
- Confirmation code (if shown).
- "Card ending 1234" (never expose full card).

## Error Handling

- If element not found: wait 2–3s, snapshot again (max 3 retries).
- If redirected to login: stop and ask user.
- If no card on file: stop and ask user to add a card to their OpenTable account.
- If timeslots not visible: adjust date/time and retry.

## Tooling Constraints

- Always use browser tool (navigate/snapshot/act/screenshot).
- One action per step; re-snapshot after each.
- No CSS/XPath selectors; use refs from snapshot.

## External Endpoints

- `opentable.co.uk` / `opentable.com` / other regional OpenTable domains (booking flow only).

## Security & Privacy

- This skill navigates only to OpenTable domains.
- Card details are never read, logged, or transmitted — they are pre-filled by OpenTable from the user's saved account.
- No environment variables or API keys are required.
- This skill does not handle or source payment credentials. Payment relies entirely on the card already saved in the user's OpenTable account.

## Trust Statement

By using this skill, your browser navigates to OpenTable and interacts with the page on your behalf. No data is sent to any third party. All booking actions happen within your existing authenticated OpenTable session.
