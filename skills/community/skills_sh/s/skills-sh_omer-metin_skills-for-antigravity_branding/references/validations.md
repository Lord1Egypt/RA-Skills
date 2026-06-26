# Branding - Validations

## Hardcoded Color Values

### **Id**
hardcoded-colors
### **Severity**
error
### **Type**
regex
### **Pattern**
#[0-9a-fA-F]{3,6}(?![a-zA-Z0-9])|rgb\\(|rgba\\(|hsl\\(|hsla\\(
### **Message**
Hardcoded color values found. Use brand tokens from design system instead.
### **Fix Action**
Replace with brand color tokens (e.g., colors.brand.primary, var(--color-primary))
### **Applies To**
  - *.tsx
  - *.jsx
  - *.css
  - *.scss

## Inconsistent Font Family Usage

### **Id**
inconsistent-font-family
### **Severity**
error
### **Type**
regex
### **Pattern**
font-family:\s*["'](?!var\(|inherit|Montserrat|Inter)|fontFamily:\s*["'](?!var\(|inherit|Montserrat|Inter)
### **Message**
Non-standard font family detected. Use brand typography tokens.
### **Fix Action**
Use brand font tokens (e.g., font.family.heading, var(--font-heading))
### **Applies To**
  - *.tsx
  - *.jsx
  - *.css
  - *.scss

## Magic Number Spacing Values

### **Id**
magic-spacing-numbers
### **Severity**
warning
### **Type**
regex
### **Pattern**
(margin|padding|gap):\s*[0-9]+px(?!\s*/\*)|(margin|padding|gap):\s*[0-9]+rem(?!\s*/\*)
### **Message**
Magic number spacing detected. Use spacing scale from design system.
### **Fix Action**
Replace with spacing tokens (e.g., spacing[4], var(--spacing-4))
### **Applies To**
  - *.tsx
  - *.jsx
  - *.css
  - *.scss

## Inconsistent Border Radius

### **Id**
inconsistent-border-radius
### **Severity**
warning
### **Type**
regex
### **Pattern**
border-radius:\s*[0-9]+px|borderRadius:\s*["'][0-9]+px["']
### **Message**
Custom border radius values should use brand tokens.
### **Fix Action**
Use border radius tokens (e.g., borderRadius.md, var(--radius-md))
### **Applies To**
  - *.tsx
  - *.jsx
  - *.css
  - *.scss

## Missing Logo Alt Text

### **Id**
missing-brand-logo-alt
### **Severity**
error
### **Type**
regex
### **Pattern**
<img[^>]+src=["'][^"']*logo[^"']*["'][^>]+alt=["']["']|<img[^>]+alt=["']["'][^>]+src=["'][^"']*logo
### **Message**
Brand logo missing descriptive alt text.
### **Fix Action**
Add meaningful alt text for brand logo (e.g., 'Vibeship - Company Logo')
### **Applies To**
  - *.tsx
  - *.jsx
  - *.html

## Inconsistent Box Shadow

### **Id**
inconsistent-shadow-values
### **Severity**
warning
### **Type**
regex
### **Pattern**
box-shadow:\s*[0-9]|boxShadow:\s*["'][0-9]
### **Message**
Custom shadow values detected. Use brand elevation tokens.
### **Fix Action**
Replace with elevation tokens (e.g., shadows.md, var(--shadow-md))
### **Applies To**
  - *.tsx
  - *.jsx
  - *.css
  - *.scss

## Non-Standard Icon Library Usage

### **Id**
non-brand-icon-library
### **Severity**
info
### **Type**
regex
### **Pattern**
from\s+["']react-icons/fa["']|from\s+["']react-icons/ai["']|from\s+["']@fortawesome
### **Message**
Non-standard icon library detected. Use brand-approved icon system.
### **Fix Action**
Use approved icon library (e.g., lucide-react, heroicons)
### **Applies To**
  - *.tsx
  - *.jsx

## Missing Brand Focus Styles

### **Id**
missing-focus-styles
### **Severity**
warning
### **Type**
regex
### **Pattern**
outline:\s*none(?!.*focus)|outline:\s*0(?!.*focus)
### **Message**
Focus outline removed without brand-compliant replacement.
### **Fix Action**
Add brand focus styles using focus ring tokens (e.g., ring-offset-2 ring-brand)
### **Applies To**
  - *.tsx
  - *.jsx
  - *.css
  - *.scss

## Custom Button Styling

### **Id**
inconsistent-button-styles
### **Severity**
warning
### **Type**
regex
### **Pattern**
<button[^>]+style=|<button[^>]+className=["'][^"']*bg-\[#
### **Message**
Custom button styling detected. Use brand Button component.
### **Fix Action**
Use standardized Button component with variant props (e.g., <Button variant='primary'>)
### **Applies To**
  - *.tsx
  - *.jsx

## Missing Brand Metadata

### **Id**
missing-brand-metadata
### **Severity**
error
### **Type**
regex
### **Pattern**
<meta[^>]+property=["']og:image["'][^>]+content=["']["']|<title></title>
### **Message**
Missing or empty brand metadata (OG image, title).
### **Fix Action**
Add complete brand metadata including OG image, title, and description
### **Applies To**
  - *.html
  - *.tsx
  - *.jsx

## Inconsistent Animation Timing

### **Id**
inconsistent-transition-timing
### **Severity**
info
### **Type**
regex
### **Pattern**
transition:\s*[^;]+[0-9]+ms|transition:\s*[^;]+[0-9\.]+s
### **Message**
Custom transition timing detected. Use brand animation tokens.
### **Fix Action**
Use standard timing tokens (e.g., transition.fast, var(--transition-base))
### **Applies To**
  - *.tsx
  - *.jsx
  - *.css
  - *.scss

## Unclear Color Token Naming

### **Id**
brand-color-naming-convention
### **Severity**
warning
### **Type**
regex
### **Pattern**
(color1|color2|color3|myColor|customColor)|const\s+\w*Color\w*\s*=\s*["']#
### **Message**
Unclear color naming convention. Use semantic brand color names.
### **Fix Action**
Use semantic names (e.g., brandPrimary, accentGreen, neutralGray)
### **Applies To**
  - *.tsx
  - *.jsx
  - *.ts
  - *.js