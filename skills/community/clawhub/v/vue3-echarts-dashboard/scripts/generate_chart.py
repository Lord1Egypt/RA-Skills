#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
vue3-echarts-codegen 生成器（离线兜底，不依赖 plop）。

产出（相对 <target>/src，均为自包含、彼此弱耦合）：
  hooks/charts/builders/<kebab>.ts      # 选项构造器（自带 data/config 类型，纯函数）
  hooks/charts/use<Pascal>Chart.ts      # 业务组合式函数（内置 ECharts 生命周期，不依赖共享文件）
  components/charts/<Pascal>Chart.vue   # UI 组件

说明：每个生成的图表都是独立单元，只依赖自身的 hook + builder，放进任意
Vue3 项目即可用；不会注入/覆盖任何共享 useECharts.ts。
如需集中治理生命周期，可手动采用 assets/use-echarts.ts（可选共享 composable）。

用法：
  python generate_chart.py --target <项目根> --name sales-trend --type line
  python generate_chart.py --target <项目根> --name my-pie --type pie --dry-run
  python generate_chart.py --target <项目根> --name custom-x --type custom --force
"""
import argparse
import os
import re
import sys

SKILL_ROOT = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.dirname(SKILL_ROOT)  # 上一级 = skill 根
ASSETS = os.path.join(SKILL_ROOT, "assets")

BUILDERS = {
    # 第一行：趋势 / 分布 / 对比
    "line": "builders/line.ts",
    "bar": "builders/bar.ts",
    "pie": "builders/pie.ts",
    "scatter": "builders/scatter.ts",
    "radar": "builders/radar.ts",
    # 第二行：指标 / 占比
    "gauge": "builders/gauge.ts",
    "kpi": "builders/kpi.ts",
    "funnel": "builders/funnel.ts",
    "liquidfill": "builders/liquidfill.ts",
    "wordcloud": "builders/wordcloud.ts",
    # 第三行：关系 / 结构 / 地理（map 需 registerMap，liquidfill / wordcloud 需装插件）
    "sunburst": "builders/sunburst.ts",
    "sankey": "builders/sankey.ts",
    "treemap": "builders/treemap.ts",
    "heatmap": "builders/heatmap.ts",
    "map": "builders/map.ts",
}


def to_pascal(name: str) -> str:
    parts = re.split(r"[-_\s]+|(?<=[a-z])(?=[A-Z])", name)
    return "".join(p[:1].upper() + p[1:] for p in parts if p)


def to_kebab(name: str) -> str:
    s = re.sub(r"(?<=[a-z])(?=[A-Z])", "-", name)
    s = re.sub(r"[\s_]+", "-", s)
    return s.lower()


def read_asset(rel: str) -> str:
    with open(os.path.join(ASSETS, rel), encoding="utf-8") as f:
        return f.read()


def render(template: str, **kw) -> str:
    for k, v in kw.items():
        template = template.replace("{{%s}}" % k, v)
    return template


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate Vue3 + TS ECharts chart encapsulation")
    ap.add_argument("--target", required=True, help="project root (must contain src/)")
    ap.add_argument("--name", required=True, help="chart name, e.g. sales-trend")
    ap.add_argument(
        "--type",
        default="line",
        choices=sorted(BUILDERS.keys()) + ["custom"],
        help="chart type",
    )
    ap.add_argument("--dry-run", action="store_true", help="print plan, write nothing")
    ap.add_argument("--force", action="store_true", help="overwrite existing files")
    args = ap.parse_args()

    pascal = to_pascal(args.name)
    kebab = to_kebab(args.name)
    root = os.path.abspath(args.target)
    src = os.path.join(root, "src")

    if not os.path.isdir(src):
        print("[ERROR] 找不到 %s，请确认 --target 指向含 src/ 的项目根" % src, file=sys.stderr)
        return 2

    hooks_charts = os.path.join(src, "hooks", "charts")
    comp_charts = os.path.join(src, "components", "charts")

    builder_file = os.path.join(hooks_charts, "builders", "%s.ts" % kebab)
    hook_file = os.path.join(hooks_charts, "use%sChart.ts" % pascal)
    comp_file = os.path.join(comp_charts, "%sChart.vue" % pascal)

    files = {}

    # 1) 选项构造器
    if args.type == "custom":
        builder_src = read_asset("builders/_custom.ts")
    else:
        builder_src = read_asset(BUILDERS[args.type])
    files[builder_file] = builder_src

    # 2) 业务组合式函数（自包含，不依赖共享 composable）
    hook_tpl = read_asset("chart-hook.ts")
    files[hook_file] = render(hook_tpl, PASCAL=pascal, KEBAB=kebab)

    # 3) UI 组件
    comp_tpl = read_asset("chart-component.vue")
    files[comp_file] = render(comp_tpl, PASCAL=pascal, KEBAB=kebab)

    # 写出
    if args.dry_run:
        for path in files:
            print("[DRY-RUN] 将写入 %s" % path)
        print("\n类型=%s  Pascal=%s  Kebab=%s" % (args.type, pascal, kebab))
        print("下一步：在用到图表的地方 <%sChart :data=\"...\" />" % pascal)
        return 0

    written, skipped = [], []
    for path, content in files.items():
        if os.path.exists(path) and not args.force:
            skipped.append(path)
            continue
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        written.append(path)

    for p in written:
        print("[WRITE] %s" % p)
    for p in skipped:
        print("[SKIP ] 已存在（--force 可覆盖）: %s" % p)

    print("\n完成。%d 个文件写入，%d 个跳过。" % (len(written), len(skipped)))
    print("提醒：项目需安装 echarts（npm i echarts）；若 @ 不是 src 别名，请调整导入路径。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
