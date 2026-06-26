# purchase_record - 采购记录管理技能

自动将采购信息写入 Excel 表格的采购记录管理工具。

## 功能说明

当您输入 `采购 日期 物品名称 价格` 格式的命令时，会自动：
1. 解析日期（如 0312 = 3 月 12 日）
2. 提取物品名称和价格数字
3. 将数据追加到 Excel 表格的第一非空白行

## 使用示例

```
采购 0312 螺丝 3 元
采购 0317 小锂 3125 手电钻 290 元
采购 0401 USB 数据线 15.5
```

## 技能配置

- **名称**: purchase_record
- **版本**: 1.0.0
- **主要功能**: scripts/index.js
- **Excel 路径**: C:\Users\Administrator.rjazz-2022BWPUD\Desktop\purchase_record.xlsx