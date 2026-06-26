**Skill**: [LaTeX Tables with tabularray](../SKILL.md)

## Column Specification (colspec)

### Alignment Options

| Code       | Meaning                          |
|------------|----------------------------------|
| `l`        | Left-aligned                     |
| `c`        | Centered                         |
| `r`        | Right-aligned                    |
| `X`        | Flexible width (expands to fill) |
| `Q[width]` | Fixed width with wrapping        |

### Examples

```latex
% 3 centered columns
colspec = {ccc}

% Left, center, right
colspec = {lcr}

% Fixed widths
colspec = {Q[2cm] Q[3cm] Q[1.5cm]}

% Mixed: fixed left, flexible middle, fixed right
colspec = {Q[2cm] X Q[2cm]}

% With alignment in fixed-width
colspec = {Q[2cm,l] Q[3cm,c] Q[2cm,r]}
```
