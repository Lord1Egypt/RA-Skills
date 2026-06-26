# Confluence Storage Format Reference

Confluence uses an XHTML-based storage format for page content. This document covers the most common elements and macros.

## Basic Elements

### Headings

```html
<h1>Heading 1</h1>
<h2>Heading 2</h2>
<h3>Heading 3</h3>
<h4>Heading 4</h4>
<h5>Heading 5</h5>
<h6>Heading 6</h6>
```

### Paragraphs and Text

```html
<p>A simple paragraph.</p>
<p><strong>Bold text</strong></p>
<p><em>Italic text</em></p>
<p><u>Underlined text</u></p>
<p><s>Strikethrough text</s></p>
<p><sub>subscript</sub> and <sup>superscript</sup></p>
<p><code>inline code</code></p>
```

### Line Breaks

```html
<p>Line one<br />Line two</p>
```

### Horizontal Rule

```html
<hr />
```

## Lists

### Unordered List

```html
<ul>
  <li>Item 1</li>
  <li>Item 2
    <ul>
      <li>Nested item</li>
    </ul>
  </li>
</ul>
```

### Ordered List

```html
<ol>
  <li>First</li>
  <li>Second</li>
  <li>Third</li>
</ol>
```

### Task List

```html
<ac:task-list>
  <ac:task>
    <ac:task-id>1</ac:task-id>
    <ac:task-status>incomplete</ac:task-status>
    <ac:task-body>Task to complete</ac:task-body>
  </ac:task>
  <ac:task>
    <ac:task-id>2</ac:task-id>
    <ac:task-status>complete</ac:task-status>
    <ac:task-body>Completed task</ac:task-body>
  </ac:task>
</ac:task-list>
```

## Links

### External Link

```html
<a href="https://example.com">Link text</a>
<a href="https://example.com" target="_blank">Opens in new tab</a>
```

### Internal Page Link

```html
<ac:link>
  <ri:page ri:content-title="Page Title" />
</ac:link>

<!-- With link text -->
<ac:link>
  <ri:page ri:content-title="Page Title" />
  <ac:plain-text-link-body><![CDATA[Custom link text]]></ac:plain-text-link-body>
</ac:link>

<!-- Link to page in different space -->
<ac:link>
  <ri:page ri:content-title="Page Title" ri:space-key="SPACEKEY" />
</ac:link>
```

### Anchor Link

```html
<!-- Create anchor -->
<ac:structured-macro ac:name="anchor">
  <ac:parameter ac:name="">section-name</ac:parameter>
</ac:structured-macro>

<!-- Link to anchor on same page -->
<ac:link ac:anchor="section-name">
  <ac:plain-text-link-body><![CDATA[Jump to section]]></ac:plain-text-link-body>
</ac:link>
```

## Tables

### Basic Table

```html
<table>
  <tbody>
    <tr>
      <th>Header 1</th>
      <th>Header 2</th>
    </tr>
    <tr>
      <td>Cell 1</td>
      <td>Cell 2</td>
    </tr>
    <tr>
      <td>Cell 3</td>
      <td>Cell 4</td>
    </tr>
  </tbody>
</table>
```

### Table with Styling

```html
<table class="wrapped">
  <colgroup>
    <col style="width: 100px;" />
    <col style="width: 200px;" />
  </colgroup>
  <tbody>
    <tr>
      <th style="text-align: center;">Centered Header</th>
      <td style="background-color: #f0f0f0;">Shaded cell</td>
    </tr>
  </tbody>
</table>
```

## Images

### Attached Image

```html
<ac:image>
  <ri:attachment ri:filename="image.png" />
</ac:image>

<!-- With size -->
<ac:image ac:width="300">
  <ri:attachment ri:filename="image.png" />
</ac:image>

<!-- With alt text -->
<ac:image ac:alt="Description">
  <ri:attachment ri:filename="image.png" />
</ac:image>
```

### External Image

```html
<ac:image>
  <ri:url ri:value="https://example.com/image.png" />
</ac:image>
```

## Macros

Macros use `ac:structured-macro` with a name attribute.

### Code Block

```html
<ac:structured-macro ac:name="code">
  <ac:parameter ac:name="language">python</ac:parameter>
  <ac:parameter ac:name="title">Example Code</ac:parameter>
  <ac:parameter ac:name="linenumbers">true</ac:parameter>
  <ac:plain-text-body><![CDATA[
def hello():
    print("Hello, World!")
  ]]></ac:plain-text-body>
</ac:structured-macro>
```

Supported languages: `java`, `javascript`, `python`, `ruby`, `bash`, `sql`, `xml`, `json`, `yaml`, `html`, `css`, `cpp`, `csharp`, `go`, `rust`, etc.

### Panel Macros

