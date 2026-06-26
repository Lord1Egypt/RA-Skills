# Code Architecture Review - Sharp Edges

## Abstraction Before Duplication

### **Id**
abstraction-before-duplication
### **Summary**
Creating abstractions before you have concrete examples
### **Severity**
critical
### **Situation**
  You see a pattern that might repeat, so you create an interface,
  abstract class, or generic solution before you have 2+ concrete
  implementations.
  
### **Why**
  Premature abstraction creates the WRONG abstraction. You don't know
  the requirements yet. You'll either:
  1. Force future code to fit your bad abstraction
  2. Rewrite the abstraction when requirements become clear
  3. Work around it with hacks that defeat the purpose
  
  Wait for duplication. "Rule of three" - abstract on the third use.
  
### **Solution**
  Write concrete code first. When you see ACTUAL duplication:
  1. Note what's the same and what's different
  2. Extract the common parts
  3. Parameterize the differences
  
  The pattern reveals itself through real usage.
  
### **Symptoms**
  - We might need to support X someday
  - Interface with one implementation
  - Generic<T> used with only one type
  - Abstract class with one child
### **Detection Pattern**
interface.*\{[^}]+\}.*class.*implements

## Circular Dependency Spiral

### **Id**
circular-dependency-spiral
### **Summary**
Circular dependencies that grow until the system is unmaintainable
### **Severity**
critical
### **Situation**
  Module A imports from B, B imports from C, C imports from A.
  Or worse: A <-> B direct circular import.
  
### **Why**
  Circular dependencies make it impossible to:
  - Load modules in a sensible order
  - Test modules in isolation
  - Understand the flow of data
  - Reason about side effects
  
  They grow over time. Adding "just one more import" is easy.
  The circular graph becomes load-bearing.
  
### **Solution**
  Break the cycle:
  1. Extract shared logic into a new module both depend on
  2. Use dependency injection - pass dependencies in
  3. Create an interface in the "lower" module, implement in "higher"
  4. Use events/callbacks instead of direct calls
  
  # Before (circular)
  userService.ts -> orderService.ts -> userService.ts
  
  # After (broken cycle)
  userService.ts -> IOrderNotifier (interface)
  orderService.ts implements IOrderNotifier
  orderService.ts -> userService.ts (one direction only)
  
### **Symptoms**
  - Cannot access X before initialization
  - Import order matters
  - Webpack/bundler circular dependency warnings
  - Tests fail when run in different order
### **Detection Pattern**
import.*from.*\.\..*import.*from.*\.\.

## God Module Accumulation

### **Id**
god-module-accumulation
### **Summary**
One module grows to handle everything because it's "convenient"
### **Severity**
critical
### **Situation**
  A module starts small but grows to 1000+ lines because it's easier
  to add code there than to create proper structure.
  
### **Why**
  God modules become:
  - Impossible to test (too many dependencies)
  - Impossible to understand (too many responsibilities)
  - Merge conflict magnets (everyone touches them)
  - Performance problems (load everything for anything)
  
  They grow because adding code is easier than reorganizing.
  
### **Solution**
  Split by responsibility, not by size:
  1. Identify distinct responsibilities (list them)
  2. Group related functions together
  3. Extract each group to its own module
  4. Use a facade if you need backward compatibility
  
  # Before: UserManager.ts (1500 lines)
  # After:
  userAuth.ts      -> login, logout, session
  userProfile.ts   -> update, preferences
  userBilling.ts   -> subscription, invoices
  userNotify.ts    -> email, push notifications
  
### **Symptoms**
  - File over 500 lines
  - Where does this code go? Just put it in utils
  - Need to import 10 things from one module
  - Tests for module take forever to run
### **Detection Pattern**
export (function|const|class).*\n.*export.*\n.*export

## Leaky Database Abstraction

### **Id**
leaky-database-abstraction
### **Summary**
Database implementation details leak into business logic
### **Severity**
high
### **Situation**
  Business logic contains SQL queries, Prisma/Drizzle syntax,
  or database-specific concepts like transactions and locks.
  
### **Why**
  Business logic becomes tied to database choice. Changing databases
  requires rewriting business rules. Testing requires database setup.
  Business code is harder to read.
  
### **Solution**
  Create a repository layer:
  
  # Bad: Business logic with DB details
  async function getActiveUsers() {
    return prisma.user.findMany({
      where: { status: 'active', deletedAt: null }
    });
  }
  
  # Good: Repository hides DB
  interface UserRepository {
    getActive(): Promise<User[]>;
  }
  
  class PrismaUserRepository implements UserRepository {
    getActive() {
      return prisma.user.findMany({
        where: { status: 'active', deletedAt: null }
      });
    }
  }
  
  # Business logic uses interface
  async function notifyActiveUsers(repo: UserRepository) {
    const users = await repo.getActive();
    // ...
  }
  
### **Symptoms**
  - SQL in component files
  - Prisma/Drizzle imports in non-db files
  - Tests need database to run
  - We can't change databases because...
### **Detection Pattern**
prisma\.|\.findMany|\.findUnique|SELECT.*FROM

## Implicit Coupling Through Globals

### **Id**
implicit-coupling-through-globals
### **Summary**
Modules communicate through global state instead of explicit parameters
### **Severity**
high
### **Situation**
  Functions rely on global variables, singletons, or module-level state
  rather than receiving what they need as parameters.
  
