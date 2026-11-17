# bus 契约接线（shizheng-suanliang）

## 链路

```
cad-file-reader（municipal-geometry 识图包）
    └─ 产物 *.municipal.json，schema cad-municipal-geometry/v1
        └─ lis-skill-bus（push/pull，sections: components, pipe_network, systems,
                        labels, municipal_geometry, materials, references；
                        core: pipe_network, components）
            └─ shizheng-suanliang --from-contract <contract_id>
```

## push（识图侧 → bus）

```bash
bash scripts/shizheng_statesync.sh push --entry-file 市政识图/xxx.municipal.json \
    --project 项目 --specialty 市政 --skill shizheng
```

缺 bus 时退出码 2，不降级本地。

## pull（算量侧正式入口）

```bash
python3 scripts/municipal_qty.py --from-contract <contract_id> --project 项目 --out-prefix 市政算量
```

- bus entry 若已是 `cad-contract/v1` 外壳则原样校验；若是裸 `cad-municipal-geometry/v1` 载荷，自动套最小外壳再验（与钢结构同法）。
- `mode != formal` 一律拒绝（exit 3），不静默降级。
- bus 文档无法保留原始字节，校验跳过内嵌哈希绊线（`require_hash=False`），与共享 guard 行为一致。

## 手工/文件降级

```bash
python3 scripts/municipal_qty.py --municipal xxx.municipal.json --allow-manual --out-prefix 市政算量
```

- 必须显式 `--allow-manual`，缺了 exit 3。
- 结果 `provenance=manual`、`final_quantity=false`、`formal_ledger_eligible=false`。
- 直接给 DWG/DXF/DWT 一律 exit 23。
