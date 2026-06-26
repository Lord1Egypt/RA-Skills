/**
 * Twitter Dance API Client
 * 
 * 使用 apidance.pro 的 Twitter API
 * 支持发推、查询、点赞等操作
 * 
 * 优势：
 * - 支持 Twitter v1.1 和 GraphQL API
 * - 完全兼容官方 API
 * - 支持 AuthToken 操作自己的账户
 * - 绕过 Cloudflare 验证
 */

const https = require('https');

class TwitterDanceAPIClient {
  constructor(options = {}) {
    this.apiKey = options.apiKey || process.env.APIDANCE_API_KEY;
    this.authToken = options.authToken || process.env.TWITTER_AUTH_TOKEN;
    this.baseUrl = 'https://api.apidance.pro';
    this.verbose = options.verbose || false;

    if (!this.apiKey) {
      throw new Error('缺少 APIDANCE_API_KEY (在 https://t.me/shingle 购买)');
    }
  }

  /**
   * 发送 API 请求（通用 - 向后兼容）
   * 
   * 注：新代码应使用 v2Request() 或 graphqlRequest()
   * 这个方法保留用于向后兼容
   */
  async request(endpoint, options = {}) {
    return new Promise((resolve, reject) => {
      const method = options.method || 'GET';
      const headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Apidog/1.0.0 (https://apidog.com)',
        ...options.headers
      };

      // 使用小写的认证头（新标准）
      headers['apikey'] = this.apiKey;
      if (this.authToken) {
        headers['authtoken'] = this.authToken;
      }

      let url = `${this.baseUrl}${endpoint}`;
      const urlObj = new URL(url);

      const reqOptions = {
        hostname: urlObj.hostname,
        path: urlObj.pathname + urlObj.search,
        method,
        headers
      };

      if (this.verbose) {
        console.log(`[API] ${method} ${endpoint}`);
      }

      const req = https.request(reqOptions, (res) => {
        let data = '';

        res.on('data', (chunk) => {
          data += chunk;
        });

        res.on('end', () => {
          try {
            // 先尝试 JSON 解析
            try {
              const json = JSON.parse(data);
              resolve(json);
            } catch (jsonErr) {
              // 如果是纯数字（比如配额查询返回 9998），直接返回数字
              const num = parseInt(data);
              if (!isNaN(num)) {
                resolve(num);
              } else {
                // 其他格式，返回原始数据
                resolve(data);
              }
            }
          } catch (e) {
            reject(new Error(`解析失败: ${data}`));
          }
        });
      });

      req.on('error', (err) => {
        reject(err);
      });

      if (options.body) {
        req.write(JSON.stringify(options.body));
      }

      req.end();
    });
  }

  /**
   * 发送 GraphQL API 请求（特化版本）
   * 用于 CreateTweet 等 GraphQL 端点
   */
  async graphqlRequest(endpoint, variables = {}) {
    return new Promise((resolve, reject) => {
      const url = `${this.baseUrl}${endpoint}`;
      const urlObj = new URL(url);

      const headers = {
        'Authtoken': this.authToken || '',
        'apikey': this.apiKey,
        'User-Agent': 'Apidog/1.0.0 (https://apidog.com)',
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Host': urlObj.hostname,
        'Connection': 'keep-alive'
      };

      const reqOptions = {
        hostname: urlObj.hostname,
        path: urlObj.pathname + urlObj.search,
        method: 'POST',
        headers
      };

      if (this.verbose) {
        console.log(`[GraphQL] ${endpoint}`);
        if (this.verbose > 1) {
          console.log(`[Payload]`, JSON.stringify(variables, null, 2));
        }
      }

      const req = https.request(reqOptions, (res) => {
        let data = '';

        res.on('data', (chunk) => {
          data += chunk;
        });

        res.on('end', () => {
          try {
            const json = JSON.parse(data);
            if (this.verbose) {
              console.log(`[Response]`, JSON.stringify(json, null, 2));
            }
            resolve(json);
          } catch (err) {
            reject(new Error(`解析失败: ${data}`));
          }
        });
      });

      req.on('error', (err) => {
        reject(err);
      });

      const body = { variables };
      req.write(JSON.stringify(body));
      req.end();
    });
  }

