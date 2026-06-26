# 接口测试标准

> 适用范围：券商交易系统 RESTful/WebSocket 接口的测试规范，涵盖断言策略、接口串联、并发幂等、异常注入。

## 1. 断言三层次

### 1.1 第一层：状态断言（HTTP 状态码）

#### 定义

验证接口返回的 HTTP 状态码是否符合预期。这是最基础的断言层次，确保接口可达且请求被正确处理。

#### 适用场景

- 所有接口测试的第一步
- 快速判断接口是否正常响应
- 验证权限控制（401/403）、资源存在性（404）、服务可用性（500/503）

#### 券商业务示例

```python
import requests
import pytest

class TestOrderAPI:
    BASE_URL = "https://api.broker.com/v1"
    
    def test_place_order_success(self, auth_headers):
        """正常下单 - 期望200"""
        payload = {
            "stockCode": "600519",
            "price": 1800.00,
            "quantity": 100,
            "direction": "BUY",
            "orderType": "LIMIT"
        }
        resp = requests.post(
            f"{self.BASE_URL}/orders",
            json=payload,
            headers=auth_headers
        )
        assert resp.status_code == 200
    
    def test_place_order_unauthorized(self):
        """未携带token - 期望401"""
        resp = requests.post(f"{self.BASE_URL}/orders", json={})
        assert resp.status_code == 401
    
    def test_place_order_forbidden(self, readonly_headers):
        """只读权限下单 - 期望403"""
        resp = requests.post(
            f"{self.BASE_URL}/orders",
            json={"stockCode": "600519"},
            headers=readonly_headers
        )
        assert resp.status_code == 403
    
    def test_query_nonexistent_order(self, auth_headers):
        """查询不存在的委托 - 期望404"""
        resp = requests.get(
            f"{self.BASE_URL}/orders/NONEXISTENT_ID",
            headers=auth_headers
        )
        assert resp.status_code == 404
```

#### 测试点模板

| 编号 | 测试点 | 优先级 | 预期结果 |
|------|--------|--------|---------|
| TC-SA-001 | 正常请求下单接口，验证返回 HTTP 200 | P0 | status_code == 200 |
| TC-SA-002 | 未携带 Authorization 头请求下单，验证返回 401 | P0 | status_code == 401 |
| TC-SA-003 | 使用只读 token 请求下单，验证返回 403 | P1 | status_code == 403 |

### 1.2 第二层：JSONPath 断言（响应体字段）

#### 定义

验证响应体 JSON 中特定字段的值、类型、结构是否符合预期。使用 JSONPath 表达式精确定位字段，验证业务逻辑的正确性。

#### 适用场景

- 验证业务返回值的正确性（委托编号、成交价格、账户余额）
- 验证响应结构完整性（必填字段是否存在）
- 验证枚举值是否在合法范围内

#### 券商业务示例

```python
import jsonpath_ng.ext as jp

class TestOrderResponse:
    
    def test_order_response_structure(self, auth_headers):
        """验证下单响应体结构和字段值"""
        payload = {
            "stockCode": "600519",
            "price": 1800.00,
            "quantity": 100,
            "direction": "BUY",
            "orderType": "LIMIT",
            "clientOrderId": "CLI_20260418_001"
        }
        resp = requests.post(
            f"{self.BASE_URL}/orders",
            json=payload,
            headers=auth_headers
        )
        data = resp.json()
        
        # 验证业务状态码
        assert data["code"] == 0, f"业务错误: {data.get('message')}"
        
        # 验证必填字段存在且类型正确
        result = data["data"]
        assert isinstance(result["orderId"], str)
        assert len(result["orderId"]) > 0
        
        # 验证回显字段与请求一致
        assert result["stockCode"] == "600519"
        assert result["direction"] == "BUY"
        assert result["quantity"] == 100
        
        # 验证状态枚举值
        assert result["status"] in [
            "PENDING", "SUBMITTED", "PARTIAL_FILLED",
            "FILLED", "CANCELLED", "REJECTED"
        ]
        
        # 验证时间戳合理性
        assert result["createTime"] > 0
        
    def test_order_list_pagination(self, auth_headers):
        """验证分页查询响应"""
        resp = requests.get(
            f"{self.BASE_URL}/orders?page=1&pageSize=10",
            headers=auth_headers
        )
        data = resp.json()["data"]
        
        # 验证分页结构
        assert "total" in data
        assert "list" in data
        assert isinstance(data["list"], list)
        assert len(data["list"]) <= 10  # 不超过pageSize
        
        # 验证列表中每条记录的必填字段
        for order in data["list"]:
            assert "orderId" in order
            assert "stockCode" in order
            assert "status" in order
```

