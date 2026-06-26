# skill-feishu - 飞书相关技能

这个技能包用于处理飞书相关操作，**收集飞书 API 到 open-apis/ 目录**。

## API 文档格式

API 文档严格遵循 `open-apis/TEMPLATE.md` 模板格式，示例参考 `open-apis/contact-v3-users-find_by_department.md`。

## 重要规则（必读）

### 🚫 严格禁止的操作

以下操作在任何情况下都**绝对禁止**，否则视为严重 BUG 和错误：

| 禁止操作 | 说明 |
|---------|------|
| **简化内容** | 任何文档、API 说明、字段描述、权限要求等**必须完整版**，禁止省略、缩写、合并 |
| **数据推算** | 禁止根据已有数据推算出不存在的信息，必须**真实记录**，没有就写"无此信息" |
| **省略示例** | 请求示例、响应示例、错误码示例等**必须完整**，禁止省略部分行 |
| **偷懒操作** | 不得跳过必填字段说明、参数说明等文档内容 |
| **模糊处理** | 所有字段说明、权限要求、参数说明必须清晰完整，不可模糊 |

### 违反规则的严重性

违反上述任何一条规则，均视为：
- ❌ **严重 BUG**
- ❌ **错误**
- ❌ **过错**
- ❌ **偷懒**
- ❌ **失误**

这些操作在任何情况下都不允许发生。

## 使用说明

### 目录结构

- **open-apis/** - 飞书 API 文档集合
  - README.md
  - TEMPLATE.md
  - auth-v3-tenant_access_token-internal.md - 自建应用获取 tenant_access_token
  - authen-v1-user_info.md - 获取用户信息
  - contact-v3-*.md - 通讯录 v3 API（用户、部门）
  - im-v1-*.md - 消息 API
  - passport-v1-sessions-query.md - 获取用户登录信息

## App 配置

⚠️ **安全提示**：应用凭证应存储在环境变量或配置文件中，不要硬编码在代码中。

## 权限链接规范

⚠️ **重要**：所有 API 文档中涉及权限相关的描述，必须包含以下链接：

| 权限类型 | 链接 |
|---------|------|
| 应用权限配置 | [https://open.feishu.cn/document/ugTN1YjL4UTN24CO1UjN/uQzN1YjL0cTN24CN3UjN](https://open.feishu.cn/document/ugTN1YjL4UTN24CO1UjN/uQzN1YjL0cTN24CN3UjN) |
| 用户相关的 ID 概念 | [https://open.feishu.cn/document/home/user-identity-introduction/introduction](https://open.feishu.cn/document/home/user-identity-introduction/introduction) |
| 部门 ID 说明 | [https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/contact-v3/department/field-overview](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/contact-v3/department/field-overview) |
| 权限范围校验 | [https://open.feishu.cn/document/ukTMukTMukTM/uETNz4SM1MjLxUzM/v3/guides/scope_authority](https://open.feishu.cn/document/ukTMukTMukTM/uETNz4SM1MjLxUzM/v3/guides/scope_authority) |
| 通用错误码 | [https://open.feishu.cn/document/ukTMukTMukTM/ugjM14COyUjL4ITN](https://open.feishu.cn/document/ukTMukTMukTM/ugjM14COyUjL4ITN) |

## 记录规则

1. **API 文档** - 每个 API 文件必须包含权限要求小节
2. **字段权限** - 涉及敏感字段时，必须标注所需权限及链接
3. **错误码** - 权限错误（如 40004, 41050）必须包含权限排查链接
4. **配置说明** - 权限配置步骤必须包含飞书后台操作指引

**使用规范**

- 所有文档必须保持飞书官方文档的完整性，禁止简化、省略、合并
- 所有示例必须完整展示，禁止省略部分行
- 所有字段必须完整说明权限要求，禁止推算或猜测
- 所有内容必须真实记录，禁止偷懒、失误或简化
- **禁止擅自发挥**：不允许对原始内容进行任何未明确要求的修改、改名、结构调整
- **禁止理解偏差**：如有不明确之处，必须向用户确认后再操作
- **必须认真仔细**：每一步操作都要核对原始文档，确保准确无误
