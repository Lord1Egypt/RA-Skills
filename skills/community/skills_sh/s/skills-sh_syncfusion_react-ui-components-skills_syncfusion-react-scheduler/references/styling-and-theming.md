# Styling and Theming

## Table of Contents
- [Overview](#overview)
- [Built-in Themes](#built-in-themes)
- [CSS Customization](#css-customization)
- [Custom CSS Classes for Events](#custom-css-classes-for-events)
- [Cell Styling](#cell-styling)
- [Resource Styling](#resource-styling)
- [Theme Studio Integration](#theme-studio-integration)
- [Event Color Customization](#event-color-customization)

## Overview

The Syncfusion React Scheduler component provides comprehensive styling capabilities to customize its appearance. You can override default CSS classes to match your application's design requirements. The Scheduler supports built-in themes and allows for custom theme creation through Theme Studio.

### Key Styling Features
- Built-in theme support
- Customizable CSS classes for all elements
- View-specific styling options
- Resource-based styling
- Event color customization
- Work hours and work days styling
- Cell and header customization

## Built-in Themes

The Scheduler component comes with several built-in themes that can be applied to match your application's look and feel:

### Available Themes
- **Material** - Google's Material Design theme
- **Bootstrap** - Twitter Bootstrap theme
- **Fabric** - Microsoft Office Fabric theme
- **Tailwind** - Tailwind CSS theme
- **Fluent** - Microsoft Fluent Design theme
- **High Contrast** - High contrast theme for accessibility

### Theme Application
Themes are applied by referencing the appropriate CSS file in your application. The Scheduler automatically inherits the theme from the CSS references.

## CSS Customization

Override default CSS classes to customize the Scheduler's appearance. Below are the primary CSS classes available for customization.

### Work Cells Styling

Work cells represent the time slots in the Scheduler views:

| CSS Class | Description |
|-----------|-------------|
| `.e-schedule .e-vertical-view .e-work-cells` | Work cells in vertical views (Day, Week, WorkWeek) |
| `.e-schedule .e-month-view .e-work-cells` | Work cells in month view |
| `.e-schedule .e-month-view .e-other-month` | Work cells of other months in month view |
| `.e-schedule .e-timeline-view .e-work-cells` | Work cells in timeline views |
| `.e-schedule .e-timeline-month-view .e-work-cells` | Work cells in timeline month view |
| `.e-schedule .e-timeline-year-view .e-work-cells` | Work cells in timeline year view |
| `.e-schedule .e-timeline-year-view .e-work-cells.e-other-month` | Work cells of other months in timeline year view |
| `.e-schedule .e-month-agenda-view .e-work-cells` | Work cells in month agenda view |
| `.e-schedule .e-month-agenda-view .e-other-month` | Work cells of other months in month agenda view |
| `.e-schedule .e-year-view .e-calendar-wrapper .e-month-calendar.e-calendar .e-other-month` | Work cells of other months in year view |

### All Day and Work Hours Styling

| CSS Class | Description |
|-----------|-------------|
| `.e-schedule .e-vertical-view .e-all-day-cells` | All day cells in vertical views |
| `.e-schedule .e-vertical-view .e-work-hours` | Work hour cells in vertical views |
| `.e-schedule .e-timeline-view .e-work-hours` | Work hour cells in timeline views |
| `.e-schedule .e-month-view .e-work-days` | Work day cells in month view |
| `.e-schedule .e-month-agenda-view .e-work-days` | Work day cells in month agenda view |
| `.e-schedule .e-timeline-month-view .e-work-days` | Work day cells in timeline month view |
| `.e-schedule .e-timeline-year-view .e-work-cells.e-work-days` | Work day cells in timeline year view |

### Header Cells Styling

| CSS Class | Description |
|-----------|-------------|
| `e-header-cells` | Header cells of the Scheduler (use hierarchically based on views) |

### Selection States

| CSS Class | Description |
|-----------|-------------|
| `e-selected-cells` | Currently selected work cells (use hierarchically based on views) |
| `e-appointment-border` | Currently selected appointments (use hierarchically based on views) |

## Custom CSS Classes for Events

Appointments in the Scheduler can be styled using view-specific CSS classes:

### Appointment Styling by View

| CSS Class | Description |
|-----------|-------------|
| `.e-schedule .e-vertical-view .e-day-wrapper .e-appointment` | Appointments in vertical views |
| `.e-schedule .e-vertical-view .e-all-day-appointment-wrapper .e-appointment` | All day appointments in vertical views |
| `.e-schedule .e-month-view .e-appointment` | Appointments in month view |
| `.e-schedule .e-timeline-view .e-appointment` | Appointments in timeline views |
| `.e-schedule .e-timeline-month-view .e-appointment` | Appointments in timeline month view |
| `.e-schedule .e-timeline-year-view .e-event-table .e-appointment` | Appointments in timeline year view |
| `.e-schedule .e-year-view .e-calendar-wrapper .e-month-calendar.e-calendar .e-appointment` | Appointments in year view |
| `.e-schedule .e-agenda-view .e-appointment` | Appointments in agenda view |
| `.e-schedule .e-month-agenda-view .e-appointment-indicator` | Appointment indicators in month agenda view |

### Special Appointment Types

| CSS Class | Description |
|-----------|-------------|
| `.e-schedule .e-block-appointment` | Block appointments (unavailable time slots) |
| `.e-schedule .e-read-only` | Read-only appointments |

### Example: Custom Event Styling

```css
/* Customize appointment appearance */
.e-schedule .e-vertical-view .e-day-wrapper .e-appointment {
    border-radius: 8px;
    border-left: 4px solid #007bff;
}

/* Style all day appointments */
.e-schedule .e-vertical-view .e-all-day-appointment-wrapper .e-appointment {
    background-color: #e3f2fd;
    color: #1976d2;
}

/* Block appointments styling */
.e-schedule .e-block-appointment {
    background-color: #f5f5f5;
    opacity: 0.7;
    pattern: diagonal-stripes;
}
```

## Cell Styling

Customize the appearance of work cells, all-day cells, and time cells in the Scheduler.

### Work Cell Customization

```css
/* Customize work cells in day/week view */
.e-schedule .e-vertical-view .e-work-cells {
    background-color: #ffffff;
    border-color: #e0e0e0;
}

/* Highlight work hours */
.e-schedule .e-vertical-view .e-work-hours {
    background-color: #f9f9f9;
}

/* Style other month cells in month view */
.e-schedule .e-month-view .e-other-month {
    background-color: #fafafa;
    color: #9e9e9e;
}
```

### All Day Cells Customization

```css
/* Customize all day row */
.e-schedule .e-vertical-view .e-all-day-cells {
    background-color: #f5f5f5;
    border-bottom: 2px solid #e0e0e0;
}
```

### Selected Cell Styling

```css
/* Style selected cells */
.e-schedule .e-selected-cells {
    background-color: #bbdefb;
    border: 2px solid #2196f3;
}
```

### Timeline View Cell Styling

```css
/* Customize timeline work cells */
.e-schedule .e-timeline-view .e-work-cells {
    background-color: #ffffff;
}

/* Timeline work hours */
.e-schedule .e-timeline-view .e-work-hours {
    background-color: #f0f0f0;
}
```

## Resource Styling

When using resources in the Scheduler, you can customize resource cells and differentiate between parent and child resources.

### Resource Cell Classes

| CSS Class | Description |
|-----------|-------------|
| `.e-schedule .e-vertical-view .e-resource-cells` | Resource cells in vertical views |
| `.e-schedule .e-month-view .e-resource-cells` | Resource cells in month view |
| `.e-schedule .e-timeline-view .e-resource-cells` | Resource cells in timeline views |
| `.e-schedule .e-timeline-month-view .e-resource-cells` | Resource cells in timeline month view |
| `e-parent-node` | Parent resource cells in timeline views |
| `e-child-node` | Child resource cells in timeline views |

### Resource Styling Examples

```css
/* Style resource cells in timeline view */
.e-schedule .e-timeline-view .e-resource-cells {
    background-color: #eceff1;
    font-weight: 600;
    padding: 10px;
}

/* Parent resource styling */
.e-schedule .e-parent-node {
    background-color: #cfd8dc;
    font-size: 14px;
    font-weight: bold;
}

/* Child resource styling */
.e-schedule .e-child-node {
    background-color: #f5f5f5;
    font-size: 12px;
    padding-left: 20px;
}

/* Resource-specific colors */
.e-schedule .e-resource-cells[data-resource="room1"] {
    border-left: 4px solid #4caf50;
}

.e-schedule .e-resource-cells[data-resource="room2"] {
    border-left: 4px solid #2196f3;
}
```

## Theme Studio Integration

The Syncfusion Theme Studio provides a visual interface for creating custom themes for the Scheduler component.

### Using Theme Studio

1. **Access Theme Studio**: Navigate to syncfusion theme studio

2. **Select Base Theme**: Choose a base theme to start with (Material, Bootstrap, Fabric, Tailwind, Fluent, or High Contrast)

3. **Customize Colors**: Modify primary colors, secondary colors, and component-specific colors

4. **Preview Changes**: See real-time preview of your customizations on various components including Scheduler

5. **Download Theme**: Export your custom theme as CSS files

6. **Apply to Application**: Include the generated CSS files in your React application

### Theme Studio Features
- Color palette customization
- Component-specific styling
- Export as CSS or SCSS
- Preview across all Syncfusion components
- Responsive design support

### Integration Steps

```javascript
// Import custom theme CSS in your application
import './custom-theme.css';

// Or reference in HTML
<link rel="stylesheet" href="path/to/custom-theme.css" />
```

## Event Color Customization

Customize event colors based on categories, priorities, or custom fields.

### Inline Style Application

Events can have custom colors applied through the event data:

```javascript
const eventData = [
    {
        Id: 1,
        Subject: 'Meeting',
        StartTime: new Date(2023, 0, 10, 10, 0),
        EndTime: new Date(2023, 0, 10, 11, 0),
        CategoryColor: '#1aaa55' // Custom color
    }
];
```

### CSS-Based Color Customization

```css
/* Style events by category */
.e-schedule .e-appointment.category-meeting {
    background-color: #2196f3;
    color: #ffffff;
}

.e-schedule .e-appointment.category-task {
    background-color: #ff9800;
    color: #ffffff;
}

.e-schedule .e-appointment.category-event {
    background-color: #4caf50;
    color: #ffffff;
}

/* Priority-based styling */
.e-schedule .e-appointment.priority-high {
    border-left: 5px solid #f44336;
}

.e-schedule .e-appointment.priority-medium {
    border-left: 5px solid #ff9800;
}

.e-schedule .e-appointment.priority-low {
    border-left: 5px solid #4caf50;
}
```

### Template-Based Color Customization

Use event templates for advanced color customization:

```javascript
function eventTemplate(props) {
    const color = props.CategoryColor || '#1aaa55';
    return (
        <div style={{ backgroundColor: color }} className="template-wrap">
            <div className="subject">{props.Subject}</div>
            <div className="time">{props.StartTime.toLocaleTimeString()}</div>
        </div>
    );
}

<ScheduleComponent eventSettings={{ 
    dataSource: eventData,
    template: eventTemplate 
}} />
```

### Resource-Based Color Coding

Events can inherit colors from their associated resources:

```javascript
const resourceData = [
    { Id: 1, Text: 'Room A', Color: '#1aaa55' },
    { Id: 2, Text: 'Room B', Color: '#357cd2' }
];

// Events will use resource colors
const eventData = [
    {
        Id: 1,
        Subject: 'Meeting',
        StartTime: new Date(2023, 0, 10, 10, 0),
        EndTime: new Date(2023, 0, 10, 11, 0),
        RoomId: 1 // Uses Room A color
    }
];
```

### Dynamic Color Assignment

Programmatically assign colors based on event properties:

```css
/* Use data attributes for dynamic styling */
.e-schedule .e-appointment[data-status="confirmed"] {
    background-color: #4caf50;
}

.e-schedule .e-appointment[data-status="pending"] {
    background-color: #ff9800;
    opacity: 0.7;
}

.e-schedule .e-appointment[data-status="cancelled"] {
    background-color: #f44336;
    text-decoration: line-through;
}
```

**Note**: When overriding CSS classes, ensure specificity is maintained to properly apply custom styles. Use hierarchical selectors based on the view type to target specific elements accurately.
