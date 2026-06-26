# v17.3 前端答案卡片 + Finance Query 改写

## v17.3 答案卡片 UI (index.html)

**目标**: 在结果列表**上方**加 AI 答案大卡片, 用户一眼看到答案 + 来源, 下面是 8 条蓝链 (Perplexity AI 风格)。

## HTML 结构

```html
<!-- 状态栏 (右上角加 AI 答案 开关) -->
<div id="status-bar" class="text-sm text-gray-500 mb-6 flex items-center gap-3">
  <span id="status-text">准备搜索...</span>
  <span id="answer-mode-toggle" class="ml-auto text-xs cursor-pointer"
        title="v17.3: 关闭后只返蓝链 (省时间)">
    <span id="answer-mode-icon">✦</span>
    <span id="answer-mode-text">AI 答案</span>
  </span>
</div>

<!-- AI 答案卡片 -->
<div id="answer-card" class="hidden mb-8">
  <div class="answer-card-inner rounded-2xl p-6 md:p-8">
    <div class="flex items-center gap-2 mb-4">
      <span class="answer-badge">✦ AI 答案</span>
      <span id="answer-model" class="text-xs text-gray-500"></span>
      <span id="answer-elapsed" class="text-xs text-gray-600 ml-auto"></span>
    </div>
    <div id="answer-text" class="answer-text text-gray-100 text-base md:text-lg leading-relaxed mb-5"></div>
    <div class="flex items-center gap-2 flex-wrap">
      <span class="text-xs text-gray-500">来源:</span>
      <div id="answer-sources" class="flex flex-wrap gap-2"></div>
    </div>
    <button id="answer-show-sources-btn" class="hidden mt-3 text-xs text-blue-400">
      ▼ 查看下方原始来源 (8 条)
    </button>
  </div>
</div>

<!-- 结果列表 -->
<div id="results-list" class="space-y-4"></div>
```

## CSS 关键样式 (玻璃态)

```css
.answer-card-inner {
  background: linear-gradient(135deg, rgba(30, 41, 59, 0.85) 0%, rgba(15, 23, 42, 0.85) 100%);
  border: 1px solid rgba(96, 165, 250, 0.3);
  box-shadow: 0 0 30px rgba(96, 165, 250, 0.15), inset 0 1px 0 rgba(255, 255, 255, 0.05);
  animation: slideUp 0.5s ease-out;
}
.answer-badge {
  display: inline-block;
  padding: 3px 10px;
  background: linear-gradient(135deg, #60a5fa 0%, #2563eb 100%);
  color: white;
  font-size: 12px;
  font-weight: 600;
  border-radius: 999px;
  box-shadow: 0 0 12px rgba(96, 165, 250, 0.4);  /* 跟 5 角星同色发光 */
}
.answer-source-chip {
  display: inline-flex;
  padding: 4px 10px;
  background: rgba(96, 165, 250, 0.1);
  border: 1px solid rgba(96, 165, 250, 0.25);
  color: #93c5fd;
  font-size: 11px;
  border-radius: 999px;
  transition: all 0.2s;
}
.answer-source-chip:hover {
  background: rgba(96, 165, 250, 0.2);
  transform: translateY(-1px);
}

/* Shimmer 加载动画 (1.4s 循环) */
.answer-shimmer {
  background: linear-gradient(90deg, rgba(96,165,250,0.05) 25%, rgba(96,165,250,0.2) 50%, rgba(96,165,250,0.05) 75%);
  background-size: 200% 100%;
  animation: shimmer 1.4s ease-in-out infinite;
  border-radius: 6px;
}
@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
```

## JS 关键逻辑

```javascript
let answerMode = true;  // 默认开 (Perplexity Mode)

async function doSearch(query) {
  currentQuery = query.trim();
  showResults(currentQuery);
  resultsList.innerHTML = '';

  // v17.3: 答案模式开启 → 显示 shimmer loading 卡片
  if (answerMode) {
    $('answer-card').classList.remove('hidden');
    $('answer-text').innerHTML = '<div class="answer-shimmer h-4 w-3/4 mb-3"></div>...';
  } else {
    $('answer-card').classList.add('hidden');
  }

  // fetch 加 answer: answerMode
  const r = await fetch(`${API_BASE}/v1/search`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query: currentQuery, top: 20, answer: answerMode })
  });
  const j = await r.json();

  currentResults = j.results || [];
  currentAnswer = j.answer || null;

  renderAnswer();  // 渲染答案卡片
  renderResults();
}

function renderAnswer() {
  if (!currentAnswer || !currentAnswer.answer) {
    $('answer-card').classList.add('hidden');
    return;
  }
  const a = currentAnswer;
  $('answer-text').textContent = a.answer;
  $('answer-model').textContent = a.model || 'AI';
  $('answer-elapsed').textContent = a.elapsed_ms ? `${a.elapsed_ms}ms · ${a.tokens} tokens` : '';

  // 来源 chips
  const sourcesEl = $('answer-sources');
  sourcesEl.innerHTML = '';
  (a.sources || []).forEach(src => {
    const chip = document.createElement('a');
    chip.href = `https://${src}`;
    chip.target = '_blank';
    chip.className = 'answer-source-chip';
    chip.textContent = src;
    sourcesEl.appendChild(chip);
  });
}

