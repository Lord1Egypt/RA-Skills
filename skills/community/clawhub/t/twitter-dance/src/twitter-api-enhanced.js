/**
 * Twitter Dance - 增强 API 客户端
 * 
 * 基于 TwitterDanceAPIClient 的扩展功能
 * 包括：通知、账户统计、自动回复、互动管理等
 */

const TwitterDanceAPIClient = require('./twitter-api-client');

class TwitterDanceEnhanced extends TwitterDanceAPIClient {
  /**
   * 获取账户统计概览（粉丝、推文、点赞等）
   */
  async getAccountStats() {
    if (!this.authToken) {
      throw new Error('需要 TWITTER_AUTH_TOKEN');
    }

    console.log('[📊] 获取账户统计...');

    try {
      const info = await this.getMyInfo();
      
      if (info.success) {
        const stats = {
          success: true,
          account: {
            name: info.user.name,
            handle: info.user.screen_name,
            bio: info.user.description,
            location: info.user.location,
            verified: info.user.id_str ? true : false
          },
          stats: {
            followers: info.user.followers_count || 0,
            following: info.user.friends_count || 0,
            tweets: info.user.statuses_count || 0,
            likes: info.user.favourites_count || 0,
            mediaCount: info.user.media_count || 0,
            listedCount: info.user.listed_count || 0
          },
          profile: {
            profileImage: info.user.profile_image_url || '',
            createdAt: info.user.created_at || '',
            isProtected: info.user.protected || false
          }
        };

        console.log('[✅] 统计获取成功');
        return stats;
      }

      throw new Error('获取账户信息失败');
    } catch (err) {
      console.error(`[❌] 统计获取失败: ${err.message}`);
      throw err;
    }
  }

  /**
   * 获取最新通知（mentions、likes、retweets、follows）
   * 
   * 支持两种方式：
   * 1. Twitter API v2 的 Notifications 端点（需要专业 API Key）
   * 2. 基于 home timeline 的模拟通知
   */
  async getNotifications(options = {}) {
    if (!this.authToken) {
      throw new Error('需要 TWITTER_AUTH_TOKEN');
    }

    console.log('[🔔] 获取通知...');

    try {
      // 使用 v2Request（正确的小写 header 格式）获取通知
      console.log('[🔍] 获取 Twitter API v2 通知...');

      const response = await this.v2Request('/2/notifications/all.json');

      if (response.code === 401) {
        throw new Error('需要升级 API Key - 联系 @shingle (https://t.me/shingle)');
      }

      // 处理 globalObjects 格式
      let notificationsData = [];

      if (response.globalObjects?.notifications) {
        notificationsData = Object.values(response.globalObjects.notifications);
      } else if (Array.isArray(response.data)) {
        notificationsData = response.data;
      } else if (Array.isArray(response)) {
        notificationsData = response;
      }

      if (notificationsData.length > 0) {
        const summary = {
          total: notificationsData.length,
          mentions: 0,
          likes: 0,
          retweets: 0,
          follows: 0,
          quotes: 0,
          replies: 0,
          other: 0
        };

        const notifications = [];

        notificationsData.forEach(notif => {
          const type = typeof notif.type === 'string' ? notif.type.toLowerCase() : '';
          const template = typeof notif.template === 'string' ? notif.template.toLowerCase() : '';
          const templateStr = JSON.stringify(notif.template || '').toLowerCase();
          const message = notif.message?.text || '';
          const combined = (type + templateStr + message).toLowerCase();

          if (combined.includes('mention')) summary.mentions++;
          else if (combined.includes('like') || combined.includes('favorite') || combined.includes('liked')) summary.likes++;
          else if (combined.includes('retweet') || combined.includes('retweeted')) summary.retweets++;
          else if (combined.includes('follow')) summary.follows++;
          else if (combined.includes('quote') || combined.includes('quoted')) summary.quotes++;
          else if (combined.includes('reply') || combined.includes('replied')) summary.replies++;
          else summary.other++;

          notifications.push({
            type: type || 'interaction',
            text: message,
            handle: '',
            likes: 0,
            retweets: 0,
            timestamp: notif.timestampMs ? new Date(parseInt(notif.timestampMs)).toISOString() : '',
            tweetId: ''
          });
        });

        console.log(`[✅] 获取到 ${notificationsData.length} 条通知`);

        return {
          success: true,
          source: 'v2-notifications',
          notifications,
          summary,
          pagination_token: null,
          timestamp: new Date().toISOString()
        };
      }

      throw new Error('获取通知失败：无数据');
    } catch (err) {
      console.error(`[❌] 通知获取失败: ${err.message}`);
      throw err;
    }
  }

