# 日报报表生成器 - 使用说明

## 快速开始

### 1. 确保依赖已安装

```bash
pip3 install pandas openpyxl
```

### 2. 准备输入数据

将你的数据文件放到以下位置：

```
/Users/ahs/.openclaw/workspace/传输单边故障/output/结果D_最终数据.xlsx
```

或者修改脚本中的 `INPUT_DIR` 和 `INPUT_FILE` 变量。

### 3. 运行脚本

```bash
cd /Users/ahs/.openclaw/workspace/传输单边故障
python3 scripts/generate_assessment_period_report.py
```

### 4. 查看输出

生成的报表会保存在：

```
/Users/ahs/.openclaw/workspace/传输单边故障/output/日报报表_按考核周期_YYYYMMDD_HHMMSS.xlsx
```

## 自定义配置

### 修改输入/输出目录

编辑 `scripts/generate_assessment_period_report.py`：

```python
# 配置
INPUT_DIR = "/path/to/your/input/directory"
OUTPUT_DIR = "/path/to/your/output/directory"
```

### 修改超时标准

编辑 `scripts/generate_assessment_period_report.py`：

```python
# 超时标准
TIMEOUT_STANDARDS = {
    '汇聚骨干单边': 4,      # 修改为你的标准
    '重要环': 12,          # 修改为你的标准
    '一般环': 24           # 修改为你的标准
}
```

### 修改考核周期规则

编辑 `scripts/generate_assessment_period_report.py` 中的 `get_assessment_period()` 函数。

## 常见问题

### Q: 如何处理多个数据文件？

A: 你可以修改脚本，从多个 Excel 文件读取数据并合并：

```python
# 读取多个文件
all_data = []
for file_path in file_list:
    df = pd.read_excel(file_path)
    all_data.append(df)

# 合并数据
all_data = pd.concat(all_data, ignore_index=True)
```

### Q: 如何添加自定义统计指标？

A: 在 `generate_period_report()` 函数中添加你的统计逻辑。

### Q: 如何修改报表格式？

A: 在 `write_sheet_with_format()` 函数中修改样式设置。

## 示例数据

如果你需要测试，可以使用以下示例数据结构：

```
督办类型 | 管控记录 | 风险评分 | 故障类型 | 地市 | 厂家 | 设备类型 | 持续时长（小时） | 告警发现时间 | 告警发生时间 | 告警清除时间 | ...
---------|---------|---------|---------|------|------|---------|---------------|------------|------------|------------|----
无       | 无      | 36      | 接入环单边 | 韶关 | 华为 | PTN     | 47.26         | 2026-01-01 12:04:18 | 2026-01-01 12:04:15 | 2026-01-03 11:19:54 | ...
```

## 联系支持

如有问题，请联系：
- 技术支持：[你的联系方式]
- 文档更新：[更新日期]
