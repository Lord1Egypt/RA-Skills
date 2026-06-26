# 接口契约知识

> 适用范围：券商交易系统 API 接口的契约规范，涵盖字段约束、枚举值、签名验证、幂等键设计、错误码体系。

## 1. 请求/响应字段约束

### 定义

接口契约中每个字段都有明确的约束条件：是否必填、数据类型、长度限制、格式要求、取值范围。字段约束是接口测试的基础，违反约束的请求应被明确拒绝。

### 适用场景

- 接口联调时验证字段格式
- 回归测试中验证字段约束未被破坏
- 新接口上线前的契约验证
- 前后端字段对齐检查

### 券商业务示例：委托下单接口字段约束

#### 请求字段（POST /api/v1/orders）

| 字段名 | 类型 | 必填 | 长度/范围 | 格式 | 说明 |
|--------|------|------|----------|------|------|
| stockCode | string | 是 | 6位 | `^\d{6}$` | 证券代码 |
| exchangeId | string | 是 | 枚举 | SH/SZ/BJ | 交易所代码 |
| direction | string | 是 | 枚举 | BUY/SELL | 买卖方向 |
| orderType | string | 是 | 枚举 | LIMIT/MARKET/STOP | 委托类型 |
| price | decimal | 条件必填 | >0, ≤2位小数 | `^\d+(\.\d{1,2})?$` | 限价委托必填，市价委托不填 |
| quantity | integer | 是 | 100~99999900 | 正整数 | 委托数量 |
| clientOrderId | string | 否 | 1~64字符 | `^[a-zA-Z0-9_-]+$` | 客户端幂等键 |
| accountId | string | 是 | 1~32字符 | 字母数字 | 资金账号 |
| remark | string | 否 | 0~256字符 | UTF-8 | 备注 |

#### 响应字段（成功时）

| 字段名 | 类型 | 必返回 | 说明 |
|--------|------|--------|------|
| code | integer | 是 | 业务状态码，0=成功 |
| message | string | 是 | 状态描述 |
| data.orderId | string | 是 | 系统委托编号 |
| data.stockCode | string | 是 | 回显证券代码 |
| data.direction | string | 是 | 回显买卖方向 |
| data.orderType | string | 是 | 回显委托类型 |
| data.price | decimal | 是 | 回显委托价格 |
| data.quantity | integer | 是 | 回显委托数量 |
| data.status | string | 是 | 委托状态枚举 |
| data.createTime | long | 是 | 创建时间戳（毫秒） |
| data.clientOrderId | string | 条件 | 请求中传了则回显 |

### 测试点模板

| 编号 | 测试点 | 优先级 | 预期结果 |
|------|--------|--------|---------|
| TC-FC-001 | 缺少必填字段 stockCode，验证返回明确错误 | P0 | 返回 400，message 包含"stockCode 不能为空" |
| TC-FC-002 | stockCode 传入7位数字"6005199"，验证长度校验 | P0 | 返回 400，message 包含"stockCode 格式错误" |
| TC-FC-003 | 市价委托时传入 price 字段，验证条件字段处理 | P1 | 忽略 price 或返回提示 |
| TC-FC-004 | clientOrderId 传入特殊字符"abc@#$"，验证格式校验 | P1 | 返回 400，提示 clientOrderId 格式不合法 |
| TC-FC-005 | remark 传入257个字符，验证长度上限 | P2 | 返回 400 或截断为256字符 |

---

## 2. 枚举值规范

### 定义

接口中的枚举字段有固定的合法取值集合。传入非法枚举值应被明确拒绝，不能静默忽略或产生未定义行为。

### 适用场景

- 委托类型、买卖方向、委托状态等核心枚举字段
- 新增枚举值时的兼容性验证
- 前后端枚举值对齐检查

### 券商业务枚举值定义

#### 委托类型（orderType）

| 枚举值 | 含义 | 适用市场 | 说明 |
|--------|------|---------|------|
| LIMIT | 限价委托 | 全市场 | 指定价格，等待撮合 |
| MARKET | 市价委托 | 沪深（连续竞价时段） | 按市场最优价成交 |
| MARKET_BEST5 | 最优五档即时成交 | 沪市 | 对手方最优5档 |
| MARKET_BEST5_CANCEL | 最优五档即时成交剩余撤销 | 深市 | 未成交部分自动撤单 |
| MARKET_COUNTERPART_BEST | 对手方最优价格 | 深市 | 按对手方最优价 |
| STOP | 条件单/止损单 | 部分券商 | 触发条件后自动下单 |

