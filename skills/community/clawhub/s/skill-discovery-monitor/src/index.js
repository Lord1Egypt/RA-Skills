require('dotenv').config();
const express = require('express');
const SkillPayment = require('./payment');
const ClawhubScraper = require('./scrapers/clawhub');
const GitHubScraper = require('./scrapers/github');
const NpmScraper = require('./scrapers/npm');
const TelegramNotifier = require('./notifiers/telegram');
const DiscordNotifier = require('./notifiers/discord');
const EmailNotifier = require('./notifiers/email');
const Scheduler = require('./scheduler');
const FlowchartGenerator = require('./utils/flowchart');

/**
 * Skill Discovery Monitor Application
 */
class SkillDiscoveryMonitor {
  constructor() {
    this.app = express();
    this.port = process.env.PORT || 3000;

    // Initialize payment system
    this.payment = new SkillPayment(process.env.SKILLPAY_API_KEY);

    // Initialize scrapers
    this.clawhubScraper = new ClawhubScraper(process.env.CLAWHUB_TOKEN);
    this.githubScraper = new GitHubScraper(process.env.GITHUB_TOKEN);
    this.npmScraper = new NpmScraper();

    // Initialize notifiers
    this.telegramNotifier = new TelegramNotifier(process.env.TELEGRAM_BOT_TOKEN);
    this.discordNotifier = new DiscordNotifier(process.env.DISCORD_WEBHOOK_URL);
    this.emailNotifier = new EmailNotifier({
      host: process.env.EMAIL_HOST,
      port: process.env.EMAIL_PORT,
      user: process.env.EMAIL_USER,
      pass: process.env.EMAIL_PASS
    });

    // Initialize scheduler
    this.scheduler = new Scheduler();

    // Subscription storage
    this.subscriptions = new Map();

    this.setupMiddleware();
    this.setupRoutes();
    this.setupScheduledTasks();
  }

  /**
   * Setup Express middleware
   */
  setupMiddleware() {
    this.app.use(express.json());
    this.app.use(express.urlencoded({ extended: true }));

    // CORS
    this.app.use((req, res, next) => {
      res.header('Access-Control-Allow-Origin', '*');
      res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept, Authorization');
      next();
    });

    // Logging
    this.app.use((req, res, next) => {
      console.log(`[${new Date().toISOString()}] ${req.method} ${req.path}`);
      next();
    });
  }

