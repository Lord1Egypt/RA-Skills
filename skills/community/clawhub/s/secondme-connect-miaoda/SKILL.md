---
name: secondme-connect
description: "SecondMe Connect - 数字分身集成器。让百度秒哒应用轻松接入SecondMe生态，一键实现OAuth2登录和完整API调用。3步完成集成，开箱即用。"
metadata:
  openclaw:
    emoji: "🔐"
    tags:
      - secondme
      - oauth2
      - authentication
      - api-integration
      - react
      - supabase
      - 百度秒哒
      - 数字分身
    requires:
      bins:
        - node
        - npm
      env:
        # 前端环境变量
        - name: VITE_SUPABASE_URL
          required: true
          description: "Supabase项目URL（前端使用）"
        - name: VITE_SUPABASE_ANON_KEY
          required: true
          description: "Supabase匿名密钥（前端使用，可公开）"
        - name: VITE_SECONDME_CLIENT_ID
          required: true
          description: "SecondMe OAuth Client ID（前端使用）"
        - name: VITE_SECONDME_REDIRECT_URI
          required: true
          description: "OAuth回调地址，如 https://yourdomain.com/auth/callback"
        # Edge Function 环境变量
        - name: SUPABASE_URL
          required: true
          description: "Supabase项目URL（Edge Function使用）"
        - name: SUPABASE_SERVICE_ROLE_KEY
          required: true
          description: "Supabase服务角色密钥（Edge Function使用，⚠️高权限，严格保密）"
        - name: SECONDME_CLIENT_ID
          required: true
          description: "SecondMe OAuth Client ID（Edge Function使用）"
        - name: SECONDME_CLIENT_SECRET
          required: true
          description: "SecondMe OAuth Client Secret（Edge Function使用，⚠️严格保密）"
        - name: SECONDME_REDIRECT_URI
          required: true
          description: "OAuth回调地址（Edge Function使用）"
        - name: ALLOWED_ORIGINS
          required: false
          description: "允许的CORS来源，多个用逗号分隔（默认为前端域名）"
    network:
      - host: api.mindverse.com
        purpose: "SecondMe OAuth2和API服务"
      - host: go.second-me.cn
        purpose: "SecondMe授权页面"
user-invocable: true
disable-model-invocation: false
---

# SecondMe Connect - 数字分身集成器

> **让百度秒哒应用轻松接入SecondMe生态，一键实现OAuth2登录和API调用**

**快速集成** | **开箱即用** | **安全可靠** | **完整文档**

---

## 🎯 一句话介绍

专为百度秒哒应用打造的SecondMe OAuth2登录和API集成工具，30分钟完成接入，无需OAuth2专业知识。

---

## ⚠️ 安全要求（部署前必读）

### 🔐 高权限密钥保护

**SUPABASE_SERVICE_ROLE_KEY**:
- ⚠️ **极高权限** - 可完全控制Supabase项目
- ✅ 仅配置在Edge Function环境变量
- ❌ 绝不提交到代码仓库
- ❌ 绝不在前端使用
- ❌ 绝不暴露给用户

**SECONDME_CLIENT_SECRET**:
- ✅ 仅在Edge Function中使用
- ❌ 绝不在前端配置

### 🎫 Access Token 存储与访问

**存储方式**:
- SecondMe access_token 存储在数据库 `profiles.secondme_access_token` 字段
- 通过 RLS 策略保护：用户只能访问自己的 token

**前端访问说明**:
- ✅ **允许**：已认证用户可以读取自己的 access_token（通过 RLS 策略保护）
- ✅ **用途**：前端需要 access_token 来调用 SecondMe API（聊天、记忆等）
- ⚠️ **安全风险**：如果 RLS 配置错误，可能导致 token 泄露

**RLS 策略**:
```sql
-- 用户只能访问自己的 profile（包括 access_token）
CREATE POLICY "Users can view own profile"
  ON profiles FOR SELECT USING (auth.uid() = id);
```

