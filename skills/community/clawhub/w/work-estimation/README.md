# 📊 Software Development Work Estimation

Automatically analyze requirements, break down work items, estimate effort, and output professional Excel evaluation reports.

## Features

- ✅ **AI Smart Breakdown** - Automatically analyze requirements and split into work modules
- ✅ **Six-Dimension Estimation** - Analysis, Design, Frontend, Backend, Algorithm, Testing
- ✅ **Gantt Chart** - Visual project progress with parallel work display
- ✅ **Risk Assessment** - Highlight high-risk and uncertain items
- ✅ **Coordination Relations** - Clear dependencies and coordination matters

## Output Structure

| Sheet | Content |
|-------|---------|
| Overview | All work items summary with dimension ratios |
| Analysis | Analysis dimension details |
| Design | Design dimension details |
| Frontend | Frontend development details |
| Backend | Backend development details |
| Algorithm | Algorithm development details |
| Testing | Testing details |
| Gantt Chart | Project progress (skips weekends/holidays) |
| Key Risks | High-risk items |
| Coordination | Dependencies and coordination |
| Cost Estimation | Labor + hardware/software costs |

## Usage

Describe your requirements:
```
Help me estimate this project: Develop an e-commerce mini-app with user login, product display, shopping cart, and order payment
```

## Files

```
work-estimation-en/
├── SKILL.md           # Skill definition
├── README.md          # This file
├── scripts/
│   └── generate_estimation.py  # Excel generator
├── references/
│   └── evaluation-guide.md      # Estimation guide
└── evals/
    └── evals.json    # Test cases
```
