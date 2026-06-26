# Volcengine 文档解析与索引方案

## 📋 项目目标

解析火山引擎（Volcengine）文档结构，建立功能索引，为优化 volcengine 技能提供依据。

## 🔗 目标文档
- **主URL**: https://www.volcengine.com/docs/82379/1399009?lang=zh
- **产品ID**: 82379 (火山方舟)
- **文档ID**: 1399009 (文本生成)
- **语言**: zh (中文)

## 🎯 解析挑战

### 技术障碍
1. **动态内容加载**: 文档使用现代JavaScript框架（React/Next.js），内容客户端渲染
2. **SPA架构**: 单页应用，传统爬虫难以获取完整内容
3. **认证可能**: 部分内容可能需要登录或API密钥
4. **反爬机制**: 可能存在的反爬虫保护

### 内容挑战
1. **结构复杂**: 文档可能包含嵌套目录、代码示例、API参数表
2. **版本差异**: 不同模型版本可能有不同文档
3. **多语言支持**: 中英文内容可能结构不同

## 🛠️ 解析策略（多层次方案）

### 策略1: URL模式分析与映射
**目标**: 通过URL结构推断文档组织

```yaml
URL模式: https://www.volcengine.com/docs/{product_id}/{doc_id}?lang={language}

已知映射:
- 82379: 火山方舟 (产品)
- 1399009: 文本生成 (具体文档)
- 1263693: API参考 (从SKILL.md得知)

推断结构:
/docs/82379/                      # 产品主页
/docs/82379/1263693               # API参考文档  
/docs/82379/1399009               # 文本生成文档
/docs/82379/{其他doc_id}          # 其他功能文档
```

### 策略2: 静态资源分析
**目标**: 从JavaScript bundles中提取内容线索

```bash
# 可能的资源文件
- 静态JSON文件 (文档索引)
- Sitemap.xml
- robots.txt
- API规范文件 (OpenAPI/Swagger)
```

### 策略3: 模拟浏览器访问
**目标**: 使用工具获取渲染后内容

**工具选项:**
1. **Playwright/Puppeteer**: Headless浏览器自动化
2. **Selenium**: 浏览器自动化框架  
3. **curl with JS引擎**: 有限JS执行
4. **专门爬虫工具**: Scrapy with Splash

### 策略4: API端点发现
**目标**: 查找实际的API文档端点

```bash
# 可能的API端点
- /api/v1/docs
- /openapi.json
- /swagger.json
- /redoc/v1
- GraphQL端点
```

## 📊 实施步骤

### 阶段1: 侦察与发现 (1-2天)

#### 任务1.1: URL结构分析
```powershell
# 生成可能的URL模式
$baseUrl = "https://www.volcengine.com/docs/82379"
$potentialDocs = @(
    "1263693",  # API参考 (已知)
    "1399009",  # 文本生成 (目标)
    "overview",
    "quickstart", 
    "models",
    "pricing",
    "authentication",
    "errors",
    "examples"
)
```

#### 任务1.2: 资源文件扫描
```powershell
# 检查常见资源文件
$resources = @(
    "/sitemap.xml",
    "/robots.txt",
    "/api-docs",
    "/openapi.json",
    "/static/docs-index.json"
)
```

#### 任务1.3: 网络请求分析
- 使用浏览器开发者工具分析XHR/Fetch请求
- 查找文档数据加载的API端点
- 分析响应格式 (JSON/HTML/其他)

### 阶段2: 内容提取 (2-3天)

#### 任务2.1: 渲染内容获取
**方案A: 使用Playwright (推荐)**
```powershell
# PowerShell调用Playwright
$playwrightScript = @"
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  
  // 访问目标文档
  await page.goto('https://www.volcengine.com/docs/82379/1399009?lang=zh');
  
  // 等待内容加载
  await page.waitForSelector('article, .documentation-content, main', { timeout: 10000 });
  
  // 提取主要内容
  const content = await page.evaluate(() => {
    const main = document.querySelector('article') || 
                 document.querySelector('.documentation-content') ||
                 document.querySelector('main') ||
                 document.body;
    
    return {
      title: document.title,
      headings: Array.from(main.querySelectorAll('h1, h2, h3, h4')).map(h => ({
        level: parseInt(h.tagName[1]),
        text: h.textContent.trim(),
        id: h.id
      })),
      textContent: main.innerText,
      htmlContent: main.innerHTML.substring(0, 50000) // 限制长度
    };
  });
  
  console.log(JSON.stringify(content, null, 2));
  
  await browser.close();
})();
"@
```

