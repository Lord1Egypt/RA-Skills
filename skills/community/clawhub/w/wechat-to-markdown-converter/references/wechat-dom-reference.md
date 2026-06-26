# 微信公众号文章 DOM 结构参考

> 本文档记录微信公众号文章页面的 HTML/CSS 结构，用于指导内容提取和转换逻辑。
> 最后更新: 2026-04-08

---

## 1. 页面整体结构

```
html
├── head
│   ├── title                          # 文章标题
│   ├── meta[property="og:title"]      # 分享标题
│   ├── meta[property="article:published_time"]  # 发布时间
│   ├── meta[name="description"]       # 文章描述
│   └── script (大量内联JS)
└── body
    ├── #js_profile_arrow              # 返回按钮区
    ├── #activity-name                 # 文章标题（h1）
    ├── .rich_media_meta               # 元信息区
    │   ├── .rich_media_meta_primary_category_time  # 分类+时间
    │   │   └── #publish_time          # 发布时间
    │   ├── #js_name                   # 公众号名称
    │   └── .rich_media_meta_nickname_extra
    ├── .rich_media_content            # ★ 文章正文容器（核心）
    ├── #js_content                    # ★ 文章正文（核心，与上面二选一）
    ├── #js_tags_wrap                  # 标签区（噪声）
    ├── #js_cmt_area                   # 评论区（噪声）
    ├── .rich_media_tool               # 工具栏（噪声）
    ├── .rich_media_footer             # 页脚（噪声）
    ├── #page_bottom                   # 页面底部（噪声）
    └── #js_pc_close                   # 关闭按钮（噪声）
```

### 正文容器选择器（优先级）

1. `#js_content` — 最常用，绝大多数文章
2. `.rich_media_content` — 部分旧版文章
3. `#page-content` — 极少情况

---

## 2. 元数据提取

| 字段 | 选择器 | 备注 |
|------|--------|------|
| 标题 | `#activity-name`, `#js_activity_name`, `h1.rich_media_title` | 多选器兼容 |
| 公众号名称 | `#js_name`, `.profile_nickname`, `a.rich_media_meta_link` | |
| 发布时间 | `#publish_time`, `em#publish_time`, `meta[property="article:published_time"]` | 可能需要解析 |
| 文章描述 | `meta[name="description"]` | |
| 原文链接 | 当前 URL | |

---

## 3. 正文内容元素

### 3.1 标题

```html
<!-- H2 标题 -->
<h2 style="text-align: center; font-size: 22px;">标题文本</h2>

<!-- 自定义标题（通过 section 模拟） -->
<section style="font-size: 22px; font-weight: bold;">标题文本</section>

<!-- H1 标题（少见） -->
<h1 class="rich_media_title">标题文本</h1>
```

**特征**：字号 ≥ 22px 通常为二级标题，≥ 19px 为三级标题。

### 3.2 段落

```html
<p>正文段落</p>

<!-- 微信常见的带样式段落 -->
<p style="text-indent: 2em; line-height: 2;">首行缩进段落</p>
<p style="text-align: center;">居中段落</p>
<p style="text-align: right;">右对齐段落</p>
```

### 3.3 加粗与斜体

```html
<strong>加粗文本</strong>
<b>加粗文本</b>
<em>斜体文本</em>
<i>斜体文本</i>
<span style="font-weight: bold;">内联加粗</span>
<span style="font-style: italic;">内联斜体</span>
```

### 3.4 列表

```html
<!-- 微信不使用标准 ol/ul，而是通过 p + 特殊字符模拟 -->
<p>• 无序列表项 1</p>
<p>• 无序列表项 2</p>
<p>· 另一种无序列表</p>

<p>1. 有序列表项 1</p>
<p>2. 有序列表项 2</p>

<p>(1) 括号式有序列表</p>
<p>(2) 括号式有序列表</p>

<!-- 偶尔使用标准列表 -->
<ul><li>标准无序</li></ul>
<ol><li>标准有序</li></ol>
```

**列表标记字符**：`•` `·` `◦` `▪` `▫` `–` `-` `●` `○` `◆` `◇` `►` `▸` `■` `□`

### 3.5 引用块

```html
<!-- 标准引用 -->
<blockquote>引用内容</blockquote>

<!-- 微信自定义引用（通过 section + 左边框模拟） -->
<section style="border-left: 4px solid #xxx; padding-left: 10px;">
  引用内容
</section>
```

### 3.6 图片

```html
<!-- 微信懒加载图片（核心） -->
<img
  data-src="https://mmbiz.qpic.cn/mmbiz_png/xxx/640?wx_fmt=png"
  src=""                     ← 可能为空
  data-type="png"
  data-w="1080"
  data-ratio="0.75"
  style="width: 100%;"
/>

<!-- 普通图片 -->
<img src="https://mmbiz.qpic.cn/mmbiz_jpg/xxx/640?wx_fmt=jpg" alt="" />

<!-- 带说明的图片 -->
<img data-src="https://mmbiz.qpic.cn/..." />
<p style="text-align: center; font-size: 12px; color: #999;">图片说明</p>
```

**关键要点**：
- 图片真实 URL 在 `data-src` 属性中，`src` 常为空
- 域名通常为 `mmbiz.qpic.cn`（图片CDN）
- `data-type` 标明图片格式
- `data-w` 和 `data-ratio` 标明原始尺寸

### 3.7 链接

