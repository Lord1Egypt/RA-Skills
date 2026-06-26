# Drupal Theming Reference

Comprehensive guide to Drupal theming for Drupal 8-11+.

## Theme Structure

```
mytheme/
├── mytheme.info.yml          # Theme metadata (required)
├── mytheme.libraries.yml     # CSS/JS libraries
├── mytheme.theme             # Theme functions and preprocess
├── mytheme.breakpoints.yml   # Responsive breakpoints
├── logo.svg                  # Theme logo
├── screenshot.png            # Admin screenshot
├── composer.json             # Composer dependencies
├── package.json              # NPM dependencies (if using build tools)
├── config/
│   ├── install/             # Default configuration
│   └── schema/              # Configuration schema
├── css/
│   ├── base/
│   ├── components/
│   ├── layout/
│   └── theme/
├── js/
│   └── custom.js
├── images/
├── templates/
│   ├── block/
│   ├── content/
│   ├── field/
│   ├── layout/
│   ├── navigation/
│   ├── views/
│   ├── page.html.twig
│   ├── node.html.twig
│   └── block.html.twig
└── src/                     # Optional PHP classes
    └── Plugin/
        └── Preprocess/
```

## Theme Info File (mytheme.info.yml)

```yaml
name: My Theme
type: theme
description: 'A custom Drupal theme'
core_version_requirement: ^9 || ^10 || ^11
package: Custom

# Base theme
base theme: stable9
# Or for no base theme:
# base theme: false

# Regions
regions:
  header: Header
  primary_menu: 'Primary menu'
  secondary_menu: 'Secondary menu'
  page_top: 'Page top'
  page_bottom: 'Page bottom'
  highlighted: Highlighted
  breadcrumb: Breadcrumb
  content: Content
  sidebar_first: 'Sidebar first'
  sidebar_second: 'Sidebar second'
  footer: Footer

# Libraries to load on all pages
libraries:
  - mytheme/global-styling
  - mytheme/global-scripts

# Libraries to load only when certain conditions are met
libraries-override:
  # Replace core library
  core/drupal.dialog:
    mytheme/custom-dialog: {}

libraries-extend:
  # Add to existing library
  core/drupal.dialog:
    - mytheme/dialog-extend

# Remove libraries
libraries-override:
  core/normalize:
    css:
      base:
        assets/vendor/normalize-css/normalize.css: false

# Component libraries (for single-directory components)
component-libraries:
  atoms:
    paths:
      - components/atoms
  molecules:
    paths:
      - components/molecules

# Logo and favicon
logo: images/logo.svg
favicon: images/favicon.ico

# Stylesheets to remove
stylesheets-remove:
  - core/assets/vendor/normalize-css/normalize.css
  - '@classy/css/components/tabs.css'

# CKEditor stylesheet
ckeditor_stylesheets:
  - css/ckeditor.css

# Hidden theme (for base themes)
hidden: false
```

## Libraries (mytheme.libraries.yml)

```yaml
global-styling:
  version: 1.0
  css:
    base:
      css/base/reset.css: {}
    layout:
      css/layout/layout.css: {}
    component:
      css/components/button.css: {}
      css/components/card.css: {}
    theme:
      css/theme/colors.css: {}
      css/theme/typography.css: {}

global-scripts:
  version: 1.0
  js:
    js/custom.js: {}
  dependencies:
    - core/drupal
    - core/jquery

# Conditional library (loaded via preprocess or template)
modal:
  version: 1.0
  css:
    component:
      css/components/modal.css: {}
  js:
    js/modal.js: {}
  dependencies:
    - core/drupal
    - core/drupalSettings

# External library
fontawesome:
  version: 6.0
  css:
    theme:
      https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css: { type: external, minified: true }

# SCSS/SASS (requires compilation)
compiled-styles:
  version: 1.0
  css:
    theme:
      dist/css/styles.css: {}
  dependencies:
    - core/normalize
```

## Theme Functions (mytheme.theme)

