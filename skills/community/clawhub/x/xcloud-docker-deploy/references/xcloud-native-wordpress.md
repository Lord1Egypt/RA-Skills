# xCloud Native WordPress Deployment

WordPress on xCloud is fully managed — no Docker needed.

## Method 1: One-Click Install (Recommended for new sites)

1. Server → New Site → WordPress tab
2. Fill in: site title, admin email, admin username, admin password
3. PHP version: 8.1 or 8.2 recommended
4. Web stack: NGINX (recommended) or OpenLiteSpeed
5. Click Deploy — WordPress installed automatically

## Method 2: Git Deploy (existing WordPress sites)

Repository setup:
```
your-repo/
├── wp-content/
│   ├── plugins/
│   ├── themes/
│   └── uploads/     ← add to .gitignore
├── wp-config.php    ← use env vars for DB credentials
└── ...
```

wp-config.php — use environment variables:
```php
define('DB_NAME',     getenv('DB_NAME'));
define('DB_USER',     getenv('DB_USER'));
define('DB_PASSWORD', getenv('DB_PASSWORD'));
define('DB_HOST',     getenv('DB_HOST') ?: 'localhost');
```

xCloud UI Steps:
1. Server → New Site → WordPress tab → Git option
2. Connect repo
3. Add DB environment variables
4. Deploy

## Performance Recommendations

- Enable NGINX FastCGI Cache in xCloud site settings
- Enable Redis Object Cache (available as xCloud addon)
- Set PHP version to 8.2+
- Enable AI Bot Blocker in security settings
