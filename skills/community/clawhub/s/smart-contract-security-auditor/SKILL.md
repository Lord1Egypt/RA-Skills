---
name: smart-contract-security-auditor
description: "Smart Contract Security Auditor: Analyzes Solidity and Go smart contracts for security vulnerabilities, provides gas optimization suggestions, and generates corresponding test cases (Foundry or Go tests)."
---

# smart-contract-security-auditor

A skill designed to enhance smart contract security, optimize gas costs, and ensure thorough test coverage for Solidity and Golang (Cosmos/Hyperledger) projects.

## Workflows

### 1. Security Static Analysis
When you finish writing or modifying a smart contract, trigger this skill to analyze the code for common vulnerabilities.
- For Solidity, it checks for reentrancy, overflow, access control issues, and more.
- For Go, it checks for determinism issues and state access control.

**How to trigger**: "Audit this contract: [file_path]" or "Check my changes in [file_path] for security vulnerabilities."

### 2. Gas & Performance Optimization
Use this workflow to get suggestions on reducing EVM Gas costs or optimizing state read/write operations in Cosmos/Hyperledger.

**How to trigger**: "Optimize gas for [file_path]" or "Suggest performance improvements for [file_path]."

### 3. Automatic Test Generation
Whenever contract logic changes, this skill can automatically generate or update the corresponding tests.
- **Solidity**: Generates Foundry tests (`.t.sol`).
- **Go**: Generates Go tests using the `testing` package (`_test.go`).

**How to trigger**: "Generate tests for [file_path]" or "Write a Foundry test script for my new logic."

## Reference Materials
When performing tasks, reference the following documents to ensure standard compliance:
- [Vulnerabilities](references/vulnerabilities.md): Known issues to look for during an audit.
- [Gas Optimization](references/gas_optimization.md): Strategies to reduce on-chain costs.
- [Testing Strategies](references/testing.md): Templates and principles for writing tests.

## Usage Guidelines
- **Be Explicit**: If you want both an audit and test generation, ask for both (e.g., "Audit this file and write tests for it").
- **Review Findings**: The auditor will present findings and suggestions. Review them before requesting code changes.
- **Test Context**: When generating tests for Go, ensure you provide context on the specific framework (Cosmos SDK vs. Hyperledger Fabric) if it's not obvious from the code.
