---
name: terraform-module-linter
description: Lint Terraform modules and configurations (.tf files) for structure, naming, security, and best practices. 24 rules across structure, naming, security, and best practices categories. Supports HCL syntax parsing.
---

# Terraform Module Linter

Lint Terraform `.tf` files and modules for structure, naming conventions, security issues, and best practices.

## Commands

```bash
# Lint a Terraform directory (all rules)
python3 scripts/terraform_module_linter.py lint path/to/module/

# Check security issues only
python3 scripts/terraform_module_linter.py security path/to/module/

# Check naming conventions
python3 scripts/terraform_module_linter.py naming path/to/module/

# Validate module structure
python3 scripts/terraform_module_linter.py validate path/to/module/

# Lint a single file
python3 scripts/terraform_module_linter.py lint path/to/main.tf

# JSON output
python3 scripts/terraform_module_linter.py lint path/to/module/ --format json

# Summary only
python3 scripts/terraform_module_linter.py lint path/to/module/ --format summary
```

## Rules (24)

### Structure (6)
- Missing main.tf, variables.tf, or outputs.tf
- Missing terraform block with required_version
- Missing required_providers block
- Empty variable/output blocks
- Unused variables (declared but not referenced)
- Missing variable descriptions

### Naming (6)
- Resource names must be snake_case
- Variable names must be snake_case
- Output names must be snake_case
- Module names must be snake_case
- Local names must be snake_case
- Data source names must be snake_case

### Security (6)
- Hardcoded credentials/secrets in values
- Overly permissive IAM policies (*)
- Missing encryption configuration
- Public access enabled (public_access, publicly_accessible)
- Hardcoded IP addresses (0.0.0.0/0)
- Sensitive variables without sensitive flag

### Best Practices (6)
- Missing variable type constraints
- Missing variable default values
- Missing output descriptions
- Using deprecated resource attributes
- Missing lifecycle blocks for stateful resources
- Missing tags on taggable resources

## Output Formats

- **text** (default): Human-readable with colors and severity icons
- **json**: Machine-readable with file, line, rule, severity, message
- **summary**: Counts by severity only

## Exit Codes

- 0: No issues (or warnings only)
- 1: Errors found
- 2: Invalid input
