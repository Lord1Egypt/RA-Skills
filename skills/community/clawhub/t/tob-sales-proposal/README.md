# ToB Sales Proposal Generator

> ToB 销售提案生成器 - 输出带品牌色 CSS 的 HTML 四页提案

## 快速开始

```bash
# 安装
npm install

# 交互模式
node src/cli.js

# 快速模式（命令行参数直接生成）
node src/cli.js --quick --client "某银行" --industry "金融" --product "智能客服系统"
```

## 功能特性

- 🎨 HTML 完整页面输出（品牌色 + CSS）
- 📄 4 模块分页：痛点对齐 / 方案对齐 / 实施路径 / ROI与案例
- 🎯 客户痛点分析
- 📊 解决方案匹配
- 💰 ROI 量化分析
- 🏆 案例智能匹配
- 💡 页面底部提示：复制内容给 AI 生成 PPT

## 提案结构

1. **痛点对齐** - 客户输入摘要、行业趋势、共性挑战、客户痛点翻译
2. **方案对齐** - 方案核心、核心功能、客户价值、能力维度
3. **实施路径** - 分阶段交付计划、里程碑、客户配合清单
4. **承诺型 ROI 与案例** - 投资概算、收益分析、成功案例、商务建议

## 使用方法

### 交互模式
```bash
tob-sales-proposal
```

按提示输入客户信息，自动生成 `proposal.html`。

### 快速模式
```bash
tob-sales-proposal --quick --client "客户名称" --industry "行业" --product "产品"
```

### 完整参数
```bash
tob-sales-proposal \
  --quick \
  --client "客户名称" \
  --industry "金融" \
  --product "智能客服" \
  --painpoints "数据孤岛,效率低下" \
  --budget "50-100万" \
  --timeline "3个月" \
  --output ./proposal.html
```

> `--quick` 保留为兼容参数；只要传入必要命令行参数，就会直接生成 HTML，不进入交互。

## 输出说明

- 默认输出：`./proposal.html`
- 输出格式：HTML 页面，可直接浏览器打开、打印为 PDF，或复制给 AI 生成 PPT/Keynote/路演稿。

## License

MIT
