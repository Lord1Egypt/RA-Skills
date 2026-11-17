# 维修报告模板

## 标准文本报告格式

```
## 🔧 {设备名称} 故障诊断报告

### 📋 故障摘要
- **设备**：{品牌} {型号}（使用 {X} 年）
- **故障现象**：{用户描述}
- **诊断结论**：{最可能原因}
- **置信度**：{高/中/低}
- **严重程度**：P{0/1/2} — {说明}
- **诊断依据**：{简述推理链条}

---

### 🚨 安全警告
{如涉及燃气/高压电/高空作业，在此详细列出安全注意事项}

---

### 🔍 方案一：快速自查（推荐先试试）
**难度**：★☆☆☆☆ | **成本**：0 元 | **耗时**：{X} 分钟 | **成功率**：{XX}%

1. {步骤一（具体动作）}
2. {步骤二}
3. {步骤三}

⚠️ 注意：{操作注意事项}

---

### 🛠️ 方案二：DIY 维修
**难度**：{★★★☆☆} | **成本**：{XX-XX} 元 | **耗时**：{XX} 分钟

**所需配件：**
| 配件 | 规格/型号 | 参考价格 | 购买关键词 |
|------|----------|----------|-----------|
| {名称} | {规格} | {价格} | {淘宝/京东搜索词} |

**所需工具：**
{工具清单}

**操作步骤：**
1. ⚠️ 先{断电/断水/断气}！
2. {步骤一详细描述}
3. {步骤二详细描述}
4. {步骤三详细描述}
5. 复原并测试

🔗 视频参考：B站/抖音搜"{关键词}"

---

### 👨‍🔧 方案三：专业维修
- **渠道**：官方售后（400-XXX-XXXX）/ 社区维修店 / 58同城搜索"{关键词}"
- **预估费用**：{价格区间} 元（人工 {X} + 材料 {X}）
- **时效**：{当场修好 / 需等配件 X 天 / 需返厂 X 天}

**找师傅注意事项：**
1. 先电话确认能否修、大概价格
2. 要求出示收费标准
3. 保留旧零件
4. 索要收据（注明保修期）

---

### 📊 三方案对比
| 维度 | 方案一：自查 | 方案二：DIY | 方案三：送修 |
|------|:----------:|:----------:|:----------:|
| 成本 | 0 元 | XX-XX 元 | XX-XX 元 |
| 耗时 | X 分钟 | X 分钟 | X 天 |
| 难度 | ★☆☆☆☆ | ★★★☆☆ | — |
| 风险 | 低 | 中 | 低 |
| 推荐场景 | 先试试 | 有动手能力 | 没时间/没把握 |

### 🎯 推荐方案
{综合分析，给出推荐}

---

### 💡 预防建议
1. {如何避免再次出现此故障}
2. {日常保养建议}

---

### 📞 紧急联系
- 燃气公司：95158（新奥）/ 当地燃气公司电话
- 供电局：95598
- 自来水公司：当地供水热线
- 开锁：110联动开锁（或当地备案开锁公司）
```

## HTML 可视化报告（可选）

