# HTML Components Library

## Button Components

### Primary Button
```html
<button class="btn btn-primary">Primary Button</button>
```

### Secondary Button
```html
<button class="btn btn-secondary">Secondary Button</button>
```

### Button States
- Default
- Hover
- Active
- Disabled
- Loading

## Form Components

### Input Field
```html
<div class="form-group">
  <label for="email">Email</label>
  <input type="email" id="email" class="form-control" placeholder="Enter email">
</div>
```

### Select Dropdown
```html
<div class="form-group">
  <label for="country">Country</label>
  <select id="country" class="form-control">
    <option value="">Select...</option>
    <option value="us">United States</option>
    <option value="uk">United Kingdom</option>
  </select>
</div>
```

### Checkbox
```html
<div class="form-check">
  <input type="checkbox" id="agree" class="form-check-input">
  <label for="agree" class="form-check-label">I agree to terms</label>
</div>
```

### Radio Button
```html
<div class="form-check">
  <input type="radio" name="option" id="option1" class="form-check-input">
  <label for="option1" class="form-check-label">Option 1</label>
</div>
```

## Card Components

### Basic Card
```html
<div class="card">
  <div class="card-header">
    <h3 class="card-title">Card Title</h3>
  </div>
  <div class="card-body">
    <p class="card-text">Card content goes here.</p>
  </div>
  <div class="card-footer">
    <button class="btn btn-primary">Action</button>
  </div>
</div>
```

### Card with Image
```html
<div class="card">
  <img src="image.jpg" class="card-img-top" alt="...">
  <div class="card-body">
    <h5 class="card-title">Card Title</h5>
    <p class="card-text">Card description.</p>
  </div>
</div>
```

## Navigation Components

### Navbar
```html
<nav class="navbar">
  <div class="navbar-brand">
    <a href="#">Logo</a>
  </div>
  <ul class="navbar-nav">
    <li class="nav-item"><a href="#" class="nav-link">Home</a></li>
    <li class="nav-item"><a href="#" class="nav-link">About</a></li>
    <li class="nav-item"><a href="#" class="nav-link">Contact</a></li>
  </ul>
</nav>
```

### Breadcrumb
```html
<nav aria-label="breadcrumb">
  <ol class="breadcrumb">
    <li class="breadcrumb-item"><a href="#">Home</a></li>
    <li class="breadcrumb-item"><a href="#">Library</a></li>
    <li class="breadcrumb-item active">Data</li>
  </ol>
</nav>
```

## Modal Components

### Modal Dialog
```html
<div class="modal" id="exampleModal">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">Modal Title</h5>
        <button type="button" class="close" data-dismiss="modal">&times;</button>
      </div>
      <div class="modal-body">
        <p>Modal body content.</p>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
        <button type="button" class="btn btn-primary">Save changes</button>
      </div>
    </div>
  </div>
</div>
```

## Table Components

### Basic Table
```html
<table class="table">
  <thead>
    <tr>
      <th>#</th>
      <th>Name</th>
      <th>Email</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1</td>
      <td>John Doe</td>
      <td>john@example.com</td>
    </tr>
  </tbody>
</table>
```

### Striped Table
```html
<table class="table table-striped">
  <!-- Table content -->
</table>
```

## Alert Components

### Alert Types
```html
<div class="alert alert-success">Success message</div>
<div class="alert alert-info">Info message</div>
<div class="alert alert-warning">Warning message</div>
<div class="alert alert-danger">Error message</div>
```

## Badge Components

### Basic Badge
```html
<span class="badge badge-primary">New</span>
<span class="badge badge-secondary">Featured</span>
<span class="badge badge-success">Active</span>
<span class="badge badge-danger">Inactive</span>
```

## Progress Components

### Progress Bar
```html
<div class="progress">
  <div class="progress-bar" style="width: 75%">75%</div>
</div>
```

## Tooltip Components

### Tooltip
```html
<button class="btn btn-primary" data-toggle="tooltip" title="Tooltip text">
  Hover me
</button>
```

## Dropdown Components

### Dropdown Menu
```html
<div class="dropdown">
  <button class="btn btn-secondary dropdown-toggle" data-toggle="dropdown">
    Dropdown
  </button>
  <div class="dropdown-menu">
    <a class="dropdown-item" href="#">Action</a>
    <a class="dropdown-item" href="#">Another action</a>
  </div>
</div>
```

## Tabs Components

### Tab Navigation
```html
<ul class="nav nav-tabs">
  <li class="nav-item">
    <a class="nav-link active" href="#tab1">Tab 1</a>
  </li>
  <li class="nav-item">
    <a class="nav-link" href="#tab2">Tab 2</a>
  </li>
</ul>
<div class="tab-content">
  <div class="tab-pane active" id="tab1">Content 1</div>
  <div class="tab-pane" id="tab2">Content 2</div>
</div>
```

## Pagination Components

### Pagination
```html
<nav>
  <ul class="pagination">
    <li class="page-item"><a class="page-link" href="#">Previous</a></li>
    <li class="page-item active"><a class="page-link" href="#">1</a></li>
    <li class="page-item"><a class="page-link" href="#">2</a></li>
    <li class="page-item"><a class="page-link" href="#">3</a></li>
    <li class="page-item"><a class="page-link" href="#">Next</a></li>
  </ul>
</nav>
```

## Layout Components

### Container
```html
<div class="container">
  <!-- Content -->
</div>
```

### Grid System
```html
<div class="row">
  <div class="col-6">Column 1</div>
  <div class="col-6">Column 2</div>
</div>
```

### Flexbox Layout
```html
<div class="d-flex justify-content-between align-items-center">
  <div>Left</div>
  <div>Center</div>
  <div>Right</div>
</div>
```
