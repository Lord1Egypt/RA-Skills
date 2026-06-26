# Morning Briefing Integration

## Cron 配置

Morning Briefing cron 的 payload message：

```
Read scripts/morning-briefing-instructions.md for instructions.
```

完整指令文件见：`scripts/morning-briefing-instructions.md`

## 晨报执行流程

```
1. 运行清理脚本（删除过期行程）
   python3 skills/travel-morning-weather/scripts/travel-cleaner.py

2. 读取 travel-plan.json，获取 today 对应的地点
   - 有匹配 → 使用该地点
   - 无匹配 → 使用 default_location

3. 查询天气
   curl -s "wttr.in/<City,Country>?format=%l:+%c+%t+(feels+like+%f)"

4. 整合晨报
   开头播报天气 + 今日日程 + 其他提醒
```

## 天气播报格式

**在旅行中**：
```
🌍 早安，主人！您在巴黎，今天多云，12°C（体感 10°C）
```

**在家中**：
```
☀️ 早安！您在家中，今天晴，18°C（体感 16°C）
```
