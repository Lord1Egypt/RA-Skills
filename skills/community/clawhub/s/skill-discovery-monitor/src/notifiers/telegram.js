const { Telegraf } = require('telegraf');

/**
 * Telegram Notifier
 */
class TelegramNotifier {
  constructor(botToken) {
    this.botToken = botToken;
    this.bot = botToken ? new Telegraf(botToken) : null;
  }

  /**
   * Send trending report to Telegram
   * @param {string} chatId - Chat ID
   * @param {Array} repos - Trending repositories
   * @param {object} options - Additional options
   */
  async sendTrendingReport(chatId, repos, options = {}) {
    if (!this.bot) {
      console.warn('Telegram bot not configured');
      return false;
    }

    const message = this.formatMessage(repos, options);

    try {
      await this.bot.telegram.sendMessage(chatId, message, {
        parse_mode: 'Markdown',
        disable_web_page_preview: true
      });
      return true;
    } catch (error) {
      console.error('Telegram send failed:', error.message);
      return false;
    }
  }

  /**
   * Format trending repositories as Markdown message
   */
  formatMessage(repos, options = {}) {
    const { language = 'All', since = 'daily' } = options;
    const timeLabel = { daily: 'Today', weekly: 'This Week', monthly: 'This Month' }[since] || 'Today';

    let message = `🔥 *GitHub Trending - ${timeLabel}*\n`;
    if (language && language !== 'all') {
      message += `📚 Language: *${language}*\n`;
    }
    message += `📅 ${new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })}\n\n`;

    if (!repos || repos.length === 0) {
      message += '❌ No trending repositories found.\n';
      return message;
    }

    repos.slice(0, 10).forEach((repo, index) => {
      message += `*${index + 1}. ${repo.fullName}*\n`;
      message += `   ⭐ ${repo.stars.toLocaleString()} stars`;
      if (repo.todayStars > 0) {
        message += ` (+${repo.todayStars} today)`;
      }
      message += `\n`;
      message += `   🍴 ${repo.forks.toLocaleString()} forks\n`;
      if (repo.language) {
        message += `   💻 ${repo.language}\n`;
      }
      if (repo.description) {
        const desc = repo.description.length > 100
          ? repo.description.substring(0, 100) + '...'
          : repo.description;
        message += `   📝 ${desc}\n`;
      }
      message += `   🔗 [View on GitHub](${repo.url})\n\n`;
    });

    message += '---\n';
    message += '💡 *Powered by GitHub Trending Monitor*\n';
    message += '⚡ Subscribe for daily updates!';

    return message;
  }

  /**
   * Launch bot to listen for commands
   */
  launch() {
    if (!this.bot) {
      console.warn('Telegram bot not configured');
      return;
    }

    this.bot.start((ctx) => {
      ctx.reply(
        'Welcome to GitHub Trending Monitor! 🚀\n\n' +
        'Use /subscribe to receive daily trending updates.\n' +
        'Use /trending to get current trending repos.'
      );
    });

    this.bot.command('subscribe', (ctx) => {
      ctx.reply('✅ Subscribed! You will receive daily GitHub trending updates.');
    });

    this.bot.command('unsubscribe', (ctx) => {
      ctx.reply('❌ Unsubscribed from daily updates.');
    });

    this.bot.command('trending', (ctx) => {
      ctx.reply('Fetching trending repositories... Please wait.');
    });

    this.bot.launch();
    console.log('Telegram bot started');
  }
}

module.exports = TelegramNotifier;