  /**
   * 发送 API v2 请求（GET 方式）
   * 用于 /2/notifications/all.json 等端点
   * 注：使用小写的 authtoken 和 apikey 头
   */
  async v2Request(endpoint, options = {}) {
    return new Promise((resolve, reject) => {
      const method = options.method || 'GET';
      const headers = {
        'authtoken': this.authToken || '',
        'apikey': this.apiKey,
        'User-Agent': 'Apidog/1.0.0 (https://apidog.com)',
        'Accept': '*/*',
        'Connection': 'keep-alive'
      };

      let url = `${this.baseUrl}${endpoint}`;
      const urlObj = new URL(url);

      const reqOptions = {
        hostname: urlObj.hostname,
        path: urlObj.pathname + urlObj.search,
        method,
        headers
      };

      if (this.verbose) {
        console.log(`[API v2] ${method} ${endpoint}`);
      }

      const req = https.request(reqOptions, (res) => {
        let data = '';

        res.on('data', (chunk) => {
          data += chunk;
        });

        res.on('end', () => {
          try {
            const json = JSON.parse(data);
            if (this.verbose) {
              console.log(`[Response]`, JSON.stringify(json, null, 2).substring(0, 500));
            }
            resolve(json);
          } catch (err) {
            reject(new Error(`解析失败: ${data}`));
          }
        });
      });

      req.on('error', (err) => {
        reject(err);
      });

      if (options.body) {
        req.write(JSON.stringify(options.body));
      }

      req.end();
    });
  }

  /**
   * 发推文（GraphQL API - CreateTweet）
   * 
   * 使用 apidance.pro 的官方 GraphQL 端点
   * 支持纯文本推文、带媒体推文、回复推文等
   */
  async tweet(text, options = {}) {
    if (!text || text.trim().length === 0) {
      throw new Error('推文内容不能为空');
    }

    if (text.length > 280) {
      throw new Error(`推文过长 (${text.length}/280)`);
    }

    if (!this.authToken) {
      throw new Error('需要 TWITTER_AUTH_TOKEN 来发推文（在 X.com/settings 中获取）');
    }

    console.log('[📝] 发布推文...');
    console.log(`     内容: ${text.substring(0, 60)}...`);
    console.log(`     字数: ${text.length}/280`);

    try {
      // 构建 GraphQL variables（严格按照 apidance.pro 格式）
      const variables = {
        // 必需字段
        tweet_text: text,
        dark_request: false,

        // reply 模块 - 如果没有回复需求则为 null
        reply: options.inReplyToTweetId ? {
          in_reply_to_tweet_id: options.inReplyToTweetId,
          exclude_reply_user_ids: options.excludeReplyUserIds || []
        } : null,

        // media 模块 - 如果没有媒体则为 null
        media: options.media && Array.isArray(options.media) && options.media.length > 0
          ? {
              media_entities: options.media.map(m => ({
                media_id: typeof m === 'string' ? m : m.media_id,
                tagged_users: m.tagged_users || []
              })),
              possibly_sensitive: options.possiblySensitive || false
            }
          : null,

        // 其他字段
        semantic_annotation_ids: options.semanticAnnotationIds || [],
        includePromotedContent: options.includePromotedContent || false
      };

      if (this.verbose) {
        console.log('[Variables]', JSON.stringify(variables, null, 2));
      }

      // 调用 GraphQL API
      const response = await this.graphqlRequest('/graphql/CreateTweet', variables);

      // 检查响应
      if (response.data && (response.data.create_tweet || response.data.tweet_results)) {
        const tweetData = response.data.create_tweet || response.data.tweet_results;
        const tweetId = tweetData.tweet_results?.result?.rest_id || 
                        tweetData.result?.rest_id || 
                        tweetData.id ||
                        'unknown';

        console.log(`[✅] 推文已发布！`);
        console.log(`     Tweet ID: ${tweetId}`);

        return {
          success: true,
          tweetId,
          timestamp: new Date().toISOString(),
          text,
          length: text.length,
          rawResponse: response
        };
      }

      // 检查是否有错误
      if (response.errors) {
        throw new Error(`API 错误: ${response.errors.map(e => e.message).join(', ')}`);
      }

      // 其他异常响应
      throw new Error(`API 返回异常格式: ${JSON.stringify(response)}`);

    } catch (err) {
      console.error(`[❌] 发推失败: ${err.message}`);
      throw err;
    }
  }

  /**
   * 点赞推文（使用 GraphQL API）
   */
  async likeTweet(tweetId) {
    if (!this.authToken) {
      throw new Error('需要 TWITTER_AUTH_TOKEN');
    }

    console.log(`[❤️] 点赞推文: ${tweetId}`);

    try {
      // 使用 GraphQL 端点
      const response = await this.graphqlRequest('/graphql/FavoriteTweet', {
        tweet_id: tweetId
      });

      if (response && response.data) {
        console.log(`[✅] 点赞成功`);
        return { success: true, tweetId };
      }

      throw new Error('点赞失败');
    } catch (err) {
      console.error(`[❌] 点赞失败: ${err.message}`);
      throw err;
    }
  }

