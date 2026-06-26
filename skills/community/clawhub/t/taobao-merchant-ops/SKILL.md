---
name: taobao-merchant-ops
description: 淘宝商家运营自动化客户使用说明。包含功能介绍、安装步骤、卡密激活方式、运行方法和购买信息。
---

# Taobao Merchant Ops 客户使用说明

**版本：1.0.7**

淘宝商家运营自动化客户运行包。

主要功能：
- 数据板块：查看昨日核心数据、推广数据、竞店竞品对比、异常指标记录
- 巡店与基础检查：检查前台页面、评价问大家、后台提醒、客服对话、发货时效

## 购买卡密

- 日卡 9.9元：https://www.zhufaka.cn/item/tgcsid
- 月卡 399元：https://www.zhufaka.cn/item/i6wfue
- 年卡 3500元：https://www.zhufaka.cn/item/x8ancz
- 定制/联系：微信 CChenJ_

## 安装依赖

在项目目录下运行：

```bash
cd scripts
python install.py
```

## 激活卡密

首次运行需要激活卡密，可直接运行：

```bash
python scripts/run_taobao_merchant_ops.py --card-key "你的卡密"
```

如果不带 `--card-key`，程序会在首次运行时提示手动输入卡密。

## 开始运行

```bash
python scripts/run_taobao_merchant_ops.py
```

## 常用运行方式

```bash
# 只跑数据抓取
python scripts/run_taobao_merchant_ops.py --skip-inspection

# 只跑巡检
python scripts/run_taobao_merchant_ops.py --skip-capture --skip-parse
```

## 常用检查命令

```bash
# 查看机器码
python scripts/run_taobao_merchant_ops.py --show-machine-id

# 查看授权状态
python scripts/run_taobao_merchant_ops.py --license-status

# 运行环境自检
python scripts/run_taobao_merchant_ops.py --doctor
```

## 注意事项

- 卡密与机器指纹绑定，换电脑通常需要重新激活
- 首次运行前请先安装依赖和 Playwright 浏览器
- 本工具结果仅供运营参考
