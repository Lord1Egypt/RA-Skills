# 定时任务配置指南

## Windows 任务计划程序

### 图形界面配置

1. **打开任务计划程序**
   - Win + R → 输入 `taskschd.msc` → 回车

2. **创建基本任务**
   - 右侧操作栏 → "创建基本任务"
   - 名称：`每日金融课件推送`
   - 描述：`每天上午 9 点自动生成并推送金融分析教学课件`

3. **设置触发器**
   - 选择"每天"
   - 开始时间：`09:00:00`
   - 重复任务间隔：留空

4. **设置操作**
   - 选择"启动程序"
   - 程序/脚本：`python.exe`（填写完整路径，如 `C:\Python311\python.exe`）
   - 添加参数：`C:\Users\wwwir\.openclaw\workspace\skills\wework-financial-daily\scripts\generate_and_send.py`
   - 起始于：`C:\Users\wwwir\.openclaw\workspace\skills\wework-financial-daily`

5. **完成配置**
   - 勾选"当单击完成时打开属性对话框"
   - 在属性中勾选"不管用户是否登录都要运行"
   - 勾选"使用最高权限运行"

### 命令行配置（管理员权限）

```powershell
# 创建任务
schtasks /Create /TN "每日金融课件推送" /TR "python.exe C:\Users\wwwir\.openclaw\workspace\skills\wework-financial-daily\scripts\generate_and_send.py" /SC DAILY /ST 09:00 /RL HIGHEST /F

# 查看任务
schtasks /Query /TN "每日金融课件推送"

# 删除任务
schtasks /Delete /TN "每日金融课件推送" /F
```

## OpenClaw Cron 配置

如果使用 OpenClaw 的 cron 功能，在配置文件中添加：

```yaml
cron:
  - name: daily-financial-courseware
    schedule: "0 9 * * *"  # 每天 9:00
    command: "python C:\\Users\\wwwir\\.openclaw\\workspace\\skills\\wework-financial-daily\\scripts\\generate_and_send.py"
    env:
      WEWORK_X_TOKEN: "your-token-here"
      WEWORK_TO_USER: "your-user-id"
      FINANCIAL_OUTPUT_DIR: "C:/Users/your-name/Desktop"
```

## 环境变量配置

### 方式一：系统环境变量（推荐）

1. Win + R → 输入 `sysdm.cpl` → 回车
2. "高级" → "环境变量"
3. "系统变量" → "新建"
   - 变量名：`WEWORK_X_TOKEN`
   - 变量值：`your-x-token-here`
4. 重复添加其他变量

### 方式二：批处理包装脚本

创建 `run_daily.bat`：

```batch
@echo off
set WEWORK_X_TOKEN=your-x-token-here
set WEWORK_TO_USER=your-user-id
set FINANCIAL_OUTPUT_DIR=C:/Users/your-name/Desktop
python C:\Users\wwwir\.openclaw\workspace\skills\wework-financial-daily\scripts\generate_and_send.py
```

然后在任务计划程序中调用此批处理文件。

## 测试定时任务

### 手动触发测试

```powershell
# 立即运行任务
schtasks /Run /TN "每日金融课件推送"

# 查看运行历史
schtasks /Query /TN "每日金融课件推送" /V /FO LIST
```

### 查看日志

脚本输出会显示在任务计划程序的"历史记录"选项卡中。如需保存到文件，修改脚本添加日志：

```python
import logging
logging.basicConfig(
    filename='C:/Users/wwwir/.openclaw/workspace/skills/wework-financial-daily/daily_run.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
```

## 常见问题

### 任务不执行

1. 检查任务状态是否为"就绪"
2. 确认"不管用户是否登录都要运行"已勾选
3. 检查 Python 路径是否正确

### 环境变量未生效

1. 使用批处理包装脚本（方式二）
2. 或在任务属性中手动添加环境变量

### 权限不足

1. 勾选"使用最高权限运行"
2. 或以管理员身份创建任务
