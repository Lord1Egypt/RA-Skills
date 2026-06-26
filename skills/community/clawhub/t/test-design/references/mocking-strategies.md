# Mocking Strategies

## When to Mock

### Good Reasons to Mock
- External API calls (slow, unreliable, expensive)
- Database operations (isolation, speed)
- Time-dependent logic (freeze time)
- Non-deterministic systems

### Bad Reasons to Mock
- Too lazy to set up real dependency
- Speed over correctness
- Hiding a design problem

## Test Doubles

| Type | What it does | Use When |
|------|--------------|----------|
| **Dummy** | Passes values, never used | Fill parameter lists |
| **Fake** | Works implementation (simplified) | Real is too slow/complex |
| **Stub** | Provides canned responses | Need specific data |
| **Spy** | Records how it was called | Verify interactions |
| **Mock** | Pre-programmed with expectations | Verify behavior + interactions |

## Go Mocking

### Interface-based Mocking

```go
// Define interface
type UserRepo interface {
    FindByID(id int) (*User, error)
    Create(user *User) error
}

// Use in service
type UserService struct {
    repo UserRepo
}

// Test with mock
type mockUserRepo struct {
    findByIDCalled bool
    findByIDID     int
    findByIDResult *User
    findByIDError  error
}

func (m *mockUserRepo) FindByID(id int) (*User, error) {
    m.findByIDCalled = true
    m.findByIDID = id
    return m.findByIDResult, m.findByIDError
}

func TestUserService_Get(t *testing.T) {
    mock := &mockUserRepo{
        findByIDResult: &User{Name: "Test"},
    }
    svc := NewUserService(mock)
    
    user, err := svc.Get(1)
    
    if err != nil {
        t.Fatal(err)
    }
    if !mock.findByIDCalled {
        t.Error("expected FindByID to be called")
    }
    if user.Name != "Test" {
        t.Errorf("expected name Test, got %s", user.Name)
    }
}
```

### Using testify/mock

```go
import "github.com/stretchr/testify/mock"

type MockDB struct {
    mock.Mock
}

func (m *MockDB) FindUser(id int) (*User, error) {
    args := m.Called(id)
    return args.Get(0).(*User), args.Error(1)
}

func TestWithTestify(t *testing.T) {
    mockDB := new(MockDB)
    
    mockDB.On("FindUser", 1).Return(&User{Name: "Test"}, nil)
    
    svc := NewUserService(mockDB)
    user, _ := svc.Get(1)
    
    mockDB.AssertExpectations(t)
    assert.Equal(t, "Test", user.Name)
}
```

## Python Mocking

### Using unittest.mock

```python
from unittest.mock import Mock, patch, MagicMock

def test_with_mock():
    mock_repo = Mock()
    mock_repo.find_by_id.return_value = User(name="Test")
    
    svc = UserService(mock_repo)
    user = svc.get(1)
    
    mock_repo.find_by_id.assert_called_once_with(1)
    assert user.name == "Test"

def test_with_patch():
    with patch('app.external_api.Client') as mock_client:
        mock_client.return_value.get_user.return_value = {"name": "Test"}
        # ... test code
```

### Using pytest-mock

```python
def test_with_fixture(mocker):
    mock_repo = mocker.Mock()
    mock_repo.find_by_id.return_value = User(name="Test")
    
    svc = UserService(mock_repo)
    user = svc.get(1)
    
    assert user.name == "Test"
    mock_repo.find_by_id.assert_called_once()
```

## TypeScript Mocking

### Using jest.fn()

```typescript
const mockRepo = {
  findById: jest.fn(),
  create: jest.fn(),
};

mockRepo.findById.mockResolvedValue({ id: 1, name: 'Test' });

const svc = new UserService(mockRepo);
const user = await svc.get(1);

expect(mockRepo.findById).toHaveBeenCalledWith(1);
expect(user.name).toBe('Test');
```

### Using jest.spyOn()

```typescript
const db = require('./db');
jest.spyOn(db, 'findUser').mockResolvedValue({ id: 1, name: 'Test' });
```

## Best Practices

1. **Mock interfaces, not concrete classes** — Allows implementation changes
2. **Don't mock what you don't own** — Could create false confidence
3. **Verify interactions, not just return values** — Ensures correct usage
4. **Reset mocks between tests** — Prevents test pollution
5. **Use specific assertions** — `assert_called_once_with()` not just `assert_called()`

## Anti-Patterns

### Over-mocking
```python
# Bad: Mocking everything
mock_db = Mock()
mock_cache = Mock()
mock_logger = Mock()
mock_config = Mock()
```
Better: Use real objects when they don't complicate tests

### Brittle mocks
```python
# Bad: Too specific
mock.method.assert_called_with("arg1", 2, True, something_else)

# Better: What matters
mock.method.assert_called()
```

### Mocking private methods
Don't mock internal implementation details. Test behavior, not implementation.
