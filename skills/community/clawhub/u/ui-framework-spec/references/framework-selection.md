# Framework Selection Guide

## Decision Process

### Step 1: Determine Target Platform / Tech Stack

```
Vue 3 project?
├── Yes → Element Plus (First choice), TDesign (Alternative)
└── No → React project?
    ├── Yes → Go to Step 2
    └── No → Recommended: TDesign (supports Vue/React/Angular/Miniprogram)
```

### Step 2: Design Tone Matching

| Design Tone | Recommended Framework | Typical Scenarios |
|---|---|---|
| Professional, enterprise-grade, B2B | Ant Design | Admin panels, enterprise applications, data analysis platforms |
| Clean neutral, lightweight, Vue ecosystem | Element Plus | Back-office, admin panels, first choice for Vue projects |
| Modern flexible, customizable, creative | Arco Design | Innovative back-office, SaaS platforms |
| General enterprise, cross-platform, Tencent ecosystem | TDesign | Enterprise applications, cross-platform projects |
| Content-immersive, information-dense, high-performance | Semi Design | Data-intensive applications, editing tools, live streaming dashboards |

### Step 3: Framework Feature Comparison

| Dimension | Element Plus | Ant Design | Arco Design | TDesign | Semi Design |
|---|---|---|---|---|---|
| Number of Components | 70+ | 60+ | 50+ | 60+ | 70+ |
| Internationalization (i18n) | Full | Full | Full | Full | Full |
| Theme Customization | CSS Var | Design Token | CSS Var | CSS Var | CSS Var + Token |
| TypeScript | Full Support | Full Support | Full Support | Full Support | Full Support |
| Dark Mode | Built-in | Built-in | Built-in | Built-in | Built-in |
| On-demand Loading | Automatic | Automatic | Automatic | Automatic | Automatic |
| Community Activity | High | Highest | Medium | Medium | Medium |
| Learning Curve | Low | Medium | Low | Low | Medium |
| Design Resources (Figma/Sketch) | Available | Available | Available | Available | Available |

### Step 4: Framework-Specific Advantages

| Framework | Specific Advantages |
|---|---|
| Element Plus | Best choice for Vue 3 ecosystem, works perfectly with VueUse/Pinia, intuitive component API |
| Ant Design | Most mature, ProComponents ecosystem, rich business component templates, best internationalization |
| Arco Design | Visual theme editor, supporting material platform, strong modern design sense |
| TDesign | Multi-platform unified solution (Mobile/Desktop/Miniprogram), available for both Vue and React |
| Semi Design | Content-scenario optimization, D2C design-to-code, high-performance virtual list |

## Combination Recommendations

### Pure Vue 3 Project
- **First choice**: Element Plus + matching layout solution
- **Alternative**: TDesign Vue (if cross-platform needed)

### Pure React Project
- **General back-office**: Ant Design
- **Innovation/design-driven**: Arco Design
- **Content-dense / high-performance**: Semi Design
- **Cross-platform needs**: TDesign React

### Multi-Framework Mix
Mixing multiple frameworks in the same project is not recommended. If necessary (e.g., legacy), use `ConfigProvider` to isolate namespaces and themes.
