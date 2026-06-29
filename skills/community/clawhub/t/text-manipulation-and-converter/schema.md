# Text Manipulation and Converter Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `text-manipulation-and-converter`

x402 availability: not enabled for this product.

## `add-quotes`

Action slug: `add-quotes`

Price: `5` credits

Wrap each line in quotes of the specified type.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `quote_type` | `string` | no | Type of quote: 'single', 'double' (default), or 'backtick'. |
| `text` | `string` | yes | The input text to process. |

Sample parameters:

```json
{
  "quote_type": "double",
  "text": "example text"
}
```

Generated JSON parameter schema:

```json
{
  "quote_type": {
    "default": "double",
    "description": "Type of quote: 'single', 'double' (default), or 'backtick'.",
    "enum": [
      "single",
      "double",
      "backtick"
    ],
    "required": false,
    "type": "string"
  },
  "text": {
    "description": "The input text to process.",
    "required": true,
    "type": "string"
  }
}
```

## `alternate-case`

Action slug: `alternate-case`

Price: `5` credits

Alternate between uppercase and lowercase for each character position.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `text` | `string` | yes | The input text to process. |

Sample parameters:

```json
{
  "text": "example text"
}
```

Generated JSON parameter schema:

```json
{
  "text": {
    "description": "The input text to process.",
    "required": true,
    "type": "string"
  }
}
```

## `change-case`

Action slug: `change-case`

Price: `5` credits

Convert text to a target case format. Supports 11 case types: camel (camelCase), snake (snake_case), pascal (PascalCase), kebab (kebab-case), screaming-snake (SCREAMING_SNAKE_CASE), upper (UPPERCASE), lower (lowercase), title (Title Case), sentence (Sentence case), dot (dot.case), path (path/case).

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `case_type` | `string` | yes | Target case type for conversion. |
| `text` | `string` | yes | The input text to process. |

Sample parameters:

```json
{
  "case_type": "camel",
  "text": "example text"
}
```

Generated JSON parameter schema:

```json
{
  "case_type": {
    "description": "Target case type for conversion.",
    "enum": [
      "camel",
      "snake",
      "pascal",
      "kebab",
      "screaming-snake",
      "upper",
      "lower",
      "title",
      "sentence",
      "dot",
      "path"
    ],
    "required": true,
    "type": "string"
  },
  "text": {
    "description": "The input text to process.",
    "required": true,
    "type": "string"
  }
}
```

## `count-characters`

Action slug: `count-characters`

Price: `5` credits

Return detailed character statistics: total characters, characters without spaces, letters, digits, spaces, and line count.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `text` | `string` | yes | The input text to analyze. |

Sample parameters:

```json
{
  "text": "example text"
}
```

Generated JSON parameter schema:

```json
{
  "text": {
    "description": "The input text to analyze.",
    "required": true,
    "type": "string"
  }
}
```

## `count-lines`

Action slug: `count-lines`

Price: `5` credits

Count the number of lines in the text.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `text` | `string` | yes | The input text to count. |

Sample parameters:

```json
{
  "text": "example text"
}
```

Generated JSON parameter schema:

```json
{
  "text": {
    "description": "The input text to count.",
    "required": true,
    "type": "string"
  }
}
```

## `count-words`

Action slug: `count-words`

Price: `5` credits

Count the number of words in the text.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `text` | `string` | yes | The input text to count. |

Sample parameters:

```json
{
  "text": "example text"
}
```

Generated JSON parameter schema:

```json
{
  "text": {
    "description": "The input text to count.",
    "required": true,
    "type": "string"
  }
}
```

## `dedent-text`

Action slug: `dedent-text`

Price: `5` credits

Remove common leading whitespace from all lines.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `text` | `string` | yes | The input text to process. |

Sample parameters:

```json
{
  "text": "example text"
}
```

Generated JSON parameter schema:

```json
{
  "text": {
    "description": "The input text to process.",
    "required": true,
    "type": "string"
  }
}
```

## `indent-text`

Action slug: `indent-text`

Price: `5` credits

