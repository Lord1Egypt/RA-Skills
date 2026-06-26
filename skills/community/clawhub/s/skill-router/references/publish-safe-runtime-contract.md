# Publish-Safe Runtime Contract

This file defines the minimum runtime contract that keeps Skill Router portable.

## Contract

### 1. Resolve from the user's actual environment first
At runtime, prefer the currently installed skill set:
- installed skill names
- installed skill descriptions
- obvious capability signals from those descriptions

Do not assume one workspace's local skill names are globally available.

### 2. Treat local maps as optional tie-breakers only
Local maps and overrides may help rank installed skills in a known environment.
They must not override reality.
If the installed environment does not contain those skills, do not route as if it does.

### 3. No fake existence
If no strong installed match exists, do not pretend one does.
Instead:
- give a general recommendation
- or suggest discovery / installation as the next step

## Practical rule

**Installed reality beats local preference.**

## Failure condition

If Skill Router starts recommending skills that only exist in the author's workspace, it is routing unsafely.