**方案B: 使用curl+jsdom (轻量级)**
```bash
# 需要Node.js环境
npm install jsdom
node -e "
const jsdom = require('jsdom');
const { JSDOM } = jsdom;
const dom = new JSDOM('<body>动态内容需要JS执行</body>', {
  runScripts: 'dangerously',
  resources: 'usable'
});
// 复杂，不推荐用于复杂SPA
"
```

#### 任务2.2: PDF版本获取
```powershell
# 查找PDF下载链接
$pdfPatterns = @(
    "*.pdf",
    "download-pdf",
    "pdf-download",
    "export-pdf"
)

# 如果找到PDF，下载并转换为文本
if ($pdfUrl) {
    # 使用工具如pdftotext或在线转换
    # pdftotext document.pdf document.txt
}
```

### 阶段3: 结构分析与索引 (1-2天)

#### 任务3.1: 文档结构解析
```powershell
# 解析提取的内容
function Parse-VolcengineDoc {
    param([string]$content)
    
    $structure = @{
        Sections = @()
        APIs = @()
        Models = @()
        CodeExamples = @()
        Parameters = @()
        ErrorCodes = @()
    }
    
    # 解析标题层级
    # 识别API端点 (如 /api/v3/chat/completions)
    # 提取模型列表
    # 识别参数表格
    # 提取代码示例
}
```

#### 任务3.2: 功能分类
```yaml
功能分类体系:
1. 认证与授权
   - API密钥管理
   - 访问控制
   - 令牌刷新

2. 模型管理  
   - 模型列表
   - 模型特性
   - 版本信息

3. API调用
   - 文本生成
   - 聊天完成
   - 流式响应
   - 图像处理

4. 配置参数
   - 温度 (temperature)
   - Top-p
   - 最大token数
   - 停止序列

5. 错误处理
   - 错误代码
   - 速率限制
   - 配额管理

6. 高级功能
   - 函数调用
   - 工具使用
   - 多模态
   - 批量处理
```

#### 任务3.3: 创建索引数据库
```powershell
# JSON索引结构
$docIndex = @{
    metadata = @{
        product = "火山方舟"
        product_id = "82379"
        crawled_at = (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
        version = "未知" # 需要从文档中提取版本号
    }
    
    documents = @(
        @{
            id = "1399009"
            title = "文本生成"
            url = "https://www.volcengine.com/docs/82379/1399009?lang=zh"
            categories = @("api", "text-generation")
            apis = @("POST /api/v3/chat/completions", "POST /api/v3/completions")
            models = @("doubao-seed-1-8-251228", "glm-4-7-251222")
            last_updated = "2026-03-11" # 从页面获取
        }
    )
    
    models = @(
        @{
            id = "doubao-seed-1-8-251228"
            name = "Doubao Seed 1.8"
            capabilities = @("text", "image")
            context_window = 256000
            provider = "volcengine"
            documentation = "1399009"
        }
    )
    
    api_endpoints = @(
        @{
            method = "POST"
            path = "/api/v3/chat/completions"
            description = "聊天补全接口"
            parameters = @("model", "messages", "temperature", "max_tokens")
            document = "1399009"
        }
    )
}
```

### 阶段4: 集成到技能 (1-2天)

#### 任务4.1: 更新技能文档
```powershell
# 基于解析结果更新SKILL.md
$enhancedSections = @{
    "新增功能" = $parsedCapabilities
    "API详细参数" = $parsedParameters  
    "错误代码参考" = $parsedErrorCodes
    "最佳实践" = $parsedBestPractices
    "代码示例" = $parsedCodeExamples
}
```

#### 任务4.2: 创建文档查询工具
```powershell
# PowerShell模块: Volcengine-DocHelper.psm1
function Get-VolcengineDoc {
    param(
        [string]$Topic,
        [string]$Category,
        [switch]$ListAll
    )
    
    # 查询本地索引
    # 返回相关文档摘要
    # 提供直接链接
}

function Search-VolcengineAPI {
    param([string]$Endpoint)
    
    # 搜索API端点文档
    # 显示参数、示例、错误处理
}
```

#### 任务4.3: 自动化更新机制
```powershell
# 定时更新脚本
function Update-VolcengineDocs {
    # 1. 检查文档更新
    # 2. 增量爬取新内容
    # 3. 更新索引
    # 4. 通知变更
}

# 添加到cron
cron add -Name "volcengine-docs-update" -Schedule "0 2 * * 0" `
  -Command "Update-VolcengineDocs -Notify"
