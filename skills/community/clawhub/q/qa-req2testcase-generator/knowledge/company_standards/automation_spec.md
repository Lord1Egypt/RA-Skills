# 自动化测试用例编写规范

> 文档编号：L3-AUT-001  
> 版本：v1.0  
> 生效日期：2026-04-18  
> 适用范围：全公司自动化测试用例的编写与维护

## 1. 目的

规范自动化测试用例的编写标准，确保用例可维护、可复用、执行稳定，降低自动化测试的维护成本。

## 2. 用例基本结构

每条自动化测试用例必须包含以下要素：

| 要素 | 必填 | 说明 |
|------|------|------|
| 元素定位方式 | 是 | 页面元素的定位策略和定位表达式 |
| 等待策略 | 是 | 元素加载/接口响应的等待方式 |
| 断言规则 | 是 | 验证点的断言方式和预期值 |
| 数据清理步骤 | 是 | 用例执行后的数据恢复/清理操作 |
| 前置数据准备 | 是 | 用例执行前的数据初始化 |
| 异常处理 | 是 | 执行失败时的截图/日志/恢复操作 |

## 3. 元素定位规范

### 3.1 定位方式优先级

按稳定性从高到低排列，优先使用高稳定性定位方式：

| 优先级 | 定位方式 | 稳定性 | 适用场景 |
|--------|----------|--------|----------|
| 1 | data-testid 属性 | ★★★★★ | 所有可控前端项目（推荐） |
| 2 | ID | ★★★★☆ | ID唯一且稳定的元素 |
| 3 | Name | ★★★☆☆ | 表单元素 |
| 4 | CSS Selector | ★★★☆☆ | 组合定位 |
| 5 | XPath（相对路径） | ★★☆☆☆ | 复杂层级关系 |
| 6 | XPath（绝对路径） | ★☆☆☆☆ | **禁止使用** |
| 7 | Link Text | ★★☆☆☆ | 仅用于超链接 |

### 3.2 定位方式代码示例

#### Selenium（Web端）

```python
from selenium.webdriver.common.by import By

# ✅ 推荐：data-testid 定位
login_btn = driver.find_element(By.CSS_SELECTOR, '[data-testid="login-submit"]')

# ✅ 推荐：ID 定位
username_input = driver.find_element(By.ID, 'username')

# ✅ 可用：CSS Selector 组合定位
order_row = driver.find_element(By.CSS_SELECTOR, '.order-table tr[data-order-id="12345"]')

# ✅ 可用：相对 XPath
confirm_dialog = driver.find_element(By.XPATH, '//div[@class="modal"]//button[text()="确认"]')

# ❌ 禁止：绝对 XPath
# bad = driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/form/button')

# ❌ 禁止：纯 class 名定位（易变）
# bad = driver.find_element(By.CLASS_NAME, 'btn-primary')
```

#### Appium（移动端）

```python
from appium.webdriver.common.appiumby import AppiumBy

# ✅ 推荐：accessibility id
login_btn = driver.find_element(AppiumBy.ACCESSIBILITY_ID, 'login_submit_button')

# ✅ 推荐：resource-id（Android）
username_input = driver.find_element(AppiumBy.ID, 'com.broker.app:id/et_username')

# ✅ 可用：iOS predicate
stock_cell = driver.find_element(AppiumBy.IOS_PREDICATE, 'name == "stock_600000" AND type == "XCUIElementTypeCell"')

# ✅ 可用：Android UIAutomator
scroll_to = driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
    'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().text("更多"))')

# ❌ 禁止：坐标定位
# bad = TouchAction(driver).tap(x=200, y=500).perform()
```

### 3.3 定位表达式管理

1. 所有定位表达式必须集中管理在 Page Object 的常量中，禁止在测试方法中硬编码
2. 定位表达式变更时只需修改 Page Object，不影响测试逻辑

```python
# ✅ Page Object 模式
class LoginPage:
    """登录页面对象"""
    # 定位器集中定义
    USERNAME_INPUT = (By.CSS_SELECTOR, '[data-testid="login-username"]')
    PASSWORD_INPUT = (By.CSS_SELECTOR, '[data-testid="login-password"]')
    SUBMIT_BTN = (By.CSS_SELECTOR, '[data-testid="login-submit"]')
    ERROR_MSG = (By.CSS_SELECTOR, '[data-testid="login-error-message"]')
    
    def __init__(self, driver):
        self.driver = driver
    
    def login(self, username: str, password: str):
        self.driver.find_element(*self.USERNAME_INPUT).send_keys(username)
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)
        self.driver.find_element(*self.SUBMIT_BTN).click()
    
    def get_error_message(self) -> str:
        return self.driver.find_element(*self.ERROR_MSG).text
```

