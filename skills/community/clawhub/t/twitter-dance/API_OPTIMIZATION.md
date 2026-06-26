# Twitter Dance API - 优化方案

> 统一所有方法使用小写 authtoken 和 apikey 请求头

## 优化规则

### 请求头格式标准化

所有 API 请求都改为使用小写格式：

```javascript
// ❌ 旧格式（不兼容某些端点）
{
  'Authtoken': 'xxx',
  'X-AuthToken': 'xxx',
  'Authorization': 'xxx'
}

// ✅ 新格式（统一兼容）
{
  'authtoken': 'xxx',
  'apikey': 'xxx'
}
```

### 核心优化点

1. **GraphQL 请求** (`/graphql/*`)
   - 使用小写 `authtoken` 和 `apikey`
   - 保持 POST 方法
   - Content-Type: application/json

2. **REST API v2** (`/2/*`)
   - 使用小写 `authtoken` 和 `apikey`
   - 支持 GET/POST 方法
   - Accept: */* 
   - User-Agent: Apidog/1.0.0

3. **REST API v1.1** (`/v1.1/*`)
   - 使用小写 `authtoken` 和 `apikey`
   - 向后兼容
   - 自动处理查询参数

## 待优化方法列表

| 方法 | 端点 | 类型 | 优先级 | 状态 |
|------|------|------|--------|------|
| tweet() | /graphql/CreateTweet | GraphQL | P0 | ✅ |
| likeTweet() | /graphql/FavoriteTweet | GraphQL | P0 | ⏳ |
| retweet() | /graphql/CreateRetweet | GraphQL | P0 | ⏳ |
| getTweet() | /graphql/TweetDetail | GraphQL | P1 | ⏳ |
| getMyInfo() | /v1.1/account/verify_credentials.json | REST | P0 | ⏳ |
| getTimeline() | /v1.1/statuses/home_timeline.json | REST | P1 | ⏳ |
| getMyTweets() | /v1.1/statuses/user_timeline.json | REST | P1 | ⏳ |
| searchTweets() | /v1.1/search/tweets.json | REST | P1 | ⏳ |
| getUser() | /v1.1/users/show.json | REST | P1 | ⏳ |
| getFollowers() | /v1.1/followers/list.json | REST | P2 | ⏳ |
| getFollowing() | /v1.1/friends/list.json | REST | P2 | ⏳ |
| followUser() | /v1.1/friendships/create.json | REST | P2 | ⏳ |
| unfollowUser() | /v1.1/friendships/destroy.json | REST | P2 | ⏳ |

## 统一请求方法

所有方法都将使用以下三个统一的请求方法：

### 1. v2Request() - API v2 和 v1.1

```javascript
async v2Request(endpoint, options = {}) {
  // 使用小写的 authtoken 和 apikey
  // 支持 GET/POST
  // 自动处理响应格式
}
```

### 2. graphqlRequest() - GraphQL

```javascript
async graphqlRequest(endpoint, variables = {}) {
  // 使用小写的 authtoken 和 apikey
  // 自动包装 variables
  // POST 方法
}
```

### 3. requestWithAuth() - 通用方法

```javascript
async requestWithAuth(endpoint, options = {}) {
  // 统一认证头格式
  // 自动选择 v2Request 或 request
}
```

## 实现顺序

### Phase 1（紧急 - P0）
- [ ] 修改 graphqlRequest 确保小写头
- [ ] 优化 tweet()
- [ ] 优化 likeTweet()
- [ ] 优化 retweet()
- [ ] 优化 getMyInfo()

### Phase 2（重要 - P1）
- [ ] 优化 getTweet()
- [ ] 优化 getTimeline()
- [ ] 优化 getMyTweets()
- [ ] 优化 searchTweets()
- [ ] 优化 getUser()

### Phase 3（可选 - P2）
- [ ] 优化 getFollowers()
- [ ] 优化 getFollowing()
- [ ] 优化 followUser()
- [ ] 优化 unfollowUser()
- [ ] 优化 deleteTweet()

## 测试覆盖

每个优化的方法都需要测试：

```bash
# P0 测试
node scripts/test-tweet-graphql.js "test"          # tweet()
node scripts/test-advanced-features.js metrics <id> # getTweet()
node scripts/test-advanced-features.js stats        # getMyInfo()

# P1 测试
node scripts/test-advanced-features.js timeline-analytics # getMyTweets()
```

## 回滚计划

如果优化导致问题：

1. 保留原始 request() 方法
2. 在新方法中尝试 v2Request，失败时回退到 request()
3. 设置 verbose 日志便于调试

```javascript
async optimizedMethod() {
  try {
    // 尝试新方法（v2Request）
    return await this.v2Request(endpoint, options);
  } catch (err) {
    // 回退到旧方法
    console.warn('[⚠️] v2Request 失败，回退到 request');
    return await this.request(endpoint, options);
  }
}
```

## 关键发现

🔑 **正确格式**
```bash
curl -H 'authtoken: xxx' -H 'apikey: yyy' \
     -H 'User-Agent: Apidog/1.0.0' \
     https://api.apidance.pro/2/notifications/all.json
```

🔑 **关键点**
- 小写 `authtoken` 和 `apikey`（不是大写！）
- 必须包含 `User-Agent: Apidog/1.0.0`
- `Accept: */*` 和 `Connection: keep-alive`
- 不需要 `Authorization` 头

## 文档更新

优化完成后更新：
- SKILL.md - 方法参考
- GRAPHQL_API_GUIDE.md - 请求格式
- ADVANCED_FEATURES.md - 使用示例

---

**优化目标**: 100% API 兼容性 + 统一请求格式
**预期收益**: 更稳定的 API 调用 + 更少的认证错误