  /**
   * Setup API routes
   */
  setupRoutes() {
    // Health check
    this.app.get('/health', (req, res) => {
      res.json({ status: 'ok', timestamp: new Date().toISOString() });
    });

    // Discover skills from all platforms
    this.app.get('/discover', async (req, res) => {
      try {
        const { category = null, limit = 10 } = req.query;
        const skills = await this.discoverSkills(category, parseInt(limit));

        res.json({
          success: true,
          data: skills,
          count: skills.length,
          platforms: ['clawhub', 'github', 'npm']
        });
      } catch (error) {
        console.error('Discover endpoint error:', error);
        res.status(500).json({ error: error.message });
      }
    });

    // Get skills from specific platform
    this.app.get('/platform/:platform', async (req, res) => {
      try {
        const { platform } = req.params;
        const { limit = 10 } = req.query;

        let skills = [];
        switch (platform.toLowerCase()) {
          case 'clawhub':
            skills = await this.clawhubScraper.getTrendingSkills(parseInt(limit));
            break;
          case 'github':
            skills = await this.githubScraper.getPopularActions(parseInt(limit));
            break;
          case 'npm':
            skills = await this.npmScraper.getPopularCLITools(parseInt(limit));
            break;
          default:
            return res.status(400).json({ error: 'Invalid platform' });
        }

        // Add flowcharts
        skills = skills.map(skill => ({
          ...skill,
          usageFlow: FlowchartGenerator.generateUsageFlow(skill)
        }));

        res.json({
          success: true,
          platform,
          data: skills,
          count: skills.length
        });
      } catch (error) {
        console.error('Platform endpoint error:', error);
        res.status(500).json({ error: error.message });
      }
    });

    // Trigger notification
    this.app.post('/notify', async (req, res) => {
      try {
        const { userId, transactionId, channels, category = null, limit = 5 } = req.body;

        // Verify payment
        const paymentVerified = await this.payment.verifyPayment(userId, transactionId);
        if (!paymentVerified) {
          return res.status(402).json({ error: 'Payment required or verification failed' });
        }

        // Discover skills
        const skills = await this.discoverSkills(category, parseInt(limit));

        // Send notifications
        const results = await this.sendNotifications(skills, channels);

        // Log usage
        await this.payment.logUsage(userId, 'notify');

        res.json({
          success: true,
          data: {
            skillCount: skills.length,
            notifications: results
          }
        });
      } catch (error) {
        console.error('Notify endpoint error:', error);
        res.status(500).json({ error: error.message });
      }
    });

    // Subscribe
    this.app.post('/subscribe', async (req, res) => {
      try {
        const { userId, channels, preferences = {} } = req.body;

        if (!userId || !channels) {
          return res.status(400).json({ error: 'Missing required fields' });
        }

        // Create payment request
        const paymentRequest = await this.payment.createPaymentRequest(userId);

        // Save subscription
        this.subscriptions.set(userId, {
          channels,
          preferences: {
            categories: preferences.categories || ['all'],
            platforms: preferences.platforms || ['clawhub', 'github', 'npm'],
            limit: preferences.limit || 5,
            schedule: preferences.schedule || process.env.SCHEDULE || '0 10 * * *'
          },
          status: 'pending',
          paymentId: paymentRequest.paymentId,
          createdAt: new Date().toISOString()
        });

        res.json({
          success: true,
          message: 'Subscription created, please complete payment',
          payment: paymentRequest
        });
      } catch (error) {
        console.error('Subscribe endpoint error:', error);
        res.status(500).json({ error: error.message });
      }
    });

    // Unsubscribe
    this.app.post('/unsubscribe', async (req, res) => {
      try {
        const { userId } = req.body;
        if (!userId) {
          return res.status(400).json({ error: 'Missing userId' });
        }

        this.subscriptions.delete(userId);
        res.json({ success: true, message: 'Subscription cancelled' });
      } catch (error) {
        console.error('Unsubscribe endpoint error:', error);
        res.status(500).json({ error: error.message });
      }
    });

    // Get subscription status
    this.app.get('/subscription/:userId', (req, res) => {
      const { userId } = req.params;
      const subscription = this.subscriptions.get(userId);

      if (!subscription) {
        return res.status(404).json({ error: 'Subscription not found' });
      }

      res.json({ success: true, subscription });
    });

    // Payment callback
    this.app.post('/payment/callback', async (req, res) => {
      try {
        const { userId, paymentId, status } = req.body;

        if (status === 'completed') {
          const subscription = this.subscriptions.get(userId);
          if (subscription && subscription.paymentId === paymentId) {
            subscription.status = 'active';
            this.subscriptions.set(userId, subscription);
          }
        }

        res.json({ success: true });
      } catch (error) {
        console.error('Payment callback error:', error);
        res.status(500).json({ error: error.message });
      }
    });
  }

  /**
   * Discover skills from all platforms
   */
  async discoverSkills(category = null, limit = 10) {
    const perPlatform = Math.ceil(limit / 3);

    const [clawhubSkills, githubSkills, npmSkills] = await Promise.all([
      this.clawhubScraper.getTrendingSkills(perPlatform, category),
      this.githubScraper.getPopularActions(perPlatform),
      this.npmScraper.getPopularCLITools(perPlatform)
    ]);

    let allSkills = [...clawhubSkills, ...githubSkills, ...npmSkills];

    // Filter by category if specified
    if (category && category !== 'all') {
      allSkills = allSkills.filter(s => s.category === category);
    }

    // Add flowcharts
    allSkills = allSkills.map(skill => ({
      ...skill,
      usageFlow: FlowchartGenerator.generateUsageFlow(skill),
      usageFlowASCII: FlowchartGenerator.toASCII(FlowchartGenerator.generateUsageFlow(skill))
    }));

    // Sort by popularity
    allSkills.sort((a, b) => (b.stars + b.downloads) - (a.stars + a.downloads));

    return allSkills.slice(0, limit);
  }

