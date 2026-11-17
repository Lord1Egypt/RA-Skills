# API 测试（REST / GraphQL）

> 对 REST 与 GraphQL 接口做系统化测试：请求构造、参数校验、鉴权验证、响应断言。覆盖正常 / 边界 / 异常 / 安全四类矩阵。

## 何时使用

- 用户说「测试这个接口」「验证 API 鉴权」「对 GraphQL 做安全测试」「上线前检查端点」
- 需要为某个 REST/GraphQL 端点建立测试矩阵或冒烟测试

## 测试矩阵（四象限）

对每个端点，设计四类用例：

| 类别 | 目标 | 示例 |
|------|------|------|
| 正常 | 功能正确 | 合法参数 → 200 + 正确结构 |
| 边界 | 极限输入 | 空值、超长、最大值、特殊字符、类型错误 |
| 异常 | 错误处理 | 缺必填、格式错、资源不存在 → 4xx + 规范错误体 |
| 安全 | 越权/注入 | 无 token、过期 token、越权访问他人资源、注入 payload |

## REST 示例（httpie / curl）

```bash
# 正常
http POST :8080/api/login username=hope password=secret
# 异常：缺参
http POST :8080/api/login username=hope
# 安全：无 token
http GET :8080/api/orders
# 边界：超长
http POST :8080/api/comment text=$(python3 -c "print('A'*10000)")
```

## GraphQL 示例

```bash
http POST :8080/graphql query='{ user(id: 1) { id name } }'
# 深度限制 / 字段级权限
http POST :8080/graphql query='{ user(id: 1) { email ssn } }'   # 应被权限拦截
```

## 断言要点

- **状态码**：正常 2xx，校验错误 4xx，服务端 5xx 需排查。
- **响应体结构**：字段类型、必填字段、错误信息格式一致。
- **鉴权**：无 token → 401；越权 → 403；过期 → 401/重新签发。
- **CORS**：预检 OPTIONS 返回正确头。
- **响应时间**：记录 p95，超阈值告警（性能见 [references/performance-testing.md](performance-testing.md)）。

## 鉴权测试清单

- [ ] 无 Token → 401
- [ ] 过期 Token → 401
- [ ] 错误权限 Token 访问他人资源 → 403
- [ ] 篡改 Token 签名 → 拒绝
- [ ] 刷新 Token 流程正常

## 脚本加速

```bash
python3 scripts/test_matrix.py --method POST --path /api/login --params username,password
```

生成「正常/边界/异常/安全」四类 markdown 测试矩阵，可直接作为用例清单。

## 相关子技能（L3）

- 落地为 API 测试动作（REST/GraphQL 请求构造、参数与鉴权测试）→ [skills/api-testing/SKILL.md](../skills/api-testing/SKILL.md)

## 限制

- 不替代 Postman / Bruno / Supertest 等完整框架的编排能力。
- 不涉及复杂 OAuth 授权码流程与性能压测（见对应 references）。
- 安全深度测试见 [references/security-testing.md](security-testing.md)。
