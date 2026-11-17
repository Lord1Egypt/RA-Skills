# samples（业务测试样例，默认不执行）

本目录存放**可复制到根目录的业务测试范式**，面向「企业数字员工技能」中 **ERP、TMS、WMS、船司、报关、邮件、LLM、RPA** 等外联场景下的 **service / golden** 测法说明。

---

## 作用

- 这里的文件是 **`.py.sample`**：`python tests/run_tests.py` **不会**收集本目录（`run_tests.py` 只发现 `tests/` 根目录下的 `test_*.py`）。
- 人类或 AI 需要启用范式时：**复制**到 `tests/test_<名称>.py`（去掉 `.sample`），再按业务改 import、断言与 fixture 路径。
- **禁止**把真实联调、真实网络、真实 RPA 写进复制后的默认用例；此类内容应放在 `tests/integration/*.sample` 并配合环境变量开关。

---

## 两类样例文件

### 1. `test_service_contract.py.sample`

**适合：**

- 技能有清晰的 **service 层入口**，例如 `run(...)`、`handle(...)`、`execute(...)`。
- 需要验证：**成功路径**、**参数/校验错误**、**adapter 异常被转换为业务可读错误**。
- 需要用 **`FakeAdapter`**（见 `tests/adapter_test_utils.py`）或自建 **stub** 替代 ERP、TMS、WMS、船司、报关、LLM、RPA 等，**不**发真实 HTTP、**不**开真实浏览器。

### 2. `test_golden_cases.py.sample`

**适合：**

- **解析类**：邮件/单证/PDF/Excel 等结构化输出。
- **计算类**：费用、税费、分摊、账单字段。
- **校验类**：合规、字段一致性、状态机规则。

推荐配合根目录下的 **`tests/fixtures/sample_request.json`** 与 **`tests/fixtures/expected_response.json`**（复制技能后按域替换字段，保持脱敏）。

---

## 如何启用 service contract 样例

1. **复制文件**  
   `tests/samples/test_service_contract.py.sample`  
   → `tests/test_service_contract.py`（或 `tests/test_<domain>_service_contract.py`，须符合根目录 `test_*.py` 命名以便 `run_tests.py` 收集）。

2. **替换示例 import**  
   把注释中的示意：  
   `# from service.your_service import run`  
   改为真实模块，例如：  
   `from service.quote_service import run_quote`  
   （具体路径以技能代码为准。）

3. **注入假外部依赖**  
   - **不要**在默认用例里直接 `requests` 访问 ERP/TMS/WMS 等。  
   - **不要**打开真实网页或驱动真实 RPA。  
   - **不要**调用真实 LLM；可 stub 返回固定 JSON。  
   - 对 **timeout / unauthorized / invalid_response** 等分支，用 `FakeAdapter` 或自建 fake 模拟（与 `adapter_test_utils` 思路一致）。

4. **至少保留三类断言习惯**  
   - **成功路径**：返回 `success: true` 或与技能约定的成功结构。  
   - **参数错误**：缺必填字段时返回**结构化** error（字段/码），而非未捕获裸异常。  
   - **外部异常**：adapter 超时、鉴权失败、脏响应等被转换为**可读、可重试标识明确**的错误形态（按产品约定）。

5. **给 AI 的提示**  
   复制后全文搜索 `your_service`、`TODO`、`伪代码` 等占位符并替换；不要留下指向真实客户的示例数据。

---

## 如何启用 golden case 样例

1. **复制文件**  
   `tests/samples/test_golden_cases.py.sample`  
   → `tests/test_golden_cases.py`（或 `tests/test_<domain>_golden.py`）。

2. **按业务修改 fixtures**（仍须脱敏）  
   - `tests/fixtures/sample_request.json`：请求或输入快照。  
   - `tests/fixtures/expected_response.json`：期望摘要或关键字段。  
   可新增多组文件，如 `case_valid_001.json`，并在测试中显式读取路径。

3. **断言建议（避免脆弱用例）**  
   - 比较**关键字段**，避免对整段 JSON 做机械全文 diff。  
   - **忽略**时间戳、随机 id、`trace_id` 等非确定字段。  
   - 对列表：断言**长度**、**关键元素**、**排序规则**（若业务保证顺序）。  
   - 对金额/数量：断言 Decimal 字符串、或允许文档约定的小范围误差。

4. **与 service 的关系**  
   golden 用例仍应通过 **service 层**（或纯函数）得到输出，再与 fixture 对比，而不是从 CLI 字符串 scrape。

---

## 不应该写在 samples 复制件里的内容

以下若出现，应移到 **`tests/integration/*.sample`** 或 **`tests/desktop/*.sample`**，并加环境变量授权说明：

- 访问**真实** API 或内网服务。  
- 打开**真实** RPA 页面或生产门户。  
- 读取**真实**客户文件、生产数据库。  
- 在测试中写入**真实**数据根或共享盘。  
- 任何真实 **token / cookie / 密码** 字面量。  
- 耗时极长、强依赖宿主 UI 抖动、无法在 CI 稳定复现的用例（不要塞进默认 `tests/test_*.py`）。

---

## 推荐命名（复制到根目录后）

| 用途 | 示例文件名 |
|------|------------|
| Service 契约 | `tests/test_service_contract.py` |
| Golden / fixture 回归 | `tests/test_golden_cases.py` |
| 领域规则 | `tests/test_<domain>_rules.py` |
| 校验逻辑 | `tests/test_<domain>_validation.py` |

命名需满足：`tests/` 根目录下 `test_*.py`，以便 `python tests/run_tests.py` 默认发现。

更多分层说明见 **`tests/README.md`**（「我该把测试写在哪里？」与「新技能最小测试清单」）。
