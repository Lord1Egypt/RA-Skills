---
name: wechat-article-collector
description: 微信公众号文章批量采集工具。通过 Browser Harness 连接用户已登录的微信公众号后台，自动提取文章列表、去重、下载全文并保存到本地知识库。适用于个人公众号内容备份、知识库构建、文章管理等场景。
---

# 微信公众号文章采集器

通过 Browser Harness 自动采集微信公众号文章，支持去重、全文下载、本地存储。

## 功能特性

- ✅ 自动连接已登录的微信公众号后台
- ✅ 提取原创文章列表（标题、日期、链接）
- ✅ 智能去重（对比本地已收录文章）
- ✅ 批量下载文章全文
- ✅ 保存为 Markdown 格式
- ✅ 支持翻页获取所有文章

## 前置条件

1. **Browser Harness 已安装**（必需依赖）
   - 项目地址：https://github.com/browser-use/browser-harness
   - 安装位置：`~/.openclaw/workspace/browser-harness`
   - 命令行工具：`browser-harness`（已在 PATH）
   - Chrome 远程调试已授权
   - 安装方法：
     ```bash
     cd ~/.openclaw/workspace
     git clone https://github.com/browser-use/browser-harness
     cd browser-harness
     uv tool install -e .
     browser-harness --setup
     ```

2. **微信公众号后台已登录**
   - 在 Chrome 中打开 `https://mp.weixin.qq.com`
   - 登录你的公众号账号
   - 保持浏览器打开

## 使用方法

### 1. 快速采集（一键完成）

```bash
cd ~/.openclaw/workspace/skills/wechat-article-collector
python3 scripts/collect_articles.py
```

脚本会自动：
1. 连接到微信公众号后台
2. 进入原创文章页面
3. 提取所有文章列表
4. 对比本地知识库去重
5. 下载新文章全文
6. 保存到 `~/.openclaw/workspace/knowledge/wechat/gh_<公众号ID>/`

### 2. 分步执行

#### 步骤 1：提取文章列表

```bash
python3 scripts/extract_article_list.py
```

输出：`/tmp/all_articles.json`

#### 步骤 2：去重并下载

```bash
python3 scripts/download_new_articles.py
```

读取 `/tmp/all_articles.json`，对比本地知识库，下载新文章。

## 配置

编辑 `config.json` 自定义设置：

```json
{
  "save_dir": "~/.openclaw/workspace/knowledge/wechat/gh_511119f160d8",
  "mp_url": "https://mp.weixin.qq.com/cgi-bin/appmsgcopyright?action=orignal&type=1&token=YOUR_TOKEN",
  "sleep_between_downloads": 1.5
}
```

## 文件结构

```
wechat-article-collector/
├── SKILL.md                    # 本文件
├── config.json                 # 配置文件
├── scripts/
│   ├── collect_articles.py    # 一键采集脚本
│   ├── extract_article_list.py # 提取文章列表
│   ├── download_new_articles.py # 下载新文章
│   └── utils.py               # 工具函数
└── README.md                   # 详细文档
```

## 输出格式

每篇文章保存为独立的 Markdown 文件：

```
YYYY-MM-DD_文章标题.md
```

文件内容：

```markdown
# 文章标题

**发布日期**: YYYY-MM-DD

**原文链接**: http://mp.weixin.qq.com/s/xxxxx

---

文章正文内容...
```

## 故障排查

### 问题 1：Browser Harness 连接失败

**症状**：`daemon alive — run browser-harness --setup to attach`

**解决**：
```bash
browser-harness --doctor
browser-harness --setup
```

### 问题 2：提取不到文章列表

**症状**：`Total: 0 articles`

**原因**：未登录或未进入原创文章页面

**解决**：
1. 在 Chrome 中手动打开 `https://mp.weixin.qq.com`
2. 登录公众号
3. 点击左侧菜单"原创管理" → "原创声明"
4. 重新运行脚本

### 问题 3：文章内容提取失败

**症状**：`❌ 提取失败 (len=0)`

**原因**：页面加载慢或选择器不匹配

**解决**：
- 增加 `time.sleep()` 等待时间
- 检查微信公众号文章页面结构是否变化
- 更新选择器：`#js_content` 或 `.rich_media_content`

## 高级用法

### 自定义保存目录

```python
python3 scripts/collect_articles.py --save-dir ~/Documents/公众号备份
```

### 只提取列表不下载

```python
python3 scripts/extract_article_list.py --output /tmp/my_articles.json
```

### 指定公众号 ID

```python
python3 scripts/collect_articles.py --account-id gh_abc123def456
```

## 依赖

- **Browser Harness**: 浏览器自动化
- **Python 3.10+**: 脚本运行环境
- **Chrome**: 已登录微信公众号后台

## 注意事项

1. **登录态**：必须在 Chrome 中保持微信公众号后台登录
2. **速率限制**：下载间隔建议 ≥1.5 秒，避免触发反爬
3. **文件命名**：自动过滤特殊字符，避免文件系统冲突
4. **去重逻辑**：基于文件名模糊匹配，建议定期清理重复文件

## 扩展应用场景

基于 Browser Harness 的浏览器自动化能力，本 skill 可扩展到更多场景：

### 1. 内容采集类
- **社交媒体**：微博、小红书、知乎专栏、掘金文章
- **新闻资讯**：RSS 替代、新闻聚合、行业动态
- **电商数据**：价格监控、商品评论、销量趋势
- **招聘信息**：Boss、拉勾、猎聘职位聚合

### 2. 自动化操作类
- **批量操作**：回复评论、发布动态、点赞转发
- **表单填写**：报销申请、问卷调查、重复性表单
- **账号管理**：多平台内容同步、数据备份

### 3. 监控告警类
- **网页变化**：价格、库存、状态监控
- **关键词监控**：品牌舆情、竞品动态
- **系统状态**：后台面板、服务器监控

### 4. 数据导出类
- **财务数据**：发票下载、订单导出、账单备份
- **业务数据**：客户信息、交易记录、报表导出

### 如何扩展

1. **修改选择器配置**：编辑 `config.json` 中的 `profiles`
2. **自定义提取逻辑**：修改 `scripts/utils.py` 中的提取函数
3. **添加新功能**：在 `scripts/` 目录下创建新脚本

详见 `USAGE.md` 中的自定义配置教程。

## 快速扩展示例

### 支持其他公众号

修改 `config.json` 中的 `mp_url` 和 `save_dir`，可采集多个公众号。

### 定时采集

添加 cron 任务：

```bash
# 每天凌晨 2 点采集
0 2 * * * cd ~/.openclaw/workspace/skills/wechat-article-collector && python3 scripts/collect_articles.py
```

### 导出为其他格式

在 `scripts/utils.py` 中添加转换函数：

```python
def convert_to_pdf(md_file):
    # 使用 pandoc 或其他工具转换
    pass
```

## 许可

MIT License - 自由使用、修改、分发

## 贡献

欢迎提交 Issue 和 Pull Request！

---

**作者**: ZHAO  
**版本**: 1.0.0  
**更新日期**: 2026-04-22
