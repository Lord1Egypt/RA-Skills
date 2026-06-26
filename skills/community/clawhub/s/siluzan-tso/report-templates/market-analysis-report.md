# 战略市场分析报告（交付模板）

> **最终交付物**：可打开的 `market-analysis-report.html`。  
> **质量门禁**：`render` 按 **TSO getMarketReport 原始业务维度** 校验 HTML，缺项失败（非文件大小）。

---

## 数据流

```
collect → Agent 按维度清单调研撰写 → market-report.json → render → HTML
```

---

## Agent 必读

- `assets/market-analysis-rules.md` — **原始业务维度清单**（校验依据）
- `collect` 中的 `customerInfo`、`websitePreview`

---

## 交付前自检（对照维度清单）

### 六大章 + 附录

- [ ] **一、市场与趋势**：TAM/SAM/SOM、价值链、国家拆解、PESTEL、3–5 年预测
- [ ] **二、行业洞察**：≥4 痛点、合规模块、BPMN 流程对比 + 量化
- [ ] **三、受众场景**：受众分层表、场景价值 + 图表
- [ ] **四、竞争定位**：≥3 竞品、≥10 行对比表、四类空白、定位陈述
- [ ] **五、增长品牌**：GTM 三阶段、品牌传播、营销战术
- [ ] **六、实施风险**：里程碑表、预算、风险矩阵
- [ ] **附录**：来源清单、调研方法、术语表（ROI/CAGR/GTM/BPMN）

### 呈现

- [ ] ECharts 图表（`homeCDN/echarts.js`）+ Source 脚注
- [ ] 已 `render` 成功（无「缺少 N 项必含内容」）

**不通过** → 针对 CLI 列出的缺失维度补研扩写，勿交付简版。
