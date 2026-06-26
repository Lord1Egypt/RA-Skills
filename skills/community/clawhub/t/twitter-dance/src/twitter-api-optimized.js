/**
 * Twitter Dance API - 优化版本
 * 
 * 所有方法都使用标准化的请求头格式：
 * - authtoken (小写)
 * - apikey (小写)
 * 
 * 兼容所有 apidance.pro 端点
 */

const TwitterDanceAPIClient = require('./twitter-api-client');

class TwitterDanceOptimized extends TwitterDanceAPIClient {
  /**
   * 优化的点赞方法 - 支持 GraphQL
   */
  async likeTweet(tweetId) {
    if (!this.authToken) {
      throw new Error('需要 TWITTER_AUTH_TOKEN');
    }

    console.log(`[❤️] 点赞推文: ${tweetId}`);

    try {
      const response = await this.graphqlRequest('/graphql/FavoriteTweet', {
        tweet_id: tweetId
      });

      if (response && response.data) {
        console.log(`[✅] 点赞成功: ${tweetId}`);
        return { success: true, tweetId, timestamp: new Date().toISOString() };
      }

      throw new Error('点赞失败');
    } catch (err) {
      console.error(`[❌] 点赞失败: ${err.message}`);
      throw err;
    }
  }

  /**
   * 优化的转发方法 - 支持 GraphQL
   */
  async retweet(tweetId) {
    if (!this.authToken) {
      throw new Error('需要 TWITTER_AUTH_TOKEN');
    }

    console.log(`[🔄] 转发推文: ${tweetId}`);

    try {
      const response = await this.graphqlRequest('/graphql/CreateRetweet', {
        tweet_id: tweetId
      });

      if (response && response.data) {
        console.log(`[✅] 转发成功: ${tweetId}`);
        return { success: true, tweetId, timestamp: new Date().toISOString() };
      }

      throw new Error('转发失败');
    } catch (err) {
      console.error(`[❌] 转发失败: ${err.message}`);
      throw err;
    }
  }

  /**
   * 优化的删除推文方法
   */
  async deleteTweet(tweetId) {
    if (!this.authToken) {
      throw new Error('需要 TWITTER_AUTH_TOKEN');
    }

    console.log(`[🗑️] 删除推文: ${tweetId}`);

    try {
      const response = await this.graphqlRequest('/graphql/DeleteTweet', {
        tweet_id: tweetId
      });

      if (response && response.data) {
        console.log(`[✅] 推文已删除`);
        return { success: true, tweetId };
      }

      throw new Error('删除失败');
    } catch (err) {
      console.error(`[❌] 删除失败: ${err.message}`);
      throw err;
    }
  }

  /**
   * 优化的获取推文信息方法
   */
  async getTweet(tweetId) {
    console.log(`[🔍] 查询推文: ${tweetId}`);

    try {
      const response = await this.graphqlRequest('/graphql/TweetDetail', {
        id: tweetId
      });

      if (response && response.data) {
        console.log(`[✅] 推文查询成功`);
        return { success: true, tweet: response.data };
      }

      throw new Error('推文不存在');
    } catch (err) {
      console.error(`[❌] 查询失败: ${err.message}`);
      throw err;
    }
  }

  /**
   * 优化的回复推文方法
   */
  async replyTweet(tweetId, text) {
    if (!this.authToken) {
      throw new Error('需要 TWITTER_AUTH_TOKEN');
    }

    if (!text || text.trim().length === 0) {
      throw new Error('回复内容不能为空');
    }

    console.log(`[💬] 回复推文: ${tweetId}`);

    try {
      const response = await this.graphqlRequest('/graphql/CreateTweet', {
        tweet_text: text,
        reply: { in_reply_to_tweet_id: tweetId },
        media: null,
        dark_request: false,
        semantic_annotation_ids: [],
        includePromotedContent: false
      });

      if (response && response.data) {
        const replyId = response.data.create_tweet?.tweet_results?.result?.rest_id || 'unknown';
        console.log(`[✅] 回复成功: ${replyId}`);
        return { success: true, replyId, timestamp: new Date().toISOString() };
      }

      throw new Error('回复失败');
    } catch (err) {
      console.error(`[❌] 回复失败: ${err.message}`);
      throw err;
    }
  }

