# Website Reproduction Examples

## Example 1: Simple Landing Page

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Landing Page Example</title>
  <style>
    :root {
      --primary: #2563eb;
      --text-dark: #1f2937;
      --text-light: #6b7280;
      --bg-light: #f9fafb;
    }
    
    * { margin: 0; padding: 0; box-sizing: border-box; }
    
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      line-height: 1.6;
      color: var(--text-dark);
    }
    
    .hero {
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      text-align: center;
      padding: 2rem;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
    }
    
    .hero h1 { font-size: 3rem; margin-bottom: 1rem; }
    .hero p { font-size: 1.25rem; opacity: 0.9; max-width: 600px; }
    
    .btn {
      margin-top: 2rem;
      padding: 1rem 2rem;
      background: white;
      color: var(--primary);
      border: none;
      border-radius: 8px;
      font-size: 1rem;
      cursor: pointer;
      transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .btn:hover {
      transform: translateY(-2px);
      box-shadow: 0 10px 20px rgba(0,0,0,0.2);
    }
  </style>
</head>
<body>
  <section class="hero">
    <h1>Product Name</h1>
    <p>Concise and compelling product description, highlighting value proposition</p>
    <button class="btn">Get Started</button>
  </section>
</body>
</html>
```

## Example 2: Navigation + Content Layout

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Navigation Layout Example</title>
  <style>
    :root {
      --header-height: 64px;
      --sidebar-width: 240px;
    }
    
    * { margin: 0; padding: 0; box-sizing: border-box; }
    
    body {
      font-family: system-ui, sans-serif;
    }
    
    /* Navigation bar */
    .navbar {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      height: var(--header-height);
      background: #fff;
      border-bottom: 1px solid #e5e7eb;
      display: flex;
      align-items: center;
      padding: 0 2rem;
      z-index: 100;
    }
    
    .navbar__logo { font-weight: 700; font-size: 1.25rem; }
    
    .navbar__menu {
      display: flex;
      gap: 2rem;
      margin-left: auto;
      list-style: none;
    }
    
    .navbar__link {
      text-decoration: none;
      color: #4b5563;
      transition: color 0.2s;
    }
    
    .navbar__link:hover { color: #2563eb; }
    
    /* Sidebar + Main content */
    .layout {
      display: flex;
      padding-top: var(--header-height);
      min-height: 100vh;
    }
    
    .sidebar {
      width: var(--sidebar-width);
      background: #f9fafb;
      padding: 1.5rem;
      border-right: 1px solid #e5e7eb;
    }
    
    .main {
      flex: 1;
      padding: 2rem;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
      .sidebar { display: none; }
      .navbar__menu { display: none; }
    }
  </style>
</head>
<body>
  <header class="navbar">
    <div class="navbar__logo">Brand</div>
    <ul class="navbar__menu">
      <li><a href="#" class="navbar__link">Home</a></li>
      <li><a href="#" class="navbar__link">Products</a></li>
      <li><a href="#" class="navbar__link">About</a></li>
    </ul>
  </header>
  
  <div class="layout">
    <aside class="sidebar">
      <nav><!-- Sidebar navigation --></nav>
    </aside>
    <main class="main">
      <h1>Main Content Area</h1>
      <p>This is the main content of the page...</p>
    </main>
  </div>
</body>
</html>
```

## Example 3: Card Grid

```html
<section class="card-grid">
  <article class="card">
    <img src="https://picsum.photos/400/300" alt="Placeholder" class="card__image">
    <div class="card__content">
      <h3 class="card__title">Card Title</h3>
      <p class="card__desc">Card description text</p>
    </div>
  </article>
  <!-- More cards... -->
</section>

<style>
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
  padding: 2rem;
}

.card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  transition: transform 0.2s, box-shadow 0.2s;
}

.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0,0,0,0.15);
}

.card__image {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.card__content { padding: 1.5rem; }
.card__title { font-size: 1.125rem; margin-bottom: 0.5rem; }
.card__desc { color: #6b7280; font-size: 0.875rem; }
</style>
```