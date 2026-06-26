# BOSS直聘手机号提取器 - 配置指南

## 安装依赖

### 1. 安装 Python 依赖

```bash
pip install playwright
playwright install chromium
```

### 2. 验证安装

```bash
python scripts/extract_phones.py --help
```

## 首次使用

### 1. 手动登录

首次使用需要手动登录 BOSS直聘：

```bash
# 使用非无头模式，可以看到浏览器界面
python scripts/extract_phones.py
```

脚本会打开浏览器，等待你手动登录。

### 2. 保存登录状态

Playwright 会自动保存 cookies，下次使用时无需重新登录。

## 使用示例

### 基本使用
```bash
# 提取所有新消息中的手机号
python scripts/extract_phones.py
```

### 指定输出文件
```bash
python scripts/extract_phones.py --output ~/Documents/contacts.txt
```

### 限制提取数量
```bash
# 只提取前 10 条消息
python scripts/extract_phones.py --limit 10
```

### 无头模式（后台运行）
```bash
# 不显示浏览器窗口，适合定时任务
python scripts/extract_phones.py --headless
```

## 定时任务配置

### macOS/Linux (crontab)

```bash
# 编辑 crontab
crontab -e

# 每 30 分钟检查一次
*/30 * * * * cd ~/.openclaw/workspace/skills/zhipin-phone-extractor && python scripts/extract_phones.py --headless
```

### 配合 OpenClaw 心跳

在 `HEARTBEAT.md` 中添加：

```markdown
## 3. BOSS直聘新消息
- 每 2 小时检查一次新消息
- 如有新手机号，发送提醒到 Telegram
```

## 故障排查

### 问题 1: Playwright 安装失败

```bash
# 使用国内镜像
export PLAYWRIGHT_DOWNLOAD_HOST=https://npmmirror.com/mirrors/playwright/
playwright install chromium
```

### 问题 2: 找不到消息元素

BOSS直聘可能更新了页面结构，需要更新选择器：

```python
# 在 extract_phones.py 中更新选择器
message_items = await page.query_selector_all('.新的选择器')
```

### 问题 3: 验证码拦截

如果频繁访问触发验证码：

1. 降低检查频率
2. 使用代理 IP
3. 手动处理验证码后继续

## 扩展开发

### 支持其他招聘平台

参考 `extract_phones.py`，可以创建类似的脚本：

- `extract_liepin.py` - 猎聘
- `extract_zhaopin.py` - 智联招聘
- `extract_lagou.py` - 拉勾

### 添加通知功能

在 `_save_results()` 方法中添加：

```python
# 发送到 Telegram
import requests
requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={
    "chat_id": CHAT_ID,
    "text": f"新提取 {len(unique_phones)} 个手机号！"
})
```

## 数据格式

输出文件格式：

```
=== 2026-03-11 14:44:00 ===
张经理 - 13800138000 - 腾讯科技
李HR - 13900139000 - 字节跳动
王总 - 13700137000 - 阿里巴巴
```

可以轻松导入到 Excel 或其他工具中。