  /**
   * 优化的获取账户信息方法
   */
  async getMyInfo() {
    if (!this.authToken) {
      throw new Error('需要 TWITTER_AUTH_TOKEN');
    }

    console.log('[👤] 获取账户信息...');

    try {
      const response = await this.v2Request('/v1.1/account/verify_credentials.json');

      if (response && response.id) {
        console.log('[✅] 账户信息获取成功');
        return {
          success: true,
          user: {
            id: response.id,
            name: response.name,
            screen_name: response.screen_name,
            followers_count: response.followers_count,
            friends_count: response.friends_count,
            statuses_count: response.statuses_count,
            description: response.description,
            profile_image_url: response.profile_image_url_https
          }
        };
      }

      throw new Error('获取账户信息失败');
    } catch (err) {
      console.error(`[❌] 获取失败: ${err.message}`);
      throw err;
    }
  }

  /**
   * 优化的获取我的推文列表
   */
  async getMyTweets(options = {}) {
    if (!this.authToken) {
      throw new Error('需要 TWITTER_AUTH_TOKEN');
    }

    console.log('[📝] 获取我的推文...');

    try {
      const params = new URLSearchParams({
        count: options.count || 20,
        exclude_replies: options.excludeReplies || false,
        include_rts: options.includeRetweets !== false,
        trim_user: 'true'
      });

      const response = await this.v2Request(
        `/v1.1/statuses/user_timeline.json?${params.toString()}`
      );

      if (Array.isArray(response)) {
        console.log(`[✅] 获取成功: ${response.length} 条推文`);
        return {
          success: true,
          tweets: response,
          count: response.length
        };
      }

      throw new Error('获取推文失败');
    } catch (err) {
      console.error(`[❌] 获取失败: ${err.message}`);
      throw err;
    }
  }

  /**
   * 优化的获取时间线
   */
  async getTimeline(options = {}) {
    if (!this.authToken) {
      throw new Error('需要 TWITTER_AUTH_TOKEN');
    }

    console.log('[📰] 获取 Timeline...');

    try {
      const params = new URLSearchParams({
        count: options.count || 20,
        exclude_replies: options.excludeReplies || false,
        include_rts: options.includeRetweets !== false
      });

      const response = await this.v2Request(
        `/v1.1/statuses/home_timeline.json?${params.toString()}`
      );

      if (Array.isArray(response)) {
        console.log(`[✅] 获取成功: ${response.length} 条推文`);
        return {
          success: true,
          tweets: response,
          count: response.length
        };
      }

      throw new Error('获取 Timeline 失败');
    } catch (err) {
      console.error(`[❌] 获取失败: ${err.message}`);
      throw err;
    }
  }

  /**
   * 优化的搜索推文
   */
  async searchTweets(query, options = {}) {
    console.log(`[🔎] 搜索推文: ${query}`);

    try {
      const params = new URLSearchParams({
        q: query,
        count: options.count || 10,
        lang: options.lang || 'en'
      });

      const response = await this.v2Request(
        `/v1.1/search/tweets.json?${params.toString()}`
      );

      if (response && response.statuses) {
        console.log(`[✅] 搜索成功: ${response.statuses.length} 条结果`);
        return {
          success: true,
          tweets: response.statuses,
          count: response.statuses.length
        };
      }

      throw new Error('搜索失败');
    } catch (err) {
      console.error(`[❌] 搜索失败: ${err.message}`);
      throw err;
    }
  }

  /**
   * 优化的获取用户信息
   */
  async getUser(username) {
    console.log(`[👤] 查询用户: ${username}`);

    try {
      const response = await this.v2Request(
        `/v1.1/users/show.json?screen_name=${username}`
      );

      if (response && response.id) {
        console.log('[✅] 用户查询成功');
        return {
          success: true,
          user: {
            id: response.id,
            name: response.name,
            screen_name: response.screen_name,
            followers_count: response.followers_count,
            description: response.description
          }
        };
      }

      throw new Error('用户不存在');
    } catch (err) {
      console.error(`[❌] 查询失败: ${err.message}`);
      throw err;
    }
  }

