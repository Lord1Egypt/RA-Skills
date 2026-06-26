# Java Best Practices Templates

This directory contains template files demonstrating Java best practices.

## Available Templates

### 1. Service Template (`service-template.java`)

**Purpose:** Template for creating Spring service classes following best practices.

**Features:**
- Single Responsibility Principle
- Constructor dependency injection
- Uses Optional instead of null
- Proper transaction management
- Clear separation of concerns
- Validation methods
- Comprehensive JavaDoc

**Usage:**
1. Copy template to your service package
2. Replace `Entity` with your actual entity name
3. Implement validation and update logic
4. Add custom business methods as needed

**Example:**
```java
@Service
public class UserService {
    private final UserRepository userRepository;

    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    // Methods follow template pattern
}
```

### 2. Test Template (`test-template.java`)

**Purpose:** Template for creating JUnit 5 unit tests with Mockito.

**Features:**
- AAA pattern (Arrange-Act-Assert)
- Descriptive test names with @DisplayName
- Nested test classes for logical grouping
- Parameterized tests for multiple inputs
- Proper use of mocks and assertions
- Test coverage for all CRUD operations

**Usage:**
1. Copy template to your test package
2. Replace `Entity` with your actual entity name
3. Add test cases specific to your business logic
4. Ensure all edge cases are covered

**Example:**
```java
@ExtendWith(MockitoExtension.class)
@DisplayName("User Service Tests")
class UserServiceTest {
    @Mock
    private UserRepository userRepository;

    @InjectMocks
    private UserService userService;

    // Test methods follow template pattern
}
```

### 3. Builder Pattern Template (`builder-pattern.java`)

**Purpose:** Complete implementation of Builder Pattern for complex objects.

**Features:**
- Immutable object creation
- Required vs optional fields
- Fluent API with method chaining
- Validation in build() method
- Clear separation of concerns
- Comprehensive JavaDoc

**Usage:**
1. Copy template to your model package
2. Replace `User` with your actual class name
3. Add/remove fields as needed
4. Mark required vs optional fields
5. Implement validation logic

**Example:**
```java
User user = User.builder()
    .email("john@example.com")
    .firstName("John")
    .lastName("Doe")
    .phoneNumber("555-1234")
    .build();
```

## Best Practices Demonstrated

All templates demonstrate these key principles:

1. **SOLID Principles**
   - Single Responsibility
   - Dependency Inversion
   - Interface Segregation

2. **Clean Code**
   - Meaningful names
   - Small, focused methods
   - Proper comments
   - Clear structure

3. **Java-Specific**
   - Optional over null
   - Immutability with final
   - Constructor injection
   - Try-with-resources (where applicable)

4. **Testing**
   - AAA pattern
   - Proper mocking
   - Descriptive names
   - Edge case coverage

## Integration with uncle-duke-java

These templates are referenced by the `uncle-duke-java` agent during code reviews. When reviewing code, Uncle Duke will compare implementations against these templates and suggest improvements.

## Customization

Feel free to customize these templates for your project's specific needs:
- Add project-specific validation
- Include custom annotations
- Adjust naming conventions
- Add logging patterns
- Include security considerations

## Additional Resources

See the main SKILL.md file for comprehensive Java best practices covering:
- SOLID principles
- DRY principle
- Clean Code
- Exception handling
- Collections and generics
- Concurrency
- Performance optimization
- Common anti-patterns
