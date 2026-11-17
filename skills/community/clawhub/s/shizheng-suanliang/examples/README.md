# examples — shizheng-suanliang

- `minimal.municipal.json`：合成最小市政识图契约（schema `cad-municipal-geometry/v1`），含 1 个雨水管道几何段（120 m）、2 座检查井、1 个雨水口、1 条 DN800 管径文本、红线宽 40m 标注、1 条道路中线段（80 m）。**纯合成数据，不含任何真实项目内容。**

跑一遍：

```bash
python3 scripts/municipal_qty.py --municipal examples/minimal.municipal.json \
    --allow-manual --out-prefix /tmp/municipal_example
```

期望输出（估算带，final_quantity=false）：

- 雨水管道延米：120.0 ~ 138.0 m
- 管径分档：DN≤800 ×1；无管径候选 ×1（进警告）
- 井类：检查井 ×2、雨水口 ×1（雨水系统）
- 道路面积带：3200 ~ 3680 m²（中线 80m × 宽 40m）
- 连通性提示：开放端点 2 个
