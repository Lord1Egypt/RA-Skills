---
name: wms-reconciliation
description: "第三方仓库收费对账技能。用于将仓库方提供的Excel收费清单与WMS（仓库管理系统）OpenAPI中的实际业务记录逐笔核对，验证每笔收费是否真实发生、业务是否实际完成。已适配TopWMS（极欧云仓）系统，其他WMS系统可扩展适配。触发词：仓库对账、核账、WMS对账、收费核对、仓租费核对、出库费核对、包装费核对、退件费核对。当用户需要核对仓库收费清单与WMS系统数据是否一致时使用此技能。"
agent_created: true
---

> **免责声明**：本技能为第三方独立开发工具，与 TopWMS、极欧云仓及其所属公司无任何隶属、背书或合作关系。"TopWMS" 等系统名称为其各自所有者的商标或商号，本文仅作兼容性描述使用。用户的 AppKey/AppSecret 仅在本机使用，不存储、不上传。

# WMS 仓库收费对账技能

## 概述

将仓库方提供的Excel收费清单与WMS OpenAPI中的实际业务记录逐笔核对，验证：
1. 每笔收费对应的业务是否真实存在
2. 该笔业务是否事实上完成了（如出库单是否真正出库、退货是否真正入库）
3. 收费金额是否与WMS系统记录一致

> 当前已适配：TopWMS（极欧云仓）OpenAPI。其他WMS系统的接口适配方式类似（业务单据查询 + 状态/金额字段比对），可按需扩展。

## 适用场景

- 跨境电商第三方仓库月度/季度收费对账
- 质疑仓库收费合理性，需要逐笔验证
- Excel收费清单包含：出库费、包装费、退件处理费、仓租费、销毁费等

## 对账方法

### 1. 出库费核对（以运单号为准）

以Excel中的**运单号**匹配WMS出库单的`logisticsNo`字段，逐笔检查以下5项：
- ① `stage == has_out_storage`（订单状态为已出库）
- ② `gmtOutStorage` 不为空（有出库时间）
- ③ `waybillOssUrl` 不为空（有面单，证明运单已生成）
- ④ `holdUpStatus == 0`（无拦截）
- ⑤ `closedReason` 为空（未关闭）

任一项不通过则标记为异常。

### 2. 退件处理费核对（以业务单号为准，验证入库）

以Excel中的**业务单号**（RMA单号）匹配WMS退货单的`returnSn`字段，检查：
- ① `tab == finished`（退货流程已完成）
- ② `gmtSign` 不为空（已签收）
- ③ `goodsSkuList` 中 `inStorageQuantity > 0`（已实际入库，库存增加）

### 3. 包装费核对（以WMS数据为准）

逻辑同出库费验证业务真实性，**金额以WMS系统`packagingCost`字段为准**：
- 用运单号或业务单号匹配WMS出库单
- 对比Excel收费金额与WMS `packagingCost`
- 不一致的笔目标红并列出差异

### 4. 仓租费核对（可选，复杂度高）

仓租费按SKU和日期逐笔记录，涉及库龄计算。如需核对，用`/goods_sku_warehouse/search_page`或`/goods/search_goods_sku_page`验证SKU存在性。默认跳过。

### 5. 销毁费核对

手工收费，检查关联单号在WMS中是否存在（通常关联出库单的`platformOrderSn`）。

## 使用流程

### Step 1: 收集对账参数

向用户确认以下信息：
- **Excel收费清单路径**（必填）
- **WMS API地址**（默认 `https://jou.topwms.com/api/open/erp`，由仓库方提供）
- **AppKey** 和 **AppSecret**
- **仓库ID**（warehouseId，由仓库方提供）
- **账期范围**（从Excel账单明细Sheet自动读取，或手动指定）
- **需要核对哪些费用项**（默认全部，仓租费可选跳过）

### Step 2: 执行对账脚本

运行 `scripts/reconcile.py`，传入参数：

```bash
python scripts/reconcile.py \
  --excel "C:/path/to/收费清单.xlsx" \
  --base-url "https://jou.topwms.com/api/open/erp" \
  --app-key "xxx" \
  --app-secret "xxx" \
  --warehouse-id "<仓库ID>" \
  --date-from "2026-06-01 00:00:00" \
  --date-to "2026-08-17 23:59:59" \
  --skip-rent  # 跳过仓租费
  --mark-excel  # 标红Excel异常
```

脚本会自动完成：
1. 读取Excel各Sheet收费明细
2. 通过API分页获取WMS出库单、退货单数据
3. 逐笔核对（出库费→运单号匹配+5项状态检查，退件费→业务单号匹配+入库验证，包装费→WMS金额为准对比）
4. 生成HTML对账报告 + JSON详细数据
5. （可选）标红Excel异常行并增加异常说明列

### Step 3: 汇报结果

向用户汇报：
- 各费用项核对通过率
- 异常笔明细（业务单号、运单号、问题描述）
- 金额差异汇总（Excel总计 vs WMS总计）

## Excel收费清单预期结构

| Sheet名 | 内容 | 关键列 |
|---------|------|--------|
| 账单明细 | 汇总信息 | 账单编号、账单金额、各费用项金额、账期 |
| 出库费明细 | 每笔出库订单收费 | 业务时间、消费金额、业务单号、运单号 |
| 退件处理费明细 | 退货处理收费 | 业务时间、消费金额、业务单号(RMA号)、运单号 |
| 包装费明细 | 包材费 | 业务时间、消费金额、业务单号、运单号 |
| 仓租费明细 | 按SKU按日仓租 | 业务时间、流水号、商品SKU、入库批次 |
| 销毁费明细 | 销毁收费 | 业务时间、消费金额、补收销毁费单号 |

## WMS API要点

详见 `references/wms_api_reference.md`。关键点：
- 签名：`Signature = MD5(MD5(jsonBody) + appSecret)`
- `requestTimestamp` 必须为**秒级整数时间戳**（非毫秒、非字符串）
- `source` 为可选参数，不传即可
- 使用游标分页（cursor-based pagination）
- OpenAPI无财务明细端点，只能通过业务单据间接验证

## 资源文件

### scripts/reconcile.py
完整对账脚本，支持命令行参数。功能：
- API连接与数据获取（出库单、退货单分页获取）
- Excel读取（openpyxl）
- 逐笔核对逻辑（出库费/退件费/包装费/销毁费）
- HTML报告生成
- JSON详细数据保存
- Excel标红与异常说明列（`--mark-excel`参数）

### references/wms_api_reference.md
WMS OpenAPI接口参考文档（基于实际接口调用测试自行整理），包含：
- 签名方法与请求格式
- 各端点URI与参数说明
- 关键返回字段说明
- 分页机制说明
- 已知限制与注意事项

### NOTICE.md
法律免责声明：商标归属、API文档来源、数据安全与使用责任说明。发布与分发时须保留此文件。