```

## 🚀 优先实施路径

### 立即可行方案 (无需特殊工具)
1. **URL模式分析** - 基于已知URL推断结构
2. **静态资源检查** - robots.txt, sitemap.xml
3. **页面元数据提取** - 标题、描述、最后更新时间

### 中等难度方案 (需要基础工具)
1. **简单爬虫** - 使用wget/curl获取基础HTML
2. **JSON端点发现** - 查找API文档的JSON端点
3. **PDF版本处理** - 如果存在PDF下载

### 高级方案 (需要专门工具)
1. **Headless浏览器** - Playwright/Puppeteer
2. **完整爬虫框架** - Scrapy + Splash
3. **API反向工程** - 分析网络请求

## 📁 产出物

### 核心产出
1. **文档索引文件** (`volcengine-docs-index.json`)
   - 结构化文档目录
   - 功能分类映射
   - API端点索引

2. **解析工具集** (`scripts/parse-docs.ps1`)
   - 文档爬取工具
   - 内容提取函数
   - 结构分析模块

3. **更新技能组件**
   - 增强的SKILL.md
   - 文档查询工具
   - 自动更新脚本

### 辅助产出
1. **URL映射表** - 文档ID到功能的映射
2. **模型矩阵** - 各模型能力对比
3. **API速查表** - 常用API参数参考
4. **错误代码手册** - 错误处理指南

## 🔧 技术要求

### 必需工具
- **PowerShell 5.1+** - 主要开发语言
- **Node.js** - Playwright/JavaScript执行
- **Git** - 版本控制

### 可选工具
- **Playwright** - 浏览器自动化 (推荐)
- **Python + Scrapy** - 高级爬虫
- **jq** - JSON处理
- **pandoc** - 文档格式转换

### 开发环境
```bash
# 安装Playwright (如果选择该方案)
npm install playwright
npx playwright install chromium

# 安装Python依赖 (如果选择Scrapy)
pip install scrapy scrapy-splash
```

## ⚠️ 注意事项

### 法律与合规
1. **遵守robots.txt** - 尊重网站爬虫政策
2. **速率限制** - 避免对目标服务器造成压力
3. **版权尊重** - 文档内容仅用于个人技能优化

### 技术风险
1. **反爬虫检测** - 可能被屏蔽IP
2. **结构变更** - 文档网站可能改版
3. **内容不完整** - 动态内容可能加载不全

### 维护考虑
1. **定期更新** - 文档可能频繁更新
2. **版本兼容** - 保持与多版本文档兼容
3. **错误处理** - 网络问题、解析失败等

## 📈 成功标准

### 初级成功
- ✅ 建立基础URL结构映射
- ✅ 提取关键文档元数据
- ✅ 创建基本功能分类

### 中级成功  
- ✅ 获取主要API文档内容
- ✅ 建立模型能力矩阵
- ✅ 创建本地文档索引

### 高级成功
- ✅ 完整文档结构解析
- ✅ 自动化更新机制
- ✅ 集成到volcengine技能中

## 🔄 后续优化

### 短期优化 (完成基础解析后)
1. **增量更新** - 只爬取变更内容
2. **缓存机制** - 减少重复请求
3. **离线访问** - 本地文档镜像

### 长期愿景
1. **智能搜索** - 语义搜索文档内容
2. **代码生成** - 根据文档生成客户端代码
3. **变更检测** - 自动检测API变更并提醒
4. **多产品支持** - 扩展到火山引擎其他产品

---

## 🎯 实施建议

基于当前技能状态和资源限制，建议采用**渐进式实施**：

### 第一步: 立即开始 (今天)
1. 分析现有volcengine技能的需求缺口
2. 实施"立即可行方案"中的项目
3. 创建基础文档索引结构

### 第二步: 核心解析 (本周)
1. 选择并实施一种内容提取方案
2. 解析"文本生成"核心文档
3. 更新技能中的关键信息

### 第三步: 完整集成 (下周)
1. 扩展解析到其他重要文档
2. 创建文档查询工具
3. 建立自动化更新流程

**关键决策点**: 选择内容提取技术方案 (Playwright vs 其他)

---

*文档解析方案创建于: 2026-04-15*
*目标: 为volcengine技能优化提供文档依据*