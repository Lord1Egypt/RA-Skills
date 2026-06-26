---
name: leisang-zl--virtual-item-constructor
description: >
  智能构造合规测试商品，支持按类目、业务身份、商品属性、商品标等条件查找或克隆商品，并自动改价和清理标签。
  当用户需要构造测试商品、查找测试商品、克隆商品到测试账号、修改测试商品价格，或用户提出"帮我找一个测试商品""构造一个XX类目的商品"时使用。
---

# 智能构造合规测试商品

根据用户需求，自动查找或构造一个合规、可用、价格正确、标签干净的测试商品。

## 基本要求

- 仅处理测试商品构造相关任务，超出职责范围的请求应礼貌拒绝
- 所有商品数据必须通过工具获取，不假设任何不存在的数据
- 工具调用失败时尝试修改参数重试，多次失败则跳过当前步骤继续分析
- 失败时必须返回具体原因，而非模糊提示

---

## 执行步骤

### 第 1 步：收集用户搜索条件

从用户输入中提取以下信息（如有）：

- 商品 ID（itemId）
- 卖家 ID（sellerId）
- 类目（category）
- 商品标（itemTags）
- 商品属性（itemProperties 或 features）
- 业务身份（bizCode）
- 价格要求

### 第 2 步：调用知识库补全业务规则

如果用户提到了业务身份（如 `ali.china.digital.virtual.charge`）或业务场景（如"话费""婚摄"），调用【虚拟商品Agent知识库搜索工具】查询对应的类目、商品标和属性规则。

**用户给的条件优先级更高**，知识库仅用于补充或修正。

**业务身份与商品标的映射规则**：

| 业务身份 | 处理方式 |
|---|---|
| `ali.china.digital.virtual.charge` | **不设置为 bizCode**，必须设置 itemTags = `2460930` |
| `ali.china.digital.virtual` | **不设置为 bizCode**，必须设置 itemTags = `3017730` |
| `ali.china.tmall.wt.telecom.custom`、`ali.china.tmall.wt.ecard.flow`、`ali.china.tmall.wt.vt.contract`、`ali.china.tmall.wt.vt.mobilenumber`、`ali.china.tmall.game.appledirect` | **不设置为 bizCode**，直接基于叶子类目搜索 |
| 其他业务身份（如 `ali.china.taobao.game.smc`、`ali.china.tmall.life` 等） | 直接将 bizCode 设为用户指定值 |

**注意**：知识库中"商品标的值为无"表示该类商品不需要专门打标，不需要调用打标去标工具。

### 第 3 步：判断是否按商品属性查找

如果最终搜索条件中包含 **商品属性（itemProperties）**：

1. 调用【通过商家id与属性查找商品】工具，仅传入 `itemProperties`，**不需要输入 sellerId**
2. 如果找到商品 → 跳到第 6 步（改价）
3. 如果没找到 → 告知用户"没找到匹配该属性的商品，请手动发布"

> 带属性的商品（如自动充值、区服）不能克隆，必须精准匹配。

### 第 4 步：查找已有测试商品（无属性时）

如果没有商品属性条件，则尝试查找已有测试商品：

1. 遍历所有可用类目（如有多个类目，逐个尝试）
2. 调用【商品查找】工具，设置标题为 `测试，请不要拍`，加上类目、商品标等条件
3. 一旦找到任意商品 → 记录商品 ID，跳到第 6 步

### 第 5 步：查找正式商品并克隆

如果所有类目都未找到测试商品：

1. 再次遍历类目，调用【商品查找】工具，**不设置标题**（查找正式商品）
2. 找到商品后，先调用【判断商品是否是测试商品】工具确认
3. 如果不是测试商品，调用【商品克隆】工具，依次尝试以下测试卖家：
   - `商家测试帐号10`
   - `文娱测试卖家`
4. 克隆成功 → 使用新商品 ID，进入第 6 步
5. 全部失败 → 告知用户具体失败原因
6. 如果连正式商品都找不到 → 告知"没找到符合条件的商品，请手动发布"

### 第 6 步：按用户要求调整价格

如果用户指定了价格（默认 1 分）：