```php
<?php

/**
 * @file
 * Functions to support theming in the My Theme theme.
 */

use Drupal\Core\Form\FormStateInterface;
use Drupal\node\NodeInterface;

/**
 * Implements hook_preprocess_HOOK() for page templates.
 */
function mytheme_preprocess_page(&$variables) {
  // Add custom variable to all pages
  $variables['site_slogan'] = \Drupal::config('system.site')->get('slogan');

  // Add body classes
  $variables['attributes']['class'][] = 'custom-page-class';
}

/**
 * Implements hook_preprocess_HOOK() for node templates.
 */
function mytheme_preprocess_node(&$variables) {
  /** @var \Drupal\node\NodeInterface $node */
  $node = $variables['node'];

  // Add custom variables
  $variables['created_date'] = \Drupal::service('date.formatter')->format(
    $node->getCreatedTime(),
    'custom',
    'F j, Y'
  );

  // Add template suggestions
  $variables['theme_hook_suggestions'][] = 'node__' . $node->bundle() . '__' . $variables['view_mode'];
}

/**
 * Implements hook_preprocess_HOOK() for block templates.
 */
function mytheme_preprocess_block(&$variables) {
  // Add block ID as class
  if (isset($variables['elements']['#id'])) {
    $variables['attributes']['class'][] = 'block-' . $variables['elements']['#id'];
  }
}

/**
 * Implements hook_preprocess_HOOK() for field templates.
 */
function mytheme_preprocess_field(&$variables) {
  $element = $variables['element'];

  // Custom preprocessing for specific fields
  if ($element['#field_name'] == 'field_custom') {
    $variables['custom_class'] = 'field-custom-class';
  }
}

/**
 * Implements hook_theme_suggestions_HOOK_alter() for page templates.
 */
function mytheme_theme_suggestions_page_alter(array &$suggestions, array $variables) {
  // Add template suggestions based on current route
  if ($node = \Drupal::routeMatch()->getParameter('node')) {
    if ($node instanceof NodeInterface) {
      $suggestions[] = 'page__node__' . $node->bundle();
      $suggestions[] = 'page__node__' . $node->id();
    }
  }
}

/**
 * Implements hook_theme_suggestions_HOOK_alter() for node templates.
 */
function mytheme_theme_suggestions_node_alter(array &$suggestions, array $variables) {
  /** @var \Drupal\node\NodeInterface $node */
  $node = $variables['elements']['#node'];
  $view_mode = $variables['elements']['#view_mode'];

  // Add suggestion for bundle and view mode combination
  $suggestions[] = 'node__' . $node->bundle() . '__' . $view_mode;
}

/**
 * Implements hook_form_alter().
 */
function mytheme_form_alter(&$form, FormStateInterface $form_state, $form_id) {
  // Add custom classes to forms
  if ($form_id == 'search_block_form') {
    $form['actions']['submit']['#attributes']['class'][] = 'custom-search-submit';
  }
}

/**
 * Implements hook_page_attachments_alter().
 */
function mytheme_page_attachments_alter(array &$attachments) {
  // Add custom meta tags
  $meta_charset = [
    '#tag' => 'meta',
    '#attributes' => [
      'charset' => 'utf-8',
    ],
  ];
  $attachments['#attached']['html_head'][] = [$meta_charset, 'meta_charset'];
}

/**
 * Implements hook_library_info_alter().
 */
function mytheme_library_info_alter(&$libraries, $extension) {
  // Modify libraries from other modules
  if ($extension == 'core' && isset($libraries['drupal.dialog'])) {
    $libraries['drupal.dialog']['dependencies'][] = 'mytheme/custom-dialog';
  }
}
```

## Twig Templates

### page.html.twig
```twig
<div class="layout-container">
  <header role="banner">
    {{ page.header }}
    {{ page.primary_menu }}
  </header>

  {{ page.breadcrumb }}
  {{ page.highlighted }}

  <main role="main" class="main-content">
    <a id="main-content" tabindex="-1"></a>

    <div class="layout-content">
      {{ page.content }}
    </div>

    {% if page.sidebar_first %}
      <aside class="sidebar sidebar--first" role="complementary">
        {{ page.sidebar_first }}
      </aside>
    {% endif %}

    {% if page.sidebar_second %}
      <aside class="sidebar sidebar--second" role="complementary">
        {{ page.sidebar_second }}
      </aside>
    {% endif %}
  </main>

  {% if page.footer %}
    <footer role="contentinfo">
      {{ page.footer }}
    </footer>
  {% endif %}
</div>
```

### node.html.twig
```twig
<article{{ attributes.addClass('node', 'node--type-' ~ node.bundle|clean_class, node.isPromoted() ? 'node--promoted', node.isSticky() ? 'node--sticky', not node.isPublished() ? 'node--unpublished', view_mode ? 'node--view-mode-' ~ view_mode|clean_class) }}>

  {{ title_prefix }}
  {% if not page %}
    <h2{{ title_attributes.addClass('node__title') }}>
      <a href="{{ url }}" rel="bookmark">{{ label }}</a>
    </h2>
  {% endif %}
  {{ title_suffix }}

  {% if display_submitted %}
    <div class="node__meta">
      {{ author_picture }}
      <span{{ author_attributes }}>
        {% trans %}Submitted by {{ author_name }} on {{ date }}{% endtrans %}
      </span>
      {{ metadata }}
    </div>
  {% endif %}

  <div{{ content_attributes.addClass('node__content') }}>
    {{ content }}
  </div>

</article>
```

### block.html.twig
```twig
<div{{ attributes.addClass('block', 'block-' ~ configuration.provider|clean_class, 'block-' ~ plugin_id|clean_class) }}>
  {{ title_prefix }}
  {% if label %}
    <h2{{ title_attributes }}>{{ label }}</h2>
  {% endif %}
  {{ title_suffix }}

  {% block content %}
    {{ content }}
  {% endblock %}
</div>
```