**安全建议**:
1. 部署后测试 RLS 策略是否正确
2. 使用 Supabase SQL Editor 验证：尝试以不同用户身份查询 profiles 表
3. 定期轮换 access_token（如果 SecondMe 支持刷新）

### 🌐 CORS安全配置

**必须配置ALLOWED_ORIGINS**:
```bash
# ✅ 正确：只允许您的域名
supabase secrets set ALLOWED_ORIGINS="https://yourdomain.com,https://www.yourdomain.com"

# ❌ 错误：允许任何网站调用（不安全）
# 不配置ALLOWED_ORIGINS或配置为'*'
```

**安全风险**:
- 未配置时：Edge Function拒绝跨域请求
- 配置为'*'：任何网站都可调用
- 正确配置：只允许您的域名

---

## 🎯 适用场景

- ✅ 百度秒哒生成的应用需要接入SecondMe登录
- ✅ 需要调用SecondMe API（聊天、记忆、广场等）
- ✅ React + TypeScript + Vite + Supabase技术栈
- ✅ 前后端分离架构

---

## 📦 包含内容

### 1. OAuth2 登录功能
- 完整的授权码流程实现
- CSRF防护（state参数验证）
- 用户信息同步
- Session管理

### 2. SecondMe API 封装
- 用户信息API
- 流式聊天API
- 记忆搜索API
- 笔记添加API
- 广场浏览API
- 语音合成API

### 3. 完整代码模板
- Edge Function代码
- 前端React组件
- 数据库脚本
- API调用工具类

---

## 🚀 快速集成（3步完成）

### 步骤 1: 安装依赖

```bash
npm install @supabase/supabase-js react-router-dom
```

### 步骤 2: 配置环境变量

**前端 `.env`**:
```env
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key
VITE_SECONDME_CLIENT_ID=your-client-id
VITE_SECONDME_REDIRECT_URI=https://yourdomain.com/auth/callback
```

**Edge Function 环境变量**:
```bash
# 必需环境变量
supabase secrets set SUPABASE_URL=https://your-project.supabase.co
supabase secrets set SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
supabase secrets set SECONDME_CLIENT_ID=your-client-id
supabase secrets set SECONDME_CLIENT_SECRET=your-client-secret
supabase secrets set SECONDME_REDIRECT_URI=https://yourdomain.com/auth/callback

# ⚠️ 重要：配置CORS允许的域名
supabase secrets set ALLOWED_ORIGINS="https://yourdomain.com"
```

### 步骤 3: 部署

```bash
# 1. 创建数据库表
# 在Supabase SQL Editor执行 templates/database/profiles.sql

# 2. 部署Edge Function
supabase functions deploy secondme-oauth-callback

# 3. 复制前端代码到项目
cp -r templates/src/* your-project/src/

# 4. 启动项目
npm run dev
```

---

## 📁 项目结构

```
templates/
├── database/
│   └── profiles.sql              # 数据库初始化脚本
├── supabase/
│   └── functions/
│       └── secondme-oauth-callback/
│           └── index.ts          # Edge Function主文件
├── src/
│   ├── lib/
│   │   ├── supabase.ts           # Supabase客户端
│   │   └── secondme-api.ts       # SecondMe API封装
│   ├── hooks/
│   │   └── useSecondMe.ts        # React Hook
│   ├── components/
│   │   ├── LoginButton.tsx       # 登录按钮
│   │   └── LoginButton.css
│   ├── pages/
│   │   ├── HomePage.tsx          # 首页
│   │   ├── AuthCallbackPage.tsx  # OAuth回调页
│   │   └── *.css
│   └── App.tsx                   # 路由配置
├── .env.template                 # 环境变量模板
└── INTEGRATION.md                # 百度秒哒集成指南
```

---

## 🔑 核心功能

### 1. 一键登录

```typescript
import { LoginButton } from './components/LoginButton';

<LoginButton>使用 SecondMe 登录</LoginButton>
```

### 2. 使用React Hook

