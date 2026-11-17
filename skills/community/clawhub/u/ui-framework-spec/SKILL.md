---
name: ui-framework-spec
version: "0.1.0"
license: Apache-2.0
description: "A UI design specification system based on off-the-shelf UI frameworks (Element Plus, Ant Design, Arco Design, TDesign, Semi Design). Suitable for projects using framework-built-in components, as opposed to headless component libraries (shadcn/ui, Radix UI). Use when: generating UI code with a specified framework, reviewing existing code for framework compliance, recommending between frameworks, or migrating code from one framework to another. Keywords: Element Plus, Ant Design, Arco Design, TDesign, Semi Design, framework components, Vue components, React components, framework migration, design tokens, theme variables."
metadata:
  openclaw:
    emoji: 🧩
---

# UI Framework Spec

## Overview

This skill provides specification references for five major UI frameworks, guiding project development based on off-the-shelf UI frameworks. Unlike `custom-ui-spec` (for headless customization), this skill mandates using framework-provided components and design systems — do not implement component styles outside the framework.

## Supported Frameworks

| Framework | Ecosystem | Version | Design Language |
|---|---|---|---|
| Element Plus | Vue 3 | Latest | Enterprise back-office, clean and neutral |
| Ant Design | React | 5.x | Back-office, professional and stable |
| Arco Design | React | 2.x | ByteDance, modern and flexible |
| TDesign | React / Vue | Latest | Tencent, general enterprise-grade |
| Semi Design | React | 2.x | Douyin, content-immersive |

## Usage Modes

### Mode 1: Framework Selection Consultation

When the user has not specified a framework, read `references/framework-selection.md` for guidance.

**Selection Flow:**
1. Determine target platform (Vue / React / Other)
2. Determine design tone preference
3. Recommend 1-2 most suitable frameworks
4. Provide rationale and key differences

### Mode 2: Generating UI Code

When generating UI code with a specified framework:

1. Read the corresponding framework reference file (e.g., `references/ant-design.md`)
2. Follow the framework's component naming, Props conventions, and layout system
3. Use framework-provided APIs (Form, Table, Modal, etc.) — do not re-implement them
4. Follow the framework's design token / theme variable system
5. For detailed framework-specific component APIs, Claude should generate based on its own knowledge without exceeding the scope of official framework documentation
6. Code must import components from the official framework package (e.g., `import { Button } from 'antd'`) — do not create custom substitutes

### Mode 3: Reviewing UI Code

When reviewing existing code for framework compliance:

1. Determine the framework version in use
2. Read the corresponding framework reference file
3. Check item by item: correct component usage, Props compliance, use of framework tokens for styles, adherence to the framework grid system for layout
4. Report non-compliant items with suggested fixes

### Mode 4: Framework Migration

When migrating code from one framework to another:

1. Read the source and target framework reference files
2. Establish component mapping
3. Migrate Props and events (note naming differences, e.g., Ant Design's `onChange` vs Element Plus's `@change`)
4. Migrate the layout system (Flex/Grid)
5. Migrate the form validation system
6. Output the migration plan and change list

## Framework Differences Quick Reference

### Component Naming Differences

| Unified Concept | Element Plus | Ant Design | Arco Design | TDesign | Semi Design |
|---|---|---|---|---|---|
| Button | ElButton | Button | Button | Button | Button |
| Input | ElInput | Input | Input | Input | Input |
| Table | ElTable | Table | Table | Table | Table |
| Form | ElForm | Form | Form | Form | Form |
| Dialog | ElDialog | Modal | Modal | Dialog | Modal |
| Toast Message | ElMessage | message | Message | Message | Toast |
| Tabs | ElTabs | Tabs | Tabs | Tabs | Tab |
| Select | ElSelect | Select | Select | Select | Select |
| DatePicker | ElDatePicker | DatePicker | DatePicker | DatePicker | DatePicker |
| Tree | ElTree | Tree | Tree | Tree | Tree |

### Design Token / Theme Variable Systems

| Framework | Theming Mechanism | Variable Format |
|---|---|---|
| Element Plus | CSS Variables + SCSS | `--el-color-primary` |
| Ant Design | Design Token (CSS-in-JS) | `colorPrimary`, `borderRadius` |
| Arco Design | CSS Variables | `--color-primary-6` |
| TDesign | CSS Variables + Less | `--td-primary-color` |
| Semi Design | CSS Variables + Design Token | `--semi-color-primary` |

### Layout Systems

| Framework | Layout Approach |
|---|---|
| Element Plus | `ElContainer` + `ElRow`/`ElCol` (24-column grid) |
| Ant Design | `Layout` + `Row`/`Col` (24-column grid) + Flex |
| Arco Design | `Layout` + `Grid` (24-column grid) + `Grid.Row`/`Grid.Col` |
| TDesign | `Layout` + `Row`/`Col` (24-column grid) |
| Semi Design | `Layout` + `Row`/`Col` (24-column grid) |

## General Principles

1. **Prefer framework-built-in components** — do not re-implement standard components
2. **Follow the framework theming mechanism** — do not hardcode color values
3. **Use the framework layout system** — do not mix multiple layout approaches
4. **Use the framework icon library** — do not mix in external icon libraries
5. **Do not modify framework component DOM structures** — customize via Props or ConfigProvider
6. **Lock the version** — specify the framework version in use and reference the corresponding documentation

## Resource Reference

| File | When to Read |
|---|---|
| `references/framework-selection.md` | When the user has not specified a framework and needs a recommendation |
| `references/element-plus.md` | When using Element Plus (Vue) |
| `references/ant-design.md` | When using Ant Design (React) |
| `references/arco-design.md` | When using Arco Design (React) |
| `references/tdesign.md` | When using TDesign (React/Vue) |
| `references/semi-design.md` | When using Semi Design (React) |

For detailed framework API references and component documentation, Claude should generate based on its own knowledge or use WebSearch to fetch the latest official documentation. The reference files only cover core design philosophies, specification highlights, and key differences.