### field.html.twig
```twig
{% if multiple %}
  <div{{ attributes.addClass('field', 'field--name-' ~ field_name|clean_class, 'field--type-' ~ field_type|clean_class) }}>
    {% if label %}
      <div{{ title_attributes.addClass('field__label') }}>{{ label }}</div>
    {% endif %}
    <div class="field__items">
      {% for item in items %}
        <div{{ item.attributes.addClass('field__item') }}>{{ item.content }}</div>
      {% endfor %}
    </div>
  </div>
{% else %}
  {% for item in items %}
    <div{{ attributes.addClass('field', 'field--name-' ~ field_name|clean_class, 'field--type-' ~ field_type|clean_class) }}>
      {% if label %}
        <div{{ title_attributes.addClass('field__label') }}>{{ label }}</div>
      {% endif %}
      <div{{ item.attributes.addClass('field__item') }}>{{ item.content }}</div>
    </div>
  {% endfor %}
{% endif %}
```

## Twig Filters & Functions

### Common Filters
```twig
{# Translate #}
{{ 'Hello World'|t }}

{# Clean class name #}
{{ 'Field Name'|clean_class }}

{# Format date #}
{{ node.created.value|date('F j, Y') }}

{# Safe join #}
{{ items|safe_join(', ') }}

{# Render #}
{{ content|render }}

{# Without (remove array elements) #}
{{ content|without('field_image') }}

{# Placeholder #}
{{ 'Hello @name'|t({'@name': name}) }}
```

### Common Functions
```twig
{# Attach library #}
{{ attach_library('mytheme/modal') }}

{# URL #}
<a href="{{ url('entity.node.canonical', {'node': node.id}) }}">Link</a>

{# Path #}
<a href="{{ path('entity.node.canonical', {'node': node.id}) }}">Link</a>

{# File URL #}
{{ file_url('public://image.jpg') }}

{# Create attribute #}
{% set attributes = create_attribute() %}
{{ attributes.addClass('custom-class') }}
```

## Breakpoints (mytheme.breakpoints.yml)

```yaml
mytheme.mobile:
  label: Mobile
  mediaQuery: 'screen and (min-width: 0px)'
  weight: 0
  multipliers:
    - 1x
    - 2x

mytheme.tablet:
  label: Tablet
  mediaQuery: 'screen and (min-width: 768px)'
  weight: 1
  multipliers:
    - 1x
    - 2x

mytheme.desktop:
  label: Desktop
  mediaQuery: 'screen and (min-width: 1024px)'
  weight: 2
  multipliers:
    - 1x
    - 2x

mytheme.wide:
  label: Wide
  mediaQuery: 'screen and (min-width: 1440px)'
  weight: 3
  multipliers:
    - 1x
```

## Debug Mode

Enable Twig debugging in development:

**sites/default/services.yml**
```yaml
parameters:
  twig.config:
    debug: true
    auto_reload: true
    cache: false
```

Then clear cache:
```bash
ddev drush cr
```

## Theme Development Workflow

1. **Enable development settings**
   ```bash
   # Copy and enable development settings
   cp sites/example.settings.local.php sites/default/settings.local.php
   ```

2. **Disable CSS/JS aggregation**
   - Go to `/admin/config/development/performance`
   - Uncheck "Aggregate CSS files"
   - Uncheck "Aggregate JavaScript files"

3. **Clear cache frequently**
   ```bash
   ddev drush cr
   ```

4. **Use Twig debugging**
   - Check HTML source for template suggestions
   - Look for `<!-- BEGIN OUTPUT -->` comments

5. **Rebuild theme registry**
   ```bash
   ddev drush drush cr
   ```

## Best Practices

1. **BEM Methodology**: Use BEM for CSS class naming
2. **Component-based**: Build reusable components
3. **Accessibility**: Follow WCAG guidelines
4. **Performance**: Optimize images, minimize CSS/JS
5. **Mobile-first**: Design for mobile, enhance for desktop
6. **Semantic HTML**: Use proper HTML5 elements
7. **Template suggestions**: Use specific templates when needed
8. **Libraries**: Group related CSS/JS in libraries
9. **Preprocessing**: Keep logic in .theme file, not templates
10. **Documentation**: Comment complex template logic

## Common Template Suggestions

```
page--front.html.twig                  # Front page
page--node--123.html.twig              # Specific node
page--node--article.html.twig          # Content type
node--article--full.html.twig          # Bundle and view mode
node--123.html.twig                    # Specific node
block--system-branding-block.html.twig # Specific block
field--node--title--article.html.twig  # Specific field
views-view--blog--page-1.html.twig     # View and display
```

## Useful Resources

- Theming Guide: https://www.drupal.org/docs/theming-drupal
- Twig Documentation: https://twig.symfony.com/doc/
- Template Suggestions: https://www.drupal.org/docs/theming-drupal/twig-in-drupal/debugging-twig-templates
