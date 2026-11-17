#!/usr/bin/env python3
"""校验 Vue3 大屏脚手架模板/复制结果的完整性。

用法:
    python verify_scaffold.py <项目目录>

校验项:
    - 必需文件齐全（package.json / vite.config.ts / src 结构与 public/data 十六个 JSON）
    - package.json 包含约定依赖（vue/echarts/axios/pinia/element-plus/vue3-digital-flop）
    - public/data/*.json 均可解析，且与类型契约字段对应
"""
import argparse
import json
import os
import sys

REQUIRED_FILES = [
    "package.json",
    "vite.config.ts",
    "tsconfig.json",
    "index.html",
    "src/main.ts",
    "src/App.vue",
    "src/env.d.ts",
    "src/api/index.ts",
    "src/stores/dashboard.ts",
    "src/types/index.ts",
    "src/theme/theme.ts",
    "src/theme/index.ts",
    "src/styles/theme.css",
    "src/components/KpiCard.vue",
    "src/components/ChartPanel.vue",
    "src/components/FullscreenBtn.vue",
    "src/views/BigScreen.vue",
    "public/data/kpi.json",
    "public/data/trend.json",
    "public/data/product.json",
    "public/data/channel.json",
    "public/data/profit.json",
    "public/data/region.json",
    "public/data/funnel.json",
    "public/data/gauge.json",
    "public/data/scatter.json",
    "public/data/sunburst.json",
    "public/data/sankey.json",
    "public/data/tree.json",
    "public/data/heatmap.json",
    "public/data/map.json",
    "public/data/wordcloud.json",
    "public/data/china.json",
]

REQUIRED_DEPS = ["vue", "echarts", "axios", "pinia", "element-plus", "vue3-digital-flop"]
REQUIRED_DEVDEPS = ["vite", "typescript", "vue-tsc", "@vitejs/plugin-vue"]

DATA_SHAPES = {
    "kpi.json": lambda d: isinstance(d, list) and all("value" in i for i in d),
    "trend.json": lambda d: {"categories", "values"} <= set(d),
    "product.json": lambda d: isinstance(d.get("items"), list),
    "channel.json": lambda d: {"categories", "values"} <= set(d),
    "profit.json": lambda d: {"categories", "values"} <= set(d),
    "region.json": lambda d: isinstance(d.get("indicators"), list) and isinstance(d.get("values"), list),
    "funnel.json": lambda d: isinstance(d.get("items"), list),
    "gauge.json": lambda d: {"value", "max"} <= set(d),
    "scatter.json": lambda d: isinstance(d.get("points"), list),
    "sunburst.json": lambda d: isinstance(d.get("items"), list),
    "sankey.json": lambda d: isinstance(d.get("nodes"), list) and isinstance(d.get("links"), list),
    "tree.json": lambda d: isinstance(d.get("items"), dict),
    "heatmap.json": lambda d: isinstance(d.get("values"), list) and isinstance(d.get("series"), list),
    "map.json": lambda d: isinstance(d.get("items"), list),
    "wordcloud.json": lambda d: isinstance(d.get("items"), list),
    "china.json": lambda d: isinstance(d.get("features"), list),
}


def main():
    parser = argparse.ArgumentParser(description="校验 Vue3 大屏脚手架")
    parser.add_argument("dir", help="项目目录")
    args = parser.parse_args()

    problems = []
    root = args.dir
    for rel in REQUIRED_FILES:
        if not os.path.isfile(os.path.join(root, rel)):
            problems.append("缺少文件: %s" % rel)

    pkg_path = os.path.join(root, "package.json")
    if os.path.isfile(pkg_path):
        try:
            pkg = json.load(open(pkg_path, encoding="utf-8"))
        except Exception as e:
            problems.append("package.json 解析失败: %s" % e)
            pkg = {}
        deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
        for dep in REQUIRED_DEPS + REQUIRED_DEVDEPS:
            if dep not in deps:
                problems.append("缺少依赖: %s" % dep)

    data_dir = os.path.join(root, "public", "data")
    for name, check in DATA_SHAPES.items():
        path = os.path.join(data_dir, name)
        if not os.path.isfile(path):
            continue
        try:
            data = json.load(open(path, encoding="utf-8"))
            if not check(data):
                problems.append("%s 数据结构与契约不符" % name)
        except Exception as e:
            problems.append("%s 解析失败: %s" % (name, e))

    if problems:
        print("[FAIL] 脚手架校验未通过")
        for p in problems:
            print("  -", p)
        sys.exit(1)
    print("[OK] 脚手架校验通过（%d 个必需文件 / %d 个数据文件）" % (len(REQUIRED_FILES), len(DATA_SHAPES)))
    sys.exit(0)


if __name__ == "__main__":
    main()
