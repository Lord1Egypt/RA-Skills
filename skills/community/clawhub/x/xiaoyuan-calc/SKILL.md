---
name: xiaoyuan-calc
description: |
  A powerful mathematical assistant that supports all scientific calculator functions, 
  equation solving, inequality solving, and provides detailed calculation steps and explanations.
  Powered by 小猿 AI (Xiaoyuan AI)
---

# xiaoyuan Calculator

A powerful mathematical calculation tool that supports scientific calculations, equation solving, inequality solving, and provides detailed calculation steps and explanations.

**Powered by 小猿 AI (Xiaoyuan AI)**

## Usage

**Important: All inputs must use LaTeX format!**

```bash
python3 <skill-path>/scripts/calc.py "<LaTeX expression>" [language]
```

### LaTeX Format Guide
- Multiplication: Use `\times` or `\cdot`, e.g., `3 \times 4`
- Division: Use `\div` or `/`, e.g., `8 \div 2`
- Fraction: Use `\frac{numerator}{denominator}`, e.g., `\frac{1}{2}`
- Square root: Use `\sqfrt{number}`, e.g., `\sqrt{16}`
- Power: Use `^`, e.g., `x^2`
- Trigonometric functions: `\sin`, `\cos`, `\tan`, etc.
- Inequality symbols: `\geq`, `\leq`, `>`, `<`
- Greek letters: `\pi`, `\theta`, `\alpha`, etc.
- System of equations: Use `\begin{cases}...\end{cases}`, e.g.:
  ```
  \begin{cases}
  x + y = 10 \\
  x - y = 2
  \end{cases}
  ```

## Core Features

### 1. Basic Operations
- Arithmetic operations: `+`, `-`, `\times`, `\div`
- Power operations: `x^2`, `x^3`
- Roots: `\sqrt{x}`, `\sqrt[3]{x}`
- Fractions: `\frac{a}{b}`
- Percentage calculations

### 2. Scientific Calculations
- **Trigonometric functions**: `\sin(x)`, `\cos(x)`, `\tan(x)`, `\arcsin(x)`, `\arccos(x)`, `\arctan(x)`
- **Logarithms**: `\log(x)`, `\ln(x)`, `\log_{a}(b)`
- **Exponentials**: `e^x`, `a^b`
- **Others**: Absolute value `|x|`, factorial `n!`
- **Constants**: `\pi`, `e`

### 3. Equation Solving
Supports solving various algebraic equations (**no need** for `solve()` wrapper):
- Linear equations: `2x + 5 = 15`
- Quadratic equations: `x^2 - 5x + 6 = 0`
- Higher-order equations: `x^3 - 6x^2 + 11x - 6 = 0`
- System of linear equations (two variables):
  ```
  \begin{cases}
  x + y = 10 \\
  x - y = 2
  \end{cases}
  ```
- Multi-variable systems:
  ```
  \begin{cases}
  x + y + z = 6 \\
  2x - y + z = 3 \\
  x + 2y - z = 2
  \end{cases}
  ```

### 4. Inequality Solving
Supports solving various inequalities (**no need** for `solve()` wrapper):
- Single-variable inequalities: `2x + 5 > 15`
- Quadratic inequalities: `x^2 - 4 \geq 0`
- Inequality systems: `x + 2 > 5, x - 3 < 10`

### 5. Step-by-Step Solutions
Automatically returns detailed calculation process, for example:

```
Input: x^2 - 5x + 6 = 0
Step 1: Identified as a quadratic equation
Step 2: Using factorization method (x-2)(x-3) = 0
Step 3: Solutions found: x = 2 or x = 3
Result: x = 2, x = 3
```

## Usage Examples

```bash
# Basic calculations (LaTeX format)
python3 scripts/calc.py "2 + 3 \times 4"                    # 14
python3 scripts/calc.py "(2 + 3) \times 4"                  # 20
python3 scripts/calc.py "\sqrt{144}"                        # 12
python3 scripts/calc.py "2^8"                               # 256
python3 scripts/calc.py "\frac{10}{2}"                      # 5

# Scientific calculations
python3 scripts/calc.py "\sin(\frac{\pi}{2})"               # 1.0
python3 scripts/calc.py "\log(1000)"                        # 3.0
python3 scripts/calc.py "5!"                                # 120

# Equation solving (direct input, no solve wrapper needed)
python3 scripts/calc.py "2x + 5 = 15"                       # Linear equation: x = 5
python3 scripts/calc.py "x^2 - 4 = 0"                       # Quadratic equation: x = -2, x = 2

# System of linear equations (two variables)
python3 scripts/calc.py "\\begin{cases} x + y = 10 \\\\ x - y = 2 \\end{cases}"              # x = 6, y = 4
python3 scripts/calc.py "\\begin{cases} 2x + 3y = 12 \\\\ x - y = 1 \\end{cases}"            # x = 3, y = 2

# System of linear equations (three variables)
python3 scripts/calc.py "\\begin{cases} x + y + z = 6 \\\\ 2x - y + z = 3 \\\\ x + 2y - z = 2 \\end{cases}"

# Inequality solving
python3 scripts/calc.py "2x + 5 > 15"                       # x > 5
python3 scripts/calc.py "x^2 - 4 \geq 0"                    # x ≤ -2 or x ≥ 2

# Specify language
python3 scripts/calc.py "2 + 3" zh
python3 scripts/calc.py "2 + 3" en
```

## Features

- Supports complete LaTeX mathematical expressions
- Automatically records and displays calculation steps
- High-precision numerical calculations
- User-friendly error messages
- Multi-language output support

## Notes

- **LaTeX format input is required**
- Equations and inequalities should be input directly, no `solve()` wrapper needed
- Trigonometric functions use radians by default
- Default variable for equation solving is `x`
- Inequality solutions are represented in interval notation