## 4. 等待策略规范

### 4.1 等待方式优先级

| 优先级 | 等待方式 | 说明 | 适用场景 |
|--------|----------|------|----------|
| 1 | 显式等待（Expected Conditions） | 等待特定条件满足 | **所有场景首选** |
| 2 | 自定义等待条件 | 自定义轮询逻辑 | 复杂业务条件 |
| 3 | 隐式等待 | 全局等待 | 仅作为兜底，不可替代显式等待 |
| 4 | 强制等待（sleep） | 固定时间等待 | **禁止使用** |

### 4.2 等待策略代码示例

```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ✅ 推荐：显式等待 - 元素可见
wait = WebDriverWait(driver, timeout=10, poll_frequency=0.5)
element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="order-result"]')))

# ✅ 推荐：显式等待 - 元素可点击
submit_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="submit"]')))

# ✅ 推荐：显式等待 - 文本包含
wait.until(EC.text_to_be_present_in_element(
    (By.CSS_SELECTOR, '[data-testid="order-status"]'), '已成交'
))

# ✅ 可用：自定义等待条件（等待接口返回特定状态）
def order_completed(driver):
    """自定义等待条件：订单完成"""
    status_el = driver.find_element(By.CSS_SELECTOR, '[data-testid="order-status"]')
    return status_el.text in ['已成交', '已撤单', '已拒绝']

wait.until(order_completed)

# ❌ 禁止：强制等待
# import time
# time.sleep(5)  # 绝对禁止
```

### 4.3 超时配置

| 场景 | 默认超时 | 最大超时 | 轮询间隔 |
|------|----------|----------|----------|
| 页面元素加载 | 10秒 | 30秒 | 0.5秒 |
| 接口响应 | 15秒 | 60秒 | 1秒 |
| 文件下载 | 30秒 | 120秒 | 2秒 |
| 异步任务完成 | 30秒 | 300秒 | 5秒 |

超时时间必须通过配置文件管理，禁止硬编码：

```python
# config/timeout.yaml
timeout:
  element_load: 10
  api_response: 15
  file_download: 30
  async_task: 30
  poll_interval: 0.5
```

## 5. 断言规则

### 5.1 断言原则

1. 每条用例至少包含一个断言
2. 断言必须验证业务结果，不仅验证页面元素存在
3. 断言信息必须包含有意义的失败描述
4. 多个验证点使用软断言（Soft Assert），避免第一个失败后跳过后续验证

### 5.2 断言代码示例

```python
import pytest
from assertpy import assert_that

# ✅ 推荐：明确的断言消息
def test_order_submit():
    """验证限价委托提交成功"""
    order_page.submit_limit_order(stock='600000', price=10.50, qty=100)
    
    # 断言1：委托状态
    status = order_page.get_order_status()
    assert status == '已报', f'委托状态预期为"已报"，实际为"{status}"'
    
    # 断言2：委托数量
    actual_qty = order_page.get_order_quantity()
    assert actual_qty == 100, f'委托数量预期为100，实际为{actual_qty}'
    
    # 断言3：委托价格（浮点数比较使用精度）
    actual_price = order_page.get_order_price()
    assert abs(actual_price - 10.50) < 0.001, f'委托价格预期为10.50，实际为{actual_price}'

# ✅ 推荐：软断言（收集所有失败）
def test_account_info():
    """验证账户信息展示"""
    from pytest_check import check
    
    info = account_page.get_account_info()
    
    with check:
        assert info['name'] == '张**', f'姓名脱敏显示错误: {info["name"]}'
    with check:
        assert info['phone'] == '138****5678', f'手机号脱敏显示错误: {info["phone"]}'
    with check:
        assert info['id_card'] == '310***********1234', f'身份证脱敏显示错误: {info["id_card"]}'

# ✅ 推荐：接口断言
def test_api_transfer():
    """验证转账接口响应"""
    response = api.post('/transfer', json={'amount': 10000, 'target': '90000001'})
    
    assert_that(response.status_code).is_equal_to(200)
    assert_that(response.json()).has_code(0)
    assert_that(response.json()['data']['status']).is_equal_to('SUCCESS')
    assert_that(response.json()['data']['amount']).is_close_to(10000, tolerance=0.01)
```

### 5.3 禁止的断言方式

```python
# ❌ 禁止：无断言消息
# assert result == True

# ❌ 禁止：仅断言元素存在，不验证内容
# assert order_status_element is not None

# ❌ 禁止：断言写在 try-except 中被吞掉
# try:
#     assert result == expected
# except AssertionError:
#     pass
```

## 6. 数据清理步骤

### 6.1 清理原则

