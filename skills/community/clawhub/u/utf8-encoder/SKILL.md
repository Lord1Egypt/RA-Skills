---
name: UTF-8发布基础设施
description: 自动处理多平台中文编码问题的发布基础设施，集成防卡顿策略，支持Discord、GitHub等平台，遵循'防止勤务干扰'原则。
read_when:
  - 在多平台发布内容时遇到编码问题
  - 需要自动化处理发布流程中的编码转换
  - 希望集成韧性发布机制（重试+备选方案）
  - 需要将编码处理作为基础设施而非手动任务
metadata: {"clawdbot":{"emoji":"🏛️","requires":{"bins":["node","npm"]}}}
allowed-tools: Bash(utf8-encoder:*)
---

# UTF-8发布基础设施 (UTF-8 Publishing Infrastructure)

## 概述

**核心定位**：不是手动调用的编码工具，而是**自动运行的发布流程基础设施**。遵循Gemini专业评审建议：作为"底层律令"，防止"勤务干扰"，整合验证机制。

**解决的核心问题**：PowerShell控制台使用GB2312编码显示UTF-8内容，导致控制台输出乱码，误导开发者认为发布失败。实际HTTP数据正确，但显示误导导致重复发布浪费API token。

**Gemini评审核心洞察**：
- 🏛️ **作为"底层律令"**：不应把编码转换当作需要思考的任务，应设为强制性后处理器
- 🚫 **防止"勤务干扰"**：禁止将编码转换作为工作成果汇报，处理完后直接汇报主线任务进度  
- 🔄 **整合验证机制**：与三次尝试法则结合，形成完整的韧性系统

**基础设施特性**：
- ✅ **自动运行**：集成到I/O过滤层，无需手动调用
- ✅ **韧性保障**：内置防卡顿策略，失败时智能切换方案
- ✅ **智能检测**：自动判断是否需要编码处理，提供详细原因
- ✅ **中间件模式**：提供系统级集成接口，易嵌入工作流

**已验证的平台**：
- ✅ Discord Webhook（带重试和备选方案）
- ✅ GitHub Gist & Issues（带韧性保障）
- ✅ 本地文件读写（自动编码处理）
- 🔄 Reddit API（架构支持，待验证）

## 安装

### 方式一：npm全局安装（推荐）
```bash
npm install -g utf8-encoder-tool
```

### 方式二：本地项目使用
```bash
npm install utf8-encoder-tool
# 或
yarn add utf8-encoder-tool
```

### 方式三：直接使用源码
```bash
git clone https://github.com/mrpulorx2025-source/utf8-encoder-skill
cd utf8-encoder-skill
npm install
```

## 核心功能

### 🏛️ 基础设施模式（推荐）

#### 1.1 作为基础设施集成
```javascript
// 导入基础设施类
const { UTF8Infrastructure } = require('utf8-encoder-tool');
const infrastructure = new UTF8Infrastructure();

// 自动集成中间件，无需手动处理编码
const middleware = infrastructure.integrateAsMiddleware();

// 智能检测是否需要编码处理
const check = infrastructure.shouldProcess("中文测试内容");
if (check.needsProcessing) {
  console.debug('🔄 基础设施自动处理编码问题');
  console.debug(`检测原因: ${check.reasons.join(', ')}`);
  // 遵循"防止勤务干扰"原则：不汇报编码处理细节，直接推进主线任务
}

// 带重试的发送（整合三次尝试法则）
const result = await middleware.sendToDiscordWithRetry(
  process.env.DISCORD_WEBHOOK,
  '消息内容',
  { username: 'UTF8-Infrastructure' }
);

// 批量发布到多个平台
const platforms = [
  {
    type: 'discord',
    url: process.env.DISCORD_WEBHOOK,
    options: { username: 'UTF8-Bot' }
  },
  {
    type: 'github',
    token: process.env.GITHUB_TOKEN,
    filename: 'content.md',
    description: '基础设施发布',
    isPublic: false
  }
];

const results = await middleware.publishToMultiplePlatforms(platforms, '发布内容');
console.log(`发布结果: ${results.filter(r => r.success).length}/${results.length} 成功`);
```

#### 1.2 基础设施特性
- **智能检测**：自动判断是否需要编码处理，提供详细原因（乱码、中文、Emoji等）
- **韧性保障**：内置三次尝试法则，同一方法失败2次即切换方案，支持指数退避重试
- **中间件模式**：提供`integrateAsMiddleware()`系统级集成，支持批量发布
- **防卡顿策略**：集成防卡顿四层策略框架，自动处理发布过程中的阻塞问题
- **备选方案**：支持添加备选发布方案，主方案失败时自动切换
- **状态监控**：提供`getInfrastructureStatus()`实时监控基础设施状态
- **自动恢复**：失败时自动备份内容到本地，防止数据丢失

