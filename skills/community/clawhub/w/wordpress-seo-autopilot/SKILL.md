---
name: wordpress-seo-autopilot
description: "Automate comprehensive WordPress SEO optimization including meta tags, schema markup, internal linking, and RankMath integration."
version: "1.0.0"
---

# WordPress SEO Autopilot

Transform your WordPress site into an SEO powerhouse with comprehensive automation. This skill handles everything from meta tag optimization and schema markup generation to internal linking strategies and RankMath integration, delivering enterprise-level SEO without the manual work.

## Overview

WordPress SEO Autopilot eliminates the tedious manual work of optimizing WordPress sites for search engines. It integrates directly with your WordPress REST API, RankMath SEO plugin, Google Search Console, and other essential SEO tools to provide:

- **Automated Meta Optimization**: Generates compelling titles, descriptions, and Open Graph tags
- **Schema Markup Generation**: Creates structured data for articles, products, events, and local businesses  
- **Internal Linking Strategy**: Identifies and implements strategic internal link opportunities
- **Content Analysis**: Performs keyword density analysis and readability scoring
- **Technical SEO Audits**: Checks site speed, mobile-friendliness, and crawlability issues
- **RankMath Integration**: Syncs with RankMath Pro for advanced SEO features
- **Bulk Operations**: Processes hundreds of posts/pages in automated workflows

Perfect for agencies, content marketers, and WordPress developers managing multiple sites or large content libraries.

## Quick Start

Get started immediately with these example prompts:

```
Audit my WordPress site at example.com and generate a complete SEO report with actionable recommendations
```

```
Optimize the meta tags for all blog posts published in the last 30 days, focusing on click-through rate improvement
```

```
Create schema markup for my WooCommerce product pages and implement internal linking between related products
```

```
Analyze my top 20 pages in Google Search Console and suggest title/description improvements to boost rankings
```

```
Set up automated SEO workflows for new blog posts including meta optimization, schema generation, and internal linking
```

## Capabilities

### Meta Tag Optimization
- **Smart Title Generation**: Creates compelling, keyword-optimized titles under 60 characters
- **Description Crafting**: Generates meta descriptions with clear CTAs and keyword placement
- **Open Graph & Twitter Cards**: Optimizes social media sharing with proper OG tags
- **Bulk Processing**: Updates hundreds of posts simultaneously with consistent formatting

### Schema Markup & Structured Data
- **Article Schema**: Implements proper structured data for blog posts and news articles
- **Product Schema**: Enhances WooCommerce products with rich snippets
- **Local Business Schema**: Optimizes location-based businesses for local search
- **FAQ & How-To Schema**: Creates structured data for informational content
- **Review Schema**: Implements star ratings and review markup

### Internal Linking Strategy
- **Contextual Link Discovery**: Identifies relevant internal linking opportunities using semantic analysis
- **Anchor Text Optimization**: Suggests natural, keyword-rich anchor text variations
- **Link Equity Distribution**: Balances internal link flow to boost important pages
- **Automated Implementation**: Inserts internal links directly into post content

### Technical SEO Analysis
- **Core Web Vitals Monitoring**: Tracks LCP, FID, and CLS metrics
- **Mobile-First Indexing**: Ensures mobile optimization compliance
- **Crawlability Assessment**: Identifies blocked resources and crawl errors
- **Site Speed Analysis**: Provides specific performance improvement recommendations

### RankMath Integration
- **Score Optimization**: Automatically improves RankMath SEO scores
- **Keyword Tracking**: Syncs with RankMath's rank tracking features
- **Content Analysis**: Leverages RankMath's content AI for optimization suggestions
- **Schema Sync**: Coordinates schema markup with RankMath settings

## Configuration

### Required Environment Variables

```bash
WORDPRESS_URL=https://yoursite.com
WORDPRESS_USERNAME=your_admin_username
WORDPRESS_APP_PASSWORD=your_app_password
RANKMATH_API_KEY=your_rankmath_api_key
```

### Optional Configuration

```bash
GOOGLE_SEARCH_CONSOLE_KEY=path/to/service-account.json
SEMRUSH_API_KEY=your_semrush_key
AHREFS_API_TOKEN=your_ahrefs_token
```

### WordPress Setup
1. Install WordPress Application Passwords plugin (or use WordPress 5.6+)
2. Generate application password: Users → Profile → Application Passwords
3. Install RankMath SEO plugin (free or pro)
4. Enable WordPress REST API (usually enabled by default)

### RankMath Configuration
1. Install RankMath SEO plugin
2. Complete setup wizard with your target keywords
3. Enable API access in RankMath → General Settings → API
4. Copy your API key to environment variables

## Example Outputs

