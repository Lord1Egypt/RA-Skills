# Test Case Templates

## Unit Test Template

### Go
```go
func Test<UnitName>_<Scenario>_<Expected>(t *testing.T) {
    // Arrange
    <setup code>
    
    // Act
    <action being tested>
    
    // Assert
    <verify expected outcome>
}
```

### Python
```python
def test_<unit>_<scenario>_<expected>():
    # Arrange
    <setup code>
    
    # Act
    <action being tested>
    
    # Assert
    <verify expected outcome>
```

### TypeScript
```typescript
describe('UnitName', () => {
  describe('Scenario', () => {
    it('should Expected', () => {
      // Arrange
      const <setup>
      
      // Act
      const <result> = <action>()
      
      // Assert
      expect(<result>).to<matcher>(<expected>)
    })
  })
})
```

## Integration Test Template

```
Test Case: <Name>
Preconditions: <What must be true before>
Test Steps:
  1. <Step 1>
  2. <Step 2>
  3. <Step 3>
Expected Result: <What should happen>
Cleanup: <How to clean up>
```

## E2E Test Template (Gherkin)

```gherkin
Feature: <Feature Name>

  Scenario: <Scenario description>
    Given <precondition>
    And <additional precondition>
    When <action performed>
    And <another action>
    Then <expected outcome>
    And <another expected outcome>
```

## Test Data Factory Template

```python
# Factory for test data
class UserFactory:
    @staticmethod
    def create(email: str = "test@example.com", 
               name: str = "Test User",
               **kwargs) -> User:
        return User(
            email=email,
            name=name,
            *kwargs
        )
    
    @staticmethod
    def create_batch(count: int, **kwargs) -> list[User]:
        return [UserFactory.create(**kwargs) for _ in range(count)]
```

## Property-Based Test Template (Python/pytest)

```python
from hypothesis import given, strategies as st

@given(
    name=st.text(min_size=1, max_size=100),
    email=st.email()
)
def test_user_creation_property(name, email):
    user = User(name=name, email=email)
    assert user.name == name
    assert user.email == email
```
