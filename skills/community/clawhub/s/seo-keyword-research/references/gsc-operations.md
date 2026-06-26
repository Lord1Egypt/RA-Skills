# GSC web UI playbook (CDP automation)

> Use case: automate Google Search Console in the browser via a CDP proxy (default `localhost:3456`).

---

## 1. Correct GSC starting URL

**Do not** start from the GSC home and click through—open a fully parameterized URL so the date window and columns are correct immediately:

```
https://search.google.com/search-console/performance/search-analytics?resource_id=sc-domain%3A{domain}&num_of_days=28&metrics=CLICKS%2CIMPRESSIONS%2CCTR%2CPOSITION
```

Replace `{domain}` with the target domain, e.g. `example.com`:

```
https://search.google.com/search-console/performance/search-analytics?resource_id=sc-domain%3Aexample.com&num_of_days=28&metrics=CLICKS%2CIMPRESSIONS%2CCTR%2CPOSITION
```

**URL parameters**:

| Parameter | Value | Purpose |
|-----|---|-----|
| `resource_id` | `sc-domain%3A{domain}` | Selects the GSC property (`sc-domain:` for domain properties; URL-prefix properties use the full URL) |
| `num_of_days` | `28` | 28-day window (see warning below) |
| `metrics` | `CLICKS%2CIMPRESSIONS%2CCTR%2CPOSITION` | Enables Clicks + Impressions + CTR + Position (`%2C` = comma) |

> ⚠️ **Date window**: A default 3-month average suits mature, stable sites. If SEO work started recently (<3 months), a 3-month window mixes in a lot of pre-optimization low-rank noise and skews conclusions. Which window to use may also be specified per project in `AGENTS.md`.

---

## 2. Pre-extraction checks

After navigation, **verify before scraping** so you do not read stale cached DOM.

### 2.1 Verify headers (Position column on)

```javascript
(function(){
  var table = document.querySelectorAll("table")[1];
  var headers = table.querySelectorAll("thead th");
  var cols = [];
  for(var i=0; i<headers.length; i++) cols.push(headers[i].textContent.trim());
  return cols.join(" | ");
})()
```

Expected: `Top queries | Clicks | Impressions | CTR | Position`

If only four columns (no Position), the `metrics` param did not apply—manually click the “Average position” metric chip (see 2.3).

### 2.2 Verify the date window (28 days)

Screenshot the date picker at the top and confirm it shows “28 days” (or a 28-day range), not “3 months”.

```javascript
// Quick sanity check: does row 1 match expectations? (compare to a known prior export)
(function(){
  var table = document.querySelectorAll("table")[1];
  var row1 = table.querySelector("tbody tr");
  var cells = row1 ? row1.querySelectorAll("td") : [];
  var data = [];
  for(var i=0; i<cells.length; i++) data.push(cells[i].textContent.trim());
  return data.join(" | ");
})()
```

### 2.3 Manually enable Position (fallback if URL params fail)

```javascript
// Find the Average position metric chip and click (it should highlight, e.g. orange)
(function(){
  var cards = document.querySelectorAll("[data-metric], .nnLLaf, button");
  // Alternatively hit the metric strip via coordinates
  var el = document.elementFromPoint(1060, 250);
  el.click();
  return "clicked: " + el.textContent.trim().substring(0,50);
})()
```

---

## 3. Set rows-per-page to 500

Default is 10 rows; set **500** to pull the full query set in one page. This is a **two-step** flow:

### Step A: Open the rows-per-page control

```javascript
// Click the control that shows the current row count (e.g. "10") to open the menu
(function(){
  var el = document.elementFromPoint(1291, 855);
  el.click();
  return "clicked: " + el.textContent.trim();
})()
```

> Note: coordinates `1291, 855` fit a **1615×963** viewport—adjust for other sizes.  
> Or locate the control by text:

```javascript
(function(){
  var all = document.querySelectorAll("div");
  for(var i=0; i<all.length; i++){
    if(all[i].textContent.trim().startsWith("Rows per page")){
      var r = all[i].getBoundingClientRect();
      if(r.width > 0 && r.height > 0){
        all[i].click();
        return "clicked rows selector at x=" + Math.round(r.x) + " y=" + Math.round(r.y);
      }
    }
  }
  return "not found";
})()
```

### Step B: Click the “500” option in the open menu

