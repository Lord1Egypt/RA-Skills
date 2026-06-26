# Slidev Diagrams

Mermaid and PlantUML diagram integration.

## Mermaid Diagrams

Use fenced code blocks with `mermaid` language.
````markdown
```mermaid
graph TD
  A[Start] --> B{Decision}
  B -->|Yes| C[Result 1]
  B -->|No| D[Result 2]
```
````

### Mermaid Options

Pass options as an object after the language identifier.
````markdown
```mermaid {theme: 'neutral', scale: 0.8}
graph TD
  A --> B
```
````

Common options:
- `theme` - Mermaid theme ('default', 'neutral', 'dark', 'forest')
- `scale` - Diagram scale factor

### Diagram Types

Mermaid supports many diagram types:
````markdown
```mermaid
flowchart LR
  A --> B --> C
```
```mermaid
sequenceDiagram
  Alice->>Bob: Hello
  Bob->>Alice: Hi
```
```mermaid
classDiagram
  Animal <|-- Dog
  Animal : +int age
  Dog : +bark()
```
```mermaid
stateDiagram-v2
  [*] --> Active
  Active --> [*]
```
```mermaid
erDiagram
  CUSTOMER ||--o{ ORDER : places
  ORDER ||--|{ LINE-ITEM : contains
```
```mermaid
pie title Pets
  "Dogs" : 386
  "Cats" : 85
  "Rats" : 15
```
```mermaid
gantt
  title Project
  section Phase 1
  Task 1 :a1, 2024-01-01, 30d
  Task 2 :after a1, 20d
```
````

### Configure Mermaid

Create `setup/mermaid.ts` for global configuration:
````typescript
import { defineMermaidSetup } from '@slidev/types'

export default defineMermaidSetup(() => {
  return {
    theme: 'forest',
    themeVariables: {
      primaryColor: '#4a9eff',
    },
  }
})
````

## PlantUML Diagrams

Use fenced code blocks with `plantuml` language.
````markdown
```plantuml
@startuml
Alice -> Bob: Hello
Bob --> Alice: Hi there
@enduml
```
````

PlantUML requires an external server. By default, Slidev uses the public PlantUML server.

### PlantUML Options
````markdown
```plantuml {scale: 0.7}
@startuml
class User {
  +name: String
  +login()
}
@enduml
```
````

### Configure PlantUML Server

Set a custom server in headmatter:
````yaml
---
plantUmlServer: https://www.plantuml.com/plantuml
---
````

Or use a local server for offline use:
````yaml
---
plantUmlServer: http://localhost:8080
---
````

## Click Animations in Diagrams

Mermaid diagrams do NOT support v-click animations directly. To animate diagram elements, split into multiple slides or use multiple diagrams with v-click:
````markdown
<v-click>
```mermaid
graph LR
  A --> B
```

</v-click>

<v-click>
```mermaid
graph LR
  A --> B --> C
```

</v-click>
````