#### 委托状态（orderStatus）

| 枚举值 | 含义 | 是否终态 | 可转换到 |
|--------|------|---------|---------|
| PENDING | 未报 | 否 | SUBMITTED, REJECTED |
| SUBMITTED | 已报 | 否 | PARTIAL_FILLED, FILLED, CANCELLED |
| PARTIAL_FILLED | 部分成交 | 否 | FILLED, CANCELLED |
| FILLED | 全部成交 | 是 | — |
| CANCELLED | 已撤单 | 是 | — |
| REJECTED | 废单 | 是 | — |

#### 买卖方向（direction）

| 枚举值 | 含义 | 说明 |
|--------|------|------|
| BUY | 买入 | 普通买入 |
| SELL | 卖出 | 普通卖出 |
| MARGIN_BUY | 融资买入 | 信用账户 |
| SHORT_SELL | 融券卖出 | 信用账户 |
| BUY_TO_COVER | 买券还券 | 信用账户 |
| SELL_TO_REPAY | 卖券还款 | 信用账户 |

### 测试点模板

| 编号 | 测试点 | 优先级 | 预期结果 |
|------|--------|--------|---------|
| TC-EN-001 | orderType 传入非法值"INVALID_TYPE"，验证枚举校验 | P0 | 返回 400，提示"不支持的委托类型" |
| TC-EN-002 | direction 传入"buy"（小写），验证大小写敏感性 | P0 | 返回 400 或自动转换（取决于契约约定） |
| TC-EN-003 | 沪市传入深市专属市价类型 MARKET_BEST5_CANCEL，验证市场适用性 | P1 | 返回 400，提示"该委托类型不适用于沪市" |
| TC-EN-004 | 普通账户传入 MARGIN_BUY（融资买入），验证账户类型校验 | P1 | 返回 400，提示"非信用账户不支持融资买入" |
| TC-EN-005 | 传入空字符串""作为 direction，验证空值处理 | P2 | 返回 400，提示"direction 不能为空" |

---

## 3. 签名规则

### 定义

API 请求通过数字签名验证请求的完整性和身份真实性。常见方案有 HMAC-SHA256 和 RSA 签名。签名错误的请求必须被拒绝，防止篡改和伪造。

### 适用场景

- 所有涉及资金操作的接口（下单、转账、出金）
- 第三方系统对接（银行、交易所）
- Open API 对外开放接口

### 券商业务签名方案

#### HMAC-SHA256 签名流程

```
1. 构造待签名字符串：
   - 将请求参数按 key 字母序排列
   - 拼接为 key1=value1&key2=value2&... 格式
   - 追加 timestamp 和 nonce

2. 使用 secretKey 计算 HMAC-SHA256

3. 将签名放入请求头 X-Signature
```

#### Python 工程实现

```python
import hmac
import hashlib
import time
import uuid
from urllib.parse import urlencode
from collections import OrderedDict

class ApiSigner:
    """券商API签名工具"""
    
    def __init__(self, api_key: str, secret_key: str):
        self.api_key = api_key
        self.secret_key = secret_key
    
    def sign(self, params: dict, method: str = "POST", path: str = "") -> dict:
        """
        生成签名和请求头
        
        Args:
            params: 请求参数（body或query）
            method: HTTP方法
            path: 请求路径
        
        Returns:
            包含签名的请求头字典
        """
        timestamp = str(int(time.time() * 1000))
        nonce = str(uuid.uuid4()).replace("-", "")[:16]
        
        # Step 1: 参数排序
        sorted_params = OrderedDict(sorted(params.items()))
        
        # Step 2: 构造待签名字符串
        param_str = urlencode(sorted_params)
        sign_str = f"{method}\n{path}\n{param_str}\n{timestamp}\n{nonce}"
        
        # Step 3: HMAC-SHA256 签名
        signature = hmac.new(
            self.secret_key.encode('utf-8'),
            sign_str.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        return {
            "X-Api-Key": self.api_key,
            "X-Timestamp": timestamp,
            "X-Nonce": nonce,
            "X-Signature": signature,
            "Content-Type": "application/json"
        }
    
    def verify(self, params: dict, method: str, path: str,
               timestamp: str, nonce: str, signature: str,
               max_age_ms: int = 300000) -> bool:
        """
        验证签名（服务端逻辑）
        
        Args:
            max_age_ms: 签名最大有效期（默认5分钟）
        """
        # 检查时间戳有效期（防重放）
        now = int(time.time() * 1000)
        if abs(now - int(timestamp)) > max_age_ms:
            return False
        
        # 重新计算签名
        sorted_params = OrderedDict(sorted(params.items()))
        param_str = urlencode(sorted_params)
        sign_str = f"{method}\n{path}\n{param_str}\n{timestamp}\n{nonce}"
        
        expected = hmac.new(
            self.secret_key.encode('utf-8'),
            sign_str.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        # 使用 hmac.compare_digest 防止时序攻击
        return hmac.compare_digest(signature, expected)


# 使用示例
signer = ApiSigner(api_key="ak_test_001", secret_key="sk_xxxxxxxxxxxx")

# 客户端签名
params = {"stockCode": "600519", "price": "1800.00", "quantity": "100", "direction": "BUY"}
headers = signer.sign(params, method="POST", path="/api/v1/orders")
# headers 包含 X-Api-Key, X-Timestamp, X-Nonce, X-Signature
```

