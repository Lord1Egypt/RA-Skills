# Table and List Rendering

## :::table

Body is a Markdown table. Convert to HTML. If `caption` param is provided, emit `<caption>[caption text]</caption>` as the first child of `<table>`.

    <div data-component="table" class="table-wrapper fade-in-up">
      <table class="report-table">
        <caption>Table title if provided</caption>
        <thead><tr><th>Col1</th>...</tr></thead>
        <tbody><tr><td>Val</td>...</tr></tbody>
      </table>
    </div>

## :::list

Body is a Markdown list (ordered `1. Item` or unordered `- Item`). `style=ordered` → `<ol>`, default → `<ul>`.

**Single-line format (compatibility only):** `:::list style=ordered 1. A 2. B :::` — split on `N. ` or `- ` separators to recover individual items; render the same HTML below. Do not generate this as the primary syntax.

    <div data-component="list" class="report-list">
      <ul class="styled-list">  <!-- or <ol> if style=ordered -->
        <li>Item</li>
        <li>Item with sub-items
          <ul><li>Sub-item</li></ul>
        </li>
      </ul>
    </div>

If an item has indented sub-items (2-space or 4-space indent), render them as nested `<ul>` or `<ol>` inside the parent `<li>`.

**Do NOT output `:::list`, params, or `:::` closing marker as text — they are never user-visible content.**
