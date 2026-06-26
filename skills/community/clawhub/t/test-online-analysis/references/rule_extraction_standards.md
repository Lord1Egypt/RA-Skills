# Rule Extraction Standards

## Overview
This document defines the standards for extracting and documenting business rules from online data streams.

## Rule Classification

### 1. Business Rules
- **Definition:** Rules that enforce business logic and requirements
- **Examples:** Transaction limits, eligibility criteria, approval workflows
- **Confidence Level:** High (≥0.8) when extracted from multiple data points

### 2. Technical Rules
- **Definition:** Rules that enforce technical constraints and system behavior
- **Examples:** Data type constraints, format validations, API rate limits
- **Confidence Level:** Very High (≥0.9) when consistently observed

### 3. Implicit Rules
- **Definition:** Rules that are not explicitly documented but observed in practice
- **Examples:** Undocumented edge case handling, default behaviors
- **Confidence Level:** Medium (≥0.6) when pattern is consistent

## Rule Documentation Format

Each extracted rule must include:
1. **Rule ID:** Unique identifier (RULE-XXXX)
2. **Rule Type:** Business/Technical/Implicit
3. **Condition:** Clear statement of the rule condition
4. **Source:** Data source where the rule was observed
5. **Confidence:** 0.0-1.0 score indicating reliability
6. **Examples:** 1-2 concrete examples of the rule in action

## Quality Criteria

### High Confidence (≥0.8)
- Observed in ≥10 independent data points
- No counterexamples found
- Consistent across different time periods

### Medium Confidence (0.6-0.8)
- Observed in 3-10 data points
- No significant counterexamples
- Mostly consistent across scenarios

### Low Confidence (<0.6)
- Observed in <3 data points
- Potential counterexamples exist
- Pattern may be coincidental

## Validation Process

1. **Initial Extraction:** Automatic extraction from data
2. **Pattern Verification:** Check for consistency across multiple data points
3. **Counterexample Check:** Search for data points that violate the candidate rule
4. **Confidence Scoring:** Assign confidence level based on validation results
5. **Documentation:** Record rule in standard format
