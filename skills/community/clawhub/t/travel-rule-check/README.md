# 旅行规则校验（Travel-Rule Check）

LGD 三律在「链上资产 / VASP 旅行规则（FATF）」域的纵深合规工具：VASP 转账收发方 KYC（姓名+账号/地址+地理）超阈强制校验（零依赖）。

## 痛点
链上转账收发方 KYC（旅行规则）缺乏轻量校验，易踩反洗钱合规红线。

## 快速开始
```bash
python travel_rule_check.py --help
```

## 三律落地
- 有籍 → 系统/数据身份登记（本域术语）
- 有证 → 证据工件可核验（本域证据类型）
- 有门禁 → 高风险动作过门禁（本域阈值）

## 竞争优势定位
本技能是"凡自治之物"标准在链上资产 / VASP 旅行规则（FATF）域的**纵深落地件**——别人可抄功能，抄不走标准定义权。

![LGD-Powered](lgd-powered.png)

---

## License & attribution
**分层许可（务必并读；代码许可不覆盖文档与理论文本）**

- **代码**（本包 `.py` 文件）：**MIT**
- **本 `README.md` / `SKILL.md` 及其中的理论文本、方法论与一切理论表述**：**不在 MIT 覆盖范围内**，保留所有权利（All rights reserved）

```
© 2026 SynomosAI. All rights reserved.
理论署名 (attribution) : LGD（Lifecycle Governance Doctrine / 全程治理论）— SynomosAI initiative
名称状态 (name status)  : "SynomosAI" — 未申请实体注册、未申请商标注册
                        (not a registered legal entity; no trademark registered)
生产参考部署 (production reference, self-reported) : 无（未声明外部生产参考部署）
                    ← 非认证、非背书、非监管认可（not a certification or endorsement）
代码许可 (code license) : 本包未附 LICENSE 文件（许可待定）
                    本文本与理论表述不在任何代码许可覆盖范围内
引用格式 (cite as)      : 本资产无 DOI
```
（上列为《LGD 对外表述规范》§3.2 统一块，**整体复制、未删改**；发布/重提前须照最新版本复核。）
