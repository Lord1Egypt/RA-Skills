import os
import argparse

def main():
    parser = argparse.ArgumentParser(description="Apply UI design rules to .cursorrules or IDENTITY_UI.md")
    parser.add_argument("--style", choices=["fluent", "ant", "carbon", "atlassian", "apple-hig", "polaris", "material", "minimal", "glass", "neumorphism", "neo-brutalism", "claymorphism", "skeuomorphism", "swiss", "m3-pastel", "neo-m3"], default="minimal", help="The design language to use.")
    parser.add_argument("--palette", choices=["pastel", "dark", "vibrant", "mono"], default="pastel", help="The color palette preference.")
    args = parser.parse_args()

    # Base rules that always apply
    base_rules = """
# AI Design Rules (Frea's UI Core)

## Core Philosophy
- "Just enough engineering to get it done well." No bloat.
- Precision, Clarity, and Accessibility-First.
- Professional, production-ready interfaces.
"""

    style_rules = {
        "fluent": """- **Fluent Design (Microsoft)**
- Light, depth, motion, material, scale principles.
- Acrylic materials with backdrop-blur (30px) and saturate (125%).
- Reveal effect on hover with radial gradients.
- Dual shadow system for depth (light/dark).
- Segoe UI Variable font or system fonts.""",
        "ant": """- **Ant Design (Enterprise UI)**
- Natural, certain, meaningful, growing principles.
- 8px base spacing system.
- 12-column responsive grid (xs to xxl).
- Ant Blue (#1677FF) for primary actions.
- Clean borders (1-2px), subtle shadows.
- System fonts or -apple-system.""",
        "carbon": """- **Carbon Design (IBM)**
- Clarity, efficiency, consistency, inclusive.
- 16-column grid with 32px gutters.
- IBM Plex Sans/Mono typography.
- Layering model for depth (alternating surfaces).
- Gray scale (10-100) with Blue 60 (#0F62FE) primary.
- Sharp corners (0-4px), clean lines.""",
        "atlassian": """- **Atlassian Design System**
- Bold, optimistic, practical, approachable.
- 8px spacing grid system.
- Atlassian Blue (#0052CC) for brand/primary.
- 3px border radius (subtle).
- Clear elevation with layered shadows.
- System fonts for consistency.""",
        "apple-hig": """- **Apple Human Interface Guidelines**
- Clarity, deference, depth principles.
- SF Pro Text/Display typography.
- Vibrancy and blur materials (20px blur, 180% saturate).
- iOS system colors (Blue #007AFF, etc.).
- 44pt minimum touch targets.
- Smooth, natural animations (200-400ms).""",
        "polaris": """- **Shopify Polaris**
- Fresh, efficient, considerate, trustworthy.
- Teal (#008060) brand color.
- Clean, merchant-focused components.
- 8px spacing with 4px increments.
- System fonts or San Francisco.
- Clear feedback and helpful errors.""",
        "material": """- **Material You (M3)**
- Large rounded corners (rounded-3xl).
- Tonal palettes and subtle elevation.
- Dynamic color system support.
- Expressive typography.
- Adaptive layouts.""",
        "minimal": """- **Minimalism (Functional Elegance)**
- Focus on typography and generous whitespace.
- Limit borders. Ambient shadows only (2-5% opacity).
- High contrast hierarchy using Zinc shades (500 to 950).
- Content-first approach.""",
        "glass": """- **Glassmorphism**
- Use backdrop-blur-md/lg (12-20px).
- Semi-transparent backgrounds (bg-white/20).
- Subtle white borders (border-white/10).
- Vibrant background gradients.""",
        "neumorphism": """- **Neumorphism (Soft UI)**
- Monochromatic color scheme (same family).
- Dual shadow system (light top-left, dark bottom-right).
- Convex (raised) and concave (pressed) surfaces.
- Large border radius (12px+).
- Low contrast, soft aesthetic.""",
        "neo-brutalism": """- **Neo-Brutalism (Digital Rawness)**
- Thick black borders (4px solid #000).
- Hard offset shadows ONLY (shadow-[8px_8px_0px_0px_rgba(0,0,0,1)]).
- Vibrant, clashing colors.
- Bold typography.
- Snappy, springy transitions (cubic-bezier 0.175, 0.885, 0.32, 1.275).""",
        "claymorphism": """- **Claymorphism (Soft 3D)**
- Soft 3D "inflated" shapes.
- Double inner shadows (one light, one dark).
- Very large border radius (rounded-[40px]).
- Playful, pastel colors.
- Smooth, tactile feel.""",
        "skeuomorphism": """- **Skeuomorphism (Physical Realism)**
- Realistic textures (leather, wood, metal).
- Rich gradients and multiple shadow layers.
- Material-based colors.
- Embossed/debossed effects.
- Detailed, tactile interfaces.""",
        "swiss": """- **Swiss Design (International Typographic Style)**
- Strict 12-column modular grid is law.
- Sans-serif (Inter/Helvetica). Massive display type, tight letter-spacing (-0.04em).
- Sharp corners (0px-4px). No shadows. No gradients.
- Asymmetric balance. Horizontal rules as dividers. Indexing with numbers (01, 02).""",
        "m3-pastel": """- **M3 Pastel Glass (Hybrid)**
- Shape: Large rounded corners (28px). Morph to sharper (12px) on interaction.
- Glass: 12px-20px backdrop blur + 1px white border (15% opacity).
- Palette: Low saturation, high value pastels (Blue #D1E4FF, Purple #F7D8FF).""",
        "neo-m3": """- **Neo-M3 Hybrid (Industrial Modernism)**
- Structure: 3px solid black borders + 24px-32px rounded corners.
- Dashed: Use dashed borders for experimental features.
- Shadows: Hard offset 6px-10px. Vibe: Physical items on a grid.
- Typography: Bold headers + Monospace (JetBrains Mono) for technical metadata."""
    }

    palette_rules = {
        "pastel": "- Use soft, muted colors. Backgrounds: Slate-50 or Zinc-50.",
        "dark": "- Use deep Zinc-950 or Slate-950 for backgrounds.\n- Accents: High-visibility neon or pure white.",
        "vibrant": "- High-saturation primaries against pure black or white.",
        "mono": "- Single hue with varying lightness/saturation.\n- Sophisticated, cohesive aesthetic."
    }

    rules_to_add = f"""
{base_rules}
### Current Design Language: {args.style.upper()}
{style_rules[args.style]}

### Palette Selection: {args.palette.upper()}
{palette_rules[args.palette]}

### Technical Standards
- Tailwind CSS (Utility-first)
- Font Awesome 6 (Solid/Light)
- Clean, self-documenting code.
"""

    rules_file = ".cursorrules"
    mode = "a" if os.path.exists(rules_file) else "w"
    
    with open(rules_file, mode) as f:
        if mode == "a":
            f.write("\n\n--- UI Rule Update ---\n")
        f.write(rules_to_add)
    
    print(f"✅ Design language '{args.style}' with '{args.palette}' palette injected into {rules_file}")

if __name__ == "__main__":
    main()
