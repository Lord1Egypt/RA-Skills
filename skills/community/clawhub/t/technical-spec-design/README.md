# Technical Specification Design Skill

> A comprehensive skill for writing technical specifications based on product requirements.

## 📁 Directory Structure

```
technical-spec-design/
├── skill.md                         # Main skill file (entry point)
├── README.md                        # This file
├── scripts/                         # Executable scripts (Python)
│   ├── generate_spec.py            # Generate spec from template
│   ├── validate.py                 # Validate skill structure
│   └── pyproject.toml              # Python project config
├── resources/                       # Templates and reference docs
│   ├── spec_template.md            # Main spec template
│   ├── component_template.md       # Component design template
│   └── requirements_analysis_template.md  # Requirements analysis guide
└── examples/                        # Sample inputs and outputs
    ├── sample_input.md             # Sample PRD
    └── sample_output.md            # Complete spec example
```

## 🚀 Quick Start

### For Users

1. **Learn fundamentals**: Read [`resources/requirements_analysis_template.md`](resources/requirements_analysis_template.md)
2. **Use templates**: Copy [`resources/spec_template.md`](resources/spec_template.md) to start
3. **Review examples**: Examine [`examples/sample_output.md`](examples/sample_output.md)

### For Developers

1. **No dependencies required** - Scripts use Python standard library only

2. **Interactive spec generation**:
   ```bash
   cd ~/.claude/skills/technical-spec-design/scripts
   python generate_spec.py --interactive -o my_spec.md
   ```

3. **Validate skill structure**:
   ```bash
   cd ~/.claude/skills/technical-spec-design/scripts
   python validate.py
   ```

## 📚 Learning Path

### Level 1: Beginner
Understand **the Requirements Analysis Trifecta**:
- Feature Breakdown
- Use Case Analysis
- Page Operation Details

### Level 2: Intermediate
Learn **Component Design**:
- How to write component-level specs
- Pseudocode vs actual code
- API design documentation

### Level 3: Advanced
Master **Full Technical Specifications**:
- State machine design
- Technical research and comparison
- Integration and monitoring planning

## 🛠️ Scripts

### generate_spec.py

Generate technical specifications from templates using Python.

```bash
# Interactive mode
python generate_spec.py --interactive

# Generate from PRD file
python generate_spec.py --prd prd.md --output spec.md

# Output template only
python generate_spec.py --template

# Show help
python generate_spec.py --help
```

### validate.py

Validate skill structure and content.

```bash
# Run validation
python validate.py

# Verbose output
python validate.py --verbose
```

## 📖 Core Concepts

### The Requirements Analysis Trifecta

This skill emphasizes three key components of requirements analysis:

1. **Feature Breakdown**: Map product requirements to technical features
2. **Use Case Analysis**: Describe end-to-end business flows
3. **Page Operation Details**: Define page-level operation specifics

### Component-Level Design

All technical changes must be drilled down to component/module level, not just page-level descriptions.

### Pseudocode Convention

Use pseudocode structure to describe implementation approach, not actual implementation code.

## 🎯 Best Practices

1. **Clarify first, write second**: Always clarify ambiguous requirements first
2. **Component-first**: Drill down to component level, not page level
3. **Pseudocode**: Use pseudocode, not actual code
4. **Structured research**: Use comparison tables for technical decisions
5. **Review-ready**: Specs should be directly implementable

## 📝 Usage Example

```bash
# Copy template
cp resources/spec_template.md my_project_spec.md

# Edit content
vim my_project_spec.md

# Or generate interactively
python scripts/generate_spec.py --interactive -o my_project_spec.md

# Validate spec
python scripts/validate.py
```

## 🔗 Related Resources

- [Claude Skills Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [Skills Structure Guide](https://yeasy.gitbook.io/claude_guide/di-san-bu-fen-jin-jie-pian/06_skills/6.2_structure)

## 📄 License

This skill is provided as-is for educational and commercial use.
