# Rendering Responsive Images in Hyvä Templates

The Hyvä Theme provides the `\Hyva\Theme\ViewModel\Media` view model for rendering responsive images using the HTML `<picture>` element. This view model generates semantic markup with `<source>` elements for different screen sizes and image formats, enabling art direction and format selection for optimal performance.

## Method Signature

```php
\Hyva\Theme\ViewModel\Media::getResponsivePictureHtml(
    array $images,
    array $imgAttributes = [],
    array $pictureAttributes = []
): string
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `$images` | `array` | Array of image configurations, each with path, dimensions, and optional media query |
| `$imgAttributes` | `array` | HTML attributes for the `<img>` fallback element (alt, class, loading, etc.) |
| `$pictureAttributes` | `array` | HTML attributes for the `<picture>` wrapper element |

**Image configuration keys:**

| Key | Required | Description |
|-----|----------|-------------|
| `path` | Yes | Relative path to the image in `pub/media/` |
| `width` | Yes | Image width in pixels |
| `height` | Yes | Image height in pixels |
| `media` | No | CSS media query for when this source applies (e.g., `(min-width: 768px)`) |
| `fallback` | No | Set to `true` to use this image as the `<img>` src for browsers without `<picture>` support |

## Image Configuration Format

Image data can be provided as literal values or stored in PHP variables. The `$images` parameter expects an array of image configuration arrays.

**Single image config structure:**
```php
$imageData = [
    'path' => 'relative/path/in/pub/media/image.jpg',  // Required
    'width' => 800,                                      // Required
    'height' => 600,                                     // Required
    'media' => '(min-width: 768px)',                    // Optional: CSS media query
    'fallback' => true                                   // Optional: use as <img> fallback
];
```

**Passing to the method:**
```php
// Single image config must be wrapped in an array
echo $mediaViewModel->getResponsivePictureHtml([$imageData], $imgAttributes);

// Multiple image configs are already an array
echo $mediaViewModel->getResponsivePictureHtml($images, $imgAttributes);
```

## Single Image Example

```php
<?php
/** @var \Hyva\Theme\ViewModel\Media $mediaViewModel */
$mediaViewModel = $viewModels->require(\Hyva\Theme\ViewModel\Media::class);

$imageConfig = [
    [
        'path' => 'catalog/product/w/b/wb01-blue-0.jpg',
        'width' => 400,
        'height' => 500
    ]
];

echo $mediaViewModel->getResponsivePictureHtml($imageConfig);
```

## Responsive Images with Media Queries

```php
<?php
/** @var \Hyva\Theme\ViewModel\Media $mediaViewModel */
$mediaViewModel = $viewModels->require(\Hyva\Theme\ViewModel\Media::class);

// Desktop image: wide landscape format for large screens
$desktopImage = [
    'path' => 'wysiwyg/homepage-main-hero.jpg',
    'width' => 1920,
    'height' => 600,
    'media' => '(min-width: 768px)',
    'fallback' => true
];

// Mobile image: taller portrait format for small screens
$mobileImage = [
    'path' => 'wysiwyg/homepage-mobile-hero.jpg',
    'width' => 768,
    'height' => 800,
    'media' => '(max-width: 767px)'
];

$imgAttributes = [
    'alt' => 'Summer Collection',
    'class' => 'w-full h-auto',
    'loading' => 'eager',
    'fetchpriority' => 'high'
];

echo $mediaViewModel->getResponsivePictureHtml(
    [$desktopImage, $mobileImage],
    $imgAttributes
);
```

## Picture Element Attributes

```php
$pictureAttributes = [
    'class' => 'hero-banner aspect-video',
    'data-testid' => 'homepage-hero'
];

echo $mediaViewModel->getResponsivePictureHtml(
    $imageConfig,
    $imgAttributes,
    $pictureAttributes
);
```

## Common Image Attributes

| Attribute | Values | Use Case |
|-----------|--------|----------|
| `loading` | `lazy`, `eager` | Lazy loading for below-the-fold images, eager for hero images |
| `fetchpriority` | `high`, `low`, `auto` | Prioritize critical images like LCP elements |
| `decoding` | `async`, `sync`, `auto` | Allow async decoding for non-blocking rendering |
| `alt` | string | Always provide meaningful alt text for accessibility |
| `class` | string | Tailwind CSS classes for styling |

## Best Practices

1. **Always specify width and height** - Prevents Cumulative Layout Shift (CLS)
2. **Use `loading="lazy"`** - For images below the fold
3. **Use `loading="eager"` + `fetchpriority="high"`** - For LCP (Largest Contentful Paint) images
4. **Provide meaningful alt text** - Required for accessibility
5. **Use media queries for art direction** - Different crops for mobile vs desktop
6. **Mark one image as `fallback`** - For browsers without `<picture>` support

## Common Mistakes

1. **Forgetting to wrap a single image in an array**
   ```php
   // Wrong - passing image config directly
   echo $mediaViewModel->getResponsivePictureHtml($imageData, $imgAttributes);

   // Correct - wrap in array
   echo $mediaViewModel->getResponsivePictureHtml([$imageData], $imgAttributes);
   ```

2. **Using absolute paths instead of relative `pub/media/` paths**
   ```php
   // Wrong - absolute or full URL paths
   'path' => '/pub/media/wysiwyg/hero.jpg'
   'path' => 'https://example.com/media/wysiwyg/hero.jpg'

   // Correct - relative to pub/media/
   'path' => 'wysiwyg/hero.jpg'
   ```

3. **Missing width and height causing layout shift (CLS)**
   ```php
   // Wrong - missing dimensions
   $imageConfig = [['path' => 'wysiwyg/hero.jpg']];

   // Correct - always specify dimensions
   $imageConfig = [[
       'path' => 'wysiwyg/hero.jpg',
       'width' => 1920,
       'height' => 600
   ]];
   ```

4. **Using `loading="lazy"` on above-the-fold LCP images**
   ```php
   // Wrong - lazy loading hero images delays LCP
   'loading' => 'lazy'

   // Correct - eager load with high priority for hero/LCP images
   'loading' => 'eager',
   'fetchpriority' => 'high'
   ```

5. **Overlapping media queries in responsive images**
   ```php
   // Wrong - both match at 768px
   'media' => '(min-width: 768px)'  // desktop
   'media' => '(max-width: 768px)'  // mobile

   // Correct - no overlap
   'media' => '(min-width: 768px)'  // desktop
   'media' => '(max-width: 767px)'  // mobile
   ```