#!/bin/bash
# Auto Publisher - Quick Setup Script
# Run this after installing the skill to set up your configuration

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="$SCRIPT_DIR/config.json"
EXAMPLE_FILE="$SCRIPT_DIR/config.example.json"

echo "================================================"
echo "  Auto Publisher - Setup Wizard"
echo "================================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "ERROR: python3 is required but not found."
    echo "Please install Python 3.8+ and try again."
    exit 1
fi
echo "Python3: $(python3 --version)"

# Check if config already exists
if [ -f "$CONFIG_FILE" ]; then
    echo ""
    echo "Config file already exists: $CONFIG_FILE"
    read -p "Overwrite? (y/N): " overwrite
    if [ "$overwrite" != "y" ] && [ "$overwrite" != "Y" ]; then
        echo "Setup cancelled. Edit config.json manually or run /auto-publisher config"
        exit 0
    fi
fi

echo ""
echo "--- Platform Configuration ---"
echo ""

# Platform type
read -p "Platform type [wordpress]: " platform_type
platform_type=${platform_type:-wordpress}

# Site URL
read -p "Your website URL (e.g., https://example.com): " site_url
site_url=${site_url%/}

# Username
read -p "WordPress username: " wp_username

echo ""
echo "--- WordPress Application Password ---"
echo "You need to generate an Application Password in WordPress:"
echo "  1. Login to $site_url/wp-admin/"
echo "  2. Go to Users > Your Profile"
echo "  3. Scroll to 'Application Passwords'"
echo "  4. Enter name 'auto-publisher', click 'Add New'"
echo "  5. Copy the generated password"
echo ""
read -p "Have you set the WP_APP_PASSWORD environment variable? (y/N): " has_password

if [ "$has_password" != "y" ] && [ "$has_password" != "Y" ]; then
    echo ""
    echo "Please set it before publishing:"
    echo "  export WP_APP_PASSWORD='xxxx xxxx xxxx xxxx'"
    echo ""
    echo "Or add to your OpenClaw settings (~/.openclaw/openclaw.json):"
    echo '  { "skills": { "entries": { "auto-publisher": { "env": { "WP_APP_PASSWORD": "..." } } } } }'
fi

echo ""
echo "--- Publishing Settings ---"
echo ""

read -p "Posts per day [5]: " posts_per_day
posts_per_day=${posts_per_day:-5}

read -p "Content language (en/zh/ja/ko) [zh]: " language
language=${language:-zh}

read -p "Post status (publish/draft) [publish]: " post_status
post_status=${post_status:-publish}

read -p "Categories (comma-separated) [News,World]: " categories
categories=${categories:-News,World}

echo ""
echo "--- Image Source ---"
echo "Options: unsplash, pexels, pixabay, none (RSS images only)"
read -p "Image source [none]: " image_source
image_source=${image_source:-none}

# Generate config
IFS=',' read -ra CAT_ARRAY <<< "$categories"
CAT_JSON=""
for cat in "${CAT_ARRAY[@]}"; do
    cat=$(echo "$cat" | xargs)  # trim whitespace
    if [ -n "$CAT_JSON" ]; then CAT_JSON="$CAT_JSON, "; fi
    CAT_JSON="$CAT_JSON\"$cat\""
done

IMAGE_BLOCK='"images": { "fallback_from_rss": true }'
if [ "$image_source" != "none" ]; then
    KEY_ENV="${image_source^^}_API_KEY"
    IMAGE_BLOCK="\"images\": { \"source\": \"$image_source\", \"api_key_env\": \"$KEY_ENV\", \"fallback_from_rss\": true }"
fi

cat > "$CONFIG_FILE" << CONFIGEOF
{
  "platform": {
    "type": "$platform_type",
    "url": "$site_url",
    "username": "$wp_username",
    "auth_method": "application_password",
    "app_password_env": "WP_APP_PASSWORD"
  },
  "news_sources": [
    {
      "type": "rss",
      "url": "https://feeds.bbci.co.uk/news/world/rss.xml",
      "name": "BBC World News",
      "max_items": 5
    },
    {
      "type": "rss",
      "url": "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
      "name": "NYT World",
      "max_items": 5
    },
    {
      "type": "rss",
      "url": "https://www.aljazeera.com/xml/rss/all.xml",
      "name": "Al Jazeera",
      "max_items": 3
    }
  ],
  "publishing": {
    "posts_per_day": $posts_per_day,
    "categories": [$CAT_JSON],
    "default_tags": ["news", "global"],
    "status": "$post_status",
    "language": "$language",
    "content_template": "default"
  },
  $IMAGE_BLOCK,
  "schedule": {
    "enabled": true,
    "cron": "0 9 * * *",
    "timezone": "Asia/Shanghai"
  },
  "content_rules": {
    "min_words": 300,
    "max_words": 800,
    "include_source_link": true,
    "include_image_credit": true,
    "seo_optimize": true
  }
}
CONFIGEOF

echo ""
echo "================================================"
echo "  Setup Complete!"
echo "================================================"
echo ""
echo "Config saved to: $CONFIG_FILE"
echo ""
echo "Next steps:"
echo "  1. Set environment variable: export WP_APP_PASSWORD='your-app-password'"
echo "  2. Test with: /auto-publisher preview"
echo "  3. Publish with: /auto-publisher publish"
echo ""
echo "Edit $CONFIG_FILE to customize news sources, categories, etc."
