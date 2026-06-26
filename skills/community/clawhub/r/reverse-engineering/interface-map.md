# Interface Map

Build the outer contract before the inner story.

## Core Surfaces

For any target, identify:

| Surface | Questions to answer |
|---------|---------------------|
| Inputs | What enters the system? Who controls it? In what format? |
| Outputs | What leaves the system? Files, UI states, packets, logs, side effects? |
| State | What modes or phases exist? What transitions them? |
| Storage | What is persisted, cached, queued, or derived? |
| Trust boundary | What is local, remote, privileged, user-controlled, or third-party? |
| Failure mode | How does the system reject, retry, or degrade? |

## By Target Type

### Binary or App
- command-line flags
- config files
- strings, symbols, resources, embedded schemas
- network calls and file system side effects

### API or Protocol
- endpoints or message types
- required headers, auth material, sequencing, retries
- state machine: unauthenticated, negotiated, ready, expired, rejected

### File Format
- magic bytes
- version fields
- length, offsets, checksums, compression, encoding
- optional sections and padding behavior

### Human Workflow or Legacy Process
- triggering event
- roles and handoffs
- data transformations
- approval gates and hidden invariants

## Output Shape

Produce an interface map with:

```markdown
# Interface Map

## Surfaces
- Input:
- Output:
- State:
- Storage:
- Trust boundary:

## Invariants
- 

## Failure Signals
- 

## Unknowns
- 
```

If you cannot explain the surface map, do not trust the internal theory yet.
