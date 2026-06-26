---
name: Xiaoqinli (XQL)
description: AST-First transpiler for AI agents 鈥?write structured .xql.json, compile to Go/Rust/TypeScript/Kotlin/Swift/Python with type safety, effect inference, and capability checks
version: 2.1.0
metadata:
  openclaw:
    requirements:
      binaries:
        - xql
---

# Xiaoqinli (XQL) 鈥?AST-First Transpiler

AI agents write structured `.xql.json` (JSON AST) directly 鈥?no parser needed, no syntax errors possible. The compiler validates types, effects, and capabilities at compile time, then emits idiomatic source code in 6 languages.

## Install

```bash
# From source (requires Go 1.23+)
git clone https://github.com/Freecode100Year/xiaoqinli.git
cd xiaoqinli && go build -o xql .

# Move to PATH
# Linux/macOS: sudo mv xql /usr/local/bin/
# Windows: move xql.exe to a directory in %PATH%
```

## Usage

```bash
# Validate AST
xql validate --file program.xql.json

# Compile to target language
xql compile --file program.xql.json --target go
xql compile --file program.xql.json --target rust --out main.rs
xql compile --file program.xql.json --target ts --out main.ts
xql compile --file program.xql.json --target kotlin --out Main.kt
xql compile --file program.xql.json --target swift --out main.swift
xql compile --file program.xql.json --target py --out main.py
```

## .xql.json AST Format

Every node has a `"kind"` field. Top-level must be `"Program"` with `"declarations"` array.

### Type System

| Kind | Go | Rust | TypeScript | Kotlin | Swift | Python |
|------|-----|------|------------|--------|-------|--------|
| `Int` | `int` | `i64` | `number` | `Long` | `Int` | `int` |
| `Float` | `float64` | `f64` | `number` | `Double` | `Double` | `float` |
| `String` | `string` | `String` | `string` | `String` | `String` | `str` |
| `Bool` | `bool` | `bool` | `boolean` | `Boolean` | `Bool` | `bool` |
| `Void` | *(none)* | *(none)* | `void` | `Unit` | *(none)* | `None` |
| `Array` | `[]T` | `Vec<T>` | `T[]` | `List<T>` | `[T]` | `list[T]` |
| `Option` | `*T` | `Option<T>` | `T \| null` | `T?` | `T?` | `Optional[T]` |
| `Result` | `(T, error)` | `Result<T, E>` | 鈥?| 鈥?| 鈥?| 鈥?|

### Node Kinds

**Declarations:**
- `Program` 鈥?top-level, contains `declarations[]`
- `FunctionDecl` 鈥?`name`, `params[]`, `returnType`, `effects[]`, `grant[]`, `body[]`

**Statements:**
- `VarDecl` 鈥?`name`, `type`, `value`
- `AssignStmt` 鈥?`target`, `value`
- `ReturnStmt` 鈥?`value` (optional)
- `IfStmt` 鈥?`cond`, `then[]`, `else[]`
- `WhileStmt` 鈥?`cond`, `body[]`
- `ExprStmt` 鈥?`expr`

**Expressions:**
- `Literal` 鈥?`valueType` (String/Int/Float/Bool), `value`
- `Ident` 鈥?`name`
- `BinaryExpr` 鈥?`op` (+, -, *, /, %, ==, !=, <, >, <=, >=, &&, ||), `left`, `right`
- `UnaryExpr` 鈥?`op` (!, -), `operand`
- `CallExpr` 鈥?`callee` (string), `args[]`
- `MemberExpr` 鈥?`object`, `field`

### Built-in Functions

| Name | Effect | Description |
|------|--------|-------------|
| `println` | state | Print with newline |
| `printf` | state | Formatted print |
| `sprintf` | pure | Formatted string build |

### Safety Annotations

- `effects: ["pure"]` 鈥?compiler verifies no side effects (transitive)
- `effects: ["state"]` / `["network"]` / `["filesystem"]` 鈥?declare side effects
- `grant: ["io", "network"]` 鈥?capability declaration; callee must be subset of caller

## Example

```json
{
  "kind": "Program",
  "declarations": [
    {
      "kind": "FunctionDecl",
      "name": "greet",
      "params": [{"name": "name", "type": {"kind": "String"}}],
      "returnType": {"kind": "String"},
      "effects": ["pure"],
      "grant": [],
      "body": [{
        "kind": "ReturnStmt",
        "value": {
          "kind": "BinaryExpr", "op": "+",
          "left": {"kind": "Literal", "valueType": "String", "value": "Hello, "},
          "right": {"kind": "Ident", "name": "name"}
        }
      }]
    },
    {
      "kind": "FunctionDecl",
      "name": "main",
      "params": [],
      "returnType": {"kind": "Void"},
      "effects": ["state"],
      "grant": ["io"],
      "body": [{
        "kind": "ExprStmt",
        "expr": {
          "kind": "CallExpr", "callee": "println",
          "args": [{
            "kind": "CallExpr", "callee": "greet",
            "args": [{"kind": "Literal", "valueType": "String", "value": "World"}]
          }]
        }
      }]
    }
  ]
}
```

Compiles to Go:
```go
package main

import "fmt"

func greet(name string) string {
    return "Hello, " + name
}

func main() {
    fmt.Println(greet("World"))
}
```

## Three Static Checks

| Check | What it does | Error codes |
|-------|-------------|-------------|
| **Type check** | Validates types, function signatures, return types, argument counts | `XQL_E2xx` |
| **Effect inference** | Infers side effects transitively through call chains | `XQL_E2xx` |
| **Capability check** | Enforces `@grant` 鈥?callee capabilities must be subset of caller's | `XQL_E3xx` |

## Error Codes

| Range | Category |
|-------|----------|
| `XQL_E1xx` | Parse / AST errors |
| `XQL_E2xx` | Type / effect errors |
| `XQL_E3xx` | Capability errors |
| `XQL_E4xx` | Codegen errors |

## Workflow

1. Write `.xql.json` AST file
2. Run `xql validate --file program.xql.json` to check
3. Run `xql compile --file program.xql.json --target go --out main.go` to generate source
4. Build with target language toolchain (e.g., `go build -o app.exe main.go`)

## Source

https://github.com/Freecode100Year/xiaoqinli