  /**
   * 转发推文（使用 GraphQL API）
   */
  async retweet(tweetId) {
    if (!this.authToken) {
      throw new Error('需要 TWITTER_AUTH_TOKEN');
    }

    console.log(`[🔄] 转发推文: ${tweetId}`);

    try {
      // 使用 GraphQL 端点
      const response = await this.graphqlRequest('/graphql/CreateRetweet', {
        tweet_id: tweetId
      });

      if (response && response.data) {
        console.log(`[✅] 转发成功`);
        return { success: true, tweetId };
      }

      throw new Error('转发失败');
    } catch (err) {
      console.error(`[❌] 转发失败: ${err.message}`);
      throw err;
    }
  }

  /**
   * 查询推文信息（使用 GraphQL TweetDetail）
   */
  async getTweet(tweetId) {
    console.log(`[🔍] 查询推文: ${tweetId}`);

    try {
      const response = await this.graphqlRequest('/graphql/TweetDetail', {
        focalTweetId: tweetId,
        with_rux_injections: false,
        includePromotedContent: false,
        withCommunity: false,
        withQuickPromoteEligibilityTweetFields: false,
        withBirdwatchNotes: false,
        withVoice: false
      });

      if (response.data && response.data.threaded_conversation_with_injections_v2) {
        const instructions = response.data.threaded_conversation_with_injections_v2.instructions || [];
        const addEntries = instructions.find(i => i.type === 'TimelineAddEntries');
        const entries = addEntries?.entries || [];

        // 提取主推文和回复
        const tweetEntry = entries.find(e => e.entryId?.startsWith('tweet-'));
        const tweetResult = tweetEntry?.content?.itemContent?.tweet_results?.result;

        return {
          success: true,
          tweet: response.data.threaded_conversation_with_injections_v2,
          tweetData: tweetResult?.legacy || null,
          entries
        };
      }

      if (response.errors) {
        throw new Error(`API 错误: ${response.errors.map(e => e.message).join(', ')}`);
      }

      throw new Error('推文不存在');
    } catch (err) {
      console.error(`[❌] 查询失败: ${err.message}`);
      throw err;
    }
  }

  /**
   * 查询用户信息（使用 GraphQL UserByScreenName）
   */
  async getUser(username) {
    console.log(`[👤] 查询用户: ${username}`);

    try {
      const response = await this.graphqlRequest('/graphql/UserByScreenName', {
        screen_name: username
      });

      const userResult = response.data?.user?.result;
      if (!userResult) {
        throw new Error('用户不存在');
      }

      const legacy = userResult.legacy || {};
      return {
        success: true,
        user: {
          id: userResult.rest_id || '',
          id_str: userResult.rest_id || '',
          name: legacy.name || userResult.core?.name || '',
          screen_name: legacy.screen_name || userResult.core?.screen_name || '',
          followers_count: legacy.followers_count || 0,
          friends_count: legacy.friends_count || 0,
          statuses_count: legacy.statuses_count || 0,
          description: legacy.description || '',
          verified: userResult.is_blue_verified || false
        }
      };
    } catch (err) {
      console.error(`[❌] 用户查询失败: ${err.message}`);
      throw err;
    }
  }

  /**
   * 搜索推文（使用 GraphQL SearchTimeline）
   */
  async searchTweets(query, options = {}) {
    console.log(`[🔎] 搜索推文: ${query}`);

    try {
      const response = await this.graphqlRequest('/graphql/SearchTimeline', {
        rawQuery: query,
        count: options.count || 10,
        querySource: 'typed_query',
        product: 'Top'
      });

      const instructions = response.data?.search_by_raw_query?.search_timeline?.timeline?.instructions || [];
      const addEntries = instructions.find(i => i.type === 'TimelineAddEntries');
      const entries = addEntries?.entries || [];

      const tweets = [];
      for (const entry of entries) {
        const tweetResult = entry.content?.itemContent?.tweet_results?.result;
        if (tweetResult && tweetResult.legacy) {
          const legacy = tweetResult.legacy;
          const userLegacy = tweetResult.core?.user_results?.result?.legacy || {};
          tweets.push({
            id_str: tweetResult.rest_id || '',
            text: legacy.full_text || '',
            favorite_count: legacy.favorite_count || 0,
            retweet_count: legacy.retweet_count || 0,
            created_at: legacy.created_at || '',
            user: {
              screen_name: userLegacy.screen_name || '',
              name: userLegacy.name || ''
            }
          });
        }
      }

      return {
        success: true,
        tweets,
        count: tweets.length
      };
    } catch (err) {
      console.error(`[❌] 搜索失败: ${err.message}`);
      throw err;
    }
  }

