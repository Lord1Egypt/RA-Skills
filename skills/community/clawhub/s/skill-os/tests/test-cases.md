# Test Case Library

> Ready-to-use test cases for validating skills.

---

## Test Case 1: Basic Functionality

```
ID: TC-001
NAME: Basic Task Execution
PURPOSE: Verify skill handles standard task

INPUT:
→ "[Standard task request]"

EXPECTED:
→ Skill activates correctly
→ Output is relevant and complete
→ Quality meets minimum standard

PASS CRITERIA:
→ Output addresses the request
→ No errors or crashes
→ Format is correct
```

## Test Case 2: Edge Case Handling

```
ID: TC-002
NAME: Empty Input Handling
PURPOSE: Verify skill handles empty/missing input

INPUT:
→ "" (empty string)
→ " " (whitespace only)
→ null/undefined

EXPECTED:
→ Skill asks for clarification
→ Skill doesn't crash
→ Skill provides helpful guidance

PASS CRITERIA:
→ Graceful handling
→ Clear error message
→ No hallucination
```

## Test Case 3: Ambiguity Resolution

```
ID: TC-003
NAME: Vague Request Handling
PURPOSE: Verify skill handles ambiguous requests

INPUT:
→ "Help me with this"
→ "Make it better"
→ "Do something"

EXPECTED:
→ Skill asks clarifying questions
→ Skill makes reasonable assumptions
→ Skill states assumptions explicitly

PASS CRITERIA:
→ No wild guesses
→ Clear communication
→ User guided to specificity
```

## Test Case 4: Multi-Turn Context

```
ID: TC-004
NAME: Context Preservation
PURPOSE: Verify skill remembers context across turns

INPUT:
→ Turn 1: "I need help with X"
→ Turn 2: "What about Y?"
→ Turn 3: "Can you combine them?"

EXPECTED:
→ Skill remembers X from turn 1
→ Skill connects X and Y
→ Skill produces combined output

PASS CRITERIA:
→ Context preserved
→ Connections made
→ Coherent output
```

## Test Case 5: Quality Threshold

```
ID: TC-005
NAME: Output Quality Verification
PURPOSE: Verify output meets quality standards

INPUT:
→ "[Task that should produce high-quality output]"

EXPECTED:
→ Output is accurate
→ Output is complete
→ Output is clear
→ Output is actionable

PASS CRITERIA:
→ 10-dimension score >= 85
→ No critical errors
→ User would be satisfied
```
