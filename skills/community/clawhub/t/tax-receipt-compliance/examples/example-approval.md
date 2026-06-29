# 示例3：对接企业审批系统

## 场景
企业已配置好想接入的审批平台（如钉钉/企业微信/飞书），并提供了API密钥和审批流程编码。

## 前置条件
企业需在 `config.yaml` 中配置审批平台信息：

### 钉钉配置示例
```yaml
approval:
  platform: "dingtalk"
  dingtalk:
    app_key: "dingkingxxxxxxxxxx"
    app_secret: "xxxxxxxxxxxxxxxxxxxxx"
    process_code: "PROC-XXXXXXXXXXX"
```

### 企业微信配置示例
```yaml
approval:
  platform: "wecom"
  wecom:
    corp_id: "wwxxxxxxxxxx"
    secret: "xxxxxxxxxxxxxxxxxxxxx"
    template_id: "CTL-XXXXXXXXXXX"
```

### 飞书配置示例
```yaml
approval:
  platform: "feishu"
  feishu:
    app_id: "cli_xxxxxxxxxx"
    app_secret: "xxxxxxxxxxxxxxxxxxxxx"
    approval_code: "OC-XXXXXXXXXXX"
```

## 输入
```
提交审批 D:\output\报销单_20260629.xlsx
```

## 处理步骤
1. `approval_abstract.py` 读取配置文件中的审批平台设置
2. 根据平台选择对应的审批引擎（钉钉/企业微信/飞书/自建）
3. 检查API密钥和配置是否完整
4. 如果配置完整，调用对应API提交审批
5. 返回审批提交结果

## 预期输出
```json
{
  "engine": "钉钉审批",
  "status": "framework_ready",
  "message": "企业需自行调用钉钉审批API实现提交逻辑",
  "params": {
    "app_key": "ding****",
    "process_code": "PROC-XXXXXXXXXXX",
    "expense_file": "D:\\output\\报销单_20260629.xlsx"
  },
  "reference_url": "https://open.duxiaoman.com/document",
  "submit_time": "2026-06-29T00:15:41+08:00"
}
```

> **注意**：审批引擎目前为接口框架，企业需自行实现具体的API调用逻辑。

## 未配置审批平台时
```json
{
  "engine": "手动提交",
  "status": "manual_required",
  "message": "审批系统未配置，请手动提交报销单",
  "file_path": "D:\\output\\报销单_20260629.xlsx",
  "submit_time": "2026-06-29T00:15:41+08:00"
}
```

## 命令
```bash
# 提交审批（需先配置审批平台）
python scripts/approval_abstract.py --config config.yaml --expense D:\output\报销单_20260629.xlsx
```

## 风险提示
- 审批提交后可能无法撤销，请确认报销单内容无误后再提交
- API密钥请妥善保管，泄露风险由企业自行承担
- Skill仅提供技术支持，不对审批结果承担责任

## 企业自行实现清单
企业需根据选择的审批平台，自行实现以下功能：

| 平台 | 需实现的内容 |
|------|-------------|
| 钉钉 | OAuth2.0鉴权 → 获取AccessToken → 调用审批提交API |
| 企业微信 | 获取Token → 构建审批数据 → 调用提交API |
| 飞书 | 获取TenantToken → 构建审批表单 → 调用提交API |
| 自建 | 按企业接口规范实现HTTP请求 |