  /**
   * 获取完整通知（Twitter API v2）
   * 
   * 使用 /2/notifications/all.json 端点
   * 注：需要使用小写的 authtoken 和 apikey 头
   */
  async getNotificationsV2() {
    if (!this.authToken) {
      throw new Error('需要 TWITTER_AUTH_TOKEN');
    }

    console.log('[🔔] 获取完整通知（API v2）...');

    try {
      // 使用专门的 v2Request 方法，它使用正确的头格式
      const response = await this.v2Request('/2/notifications/all.json');

      if (response.code === 401) {
        throw new Error('需要升级 API Key - 联系 @shingle (https://t.me/shingle)');
      }

      // 处理 globalObjects 格式响应
      let notificationsData = [];
      
      if (response.globalObjects?.notifications) {
        // Twitter API v2 格式
        const notificationsObj = response.globalObjects.notifications;
        notificationsData = Object.values(notificationsObj);
      } else if (Array.isArray(response.data)) {
        // 标准 data 数组格式
        notificationsData = response.data;
      } else if (Array.isArray(response)) {
        // 直接数组格式
        notificationsData = response;
      } else {
        throw new Error('通知数据格式未知');
      }

      const notifications = {
        success: true,
        source: 'v2-notifications',
        notifications: notificationsData,
        summary: {
          total: notificationsData.length,
          mentions: 0,
          likes: 0,
          retweets: 0,
          follows: 0,
          quotes: 0,
          replies: 0,
          other: 0
        },
        timestamp: new Date().toISOString()
      };

      // 分类统计
      notificationsData.forEach(notif => {
        // 尝试从不同字段获取类型信息
        const type = typeof notif.type === 'string' ? notif.type.toLowerCase() : '';
        const template = typeof notif.template === 'string' ? notif.template.toLowerCase() : '';
        const message = notif.message?.text || '';
        const combined = (type + template + message).toLowerCase();
        
        if (combined.includes('mention')) notifications.summary.mentions++;
        else if (combined.includes('like') || combined.includes('favorite') || combined.includes('liked')) notifications.summary.likes++;
        else if (combined.includes('retweet') || combined.includes('retweeted')) notifications.summary.retweets++;
        else if (combined.includes('follow')) notifications.summary.follows++;
        else if (combined.includes('quote') || combined.includes('quoted')) notifications.summary.quotes++;
        else if (combined.includes('reply') || combined.includes('replied')) notifications.summary.replies++;
        else notifications.summary.other++;
      });

      console.log('[✅] 完整通知获取成功');
      return notifications;
    } catch (err) {
      console.error(`[❌] 通知获取失败: ${err.message}`);
      throw err;
    }
  }

