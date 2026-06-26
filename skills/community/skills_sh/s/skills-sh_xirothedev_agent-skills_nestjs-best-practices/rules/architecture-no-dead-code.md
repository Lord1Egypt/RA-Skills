---
title: Remove Unused Code and Dependencies
impact: MEDIUM
section: 3
impactDescription: Reduces bundle size and maintenance burden
tags: code-quality, cleanup, dead-code, dependencies
---

## Remove Unused Code and Dependencies

Dead code bloats the project and confuses developers. Unused dependencies increase attack surface. Regular cleanup keeps codebase lean. **No unused imports, functions, or packages.**

**Incorrect (code rot):**

```typescript
// users.service.ts - Dead weight 🚨
import * as bcrypt from 'bcrypt';  // Unused
import { SomeOtherService } from './other.service';  // Unused

@Injectable()
export class UsersService {
  unusedFunction() {  // Never called
    return 'unused';
  }
  
  async createUser(data: any) {
    return this.prisma.user.create({ data });  // bcrypt never used
  }
}
```

```json
// package.json - Unused deps
{
  "dependencies": {
    "lodash": "^4.17.20",     // Never imported
    "moment": "^2.29.4",      // Replaced by date-fns
    "axios": "^1.0.0"         // Switched to fetch
  }
}
```

**Correct (clean codebase):**

```bash
# Remove dead code
bun run lint -- --fix  # eslint --fix
bun run depcheck       # Find unused deps

# Tools
bunx depcheck           # Unused packages
bunx ts-unused-exports  # Unused exports
```

```json
// package.json - Clean ✅
{
  "scripts": {
    "cleanup": "bun pm prune && bun pm cache rm && bun run lint:fix",
    "depcheck": "depcheck && ts-unused-exports tsconfig.json"
  }
}
```