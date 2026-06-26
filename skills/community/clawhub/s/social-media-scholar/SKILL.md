---
name: social-media-scholar
description: 把论文帖分享给我，我帮你加进zotero：从公众号/小红书/X等社交媒体文章链接提取论文信息，将论文保存到 Zotero 文库。(When you share a link of social media article that contains citation a paper, this skill can extract the paper information and save it to Zotero library.)
homepage: https://www.zotero.org
metadata:
  {
    "openclaw": {
      "emoji": "📚",
      "requires": {
        "bins": ["python"],
        "env": ["ZOTERO_CREDENTIALS"]
      },
      "primaryEnv": "ZOTERO_CREDENTIALS",
      "optional": {
        "bins": ["security"]
      },
      "install": [
        {
          "id": "python",
          "kind": "system",
          "label": "Install Python 3.10+"
        },
        {
          "id": "pip_deps",
          "kind": "pip",
          "packages": ["pyzotero"],
          "label": "Install Python dependencies (pyzotero)"
        }
      ]
    }
  }
---

# Social Media Scholar
当用户分享包含citation/链接/论文解读分享时，此 Skill 可以自动提取论文信息并保存到 Zotero 文库。
支持以下场景：

1. **直接保存论文**：将论文元数据、PDF 链接以及 AI 生成的总结一键保存到 Zotero
2. **从公众号/小红书/X等社交媒体保存**：分享公众号或小红书或X等社交媒体文章链接，自动提取论文信息并保存，文章内容作为笔记附加

## 使用说明

此 Skill 依赖本机安装的 Python（建议 Python 3.10 或更高版本）。

API Key 安全存储在 **macOS Keychain** 中，避免明文存储风险；

在非macOS环境中，采用环境变量 `ZOTERO_CREDENTIALS` 存储，格式为：

```bash
userid:apiKey
```
注意：最终回复语言要根据用户触发的query语言而定，不一定是中文。/
Note: The final response language depends on the user's query language and is not necessarily in Chinese.


## 首次配置

### 如果是macOS：
将你的 Zotero API Key 存入 Keychain：

```bash
security add-generic-password \
  -a "openclaw-zotero" \
  -s "openclaw-zotero" \
  -l "OpenClaw Zotero API Key" \
  -w "你的userid:你的API_Key"
```

如需更新密钥，添加 `-U` 参数：

```bash
security add-generic-password -U -s "openclaw-zotero" -w "你的userid:新的API_Key"
```

### 如果是其他系统：
采用环境变量 `ZOTERO_CREDENTIALS` 存储，格式为：

```bash
userid:apiKey
```

例如在 Windows PowerShell 中：

```powershell
$env:ZOTERO_CREDENTIALS="你的userid:你的apiKey"
```

例如在 Windows CMD 中：

```cmd
set ZOTERO_CREDENTIALS=你的userid:你的apiKey
```

## 使用方式
1. 用户输入包含链接的论文/论文解读分享，以及用户的需求

2. 分析用户提供的链接以及用户需求，判断是直接的论文标题（或者citation），还是论文链接（通常是 arXiv、PubMed 等）还是社交媒体链接（社交媒体链接通常形如 https://mp.weixin.qq.com/s/xxx 或  https://xhslink.com 或 https://x.com/xxx 等）