#### 测试点模板

| 编号 | 测试点 | 优先级 | 预期结果 |
|------|--------|--------|---------|
| TC-JP-001 | 下单成功后验证 data.orderId 非空且为字符串 | P0 | orderId 存在且 len > 0 |
| TC-JP-002 | 下单成功后验证 data.status 为合法枚举值 | P0 | status ∈ {PENDING, SUBMITTED, ...} |
| TC-JP-003 | 分页查询验证 data.list 长度不超过 pageSize | P1 | len(list) <= pageSize |

### 1.3 第三层：DB 断言（数据库验证）

#### 定义

直接查询数据库，验证接口操作后数据库中的数据状态是否正确。这是最深层的断言，确保数据持久化的正确性，防止"接口返回成功但数据未落库"的问题。

#### 适用场景

- 涉及资金变动的操作（下单冻结、成交扣款、撤单释放）
- 状态变更操作（委托状态、账户状态）
- 数据一致性验证（缓存与数据库是否一致）

#### 券商业务示例

```python
import pymysql
import pytest

class TestOrderDBAssert:
    
    @pytest.fixture
    def db_conn(self):
        conn = pymysql.connect(
            host="test-db.broker.internal",
            port=3306,
            user="test_reader",
            password="****",
            database="trade_db",
            charset="utf8mb4"
        )
        yield conn
        conn.close()
    
    def test_order_persisted_after_place(self, auth_headers, db_conn):
        """下单后验证数据库委托记录"""
        client_order_id = f"CLI_{int(time.time())}"
        payload = {
            "stockCode": "600519",
            "price": 1800.00,
            "quantity": 100,
            "direction": "BUY",
            "clientOrderId": client_order_id
        }
        resp = requests.post(
            f"{self.BASE_URL}/orders",
            json=payload,
            headers=auth_headers
        )
        order_id = resp.json()["data"]["orderId"]
        
        # DB断言：验证委托记录落库
        cursor = db_conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            "SELECT * FROM t_order WHERE order_id = %s",
            (order_id,)
        )
        row = cursor.fetchone()
        
        assert row is not None, "委托记录未落库"
        assert row["stock_code"] == "600519"
        assert float(row["price"]) == 1800.00
        assert row["quantity"] == 100
        assert row["direction"] == "BUY"
        assert row["status"] == "PENDING"
        assert row["client_order_id"] == client_order_id
    
    def test_fund_frozen_after_place(self, auth_headers, db_conn, account_id):
        """下单后验证资金冻结"""
        # 下单前查询可用资金
        cursor = db_conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            "SELECT available_balance, frozen_amount FROM t_fund_account WHERE account_id = %s",
            (account_id,)
        )
        before = cursor.fetchone()
        
        # 下单：买入100股 × 1800元 = 180,000元
        payload = {
            "stockCode": "600519", "price": 1800.00,
            "quantity": 100, "direction": "BUY"
        }
        requests.post(f"{self.BASE_URL}/orders", json=payload, headers=auth_headers)
        
        # DB断言：验证资金冻结
        cursor.execute(
            "SELECT available_balance, frozen_amount FROM t_fund_account WHERE account_id = %s",
            (account_id,)
        )
        after = cursor.fetchone()
        
        expected_frozen = 1800.00 * 100  # 不含手续费简化示例
        assert float(after["frozen_amount"]) - float(before["frozen_amount"]) == pytest.approx(expected_frozen, rel=1e-2)
        assert float(before["available_balance"]) - float(after["available_balance"]) == pytest.approx(expected_frozen, rel=1e-2)

#### 测试点模板

| 编号 | 测试点 | 优先级 | 预期结果 |
|------|--------|--------|---------|
| TC-DB-001 | 下单成功后查询 t_order 表，验证委托记录正确落库 | P0 | 记录存在，字段值与请求一致 |
| TC-DB-002 | 买入下单后查询 t_fund_account，验证可用资金减少、冻结金额增加 | P0 | frozen_amount 增加 = price × quantity |
| TC-DB-003 | 撤单成功后查询 t_fund_account，验证冻结资金释放 | P0 | frozen_amount 减少，available_balance 恢复 |
```

