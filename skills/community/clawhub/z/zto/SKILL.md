---
name: zto
description: Use ZTO Express (中通快递) for shipment tracking, shipping guidance, service-type comparison, outlet lookup, and delivery-time or fee estimation.
version: 1.0.0
tags: logistics, shipping, china, tracking, express, zhongtong
---

# ZTO (中通快递)

## Overview

Use this skill to help users with common ZTO Express tasks such as tracking shipments, understanding service levels, estimating timing or fees, and preparing to send a parcel.

## Usage Scenarios

### Scenario 1: Track an existing ZTO shipment
**User input:** "帮我查一下中通快递单号 773012345678901"
**Expected output:** Retrieve tracking status for the given waybill number, showing the latest checkpoint (e.g., "包裹已到达上海分拣中心"), origin and destination, estimated delivery time, and any exception notes. If the tracking number format is invalid, ask the user to recheck.

### Scenario 2: Estimate ZTO shipping fee for a parcel
**User input:** "从广州寄到北京，一个3公斤的普通包裹，中通多少钱？"
**Expected output:** Provide a fee estimate based on weight and route; explain standard ZTO pricing factors (starting price per kg, incremental weight charges, rural vs urban surcharges). If exact pricing data is unavailable, provide a cautious range and state assumptions.

### Scenario 3: Find a nearby ZTO outlet
**User input:** "附近有没有中通网点，我想寄个快递"
**Expected output:** Guide the user to check the ZTO official app or mini-program for outlet locations, or provide general tips on searching by city/district. If the user provides a city name, suggest typical outlet density and how to locate the nearest drop-off point.
### Scenario 4: 寄件遇到问题找客服前先查物流
**User input:** "我在淘宝买的东西用中通发的，好几天没更新物流了，帮我看看是不是丢了？"
**Expected output:** 读取运单号的完整物流轨迹，判断是否出现'超过48小时未更新'等异常状态，分析可能的原因（如转站未扫描、节假日延迟等），提供针对性的下一步建议：联系卖家催件、打中通客服热线95311投诉、或在菜鸟App发起物流查询。

## Local Persistence

When the local CLI/runtime code is used, this skill may create and persist local data under:

- `~/.openclaw/data/zto/zto.db`
  - stores query history
  - stores shipment-subscription records
  - may store saved address records if those commands are implemented/used
- `~/.openclaw/data/zto/secure/`
  - stores encrypted local files used by the privacy/storage helper
- `~/.openclaw/data/zto/secure/.key`
  - stores a local encryption key file with mode `600`
- `~/.openclaw/data/zto/privacy_export.json`
  - may be created when the user runs privacy export

Only use persistence when it is necessary for the user's requested workflow. If the user asks about privacy, disclose these paths clearly.

## Privacy Controls

The local CLI supports privacy operations:

- `privacy info` — show local storage paths and stored-file info
- `privacy clear` — clear local SQLite history/subscription data and encrypted local files
- `privacy export` — export local storage metadata to `privacy_export.json`

## Workflow

1. Determine the user's goal:
   - track an existing shipment
   - estimate fee or delivery time
   - compare service types
   - find a nearby outlet or pickup point
   - prepare shipment details
   - review or clear local history/subscriptions/privacy data
2. Ask for only the missing essentials, such as tracking number, route, package size, or urgency.
3. Give the most practical answer first.
4. If exact fee or timing cannot be confirmed, provide a cautious estimate and state assumptions.
5. If the task uses local runtime features that persist data, mention that local history/subscription/privacy files may be created under `~/.openclaw/data/zto/`.
6. Do not claim to complete real shipping actions unless live tools are available and confirmed.