```javascript
// Click the first visible element whose trimmed text is exactly "500"
(function(){
  var all = document.querySelectorAll("div, li, span");
  for(var i=0; i<all.length; i++){
    if(all[i].textContent.trim() === "500"){
      var r = all[i].getBoundingClientRect();
      if(r.width > 0 && r.height > 0){
        all[i].click();
        return "clicked 500 at x=" + Math.round(r.x) + " y=" + Math.round(r.y);
      }
    }
  }
  return "500 option not found";
})()
```

> ⚠️ Do **not** run Step B before Step A—when the menu is closed, the “500” node often has `width=0` and cannot be hit.

---

## 4. Extract all rows

After rows-per-page shows 500, scrape all body rows.

### 4.1 Which table is visible?

GSC often renders two `<table>` nodes: `table[0]` may be hidden/stale (e.g. x=0,y=0); `table[1]` is usually the live, visible grid.

```javascript
(function(){
  var tables = document.querySelectorAll("table");
  var info = [];
  for(var i=0; i<tables.length; i++){
    var r = tables[i].getBoundingClientRect();
    var rows = tables[i].querySelectorAll("tbody tr");
    info.push("table["+i+"]: x="+Math.round(r.x)+" y="+Math.round(r.y)+" rows="+rows.length);
  }
  return info.join("\n");
})()
```

Expect: `table[1]` on-screen (x>0, y>0), row count ≈ total queries for the property.

### 4.2 Scrape all rows

```javascript
(function(){
  var table = document.querySelectorAll("table")[1];
  var rows = table.querySelectorAll("tbody tr");
  var data = [];
  for(var i=0; i<rows.length; i++){
    var cells = rows[i].querySelectorAll("td");
    if(cells.length >= 5){
      data.push(
        cells[0].textContent.trim() + "\t" +   // keyword
        cells[1].textContent.trim() + "\t" +   // clicks
        cells[2].textContent.trim() + "\t" +   // impressions
        cells[4].textContent.trim()            // position (index 4, not 3—CTR is index 3)
      );
    }
  }
  return data.join("|||");
})()
```

> ⚠️ **Column order**: `keyword(0) | clicks(1) | impressions(2) | CTR(3) | position(4)`. Position is index **4**, not 3.

Parse the eval response in Python:

```python
import json, sys
resp = json.load(sys.stdin)
val = resp.get('value', '')
lines = val.split('|||')
print(f"Total: {len(lines)} rows")
for line in lines[:10]:
    print(line)
```

---

## 5. CDP conventions

### 5.1 Clicks by coordinates

The CDP proxy `/click` endpoint accepts **CSS selectors only**, not raw coordinates. For coordinate clicks, use `/eval`:

```bash
curl -s -X POST "http://localhost:3456/eval?target={tabId}" \
  -d 'document.elementFromPoint(X, Y).click()'
```

**Do not** do this (will error):

```bash
# Wrong: /click does not accept coordinates
curl -X POST "http://localhost:3456/click?target=..." -d '{"x": 100, "y": 200}'
```

### 5.2 Wrap complex JS in an IIFE

Avoid scope pollution and flaky top-level `var` in eval:

```javascript
// Good: IIFE wrapper
(function(){
  var result = [];
  // ... your code
  return result.join("\n");
})()

// Avoid: bare top-level var in eval can fail intermittently
var result = [];
```

### 5.3 Avoid arrow functions

Some GSC bundles handle arrow functions (`=>`) inconsistently—prefer `function` syntax.

### 5.4 After changing filters, wait for fresh data

After changing the date range or filters, **do not scrape immediately**—the DOM may still show old numbers. Screenshot or run a quick row check first:

```bash
curl -s "http://localhost:3456/screenshot?target={tabId}&file=/tmp/verify.png"
```

---

## 6. Pitfall quick reference

| Pitfall | Symptom | Fix |
|------|------|---------|
| Missing Position column | Only four columns (no rank) | Add `metrics=CLICKS%2CIMPRESSIONS%2CCTR%2CPOSITION` to the URL |
| Stale scrape | Numbers unchanged after filter change | Screenshot until UI reflects new range, then scrape |
| Wrong column scraped | You pulled CTR instead of position | Position is `cells[4]`, not `cells[3]` |
| “500” not found | `"500 option not found"` | Open the rows menu first, then click a visible “500” |
| `/click` errors | Coordinates sent to `/click` | Use `/eval` + `document.elementFromPoint` |
