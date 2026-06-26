---
name: calculator
description: Perform mathematical calculations and unit conversions. Use when the user needs to calculate expressions, convert units (length, mass, temperature, volume, area, time), or solve math problems. Supports basic arithmetic (+, -, *, /, %, ^), scientific functions (sin, cos, tan, log, sqrt, etc.), and common unit conversions.
---

# Calculator Skill

Perform mathematical calculations and unit conversions.

## Usage

### Calculate Expressions

```bash
python3 scripts/calculator.py calc "<expression>"
```

**Supported operations:**
- Basic arithmetic: `+`, `-`, `*`, `/`, `%`, `^` (or `**`)
- Parentheses for grouping: `(2 + 3) * 4`
- Percentage: `50%` → `0.5`, `100 + 10%` → `110`

**Math functions:**
- Trigonometric: `sin()`, `cos()`, `tan()`, `asin()`, `acos()`, `atan()`
- Hyperbolic: `sinh()`, `cosh()`, `tanh()`
- Logarithms: `log()` (natural), `log10()`, `log2()`, `ln()`
- Powers/roots: `sqrt()`, `pow()`, `exp()`
- Rounding: `round()`, `floor()`, `ceil()`
- Other: `abs()`, `max()`, `min()`, `factorial()`, `gcd()`
- Constants: `pi`, `e`
- Angle conversion: `degrees()`, `radians()`

**Examples:**
```bash
python3 scripts/calculator.py calc "2 + 2"
python3 scripts/calculator.py calc "sin(pi/2)"
python3 scripts/calculator.py calc "sqrt(16) + log(10)"
python3 scripts/calculator.py calc "(100 - 20) * 1.5"
python3 scripts/calculator.py calc "2^10"
python3 scripts/calculator.py calc "50% of 200"
```

### Unit Conversions

```bash
python3 scripts/calculator.py convert <value> <from_unit> <to_unit>
```

**Supported categories:**

| Category | Units |
|----------|-------|
| Length | m, km, cm, mm, mi, yd, ft, in, nm |
| Mass | g, kg, mg, lb, oz, t/ton |
| Volume | l, ml, gal, qt, pt, cup, fl oz, tbsp, tsp |
| Area | m², km², cm², ha, acre, ft², in² |
| Time | s, min, h, d, wk, mo, y |
| Temperature | °C, °F, K |

**Examples:**
```bash
python3 scripts/calculator.py convert 100 km miles
python3 scripts/calculator.py convert 70 f c
python3 scripts/calculator.py convert 2.5 kg lb
python3 scripts/calculator.py convert 500 ml cups
```

## Output Format

All commands output JSON:

```json
{"result": 42}
{"result": 3.14159, "category": "length"}
{"error": "Division by zero"}
```

## Error Handling

Common errors and their meanings:
- `Division by zero` - Attempted to divide by zero
- `Invalid expression syntax` - Malformed expression
- `Unknown function or variable` - Used unsupported function/variable
- `Unsupported unit conversion` - Units not in same category or not recognized