1. 调用【获取商品skuId】工具获取 skuId
   - 有 SKU → 使用第一个 skuId
   - 无 SKU → 使用 `skuId = 0`
2. 调用【商品改价】工具：
   - `itemId`：当前商品 ID
   - `skuId`：上一步获取的值
   - `price`：用户指定价格（**单位为分**，1 元 = 100 分）

### 第 7 步：清理不该有的商品标

1. 调用【虚拟商品Agent知识库搜索工具】，查询该类目/业务身份下不应包含的商品标
2. 调用【商品信息查询】工具，获取当前商品实际商品标
3. 对比两者，若发现不该有的标签，调用【IC-商品打标&去标】工具逐个删除：
   - `itemId`：当前商品 ID
   - `removeTagId`：要删除的标签 ID

---

## 可用工具

### 商品查找

通过条件搜索商品。

```bash
python3 scripts/tool_7b712rnk8z.py '{"itemId": "...", "category": "...", "itemTags": "...", "bizCode": "...", "title": "...", "sellerId": "...", "features": "..."}'
```

**参数说明**：
- `itemId`（选填，string）：商品 ID，如 `973136869149`
- `category`（选填，string）：叶子类目 ID，如 `1623`
- `itemTags`（选填，string）：商品标，如 `4166`
- `bizCode`（选填，string）：业务身份，如 `ali.china.taobao`
- `title`（选填，string）：商品标题，如 `测试，请不要拍`
- `sellerId`（选填，string）：商家 ID
- `features`（选填，string）：商品 feature，如 `market:2`

### 商品克隆

将商品克隆到测试商家账号（已做安全处理，非测试商品不可用）。

```bash
python3 scripts/tool_780a1gyi1a.py '{"nick": "商家测试帐号10", "itemId": "963014656847"}'
```

**参数说明**：
- `nick`（选填，string）：测试账号名称，如 `商家测试帐号10`、`文娱测试卖家`
- `itemId`（选填，string）：要克隆的源商品 ID

### 商品改价

编辑测试商品价格。

```bash
python3 scripts/tool_d9be0gk8fx.py '{"itemId": "963014656847", "price": "100", "skuId": "0"}'
```

**参数说明**：
- `itemId`（必填，string）：商品 ID
- `price`（必填，string）：商品价格，**单位为分**（1 元 = 100 分）
- `skuId`（必填，string）：商品 skuId，若无 SKU 则设为 `0`

### 商品上下架

用于测试商品上下架（非测试商品不可用）。

```bash
python3 scripts/tool_d9158w6o48.py '{"itemId": "963014656847", "status": "0"}'
```

**参数说明**：
- `itemId`（必填，string）：商品 ID
- `status`（必填，string）：状态值，`0` 上架（正常态）、`1` 上架（被cc过）、`-2` 用户下架、`-3` 小二下架

### IC-商品打标&去标

对商品 tags 进行打标或去标。

```bash
python3 scripts/tool_b60afhvypr.py '{"itemId": 909844196750, "addTagId": 12345, "removeTagId": 12345}'
```

**参数说明**：
- `itemId`（必填，number）：商品 ID
- `addTagId`（选填，integer）：要打的标签 ID
- `removeTagId`（选填，integer）：要去掉的标签 ID

### 通过商家id与属性查找商品

通过商品属性精准匹配商品，**不需要输入 sellerId**。

```bash
python3 scripts/tool_1c309hxx6w.py '{"itemProperties": "20000:34611175102"}'
```

**参数说明**：
- `sellerId`（选填，string）：商家 ID（通常不需要输入）
- `itemProperties`（选填，string）：商品属性键值对，如 `20000:34611175102`

### 商品信息查询

查询商品详细信息，可辅助测试。

```bash
python3 scripts/tool_15f61488ow.py '{"itemId": 963014656847}'
```

**参数说明**：
- `itemId`（必填，number）：商品 ID

### 获取商品skuId

获取商品的 skuId 列表。

```bash
python3 scripts/tool_ac98dsyyv7.py '{"itemId": 887404976031}'
```

**参数说明**：
- `itemId`（必填，number）：商品 ID

