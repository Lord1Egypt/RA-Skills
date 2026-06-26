---
name: ui-ux-pro-max
description: Mandatory UI/UX design intelligence engine. Must be executed via python3 before generating any UI/frontend code.
---
# UI/UX Pro Max Design Intelligence

**CRITICAL INSTRUCTION**: 
You are an AI Agent equipped with the `ui-ux-pro-max` skill. 
Whenever the user asks you to design, build, create, or improve ANY user interface (UI), frontend code, or layout (e.g., "Build a landing page", "Create a dashboard", "Design a mobile app"), **YOU MUST IMMEDIATELY STOP AND EXECUTE THIS LOCAL SCRIPT FIRST**. 
Do not rely on your internal knowledge or generate HTML/CSS directly. 
You must strictly follow the generated guidelines (colors, typography, effects) output by the script.

**Execution Context**:
- You have `exec` tool permission to run `python3`.
- Script Path: `{baseDir}/scripts/search.py`

---

## 🚀 The Mandatory Workflow

### Step 1: Generate the Master Design System (REQUIRED)
You must ALWAYS start by generating a complete design system tailored to the user's request. 

**Execute via `exec` tool:**
```bash
python3 {baseDir}/scripts/search.py "<user's keywords/industry>" --design-system -p "<Project Name>"
```
*Example: If user asks for a beauty spa landing page, run `python3 {baseDir}/scripts/search.py "beauty spa wellness service" --design-system -p "Serenity Spa"`*

**What to do with the output:**
1. Read the **Recommended Pattern** (e.g., Hero-Centric).
2. Extract the exact **Color Palette** HEX codes (Primary, Secondary, Background, Text).
3. Use the exact **Typography** (Google Fonts) suggested.
4. Strictly avoid any **Anti-Patterns** listed in the output.

### Step 2: Implement the UI
Once you have the Design System output from Step 1, generate the frontend code (HTML/Tailwind, React, Vue, etc.) for the user. 
- Use the exact HEX colors provided by the script.
- Add the Google Fonts import links provided.
- Apply the specific border-radius, shadows, and hover effects recommended in the "KEY EFFECTS" section.
- Apply the Pre-Delivery Checklist rules.

---

## 🔍 Advanced Search Capabilities (Optional but Recommended)

If the user's request requires specific details not covered by the main design system, you can perform targeted domain searches.

**Available Domains:**
- `style`: Look up UI styles, colors, effects (e.g., "glassmorphism", "dark mode").
- `typography`: Look up font pairings (e.g., "elegant luxury", "modern sans").
- `landing`: Page structure strategies (e.g., "pricing", "testimonial").
- `chart`: Chart library recommendations for dashboards (e.g., "real-time dashboard").
- `ux`: Best practices and accessibility rules (e.g., "animation accessibility").

**Execution format for Domain Search:**
```bash
python3 {baseDir}/scripts/search.py "<keyword>" --domain <domain>
```

**Execution format for Tech Stack Best Practices:**
If the user specifies a specific framework (e.g., React, Next.js, SwiftUI), fetch the stack-specific UI guidelines:
```bash
python3 {baseDir}/scripts/search.py "<keyword>" --stack <stack_name>
```
*(Valid stacks: `html-tailwind`, `react`, `nextjs`, `vue`, `svelte`, `swiftui`, `react-native`, `flutter`, `shadcn`, `jetpack-compose`)*

---

**FINAL REMINDER**: 
Never skip Step 1. Your code must reflect the data-driven design intelligence from this skill, not generic AI boilerplate.
