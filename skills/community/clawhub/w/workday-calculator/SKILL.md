---
name: workday-calculator
description: 计算时间区间内有多少个工作日的技能。支持排除中国的节假日和调休安排。当用户询问工作日计算、节假日排除、工作时间计算时使用此技能。
license: MIT
---

# Workday Calculator Skill

用于计算任意两个日期之间工作日数量的Python技能。支持排除中国的法定节假日和调休安排。

## 功能特性

- ✅ 计算任意日期区间内的工作日数量
- ✅ 自动排除周末（周六、周日）
- ✅ 自动排除中国法定节假日（2025-2026年）
- ✅ 支持调休工作日（周末需要上班的情况）
- ✅ 提供详细信息查看功能
- ✅ 支持结果导出为JSON格式
- ✅ 节假日数据可更新

## 快速开始

### 安装依赖
无需额外依赖，只需要Python 3.6+。

### 基本使用

```bash
# 计算2025-01-01到2025-01-31之间的工作日
python3 scripts/workday_calculator.py 2025-01-01 2025-01-31

# 查看详细信息
python3 scripts/workday_calculator.py 2025-01-01 2025-01-31 --details

# 导出结果到JSON文件
python3 scripts/workday_calculator.py 2025-01-01 2025-01-31 --details --export result.json
```

### 参数说明

```
参数：
  start_date  开始日期 (格式: YYYY-MM-DD)
  end_date    结束日期 (格式: YYYY-MM-DD)

选项：
  --details   显示详细信息（工作日、节假日、周末列表）
  --export    导出结果到JSON文件
```

## 文件结构

```
workday-calculator/
├── SKILL.md                  # 本文件
├── scripts/
│   ├── workday_calculator.py # 主程序
│   ├── update_holidays.py    # 节假日更新工具
│   └── example_usage.py      # 使用示例
└── references/
    └── holidays_2025_2026.md # 节假日数据文档
```

## 节假日数据

### 当前包含的节假日

技能内置了2025-2026年的中国节假日数据，包括：
- 元旦
- 春节
- 清明节
- 劳动节
- 端午节
- 中秋节
- 国庆节

### 更新节假日数据

节假日数据需要每年更新，可以通过以下方式：

1. **手动更新**：编辑 `scripts/workday_calculator.py` 文件中的 `_load_holidays()` 方法
2. **使用更新工具**：运行 `python3 scripts/update_holidays.py`
3. **从政府网站获取**：访问中国政府网 (www.gov.cn) 获取最新的节假日安排

### 数据来源

节假日数据基于以下来源：
- 中国政府网（www.gov.cn）发布的节假日安排通知
- 国务院办公厅正式通知
- 百度百科相关词条

## 使用示例

### 示例1：基本计算

```bash
$ python3 scripts/workday_calculator.py 2025-01-01 2025-01-31
从 2025-01-01 到 2025-01-31:
总天数: 31
工作日数量: 18
```

### 示例2：详细信息查看

```bash
$ python3 scripts/workday_calculator.py 2026-02-01 2026-02-28 --details

=== 工作日计算详情 ===
时间区间: 2026-02-01 到 2026-02-28
总天数: 28
工作日数量: 17
节假日数量: 7
周末数量: 8
调休工作日数量: 2

工作日列表 (17天):
  1. 2026-02-04 Tuesday
  2. 2026-02-05 Wednesday
  ...
```

### 示例3：批量计算

```bash
$ python3 scripts/example_usage.py
```

## 导出格式

导出的JSON文件格式：

```json
{
  "start_date": "2025-01-01",
  "end_date": "2025-01-31",
  "workdays": ["2025-01-02", "2025-01-03", ...],
  "holidays": ["2025-01-01"],
  "weekends": ["2025-01-04", "2025-01-05", ...],
  "extra_workdays": ["2025-02-08"],
  "total_days": 31,
  "workday_count": 22
}
```

## 集成到其他系统

### 作为Python模块使用

```python
from scripts.workday_calculator import WorkdayCalculator

calculator = WorkdayCalculator()
workdays = calculator.calculate_workdays(date(2025, 1, 1), date(2025, 1, 31))
print(f"工作日数量: {workdays}")
```

### 作为命令行工具

可以将脚本添加到系统PATH中：

```bash
# Linux/macOS
sudo ln -s $(pwd)/scripts/workday_calculator.py /usr/local/bin/workday-calc

# 使用
workday-calc 2025-01-01 2025-01-31
```

## 节假日数据更新指南

### 方法1：使用更新工具

```bash
python3 scripts/update_holidays.py
```

### 方法2：手动更新

1. 获取最新的节假日安排通知（中国政府网）
2. 编辑 `scripts/workday_calculator.py` 中的节假日数据
3. 测试更新后的数据是否正确

### 方法3：从外部API获取

可以扩展 `update_holidays.py` 来从政府网站API获取数据。

## 扩展开发

### 支持其他国家

要支持其他国家的节假日，修改 `WorkdayCalculator` 类：

1. 更新 `weekends` 属性以匹配目标国家的周末定义
2. 更新 `holidays` 和 `extra_workdays` 数据
3. 可以添加从配置文件或数据库加载节假日数据的功能

### 添加Web界面

可以创建Flask或FastAPI应用，提供Web界面和REST API。

## 故障排除

### 常见问题

1. **日期格式错误**：确保使用 `YYYY-MM-DD` 格式
2. **节假日数据过期**：每年更新节假日数据
3. **权限问题**：确保有执行Python脚本的权限

### 错误信息

- `日期格式错误`：检查日期格式是否为 `YYYY-MM-DD`
- `文件写入失败`：检查导出目录的写入权限
- `节假日数据缺失`：更新节假日数据

## 性能说明

- 对于非常大的日期范围（如多年），计算速度可能会变慢
- 内存使用与日期范围大小成正比
- 节假日数据存储在内存中，启动时加载

## 许可证

MIT License - 详见 LICENSE 文件

## 贡献指南

1. Fork 仓库
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

## 联系方式

如有问题或建议，请通过GitHub Issues提交。