#!/bin/bash
# 查询瑜伽体式知识库 (CUC瑜伽精品课)
# 返回 NocoDB 中所有瑜伽体式数据

XC_TOKEN="${NOCODB_XC_TOKEN:-cCCOb9nNdeWSFIWr7tg7rWfOZeKyTfJ0Qtis_bm3}"
BASE_URL="https://nocodb.dixchain.com/api/v2"
TABLE_ID="m7myxl3aw1300o3"
VIEW_ID="vw1q0o7tyka9o9oz"

url="${BASE_URL}/tables/${TABLE_ID}/records?offset=0&limit=100&viewId=${VIEW_ID}"
curl -s "${url}" -H "xc-token: ${XC_TOKEN}"