---

## 2. 接口串联场景

### 定义

模拟真实业务流程中多个接口的调用顺序和数据传递关系。前置接口的输出作为目标接口的输入，目标接口执行后通过后置接口或 DB 验证最终状态。

### 适用场景

- 业务流程涉及多步骤操作（开户→入金→下单→查询）
- 接口之间有数据依赖（下单返回 orderId → 撤单需要 orderId）
- 需要验证全链路数据一致性

### 券商业务示例：委托下单→查询→撤单 全链路

```python
class TestOrderChain:
    """委托全链路串联测试"""
    
    def test_order_full_lifecycle(self, auth_headers):
        """
        串联流程：
        1. [前置] 查询账户资金 → 确认可用余额充足
        2. [目标] 提交限价买入委托
        3. [后置] 查询委托详情 → 验证状态和字段
        4. [目标] 提交撤单请求
        5. [后置] 查询委托详情 → 验证状态变为已撤
        6. [后置] 查询账户资金 → 验证冻结释放
        """
        # Step 1: 前置 - 查询可用资金
        fund_resp = requests.get(
            f"{self.BASE_URL}/account/fund",
            headers=auth_headers
        )
        assert fund_resp.status_code == 200
        available_before = fund_resp.json()["data"]["availableBalance"]
        assert available_before >= 180000, "可用资金不足，无法执行测试"
        
        # Step 2: 目标 - 下单
        order_payload = {
            "stockCode": "600519",
            "price": 1800.00,
            "quantity": 100,
            "direction": "BUY",
            "orderType": "LIMIT"
        }
        order_resp = requests.post(
            f"{self.BASE_URL}/orders",
            json=order_payload,
            headers=auth_headers
        )
        assert order_resp.status_code == 200
        order_id = order_resp.json()["data"]["orderId"]
        
        # Step 3: 后置验证 - 查询委托详情
        detail_resp = requests.get(
            f"{self.BASE_URL}/orders/{order_id}",
            headers=auth_headers
        )
        assert detail_resp.status_code == 200
        detail = detail_resp.json()["data"]
        assert detail["status"] in ["PENDING", "SUBMITTED"]
        assert detail["stockCode"] == "600519"
        
        # Step 4: 目标 - 撤单
        cancel_resp = requests.delete(
            f"{self.BASE_URL}/orders/{order_id}",
            headers=auth_headers
        )
        assert cancel_resp.status_code == 200
        
        # Step 5: 后置验证 - 确认撤单状态
        import time
        time.sleep(1)  # 等待异步处理
        detail_resp2 = requests.get(
            f"{self.BASE_URL}/orders/{order_id}",
            headers=auth_headers
        )
        assert detail_resp2.json()["data"]["status"] == "CANCELLED"
        
        # Step 6: 后置验证 - 资金释放
        fund_resp2 = requests.get(
            f"{self.BASE_URL}/account/fund",
            headers=auth_headers
        )
        available_after = fund_resp2.json()["data"]["availableBalance"]
        assert available_after == pytest.approx(available_before, rel=1e-2)
```

### 测试点模板

| 编号 | 测试点 | 优先级 | 预期结果 |
|------|--------|--------|---------|
| TC-CH-001 | 下单→查询→撤单→查询 全链路，验证状态流转和资金变化 | P0 | 各步骤状态正确，撤单后资金释放 |
| TC-CH-002 | 开户→风险评估→签署协议→开通融资融券 串联流程 | P0 | 各步骤依次成功，最终融资融券状态为已开通 |
| TC-CH-003 | 银行转账→资金到账→下单→成交→资金扣减 全链路 | P1 | 资金流水完整，余额变化与成交金额一致 |