3. 
  直接的论文标题（或者citation）->方式一；
  论文链接（通常是 arXiv、PubMed 等）->方式二；
  社交媒体链接->方式三；

  ### 方式一：直接的论文标题
  ```
  保存论文：标题=xxx, 作者=xxx
  ```
  ```
  保存论文xxxxxxx,doi: xxx
  ```
  去检索论文对应的链接（通常是 arXiv、PubMed 等），并保存到 Zotero。  
  利用 `save_paper.py` 脚本保存论文：
  ```bash
  python {baseDir}/scripts/save_paper.py \
    --title "Attention Is All You Need" \
    --authors "Vaswani et al." \
    --url "https://arxiv.org/abs/1706.03762"
  ```

  ### 方式二：论文链接
  ```
  保存论文：标题=xxx, 作者=xxx, 链接=https://arxiv.org/abs/xxx
  ```
  提供论文标题、作者、链接即可：
  去检索论文对应的链接（通常是 arXiv、PubMed 等），并保存到 Zotero。  
  利用 `save_paper.py` 脚本保存论文：
  ```bash
  python {baseDir}/scripts/save_paper.py \
    --title "Attention Is All You Need" \
    --authors "Vaswani et al." \
    --url "https://arxiv.org/abs/1706.03762"
  ```


  ### 方式三：从公众号/小红书/X等社交媒体保存

  用户直接分享文章链接和指定要求：
  **示例**：
  ```
  把这个里面提及的论文 https://mp.weixin.qq.com/s/xxx 加入 Zotero
  ```
  1) 利用`网页内容爬取方法`，打开链接，提取文章中提及的论文信息（标题、作者、arXiv 链接等）；如果用户有截图，直接利用图片中解析的文字提取论文信息也可以。
  2) 去**检索**提及的论文，保存论文本体到 Zotero
  利用 `save_paper.py` 脚本保存论文：
  ```bash
  python {baseDir}/scripts/save_paper.py \
    --title "Attention Is All You Need" \
    --authors "Vaswani et al." \
    --url "https://arxiv.org/abs/1706.03762"
  ```
  3) 自动下载并附加 PDF（支持 arXiv）
  4) 将公众号/小红书文章内容作为笔记附加

4. 如果save_paper.py报错zotero连接失败，要求用户检查是否已正确配置 API Key。

## 依赖安装

请先在本机安装 Python 依赖：

```bash
pip install pyzotero
```

## 参数说明（save_paper.py）

| 参数 | 说明 |
|------|------|
| `--title` | 论文标题 |
| `--authors` | 作者列表（逗号分隔） |
| `--url` | 论文链接（用于排重） |
| `--abstract` | 论文摘要 |
| `--summary` | AI 生成的简短总结或 Insight（支持 HTML） |
| `--tags` | 标签列表（逗号分隔） |


## 网页内容爬取方法

公众号、小红书等复杂网页通常有动态加载和反爬机制，推荐以下方法：

### 方法一：web_fetch（优先尝试，快速但可能截断）

```python
# 使用 web_fetch 工具快速获取
# 优点：速度快，无需启动浏览器
# 缺点：复杂页面内容可能被截断
```

适用于：简单页面、纯文本内容。
如果获取内容包含人机验证，建议使用方法二。

### 方法二：browser + snapshot（推荐）

公众号等复杂页面需要用浏览器自动化：

```
1. browser action=start profile=openclaw
   # 启动浏览器

2. browser action=navigate url=https://mp.weixin.qq.com/s/xxx
   # 访问目标链接

3. browser action=snapshot
   # 获取页面完整结构化内容（包含标题、作者、正文、链接等）
```

**优点**：
- 获取完整内容，不会截断
- 可以提取页面中的所有链接（如 arXiv、GitHub）
- 支持动态加载的页面

**提取论文信息的技巧**：
- 查找 `arxiv.org/abs/` 链接获取论文 URL
- 查找 `github.com/` 链接获取代码仓库
- 查找标题附近的作者信息
- 查找 "arXiv"、"论文" 等关键词定位论文信息

### 内容整理格式

将公众号内容整理为 HTML 笔记：

```html
<h2>来源：{来源名称}</h2>
<p>原文链接：<a href="{url}">{标题}</a></p>
<p>发布时间：{日期}</p>

<h3>文章摘要</h3>
<p>{摘要内容}</p>

<h3>核心亮点</h3>
<ul>
<li>{亮点1}</li>
<li>{亮点2}</li>
</ul>

<h3>资源链接</h3>
<ul>
<li>arXiv: {arxiv_url}</li>
<li>GitHub: {github_url}</li>
</ul>
```
