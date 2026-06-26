"""单独跑面试卡（脱离 main.py，防止和 rewrite 串行超时）"""
import os, sys, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, ".")
from pathlib import Path
from lib.parser import parse_resume
from lib.jd_fetcher import fetch_jd
from lib.interview import generate_interview_cards

resume = parse_resume(Path("examples/chenhongzhu.pdf"))
jd = fetch_jd("【字节跳动】大数据开发工程师 / 高级 - 要求：3+ 年大数据开发经验；精通 Hive/Spark/SQL；熟悉 Kafka/Flink 实时计算；有数据仓库建模（Kimball/Inmon）经验；熟悉 DolphinScheduler。加分：Doris/ClickHouse、数据治理、LLM+数据。本科及以上。")

md = generate_interview_cards(resume, jd, n=10)
out = Path("output/chen-demo/interview-cards.md")
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(md, encoding="utf-8")
print(f"✅ 已生成: {out} ({len(md)} chars)")
