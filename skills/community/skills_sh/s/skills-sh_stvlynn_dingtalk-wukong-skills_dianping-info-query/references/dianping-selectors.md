# 大众点评常用CSS选择器参考

## 搜索框选择器（跨页面兼容性）

### 首页搜索框
- `#myInput` - 首页主搜索框
- `input[placeholder="美食、电影、酒店..."]` - 通过placeholder定位

### 城市页面搜索框  
- `#J-search-input` - 城市页面搜索框
- `input.j-search-input` - 带有特定class的搜索框
- `input[placeholder="搜索商户名、地址、菜名、外卖等"]` - 通过placeholder定位

### 统一搜索框定位策略
```javascript
// 推荐使用以下查询字符串进行动态定位
"input[placeholder*='搜索'],#myInput,#J-search-input,input.j-search-input"
```

## 登录状态检测选择器

### 已登录状态
- `.username` 或 `.nick-name` - 用户名元素
- `.user-face` - 用户头像元素  
- `a[href*='/member/']` - 个人中心链接

### 未登录状态
- `.login-link` 或包含"请登录/注册"文本的元素
- `#account-login` - 登录表单容器
- `[src*='qrcode']` - 二维码图片

## 商户信息选择器

### 基础信息
- `#pc-shop-head` - 商户头部信息容器
- `.shop-name` - 商户名称
- `.address` - 地址信息
- `.tel` - 电话号码

### 评分信息
- `.star-container` - 星级评分容器
- `.score` - 综合评分数字
- `.comment-condition` - 分项评分（口味/环境/服务/食材）

### 用户标签
- `.tag-list` - 标签列表容器
- `.tag-item` - 单个标签项
- `.count` - 标签提及次数

## 城市切换选择器

### 城市选择
- `.city` - 当前城市显示
- `.city-select-icon` - 城市选择图标
- `a[href*='/citylist']` - 城市列表链接

### 目标城市
- `a[href*='/xian']` - 西安城市链接（示例）
- `a[href*='/beijing']` - 北京城市链接（示例）
- `strong:contains('城市名')` - 城市名称高亮

## 最佳实践建议

1. **优先使用属性选择器**：如`[placeholder*='搜索']`比ID选择器更稳定
2. **组合选择器提高准确性**：如`input.j-search-input[placeholder*='搜索']`
3. **避免硬编码ref**：始终使用`search`工具动态定位元素
4. **处理页面加载时机**：在关键操作后添加适当的等待
5. **验证元素存在性**：在操作前确认目标元素确实存在

## 动态定位示例

```javascript
// 搜索框动态定位
use_browser(action="search", query="input[placeholder*='搜索'],#myInput,#J-search-input")

// 登录状态检测
use_browser(action="search", query=".username,.nick-name,.login-link")

// 商户评分提取  
use_browser(action="search", query=".score,.star-container")
```