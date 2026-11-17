---
name: 查询微信unionid关联的京东账号及基础信息
description: "根据微信unionid查询关联的支付PIN和登录PIN，并查询对应京东账号的基础信息；入参为：微信unionid"
---

# 查询微信unionid关联的京东账号及基础信息

## 适用场景
根据微信unionid查询关联的支付PIN和登录PIN，并查询对应京东账号的基础信息；入参为：微信unionid

## 输入参数
- unionid

## 执行流程
> Claude 请严格按以下步骤依次查询数据表并分析，注意每一步的依赖关系、输入与输出字段。

```
step1: 目标：根据微信unionid查询支付PIN和登录PIN
操作：从表{cdm_map_app_icc_connect_relation_da_new_nonsensitive}，输入{dst_val（unionid）,sub_type in(10501, 10502)}，输出{src_val（PIN）， index_json（样例数据）}
依赖：无
备注：10501：商城订单微信支付；10502：微信登录
step1: 目标：根据PIN查询用户基础信息
操作：从表{app_lb_acct_base_info}，输入{pin（京东账号）}，输出全部字段
依赖：step1.src_val
```

---
_来源思维链ID: 2029845474681409840 ｜ owner: 陈靓（bjchenliangyf） ｜ 创建时间: 2026-07-31 16:09:50 ｜ 最近更新: bjchenliangyf 2026-07-31 16:09:50_
