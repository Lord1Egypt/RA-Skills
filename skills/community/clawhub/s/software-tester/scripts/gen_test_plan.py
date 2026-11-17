#!/usr/bin/env python3
"""Generate a test plan Markdown from a module name and feature list.

Usage:
    python3 scripts/gen_test_plan.py --name 支付模块 --features 创建订单,退款,对账
    python3 scripts/gen_test_plan.py --name 用户服务 --features 注册,登录 --output plan.md
"""
import argparse
import sys
from datetime import date


TEMPLATE = """\
# 测试计划：{name}

> 自动生成于 {date}。结合 references/test-strategy.md 调整金字塔比例与准入准出标准。

## 1. 范围（Scope）
- 模块 / 功能：{name}
- 不在范围内：（填写：明确排除的模块、平台、场景）

### 被测功能
{features_bullets}

## 2. 测试策略（测试金字塔）
- 单元测试 ~70%：每个功能的纯逻辑与边界
- 集成测试 ~20%：模块间协作、数据库、外部依赖
- E2E ~10%：仅核心用户链路

## 3. 测试环境
- 语言/框架：（按项目选择 pytest / jest / vitest）
- 数据：使用独立测试库或 mock，禁止污染生产
- CI：覆盖率门禁见 assets/ci-coverage.yml

## 4. 用例清单（按功能）
{feature_sections}

## 5. 准入 / 准出标准
- 准出：核心模块行覆盖 ≥ 90%，分支覆盖 ≥ 85%；关键 E2E 全绿；无高危安全风险
- 阻断：存在高危安全漏洞或覆盖率大幅回退

## 6. 风险与依赖
- （填写：外部依赖、环境限制、已知脆弱点）
"""


def feature_section(name):
    return f"""\
### {name}
- [ ] 正常路径
- [ ] 边界值（空/最大/超长/特殊字符）
- [ ] 异常路径（缺参/格式错/资源不存在）
- [ ] 鉴权/权限（匿名/越权）
- [ ] 性能（如涉及，p95 阈值）
"""


def main():
    ap = argparse.ArgumentParser(description="Generate a test plan Markdown.")
    ap.add_argument("--name", required=True, help="module name")
    ap.add_argument("--features", required=True, help="comma-separated feature list")
    ap.add_argument("--output", help="write to file instead of stdout")
    args = ap.parse_args()

    features = [f.strip() for f in args.features.split(",") if f.strip()]
    bullets = "\n".join(f"- {f}" for f in features)
    sections = "\n".join(feature_section(f) for f in features)
    doc = TEMPLATE.format(
        name=args.name,
        date=date.today().isoformat(),
        features_bullets=bullets,
        feature_sections=sections,
    )
    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(doc)
        print(f"written: {args.output}", file=sys.stderr)
    else:
        print(doc)


if __name__ == "__main__":
    main()
