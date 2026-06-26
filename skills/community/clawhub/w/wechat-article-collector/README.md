# 微信公众号文章采集器

自动采集微信公众号文章到本地知识库，支持去重、全文下载、Markdown 存储。

## 快速开始

```bash
# 1. 确保 Browser Harness 已安装并连接
browser-harness --doctor

# 2. 在 Chrome 中登录微信公众号后台
# 打开 https://mp.weixin.qq.com 并登录

# 3. 进入原创文章页面
# 点击左侧菜单"原创管理" → "原创声明"

# 4. 运行采集脚本
cd ~/.openclaw/workspace/skills/wechat-article-collector
python3 scripts/collect_articles.py
```

## 工作流程

1. **连接浏览器**：通过 Browser Harness 连接已登录的 Chrome
2. **提取列表**：从原创文章页面提取所有文章（标题、日期、链接）
3. **智能去重**：对比本地知识库，找出未收录的文章
4. **下载全文**：逐个打开文章链接，提取正文内容
5. **保存文件**：以 `YYYY-MM-DD_标题.md` 格式保存

## 技术栈

- **Browser Harness**：浏览器自动化（CDP 协议）
- **Python 3.10+**：脚本语言
- **Unix Socket**：与 Browser Harness daemon 通信
- **JSON**：数据交换格式

## 核心特性

### 1. 智能去重

基于文件名模糊匹配，避免重复下载：

```python
# 已存在：2026-03-25_给OpenClaw当爹日志0325之向量索引报错.md
# 新文章：给OpenClaw当爹日志0325之向量索引报错
# 结果：跳过（标题匹配）
```

### 2. 容错机制

- 页面加载失败：自动重试
- 内容提取失败：记录日志并跳过
- 网络超时：设置合理超时时间

### 3. 速率控制

下载间隔 1.5 秒，避免触发反爬：

```json
{
  "sleep_between_downloads": 1.5
}
```

## 配置说明

编辑 `config.json`：

```json
{
  "save_dir": "~/.openclaw/workspace/knowledge/wechat",
  "sleep_between_downloads": 1.5,
  "wait_after_page_load": 3,
  "max_pages": 50,
  "articles_per_page": 10
}
```

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `save_dir` | 保存目录 | `~/.openclaw/workspace/knowledge/wechat` |
| `sleep_between_downloads` | 下载间隔（秒） | 1.5 |
| `wait_after_page_load` | 页面加载等待（秒） | 3 |
| `max_pages` | 最大翻页数 | 50 |
| `articles_per_page` | 每页文章数 | 10 |

## 输出示例

```
=== 微信公众号文章采集器 ===

[1/5] 检查 Browser Harness...
✅ Browser Harness 就绪

[2/5] 连接微信公众号后台...
✅ 已连接公众号: gh_511119f160d8

[3/5] 提取文章列表...
✅ 提取到 10 篇文章

[4/5] 对比本地知识库去重...
✅ 需要下载 7 篇新文章

[5/5] 下载新文章全文...
[1/7] 给OpenClaw当爹日志0415之自动上下文管理
  ✅ 已保存
[2/7] 给OpenClaw当爹日志0413—Syncthing 外置硬盘"降温"实战
  ✅ 已保存
...

=== 完成 ===
成功下载: 7/7 篇
保存位置: /Users/xxx/.openclaw/workspace/knowledge/wechat/gh_511119f160d8
```

## 故障排查

### 问题 1：Browser Harness 未就绪

```bash
❌ Browser Harness 未就绪，请先运行: browser-harness --setup
```

**解决**：

```bash
browser-harness --doctor
browser-harness --setup
```

### 问题 2：未找到公众号后台

```bash
❌ 未找到微信公众号后台页面，请先在 Chrome 中登录
```

**解决**：

1. 打开 Chrome
2. 访问 `https://mp.weixin.qq.com`
3. 登录公众号
4. 重新运行脚本

### 问题 3：提取不到文章

```bash
❌ 未提取到文章，请检查是否在原创文章页面
```

**解决**：

1. 在公众号后台点击"原创管理" → "原创声明"
2. 确保页面显示文章列表
3. 重新运行脚本

## 扩展用法

### 定时采集

添加 cron 任务：

```bash
# 每天凌晨 2 点采集
0 2 * * * cd ~/.openclaw/workspace/skills/wechat-article-collector && python3 scripts/collect_articles.py >> /tmp/wechat_collector.log 2>&1
```

### 多公众号采集

修改 `utils.py` 中的 `get_account_id()` 函数，支持多账号：

```python
def get_account_id():
    # 从 URL 或页面元素提取真实公众号 ID
    # 返回格式：gh_xxxxxx
    pass
```

### 导出为 PDF

安装 `pandoc`：

```bash
brew install pandoc

# 转换单个文件
pandoc input.md -o output.pdf

# 批量转换
for f in *.md; do pandoc "$f" -o "${f%.md}.pdf"; done
```

## 许可

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

## 作者

ZHAO - 2026-04-22

## 致谢

- [Browser Harness](https://github.com/browser-use/browser-harness) - 浏览器自动化框架
- [OpenClaw](https://openclaw.ai) - AI 助手平台