  /**
   * 自动回复（增强版）
   * 
   * 支持：
   * - 简单文本回复
   * - 带 mention 的智能回复
   * - 回复链
   */
  async autoReply(tweetId, replyText, options = {}) {
    if (!this.authToken) {
      throw new Error('需要 TWITTER_AUTH_TOKEN');
    }

    if (!tweetId) {
      throw new Error('需要推文 ID');
    }

    if (!replyText || replyText.trim().length === 0) {
      throw new Error('回复内容不能为空');
    }

    console.log(`[💬] 自动回复推文: ${tweetId}`);
    console.log(`     内容: ${replyText.substring(0, 60)}...`);

    try {
      // 获取原始推文信息（如果需要）
      if (options.prependMention) {
        // 这里可以添加自动 @ 提及的逻辑
      }

      // 构建回复
      const result = await this.replyTweet(tweetId, replyText);

      if (result.success) {
        console.log(`[✅] 回复成功: ${result.tweetId}`);
        return {
          success: true,
          replyId: result.tweetId,
          originalTweetId: tweetId,
          text: replyText,
          timestamp: new Date().toISOString()
        };
      }

      throw new Error('回复失败');
    } catch (err) {
      console.error(`[❌] 回复失败: ${err.message}`);
      throw err;
    }
  }

  /**
   * 获取推文完整对话线程
   */
  async getConversationThread(tweetId) {
    console.log(`[🧵] 获取对话线程: ${tweetId}`);

    try {
      const tweet = await this.getTweet(tweetId);
      
      if (tweet.success) {
        return {
          success: true,
          rootTweet: tweet.tweet,
          replies: await this.getReplies(tweetId),
          timestamp: new Date().toISOString()
        };
      }

      throw new Error('获取线程失败');
    } catch (err) {
      console.error(`[❌] 线程获取失败: ${err.message}`);
      throw err;
    }
  }

  /**
   * 批量操作推文（比如批量点赞）
   */
  async bulkLikeTweets(tweetIds) {
    if (!Array.isArray(tweetIds) || tweetIds.length === 0) {
      throw new Error('需要提供推文 ID 数组');
    }

    console.log(`[❤️] 批量点赞 ${tweetIds.length} 条推文...`);

    const results = {
      success: true,
      liked: 0,
      failed: 0,
      errors: []
    };

    for (const tweetId of tweetIds) {
      try {
        await this.likeTweet(tweetId);
        results.liked++;
        
        // 避免速率限制
        await new Promise(r => setTimeout(r, 500));
      } catch (err) {
        results.failed++;
        results.errors.push({
          tweetId,
          error: err.message
        });
      }
    }

    console.log(`[✅] 完成: ${results.liked} 成功，${results.failed} 失败`);
    return results;
  }

  /**
   * 批量转发推文
   */
  async bulkRetweet(tweetIds) {
    if (!Array.isArray(tweetIds) || tweetIds.length === 0) {
      throw new Error('需要提供推文 ID 数组');
    }

    console.log(`[🔄] 批量转发 ${tweetIds.length} 条推文...`);

    const results = {
      success: true,
      retweeted: 0,
      failed: 0,
      errors: []
    };

    for (const tweetId of tweetIds) {
      try {
        await this.retweet(tweetId);
        results.retweeted++;
        
        // 避免速率限制
        await new Promise(r => setTimeout(r, 500));
      } catch (err) {
        results.failed++;
        results.errors.push({
          tweetId,
          error: err.message
        });
      }
    }

    console.log(`[✅] 完成: ${results.retweeted} 成功，${results.failed} 失败`);
    return results;
  }

  /**
   * 获取推文趋势数据
   */
  async getTweetMetrics(tweetId) {
    console.log(`[📈] 获取推文指标: ${tweetId}`);

    try {
      const tweet = await this.getTweet(tweetId);

      if (tweet.success) {
        // 从 GraphQL 响应中提取指标
        const tweetData = tweet.tweetData || {};
        const metrics = {
          success: true,
          tweetId,
          metrics: {
            likes: tweetData.favorite_count || 0,
            retweets: tweetData.retweet_count || 0,
            replies: tweetData.reply_count || 0,
            quotes: tweetData.quote_count || 0,
            views: parseInt(tweetData.ext_views?.count || '0') || 0
          },
          engagement: {
            totalEngagement: 0,
            engagementRate: 0
          }
        };

        metrics.engagement.totalEngagement =
          metrics.metrics.likes +
          metrics.metrics.retweets +
          metrics.metrics.replies;

        console.log('[✅] 指标获取成功');
        return metrics;
      }

      throw new Error('获取指标失败');
    } catch (err) {
      console.error(`[❌] 指标获取失败: ${err.message}`);
      throw err;
    }
  }