#### Java 工程实现

```java
import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;
import java.nio.charset.StandardCharsets;
import java.util.TreeMap;
import java.util.stream.Collectors;

public class ApiSigner {
    
    private final String apiKey;
    private final String secretKey;
    
    public ApiSigner(String apiKey, String secretKey) {
        this.apiKey = apiKey;
        this.secretKey = secretKey;
    }
    
    public String sign(Map<String, String> params, String method, String path,
                       String timestamp, String nonce) throws Exception {
        // 参数排序
        TreeMap<String, String> sorted = new TreeMap<>(params);
        String paramStr = sorted.entrySet().stream()
            .map(e -> e.getKey() + "=" + e.getValue())
            .collect(Collectors.joining("&"));
        
        // 构造待签名字符串
        String signStr = method + "\n" + path + "\n" + paramStr + "\n" + timestamp + "\n" + nonce;
        
        // HMAC-SHA256
        Mac mac = Mac.getInstance("HmacSHA256");
        mac.init(new SecretKeySpec(secretKey.getBytes(StandardCharsets.UTF_8), "HmacSHA256"));
        byte[] hash = mac.doFinal(signStr.getBytes(StandardCharsets.UTF_8));
        
        // 转十六进制
        StringBuilder sb = new StringBuilder();
        for (byte b : hash) {
            sb.append(String.format("%02x", b));
        }
        return sb.toString();
    }
}
```

### 测试点模板

| 编号 | 测试点 | 优先级 | 预期结果 |
|------|--------|--------|---------|
| TC-SG-001 | 使用正确的 secretKey 签名请求，验证签名通过 | P0 | 请求正常处理，返回 200 |
| TC-SG-002 | 篡改请求参数（修改 quantity）但不重新签名，验证签名校验失败 | P0 | 返回 401，提示"签名验证失败" |
| TC-SG-003 | 使用过期时间戳（>5分钟前），验证防重放机制 | P0 | 返回 401，提示"请求已过期" |
| TC-SG-004 | 使用错误的 secretKey 签名，验证身份校验 | P1 | 返回 401，提示"签名验证失败" |
| TC-SG-005 | 缺少 X-Signature 请求头，验证签名必填校验 | P1 | 返回 401，提示"缺少签名" |
| TC-SG-006 | 重复使用相同 nonce，验证防重放（nonce去重） | P2 | 返回 401，提示"请求已处理" |

---

## 4. 幂等键设计

### 定义

幂等键（Idempotency Key）确保同一请求被重复提交时，系统只执行一次业务操作。在网络不稳定的交易场景中，幂等性是防止重复下单、重复扣款的关键机制。

### 适用场景

- 委托下单（防止网络重试导致重复委托）
- 资金转账（防止重复扣款）
- 任何有副作用的写操作

### 券商业务幂等键方案

#### 设计原则

1. 幂等键由客户端生成，全局唯一
2. 服务端以幂等键为维度去重
3. 幂等键有效期（如24小时），过期后允许重用
4. 相同幂等键 + 不同参数 → 返回冲突错误

#### Python 工程实现

