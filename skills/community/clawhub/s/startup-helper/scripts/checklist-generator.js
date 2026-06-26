#!/usr/bin/env node

/**
 * 创业流程检查清单生成器
 * 用法: node scripts/checklist-generator.js
 */

const fs = require('fs');
const path = require('path');

// 创业流程检查清单数据
const checklistData = {
  公司注册: {
    周期: '7-15个工作日',
    费用: '500-2000元（代理）',
    步骤: [
      { name: '企业名称核准', duration: '1-2天', tool: 'e-dengji.com' },
      { name: '提交注册材料', duration: '3-5天', tool: '工商局/全程电子化' },
      { name: '领取营业执照', duration: '1天', tool: '工商局' },
      { name: '刻制公章', duration: '1天', tool: '公安局指定刻章点' },
      { name: '银行开户', duration: '1-3天', tool: '各大银行' },
      { name: '税务登记', duration: '1天', tool: '税务局/电子税务局' }
    ]
  },
  ICP备案: {
    周期: '15-30个工作日',
    费用: '免费（阿里云/腾讯云代备案）',
    步骤: [
      { name: '购买域名和服务器', duration: '1天', tool: '阿里云/腾讯云' },
      { name: '提交备案材料', duration: '3-5天', tool: '备案系统' },
      { name: '服务商初审', duration: '1-2天', tool: '阿里云/腾讯云' },
      { name: '短信核验', duration: '1天', tool: '收到短信后操作' },
      { name: '管局审核', duration: '7-20天', tool: '省通信管理局' },
      { name: '备案成功', duration: '获取备案号', tool: '可在信产部查询' }
    ]
  },
  商标注册: {
    周期: '9-12个月',
    费用: '270元/类（官费）',
    步骤: [
      { name: '商标查询', duration: '1天', tool: '国家商标局/第三方工具' },
      { name: '确认分类', duration: '1天', tool: '尼斯分类表' },
      { name: '准备申请材料', duration: '3天', tool: '营业执照+商标图样' },
      { name: '提交申请', duration: '1天', tool: '商标局/代理机构' },
      { name: '形式审查', duration: '1个月', tool: '商标局' },
      { name: '实质审查', duration: '4-6个月', tool: '商标局' },
      { name: '初审公告', duration: '3个月', tool: '商标局' },
      { name: '核准注册', duration: '1个月', tool: '下发注册证' }
    ]
  },
  银行开户: {
    周期: '1-3个工作日',
    费用: '300-1000元（部分银行免费）',
    步骤: [
      { name: '预约开户', duration: '1天', tool: '银行网点/手机银行' },
      { name: '准备材料', duration: '根据要求', tool: '见材料清单' },
      { name: '前往银行办理', duration: '1天', tool: '银行网点' },
      { name: '等待审核', duration: '1-2天', tool: '银行' },
      { name: '领取开户许可证', duration: '1天', tool: '银行' },
      { name: '开通网银', duration: '1天', tool: '银行' }
    ]
  },
  税务登记: {
    周期: '1-3个工作日（领取执照30日内完成）',
    费用: '金税盘/UK约400元',
    步骤: [
      { name: '准备材料', duration: '1天', tool: '营业执照+公章等' },
      { name: '前往税务机关', duration: '1天', tool: '主管税务局' },
      { name: '填写税种登记表', duration: '1天', tool: '税务局' },
      { name: '核定税种', duration: '1天', tool: '税务局' },
      { name: '购买金税盘/UK', duration: '1天', tool: '航天信息/百旺' },
      { name: '开通电子税务局', duration: '1天', tool: '网上操作' },
      { name: '签署三方协议', duration: '1天', tool: '企业-银行-税务局' }
    ]
  },
  社保开户: {
    周期: '3-5个工作日',
    费用: '免费（开户）',
    步骤: [
      { name: '准备材料', duration: '1天', tool: '营业执照+公章等' },
      { name: '前往社保中心', duration: '1天', tool: '区社保中心' },
      { name: '办理社保登记', duration: '1天', tool: '社保中心' },
      { name: '获取社保账号', duration: '1-2天', tool: '社保中心' },
      { name: '添加员工信息', duration: '1天', tool: '社保网上服务平台' },
      { name: '办理公积金（如需）', duration: '3-5天', tool: '公积金中心' }
    ]
  }
};

// 生成Markdown格式的检查清单
function generateMarkdownChecklist() {
  let md = `# 创业流程检查清单

> 生成时间：${new Date().toLocaleDateString('zh-CN')}
> 版本：v1.0

## 快速导航

| 流程 | 周期 | 费用 |
|------|------|------|
`;

  for (const [key, value] of Object.entries(checklistData)) {
    md += `| [${key}](#${key.toLowerCase().replace(/\s+/g, '-')}) | ${value.周期} | ${value.费用} |\n`;
  }

  md += `
---

## 详细流程

`;

  for (const [key, value] of Object.entries(checklistData)) {
    md += `### ${key}

**周期**: ${value.周期}
**费用**: ${value.费用}

**步骤清单**:

| 序号 | 步骤 | 时长 | 操作入口 |
|------|------|------|----------|
`;

    value.步骤.forEach((step, index) => {
      md += `| ${index + 1} | ${step.name} | ${step.duration} | ${step.tool} |\n`;
    });

    md += `
---
`;
  }

  md += `
## 费用汇总

| 流程 | 一次性费用 | 年度费用 | 备注 |
|------|------------|----------|------|
| 公司注册 | 500-2000元 | - | 代理服务费 |
| 代理记账 | - | 2000-6000元 | 小规模/一般纳税人 |
| 银行开户 | 300-1000元 | 300-1000元 | 年费 |
| 社保开户 | 免费 | - | - |
| 商标注册 | 270元/类 | - | 官费 |
| 云服务器 | - | 500-3000元 | 根据配置 |
| 域名 | - | 20-100元 | 每年续费 |
| **合计** | **1000-5000元** | **4000-10000元** | **首年** |

---

## 注意事项

### ⚠️ 公司注册
- 注册资本2024年新公司法要求5年内实缴到位
- 注册地址须为商用或综合用途
- 建议多准备几个名称备选

### ⚠️ ICP备案
- 备案期间服务器会被暂停访问
- 一个企业可备案多个网站
- 法人需配合接收短信验证码

### ⚠️ 商标注册
- 申请前务必进行商标查询
- 商品分类选择要覆盖当前及未来业务
- 恶意抢注会被驳回并纳入信用档案

### ⚠️ 税务
- 领取营业执照30日内必须完成税务登记
- 即使无业务也要进行零申报
- 未按时报税会被罚款

---

*本清单由创业启动助手智能体生成*
`;

  return md;
}

// 主函数
function main() {
  const outputPath = path.join(__dirname, '..', 'assets', 'startup-checklist.md');
  const markdown = generateMarkdownChecklist();

  fs.mkdirSync(path.dirname(outputPath), { recursive: true });
  fs.writeFileSync(outputPath, markdown, 'utf-8');

  console.log(`✅ 检查清单已生成: ${outputPath}`);
  console.log(`📄 共 ${markdown.split('\n').length} 行`);
}

// 运行
main();
