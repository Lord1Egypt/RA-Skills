# 故障排查

## 常见问题

### 1. 行情获取失败

**症状：** 执行 `quote` 或 `analyze` 命令时提示获取行情失败

**可能原因：**
- 网络连接问题
- 新浪/腾讯接口维护
- 股票代码错误或停牌

**排查步骤：**
```bash
# 1. 测试网络连接
ping finance.sina.com.cn
ping qt.gtimg.cn

# 2. 检查股票代码是否正确
python stock_monitor.py quote 600900

# 3. 尝试获取大盘指数（测试网络）
python stock_monitor.py index
```

**解决方案：**
- 等待接口恢复（通常几分钟）
- 检查防火墙/代理设置
- 验证股票代码是否正确

---

### 2. 报告生成超时

**症状：** `report` 命令执行时间过长或超时

**可能原因：**
- 网络延迟导致行情获取慢
- 股票数量过多
- 资讯接口响应慢

**排查步骤：**
```bash
# 检查监控池股票数量
python stock_monitor.py list
```

**解决方案：**
- 减少监控池股票数量
- 分批生成报告（使用 `report-a` 或 `report-hk`）
- 盘中时间避免生成完整报告

---

### 3. 持仓数据不准确

**症状：** 持仓盈亏计算结果与实际不符

**可能原因：**
- 持仓记录中的成本价错误
- 未同步最新交易
- 货币单位混淆（港股A股）

**排查步骤：**
```bash
# 1. 查看当前持仓记录
python stock_monitor.py position list

# 2. 检查交易记录
python stock_monitor.py trades
```

**解决方案：**
```bash
# 更新持仓成本
python stock_monitor.py position add 600900 6000 28.69

# 清除错误持仓后重新添加
python stock_monitor.py position remove 600900
python stock_monitor.py position add 600900 6000 28.50
```

---

### 4. 港股代码识别错误

**症状：** 港股行情获取失败或显示错误

**可能原因：**
- 港股代码格式不正确
- 港股代码需要以0开头

**正确格式：**
| 股票 | 正确代码 | 错误代码 |
|------|----------|----------|
| 联想集团 | 00992 | 992 |
| 中国神华(港) | 01088 | 1088 |
| 汇丰控股 | 00005 | 5 |
| 中芯国际 | 00981 | 981 |

**解决方案：**
- 确保港股代码为4-5位，以0开头
- 更新持仓记录中的港股代码

---

### 5. 预警不触发

**症状：** 股票达到预警条件但未收到提醒

**可能原因：**
- 未配置预警规则
- 预警功能需要定时任务配合
- 预警配置未启用

**排查步骤：**
```bash
# 检查预警配置文件
Get-Content "$env:USERPROFILE\.openclaw\stock-alerts.json"
```

**解决方案：**
- 确认 OpenClaw cron 任务配置正确
- 检查预警规则是否启用
- 手动触发一次监控测试

---

### 6. 技术指标显示异常

**症状：** MA、MACD、RSI 等指标显示 "N/A" 或异常值

**可能原因：**
- 历史数据不足（新股/港股）
- 数据接口返回格式变化
- 停牌期间无数据

**排查步骤：**
```bash
# 检查单只股票分析
python stock_monitor.py analyze 600900
```

**解决方案：**
- 等待更多交易日数据积累
- 检查是否为停牌股票
- 港股数据可能不完整

---

### 7. 中文显示乱码

**症状：** 输出中文字符显示为乱码

**可能原因：**
- 终端编码设置不正确
- Windows PowerShell 默认编码问题

**解决方案：**
```powershell
# 设置控制台编码为UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
chcp 65001

# 或在执行命令前设置
$env:PYTHONIOENCODING = "utf-8"
```

---

### 8. 脚本执行报错

**症状：** Python 脚本执行时报语法错误或导入错误

**可能原因：**
- Python 版本不兼容
- 缺少依赖库

**排查步骤：**
```bash
# 检查 Python 版本
python --version

# 检查已安装的依赖
pip list | Select-String "urllib|json"
```

**解决方案：**
```powershell
# 安装必要依赖（如需要）
pip install urllib3 json
```

---

## 日志与调试

### 启用调试模式

目前脚本未提供调试模式开关，可通过修改脚本添加 `print` 语句进行调试。

### 查看 OpenClaw 日志

```powershell
# 查看 OpenClaw 日志
Get-Content "$env:USERPROFILE\.openclaw\logs\*.log" -Tail 50
```

### 验证配置文件

```powershell
# 验证 JSON 格式
Get-Content "$env:USERPROFILE\.openclaw\stock-pool.json" | ConvertFrom-Json | ConvertTo-Json -Depth 3
```

---

## 性能优化

### 减少监控股票数量

每次只保留必要的监控股票，避免每次请求超时：
```bash
python stock_monitor.py list
# 逐个移除不需要的
python stock_monitor.py remove <code>
```

### 使用缓存

报告生成会自动缓存行情数据，但频繁查询仍可能导致限流。

### 分时段策略

| 时段 | 建议操作 |
|------|----------|
| 开盘前 9:00-9:30 | 生成早报 `report` |
| 盘中 9:30-15:00 | 少量监控 `monitor` |
| 午休 11:30-13:00 | 生成午报 `report` |
| 收盘后 15:00-17:00 | 生成晚报 `report` |
| 盘后 17:00后 | 完整分析 `report` |

---

## 联系方式

如问题持续存在，请检查：
1. OpenClaw 版本是否最新
2. 技能是否通过 ClawHub 更新到最新版本
3. 网络环境是否稳定
