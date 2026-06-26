# 住宅装修造价估算器 (Vertical)

一款基于 AI 的住宅装修造价估算工具，帮助业主快速了解装修费用区间。

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Windows-green.svg)
![License](https://img.shields.io/badge/License-MIT-orange.svg)

## 功能特点

- ✅ **快速估算**：输入面积、档次、城市，3秒出结果
- ✅ **权威数据**：基于广材网、造价通等专业平台数据
- ✅ **三档价格**：经济型/舒适型/品质型可选
- ✅ **分项拆解**：硬装/软装/电器详细费用构成
- ✅ **不确定项提示**：提醒可能的费用偏差
- ✅ **适用范围广**：覆盖 300+ 城市

## 快速开始

### 方法1：使用脚本

```bash
# 进入脚本目录
cd scripts

# 运行估算（示例：100㎡ 精装 杭州）
python estimate.py 100 精装 杭州

# 查看帮助
python estimate.py
```

### 方法2：集成到 OpenClaw

1. 将整个 `home-reno-estimator` 目录复制到 OpenClaw skills 目录
2. 在 OpenClaw 中输入：`帮我估算一下装修费用，100㎡，精装，北京`
3. AI 将自动调用工具生成专业报告

## 支持的城市

| 等级 | 城市 |
|------|------|
| 一线城市 | 北京、上海、广州、深圳 |
| 新一线城市 | 杭州、成都、武汉、南京、苏州、天津、重庆、西安、郑州、东莞、青岛、沈阳、长沙、昆明、大连 |
| 二线城市 | 合肥、福州、济南、温州、常州、南通、徐州、佛山、珠海、中山、惠州、泉州、无锡、烟台、兰州、太原、吉林、贵阳、南阳、齐齐哈尔 |
| 三四线城市 | 其他地级市 |

> 注：未列出的城市默认按二线城市系数计算

## 装修档次说明

| 档次 | 说明 | 适用场景 |
|------|------|----------|
| 简装 | 基础功能性装修 | 出租、过渡性居住、预算有限 |
| 精装 | 中档品牌材料 | 自住刚需、追求性价比 |
| 豪装 | 高端品牌、定制化 | 改善型住房、追求品质 |

## 数据来源

- **广材网** (gldjc.com) - 广联达旗下，材料市场价
- **造价通** (zjtcn.com) - 工程造价信息
- **各省市造价信息网** - 政府指导价

## 项目结构

```
home-reno-estimator/
├── SKILL.md                    # OpenClaw 技能文件
├── scripts/
│   ├── estimate.py            # 核心估算脚本
│   └── package.py             # 打包脚本
├── references/
│   ├── data-sources.md        # 数据来源说明
│   ├── price-data-2024.md     # 参考价格数据
│   ├── pricing-strategy.md    # 变现策略
│   └── launch-guide.md        # 推广指南
├── dist/
│   └── home-reno-estimator.skill  # 打包文件
└── README.md                  # 本文件
```

## 变现计划

| 阶段 | 时间 | 目标 |
|------|------|------|
| MVP | 第1个月 | 验证需求，小红书冷启动 |
| 成长期 | 2-3个月 | 优化产品，积累口碑 |
| 稳定期 | 4-6个月 | 月收入突破 2 万 |

详见：[references/pricing-strategy.md](references/pricing-strategy.md)

## 推广渠道

- [x] 小红书（主战场）
- [ ] 知乎
- [ ] 公众号
- [ ] 微信群

详见：[references/launch-guide.md](references/launch-guide.md)

## ClawHub 上架

详见：[references/listing.md](references/listing.md)

## 免责声明

本工具基于公开市场数据估算，仅供参考。实际装修费用受多种因素影响，建议：
1. 以具体设计方案和当地市场报价为准
2. 咨询多家装修公司进行比价
3. 签订闭口合同避免后期增项

## 更新日志

### v1.1 (2026-04-07)
- 更新价格数据至2025-2026年
- 新增城市：宁波、无锡、厦门、哈尔滨、长春、石家庄、南宁、乌鲁木齐
- 优化输出报告格式
- 完善测试用例

### v1.0 (2026-03-27)
- 初始版本
- 支持 300+ 城市
- 三档价格估算
- 分项费用拆解

## 联系方式

如有问题或建议，欢迎通过 OpenClaw 联系。

---

*最后更新：2026-03-27*
