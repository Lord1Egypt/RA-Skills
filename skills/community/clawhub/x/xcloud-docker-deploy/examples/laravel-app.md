# Example: Fresh Laravel App → xCloud Native Deploy

## Project structure detected
- composer.json ✓
- artisan ✓

Detected: Laravel | Recommended: xCloud Native

## Step 1 — Prepare .env.example

```env
APP_NAME=MyLaravelApp
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

## Step 2 — Add to .gitignore
```
.env
/vendor
/node_modules
/public/storage
/storage/*.key
```

## Step 3 — Push to GitHub
```bash
git init && git add . && git commit -m "Initial commit"
git remote add origin https://github.com/OWNER/REPO.git
git push -u origin main
```

## Step 4 — Deploy in xCloud
1. Server → New Site → Laravel tab
2. Connect GitHub repo, PHP version: 8.2
3. Deploy hooks:
   ```
   composer install --no-dev --optimize-autoloader
   php artisan config:cache
   php artisan route:cache
   php artisan view:cache
   php artisan migrate --force
   php artisan storage:link
   ```
4. Add env vars — APP_KEY from `php artisan key:generate --show`
5. Deploy
