# 地域归一化公共规则

## 适用范围

本规则适用于 `tencent-pg-management`、`tencent-pg-inspection`、`tencent-pg-slowquery-diagnosis`，以及对应 bundle 根入口。

## 目标

- 在真正发起腾讯云接口调用前，把用户输入的地域统一转换为标准地域码
- 尽量接受用户常见写法，但**不要对无法确认的输入做猜测性修正**
- 当地域无效或无法归一化时，统一转入 `@references/common/error_handling.md` 中的 `invalid-region` 模板

## 归一化顺序

1. **优先使用标准地域码**：如果输入已经是 `ap-guangzhou`、`ap-shanghai`、`ap-chengdu`、`ap-beijing`，直接使用。
2. **接受常见中文别名**：若用户输入为常见中文地域，则映射到标准地域码。
3. **接受运行时默认地域**：如果用户未显式提供地域，但运行时已提供 `TENCENTCLOUD_REGION`，则可将其视为默认地域。
4. **无法安全确认时立即停止**：若输入无法稳定映射，或存在多个可能值，不要自行猜测，应直接提示用户修正。

## 当前支持的常见别名

| 用户输入 | 标准地域码 |
|---|---|
| `广州` | `ap-guangzhou` |
| `上海` | `ap-shanghai` |
| `成都` | `ap-chengdu` |
| `北京` | `ap-beijing` |

## 非法地域处理规则

出现以下任一情况，都视为“地域非法”或“地域无法确认”：

- 输入既不是标准地域码，也不在别名表中
- 输入为模糊描述，例如“华南”“国内”“离用户近一点”
- 输入包含明显拼写错误，例如 `guangzou`、`ap-gz`

此时必须：

- 原样回显用户输入
- 给出最接近的合法示例，但不要伪造“已确认映射”
- 附上可直接操作的 PostgreSQL 控制台入口和最短核对路径
- 如果当前链路具备只读能力，再补一句可代查支持地域
- 参考 `@references/common/error_handling.md` 中的 `invalid-region` 模板

## 官方核对入口

- [PostgreSQL 控制台](https://console.cloud.tencent.com/postgres)
  - 打开后先看右上角地域选择器
  - 如果已有实例，也可以在实例列表里直接查看实例所属地域

## 输出要求

在进入后续接口调用前，最终上下文里至少保留两项：

- 原始输入地域
- 归一化后的标准地域码

如果无法归一化，则明确标记为 `region unresolved`，并停止后续调用。