### **Why**
  Hidden dependencies make code:
  - Untestable without mocking globals
  - Unpredictable (order matters)
  - Hard to parallelize
  - Impossible to reason about in isolation
  
### **Solution**
  Pass dependencies explicitly:
  
  # Bad: Global state
  let currentUser: User | null = null;
  
  function createOrder(items: Item[]) {
    if (!currentUser) throw new Error('Not logged in');
    return { userId: currentUser.id, items };
  }
  
  # Good: Explicit dependency
  function createOrder(user: User, items: Item[]) {
    return { userId: user.id, items };
  }
  
### **Symptoms**
  - Module-level `let` variables
  - Functions that "just work" without visible inputs
  - Tests failing when run in different order
  - You have to call X before Y
### **Detection Pattern**
let [a-z]+\s*[:=].*\nexport

## Wrong Layer Responsibilities

### **Id**
wrong-layer-responsibilities
### **Summary**
UI components contain business logic, or data layer contains validation
### **Severity**
high
### **Situation**
  Logic is placed in the wrong architectural layer:
  - Business rules in React components
  - Validation in database layer
  - API calls directly from UI
  
### **Why**
  Wrong placement causes:
  - Duplicate logic (same validation in UI and API)
  - Untestable business rules (need to render component)
  - Tight coupling to presentation framework
  
### **Solution**
  Put logic in the right layer:
  
  Presentation (React):
  - Display state
  - Handle user events
  - Call application layer
  
  Application (use cases):
  - Orchestrate business operations
  - Validate business rules
  - Call domain and infrastructure
  
  Domain (business logic):
  - Pure functions
  - Business rules
  - No external dependencies
  
  Infrastructure (external services):
  - Database access
  - API calls
  - File system
  
### **Symptoms**
  - Business logic in useEffect
  - Validation in database triggers
  - fetch() in components
  - Can't reuse logic in different UI
### **Detection Pattern**
useEffect.*fetch|useState.*validate

## String Typing Everywhere

### **Id**
string-typing-everywhere
### **Summary**
Using strings where enums or union types should exist
### **Severity**
medium
### **Situation**
  Status fields, type discriminators, and options passed as strings
  rather than typed enums or union types.
  
### **Why**
  Strings are:
  - Not autocomplete-friendly
  - Not typo-proof
  - Not refactor-safe
  - Not self-documenting
  
### **Solution**
  # Bad
  function setStatus(status: string) { ... }
  setStatus('actve'); // Typo, no error
  
  # Good
  type Status = 'active' | 'inactive' | 'pending';
  function setStatus(status: Status) { ... }
  setStatus('actve'); // Type error!
  
### **Symptoms**
  - Comparing strings with ===
  - Typo bugs that reach production
  - Magic strings scattered in code
### **Detection Pattern**
status.*===.*['"]|type.*===.*['"]

## Test Coupling To Implementation

### **Id**
test-coupling-to-implementation
### **Summary**
Tests break when refactoring even though behavior is unchanged
### **Severity**
medium
### **Situation**
  Tests verify implementation details rather than behavior.
  Refactoring working code breaks tests.
  
### **Why**
  Tests become a burden rather than a safety net.
  Developers avoid refactoring to avoid fixing tests.
  Test failures don't indicate real problems.
  
### **Solution**
  Test behavior, not implementation:
  
  # Bad: Tests implementation
  test('calls database with correct query', () => {
    createUser({ name: 'Test' });
    expect(prisma.user.create).toHaveBeenCalledWith({
      data: { name: 'Test' }
    });
  });
  
  # Good: Tests behavior
  test('creates user with given name', async () => {
    const user = await createUser({ name: 'Test' });
    expect(user.name).toBe('Test');
  
    const saved = await getUser(user.id);
    expect(saved.name).toBe('Test');
  });
  
### **Symptoms**
  - Tests full of mocks
  - Refactoring breaks tests
  - Tests pass but bugs exist
  - Testing private methods
### **Detection Pattern**
toHaveBeenCalledWith|mock\(

## Feature Folder Vs Type Folder

### **Id**
feature-folder-vs-type-folder
### **Summary**
Organizing by file type instead of feature
### **Severity**
medium
### **Situation**
  Code organized as components/, hooks/, utils/, api/
  instead of by feature like users/, orders/, payments/
  
### **Why**
  Type-based organization:
  - Scatters related code across folders
  - Makes it hard to find everything for a feature
  - Creates import paths across the codebase
  - Makes deleting features error-prone
  
  Feature-based keeps related code together.
  
### **Solution**
  # Bad: Type-based
  components/
    UserProfile.tsx
    OrderList.tsx
  hooks/
    useUser.ts
    useOrders.ts
  api/
    userApi.ts
    orderApi.ts
  
  # Good: Feature-based
  features/
    users/
      UserProfile.tsx
      useUser.ts
      userApi.ts
    orders/
      OrderList.tsx
      useOrders.ts
      orderApi.ts
  
### **Symptoms**
  - Imports from many directories for one feature
  - Hard to find all code for a feature
  - Deleting feature leaves orphaned files
### **Detection Pattern**
components/.*hooks/.*api/