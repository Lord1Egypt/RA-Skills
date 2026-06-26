# tob-poc-war-room

ToB POC 战情室。用于根据 POC 目标、通过率、问题级别、客户沉默和采购路径信号，输出健康度评估、48 小时排兵布阵、客户沟通动作和 closing 触发判断。

## Quick Start

```bash
node src/generator.js \
  --industry "零售" \
  --objective "客服知识库 POC 通过率 >=90%" \
  --day 8 \
  --pass-rate 93 \
  --silence-days 7 \
  --problems "一个 SSO 问题 60h 未关闭，客户 champion 认可结果"

npm test
```

## Boundary

本 Skill 判断 POC 是否 closeable，但不把 closeable 等同于 contract-ready。合同推进需交给 `poc-to-contract-closer` 检查采购路径、closing 窗口和冷却阈值。
