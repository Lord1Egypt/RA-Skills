# Connascence Types: Detailed Examples

## Static Connascence

### Connascence of Name (CoN) - Weakest

Components must agree on the name of an entity.
```python
# If deliver() is renamed, all callers must update
class Mailer:
    def deliver(self, message):
        pass

mailer = Mailer()
mailer.deliver(message)  # Coupled to name "deliver"
```

**Impact**: Low - IDE refactoring handles this easily
**Action**: Generally acceptable; use consistent naming conventions

---

### Connascence of Type (CoT)

Components must agree on the type of an entity.
```python
# BAD: Strict type coupling
def average(values: list) -> float:
    return sum(values) / len(values)

# BETTER: Duck typing reduces to CoN
def average(values):
    """Works with any iterable supporting sum() and len()"""
    return sum(values) / len(values)
```

**Impact**: Medium - Changes require updating type annotations
**Action**: Use interfaces/protocols; prefer duck typing where appropriate

---

### Connascence of Meaning (CoM) - Magic Values

Components must agree on the meaning of specific values.
```python
# BAD: Magic number coupling
def get_user_role(user):
    if user.is_admin:
        return 0  # What does 0 mean?
    return 2

if get_user_role(user) == 0:  # Must know 0 = admin
    grant_access()

# GOOD: Named constant (reduces to CoN)
class Role:
    ADMIN = "admin"
    USER = "user"

def get_user_role(user):
    return Role.ADMIN if user.is_admin else Role.USER

if get_user_role(user) == Role.ADMIN:
    grant_access()
```

**Impact**: High - Silent bugs when meanings diverge
**Action**: Replace magic values with named constants, enums, or types

---

### Connascence of Position (CoP)

Components must agree on the order of values.
```python
# BAD: Position-dependent
def create_user(first, last, age, email, admin):
    pass

create_user("John", "Doe", 30, "john@example.com", True)
# Easy to mix up parameters

# GOOD: Named parameters or object (reduces to CoN)
@dataclass
class UserData:
    first_name: str
    last_name: str
    age: int
    email: str
    is_admin: bool

def create_user(data: UserData):
    pass

# Or use keyword arguments
create_user(first="John", last="Doe", age=30, 
            email="john@example.com", admin=True)
```

**Impact**: High - Silent bugs from parameter order mistakes
**Action**: Use named parameters, builder pattern, or parameter objects

---

### Connascence of Algorithm (CoA) - Strongest Static

Components must agree on a particular algorithm.
```python
# BAD: Algorithm duplicated
class PasswordService:
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

class AuthService:
    def verify_password(self, password, stored_hash):
        # Algorithm duplicated - must stay in sync!
        return hashlib.sha256(password.encode()).hexdigest() == stored_hash

# GOOD: Single algorithm location (reduces to CoN)
class PasswordHasher:
    @staticmethod
    def hash(value: str) -> str:
        return hashlib.sha256(value.encode()).hexdigest()

class PasswordService:
    def hash_password(self, password):
        return PasswordHasher.hash(password)

class AuthService:
    def verify_password(self, password, stored_hash):
        return PasswordHasher.hash(password) == stored_hash
```

**Impact**: Very High - Algorithm changes break dependent code
**Action**: Extract shared algorithms to single, well-tested location

---

## Dynamic Connascence

### Connascence of Execution (CoE) - Weakest Dynamic

Order of method execution matters.
```python
# BAD: Implicit order dependency
email = Email()
email.set_recipient("user@example.com")
email.set_sender("me@example.com")
email.send()
email.set_subject("Hello")  # Too late! Already sent

# GOOD: Constructor enforces required fields
email = Email(
    recipient="user@example.com",
    sender="me@example.com",
    subject="Hello"
)
email.send()

# Or use builder pattern
email = EmailBuilder()
    .recipient("user@example.com")
    .sender("me@example.com")
    .subject("Hello")
    .build()  # Validates all required fields
    .send()
```

**Impact**: High - Runtime errors from wrong order
**Action**: Use constructors, builders, or state machines to enforce order

---

### Connascence of Timing (CoTm)

Timing of execution matters.
```python
# BAD: Timing dependency
cache.write("session", data)
time.sleep(61)  # Cache expires after 60 seconds
data = cache.read("session")  # Returns None - expired!

# Common scenarios:
# - Database connection timeouts
# - Race conditions in concurrent code
# - Eventual consistency windows
```

**Impact**: Very High - Intermittent, hard-to-reproduce bugs
**Action**: Make timing explicit; use async/await, promises, locks appropriately

---

### Connascence of Value (CoV)

Multiple values must change together.
```python
# BAD: Values must stay consistent
class Rectangle:
    def __init__(self):
        self.width = 10
        self.height = 5
        self.area = 50  # Must equal width * height!
    
    def set_width(self, w):
        self.width = w
        # Forgot to update area!

# GOOD: Compute derived values
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    @property
    def area(self):
        return self.width * self.height  # Always consistent
```

**Impact**: Very High - Data inconsistency bugs
**Action**: Compute derived values; use invariant-preserving methods

---

### Connascence of Identity (CoI) - Strongest

Components must reference the same instance.
```python
# BAD: Implicit shared identity
class Publisher:
    def __init__(self):
        self.queue = Queue()
    
    def publish(self, msg):
        self.queue.put(msg)

class Subscriber:
    def __init__(self, publisher):
        self._pub = publisher
    
    def consume(self):
        return self._pub.queue.get()  # Depends on same Queue instance

# GOOD: Explicit dependency injection
class Publisher:
    def __init__(self, queue: Queue):
        self._queue = queue
    
    def publish(self, msg):
        self._queue.put(msg)

class Subscriber:
    def __init__(self, queue: Queue):
        self._queue = queue
    
    def consume(self):
        return self._queue.get()

# Wiring is explicit
shared_queue = Queue()
publisher = Publisher(shared_queue)
subscriber = Subscriber(shared_queue)
```

**Impact**: Highest - Hidden dependencies, testing nightmares
**Action**: Make identity dependencies explicit through dependency injection

---

## Connascence Strength Hierarchy

```
WEAKEST (easiest to refactor)
│
├── STATIC
│   ├── 1. Name (CoN)
│   ├── 2. Type (CoT)
│   ├── 3. Meaning (CoM)
│   ├── 4. Position (CoP)
│   └── 5. Algorithm (CoA)
│
├── DYNAMIC
│   ├── 6. Execution (CoE)
│   ├── 7. Timing (CoTm)
│   ├── 8. Value (CoV)
│   └── 9. Identity (CoI)
│
STRONGEST (hardest to refactor)
```

**Rule**: Static connascence is always weaker than dynamic because it can be detected by examining source code.