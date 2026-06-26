# SenseCraft HMI Screen Specifications

## Supported Resolutions

| Product | Resolution | Color Support |
|---------|-----------|---------------|
| reTerminal E1001 | 800x480 | Monochrome |
| reTerminal E1002 | 800x480 | E-Ink Spectra 6 |
| reTerminal E1003 | 1404x1872 | Monochrome |
| reTerminal E1004 | 1200x1600 | E-Ink Spectra 6 |
| ePaper DIY Kit - EE02 | 1600x1200 | E-Ink Spectra 6 |
| ePaper DIY Kit - EE03 | 1404x1872 | Monochrome |
| e-ink template 7.5" (OG) DIY Kit | 800x480 | Monochrome |
| EE04 - 4.26" Monochrome | 800x480 | Monochrome |
| EE04 - 2.9" BWRY | 128x296 | BWRY (Black/White/Red/Yellow) |
| EE04 - 2.9" Monochrome | 128x296 | Monochrome |
| EE04 - 2.13" BWRY | 122x250 | BWRY (Black/White/Red/Yellow) |
| EE04 - 2.13" Monochrome | 122x250 | Monochrome |
| EE04 - 1.54" Monochrome | 200x200 | Monochrome |
| EE04 - 7.5" Monochrome | 800x480 | Monochrome |
| EE04 - 7.3" Full Color | 800x480 | E-Ink Spectra 6 |

## Color Palettes

### Monochrome
- Black: `#000000`
- White: `#FFFFFF`
- Gray shades: `#333333`, `#666666`, `#999999`, `#CCCCCC`

### BWRY (4-color)
- Black: `#000000`
- White: `#FFFFFF`
- Red: `#FF0000`
- Yellow: `#FFFF00`

### E-Ink Spectra 6 (6-color)
- Black: `#000000`
- White: `#FFFFFF`
- Red: `#FF0000`
- Yellow: `#FFFF00`
- Blue: `#0000FF`
- Green: `#00FF00`

## Design Guidelines

1. **High contrast** - E-ink displays require strong contrast
2. **Large fonts (MANDATORY)** - Minimum 32px for all text, 48px+ for main content. Small fonts become unreadable after e-ink dithering.
3. **Bold text preferred** - Improves readability on e-ink
4. **Simple layouts** - Avoid complex gradients or shadows
5. **Static content** - E-ink refresh is slow (2-5 seconds)
6. **Minimal colors** - Use only supported palette colors
7. **Generous spacing** - Use large padding (40px+) and line-height (1.8+)
