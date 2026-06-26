# Test Strategies (Test Design Techniques)

Techniques applicable when designing unit tests. Boundary value testing alone is insufficient; combining multiple techniques is necessary to increase reliability.

## Technique Guide

### 1. Boundary Value Analysis

Detects errors occurring at the edges (minimum, maximum, boundary) of input conditions. **The most efficient technique for defect detection.**

```
Test points: minimum, minimum+1, normal value (middle), maximum-1, maximum
```

```typescript
// Example: 0-100 score input
it('boundary values for score', () => {
  expect(validateScore(-1)).toBe(false)  // below minimum
  expect(validateScore(0)).toBe(true)    // minimum
  expect(validateScore(1)).toBe(true)    // minimum+1
  expect(validateScore(50)).toBe(true)   // middle value
  expect(validateScore(99)).toBe(true)   // maximum-1
  expect(validateScore(100)).toBe(true)  // maximum
  expect(validateScore(101)).toBe(false) // above maximum
})
```

**Limitation**: Cannot catch logical errors within the normal range outside boundaries.

---

### 2. Equivalence Partitioning

Divides input data into groups that are processed identically and tests only one representative value per group.

```
Test at least 1 valid partition + 1 invalid partition
```

```typescript
// Example: age input (0-17: minor, 18-64: adult, 65+: senior)
it('equivalence partitions for age', () => {
  expect(getAgeGroup(10)).toBe('minor')   // minor partition representative
  expect(getAgeGroup(30)).toBe('adult')   // adult partition representative
  expect(getAgeGroup(70)).toBe('senior')  // senior partition representative
  expect(getAgeGroup(-1)).toThrow()       // invalid partition
})
```

---

### 3. Decision Table

Validates business logic where multiple conditions are intertwined. Prevents omission of condition combinations.

```
N conditions → maximum 2^N combinations → select representative cases
```

```typescript
// Example: discount application (membership × purchase amount)
// | Member | Amount>=100K | Discount |
// |   O    |      O       |   20%    |
// |   O    |      X       |   10%    |
// |   X    |      O       |    5%    |
// |   X    |      X       |    0%    |
it('decision table for discount', () => {
  expect(getDiscount(true, 100000)).toBe(0.20)
  expect(getDiscount(true, 50000)).toBe(0.10)
  expect(getDiscount(false, 100000)).toBe(0.05)
  expect(getDiscount(false, 50000)).toBe(0.00)
})
```

---

### 4. Error Guessing

Experience-based inspection of specific cases where developers are likely to make mistakes.

```typescript
it('error guessing: edge cases', () => {
  // null / undefined
  expect(() => process(null)).toThrow()
  expect(() => process(undefined)).toThrow()

  // empty string / whitespace
  expect(trim('')).toBe('')
  expect(trim('  ')).toBe('')

  // special characters
  expect(sanitize('<script>alert(1)</script>')).not.toContain('<script>')

  // very large numbers
  expect(add(Number.MAX_SAFE_INTEGER, 1)).toBeDefined()

  // negative numbers
  expect(sqrt(-1)).toBeNaN()
})
```

---

### 5. Path Coverage

Verifies that all conditionals and loops in the code are executed at least once. Used in conjunction with coverage tools.

```typescript
// Example: conditional coverage check
function classify(n: number) {
  if (n > 0) return 'positive'      // branch 1
  else if (n < 0) return 'negative' // branch 2
  else return 'zero'                 // branch 3
}

it('path coverage for classify', () => {
  expect(classify(1)).toBe('positive')   // branch 1
  expect(classify(-1)).toBe('negative')  // branch 2
  expect(classify(0)).toBe('zero')       // branch 3
})
```

**Tools**: Istanbul/nyc (JS), pytest-cov (Python), JaCoCo (Java)

---

## Technique Selection Guide

| Situation | Recommended Technique |
|------|-----------|
| Numeric range validation | Boundary Value Analysis |
| Category classification logic | Equivalence Partitioning |
| Complex business rules | Decision Table |
| Input validation / defensive code | Error Guessing |
| Achieving code coverage goals | Path Coverage |
| Overall reliability assurance | **Combine all techniques** |

## Priority

```
Boundary Value Analysis (highest priority) → Equivalence Partitioning → Error Guessing → Path Coverage → Decision Table
```

Boundary values alone are not sufficient. The more complex the logic, the more techniques need to be combined.
