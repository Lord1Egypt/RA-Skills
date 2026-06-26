---
name: wechat-article-reader
description: 读取微信公众号文章，提取全文内容和图片，结合阅读分析。当用户提供 mp.weixin.qq.com 链接、让看公众号文章内容、或需要分析微信文章的文字和图片时使用。
---

# 微信公众号文章阅读器

## 概述

微信公众号使用懒加载机制，图片真实URL存储在 `data-src` 属性中。本skill提供完整的文章阅读流程：提取全文 + 内容图片 + 结合分析。

## 工作流程

### 1. 打开文章

```bash
agent-browser open "<文章URL>"
```

### 2. 滚动加载所有内容

微信文章使用懒加载，需要滚动到底部触发所有图片加载：

```bash
# 多次滚动确保加载完成
for i in {1..8}; do
  agent-browser scroll down 800
  sleep 1
done
```

### 3. 提取文章内容

```javascript
// 提取标题、作者、正文
const title = document.querySelector('#activity-name')?.innerText || '未找到标题';
const author = document.querySelector('#js_name')?.innerText || '';
const content = document.querySelector('#js_content')?.innerText || '';
```

执行方式：
```bash
agent-browser eval "<上述JS代码>"
```

### 4. 提取图片URL

微信图片存储在 `data-src` 属性，不在 `src`：

```javascript
// 提取所有懒加载图片的真实URL
const imgs = document.querySelectorAll('img');
const urls = [];
imgs.forEach((img) => {
  const dataSrc = img.getAttribute('data-src');
  if (dataSrc && dataSrc.startsWith('http')) {
    urls.push(dataSrc.split('#')[0]); // 去掉hash
  }
});
urls.join('\n');
```

### 5. 过滤内容图片

**内容图片特征：**
- 尺寸较大（width > 200 或 height > 200）
- 来自 `mmbiz.qpic.cn` 域名
- 格式为 png/jpg/gif/webp

**装饰图片特征（排除）：**
- 尺寸小（分隔线、图标）
- 文件大小 < 5KB
- 来自特定装饰图路径

### 6. 下载内容图片

```bash
# 创建目录
mkdir -p <输出目录>

# 下载图片
curl -o "img-01.png" "<图片URL>"
```

### 7. 结合阅读

1. 读取正文内容
2. 逐一查看内容图片
3. 将图片与对应段落关联
4. 输出完整分析报告

## 快速脚本

使用 `scripts/read_article.sh` 一键执行：

```bash
./scripts/read_article.sh "<文章URL>" <输出目录>
```

输出：
- `article.json` - 标题、作者、正文
- `images/` - 内容图片目录
- `summary.md` - 结合阅读摘要

## 图片过滤规则

| 类型 | 特征 | 处理 |
|------|------|------|
| 内容图片 | 尺寸 > 200px, 来自 mmbiz.qpic.cn | 下载并分析 |
| 装饰分隔 | 高度 < 50px 或 文件 < 2KB | 忽略 |
| 公众号图标 | 含 "yZPTcMGWibvsic9Obib" 等固定路径 | 忽略 |
| 表情包/贴纸 | 尺寸 < 100px | 忽略 |

## 输出格式

```markdown
## 文章标题

**作者：** XXX

### 正文 + 图片

> 段落内容...

配图：[图片描述]

> 继续段落...

### 图片汇总

| 图片 | 内容 | 关联段落 |
|------|------|----------|
| img-01.png | 游戏截图 | 第一节 |
| img-02.png | 数据图表 | 第三节 |
```