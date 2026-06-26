---
name: juhe-telephone-verify
description: 核验手机号码、姓名、身份证号三要素是否匹配（运营商实名认证）。支持查询运营商、省份、城市信息。Use when user needs to verify Chinese phone number + name + ID card match (telecom real-name authentication).
metadata: { "openclaw": { "emoji": "📞", "requires": { "bins": ["python3"], "env": ["JUHE_TELEPHON_VERIFY_KEY"] }, "primaryEnv": "JUHE_TELEPHON_VERIFY_KEY" }}
---

# 手机号码三要素核验

核验手机号码、姓名、身份证号三要素是否匹配，返回核验结果及运营商信息。

## 配置

在 `~/.openclaw/openclaw.json` 的 `env.vars` 中配置：

```json
"JUHE_TELEPHONE_VERIFY_KEY": "你的 API Key"
```

**获取 API Key：** https://www.juhe.cn/ → 搜索"运营商三要素核验" → 个人中心 → 我的数据

## 使用

**直接调用：** 提供姓名、身份证号、手机号

> "核验张三的三要素，身份证 44030419900101001X，手机 13800000000"

**命令行：**
```bash
python3 scripts/telephone_verify.py --mobile "13800000000" --name "张三" --idcard "44030419900101001X"
```

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| mobile | 是 | 手机号码 |
| realname | 是 | 真实姓名 |
| idcard | 是 | 身份证号码 |

## 结果

| 结果码 | 说明 |
|--------|------|
| 1 | ✅ 三要素一致 |
| 2 | ❌ 三要素不一致 |
| 220803 | 查询无此记录 |
| 220807-220809 | 参数格式错误 |

**成功响应：**
```json
{
  "error_code": 0,
  "result": {
    "res": 1,
    "resmsg": "三要素身份验证一致",
    "type": "电信",
    "province": "江苏省",
    "city": "苏州市"
  }
}
```

## 注意

- 隐私信息敏感，使用后及时清理
- 仅用于合法合规场景
- 详见 [references/api.md](references/api.md) 完整文档
