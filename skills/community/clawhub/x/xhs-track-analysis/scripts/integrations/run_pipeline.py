# -*- coding: utf-8 -*-
"""
scripts/integrations/run_pipeline.py
A 方案编排：按 config 选择数据源（mock/pgy/juguang/thirdparty），
对「关键词 × 排序」摘取并归一化为与采集器(B)同构的 CSV/MD，供 xhs-track-analysis Skill 消费。

用法:
  cd scripts/integrations
  python3 run_pipeline.py config.example.json
  python3 run_pipeline.py --help

退出码: 0 = 成功; 2 = 用法/配置错误。
"""
import sys
import json
import os

import source_base
from normalizer import save
from mock import MockAdapter
from pgy import PgyAdapter
from juguang import JuguangAdapter
from thirdparty import ThirdPartyAdapter

ADAPTERS = {
    "mock": MockAdapter,
    "pgy": PgyAdapter,
    "juguang": JuguangAdapter,
    "thirdparty": ThirdPartyAdapter,
}

DEFAULT_SORTS = ["综合", "最新", "最多点赞", "最多收藏", "最多评论"]

USAGE = """用法:
  python3 run_pipeline.py <config.json>
  python3 run_pipeline.py --help

示例:
  python3 run_pipeline.py config.example.json   # source=mock 无需凭证即可跑通演示
  python3 run_pipeline.py config.json           # source=pgy/juguang/thirdparty 需在 config 填凭证

说明:
  config.json 必填字段: keywords（非空字符串列表）
  可选字段: source(mock/pgy/juguang/thirdparty，默认 mock)、sorts、limit_per_query、output_dir。"""


def die(msg):
    print(f"错误: {msg}", file=sys.stderr)
    print("提示: 运行 python3 run_pipeline.py --help 查看用法。", file=sys.stderr)
    sys.exit(2)


def load_config(path):
    if not os.path.exists(path):
        die(f"找不到配置文件: {path}")
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        die(f"配置文件不是合法 JSON（第 {e.lineno} 行附近）: {e.msg}")
    except OSError as e:
        die(f"读取配置文件失败: {e}")


def validate_config(cfg):
    source = cfg.get("source", "mock")
    if source not in ADAPTERS:
        die(f"未知 source: {source}。可选: {', '.join(ADAPTERS)}")

    keywords = cfg.get("keywords", [])
    if not isinstance(keywords, list) or not keywords:
        die("配置缺少 keywords：请填写要研究的关键词列表（非空字符串数组）。")
    if not all(isinstance(k, str) and k.strip() for k in keywords):
        die("keywords 中存在空字符串或非字符串项，请检查配置。")

    sorts = cfg.get("sorts", DEFAULT_SORTS)
    if not isinstance(sorts, list) or not sorts:
        die("配置 sorts 为空：请至少保留一种排序角度（如「最新」）。")
    if not all(isinstance(s, str) and s.strip() for s in sorts):
        die("sorts 中存在空字符串或非字符串项，请检查配置。")

    try:
        limit = int(cfg.get("limit_per_query", 20))
    except (TypeError, ValueError):
        die("limit_per_query 必须为数字。")
    if limit <= 0:
        die("limit_per_query 必须为正整数。")

    out_dir = cfg.get("output_dir", "output")
    if not isinstance(out_dir, str) or not out_dir.strip():
        die("output_dir 不能为空。")

    return source, [k.strip() for k in keywords], sorts, limit, out_dir.strip()


def build_adapter(name, config):
    return ADAPTERS[name](config)


def main():
    args = sys.argv[1:]
    if args and args[0] in ("--help", "-h"):
        print(USAGE)
        sys.exit(0)
    if not args:
        die("缺少 config.json 参数。用法: python3 run_pipeline.py <config.json>")

    cfg = load_config(args[0])
    source, keywords, sorts, limit, out_dir = validate_config(cfg)

    print(f"[A方案] 数据源={source}")
    adapter = build_adapter(source, cfg)
    try:
        adapter.authenticate()
    except Exception as e:
        die(f"数据源鉴权失败（{source}）: {e}. 请检查 config 中的凭证，或改用 source=mock 演示。")

    all_records = []
    for kw in keywords:
        for s in sorts:
            try:
                recs = adapter.search_notes(kw, s, limit)
                all_records.extend(recs)
                print(f"  [{source}] {kw}/{s} → {len(recs)} 条")
            except NotImplementedError as e:
                print(f"  [骨架] {kw}/{s} 未实现：{e}")
            except Exception as e:
                print(f"  [错误] {kw}/{s}：{e}")

    if not all_records:
        print("[A方案] 无数据（骨架未实现或配置缺凭证）。可用 source=mock 跑通演示。")
        return

    csv_path, md_path = save(all_records, out_dir)
    print(f"[输出] {csv_path}\n[输出] {md_path}")


if __name__ == "__main__":
    main()
