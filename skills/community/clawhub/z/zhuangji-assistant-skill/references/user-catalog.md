# 用户硬件与报价 overlay

用户只和 Agent 对话。Agent 可从自然语言或图片提取事实，必要时查询品牌官网或向用户补问，再生成符合 `user-overlay.schema.json` 的 JSON。脚本不提问、不识图、不联网，也不扫描默认目录或环境变量。

先校验并规范化：

```bash
python -B scripts/import_user_catalog.py draft.json --validate-only --json
python -B scripts/import_user_catalog.py draft.json --output ./user-catalog.json --json
```

查询和检查必须显式传入同一 overlay；可重复传入，后传报价优先：

```bash
python -B scripts/query_components.py --category gpu --id BASE_ID --overlay ./user-catalog.json --currency USD --json
python -B scripts/check_compatibility.py --strict --require-complete --overlay ./user-catalog.json ...
```

- `quote_patches` 只更新价格、日期和备注，精确 `target_id` 继承基础库全部规格；不能用模糊型号继承。
- `components` 新 ID 必须以 `user-<category>-` 开头。`base_component_id` 只允许原始品牌/完整型号经归一后可证明为完全相同 SKU 时继承；显式 `brand_en` / `model_en` 是附加否决条件，不能单独覆盖冲突或缩写过度的原始身份。品牌或完整型号不同会以 `base_identity_conflict` 拒绝。已有基础条目的本地报价应使用 `quote_patches`，用户称呼用 `aliases`，不要克隆成另一型号。显式规格与基础事实冲突时同样拒绝。
- 基础库同一完整 GPU 型号若带 `spec_conflicts`，说明渠道记录的关键规格互相矛盾。报价补丁和别名只改价格/称呼，不能让冲突消失；Agent 必须按精确 SKU 官网或用户明确证据核实后，以同型号 `base_component_id` 副本显式补入对应字段。只清除已核实字段，其余冲突仍保持待复核。
- 完整性在继承和确定性字段推断之后计算：例如同 SKU 基础规格或明确型号中的 `1TB` 可以补出 SSD 容量；用户显式规格若与这种确定性推断冲突会被拒绝，不会静默改写。推断不能补造散热扣具或显卡供电接口；自定义散热器必须提供或继承 `socket_support`，显式不支持 CPU socket 会判为不兼容。可同时提供 `air_cooler_layout`（`low_profile` / `down_draft` / `single_tower` / `dual_tower`）、`heatpipe_count` 或水冷 `radiator_mm`；这些结构证据缺失时，高负载 CPU 的严格检查会标为待复核。新显卡必须提供或继承规范接口值（如 `8pin`、`2x8pin`、`16pin`、`12VHPWR`、`12V-2x6`）；只有明确需要 16pin 时，`requires_16pin_psu: true` 才能单独作为供电证据，`false` 必须同时有规范接口事实。识图/文字只能确认“未知、待核实”时应省略这些字段，让严格检查标为待复核，不能把“未知”写成接口值或猜成 `false`。
- 主板视频输出只写规范值 `HDMI`、`DisplayPort`、`VGA`、`DVI`、`USB-C`、`Thunderbolt`；`unknown`、`待确认` 或接口版本/数量描述应先由 Agent 归一或省略，不能借非空字符串绕过无独显完整度门禁。
- 主板 PCIe 扩展槽必须把 `mechanical` 与 `electrical` 分开，按 `slot_id` 写入 `pcie_slot_layout`；M.2 存储槽单独写入 `m2_slot_layout`，记录 `interfaces`、`pcie_generation`、`lanes` 和 `source`，支持 M.2 SATA 的槽才在 `interfaces` 中同时写 `sata`。两种槽位不能混用；未知代际、来源或通道数时省略整项，不用芯片组默认值补齐。USB4/雷电需同时填写状态和已核实后置端口数；`thunderbolt_status: header_only` 只表示扩展针脚，不能填写后置端口。共享和禁用条件保留为字符串列表，供 Agent 在报告中明确复核。
- `aliases` 只做精确别名到稳定 ID 的映射；零匹配是未找到，多匹配是歧义错误。
- 用户价状态固定为 `user_quote`。通过 `base_component_id` 克隆同 SKU 时，基础 CNY 金额、状态和日期仍作为完整基准报价保留；外币用户价保存在独立字段并成为该币种的活动报价。不同币种不换算，不把基准 CNY 与外币新价、预算或排序串用，查询时显式使用 `--currency`。
- `brand_en` / `model_en` 可由用户明确提供。内置别名仅覆盖已确认的官方英文品牌/系列；不机翻营销昵称。
- overlay 是用户本地文件，不进入 Skill、Git 仓库或发布包。
