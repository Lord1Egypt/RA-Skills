# 知识星球搜索技能

在知识星球（wx.zsxq.com）上搜索指定关键词并返回结果。

## 触发条件

以下说法均触发此技能：
- "你去星球搜一下xx"
- "星球搜一下xx"
- "搜一下星球xx"
- "知识星球搜索xx"
- "在星球里搜xx"
- "星球里有没有xx相关的"
- "去知识星球找一下xx"
- "zsxq搜xx"
- "知识星球搜一下xx"
- "zsxq搜一下xx"
- "星球里找一下xx"
- "帮我在星球搜xx"
- "星球查一下xx"

## 默认配置

- **浏览器Profile**: `openclaw`
- **搜索范围**: 全部星球
- **Tab**: 主题
- **排序**: 最新
- **targetId**: 通过 `browser(action="list_tabs")` 动态获取，不要硬编码

## 操作流程

> 约定：以下所有 browser 调用均使用 `profile="openclaw"`。`<tabId>` 为当前标签页ID，需动态获取。

### Step 1: 直接导航到全局搜索URL

> **核心方案：** 从星球页面内部搜索默认为"当前星球"。知识星球的"全部星球"按钮是Angular组件（`.search-btn > .all`），JS的DOM click和MouseEvent都无法触发Angular事件绑定。
> **正确做法是直接导航到全局搜索URL**（不带groupId参数）。

```
browser(action="navigate", profile="openclaw", targetId=<tabId>, url="https://wx.zsxq.com/search/<URL编码的关键词>?searchUid=0.999")
```

等待页面加载：

```
browser(action="act", profile="openclaw", targetId=<tabId>, request={"kind":"wait", "timeMs":1000})
```

> **如果需要搜索"当前星球"：** URL加groupId参数：`https://wx.zsxq.com/search/<关键词>?groupId=<星球ID>`
>
> **登录态检测：** 如果导航后跳转到登录页，告知用户"浏览器登录态已失效，请先登录后重试"。

### Step 2: 切换到"主题"筛选

