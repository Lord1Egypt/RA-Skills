# Workday Calculator Skill

[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://clawhub.ai)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-green.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

一个用于计算时间区间内有多少个工作日的OpenClaw技能。支持排除中国的节假日和调休安排。

## ✨ 功能特性

- ✅ **智能计算**：计算任意两个日期之间的工作日数量
- ✅ **节假日排除**：自动排除中国法定节假日（2025-2026年）
- ✅ **调休支持**：支持周末调休工作日（周末上班的情况）
- ✅ **详细信息**：显示工作日、节假日、周末详细列表
- ✅ **数据导出**：支持JSON格式导出，便于数据分析
- ✅ **数据更新**：节假日数据可轻松更新
- ✅ **命令行工具**：提供完整的命令行界面
- ✅ **Python模块**：可作为Python模块集成到其他应用

## 🚀 快速开始

### 安装

```bash
# 通过ClawHub安装（发布后）
clawhub install workday-calculator

# 或手动安装
git clone <repository-url>
cd workday-calculator
```

### 基本使用

```bash
# 计算2025年1月的工作日
python3 scripts/workday_calculator.py 2025-01-01 2025-01-31

# 查看详细信息
python3 scripts/workday_calculator.py 2026-02-01 2026-02-28 --details

# 导出结果到JSON
python3 scripts/workday_calculator.py 2025-03-01 2025-03-31 --details --export result.json
```

### 在OpenClaw中使用

当用户询问以下问题时，技能会自动触发：
- "帮我计算工作日"
- "3月13日到月底有多少个工作日"
- "排除节假日后的工作时间"
- "中国的节假日安排"

## 📁 文件结构

```
workday-calculator/
├── SKILL.md                    # 技能说明文档
├── README.md                   # 本文件
├── _meta.json                  # 技能元数据
├── LICENSE                     # 许可证文件
├── scripts/
│   ├── workday_calculator.py   # 主程序
│   ├── update_holidays.py      # 节假日更新工具
│   └── example_usage.py        # 使用示例
└── .clawhub/
    └── origin.json            # ClawHub配置
```

## 📊 节假日数据

### 当前包含的节假日

技能内置了2025-2026年的中国节假日数据：

| 节假日 | 2025年 | 2026年 | 天数 |
|--------|--------|--------|------|
| 元旦 | 1月1日 | 1月1-3日 | 1-3天 |
| 春节 | 1月28日-2月3日 | 2月15-23日 | 7-9天 |
| 清明节 | 4月4-6日 | 4月4-6日 | 3天 |
| 劳动节 | 5月1-5日 | 5月1-5日 | 5天 |
| 端午节 | 5月31日-6月2日 | 6月19-21日 | 3天 |
| 中秋节 | 10月1-3日 | 9月25-27日 | 3天 |
| 国庆节 | 10月4-7日 | 10月1-7日 | 4-7天 |

### 数据更新

节假日数据每年需要更新：

```bash
# 使用更新工具
python3 scripts/update_holidays.py

# 或手动编辑 scripts/workday_calculator.py
```

## 🛠️ 高级用法

### 作为Python模块使用

```python
from scripts.workday_calculator import WorkdayCalculator
from datetime import date

# 创建计算器实例
calculator = WorkdayCalculator()

# 计算工作日
workdays = calculator.calculate_workdays(date(2025, 1, 1), date(2025, 1, 31))
print(f"工作日数量: {workdays}")

# 获取详细信息
details = calculator.get_workday_details(date(2026, 2, 1), date(2026, 2, 28))
print(f"总天数: {details['total_days']}")
print(f"工作日: {details['workday_count']}")

# 添加自定义节假日
calculator.add_holiday(date(2025, 12, 25), "圣诞节")
```

### 命令行选项

```
用法: workday_calculator.py [OPTIONS] START_DATE END_DATE

参数:
  START_DATE   开始日期 (格式: YYYY-MM-DD)
  END_DATE     结束日期 (格式: YYYY-MM-DD)

选项:
  --details    显示详细信息
  --export     导出结果到JSON文件
  --version    显示版本信息
  --help       显示帮助信息
```

## 📋 使用示例

### 示例1：基本计算

```bash
$ python3 scripts/workday_calculator.py 2025-01-01 2025-01-31
📅 从 2025-01-01 到 2025-01-31:
📊 总天数: 31
💼 工作日数量: 18
🎉 非工作日数量: 13
```

### 示例2：详细信息

```bash
$ python3 scripts/workday_calculator.py 2026-01-01 2026-01-10 --details

============================================================
📅 工作日计算详情
============================================================
📌 时间区间: 2026-01-01 到 2026-01-10
📊 总天数: 10
💼 工作日数量: 6
🎉 节假日数量: 2
🌴 周末数量: 2
🏢 调休工作日数量: 1

💼 工作日列表 (6天):
  1. 2026-01-04 Sunday
  2. 2026-01-05 Monday
  ...
```

### 示例3：导出数据

```bash
$ python3 scripts/workday_calculator.py 2025-03-01 2025-03-31 --details --export march_2025.json
✅ 结果已导出到: march_2025.json
```

导出的JSON格式：
```json
{
  "start_date": "2025-03-01",
  "end_date": "2025-03-31",
  "workdays": ["2025-03-03", "2025-03-04", ...],
  "holidays": [],
  "weekends": ["2025-03-01", "2025-03-02", ...],
  "extra_workdays": [],
  "total_days": 31,
  "workday_count": 21,
  "generated_at": "2026-03-12T21:45:00.123456"
}
```

## 🔧 节假日更新工具

技能提供了交互式节假日更新工具：

```bash
$ python3 scripts/update_holidays.py
============================================================
📅 节假日数据更新工具
============================================================

📋 功能菜单
============================================================
1. 查看当前节假日数据
2. 添加节假日
3. 添加调休工作日
4. 在线搜索节假日信息
5. 生成Python代码
6. 退出
```

## 🌍 扩展支持其他国家

要支持其他国家的节假日，可以修改 `WorkdayCalculator` 类：

```python
class WorkdayCalculator:
    def __init__(self, country='china'):
        if country == 'china':
            self.weekends = {5, 6}  # 周六和周日
            self.holidays = self._load_china_holidays()
        elif country == 'usa':
            self.weekends = {5, 6}  # 周六和周日
            self.holidays = self._load_usa_holidays()
        # ... 其他国家
```

## 📈 性能说明

- 对于非常大的日期范围（如多年），计算速度可能会变慢
- 内存使用与日期范围大小成正比
- 节假日数据存储在内存中，启动时加载

## 🐛 故障排除

### 常见问题

1. **日期格式错误**
   ```
   ❌ 日期格式错误
   💡 请使用 YYYY-MM-DD 格式，例如: 2025-01-01
   ```

2. **节假日数据过期**
   - 每年需要更新节假日数据
   - 使用 `update_holidays.py` 工具

3. **权限问题**
   - 确保有执行Python脚本的权限
   - 确保导出目录有写入权限

### 错误信息

- `日期格式错误`：检查日期格式是否为 `YYYY-MM-DD`
- `文件写入失败`：检查导出目录的写入权限
- `节假日数据缺失`：更新节假日数据

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

## 👥 贡献指南

1. Fork 仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建Pull Request

## 🤝 支持

- 提交问题：[GitHub Issues](https://github.com/yourusername/workday-calculator/issues)
- 功能请求：[GitHub Discussions](https://github.com/yourusername/workday-calculator/discussions)
- 电子邮件：hunterxysy@126.com

## 🙏 致谢

- 感谢中国政府网提供节假日安排信息
- 感谢OpenClaw社区的支持
- 感谢所有贡献者和用户

---

**Made with ❤️ for the OpenClaw community**

[![OpenClaw](https://img.shields.io/badge/Powered%20by-OpenClaw-blue)](https://openclaw.ai)
[![ClawHub](https://img.shields.io/badge/Available%20on-ClawHub-orange)](https://clawhub.ai)