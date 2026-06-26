# Automation Scripts 🤖

自动化脚本集合。

## 安装

```bash
npx clawhub@latest install automation-scripts
```

## 脚本列表

1. 批量重命名
2. 自动备份
3. 网页截图
4. 数据抓取
5. 定时任务

## 示例

### 备份工作目录

```bash
clawhub auto backup --source ~/workspace --dest ~/backup/daily
```

### 定时截图监控

```bash
clawhub auto schedule --cron "*/30 * * * *" \
  --command "screenshot --url https://example.com"
```