```html
<!-- 文章内链接 -->
<a href="https://mp.weixin.qq.com/s/xxx" target="_blank">链接文本</a>

<!-- 外部链接（微信可能包装） -->
<a href="javascript:void(0);" data-url="https://example.com">外部链接</a>
```

### 3.8 表格

```html
<table>
  <thead>
    <tr><th>表头1</th><th>表头2</th></tr>
  </thead>
  <tbody>
    <tr><td>数据1</td><td>数据2</td></tr>
  </tbody>
</table>

<!-- 微信表格常带大量内联样式 -->
<table style="border-collapse: collapse; width: 100%;">
```

---

## 4. 代码块结构（重点）

微信有 **3 种代码块格式**，需要全部兼容：

### 格式 1：`pre.code-snippet`（最新版）

```html
<pre class="code-snippet" data-lang="python">
  <code class="language-python">
    <!-- 代码内容 -->
  </code>
</pre>
```

### 格式 2：`.code-snippet__fix` 容器（常见）

```html
<div class="code-snippet__fix code-snippet__js">
  <div class="code-snippet__header">
    <span class="code-snippet__lang">python</span>
    <button class="code-snippet__copy">复制</button>
  </div>
  <div class="code-snippet__body">
    <pre data-lang="python">
      <code>
        <!-- 代码内容 -->
      </code>
    </pre>
  </div>
  <div class="code-snippet__line-index">
    <span>1</span><span>2</span>...  <!-- 行号，需移除 -->
  </div>
</div>
```

### 格式 3：`pre[data-lang]`（简化版）

```html
<pre data-lang="javascript">
  <code>
    // 代码内容
    console.log("hello");
  </code>
</pre>
```

### 代码块处理要点

1. **语言检测**：优先读取 `data-lang` 属性，其次检查 CSS class（`language-xxx`），最后通过代码内容自动推断
2. **行号移除**：`.code-snippet__line-index` 和 `[class*='line-number']` 必须移除
3. **CSS 泄漏过滤**：微信代码块常泄漏 `counter(line)` 等垃圾文本，需通过正则过滤
4. **复制按钮移除**：`.code-snippet__copy` / `.code-snippet__header` 不需要保留
5. **占位符策略**：代码块先提取内容，替换为占位符 `__CODEBLOCK_N__`，HTML→MD 转换后再还原为围栏代码块

---

## 5. 需要移除的噪声元素

### 5.1 广告与推广

| 选择器 | 说明 |
|--------|------|
| `.mp_profile_iframe` | 公众号名片 |
| `#js_pc_close` | PC 端关闭按钮 |
| `.qr_code_pc` | PC 端二维码 |
| `#ad_content` | 广告内容 |
| `.mp-ad` | 广告模块 |

### 5.2 赞赏与打赏

| 选择器 | 说明 |
|--------|------|
| `.reward_area` | 赞赏区域 |
| `#reward_area` | 赞赏区域（ID） |
| `.rewards_area` | 赞赏区域 |
| `.reward_qrcode_area` | 赞赏二维码 |

### 5.3 评论区

| 选择器 | 说明 |
|--------|------|
| `#comment_container` | 评论容器 |
| `.discuss_container` | 讨论容器 |
| `#js_cmt_area` | 评论区域 |

### 5.4 音频与视频

| 选择器 | 说明 |
|--------|------|
| `mpvoice` | 音频播放器 |
| `.mp_voice_inner` | 音频内部 |
| `mpvideo` | 视频播放器 |
| `.mp_video_inner` | 视频内部 |

### 5.5 页面组件

| 选择器 | 说明 |
|--------|------|
| `.rich_media_tool` | 工具栏 |
| `.rich_media_footer` | 页脚 |
| `#page_bottom` | 页面底部 |
| `#js_bottom_ad_area` | 底部广告 |
| `#relation_article` | 相关文章推荐 |
| `#recommend_article` | 推荐文章 |
| `#js_tags_wrap` | 标签区 |
| `#copyright_area` | 版权声明 |

### 5.6 脚本与样式

| 选择器 | 说明 |
|--------|------|
| `script` | JavaScript |
| `style` | CSS 样式 |
| `noscript` | 无脚本提示 |

---

## 6. 特殊情况处理

### 6.1 验证码页面

```
特征: 页面包含 "验证码" 文本和 captcha 相关元素
处理: 报错提示用户等待后重试
```

### 6.2 内容为空

```
特征: #js_content 不存在或内容为空
处理: 抛出 ParseError
```

### 6.3 图片以 SVG/图片代码块形式呈现

```
特征: 代码块内容实际是一张图片（img 标签在 pre 内）
处理: 跳过文本提取，保留图片引用
```

### 6.4 嵌套 section 深度过深

```
特征: 微信编辑器产生多层嵌套 section
处理: 递归展平，将 section 转换为语义化标签或移除
```

### 6.5 内容中使用特殊符号

```
特征: 微信可能使用特殊 Unicode 字符作为列表标记
处理: 检测并转换为标准 Markdown 列表语法
```

---

## 7. URL 格式

### 标准文章 URL

```
https://mp.weixin.qq.com/s/xxxxxxxxxxxxx
https://mp.weixin.qq.com/s?__biz=xxx&mid=xxx&idx=xxx&sn=xxx
```

### 短链接

```
https://mp.weixin.qq.com/s/xxxxx（短格式）
wxf://...（微信内部链接，不适用）
```
