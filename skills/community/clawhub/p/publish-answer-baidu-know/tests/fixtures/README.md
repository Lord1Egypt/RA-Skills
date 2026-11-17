# fixtures（脱敏样例）

本目录存放 **golden case / contract test** 用的输入、期望输出与 **adapter profile 样例**。

## 规则

- 只能放**虚构、脱敏、可公开**的数据（演示租户、演示 request_id 等）。
- **禁止**：真实客户名、真实订单/提单号、真实报关单、真实 token/cookie、真实内网 URL、生产环境凭证。
- `adapter_profiles.sample.yaml` 中的 URL 须使用 `localhost`、`example.invalid` 等明显占位；`credential_ref` 仅表达「从密钥库引用」的约定，**不得**内嵌密钥。

## 与本仓库测试的对应关系

| 文件 | 用途 |
|------|------|
| `sample_request.json` | 通用请求体样例，供 ``tests/samples/test_golden_cases.py.sample`` 演示读取。 |
| `expected_response.json` | 与上配套的期望摘要字段（业务复制后按域替换）。 |
| `adapter_profiles.sample.yaml` | 五类运行方式（mock / simulator_api / simulator_rpa / real_api / real_rpa）的配置表达样例。 |

---

## 给 AI 工具的替换规则

- 可以按业务**重命名字段**、增减键名，但必须保持**虚构、脱敏**；不得把真实客户标识原样搬进仓库。
- 可以**新增**更多 fixture 文件，例如 `case_valid_001.json`、`case_missing_required_001.json`，并在测试中通过相对路径读取。
- **禁止**将真实企业数据、真实单证截图中的文字、真实报关要素未经处理直接复制进 `fixtures/`。
- 若用例来自真实客户样本，须先**脱敏、泛化、替换编号与地名**，再作为模板数据提交。

