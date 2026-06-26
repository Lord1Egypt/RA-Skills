# xCloud Native Laravel Deployment

## Repository Setup (Required)

File structure xCloud expects:
```
your-repo/
├── app/
├── public/          ← web root
├── storage/         ← must be writable
├── bootstrap/
├── config/
├── routes/
├── .env.example     ← commit this
├── composer.json
├── artisan
└── ...
```

Critical: Never commit `.env`. Set all variables in xCloud UI.

.env.example (minimum required):
```env
APP_NAME=MyApp
APP_ENV=production
APP_KEY=
APP_DEBUG=false
APP_URL=https://yourdomain.com

DB_CONNECTION=mysql
DB_HOST=
DB_PORT=3306
DB_DATABASE=
DB_USERNAME=
DB_PASSWORD=

CACHE_DRIVER=file
QUEUE_CONNECTION=sync
SESSION_DRIVER=file
```

## xCloud UI Steps

1. Server → New Site → Laravel tab
2. Connect Git repo (GitHub/GitLab/Bitbucket)
3. Set branch (usually `main` or `master`)
4. PHP version: select 8.2 or 8.3
5. Add environment variables (from your .env.example)
   - Generate APP_KEY locally: `php artisan key:generate --show`
6. Deploy hooks — add these commands in order:
   ```bash
   composer install --no-dev --optimize-autoloader
   php artisan config:cache
   php artisan route:cache
   php artisan view:cache
   php artisan migrate --force
   php artisan storage:link
   ```
7. Click Deploy

## Queue Workers (if using)

In xCloud site settings → Supervisor → Add worker:
```
php artisan queue:work --sleep=3 --tries=3 --max-time=3600
```

## Scheduler (if using)

In xCloud site settings → Cron Jobs → Add:
```
* * * * *    php artisan schedule:run >> /dev/null 2>&1
```

## Common Issues

| Issue | Fix |
|---|---|
| 500 error after deploy | Check APP_KEY is set |
| Assets not loading | Run `npm run build` locally, commit public/build/ |
| Queue jobs not processing | Add supervisor worker |
| Storage files missing | Ensure storage:link is in deploy hooks |
| Migration errors | Check DB credentials, ensure --force flag |