```html
<!-- Info panel (blue) -->
<ac:structured-macro ac:name="info">
  <ac:parameter ac:name="title">Note</ac:parameter>
  <ac:rich-text-body>
    <p>Information message</p>
  </ac:rich-text-body>
</ac:structured-macro>

<!-- Note panel (yellow) -->
<ac:structured-macro ac:name="note">
  <ac:rich-text-body>
    <p>Warning message</p>
  </ac:rich-text-body>
</ac:structured-macro>

<!-- Warning panel (red) -->
<ac:structured-macro ac:name="warning">
  <ac:rich-text-body>
    <p>Critical warning</p>
  </ac:rich-text-body>
</ac:structured-macro>

<!-- Tip panel (green) -->
<ac:structured-macro ac:name="tip">
  <ac:rich-text-body>
    <p>Helpful tip</p>
  </ac:rich-text-body>
</ac:structured-macro>
```

### Expand (Collapsible Section)

```html
<ac:structured-macro ac:name="expand">
  <ac:parameter ac:name="title">Click to expand</ac:parameter>
  <ac:rich-text-body>
    <p>Hidden content here</p>
  </ac:rich-text-body>
</ac:structured-macro>
```

### Table of Contents

```html
<ac:structured-macro ac:name="toc">
  <ac:parameter ac:name="maxLevel">3</ac:parameter>
</ac:structured-macro>
```

### Status Macro (Lozenges)

```html
<ac:structured-macro ac:name="status">
  <ac:parameter ac:name="title">IN PROGRESS</ac:parameter>
  <ac:parameter ac:name="colour">Yellow</ac:parameter>
</ac:structured-macro>

<ac:structured-macro ac:name="status">
  <ac:parameter ac:name="title">DONE</ac:parameter>
  <ac:parameter ac:name="colour">Green</ac:parameter>
</ac:structured-macro>

<ac:structured-macro ac:name="status">
  <ac:parameter ac:name="title">BLOCKED</ac:parameter>
  <ac:parameter ac:name="colour">Red</ac:parameter>
</ac:structured-macro>
```

Colors: `Grey`, `Red`, `Yellow`, `Green`, `Blue`

### Excerpt

```html
<ac:structured-macro ac:name="excerpt">
  <ac:parameter ac:name="hidden">false</ac:parameter>
  <ac:rich-text-body>
    <p>This text will be used as the page excerpt.</p>
  </ac:rich-text-body>
</ac:structured-macro>
```

### Include Page

```html
<ac:structured-macro ac:name="include">
  <ac:parameter ac:name=""><ri:page ri:content-title="Page to Include" /></ac:parameter>
</ac:structured-macro>
```

### Children Display

```html
<ac:structured-macro ac:name="children">
  <ac:parameter ac:name="depth">2</ac:parameter>
  <ac:parameter ac:name="sort">title</ac:parameter>
</ac:structured-macro>
```

## User Mentions

```html
<ac:link>
  <ri:user ri:account-id="5a1234567890abcdef012345" />
</ac:link>
```

## Emoticons

```html
<ac:emoticon ac:name="smile" />
<ac:emoticon ac:name="sad" />
<ac:emoticon ac:name="cheeky" />
<ac:emoticon ac:name="laugh" />
<ac:emoticon ac:name="wink" />
<ac:emoticon ac:name="thumbs-up" />
<ac:emoticon ac:name="thumbs-down" />
<ac:emoticon ac:name="information" />
<ac:emoticon ac:name="tick" />
<ac:emoticon ac:name="cross" />
<ac:emoticon ac:name="warning" />
```

## Complete Page Example

```html
<h1>Project Overview</h1>

<ac:structured-macro ac:name="toc">
  <ac:parameter ac:name="maxLevel">2</ac:parameter>
</ac:structured-macro>

<h2>Introduction</h2>
<p>This document describes the project goals and timeline.</p>

<ac:structured-macro ac:name="info">
  <ac:parameter ac:name="title">Status</ac:parameter>
  <ac:rich-text-body>
    <p>Current status: <ac:structured-macro ac:name="status">
      <ac:parameter ac:name="title">IN PROGRESS</ac:parameter>
      <ac:parameter ac:name="colour">Yellow</ac:parameter>
    </ac:structured-macro></p>
  </ac:rich-text-body>
</ac:structured-macro>

<h2>Requirements</h2>
<ul>
  <li>Requirement 1</li>
  <li>Requirement 2</li>
</ul>

<h2>Technical Details</h2>
<ac:structured-macro ac:name="code">
  <ac:parameter ac:name="language">json</ac:parameter>
  <ac:plain-text-body><![CDATA[{
  "name": "project",
  "version": "1.0.0"
}]]></ac:plain-text-body>
</ac:structured-macro>

<h2>Related Pages</h2>
<ac:structured-macro ac:name="children">
  <ac:parameter ac:name="depth">1</ac:parameter>
</ac:structured-macro>
```

## Tips

1. **Always escape special characters** in CDATA sections
2. **Use `<br />` for line breaks** within paragraphs
3. **Tables must have `<tbody>`** wrapper
4. **Test complex formatting** with simple pages first
5. **Check macro names** are correctly spelled (case-sensitive)
