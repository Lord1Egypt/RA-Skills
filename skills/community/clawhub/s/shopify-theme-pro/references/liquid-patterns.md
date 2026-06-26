# Liquid Patterns Reference

Common Liquid templating patterns for Shopify theme development.

## Modular Section Pattern

**Purpose:** Build customizable sections with blocks.

```liquid
{%- # sections/feature-grid.liquid -%}
<div class="feature-grid" style="--columns: {{ section.settings.columns }}">
  {% for block in section.blocks %}
    <div class="feature-item" {{ block.shopify_attributes }}>
      {% if block.settings.image %}
        {{ block.settings.image | image_url: width: 400 | image_tag: loading: 'lazy' }}
      {% endif %}
      <h3>{{ block.settings.heading }}</h3>
      <p>{{ block.settings.text }}</p>
    </div>
  {% endfor %}
</div>

{% schema %}
{
  "name": "Feature Grid",
  "settings": [
    {
      "type": "range",
      "id": "columns",
      "min": 2,
      "max": 4,
      "step": 1,
      "default": 3,
      "label": "Columns"
    }
  ],
  "blocks": [
    {
      "type": "feature",
      "name": "Feature",
      "settings": [
        {
          "type": "image_picker",
          "id": "image",
          "label": "Image"
        },
        {
          "type": "text",
          "id": "heading",
          "label": "Heading"
        },
        {
          "type": "textarea",
          "id": "text",
          "label": "Text"
        }
      ]
    }
  ],
  "presets": [
    {
      "name": "Feature Grid",
      "blocks": [
        { "type": "feature" },
        { "type": "feature" },
        { "type": "feature" }
      ]
    }
  ]
}
{% endschema %}
```

**Key Concepts:**
- `section.blocks` — Array of blocks added by merchant
- `block.shopify_attributes` — Required for theme editor integration
- `presets` — Default configuration when section is added

---

## Reusable Snippet Pattern

**Purpose:** DRY code for components used across templates.

```liquid
{%- # snippets/product-card.liquid -%}
{%- # Usage: {% render 'product-card', product: product, show_vendor: true %} -%}

<div class="product-card">
  <a href="{{ product.url }}">
    {% if product.featured_image %}
      {{ product.featured_image | image_url: width: 400 | image_tag: loading: 'lazy', alt: product.title }}
    {% endif %}

    {% if show_vendor %}
      <p class="vendor">{{ product.vendor }}</p>
    {% endif %}

    <h3>{{ product.title }}</h3>
    <p class="price">
      {% if product.compare_at_price > product.price %}
        <span class="price--sale">{{ product.price | money }}</span>
        <span class="price--compare">{{ product.compare_at_price | money }}</span>
      {% else %}
        {{ product.price | money }}
      {% endif %}
    </p>

    {% if product.available %}
      <span class="badge">{{ 'products.available' | t }}</span>
    {% else %}
      <span class="badge badge--sold-out">{{ 'products.sold_out' | t }}</span>
    {% endif %}
  </a>
</div>
```

**Best Practices:**
- Accept parameters for flexibility
- Use translation keys (`{{ 'key' | t }}`)
- Include alt text for accessibility
- Handle edge cases (no image, sold out, sale price)

---

## Product Variant Selector

**Purpose:** Dropdown for variant selection with JavaScript integration.

```liquid
{%- # snippets/variant-selector.liquid -%}
<div class="variant-selector">
  <label for="variant-select">{{ 'products.select_variant' | t }}</label>
  <select id="variant-select" name="id">
    {% for variant in product.variants %}
      <option
        value="{{ variant.id }}"
        {% unless variant.available %}disabled{% endunless %}
        data-price="{{ variant.price | money }}"
      >
        {{ variant.title }}
        {% unless variant.available %} - {{ 'products.sold_out' | t }}{% endunless %}
      </option>
    {% endfor %}
  </select>
</div>

<script>
  document.getElementById('variant-select').addEventListener('change', function(e) {
    const selectedOption = e.target.selectedOptions[0];
    const price = selectedOption.dataset.price;
    document.querySelector('.product-price').textContent = price;
  });
</script>
```

