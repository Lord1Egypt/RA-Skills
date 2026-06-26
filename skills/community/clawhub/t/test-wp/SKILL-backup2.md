---
name: wordpress-auto-publish
description: Automatically publish Markdown articles to WordPress blog. Supports REST API publishing, batch processing, draft management, category and tag management.
version: 1.0.0
date: 2026-04-04
compatibility: OpenClaw >= 2026.3.0
status: Stable
---

# WordPress Auto-Publish Skill

## 🎯 Skill Description

Automatically publish Markdown articles to WordPress blog. Supports:
- Publishing articles via REST API
- Batch publishing articles
- Scheduled publishing
- Draft management
- Markdown to HTML conversion
- Category and tag management
- Featured image upload

## 📋 Features

### Core Features
- ✅ Automatically publish Markdown articles to WordPress
- ✅ Support draft and published status
- ✅ Batch processing multiple articles
- ✅ Automatic HTML conversion
- ✅ Category and tag management
- ✅ Featured image support

### Management Features
- ✅ List all articles
- ✅ Update/delete articles
- ✅ Manage media library
- ✅ Category and tag management

### Tool Features
- ✅ Configuration management
- ✅ Error handling and logging
- ✅ Environment variable support
- ✅ Batch processing queue

## 🚀 Quick Start

### Step 1: Install dependencies
```bash
npm install axios marked
```

### Step 2: Configure WordPress
1. Enable REST API in WordPress
2. Create application password
3. Set WordPress site URL

### Step 3: Configure skill
1. Copy `config.example.js` to `config.js`
2. Fill in WordPress configuration information
3. Set article directory

### Step 4: Usage examples
```bash
# Publish single article
node publish.js --file posts/my-article.md

# Publish as draft
node publish.js --file posts/draft.md --draft

# Batch publish
node batch-publish.js --dir posts/
```

## 📁 Project Structure

```
wordpress-auto-publish/
├── SKILL.md                    # Skill documentation
├── package.json               # Project configuration
├── config.js                  # Configuration file
├── wordpress-api.js           # WordPress API client
├── publish.js                 # Main publishing script
├── batch-publish.js           # Batch publishing script
├── list-posts.js              # List articles
├── delete-post.js             # Delete article
├── upload-media.js            # Upload media files
├── manage-categories.js       # Manage categories
├── manage-tags.js             # Manage tags
├── posts/                     # Article directory
│   └── example-post.md       # Example article
└── scripts/                  # Tool scripts
    └── setup-wordpress.sh    # Installation script
```

## 🔧 Detailed Usage Guide

### 1. WordPress REST API Configuration
1. Log in to WordPress admin
2. Go to **Users → Profile**
3. Find **Application Passwords** at the bottom
4. Create new password (e.g., `your-app-password`)
5. Save the generated password

### 2. Get WordPress Configuration Information
- **WordPress URL**: Your WordPress site URL (e.g., `https://your-site.com`)
- **Username**: WordPress username
- **Application Password**: Password generated in previous step

### 3. Configuration File Setup
Create `config.js`:
```javascript
module.exports = {
  // WordPress configuration
  wordpress: {
    url: process.env.WORDPRESS_URL || 'https://your-site.com',
    username: process.env.WORDPRESS_USERNAME || 'admin',
    password: process.env.WORDPRESS_PASSWORD || 'your-app-password',
    
    // API endpoints
    apiBase: '/wp-json/wp/v2',
    
    // Default settings
    defaultStatus: 'draft', // draft, publish, pending, private
    defaultAuthor: 1,
    
    // Media settings
    mediaPath: './media',
    supportedFormats: ['jpg', 'jpeg', 'png', 'gif', 'pdf', 'doc', 'docx']
  },
  
  // Article configuration
  posts: {
    directory: process.env.POSTS_DIR || './posts',
    defaultCategory: 1,
    defaultTags: [],
    
    // Markdown conversion settings
    markdownOptions: {
      gfm: true,
      breaks: true,
      sanitize: false
    }
  },
  
  // Publishing settings
  publish: {
    batchSize: 5,
    delayBetweenPosts: 2000, // milliseconds
    maxRetries: 3,
    retryDelay: 1000
  },
  
  // Logging settings
  logging: {
    level: 'info',
    file: './logs/wordpress-publish.log',
    console: true
  }
};
```

## 📝 Usage Examples

### Publish single article
```bash
node publish.js --file posts/my-article.md --status publish
```

### Batch publish
```bash
node batch-publish.js --dir posts/ --status draft
```

### List all articles
```bash
node list-posts.js --status any --per-page 20
```

### Upload featured image
```bash
node upload-media.js --file images/featured.jpg --post-id 123
```

### Manage categories
```bash
# List categories
node manage-categories.js --list

# Create category
node manage-categories.js --create --name "Technology" --slug "tech"
```

## 🔍 Troubleshooting

### Common Issues

1. **API connection failed**
   - Check if WordPress URL is correct
   - Verify application password
   - Ensure REST API is enabled

2. **Authentication failed**
   - Check username and password
   - Regenerate application password
   - Verify user permissions

3. **Article publishing failed**
   - Check network connection
   - Verify article format
   - Check error logs

### Error Codes
- `401`: Authentication failed, check credentials
- `403`: Insufficient permissions, check user role
- `404`: Resource does not exist, check URL
- `500`: Server error, check WordPress logs

## 📊 Performance Optimization

### Batch Processing Recommendations
- Process no more than 10 articles at a time
- Add delays to avoid server pressure
- Use draft mode for verification first

### Resource Management
- Regularly clean log files
- Backup configuration files
- Use environment variables to manage sensitive information

## 🎯 Skill Trigger Conditions

Automatically triggered when OpenClaw detects the following needs:
- Automatically publish articles to WordPress
- Batch or scheduled publishing
- WordPress API integration needs
- Markdown to WordPress conversion

## 🔄 Update Plan

### v1.1.0 (Planned)
- [ ] Scheduled publishing feature
- [ ] Article import/export
- [ ] Multi-site support
- [ ] Advanced media management

### v1.2.0 (Planned)
- [ ] Theme template support
- [ ] SEO optimization
- [ ] Social media sharing
- [ ] Analytics integration

## 📞 Support and Feedback

If you have questions or suggestions:
1. Check detailed documentation
2. Run `node publish.js --help` to view help
3. Check error logs for detailed information
4. Submit issues to GitHub repository

---

**Note**: This skill requires WordPress 5.0+ version with REST API functionality enabled.