```python
import uuid
import time
import redis
import json
import hashlib

class IdempotencyManager:
    """幂等键管理器"""
    
    def __init__(self, redis_client: redis.Redis, ttl_seconds: int = 86400):
        self.redis = redis_client
        self.ttl = ttl_seconds  # 默认24小时
    
    def generate_key(self, account_id: str, action: str) -> str:
        """
        生成幂等键
        格式：{accountId}_{action}_{uuid}
        """
        return f"{account_id}_{action}_{uuid.uuid4().hex[:16]}"
    
    def check_and_lock(self, idempotency_key: str, request_hash: str) -> dict:
        """
        检查幂等键并加锁
        
        Returns:
            {"status": "new"} - 新请求，可以处理
            {"status": "duplicate", "response": {...}} - 重复请求，返回缓存结果
            {"status": "conflict"} - 相同key不同参数，冲突
        """
        cache_key = f"idempotency:{idempotency_key}"
        
        # 尝试获取已有记录
        existing = self.redis.get(cache_key)
        
        if existing is None:
            # 新请求：加锁（SET NX + TTL）
            locked = self.redis.set(
                cache_key,
                json.dumps({"request_hash": request_hash, "status": "processing"}),
                nx=True,
                ex=self.ttl
            )
            if locked:
                return {"status": "new"}
            else:
                # 并发竞争，重新检查
                existing = self.redis.get(cache_key)
        
        record = json.loads(existing)
        
        # 检查请求参数是否一致
        if record["request_hash"] != request_hash:
            return {"status": "conflict"}
        
        # 相同请求重复提交
        if record["status"] == "completed":
            return {"status": "duplicate", "response": record["response"]}
        
        # 正在处理中（前一个请求还没完成）
        return {"status": "processing"}
    
    def complete(self, idempotency_key: str, response: dict):
        """请求处理完成，缓存结果"""
        cache_key = f"idempotency:{idempotency_key}"
        existing = self.redis.get(cache_key)
        if existing:
            record = json.loads(existing)
            record["status"] = "completed"
            record["response"] = response
            self.redis.set(cache_key, json.dumps(record), ex=self.ttl)
    
    @staticmethod
    def hash_request(params: dict) -> str:
        """计算请求参数哈希"""
        sorted_str = json.dumps(params, sort_keys=True)
        return hashlib.sha256(sorted_str.encode()).hexdigest()


# 使用示例（在下单接口中）
def place_order(request):
    idempotency_key = request.headers.get("X-Idempotency-Key")
    if not idempotency_key:
        return {"code": 400, "message": "缺少幂等键"}
    
    manager = IdempotencyManager(redis_client)
    request_hash = manager.hash_request(request.json)
    
    result = manager.check_and_lock(idempotency_key, request_hash)
    
    if result["status"] == "duplicate":
        return result["response"]  # 返回缓存的响应
    elif result["status"] == "conflict":
        return {"code": 409, "message": "幂等键冲突：相同key不同参数"}
    elif result["status"] == "processing":
        return {"code": 409, "message": "请求处理中，请稍后查询"}
    
    # 新请求，执行业务逻辑
    try:
        order = execute_order(request.json)
        response = {"code": 0, "data": {"orderId": order.id}}
        manager.complete(idempotency_key, response)
        return response
    except Exception as e:
        return {"code": 500, "message": str(e)}
```

#### clientOrderId 设计建议

| 方案 | 格式 | 优点 | 缺点 |
|------|------|------|------|
| UUID | `550e8400-e29b-41d4-a716-446655440000` | 全局唯一，无冲突 | 无业务含义，不便排查 |
| 业务前缀+时间戳+序号 | `ORD_20260418_143000_001` | 可读性好，便于排查 | 需保证序号不重复 |
| 账户+时间戳+随机数 | `ACC001_1713430200000_a3f2` | 含账户信息，便于定位 | 长度较长 |

### 测试点模板

| 编号 | 测试点 | 优先级 | 预期结果 |
|------|--------|--------|---------|
| TC-IK-001 | 相同 clientOrderId + 相同参数重复提交，验证返回相同 orderId | P0 | 第二次返回与第一次相同的 orderId |
| TC-IK-002 | 相同 clientOrderId + 不同参数（如不同数量），验证返回冲突 | P0 | 返回 409，提示"幂等键冲突" |
| TC-IK-003 | 不传 clientOrderId，验证系统是否有默认幂等策略 | P1 | 每次生成新委托（无幂等保护）或返回400要求必填 |
| TC-IK-004 | 幂等键过期后（>24小时）重新使用相同key，验证允许 | P2 | 生成新委托，不与历史记录冲突 |

---