当用户说"生成报告"、"保存下来"、"可视化"时，使用以下模板生成交互式 HTML 报告：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>维修报告 — {设备名称}</title>
<style>
  :root {
    --bg: #f5f0e8;
    --card: #fffef9;
    --border: #d4c5a9;
    --text: #3d3226;
    --accent: #c0392b;
    --green: #27ae60;
    --blue: #2980b9;
    --tag-bg: #fef3e2;
  }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    font-family: "PingFang SC", "Microsoft YaHei", "Noto Sans SC", sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.7;
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
  }
  .report-header {
    text-align: center;
    padding: 30px 0 20px;
    border-bottom: 2px solid var(--border);
    margin-bottom: 20px;
  }
  .report-header h1 { font-size: 24px; margin-bottom: 8px; }
  .report-header .meta { color: #888; font-size: 14px; }
  .card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 16px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
  }
  .card h2 {
    font-size: 18px;
    margin-bottom: 12px;
    padding-bottom: 8px;
    border-bottom: 1px dashed var(--border);
  }
  .severity { display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; }
  .severity.p0 { background: #fde8e8; color: #c0392b; }
  .severity.p1 { background: #fef3e2; color: #e67e22; }
  .severity.p2 { background: #e8f5e9; color: #27ae60; }
  .safety-warning {
    background: #fde8e8;
    border-left: 4px solid #c0392b;
    padding: 12px 16px;
    margin: 10px 0;
    border-radius: 0 6px 6px 0;
  }
  .safety-warning::before { content: "⚠️ 安全警告"; font-weight: bold; display: block; margin-bottom: 4px; }
  table { width: 100%; border-collapse: collapse; margin: 10px 0; }
  th, td { padding: 10px 12px; border-bottom: 1px solid var(--border); text-align: left; font-size: 14px; }
  th { background: var(--tag-bg); font-weight: 600; }
  .steps { padding-left: 20px; }
  .steps li { margin-bottom: 8px; }
  .tag { display: inline-block; background: var(--tag-bg); padding: 2px 8px; border-radius: 4px; font-size: 12px; margin-right: 4px; }
  .cost { font-size: 20px; font-weight: bold; color: var(--accent); }
  .comparison-table th:first-child { width: 20%; }
  .footer { text-align: center; color: #aaa; font-size: 12px; padding: 20px; }
  @media print {
    body { background: #fff; }
    .card { box-shadow: none; break-inside: avoid; }
  }
</style>
</head>
<body>

<div class="report-header">
  <h1>🔧 {设备名称} 维修报告</h1>
  <p class="meta">生成时间：{日期} | WorkBuddy 维修工</p>
</div>

<div class="card">
  <h2>📋 故障摘要</h2>
  <table>
    <tr><td style="width:80px;color:#888">设备</td><td>{品牌} {型号}</td></tr>
    <tr><td style="color:#888">使用年限</td><td>{X} 年</td></tr>
    <tr><td style="color:#888">故障现象</td><td>{描述}</td></tr>
    <tr><td style="color:#888">诊断结论</td><td><strong>{结论}</strong></td></tr>
    <tr><td style="color:#888">置信度</td><td>{高/中/低}</td></tr>
    <tr><td style="color:#888">严重程度</td><td><span class="severity p{N}">P{N}</span></td></tr>
  </table>
</div>

<!-- 安全警告 -->
<div class="card" style="border-color:#c0392b;">
  <h2>🚨 安全须知</h2>
  <div class="safety-warning">{安全警告内容}</div>
</div>

<!-- 方案一：自查 -->
<div class="card">
  <h2>🔍 方案一：快速自查</h2>
  <p><span class="tag">难度 ★☆☆☆☆</span> <span class="tag">成本 0元</span> <span class="tag">{X}分钟</span></p>
  <ol class="steps">
    <li>{步骤1}</li>
    <li>{步骤2}</li>
    <li>{步骤3}</li>
  </ol>
</div>

<!-- 方案二：DIY -->
<div class="card">
  <h2>🛠️ 方案二：DIY 维修</h2>
  <p><span class="tag">难度 {★★★☆☆}</span> <span class="tag">成本 {XX}元</span> <span class="tag">{X}分钟</span></p>
  <h3 style="font-size:15px;margin:12px 0 6px;">所需配件</h3>
  <table>
    <tr><th>配件</th><th>规格</th><th>参考价</th></tr>
    <tr><td>{配件}</td><td>{规格}</td><td>{价格}</td></tr>
  </table>
  <h3 style="font-size:15px;margin:12px 0 6px;">操作步骤</h3>
  <ol class="steps">
    <li>{步骤1}</li>
    <li>{步骤2}</li>
  </ol>
</div>

<!-- 方案三：送修 -->
<div class="card">
  <h2>👨‍🔧 方案三：专业维修</h2>
  <p><strong>预估费用</strong>：<span class="cost">{XX}元</span></p>
  <p><strong>渠道</strong>：{官方售后 / 58同城搜}"{关键词}"</p>
</div>

<!-- 方案对比 -->
<div class="card">
  <h2>📊 三方案对比</h2>
  <table class="comparison-table">
    <tr><th>维度</th><th>自查</th><th>DIY</th><th>送修</th></tr>
    <tr><td>成本</td><td>0元</td><td>XX元</td><td>XX元</td></tr>
    <tr><td>耗时</td><td>X分</td><td>X分</td><td>X天</td></tr>
    <tr><td>难度</td><td>★</td><td>★★★</td><td>—</td></tr>
    <tr><td>推荐</td><td>先试</td><td>⭐推荐</td><td>备选</td></tr>
  </table>
</div>

<!-- 预防建议 -->
<div class="card">
  <h2>💡 预防建议</h2>
  <ol class="steps">
    <li>{建议1}</li>
    <li>{建议2}</li>
  </ol>
</div>

<div class="footer">WorkBuddy 维修工 · 仅供参考，安全第一</div>

</body>
</html>
```

### HTML 报告使用说明

1. 将上述模板中的 `{占位符}` 替换为实际诊断内容
2. 如果不需要某个方案（如不需要送修），删除对应 card
3. 安全警告 card 在无 P0/P1 风险时可删除
4. 生成的 HTML 文件保存到工作目录供用户保存/打印