### 🛠️ 传统工具模式（向后兼容）

#### 2.1 确保UTF-8编码
```javascript
const { UTF8Encoder } = require('utf8-encoder-tool');
const encoder = new UTF8Encoder();

const text = "中文测试 Chinese Test 🎯";
const utf8Text = encoder.ensureUTF8(text);
// 确保文本是有效的UTF-8编码
```

### 2. 计算UTF-8字节长度
```javascript
const byteLength = encoder.calculateUTF8ByteLength(text);
console.log(`字符数: ${text.length}, UTF-8字节数: ${byteLength}`);
// 用于设置HTTP请求的Content-Length头
```

### 3. 读取UTF-8文件
```javascript
const content = encoder.readFileUTF8('./chinese-content.md');
console.log(`文件内容: ${content.substring(0, 100)}...`);
// 自动验证中文字符，统计数量
```

### 4. 创建UTF-8 JSON载荷
```javascript
const payload = encoder.createUTF8JSONPayload({
  message: "中文内容",
  timestamp: new Date().toISOString(),
  author: "丞相"
}, true); // true表示美化输出
```

### 5. 发送到Discord（Webhook）
```javascript
const result = await encoder.sendToDiscord(
  'https://discord.com/api/webhooks/...',
  'Discord消息：中文测试 🎯',
  {
    username: 'UTF8-Bot',
    avatar_url: 'https://example.com/avatar.png'
  }
);

console.log(result.success ? '✅ 发送成功' : '❌ 发送失败');
```

### 6. 创建GitHub Gist
```javascript
const result = await encoder.createGitHubGist(
  'ghp_your_token_here',
  '# GitHub Gist测试\n\n中文内容正常显示测试。',
  'test.md',
  'UTF-8编码测试Gist',
  true // 公开
);

if (result.gistUrl) {
  console.log(`Gist已创建: ${result.gistUrl}`);
}
```

### 7. 乱码检测
```javascript
const validation = encoder.validateNoGarbledChars(text);
if (validation.valid) {
  console.log('✅ 文本无乱码字符');
} else {
  console.log(`❌ 发现${validation.garbledCount}个乱码字符`);
  console.log('乱码字符:', validation.garbledChars);
}
```

## 实战示例

### 示例1：发布调研到多个平台
```javascript
const UTF8Encoder = require('utf8-encoder-tool');
const encoder = new UTF8Encoder();
const fs = require('fs');

async function publishResearch() {
  // 1. 读取调研内容
  const researchContent = encoder.readFileUTF8('./research.md');
  
  // 2. 验证内容
  const validation = encoder.validateNoGarbledChars(researchContent);
  if (!validation.valid) {
    throw new Error(`调研内容包含乱码: ${validation.garbledChars.join(', ')}`);
  }
  
  // 3. 发送到Discord（拆分长消息）
  const discordResult = await encoder.sendToDiscord(
    process.env.DISCORD_WEBHOOK,
    researchContent.substring(0, 1900) // Discord消息限制
  );
  
  // 4. 创建GitHub Gist
  const gistResult = await encoder.createGitHubGist(
    process.env.GITHUB_TOKEN,
    researchContent,
    'research.md',
    '用户调研 - UTF-8测试',
    true
  );
  
  // 5. 生成报告
  const report = encoder.generateTestReport([discordResult, gistResult]);
  fs.writeFileSync('./publish-report.md', report, 'utf8');
  
  console.log('🎉 调研发布完成！');
}

publishResearch().catch(console.error);
```

### 示例2：PowerShell中调用Node.js模块
```powershell
# PowerShell脚本：通过Node.js确保UTF-8编码
$nodeScript = @'
const UTF8Encoder = require('utf8-encoder-tool');
const encoder = new UTF8Encoder();

const text = process.argv[2];
const utf8Text = encoder.ensureUTF8(text);
console.log(utf8Text);
'@

# 保存临时脚本
$nodeScript | Out-File -FilePath "temp-utf8.js" -Encoding UTF8

# 执行并获取结果
$inputText = "PowerShell中的中文测试"
$result = node temp-utf8.js "$inputText"
Write-Host "UTF-8编码结果: $result"

# 清理
Remove-Item "temp-utf8.js"
```

### 示例3：API服务器中间件
```javascript
// Express.js中间件：确保请求体UTF-8编码
const UTF8Encoder = require('utf8-encoder-tool');
const encoder = new UTF8Encoder();

function utf8Middleware(req, res, next) {
  // 确保请求体文本是UTF-8编码
  if (req.body && typeof req.body.text === 'string') {
    req.body.text = encoder.ensureUTF8(req.body.text);
    
    // 验证无乱码
    const validation = encoder.validateNoGarbledChars(req.body.text);
    if (!validation.valid) {
      return res.status(400).json({
        error: '请求包含乱码字符',
        garbledChars: validation.garbledChars
      });
    }
  }
  
  // 设置响应头
  res.setHeader('Content-Type', 'application/json; charset=utf-8');
  next();
}

// 使用中间件
app.use(express.json());
app.use(utf8Middleware);
```