  /**
   * 获取 Timeline（使用 GraphQL HomeTimeline）
   *
   * 注：v1.1 的 home_timeline 在 apidance.pro 上返回 null，
   * 因此改用 GraphQL HomeTimeline 端点
   */
  async getTimeline(options = {}) {
    console.log('[📰] 获取 Timeline...');

    try {
      const response = await this.graphqlRequest('/graphql/HomeTimeline', {
        count: options.count || 20,
        includePromotedContent: false,
        latestControlAvailable: true,
        withCommunity: false
      });

      const instructions = response.data?.home?.home_timeline_urt?.instructions || [];
      const addEntries = instructions.find(i => i.type === 'TimelineAddEntries');
      const entries = addEntries?.entries || [];

      const tweets = [];
      for (const entry of entries) {
        const tweetResult = entry.content?.itemContent?.tweet_results?.result;
        if (tweetResult && tweetResult.legacy) {
          const legacy = tweetResult.legacy;
          const userLegacy = tweetResult.core?.user_results?.result?.legacy || {};

          if (options.excludeReplies && legacy.in_reply_to_status_id_str) continue;
          if (options.includeRetweets === false && legacy.retweeted_status_result) continue;

          tweets.push({
            id_str: tweetResult.rest_id || '',
            text: legacy.full_text || '',
            favorite_count: legacy.favorite_count || 0,
            retweet_count: legacy.retweet_count || 0,
            reply_count: legacy.reply_count || 0,
            created_at: legacy.created_at || '',
            user: {
              screen_name: userLegacy.screen_name || '',
              name: userLegacy.name || ''
            }
          });
        }
      }

      return {
        success: true,
        tweets,
        count: tweets.length
      };
    } catch (err) {
      console.error(`[❌] 获取失败: ${err.message}`);
      throw err;
    }
  }

  /**
   * 检查 API 配额
   */
  async checkQuota() {
    console.log('[📊] 检查 API 配额...');

    try {
      // API 返回纯数字（剩余次数）
      const response = await this.request(`/key/${this.apiKey}`);
      
      // 解析响应（可能是 JSON 或纯数字）
      let remaining = 0;
      
      if (typeof response === 'number') {
        remaining = response;
      } else if (response && typeof response === 'object') {
        remaining = response.remaining || response.remaining_calls || 0;
      } else if (typeof response === 'string') {
        remaining = parseInt(response) || 0;
      }

      return {
        success: true,
        remaining: remaining,
        timestamp: new Date().toISOString()
      };
    } catch (err) {
      console.error(`[❌] 配额检查失败: ${err.message}`);
      throw err;
    }
  }

  /**
   * 删除推文（使用 GraphQL DeleteTweet）
   */
  async deleteTweet(tweetId) {
    if (!this.authToken) {
      throw new Error('需要 TWITTER_AUTH_TOKEN');
    }

    console.log(`[🗑️] 删除推文: ${tweetId}`);

    try {
      const response = await this.graphqlRequest('/graphql/DeleteTweet', {
        tweet_id: tweetId,
        dark_request: false
      });

      if (response.data) {
        console.log(`[✅] 推文已删除`);
        return { success: true, tweetId };
      }

      if (response.errors) {
        throw new Error(`API 错误: ${response.errors.map(e => e.message).join(', ')}`);
      }

      throw new Error('删除失败');
    } catch (err) {
      console.error(`[❌] 删除失败: ${err.message}`);
      throw err;
    }
  }

