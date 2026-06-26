# 股票投资智投顾问 - 安装说明

## 技能简介

整合五大股票投资技能的综合智投顾问系统，提供从数据采集、多维度分析到专业报告输出的全流程服务。

**核心能力：**
- 实时数据采集：沪深北港美股实时行情、分时量能、资金流向
- 多源信息搜索：新闻、财报、公告、分析师评级
- 多模态图表分析：K线图/分时图智能识别与解读
- 四角色协作分析：市场研究、宏观研判、情绪分析、投资决策
- 专业报告输出：飞书云文档，咨询级格式

---

## 安装步骤

### 方法一：复制到 OpenClaw 技能目录

```bash
# 1. 复制技能文件夹到 OpenClaw 技能目录
cp -r stock-investment-advisor ~/.openclaw/skills/

# 或复制到工作空间技能目录
cp -r stock-investment-advisor ~/workspace/agent/skills/

# 2. 重启 OpenClaw
openclaw gateway restart
# 或
sh scripts/restart.sh
```

### 方法二：使用 ClawHub 安装

如果此技能已发布到 ClawHub：

```bash
# 安装技能
npx clawhub install stock-investment-advisor

# 或在 OpenClaw 中
clawhub install stock-investment-advisor
```

### 方法三：配置文件启用

在 OpenClaw 配置中添加：

```json
{
  "skills": {
    "entries": {
      "stock-investment-advisor": {
        "enabled": true,
        "path": "~/Desktop/stock-investment-advisor"
      }
    }
  }
}
```

---

## 目录结构

```
stock-investment-advisor/
├── SKILL.md              # 技能主文件（必读）
├── README.md             # 安装说明（本文件）
├── scripts/              # 脚本工具
│   └── analyze.py        # 统一入口脚本
└── references/           # 参考资料（预留）
```

---

## 依赖要求

### 必需依赖

1. **OpenClaw 环境**
   - 支持多模态模型（如 glm-5v-turbo）
   - 支持飞书集成（用于生成云文档）

2. **Python 环境**
   - Python 3.8+
   - uv 包管理器

3. **网络访问**
   - 东方财富、新浪财经等数据源
   - 飞书 API（如需云文档输出）

### 可选依赖

1. **Tushare Token** - 增强A股数据获取
   ```bash
   export TUSHARE_TOKEN="your_token"
   ```

2. **子技能脚本**（可选安装）
   - `scripts/a-stock/` - A股行情采集器
   - `scripts/glmv/` - K线图采集器
   - `scripts/autoglm/` - 新闻搜索器

---

## 使用方法

### 触发词

- "分析一下XX股票"
- "XX股票怎么样"
- "XX能不能买"
- "生成XX的投资报告"
- "比较XX和YY"
- 发送股票K线图截图

### 支持市场

| 市场 | 代码格式 | 示例 |
|------|---------|------|
| A股（沪深） | 6位数字 | 600519、002446 |
| A股（北交所） | 8开头 | 830799 |
| 港股 | 数字.HK | 0700.HK、09988.HK |
| 美股 | 字母代码 | AAPL、TSLA |

---

## 示例对话

**用户：** 分析一下贵州茅台

**AI：**
1. 确认代码：600519
2. 采集实时行情
3. 搜索新闻和财报
4. 四角色协作分析
5. 生成飞书云文档报告
6. 输出精炼总结

---

## 自定义配置

### 修改输出格式

编辑 `SKILL.md` 中的报告模板部分。

### 添加新数据源

在 `scripts/` 目录下添加新的采集脚本。

### 调整分析权重

修改 `SKILL.md` 中的量化评分权重：

| 维度 | 默认权重 | 可调整范围 |
|------|---------|-----------|
| 盈利增速 | 30% | 20-40% |
| 资金流向 | 30% | 20-40% |
| 技术形态 | 20% | 10-30% |
| 催化剂 | 20% | 10-30% |

---

## 注意事项

1. **数据时效性**：行情数据实时，新闻近3日，财报最新披露
2. **风险提示**：每份报告必须包含具体风险提示
3. **免责声明**：报告末尾必须包含免责声明
4. **数据不编造**：没获取到的数据说明暂无

---

## 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|---------|
| v1.0 | 2026-04-03 | 初始版本，整合五大股票投资技能 |

---

## 技术支持

- 问题反馈：在 OpenClaw 社区提问
- 功能建议：提交 Issue 或 Pull Request

---

## 免责声明

本技能生成的所有分析报告仅供参考，不构成投资建议。股市有风险，投资需谨慎。投资者应根据自身情况独立决策，并自行承担投资风险。
