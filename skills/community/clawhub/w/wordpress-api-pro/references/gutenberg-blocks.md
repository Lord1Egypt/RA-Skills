# Gutenberg Block Format

WordPress Gutenberg uses HTML comments to define blocks.

## Basic Blocks

### Paragraph

```html
<!-- wp:paragraph -->
<p>This is a paragraph.</p>
<!-- /wp:paragraph -->
```

### Heading

```html
<!-- wp:heading -->
<h2 class="wp-block-heading">Heading Text</h2>
<!-- /wp:heading -->

<!-- wp:heading {"level":3} -->
<h3 class="wp-block-heading">H3 Heading</h3>
<!-- /wp:heading -->
```

### List

```html
<!-- wp:list -->
<ul>
<li>Item 1</li>
<li>Item 2</li>
</ul>
<!-- /wp:list -->
```

### Link/Button

```html
<!-- wp:paragraph -->
<p><a href="https://example.com">Link text</a></p>
<!-- /wp:paragraph -->
```

### Separator

```html
<!-- wp:separator -->
<hr class="wp-block-separator has-alpha-channel-opacity"/>
<!-- /wp:separator -->
```

### Table

```html
<!-- wp:table -->
<figure class="wp-block-table">
<table>
<thead><tr><th>Header 1</th><th>Header 2</th></tr></thead>
<tbody>
<tr><td>Cell 1</td><td>Cell 2</td></tr>
</tbody>
</table>
</figure>
<!-- /wp:heading -->
```

## Formatting

**Bold:** `<strong>text</strong>`  
**Italic:** `<em>text</em>`  
**Link:** `<a href="url">text</a>`

## Best Practices

- Always wrap content in appropriate blocks
- Use proper HTML encoding
- Test with WordPress block editor
- Validate block syntax