---

## Metafield Access Pattern

**Purpose:** Display custom metafield data.

```liquid
{%- # Access product metafield -%}
{% if product.metafields.custom.ingredients %}
  <div class="product-ingredients">
    <h4>{{ 'products.ingredients' | t }}</h4>
    <p>{{ product.metafields.custom.ingredients }}</p>
  </div>
{% endif %}

{%- # Access with fallback -%}
{% assign warranty = product.metafields.custom.warranty | default: '1 year' %}
<p>{{ 'products.warranty' | t }}: {{ warranty }}</p>

{%- # Rich text metafield -%}
{% if product.metafields.custom.care_instructions.type == 'rich_text_field' %}
  <div class="care-instructions">
    {{ product.metafields.custom.care_instructions | metafield_tag }}
  </div>
{% endif %}
```

**Metafield Namespace Structure:**
- `product.metafields.namespace.key`
- Common namespaces: `custom`, `descriptors`, `facts`

---

## Collection Filtering Pattern

**Purpose:** Filter products in a collection.

```liquid
{%- # templates/collection.liquid -%}
<div class="collection-filters">
  <form id="filter-form">
    <label>
      <input type="checkbox" name="filter.p.vendor" value="Nike">
      Nike
    </label>
    <label>
      <input type="checkbox" name="filter.p.vendor" value="Adidas">
      Adidas
    </label>
  </form>
</div>

<div class="product-grid">
  {% for product in collection.products %}
    {% render 'product-card', product: product %}
  {% endfor %}
</div>

<script>
  document.getElementById('filter-form').addEventListener('change', function(e) {
    const formData = new FormData(e.currentTarget);
    const params = new URLSearchParams(formData);
    window.location.search = params.toString();
  });
</script>
```

---

## Pagination Pattern

**Purpose:** Navigate through paginated results.

```liquid
{%- # Pagination for collections/blogs -%}
{% if paginate.pages > 1 %}
  <nav class="pagination" role="navigation">
    {% if paginate.previous %}
      <a href="{{ paginate.previous.url }}" class="pagination__prev">
        {{ 'pagination.previous' | t }}
      </a>
    {% endif %}

    {% for part in paginate.parts %}
      {% if part.is_link %}
        <a href="{{ part.url }}">{{ part.title }}</a>
      {% else %}
        {% if part.title == paginate.current_page %}
          <span class="pagination__current" aria-current="page">{{ part.title }}</span>
        {% else %}
          <span>{{ part.title }}</span>
        {% endif %}
      {% endif %}
    {% endfor %}

    {% if paginate.next %}
      <a href="{{ paginate.next.url }}" class="pagination__next">
        {{ 'pagination.next' | t }}
      </a>
    {% endif %}
  </nav>
{% endif %}
```

**Wrap collection loop:**
```liquid
{% paginate collection.products by 12 %}
  {% for product in collection.products %}
    {%- # product display -%}
  {% endfor %}
  {% render 'pagination', paginate: paginate %}
{% endpaginate %}
```

---

## Breadcrumbs Pattern

**Purpose:** Navigation trail for SEO and UX.

```liquid
{%- # snippets/breadcrumbs.liquid -%}
<nav class="breadcrumbs" aria-label="Breadcrumb">
  <ol itemscope itemtype="https://schema.org/BreadcrumbList">
    <li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
      <a href="/" itemprop="item">
        <span itemprop="name">{{ 'general.breadcrumbs.home' | t }}</span>
      </a>
      <meta itemprop="position" content="1" />
    </li>

    {% if collection %}
      <li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
        <a href="{{ collection.url }}" itemprop="item">
          <span itemprop="name">{{ collection.title }}</span>
        </a>
        <meta itemprop="position" content="2" />
      </li>
    {% endif %}

    {% if product %}
      <li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
        <span itemprop="name">{{ product.title }}</span>
        <meta itemprop="position" content="3" />
      </li>
    {% endif %}
  </ol>
</nav>
```

---

## Responsive Image Pattern

**Purpose:** Serve appropriately sized images.

