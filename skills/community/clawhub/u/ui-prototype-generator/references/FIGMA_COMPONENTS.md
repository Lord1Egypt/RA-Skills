# Figma Components Library

## Component Structure

### Frame
- Name: Descriptive name
- Layout: Auto-layout with hug contents
- Padding: 16px standard
- Gap: 8px between elements

### Component Properties
- Variants for different states
- Boolean properties for optional elements
- Instance swap for icons
- Text properties for labels

## Button Components

### Primary Button
- **Frame**: 120x40px (min-width)
- **Fill**: Primary color (#1890ff)
- **Corner Radius**: 4px
- **Text**: White, 14px, Semi-bold
- **Padding**: 12px 24px
- **States**:
  - Default
  - Hover (darker shade)
  - Active (darker shade + inset shadow)
  - Disabled (opacity 0.5)
  - Loading (spinner icon)

### Secondary Button
- **Frame**: 120x40px (min-width)
- **Fill**: White
- **Stroke**: 1px Primary color
- **Corner Radius**: 4px
- **Text**: Primary color, 14px, Semi-bold
- **Padding**: 12px 24px

### Ghost Button
- **Frame**: 120x40px (min-width)
- **Fill**: Transparent
- **Text**: Primary color, 14px, Semi-bold
- **Padding**: 12px 24px

## Form Components

### Input Field
- **Frame**: Hug contents, min-width 200px
- **Background**: White
- **Stroke**: 1px #d9d9d9
- **Corner Radius**: 4px
- **Padding**: 8px 12px
- **Text**: 14px, Regular
- **Placeholder**: 14px, #bfbfbf
- **States**:
  - Default
  - Focus (Primary color border)
  - Error (Red border)
  - Disabled (Gray background)

### Label
- **Text**: 14px, Medium, #333333
- **Margin Bottom**: 8px

### Helper Text
- **Text**: 12px, Regular, #666666
- **Margin Top**: 4px

### Select Dropdown
- **Frame**: Hug contents, min-width 200px
- **Background**: White
- **Stroke**: 1px #d9d9d9
- **Corner Radius**: 4px
- **Padding**: 8px 12px
- **Icon**: Chevron down, right side

### Checkbox
- **Box**: 16x16px
- **Corner Radius**: 2px
- **Stroke**: 1px #d9d9d9
- **Check Icon**: 12px, Primary color
- **Label**: 14px, Regular, left margin 8px
- **States**:
  - Unchecked
  - Checked
  - Indeterminate
  - Disabled

### Radio Button
- **Circle**: 16x16px
- **Stroke**: 1px #d9d9d9
- **Dot**: 8x8px, Primary color (when selected)
- **Label**: 14px, Regular, left margin 8px
- **States**:
  - Unselected
  - Selected
  - Disabled

## Card Components

### Basic Card
- **Frame**: Hug contents, min-width 300px
- **Background**: White
- **Corner Radius**: 8px
- **Shadow**: 0 2px 8px rgba(0,0,0,0.1)
- **Padding**: 16px
- **Sections**:
  - Header (optional)
  - Body
  - Footer (optional)

### Card Header
- **Text**: 16px, Semi-bold
- **Padding Bottom**: 12px
- **Border Bottom**: 1px #f0f0f0

### Card Body
- **Padding**: 16px

### Card Footer
- **Padding Top**: 12px
- **Border Top**: 1px #f0f0f0
- **Alignment**: Right or space-between

## Navigation Components

### Navbar
- **Frame**: Full width, 64px height
- **Background**: White
- **Shadow**: 0 1px 4px rgba(0,0,0,0.1)
- **Padding**: 0 24px
- **Content**:
  - Logo (left)
  - Navigation links (center)
  - User menu (right)

### Nav Link
- **Text**: 14px, Regular
- **Color**: #666666 (default), Primary (active)
- **Padding**: 0 16px
- **States**:
  - Default
  - Hover
  - Active

### Sidebar
- **Frame**: 240px width, full height
- **Background**: #001529
- **Padding**: 16px 0
- **Menu Items**:
  - Icon (24px)
  - Label (14px, white)
  - Padding: 12px 24px

### Breadcrumb
- **Text**: 14px, Regular
- **Separator**: > (12px, #999999)
- **Active Item**: Primary color
- **Spacing**: 8px between items

## Modal Components

### Modal Overlay
- **Frame**: Full screen
- **Background**: rgba(0,0,0,0.5)
- **Z-index**: 1000

### Modal Dialog
- **Frame**: 520px width, hug contents height
- **Background**: White
- **Corner Radius**: 8px
- **Shadow**: 0 4px 12px rgba(0,0,0,0.15)
- **Centered**: Both horizontally and vertically

### Modal Header
- **Padding**: 16px 24px
- **Border Bottom**: 1px #f0f0f0
- **Title**: 16px, Semi-bold
- **Close Button**: 24x24px, right aligned

### Modal Body
- **Padding**: 24px
- **Max Height**: 60vh (scrollable)

### Modal Footer
- **Padding**: 16px 24px
- **Border Top**: 1px #f0f0f0
- **Alignment**: Right
- **Gap**: 8px between buttons

## Table Components

### Table Container
- **Frame**: Full width, hug contents height
- **Background**: White
- **Corner Radius**: 4px
- **Border**: 1px #f0f0f0

### Table Header
- **Background**: #fafafa
- **Height**: 48px
- **Text**: 14px, Semi-bold, #333333
- **Padding**: 12px 16px
- **Border Bottom**: 1px #f0f0f0

### Table Row
- **Height**: 48px
- **Padding**: 12px 16px
- **Border Bottom**: 1px #f0f0f0
- **Hover Background**: #fafafa

### Table Cell
- **Text**: 14px, Regular, #333333
- **Alignment**: Left (default), Right (numbers)

## Alert Components

### Alert Container
- **Frame**: Full width, hug contents height
- **Corner Radius**: 4px
- **Padding**: 12px 16px
- **Icon**: 16px, left side
- **Gap**: 8px between icon and text

### Alert Types
- **Success**: Green background (#f6ffed), Green icon
- **Info**: Blue background (#e6f7ff), Blue icon
- **Warning**: Yellow background (#fffbe6), Yellow icon
- **Error**: Red background (#fff2f0), Red icon

## Badge Components

### Badge
- **Frame**: Hug contents
- **Height**: 20px
- **Corner Radius**: 10px (pill shape)
- **Padding**: 0 8px
- **Text**: 12px, Medium, white
- **Types**:
  - Primary: Primary color
  - Success: Green
  - Warning: Orange
  - Error: Red
  - Default: Gray

## Progress Components

### Progress Bar Container
- **Frame**: Full width, 8px height
- **Background**: #f5f5f5
- **Corner Radius**: 4px

### Progress Bar Fill
- **Height**: 8px
- **Corner Radius**: 4px
- **Colors**:
  - Default: Primary color
  - Success: Green
  - Exception: Red

### Progress Text
- **Text**: 14px, Regular
- **Position**: Right of bar or inside

## Tooltip Components

### Tooltip Container
- **Frame**: Hug contents
- **Background**: rgba(0,0,0,0.75)
- **Corner Radius**: 4px
- **Padding**: 8px 12px
- **Text**: 12px, Regular, white

### Tooltip Arrow
- **Size**: 8px
- **Color**: rgba(0,0,0,0.75)
- **Position**: Top, bottom, left, or right

## Dropdown Components

### Dropdown Menu
- **Frame**: Hug contents, min-width 160px
- **Background**: White
- **Corner Radius**: 4px
- **Shadow**: 0 2px 8px rgba(0,0,0,0.15)
- **Padding**: 4px 0

### Dropdown Item
- **Height**: 32px
- **Padding**: 0 12px
- **Text**: 14px, Regular
- **Hover Background**: #f5f5f5
- **Divider**: 1px #f0f0f0 (optional)

## Tabs Components

### Tab Bar
- **Frame**: Full width, 48px height
- **Background**: White
- **Border Bottom**: 1px #f0f0f0

### Tab Item
- **Height**: 48px
- **Padding**: 0 16px
- **Text**: 14px, Regular
- **Active**: Primary color text + bottom border
- **Hover**: Primary color text

### Tab Content
- **Padding**: 24px
- **Background**: White

## Pagination Components

### Pagination Container
- **Frame**: Hug contents
- **Gap**: 8px between items

### Page Item
- **Size**: 32x32px
- **Corner Radius**: 4px
- **Text**: 14px, Regular, centered
- **States**:
  - Default: White background, gray border
  - Active: Primary color background, white text
  - Hover: Primary color border
  - Disabled: Gray text, no pointer events

## Layout Components

### Container
- **Max Width**: 1200px
- **Padding**: 0 24px
- **Centered**: Auto margins

### Grid System
- **Columns**: 12
- **Gutter**: 24px
- **Column Width**: (100% - 11*24px) / 12

### Spacing Scale
- xs: 4px
- sm: 8px
- md: 16px
- lg: 24px
- xl: 32px
- xxl: 48px

## Color Palette

### Primary Colors
- Primary: #1890ff
- Primary Hover: #40a9ff
- Primary Active: #096dd9

### Neutral Colors
- Text Primary: #333333
- Text Secondary: #666666
- Text Disabled: #bfbfbf
- Border: #d9d9d9
- Divider: #f0f0f0
- Background: #f5f5f5

### Functional Colors
- Success: #52c41a
- Warning: #faad14
- Error: #f5222d
- Info: #1890ff

## Typography

### Font Family
- Primary: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif
- Monospace: 'SF Mono', Monaco, monospace

### Font Sizes
- Heading 1: 24px, Bold
- Heading 2: 20px, Bold
- Heading 3: 16px, Semi-bold
- Body: 14px, Regular
- Small: 12px, Regular

### Line Heights
- Heading: 1.4
- Body: 1.5
- Tight: 1.2

## Shadow System

- Shadow 1: 0 1px 2px rgba(0,0,0,0.05)
- Shadow 2: 0 2px 8px rgba(0,0,0,0.1)
- Shadow 3: 0 4px 12px rgba(0,0,0,0.15)
- Shadow 4: 0 8px 24px rgba(0,0,0,0.2)
