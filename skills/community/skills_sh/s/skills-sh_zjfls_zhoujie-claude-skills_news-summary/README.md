# 新闻搜索摘要 Skill

一个用于搜索最近3-5天内的新闻、生成HTML摘要页面并支持AI解读功能的Claude Code skill。

## 功能特性

- 🔍 **智能搜索**：搜索最近3-5天内的新闻内容
- 📊 **权威评估**：自动评估新闻来源的权威性（高/中/低）
- 🎨 **美观展示**：生成现代化、响应式的HTML页面
- 🤖 **AI解读**：点击按钮即可获取AI深度分析
- ⚡ **自动打开**：生成后自动在浏览器中打开
- 🕒 **时间标记**：清晰显示新闻发布时间和来源信息

## 目录结构

```
.claude/skills/news-summary/
├── skill.json          # Skill配置文件
├── index.md           # Skill入口点（提示词）
├── server.js          # AI解读后端服务器
├── lib/
│   └── html-generator.js  # HTML生成工具库
├── package.json       # Node.js项目配置
├── output/            # 生成的文件输出目录
│   ├── 2025-12-08_14-30-00_AI技术新闻/
│   │   ├── summary.html      # 新闻摘要HTML
│   │   ├── data.json         # 原始数据
│   │   └── analysis/         # AI解读文件
│   │       └── analysis_xxx.html
│   └── 2025-12-08_15-20-00_物理引擎/
│       ├── summary.html
│       ├── data.json
│       └── analysis/
└── README.md          # 使用说明文档
```

### 输出目录说明

每次查询会自动创建一个独立的目录，格式为：`{时间戳}_{查询主题}/`

例如：`2025-12-08_14-30-00_AI技术新闻/`

每个查询目录包含：
- `summary.html` - 新闻摘要HTML页面
- `data.json` - 原始JSON数据
- `analysis/` - 该次查询的所有AI解读文件

## 使用方法

### 1. 启动AI解读服务器

在使用skill之前，需要先启动AI解读服务器：

```bash
cd ~/.claude/skills/news-summary
node server.js
```

服务器将在 `http://localhost:3456` 上运行。

### 2. 使用Skill

在Claude Code中激活skill：

```bash
/skill news-summary
```

然后按照提示操作：

1. 输入你想搜索的新闻主题或关键词
2. 等待Claude搜索并分析新闻
3. 生成的HTML页面会自动在浏览器中打开
4. 点击任意新闻卡片上的"AI解读"按钮获取深度分析

## 工作流程

```
用户输入主题
    ↓
使用WebSearch搜索新闻
    ↓
分析新闻信息
    ↓
生成HTML摘要页面
    ↓
自动打开浏览器
    ↓
用户点击"AI解读"按钮
    ↓
发送请求到本地服务器
    ↓
生成AI解读HTML页面
    ↓
自动打开新页面
```

## 生成的HTML功能

### 新闻摘要页面

- **新闻卡片**：每条新闻以卡片形式展示
- **元信息**：显示来源、时间、权威性标签
- **操作按钮**：
  - "查看原文"：跳转到新闻原始链接
  - "AI解读"：生成AI深度分析

### AI解读页面

AI解读页面包含以下部分：

- 📋 **新闻摘要**：新闻内容概述
- 🔍 **背景分析**：事件的历史和背景信息
- 💡 **关键要点**：核心观点和主要影响
- 📊 **影响评估**：正面和负面影响分析
- 🔗 **相关延伸**：相关话题和深入思考

## 权威性评估标准

- **高（绿色）**：权威媒体、官方网站、知名新闻机构
- **中（黄色）**：一般媒体、行业网站、区域性媒体
- **低（灰色）**：个人博客、社交媒体、待验证来源

## 技术栈

- **Claude Code**：AI能力和自动化
- **Node.js**：后端服务器
- **HTML/CSS/JavaScript**：前端页面
- **HTTP**：本地服务器通信

## 配置说明

### 端口配置

默认端口：`3456`

如需修改端口，编辑 `server.js` 文件：

```javascript
const PORT = 3456; // 修改为你想要的端口
```

同时需要修改 `template.js` 中的端口：

```javascript
const response = await fetch('http://localhost:3456/analyze', {
    // 修改为相同的端口
```