## 5. 错误码语义

### 定义

统一的错误码体系将错误按类别分组，每个错误码有明确的语义和处理建议。前端根据错误码展示对应提示，运维根据错误码定位问题。

### 适用场景

- 接口异常响应的分类处理
- 前端错误提示的国际化映射
- 监控告警的错误码分级
- 问题排查的快速定位

### 券商业务错误码体系

#### 错误码格式

```
错误码格式：XYYZZZ
  X   = 错误大类（1-业务错误, 2-系统错误, 3-权限错误, 4-限流错误）
  YY  = 模块编号（01-账户, 02-委托, 03-资金, 04-行情, 05-风控）
  ZZZ = 具体错误序号
```

#### 业务错误（1YYZZZ）

| 错误码 | 含义 | HTTP状态码 | 处理建议 |
|--------|------|-----------|---------|
| 102001 | 委托价格超出涨跌停限制 | 400 | 提示用户调整价格 |
| 102002 | 委托数量不符合规则（非整手） | 400 | 提示用户调整数量 |
| 102003 | 委托数量超过单笔上限 | 400 | 提示用户减少数量 |
| 102004 | 非交易时段不接受委托 | 400 | 提示当前时段和交易时间 |
| 102005 | 证券代码不存在或已退市 | 400 | 提示用户检查证券代码 |
| 102006 | 该证券当日停牌 | 400 | 提示停牌信息 |
| 103001 | 可用资金不足 | 400 | 提示可用余额和所需金额 |
| 103002 | 可用持仓不足（卖出） | 400 | 提示可用持仓数量 |
| 103003 | 银证转账金额超限 | 400 | 提示转账限额 |
| 105001 | 触发风控规则（集中度超限） | 400 | 提示风控规则详情 |
| 105002 | 账户被风控冻结 | 403 | 提示联系客服 |

#### 系统错误（2YYZZZ）

| 错误码 | 含义 | HTTP状态码 | 处理建议 |
|--------|------|-----------|---------|
| 200001 | 系统内部错误 | 500 | 重试或联系技术支持 |
| 200002 | 数据库连接异常 | 500 | 系统自动重试，告警运维 |
| 200003 | 报盘通道异常 | 500 | 检查交易所连接 |
| 200004 | 服务超时 | 504 | 查询委托状态，不要重复提交 |
| 200005 | 依赖服务不可用 | 503 | 等待服务恢复 |
| 204001 | 行情服务异常 | 500 | 使用缓存行情或提示稍后重试 |

#### 权限错误（3YYZZZ）

| 错误码 | 含义 | HTTP状态码 | 处理建议 |
|--------|------|-----------|---------|
| 300001 | 未登录或 token 过期 | 401 | 重新登录 |
| 300002 | 签名验证失败 | 401 | 检查签名算法和密钥 |
| 300003 | 无该接口访问权限 | 403 | 联系管理员开通权限 |
| 300004 | IP 不在白名单 | 403 | 添加 IP 到白名单 |
| 301001 | 非信用账户，不支持融资融券 | 403 | 开通信用账户 |
| 301002 | 未签署风险揭示书 | 403 | 引导签署协议 |

#### 限流错误（4YYZZZ）

| 错误码 | 含义 | HTTP状态码 | 处理建议 |
|--------|------|-----------|---------|
| 400001 | 接口调用频率超限 | 429 | 按 Retry-After 等待后重试 |
| 400002 | 单日委托次数超限 | 429 | 提示当日限额 |
| 400003 | 并发请求数超限 | 429 | 排队等待 |

### 测试点模板

| 编号 | 测试点 | 优先级 | 预期结果 |
|------|--------|--------|---------|
| TC-EC-001 | 可用资金不足时下单，验证返回错误码 103001 和明确提示 | P0 | code=103001, message 包含可用余额和所需金额 |
| TC-EC-002 | token 过期后请求，验证返回 300001 和 HTTP 401 | P0 | HTTP 401, code=300001, message="token已过期" |
| TC-EC-003 | 触发限流后验证返回 400001 和 Retry-After 头 | P1 | HTTP 429, code=400001, 包含 Retry-After |
| TC-EC-004 | 系统内部错误时验证不泄露堆栈信息 | P1 | code=200001, message 为通用提示，不含异常堆栈 |
| TC-EC-005 | 验证所有错误响应都包含 code 和 message 字段 | P2 | 任何非200响应都有统一的错误结构 |
