# Browser Booking — JS Snippet Reference

Reusable `browser.act(evaluate: ...)` patterns for elements that the aria
tree / snapshot doesn't expose. All snippets are designed for use with
OpenClaw's browser tool `evaluate` action.

## 1. Find Time Slots (Hidden Links)

OpenTable renders time-slot buttons as `<a>` elements that don't appear in the accessibility tree.

```javascript
(() => {
  const els = [...document.querySelectorAll('a, button, [role="button"]')];
  const slots = els.filter(el => {
    const text = el.textContent.trim();
    return /^\d{1,2}:\d{2}$/.test(text) && el.offsetParent !== null;
  });
  return slots.map(el => ({
    time: el.textContent.trim(),
    tag: el.tagName,
    id: el.id || '',
    href: el.href || '',
    rect: el.getBoundingClientRect().toJSON()
  }));
})()
```

**Click a specific slot:**

```javascript
(() => {
  const TARGET = '20:30';
  const els = [...document.querySelectorAll('a, button, [role="button"]')];
  const match = els.find(el =>
    el.textContent.trim() === TARGET && el.offsetParent !== null
  );
  if (match) { match.click(); return 'clicked ' + match.textContent.trim(); }
  return 'not found';
})()
```

## 2. Find and Check Terms Checkbox

OpenTable's terms checkbox is often not in the aria tree.

```javascript
(() => {
  const cbs = [...document.querySelectorAll('input[type="checkbox"]')];
  const terms = cbs.find(cb => {
    const label = cb.closest('label')
      || document.querySelector('label[for="' + cb.id + '"]');
    return label && /terms|conditions|policy|agree|accept/i.test(label.textContent);
  });
  if (terms && !terms.checked) {
    terms.click();
    return 'checked terms';
  }
  if (terms && terms.checked) return 'already checked';
  return 'terms checkbox not found';
})()
```

## 3. Enumerate All Checkboxes

When you need to see what checkboxes exist on the page:

```javascript
(() => {
  const cbs = [...document.querySelectorAll('input[type="checkbox"]')];
  return cbs.map(cb => {
    const label = cb.closest('label')
      || document.querySelector('label[for="' + cb.id + '"]');
    return {
      id: cb.id,
      name: cb.name || '',
      checked: cb.checked,
      visible: cb.offsetParent !== null,
      label: label ? label.textContent.trim().substring(0, 100) : 'no label',
      rect: cb.getBoundingClientRect().toJSON()
    };
  });
})()
```

## 4. Discover Form Fields

Map all interactive elements when the aria tree is incomplete:

```javascript
(() => {
  const els = [...document.querySelectorAll(
    'input, select, textarea, button, [role="button"], [role="listbox"], [role="combobox"]'
  )];
  return els.filter(el => el.offsetParent !== null).map(el => ({
    tag: el.tagName,
    type: el.type || '',
    name: el.name || '',
    id: el.id || '',
    placeholder: el.placeholder || '',
    ariaLabel: el.getAttribute('aria-label') || '',
    value: el.value || '',
    text: el.textContent?.trim().substring(0, 50) || '',
    rect: el.getBoundingClientRect().toJSON()
  }));
})()
```

## 5. Scroll to Element (When Below Fold)

```javascript
(() => {
  const TARGET_TEXT = 'Complete reservation';
  const els = [...document.querySelectorAll('button, a, input[type="submit"]')];
  const match = els.find(el =>
    el.textContent.trim().toLowerCase().includes(TARGET_TEXT.toLowerCase())
  );
  if (match) {
    match.scrollIntoView({ behavior: 'smooth', block: 'center' });
    return 'scrolled to: ' + match.textContent.trim();
  }
  return 'not found';
})()
```

## 6. Extract Confirmation Details

After booking completes, scrape the confirmation page:

```javascript
(() => {
  const text = document.body.innerText;
  const confMatch = text.match(/(?:confirmation|reference|booking)\s*(?:number|#|code|id|ref|reference)?[:\s]*(?:is\s+)?(?=[A-Z0-9-]{4,})([A-Z0-9-]*\d[A-Z0-9-]*)/i);
  const dateMatch = text.match(/(\d{1,2}\s+\w+\s+\d{4}|\w+\s+\d{1,2},?\s+\d{4})/);
  const timeMatch = text.match(/(\d{1,2}:\d{2}\s*(?:AM|PM)?)/i);
  const partySizeMatch = text.match(/(\d+)\s*(?:guest|people|diner|cover|seat)/i);
  const cardMatch = text.match(/(?:card|visa|mastercard|amex).*?(\d{4})\b/i);

  return {
    confirmation: confMatch ? confMatch[1] : null,
    date: dateMatch ? dateMatch[1] : null,
    time: timeMatch ? timeMatch[1] : null,
    partySize: partySizeMatch ? partySizeMatch[1] : null,
    cardLast4: cardMatch ? cardMatch[1] : null,
    pageTitle: document.title
  };
})()
```

## Usage Notes

- All snippets return serialisable data (no DOM nodes).
- All snippets check `offsetParent !== null` to skip hidden elements.
- Replace placeholder values (marked with comments) before use.
- Always re-snapshot after any snippet that calls `.click()`.
