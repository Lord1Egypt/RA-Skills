# UI Prototype Generator - Examples

Complete examples of prototypes generated using this skill.

## Example 1: Admin Dashboard with Data Table

**Scenario**: User provides a screenshot of a business configuration page and wants to add a "Region" column.

**Generated Prototype**: See `examples/admin-dashboard.html`

**Key Features**:
- Top navigation bar with menu
- Left sidebar with active state
- Filter section with multiple input types
- Data table with sortable columns
- Status badges and action links
- Added "Region" column with tooltip

## Example 2: Create Business Modal Form

**Scenario**: User needs a modal form to create a new business entry with specific fields.

**Generated Prototype**: See `examples/create-business-modal.html`

**Key Features**:
- Modal dialog with header, body, footer
- Form fields: text inputs, selects, radio buttons
- Required field indicators
- Help text for complex fields
- Radio group for "Region" selection
- Default selection and validation hints

## Example 3: User Management Table

**Scenario**: User wants a user management interface with search, filters, and actions.

**HTML Structure**:
```html
<div class="page-container">
    <div class="filter-bar">
        <input type="text" placeholder="Search users...">
        <select><option>All Roles</option></select>
        <button class="btn-primary">Add User</button>
    </div>
    <table class="data-table">
        <thead>...</thead>
        <tbody>...</tbody>
    </table>
    <div class="pagination">...</div>
</div>
```

## Example 4: Settings Form

**Scenario**: Settings page with multiple sections and various input types.

**Components Used**:
- Section headers
- Text inputs
- Textarea
- Toggle switches
- Select dropdowns
- File upload
- Save/Cancel buttons

## Example 5: Login Page

**Scenario**: Simple login interface.

**Features**:
- Centered card layout
- Logo and branding
- Email/password inputs
- Remember me checkbox
- Forgot password link
- Submit button
- Social login options

## Common Patterns

### Pattern 1: Filter + Table + Pagination
```
[Filter Bar]
  - Search input
  - Status dropdown
  - Date range picker
  - Export button

[Data Table]
  - Sortable headers
  - Row actions
  - Status badges
  - Empty state

[Pagination]
  - Page numbers
  - Items per page
  - Total count
```

### Pattern 2: Master-Detail View
```
[Sidebar - Master List]
  - Searchable list
  - Selected item highlight
  - New item button

[Main Area - Detail View]
  - Header with actions
  - Form or read-only view
  - Tabs for sections
  - Save/Edit buttons
```

### Pattern 3: Wizard/Stepper
```
[Step Indicator]
  - Step 1: Basic Info (active)
  - Step 2: Configuration
  - Step 3: Review

[Form Content]
  - Current step fields
  - Validation messages

[Navigation]
  - Previous button
  - Next/Finish button
  - Cancel link
```

## CSS Snippets

### Card Layout
```css
.card {
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    padding: 24px;
}

.card-header {
    border-bottom: 1px solid #e8e8e8;
    padding-bottom: 16px;
    margin-bottom: 24px;
}
```

### Button Variants
```css
.btn {
    padding: 8px 16px;
    border-radius: 4px;
    font-size: 14px;
    cursor: pointer;
    transition: all 0.3s;
}

.btn-primary {
    background: #1890ff;
    color: white;
    border: none;
}

.btn-primary:hover {
    background: #40a9ff;
}

.btn-default {
    background: white;
    color: #333;
    border: 1px solid #d9d9d9;
}

.btn-danger {
    background: #ff4d4f;
    color: white;
    border: none;
}
```

### Status Badge
```css
.badge {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 2px;
    font-size: 12px;
}

.badge-success {
    background: #f6ffed;
    border: 1px solid #b7eb8f;
    color: #52c41a;
}

.badge-warning {
    background: #fffbe6;
    border: 1px solid #ffe58f;
    color: #faad14;
}

.badge-error {
    background: #fff1f0;
    border: 1px solid #ffa39e;
    color: #ff4d4f;
}
```

## Iteration Examples

### Iteration 1: Initial Version
- Basic structure
- Core components
- Placeholder data

### Iteration 2: Add Features
- New column in table
- Additional form field
- Tooltip or help text
- Interactive states

### Iteration 3: Polish
- Adjust colors
- Fine-tune spacing
- Add animations
- Responsive tweaks

## Real-World Use Cases

### Use Case 1: E-commerce Admin
- Product listing page
- Order management
- Inventory tracking
- Customer management

### Use Case 2: SaaS Dashboard
- Analytics overview
- User activity charts
- Subscription management
- Feature flags

### Use Case 3: CRM System
- Contact management
- Deal pipeline
- Task assignments
- Email templates

### Use Case 4: Content Management
- Article editor
- Media library
- Category management
- Publishing workflow

## Tips for Best Results

1. **Start with structure**: Layout first, details later
2. **Use real data**: Replace placeholders with realistic content
3. **Test interactions**: Click through all buttons and links
4. **Check responsive**: Resize browser to test adaptability
5. **Get feedback**: Share with stakeholders early
6. **Iterate quickly**: Make small, frequent improvements
7. **Document decisions**: Note why certain choices were made
8. **Keep it simple**: Avoid over-engineering the prototype