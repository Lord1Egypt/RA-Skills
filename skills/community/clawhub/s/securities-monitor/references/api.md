# API 说明

## XCrawl Scrape API

### 端点
```
POST https://run.xcrawl.com/v1/scrape
```

### 请求头
```
Content-Type: application/json
Authorization: Bearer ${XCRAWL_API_KEY}
```

### 请求体
```json
{
  "url": "目标URL",
  "mode": "sync",
  "js_render": {
    "enabled": true,
    "wait_until": "networkidle"
  },
  "output": {
    "formats": ["markdown", "links"]
  }
}
```

### 响应格式
```json
{
  "scrape_id": "抓取ID",
  "endpoint": "scrape",
  "version": "版本号",
  "status": "completed",
  "url": "请求的URL",
  "data": {
    "markdown": "Markdown格式内容",
    "links": "链接列表"
  }
}
```

## 企业微信消息 API

### 使用 message 工具发送

#### 方式一：通过 AI Agent 发送
在对话中请求发送消息，AI会使用 `message` 工具：

```json
{
  "name": "message",
  "parameters": {
    "action": "send",
    "channel": "wecom",
    "to": "yumin1_cj",
    "message": "消息内容"
  }
}
```

#### 响应格式
```json
{
  "channel": "wecom",
  "to": "yumin1_cj",
  "via": "gateway",
  "result": {
    "runId": "运行ID",
    "messageId": "消息ID",
    "channel": "wecom",
    "chatId": "yumin1_cj"
  }
}
```

### 方式二：wecom_mcp 工具（当前有问题）

错误码：846610
```
unsupported mcp biz type
```

建议使用 `message` 工具替代。

## 脚本 API

### crawl_all.sh
批量抓取所有站点。

**用法：**
```bash
bash /root/monitoring/securities/scripts/crawl_all.sh
```

**输出：**
- 执行日志到 stdout
- 详细日志到 `/var/log/securities/cron.log`

### crawl_generic.sh
通用抓取脚本，由各站点脚本调用。

**环境变量：**
- `BASE_DIR` - 根目录
- `TARGET_URL` - 目标URL
- `SITE_NAME` - 站点名称
- `FILE_PREFIX` - 文件前缀

**用法：**
```bash
BASE_DIR="/path" TARGET_URL="url" SITE_NAME="name" FILE_PREFIX="prefix" \
  bash /root/monitoring/securities/scripts/crawl_generic.sh
```

### check_notifications.sh
检查待发送的通知。

**用法：**
```bash
bash /root/monitoring/securities/scripts/check_notifications.sh
```

**输出：**
- 发现的通知列表
- 通知内容预览

### send_wechat_notification.sh
准备企业微信通知（需要AI Agent配合发送）。

**用法：**
```bash
bash /root/monitoring/securities/scripts/send_wechat_notification.sh /path/to/notification.txt
```

## 文件格式

### Markdown 页面文件
- 位置：`/root/monitoring/securities/YYYYMMDD/${prefix}_HHMMSS.md`
- 格式：纯Markdown文本
- 内容：XCrawl抓取的页面内容

### 原始 JSON 文件
- 位置：`/root/monitoring/securities/YYYYMMDD/${prefix}_HHMMSS_raw.json`
- 格式：JSON
- 内容：XCrawl API的完整响应

### 通知文件
- 位置：`/tmp/securities_${prefix}_notification_HHMMSS.txt`
- 格式：纯文本
- 内容：格式化的通知消息

### 差异文件
- 位置：`/tmp/securities_${prefix}_diff_HHMMSS.txt`
- 格式：diff -u 格式
- 内容：前后版本的差异对比
