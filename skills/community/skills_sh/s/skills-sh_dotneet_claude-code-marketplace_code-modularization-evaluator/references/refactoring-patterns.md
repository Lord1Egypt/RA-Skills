# Refactoring Patterns for Coupling Reduction

## Pattern: Extract Contract

**When**: High model coupling between services
```python
# BEFORE: Services share domain model
# Service A
class Order:
    customer: Customer
    items: List[OrderItem]
    internal_status: str  # Internal detail

# Service B imports and uses Order directly

# AFTER: Contract coupling via DTO
# Shared contract
@dataclass
class OrderDTO:
    customer_id: str
    item_ids: List[str]
    status: str

# Service A
class OrderService:
    def get_order(self, id) -> OrderDTO:
        order = self._repository.find(id)
        return OrderDTO(
            customer_id=order.customer.id,
            item_ids=[i.id for i in order.items],
            status=self._map_status(order.internal_status)
        )
```

## Pattern: Introduce Facade

**When**: High efferent coupling from orchestration
```python
# BEFORE: Client couples to many subsystems
client.subsystem_a.operation1()
client.subsystem_b.operation2()
client.subsystem_c.operation3()

# AFTER: Single facade reduces coupling
class Facade:
    def unified_operation(self):
        self._a.operation1()
        self._b.operation2()
        self._c.operation3()

client.facade.unified_operation()
```

## Pattern: Replace Inheritance with Composition

**When**: Inheritance creates tight coupling
```python
# BEFORE: Inheritance coupling
class Animal:
    def move(self): pass

class Bird(Animal):
    def move(self):
        self.fly()

class Penguin(Bird):  # Problem: penguins can't fly!
    def move(self):
        self.swim()  # Breaks Liskov Substitution

# AFTER: Composition
class Animal:
    def __init__(self, movement_strategy):
        self._movement = movement_strategy
    
    def move(self):
        self._movement.move()

penguin = Animal(SwimmingStrategy())
eagle = Animal(FlyingStrategy())
```

## Pattern: Dependency Injection

**When**: Content/common coupling via direct instantiation
```python
# BEFORE: Hardcoded dependency
class OrderProcessor:
    def __init__(self):
        self._repository = MySQLRepository()  # Tight coupling
    
    def process(self, order):
        self._repository.save(order)

# AFTER: Injected dependency
class OrderProcessor:
    def __init__(self, repository: Repository):
        self._repository = repository
    
    def process(self, order):
        self._repository.save(order)

# Wiring
processor = OrderProcessor(MySQLRepository())
# Or for testing
test_processor = OrderProcessor(InMemoryRepository())
```

## Pattern: Event-Driven Decoupling

**When**: Functional coupling requiring synchronous communication
```python
# BEFORE: Direct coupling
class OrderService:
    def __init__(self, inventory_service, notification_service):
        self._inventory = inventory_service
        self._notifications = notification_service
    
    def place_order(self, order):
        self._inventory.reserve(order.items)  # Sync call
        self._notifications.send(order.customer)  # Sync call

# AFTER: Event-driven
class OrderService:
    def __init__(self, event_bus):
        self._events = event_bus
    
    def place_order(self, order):
        self._events.publish(OrderPlaced(order))
        # Inventory and Notification services subscribe independently
```
