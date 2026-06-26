# xCloud Native PHP Deployment

## Repository Setup

Web root: xCloud serves from `public/` by default.

Required files:
```
your-repo/
├── public/
│   └── index.php
├── .env.example
└── ...
```

.env.example:
```env
APP_ENV=production
DB_HOST=
DB_DATABASE=
DB_USERNAME=
DB_PASSWORD=
```

## xCloud UI Steps

1. Server → New Site → PHP tab
2. Connect Git repo
3. PHP version: 7.4, 8.0, 8.1, 8.2, or 8.3
4. Web root: `public` (or `/` if serving from root)
5. Add environment variables
6. Deploy hooks (if using Composer):
   ```bash
   composer install --no-dev --optimize-autoloader
   ```
7. Click Deploy

## Common Issues

| Issue | Fix |
|---|---|
| 403 Forbidden | Check web root config |
| Missing extensions | Use Docker path for custom extensions |
| Composer errors | Ensure composer.json is committed, vendor/ in .gitignore |
