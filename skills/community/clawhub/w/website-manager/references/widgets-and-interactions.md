# Widgets and Interactions

Use this file when the website needs lightweight but intentional interaction design.

## Widgets

Common additions:
- booking CTA bars
- opening-hours widgets
- maps
- testimonial rails
- newsletter signup modules
- category chips
- related-content cards

Rules:
- every widget should support a real user task
- define a fallback or empty state
- keep mobile behavior explicit

## Filtering

Listing pages should account for:
- category filters
- tag filters
- combined filter states when appropriate
- URL-deep-linking when useful
- clear reset behavior
- empty-state messaging

Good default behavior:
- filter state should be visible
- selected values should be obvious
- if no result matches, explain why and offer reset

## Search

For small collections:
- client-side search is usually enough

For larger collections:
- use a server-side or precomputed index only when needed

Always provide:
- no-results state
- debounced input or sensible submit behavior
- consistent matching across titles, excerpts, tags, and categories

## Pagination and load more

Choose based on content shape:
- pagination for archive-heavy blogs
- load more for shorter marketing collections

Always account for:
- state persistence after filtering
- accessible controls
- mobile usability

## Blog and CMS listings

When using Notion-backed content, design the listing so it can support:
- featured posts
- latest posts
- category pages
- tag filters
- search
- pagination
- graceful loading states
