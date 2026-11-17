# ZhenZhen EHS Assistant (臻臻aiEHS专员助理伙伴)

An AI-powered EHS (Environment, Health & Safety) work companion designed for EHS officers and safety inspectors. Built on practical experience from large-scale infrastructure projects.

**No theory — just actionable standards.** Tell it your scenario, it tells you what to do, which regulations apply, what template to use, and what pitfalls to avoid.

## Features

| Domain | Features |
|:-------|:---------|
| **Daily Core** | Regulations quick reference, daily inspection SOP (8 categories, 50+ points), training support, hazard close-loop management, emergency management |
| **Specialized** | Special equipment/personnel management, certification guidance, resume & interview, document templates, workplace social skills |
| **Integrated** | Multi-level audit reception, safety meetings, documentation management, labor team management |
| **Professional** | High-risk operations (8 types), fire safety, occupational health, safety costs & insurance, seasonal safety, safety signs |

## File Structure

```
zhenzhen-ehs-assistant/
├── SKILL.md                          # Main skill document (OpenClaw format)
├── README.md                         # This file
├── docs/
│   └── project-plan.md               # Project planning document
└── references/                       # 21 scenario reference files (SOP format)
    ├── 01-ehs-regulations.md
    ├── 02-ehs-daily-inspection.md
    ├── ...
    └── 21-safety-signs.md
```

## Usage

This is an OpenClaw skill. To use it:

1. Install via ClawHub: `npx clawhub install zhenzhen-ehs-assistant`
2. Or manually place the folder in your OpenClaw skills directory
3. Then ask questions like:
   - "Generate today's daily inspection checklist"
   - "Prepare a pre-shift talk on temporary electrical safety"
   - "Generate a fire drill plan template"
   - "Prepare inspection document checklist for owner quarterly audit"

## License

MIT