1. 每条用例执行后必须恢复到执行前的状态
2. 清理操作放在 `teardown` / `finally` 中，确保即使用例失败也能执行
3. 清理操作使用独立的数据库连接或API调用，不依赖UI操作

### 6.2 清理代码示例

```python
import pytest

class TestOrderSubmit:
    """委托下单测试"""
    
    created_orders = []  # 记录创建的订单用于清理
    
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self, db_connection):
        """前置准备和后置清理"""
        # === Setup ===
        self.db = db_connection
        # 准备测试账户余额
        self.db.execute(
            "UPDATE fund_account SET balance = 1000000 WHERE account_id = '90000001'"
        )
        self.db.commit()
        
        yield  # 执行测试用例
        
        # === Teardown ===
        # 清理创建的委托
        for order_id in self.created_orders:
            try:
                api.delete(f'/orders/{order_id}')
            except Exception as e:
                logger.warning(f'清理委托 {order_id} 失败: {e}')
        self.created_orders.clear()
        
        # 恢复账户余额
        self.db.execute(
            "UPDATE fund_account SET balance = 1000000 WHERE account_id = '90000001'"
        )
        self.db.commit()
    
    def test_limit_order(self):
        order_id = order_page.submit_limit_order('600000', 10.50, 100)
        self.created_orders.append(order_id)  # 记录以便清理
        assert order_page.get_order_status() == '已报'
```

## 7. 禁止硬编码

### 7.1 禁止硬编码的内容

| 类别 | 错误示例 | 正确做法 |
|------|----------|----------|
| 测试数据 | `username = "testuser01"` | 从配置文件或数据工厂读取 |
| 环境地址 | `url = "http://192.168.1.100:8080"` | 从环境配置读取 |
| 等待时间 | `time.sleep(5)` | 使用显式等待 + 配置化超时 |
| 数据库连接 | `host = "10.0.0.1"` | 从环境变量或配置中心读取 |
| 文件路径 | `path = "/home/test/data.csv"` | 使用相对路径或配置 |
| 验证码 | `code = "123456"` | 使用Mock服务或万能验证码配置 |

### 7.2 配置管理示例

```python
# config/env_config.yaml
environments:
  sit:
    base_url: "http://sit-trade.internal:8080"
    db_host: "sit-db.internal"
    db_port: 3306
    db_name: "trade_sit"
  uat:
    base_url: "http://uat-trade.internal:8080"
    db_host: "uat-db.internal"
    db_port: 3306
    db_name: "trade_uat"

# config/test_data.yaml
test_accounts:
  normal_user:
    fund_account: "90000001"
    password: "${ENCRYPTED_PASSWORD}"
    phone: "13000000001"
  admin_user:
    fund_account: "90000002"
    password: "${ENCRYPTED_PASSWORD}"
    phone: "13000000002"
```

```python
# 配置读取工具
import yaml
import os

class Config:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            env = os.getenv('TEST_ENV', 'sit')
            with open('config/env_config.yaml', 'r') as f:
                all_config = yaml.safe_load(f)
            cls._instance.env_config = all_config['environments'][env]
            with open('config/test_data.yaml', 'r') as f:
                cls._instance.test_data = yaml.safe_load(f)
        return cls._instance
    
    @property
    def base_url(self):
        return self.env_config['base_url']
```

## 8. 用例独立性

### 8.1 独立性要求

1. 每条用例可独立执行，不依赖其他用例的执行顺序
2. 每条用例执行前后状态一致（幂等性）
3. 并行执行时不产生数据冲突
4. 用例失败不影响其他用例执行

### 8.2 实现方式

```python
# ✅ 推荐：每条用例使用独立的测试数据
@pytest.fixture
def unique_test_account(db):
    """为每条用例创建独立的测试账户"""
    import uuid
    account_id = f"9{uuid.uuid4().hex[:7]}"  # 测试账号段
    db.execute(
        "INSERT INTO fund_account (account_id, balance) VALUES (%s, %s)",
        (account_id, 1000000)
    )
    db.commit()
    yield account_id
    # 清理
    db.execute("DELETE FROM fund_account WHERE account_id = %s", (account_id,))
    db.commit()

def test_buy_order(unique_test_account):
    """使用独立账户，不与其他用例冲突"""
    order_page.login(unique_test_account)
    order_page.submit_order(...)
```

### 8.3 禁止的依赖模式

```python
# ❌ 禁止：用例间数据依赖
class TestOrderFlow:
    order_id = None  # 共享状态
    
    def test_01_create_order(self):
        TestOrderFlow.order_id = create_order()  # 后续用例依赖此ID
    
    def test_02_cancel_order(self):
        cancel_order(TestOrderFlow.order_id)  # 如果01失败，02必然失败
```

## 9. 用例命名规范

### 9.1 命名格式

```
test_{模块}_{功能}_{场景}_{预期结果}
```

