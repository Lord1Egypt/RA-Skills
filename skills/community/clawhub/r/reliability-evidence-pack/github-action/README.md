# REP GitHub Actions Workflow

This directory contains GitHub Actions workflows for validating REP (Record of Execution Protocol) bundles.

## Workflows

### rep-validate.yml

Validates REP bundles on push and pull request events. Uses the `rep.mjs validate` command and outputs validation results as GitHub code annotations.

## Setup Instructions

To use this workflow in your repository:

1. Copy `rep-validate.yml` to `.github/workflows/` in your repository:

   ```bash
   mkdir -p .github/workflows
   cp rep-validate.yml .github/workflows/
   ```

2. Ensure `rep.mjs` is available in your repository (or update the workflow to use a path relative to your repo).

3. By default, the workflow validates:
   - All `.json` and `.jsonl` files in `artifacts/` directory
   - Any `rep-bundle.json` file in the root

4. To customize validation, edit the `VALIDATE_TARGETS` matrix in the workflow:
   
   ```yaml
   VALIDATE_TARGETS: |
     artifacts/decision_rejection_log.jsonl
     artifacts/agent_execution_log.jsonl
     rep-bundle.json
   ```

5. Enable additional validation flags in the `run` command:
   
   ```bash
   node scripts/rep.mjs validate ${{ matrix.target }} --json --require-pack --check-chain --xref
   ```

## Validation Output

The workflow outputs validation results as GitHub annotations:
- **Errors** (red): Critical validation failures
- **Warnings** (yellow): Non-critical issues
- The full JSON output is also available as a workflow artifact

## Example Validation Results

After running, you'll see annotation summaries like:
- ✅ "REP validation passed" - All checks passed
- ❌ "REP validation failed" - Check annotations for details