// toggle 按钮
$('answer-mode-toggle').onclick = () => setAnswerMode(!answerMode);
```

## patch 工具坑 (sibling 改过文件)

**问题**: sibling subagent 改过 index.html 后, 我再 patch, **老 string 匹配不到** (因为 sibling 加了新内容), **patch 报 "Could not find a match"**。

**修法**:
1. **必须先 read_file**, 看最新内容
2. 找**唯一**的小段文字当 anchor (用 `<style>` 标签, 不变量)
3. patch 完用 `grep` 验证 (例: `grep '</style>'` 确认只有 1 个, 不会被意外加 2 个)

**最严重 bug**: 之前 patch 在 `</style>` 前插 CSS, 但 sibling 之前**已经**在 `</style>` 前加 `main, footer { position: relative; z-index: 1; }`, 匹配时把 `main, footer` 后的 `</style>` 一起作为 anchor, 替换后**多了一个 `</style>`**!

**修法**: anchor 用**最独特的最后一行**而不是中间, 然后二次 grep 确认没重复。

## nginx 静态文件路径坑

**问题**: index.html 上传到 `/home/ubuntu/star-search/`, 公网访问还是**旧版** (没新答案卡片)!

**根因**: nginx 静态文件 root 是 `/var/www/star-search/`, **不是** `/home/ubuntu/star-search/`!

**修法**:
```bash
# 错误: 上传到 home 目录
echo "..." | base64 -d > /home/ubuntu/star-search/index.html

# 正确: 上传到 nginx root
echo "..." | base64 -d > /var/www/star-search/index.html
```

**验证**: 看到 nginx conf 里 `location / { root /var/www/star-search; }` 才确定路径。

## v17.2 finance 模式 query 改写 — 隐藏 bug

**问题**: 用户搜 "比亚迪股价", 8 条结果**全是新闻/资讯/公告**, **没有 1 条是实时报价页** ("当前股价 96.76 元" 这种)。

**根因**: bing_cn 搜 "比亚迪股价", 搜索引擎**优先返回新闻** (5/2 销量新闻 "股价飙升"), 不返回 quote.eastmoney.com/sz002594 这种**实时报价页**。

**修法** (search.py smart routing): query 末尾自动加 "行情" 关键词, 强制搜实时报价:

```python
# v16.2.2: 智能识别 — query 含财经词自动用 finance 引擎
stock_kw = ('股票','股价','股市','A股','a股','大盘','上证','深证','沪深',
            '港股','美股','纳斯达克','道琼斯','标普','基金','行情','涨停',
            '跌停','个股','板块','开盘','收盘','指数','成份股','龙虎榜',
            'ETF','etf','基金净值','今天股票','今天股市')
if any(kw in query for kw in stock_kw):
    engines = MODES.get('finance', CN_ENGINES)
    _used_smart = True
    # v17.2: 如果 query 没含"行情/股价"等, 追加 "行情" 让搜实时报价页
    if not any(w in query for w in ('行情', '股价', '收盘', '开盘', '实时', '今日')):
        query_for_search = query + ' 行情'
    else:
        query_for_search = query
```

**注意 LSP 报错**: `query_for_search` 在 cache_get 行**还没定义** (因为新逻辑定义在路由判断后)。

**修法**: 函数顶部**提前初始化**:
```python
async def search_async(query, ...):
    # v17.2: 默认用原 query, 智能识别时改写
    query_for_search = query

    if not force_refresh:
        cached = _cache_get(query_for_search, ...)  # 不再 unbound
```

## 实战效果对比

**query "比亚迪股价"**:

| 阶段 | 8 条结果 | LLM 答案 |
|---|---|---|
| **v17.1 (无改写)** | 全是新闻 (5/2 销量飙升) | 幻觉: "94.78 元 -2.05%" (编的) |
| **v17.2 (加 "行情" 关键词)** | 5 条财经/资讯页 + 3 条新闻 | 诚实: "实时报价请查询东方财富..." |
| **v17.3 (前端答案卡片)** | 同上 | 同上, 但用玻璃态卡片展示 + 来源 chips |

**query "上证指数" (有数据时)**:
- v17.2: "上证指数最新报 4075.10 点, 涨幅 0.43%\n\n来源: finance.sina.com.cn / quote.eastmoney.com / sse.com.cn / finance.baidu.com"
- v17.3: 玻璃态卡片显示这段 + 4 个来源 chips (可点直达)

## 公网实测 (端到端 3.4s)

- **search 阶段**: 1.0s (7 引擎并发)
- **LLM 阶段**: 2.4s (DeepSeek-V4-Flash, 712 tokens)
- **前端**: 玻璃态卡片 slideUp 0.5s 动画 + 来源 chips 立即可点

## Pitfalls

1. **patch 工具要用唯一 anchor** + 验证 `grep` 没重复 `</style>`
2. **nginx static root 不等于 home dir** — 先 `cat conf` 确认
3. **sibling subagent 改过文件** — 必先 read 再 patch, 否则老 string 找不到
4. **finance 模式加 "行情"** 让搜实时报价页 (不是新闻), 否则 LLM 拿到新闻会编价格
5. **shimmer 动画** 用 `background-position` 200% 渐变, 比 border 闪烁优雅
6. **答案 toggle 默认 ON** — 用户进来就能用 Perplexity Mode, 不用找开关
