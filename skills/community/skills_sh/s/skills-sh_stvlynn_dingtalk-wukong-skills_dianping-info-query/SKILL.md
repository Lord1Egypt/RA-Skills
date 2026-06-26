---
name: dianping-info-query
description: 专业的大众点评网站信息查询技能，支持商户搜索、详情获取、评分信息提取、城市切换和深度信息查询等功能。当用户需要从大众点评网站查询商户信息、获取店铺详情、查看评分评论、切换城市等数据时使用。该技能包含完整的双状态登录检测机制（已登录/未登录）、用户引导机制和标准化操作流程，并支持包括食材评分在内的完整分项评分提取。新增跨页面搜索框动态定位、多标签页自动管理、商圈查询支持和用户标签标准化处理功能。
---

# 大众点评信息查询技能

## 概述

本技能提供对大众点评网站（dianping.com）的专业信息查询能力，能够安全、高效地获取商户信息、评分数据和相关详情。技能内置完整的**双状态登录检测机制**，能够准确识别已登录和未登录两种状态，并提供相应的处理流程。

## 核心功能范围

### 支持的查询类型
- **商户搜索**：按关键词、地点、分类搜索商户
- **商圈查询**：支持热门商圈（如回民街、南京路等）的整体信息查询
- **商户详情**：获取商户基本信息（名称、地址、电话、营业时间）
- **评分信息**：获取综合评分、口味/环境/服务/**食材**分项评分（新增食材评分支持）
- **扩展信息**：评价数量、人均消费、菜系分类、商圈位置、团购/订座标识
- **城市切换**：支持在全国所有大众点评覆盖城市间灵活切换
- **深度信息查询**：获取推荐菜列表、用户评论内容、**评论标签及高频提及次数**、营业时间等深度信息
- **多标签页管理**：自动处理搜索过程中产生的新标签页，确保操作连续性

### 不支持的功能
- 需要深度登录验证的个人化内容（如个人收藏、历史记录）
- 批量自动化查询（单次查询为主）

## 登录状态检测与处理

### 双状态检测机制
1. **未登录状态检测**：
   - 检查页面右上角是否存在"请登录/注册"文本
   - 检查URL是否包含`account.dianping.com/pclogin`
   - 查找登录相关的二维码图片或表单元素

2. **已登录状态检测**：
   - 检查是否存在用户名元素（`.nick-name` 或 `.username`）
   - 验证用户头像元素（`.user-face`）是否存在
   - 确认个人中心链接是否可访问

### 用户引导流程
**未登录状态**：
1. 立即暂停自动化操作
2. 向用户说明当前需要手动登录
3. 提供具体的登录指导（主要为二维码扫码登录）
4. 等待用户确认登录完成后再继续执行查询

**已登录状态**：
1. 直接执行查询操作
2. 利用登录状态获取更完整的商户信息
3. 如遇异常，重新检测登录状态

## 标准化操作SOP流程

### 基础查询流程
```
Step 1: 导航到大众点评首页 (https://www.dianping.com)
Step 2: 使用backbone分析页面结构，检测登录状态（双状态检测）
Step 3: 
   - 未登录：暂停并引导用户手动完成登录
   - 已登录：继续执行查询
Step 4: 动态定位搜索框并输入查询关键词
   - 使用search工具动态查找多种选择器：#myInput, #J-search-input, input.j-search-input
   - 优先使用placeholder属性进行模糊匹配：input[placeholder*='搜索']
   - 避免硬编码ref引用，提高跨页面稳定性
Step 5: 提交搜索并等待结果页面加载
Step 6: 自动处理标签页切换（如产生新标签页）
Step 7: 使用readability提取结构化信息（包含完整分项评分和用户标签）
Step 8: 返回整理后的商户信息
```

### 城市切换流程
```
Step 1: 导航到当前城市页面
Step 2: 点击城市选择图标（img.city-select-icon）
Step 3: 在城市列表页面搜索目标城市
Step 4: 点击目标城市链接完成切换
Step 5: 验证城市切换成功（检查URL和当前城市显示）
Step 6: 执行目标城市的查询操作
```

### 深度信息查询流程
```
Step 1: 完成基础查询，进入商户详情页面
Step 2: 使用readability提取完整页面内容（自动包含食材评分和用户标签次数）
Step 3: 定位推荐菜区域（#shop-dish）获取菜品列表
Step 4: 提取用户评论信息（评分、评论数量、评论标签及提及次数、详细评论内容）
Step 5: 整理并返回完整的深度信息
```

### 多标签页管理流程
```
Step 1: 执行可能产生新标签页的操作（如搜索提交）
Step 2: 使用list_tabs获取所有打开的标签页
Step 3: 识别最新打开的标签页（通常为搜索结果页）
Step 4: 自动focus到最新标签页
Step 5: 验证标签页URL和标题确保正确性
Step 6: 继续后续操作
```

## 浏览器工具Action支持清单

### 导航与页面分析
- `navigate`: 访问指定URL（首页或具体商户页面）
- `backbone`: 分析页面整体结构，识别关键交互元素
- `search`: **优先使用**动态定位特定元素（搜索框、商户卡片、评分元素等）
- `readability`: 提取商户详情页面的结构化文本内容（**推荐首选**）
- `list_tabs`: 获取所有打开的标签页信息（用于多标签页管理）

### 用户交互
- `type`: 在搜索框中输入查询关键词
- `click`: 点击搜索按钮、商户链接或城市选择图标
- `press`: 模拟键盘操作（如Enter提交）
- `focus_tab`: 切换到指定标签页（用于多标签页场景）

### 内容提取
- `readability`: **首选方案**提取商户详情页面的完整结构化内容（包含食材评分、用户标签次数等）
- `snapshot`: 获取完整DOM用于复杂内容分析（**备用方案**）

## 具体操作示例

### 示例1：查询成都小龙坎火锅（已登录状态）
```javascript
// Step 1: 导航到首页
use_browser(action="navigate", url="https://www.dianping.com")

// Step 2: 检测登录状态
use_browser(action="backbone")
// 检查是否存在用户名元素（已登录状态）

// Step 3: 动态定位搜索框
use_browser(action="search", query="#myInput")

// Step 4: 执行搜索（已登录，直接执行）
use_browser(action="type", ref="found-ref", text="成都小龙坎老火锅", submit=true)

// Step 5: 提取完整结果（包含食材评分4.7、用户标签次数等）
use_browser(action="readability")
```

### 示例2：处理未登录状态
```javascript
// Step 1: 导航到首页
use_browser(action="navigate", url="https://www.dianping.com")

// Step 2: 检测到未登录状态
use_browser(action="backbone")
// 发现"请登录/注册"文本

// Step 3: 引导用户手动登录
// [暂停操作，提示用户扫码登录]

// Step 4: 用户确认登录后继续
use_browser(action="search", query="#myInput")
use_browser(action="type", ref="found-ref", text="北京中关村 咖啡店", submit=true)
```

### 示例3：城市切换操作
```javascript
// Step 1: 导航到当前城市
use_browser(action="navigate", url="https://www.dianping.com")

// Step 2: 点击城市选择图标
use_browser(action="search", query=".city-select-icon")
use_browser(action="click", ref="found-ref")

// Step 3: 搜索目标城市
use_browser(action="search", query="成都")

// Step 4: 点击成都城市链接
use_browser(action="click", ref="found-beijing-ref")

// Step 5: 验证切换成功后执行查询
use_browser(action="search", query="#myInput")
use_browser(action="type", ref="found-ref", text="小龙坎火锅", submit=true)
```

### 示例4：深度信息查询（包含食材评分和用户标签）
```javascript
// Step 1: 进入商户详情页面后
use_browser(action="readability") // 提取完整页面内容

// 结果将包含：
// - 综合评分: 4.4分
// - 分项评分: 口味4.4, 环境4.4, 服务4.4, 食材4.7
// - 用户标签: ["排队情况(2269次)", "收银员态度好(647次)", "环境干净整洁(646次)", ...]
// - 推荐菜: ["鸳鸯锅", "玫瑰圆子", "牛奶鸭血", ...]
// - 营业时间: 11:00-次日02:00
```

### 示例5：动态搜索框定位（增强稳定性）
```javascript
// 使用search工具动态定位搜索框，避免硬编码
use_browser(action="search", query="#myInput")
// 或在搜索结果页
use_browser(action="search", query="#J-search-input")

// 根据返回的ref进行操作
use_browser(action="type", ref="found-ref", text="查询关键词", submit=true)
```

### 示例6：跨页面搜索框动态定位（最新优化）
```javascript
// 统一的搜索框定位策略，兼容不同页面
use_browser(action="search", query="input[placeholder*='搜索'],#myInput,#J-search-input,input.j-search-input")
// 选择第一个找到的搜索框
use_browser(action="type", ref="first-found-ref", text="西安回民街", submit=true)
```

### 示例7：自动标签页管理（最新优化）
```javascript
// 执行搜索后自动处理标签页
use_browser(action="type", ref="search-input-ref", text="回民街", submit=true)

// 获取所有标签页
use_browser(action="list_tabs")

// 自动切换到最新标签页（搜索结果页）
use_browser(action="focus_tab", targetId="latest-search-tab-id")

// 继续后续操作
use_browser(action="readability")
```

### 示例8：商圈查询支持（最新优化）
```javascript
// 查询热门商圈（如回民街、南京路等）
use_browser(action="search", query="input[placeholder*='搜索']")
use_browser(action="type", ref="found-ref", text="西安回民街", submit=true)

// 提取商圈整体信息
use_browser(action="readability")
// 结果包含商圈评分、总评价数、热门标签、地理位置等信息
```

## 错误处理与最佳实践

### 常见问题处理
- **登录状态异常**：重新检测登录状态，必要时重新引导
- **网络超时**：重试1-2次，如仍失败则报告错误
- **元素未找到**：**使用search动态定位**，避免硬编码ref（重要优化）
- **内容加载不全**：添加适当的等待时间或使用wait_for
- **搜索结果为空**：提供友好的空结果提示
- **城市切换失败**：验证城市列表页面结构，重新定位城市链接
- **验证码/滑块验证**：识别安全机制，引导用户手动处理
- **标签页管理异常**：使用list_tabs重新获取标签页列表，确保操作正确性

### 性能优化建议
- **优先使用`readability`而非`snapshot`**以提高效率和信息完整性
- **使用`search`工具进行动态元素定位**（核心优化点）
- **实施多标签页自动管理**，避免手动切换错误
- 避免不必要的页面刷新和重复导航
- 合理设置超时时间（建议30-60秒）
- 利用登录状态持久化特性减少重复登录
- 城市切换后验证URL变化确保切换成功
- **完整提取分项评分**，包括新增的食材评分维度
- **提取用户标签及提及次数**，提供更丰富的用户反馈分析
- **支持商圈查询**，扩展应用场景覆盖范围

## 参考资源

### 浏览器工具文档
- `references/browser-actions.md`：详细的浏览器工具Action使用指南（已更新动态定位策略）
- `references/dianping-selectors.md`：大众点评常用CSS选择器参考（已更新食材评分和用户标签）
- `references/tab-management.md`：多标签页处理最佳实践指南（新增）
- `references/city-switching.md`：城市切换操作指南
- `references/deep-info-extraction.md`：深度信息提取方法（已更新商圈查询支持）

### 操作流程模板
- `references/query-workflow.md`：标准查询工作流模板
- `references/login-handling.md`：双状态登录处理最佳实践

## 使用场景触发条件

当用户提出以下类型的需求时，应触发本技能：
- "帮我查一下大众点评上[地点][类型]的店铺"
- "在大众点评搜索[关键词]"
- "获取大众点评上某家店的详细信息"
- "查询大众点评的商户评分和地址"
- "查看大众点评上某家店的评价数量和人均价格"
- "切换到[城市]查询[关键词]"
- "获取某家店的推荐菜和用户评论"
- "查询商户的食材评分和用户标签"
- "查询热门商圈（如回民街、南京路）的整体信息"
- 任何涉及从大众点评网站提取结构化商户信息的请求

## 验证状态

本技能已通过多场景验证，包括：
- ✅ 北京中关村咖啡店查询
- ✅ 上海外滩餐厅查询  
- ✅ 广州天河粤菜查询
- ✅ 成都小龙坎火锅查询（最新验证，确认食材评分4.7和用户标签次数提取）
- ✅ 杭州老陕面馆查询
- ✅ **西安回民街商圈查询（最新验证，确认跨区域城市切换、商圈信息提取、多标签页管理功能）**

技能现已完全符合Anthropic标准skill规范，能够在生产环境中稳定运行。