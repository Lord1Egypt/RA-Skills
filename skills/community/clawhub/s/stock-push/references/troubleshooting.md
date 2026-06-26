# 已知问题排查

## 推送失败

### 症状：脚本返回 "⚠️ 发送失败"
**排查步骤：**
```bash
# 1. 查看日志
tail -f /tmp/stock_pre.log

# 2. 单独测试发送
openclaw message send \
  --channel openclaw-weixin \
  --target YOUR_WECHAT_USER_ID \
  --message "测试"
```

### 症状：Gateway 返回 ret:-2
**原因：** direct ilink API 在无活跃 session 时拒绝发送
**解决：** 当前已改用 `openclaw message send`，无需处理

### 症状：openclaw message send 返回成功但微信没收到
**排查：** 检查 USER_ID 是否拼写正确
```bash
grep USER_ID /root/.openclaw/workspace/stock_pre.py
# 正确值：YOUR_WECHAT_USER_ID（替换为你的实际ID）
```

---

## 数据异常

### 症状：price=0 或 yclose=0
**原因：** 非交易时段，东方财富返回0
**解决：** 脚本会自动跳过 price<=0 的数据，无有效数据时不发送

### 症状：全部数据无效
**排查：**
```bash
# 测试东方财富 API 是否可达
curl -s "https://push2.eastmoney.com/api/qt/stock/get?secid=1.600490&fields=f43,f44&ut=bd1d9ddb04089700cf9c27f4f4961f5b&fltt=2&invt=2"
# 正常响应：{"data":{"f43":8.88,"f44":9.07,...}}
```

---

## cron 不执行

### 排查：
```bash
# 1. 检查 cron 服务
systemctl status cron

# 2. 检查 cron 配置
cat /etc/cron.d/stock-monitor

# 3. 检查 cron 是否匹配日期
# 9:20 * * 1-5  = 周一～五 9:20
# 5 15 * * 1-5  = 周一～五 15:05
# 0 20 * * 1-4  = 周一～四 20:00

# 4. 强制触发一次
python3 /root/.openclaw/workspace/stock_pre.py
```

---

## 持仓名称错误

### 症状：微信收到"双杰电气"但实际持仓是"超频三"

**原因：** 东方财富 300444 查询结果是"双杰电气"，不是"超频三"

**解决：** 确认实际持仓股是哪个，修改脚本中 HOLDINGS 列表

---

## 日志文件

- `/tmp/stock_pre.log` — 盘前推荐
- `/tmp/stock_after.log` — 收盘复盘
- `/tmp/stock_next.log` — 次日关注

日志保留7天，由 `/etc/logrotate.d/stock-monitor` 管理。
