# Mermaid Diagram Cheatsheet

Quick reference for all major Mermaid diagram types. Renders natively on GitHub, GitLab, Docusaurus, and most documentation tools.

## Flowchart

```mermaid
flowchart TD
    A[Start] --> B{Decision?}
    B -->|Yes| C[Action 1]
    B -->|No| D[Action 2]
    C --> E[End]
    D --> E
```

**Node shapes:** `[text]` rectangle, `(text)` rounded, `{text}` diamond, `((text))` circle, `>text]` flag

**Arrow styles:** `-->` solid, `-.->` dotted, `==>` thick, `--text-->` labeled

**Direction:** `TD` top-down, `LR` left-right, `BT` bottom-top, `RL` right-left

## Sequence Diagram

```mermaid
sequenceDiagram
    participant C as Client
    participant S as Server
    participant D as Database

    C->>S: POST /login
    activate S
    S->>D: SELECT user
    D-->>S: User record
    alt Valid password
        S-->>C: 200 + JWT
    else Invalid
        S-->>C: 401 Unauthorized
    end
    deactivate S

    Note over C,S: Subsequent requests use JWT

    loop Every 15 min
        C->>S: POST /refresh
        S-->>C: New JWT
    end
```

**Arrow types:** `->>` solid, `-->>` dashed, `-x` cross (failed), `)` open

**Blocks:** `alt/else/end`, `loop/end`, `opt/end`, `par/and/end`, `critical/end`

## Class Diagram

```mermaid
classDiagram
    class User {
        +String id
        +String email
        +String name
        +login() bool
        +logout() void
    }
    class Order {
        +String id
        +Decimal total
        +String status
        +cancel() bool
    }
    class Product {
        +String id
        +String name
        +Decimal price
    }

    User "1" --> "*" Order : places
    Order "*" --> "*" Product : contains
```

**Visibility:** `+` public, `-` private, `#` protected, `~` package

**Relations:** `-->` association, `--|>` inheritance, `..|>` implementation, `--*` composition, `--o` aggregation

## Entity Relationship

```mermaid
erDiagram
    USER ||--o{ ORDER : places
    ORDER ||--|{ LINE_ITEM : contains
    LINE_ITEM }o--|| PRODUCT : "refers to"

    USER {
        uuid id PK
        string email UK
        string name
    }
    ORDER {
        uuid id PK
        uuid user_id FK
        decimal total
    }
```

**Cardinality:** `||` exactly one, `o|` zero or one, `}|` one or more, `}o` zero or more

## State Diagram

```mermaid
stateDiagram-v2
    [*] --> Draft
    Draft --> Review: submit
    Review --> Draft: reject
    Review --> Approved: approve
    Approved --> Published: publish
    Published --> [*]: archive

    state Review {
        [*] --> PeerReview
        PeerReview --> TechReview
        TechReview --> [*]
    }
```

## Gantt Chart

```mermaid
gantt
    title Project Timeline
    dateFormat YYYY-MM-DD

    section Design
    Research          :done, d1, 2025-01-01, 7d
    Wireframes        :done, d2, after d1, 5d
    UI Design         :active, d3, after d2, 10d

    section Development
    Frontend          :dev1, after d3, 15d
    Backend           :dev2, after d3, 20d
    Integration       :dev3, after dev1, 5d

    section Testing
    QA Testing        :test1, after dev3, 7d
    Bug Fixes         :test2, after test1, 5d
```

## Pie Chart

```mermaid
pie title Browser Market Share
    "Chrome" : 65
    "Safari" : 18
    "Firefox" : 8
    "Edge" : 5
    "Other" : 4
```

## Git Graph

```mermaid
gitgraph
    commit id: "initial"
    branch develop
    checkout develop
    commit id: "feat-1"
    commit id: "feat-2"
    checkout main
    merge develop id: "v1.0"
    branch hotfix
    commit id: "fix-1"
    checkout main
    merge hotfix id: "v1.0.1"
```

## Mindmap

```mermaid
mindmap
    root((Documentation))
        Tutorials
            Getting Started
            Quick Start
        How-to Guides
            Authentication
            Deployment
        Reference
            API
            CLI
            Config
        Explanation
            Architecture
            Design Decisions
```

## C4 Context (using flowchart)

```mermaid
flowchart TB
    subgraph "External"
        U[fa:fa-user Customer]
        E[fa:fa-envelope Email Service]
    end

    subgraph "My System"
        WEB[Web Application]
        API[API Server]
        DB[(Database)]
    end

    U --> WEB
    WEB --> API
    API --> DB
    API --> E
```

## Tips

- **GitHub:** Wrap in triple backticks with `mermaid` language tag
- **Docusaurus/VitePress:** Supported natively via MDX plugins
- **Live editor:** [mermaid.live](https://mermaid.live)
- **Max complexity:** Keep diagrams under ~30 nodes for readability
- **Accessibility:** Always add a text description near the diagram
