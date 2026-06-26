#!/usr/bin/env python3
"""Disabled: do not generate or save Alipay private keys locally.

The smyx_payment flow must obtain the Alipay privateKey from the cloud
create_order response and keep it in memory only for the current payment
operation. Persisting keys to disk is forbidden.
"""

raise SystemExit(
    "已禁用：支付宝私钥不能生成或保存到本地；请使用 create_order 返回的 privateKey 仅在内存中完成 H5 支付签名。"
)
