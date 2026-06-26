# Code File Header Template

Every code file starts with three header comment lines:

## TypeScript / JavaScript

```typescript
// input:  [external dependencies (params, imported modules)]
// output: [what this file exports]
// pos:    [this file's role in the local system]
// ⚠️ When this file is updated, update its header and the parent FOLDER.md
```

## Python

```python
# input:  [external dependencies (params, imported modules)]
# output: [what this file exports (classes/functions)]
# pos:    [this file's role in the local system]
# ⚠️ When this file is updated, update its header and the parent FOLDER.md
```

## Go

```go
// input:  [external dependencies (params, imported packages)]
// output: [what this file exports (functions/structs)]
// pos:    [this file's role in the local system]
// ⚠️ When this file is updated, update its header and the parent FOLDER.md
```

## Java / C++ / C#

```java
// input:  [external dependencies (params, imported classes)]
// output: [what this file exports (public methods/classes)]
// pos:    [this file's role in the local system]
// ⚠️ When this file is updated, update its header and the parent FOLDER.md
```

---

## Examples

### Good Example (TypeScript)

```typescript
// input:  UserService, UserRepository
// output: UserController
// pos:    HTTP entry point for the user module; handles request parsing and response formatting
// ⚠️ When this file is updated, update its header and the parent FOLDER.md

import { UserService } from './user.service';
import { UserRepository } from './user.repository';

export class UserController {
  // ...
}
```

### Bad Example

```typescript
// User controller
// Handles user-related requests
// update: 2024-01-01
```

❌ No input/output/pos format — impossible to quickly understand module dependencies and responsibilities.