### 判断商品是否是测试商品

判断指定商品是否为测试商品。

```bash
python3 scripts/tool_f85a579qn4.py '{"itemId": 837897208146}'
```

**参数说明**：
- `itemId`（必填，number）：商品 ID

### 类目&SPU数据构造助手

类目与 SPU 业务相关数据构造，支持多种意图。

```bash
python3 scripts/tool_c28c07jylq.py '{"question": "用户提问内容", "intentCode": "..."}'
```

**参数说明**：
- `question`（必填，string）：用户提问
- `intentCode`（选填，string）：意图编码，可选值：
  - `SPU Schema审核链路数据构造_task_ceab2ridux`
  - `推送类目增量包_task_d5477kjqtm`
  - `商家类目品牌授权_task_d5b24ucwyr`
  - `查询指定下类目的属性列表_task_53d8chhsvi`
  - `查询指定类目下指定属性的属性值_task_54011kgiyw`

### 虚拟商品Agent知识库搜索工具

从知识库中检索与查询相关的文本片段。

```bash
python3 scripts/tool_c28c0a39lt.py '{"query": "查询内容"}'
```

**参数说明**：
- `query`（必填，string）：查询内容

---

## 输出格式

构造完成后，按以下格式输出最终结果：

```
✅ 已为您构造测试商品：
商品ID：<商品ID>
标题：<商品标题>
价格：<价格，单位元>
卖家：<测试卖家名称>
商品标：<商品标列表，无则写"无">
链接：https://item.taobao.com/item.htm?id=<商品ID>
```

---

## 边界条件

| 场景 | 处理方式 |
|---|---|
| 用户未指定价格 | 默认改价为 1 分（0.01 元） |
| 用户未指定类目/业务身份 | 通过知识库搜索补全，无法补全时询问用户 |
| 有多个可用类目 | 逐个遍历尝试，直到找到可用商品 |
| 带商品属性（如自动充值、区服） | 走属性精准匹配，不克隆 |
| 克隆到第一个测试卖家失败 | 自动尝试第二个测试卖家 |
| 所有方式均未找到商品 | 返回具体失败原因，建议用户手动发布 |
| 知识库中商品标值为"无" | 不需要打标或去标 |
| 用户需求超出职责范围 | 礼貌拒绝，说明职责定位 |
| 工具调用多次失败 | 跳过当前步骤继续，最终告知用户哪些步骤未完成 |

---

## 交互样例

### 样例：构造话费测试商品

**用户**：构造一个话费测试商品，运营商为浙江移动，面额为1元，用于测试下单

**执行过程**：

1. 提取条件：话费、浙江移动、1 元
2. 调用知识库查询话费类目规则：

```bash
python3 scripts/tool_c28c0a39lt.py '{"query": "话费类目 商品标 属性"}'
```

3. 根据返回确认类目 150401（中国移动充值卡），属性 `20779:30676`（10元面值）
4. 因包含商品属性，调用属性查找：

```bash
python3 scripts/tool_1c309hxx6w.py '{"itemProperties": "20779:30676"}'
```

5. 找到商品后，判断是否为测试商品：

```bash
python3 scripts/tool_f85a579qn4.py '{"itemId": 13283288366}'
```

6. 非测试商品，克隆至测试卖家：

```bash
python3 scripts/tool_780a1gyi1a.py '{"nick": "商家测试帐号10", "itemId": "13283288366"}'
```

7. 获取 SKU 信息并改价为 100 分（1 元）：

```bash
python3 scripts/tool_ac98dsyyv7.py '{"itemId": 1028188541294}'
python3 scripts/tool_d9be0gk8fx.py '{"itemId": "1028188541294", "price": "100", "skuId": "0"}'
```

8. 查询商品信息确认标签，清理不该有的标签（如有）
9. 输出结果：

```
✅ 已为您构造测试商品：
商品ID：1028188541294
标题：(测试商品请不要拍)原品=13283288366
价格：0.01 元
卖家：商家测试帐号10
商品标：无（符合话费类目规则）
链接：https://item.taobao.com/item.htm?id=1028188541294