# 配置说明

## 目录结构

```
/root/monitoring/securities/
├── config/
│   └── sites.json          # 监控站点配置
├── scripts/
│   ├── crawl_all.sh        # 批量抓取主脚本
│   ├── crawl_generic.sh    # 通用抓取脚本
│   ├── crawl_*.sh          # 各站点专用脚本
│   ├── check_notifications.sh  # 检查通知脚本
│   └── send_wechat_notification.sh  # 发送通知脚本
├── YYYYMMDD/               # 按日期存储的抓取数据
│   ├── *.md               # Markdown格式页面
│   └── *_raw.json         # 原始JSON响应
├── latest_*.md            # 最新页面的软链接
└── test_diff.sh           # 测试脚本
```

## 定时任务配置

### 当前配置
```bash
# 每天早上9:00执行
0 9 * * * /root/monitoring/securities/scripts/crawl_all.sh >> /var/log/securities/cron.log 2>&1
```

### 修改定时任务
```bash
# 编辑crontab
crontab -e

# 常用时间表达式示例：
# 每6小时执行一次
0 */6 * * * ...

# 每2小时执行一次（8点-20点）
0 8-20/2 * * * ...

# 每小时执行一次
0 * * * * ...

# 每天凌晨2点执行
0 2 * * * ...
```

## 站点配置

### sites.json 格式
```json
[
  {
    "name": "站点名称",
    "url": "目标URL",
    "prefix": "文件前缀"
  }
]
```

### 添加新站点
1. 在 `config/sites.json` 中添加配置
2. 创建对应的 `crawl_${prefix}.sh` 脚本
3. 在 `crawl_all.sh` 中添加到脚本列表

## 日志文件

### 执行日志
- **位置**：`/var/log/securities/cron.log`
- **内容**：每次批量抓取的详细输出
- **查看**：`tail -f /var/log/securities/cron.log`

### 通知文件
- **位置**：`/tmp/securities_*_notification_*.txt`
- **内容**：站点更新通知消息
- **清理**：定期清理旧的通知文件

### 差异文件
- **位置**：`/tmp/securities_*_diff_*.txt`
- **内容**：详细的diff输出
- **格式**：diff -u 格式

## 环境变量

### crawl_generic.sh 使用的变量
- `BASE_DIR` - 监控系统根目录
- `TARGET_URL` - 目标URL
- `SITE_NAME` - 站点名称
- `FILE_PREFIX` - 文件前缀
- `WECHAT_OPEN_ID` - 企业微信用户ID

## 存储空间管理

### 定期清理旧数据
```bash
# 清理30天前的数据
find /root/monitoring/securities -type d -name "20??????" -mtime +30 -exec rm -rf {} \;

# 清理临时通知文件
find /tmp -name "securities_*.txt" -mtime +7 -delete
```

### 查看磁盘使用
```bash
# 查看监控系统占用空间
du -sh /root/monitoring/securities/

# 查看各日期目录大小
du -sh /root/monitoring/securities/20??????/ | sort -h
```
