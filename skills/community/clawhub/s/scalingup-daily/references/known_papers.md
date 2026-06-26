# 已知核心论文列表（去重 + 机构归属参考）

> **强制规则**：论文机构归属必须基于**作者 affiliation** 而非部署业务线推断。
> 遇到不确定的机构归属时，优先 `web_fetch` arxiv 页面核对作者 affiliation。

以下论文已在之前的日报中收录，检索时跳过，不需要重复列出。

---

## 字节跳动（ByteDance）— 推荐排序架构系列

| 论文 | arXiv ID | 年月 | 核心贡献 |
|------|----------|------|---------|
| RankMixer | 2507.15551 | 2025-07 | 抖音广告排序，Multi-head Token Mixing + Per-token FFN |
| TokenMixer-Large | 2602.06563 | 2026-02 | RankMixer 的 15B 参数升级版，Mixing & Reverting |
| OneTrans | 2510.26104 | 2025-10 | 统一特征交互与序列建模，WWW 2026 |
| HyFormer | 2601.12681 | 2026-01 | CTR 特征交互与序列建模 |
| MixFormer | 2602.14110 | 2026-02 | RankMixer × LONGER 统一化升级 |
| MDL | 2602.07520 | 2026-02 | 多分布统一学习 + Tokenization |
| LONGER | 2505.04421 | 2025-05 | 长序列行为建模，RecSys 2025 |

## 腾讯广告（Tencent Ads）— 独立团队，与字节系列无传承关系

| 论文 | arXiv ID | 年月 | 核心贡献 |
|------|----------|------|---------|
| RankUp | 2604.17878 | 2026-04 | 腾讯广告独立工作，**不是 RankMixer 续作**；研究"有效秩随深度振荡"问题 |
| OneRanker | 2603.02999 | 2026-03 | 腾讯广告生成式排序统一建模 |
| TokenFormer | 2604.13737 | 2026-04 | 腾讯广告，统一多域推荐与序列建模 |
| Tencent Ad Challenge 2025 | 2604.04976 | 2026-04 | 腾讯广告全模态数据集（TencentGR-1M / TencentGR-10M）|

## Meta — 大规模推荐系统

| 论文 | arXiv ID | 年月 | 核心贡献 |
|------|----------|------|---------|
| Kunlun | 2602.10016 | 2026-02 | 大规模推荐系统 2 倍 Scaling 效率提升，MFU 37% |
| ULTRA-HSTU | 2602.16986 | 2026-02 | 端到端系统协同设计，训练 5x/推理 21x 提速 |
| HSTU | — | 2024 | Actions Speak Louder than Words，ICML 2024 |
| Wukong | 2403.02545 | 2024 | 推荐系统 Scaling Law 验证，ICML 2024 |

## 快手（Kuaishou）

| 论文 | arXiv ID | 年月 | 核心贡献 |
|------|----------|------|---------|
| OneRec | 2502.18965 | 2025-02 | 端到端生成式推荐 |
| GR4AD | 2602.22732 | 2026-02 | 大规模广告生成式推荐 |
| UniMixer | 2604.00590 | 2026-04 | Attention/TokenMixer/FM 统一 |
| Align³GR | 2511.11255 | 2025-11 | AAAI 2026 Oral |
| OneSug | — | 2026 | AAAI 2026 |

## 阿里巴巴（Alibaba）

| 论文 | arXiv ID | 年月 | 核心贡献 |
|------|----------|------|---------|
| SUAN | 2508.15326 | 2025-08 | CTR Scaling Law 工业落地，RecSys 2025（阿里 × 美团合作）|
| EST | 2602.10811 | 2026-02 | 高效统一 CTR Scaling |
| RecGPT-V2 | 2512.14503 | 2025-12 | 生成式推荐 |

## 其他重要团队

| 论文 | arXiv ID | 机构 | 核心贡献 |
|------|----------|------|---------|
| MTGR | — | 美团 | 基于 HSTU，美团外卖推荐落地 |
| Climber | 2502.09888 | 网易云音乐 | CIKM 2025 |
| CADET | 2602.11410 | LinkedIn | Context-Conditioned Ads Decoder Transformer |
| GenRec | 2604.14878 | 京东 | SIGIR 2026 Camera-Ready |
| NEO | 2603.17533 | 微软 × Spotify | 协同推荐 |
| MBGen | 2405.16871 | UCSB | 多行为生成式推荐 |
| LLaTTE | 2501.02032 | Meta | LLM as Feature Encoder，AAAI 2025 |
| STCA | 2511.09741 | 字节跳动 | Spatio-Temporal CTR Attention |

---

## 归属判定关键规则（强制）

1. **不要按论文的部署场景/业务线推断作者团队**：RankUp 部署在微信广告，团队归属仍是**腾讯广告**而不是"微信"或"腾讯+微信"；MTGR 部署在美团外卖，团队是**美团外卖推荐技术团队**。
2. **不要仅因两篇论文研究相近问题就判定为"同团队续作"**：RankUp 研究 RankMixer 提出的秩问题，但两者分别来自**腾讯广告**和**字节跳动**，是独立团队的独立工作。
3. **写日报遇到不确定的机构归属时，优先 web_fetch arxiv 页面核对作者 affiliation**（尤其是第一作者、通讯作者和知名研究员），不要凭记忆或第一直觉填写。
4. **RankMixer / TokenMixer-Large / OneTrans / HyFormer / MixFormer / MDL / LONGER 全部归字节跳动，不要误写为腾讯或其他**。

---

## GitHub 开源项目

- SUAN: https://github.com/laiweijiang/SUAN
- OneRec/OpenOneRec: https://github.com/Kuaishou-OneRec/OpenOneRec
- Meta generative-recommenders: https://github.com/meta-recsys/generative-recommenders
- Monolith: https://github.com/bytedance/monolith
- DeepCTR-Torch: https://github.com/shenweichen/DeepCTR-Torch
- Awesome-Generative-Recommendation: https://github.com/uestc-huangyw/Awesome-Generative-Recommendation
- RecBole: https://github.com/RUCAIBox/RecBole
