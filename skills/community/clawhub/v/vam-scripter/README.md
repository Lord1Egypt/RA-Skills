# VAM Scripter Skill

This skill provides comprehensive documentation and examples for using VAM Scripter, the JavaScript-inspired scripting language for Virt-A-Mate.

## Structure

```
skills/vam-scripter/
├── SKILL.md              # Main documentation
├── references/           # API references
│   ├── module-api.md     # Module API documentation
│   └── common-patterns.md# Common patterns and examples
└── scripts/              # Example scripts
    ├── interaction-detection.js
    ├── circular-motion.js
    ├── parameter-animation.js
    ├── state-persistence.js
    ├── keybindings.js
    ├── multiple-atoms.js
    └── player-proximity.js
```

## Installation

### Via ClawHub

```bash
clawhub install vam-scripter
```

### From Local Source

Copy the entire `vam-scripter` folder to your `skills/` directory.

## Usage

### Use Example Scripts

Copy scripts from `scripts/` to your VAM Scripter directory:

```
Custom/Scripts/AcidBubbles/Scripter/index.js
```

### Documentation

See `../SKILL.md` in this skill for comprehensive documentation.

## Available Scripts

1. **interaction-detection.js** - Detects when objects collide
2. **circular-motion.js** - Animates objects in circular patterns
3. **parameter-animation.js** - Uses scripter parameters for animations
4. **state-persistence.js** - Saves and loads state across sessions
5. **keybindings.js** - Manages keybindings and actions
6. **multiple-atoms.js** - Works with multiple atoms simultaneously
7. **player-proximity.js** - Reacts to player presence

## Module Overview

| Module | Purpose |
|--------|---------|
| `scripter` | Lifecycle hooks and parameters |
| `scene` | Scene access (atoms, audio) |
| `player` | Player information |
| `keybindings` | Keybinding management |
| `fs` | File system operations |
| `Time` | Time properties |
| `Random` | Random number generation |
| `Math` | Mathematical functions |
| `DateTime` | Date/time operations |

## Development Workflow

1. **Plan** - Review `SKILL.md` and decide on approach
2. **Prototype** - Use example scripts as templates
3. **Test** - Load in VAM and test
4. **Refine** - Adjust parameters and logic
5. **Document** - Add to your documentation

## Tips

- Cache atom references (expensive to look up)
- Use parameters for configurable behavior
- Handle errors gracefully with try/catch
- Clean up with `onDisable` and `onDestroy`
- Use proper comments for maintainability

## Troubleshooting

- **Module not found** - Ensure `import { ... } from "vam-scripter"`
- **Atom not found** - Check atom names match exactly
- **Performance issues** - Reduce update frequency or cache references
- **Parameter not updating** - Check `onChange` callback is set