---

## 3. 并发与幂等性测试

### 定义

- **并发测试**：模拟多个请求同时到达，验证系统在并发场景下的数据一致性和正确性。
- **幂等性测试**：验证同一请求重复提交多次，系统只产生一次业务效果（不重复下单、不重复扣款）。

### 适用场景

- 资金操作（转账、下单）的并发安全
- 网络重试导致的重复请求
- 高频交易场景的吞吐量验证
- 分布式系统的一致性保障

### 券商业务示例

```python
import concurrent.futures
import uuid

class TestConcurrencyAndIdempotency:
    
    def test_concurrent_buy_sell_same_stock(self, auth_headers):
        """并发测试：同一账户同时买入和卖出同一股票"""
        def place_order(direction):
            payload = {
                "stockCode": "600519",
                "price": 1800.00,
                "quantity": 100,
                "direction": direction,
                "orderType": "LIMIT",
                "clientOrderId": str(uuid.uuid4())
            }
            return requests.post(
                f"{self.BASE_URL}/orders",
                json=payload,
                headers=auth_headers
            )
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            for _ in range(5):
                futures.append(executor.submit(place_order, "BUY"))
                futures.append(executor.submit(place_order, "SELL"))
            
            results = [f.result() for f in futures]
        
        # 验证：所有请求都应得到明确响应（成功或明确的业务拒绝）
        for resp in results:
            assert resp.status_code in [200, 400, 409]
            if resp.status_code == 200:
                assert resp.json()["data"]["orderId"] is not None
    
    def test_idempotency_with_client_order_id(self, auth_headers):
        """幂等性测试：相同clientOrderId重复提交，只产生一笔委托"""
        client_order_id = f"IDEM_{uuid.uuid4()}"
        payload = {
            "stockCode": "600519",
            "price": 1800.00,
            "quantity": 100,
            "direction": "BUY",
            "clientOrderId": client_order_id
        }
        
        # 第一次提交
        resp1 = requests.post(
            f"{self.BASE_URL}/orders",
            json=payload,
            headers=auth_headers
        )
        assert resp1.status_code == 200
        order_id_1 = resp1.json()["data"]["orderId"]
        
        # 第二次提交（模拟网络重试）
        resp2 = requests.post(
            f"{self.BASE_URL}/orders",
            json=payload,
            headers=auth_headers
        )
        # 幂等：应返回相同orderId或明确的重复提示
        if resp2.status_code == 200:
            order_id_2 = resp2.json()["data"]["orderId"]
            assert order_id_1 == order_id_2, "幂等失败：产生了不同的委托编号"
        elif resp2.status_code == 409:
            assert "duplicate" in resp2.json()["message"].lower()
    
    def test_concurrent_fund_withdraw(self, auth_headers):
        """并发测试：同时发起多笔出金，验证不超额"""
        def withdraw(amount):
            return requests.post(
                f"{self.BASE_URL}/fund/withdraw",
                json={"amount": amount, "bankAccount": "6222****1234"},
                headers=auth_headers
            )
        
        # 假设可用余额10万，同时发起5笔3万出金
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(withdraw, 30000) for _ in range(5)]
            results = [f.result() for f in futures]
        
        success_count = sum(1 for r in results if r.status_code == 200)
        # 最多只能成功3笔（3×3万=9万 < 10万），第4笔应因余额不足失败
        assert success_count <= 3, f"超额出金：成功了{success_count}笔"
```

### 测试点模板

| 编号 | 测试点 | 优先级 | 预期结果 |
|------|--------|--------|---------|
| TC-CI-001 | 相同 clientOrderId 重复提交下单，验证幂等性（只产生一笔委托） | P0 | 第二次返回相同 orderId 或 409 |
| TC-CI-002 | 10线程并发出金，验证总出金不超过可用余额 | P0 | 成功笔数 × 金额 ≤ 可用余额 |
| TC-CI-003 | 并发撤单同一委托，验证只有一次撤单成功 | P1 | 仅一个请求返回成功，其余返回"已撤单"或 409 |

