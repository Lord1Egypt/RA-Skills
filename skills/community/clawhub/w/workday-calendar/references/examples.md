# 典型场景

### 场景1：查工作日
```
用户：2026年有多少个工作日？
AI：调用 calculate_total_workdays(2026)
```

### 场景2：安排会议找空闲时间
```
用户：5月20日下午有什么空闲时间？
AI：调用 find_free_slots("2026-05-20", "09:00", "18:00")
返回：[{"start": "15:30", "end": "18:00", "duration": 150}]
```

### 场景3：添加新日程
```
用户：明天下午2点到3点我要开会
AI：调用 add_schedule_event("开会", tomorrow, "14:00", "15:00")
```

### 场景4：查看今天和未来几天的安排
```
用户：帮我看看这周有什么安排
AI：调用 generate_today_schedule()
```

### 场景5：删除或更新日程
```
用户：取消明天的会议
AI：先 list 找到ID，然后 delete <id>

用户：把下午的会议改到3点
AI：update <id> --start=15:00 --end=16:00
```

### 场景6：每天定时生成日程列表
```
命令：python scripts/workday_calendar.py today
时间：每天早上 08:00
```

### 场景7：配置轮休
```
用户：给A组配置一个轮休，7天一周期，工作5天休息2天，跳过法定假
AI：调用 add_rotation_config("A组", "2026-01-05", 7, 5, True)
生成：rotate_generate(2026)
```

### 场景8：公休/临修
```
用户：下周一公司统一调休
AI：调用 add_special_rest("公休", date="2026-03-15")

用户：15号到17号办公室装修，临时休息
AI：调用 add_special_rest("临修", start_date="2026-04-15", end_date="2026-04-17")
```

### 场景9：法定假休被改为轮休
```
用户：这个项目期间，春节假期按轮休走
AI：创建轮休配置 + 可选调整/删除春节假期区间 -> generate -> check rules
```
