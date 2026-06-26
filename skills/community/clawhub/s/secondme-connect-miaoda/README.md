# SecondMe Connect - 数字分身集成器

> **让百度秒哒应用轻松接入SecondMe生态**

## 🎯 名称

**英文名称**: SecondMe Connect  
**中文名称**: SecondMe 数字分身集成器  
**Emoji**: 🔐

---

## ⚠️ 安全警告（部署前必读）

### 高权限密钥保护

**SUPABASE_SERVICE_ROLE_KEY**:
- ⚠️ 极高权限，可完全控制Supabase项目
- ✅ 仅配置在Edge Function环境变量
- ❌ 绝不提交到代码仓库或前端

### Access Token 存储说明

**存储方式**:
- SecondMe access_token 存储在数据库 `profiles` 表
- 通过 RLS 策略保护：用户只能访问自己的 token

**前端访问**:
- ✅ 已认证用户可读取自己的 access_token（RLS 保护）
- ✅ 用于调用 SecondMe API（聊天、记忆等）
- ⚠️ 确保 RLS 策略正确配置

### CORS安全配置

**必须配置ALLOWED_ORIGINS**:
```bash
# ✅ 正确
supabase secrets set ALLOWED_ORIGINS="https://yourdomain.com"

# ❌ 错误（允许任何网站调用）
# 不配置或配置为'*'
```

---

## 📝 介绍

专为百度秒哒应用打造的SecondMe OAuth2登录和API集成工具，30分钟完成接入，无需OAuth2专业知识。

### 核心特性

- 🚀 **快速集成**: 3步完成，1小时内上线
- 💪 **功能完整**: 支持所有主要SecondMe API
- 🛡️ **安全可靠**: 符合OAuth2最佳实践
- 📖 **文档完善**: 详细指南和完整示例

---

## 🚀 快速开始

### 1. 安装依赖

```bash
npm install @supabase/supabase-js react-router-dom
```

### 2. 配置环境变量

**前端 `.env`**:
```env
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key
VITE_SECONDME_CLIENT_ID=your-client-id
VITE_SECONDME_REDIRECT_URI=https://yourdomain.com/auth/callback
```

**Edge Function 环境变量**:
```bash
# 必需
supabase secrets set SUPABASE_URL=https://your-project.supabase.co
supabase secrets set SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
supabase secrets set SECONDME_CLIENT_ID=your-client-id
supabase secrets set SECONDME_CLIENT_SECRET=your-client-secret
supabase secrets set SECONDME_REDIRECT_URI=https://yourdomain.com/auth/callback

# ⚠️ 重要：配置CORS
supabase secrets set ALLOWED_ORIGINS="https://yourdomain.com"
```

### 3. 部署Edge Function

```bash
supabase functions deploy secondme-oauth-callback
```

### 4. 复制模板文件

```bash
cp -r templates/src/* your-project/src/
```

---

## 💡 使用示例

### 一键登录
```tsx
import { LoginButton } from './components/LoginButton';

<LoginButton>使用 SecondMe 登录</LoginButton>
```

### 调用API
```tsx
import { useSecondMe } from './hooks/useSecondMe';

const { chat, searchMemory } = useSecondMe();

// 聊天
const response = await chat('你好');

// 搜索记忆
const memories = await searchMemory('Python');
```

---

## 📦 包含内容

- ✅ 完整OAuth2登录流程
- ✅ SecondMe API完整封装
- ✅ React组件和Hook
- ✅ 数据库脚本
- ✅ Edge Function代码
- ✅ 详细集成文档

---

## 📚 API列表

| API | 功能 |
|-----|------|
| `getUserInfo()` | 获取用户信息 |
| `chat(message)` | 流式聊天 |
| `searchMemory(query)` | 搜索记忆 |
| `addNote(content)` | 添加笔记 |
| `getPlazaFeed()` | 浏览广场 |
| `createPost(content)` | 发布帖子 |
| `textToSpeech(text)` | 语音合成 |

---

## ⚠️ 重要提示

1. redirect_uri必须三处一致
2. Client Secret仅在后端
3. 配置ALLOWED_ORIGINS确保CORS安全
4. SUPABASE_SERVICE_ROLE_KEY严格保密

---

## 📖 详细文档

查看 `SKILL.md` 获取完整说明。  
查看 `templates/INTEGRATION.md` 获取百度秒哒集成指南。

---

## 🏷️ 标签

`secondme` `oauth2` `authentication` `api-integration` `react` `typescript` `supabase` `百度秒哒` `数字分身`

---

**Connect to SecondMe. Connect to the Future.**

## License

MIT
