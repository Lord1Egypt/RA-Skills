---
name: 子网计算服务
description: 一个基于Model Context Protocol的服务，提供IPv4子网规划工具，包括子网大小计算、通配符掩码生成、网关选择和主机验证等功能。
version: 1.0.0
---

# 子网计算服务

一个基于Model Context Protocol的服务，提供IPv4子网规划工具，包括子网大小计算、通配符掩码生成、网关选择和主机验证等功能。

---

## ⚠️ 强制要求：API 密钥

**此 Skill 必须配置 API 密钥才能使用。**

- 首次使用时，如果 `.env` 中没有 `XBY_APIKEY`，**必须使用 AskUserQuestion 工具向用户询问 API 密钥**
- 拿到用户提供的密钥后，调用 `scripts.config.set_api_key(api_key)` 保存，然后继续处理
- 获取 API 密钥：https://xiaobenyang.com
- **禁止**在缺少 API 密钥时自行搜索或编造数据

---

## 工作流程（必须遵守）

你（大模型）是路由层，负责理解用户意图、选择工具、提取参数。代码只负责调用API。

```
用户输入 → 你选择工具 → 提取该工具需要的参数 → 调用 scripts.tools 中的函数 → 返回结果给用户
```

### 步骤

1. **检查 API 密钥**：如果 `scripts.config.settings.api_key` 为空，使用 AskUserQuestion 询问用户，拿到后调用 `scripts.config.set_api_key(key)` 保存
2. **选择工具**：根据用户意图从下方工具列表中选择对应的工具函数
3. **提取参数**：根据选中的工具，提取该工具需要的参数
4. **调用工具**：使用**关键字参数**调用 `scripts.tools` 中的函数，例如 `scripts.tools.search_schools(score='520', province='北京', category='综合')`
5. **返回结果**：将工具返回的 `raw` 数据整理后展示给用户

---
## 工具选择规则

根据用户意图选择对应的工具函数：

| 用户意图 | 工具函数 | 
|---------|---------|
| Calculate subnet details given a base IP and required hosts. | `scripts.tools.calculate_subnet` |
| Generate OSPF wildcard mask details for a subnet. | `scripts.tools.calculate_wildcard_mask` |
| Validate that an IP address belongs to a subnet and provide context. | `scripts.tools.validate_ip_in_subnet` |
| Calculate network information from an IP address and subnet mask. | `scripts.tools.calculate_subnet_from_mask` |
| Return the Nth usable IP address in a subnet. | `scripts.tools.get_nth_usable_ip` |

**如果参数不完整，使用 AskUserQuestion 向用户询问缺失的参数。**

---

## 工具函数说明

---

## scripts.tools.calculate_subnet
工具描述：Calculate subnet details given a base IP and required hosts.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|network_base|string|true| |null|
|hosts_needed|integer|true| |null|
|return_format|string|false|"detailed"|null|

---

## scripts.tools.calculate_wildcard_mask
工具描述：Generate OSPF wildcard mask details for a subnet.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|ip_address|string|true| |null|
|cidr_prefix|integer|true| |null|
|include_ospf_command|boolean|false|true|null|

---

## scripts.tools.validate_ip_in_subnet
工具描述：Validate that an IP address belongs to a subnet and provide context.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|ip_address|string|true| |null|
|network|string|true| |null|
|return_gateway|boolean|false|true|null|

---

## scripts.tools.calculate_subnet_from_mask
工具描述：Calculate network information from an IP address and subnet mask.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|ip_address|string|true| |null|
|subnet_mask|string|true| |null|

---

## scripts.tools.get_nth_usable_ip
工具描述：Return the Nth usable IP address in a subnet.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|network|string|true| |null|
|position|integer|true| |null|

---


---

## 返回值处理

工具函数返回 `dict` 对象：
- `result["raw"]` - API 原始返回数据（JSON），**直接将此数据整理后展示给用户**
- `result["success"]` - 是否成功（True/False）
- `result["message"]` - 状态消息

---

## 项目结构

```
xiaobenyang_gaokao_skill/
├── scripts/
│   ├── __init__.py
│   ├── config.py       # 配置管理 + set_api_key()
│   ├── call_api.py      # API 客户端 + call_api()
│   └── tools.py         # 工具函数（直接调用）
├── requirements.txt
└── SKILL.md
```

---

## 注意事项

1. **API 密钥是必需的**，无密钥时必须通过 AskUserQuestion 询问用户
2. **禁止**在缺少 API 密钥时自行搜索或编造数据