```liquid
{%- # Basic responsive image -%}
{{ product.featured_image | image_url: width: 800 | image_tag: loading: 'lazy', sizes: '(min-width: 768px) 50vw, 100vw' }}

{%- # Advanced srcset -%}
<img
  src="{{ product.featured_image | image_url: width: 800 }}"
  srcset="
    {{ product.featured_image | image_url: width: 400 }} 400w,
    {{ product.featured_image | image_url: width: 800 }} 800w,
    {{ product.featured_image | image_url: width: 1200 }} 1200w
  "
  sizes="(min-width: 1024px) 33vw, (min-width: 768px) 50vw, 100vw"
  alt="{{ product.title | escape }}"
  loading="lazy"
  width="800"
  height="800"
>
```

**Key Attributes:**
- `loading="lazy"` — Defer off-screen images
- `sizes` — Tell browser which size to use at different viewports
- `width`/`height` — Prevent layout shift

---

## Dynamic Section Rendering

**Purpose:** Render sections outside their default template context.

```liquid
{%- # Render a section dynamically -%}
{% section 'featured-collection' %}

{%- # Render with custom settings -%}
{% section 'hero-banner' with collection: collections['best-sellers'] %}
```

**Use Cases:**
- Modular homepage layouts
- Reusable promotional banners
- Conditional section display

---

## Translation Pattern

**Purpose:** Multi-language support.

```liquid
{%- # Basic translation -%}
{{ 'cart.add_to_cart' | t }}

{%- # Translation with variable -%}
{{ 'products.price_html' | t: price: product.price | money }}

{%- # Fallback -%}
{{ product.metafields.custom.title_override | default: product.title }}
```

**Locale File (`locales/en.default.json`):**
```json
{
  "cart": {
    "add_to_cart": "Add to Cart"
  },
  "products": {
    "price_html": "Price: {{ price }}"
  }
}
```

---

## Custom Form Handling

**Purpose:** Contact forms, newsletter signups, custom submissions.

```liquid
{%- # snippets/newsletter-form.liquid -%}
{% form 'customer', class: 'newsletter-form' %}
  {% if form.posted_successfully? %}
    <p class="form-success">{{ 'newsletter.success' | t }}</p>
  {% endif %}

  {% if form.errors %}
    <div class="form-errors">
      {{ form.errors | default_errors }}
    </div>
  {% endif %}

  <label for="email">{{ 'newsletter.email_label' | t }}</label>
  <input
    type="email"
    name="contact[email]"
    id="email"
    placeholder="{{ 'newsletter.email_placeholder' | t }}"
    required
  >

  <button type="submit">{{ 'newsletter.submit' | t }}</button>
{% endform %}
```

---

## Schema Reference

**Common Setting Types:**

| Type | Purpose | Example Value |
|------|---------|---------------|
| `text` | Short text input | "Welcome to our store" |
| `textarea` | Multi-line text | "Long description..." |
| `richtext` | WYSIWYG editor | `<p>Formatted content</p>` |
| `html` | Raw HTML input | Custom code |
| `image_picker` | Image selector | Image object |
| `color` | Color picker | `#000000` |
| `font_picker` | Font selector | `helvetica_n4` |
| `collection` | Collection selector | Collection object |
| `product` | Product selector | Product object |
| `blog` | Blog selector | Blog object |
| `url` | URL input | `/pages/about` |
| `range` | Slider | Integer (2-12) |
| `checkbox` | Boolean toggle | `true`/`false` |
| `select` | Dropdown | Selected option |
| `radio` | Radio buttons | Selected value |

**Example Schema:**
```json
{
  "name": "Hero Banner",
  "settings": [
    {
      "type": "image_picker",
      "id": "background_image",
      "label": "Background Image"
    },
    {
      "type": "text",
      "id": "heading",
      "label": "Heading",
      "default": "Welcome"
    },
    {
      "type": "richtext",
      "id": "text",
      "label": "Description"
    },
    {
      "type": "url",
      "id": "cta_link",
      "label": "Button Link"
    },
    {
      "type": "text",
      "id": "cta_text",
      "label": "Button Text",
      "default": "Shop Now"
    }
  ]
}
```

---

**Last Updated:** 2026-03-13
