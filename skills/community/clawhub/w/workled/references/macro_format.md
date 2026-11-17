# Macro Format Reference

This document details the macro JSON array format used by the workled device.

## Syntax

A macro is a JSON array of segments. Each segment is an object with **exactly
one key**: the key names the segment type and the value carries its parameters.

```json
[
  {"combo": "ctrl+c"},
  {"delay": 500},
  {"text": "Hello World"}
]
```

- Scalar types (`combo`, `press`, `release`, `delay`, `text`, `password`) take
  a plain value (string or number).
- Multi-field types (`delay_rand`, `mouse_move`, `mouse_scroll`,
  `mouse_button`) take a nested object.
- `[]` is a valid empty macro (no-op).

## Segment Overview

| type | parameter | description |
|---|---|---|
| `combo` | string | press and release a key combo |
| `press` | string | hold a key combo down |
| `release` | string | release a held key combo |
| `delay` | int (ms) | wait a fixed time (min 20) |
| `delay_rand` | object `{min, max}` | wait a random time between MIN-MAX ms (min 20) |
| `text` | string | type ASCII text |
| `password` | string | type a password stored in encrypted NVS |
| `mouse_move` | object `{x, y}` | relative cursor move (-128..127) |
| `mouse_scroll` | object `{wheel, pan?}` | wheel scroll (-128..127) |
| `mouse_button` | object `{button, gesture?}` | click or hold a mouse button |

### combo

Press and release a key combination. Case-insensitive.

- `{"combo": "a"}` — press key and release
- `{"combo": "shift+ctrl+a"}` — press key combo and release

### press

Press and hold a key combo.

- `{"press": "space"}` — press and hold

### release

Release a held key combo.

- `{"release": "shift"}` — release key
- `{"release": "ctrl+b"}` — release combo

### delay

Wait N ms (min 20).

- `{"delay": 50}` — delay 50 ms

### delay_rand

Random wait between MIN and MAX ms (min 20, MAX >= MIN).

- `{"delay_rand": {"min": 100, "max": 500}}`

### text

Type ASCII text. JSON escaping handles quotes, backslashes and whitespace.

- `{"text": "hello"}` — plain text
- `{"text": "hello world"}` — with spaces
- `{"text": "hello\"world"}` — escaped quote
- `{"text": "hello\\world"}` — escaped backslash

### password

Type a password stored in encrypted hardware NVS. Stored/queried macros show
`*` of identical length.

- `{"password": "Abc123"}` — plain password

### mouse_move

Move cursor by relative delta. Both `x` and `y` required, range -128..127.

- `{"mouse_move": {"x": 30, "y": 0}}` — move right 30 px
- `{"mouse_move": {"x": 0, "y": -40}}` — move up 40 px

### mouse_scroll

Scroll the mouse wheel. `wheel` required; `pan` optional (default 0).
Both in range -128..127.

- `{"mouse_scroll": {"wheel": -3}}` — scroll down 3 notches
- `{"mouse_scroll": {"wheel": 0, "pan": 3}}` — pan right

### mouse_button

Click or hold a mouse button. `button`: left, right, middle.
`gesture`: click (default), down, up.

- `{"mouse_button": {"button": "left"}}` — left click
- `{"mouse_button": {"button": "right", "gesture": "click"}}` — right click
- `{"mouse_button": {"button": "left", "gesture": "down"}}` — press and hold
- `{"mouse_button": {"button": "left", "gesture": "up"}}` — release

## Key Names (case-insensitive)

### Letters

| a | b | c | d | e | f | g | h | i | j | k | l |
|---|---|---|---|---|---|---|---|---|---|---|---|
| m | n | o | p | q | r | s | t | u | v | w | x | y | z |

### Digits

| 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|

### Function Keys

| f1 | f2 | f3 | f4 | f5 | f6 |
|---|---|---|---|---|---|
| f7 | f8 | f9 | f10 | f11 | f12 |

### Navigation

| enter | esc | escape | tab | space | backspace | delete |
|---|---|---|---|---|---|---|
| insert | home | end | page_up | page_down |

### Arrows

| up | down | left | right |
|---|---|---|---|

### Lock Keys

| caps_lock | num_lock | scroll_lock |
|---|---|---|

### System Keys

| print_screen | pause | menu |
|---|---|---|

### Media Keys

| mute | volume_up | volume_down | play_pause | next_track | previous_track |
|---|---|---|---|---|---|

### Modifier Keys

| Name | Aliases |
|---|---|
| `ctrl` | `left_ctrl`, `right_ctrl` |
| `shift` | `left_shift`, `right_shift` |
| `alt` | `left_alt`, `right_alt`, `option` |
| `gui` | `left_gui`, `right_gui`, `command`, `cmd`, `meta`, `win` |

Modifiers are combined with other keys using `+`, e.g. `ctrl+c`, `shift+tab`, `ctrl+alt+delete`, `ctrl+win+v`.

## Examples

### type with delay:
```json
[
  {"text": "Hello"},
  {"delay": 500},
  {"text": "World"}
]
```

### type with random delay:
```json
[
  {"text": "Hello"},
  {"delay_rand": {"min": 100, "max": 200}},
  {"text": "World"}
]
```

### type uppercase ABC:
```json
[
  {"text": "ABC"}
]
```

### type uppercase ABC (external SHIFT):
```json
[
  {"press": "shift"},
  {"text": "abc"},
  {"release": "shift"}
]
```

### copy and paste:
```json
[
  {"combo": "ctrl+c"},
  {"combo": "ctrl+v"}
]
```

### multi-line input:
```json
[
  {"text": "Line 1"},
  {"combo": "enter"},
  {"text": "Line 2"}
]
```

### Volume sequence:
```json
[
  {"combo": "volume_up"},
  {"delay": 100},
  {"combo": "volume_down"}
]
```

### drag with the left button:
```json
[
  {"mouse_button": {"button": "left", "gesture": "down"}},
  {"mouse_move": {"x": 40, "y": 10}},
  {"mouse_move": {"x": -30, "y": -50}},
  {"mouse_button": {"button": "left", "gesture": "up"}}
]
```

### Windows: open Run dialog:
```json
[
  {"combo": "gui+r"},
  {"delay": 100},
  {"text": "notepad"},
  {"combo": "enter"}
]
```

### Windows unlock with long press:
Recommended binding: `long_press`. Locks the screen first, waits for the display to wake, then types the password and confirms:
```json
[
  {"combo": "gui+l"},
  {"delay": 1000},
  {"combo": "enter"},
  {"password": "hello"},
  {"combo": "enter"}
]
```

### WeChat voice to text:
Recommended binding: `single_click`. Toggle voice recording on/off with touch effect:
```json
[
  {"press": "ctrl+win"}
]
```

### WorkBuddy voice to text:
Recommended binding: `single_click`. Toggle voice recording on/off without touch effect:
```json
[
  {"combo": "ctrl+d"}
]
```
