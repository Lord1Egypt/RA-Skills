# 百度秒哒集成指南

本文档指导您如何在百度秒哒生成的应用中集成SecondMe OAuth2登录和API调用功能。

## ⚠️ 重要安全说明

### Access Token 存储与访问

**存储方式**:
- SecondMe `access_token` 存储在数据库 `profiles.secondme_access_token` 字段
- 通过 RLS（行级安全）策略保护：用户只能访问自己的 token

**前端访问**:
- ✅ 已认证用户可以读取自己的 `access_token`（通过 RLS 保护）
- ✅ 用于调用 SecondMe API（聊天、记忆搜索等）
- ⚠️ **安全风险**：如果 RLS 策略配置错误，可能导致 token 泄露

**验证 RLS 策略**:
```sql
-- 在 Supabase SQL Editor 中测试
-- 以不同用户身份登录后执行：
SELECT * FROM profiles;
-- 应该只返回当前用户自己的数据
```

### 高权限密钥保护

**SUPABASE_SERVICE_ROLE_KEY** 和 **SECONDME_CLIENT_SECRET**:
- ⚠️ 极高权限，仅在 Edge Function 中使用
- ❌ 绝不提交到代码仓库或在前端使用
- ✅ 仅通过 `supabase secrets set` 配置

---

## 前提条件

1. 已创建百度秒哒应用（React + TypeScript + Vite）
2. 已创建Supabase项目
3. 已在SecondMe开发者后台创建OAuth应用

## 集成步骤

### 1. 安装依赖

```bash
cd your-miaoda-app
npm install @supabase/supabase-js react-router-dom
```

### 2. 复制Skill文件

将Skill中的模板文件复制到您的项目：

```bash
# 复制核心库
cp -r templates/src/lib/* src/lib/
cp -r templates/src/hooks src/hooks/

# 复制组件
cp -r templates/src/components src/components/

# 复制页面（如需自定义可选择性复制）
cp -r templates/src/pages src/pages/
```

### 3. 配置环境变量

创建 `.env` 文件：

```env
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key
VITE_SECONDME_CLIENT_ID=your-client-id
VITE_SECONDME_REDIRECT_URI=https://yourdomain.com/auth/callback
```

### 4. 创建数据库表

在Supabase SQL Editor执行：

```sql
CREATE TABLE profiles (
  id uuid PRIMARY KEY REFERENCES auth.users(id),
  email text UNIQUE NOT NULL,
  name text,
  avatar_url text,
  secondme_access_token text,
  secondme_refresh_token text,
  created_at timestamptz DEFAULT now()
);

ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own profile"
  ON profiles FOR SELECT USING (auth.uid() = id);
```

### 5. 部署Edge Function

```bash
# 1. 创建Edge Function目录
mkdir -p supabase/functions/secondme-oauth-callback

# 2. 复制Edge Function代码
cp templates/supabase/functions/secondme-oauth-callback/index.ts \
   supabase/functions/secondme-oauth-callback/

# 3. 部署
supabase functions deploy secondme-oauth-callback

# 4. 配置环境变量
supabase secrets set SECONDME_CLIENT_ID=your-client-id
supabase secrets set SECONDME_CLIENT_SECRET=your-client-secret
supabase secrets set SECONDME_REDIRECT_URI=https://yourdomain.com/auth/callback
```

### 6. 配置路由

在 `src/App.tsx` 中添加回调路由：

```typescript
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { AuthCallbackPage } from './pages/AuthCallbackPage';
// ...其他导入

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* 您的现有路由 */}
        <Route path="/" element={<YourHomePage />} />
        
        {/* 添加SecondMe回调路由 */}
        <Route path="/auth/callback" element={<AuthCallbackPage />} />
      </Routes>
    </BrowserRouter>
  );
}
```

### 7. 添加登录按钮

在需要登录的页面：

