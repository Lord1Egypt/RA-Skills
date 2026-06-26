# 厦门潮汐计算器

> 一款专为厦门赶海爱好者设计的智能潮汐计算技能，支持公历自动转农历、多窗口期分析、赶海评分等强大功能。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/kingwingshome/xiamen-tide-calculator/blob/main/LICENSE)
[![Version](https://img.shields.io/badge/Version-v3.2-blue.svg)](https://github.com/kingwingshome/xiamen-tide-calculator)
[![Author](https://img.shields.io/badge/Author-%E6%9F%AF%E8%8B%B1%E6%9D%B0-green.svg)](https://github.com/kingwingshome)

## 📋 项目简介

厦门潮汐计算器是根据农历日期计算厦门海域潮汐时间的智能工具，专为赶海爱好者设计。支持公历自动转农历、当前日期自动识别、闰月处理，提供赶海评分、地点推荐、装备建议和安全提醒等功能。

## ✨ 核心特性

### 🌊 潮汐计算
- ✅ 基于农历日期精确计算高潮低潮时间
- ✅ 自动判断潮汐大小（大潮/中潮/小潮）
- ✅ 支持公历自动转农历
- ✅ 当前日期自动识别
- ✅ 完整的闰月处理

### 🎯 赶海建议
- ✅ 智能赶海评分系统（0-10分）
- ✅ 多窗口期分析（上午/下午/傍晚/清晨）
- ✅ 每个窗口详细的优缺点分析
- ✅ 推荐指数评定（⭐⭐⭐-⭐⭐⭐⭐⭐）
- ✅ 整合窗口功能（显示当天所有可用窗口）

### 📊 智能推荐
- ✅ 根据潮汐大小智能推荐赶海地点
- ✅ 预期收获提示
- ✅ 季节适配的装备建议
- ✅ 完整的安全提醒
- ✅ 多日比较功能（推荐最佳赶海日期）

## 🚀 安装方式

### 方法一：通过 WorkBuddy 技能市场安装（推荐）

1. 打开 WorkBuddy 客户端
2. 点击顶部「技能」按钮，或进入个人头像 → 「Claw 设置」→ 「SkillHub 商店」
3. 搜索"厦门潮汐计算器"
4. 点击「免费订阅」完成安装

### 方法二：通过 Git 仓库导入

1. 访问 GitHub 仓库：https://github.com/kingwingshome/xiamen-tide-calculator
2. 复制仓库的 HTTPS 克隆地址
3. 在 WorkBuddy 的「Skills 管理」中点击「从 Git 仓库导入」
4. 粘贴仓库地址，选择分支，点击「验证并导入」

### 方法三：本地文件导入

1. 下载技能包：`xiamen-tide-calculator-v3.2.skill`
2. 在 WorkBuddy 中进入「Claw 设置」→「Skills 管理」
3. 点击「导入 Skills」，选择下载的 `.skill` 文件
4. 等待导入完成

## 📖 使用方法

### 标准模式：查询潮汐时间

```bash
# 使用当前日期
python scripts/tide_calculator.py --today

# 使用公历日期
python scripts/tide_calculator.py --solar-date 2025-04-02

# 使用农历日期
python scripts/tide_calculator.py --lunar-day 15 --lunar-month 3
```

### 赶海专门模式：获取赶海建议

```bash
# 当前日期赶海建议
python scripts/tide_calculator.py --today --beach-mode

# 指定日期赶海建议
python scripts/tide_calculator.py --solar-date 2025-04-02 --beach-mode

# 整合窗口模式（推荐）
python scripts/tide_calculator.py --solar-date 2026-04-05 --beach-mode --integrated
```

### 多日比较：选择最佳赶海日期

```bash
python scripts/compare_beach_days.py --lunar-month 3 --start-day 1 --days 10
```

## 📁 项目结构

```
xiamen-tide-calculator/
├── SKILL.md                          # 技能主文档
├── README.md                         # 项目说明文档
├── LICENSE                           # MIT License 许可文件
├── 使用说明.md                       # 基础使用说明
├── 新功能使用指南.md                 # 新功能详细指南
├── references/                       # 参考文档目录
│   ├── beachcombing_improvement.md    # 赶海功能改进方案
│   └── lunar_conversion.md           # 农历转换参考
└── scripts/                         # 脚本目录
    ├── tide_calculator.py            # 潮汐计算主脚本
    └── compare_beach_days.py        # 多日比较脚本
```

## 🎯 功能演示

### 潮汐查询示例

```
【厦门潮汐・农历 2026年2月17日】
高潮 1：01:36
高潮 2：14:00
低潮 1：前日 19:24
低潮 2：07:48
最佳赶海：05:48-08:48（窗口1）、18:12-21:12（窗口2）
潮汐大小：大潮
赶海评分：9.0分（强烈推荐）
```

### 赶海建议示例

```
【厦门赶海建议・农历 2026年2月17日】

🌊 赶海评分：9.0分（强烈推荐）

⏰ 最佳赶海时段：

  【窗口1】05:48-08:48
  └─ 时间类型：清晨
  └─ 优势：
     ✅ 气温凉爽，赶海舒适度高
     ✅ 潮水退潮程度最好，海货最多
     ✅ 环境安静，赶海体验佳
  └─ 注意事项：
     ❌ 需要非常早起（3-4点）
     ❌ 光线较暗，需要照明设备
  └─ ⭐ 推荐指数：⭐⭐⭐

  【窗口2】18:12-21:12
  └─ 时间类型：傍晚
  └─ 优势：
     ✅ 气温凉爽，赶海舒适度高
     ✅ 光线柔和，适合拍照
     ✅ 退潮时间长，海货丰富
  └─ 注意事项：
     ❌ 天色渐暗，视野受限
     ❌ 潮水上涨较快，需注意安全
  └─ ⭐ 推荐指数：⭐⭐⭐⭐⭐
```

## 🔧 技术栈

- **编程语言**：Python 3.6+
- **农历转换**：zhdate 库
- **输出编码**：UTF-8
- **许可协议**：MIT License

## 📊 版本历史

### v3.2 (2026-04-03) - 整合窗口功能
- ✅ 添加整合窗口功能，优化跨天窗口显示
- ✅ 完善版权声明和开源地址
- ✅ 技能打包为 `.skill` 文件

### v3.1 (2026-04-02) - 多窗口期分析
- ✅ 多窗口期自动识别
- ✅ 窗口优缺点详细描述
- ✅ 推荐指数自动评定

### v3.0 (2026-04-02) - 基础增强
- ✅ 支持公历自动转农历
- ✅ 当前日期自动识别
- ✅ 闰月处理

### v2.0 (2026-04-02) - 赶海专门模式
- ✅ 赶海评分系统
- ✅ 地点推荐
- ✅ 装备建议
- ✅ 多日比较功能

### v1.0 (2026-04-02) - 初始版本
- ✅ 基础潮汐计算
- ✅ 潮汐大小判断
- ✅ 赶海窗口计算

## 🤝 贡献指南

欢迎对本项目贡献代码、报告问题或提出建议！

### 贡献方式
1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

### 报告问题
- 使用 GitHub Issues 报告 Bug
- 提供详细的复现步骤和环境信息
- 如有可能，请附上截图

## 📄 许可协议

本项目采用 **MIT License** 开源协议。详见 [LICENSE](LICENSE) 文件。

## 👨‍💻 作者

**柯英杰** - [GitHub](https://github.com/kingwingshome)

## 📞 联系方式

- **GitHub**：https://github.com/kingwingshome/xiamen-tide-calculator
- **WorkBuddy**：通过 WorkBuddy 平台反馈

## ⚠️ 免责声明

1. **准确性说明**：本技能基于厦门海域标准潮汐计算公式，仅供参考。实际潮汐时间可能受天气、气压、地形等因素影响，建议结合实地观测或官方潮汐表使用。

2. **安全警告**：赶海活动存在一定风险，请务必注意安全：
   - 潮水上涨速度可能超出预期
   - 礁石湿滑，容易摔倒
   - 海洋生物可能造成伤害
   - 天气变化可能带来危险

3. **责任限制**：使用本技能进行赶海活动，用户需自行承担风险。开发者不对因使用本技能而产生的任何直接或间接损失承担责任。

## ⭐ Star 支持

如果这个项目对你有帮助，请给个 ⭐ Star 支持一下！

---

**Made with ❤️ by 柯英杰**
