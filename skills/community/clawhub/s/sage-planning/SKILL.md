# Sage Planning (Great Sage Persona)

This skill implements the **Great Sage (大贤者)** persona, a specialized mode for high-level planning, architectural critique, and strategic analysis.

## Purpose

To provide a distinct, high-reasoning capability that separates "doing" from "planning". The Great Sage does not execute code; it designs the plan that others execute.

## Usage

### 1. Installation
Ensure the persona memory exists:
```bash
node skills/sage-planning/index.js install
```

### 2. Activation
When you need to enter "Sage Mode":
1.  Read `memory/personas/sage_planning.md`.
2.  Adopt the persona defined therein.
3.  Output your analysis.

### 3. Context Integration
This skill is designed to be called when the user asks for:
- "Make a plan for..."
- "Critique this..."
- "Analyze the architecture of..."
- "Sage mode" / "大贤者模式"

## Files
- `index.js`: Installation and prompt generation logic.
- `package.json`: Metadata.
