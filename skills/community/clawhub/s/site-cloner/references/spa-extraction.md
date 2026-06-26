# SPA Bundle Extraction Guide

## Identifying a SPA

The HTML body contains only `<div id="root"></div>` (React) or `<div id="app"></div>` (Vue). All content is rendered by JavaScript.

## Step 1: Find the bundle URL

Look in the HTML `<head>` for:
```html
<script type="module" crossorigin src="/assets/index-XXXXXXXX.js"></script>
<link rel="stylesheet" crossorigin href="/assets/index-XXXXXXXX.css">
```

Both files are needed.

## Step 2: Download both files

```powershell
$js = (Invoke-WebRequest -Uri "<BASE>/assets/index-XXXX.js" -UseBasicParsing).Content
$css = (Invoke-WebRequest -Uri "<BASE>/assets/index-XXXX.css" -UseBasicParsing).Content
$js | Out-File "bundle.js" -Encoding UTF8
$css | Out-File "bundle.css" -Encoding UTF8
```

## Step 3: Extract UI copy

```powershell
$js = Get-Content "bundle.js" -Raw
[regex]::Matches($js, '"([A-Z][^"]{10,400})"') | ForEach-Object { $_.Groups[1].Value } | Where-Object {
    $_ -match '\s[a-z]{3,}\s' -and
    $_ -notmatch 'function|typeof|return|Error|React|window|document|undefined|null|className|aria|data-|xmlns|\\u'
} | Select-Object -Unique
```

## Step 4: Extract image paths

```powershell
[regex]::Matches($js, '"(/[^"]+\.(jpg|jpeg|png|webp|svg|avif))"') | ForEach-Object { $_.Groups[1].Value } | Select-Object -Unique
```

## Step 5: Extract theme colors from CSS

```powershell
$css = Get-Content "bundle.css" -Raw
[regex]::Matches($css, '--[a-z-]+:\s*[^;{}]+') | ForEach-Object { $_.Value.Trim() } | Where-Object {
    $_ -match '(background|foreground|primary|secondary|muted|accent|card|border|font-serif|font-sans)' -and $_ -notmatch 'tw-'
} | Select-Object -Unique
```

## Step 6: Extract Google Fonts

Look in CSS for `@import` URL containing `fonts.googleapis.com`:
```powershell
[regex]::Matches($css, 'family=[^&"]+') | ForEach-Object { $_.Value } | Select-Object -Unique
```

## Step 7: Find nav links

```powershell
$idx = $js.IndexOf('href:"#')
if ($idx -ge 0) { $js.Substring([Math]::Max(0,$idx - 300), 800) }
```

## Step 8: Find section content by anchor

```powershell
# Search for known section IDs to get surrounding JSX
foreach ($anchor in @("hero","about","services","gallery","contact","process","archive")) {
    $idx = $js.IndexOf("id:`"$anchor`"")
    if ($idx -lt 0) { $idx = $js.IndexOf("id:""$anchor""") }
    if ($idx -ge 0) { Write-Output "=== $anchor ==="; $js.Substring($idx, 1500) }
}
```

## Tips

- Search for known text strings (like the brand name or hero headline) to find surrounding structure
- Use `$js.IndexOf("known phrase")` + `$js.Substring($idx, 1500)` to inspect any section
- The minified JSX reveals className, children, and structure — enough to rebuild pixel-perfect
- If a string contains `\u00e2\u20ac\u201d` or similar — those are UTF-8 encoding artifacts for em-dashes etc.
