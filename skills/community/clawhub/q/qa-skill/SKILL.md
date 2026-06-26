---
name: qa-skill
description: Generate comprehensive test cases and quality assurance documentation from SwiftUI iOS code. Use when iOS application code is available and needs testing strategies, test cases, and quality validation. This skill receives input from dev-skill and completes the auto-dev-pipeline by providing testing coverage.
---

# QA Skill - Quality Assurance Test Generator

## Overview

This skill analyzes SwiftUI iOS application code and generates comprehensive test cases, testing strategies, and quality assurance documentation. It ensures code quality, identifies potential issues, and provides testing coverage for the entire application.

## Testing Strategy

### 1. Test Pyramid Approach
- **Unit Tests (70%)**: Test individual components and business logic
- **Integration Tests (20%)**: Test component interactions and data flow
- **UI Tests (10%)**: Test user interface and user flows

### 2. Test Categories

#### 2.1 Functional Testing
- Feature validation against PRD requirements
- User story acceptance criteria
- Edge cases and boundary conditions

#### 2.2 Non-Functional Testing
- Performance testing (load time, memory usage)
- Security testing (data protection, authentication)
- Accessibility testing (VoiceOver, Dynamic Type)
- Compatibility testing (iOS versions, device sizes)

#### 2.3 Regression Testing
- Ensure new changes don't break existing functionality
- Automated test suite for critical paths
- Smoke tests for release validation

## Test Generation Workflow

### 1. Code Analysis
- Parse SwiftUI project structure
- Identify ViewModels and business logic
- Map data flows and dependencies
- Analyze PRD requirements for test coverage

### 2. Test Case Generation

#### 2.1 Unit Test Templates
```swift
import XCTest
@testable import ProjectName

class TaskViewModelTests: XCTestCase {
    var viewModel: TaskViewModel!
    var mockDataService: MockDataService!
    
    override func setUp() {
        super.setUp()
        mockDataService = MockDataService()
        viewModel = TaskViewModel(dataService: mockDataService)
    }
    
    func testAddTask() {
        // Given
        let initialCount = viewModel.tasks.count
        let newTask = Task(title: "Test Task")
        
        // When
        viewModel.addTask(newTask)
        
        // Then
        XCTAssertEqual(viewModel.tasks.count, initialCount + 1)
        XCTAssertEqual(viewModel.tasks.last?.title, "Test Task")
    }
    
    func testDeleteTask() { ... }
    func testToggleCompletion() { ... }
    func testFilterByCategory() { ... }
}
```

#### 2.2 UI Test Templates
```swift
import XCTest

class ProjectNameUITests: XCTestCase {
    var app: XCUIApplication!
    
    override func setUp() {
        super.setUp()
        app = XCUIApplication()
        app.launch()
    }
    
    func testTaskCreationFlow() {
        // Given: App is launched
        XCTAssertTrue(app.navigationBars["Tasks"].exists)
        
        // When: Tap add button
        app.buttons["Add"].tap()
        
        // Then: Add task screen appears
        XCTAssertTrue(app.textFields["Task Title"].exists)
        
        // When: Enter task details and save
        app.textFields["Task Title"].tap()
        app.textFields["Task Title"].typeText("Test UI Task")
        app.buttons["Save"].tap()
        
        // Then: Task appears in list
        XCTAssertTrue(app.staticTexts["Test UI Task"].exists)
    }
    
    func testTaskCompletion() { ... }
    func testCategoryFiltering() { ... }
    func testReminderSettings() { ... }
}
```

#### 2.3 Integration Test Templates
```swift
class DataServiceIntegrationTests: XCTestCase {
    func testDataPersistence() {
        // Given: Fresh data service
        let dataService = DataService()
        
        // When: Save data
        let task = Task(title: "Integration Test")
        dataService.saveTask(task)
        
        // Then: Data should be retrievable
        let retrieved = dataService.loadTasks()
        XCTAssertEqual(retrieved.count, 1)
        XCTAssertEqual(retrieved.first?.title, "Integration Test")
    }
}
```

### 3. Test Documentation Generation

#### 3.1 Test Plan Document
```
# Test Plan: [App Name]

## 1. Testing Scope
- Features to be tested
- Features out of scope
- Testing environments

## 2. Test Strategy
- Testing types and approaches
- Test data requirements
- Entry/exit criteria

## 3. Test Cases
### 3.1 Functional Tests
- [TC-001] Task Creation
  - Preconditions: App launched, no tasks
  - Steps: Tap + → Enter title → Tap Save
  - Expected: Task appears in list
  - Priority: P0

### 3.2 Non-Functional Tests
- [TC-101] Performance: App launch < 2 seconds
- [TC-102] Memory: < 100MB peak usage
- [TC-103] Accessibility: VoiceOver compatible
```

#### 3.2 Test Report Template
```
# Test Report: [App Name] v1.0

## Executive Summary
- Total test cases: XX
- Passed: XX
- Failed: XX
- Blocked: XX
- Test coverage: XX%

## Detailed Results
### Functional Testing
- Feature A: 10/10 passed
- Feature B: 8/10 passed (2 failed)
- Feature C: 5/5 passed

### Issues Found
1. **High Priority**: Crash when deleting last task
2. **Medium Priority**: UI misalignment on iPhone SE
3. **Low Priority**: Typo in settings screen

## Recommendations
- Fix high priority issues before release
- Address medium priority in next sprint
- Document low priority for future
```

## Example: Todo App Testing

**Code Input:** SwiftUI todo app with categories and reminders

**Generated Test Coverage:**

### Unit Tests (15 test cases)
1. `TaskViewModelTests`: Add/delete/toggle tasks
2. `CategoryViewModelTests`: Filter by category
3. `ReminderServiceTests`: Schedule/cancel reminders
4. `DataServiceTests`: CRUD operations

### UI Tests (8 test cases)
1. `testTaskCreationFlow`: Complete user journey
2. `testCategoryManagement`: Add/edit/delete categories
3. `testReminderSetup`: Configure and test reminders
4. `testSharingFunctionality`: Share tasks via share sheet

### Integration Tests (5 test cases)
1. `testDataPersistence`: Verify data survives app restart
2. `testNotificationIntegration`: Test reminder delivery
3. `testICloudSync`: Verify cross-device synchronization

## Auto-Trigger Completion

After generating test cases, this skill automatically:
1. Creates test files in `qa-output/` directory
2. Generates test execution report
3. Provides quality metrics and recommendations
4. Completes the auto-dev-pipeline with final summary

## Quality Metrics

### Code Coverage Targets
- **Minimum**: 70% line coverage
- **Good**: 80% line coverage  
- **Excellent**: 90% line coverage

### Performance Benchmarks
- App launch: < 2 seconds
- Screen transitions: < 0.5 seconds
- Memory usage: < 150MB peak
- Battery impact: < 5% per hour

### Accessibility Compliance
- VoiceOver: All interactive elements labeled
- Dynamic Type: Supports all text sizes
- Color contrast: WCAG AA compliant
- Reduced motion: Respects user preferences

## Integration with Pipeline

### Input Requirements
- SwiftUI project from `dev-skill`
- PRD document for requirement validation
- Compilation verification

### Output Delivery
- Complete XCTest test suite
- Test plan and strategy document
- Quality assessment report
- Release readiness checklist