# Portable Text Reference

Sanity's body content format. An array of block and inline objects.

## Standard Block (paragraph)
```json
{
  "_type": "block",
  "_key": "unique-key",
  "style": "normal",
  "markDefs": [],
  "children": [
    { "_type": "span", "_key": "span-key", "text": "Your text here", "marks": [] }
  ]
}
```

## Heading Styles
Same structure as above; change `style`:
- `"h1"`, `"h2"`, `"h3"`, `"h4"` — headings
- `"blockquote"` — pull quote

## Inline Marks
Add to span `marks` array:
- `"strong"` — bold
- `"em"` — italic
- `"code"` — inline code

## Links (annotation mark)
Define in `markDefs`, reference key in span `marks`:
```json
"markDefs": [
  { "_key": "lnk1", "_type": "link", "href": "https://example.com", "blank": true }
],
"children": [
  { "_type": "span", "_key": "s1", "text": "link text", "marks": ["lnk1"] }
]
```

## Inline Image
```json
{
  "_type": "image",
  "_key": "img1",
  "asset": { "_type": "reference", "_ref": "image-abc123-800x600-png" },
  "alt": "description",
  "caption": "optional caption"
}
```

## Code Block (custom type)
```json
{
  "_type": "code",
  "_key": "code1",
  "language": "javascript",
  "code": "console.log('hello')",
  "filename": "optional-filename.js"
}
```

## Key Rules
- Every block and span must have a unique `_key` within the document
- Use short, human-readable keys (e.g., `b01`, `b01s1`)
- `markDefs` is required even when empty (`[]`)
- Do not nest blocks — Portable Text is flat
