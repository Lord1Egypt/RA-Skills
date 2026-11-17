# audited 徽章说明

`yotta_verify.py badge <path> [--out assets/audited.svg]` 生成 audited 徽章
（本地 SVG + shields.io URL），内容 = **verdict + validate-skill + 元安/元审 verdict + 版本 + 引擎测试数**。

## 内容

| 段 | 来源 | 说明 |
|---|---|---|
| verified | scan verdict | SAFE TO INSTALL（绿）/ REVIEW（橙）/ CAUTION（黄）/ DO NOT INSTALL（红） |
| validate-skill | --validate-skill pass/fail | 发布校验结果 |
| vetter | --vetter-verdict | 元审 verdict（传入合并） |
| audit | --audit-verdict | 元安 verdict（传入合并） |
| version | --version | 包版本 |
| tests | --tests N | 引擎自测数 |

## 用法

```bash
# 直接扫描并生成（推荐：verdict 来自真实扫描）
python3 scripts/yotta_verify.py badge ./some-skill --out assets/audited.svg

# 合并验证结果（元审/元安 verdict + validate-skill + 测试数）
python3 scripts/yotta_verify.py badge ./some-skill \
    --validate-skill pass --vetter-verdict "SAFE TO INSTALL" \
    --audit-verdict "SAFE TO INSTALL" --version 0.1.1 --tests 52
```

输出：本地 SVG（随包发布到 assets/audited.svg）+ shields.io URL。

## 嵌入 README

```markdown
![verified](../assets/audited.svg)
```

或使用 shields.io 动态徽章：

```markdown
![verified](https://img.shields.io/badge/verified-SAFE%20TO%20INSTALL-brightgreen)
```