  /**
   * 优化的关注用户
   */
  async followUser(userId) {
    if (!this.authToken) {
      throw new Error('需要 TWITTER_AUTH_TOKEN');
    }

    console.log(`[👥] 关注用户: ${userId}`);

    try {
      const response = await this.v2Request(
        `/v1.1/friendships/create.json?user_id=${userId}`,
        { method: 'POST' }
      );

      if (response && response.id) {
        console.log('[✅] 已关注');
        return { success: true, userId };
      }

      throw new Error('关注失败');
    } catch (err) {
      console.error(`[❌] 关注失败: ${err.message}`);
      throw err;
    }
  }

  /**
   * 优化的取消关注
   */
  async unfollowUser(userId) {
    if (!this.authToken) {
      throw new Error('需要 TWITTER_AUTH_TOKEN');
    }

    console.log(`[👥] 取消关注: ${userId}`);

    try {
      const response = await this.v2Request(
        `/v1.1/friendships/destroy.json?user_id=${userId}`,
        { method: 'POST' }
      );

      if (response && response.id) {
        console.log('[✅] 已取消关注');
        return { success: true, userId };
      }

      throw new Error('取消关注失败');
    } catch (err) {
      console.error(`[❌] 取消关注失败: ${err.message}`);
      throw err;
    }
  }

  /**
   * 优化的获取粉丝列表
   */
  async getFollowers(options = {}) {
    if (!this.authToken) {
      throw new Error('需要 TWITTER_AUTH_TOKEN');
    }

    console.log('[👥] 获取粉丝列表...');

    try {
      const params = new URLSearchParams({
        count: options.count || 20,
        cursor: options.cursor || '-1'
      });

      const response = await this.v2Request(
        `/v1.1/followers/list.json?${params.toString()}`
      );

      if (response && response.users) {
        console.log(`[✅] 获取成功: ${response.users.length} 个粉丝`);
        return {
          success: true,
          followers: response.users,
          count: response.users.length,
          nextCursor: response.next_cursor
        };
      }

      throw new Error('获取粉丝失败');
    } catch (err) {
      console.error(`[❌] 获取失败: ${err.message}`);
      throw err;
    }
  }

  /**
   * 优化的获取关注列表
   */
  async getFollowing(options = {}) {
    if (!this.authToken) {
      throw new Error('需要 TWITTER_AUTH_TOKEN');
    }

    console.log('[👥] 获取关注列表...');

    try {
      const params = new URLSearchParams({
        count: options.count || 20,
        cursor: options.cursor || '-1'
      });

      const response = await this.v2Request(
        `/v1.1/friends/list.json?${params.toString()}`
      );

      if (response && response.users) {
        console.log(`[✅] 获取成功: ${response.users.length} 个关注`);
        return {
          success: true,
          following: response.users,
          count: response.users.length,
          nextCursor: response.next_cursor
        };
      }

      throw new Error('获取关注失败');
    } catch (err) {
      console.error(`[❌] 获取失败: ${err.message}`);
      throw err;
    }
  }

  /**
   * 批量批准方法 - 标准化错误处理和日志
   */
  async checkQuota() {
    console.log('[📊] 检查 API 配额...');

    try {
      const response = await this.v2Request(`/key/${this.apiKey}`);

      const remaining = typeof response === 'number' ? response :
                       response.remaining || response.remaining_calls || 0;

      console.log(`[✅] 配额检查成功: 剩余 ${remaining}`);
      return {
        success: true,
        remaining,
        timestamp: new Date().toISOString()
      };
    } catch (err) {
      console.error(`[❌] 配额检查失败: ${err.message}`);
      throw err;
    }
  }
}

module.exports = TwitterDanceOptimized;
