---
title: Use Consistent Naming Conventions
impact: MEDIUM
section: 3
impactDescription: Improves code readability and maintainability
tags: code-style, naming, consistency, eslint
---

## Use Consistent Naming Conventions

Inconsistent naming confuses developers and breaks tooling. NestJS follows specific conventions for maximum clarity. **Standardize all filenames, classes, and methods.**

**Incorrect (mixed conventions):**

```
userController.ts      // camelCase file
UserService.ts         // PascalCase file  
getuserById()          // mixed case method
Userservice            // missing suffix
```

**Correct (NestJS conventions):**

```
users.controller.ts    // kebab-case file
users.service.ts       // kebab-case file
UsersController        // PascalCase class
UsersService           // PascalCase class
findUserById()         // camelCase method ✅
getUserProfile()       // camelCase method ✅
```