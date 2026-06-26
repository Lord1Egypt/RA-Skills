# Complexity Standards

## Complexity Classification

### Simple Features (0.20-0.30 person-days for design)

**Definition:**
- Single function, clear logic
- Few operation steps, simple data preparation
- Minimal dependencies

**Characteristics:**
- Straightforward user flow
- No complex business rules
- Easy to prepare test data
- Limited edge cases

**Examples:**
- List display and navigation
- Simple click and jump actions
- Basic data display
- Simple form submission
- Status display (online/offline)

**Estimation:**
- Case Design: 0.20-0.30 person-days
- First Run: 0.15-0.20 person-days
- Retest: 40%-67% of first run (minimum 0.10)
- Regression: 50%-67% of first run

### Medium Features (0.35-0.40 person-days for design)

**Definition:**
- Multiple sub-functions, moderate complexity
- Requires test data preparation
- Some dependencies and interactions

**Characteristics:**
- Multiple user workflows
- Moderate business logic
- Requires specific test scenarios
- Some edge cases to consider

**Examples:**
- Data filtering and sorting
- User management (CRUD)
- Device binding (single mode)
- OTA upgrade (single device)
- Device details with multiple tabs
- Time-based filtering
- Permission configuration

**Estimation:**
- Case Design: 0.35-0.40 person-days
- First Run: 0.25-0.30 person-days
- Retest: 33%-40% of first run
- Regression: 48%-50% of first run

### Complex Features (0.50 person-days for design)

**Definition:**
- Complex business logic, multiple interaction paths
- Requires diverse test data, strong dependencies
- Multiple systems or complex state management

**Characteristics:**
- Multiple interaction modes
- Complex state transitions
- Requires extensive test data
- Many edge cases and exceptions
- Strong system dependencies

**Examples:**
- Online/offline binding with pre-binding
- Batch operations
- Complex permission combinations
- Multi-step workflows with waiting states
- Cross-system integrations
- Complex data synchronization

**Estimation:**
- Case Design: 0.50 person-days
- First Run: 0.30-0.40 person-days
- Retest: 33%-38% of first run
- Regression: 50% of first run

## Time Calculation Rules

### Rounding Rules
- All time values must be rounded to two decimals
- Use standard rounding (round half up)
- Minimum value is 0.10 person-days

### Constraint Rules
- Total estimation error should be within 0.5 person-days of actual values
- All time values must be >= 0.10 person-days
- Sum of all estimates should match expected totals

### Quality Checks
- Simple features should not exceed 0.30 person-days for design
- Complex features should be at least 0.50 person-days for design
- Medium features should fall between 0.35-0.40 person-days for design
- Retest and regression times should be proportional to first run