直接导航后默认显示"文件"tab，需切到"主题"。snapshot通常抓不到tab ref，用JS（参考 [JS: clickTabItem](#js-clicktabitem)）：

```
browser(action="act", profile="openclaw", targetId=<tabId>, request={"kind":"evaluate", "fn":"<参考JS模板，tabName='主题'>"})
```

点击后等待结果刷新：

```
browser(action="act", profile="openclaw", targetId=<tabId>, request={"kind":"wait", "timeMs":500})
```

### Step 3: 切换到"最新"排序

snapshot同样抓不到排序按钮，用JS（参考 [JS: clickSortOption](#js-clicksortoption)）：

```
browser(action="act", profile="openclaw", targetId=<tabId>, request={"kind":"evaluate", "fn":"<参考JS模板，sortName='最新'>"})
```

点击后等待排序刷新：

```
browser(action="act", profile="openclaw", targetId=<tabId>, request={"kind":"wait", "timeMs":500})
```

### Step 4: 截图确认搜索状态

```
browser(action="screenshot", profile="openclaw", targetId=<tabId>)
read(<screenshot_path>)
```

确认以下三项：
1. 标题显示"已加入星球的主题"（全部星球）或"「xxx」星球的主题"（当前星球）
2. "主题" Tab 已选中
3. "最新"排序已激活

**如果状态不对**，回到对应步骤修正后重新确认。最多重试2次。

### Step 5: 抓取结果并总结

> **必须用 `compact=false`**，否则compact模式会省略搜索结果正文内容。

```
browser(action="snapshot", compact=false, profile="openclaw", targetId=<tabId>)
```

- 解析 snapshot 内容，按日期倒序整理为结构化总结返回用户
- **只输出搜索结果，不输出中间步骤**（导航、点tab、截图确认等过程全部跳过）
- **如果搜索无结果**（snapshot中出现"暂无搜索结果"等提示文字，或结果列表为空），告知用户并建议换关键词重试

### Step 6（可选）: 滚动加载更多结果

如果用户需要更多结果：

```
browser(action="act", profile="openclaw", targetId=<tabId>, request={"kind":"evaluate", "fn":"window.scrollTo(0, document.body.scrollHeight)"})
browser(action="act", profile="openclaw", targetId=<tabId>, request={"kind":"wait", "timeMs":1000})
```

滚动后重新snapshot（`compact=false`）获取新加载的结果。**最多滚动3次**，超过或连续两次无新内容则停止。

## JS模板

> 以下JS片段供各步骤引用。
> **`kind:"evaluate"` 的参数名是 `fn`（不是 `expression`）！**
> **箭头函数 `() => {}` 格式可用。IIFE `(function(){})()` 也可用。**

### JS: clickTabItem

点击搜索结果的Tab筛选项（全部/主题/文件/用户）。优先用 `.tab-item` class匹配，若class已变则fallback到 `.navtabs` 内按文本遍历。

```javascript
() => {
  const tabName = '主题'; // 替换为目标Tab名
  const tab = [...document.querySelectorAll('.tab-item')].find(t => t.textContent.trim() === tabName && !t.classList.contains('tab-selected'));
  if (tab) { tab.click(); return 'clicked tab: ' + tabName; }
  const navtabs = document.querySelector('.navtabs, [class*="navtab"], [class*="tab-bar"]');
  if (navtabs) {
    const fallback = [...navtabs.querySelectorAll('*')].find(e => e.offsetHeight > 0 && e.offsetParent !== null && e.children.length === 0 && e.textContent.trim() === tabName);
    if (fallback) { fallback.click(); return 'clicked tab (fallback): ' + tabName; }
  }
  return 'tab not found: ' + tabName;
}
```

### JS: clickSortOption

在排序容器内精确点击排序选项（综合/最新/精华）。

```javascript
() => {
  const sortName = '最新'; // 替换为目标排序名
  const container = document.querySelector('.search-sort-container, [class*="sort"]');
  if (!container) return 'sort container not found';
  const el = [...container.querySelectorAll('*')].find(e => e.offsetHeight > 0 && e.offsetParent !== null && e.children.length === 0 && e.textContent.trim() === sortName);
  if (el) { el.click(); return 'clicked sort: ' + sortName; }
  return 'sort option not found: ' + sortName;
}
```

## 页面结构参考

| 区域 | CSS选择器/特征 | 说明 |
|------|---------------|------|
| 全局搜索URL | `/search/<关键词>` | 不带groupId=全部星球 |
| 当前星球搜索URL | `/search/<关键词>?groupId=<ID>` | 带groupId=当前星球 |
| 搜索范围按钮 | `.search-btn > .current` / `.search-btn > .all` | JS click无效（Angular绑定） |
| Tab栏 | `.navtabs` | 全部 / 主题 / 文件 / 用户 |
| Tab项 | `.tab-item` | 选中态: `.tab-selected` |
| 排序区 | `.search-sort-container` | 综合 / 最新 / 精华 |
| 搜索结果 | snapshot中的列表项 | 每条包含：标题、摘要、日期、来源星球 |
| 无结果提示 | "暂无搜索结果" 等文本 | 需识别并告知用户 |

## 注意事项

- **全部星球搜索用直接导航**：`/search/<关键词>`，不经过星球页面内部搜索面板。Angular组件的"全部星球"按钮JS click无效。
- **ref失效**：导航或页面跳转后ref全部失效，必须重新snapshot获取新ref
- **evaluate参数名是fn**：`kind:"evaluate"` 必须用 `fn` 参数传JS代码，不能用 `expression`
- **compact模式**：获取ref和检测状态用`compact=true`；**抓取搜索结果必须用`compact=false`**
- **tabId动态获取**：不要硬编码，浏览器重启后会变化
- **重试上限**：状态校验最多重试2次，滚动加载最多3次，避免死循环
- **登录态**：全局搜索URL如跳转到登录页，提示用户手动登录
- 不要建议用户安装 Chrome Browser Relay 扩展
