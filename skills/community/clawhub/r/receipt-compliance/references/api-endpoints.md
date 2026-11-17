# API 端点说明

本文档列出各平台API的接入方式和注意事项。

---

## 一、查验平台 API

### 1.1 国税总局查验平台

- **网址**: https://inv-veri.chinatax.gov.cn/
- **接口类型**: HTTP表单提交（需要处理验证码）
- **是否免费**: ✓ 完全免费
- **接入难度**: ★★★（需要处理验证码和反爬机制）
- **建议**: 仅在用户明确授权下发起单条查验请求，控制频率

### 1.2 百望云 API

- **网址**: https://www.bairong.com
- **接口类型**: RESTful API
- **认证方式**: API Key + Secret
- **是否免费**: ✗ 按量付费或包年
- **接入难度**: ★★☆（企业资质申请偏难）

### 1.3 诺诺发票 API

- **网址**: https://www.nuonuo.com
- **接口类型**: RESTful API
- **认证方式**: API Key + Secret
- **是否免费**: ✗ 按量付费或包年
- **接入难度**: ★★☆（接口文档齐全）

---

## 二、审批平台 API

### 2.1 钉钉审批

- **网址**: https://open-dev.dingtalk.com
- **审批API**: 钉钉开放平台 → 审批 → 流程引擎
- **认证方式**: AppKey + AppSecret → OAuth2.0 Token
- **接入步骤**:
  1. 创建企业内部应用
  2. 开通审批权限
  3. 创建审批流程模板
  4. 获取流程编码

### 2.2 企业微信审批

- **网址**: https://developer.weixin.qq.com
- **审批API**: 企业微信 → 审批 → 模板管理
- **认证方式**: CorpID + Secret → AccessToken
- **接入步骤**:
  1. 注册企业微信管理后台
  2. 创建审批模板
  3. 获取模板ID和审批字段

### 2.3 飞书审批

- **网址**: https://open.feishu.cn
- **审批API**: 飞书开放平台 → 审批 → 审批实例
- **认证方式**: App ID + App Secret → Tenant Access Token
- **接入步骤**:
  1. 创建企业自建应用
  2. 开通审批权限
  3. 获取审批编码

---

## 三、API 调用示例

### 3.1 钉钉审批提交示例（伪代码）

```python
# 获取钉钉 AccessToken
def get_dingtalk_token(app_key, app_secret):
    url = "https://api.dingtalk.com/v1.0/oauth2/accessToken"
    payload = {"appKey": app_key, "appSecret": app_secret}
    # ...

# 提交审批
def submit_dingtalk_approval(token, process_code, formData):
    url = f"https://api.dingtalk.com/v1.0/approval/processInstances"
    # ...
```

### 3.2 企业微信审批提交示例（伪代码）

```python
# 获取企业微信 AccessToken
def get_wecom_token(corp_id, secret):
    url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corp_id}&corpsecret={secret}"
    # ...

# 提交审批
def submit_wecom_approval(token, template_id, apply_data):
    url = f"https://qyapi.weixin.qq.com/cgi-bin/approval/submit?access_token={token}"
    # ...
```

---

## 四、安全建议

1. **API密钥分散存储**：不同平台使用不同密钥，避免一损俱损
2. **调用频率限制**：建议每分钟不超过10次查验/审批请求
3. **错误重试机制**：失败时自动重试最多3次，指数退避
4. **日志审计**：记录所有API调用，便于追踪和审计

---

## 五、接口调用频率限制

| 平台 | 建议最低间隔 | 日调用上限建议 |
|------|-------------|---------------|
| 国税总局 | 无官方限制 | 建议 ≤ 1000次/日 |
| 百望云 | 按套餐而定 | 查看服务协议 |
| 诺诺发票 | 按套餐而定 | 查看服务协议 |
| 钉钉审批 | 无官方限制 | 建议 ≤ 1000次/日 |
| 企业微信审批 | 无官方限制 | 建议 ≤ 500次/日 |
| 飞书审批 | 无官方限制 | 建议 ≤ 1000次/日 |

> 以上限制仅供参考，请以各平台官方文档为准。