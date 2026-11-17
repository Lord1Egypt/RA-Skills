---
title: README
type: note
permalink: internal/vault (neutralized)
---

# Reg Citation Normalizer / 法规引用规范化器

## English

Normalize medical-device regulatory citations: `21 CFR 820.30(a)(6)`, `ISO 13485:2016 clause 7.5.1`, `YY/T 0287-2017 7.5.1`, NMPA decrees — parse them into a canonical structure with standard formatting suggestions.

```bash
python scripts/cite_normalize.py normalize "product meets ISO 13485:2016 clause 7.5.1 and 21 CFR 820.30"
python scripts/cite_normalize.py parse "YY/T 0287-2017 7.5.1" --json
python scripts/cite_normalize.py check your-doc.md
```

**Features**: four grammars (US 21 CFR / ISO·IEC / Chinese GB·YY / NMPA decrees), agency normalization (SFDA→CFDA→NMPA), 9 errata classes, batch `check` (exit 1 for CI), zero-dependency offline.

**Related**: `udi-validator` (UDI parsing), `iso14971-risk-matrix`, this tool = citation normalization.

## 中文

把 `21 CFR 820.30(a)(6)`、`ISO 13485:2016 clause 7.5.1`、`YY/T 0287-2017 7.5.1`、NMPA 部令等写法解析为规范结构并输出标准书写建议。

```bash
python scripts/cite_normalize.py normalize "产品符合 ISO 13485:2016 clause 7.5.1 和 21 CFR 820.30 要求"
python scripts/cite_normalize.py parse "YY/T 0287-2017 7.5.1" --json
python scripts/cite_normalize.py check 你的文档.md
```

**特性**：四类文法（21 CFR / ISO·IEC / 中国 GB·YY / NMPA 部令）、机构沿革归一化、9 类勘误、批量 check（CI exit 1）、零依赖离线。

**关联**：`udi-validator`（UDI 解析）、`iso14971-risk-matrix`；本工具为法规引用规范化。

## License

MIT
