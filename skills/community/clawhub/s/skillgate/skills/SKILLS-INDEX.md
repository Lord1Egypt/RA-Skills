# 医械法规技能目录

> 所有医械法规检查 skill 的清单——用户和 AI 都能一眼看出来每个是做什么的。

---

## 📋 技能总览

| # | 技能名 | 做什么 | 适用分类 |
|---|--------|--------|---------|
| 1 | `reg-citation-normalizer` | 法规引用格式规范化 | 所有 |
| 2 | `medxpert-termbase` | 双语术语库 + 译稿 QA | 所有 |
| 3 | `iso14971-risk-matrix` | 风险管理矩阵 + 文件自查 | 所有 |
| 4 | `iec62366-usability-check` | 可用性工程文件检查 | II 类、III 类 |
| 5 | `iec62304-sdlc-check` | 软件生命周期检查 | II 类、III 类 |
| 6 | `iso10993-biocompatibility-check` | 生物相容性报告检查 | II 类、III 类 |
| 7 | `cer-clinical-evaluation-check` | CER 临床评价报告检查 | II 类、III 类 |
| 8 | `iso13485-qms-check` | 质量管理体系文件检查 | 所有 |
| 9 | `ifu-labeling-check` | 标签和说明书（IFU）检查 | 所有 |
| 10 | `pms-post-market-check` | 上市后监督（PMS）检查 | 所有 |
| 11 | `change-control-check` | 变更控制程序检查 | 所有 |
| 12 | `ai-medical-algorithm-check` | 医疗 AI 算法验证检查 | AI 医械 |
| 13 | `ai-dataset-quality-check` | 医疗 AI 数据集质量检查 | AI 医械 |
| 14 | `iec60601-electrical-safety-check` | 电气安全检查（GB 9706.1） | II 类、III 类 |
| 15 | `iec81001-cybersecurity-check` | 网络安全检查（IEC 81001） | II 类、III 类 |

---

## 🏷️ 按分类整理

### 📦 基础合规（所有分类都要做）
- `reg-citation-normalizer` — 引用格式
- `medxpert-termbase` — 术语库
- `iso14971-risk-matrix` — 风险管理
- `iso13485-qms-check` — 质量管理体系
- `ifu-labeling-check` — 标签说明书
- `pms-post-market-check` — 上市后监督
- `change-control-check` — 变更控制

### 🔬 进阶合规（II 类、III 类要做）
- `iec62366-usability-check` — 可用性工程
- `iec62304-sdlc-check` — 软件生命周期
- `iso10993-biocompatibility-check` — 生物相容性
- `cer-clinical-evaluation-check` — 临床评价

### 🤖 医疗 AI 专用
- `ai-medical-algorithm-check` — 算法验证
- `ai-dataset-quality-check` — 数据集质量

---

## 🚀 一键跑

```bash
# 第 1 类（低风险）
python medical-device-chain.py 文档.md 1

# 第 2 类（中风险）
python medical-device-chain.py 文档.md 2

# 第 3 类（高风险）
python medical-device-chain.py 文档.md 3
```

---

## ✅ 特点

- ✅ 全部本地运行，不联网
- ✅ 每个检查都有建议——告诉你应该怎么写
- ✅ 按分类调整严格程度——I 类少做，III 类多做
- ✅ 每个 skill 都能单独跑，也能串成链跑
