# VisNote Image Creator

一个自动化的图片生成工具，专为小红书等社交媒体平台设计。通过智能模板选择快速生成高质量的配图。

> 官网：https://vis-note.netlify.app/

## 特性

- 🎨 **丰富的模板库** - 支持多种风格：封面、正文、对比、步骤等
- 🔑 **智能验证** - 自动检查 API Key、会员状态、额度等
- 📸 **自定义图片** - 支持上传本地图片作为素材
- 🎯 **智能匹配** - 根据内容类型自动选择最合适的模板

## 快速开始

### 1. 前置要求

- Node.js (推荐 v18+)
- Playwright 浏览器驱动

### 2. 安装依赖

```bash
npm install playwright
npx playwright install chromium
```

### 3. 配置 API Key

在项目根目录创建 `config.json` 文件：

```json
{
  "apikey": "your_api_key_here"
}
```

**获取 API Key：**
1. 访问 VisNote 个人主页：https://vis-note.netlify.app/profile
2. 复制已生成的 API Key
3. 将其粘贴到 `config.json` 中

### 4. 基本使用

```bash
# 自定义内容
node scripts/generate-image.mjs --template yellow \
  --data '{"title":"我的标题","subtitle":"副标题","color":"#EAB308"}' \
  --out ./output.png

# 上传自定义图片
node scripts/generate-image.mjs \
  --template magazine \
  --data '{"title":"封面标题","image":"/path/to/image.jpg"}' \
  --out ./cover.png
```

## 命令参数

| 参数 | 必填 | 说明 | 示例 |
|------|------|------|------|
| `--template` | ✅ | 模板 ID | `--template yellow` |
| `--data` | ❌ | JSON 格式的数据（覆盖模板默认值） | `--data '{"title":"标题"}'` |
| `--out` | ❌ | 输出路径（默认 `./output.png`） | `--out ./my-image.png` |

## 模板 API

### 获取所有模板

```bash
curl "https://vis-note.netlify.app/api/open/templates"
```

### 搜索模板

```bash
# 搜索封面模板
curl "https://vis-note.netlify.app/api/open/templates?keyword=封面"

# 搜索正文模板
curl "https://vis-note.netlify.app/api/open/templates?keyword=正文"
```

### 响应示例

```json
{
  "success": true,
  "data": [
    {
      "id": "yellow",
      "name": "高对比大字报",
      "desc": "适合：避坑/干货/教程",
      "tags": ["封面"],
      "value": {
        "title": "示例标题",
        "subtitle": "示例副标题",
        "tag": "标签",
        "color": "#EAB308"
      }
    }
  ]
}
```

## API Key 验证

在生成图片前，脚本会自动验证 API Key 的以下状态：

1. **API Key 存在性** - 检查 API Key 是否存在系统中
2. **会员状态** - 检查用户是否为 VIP 会员
3. **会员有效期** - 检查会员是否过期
4. **可用额度** - 检查是否有剩余生图额度

### 验证错误处理

| 错误信息 | 说明 | 解决方案 |
|---------|------|---------|
| `API Key 不存在` | API Key 未注册 | 检查 config.json 或获取新 key |
| `您还不是会员` | 用户不是 VIP 会员 | 订阅 VIP 会员 |
| `您的会员已过期` | 会员已过期 | 续费会员 |
| `生图额度已用完` | 额度已用尽 | 购买额外额度 |

## 常用模板示例

### 高对比封面（yellow）

```bash
node scripts/generate-image.mjs \
  --template yellow \
  --data '{"title":"爆款标题","subtitle":"副标题","tag":"干货分享","color":"#EAB308"}' \
  --out ./cover.png
```

### 极简杂志风（magazine）

```bash
node scripts/generate-image.mjs \
  --template magazine \
  --data '{"title":"OOTD穿搭","subtitle":"日常分享","tag":"穿搭分享","image":"/path/to/photo.jpg"}' \
  --out ./ootd.png
```

### 对比图（classic-before-after）

```bash
node scripts/generate-image.mjs \
  --template classic-before-after \
  --data '{"title":"改造对比","subtitle":"前后对比","image":"/path/to/before.jpg","image2":"/path/to/after.jpg"}' \
  --out ./comparison.png
```

### 步骤教程（double-row-step）

```bash
node scripts/generate-image.mjs \
  --template double-row-step \
  --data '{"title":"使用教程","bodyText":"步骤1\\n步骤2","step":"01/05"}' \
  --out ./tutorial.png
```

## 故障排除

### 图片生成失败

1. **检查 API Key 配置**
   ```bash
   cat config.json
   ```

2. **验证 API Key 有效性**
   ```bash
   curl -H "Authorization: Bearer YOUR_API_KEY" \
     "https://vis-note.netlify.app/api/open/check"
   ```

3. **检查会员和额度**
   - 登录 VisNote 个人主页查看会员状态
   - 检查剩余生图额度

### Playwright 相关问题

```bash
# 重新安装 Playwright 浏览器
npx playwright install chromium

# 清理 Playwright 缓存
npx playwright install --force chromium
```

### 模板不存在

调用 API 查看可用模板：
```bash
curl "https://vis-note.netlify.app/api/open/templates"
```

## 项目结构

```
visnote-image-creator/
├── config.json              # API Key 配置文件（不提交到 Git）
├── example-config.json      # 配置文件示例
├── scripts/
│   └── generate-image.mjs   # 图片生成脚本
├── SKILL.md                 # AI Skill 文档
└── README.md                # 项目说明（本文件）
```

## 注意事项

- ⚠️ `config.json` 包含敏感信息，已添加到 `.gitignore`，不会被提交到版本控制
- 💡 生图会消耗额度，请合理使用
- 🔄 如批量生成建议间隔 10-15 秒，避免服务器超时
- 📝 模板数据结构可能随时更新，建议使用 API 获取最新信息

## 相关链接

- VisNote 官网：https://vis-note.netlify.app
- 个人主页（获取 API Key）：https://vis-note.netlify.app/profile
- 模板 API：`{server}/api/open/templates`
- 状态检查 API：`{server}/api/open/check`