Add consistent indentation to every line of text.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `indent_char` | `string` | no | Character for indentation: 'space' (default) or 'tab'. |
| `indent_count` | `integer` | no | Number of indent characters per level (1-16, default: 4). |
| `text` | `string` | yes | The input text to process. |

Sample parameters:

```json
{
  "indent_char": "space",
  "indent_count": 4,
  "text": "example text"
}
```

Generated JSON parameter schema:

```json
{
  "indent_char": {
    "default": "space",
    "description": "Character for indentation: 'space' (default) or 'tab'.",
    "enum": [
      "space",
      "tab"
    ],
    "required": false,
    "type": "string"
  },
  "indent_count": {
    "default": 4,
    "description": "Number of indent characters per level (1-16, default: 4).",
    "maximum": 16,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "text": {
    "description": "The input text to process.",
    "required": true,
    "type": "string"
  }
}
```

## `normalize-whitespace`

Action slug: `normalize-whitespace`

Price: `5` credits

Comprehensive cleanup: trim each line, remove empty lines, collapse multiple spaces.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `text` | `string` | yes | The input text to process. |

Sample parameters:

```json
{
  "text": "example text"
}
```

Generated JSON parameter schema:

```json
{
  "text": {
    "description": "The input text to process.",
    "required": true,
    "type": "string"
  }
}
```

## `remove-accents`

Action slug: `remove-accents`

Price: `5` credits

Strip accents and diacritical marks from characters.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `text` | `string` | yes | The input text to process. |

Sample parameters:

```json
{
  "text": "example text"
}
```

Generated JSON parameter schema:

```json
{
  "text": {
    "description": "The input text to process.",
    "required": true,
    "type": "string"
  }
}
```

## `remove-duplicate-lines`

Action slug: `remove-duplicate-lines`

Price: `5` credits

Remove duplicate lines while preserving the order of first occurrences.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `text` | `string` | yes | The input text to process. |

Sample parameters:

```json
{
  "text": "example text"
}
```

Generated JSON parameter schema:

```json
{
  "text": {
    "description": "The input text to process.",
    "required": true,
    "type": "string"
  }
}
```

## `remove-empty-lines`

Action slug: `remove-empty-lines`

Price: `5` credits

Remove all blank/empty lines from the text.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `text` | `string` | yes | The input text to process. |

Sample parameters:

```json
{
  "text": "example text"
}
```

Generated JSON parameter schema:

```json
{
  "text": {
    "description": "The input text to process.",
    "required": true,
    "type": "string"
  }
}
```

## `remove-extra-spaces`

Action slug: `remove-extra-spaces`

Price: `5` credits

Collapse multiple consecutive spaces into a single space.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `text` | `string` | yes | The input text to process. |

Sample parameters:

```json
{
  "text": "example text"
}
```

Generated JSON parameter schema:

```json
{
  "text": {
    "description": "The input text to process.",
    "required": true,
    "type": "string"
  }
}
```

## `remove-line-breaks`

Action slug: `remove-line-breaks`

Price: `5` credits

Convert multi-line text to a single line by replacing line breaks with spaces.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `text` | `string` | yes | The input text to process. |

Sample parameters:

```json
{
  "text": "example text"
}
```

Generated JSON parameter schema:

```json
{
  "text": {
    "description": "The input text to process.",
    "required": true,
    "type": "string"
  }
}
```

## `reverse-lines`

Action slug: `reverse-lines`

Price: `5` credits

Reverse the order of lines (last line becomes first).

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `text` | `string` | yes | The input text to process. |

Sample parameters:

```json
{
  "text": "example text"
}
```

Generated JSON parameter schema:

```json
{
  "text": {
    "description": "The input text to process.",
    "required": true,
    "type": "string"
  }
}
```

## `reverse-text`

Action slug: `reverse-text`

Price: `5` credits

Reverse the entire text character by character.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `text` | `string` | yes | The input text to process. |

Sample parameters:

```json
{
  "text": "example text"
}
```

Generated JSON parameter schema:

```json
{
  "text": {
    "description": "The input text to process.",
    "required": true,
    "type": "string"
  }
}
```

