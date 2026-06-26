const axios = require('axios');

/**
 * Clawhub Skills Scraper
 *
 * Fetches popular and trending skills from Clawhub platform
 */
class ClawhubScraper {
  constructor(token = null) {
    this.token = token;
    this.baseURL = 'https://api.clawhub.com';
    this.registryURL = 'https://registry.clawhub.com';
  }

  /**
   * Get trending skills from Clawhub
   * @param {number} limit - Number of skills to fetch
   * @param {string} category - Category filter
   * @returns {Promise<Array>}
   */
  async getTrendingSkills(limit = 10, category = null) {
    try {
      // Use Clawhub CLI-like approach to fetch skills
      const skills = await this.fetchFromRegistry(limit, category);
      return skills.map(skill => this.formatSkill(skill));
    } catch (error) {
      console.error('Clawhub scraping failed:', error.message);
      return [];
    }
  }

  /**
   * Fetch skills from registry
   */
  async fetchFromRegistry(limit, category) {
    try {
      const headers = {};
      if (this.token) {
        headers['Authorization'] = `Bearer ${this.token}`;
      }

      // Simulate registry API call (adjust based on actual API)
      const response = await axios.get(`${this.registryURL}/skills`, {
        params: {
          limit,
          category,
          sort: 'trending'
        },
        headers,
        timeout: 10000
      });

      return response.data.skills || [];
    } catch (error) {
      // Fallback to mock data if API fails
      console.warn('Registry API failed, using fallback data');
      return this.getMockSkills(limit, category);
    }
  }

  /**
   * Format skill data
   */
  formatSkill(skill) {
    return {
      name: skill.name || skill.slug,
      platform: 'clawhub',
      category: skill.category || 'general',
      description: skill.description || skill.summary || 'No description available',
      author: skill.owner || skill.author || 'Unknown',
      stars: skill.stars || 0,
      downloads: skill.downloads || skill.installs || 0,
      version: skill.version || skill.latestVersion || '1.0.0',
      tags: skill.tags || [],
      features: this.extractFeatures(skill),
      url: `https://clawhub.com/skills/${skill.slug || skill.name}`,
      createdAt: skill.createdAt || skill.created,
      updatedAt: skill.updatedAt || skill.updated
    };
  }

  /**
   * Extract key features from skill description
   */
  extractFeatures(skill) {
    const features = [];
    const desc = skill.description || skill.summary || '';

    // Extract bullet points or key phrases
    const lines = desc.split('\n');
    lines.forEach(line => {
      if (line.trim().startsWith('-') || line.trim().startsWith('•')) {
        features.push(line.trim().replace(/^[-•]\s*/, ''));
      }
    });

    // If no bullet points, extract first few sentences
    if (features.length === 0 && desc) {
      const sentences = desc.split('.').filter(s => s.trim());
      features.push(...sentences.slice(0, 3).map(s => s.trim()));
    }

    return features.slice(0, 5); // Max 5 features
  }

  /**
   * Get mock skills for testing/fallback
   */
  getMockSkills(limit, category) {
    const mockSkills = [
      {
        name: 'crypto-funding-monitor',
        slug: 'crypto-funding-monitor',
        category: 'crypto',
        description: 'Monitor crypto funding rounds and TEG projects with multi-channel notifications',
        owner: 'zhdryanchang',
        stars: 15,
        downloads: 120,
        version: '1.0.0',
        tags: ['crypto', 'funding', 'monitoring'],
        createdAt: new Date().toISOString()
      },
      {
        name: 'github-trending-monitor',
        slug: 'github-trending-monitor',
        category: 'developer-tools',
        description: 'Monitor GitHub trending repositories with daily notifications',
        owner: 'zhdryanchang',
        stars: 25,
        downloads: 200,
        version: '1.0.0',
        tags: ['github', 'trending', 'monitoring'],
        createdAt: new Date().toISOString()
      },
      {
        name: 'ai-code-reviewer',
        slug: 'ai-code-reviewer',
        category: 'ai',
        description: 'AI-powered code review and suggestions',
        owner: 'developer',
        stars: 150,
        downloads: 1500,
        version: '2.1.0',
        tags: ['ai', 'code-review', 'automation'],
        createdAt: new Date().toISOString()
      }
    ];

    let filtered = mockSkills;
    if (category) {
      filtered = mockSkills.filter(s => s.category === category);
    }

    return filtered.slice(0, limit);
  }

  /**
   * Search skills by keyword
   */
  async searchSkills(keyword, limit = 10) {
    try {
      const headers = {};
      if (this.token) {
        headers['Authorization'] = `Bearer ${this.token}`;
      }

      const response = await axios.get(`${this.registryURL}/search`, {
        params: { q: keyword, limit },
        headers,
        timeout: 10000
      });

      return (response.data.results || []).map(skill => this.formatSkill(skill));
    } catch (error) {
      console.error('Clawhub search failed:', error.message);
      return [];
    }
  }
}

module.exports = ClawhubScraper;
