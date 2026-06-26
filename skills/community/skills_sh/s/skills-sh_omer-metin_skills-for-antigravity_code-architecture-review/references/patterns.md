# Code Architecture Review

## Patterns


---
  #### **Name**
Dependency Injection
  #### **Description**
    Make dependencies explicit by passing them in rather than importing
    globals. This makes code testable and swappable.
    
  #### **Example**
    # Good: Dependencies are explicit
    class UserService {
      constructor(
        private db: Database,
        private emailService: EmailService
      ) {}
    }
    
    # Bad: Hidden dependencies via imports
    import { db } from '../lib/database';
    class UserService {
      // db is hidden - can't test, can't swap
    }
    
  #### **When**
Any class or module that uses external services

---
  #### **Name**
Layered Architecture
  #### **Description**
    Organize code into layers where each layer only depends on the layer
    below. Keeps business logic pure and testable.
    
  #### **Example**
    # Layer structure
    domain/        → Pure business logic, no external deps
    application/   → Use cases, orchestrates domain
    infrastructure/→ External services (DB, APIs)
    presentation/  → UI/API, calls application layer
    
    # Rule: Domain knows nothing about infrastructure
    # Application can use domain and infrastructure
    # Presentation only calls application
    
  #### **When**
Any project beyond a simple script

---
  #### **Name**
Interface Segregation
  #### **Description**
    Create focused interfaces that expose only what clients need.
    Don't force implementers to provide unused methods.
    
  #### **Example**
    # Good: Focused interfaces
    interface Readable { read(): Data }
    interface Writable { write(data: Data): void }
    
    # Bad: God interface
    interface Storage {
      read(): Data
      write(data: Data): void
      delete(id: string): void
      list(): Data[]
      watch(cb): void
      sync(): void
      # ... 10 more methods
    }
    
  #### **When**
Defining contracts between modules

---
  #### **Name**
Single Responsibility
  #### **Description**
    Each module should have exactly one reason to change.
    If a module changes for multiple unrelated reasons, split it.
    
  #### **Example**
    # Good: Separate responsibilities
    UserAuthService    → handles login/logout
    UserProfileService → handles profile updates
    UserBillingService → handles payments
    
    # Bad: God module
    UserService → auth + profile + billing + notifications + ...
    
  #### **When**
Module has methods that don't relate to each other

---
  #### **Name**
Explicit Over Implicit
  #### **Description**
    Make relationships and state visible in the code structure.
    Hidden dependencies and magic behavior create maintenance nightmares.
    
  #### **Example**
    # Good: Explicit dependency
    const order = await createOrder(user, items, paymentService);
    
    # Bad: Hidden global state
    setCurrentUser(user);
    setCart(items);
    const order = await createOrder(); // Uses globals somehow
    
  #### **When**
Any function that interacts with external state

## Anti-Patterns


---
  #### **Name**
God Module
  #### **Description**
One module that does everything
  #### **Why**
    Becomes impossible to change - every feature touches it.
    Testing requires mocking everything. New team members can't understand it.
    
  #### **Instead**
    Split by responsibility. Each module should be describable in one sentence.
    If you need "and" to describe it, split it.
    

---
  #### **Name**
Circular Dependencies
  #### **Description**
A depends on B depends on C depends on A
  #### **Why**
    Can't load modules cleanly. Can't test in isolation. Can't reason about
    the system. Changes propagate unpredictably.
    
  #### **Instead**
    Extract shared logic into a new module that both depend on.
    Or introduce an interface to break the cycle.
    

---
  #### **Name**
Leaky Abstraction
  #### **Description**
Internal implementation details exposed to callers
  #### **Why**
    Callers become dependent on implementation. Can't change internals
    without breaking callers. Abstraction provides no value.
    
  #### **Instead**
    Hide implementation behind a stable interface. Only expose what callers
    actually need to use.
    

---
  #### **Name**
Shotgun Surgery
  #### **Description**
One logical change requires editing many files
  #### **Why**
    Related code is scattered. Easy to miss a spot. High risk of bugs.
    Simple changes become complex projects.
    
  #### **Instead**
    Group related code together. If things change together, they belong together.
    

---
  #### **Name**
Premature Abstraction
  #### **Description**
Creating interfaces "for flexibility" with only one implementation
  #### **Why**
    Over-engineering. Extra complexity with no benefit. Often the wrong
    abstraction because you don't know the requirements yet.
    
  #### **Instead**
    Wait until you have 2+ implementations or clear testing needs.
    Extract abstractions when patterns emerge, not upfront.
    

---
  #### **Name**
Utils/Helpers Dumping Ground
  #### **Description**
File called utils.ts or helpers.ts with unrelated functions
  #### **Why**
    Becomes a junk drawer. No cohesion. Grows without bounds.
    Hard to find what you need. Hard to know where to put new code.
    
  #### **Instead**
    Name files by what they do, not that they're "utilities".
    formatDate.ts, validateEmail.ts, parseConfig.ts
    