---

## 4. 异常注入测试

### 定义

通过人为制造异常条件（网络超时、服务降级、数据异常），验证系统的容错能力和异常处理逻辑。确保系统在异常情况下不会产生脏数据、资金错误或无响应。

### 适用场景

- 网络不稳定场景（超时、断连、重试）
- 依赖服务故障（数据库不可用、第三方接口异常）
- 数据异常（字段缺失、类型错误、超长字符串）
- 限流/熔断验证

### 券商业务示例

```python
import responses
from unittest.mock import patch

class TestExceptionInjection:
    
    def test_timeout_handling(self, auth_headers):
        """超时注入：设置极短超时，验证客户端处理"""
        try:
            resp = requests.post(
                f"{self.BASE_URL}/orders",
                json={"stockCode": "600519", "price": 1800, "quantity": 100, "direction": "BUY"},
                headers=auth_headers,
                timeout=0.001  # 极短超时
            )
        except requests.exceptions.Timeout:
            pass  # 预期超时
        
        # 验证：超时后不应产生重复委托
        orders = requests.get(
            f"{self.BASE_URL}/orders?stockCode=600519&status=PENDING",
            headers=auth_headers,
            timeout=10
        ).json()["data"]["list"]
        # 委托数量应为0或1，不应因重试产生多笔
    
    def test_malformed_request_body(self, auth_headers):
        """数据异常注入：发送畸形请求体"""
        test_cases = [
            # 缺少必填字段
            ({"stockCode": "600519"}, "缺少price/quantity/direction"),
            # 字段类型错误
            ({"stockCode": 600519, "price": "abc", "quantity": "xyz", "direction": "BUY"}, "类型错误"),
            # 超长字符串
            ({"stockCode": "A" * 10000, "price": 1800, "quantity": 100, "direction": "BUY"}, "超长stockCode"),
            # SQL注入尝试
            ({"stockCode": "600519' OR 1=1--", "price": 1800, "quantity": 100, "direction": "BUY"}, "SQL注入"),
            # 负数金额
            ({"stockCode": "600519", "price": -1800, "quantity": -100, "direction": "BUY"}, "负数"),
        ]
        
        for payload, desc in test_cases:
            resp = requests.post(
                f"{self.BASE_URL}/orders",
                json=payload,
                headers=auth_headers
            )
            assert resp.status_code in [400, 422], f"[{desc}] 应返回400/422，实际: {resp.status_code}"
            assert resp.json()["code"] != 0, f"[{desc}] 不应返回业务成功"
    
    def test_rate_limit(self, auth_headers):
        """限流测试：短时间大量请求触发限流"""
        responses_list = []
        for _ in range(100):
            resp = requests.get(
                f"{self.BASE_URL}/orders",
                headers=auth_headers
            )
            responses_list.append(resp)
        
        rate_limited = [r for r in responses_list if r.status_code == 429]
        assert len(rate_limited) > 0, "未触发限流保护"
        
        # 验证限流响应包含 Retry-After 头
        for r in rate_limited:
            assert "Retry-After" in r.headers
```

### 测试点模板

| 编号 | 测试点 | 优先级 | 预期结果 |
|------|--------|--------|---------|
| TC-EI-001 | 发送缺少必填字段的请求体，验证参数校验 | P0 | 返回 400，明确提示缺少哪个字段 |
| TC-EI-002 | 发送 SQL 注入字符串作为 stockCode，验证安全防护 | P0 | 返回 400，不执行注入语句 |
| TC-EI-003 | 短时间发送100次请求，验证限流机制触发 | P1 | 部分请求返回 429，包含 Retry-After |
| TC-EI-004 | 请求超时后查询委托列表，验证无重复委托 | P1 | 委托数量正确，无因超时重试产生的重复单 |
| TC-EI-005 | 发送超长字符串（10000字符）作为字段值，验证长度校验 | P2 | 返回 400/422，不导致服务崩溃 |