### 输出目录

默认输出目录：`~/.claude/skills/news-summary/output/`

如需修改，编辑 `server.js` 中的 `OUTPUT_DIR` 常量。

## 注意事项

1. **服务器运行**：使用AI解读功能前，必须先启动server.js服务器
2. **浏览器支持**：需要现代浏览器（支持ES6+和Fetch API）
3. **网络连接**：需要网络连接以搜索新闻和访问原文
4. **CORS**：服务器已配置CORS，允许本地HTML文件访问
5. **文件管理**：生成的HTML文件会保存在output目录，建议定期清理
6. **新闻链接**：⚠️ 重要提示
   - "查看原文"链接应指向具体的新闻文章页面，而不是网站首页
   - 如果使用WebSearch工具，确保提取的URL是完整的文章链接
   - 手动创建数据时，需要提供真实的新闻文章URL
   - 如果无法获取具体文章URL，页面会显示相应提示信息

## 常见问题

### Q: 浏览器没有自动打开HTML页面怎么办？

**A**: 如果自动打开失败，可以使用以下方法手动打开：

**方法1：文件资源管理器**
1. 按 `Win + E` 打开文件资源管理器
2. 导航到：`C:\Users\你的用户名\.claude\skills\news-summary\output`
3. 双击HTML文件即可在默认浏览器中打开

**方法2：PowerShell命令（推荐）**
```powershell
# 方式1：使用Start-Process
powershell -Command "Start-Process 'C:\Users\你的用户名\.claude\skills\news-summary\output\2025-12-08_14-30-00_主题\summary.html'"

# 方式2：直接在PowerShell中
Start-Process "C:\Users\你的用户名\.claude\skills\news-summary\output\2025-12-08_14-30-00_主题\summary.html"
```

**方法3：CMD命令**
```cmd
start "" "C:\Users\你的用户名\.claude\skills\news-summary\output\2025-12-08_14-30-00_主题\summary.html"
```

**方法4：指定浏览器打开**
```bash
# Chrome
"C:\Program Files\Google\Chrome\Application\chrome.exe" "C:\Users\你的用户名\.claude\skills\news-summary\output\2025-12-08_14-30-00_主题\summary.html"

# Firefox
"C:\Program Files\Mozilla Firefox\firefox.exe" "C:\Users\你的用户名\.claude\skills\news-summary\output\2025-12-08_14-30-00_主题\summary.html"

# Edge
start msedge "C:\Users\你的用户名\.claude\skills\news-summary\output\2025-12-08_14-30-00_主题\summary.html"
```

**方法5：复制文件路径**
1. 在文件资源管理器中右键点击HTML文件
2. 选择"复制为路径"
3. 打开任意浏览器，粘贴路径到地址栏
4. 按回车键打开

### Q: AI解读按钮点击后没有反应？

**A**: 检查以下几点：
1. 确认server.js正在运行
2. 检查浏览器控制台是否有错误
3. 确认端口3456没有被其他程序占用

### Q: 如何停止服务器？

**A**: 在运行server.js的终端中按 `Ctrl+C`

### Q: 生成的HTML文件存放在哪里？

**A**: 在 `~/.claude/skills/news-summary/output/` 目录下

### Q: 如何搜索特定时间范围的新闻？

**A**: 在搜索关键词中加入时间限制，例如："人工智能 过去3天"

## 自定义扩展

### 添加更多导出格式

可以在 `template.js` 中添加新的HTML模板样式或在 `server.js` 中添加PDF、JSON等导出格式。

### 自定义权威性评估

修改 `index.md` 中的权威性评估逻辑，添加更多评估维度。

### 集成更多AI功能

可以扩展AI解读功能，添加：
- 情感分析
- 趋势预测
- 相关新闻推荐
- 多语言翻译

## 版本历史

- **v1.0.0** (2025-12-08)
  - 初始版本发布
  - 支持新闻搜索和摘要
  - 支持AI解读功能
  - 自动生成HTML页面

## 许可证

MIT License

## 反馈与支持

如有问题或建议，请通过以下方式联系：
- 在Claude Code中使用 `/help` 命令
- 访问 https://github.com/anthropics/claude-code/issues
