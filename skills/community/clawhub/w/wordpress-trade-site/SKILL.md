---
name: wordpress-trade-site
description: Interactive guide to deploy a production-ready WordPress site for international trade businesses. Triggers on "build a trade website", "deploy wordpress trade site", "set up B2B website", or similar requests.
---

# WordPress Trade Site Builder

Deploy a production-ready WordPress trade site from scratch through 9 interactive phases. Based on the [wordpress-trade-starter](https://github.com/iPythoning/wordpress-trade-starter) template.

**Principle:** Automate everything possible. Only pause when user decisions or information are required. When errors occur, diagnose and fix them proactively — don't tell the user to go fix things themselves.

**Interaction:** Use `AskUserQuestion` for all user-facing questions. Report progress after each phase, then continue to the next.

**Data flow:** Information collected in each phase (business info, SSH details, domain, etc.) is reused in subsequent phases. Key data is labeled with variable names for reference.

---

## Phase 1: Collect Business Information

Before any technical work, understand the user's business needs.

AskUserQuestion (collect sequentially):

1. **Company name** — "What is your company name? (Both local language and English)"
   - Example: TitanPuls Technology Co., Ltd.
   - Record as `COMPANY_EN` (and `COMPANY_LOCAL` if provided)

2. **Main products** — "What products do you mainly sell? (Brief description)"
   - Example: Semi-trailers, construction machinery
   - Record as `PRODUCTS`

3. **Target markets** — "Which markets do you primarily target?" (multiSelect)
   - Africa
   - Middle East
   - Southeast Asia
   - Latin America
   - Europe
   - North America
   - Record as `TARGET_MARKETS`

4. **Languages** — "Which languages should your website support?" (multiSelect, recommend based on target markets)
   - English (Recommended)
   - Chinese
   - Russian
   - Spanish
   - French
   - Arabic
   - Record as `LANGUAGES`

5. **Contact info** — "How should customers reach you?"
   - WhatsApp number (with country code)
   - Business email
   - Record as `WHATSAPP` and `EMAIL`

Summary confirmation: Display collected information and AskUserQuestion to confirm correctness.

---

## Phase 2: Server Preparation

### 2a. Server status

AskUserQuestion: "Do you already have a Linux server?"
- **I have a server** — Collect SSH details
- **I need guidance** — Recommend datacenter locations and providers based on `TARGET_MARKETS`

**Purchase guidance** (if needed):

Recommend based on target market:
| Target Market | Recommended DC | Recommended Providers |
|--------------|----------------|----------------------|
| Europe/Africa | Germany/Netherlands | Contabo, Hetzner |
| North America | US East/West Coast | DigitalOcean, Vultr |
| Southeast Asia | Singapore | Vultr, Alibaba Cloud |
| Middle East | Dubai/Bahrain | AWS, Alibaba Cloud |
| Latin America | US Miami | DigitalOcean |

Recommended specs: 2 cores / 2GB RAM / 40GB SSD ($10-20/month). Tell user to continue after purchase.

### 2b. SSH connection

AskUserQuestion: "Please provide your server SSH details:"
- IP address → `SERVER_IP`
- SSH port (default 22) → `SSH_PORT`
- Username (usually root) → `SSH_USER`
- Authentication: password or SSH key

Verify connection:

```bash
ssh -o ConnectTimeout=10 -o StrictHostKeyChecking=no -p ${SSH_PORT} ${SSH_USER}@${SERVER_IP} "echo CONNECTION_OK && uname -a && free -m && df -h /"
```

- CONNECTION_OK → Continue
- Connection failed → Check IP/port/credentials, prompt user to correct

### 2c. Server initialization

Execute via SSH:

```bash
# System update
apt update && apt upgrade -y

# Set timezone
timedatectl set-timezone UTC

# Create swap (if RAM <= 2GB and no swap exists)
if [ $(free -m | awk '/^Mem:/{print $2}') -le 2048 ] && [ ! -f /swapfile ]; then
    fallocate -l 2G /swapfile
    chmod 600 /swapfile
    mkswap /swapfile
    swapon /swapfile
    echo '/swapfile none swap sw 0 0' >> /etc/fstab
fi

# Firewall
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw --force enable

# Essential tools
apt install -y curl git unzip htop
```

Verify: `ufw status` shows 22/80/443 open.

---

## Phase 3: Docker Deployment

### 3a. Install Docker

```bash
if ! command -v docker &>/dev/null; then
    curl -fsSL https://get.docker.com | sh
    systemctl enable docker && systemctl start docker
fi
docker compose version || apt-get install -y docker-compose-plugin
```

Verify: `docker compose version` outputs a version number.

### 3b. Clone template

```bash
cd /opt
git clone https://github.com/iPythoning/wordpress-trade-starter.git wordpress
cd /opt/wordpress
```

### 3c. Generate .env

AskUserQuestion: "Please provide the following:"
- Domain name (e.g. example.com) → `DOMAIN`
- MySQL root password (auto-generate recommended) → `MYSQL_ROOT_PASSWORD`
- MySQL user password (auto-generate recommended) → `MYSQL_PASSWORD`

If user chooses auto-generation:
```bash
MYSQL_ROOT_PASSWORD=$(openssl rand -base64 16)
MYSQL_PASSWORD=$(openssl rand -base64 16)
```

Write .env:
```bash
cat > /opt/wordpress/.env << EOF
MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD}
MYSQL_DATABASE=wordpress
MYSQL_USER=wordpress
MYSQL_PASSWORD=${MYSQL_PASSWORD}
DOMAIN=${DOMAIN}
EMAIL=${EMAIL}
EOF
```

**Important:** Display the generated passwords to the user and remind them to save securely.

### 3d. Configure Nginx

```bash
sed -i "s/YOUR_DOMAIN/${DOMAIN}/g" /opt/wordpress/nginx.conf
```

### 3e. Start containers

```bash
cd /opt/wordpress
docker compose up -d
```

Verify:
```bash
docker compose ps
# Confirm all three containers (db, wordpress, nginx) are running/healthy
```

Wait for WordPress to be ready:
```bash
for i in $(seq 1 30); do
    curl -sf http://localhost > /dev/null 2>&1 && break
    sleep 2
done
```

- All 3 containers running → Continue
- db unhealthy → Check `docker compose logs db`, common cause is password format issues
- wordpress not starting → Check `docker compose logs wordpress`

---

## Phase 4: SSL Certificate

### 4a. Choose method

AskUserQuestion: "Which SSL certificate method?"
- **Let's Encrypt (Recommended)** — Free, auto-renewal, requires domain A record pointing to server IP
- **Cloudflare Origin Certificate** — For users already using Cloudflare proxy

### 4b-A. Let's Encrypt

Prerequisite: Domain A records must point to `SERVER_IP`. If not configured, guide the user to add in their DNS panel:
- `DOMAIN` → A → `SERVER_IP`
- `www.DOMAIN` → A → `SERVER_IP`

```bash
# Stop nginx to free port 80
cd /opt/wordpress && docker compose stop nginx

apt install -y certbot
certbot certonly --standalone -d ${DOMAIN} -d www.${DOMAIN} --email ${EMAIL} --agree-tos --non-interactive

mkdir -p /opt/wordpress/ssl
cp /etc/letsencrypt/live/${DOMAIN}/fullchain.pem /opt/wordpress/ssl/
cp /etc/letsencrypt/live/${DOMAIN}/privkey.pem /opt/wordpress/ssl/

# Auto-renewal cron
(crontab -l 2>/dev/null; echo "0 3 * * * certbot renew --quiet --pre-hook 'cd /opt/wordpress && docker compose stop nginx' --post-hook 'cp /etc/letsencrypt/live/${DOMAIN}/fullchain.pem /opt/wordpress/ssl/ && cp /etc/letsencrypt/live/${DOMAIN}/privkey.pem /opt/wordpress/ssl/ && cd /opt/wordpress && docker compose start nginx'") | crontab -

# Restart nginx
docker compose start nginx
```

### 4b-B. Cloudflare Origin Certificate

Guide the user through Cloudflare Dashboard:
1. SSL/TLS → Origin Server → Create Certificate
2. Choose RSA, 15-year validity
3. Copy Certificate and Private Key

```bash
mkdir -p /opt/wordpress/ssl
# User pastes certificate content
cat > /opt/wordpress/ssl/fullchain.pem << 'EOF'
<user pastes certificate here>
EOF
cat > /opt/wordpress/ssl/privkey.pem << 'EOF'
<user pastes private key here>
EOF
```

### 4c. Verify HTTPS

```bash
docker compose restart nginx
curl -I https://${DOMAIN} 2>/dev/null | head -5
```

- HTTP/2 200 → Success
- Connection failed → Check DNS resolution, certificate paths, nginx logs

---

## Phase 5: WordPress Initialization

### 5a. Setup wizard

Tell the user to open `https://${DOMAIN}/wp-admin/install.php` in their browser and fill in:
- Site Title: `COMPANY_EN`
- Username: suggest avoiding "admin" (security)
- Password: strong password
- Email: `EMAIL`

AskUserQuestion: "Have you completed the WordPress setup wizard?"

### 5b. Install WP-CLI

```bash
docker compose exec wordpress bash -c '
curl -O https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar
chmod +x wp-cli.phar
mv wp-cli.phar /usr/local/bin/wp
'
```

Verify: `docker compose exec wordpress wp --info --allow-root`

### 5c. Base configuration

```bash
docker compose exec wordpress wp --allow-root option update blogname "${COMPANY_EN}"
docker compose exec wordpress wp --allow-root option update blogdescription "${PRODUCTS} - ${COMPANY_EN}"
docker compose exec wordpress wp --allow-root option update timezone_string "UTC"
docker compose exec wordpress wp --allow-root option update date_format "Y-m-d"
docker compose exec wordpress wp --allow-root option update permalink_structure "/%postname%/"

# Delete default content
docker compose exec wordpress wp --allow-root post delete 1 2 --force
docker compose exec wordpress wp --allow-root widget reset --all
```

---

## Phase 6: Theme & Plugin Installation

### 6a. Astra theme + Child Theme

```bash
docker compose exec wordpress wp --allow-root theme install astra --activate

# Create Child Theme
docker compose exec wordpress bash -c '
mkdir -p /var/www/html/wp-content/themes/astra-child
cat > /var/www/html/wp-content/themes/astra-child/style.css << "CSS"
/*
Theme Name: Astra Child
Template: astra
Version: 1.0.0
*/
CSS
cat > /var/www/html/wp-content/themes/astra-child/functions.php << "PHP"
<?php
add_action("wp_enqueue_scripts", function() {
    wp_enqueue_style("parent-style", get_template_directory_uri() . "/style.css");
});
PHP
'
docker compose exec wordpress wp --allow-root theme activate astra-child
```

### 6b. Batch install plugins

Install plugins one by one to track failures:

```bash
PLUGINS="elementor seo-by-rank-math wp-super-cache imagify jetpack-boost polylang contact-form-7 flamingo chaty ecommerce-product-catalog"
for plugin in $PLUGINS; do
    docker compose exec wordpress wp --allow-root plugin install $plugin --activate 2>&1 || echo "WARN: $plugin install failed, manual install needed"
done
```

Note: Some plugins may not be in the wordpress.org directory. For failed installs, inform the user to install manually from the admin panel (Plugins → Add New).

### 6c. Configure CF7 + Flamingo

**Critical:** CF7 only sends emails by default — if the recipient email is wrong, all inquiries are lost permanently. Flamingo stores every submission in the WP database as a safety net.

After installing, verify:

```bash
# Verify Flamingo is active (auto-stores CF7 submissions)
docker compose exec wordpress wp --allow-root plugin list --status=active --field=name | grep flamingo

# Update CF7 form recipient to the admin email (not a non-existent address)
docker compose exec wordpress wp --allow-root post list --post_type=wpcf7_contact_form --fields=ID,post_title
# For each form, verify the recipient matches EMAIL:
docker compose exec wordpress wp --allow-root post meta get <FORM_ID> _mail
# If recipient is wrong, update it via WP Admin → Contact → Forms → Edit
```

Inquiries are viewable at: WP Admin → Flamingo → Inbound Messages.

### 6d. Configure Imagify

AskUserQuestion: "Do you have an Imagify API key? (Free signup at imagify.io, 20MB/month free tier)"
- Yes → Collect `IMAGIFY_API_KEY`
- Skip for now → Remind user to configure later in Settings → Imagify

### 6e. Configure WP Super Cache

```bash
docker compose exec wordpress wp --allow-root super-cache enable 2>/dev/null || true
```

If WP-CLI doesn't support it, tell the user to go to Settings → WP Super Cache:
1. Enable Caching
2. Advanced → Use mod_rewrite

### 6f. Jetpack Boost

Tell the user to enable in the admin panel:
- Critical CSS generation
- Lazy image loading
- Concatenate JS/CSS

---

## Phase 7: Multilingual + SEO

### 7a. Polylang configuration

Configure based on the `LANGUAGES` list from Phase 1:

```bash
# Set English as default language
docker compose exec wordpress wp --allow-root pll lang create "English" en en_US
```

Add each selected language:
- Chinese: `wp pll lang create "Chinese" zh zh_CN`
- Russian: `wp pll lang create "Russian" ru ru_RU`
- Spanish: `wp pll lang create "Spanish" es es_ES`
- French: `wp pll lang create "French" fr fr_FR`
- Arabic: `wp pll lang create "Arabic" ar ar`

Note: Polylang WP-CLI support may be limited. If commands fail, guide the user to add languages manually in Languages → Settings.

### 7b. Rank Math SEO configuration

Guide the user through the Rank Math setup wizard:
1. Business Type → Select "Company"
2. Company Name → `COMPANY_EN`
3. Website URL → `https://${DOMAIN}`
4. Social Profiles → If available
5. Sitemap Settings → Enable XML Sitemap
6. Schema → Organization

### 7c. Create base pages

```bash
docker compose exec wordpress bash -c '
wp --allow-root post create --post_type=page --post_title="Home" --post_status=publish --post_content="<!-- wp:paragraph --><p>Welcome to '"${COMPANY_EN}"'. We specialize in '"${PRODUCTS}"'.</p><!-- /wp:paragraph -->"
wp --allow-root post create --post_type=page --post_title="About Us" --post_status=publish --post_content="<!-- wp:paragraph --><p>About '"${COMPANY_EN}"'</p><!-- /wp:paragraph -->"
wp --allow-root post create --post_type=page --post_title="Products" --post_status=publish --post_content="<!-- wp:paragraph --><p>Our product catalog</p><!-- /wp:paragraph -->"
wp --allow-root post create --post_type=page --post_title="Contact" --post_status=publish --post_content="<!-- wp:paragraph --><p>Get in touch with us. WhatsApp: '"${WHATSAPP}"' Email: '"${EMAIL}"'</p><!-- /wp:paragraph -->[contact-form-7]"
wp --allow-root post create --post_type=page --post_title="FAQ" --post_status=publish --post_content="<!-- wp:paragraph --><p>Frequently Asked Questions</p><!-- /wp:paragraph -->"
wp --allow-root post create --post_type=page --post_title="Blog" --post_status=publish --post_content=""
'

# Set Home as front page, Blog as posts page
HOME_ID=$(docker compose exec wordpress wp --allow-root post list --post_type=page --name=home --field=ID)
BLOG_ID=$(docker compose exec wordpress wp --allow-root post list --post_type=page --name=blog --field=ID)
docker compose exec wordpress wp --allow-root option update show_on_front page
docker compose exec wordpress wp --allow-root option update page_on_front $HOME_ID
docker compose exec wordpress wp --allow-root option update page_for_posts $BLOG_ID
```

### 7d. Create navigation menu

```bash
docker compose exec wordpress bash -c '
wp --allow-root menu create "Main Menu"
wp --allow-root menu item add-post "Main Menu" $(wp --allow-root post list --post_type=page --name=home --field=ID) --title="Home"
wp --allow-root menu item add-post "Main Menu" $(wp --allow-root post list --post_type=page --name=about-us --field=ID) --title="About"
wp --allow-root menu item add-post "Main Menu" $(wp --allow-root post list --post_type=page --name=products --field=ID) --title="Products"
wp --allow-root menu item add-post "Main Menu" $(wp --allow-root post list --post_type=page --name=faq --field=ID) --title="FAQ"
wp --allow-root menu item add-post "Main Menu" $(wp --allow-root post list --post_type=page --name=blog --field=ID) --title="Blog"
wp --allow-root menu item add-post "Main Menu" $(wp --allow-root post list --post_type=page --name=contact --field=ID) --title="Contact"
wp --allow-root menu location assign "Main Menu" primary
'
```

---

## Phase 8: Cloudflare + Performance

### 8a. Cloudflare DNS

AskUserQuestion: "Are you using Cloudflare for DNS management?"
- **Yes** → Guide configuration
- **No** → Skip Cloudflare section, only do local performance optimization

**Cloudflare configuration guide:**

1. Add site `DOMAIN` in Cloudflare Dashboard
2. Change domain NS records to Cloudflare-provided nameservers
3. Add DNS records:
   - `@` → A → `SERVER_IP` (Proxied)
   - `www` → CNAME → `DOMAIN` (Proxied)

### 8b. SSL/TLS settings

In Cloudflare Dashboard:
- SSL/TLS → Overview → Full (Strict)
- Edge Certificates → Always Use HTTPS → On
- Edge Certificates → Minimum TLS Version → 1.2
- Edge Certificates → Automatic HTTPS Rewrites → On

### 8c. Cache rules

In Cloudflare Dashboard → Caching:
- Caching Level → Standard
- Browser Cache TTL → Respect Existing Headers
- Always Online → On

Page Rules (if free quota available):
- `*${DOMAIN}/wp-admin/*` → Cache Level: Bypass
- `*${DOMAIN}/wp-login.php*` → Cache Level: Bypass
- `*${DOMAIN}/*` → Cache Level: Cache Everything, Edge TTL: 2 hours

### 8d. Verify triple-layer cache

```bash
# Test 1: Check Nginx proxy cache
curl -I https://${DOMAIN} 2>/dev/null | grep -i x-cache-status
# Expected: X-Cache-Status: HIT (on second request)

# Test 2: Check Cloudflare cache
curl -I https://${DOMAIN} 2>/dev/null | grep -i cf-cache-status
# Expected: cf-cache-status: HIT

# Test 3: Check WP Super Cache
docker compose exec wordpress ls /var/www/html/wp-content/cache/supercache/ 2>/dev/null && echo "SUPER_CACHE_OK" || echo "SUPER_CACHE_EMPTY"
```

### 8e. PageSpeed test

Tell the user to visit Google PageSpeed Insights: `https://pagespeed.web.dev/analysis?url=https://${DOMAIN}`

Target metrics:
- Desktop Score: >= 75
- Mobile Score: >= 60
- TTFB: < 500ms
- LCP: < 2.5s

---

## Phase 8.5: GEO (Generative Engine Optimization)

### 8.5a. Deploy GEO functions

```bash
# Copy GEO functions to child theme
docker compose exec wordpress bash -c '
curl -sL https://raw.githubusercontent.com/iPythoning/wordpress-trade-starter/main/assets/geo-functions.php \
  -o /var/www/html/wp-content/themes/astra-child/geo-functions.php
'
```

Add configuration to child theme's functions.php:

```bash
docker compose exec wordpress bash -c '
cat >> /var/www/html/wp-content/themes/astra-child/functions.php << "GEO"

// GEO Configuration
define("GEO_SAMEAS", []);  // Add Wikipedia, LinkedIn, YouTube URLs later
define("GEO_LANGUAGES", [${LANGUAGES_ARRAY}]);
define("GEO_CONTACT_EMAIL", "${EMAIL}");
define("GEO_CONTACT_PHONE", "${WHATSAPP}");
require_once get_stylesheet_directory() . "/geo-functions.php";
GEO
'
```

AskUserQuestion: "Do you have profiles on these platforms? (We'll add them to your schema for AI recognition)" (multiSelect)
- Wikipedia page
- LinkedIn company page
- YouTube channel
- Twitter/X account
- None yet — Skip

For each selected platform, collect the URL and add to `GEO_SAMEAS` array.

### 8.5b. Verify GEO deployment

```bash
# Check robots.txt has AI bots
curl -s https://${DOMAIN}/robots.txt | grep -c "User-agent:"
# Expected: 15+ entries (standard + AI tier 1 + tier 2 + SEO bots)

# Check llms.txt auto-generation
curl -s https://${DOMAIN}/llms.txt | head -5
# Expected: "# COMPANY_NAME" followed by description

# Check JSON-LD schema
curl -s https://${DOMAIN}/ | grep -o '"@type":"[^"]*"' | sort -u
# Expected: Organization, WebSite, BreadcrumbList
```

### 8.5c. Cloudflare AI bot access

**Critical:** Cloudflare's "Managed robots.txt" blocks AI crawlers by default.

Tell the user: Go to Cloudflare Dashboard → Security → Bots → **Disable "Managed robots.txt"**.

Without this, all GEO work is nullified.

---

## Phase 9: Security Hardening + Verification

### 9a. File permissions

```bash
# WordPress file permission best practices
docker compose exec wordpress bash -c '
find /var/www/html -type d -exec chmod 755 {} \;
find /var/www/html -type f -exec chmod 644 {} \;
chmod 440 /var/www/html/wp-config.php
'
```

### 9b. Block xmlrpc.php

Already handled in nginx.conf via skip_cache rules. Additional blocking:

```bash
docker compose exec wordpress bash -c '
cat >> /var/www/html/.htaccess << "HTACCESS"

# Block xmlrpc.php
<Files xmlrpc.php>
    Require all denied
</Files>
HTACCESS
'
```

### 9c. Backup cron

```bash
# Database backup script
cat > /opt/wordpress/backup.sh << 'BACKUP'
#!/bin/bash
BACKUP_DIR="/opt/wordpress/backups"
mkdir -p $BACKUP_DIR
DATE=$(date +%Y%m%d_%H%M%S)
docker compose -f /opt/wordpress/docker-compose.yml exec -T db mysqldump -u root -p${MYSQL_ROOT_PASSWORD} wordpress > $BACKUP_DIR/db_$DATE.sql
gzip $BACKUP_DIR/db_$DATE.sql
# Keep only last 7 days of backups
find $BACKUP_DIR -name "*.sql.gz" -mtime +7 -delete
BACKUP
chmod +x /opt/wordpress/backup.sh

# Daily backup at 2am
(crontab -l 2>/dev/null; echo "0 2 * * * /opt/wordpress/backup.sh") | crontab -
```

### 9d. UptimeRobot monitoring

AskUserQuestion: "Would you like to set up free UptimeRobot monitoring?"
- **Yes** → Guide user to register at uptimerobot.com and add:
  - Monitor Type: HTTPS
  - URL: `https://${DOMAIN}`
  - Interval: 5 minutes
  - Alert Contact: `EMAIL`
- **Skip** → Continue

### 9e. Final verification checklist

Run checks and report:

```bash
echo "=== WordPress Trade Site Verification Checklist ==="

# 1. Container status
docker compose -f /opt/wordpress/docker-compose.yml ps --format "table {{.Name}}\t{{.Status}}"

# 2. HTTPS
curl -sI https://${DOMAIN} | head -1

# 3. WordPress version
docker compose -f /opt/wordpress/docker-compose.yml exec wordpress wp --allow-root core version

# 4. Active plugins
docker compose -f /opt/wordpress/docker-compose.yml exec wordpress wp --allow-root plugin list --status=active --format=table

# 5. Published pages
docker compose -f /opt/wordpress/docker-compose.yml exec wordpress wp --allow-root post list --post_type=page --post_status=publish --format=table

# 6. SSL certificate expiry
echo | openssl s_client -connect ${DOMAIN}:443 -servername ${DOMAIN} 2>/dev/null | openssl x509 -noout -dates

# 7. Cache status
curl -sI https://${DOMAIN} | grep -iE "x-cache-status|cf-cache-status"
```

Output a summary report:

```
All 3 containers running (WordPress + MySQL + Nginx)
HTTPS certificate valid, expires: YYYY-MM-DD
WordPress 6.7, X active plugins installed
6 base pages created + navigation menu
Multilingual configured with X languages
SEO (Rank Math) enabled
Triple-layer cache active
Database auto-backup configured
xmlrpc.php blocked
File permissions hardened
GEO: robots.txt has AI bot tiers, llms.txt serving, JSON-LD schemas active

Site URL:  https://${DOMAIN}
Admin URL: https://${DOMAIN}/wp-admin
Email:     ${EMAIL}
WhatsApp:  ${WHATSAPP}
```

---

## Troubleshooting

**Docker containers fail to start:** Check `docker compose logs <service>`. Common issues: port already in use (`lsof -i :80`), insufficient disk space (`df -h`).

**SSL certificate acquisition fails:** Confirm DNS has propagated (`dig ${DOMAIN}`), port 80 is accessible. Let's Encrypt limits to 5 certificates per domain per week.

**WordPress setup wizard doesn't appear:** Check `docker compose logs wordpress`. If database connection fails, check if .env passwords contain special characters (need escaping).

**Plugin installation fails:** When WP-CLI fails, install manually from the admin panel (Plugins → Add New). Ensure the WordPress container can reach wordpress.org.

**Low PageSpeed score:** Confirm all three cache layers are active, Imagify has optimized existing images, Jetpack Boost Critical CSS has been generated. Clear all caches and retest.

**SSH connection drops:** Use `screen` or `tmux` for long-running commands. Reconnect with `screen -r` to resume session.
