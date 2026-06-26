/**
 * Rating System - User ratings, statistics, and leaderboards
 */

const fs = require('fs');
const path = require('path');

class RatingSystem {
  constructor(options = {}) {
    this.dataDir = options.dataDir || './.marketplace-cache';
    this.ratingsPath = path.join(this.dataDir, 'ratings.json');
    this.statsPath = path.join(this.dataDir, 'stats.json');
    
    this._ensureDataDir();
    this._loadData();
  }

  _ensureDataDir() {
    if (!fs.existsSync(this.dataDir)) {
      fs.mkdirSync(this.dataDir, { recursive: true });
    }
  }

  _loadData() {
    // Load ratings
    if (fs.existsSync(this.ratingsPath)) {
      try {
        const data = fs.readFileSync(this.ratingsPath, 'utf8');
        this.ratings = JSON.parse(data);
      } catch (err) {
        this.ratings = {};
      }
    } else {
      this.ratings = {};
    }

    // Load stats
    if (fs.existsSync(this.statsPath)) {
      try {
        const data = fs.readFileSync(this.statsPath, 'utf8');
        this.stats = JSON.parse(data);
      } catch (err) {
        this._initStats();
      }
    } else {
      this._initStats();
    }
  }

  _initStats() {
    this.stats = {
      skills: {},
      global: {
        totalRatings: 0,
        totalReviews: 0,
        averageRating: 0,
        lastUpdated: Date.now()
      }
    };
  }

  _saveData() {
    fs.writeFileSync(this.ratingsPath, JSON.stringify(this.ratings, null, 2));
    fs.writeFileSync(this.statsPath, JSON.stringify(this.stats, null, 2));
  }

  // Rating submission
  submitRating(skillName, userId, ratingData) {
    const { rating, comment = '', version = null } = ratingData;

    // Validate rating
    if (typeof rating !== 'number' || rating < 1 || rating > 5) {
      throw new Error('Rating must be a number between 1 and 5');
    }

    // Initialize skill ratings
    if (!this.ratings[skillName]) {
      this.ratings[skillName] = {
        ratings: [],
        reviews: []
      };
    }

    const skillRatings = this.ratings[skillName];

    // Check for existing rating from this user
    const existingIndex = skillRatings.ratings.findIndex(r => r.userId === userId);
    const isUpdate = existingIndex >= 0;

    const ratingRecord = {
      userId,
      rating,
      version,
      timestamp: Date.now()
    };

    if (isUpdate) {
      skillRatings.ratings[existingIndex] = ratingRecord;
    } else {
      skillRatings.ratings.push(ratingRecord);
    }

    // Add review if provided
    if (comment && comment.trim()) {
      skillRatings.reviews.push({
        userId,
        comment: comment.trim(),
        rating,
        version,
        timestamp: Date.now(),
        helpful: 0
      });
    }

    // Update statistics
    this._updateSkillStats(skillName);
    this._updateGlobalStats();
    this._saveData();

    return {
      success: true,
      updated: isUpdate,
      skillName,
      rating,
      averageRating: this.stats.skills[skillName]?.averageRating || rating
    };
  }

  // Get ratings for a skill
  getRatings(skillName, options = {}) {
    const { includeReviews = true, limit = 10, offset = 0 } = options;
    
    const skillData = this.ratings[skillName];
    if (!skillData) {
      return {
        skillName,
        totalRatings: 0,
        averageRating: 0,
        distribution: { 1: 0, 2: 0, 3: 0, 4: 0, 5: 0 },
        reviews: []
      };
    }

    const stats = this.stats.skills[skillName] || {};
    
    const result = {
      skillName,
      totalRatings: stats.totalRatings || 0,
      averageRating: stats.averageRating || 0,
      distribution: stats.distribution || { 1: 0, 2: 0, 3: 0, 4: 0, 5: 0 }
    };

    if (includeReviews) {
      const reviews = skillData.reviews
        .sort((a, b) => b.timestamp - a.timestamp)
        .slice(offset, offset + limit);
      
      result.reviews = reviews;
      result.totalReviews = skillData.reviews.length;
    }

    return result;
  }

  // Update skill statistics
  _updateSkillStats(skillName) {
    const skillData = this.ratings[skillName];
    if (!skillData) return;

    const ratings = skillData.ratings.map(r => r.rating);
    const total = ratings.length;
    const sum = ratings.reduce((a, b) => a + b, 0);
    const average = total > 0 ? sum / total : 0;

    const distribution = { 1: 0, 2: 0, 3: 0, 4: 0, 5: 0 };
    ratings.forEach(r => distribution[r]++);

    this.stats.skills[skillName] = {
      totalRatings: total,
      averageRating: Math.round(average * 100) / 100,
      distribution,
      lastUpdated: Date.now()
    };
  }

  // Update global statistics
  _updateGlobalStats() {
    const allRatings = Object.values(this.stats.skills);
    const total = allRatings.reduce((sum, s) => sum + s.totalRatings, 0);
    const sum = allRatings.reduce((sum, s) => sum + (s.averageRating * s.totalRatings), 0);
    
    this.stats.global = {
      totalRatings: total,
      totalReviews: Object.values(this.ratings).reduce((sum, r) => sum + r.reviews.length, 0),
      averageRating: total > 0 ? Math.round((sum / total) * 100) / 100 : 0,
      lastUpdated: Date.now()
    };
  }

