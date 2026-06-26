# 多标签页处理最佳实践指南

## 场景识别

大众点评网站在以下操作中会自动打开新标签页：
- 点击搜索按钮（非Enter提交）
- 点击商户详情链接
- 点击城市切换后的确认链接
- 某些广告或推广链接

## 标准处理流程

### 1. 操作前准备
```javascript
// 记录当前标签页ID（可选）
currentTabId = activeTargetId
```

### 2. 执行可能产生新标签页的操作
```javascript
// 示例：点击搜索按钮
use_browser(action="click", ref="search-btn-ref")
```

### 3. 获取所有标签页信息
```javascript
// 获取完整的标签页列表
tabsResult = use_browser(action="list_tabs")
```

### 4. 识别目标标签页
**策略A：按时间顺序（推荐）**
- 新打开的标签页通常是列表中的最后一个
- 适用于确定会产生新标签页的场景

**策略B：按URL匹配**
- 根据预期的URL模式匹配目标标签页
- 适用于URL可预测的场景

**策略C：按标题匹配**
- 根据页面标题关键词匹配
- 适用于标题包含特定信息的场景

### 5. 切换到目标标签页
```javascript
// 按ID切换到目标标签页
use_browser(action="focus_tab", targetId="target-tab-id")
```

### 6. 验证切换成功
```javascript
// 验证URL和标题是否符合预期
use_browser(action="backbone")
// 或使用readability提取内容验证
```

## 具体实现示例

### 示例1：搜索操作后的标签页处理
```javascript
// Step 1: 执行搜索（可能打开新标签页）
use_browser(action="click", ref="search-button")

// Step 2: 获取所有标签页
tabsInfo = use_browser(action="list_tabs")

// Step 3: 提取标签页ID列表
tabIds = tabsInfo.tabs.map(tab => tab.targetId)

// Step 4: 选择最新标签页（通常是最后一个）
latestTabId = tabIds[tabIds.length - 1]

// Step 5: 切换到最新标签页
use_browser(action="focus_tab", targetId=latestTabId)

// Step 6: 验证页面加载完成
use_browser(action="readability")
```

### 示例2：商户详情页的标签页处理
```javascript
// Step 1: 点击商户链接
use_browser(action="click", ref="shop-link")

// Step 2: 等待新标签页打开
use_browser(action="wait_for", timeMs=2000)

// Step 3: 获取标签页列表并找到包含商户名称的标签页
tabsInfo = use_browser(action="list_tabs")
targetTab = tabsInfo.tabs.find(tab => 
  tab.title.includes("商户名称") || 
  tab.url.includes("/shop/")
)

// Step 4: 切换到目标标签页
if (targetTab) {
  use_browser(action="focus_tab", targetId=targetTab.targetId)
}
```

### 示例3：通用标签页管理函数
```javascript
// 封装通用的标签页切换逻辑
function switchToLatestTab() {
  // 获取所有标签页
  const tabsResult = use_browser(action="list_tabs")
  
  // 验证结果有效性
  if (!tabsResult.ok || !tabsResult.tabs || tabsResult.tabs.length === 0) {
    throw new Error("无法获取标签页列表")
  }
  
  // 获取最新标签页ID
  const latestTabId = tabsResult.tabs[tabsResult.tabs.length - 1].targetId
  
  // 切换到最新标签页
  use_browser(action="focus_tab", targetId=latestTabId)
  
  return latestTabId
}

// 使用示例
use_browser(action="type", ref="search-input", text="回民街", submit=true)
const resultTabId = switchToLatestTab()
use_browser(action="readability")
```

## 错误处理与异常情况

### 常见问题
1. **标签页未及时打开**：添加适当的等待时间
2. **标签页ID变化**：重新获取标签页列表，不要缓存旧ID
3. **多个相似标签页**：使用更精确的匹配条件（URL+标题组合）
4. **标签页关闭异常**：验证标签页仍然存在再进行操作

### 异常处理策略
```javascript
// 安全的标签页切换
try {
  const tabsResult = use_browser(action="list_tabs")
  if (tabsResult.tabs && tabsResult.tabs.length > 1) {
    const targetTabId = tabsResult.tabs[tabsResult.tabs.length - 1].targetId
    use_browser(action="focus_tab", targetId=targetTabId)
  }
} catch (error) {
  // 回退到当前标签页继续操作
  console.log("标签页切换失败，继续当前页面操作")
}
```

## 性能优化建议

1. **最小化标签页切换次数**：在一个标签页内完成尽可能多的操作
2. **避免频繁的list_tabs调用**：只在必要时获取标签页列表
3. **合理设置等待时间**：给新标签页足够的加载时间
4. **及时关闭无用标签页**：减少内存占用（可选）

## 最佳实践总结

- **始终验证标签页状态**：在关键操作前后检查标签页正确性
- **使用自动化而非手动切换**：避免依赖固定的标签页ID
- **处理异步加载**：新标签页可能需要时间完全加载
- **保持操作连续性**：确保后续操作在正确的标签页上执行
- **记录操作日志**：便于调试和问题追踪