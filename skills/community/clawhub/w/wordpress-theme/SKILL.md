# WordPress Theme Conversion Skill
This skill guides the conversion of static HTML/CSS/JS websites into WordPress themes. It ensures consistent patterns, proper WordPress integration, and maintains design fidelity.
## When to Use
Invoke this skill when:
- User asks to create a WordPress theme from static files
- User wants to convert existing website to WordPress
- User wants to add WordPress functionality to a static site
- Creating a theme from scratch or migrating from another CMS
## Workflow
### Step 1: Analyze Source Files
1. Identify all HTML templates (index, detail, about, etc.)
2. Map CSS structure and patterns
3. Identify JavaScript interactions
4. Note custom fonts and external resources
5. Document color scheme and design tokens
### Step 2: Create Theme Structure
Create the following directory structure:
```
theme-name/
├── style.css          # Theme header (must have)
├── functions.php      # Theme functions
├── header.php        # Header template
├── footer.php       # Footer template
├── index.php        # Homepage template
├── front-page.php   # Static front page
├── singular.php    # Single post template
├── archive.php     # Archive template
├── search.php      # Search template
├── 404.php        # 404 template
├── sidebar.php     # Sidebar template
├── comments.php    # Comments template
├── css/
│   └── style.css  # Compiled styles
├── js/
│   └── main.js   # Scripts
└── inc/
    ├── setup.php    # Theme setup
    ├── enqueue.php  # Scripts/styles
    ├── customizer.php # Customizer
    └── widgets.php # Widgets
```
### Step 3: Convert style.css
Add WordPress theme header to existing CSS:
```css
/*
Theme Name: Theme Name
Theme URI: https://example.com
Author: Author Name
Author URI: https://example.com
Description: Theme description
Version: 1.0.0
License: GNU General Public License v2 or later
License URI: http://www.gnu.org/ licenses/gpl-2.0. html
Text Domain: theme-slug
Tags: custom- logo, custom-menu, featured-images, translation-ready
*/
```
### Step 4: Create functions.php
Include essential theme setup:
```php
<?php
if (!defined('ABSPATH')) exit;
define('THEME_VERSION', '1.0.0');
function theme_theme_setup() {
    add_ theme_support('title-tag');
    add_theme_support('post-thumbnails');
    register_nav_menus( array(
        'primary' => 'Primary Menu',
        'footer' => 'Footer Menu',
    ));
}
add_action('after_setup_theme', 'theme_theme_setup');
function theme_enqueue_scripts() {
    wp_enqueue_style('theme-style', get_stylesheet_uri(), array(), THEME_VERSION);
    wp_enqueue_script('theme-main', get_template_directory_uri() . '/js/main.js', array('jquery'), THEME_VERSION, true);
}
add_action('wp_enqueue_scripts', 'theme_enqueue_scripts');
```
### Step 5: Convert Templates
Replace static content with WordPress functions:
| Static | WordPress | Notes |
|--------|----------|-------|
| `<title>` | `wp_title()` / `wp_get_document_title()` | Use `add_theme_support('title-tag')` |
| `<link rel="stylesheet">` | `wp_head()` | No manual link needed |
| `<script src>` | `wp_footer()` | No manual script needed |
| Static text | `bloginfo('name')`, `bloginfo('description')` | Dynamic content |
| Static menu | `wp_nav_menu()` | Use `has_nav_menu()` check |
| Static image | `the_post_thumbnail()` | Use `has_post_thumbnail()` check |
| Static posts loop | `while (have_posts())` | WordPress Loop |
| Static URL | `home_url()` | Use `esc_url()` |
### Step 6: Header Template
```php
<!DOCTYPE html>
<html <?php language_attributes(); ?>>
<head>
    <meta charset="<?php bloginfo('charset'); ?>">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <?php wp_head(); ?>
</head>
<body <?php body_class(); ?>>
<header class="header" id="header">
    <div class="container">
        <a href="<?php echo esc_url(home_url()); ?>" class="logo">
            <?php if (has_custom_logo()) : ?>
                <?php the_custom_logo(); ?>
            <?php else : ?>
                <span><?php bloginfo('name'); ?></span>
            <?php endif; ?>
        </a>
        <nav class="nav" id="nav">
            <?php 
            wp_nav_menu(array(
                'theme_location' => 'primary',
                'container' => false,
                'fallback_cb' => false,
            ));
            ?>
        </nav>
    </div>
</header>
```
### Step 7: Footer Template
```php
<footer class="footer">
    <div class="container">
        <div class="footer-grid">
            <div class="footer- brand">
                <a href="<?php echo esc_url(home_url()); ?>">
                    <?php bloginfo('name'); ?>
                </a>
                <p><?php bloginfo('description'); ?></p>
            </div>
            <div>
                <h3>Links</h3>
                <?php wp_nav_menu(array('theme_location' => 'footer')); ?>
            </div>
        </div>
    </div>
</footer>
<?php wp_footer(); ?>
</body>
</html>
```
### Step 8: Index Template (Homepage)
```php
<?php get_header(); ?>
<main>
    <section class="hero">
        <div class="hero-slides">
            <?php $slides = get_posts(array('post_type' => 'slide', 'posts_per_page' => 5)); ?>
            <?php foreach ($slides as $post) : setup_postdata($post); ?>
            <div class="hero-slide">
                <?php the_content(); ?>
            </div>
            <?php endforeach; wp_reset_postdata(); ?>
        </div>
    </section>
    <?php if (have_posts()) : while (have_posts()) : the_post(); ?>
    <section id="<?php the_sub_field('section_id'); ?>">
        <?php the_content(); ?>
    </section>
    <?php endwhile; endif; ?>
</main>
<?php get_footer(); ?>
```
### Step 9: CSS Integration
Keep CSS unchanged for design fidelity. Only add WordPress overrides if needed:
```css
/* WordPress overrides */
.wp-block-image img { max-width: 100%; height: auto; }
.alignleft { float: left; margin-right: 1rem; }
.alignright { float: right; margin-left: 1rem; }
```
### Step 10: Customizer Integration
```php
function theme_customize_register($wp_customize) {
    // Colors
    $wp_customize->add_section('theme_colors', array(
        'title' => 'Colors',
    ));
    $wp_customize->add_setting('theme_primary_color', array(
        'default' => '#00E676',
        'transport' => 'refresh',
    ));
    $wp_customize->add_control(new WP_Customize_Color_Control($wp_customize, 'theme_primary_color', array(
        'label' => 'Primary Color',
        'section' => 'theme_colors',
        'settings' => 'theme_primary_color',
    )));
}
add_action('customize_register', 'theme_customize_register');
function theme_customizer_css() {
    $primary = get_theme_mod('theme_primary_color', '#00E676');
    echo '<style>:root{--primary:' . esc_attr($primary) . ';}</style>';
}
add_action('wp_head', 'theme_customizer_css');
```
### Step 11: Theme Customizer (CSS Variables)
```css
:root {
  --primary: <?php echo esc_attr(get_theme_mod('theme_primary_color', '#00E676')); ?>;
  /* other variables */
}
```
For output, use inline style in `<head>`:
```php
function theme_customizer_css() {
    $vars = array(
        'primary' => get_theme_mod('theme_primary_color', '#00E676'),
        'primary_dark' => get_theme_mod('theme_primary_dark_color', '#00C853'),
    );
    $css = ':root {';
    foreach ($vars as $prop => $value) {
        $css .= '--' . $prop . ':' . esc_attr($value) . ';';
    }
    $css .= '}';
    echo '<style>' . $css . '</style>';
}
add_action('wp_head', 'theme_customizer_css');
```
## Naming Conventions
Follow WordPress coding standards:
| Item | Convention | Example |
|------|-----------|---------|
| Theme slug | kebab-case | `zxnd-theme` |
| Text domain | same as theme slug | `zxnd-theme` |
| Theme version | semver | `1.0.0` |
| Constants | UPPER_SNAKE | `THEME_VERSION` |
| Functions | theme_prefix_name() | `zxnd_setup()` |
| Hooks | theme_prefix_name | `zxnd_enqueue_scripts` |
| Classes | Theme_Prefix_Class | `ZXND_Setup` |
| Options | theme_option_name | `zxnd_phone` |
| CSS classes | kebab-case | `.nav-link` |
## Security Checklist
- [ ] All URLs: `esc_url()`
- [ ] All HTML output: `esc_html()`, `esc_attr()`
- [ ] All content: `wp_kses()`, `wpautop()`
- [ ] Nonce for forms: `wp_verify_nonce()`
- [ ] Capability checks: `current_user_can()`
- [ ] Prepared queries: `$wpdb->prepare()`
## Performance
- [ ] Scripts loaded in footer with `in_footer => true`
- [ ] CSS combined and minified
- [ ] Lazy loading for images: `loading="lazy"`
- [ ] Preconnect for external resources
## Common Issues
### Menu Not Showing
```php
<?php 
if (has_nav_menu('primary')) {
    wp_nav_menu(array('theme_location' => 'primary'));
} else {
    echo '<a href="' . esc_url(home_url()) . '">Home</a>';
}
?>
```
### Custom Logo Not Displaying
Use `the_custom_logo()` which outputs the `<img>` tag directly.
### Colors from Customizer
Must output as inline `<style>` in `<head>` for real-time preview.
## Template Hierarchy
For CPT archives: `archive-{post_type}.php`
For CPT singles: `single-{post_type}.php`
## Testing Checklist
- [ ] Theme activates without errors
- [ ] All templates render correctly
- [ ] Menu displays and functions
- [ ] Customizer changes apply
- [ ] Mobile responsive
- [ ] Light/dark theme toggle works
- [ ] All links go to correct pages
- [ ] No PHP errors in debug mode
- [ ] Lighthouse score acceptable