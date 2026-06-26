# 浏览器工具Action使用指南

## 核心Action分类

### 1. 导航与页面加载
- **navigate**: 访问指定URL
  - 参数: `url` (必需)
  - 用途: 加载大众点评首页或具体商户页面
  - 示例: `navigate(url="https://www.dianping.com")`

- **backbone**: 获取页面结构骨架
  - 参数: 无必需参数（可选maxElements）
  - 用途: 分析页面整体布局，识别关键交互元素
  - 返回: 带ref标记的元素列表，可用于后续交互

### 2. 元素定位与搜索
- **search**: 模糊查找页面元素
  - 参数: `query` (必需，支持文本、.class、#id、tag)
  - 用途: 定位搜索框、登录按钮、商户卡片等
  - 示例: `search(query="#myInput")` 或 `search(query="请登录/注册")`
  - **重要更新**: 优先使用search进行动态定位，避免硬编码ref引用

### 3. 用户交互操作
- **type**: 在输入框中输入文本
  - 参数: `ref` (必需), `text` (必需), `submit` (可选)
  - 用途: 在搜索框中输入查询关键词
  - 示例: `type(ref="e3", text="北京咖啡店", submit=true)`

- **click**: 点击页面元素
  - 参数: `ref` (必需)
  - 用途: 点击搜索按钮、商户链接等
  - 示例: `click(ref="search-button-ref")`

- **press**: 模拟键盘按键
  - 参数: `key` (必需，如"Enter", "Tab")
  - 用途: 提交表单、切换焦点等
  - 示例: `press(key="Enter")`

### 4. 内容提取
- **readability**: 提取文章式内容
  - 参数: 无必需参数
  - 用途: 获取商户详情页面的结构化文本
  - 优势: 自动清理广告和无关内容，返回干净的主体内容
  - **重要更新**: readability能够完整提取包括食材评分在内的所有分项评分信息

- **snapshot**: 获取完整DOM
  - 参数: 可选format="ai"（推荐）或format="aria"
  - 用途: 备用方案，当readability无法获取所需信息时使用
  - 注意: 返回数据量大，应谨慎使用

## 大众点评专用操作模式

### 登录状态检测模式
```javascript
// 模式1: 文本检测
search(query="请登录/注册")

// 模式2: URL检测  
if (currentUrl.includes("account.dianping.com/pclogin")) {
  // 需要登录
}

// 模式3: 元素存在性检测
search(query=".login-user-face")
```

### 搜索操作模式
```javascript
// 标准搜索流程
navigate(url="https://www.dianping.com")
backbone() // 获取页面结构
// 检查登录状态
// 动态定位搜索框
search(query="#myInput") // 首页
// 或
search(query="#J-search-input") // 搜索结果页
type(ref="found-ref", text="搜索关键词", submit=true)
```

### 信息提取模式
```javascript
// 商户列表页面
readability() // 获取商户概览信息

// 商户详情页面  
readability() // 获取详细商户信息，包含：
// - 基础信息（名称、地址、电话、营业时间）
// - 评分信息（综合评分、口味/环境/服务/食材分项评分）
// - 扩展信息（评价数量、人均消费、菜系分类、商圈位置）
// - 推荐菜列表
// - 用户评论内容和标签
```

## 最佳实践建议

1. **优先级顺序**: readability > backbone > snapshot
2. **错误处理**: 每个操作后检查结果，失败时重试或降级
3. **性能优化**: 避免不必要的snapshot调用
4. **稳定性**: 使用search动态定位元素，避免硬编码ref
5. **用户体验**: 登录相关操作必须明确引导用户
6. **兼容性**: 考虑不同页面类型的搜索框差异（首页vs搜索结果页）
7. **完整性**: 利用readability的完整信息提取能力，确保获取所有可用的商户详情