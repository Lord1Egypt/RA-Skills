# 小红书博主监测 Skill

监测指定小红书博主是否有新帖子，并通过飞书通知用户。

## 功能

- ✅ 自动检测多个小红书博主新帖子
- ✅ 根据时间段调整监控频率（08:00-18:00 每5分钟，18:00-24:00 每10分钟）
- ✅ 00:00-08:00 不监控
- ✅ 飞书通知推送
- ✅ 帖子快照对比，避免重复通知
- ✅ 支持登录态（保持 cookie）
- ✅ 路径动态获取，适配不同用户

## 监控的博主

1. **还是叫吴富贵吧**
   - ID: 5b6150c56b58b741e26b8c7f
   - 主页: https://www.xiaohongshu.com/user/profile/5b6150c56b58b741e26b8c7f

## 文件结构

```
~/.openclaw/workspace/
├── scripts/
│   └── xiaohongshu-monitor.sh    # 主监测脚本
└── memory/
    ├── xiaohongshu-monitor-还是叫吴富贵吧.md    # 博主1帖子快照
    ├── xiaohongshu-monitor-还是叫吴富贵吧.log   # 博主1日志
    └── xiaohongshu-cron.log                     # Cron运行日志
```

## 脚本配置

脚本使用动态路径，适配不同用户：

```bash
export PATH="..."  # 使用 $HOME 动态获取
WORKSPACE="$HOME/.openclaw/workspace"
```

博主观测配置在 `BLOGGERS` 数组中：

```bash
BLOGGERS=(
    "ID|博主名|快照文件|日志文件"
)
```

## 使用方法

### 1. 手动运行检测

```bash
bash ~/.openclaw/workspace/scripts/xiaohongshu-monitor.sh
```

### 2. 查看日志

```bash
# 查看所有日志
tail -f ~/.openclaw/workspace/memory/xiaohongshu-cron.log

# 查看特定博主日志
tail -f ~/.openclaw/workspace/memory/xiaohongshu-monitor-还是叫吴富贵吧.log
```

### 3. 查看当前快照

```bash
cat ~/.openclaw/workspace/memory/xiaohongshu-monitor-还是叫吴富贵吧.md
```

### 4. Cron 任务配置

```bash
# 查看当前 cron
crontab -l

# 当前配置:
# */5 8-18 * * *  (08:00-18:00 每5分钟)
# */10 18-23 * * * (18:00-24:00 每10分钟)
```

### 5. 修改或停止 Cron

```bash
# 编辑 crontab
crontab -e

# 停止所有任务
crontab -r
```

## 首次设置

### 1. 登录小红书（保持 cookie）

首次使用需要在浏览器中登录小红书一次，之后脚本会自动使用登录态：

```bash
openclaw browser --profile openclaw open "https://www.xiaohongshu.com"
```

在弹出的浏览器中登录小红书即可。

### 2. 验证登录态

首次设置后手动运行一次检测脚本，确认正常工作：

```bash
bash ~/.openclaw/workspace/scripts/xiaohongshu-monitor.sh
```

## 通知效果

当有新帖子时，你会收到飞书通知：

```
🔔 小红书博主「还是叫吴富贵吧」发新帖子啦：

1. 新帖子标题1
2. 新帖子标题2
```

## 添加新博主

如果要添加新博主，修改脚本中的 `BLOGGERS` 数组：

```bash
BLOGGERS=(
    "5b6150c56b58b741e26b8c7f|还是叫吴富贵吧|xiaohongshu-monitor-还是叫吴富贵吧.md|xiaohongshu-monitor-还是叫吴富贵吧.log"
    "新博主ID|新博主名字|xiaohongshu-monitor-新博主名字.md|xiaohongshu-monitor-新博主名字.log"
)
```

格式：`ID|名字|快照文件|日志文件`

## 注意事项

- 浏览器使用 `openclaw` profile，数据保存在 `~/.openclaw/browser/openclaw/`
- 小红书有频率限制，脚本已内置重试机制
- 频繁请求可能触发"请求太频繁"，脚本会自动等待后重试
- 监控时间：00:00-08:00 不监控，08:00-18:00 每5分钟，18:00-24:00 每10分钟
- 中文文件名在 Mac/Linux 系统上完全兼容