  /**
   * 获取我的推文列表（使用 GraphQL UserTweets）
   *
   * 注：v1.1 的 user_timeline 在 apidance.pro 上返回 null，
   * 因此改用 GraphQL UserTweets 端点
   */
  async getMyTweets(options = {}) {
    if (!this.authToken) {
      throw new Error('需要 TWITTER_AUTH_TOKEN');
    }

    console.log(`[📝] 获取我的推文...`);

    try {
      // 先获取当前用户 ID
      const myInfo = await this.getMyInfo();
      const userId = String(myInfo.user.id);

      const response = await this.graphqlRequest('/graphql/UserTweets', {
        userId,
        count: options.count || 20,
        includePromotedContent: false,
        withQuickPromoteEligibilityTweetFields: false,
        withVoice: false,
        withV2Timeline: true
      });

      // 从 GraphQL 响应中提取推文
      const instructions = response.data?.user?.result?.timeline_v2?.timeline?.instructions || [];
      const addEntries = instructions.find(i => i.type === 'TimelineAddEntries') || instructions.find(i => i.entries);
      const entries = addEntries?.entries || [];

      const tweets = [];
      for (const entry of entries) {
        const tweetResult = entry.content?.itemContent?.tweet_results?.result;
        if (tweetResult && tweetResult.legacy) {
          const legacy = tweetResult.legacy;
          // 过滤转发
          if (!options.includeRetweets === false && legacy.retweeted_status_result) continue;
          // 过滤回复
          if (options.excludeReplies && legacy.in_reply_to_status_id_str) continue;

          tweets.push({
            id_str: legacy.conversation_id_str || tweetResult.rest_id || entry.entryId?.replace('tweet-', ''),
            text: legacy.full_text || '',
            favorite_count: legacy.favorite_count || 0,
            retweet_count: legacy.retweet_count || 0,
            reply_count: legacy.reply_count || 0,
            created_at: legacy.created_at || '',
            user: tweetResult.core?.user_results?.result?.legacy || {}
          });
        }
      }

      return {
        success: true,
        tweets,
        count: tweets.length
      };
    } catch (err) {
      console.error(`[❌] 获取失败: ${err.message}`);
      throw err;
    }
  }

  /**
   * 关注用户
   */
  async followUser(userId) {
    if (!this.authToken) {
      throw new Error('需要 TWITTER_AUTH_TOKEN');
    }

    console.log(`[👥] 关注用户: ${userId}`);

    try {
      const response = await this.request(`/1.1/friendships/create.json?user_id=${userId}`, {
        method: 'POST'
      });

      console.log(`[✅] 已关注`);
      return { success: true, userId };
    } catch (err) {
      console.error(`[❌] 关注失败: ${err.message}`);
      throw err;
    }
  }

  /**
   * 取消关注用户
   */
  async unfollowUser(userId) {
    if (!this.authToken) {
      throw new Error('需要 TWITTER_AUTH_TOKEN');
    }

    console.log(`[👥] 取消关注用户: ${userId}`);

    try {
      const response = await this.request(`/1.1/friendships/destroy.json?user_id=${userId}`, {
        method: 'POST'
      });

      console.log(`[✅] 已取消关注`);
      return { success: true, userId };
    } catch (err) {
      console.error(`[❌] 取消关注失败: ${err.message}`);
      throw err;
    }
  }

  /**
   * 获取用户粉丝列表
   */
  async getFollowers(options = {}) {
    if (!this.authToken) {
      throw new Error('需要 TWITTER_AUTH_TOKEN');
    }

    console.log(`[👥] 获取粉丝列表...`);

    try {
      const params = new URLSearchParams({
        count: options.count || 20,
        cursor: options.cursor || '-1'
      });

      const response = await this.request(
        `/1.1/followers/list.json?${params.toString()}`
      );

      return {
        success: true,
        followers: response.users || [],
        count: response.users?.length || 0,
        nextCursor: response.next_cursor || null
      };
    } catch (err) {
      console.error(`[❌] 获取失败: ${err.message}`);
      throw err;
    }
  }

  /**
   * 获取我关注的用户列表
   */
  async getFollowing(options = {}) {
    if (!this.authToken) {
      throw new Error('需要 TWITTER_AUTH_TOKEN');
    }

    console.log(`[👥] 获取关注列表...`);

    try {
      const params = new URLSearchParams({
        count: options.count || 20,
        cursor: options.cursor || '-1'
      });

      const response = await this.request(
        `/1.1/friends/list.json?${params.toString()}`
      );

      return {
        success: true,
        following: response.users || [],
        count: response.users?.length || 0,
        nextCursor: response.next_cursor || null
      };
    } catch (err) {
      console.error(`[❌] 获取失败: ${err.message}`);
      throw err;
    }
  }

