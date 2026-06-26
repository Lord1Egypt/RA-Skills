# 使用示例

## 目录
- [用户管理示例](#用户管理示例)
- [产品管理示例](#产品管理示例)
- [订单管理示例](#订单管理示例)
- [综合场景示例](#综合场景示例)

---

## 用户管理示例

### 1. 获取所有用户
**请求**:
```
"获取所有用户"
```

**执行流程**:
1. 识别意图: GET_RESOURCE
2. 识别实体类型: uctoo_user
3. 调用API: `GET /api/uctoo/uctoo_user/10/1`
4. 返回用户列表

### 2. 获取特定用户
**请求**:
```
"查找ID为3a5a079d-38b2-4ea2-b8cd-f3c0d93dacfb的用户"
```

**执行流程**:
1. 识别意图: GET_RESOURCE
2. 提取ID: 3a5a079d-38b2-4ea2-b8cd-f3c0d93dacfb
3. 调用API: `GET /api/uctoo/uctoo_user/3a5a079d-38b2-4ea2-b8cd-f3c0d93dacfb`

### 3. 创建新用户
**请求**:
```
"创建一个名为李四的新用户，邮箱是lisi@example.com，电话是13900139000"
```

**执行流程**:
1. 识别意图: CREATE_RESOURCE
2. 提取参数:
   - username: 李四
   - email: lisi@example.com
   - phone: 13900139000
3. 调用API: `POST /api/uctoo/uctoo_user/add`

### 4. 更新用户信息
**请求**:
```
"更新用户456的邮箱为newemail@example.com"
```

**执行流程**:
1. 识别意图: UPDATE_RESOURCE
2. 提取参数:
   - id: 456
   - email: newemail@example.com
3. 调用API: `POST /api/uctoo/uctoo_user/edit`

### 5. 删除用户
**请求**:
```
"删除用户789"
```

**执行流程**:
1. 识别意图: DELETE_RESOURCE
2. 提取ID: 789
3. 调用API: `POST /api/uctoo/uctoo_user/del`

---

## 产品管理示例

### 1. 查询产品列表
**请求**:
```
"显示所有产品，每页20个"
```

**执行流程**:
1. 识别意图: GET_RESOURCE
2. 识别实体类型: product
3. 提取参数: limit=20, page=1
4. 调用API: `GET /api/uctoo/product/20/1`

### 2. 创建产品
**请求**:
```
"添加一个新产品，名称是智能手表，价格是999元，库存是100件"
```

**执行流程**:
1. 识别意图: CREATE_RESOURCE
2. 识别实体类型: product
3. 提取参数:
   - name: 智能手表
   - price: 999
   - stock: 100
4. 调用API: `POST /api/uctoo/product/add`

---

## 订单管理示例

### 1. 查询订单
**请求**:
```
"查看最近的订单"
```

**执行流程**:
1. 识别意图: GET_RESOURCE
2. 识别实体类型: order
3. 调用API: `GET /api/uctoo/order/10/1`

### 2. 创建订单
**请求**:
```
"为用户123创建一个订单，购买产品456，数量2个"
```

**执行流程**:
1. 识别意图: CREATE_RESOURCE
2. 识别实体类型: order
3. 提取参数:
   - user_id: 123
   - product_id: 456
   - quantity: 2
4. 调用API: `POST /api/uctoo/order/add`

### 3. 更新订单状态
**请求**:
```
"将订单789的状态更新为已发货"
```

**执行流程**:
1. 识别意图: UPDATE_RESOURCE
2. 识别实体类型: order
3. 提取参数:
   - id: 789
   - status: 已发货
4. 调用API: `POST /api/uctoo/order/edit`

---

## 综合场景示例

### 场景1: 完整的购物流程
**请求序列**:
1. "使用账号demo和密码123456登录"
2. "查看所有产品"
3. "创建一个新订单，购买产品1，数量3个"
4. "查看我的订单"

**执行流程**:
1. 登录 → 获取 access_token
2. 查询产品列表
3. 创建订单
4. 查询订单列表

### 场景2: 用户管理工作流
**请求序列**:
1. "登录系统"
2. "创建用户张三"
3. "查看所有用户"
4. "更新张三的电话为13800138000"
5. "删除测试用户"

**执行流程**:
1. 认证
2. CRUD操作
3. 确认结果

---

## 提示和技巧

### 1. 明确指定操作
- ✅ 好: "创建名为张三的用户"
- ❌ 坏: "处理一下用户"

### 2. 提供完整参数
- ✅ 好: "创建用户李四，邮箱lisi@example.com，电话13900139000"
- ❌ 坏: "创建一个用户"

### 3. 使用自然的语言
- ✅ 好: "帮我查一下有哪些产品"
- ❌ 坏: "执行GET /api/uctoo/product"

### 4. 先登录再操作
需要认证的操作，请先登录：
> "使用账号demo和密码123456登录"
