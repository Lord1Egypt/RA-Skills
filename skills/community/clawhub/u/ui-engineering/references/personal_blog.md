---
name: ui-spec-personal-blog
description: Detailed engineering specification for implementing "Digital Garden" or "Clean Paper" style personal blogs.
license: MIT
---

# UI Engineering Spec: Personal Blog

## 1. Engineering Context (The "Why")
**Mental Model**: "The Digital Garden" or "Clean Paper".
This style prioritizes the reading experience above all else. It is a sanctuary for thought, free from the noise of social media or marketing-heavy sites. It is fast, accessible, and typographically excellent.

**Key Traits**:
- **Typography-First**: The typeface is the main UI.
- **Breathable**: Generous whitespace and margins.
- **Fast**: Static Site Generation (SSG) for sub-100ms loads.
- **Timeless**: Avoids trendy interactions that might age quickly.

## 2. Tech Stack Recommendations
- **Framework**: Next.js (App Router) or Astro (perfect for content-heavy sites).
- **Content**: MDX (Markdown + React Components).
- **Styling**: Tailwind CSS + `@tailwindcss/typography` (The `prose` plugin is essential).
- **State**: Minimal. React Server Components (RSC) should handle most logic.

## 3. Design Tokens (The "Paper")

### 3.1 Colors (Comfortable Contrast)
Avoid pure black on pure white, which can cause eye strain.
- **Bg**: `#FFFCF9` (Warm Paper) or `#F8FAFC` (Cool Slate).
- **Text**: `#1e293b` (Slate 800) for high contrast but not harsh black.
- **Accent**: A subtle color for links, e.g., `#0891b2` (Cyan 600) or `#db2777` (Pink 600).

### 3.2 Typography (The Voice)
- **Body**: A high-readability Serif.
    - *Options*: `Merriweather` (Classic), `Newsreader` (Elegant), `Lora` (Calligraphic).
- **Headings**: A clean Sans-Serif or a contrasting Display Serif.
    - *Options*: `Inter`, `Geist Sans`, or `Playfair Display`.
- **Scale**:
    - Body: `1.125rem` (18px) or `1.25rem` (20px). Large text is better.
    - Line-height: `1.75` for body text.

### 3.3 Layout
- **Reading Column**: Max-width `65ch` (characters). This is the golden rule for readability.
- **Container**: `max-w-3xl mx-auto px-6`.

## 4. Component Recipes

### The "Prose Wrapper" (Tailwind)
The core container for your Markdown content.

```tsx
<article className="prose prose-lg prose-slate dark:prose-invert mx-auto">
  {/* MDX Content goes here */}
  {children}
</article>
```

### The "Minimal Header"
Focus on the title and metadata.

```tsx
<header className="mb-10 text-center">
  <div className="text-sm font-medium text-slate-500 mb-4 uppercase tracking-widest">
    {date} • {readingTime} min read
  </div>
  <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight text-slate-900 dark:text-white mb-6">
    {title}
  </h1>
  <div className="flex justify-center gap-4">
     {tags.map(tag => (
        <span key={tag} className="bg-slate-100 text-slate-600 px-3 py-1 rounded-full text-xs font-bold">
           #{tag}
        </span>
     ))}
  </div>
</header>
```

### The "Newsletter Box"
A non-intrusive invitation to subscribe.

```tsx
<div className="bg-slate-50 border border-slate-200 rounded-2xl p-8 my-16 text-center">
  <h3 className="text-xl font-bold mb-2">Join the garden</h3>
  <p className="text-slate-600 mb-6">I write monthly. No spam, just thoughts.</p>
  <form className="flex gap-2 max-w-sm mx-auto">
    <input 
      type="email" 
      placeholder="your@email.com" 
      className="flex-1 px-4 py-2 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-500 outline-none" 
    />
    <button className="bg-slate-900 text-white px-6 py-2 rounded-lg font-bold hover:bg-slate-800 transition">
      Subscribe
    </button>
  </form>
</div>
```

## 5. Interaction Patterns
- **No Sticky Headers**: Let the user focus on reading. When they scroll down, the UI disappears.
- **Table of Contents**: Sticky sidebar on desktop, collapsible detail on mobile.
- **Code Blocks**: High-contrast syntax highlighting (e.g., Catppuccin or Dracula theme).
- **Images**: `rounded-xl` with subtle `shadow-lg` and captions below.

## 6. SEO & Social
- **Meta Tags**: Essential. `og:image`, `twitter:card`.
- **RSS Feed**: Mandatory for a personal blog.
- **Sitemap**: Auto-generated.