  /**
   * 获取推文的评论（使用 GraphQL TweetDetail）
   */
  async getReplies(tweetId, options = {}) {
    console.log(`[💬] 获取推文回复: ${tweetId}`);

    try {
      const response = await this.graphqlRequest('/graphql/TweetDetail', {
        focalTweetId: tweetId,
        with_rux_injections: false,
        includePromotedContent: false,
        withCommunity: false,
        withQuickPromoteEligibilityTweetFields: false,
        withBirdwatchNotes: false,
        withVoice: false
      });

      const instructions = response.data?.threaded_conversation_with_injections_v2?.instructions || [];
      const addEntries = instructions.find(i => i.type === 'TimelineAddEntries');
      const entries = addEntries?.entries || [];

      // 回复的 entryId 以 'conversationthread-' 开头
      const replies = [];
      for (const entry of entries) {
        if (entry.entryId?.startsWith('conversationthread-')) {
          const items = entry.content?.items || [];
          for (const item of items) {
            const tweetResult = item.item?.itemContent?.tweet_results?.result;
            if (tweetResult && tweetResult.legacy) {
              const legacy = tweetResult.legacy;
              const userLegacy = tweetResult.core?.user_results?.result?.legacy || {};
              replies.push({
                id_str: tweetResult.rest_id || '',
                text: legacy.full_text || '',
                full_text: legacy.full_text || '',
                favorite_count: legacy.favorite_count || 0,
                retweet_count: legacy.retweet_count || 0,
                reply_count: legacy.reply_count || 0,
                created_at: legacy.created_at || '',
                in_reply_to_status_id_str: legacy.in_reply_to_status_id_str || '',
                in_reply_to_screen_name: legacy.in_reply_to_screen_name || '',
                user: {
                  screen_name: userLegacy.screen_name || 'unknown',
                  name: userLegacy.name || '',
                  id_str: tweetResult.core?.user_results?.result?.rest_id || ''
                }
              });
            }
          }
        }
      }

      const maxCount = options.count || 20;
      const limited = replies.slice(0, maxCount);

      return {
        success: true,
        replies: limited,
        count: limited.length
      };
    } catch (err) {
      console.error(`[❌] 获取失败: ${err.message}`);
      throw err;
    }
  }

  /**
   * 回复推文（使用 GraphQL CreateTweet）
   */
  async replyTweet(tweetId, text) {
    if (!this.authToken) {
      throw new Error('需要 TWITTER_AUTH_TOKEN');
    }

    if (!text || text.trim().length === 0) {
      throw new Error('回复内容不能为空');
    }

    console.log(`[💬] 回复推文: ${tweetId}`);
    console.log(`     内容: ${text.substring(0, 50)}...`);

    try {
      const response = await this.graphqlRequest('/graphql/CreateTweet', {
        tweet_text: text,
        dark_request: false,
        reply: {
          in_reply_to_tweet_id: tweetId,
          exclude_reply_user_ids: []
        },
        media: null,
        semantic_annotation_ids: [],
        includePromotedContent: false
      });

      if (response.data && (response.data.create_tweet || response.data.tweet_results)) {
        const tweetData = response.data.create_tweet || response.data.tweet_results;
        const replyId = tweetData.tweet_results?.result?.rest_id ||
                        tweetData.result?.rest_id ||
                        'unknown';
        console.log(`[✅] 回复已发送`);
        return { success: true, tweetId: replyId };
      }

      if (response.errors) {
        throw new Error(`API 错误: ${response.errors.map(e => e.message).join(', ')}`);
      }

      throw new Error('回复失败：未知响应格式');
    } catch (err) {
      console.error(`[❌] 回复失败: ${err.message}`);
      throw err;
    }
  }

  /**
   * 获取账户信息
   */
  async getMyInfo() {
    if (!this.authToken) {
      throw new Error('需要 TWITTER_AUTH_TOKEN');
    }

    console.log(`[👤] 获取账户信息...`);

    try {
      const response = await this.request(`/1.1/account/verify_credentials.json`);

      return {
        success: true,
        user: {
          id: response.id_str || String(response.id),
          id_str: response.id_str || String(response.id),
          name: response.name,
          screen_name: response.screen_name,
          followers_count: response.followers_count,
          friends_count: response.friends_count,
          statuses_count: response.statuses_count,
          favourites_count: response.favourites_count,
          listed_count: response.listed_count,
          media_count: response.media_count,
          description: response.description,
          location: response.location,
          created_at: response.created_at,
          protected: response.protected,
          profile_image_url: response.profile_image_url_https
        }
      };
    } catch (err) {
      console.error(`[❌] 获取失败: ${err.message}`);
      throw err;
    }
  }
}

module.exports = TwitterDanceAPIClient;
