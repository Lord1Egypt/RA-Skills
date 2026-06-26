#!/usr/bin/env node
/**
 * Content Pipeline Framework - Universal CLI
 * 
 * Manage multiple content creation accounts from a single interface.
 * Bootstrap new accounts, generate content, publish, and analyze performance.
 * 
 * Usage:
 *   ./cli.js create <account> --template <template>
 *   ./cli.js generate <account> --type <type> [--post]
 *   ./cli.js analytics <account> [--auto-improve]
 *   ./cli.js schedule <account> --batch <count>
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// Framework core components
const ContentGenerator = require('./core/ContentGenerator');
const Publisher = require('./core/Publisher');
const AnalyticsEngine = require('./core/AnalyticsEngine');
const PostingScheduler = require('./core/PostingScheduler');

class ContentPipelineCLI {
  constructor() {
    this.frameworkRoot = __dirname;
    this.accountsDir = path.join(this.frameworkRoot, 'accounts');
    this.templatesDir = path.join(this.frameworkRoot, 'templates');
    
    // Ensure directories exist
    [this.accountsDir, this.templatesDir].forEach(dir => {
      if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
      }
    });
  }

  async run() {
    const args = process.argv.slice(2);
    const command = args[0];
    const account = args[1];

    switch (command) {
      case 'create':
        await this.createAccount(account, this._getArgs(args));
        break;
      case 'generate':
        await this.generateContent(account, this._getArgs(args));
        break;
      case 'post':
        await this.postContent(account, this._getArgs(args));
        break;
      case 'schedule':
        await this.showSchedule(account, this._getArgs(args));
        break;
      case 'analytics':
        await this.runAnalytics(account, this._getArgs(args));
        break;
      case 'config':
        await this.configureAccount(account, this._getArgs(args));
        break;
      case 'list':
        await this.listAccounts();
        break;
      case 'help':
        this.showHelp();
        break;
      default:
        console.error(`Unknown command: ${command}`);
        this.showHelp();
        process.exit(1);
    }
  }

  /**
   * Create new account from template
   */
  async createAccount(accountName, args) {
    const template = args.template;
    if (!template) {
      console.error('❌ Template required: --template <template-name>');
      return;
    }

    const templateDir = path.join(this.templatesDir, template);
    if (!fs.existsSync(templateDir)) {
      console.error(`❌ Template '${template}' not found in ${this.templatesDir}`);
      return;
    }

    const accountDir = path.join(this.accountsDir, accountName);
    if (fs.existsSync(accountDir)) {
      console.error(`❌ Account '${accountName}' already exists`);
      return;
    }

    console.log(`🚀 Creating account '${accountName}' from template '${template}'...`);

    // Copy template to account directory
    this._copyDirectory(templateDir, accountDir);

    // Update account-specific config
    const configPath = path.join(accountDir, 'config.json');
    if (fs.existsSync(configPath)) {
      const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
      config.account = {
        ...config.account,
        name: accountName,
        template,
        createdAt: new Date().toISOString()
      };
      fs.writeFileSync(configPath, JSON.stringify(config, null, 2));
    }

    console.log(`✅ Account '${accountName}' created successfully!`);
    console.log(`📁 Location: ${accountDir}`);
    console.log(`⚙️  Configure: ./cli.js config ${accountName} --handle @${accountName}`);
  }

  /**
   * Generate content for account
   */
  async generateContent(accountName, args) {
    const accountDir = this._getAccountDir(accountName);
    const config = this._loadAccountConfig(accountDir);
    
    // Load account-specific generator
    const GeneratorClass = this._loadGenerator(config.account.template);
    const generator = new GeneratorClass(config);

    const contentType = args.type;
    if (!contentType) {
      console.error('❌ Content type required: --type <type>');
      console.log('Available types:', generator.getSupportedTypes().join(', '));
      return;
    }

    // Prepare output directory
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
    const outputDir = path.join(accountDir, 'output', `${timestamp}-${contentType}`);

    console.log(`🎨 Generating '${contentType}' content for ${accountName}...`);

    try {
      const result = await generator.generate(contentType, args, outputDir);
      console.log(`✅ Content generated successfully!`);
      console.log(`📁 Output: ${outputDir}`);
      console.log(`⏱️  Duration: ${result.duration}ms`);

      // Auto-post if requested
      if (args.post) {
        await this._postGenerated(accountDir, config, result, args);
      }

      return result;
    } catch (error) {
      console.error('❌ Content generation failed:', error.message);
      process.exit(1);
    }
  }

  /**
   * Post content to platforms
   */
  async postContent(accountName, args) {
    const accountDir = this._getAccountDir(accountName);
    const config = this._loadAccountConfig(accountDir);
    const publisher = new Publisher(config);

    const contentDir = args.dir || args.content;
    if (!contentDir) {
      console.error('❌ Content directory required: --dir <path>');
      return;
    }

    const caption = args.caption;
    if (!caption) {
      console.error('❌ Caption required: --caption "<text>"');
      return;
    }

    // Load content metadata
    const content = this._loadContentFromDir(contentDir);

    try {
      const result = await publisher.post(content, caption, {
        platform: args.platform || 'tiktok',
        draft: args.draft || false,
        schedule: args.schedule || null
      });

      console.log(`✅ Posted successfully!`);
      if (result.postId) console.log(`📋 Post ID: ${result.postId}`);
      if (result.url) console.log(`🔗 URL: ${result.url}`);

    } catch (error) {
      console.error('❌ Posting failed:', error.message);
      process.exit(1);
    }
  }

  /**
   * Run analytics and optimization
   */
  async runAnalytics(accountName, args) {
    const accountDir = this._getAccountDir(accountName);
    const config = this._loadAccountConfig(accountDir);
    const analytics = new AnalyticsEngine(config);

    const days = parseInt(args.days || '7');
    const autoImplement = args['auto-improve'] || args['auto-implement'] || false;

    console.log(`📊 Analyzing ${accountName} performance (last ${days} days)...`);

    try {
      const report = await analytics.generateReport(accountDir, {
        days,
        autoImplement,
        includeRevenue: config.revenuecat?.enabled || false
      });

      console.log('\n═══ ANALYTICS SUMMARY ═══');
      console.log(`📈 Total Views: ${report.metrics.posts.totalViews.toLocaleString()}`);
      console.log(`💬 Avg Engagement: ${(report.metrics.posts.avgEngagementRate * 100).toFixed(1)}%`);
      console.log(`📝 Posts Published: ${report.metrics.posts.posts.length}`);

      if (report.insights.alerts.length > 0) {
        console.log('\n🚨 ALERTS:');
        report.insights.alerts.forEach(alert => {
          console.log(`  • ${alert.message} (${alert.severity})`);
        });
      }

      if (report.insights.opportunities.length > 0) {
        console.log('\n💡 OPPORTUNITIES:');
        report.insights.opportunities.forEach(opp => {
          console.log(`  • ${opp.message}`);
        });
      }

      if (autoImplement && report.insights.actions.length > 0) {
        console.log('\n🔧 ACTIONS IMPLEMENTED:');
        report.insights.actions.forEach(action => {
          console.log(`  ✅ ${action.description || action.type}`);
        });
      }

      console.log(`\n📋 Full report: ${report.reportPath}`);

    } catch (error) {
      console.error('❌ Analytics failed:', error.message);
      process.exit(1);
    }
  }

  /**
   * Configure account settings
   */
  async configureAccount(accountName, args) {
    const accountDir = this._getAccountDir(accountName);
    const configPath = path.join(accountDir, 'config.json');
    const config = this._loadAccountConfig(accountDir);

    let updated = false;

    // Update handle
    if (args.handle) {
      config.app = config.app || {};
      config.app.handle = args.handle;
      console.log(`📱 Handle set to: ${args.handle}`);
      updated = true;
    }

    // Update integration ID
    if (args['integration-id']) {
      config.postiz = config.postiz || {};
      config.postiz.integrationId = args['integration-id'];
      console.log(`🔗 Integration ID set to: ${args['integration-id']}`);
      updated = true;
    }

    // Update API key
    if (args['api-key']) {
      config.postiz = config.postiz || {};
      config.postiz.apiKey = args['api-key'];
      console.log(`🔑 API key updated`);
      updated = true;
    }

    if (updated) {
      fs.writeFileSync(configPath, JSON.stringify(config, null, 2));
      console.log(`✅ Configuration updated: ${configPath}`);
    } else {
      console.log('📋 Current configuration:');
      console.log(JSON.stringify(config, null, 2));
    }
  }

  /**
   * Show posting schedule for account
   */
  async showSchedule(accountName, args) {
    const accountDir = this._getAccountDir(accountName);
    const config = this._loadAccountConfig(accountDir);
    const scheduler = new PostingScheduler(config);

    try {
      const accountAge = scheduler.getAccountAge();
      const phase = scheduler.getAccountPhase();
      const postsPerWeek = scheduler.getPostsPerWeek();
      
      console.log(`\n📅 POSTING SCHEDULE FOR ${accountName.toUpperCase()}`);
      console.log(`═══════════════════════════════════════════`);
      console.log(`📊 Account Age: ${accountAge} days`);
      console.log(`🎯 Phase: ${phase}`);
      console.log(`📝 Target: ${postsPerWeek} posts/week`);
      console.log(`⏰ Timezone: ${config.posting?.timezone || 'Europe/London'}`);

      if (args.next) {
        // Show next posting slot
        console.log(`\n⏭️  NEXT POSTING SLOT:`);
        const nextSlot = scheduler.getNextPostingSlot([]);
        console.log(`   📅 ${this._formatDateTime(nextSlot)}`);
        console.log(`   ⏱️  ${this._formatTimeFromNow(nextSlot)}`);
        
      } else {
        // Show weekly schedule
        const weeks = parseInt(args.week || '1');
        const now = new Date();
        
        for (let w = 0; w < weeks; w++) {
          const weekStart = this._getWeekStart(now, w);
          const schedule = scheduler.getWeekSchedule(weekStart);
          
          console.log(`\n📅 WEEK ${w + 1} (${this._formatDate(weekStart)}):`);
          
          if (schedule.length === 0) {
            console.log(`   📭 No posts scheduled`);
          } else {
            schedule.forEach((slot, index) => {
              const dayName = this._getDayName(slot);
              const timeStr = this._formatTime(slot);
              const isPast = slot < now;
              const icon = isPast ? '✅' : '⏰';
              
              console.log(`   ${icon} ${dayName} ${timeStr}`);
            });
          }
        }
        
        // Check for overdue posts
        const recentPosts = []; // In real usage, load from database/analytics
        if (scheduler.isOverdue(recentPosts)) {
          console.log(`\n🚨 OVERDUE POSTS DETECTED!`);
          console.log(`   Some scheduled posts may have been missed.`);
        }
      }

    } catch (error) {
      console.error(`❌ Schedule error: ${error.message}`);
      process.exit(1);
    }
  }

  /**
   * List all accounts
   */
  async listAccounts() {
    if (!fs.existsSync(this.accountsDir)) {
      console.log('📭 No accounts found');
      return;
    }

    const accounts = fs.readdirSync(this.accountsDir).filter(name => 
      fs.statSync(path.join(this.accountsDir, name)).isDirectory()
    );

    if (accounts.length === 0) {
      console.log('📭 No accounts found');
      return;
    }

    console.log('📋 Available accounts:');
    accounts.forEach(name => {
      try {
        const config = this._loadAccountConfig(path.join(this.accountsDir, name));
        const handle = config.app?.handle || 'No handle set';
        const template = config.account?.template || 'Unknown template';
        console.log(`  • ${name} (${handle}) - ${template}`);
      } catch (error) {
        console.log(`  • ${name} - Configuration error`);
      }
    });
  }

  /**
   * Show help
   */
  showHelp() {
    console.log(`
Content Pipeline Framework - Universal CLI

COMMANDS:
  create <account> --template <template>     Create new account
  generate <account> --type <type> [--post] Generate content
  post <account> --dir <path> --caption "..." Post content
  schedule <account> [--next] [--week N]    Show posting schedule
  analytics <account> [--auto-improve]      Run analytics
  config <account> [--handle @handle]       Configure account
  list                                       List accounts
  help                                       Show this help

EXAMPLES:
  # Create new account
  ./cli.js create my-brand --template example-nostalgia
  
  # Generate and post content
  ./cli.js generate my-brand --type showcase --post --caption "Check this out"
  
  # Show posting schedule
  ./cli.js schedule my-brand              # This week's schedule
  ./cli.js schedule my-brand --next       # Next posting slot
  ./cli.js schedule my-brand --week 2     # Next 2 weeks
  
  # Run analytics with auto-optimization
  ./cli.js analytics my-brand --days 7 --auto-improve
`);
  }

  // Helper methods

  _getArgs(args) {
    const parsed = {};
    for (let i = 2; i < args.length; i++) {
      if (args[i].startsWith('--')) {
        const key = args[i].slice(2);
        const value = args[i + 1] && !args[i + 1].startsWith('--') ? args[i + 1] : true;
        parsed[key] = value;
        if (value !== true) i++; // Skip next arg if it was a value
      }
    }
    return parsed;
  }

  _getAccountDir(accountName) {
    // Sanitise: only allow alphanumeric, hyphens, underscores
    if (!/^[a-zA-Z0-9_-]+$/.test(accountName)) {
      console.error(`❌ Invalid account name '${accountName}' — only alphanumeric, hyphens, and underscores allowed`);
      process.exit(1);
    }
    const accountDir = path.join(this.accountsDir, accountName);
    // Path traversal guard: ensure resolved path stays within accountsDir
    if (!path.resolve(accountDir).startsWith(path.resolve(this.accountsDir))) {
      console.error(`❌ Invalid account path`);
      process.exit(1);
    }
    if (!fs.existsSync(accountDir)) {
      console.error(`❌ Account '${accountName}' not found`);
      process.exit(1);
    }
    return accountDir;
  }

  _loadAccountConfig(accountDir) {
    const configPath = path.join(accountDir, 'config.json');
    if (!fs.existsSync(configPath)) {
      console.error(`❌ Config not found: ${configPath}`);
      process.exit(1);
    }
    return JSON.parse(fs.readFileSync(configPath, 'utf8'));
  }

  _loadGenerator(templateName) {
    // Sanitise: only allow alphanumeric, hyphens, underscores
    if (!/^[a-zA-Z0-9_-]+$/.test(templateName)) {
      console.error(`❌ Invalid template name '${templateName}' — only alphanumeric, hyphens, and underscores allowed`);
      process.exit(1);
    }
    const generatorPath = path.join(this.templatesDir, templateName, 'generator.js');
    // Path traversal guard: ensure resolved path stays within templatesDir
    if (!path.resolve(generatorPath).startsWith(path.resolve(this.templatesDir))) {
      console.error(`❌ Invalid template path`);
      process.exit(1);
    }
    if (!fs.existsSync(generatorPath)) {
      console.error(`❌ Generator not found: ${generatorPath}`);
      process.exit(1);
    }
    return require(generatorPath);
  }

  _copyDirectory(src, dest) {
    // Path traversal guard: both src and dest must stay within framework root
    const resolvedSrc = path.resolve(src);
    const resolvedDest = path.resolve(dest);
    const resolvedRoot = path.resolve(this.frameworkRoot);
    if (!resolvedSrc.startsWith(resolvedRoot) || !resolvedDest.startsWith(resolvedRoot)) {
      console.error(`❌ Path traversal blocked: copy must stay within framework directory`);
      process.exit(1);
    }

    if (!fs.existsSync(dest)) {
      fs.mkdirSync(dest, { recursive: true });
    }
    
    const items = fs.readdirSync(src);
    for (const item of items) {
      // Skip dotfiles and suspicious names
      if (item.startsWith('.') || item.includes('..')) continue;
      const srcPath = path.join(src, item);
      const destPath = path.join(dest, item);
      
      if (fs.statSync(srcPath).isDirectory()) {
        this._copyDirectory(srcPath, destPath);
      } else {
        fs.copyFileSync(srcPath, destPath);
      }
    }
  }

  _loadContentFromDir(contentDir) {
    // Load generated content metadata
    const slides = [];
    for (let i = 1; i <= 10; i++) {
      const slidePath = path.join(contentDir, `slide${i}.png`);
      if (fs.existsSync(slidePath)) {
        slides.push(slidePath);
      }
    }

    return {
      slides,
      outputDir: contentDir,
      contentType: path.basename(contentDir).split('-').slice(-1)[0]
    };
  }

  // Date/time formatting helpers for schedule command

  _formatDateTime(date) {
    const options = {
      weekday: 'short',
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      timeZoneName: 'short'
    };
    return date.toLocaleDateString('en-GB', options);
  }

  _formatDate(date) {
    const options = {
      weekday: 'short',
      month: 'short',
      day: 'numeric'
    };
    return date.toLocaleDateString('en-GB', options);
  }

  _formatTime(date) {
    const options = {
      hour: '2-digit',
      minute: '2-digit'
    };
    return date.toLocaleTimeString('en-GB', options);
  }

  _formatTimeFromNow(date) {
    const now = new Date();
    const diffMs = date.getTime() - now.getTime();
    const diffHours = Math.round(diffMs / (1000 * 60 * 60));
    const diffDays = Math.floor(diffHours / 24);
    
    if (diffMs < 0) {
      return 'Overdue';
    } else if (diffHours < 1) {
      const diffMins = Math.round(diffMs / (1000 * 60));
      return `in ${diffMins} minutes`;
    } else if (diffHours < 24) {
      return `in ${diffHours} hours`;
    } else if (diffDays === 1) {
      return 'tomorrow';
    } else {
      return `in ${diffDays} days`;
    }
  }

  _getDayName(date) {
    const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
    return days[date.getDay()];
  }

  _getWeekStart(referenceDate, weekOffset = 0) {
    const date = new Date(referenceDate);
    date.setDate(date.getDate() + (weekOffset * 7));
    
    // Get Monday of this week
    const dayOfWeek = date.getDay();
    const diffToMonday = dayOfWeek === 0 ? -6 : 1 - dayOfWeek; // Convert Sunday=0 to -6
    date.setDate(date.getDate() + diffToMonday);
    date.setHours(0, 0, 0, 0);
    
    return date;
  }

  async _postGenerated(accountDir, config, content, args) {
    const publisher = new Publisher(config);
    
    // Generate caption if not provided
    const caption = args.caption || content.hook || 'New post';
    
    try {
      const result = await publisher.post(content, caption, {
        draft: args.draft !== false // Default to draft
      });
      console.log('📤 Posted as draft - add sound and publish from TikTok inbox');
    } catch (error) {
      console.error('❌ Auto-posting failed:', error.message);
    }
  }
}

// Run CLI if called directly
if (require.main === module) {
  const cli = new ContentPipelineCLI();
  cli.run().catch(error => {
    console.error('Fatal error:', error.message);
    process.exit(1);
  });
}

module.exports = ContentPipelineCLI;