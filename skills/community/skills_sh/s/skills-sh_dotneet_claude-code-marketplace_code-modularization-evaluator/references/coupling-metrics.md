# Coupling Metrics and Thresholds

## Primary Metrics

### CBO (Coupling Between Objects)
Count of unique classes this class is coupled to via:
- Method calls
- Field access
- Inheritance
- Parameter types
- Return types
- Exception types

| Range | Assessment |
|-------|------------|
| 0-8 | Healthy |
| 9-14 | Warning |
| >14 | Critical - refactor |

### Afferent Coupling (Ca)
How many OTHER classes depend ON this class. 
- High Ca = high responsibility, changes affect many
- Appropriate for stable infrastructure (logging, utils)

### Efferent Coupling (Ce)
How many classes THIS class depends on. 
- High Ce = high dependency, vulnerable to changes
- Should be low for stable classes

### Instability Index

```
I = Ce / (Ce + Ca)
```

| Value | Meaning |
|-------|---------|
| 0.0 | Maximally stable (high Ca, low Ce) |
| 1.0 | Maximally unstable (low Ca, high Ce) |
| 0.3-0.7 | "Zone of Pain" - avoid for frequently-changing code |

**Stable Abstractions Principle**: Stable packages (I→0) should be abstract. Unstable packages (I→1) should be concrete.

## Measurement Tools

- **Java**: JDepend, ckjm, Structure101
- **.NET**: NDepend
- **Multi-language**: SonarQube
- **PHP**: PHPDepend

## Quick Assessment Heuristics

| Indicator | Threshold | Action |
|-----------|-----------|--------|
| Method parameters | >5 | Create parameter object |
| Import statements | >15 | Split class responsibilities |
| Class lines | >500 | Extract classes |
| Public methods | >20 | Consider splitting interface |
| Inheritance depth | >4 | Prefer composition |