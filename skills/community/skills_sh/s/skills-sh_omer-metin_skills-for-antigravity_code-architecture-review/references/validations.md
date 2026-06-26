# Code Architecture Review - Validations

## Potential Circular Import

### **Id**
arch-circular-import
### **Severity**
error
### **Type**
regex
### **Pattern**
  - import.*from\s+['"]\.\..*['"].*\n[\s\S]{0,2000}import.*from\s+['"]\.\..*['"]
### **Message**
Complex relative imports may indicate circular dependencies. Check module graph.
### **Fix Action**
Use dependency injection or extract shared logic to break cycles
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## God Module Detection (File Size)

### **Id**
arch-god-file-size
### **Severity**
warning
### **Type**
file_size
### **Max Lines**

### **Message**
File exceeds 500 lines. Consider splitting by responsibility.
### **Fix Action**
Split into focused modules: auth.ts, profile.ts, billing.ts, etc.
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## God Module Detection (Export Count)

### **Id**
arch-god-file-exports
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - (export\s+(const|function|class|type|interface)\s+\w+.*\n){10,}
### **Message**
File has many exports. May be accumulating too many responsibilities.
### **Fix Action**
Group related exports into separate modules
### **Applies To**
  - **/*.ts
  - **/*.tsx

## Global State Mutation

### **Id**
arch-global-state-mutation
### **Severity**
error
### **Type**
regex
### **Pattern**
  - ^let\s+\w+\s*[:=]
  - ^var\s+\w+\s*[:=]
  - globalThis\.\w+\s*=
  - window\.\w+\s*=
### **Message**
Global mutable state creates hidden dependencies. Use dependency injection.
### **Fix Action**
Pass state as function parameters or use context/store pattern
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Database Access in Component

### **Id**
arch-db-in-component
### **Severity**
error
### **Type**
regex
### **Pattern**
  - prisma\.
  - drizzle\.
  - \$queryRaw
  - \bSELECT\s+.+\s+FROM\b
  - \bINSERT\s+INTO\b
### **Message**
Database access in component file. Move to data layer/repository.
### **Fix Action**
Create repository or data access layer for database operations
### **Applies To**
  - **/*.tsx
  - **/*.jsx
  - **/components/**/*.ts
  - **/components/**/*.js

## Direct Fetch in Component

### **Id**
arch-fetch-in-component
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - \bfetch\s*\(['"]https?://
  - axios\.(get|post|put|delete)\s*\(
### **Message**
Direct API calls in component. Use API layer or hooks.
### **Fix Action**
Create api/ layer or use data fetching hooks (useSWR, useQuery)
### **Applies To**
  - **/components/**/*.tsx
  - **/components/**/*.jsx

## Business Logic in useEffect

### **Id**
arch-business-logic-in-useeffect
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - useEffect\s*\([^)]*=>\s*\{[^}]{200,}
### **Message**
Complex logic in useEffect. Extract to custom hook or service.
### **Fix Action**
Move business logic to dedicated hook or service module
### **Applies To**
  - **/*.tsx
  - **/*.jsx

## Deep Relative Import Path

### **Id**
arch-deep-import-path
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - from\s+['"]\.\.[\\/]\.\.[\\/]\.\.[\\/]
  - from\s+['"]\.\.[\\/]\.\.[\\/]\.\.[\\/]\.\.[\\/]
### **Message**
Deep relative imports (../../../). Consider path aliases or restructure.
### **Fix Action**
Use path aliases (@/lib, @/components) or move file closer to dependencies
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Utils/Helpers Dumping Ground

### **Id**
arch-utils-dumping-ground
### **Severity**
info
### **Type**
regex
### **Pattern**
  - utils\.(ts|js)$
  - helpers\.(ts|js)$
  - misc\.(ts|js)$
  - common\.(ts|js)$
### **Message**
Generic utils/helpers file. Name files by what they do.
### **Fix Action**
Rename to specific purpose: formatDate.ts, validateEmail.ts, parseConfig.ts
### **Applies To**
  - **/*.ts
  - **/*.js

## String Type Discriminator

### **Id**
arch-string-type-discriminator
### **Severity**
info
### **Type**
regex
### **Pattern**
  - status\s*===?\s*['"][a-z]+
  - type\s*===?\s*['"][a-z]+
  - state\s*===?\s*['"][a-z]+
  - kind\s*===?\s*['"][a-z]+
### **Message**
String comparison for type discrimination. Use union types or enums.
### **Fix Action**
Define type Status = 'active' | 'inactive' | 'pending'
### **Applies To**
  - **/*.ts
  - **/*.tsx

## Any Type Usage

### **Id**
arch-any-type-usage
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - :\s*any\b
  - as\s+any\b
  - <any>
### **Message**
Using 'any' type bypasses TypeScript safety. Use specific types.
### **Fix Action**
Replace with specific type or use 'unknown' with type guards
### **Applies To**
  - **/*.ts
  - **/*.tsx

## Interface with Single Implementation

### **Id**
arch-single-implementation-interface
### **Severity**
info
### **Type**
regex
### **Pattern**
  - interface\s+I[A-Z]\w+\s*\{[^}]+\}\s*\n\s*class\s+\w+\s+implements\s+I[A-Z]
### **Message**
Interface with only one implementation. May be premature abstraction.
### **Fix Action**
Wait for second implementation before abstracting. Delete interface if not needed.
### **Applies To**
  - **/*.ts
  - **/*.tsx

## Abstract Class with Single Child

### **Id**
arch-abstract-class-single-child
### **Severity**
info
### **Type**
regex
### **Pattern**
  - abstract\s+class\s+\w+[^}]+\}\s*\n\s*class\s+\w+\s+extends
### **Message**
Abstract class with only one implementation. Consider simplifying.
### **Fix Action**
Merge into concrete class unless abstraction is planned for soon
### **Applies To**
  - **/*.ts
  - **/*.tsx

## Generic Used with Single Type

### **Id**
arch-generic-single-type
### **Severity**
info
### **Type**
regex
### **Pattern**
  - <T>.*<T>(?!.*<(?!T)\w+>)
### **Message**
Generic used with only one type. May be over-engineering.
### **Fix Action**
Use concrete type until you need the generic
### **Applies To**
  - **/*.ts
  - **/*.tsx

## Domain Importing Infrastructure

### **Id**
arch-domain-imports-infrastructure
### **Severity**
error
### **Type**
regex
### **Pattern**
  - domain/.*import.*from.*infrastructure/
  - domain/.*import.*from.*api/
  - domain/.*import.*from.*database/
### **Message**
Domain layer should not import from infrastructure. Dependencies flow inward.
### **Fix Action**
Use interfaces in domain, implement in infrastructure
### **Applies To**
  - **/domain/**/*.ts

## Cross-Feature Direct Import

### **Id**
arch-cross-feature-import
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - features/\w+/.*import.*from.*features/(?!\w+/shared)
### **Message**
Direct import across features. Use shared module or events.
### **Fix Action**
Extract shared code to features/shared/ or use event-based communication
### **Applies To**
  - **/features/**/*.ts
  - **/features/**/*.tsx

## Test Coupled to Implementation

### **Id**
arch-test-implementation-coupling
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - toHaveBeenCalledWith\([^)]{100,}
  - mock\(['"][\w./]+['"]\)
  - jest\.mock\(['"][\w./]+['"]\)
### **Message**
Tests may be coupled to implementation details. Test behavior instead.
### **Fix Action**
Test observable behavior and outputs, not internal method calls
### **Applies To**
  - **/*.test.ts
  - **/*.test.tsx
  - **/*.spec.ts
  - **/*.spec.tsx

## Testing Private Methods

### **Id**
arch-private-method-test
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - \['\w+'\]\s*\(
  - \(\w+\s+as\s+any\)\.\w+
### **Message**
Testing private methods. Test through public API instead.
### **Fix Action**
Test behavior through public methods. If private method needs testing, extract to separate module.
### **Applies To**
  - **/*.test.ts
  - **/*.test.tsx
  - **/*.spec.ts
  - **/*.spec.tsx

## Mixed Concerns in Single File

### **Id**
arch-mixed-concerns-file
### **Severity**
info
### **Type**
regex
### **Pattern**
  - (export\s+function|export\s+const).*\n[\s\S]{0,500}(export\s+type|export\s+interface).*\n[\s\S]{0,500}(export\s+class)
### **Message**
File mixes functions, types, and classes. Consider separating concerns.
### **Fix Action**
Separate into types.ts, utils.ts, and service classes
### **Applies To**
  - **/*.ts
  - **/*.tsx

## Large Barrel File

### **Id**
arch-barrel-file-large
### **Severity**
info
### **Type**
regex
### **Pattern**
  - (export\s+\*\s+from\s+['"][^'"]+['"];?\s*\n){10,}
### **Message**
Large barrel file (10+ re-exports). May cause bundle size issues.
### **Fix Action**
Use direct imports or tree-shakeable exports
### **Applies To**
  - **/index.ts
  - **/index.js