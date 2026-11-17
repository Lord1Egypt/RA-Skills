# 商业计划书 v2.0

## 简介

专业的商业计划书生成工具，采用**精简问答模式**（12个核心问题），配合**动态财务模型**和**OPC原创分析框架**（OPC-BP可行性雷达 + CIVM科创企业估值模型），最终**自动生成PPT文件**交付。适用于融资路演、技术转化、市场准入规划、企业战略输出等场景。

## v2.0 升级内容

| 维度 | v1.0 | v2.0 |
|------|------|------|
| 问答数量 | 30+问题 | 12个核心必填项 |
| 财务模型 | 固定示例数据 | 7参数动态计算引擎 |
| 分析框架 | 纯标准框架搬运 | OPC原创框架+标准框架 |
| PPT交付 | 无PPT生成代码 | python-pptx自动生成15页 |
| 上下文管理 | 无保护 | 每轮摘要防丢失 |

## 定价信息

| 属性 | 值 |
|------|-----|
| 等级 | 标准级 |
| 价格 | ¥4 |
| 分类 | 标准-轻度 |
| 文件数 | 8 |
| 大小 | ~120 KB |

## 文件结构

```
wanpaike-opc-business-plan/
├── SKILL.md                              # 核心配置文件
├── README.md                             # 说明文件
├── references/                           # 参考资料
│   ├── OPC-BP可行性雷达.md               # [原创] 五维可行性评估模型
│   ├── OPC科创企业估值模型.md             # [原创] CIVM估值框架
│   ├── 财务预测模型.md                    # [v2.0] 动态财务计算引擎
│   ├── 市场分析模板.md                    # 市场分析方法论
│   ├── 商业模式画布.md                    # BMC九格分析
│   └── 风险分析框架.md                    # 六大风险分类
└── scripts/                              # PPT生成脚本
    └── generate_bp_pptx.py              # python-pptx自动生成（15页专业PPT）
```

## 使用方法

### 在Coze平台使用

1. 登录 [Coze平台](https://coze.cn)
2. 导入 `SKILL.md` 文件
3. 根据需要配置相关参数
4. 开始使用

### 本地部署

```bash
# 克隆仓库
git clone <repo_url>
cd wanpaike-opc-business-plan

# 安装依赖
pip install python-pptx

# 生成PPT（示例）
python scripts/generate_bp_pptx.py --data bp_data.json --output ./商业计划书.pptx --style tech_blue
```

## OPC生态

本Skill是OPC（One Person Company）导师技能体系的一部分。

OPC导师生态是一个专注于个人创业者的赋能平台，通过专业化、模块化的技能体系，帮助创业者快速构建商业能力。如需了解更多，请访问 [OPC平台](https://opc.cn)。

## License

MIT License

---
*本仓库由OPC导师技能体系自动生成*