```typescript
import { LoginButton } from './components/LoginButton';

function YourPage() {
  return (
    <div>
      <h1>欢迎</h1>
      <LoginButton>使用 SecondMe 登录</LoginButton>
    </div>
  );
}
```

### 8. 使用SecondMe API

#### 方式一：使用React Hook（推荐）

```typescript
import { useSecondMe } from './hooks/useSecondMe';

function YourComponent() {
  const { 
    isLoggedIn, 
    profile, 
    chat, 
    searchMemory, 
    addNote 
  } = useSecondMe();

  const handleChat = async () => {
    const response = await chat('你好');
    console.log(response);
  };

  if (!isLoggedIn) {
    return <LoginButton />;
  }

  return (
    <div>
      <h2>欢迎, {profile?.name}</h2>
      <button onClick={handleChat}>聊天</button>
    </div>
  );
}
```

#### 方式二：直接使用API类

```typescript
import { SecondMeAPI, createSecondMeAPI } from './lib/secondme-api';

async function yourFunction() {
  const api = await createSecondMeAPI();
  if (!api) {
    // 用户未登录
    return;
  }

  // 获取用户信息
  const user = await api.getUserInfo();
  
  // 流式聊天
  for await (const chunk of api.chat('你好')) {
    console.log(chunk.content);
  }
  
  // 搜索记忆
  const memories = await api.searchMemory('Python');
  
  // 添加笔记
  await api.addNote('这是我的笔记');
}
```

## 完整示例

### 示例1：聊天页面

```typescript
import { useState } from 'react';
import { useSecondMe } from './hooks/useSecondMe';

function ChatPage() {
  const { chat } = useSecondMe();
  const [message, setMessage] = useState('');
  const [response, setResponse] = useState('');

  const handleSend = async () => {
    if (!message.trim()) return;
    
    const reply = await chat(message);
    setResponse(reply);
    setMessage('');
  };

  return (
    <div>
      <input 
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="输入消息..."
      />
      <button onClick={handleSend}>发送</button>
      
      {response && <div>回复: {response}</div>}
    </div>
  );
}
```

### 示例2：记忆搜索

```typescript
import { useState } from 'react';
import { useSecondMe } from './hooks/useSecondMe';

function MemorySearch() {
  const { searchMemory } = useSecondMe();
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);

  const handleSearch = async () => {
    const memories = await searchMemory(query);
    setResults(memories);
  };

  return (
    <div>
      <input 
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="搜索记忆..."
      />
      <button onClick={handleSearch}>搜索</button>
      
      <ul>
        {results.map((m, i) => (
          <li key={i}>{m.content}</li>
        ))}
      </ul>
    </div>
  );
}
```

## 常见问题

### Q: 如何在多个页面共享登录状态？

A: 使用 `useSecondMe` Hook，它会自动处理Session管理。

### Q: 如何保护需要登录才能访问的页面？

A: 创建一个保护组件：

```typescript
import { useSecondMe } from './hooks/useSecondMe';
import { LoginButton } from './components/LoginButton';

function RequireAuth({ children }) {
  const { isLoggedIn, loading } = useSecondMe();

  if (loading) return <div>加载中...</div>;
  if (!isLoggedIn) return <LoginButton />;

  return children;
}

// 使用
<RequireAuth>
  <YourProtectedPage />
</RequireAuth>
```

### Q: 如何自定义登录按钮样式？

A: 传入className或children：

```typescript
<LoginButton className="my-custom-btn">
  🔐 使用 SecondMe 登录
</LoginButton>
```

## 下一步

- 查看 `templates/src/lib/secondme-api.ts` 了解所有可用API
- 查看 `templates/src/hooks/useSecondMe.ts` 了解Hook实现
- 参考 `templates/src/pages/HomePage.tsx` 查看完整示例

## 技术支持

如遇问题：
1. 检查环境变量配置
2. 确认redirect_uri三处一致
3. 查看浏览器控制台错误
4. 检查Edge Function日志

---

**让您的百度秒哒应用轻松接入SecondMe生态！**