  /**
   * 获取用户时间线分析
   */
  async getTimelineAnalytics(options = {}) {
    if (!this.authToken) {
      throw new Error('需要 TWITTER_AUTH_TOKEN');
    }

    console.log('[📊] 获取时间线分析...');

    try {
      const tweets = await this.getMyTweets({
        count: options.count || 100
      });

      if (tweets.success && tweets.tweets.length > 0) {
        const analytics = {
          success: true,
          totalTweets: tweets.tweets.length,
          totalLikes: 0,
          totalRetweets: 0,
          totalReplies: 0,
          averageLikes: 0,
          averageRetweets: 0,
          topTweet: null,
          tweets: tweets.tweets.map(t => ({
            id: t.id_str,
            text: t.text.substring(0, 100),
            likes: t.favorite_count,
            retweets: t.retweet_count,
            replies: t.reply_count || 0,
            createdAt: t.created_at,
            engagement: (t.favorite_count + t.retweet_count + (t.reply_count || 0))
          }))
        };

        // 计算统计数据
        analytics.tweets.forEach(t => {
          analytics.totalLikes += t.likes;
          analytics.totalRetweets += t.retweets;
          analytics.totalReplies += t.replies;
        });

        analytics.averageLikes = Math.round(analytics.totalLikes / analytics.totalTweets);
        analytics.averageRetweets = Math.round(analytics.totalRetweets / analytics.totalTweets);

        // 找出最受欢迎的推文
        analytics.topTweet = analytics.tweets.reduce((max, t) => 
          t.engagement > max.engagement ? t : max
        );

        console.log('[✅] 分析完成');
        return analytics;
      }

      throw new Error('获取时间线失败');
    } catch (err) {
      console.error(`[❌] 分析失败: ${err.message}`);
      throw err;
    }
  }

  /**
   * 互动周期分析（几点发推最好）
   */
  async getEngagementByHour() {
    if (!this.authToken) {
      throw new Error('需要 TWITTER_AUTH_TOKEN');
    }

    console.log('[⏰] 分析互动周期...');

    try {
      const tweets = await this.getMyTweets({ count: 200 });

      if (tweets.success && tweets.tweets.length > 0) {
        const hourlyStats = {};

        // 初始化 24 小时数据
        for (let i = 0; i < 24; i++) {
          hourlyStats[i] = {
            hour: i,
            tweets: 0,
            totalEngagement: 0,
            avgEngagement: 0
          };
        }

        // 分析每条推文的发布时间和互动
        tweets.tweets.forEach(tweet => {
          const date = new Date(tweet.created_at);
          const hour = date.getUTCHours();
          const engagement = tweet.favorite_count + tweet.retweet_count + (tweet.reply_count || 0);

          hourlyStats[hour].tweets++;
          hourlyStats[hour].totalEngagement += engagement;
        });

        // 计算平均互动
        Object.keys(hourlyStats).forEach(hour => {
          if (hourlyStats[hour].tweets > 0) {
            hourlyStats[hour].avgEngagement = Math.round(
              hourlyStats[hour].totalEngagement / hourlyStats[hour].tweets
            );
          }
        });

        // 找出最佳发推时间
        const bestHour = Object.values(hourlyStats).reduce((max, h) => 
          h.avgEngagement > max.avgEngagement ? h : max
        );

        console.log('[✅] 周期分析完成');
        return {
          success: true,
          hourlyStats: Object.values(hourlyStats),
          bestHour: bestHour.hour,
          bestHourEngagement: bestHour.avgEngagement
        };
      }

      throw new Error('获取推文失败');
    } catch (err) {
      console.error(`[❌] 周期分析失败: ${err.message}`);
      throw err;
    }
  }
}

module.exports = TwitterDanceEnhanced;