  // Get leaderboard
  getLeaderboard(options = {}) {
    const { category = null, limit = 10, sortBy = 'rating' } = options;
    
    let skills = Object.entries(this.stats.skills).map(([name, stats]) => ({
      name,
      ...stats
    }));

    // Filter by minimum ratings threshold
    skills = skills.filter(s => s.totalRatings >= 1);

    // Sort
    if (sortBy === 'rating') {
      skills.sort((a, b) => {
        if (b.averageRating !== a.averageRating) {
          return b.averageRating - a.averageRating;
        }
        return b.totalRatings - a.totalRatings;
      });
    } else if (sortBy === 'downloads') {
      skills.sort((a, b) => (b.downloads || 0) - (a.downloads || 0));
    } else if (sortBy === 'reviews') {
      skills.sort((a, b) => (b.totalReviews || 0) - (a.totalReviews || 0));
    }

    return {
      skills: skills.slice(0, limit),
      total: skills.length,
      sortBy
    };
  }

  // Get top rated skills
  getTopRated(limit = 10, minRatings = 5) {
    return this.getLeaderboard({ limit, sortBy: 'rating' }).skills
      .filter(s => s.totalRatings >= minRatings);
  }

  // Get trending skills (recent activity)
  getTrending(limit = 10, days = 7) {
    const cutoff = Date.now() - (days * 24 * 60 * 60 * 1000);
    
    const skills = Object.entries(this.ratings)
      .map(([name, data]) => {
        const recentRatings = data.ratings.filter(r => r.timestamp > cutoff);
        const recentReviews = data.reviews.filter(r => r.timestamp > cutoff);
        
        return {
          name,
          recentActivity: recentRatings.length + recentReviews.length,
          recentRatings: recentRatings.length,
          recentReviews: recentReviews.length,
          ...this.stats.skills[name]
        };
      })
      .filter(s => s.recentActivity > 0)
      .sort((a, b) => b.recentActivity - a.recentActivity)
      .slice(0, limit);

    return skills;
  }

  // Mark review as helpful
  markHelpful(skillName, reviewIndex, userId) {
    const skillData = this.ratings[skillName];
    if (!skillData || !skillData.reviews[reviewIndex]) {
      throw new Error('Review not found');
    }

    const review = skillData.reviews[reviewIndex];
    
    // Initialize helpful voters
    if (!review.helpfulVoters) {
      review.helpfulVoters = [];
    }

    // Toggle helpful status
    const voterIndex = review.helpfulVoters.indexOf(userId);
    if (voterIndex >= 0) {
      review.helpfulVoters.splice(voterIndex, 1);
      review.helpful--;
    } else {
      review.helpfulVoters.push(userId);
      review.helpful++;
    }

    this._saveData();
    
    return {
      success: true,
      helpful: review.helpful,
      voted: voterIndex < 0
    };
  }

  // Get user's rating for a skill
  getUserRating(skillName, userId) {
    const skillData = this.ratings[skillName];
    if (!skillData) return null;

    const rating = skillData.ratings.find(r => r.userId === userId);
    const review = skillData.reviews.find(r => r.userId === userId);

    return rating ? {
      rating: rating.rating,
      comment: review?.comment || null,
      timestamp: rating.timestamp,
      version: rating.version
    } : null;
  }

  // Delete user's rating
  deleteRating(skillName, userId) {
    const skillData = this.ratings[skillName];
    if (!skillData) {
      throw new Error('Skill has no ratings');
    }

    skillData.ratings = skillData.ratings.filter(r => r.userId !== userId);
    skillData.reviews = skillData.reviews.filter(r => r.userId !== userId);

    this._updateSkillStats(skillName);
    this._updateGlobalStats();
    this._saveData();

    return { success: true };
  }

  // Get quality metrics
  getQualityMetrics(skillName) {
    const stats = this.stats.skills[skillName];
    if (!stats) {
      return null;
    }

    const distribution = stats.distribution;
    const total = stats.totalRatings;

    // Calculate quality score (weighted average with confidence)
    const confidence = Math.min(total / 10, 1); // Max confidence at 10 ratings
    const qualityScore = stats.averageRating * confidence;

    // Calculate rating distribution quality
    const positiveRatio = ((distribution[4] + distribution[5]) / total) * 100;
    const negativeRatio = ((distribution[1] + distribution[2]) / total) * 100;

    return {
      skillName,
      qualityScore: Math.round(qualityScore * 100) / 100,
      confidence: Math.round(confidence * 100) / 100,
      averageRating: stats.averageRating,
      totalRatings: total,
      positiveRatio: Math.round(positiveRatio * 100) / 100,
      negativeRatio: Math.round(negativeRatio * 100) / 100,
      distribution
    };
  }

  // Get global stats
  getGlobalStats() {
    return { ...this.stats.global };
  }
}

module.exports = { RatingSystem };
