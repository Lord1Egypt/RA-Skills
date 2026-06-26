# 邮储银行财资管理系统接口技能

> 中国邮政储蓄银行财资管理系统统一前置平台接口完整实现

## 📦 文件结构

```
psbc-treasury-api/
├── SKILL.md                 # 技能主文档（接口清单、规范说明）
├── apis.json                # 20 个接口的完整定义和 JSON Schema
├── response-codes.json      # 响应码字典（标准码 + 业务码 + 附录代码表）
├── validator.py             # 报文验证工具
├── mock.py                  # Mock 响应生成器
├── examples/                # 示例代码
│   ├── 601118-curl-example.sh    # curl 示例
│   └── psbc_client.py            # Python 客户端示例
└── README.md                # 本文件
```

## 🚀 快速开始

### 1. 查看接口列表

```bash
cat SKILL.md | grep -A 30 "接口清单"
```

### 2. 验证报文

```bash
# 交互式验证
python3 validator.py --interactive

# 或编程方式
from validator import PSBCValidator

validator = PSBCValidator()
errors = validator.validate("601118", {
    "txCode": "100016",
    "tenantID": "eam_tenant_a_0001",
    "sendTime": "20250318163811",
    "srcSysId": "140001",
    "bankAccno": "951011013000006323"
})
print(errors)  # [] 表示验证通过
```

### 3. 生成 Mock 响应

```bash
# 交互式 Mock
python3 mock.py --interactive

# 或编程方式
from mock import PSBCMockServer

mock = PSBCMockServer()
response = mock.mock_request("601118", request_data)
```

### 4. 调用接口（Python）

```python
from examples.psbc_client import PSBCTreasuryClient

client = PSBCTreasuryClient(env="test")

# 余额查询
business_data = {
    "txCode": "100016",
    "tenantID": "eam_tenant_a_0001",
    "sendTime": "20250318163811",
    "srcSysId": "140001",
    "bankAccno": "951011013000006323"
}

request_data = client.build_request("601118", business_data)
# 发送请求前需实现国密算法
```

## 📋 接口列表

| 交易码 | 接口名称 | 安全级别 |
|--------|----------|----------|
| 601113 | 查询租户下直连账户列表 | 10 |
| 601114 | 批量工资代发 | 10 |
| 601115 | 批量工资代发结果查询 | 10 |
| 601116 | 生成单笔支付申请单或支付单 | 10 |
| 601117 | 单笔支付申请单或者支付单结果查询 | 10 |
| 601118 | 账户余额实时查询 | 10 |
| 601119 | 查询明细 | 10 |
| 601120 | 账户历史余额查询 | 10 |
| 601203 | 明细关联回单信息查询 | 15 |
| 601303 | 查询资金归集明细 | 10 |
| 601304 | 手工下拨 | 10 |
| 601311 | 融资中心付款单获取 | 10 |
| 601324 | 新增申请单 | 10 |
| 601325 | 申请单结果查询 | 10 |
| 601383 | 获取免密登录令牌 | 10 |
| 601417 | 资金计划科目同步 | 10 |
| 601418 | 资金计划填报 | 10 |
| 601419 | 资金计划追加 | 10 |
| 601420 | 资金计划占用情况查询 | 10 |
| 601732 | 手工下拨结果查询 | 10 |

## 🔐 安全说明

### 安全级别 10
- SM4 对称加密业务报文
- SM2 非对称加密 SM4 密钥
- SM2 签名/验签

### 安全级别 15
- 仅 SM2 签名/验签
- 业务报文平铺传输

### 国密算法集成
需要集成国密库（如 `gmssl` 或 `pysm2`）才能实现实际加解密：

```bash
pip install gmssl
```

## 🌐 环境地址

| 环境 | 地址 |
|------|------|

## 📝 常见错误码

| 代码 | 说明 | 处理建议 |
|------|------|----------|
| 000000 | 操作成功 | - |
| 020300 | 对方账号不合法 | 核实收款账号 |
| 020302 | 查询无记录 | 确认数据存在性 |
| 999990 | 非法参数异常 | 检查报文格式 |

## 📚 相关文档

- 《财资管理系统 - 统一前置平台接口规范 - 行外版-v1.2.5》
- 《统一前置平台安全认证开发指引-v1.0.6》

## ⚠️ 注意事项

1. 系统跟踪号必须全局唯一
2. 签名顺序不能改变
3. 金额字段保留 2 位小数
4. 日期格式严格按规范
5. 分页 pageSize 支持 1-100

## 📄 版本信息

- 接口规范版本：v1.2.5
- 更新日期：2026-03-04
- 技能版本：1.0.0
