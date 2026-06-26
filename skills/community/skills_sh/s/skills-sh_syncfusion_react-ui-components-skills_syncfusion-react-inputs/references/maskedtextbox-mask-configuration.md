# Mask Configuration

## Table of Contents
- [Standard Mask Elements](#standard-mask-elements)
- [Custom Characters](#custom-characters)
- [Regular Expression Masks](#regular-expression-masks)
- [Prompt Character](#prompt-character)
- [Common Mask Patterns](#common-mask-patterns)

## Standard Mask Elements

The `mask` property accepts combinations of these standard mask tokens (based on MSDN MaskedTextBox standard):

| Token | Description |
|-------|-------------|
| `0` | Digit required — accepts `0` to `9` |
| `9` | Digit or space, optional |
| `#` | Digit or space, optional; `+` and `-` signs allowed |
| `L` | Letter required — accepts `a-z` and `A-Z` |
| `?` | Letter or space, optional |
| `&` | Any character required (alphabets, numbers, special chars) |
| `C` | Any character or space, optional |
| `A` | Alphanumeric (`A-Za-z0-9`) required |
| `a` | Alphanumeric (`A-Za-z0-9`) or space, optional |
| `<` | Shift down — converts all following characters to lowercase |
| `>` | Shift up — converts all following characters to uppercase |
| `\|` | Disables a previous `<` or `>` shift |
| `\\` | Escape — turns the next mask token into a literal character |
| Other | Any non-token character becomes a literal (e.g., `-`, `/`, `(`, `)`) |

> **Note:** When `mask` is empty or not set, MaskedTextBox behaves as a plain text input.

### Examples of Standard Mask Elements

```tsx
import { MaskedTextBoxComponent } from '@syncfusion/ej2-react-inputs';

// # accepts digits, spaces, + and -
<MaskedTextBoxComponent mask="#####" placeholder="Mask ##### (ex: 012+-)" floatLabelType="Always" />

// L allows only letters A-Z and a-z
<MaskedTextBoxComponent mask="LLLLLL" placeholder="Mask LLLLLL (ex: Sample)" floatLabelType="Always" />

// & allows alphabets, numbers, and special characters
<MaskedTextBoxComponent mask="&&&&&" placeholder="Mask &&&&& (ex: A12@#)" floatLabelType="Always" />

// > converts to uppercase, < converts to lowercase
<MaskedTextBoxComponent mask=">LLL<LLL" placeholder="Mask >LLL<LLL (ex: SAMple)" floatLabelType="Always" />

// \\ escapes A so it appears as literal 'A'
<MaskedTextBoxComponent mask="\\A999" placeholder="Mask \\A999 (ex: A321)" floatLabelType="Always" />
```

## Custom Characters

Use the `customCharacters` property to define non-standard mask tokens with their allowed values. This lets you use any character as a mask element with a custom acceptance set.

**Use case:** AM/PM time input, country codes, domain suffixes, or any custom alphabet constraint.

```tsx
import * as React from 'react';
import { MaskedTextBoxComponent } from '@syncfusion/ej2-react-inputs';

function App() {
  // P accepts: P, A, p, a  |  M accepts: M, m
  const chars = { P: 'P,A,p,a', M: 'M,m' };

  return (
    <MaskedTextBoxComponent
      mask="00:00 >PM"
      customCharacters={chars}
      placeholder="Time (ex: 10:00 PM, 10:00 AM)"
      floatLabelType="Always"
    />
  );
}
```

**Format:** Each key is a non-mask character used in `mask`, and the value is a comma-separated string of accepted input characters.

## Regular Expression Masks

Wrap a regular expression in square brackets `[regex]` to validate individual input positions. This is useful for IP addresses, versioned formats, or custom numeric ranges.

```tsx
import * as React from 'react';
import { MaskedTextBoxComponent } from '@syncfusion/ej2-react-inputs';

// IP address: each segment accepts 000–299
function App() {
  return (
    <MaskedTextBoxComponent
      mask="[0-2][0-9][0-9].[0-2][0-9][0-9].[0-2][0-9][0-9].[0-2][0-9][0-9]"
      placeholder="IP Address (ex: 212.212.111.222)"
      floatLabelType="Always"
    />
  );
}
```

> **Note:** The `.` between segments is a literal character (not a mask token), so it appears as-is in the mask.

## Prompt Character

The `promptChar` property sets the placeholder symbol shown at unfilled mask positions. Default is `_`.

```tsx
import * as React from 'react';
import { MaskedTextBoxComponent } from '@syncfusion/ej2-react-inputs';

// Use '#' as the prompt character instead of '_'
function App() {
  return (
    <MaskedTextBoxComponent
      mask="999-999-9999"
      promptChar="#"
    />
  );
}
```

## Common Mask Patterns

| Use Case | Mask |
|----------|------|
| US Phone | `000-000-0000` |
| US Phone with area code | `(000) 000-0000` |
| Zip Code | `00000` |
| Zip+4 | `00000-0000` |
| Date (MM/DD/YYYY) | `00/00/0000` |
| Time (HH:MM) | `00:00` |
| IP Address | `[0-2][0-9][0-9].[0-2][0-9][0-9].[0-2][0-9][0-9].[0-2][0-9][0-9]` |
| Product Key | `000-000-000-000` |
| Social Security Number | `000-00-0000` |
| Credit Card | `0000-0000-0000-0000` |
| All Uppercase Letters | `>LLLLLL` |
| Mixed case (3 up, 3 down) | `>LLL<LLL` |
