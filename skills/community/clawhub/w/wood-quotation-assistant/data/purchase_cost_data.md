# 采购数据配置说明

## 配置位置

修改 `scripts/calculate_cost.py` 中的以下变量：

### MATERIAL_PRICES（材料价格）

```python
MATERIAL_PRICES = {
    "板材(18mm)": {"1-49张": 200, "50-99张": 180, "100张以上": 160},
    "颗粒板(18mm)": {"1-99张": 80, "100-199张": 75, "200张以上": 70},
}
```

### LOSS_RATES（损耗率）

```python
LOSS_RATES = {
    "板材": 0.05,
    "颗粒板": 0.03,
}
```

### PROCESS_PRICES（工艺单价）

```python
PROCESS_PRICES = {
    "切割": 5,
    "封边": 3,
    "喷漆": 25,
}
```

### PROFIT_MARGIN（利润率）

```python
PROFIT_MARGIN = 1.30  # 30% 利润率
```

## 阶梯价格说明

格式：`{"区间": 单价}`

示例：
- `"1-49张": 200` — 1到49张，单价200元
- `"50-99张": 180` — 50到99张，单价180元
- `"100张以上": 160` — 100张及以上，单价160元

## 更新步骤

1. 打开 `scripts/calculate_cost.py`
2. 修改对应变量
3. 保存文件
4. 重启 QClaw
