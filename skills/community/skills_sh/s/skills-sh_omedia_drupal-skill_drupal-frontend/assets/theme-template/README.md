# Theme Template

This is a basic Drupal theme template. To use it:

1. Copy this directory to your Drupal installation: `themes/custom/yourthemename/`
2. Rename files from `THEMENAME.*` to `yourthemename.*`
3. Replace all instances of `THEMENAME` with your theme's machine name (lowercase, underscores)
4. Replace all instances of `THEMELABEL` with your theme's human-readable name
5. Customize the theme as needed

## Files Included

- `THEMENAME.info.yml` - Theme metadata
- `THEMENAME.libraries.yml` - CSS/JS library definitions
- `THEMENAME.theme` - Theme functions and preprocessing
- `templates/page.html.twig` - Page template
- `css/base/reset.css` - Base CSS reset
- `js/custom.js` - Custom JavaScript

## Directory Structure

```
THEMENAME/
├── THEMENAME.info.yml
├── THEMENAME.libraries.yml
├── THEMENAME.theme
├── css/
│   └── base/
│       └── reset.css
├── js/
│   └── custom.js
└── templates/
    └── page.html.twig
```

You can expand the CSS structure as needed:
```
css/
├── base/
│   └── reset.css
├── layout/
│   └── layout.css
├── components/
│   └── components.css
└── theme/
    └── theme.css
```

## Next Steps

After creating your theme:

1. Clear cache: `ddev drush cr`
2. Enable your theme: Go to `/admin/appearance`
3. Set as default theme
4. Start customizing!

## Development Tips

- Enable Twig debugging in `sites/default/services.yml`
- Disable CSS/JS aggregation during development
- Clear cache frequently: `ddev drush cr`
- Use template suggestions for specific pages/content types