  /**
   * Send notifications
   */
  async sendNotifications(skills, channels = {}) {
    const results = {};

    const message = this.formatSkillsMessage(skills);

    // Telegram
    if (channels.telegram && channels.telegram.chatId) {
      results.telegram = await this.telegramNotifier.sendTrendingReport(
        channels.telegram.chatId,
        skills,
        { title: 'Skill Discovery Report' }
      );
    }

    // Discord
    if (channels.discord) {
      results.discord = await this.discordNotifier.sendTrendingReport(skills, {
        title: 'Skill Discovery Report'
      });
    }

    // Email
    if (channels.email && channels.email.to) {
      results.email = await this.emailNotifier.sendTrendingReport(
        channels.email.to,
        skills,
        { title: 'Skill Discovery Report' }
      );
    }

    return results;
  }

  /**
   * Format skills message
   */
  formatSkillsMessage(skills) {
    let message = '🔍 **Skill Discovery Report**\n\n';

    skills.forEach((skill, index) => {
      message += `${index + 1}. **${skill.name}** (${skill.platform})\n`;
      message += `   ${skill.description}\n`;
      message += `   ⭐ ${skill.stars} | 📥 ${skill.downloads}\n`;
      message += `   🔗 ${skill.url}\n\n`;
    });

    return message;
  }

  /**
   * Setup scheduled tasks
   */
  setupScheduledTasks() {
    const schedule = process.env.SCHEDULE || '0 10 * * *';

    this.scheduler.addTask(
      schedule,
      async () => {
        await this.runScheduledReport();
      },
      'Daily Skill Discovery Report'
    );

    this.scheduler.startAll();
  }

  /**
   * Run scheduled report
   */
  async runScheduledReport() {
    console.log('Running scheduled skill discovery report...');

    try {
      for (const [userId, subscription] of this.subscriptions.entries()) {
        if (subscription.status === 'active') {
          const { categories, limit } = subscription.preferences;
          const category = categories[0] || null;

          const skills = await this.discoverSkills(category, limit);
          await this.sendNotifications(skills, subscription.channels);
          await this.payment.logUsage(userId, 'scheduled_report');
        }
      }

      console.log('Scheduled report completed');
    } catch (error) {
      console.error('Scheduled report failed:', error);
    }
  }

  /**
   * Start the server
   */
  start() {
    this.app.listen(this.port, () => {
      console.log(`\n🔍 Skill Discovery Monitor started`);
      console.log(`📡 Server running on port ${this.port}`);
      console.log(`💰 SkillPay integration: ${this.payment.apiKey ? 'Enabled' : 'Disabled'}`);
      console.log(`📅 Scheduled tasks: ${this.scheduler.getTasks().length}`);
      console.log(`\nEndpoints:`);
      console.log(`  GET  /discover - Discover skills from all platforms`);
      console.log(`  GET  /platform/:platform - Get skills from specific platform`);
      console.log(`  POST /notify - Trigger notification`);
      console.log(`  POST /subscribe - Subscribe to daily reports`);
      console.log(`  POST /unsubscribe - Unsubscribe`);
      console.log(`  GET  /health - Health check`);
      console.log(`\n`);
    });

    // Launch Telegram bot
    if (process.env.TELEGRAM_BOT_TOKEN) {
      this.telegramNotifier.launch();
    }

    // Graceful shutdown
    process.on('SIGINT', () => {
      console.log('\nShutting down gracefully...');
      this.scheduler.stopAll();
      process.exit(0);
    });
  }
}

// Start application
if (require.main === module) {
  const monitor = new SkillDiscoveryMonitor();
  monitor.start();
}

module.exports = SkillDiscoveryMonitor;
