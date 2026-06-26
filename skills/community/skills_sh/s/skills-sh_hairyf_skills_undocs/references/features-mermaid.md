---
name: undocs-mermaid
description: Render Mermaid diagrams in markdown documentation
---

# Mermaid Diagrams

Undocs supports Mermaid diagrams for creating flowcharts, sequence diagrams, and other visualizations.

## Basic Usage

Use standard markdown code blocks with `mermaid` language:

````markdown
```mermaid
graph TD
    A[Start] --> B[Process]
    B --> C[End]
```
````

## Theme Configuration

Configure the theme using Mermaid initialization:

````markdown
```mermaid
%%{init: {'theme':'neutral'}}%%
graph TD
    A[Start] --> B[Process]
    B --> C[End]
```
````

## Interactive Diagrams

Add click handlers to make diagrams interactive:

````markdown
```mermaid
graph TD
    A[Getting Started] --> B[Components]
    B --> C[Content Transform]

    click A "/guide"
    click B "/guide/components/components"
    click C "/guide/components/content-transformation"
```
````

## Supported Diagram Types

Mermaid supports various diagram types:

- Flowcharts (`graph`, `flowchart`)
- Sequence diagrams (`sequenceDiagram`)
- Class diagrams (`classDiagram`)
- State diagrams (`stateDiagram`)
- Entity relationship diagrams (`erDiagram`)
- User journey (`journey`)
- Gantt charts (`gantt`)
- Pie charts (`pie`)
- Git graphs (`gitGraph`)

## Usage Examples

### Flowchart

````markdown
```mermaid
graph LR
    A[Install] --> B[Configure]
    B --> C[Deploy]
```
````

### Sequence Diagram

````markdown
```mermaid
sequenceDiagram
    participant User
    participant CLI
    participant Nuxt
    
    User->>CLI: undocs dev
    CLI->>Nuxt: Start server
    Nuxt-->>User: Ready
```
````

## Key Points

- Use standard markdown code blocks with `mermaid` language
- Theme can be configured using Mermaid initialization syntax
- Supports click handlers for interactive navigation
- Diagrams are rendered client-side using Mermaid.js
- All standard Mermaid diagram types are supported

<!--
Source references:
- https://undocs.unjs.io/guide/components/components
- https://mermaid.js.org/
-->