### 9.2 命名示例

| 用例名称 | 说明 |
|----------|------|
| `test_order_limit_buy_success` | 委托模块-限价买入-成功 |
| `test_order_limit_buy_insufficient_balance` | 委托模块-限价买入-余额不足 |
| `test_transfer_large_amount_dual_review` | 转账模块-大额-双人复核 |
| `test_login_wrong_password_lock` | 登录模块-密码错误-锁定 |
| `test_account_close_with_position_rejected` | 销户模块-有持仓-拒绝 |

### 9.3 命名规则

1. 全部使用小写字母和下划线
2. 以 `test_` 开头（pytest要求）
3. 模块名使用业务缩写（order/transfer/login/account）
4. 场景描述简洁明了，不超过5个单词
5. 预期结果放在最后（success/fail/rejected/locked）

## 10. 测试点模板

### 10.1 Web UI 自动化测试点模板

| 测试点 | 定位方式 | 等待策略 | 操作 | 断言 | 数据清理 |
|--------|----------|----------|------|------|----------|
| 登录成功 | `[data-testid="login-submit"]` | `EC.element_to_be_clickable` | 输入账号密码并点击登录 | `assert current_url CONTAINS '/dashboard'` | 退出登录 |
| 委托下单 | `[data-testid="order-submit"]` | `EC.visibility_of_element_located` | 填写委托参数并提交 | `assert order_status == '已报'` | 撤销委托 + 恢复余额 |
| 持仓查询 | `[data-testid="position-table"]` | `EC.presence_of_all_elements_located` | 进入持仓页面 | `assert len(positions) > 0 && positions[0].qty > 0` | 无需清理 |

### 10.2 接口自动化测试点模板

| 测试点 | 接口 | 请求方式 | 等待策略 | 断言 | 数据清理 |
|--------|------|----------|----------|------|----------|
| 下单接口 | `/api/v1/orders` | POST | 响应超时15s | `status_code == 200 && data.orderId != null` | `DELETE /api/v1/orders/{id}` |
| 查询持仓 | `/api/v1/positions` | GET | 响应超时10s | `status_code == 200 && data.length >= 0` | 无需清理 |
| 转账接口 | `/api/v1/transfers` | POST | 异步轮询30s | `status == 'COMPLETED' && amount == expected` | 反向转账恢复余额 |

## 11. 附则

- 新编写的自动化用例必须通过代码评审（Code Review）后方可合入主分支。
- 自动化用例的稳定性指标：连续3次执行通过率 ≥ 98%，低于此标准的用例须优化或标记为不稳定。
- 本规范每季度审查一次，根据框架升级和实践反馈修订。


## 12. AI 用例生成 automation_score 与本规范的映射关系

> 本节说明 P6 Prompt 输出的 `automation_score` 6维评分与公司自动化规范的对应关系，供 RAG 召回时建立语义关联。

### 12.1 评分维度映射表

| P6 评分维度 | 字段名 | 对应本规范章节 | 说明 |
|------------|--------|--------------|------|
| 稳定性 | stability | §3 元素定位规范、§4 等待策略 | 元素定位稳定（data-testid）→ stability 高分；频繁变更的 xpath → 低分 |
| 可重复性 | repeatability | §6 数据清理规范 | 有完整数据清理方案 → repeatability 高分；依赖脏数据 → 低分 |
| 数据可控 | data_control | §7 测试数据管理 | 数据可程序化构造（工厂函数/fixture）→ 高分；依赖人工造数 → 低分 |
| 步骤明确 | step_clarity | §5 断言规范、§10 测试点模板 | 步骤和断言无歧义、可直接转化为代码 → 高分；需人工判断 → 低分 |
| 执行频率 | frequency | §2 自动化范围 | 回归测试/冒烟测试 → 高分；一次性验证 → 低分 |
| 人工成本 | manual_cost | §2 自动化范围 | 手工执行耗时长、重复性高 → 高分；简单点击验证 → 低分 |

### 12.2 评分结果与自动化实施的对应关系

| automation_score.total | is_automatable | 本规范建议 |
|----------------------|----------------|-----------|
| ≥ 20 | true | 纳入自动化计划，按本规范 §3~§9 编写脚本 |
| 15~19 | 建议评估 | 评估投入产出比，优先考虑接口自动化（成本低于 UI） |
| < 15 | false | 保持手工执行，不强制自动化 |

### 12.3 使用说明

- `automation_score` 由 P6 Prompt 在生成用例时自动计算，**不需要测试人员手动填写**
- 评分结果仅作为自动化优先级参考，最终是否自动化由测试负责人决定
- 当 `is_automatable=true` 时，可参考本规范 §10 的测试点模板直接编写自动化脚本
