# UApp Outlier Detection Skill

友盟+ (UApp) 异常检测技能包，用于查询应用异动报告、昨日异常和智能巡检信息。

## 安装

### 方式一：复制到个人技能目录

```bash
cp -r uapp-outlier ~/.qoder/skills/
```

### 方式二：复制到项目技能目录

```bash
cp -r uapp-outlier /your/project/path/.qoder/skills/
```

## 配置

### 认证信息配置（三选一）

1. **配置文件（推荐）**：将 `umeng-config.example.json` 复制为 `umeng-config.json` 并填入你的凭证
   ```bash
   cp umeng-config.example.json umeng-config.json
   # 编辑 umeng-config.json 填入真实的 apiKey 和 apiSecurity
   ```

2. **环境变量**：设置环境变量
   ```bash
   export UMENG_API_KEY=your_api_key
   export UMENG_API_SECURITY=your_api_security
   ```

3. **直接传入**：在使用时通过代码参数传入

## 使用

### 通过 AI 对话使用

导入技能后，直接用自然语言提问：

- "我的 appkey=xxx 在昨天有没有异常？"
- "获取我的应用 zzz 的异动报告地址"
- "昨天我的哪些应用有异动？"
- "查看智能巡检基本信息"

### 通过命令行脚本使用

```bash
cd uapp-outlier

# 获取指定应用的异动报告
python scripts/helper.py report --appkey YOUR_APPKEY --date 20260401

# 查看昨日异常
python scripts/helper.py yesterday

# 查看智能巡检信息
python scripts/helper.py inspection

# 直接传入凭证
python scripts/helper.py report --appkey YOUR_APPKEY --date 20260401 --ak YOUR_AK --sk YOUR_SK
```

### 通过 Python 代码使用

```python
from scripts.helper import UAppOutlierClient

# 初始化客户端（自动从配置文件或环境变量读取凭证）
client = UAppOutlierClient()

# 或者直接传入凭证
client = UAppOutlierClient(ak="your_ak", sk="your_sk")

# 获取异动报告
report = client.get_outlier_report(appkey="59892f08310c9307b60023d0", date="20260401")
print(report)

# 获取昨日异常
yesterday = client.get_yesterday_outliers()
print(yesterday)

# 获取智能巡检信息
summary = client.get_inspection_summary()
print(summary)
```

## API 说明

本技能包封装了三个友盟+ API：

1. **获取应用异动报告** (`getOutlierPoints`)
   - 查询指定应用在特定日期的异动情况
   - 返回异动摘要、类型和详细报告链接

2. **获取昨日异常** (`getYesterdayOutliers`)
   - 查询所有应用昨日的异动情况
   - 返回各应用的基本数据和异动提醒

3. **获取智能巡检信息** (`aiEventSummary`)
   - 查询账号的智能巡检基本信息
   - 返回埋点异常、事件汇总等信息

## 依赖

- Python 3.6+
- requests 库

安装依赖：
```bash
pip install requests
```