## 技术原理

### 问题根源
1. **PowerShell编码问题**：PowerShell控制台默认使用系统活动代码页（如GB2312）显示文本
2. **编码不一致**：控制台显示编码 ≠ HTTP传输编码 ≠ 文件保存编码
3. **验证缺失**：依赖控制台输出判断，未独立验证实际网页显示

### 解决方案
1. **统一使用Node.js**：Node.js默认使用UTF-8编码，端到端一致性
2. **显式指定编码**：所有文件操作、Buffer转换都明确使用`'utf8'`
3. **独立验证**：通过web_fetch或实际访问验证网页显示
4. **字节长度计算**：使用`Buffer.byteLength(text, 'utf8')`而非`text.length`

### 核心代码片段
```javascript
// 关键：Buffer.byteLength计算UTF-8字节长度
const postData = JSON.stringify(payload);
const contentLength = Buffer.byteLength(postData, 'utf8');

// 关键：设置正确的Content-Type头
headers['Content-Type'] = 'application/json; charset=utf-8';
headers['Content-Length'] = contentLength;
```

## 常见问题与解决

### Q1：为什么控制台显示乱码但网页正常？
**A**：控制台使用GB2312编码显示UTF-8内容。解决方案：不依赖控制台输出，通过`web_fetch`工具验证实际网页显示。

### Q2：如何验证编码是否正确？
**A**：使用`encoder.validateNoGarbledChars(text)`检测乱码字符，或直接访问生成的Gist/Issue查看实际显示。

### Q3：支持哪些特殊字符？
**A**：支持中文、日文、韩文、Emoji、特殊符号。使用正则表达式`/[\u4e00-\u9fa5]/`检测中文字符。

### Q4：与平台原生API有什么区别？
**A**：平台API可能不处理编码问题。本工具确保：
1. 请求体正确UTF-8编码
2. Content-Length头准确
3. Content-Type包含charset=utf-8
4. 响应体正确解码

### Q5：性能影响大吗？
**A**：极小。主要开销是`Buffer.byteLength`计算，对于普通文本（<10KB）可忽略不计。

## 最佳实践

### 开发阶段
1. **先验证后发布**：创建测试Gist/Issue验证编码，确认无误后再正式发布
2. **使用环境变量**：将API Token、Webhook URL存储在环境变量中
3. **记录验证日志**：保存每次发布的验证结果，便于排查问题

### 生产环境
1. **错误处理**：所有API调用都要有try-catch和重试机制
2. **速率限制**：遵守平台API速率限制，添加适当的延迟
3. **监控告警**：监控发布成功率，失败时发送告警

### 测试策略
1. **单元测试**：测试`ensureUTF8`、`calculateUTF8ByteLength`等核心函数
2. **集成测试**：使用测试Webhook和测试Token进行真实API测试
3. **回归测试**：每次更新后验证所有平台兼容性

## 平台扩展指南

### 添加新平台支持
1. 在`UTF8Encoder`类中添加新方法（如`sendToReddit`）
2. 实现平台特定的参数处理和错误处理
3. 添加平台测试用例
4. 更新文档和示例

### Reddit API示例框架
```javascript
async sendToReddit(token, subreddit, title, content, options = {}) {
  const payload = {
    title: this.ensureUTF8(title),
    text: this.ensureUTF8(content),
    sr: subreddit,
    kind: 'self',
    ...options
  };
  
  // Reddit API特定的头和处理逻辑
  // ...
}
```

## 更新日志

### v1.0.0 (2026-03-15)
- ✅ 核心UTF-8编码保障功能
- ✅ Discord Webhook支持
- ✅ GitHub Gist & Issues支持  
- ✅ 乱码检测与验证
- ✅ 字节长度计算
- ✅ 完整文档和示例

### 计划功能
- 🔄 Reddit API支持
- 🔄 Telegram Bot支持
- 🔄 微信公众平台支持
- 🔄 编码转换工具（GB2312 ↔ UTF-8）
- 🔄 批量处理工具

## 贡献与反馈

### 问题反馈
1. GitHub Issues: https://github.com/mrpulorx2025-source/utf8-encoder-skill/issues
2. 邮箱: mrpulorx2025@gmail.com

### 贡献指南
1. Fork仓库
2. 创建功能分支
3. 提交更改
4. 创建Pull Request

## 许可证
MIT License - 详见LICENSE文件

---

**核心教训**：编码问题反复消耗token实属不该。本工具通过一次性测试+验证+发布流程，避免重复浪费，提高发布成功率。

**丞相谨记**：控制台显示 ≠ 实际数据，必须独立验证网页显示！