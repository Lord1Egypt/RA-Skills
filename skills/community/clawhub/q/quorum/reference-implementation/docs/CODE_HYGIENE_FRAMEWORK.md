# Code Hygiene Framework

This document outlines the code hygiene framework used by Quorum's evaluation system. The framework is grounded in established Python Enhancement Proposals (PEPs) and community best practices.

## Framework Principles

Our code quality evaluation is based on authoritative Python standards:

### Core Standards

- **PEP 8** - Style Guide for Python Code: Defines naming conventions, formatting, import organization, and code layout standards
- **PEP 20** - The Zen of Python: Fundamental design principles including "Simple is better than complex", "Readability counts", and "Errors should never pass silently"
- **PEP 257** - Docstring Conventions: Standards for documentation strings in Python code
- **PEP 484** - Type Hints: Introduction of type annotations for better code clarity and tooling support
- **PEP 526** - Variable Annotations: Syntax for type hints on variables
- **PEP 3107** - Function Annotations: Original function annotation syntax
- **PEP 585** - Type Hinting Generics in Standard Collections: Modern generic type syntax

## Rubric Categories

### 1. Correctness
Ensures code behaves as intended without logic errors or runtime failures.
- Grounded in PEP 20: "Errors should never pass silently"
- Includes type consistency validation per PEP 484/526

### 2. Design Quality
Evaluates architectural decisions and code organization.
- Based on PEP 20 principles of simplicity and clarity
- Single Responsibility Principle alignment
- Appropriate abstraction levels

### 3. Documentation
Assesses code readability and documentation quality.
- PEP 257 docstring standards
- PEP 8 naming conventions
- Clear, unambiguous variable and function names

### 4. Security
Identifies security vulnerabilities and unsafe patterns.
- Input validation requirements
- Safe handling of user data
- Avoidance of code injection vectors

### 5. Resilience
Ensures robust error handling and resource management.
- Proper exception handling scope
- Resource lifecycle management
- Graceful degradation patterns

### 6. Concurrency
Addresses async/await patterns and thread safety.
- Event loop best practices
- Synchronization requirements
- Cancellation handling

### 7. AI/Agent-Specific
Modern considerations for AI-integrated code.
- LLM API response validation
- Prompt injection prevention
- Token budget controls

## PEP Citation Guidelines

When evaluating code against these criteria, citations to relevant PEPs provide:
- Authoritative backing for evaluation decisions
- Specific sections for detailed guidance
- Community consensus on best practices
- Historical context for design decisions

## Usage in Rubrics

The Python code quality rubric (`quorum/rubrics/builtin/python-code.json`) implements these framework principles with specific PEP citations in the rationale field (`why`) for each criterion. This grounds our evaluation in established Python community standards rather than arbitrary preferences.