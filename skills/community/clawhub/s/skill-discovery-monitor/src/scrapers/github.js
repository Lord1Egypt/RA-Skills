const axios = require('axios');

/**
 * GitHub Actions Scraper
 *
 * Fetches popular GitHub Actions and automation workflows
 */
class GitHubScraper {
  constructor(token = null) {
    this.token = token;
    this.baseURL = 'https://api.github.com';
  }

  /**
   * Get popular GitHub Actions
   * @param {number} limit - Number of actions to fetch
   * @returns {Promise<Array>}
   */
  async getPopularActions(limit = 10) {
    try {
      const headers = { 'Accept': 'application/vnd.github.v3+json' };
      if (this.token) {
        headers['Authorization'] = `token ${this.token}`;
      }

      // Search for popular GitHub Actions
      const response = await axios.get(`${this.baseURL}/search/repositories`, {
        params: {
          q: 'topic:github-actions stars:>100',
          sort: 'stars',
          order: 'desc',
          per_page: limit
        },
        headers,
        timeout: 10000
      });

      return response.data.items.map(repo => this.formatAction(repo));
    } catch (error) {
      console.error('GitHub Actions scraping failed:', error.message);
      return this.getMockActions(limit);
    }
  }

  /**
   * Get automation workflows
   */
  async getAutomationWorkflows(limit = 10) {
    try {
      const headers = { 'Accept': 'application/vnd.github.v3+json' };
      if (this.token) {
        headers['Authorization'] = `token ${this.token}`;
      }

      const response = await axios.get(`${this.baseURL}/search/repositories`, {
        params: {
          q: 'topic:automation topic:workflow stars:>50',
          sort: 'stars',
          order: 'desc',
          per_page: limit
        },
        headers,
        timeout: 10000
      });

      return response.data.items.map(repo => this.formatAction(repo));
    } catch (error) {
      console.error('GitHub workflows scraping failed:', error.message);
      return [];
    }
  }

  /**
   * Format GitHub Action data
   */
  formatAction(repo) {
    return {
      name: repo.name,
      platform: 'github',
      category: this.detectCategory(repo),
      description: repo.description || 'No description available',
      author: repo.owner.login,
      stars: repo.stargazers_count,
      downloads: repo.watchers_count, // Use watchers as proxy for usage
      version: 'latest',
      tags: repo.topics || [],
      features: this.extractFeatures(repo),
      url: repo.html_url,
      createdAt: repo.created_at,
      updatedAt: repo.updated_at
    };
  }

  /**
   * Detect category from topics and description
   */
  detectCategory(repo) {
    const topics = (repo.topics || []).join(' ').toLowerCase();
    const desc = (repo.description || '').toLowerCase();
    const combined = `${topics} ${desc}`;

    if (combined.includes('ai') || combined.includes('ml') || combined.includes('machine-learning')) {
      return 'ai';
    } else if (combined.includes('automation') || combined.includes('workflow')) {
      return 'automation';
    } else if (combined.includes('deploy') || combined.includes('ci') || combined.includes('cd')) {
      return 'devops';
    } else if (combined.includes('test')) {
      return 'testing';
    } else {
      return 'developer-tools';
    }
  }

  /**
   * Extract features from README or description
   */
  extractFeatures(repo) {
    const features = [];
    const desc = repo.description || '';

    // Extract key phrases
    if (desc.includes('automat')) features.push('Automated workflows');
    if (desc.includes('deploy')) features.push('Deployment automation');
    if (desc.includes('test')) features.push('Testing integration');
    if (desc.includes('notif')) features.push('Notifications');
    if (desc.includes('CI') || desc.includes('CD')) features.push('CI/CD pipeline');

    // Add topics as features
    if (repo.topics && repo.topics.length > 0) {
      features.push(...repo.topics.slice(0, 3).map(t => t.replace(/-/g, ' ')));
    }

    return features.slice(0, 5);
  }

  /**
   * Mock actions for fallback
   */
  getMockActions(limit) {
    const mockActions = [
      {
        name: 'setup-node',
        owner: { login: 'actions' },
        description: 'Set up Node.js environment for GitHub Actions',
        stargazers_count: 3500,
        watchers_count: 3500,
        topics: ['github-actions', 'nodejs', 'setup'],
        html_url: 'https://github.com/actions/setup-node',
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      },
      {
        name: 'checkout',
        owner: { login: 'actions' },
        description: 'Checkout repository code in GitHub Actions',
        stargazers_count: 4200,
        watchers_count: 4200,
        topics: ['github-actions', 'checkout', 'git'],
        html_url: 'https://github.com/actions/checkout',
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      }
    ];

    return mockActions.slice(0, limit).map(action => this.formatAction(action));
  }
}

module.exports = GitHubScraper;