### SEO Audit Report
```
📊 WordPress SEO Audit - example.com
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 PRIORITY ISSUES (Fix First)
• 47 pages missing meta descriptions
• 23 images without alt text  
• 12 posts with titles over 60 characters
• Schema markup missing on product pages

📈 OPTIMIZATION OPPORTUNITIES
• Internal linking: 156 new link opportunities identified
• Page speed: 3.2s average load time (target: <2s)
• Mobile usability: 5 issues found

🔧 AUTOMATED FIXES AVAILABLE
✅ Generate meta descriptions for 47 pages
✅ Optimize 23 title tags for better CTR
✅ Implement schema markup for products
✅ Add 89 strategic internal links
```

### Meta Tag Optimization
```
🏷️ Meta Tags Optimized - "Ultimate Guide to WordPress SEO"

OLD TITLE: WordPress SEO Tips and Tricks for Better Rankings
NEW TITLE: WordPress SEO Guide: 47 Proven Tips to Rank #1 (2024)

OLD DESCRIPTION: Learn about WordPress SEO and how to improve your rankings
NEW DESCRIPTION: Master WordPress SEO with our complete guide. 47 expert tips, tools, and strategies to boost rankings, traffic, and conversions in 2024.

📊 IMPROVEMENTS
• Title length: 67 → 52 characters ✅
• Description length: 58 → 156 characters ✅  
• Focus keyword density: 0.8% → 1.2% ✅
• Readability score: 67 → 78 ✅
```

## Tips & Best Practices

### Content Optimization Strategy
- **Focus on User Intent**: Optimize for what users actually search for, not just keywords
- **Long-tail Opportunities**: Target specific, lower-competition phrases for quicker wins
- **Content Clusters**: Create topic clusters with pillar pages and supporting content
- **Update Frequency**: Refresh old content regularly to maintain search visibility

### Technical SEO Priorities
- **Core Web Vitals First**: Prioritize page speed and user experience metrics
- **Mobile Optimization**: Ensure all pages pass Google's mobile-friendly test
- **Schema Implementation**: Start with article/product schema, then expand to more specific types
- **Internal Linking**: Aim for 3-5 internal links per 1000 words of content

### RankMath Optimization
- **Target Score 80+**: Aim for green scores on all important pages
- **Multiple Keywords**: Optimize for 2-3 related keywords per page
- **Content AI**: Use RankMath's content suggestions for competitive analysis
- **Rank Tracking**: Monitor keyword positions and adjust strategies accordingly

### Automation Workflows
- **New Content Process**: Set up automatic meta generation and schema markup for new posts
- **Monthly Audits**: Schedule comprehensive SEO audits to catch issues early
- **Competitor Monitoring**: Track competitor keyword rankings and content strategies
- **Performance Alerts**: Set up notifications for ranking drops or technical issues

## Safety & Guardrails

### Content Boundaries
- **No Keyword Stuffing**: Maintains natural keyword density between 0.5-2%
- **Brand Voice Preservation**: Adapts to your existing content style and tone
- **Manual Review Required**: Flags significant changes for human approval
- **Backup Creation**: Always creates backups before making bulk changes

### Technical Limitations
- **Rate Limiting**: Respects WordPress API limits to prevent server overload
- **Plugin Compatibility**: Checks for conflicts with existing SEO plugins
- **Theme Restrictions**: Some schema implementations may require theme modifications
- **Server Resources**: Large sites may need processing in smaller batches

### Data Privacy
- **No Content Storage**: Processes content without storing on external servers
- **API Security**: Uses encrypted connections and secure authentication
- **GDPR Compliance**: Respects privacy settings and cookie consent
- **Local Processing**: Sensitive operations performed locally when possible

### Quality Assurance
- **Human Oversight**: Recommends manual review for critical pages
- **A/B Testing**: Suggests testing meta tag changes on less critical pages first
- **Rollback Capability**: Maintains version history for easy rollbacks
- **Performance Monitoring**: Tracks impact of changes on site performance

## Troubleshooting

### Common WordPress Issues

**Q: Getting "REST API disabled" error**
A: Enable REST API in WordPress admin → Settings → Permalinks → Save Changes. Some security plugins block REST API access.

**Q: Application password authentication fails**
A: Ensure WordPress is version 5.6+ or install Application Passwords plugin. Check username/password combination in wp-admin.

**Q: Bulk operations timing out**
A: Reduce batch sizes in configuration. Process 10-20 posts at a time for large sites.

### RankMath Integration Issues

**Q: RankMath API key not working**
A: Verify API is enabled in RankMath → General Settings → API. Copy key exactly without extra spaces.

**Q: Schema markup conflicts**
A: Disable other schema plugins. RankMath handles most schema types automatically.

**Q: SEO scores not updating**
A: Clear RankMath cache and WordPress object cache. Scores update after content changes are processed.

### Performance Optimization

**Q: Site slowing down during optimization**
A: Enable maintenance mode during bulk operations. Schedule optimizations during low-traffic periods.

**Q: Memory limit errors**
A: Increase PHP memory limit to 512MB minimum. Contact hosting provider if needed.

**Q: Database queries timing out**
A: Optimize WordPress database and enable query caching. Consider dedicated hosting for large sites.

For additional support, check the skill documentation at https://github.com/ncreighton/empire-skills or contact the ClawHub community.