# JWT端点URL设置检查清单

## 🎯 当前状态
- WordPress站点: https://openow.ai
- WordPress版本: 6.9.4
- REST API状态: ✅ 正常
- JWT插件状态: ❌ 未安装

## 🔧 安装步骤

### 第一步: 安装JWT插件
1. [ ] 登录WordPress后台: `https://openow.ai/wp-admin`
2. [ ] 进入 **插件 → 安装插件**
3. [ ] 搜索: **"JWT Authentication for WP REST API"**
4. [ ] 点击 **"立即安装"**
5. [ ] 点击 **"启用"**

### 第二步: 配置wp-config.php
1. [ ] 备份 `wp-config.php` 文件
2. [ ] 编辑文件，在 `/* That's all, stop editing! Happy publishing. */` 之前添加:
```php
// JWT Authentication Configuration
define('JWT_AUTH_SECRET_KEY', 'your-very-strong-secret-key-minimum-32-characters');
define('JWT_AUTH_CORS_ENABLE', true);
```
3. [ ] 生成安全密钥:
```bash
# 方法1: 使用OpenSSL
openssl rand -base64 32

# 方法2: 使用在线生成器
# https://randomkeygen.com/
```

### 第三步: 测试安装
1. [ ] 测试JWT端点:
```bash
curl -X POST https://openow.ai/wp-json/jwt-auth/v1/token \
  -H "Content-Type: application/json" \
  -d '{"username":"inkmind","password":"SAGI b8Zi QBOm CQhW xl4N lmP1"}'
```

2. [ ] 预期成功响应:
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user_email": "inkmind@example.com",
  "user_nicename": "inkmind",
  "user_display_name": "Inkmind"
}
```

## 🚀 JWT端点URL参考

### 标准端点 (安装JWT插件后)
| 端点 | URL | 方法 | 用途 |
|------|-----|------|------|
| 获取令牌 | `https://openow.ai/wp-json/jwt-auth/v1/token` | POST | 获取JWT令牌 |
| 验证令牌 | `https://openow.ai/wp-json/jwt-auth/v1/token/validate` | POST | 验证JWT令牌 |
| 刷新令牌 | `https://openow.ai/wp-json/jwt-auth/v1/token/refresh` | POST | 刷新JWT令牌 |

### 使用示例
```javascript
// 1. 获取JWT令牌
const tokenResponse = await axios.post(
  'https://openow.ai/wp-json/jwt-auth/v1/token',
  {
    username: 'inkmind',
    password: 'your-password'
  },
  {
    headers: { 'Content-Type': 'application/json' }
  }
);

const jwtToken = tokenResponse.data.token;

// 2. 使用JWT访问WordPress API
const api = axios.create({
  baseURL: 'https://openow.ai/wp-json/wp/v2',
  headers: {
    'Authorization': `Bearer ${jwtToken}`,
    'Content-Type': 'application/json'
  }
});

// 3. 发布文章
const postData = {
  title: 'JWT自动发布测试',
  content: '文章内容...',
  status: 'draft'
};

const response = await api.post('/posts', postData);
```

## ⚠️ 常见问题解决

### 问题1: 安装后还是404
1. 检查插件是否已激活
2. 重新保存固定链接设置
3. 检查Nginx配置（需要传递授权头）
4. 清除WordPress缓存

### 问题2: 返回500错误
1. 检查 `JWT_AUTH_SECRET_KEY` 是否设置
2. 确保密钥足够长（≥32字符）
3. 检查PHP错误日志
4. 确保 `wp-config.php` 语法正确

### 问题3: 认证失败
1. 检查用户名和密码
2. 验证用户权限
3. 检查JWT令牌是否过期
4. 确保使用POST请求

## 🔄 备用方案

### 如果JWT插件不工作，使用应用程序密码:
```javascript
// 使用WordPress应用程序密码
const api = axios.create({
  baseURL: 'https://openow.ai/wp-json/wp/v2',
  auth: {
    username: 'inkmind',
    password: 'xxxx xxxx xxxx xxxx xxxx xxxx' // 应用程序密码
  },
  headers: {
    'Content-Type': 'application/json'
  }
});
```

### 获取应用程序密码:
1. WordPress后台 → 用户 → 个人资料
2. 找到"应用程序密码"部分
3. 创建新密码并复制

## 📞 测试脚本

安装完成后，运行测试:
```bash
cd /root/.openclaw/workspace/skills/wordpress-auto-publish
node test-jwt-full.js
```

或使用快速测试:
```bash
./quick-jwt-test.sh
```

## 🎯 成功标志
- ✅ `https://openow.ai/wp-json/jwt-auth/v1/token` 返回JWT令牌
- ✅ 可以使用JWT令牌访问 `/wp-json/wp/v2/users/me`
- ✅ 可以发布文章到WordPress

## ⏱️ 预计时间
- 安装插件: 5分钟
- 配置wp-config.php: 5分钟
- 测试: 5分钟
- 总计: 约15分钟