```typescript
import { useSecondMe } from './hooks/useSecondMe';

function YourComponent() {
  const { 
    isLoggedIn,    // 是否已登录
    profile,       // 用户信息
    login,         // 登录函数
    logout,        // 登出函数
    chat,          // 聊天API
    searchMemory,  // 搜索记忆API
    addNote,       // 添加笔记API
  } = useSecondMe();

  // 使用API
  const response = await chat('你好');
  const memories = await searchMemory('Python');
  await addNote('重要笔记');
}
```

### 3. 直接使用API类

```typescript
import { SecondMeAPI, createSecondMeAPI } from './lib/secondme-api';

const api = await createSecondMeAPI();

// 获取用户信息
const user = await api.getUserInfo();

// 流式聊天
for await (const chunk of api.chat('你好')) {
  console.log(chunk.content);
}

// 搜索记忆
const memories = await api.searchMemory('关键词');
```

---

## 🔐 OAuth2 流程图

```
前端 → 点击登录
  ↓
跳转SecondMe授权页
  ↓
用户授权 → 回调
  ↓
Edge Function处理（服务端）:
  - 验证state
  - code换token（使用client_secret）
  - 获取用户信息
  - 创建Supabase用户
  - token安全存储到数据库
  - 返回hashed_token（不返回access_token）
  ↓
前端换取Session
  ↓
登录成功 → 可调用SecondMe API
```

---

## ⚠️ 重要注意事项

### 1. redirect_uri 三处必须完全一致

- 前端 `.env`
- SecondMe 后台配置
- Edge Function 环境变量

### 2. Client Secret 严格保密

- ✅ 仅存在于 Edge Function 环境变量
- ❌ 绝不出现在前端代码或 `.env` 文件

### 3. SecondMe API 响应格式

所有API响应都是：
```json
{
  "code": 0,
  "data": { /* 实际数据 */ }
}
```

**必须取 `.data` 字段！**

---

## 📚 API 文档

### 可用API列表

| API | 功能 | 所需Scope |
|-----|------|-----------|
| `getUserInfo()` | 获取用户信息 | userinfo |
| `chat(message)` | 流式聊天 | chat.write |
| `searchMemory(query)` | 搜索记忆 | memory.read |
| `addNote(content)` | 添加笔记 | note.write |
| `getPlazaFeed()` | 浏览广场 | plaza.read |
| `createPost(content)` | 发布帖子 | plaza.write |
| `textToSpeech(text)` | 语音合成 | voice |

---

## 🐛 故障排查

### Q: 点击登录报错 "redirect_uri_mismatch"

**A**: 检查三处redirect_uri是否完全一致

### Q: 回调后报错 "获取访问令牌失败"

**A**: 确认Edge Function使用 `application/x-www-form-urlencoded` 格式

### Q: 登录成功但无法调用API

**A**: 检查profile表中的secondme_access_token是否正确存储

### Q: 手机号用户无法登录

**A**: Edge Function已自动处理，生成虚拟邮箱

### Q: CORS错误

**A**: 确保配置了ALLOWED_ORIGINS环境变量

---

## 📞 技术支持

如有问题：
1. 查看 `templates/INTEGRATION.md` 详细说明
2. 检查浏览器控制台错误
3. 查看Edge Function日志：`supabase functions logs secondme-oauth-callback`

---

## 🔄 更新日志

**v1.2.0** (2026-04-08)
- 🐛 **修复**: Edge Function hashedToken 未定义错误（运行时错误）
- 🔒 **安全**: 改进 CORS 逻辑，拒绝未授权的来源
- 📝 **文档**: 明确说明 access_token 的存储和访问方式
- 📝 **文档**: 更新 RLS 策略说明和安全验证步骤
- ✅ 响应 ClawHub 安全审查第二轮

**v1.1.0** (2026-04-08)
- 🔒 **安全加固**: 修复CORS安全配置
- 🔒 **安全加固**: 不再返回明文access_token
- 📝 完善环境变量声明
- 📝 添加详细安全文档

**v1.0.0** (2026-04-07)
- ✅ 完整OAuth2登录流程
- ✅ SecondMe API封装
- ✅ 百度秒哒集成指南
- ✅ 完整代码模板

---

**让百度秒哒应用轻松接入SecondMe生态！** 🔐
