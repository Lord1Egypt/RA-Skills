---
name: Render Probe A
description: Rendering fixture probe for markdown pipeline review. <img src=x onerror="window.__desc_xss=1"> plain text continues here.
---

# Render Probe A

This document is a deterministic rendering fixture used to observe how the catalog displays
markdown and embedded markup. It contains no automation, no network calls and no credentials.
Each numbered case below is a negative test that should either be neutralized or escaped.

## Case 01 raw image handler
<img src="x" onerror="window.__xss01=1" alt="case01">

## Case 02 raw script tag
<script>window.__xss02=1</script>

## Case 03 raw iframe
<iframe src="https://example.org/" title="case03"></iframe>

## Case 04 markdown javascript link
[case04](javascript:window.__xss04=1)

## Case 05 raw anchor with javascript href
<a href="javascript:window.__xss05=1">case05</a>

## Case 06 inline style attribute
<div style="background-image:url(https://example.org/case06.png)">case06</div>

## Case 07 style element with import
<style>@import url("https://example.org/case07.css");</style>

## Case 08 svg handler
<svg onload="window.__xss08=1"><circle cx="4" cy="4" r="4"></circle></svg>

## Case 09 entity encoded image
&lt;img src=x onerror="window.__xss09=1"&gt;

## Case 10 data uri image
<img src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIG9ubG9hZD0id2luZG93Ll9feHNzMTA9MSI+PC9zdmc+">

## Case 11 mermaid directive
```mermaid
%%{init: {"themeCSS": ".markdown{outline:3px solid red}"}}%%
graph TD
  A[one] --> B[two]
```

## Case 12 nested markup mutation
<math><mtext><table><mglyph><style><img src=x onerror="window.__xss12=1"></style></mglyph></table></mtext></math>

## Case 13 form
<form action="https://example.org/case13"><input name="q" value="x"><button type="submit">case13</button></form>

## Case 14 base element
<base href="https://example.org/">

## Case 15 markdown image with javascript target
![case15](javascript:window.__xss15=1)

## Case 16 html comment carrier
<!-- <img src=x onerror="window.__xss16=1"> -->

## Case 17 table and details passthrough
<table><thead><tr><th>k</th></tr></thead><tbody><tr><td>v</td></tr></tbody></table>
<details><summary>case17</summary>body</details>

## Notes
The fixture is intentionally inert outside a rendering sandbox.