## `smart-case-detect`

Action slug: `smart-case-detect`

Price: `5` credits

Detect the case style of input text. Returns: upper, lower, title, snake, kebab, dot, path, camel, pascal, mixed, or empty.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `text` | `string` | yes | The input text to analyze. |

Sample parameters:

```json
{
  "text": "example text"
}
```

Generated JSON parameter schema:

```json
{
  "text": {
    "description": "The input text to analyze.",
    "required": true,
    "type": "string"
  }
}
```

## `sort-lines`

Action slug: `sort-lines`

Price: `5` credits

Sort lines alphabetically in ascending or descending order.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `order` | `string` | no | Sort order: 'asc' for ascending (default), 'desc' for descending. |
| `text` | `string` | yes | The input text to process. |

Sample parameters:

```json
{
  "order": "asc",
  "text": "example text"
}
```

Generated JSON parameter schema:

```json
{
  "order": {
    "default": "asc",
    "description": "Sort order: 'asc' for ascending (default), 'desc' for descending.",
    "enum": [
      "asc",
      "desc"
    ],
    "required": false,
    "type": "string"
  },
  "text": {
    "description": "The input text to process.",
    "required": true,
    "type": "string"
  }
}
```

## `spaces-to-tabs`

Action slug: `spaces-to-tabs`

Price: `5` credits

Convert leading spaces to tab characters.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `tab_width` | `integer` | no | Number of spaces per tab (1-16, default: 4). |
| `text` | `string` | yes | The input text to process. |

Sample parameters:

```json
{
  "tab_width": 4,
  "text": "example text"
}
```

Generated JSON parameter schema:

```json
{
  "tab_width": {
    "default": 4,
    "description": "Number of spaces per tab (1-16, default: 4).",
    "maximum": 16,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "text": {
    "description": "The input text to process.",
    "required": true,
    "type": "string"
  }
}
```

## `tabs-to-spaces`

Action slug: `tabs-to-spaces`

Price: `5` credits

Convert tab characters to spaces with configurable tab width.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `tab_width` | `integer` | no | Number of spaces per tab (1-16, default: 4). |
| `text` | `string` | yes | The input text to process. |

Sample parameters:

```json
{
  "tab_width": 4,
  "text": "example text"
}
```

Generated JSON parameter schema:

```json
{
  "tab_width": {
    "default": 4,
    "description": "Number of spaces per tab (1-16, default: 4).",
    "maximum": 16,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "text": {
    "description": "The input text to process.",
    "required": true,
    "type": "string"
  }
}
```

## `trim-whitespace`

Action slug: `trim-whitespace`

Price: `5` credits

Remove leading and trailing whitespace from each line and the overall text.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `text` | `string` | yes | The input text to process. |

Sample parameters:

```json
{
  "text": "example text"
}
```

Generated JSON parameter schema:

```json
{
  "text": {
    "description": "The input text to process.",
    "required": true,
    "type": "string"
  }
}
```

## `unwrap-text`

Action slug: `unwrap-text`

Price: `5` credits

Join all lines into a single line, removing line breaks.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `text` | `string` | yes | The input text to process. |

Sample parameters:

```json
{
  "text": "example text"
}
```

Generated JSON parameter schema:

```json
{
  "text": {
    "description": "The input text to process.",
    "required": true,
    "type": "string"
  }
}
```

## `wrap-text`

Action slug: `wrap-text`

Price: `5` credits

Wrap text to fit within a specified column width.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `text` | `string` | yes | The input text to process. |
| `width` | `integer` | no | Maximum line width (10-200, default: 80). |

Sample parameters:

```json
{
  "text": "example text",
  "width": 80
}
```

Generated JSON parameter schema:

```json
{
  "text": {
    "description": "The input text to process.",
    "required": true,
    "type": "string"
  },
  "width": {
    "default": 80,
    "description": "Maximum line width (10-200, default: 80).",
    "maximum": 200,
    "minimum": 10,
    "required": false,
    "type": "integer"
  }
}
```
