"""
pytest-test-master: pytest 专项技能核心库
提供 fixtures、mock、parametrize、coverage、测试数据生成的最佳实践
"""

import sys
import os
from typing import Dict, List, Any, Optional

# ============================
# Fixtures 内容库
# ============================

FIXTURES_CONTENT: Dict[str, Dict[str, str]] = {
    "scope": {
        "title": "Fixture Scope 四种级别",
        "概念": (
            "scope 控制 fixture 的生命周期和复用范围。"
            "选错 scope 会导致测试间相互影响或性能下降。"
        ),
        "何时用": (
            "- function（默认）：每个测试独立，适合需要干净状态的场景\n"
            "- class：同一类的测试共享客户端/浏览器，setup 代价高时用\n"
            "- module：模块级别一次，适合大重量资源（数据库连接池）\n"
            "- session：整个测试进程一次，适合全局配置、全局监控"
        ),
        "示例": '''import pytest

# function（默认）：每个测试函数独立
@pytest.fixture
def user_token():
    token = generate_token()
    return token  # 每个测试收到新的 token

# class：类中所有测试共享同一实例
@pytest.fixture(scope="class")
def browser():
    from selenium import webdriver
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

class TestUserFlow:
    def test_login(self, browser):      # 同 browser 实例
        browser.get("/login")
    def test_profile(self, browser):    # 同 browser 实例
        browser.get("/profile")

# module：模块内所有测试共享
@pytest.fixture(scope="module")
def app():
    app = create_app()
    return app

# session：整个测试进程只创建一次
@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine("postgresql://...")
    return engine
''',
        "避坑": (
            "- class-scope fixture 在类间共享时注意状态污染\n"
            "- session-scope fixture 不是线程安全的（多进程请用 pytest-xdist）\n"
            "- fixture 间有依赖时，子 fixture 不能比父 fixture 的 scope 大"
        ),
        "进阶": "scope=\"session\" + autouse=True 可做全局日志初始化，但别放需要干净状态的东西",
    },

    "yield": {
        "title": "yield_fixture vs setup/teardown",
        "概念": (
            "pytest 推荐用 yield 替代传统的 setup/teardown。yield 之前是 setup，"
            "之后是 teardown。测试函数抛出异常时，yield 后的代码仍会执行。"
        ),
        "何时用": (
            "- 需要在测试后清理资源（关闭文件、断开连接、回滚事务）\n"
            "- 需要在测试后验证状态（检查日志、计数、副作用）\n"
            "- 需要测试失败时也执行清理（避免污染下一个测试）"
        ),
        "示例": '''import pytest

# 推荐：yield 风格
@pytest.fixture
def temp_dir(tmp_path):
    # setup: 创建目录
    d = tmp_path / "sub"
    d.mkdir()
    # 测试代码在这里执行（由 pytest 传入）
    yield str(d)
    # teardown: 清理（无论测试是否成功）
    # d 被 tmp_path 自动清理，这里仅为演示

@pytest.fixture
def db_transaction(db_conn):
    """测试后自动回滚，不污染数据库"""
    db_conn.begin()
    yield db_conn
    db_conn.rollback()  # 测试结束回滚所有变更

def test_create_order(db_transaction):
    db_transaction.execute("INSERT INTO orders ...")
    assert order_created(db_transaction)

# 旧风格（不推荐）：try-finally
@pytest.fixture
def legacy_cleanup():
    setup()
    try:
        yield
    finally:
        cleanup()  # 效果同 yield fixture，但更冗长
''',
        "避坑": (
            "- yield 后抛出异常也会执行清理代码（这是优点）\n"
            "- fixture 的 yield 只能有一个（不是多个）\n"
            "- 如果 fixture 不 yield，等同于 scope=\"function\" 且无 teardown"
        ),
        "进阶": "request.addfinalizer(fn) 效果类似 yield，但可注册多个回调，yield 更简洁",
    },

    "params": {
        "title": "参数化 Fixture",
        "概念": (
            "@pytest.fixture(params=[...]) 让一个 fixture 被多个测试用例复用，"
            "每个参数值都会驱动一次测试，类似 parametrize 但作用于 fixture 级别。"
        ),
        "何时用": (
            "- 同一个测试逻辑需要针对多组数据进行验证\n"
            "- 需要测试多个 DB 驱动、多个 API 版本、多个配置\n"
            "- 减少重复 fixture 定义，统一管理测试数据"
        ),
        "示例": '''import pytest

# 参数化 fixture：为每个参数生成独立测试
@pytest.fixture(params=[1, 2, 3])
def worker_count(request):
    return request.param

def test_parallel_processing(worker_count):
    result = run_workers(worker_count)
    assert result >= 0

# 运行结果：3 个测试（worker_count=1/2/3 各一次）

# 进阶：params + scope 控制生成次数
@pytest.fixture(params=[
    {"driver": "chrome", "headless": True},
    {"driver": "firefox", "headless": False},
    {"driver": "safari", "headless": True},
], scope="module")
def browser_config(request):
    return request.param

class TestBrowsers:
    def test_homepage(self, browser_config):
        driver = init_driver(**browser_config)
        assert driver.title
        driver.quit()

# 组合：fixture params + parametrize 产生笛卡尔积
@pytest.fixture(params=["v1", "v2"], scope="module")
def api_version(request):
    return request.param

@pytest.fixture(params=["en", "zh"], scope="module")
def locale(request):
    return request.param
''',
        "避坑": (
            "- params 的 scope 默认是 function（每个测试都重新生成）\n"
            "- 想跨测试复用需设 scope=\"module\"，但要注意测试隔离\n"
            "- params 大时测试数指数增长，用 mark.parametrize 替代更清晰"
        ),
        "进阶": "request.getfixturevalue(name) 可以在 fixture 内动态获取其他 fixture",
    },

    "autouse": {
        "title": "autouse 自动执行 Fixture",
        "概念": (
            "autouse=True 的 fixture 不需要显式声明，pytest 自动为所有测试执行。"
            "适合全局初始化、日志开关、性能测量等横切关注点。"
        ),
        "何时用": (
            "- 开启/关闭日志、调试模式\n"
            "- 记录每个测试的执行时间\n"
            "- 自动创建测试所需的全局资源（但要谨慎状态污染）\n"
            "- 为所有测试注入相同上下文"
        ),
        "示例": '''import pytest
import time

# 自动计时：每个测试自动打印耗时
@pytest.fixture(autouse=True)
def timer():
    start = time.time()
    yield
    print(f"  [耗时: {time.time() - start:.3f}s]")

# 自动设置测试环境
@pytest.fixture(autouse=True)
def clean_env(monkeypatch):
    """每个测试前清理环境变量，避免相互干扰"""
    monkeypatch.setenv("TESTING", "1")

# 自动启用日志（只在测试函数上生效）
@pytest.fixture(autouse=True, scope="function")
def verbose_logging():
    import logging
    logging.basicConfig(level=logging.DEBUG)
    yield
    logging.getLogger().setLevel(logging.INFO)

# class-scope autouse：只在该类中自动执行
class TestAPI:
    @pytest.fixture(autouse=True)
    def reset_api_key(self, api_key):
        api_key.reset()  # 每个类开始时重置
        yield

# 谨慎：autouse=True 会影响所有测试，滥用导致难以定位问题
''',
        "避坑": (
            "- 全局 autouse=True 谨慎使用，影响所有测试难调试\n"
            "- 优先显式声明 fixture，只有横切关注点才用 autouse\n"
            "- class 级别 autouse 比 session 级别更安全"
        ),
        "进阶": "scope='session' + autouse=True 可做全局初始化，但要确保测试隔离",
    },

    "request": {
        "title": "request 内置 Fixture",
        "概念": (
            "request 是 pytest 内置 fixture，提供测试上下文信息。"
            "通过 request你可以访问测试节点、参数、配置等。"
        ),
        "何时用": (
            "- 在 fixture 内访问测试函数的名称、节点 ID\n"
            "- 根据测试参数动态调整 fixture 行为\n"
            "- 在测试报告中添加自定义信息"
        ),
        "示例": '''import pytest

# request.node：访问测试节点信息
@pytest.fixture
def test_info(request):
    print(f"运行测试: {request.node.name}")
    print(f"节点 ID: {request.node.nodeid}")
    return {
        "name": request.node.name,
        "file": request.node.fspath,
        "markers": [mark.name for mark in request.node.iter_markers()],
    }

def test_example(test_info):
    assert "example" in test_info["name"]

# request.param：获取 parametrize 参数
@pytest.fixture(params=["alice", "bob"])
def username(request):
    return request.param

# request.config：访问 pytest 配置
@pytest.fixture
def base_url(request):
    return request.config.getoption("--base-url")

def test_api(base_url):
    assert base_url.startswith("http")

# 命令行加 --base-url=https://api.example.com

# request.getfixturevalue：动态获取 fixture
@pytest.fixture
def dynamic_db(request):
    db_type = request.config.getoption("--db")
    return request.getfixturevalue(f"db_{db_type}")
''',
        "避坑": (
            "- request.node.iter_markers() 能遍历所有标记\n"
            "- request.config.getoption() 需要在 pytest.ini 注册选项\n"
            "- request.getfixturevalue 只在 fixture 内可用，不能跨文件"
        ),
        "进阶": "pytest.Report 基类提供更详细的报告信息，可自定义报告钩子",
    },

    "teardown": {
        "title": "Teardown 最佳实践",
        "概念": (
            "teardown（清理）保证测试不污染环境。pytest 中主要用 yield "
            "和 request.addfinalizer 两种方式。正确清理是测试可靠性的基石。"
        ),
        "何时用": (
            "- 测试产生临时文件/目录\n"
            "- 测试修改了全局状态（环境变量、配置）\n"
            "- 测试创建了数据库记录需要回滚\n"
            "- 测试打开了文件/网络连接"
        ),
        "示例": '''import pytest
import shutil

# 方式一：yield（推荐）
@pytest.fixture
def temp_workspace(tmp_path):
    ws = tmp_path / "workspace"
    ws.mkdir()
    yield ws
    # 自动清理（tmp_path 自动管理）
    shutil.rmtree(ws, ignore_errors=True)

# 方式二：addfinalizer（yield 不可用时，如静态方法）
@pytest.fixture(scope="class")
def app_server(request):
    server = start_server()
    request.addfinalizer(server.stop)  # 多清理函数
    request.addfinalizer(cleanup_logs)
    return server

# 方式三：try-finally（等价于 yield）
@pytest.fixture
def legacy_cleanup():
    setup_resources()
    try:
        yield setup_result
    finally:
        cleanup_resources()

# 数据库回滚
@pytest.fixture
def transactional_test(db, phonebook):
    """每个测试在事务中运行，测试后回滚"""
    db.begin(isolation_level="SERIALIZABLE")
    yield
    db.rollback()
    # 自动清理所有插入的数据

# 文件系统清理
@pytest.fixture
def generated_files(tmp_path):
    files = []
    yield files
    for f in files:
        f.unlink(missing_ok=True)
''',
        "避坑": (
            "- 清理失败（异常）会导致后续测试失败，用 try-except 包裹\n"
            "- tmp_path 是 pytest 内置 fixture，自带清理，优先使用\n"
            "- 多线程/多进程场景下 fixture teardown 可能有竞争"
        ),
        "进阶": "pytest 的 pytest_runtest_teardown 钩子可对所有测试统一做 teardown",
    },

    "session": {
        "title": "Session-Scope Fixture 跨文件共享",
        "概念": (
            "session scope 的 fixture 在整个测试进程只执行一次，"
            "可跨模块/跨文件共享，适合重量级一次性资源。"
        ),
        "何时用": (
            "- Selenium WebDriver（启动一次浏览器，所有测试复用）\n"
            "- 数据库连接池（整个进程共用一个连接）\n"
            "- 外部服务 mock（只启动一次 mock 服务器）\n"
            "- 全局配置加载（只读一次）"
        ),
        "示例": '''# conftest.py：定义 session-scope fixture
import pytest

# conftest.py（session scope 放这里）
@pytest.fixture(scope="session")
def browser():
    """所有测试共享一个浏览器实例"""
    from selenium import webdriver
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

# test_module_a.py
def test_login(browser):
    browser.get("/login")

# test_module_b.py（同样可以用 browser fixture）
def test_dashboard(browser):
    browser.get("/dashboard")

# 注意：browser 是 session 级别，所以所有测试在同一个浏览器中运行
# 需要独立浏览器时，不要用 session scope

# 跨文件共享数据库 fixture
# conftest.py
@pytest.fixture(scope="session")
def db_engine():
    from sqlalchemy import create_engine
    engine = create_engine("postgresql://test:test@localhost/testdb")
    return engine

@pytest.fixture(scope="session")
def db_connection(db_engine):
    conn = db_engine.connect()
    yield conn
    conn.close()

# test_schema.py / test_crud.py 都可以用 db_connection
''',
        "避坑": (
            "- session-scope fixture 在不同进程中不共享（pytest-xdist）\n"
            "- 测试间会相互影响（状态污染），确保测试结束后清理共享状态\n"
            "- session fixture 出错，整个测试进程终止"
        ),
        "进阶": "pytest-xdist 的 --dist=loadscope 按模块分组，每个组内共享 session fixture",
    },

    "inject": {
        "title": "Fixture 依赖注入模式",
        "概念": (
            "pytest 的 fixture 就是依赖注入容器。fixture 可以依赖其他 fixture，"
            "pytest 自动按依赖顺序解析，生成干净、可组合的测试资源。"
        ),
        "何时用": (
            "- 复杂的测试资源构建链（DB → Schema → Sample Data）\n"
            "- 不同测试需要不同组合的底层资源\n"
            "- 统一管理资源生命周期"
        ),
        "示例": '''import pytest

# 层级依赖：pytest 自动解析顺序
@pytest.fixture
def db_engine():
    """底层资源"""
    return create_engine("sqlite:///:memory:")

@pytest.fixture
def db_session(db_engine):
    """中层：依赖 db_engine"""
    session = db_engine.get_session()
    yield session
    session.close()

@pytest.fixture
def sample_data(db_session):
    """高层：依赖 db_session"""
    db_session.execute("INSERT INTO users ...")
    return db_session.query(User).all()

# 测试：只需要最上层 fixture
def test_user_count(sample_data):
    assert len(sample_data) > 0

# 参数组合：不同测试需要不同配置
@pytest.fixture
def app_config():
    return {"debug": True, "version": "v1"}

@pytest.fixture
def app(app_config):
    return create_app(app_config)

@pytest.fixture
def client(app):
    return app.test_client()

def test_homepage(client):
    assert client.get("/").status_code == 200
''',
        "避坑": (
            "- 避免循环依赖（fixture A → fixture B → fixture A）\n"
            "- fixture 参数过多说明设计有问题，考虑重构\n"
            "- 深层依赖链会影响性能，考虑合并或加 scope"
        ),
        "进阶": "conftest.py 中定义基础 fixture，子模块 fixture 继承扩展",
    },
}


# ============================
# Mock 内容库
# ============================

MOCK_CONTENT: Dict[str, Dict[str, str]] = {
    "patch": {
        "title": "@patch 装饰器和 patch 上下文管理器",
        "概念": (
            "@patch 是 unittest.mock 的核心，用于替换真实对象。"
            "装饰器从内到外执行（栈），上下文管理器更直观。"
        ),
        "何时用": (
            "- 替换外部 API、数据库、文件系统等 I/O 操作\n"
            "- 模拟不存在的对象或第三方库\n"
            "- 隔离被测代码，强制特定返回值"
        ),
        "示例": '''from unittest.mock import patch, MagicMock
import pytest

# 方式一：@patch 装饰器（从上往下参数对应）
@patch("myapp.service.requests.get")
@patch("myapp.service.validate_token")
def test_fetch_user(mock_validate, mock_get):
    mock_validate.return_value = True
    mock_get.return_value = MagicMock(
        status_code=200,
        json=lambda: {"id": 1, "name": "Alice"}
    )
    result = fetch_user(1)
    assert result["name"] == "Alice"
    mock_get.assert_called_once_with(
        "https://api.example.com/users/1"
    )

# 方式二：patch 上下文管理器（更直观）
def test_create_order():
    with patch("myapp.service.requests.post") as mock_post:
        mock_post.return_value = MagicMock(status_code=201)
        result = create_order({"product_id": 1, "qty": 2})
        assert result["status"] == "created"

# 方式三：patch.object（替换对象属性）
def test_with_specific_object():
    obj = SomeClass()
    with patch.object(obj, "send_notification", return_value=True):
        result = obj.do_work()
        assert result is not None

# target 路径是关键：必须是被测代码中实际引用的路径
# ✅ @patch("myapp.service.requests.get")  ← 被测模块中的引用路径
# ❌ @patch("requests.get")                 ← requests 内部路径，无效
''',
        "避坑": (
            "- target 路径写错会导致 mock 失效，产生假通过\n"
            "- 装饰器顺序从内到外执行，要确保路径正确\n"
            "- mock.return_value 是静态值，想要动态值用 side_effect"
        ),
        "进阶": "side_effect 可以是函数、异常或可迭代对象，比 return_value 灵活",
    },

    "mock_obj": {
        "title": "MagicMock / PropertyMock / Mock",
        "概念": (
            "Mock 是 mock 的核心类，MagicMock 自动生成属性和方法，"
            "PropertyMock 用于 mock property，Mock 更精确控制行为。"
        ),
        "何时用": (
            "- MagicMock：需要模拟任意对象的方法/属性，自动生成\n"
            "- PropertyMock：mock @property 装饰的属性\n"
            "- Mock：需要精确断言调用参数、次数、顺序"
        ),
        "示例": '''from unittest.mock import Mock, MagicMock, PropertyMock, call

# MagicMock：自动创建不存在的属性
mock_obj = MagicMock()
mock_obj.anything()  # 自动创建，返回 MagicMock
mock_obj.anything.return_value = 42
assert mock_obj.anything() == 42

# Mock：带规格的模拟对象
class User:
    def __init__(self, name):
        self.name = name
    def greet(self):
        return f"Hello, {self.name}"

mock_user = Mock(spec=User)
mock_user.name = "Alice"
mock_user.greet.return_value = "Hi Alice"
assert mock_user.greet() == "Hi Alice"
mock_user.greet.assert_called_once()  # 断言调用过

# PropertyMock：mock @property
with patch("mymodule.User.email", new_callable=PropertyMock) as mock_email:
    mock_email.return_value = "alice@example.com"
    assert User.email == "alice@example.com"

# side_effect：动态行为
def dynamic_response(*args, **kwargs):
    if args[0] > 10:
        return "big"
    return "small"

mock_fn = Mock(side_effect=dynamic_response)
assert mock_fn(5) == "small"
assert mock_fn(15) == "big"

# side_effect：抛出异常
mock_fail = Mock(side_effect=ValueError("invalid"))
with pytest.raises(ValueError):
    mock_fail()
''',
        "避坑": (
            "- MagicMock 自动创建属性，容易掩盖测试不真实的问题\n"
            "- spec=User 只允许 User 真实存在的属性/方法被调用\n"
            "- side_effect 是函数时，调用时传的是真实参数"
        ),
        "进阶": "Mock 配合 assert_called_once_with / assert_has_calls / mock.call_args_list 精确验证",
    },

    "assert_calls": {
        "title": "断言 Mock 调用次数和参数",
        "概念": (
            "mock 对象会记录所有调用记录，通过 assert_called_once_with、"
            "assert_has_calls、call_count 等验证调用是否符合预期。"
        ),
        "何时用": (
            "- 验证函数调用次数（防止漏调用/多调用）\n"
            "- 验证调用参数内容（参数值、关键字参数）\n"
            "- 验证调用顺序（多步操作的前后依赖）"
        ),
        "示例": '''from unittest.mock import Mock, call

mock_logger = Mock()

def process_order(order_id):
    mock_logger.info(f"Order {order_id} received")
    mock_logger.info(f"Processing order {order_id}")
    mock_logger.info(f"Order {order_id} completed")

# 验证调用次数
process_order(1)
assert mock_logger.info.call_count == 3
mock_logger.info.assert_called_thrice()  # 等价

# 验证最后一次调用参数
mock_logger.info.assert_called_with("Order 1 completed")

# 验证调用顺序
expected_calls = [
    call.info("Order 1 received"),
    call.info("Processing order 1"),
    call.info("Order 1 completed"),
]
mock_logger.assert_has_calls(expected_calls)

# 验证多对象调用
mock_db = Mock()
mock_cache = Mock()

def get_user(uid):
    user = mock_cache.get(f"user:{uid}")
    if not user:
        user = mock_db.query("SELECT * FROM users WHERE id=?", uid)
        mock_cache.set(f"user:{uid}", user)
    return user

get_user(1)
mock_cache.get.assert_called_once()
mock_db.query.assert_called_once()
mock_cache.set.assert_called_once()
''',
        "避坑": (
            "- assert_called_once_with 会在有多次调用时报错，明确多次调用用 assert_called\n"
            "- call_args_list 是元组列表，(args, kwargs)，检查时用 call() 对象\n"
            "- 多线程场景下 call_count 可能不准确"
        ),
        "进阶": "mock_calls 记录包括方法调用链，unittest.mock.call 可以链式调用",
    },

    "freeze": {
        "title": "freeze_time 时间冻结",
        "概念": (
            "pytest-freezegun 通过 monkeypatch 控制 datetime.now() 等时间相关函数，"
            "让时间相关测试可重复、可断言。"
        ),
        "何时用": (
            "- 测试时间戳生成、过期判断、缓存过期\n"
            "- 测试定时任务、批处理逻辑\n"
            "- 需要固定「当前时间」但代码用的是 datetime.now()"
        ),
        "示例": '''import pytest
from freezegun import freeze_time

# 冻结到固定时间点
@freeze_time("2024-06-01 12:00:00")
def test_token_expiry():
    token = create_token()
    assert token.expires_at == "2024-06-01 12:00:00"  # 固定不变

# 冻结时间 + 推进
@freeze_time("2024-01-01 00:00:00")
def test_cache_expire_after_one_day():
    cache = Cache(ttl=86400)
    cache.set("key", "value")
    # 冻结到 1 天后
    with freeze_time("2024-01-02 00:00:01"):
        assert cache.get("key") is None  # 已过期

# fixture 中使用 freeze（更灵活）
@pytest.fixture
def frozen_time():
    with freeze_time("2024-01-01 12:00:00") as frozen:
        yield frozen  # frozen.time 是 freezegun API

def test_scheduled_task(frozen_time):
    frozen_time.tick(delta=timedelta(hours=2))
    # 时间推进了 2 小时
    run_scheduled_task()
    # 验证任务是否执行

# pytest-freezegun 插件方式（pytest_freezegun_apply）
# pytest.ini: addopts = --freeze-time=2024-01-01
''',
        "避坑": (
            "- freeze_time 只冻结 datetime，其他时间库（如 time.time）需额外处理\n"
            "- 嵌套 freeze_time 行为取决于 freezegun 版本，查看文档\n"
            "- fixture freeze 需要正确 yield，确保时区恢复"
        ),
        "进阶": "freezegun 的 tick() 和 move_to() 控制时间推进，配合 pytest-repeat 可测试周期任务",
    },

    "spy": {
        "title": "Spy 模式：保留真实行为 + 记录调用",
        "概念": (
            "spy 在 mock 的基础上保留了原始对象的所有真实行为，"
            "同时记录调用信息。适合想部分 mock 又不想完全替换的场景。"
        ),
        "何时用": (
            "- 想知道某个方法被调用了，但还希望它执行真实逻辑\n"
            "- mock 某个依赖，但想验证它和其他组件的真实交互\n"
            "- 增量测试：逐步引入 mock，而非一次性全部替换"
        ),
        "示例": '''from unittest.mock import patch, MagicMock

# 方式一：wrap 模式（Spy）
real_object = SomeService()

with patch.object(
    SomeService, "send_email",
    wraps=real_object.send_email  # 保留真实行为
) as mocked_send:
    result = real_object.send_email("alice@example.com")
    # 真实发送了邮件（如果配置了真实 SMTP）
    # 同时记录了调用
    mocked_send.assert_called_once_with("alice@example.com")

# 方式二：Spy + 部分替换
class MockedCache:
    def __init__(self):
        self._cache = {}

    def get(self, key):
        """Spy 模式：真实读取 + 记录 miss"""
        if key not in self._cache:
            cache_misses.append(key)  # 记录但真实处理
        return self._cache.get(key)

    def set(self, key, value):
        self._cache[key] = value

# 方式三：pytest-mock 的 spy
from pytest_mock import MockerFixture

def test_spy_example(mocker: MockerFixture):
    spy = mocker.spy(RealClass, "real_method")
    obj = RealClass()
    obj.real_method(42)
    spy.assert_called_once_with(42)
    # 同时执行了真实逻辑（如果有副作用会真实发生）
''',
        "避坑": (
            "- spy 的真实方法会真的执行，可能有副作用（发邮件、写 DB）\n"
            "- wrap 模式下返回真实值，但无法指定特定返回值\n"
            "- spy 主要用于验证，测试隔离要求高时用纯 mock"
        ),
        "进阶": "MockerFixture.spy() 是 pytest-mock 的高级功能，比 wrap 更简洁",
    },

    "scope_mock": {
        "title": "Mock Scope：session/class/function",
        "概念": (
            "mock fixture 也有 scope。与其每次测试都重新 patch，"
            "可以在更高 scope 复用 mock 对象，减少 patch 开销。"
        ),
        "何时用": (
            "- 复杂的 mock 对象（大量 set_side_effect）需要复用\n"
            "- mock 初始化代价高（连接 mock 服务器）\n"
            "- 想验证 class 或 module 级别的调用总数"
        ),
        "示例": '''import pytest
from unittest.mock import Mock

# function scope（默认）：每个测试独立
@pytest.fixture
def mock_api():
    with patch("myapp.api_client.requests") as mock:
        mock.get.return_value = Mock(json=lambda: {"data": "ok"})
        yield mock

def test_one(mock_api): ...
def test_two(mock_api): ...  # 每个测试有独立的 mock_api

# class scope：类内共享同一个 mock
@pytest.fixture(scope="class")
def mock_db_class(request):
    mock = Mock()
    request.cls.db = mock  # 挂到类上
    return mock

class TestDB:
    def test_insert(self, mock_db_class): ...
    def test_delete(self, mock_db_class): ...  # 同一个 mock_db_class

# session scope：整个进程复用（配合 pytest-xdist 要小心）
@pytest.fixture(scope="session")
def mock_external_service():
    with patch("app.services.external.API") as mock:
        mock.return_value.health_check.return_value = True
        yield mock

# 注意：session mock 的 assert 记录是累积的
def test_api_1(mock_external_service): ...
def test_api_2(mock_external_service): ...
# mock_external_service.call_count == 两次总和
''',
        "避坑": (
            "- session/class scope mock 的调用记录是累积的，assert 要注意\n"
            "- 跨测试共享 mock 可能导致状态污染，mock 要设计为无状态的\n"
            "- fixture 级别的 mock 用 pytest-mock 的 mocker fixture 更简洁"
        ),
        "进阶": "session-scope mock 在 pytest-xdist 多进程下每个 worker 独立，共享不变",
    },

    "common": {
        "title": "Mock 常见错误和修复",
        "概念": (
            "mock 有很多坑：target 路径写错、mock 时机不对、"
            "忘记 reset、side_effect 与 return_value 冲突等。"
        ),
        "何时用": "当你遇到 mock 不生效、假通过、测试挂掉等问题时参考",
        "示例": '''# 错误1：target 路径写错（最常见）
# ❌ 错误
@patch("requests.get")  # requests 内部路径
def test_wrong(mock_get):
    # requests.get 被 mock，但你的代码用的是 myapp.requests.get
    ...

# ✅ 正确
@patch("myapp.service.requests.get")  # 被测代码的引用路径

# 错误2：side_effect 和 return_value 冲突
# ❌ 错误
mock_fn = Mock(return_value=1, side_effect=[2, 3])
# side_effect 优先级更高，return_value 被忽略
# 第一次调用返回 2，第二次返回 3

# ✅ 正确：只用其一
mock_fn = Mock(side_effect=[2, 3])  # 列表按序返回
mock_fn = Mock(return_value=1)       # 固定返回

# 错误3：mock 了但忘记调用原始方法（对 spy 的误解）
# ❌
with patch("mymodule.func"):
    result = mymodule.func()  # func 被 mock 成 MagicMock，不执行真实逻辑

# ✅ 要执行真实逻辑用 wraps
with patch("mymodule.func", wraps=real_func):
    result = mymodule.func()  # 执行真实逻辑

# 错误4：没有 reset mock，测试间相互影响
def test_bad(mock_api):
    mock_api.get.return_value = Mock(data="A")
    ...

def test_next(mock_api):
    # ❌ 继承了上一个测试的 return_value
    mock_api.get.return_value.json()  # 可能还是 "A"

# ✅ 每测试明确 reset
def test_good(mock_api):
    mock_api.reset_mock()  # 清理调用记录和返回值
    mock_api.get.return_value = Mock(data="B")
    ...

# 错误5：异步代码用同步 mock
# ❌
@patch("aiohttp.get")
def test_async_bad(mock_get):
    result = await fetch()  # aiohttp 不支持这种方式

# ✅ 异步 mock 用 AsyncMock
from unittest.mock import AsyncMock
mock_get = AsyncMock(return_value=Mock(data="ok"))
''',
        "避坑": (
            "- target 永远是「被测代码」中的引用路径，不是「被引用库」的路径\n"
            "- side_effect 可以是异常：side_effect=ValueError('err')\n"
            "- asyncio 代码用 pytest-asyncio + AsyncMock，不要混用同步 mock"
        ),
        "进阶": "mock 是手段不是目的，测试应该验证行为而非实现细节，过度 mock 反而降低测试价值",
    },
}


# ============================
# Parametrize 内容库
# ============================

PARAMETRIZE_CONTENT: Dict[str, Dict[str, str]] = {
    "basic": {
        "title": "@pytest.mark.parametrize 基础用法",
        "概念": (
            "parametrize 是 pytest 最强大的功能之一，用少量代码"
            "生成大量测试用例，每个参数组合对应一个独立测试。"
        ),
        "何时用": (
            "- 同一个测试逻辑需要多组输入/输出验证\n"
            "- 边界值测试（空值、零值、最大值）\n"
            "- 多语言/多地区/多配置场景"
        ),
        "示例": '''import pytest

# 基础：单参数
@pytest.mark.parametrize("username", ["alice", "bob", "charlie"])
def test_username_valid(username):
    assert len(username) >= 3

# 多参数：笛卡尔积
@pytest.mark.parametrize("x", [1, 2])
@pytest.mark.parametrize("y", [10, 20])
def test_pairs(x, y):
    # 运行 2*2=4 次：x=1,y=10 / x=1,y=20 / x=2,y=10 / x=2,y=20
    assert x * y >= 10

# 显式指定多参数
@pytest.mark.parametrize("a, b, expected", [
    (1, 2, 3),
    (0, 0, 0),
    (-1, 1, 0),
    (100, 200, 300),
])
def test_add(a, b, expected):
    assert a + b == expected

# 字符串参数
@pytest.mark.parametrize("status", [
    "pending", "paid", "shipped", "delivered"
])
def test_order_status(status):
    assert status in ["pending", "paid", "shipped", "delivered", "cancelled"]
''',
        "避坑": (
            "- 多装饰器叠加是笛卡尔积，不是并行，是总组合数\n"
            "- 避免参数组合爆炸（10 参数各 10 值 = 10^10 个测试）\n"
            "- 参数为空列表会导致测试被跳过"
        ),
        "进阶": "ids 参数可以给每个测试起人类可读的名字",
    },

    "ids": {
        "title": "自定义测试 ID（ids）",
        "概念": (
            "ids 参数给每个参数组合一个可读的名字，"
            "方便在测试报告中快速定位问题，也是文档的一部分。"
        ),
        "何时用": (
            "- 参数是复杂对象，需要人类可读名字\n"
            "- 参数值本身不好看懂（如编码、特殊符号）\n"
            "- 想让测试报告更友好"
        ),
        "示例": '''import pytest

# 自动 ids：pytest 用 str() 转成名字（可能不友好）
@pytest.mark.parametrize("user", [
    {"name": "Alice", "age": 25},
    {"name": "Bob", "age": 0},  # 边界值
])
def test_user_age(user):
    assert user["age"] >= 1

# 手动 ids（推荐）：列表推导或显式列表
@pytest.mark.parametrize("x, y", [
    (1, 2),
    (0, 0),
    (-1, -1),
    (999, 1000),
], ids=["positive", "zero", "both_negative", "large"])
def test_divide(x, y):
    if y == 0:
        pytest.skip("skip zero")
    assert x / y >= 0

# ids 函数：动态生成
def make_ids(params):
    return [f"input_{p}" for p in params]

@pytest.mark.parametrize("value", [1, 2, 3], ids=make_ids)
def test_value(value):
    assert value > 0

# 复杂参数 + ids
@pytest.mark.parametrize("a, b", [
    ((1, 2), (3, 4)),
    ((0, 0), (0, 0)),
    ((-1, -2), (1, 2)),
], ids=["normal_pair", "zero_pair", "negative_pair"])
def test_pair_sum(a, b):
    assert sum(a) + sum(b) == a[0] + a[1] + b[0] + b[1]
''',
        "避坑": (
            "- ids 列表长度必须和参数列表长度完全一致\n"
            "- ids 中不能有特殊字符（pytest 会自动处理）\n"
            "- 动态生成 ids 时注意不要产生重复名字"
        ),
        "进阶": "pytest-param-recorder 插件可以将测试 ID 和实际参数存入报告",
    },

    "indirect": {
        "title": "间接参数化（indirect）",
        "概念": (
            "indirect=True 让 parametrize 的参数传给 fixture，"
            "而不是直接传给测试函数，实现更灵活的数据处理。"
        ),
        "何时用": (
            "- 需要在测试前处理参数（转换格式、查 DB）\n"
            "- 同一参数要驱动多个 fixture\n"
            "- 参数是标识符，需要解析成真实对象"
        ),
        "示例": '''import pytest

# indirect：参数先传给 fixture，fixture 返回处理后的值
@pytest.fixture
def db_row(request):
    """根据 user_id 参数从 DB 查数据"""
    user_id = request.param
    return {"id": user_id, "name": f"User{user_id}"}

@pytest.mark.parametrize("db_row", [1, 2, 3], indirect=True)
def test_user_exists(db_row):
    # db_row 是 fixture 返回的处理后数据
    assert db_row["id"] in [1, 2, 3]

# 实际例子：测试多数据库驱动
@pytest.fixture
def db_connection(request):
    db_type = request.param
    if db_type == "mysql":
        return MySQLConnection()
    elif db_type == "pg":
        return PostgreSQLConnection()
    elif db_type == "sqlite":
        return SQLiteConnection()

@pytest.mark.parametrize("db_connection", ["mysql", "pg", "sqlite"], indirect=True)
def test_connectivity(db_connection):
    assert db_connection.ping()

# indirect + 多个 fixture
@pytest.fixture
def api_endpoint(request):
    return {"base": request.param["base"], "version": request.param["ver"]}

@pytest.fixture
def api_headers(request):
    return {"Authorization": f"Bearer {request.param['token']}"}

@pytest.mark.parametrize("api_endpoint, api_headers", [
    ({"base": "/v1", "ver": "1"}, {"token": "abc"}),
    ({"base": "/v2", "ver": "2"}, {"token": "xyz"}),
], indirect=True)
def test_api_request(api_endpoint, api_headers):
    assert "/v" in api_endpoint["base"]
    assert len(api_headers["Authorization"]) > 10
''',
        "避坑": (
            "- indirect=True 时，测试函数参数名必须和 fixture 名一致\n"
            "- 被 parametrize 间接传参的 fixture 会自动被 indirect 调用\n"
            "- indirect 不支持跨模块 fixture（fixture 必须在 conftest.py 或同文件）"
        ),
        "进阶": "pytest-lazy-fixture 可以在 parametrize 中直接引用 fixture 名",
    },

    "combine": {
        "title": "多个 @parametrize 组合",
        "概念": (
            "同一测试函数可以叠加多个 @pytest.mark.parametrize，"
            "效果是笛卡尔积（所有组合）。也可用 scope 控制组合范围。"
        ),
        "何时用": (
            "- 需要覆盖多个维度的组合（操作系统 × Python 版本 × DB）\n"
            "- 某些组合有特殊处理，其他是通用逻辑\n"
            "- 想把参数按维度拆分方便维护"
        ),
        "示例": '''import pytest

# 叠加：笛卡尔积（4*2=8 个测试）
@pytest.mark.parametrize("env", ["dev", "staging", "prod", "local"])
@pytest.mark.parametrize("format", ["json", "xml"])
def test_api_response(env, format):
    # 8 个组合
    ...

# 组合条件：某些参数组合需要 skip
@pytest.mark.parametrize("username", ["alice", "bob", ""])
@pytest.mark.parametrize("role", ["admin", "user"])
def test_permission(username, role):
    if username == "" and role == "admin":
        pytest.skip("空用户不能是管理员")
    if username == "alice" and role == "admin":
        assert has_admin_permission(username)
    else:
        assert not has_admin_permission(username)

# 自定义组合：用 product 显式控制
import itertools

configs = list(itertools.product(
    ["dev", "prod"],          # 环境
    ["en", "zh", "ja"],        # 语言
    [True, False],            # debug 模式
))
# 2*3*2=12 个配置

@pytest.mark.parametrize("env, lang, debug", configs)
def test_i18n_config(env, lang, debug):
    ...

# 用 pytest-cases 高级组合
# from pytest_cases import parametrize, cartesian
# @cartesian(env=["dev","prod"], lang=["en","zh"])
''',
        "避坑": (
            "- 笛卡尔积增长很快，用 mark.skip 跳过无效组合\n"
            "- itertools.product 比多层装饰器更清晰\n"
            "- 组合多时用 @pytest.mark.parametrize(ids=...) 给测试起名"
        ),
        "进阶": "pytest-param 插件支持更灵活的参数组合和过滤",
    },

    "generate": {
        "title": "动态生成参数",
        "概念": (
            "参数不一定是硬编码列表，可以从文件、DB、"
            "配置文件、代码生成动态参数列表。"
        ),
        "何时用": (
            "- 参数来自外部配置（CSV、YAML、JSON）\n"
            "- 边界值需要程序生成（极大值、极小值、边界+1）\n"
            "- 想把测试数据与测试代码分离"
        ),
        "示例": '''import pytest
import json

# 从文件加载参数
def load_test_cases():
    with open("test_data/cases.json") as f:
        return json.load(f)

@pytest.mark.parametrize("case", load_test_cases())
def test_from_file(case):
    assert validate(case["input"]) == case["expected"]

# 动态生成边界值
def boundary_values():
    """生成数值边界测试数据"""
    values = []
    for v in [0, 1, 127, 128, 255, 256, 32767, 32768]:
        values.append((v, v-1, v+1))
    return values

@pytest.mark.parametrize("value, below, above", boundary_values())
def test_boundary(value, below, above):
    assert value >= 0
    assert below < value
    assert above > value

# 用 pytest_generate_tests 自定义参数生成钩子
def pytest_generate_tests(metafunc):
    if "browser" in metafunc.fixturenames:
        metafunc.parametrize("browser", ["chrome", "firefox", "safari"])

# 参数化 + skipif：有条件跳过
@pytest.mark.parametrize("test_input,expected", [
    (1, 1),
    (2, 2),
    pytest.param(3, 3, marks=pytest.mark.skipif(True, reason="已知 bug")),
])
def test_cases(test_input, expected):
    assert test_input == expected
''',
        "避坑": (
            "- 动态生成函数在收集阶段执行，不要在其中有副作用\n"
            "- 用 pytest_generate_tests 可以自定义 scope，但不如装饰器直观\n"
            "- 生成大量参数时注意测试执行时间"
        ),
        "进阶": "pytest-param 插件支持将参数存储在外部文件并支持版本控制",
    },

    "product": {
        "title": "笛卡尔积参数化",
        "概念": (
            "多个 parametrize 叠加产生笛卡尔积，是覆盖全组合的利器。"
            "当维度多、每个维度值少时最有效。"
        ),
        "何时用": (
            "- API 测试：多版本 × 多端 × 多语言\n"
            "- 兼容性测试：Python × OS × 依赖版本\n"
            "- 配置组合：DB × Cache × 日志级别"
        ),
        "示例": '''import pytest
from itertools import product

# 显式笛卡尔积
configs = list(product(
    ["v1", "v2", "v3"],          # API 版本
    ["android", "ios", "web"],   # 客户端
    ["en", "zh", "ja", "ko"],    # 语言
    [True, False],               # debug 模式
    # 3*3*4*2 = 72 个组合
))

@pytest.mark.parametrize("version, client, lang, debug", configs)
def test_api_compatibility(version, client, lang, debug):
    ...

# 稀疏网格：只测重要组合
critical_combos = [
    ("v1", "android", "en", True),
    ("v2", "android", "en", True),
    ("v2", "ios", "zh", False),
    ("v3", "web", "en", False),
]

@pytest.mark.parametrize("version, client, lang, debug", critical_combos)
def test_critical_paths(version, client, lang, debug):
    ...

# 辅助函数：生成全组合 + ID
def generate_matrix(**dimensions):
    names = list(dimensions.keys())
    values = list(product(*dimensions.values()))
    ids = ["_".join(str(v) for v in row) for row in values]
    return names, values, ids

names, values, ids = generate_matrix(
    version=["v1", "v2"],
    client=["android", "ios"],
    auth=["token", "cookie"],
)
# [(("v1","android","token"), "v1_android_token"), ...]
params = [pytest.param(*v, id=i) for v, i in zip(values, ids)]

@pytest.mark.parametrize("version,client,auth", params)
def test_matrix(version, client, auth):
    ...
''',
        "避坑": (
            "- 全笛卡尔积在大矩阵下测试数爆炸，用稀疏网格或关键路径\n"
            "- ids 可以长到不可读，截断或用缩写\n"
            "- 参数为空会跳过整个测试"
        ),
        "进阶": "pytest-harvest 可统计笛卡尔积下各分支的覆盖率",
    },
}


# ============================
# Coverage 内容库
# ============================

COVERAGE_CONTENT: Dict[str, Dict[str, str]] = {
    "report": {
        "title": "coverage report 阅读指南",
        "概念": (
            "pytest-cov 集成 coverage.py，生成测试覆盖报告。"
            "关键指标：覆盖率百分比、缺失行、未覆盖文件。"
        ),
        "何时用": (
            "- 想了解哪些代码没有被测试覆盖\n"
            "- 想量化测试的完整性\n"
            "- 想找测试盲区"
        ),
        "示例": '''# 运行覆盖率测试
pytest --cov=myapp --cov-report=term tests/

# 输出示例
# Name                    Stmts   Miss  Cover
# -----------------------------------------------
# myapp/__init__.py           10      0   100%
# myapp/models.py             45      5    89%
# myapp/views.py              80     20    75%
# myapp/services.py          30     30     0%
# -----------------------------------------------
# TOTAL                     165     55    67%

# 字段说明：
# Stmts: 总语句数
# Miss: 未执行的语句数
# Cover: 覆盖率 = (Stmts - Miss) / Stmts

# 聚焦看某个模块
pytest --cov=myapp.services --cov-report=term tests/

# 只显示覆盖 < 80% 的模块
pytest --cov=myapp --cov-report="term-missing:skip-covered" tests/

# 关键：看 Missing 列（具体哪行没覆盖）
# 在 report 输出中找 ">>>>>>" 标记的行
''',
        "避坑": (
            "- 100% 覆盖不等于高质量测试，只保证每行执行了\n"
            "- Miss 可能是：异常处理分支、日志行、死代码\n"
            "- 外部库默认被排除，用 --cov-config 包含"
        ),
        "进阶": "coverage run + coverage combine 可以合并多次运行的报告",
    },

    "html": {
        "title": "HTML 覆盖率报告",
        "概念": (
            "HTML 报告是分析覆盖率最重要的工具，可以逐文件、逐行查看覆盖情况，"
            "红色标记未覆盖行，是重构和补充测试的直接指引。"
        ),
        "何时用": (
            "- 详细分析某个文件的覆盖细节\n"
            "- 给团队展示测试质量\n"
            "- 追踪测试改进效果"
        ),
        "示例": '''# 生成 HTML 报告
pytest --cov=myapp --cov-report=html tests/

# 打开报告（在浏览器）
# open htmlcov/index.html  # macOS
# xdg-open htmlcov/index.html  # Linux

# 自定义报告路径
pytest --cov=myapp --cov-report=html:coverage_html tests/

# CI 中生成 HTML + 上传（GitHub Actions）
# .github/workflows/test.yml
# - name: Run tests with coverage
#   run: pytest --cov=myapp --cov-report=xml --cov-report=html tests/
# - name: Upload coverage to Codecov
#   uses: codecov/codecov-action@v3
#   with:
#     files: ./coverage.xml

# 排除特定文件
# .coveragerc
# [run]
# omit =
#     */tests/*
#     */migrations/*
#     */__pycache__/*
#     */venv/*
''',
        "避坑": (
            "- HTML 报告文件大（每个源文件一个 HTML），不要提交到 git\n"
            "- .gitignore 加一行 htmlcov/\n"
            "- HTML 报告只能在有浏览器的环境打开，CI 中用 XML + badge"
        ),
        "进阶": "coverage html --title='MyApp Coverage Report v1.0' 加版本标记",
    },

    "xml": {
        "title": "XML 报告与 CI 集成",
        "概念": (
            "coverage.xml 是 CI 系统（GitHub Actions、Jenkins）读取覆盖率的标准格式，"
            "支持 Coverage Badges、覆盖率门控、趋势图。"
        ),
        "何时用": (
            "- GitHub Actions 集成覆盖率检查\n"
            "- 设置覆盖率阈值门控（不达标不允许合并）\n"
            "- Codecov/Coveralls 等覆盖率平台集成"
        ),
        "示例": '''# 生成 XML 报告
pytest --cov=myapp --cov-report=xml tests/

# GitHub Actions 示例
# .github/workflows/test.yml
name: Test
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install pytest pytest-cov
      - run: pytest --cov=myapp --cov-report=xml tests/
      - uses: codecov/codecov-action@v4
        with:
          files: ./coverage.xml
          fail_ci_if_error: true  # 覆盖率低则 CI 失败

# 设置覆盖率阈值（失败门控）
# pytest.ini 或 pyproject.toml
# [tool.coverage.report]
# fail_under = 80  # 低于 80% 测试失败

# 或在命令行
pytest --cov=myapp --cov-fail-under=80 tests/
''',
        "避坑": (
            "- XML 路径用相对路径，CI job 目录结构要一致\n"
            "- fail_under 是在报告生成后检查，可以和 --cov-report=xml 共存\n"
            "- 首次集成时阈值要合理，避免阻断正常开发"
        ),
        "进阶": "codecov.yml 可以配置覆盖率比较基准（对比 main 分支）",
    },

    "threshold": {
        "title": "覆盖率阈值设置",
        "概念": (
            "覆盖率阈值（fail_under）是 CI 门控的核心工具。"
            "设置太低没意义，太高会导致正常代码无法提交。"
        ),
        "何时用": (
            "- 想强制保持测试质量（防止测试退化）\n"
            "- 想量化新功能的测试要求\n"
            "- 想给团队设测试覆盖率 KPI"
        ),
        "示例": '''# pyproject.toml 配置
[tool.coverage.report]
# 整体阈值
fail_under = 75

# 按文件差异化阈值
[tool.coverage.report]
fail_under = 60
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
    "pass",
]

# 只检查核心业务逻辑
[tool.coverage.report]
omit = [
    "*/tests/*",
    "*/migrations/*",
    "*/admin.py",
]
fail_under = 80

# 函数/分支覆盖双阈值
[tool.coverage.run]
branch = true  # 开启分支覆盖

[tool.coverage.report]
fail_under = 70
precision = 2  # 小数点后 2 位

# 分支覆盖率特别低说明测试分支覆盖不全
# Name                   Stmts   Miss  Branch   BrPart  Cover
# myapp/logic.py            20      0       8        4    80%
# BrPart=4 表示有 4 个分支完全没测到
''',
        "避坑": (
            "- 不要盲目追求 100%，优先保证核心路径\n"
            "- branch 覆盖开启后会降低百分比（因为分母变大）\n"
            "- fail_under 是四舍五入的整数"
        ),
        "进阶": "增量覆盖率（coverage compare）可以只检查本次 PR 改动的覆盖率",
    },

    "exclude": {
        "title": "排除文件和代码行",
        "概念": (
            "不是所有代码都需要 100% 覆盖。"
            "用 exclude 过滤不需要测试的代码（migrations、config、generated）。"
        ),
        "何时用": (
            "- 测试文件、migrations、generated 代码不需要覆盖\n"
            "- 特定平台代码无法测试（if sys.platform != 'linux'）\n"
            "- 调试代码、demo 代码不需要测试"
        ),
        "示例": '''# .coveragerc 配置排除
[run]
omit =
    */tests/*
    */test_*
    */migrations/*
    */__pycache__/*
    */venv/*
    */site-packages/*
    */admin.py
    */urls.py
    settings*.py

[report]
# 排除特定行（行内注释）
exclude_lines =
    pragma: no cover        # 标记本行不计入覆盖
    def __repr__           # 快捷方法不强制要求
    if self.debug:         # 调试分支
    if TYPE_CHECKING:      # 类型检查分支
    raise NotImplementedError
    ...                   # 三点表示后续代码被跳过

# 代码中手动标记
def complex_function(x):
    if x > 0:
        return positive_handler(x)  # pragma: no cover
        # 这行被标记，上下文代码也视为未覆盖
    return default_handler(x)

# 按条件排除整个文件
# myapp/config.py 顶部加:
# if TYPE_CHECKING:
#     from .types import Config  # pragma: no cover
''',
        "避坑": (
            "- 排除太多会让覆盖率数字失真，有选择性地排除\n"
            "- pragma: no cover 只能排除单行，其后代码需要单独标记\n"
            "- 排除的业务代码应该加上注释说明原因"
        ),
        "进阶": "coverage erase 清除旧报告，coverage combine 合并多次运行结果",
    },

    "debug": {
        "title": "覆盖率调试技巧",
        "概念": (
            "当覆盖率异常（明明执行了却显示未覆盖、路径找不到）时，"
            "用 debug 命令定位根因。"
        ),
        "何时用": (
            "- 发现报告和实际执行不符\n"
            "- 某些文件/行始终不出现在报告中\n"
            "- pytest-cov 配置了但没生效"
        ),
        "示例": '''# 1. 检查 coverage 配置是否生效
coverage debug config
# 看 [run] 和 [report] 部分是否正确

# 2. 检查哪些文件被 tracking
coverage debug data | grep "no source"
# 看是否有文件找不到源码

# 3. 数据文件损坏时重建
coverage erase
pytest --cov=myapp tests/
coverage combine

# 4. 查看某个文件的具体覆盖行
coverage report --show-missing myapp/views.py
# 输出类似：
# myapp/views.py  80%  10 missing lines at lines: 12, 23, 45-52

# 5. 进程外（subprocess）覆盖收集
# 如果测试 spawn 了子进程，需要单独收集子进程覆盖
# pytest.ini
# addopts = --cov=myapp --cov-branch --cov-report=term
# 在 conftest.py
# import coverage
# cov = coverage.process_poolCoverage()

# 6. 动态修改收集范围
# conftest.py
def pytest_configure(config):
    coverage.process_startup()
''',
        "避坑": (
            "- pytest-cov 必须在收集阶段就注册，否则晚于测试运行\n"
            "- subprocess 的覆盖需要 coverage.process_startup() 钩子\n"
            "- .coverage 文件损坏时必须 coverage erase 重建"
        ),
        "进阶": "coverage debug sys 看 Python 路径，排查模块找不到问题",
    },
}


# ============================
# 测试数据内容库
# ============================

DATA_CONTENT: Dict[str, Dict[str, str]] = {
    "faker": {
        "title": "Faker.py 测试数据生成",
        "概念": (
            "Faker 是 Python 最流行的假数据生成库，"
            "支持姓名、地址、公司、信用卡等 100+ 域，自带本地化支持。"
        ),
        "何时用": (
            "- 需要真实感的测试数据（姓名、地址、邮箱）\n"
            "- 需要多种语言/地区数据\n"
            "- 需要大量随机但结构正确的数据"
        ),
        "示例": '''from faker import Faker

fake = Faker("zh_CN")  # 中文本地化

# 基础用法
fake.name()       # "张伟"
fake.email()      # "zhangwei@example.com"
fake.phone_number()  # "13812345678"
fake.address()    # "北京市朝阳区建国路1号"
fake.date()       # "2024-01-15"
fake.time()       # "14:30:00"
fake.datetime()   # "2024-01-15 14:30:00"

# 复合数据
fake.profile()    # 完整用户档案
fake.company()    # 公司名 "北京某某科技有限公司"
fake.job()        # 职位 "软件工程师"

# 数值
fake.random_int(1, 100)       # 随机整数
fake.random_float(2, 0, 100)  # 随机浮点数（小数位）
fake.pydecimal(2, 2)          # 精确Decimal（适合金额）

# 多语言支持
fake_en = Faker("en_US")
fake_jp = Faker("ja_JP")
fake_multi = Faker(["zh_CN", "en_US", "ja_JP"])

# 在 fixture 中使用
import pytest
from faker import Faker

@pytest.fixture
def fake_data():
    f = Faker("zh_CN")
    return {
        "name": f.name(),
        "email": f.email(),
        "phone": f.phone_number(),
        "address": f.address(),
        "company": f.company(),
        "job": f.job(),
    }

def test_user_creation(fake_data):
    user = create_user(**fake_data)
    assert user.email == fake_data["email"]
''',
        "避坑": (
            "- Faker 默认每次调用结果不同，想复现用 seed()\n"
            "- 中文数据不如英文丰富，某些场景英文 Faker 效果更好\n"
            "- 生产环境不要用 Faker 生成的数据（有隐私泄露风险）"
        ),
        "进阶": "Faker 的 providers 可以自定义，factory_boy 底层就是 Faker",
    },

    "factory": {
        "title": "factory_boy 工厂模式",
        "概念": (
            "factory_boy 是 Django/ORM 测试的标配，用类定义数据模板，"
            "支持关联对象、懒评估、序列生成，比 Faker 更结构化。"
        ),
        "何时用": (
            "- Django/Flask/SQLAlchemy 模型测试\n"
            "- 需要创建关联对象（ForeignKey、ManyToMany）\n"
            "- 需要可复用、可覆盖的测试数据工厂"
        ),
        "示例": '''import factory
import factory.fuzzy
from myapp.models import User, Order

# 定义用户工厂
class UserFactory(factory.Factory):
    class Meta:
        model = User

    id = factory.Sequence(lambda n: n + 1)
    name = factory.Faker("name", locale="zh_CN")
    email = factory.LazyAttribute(lambda obj: f"{obj.name}@example.com")
    age = factory.fuzzy.FuzzyInteger(18, 80)
    is_active = True

# 定义订单工厂（关联用户）
class OrderFactory(factory.Factory):
    class Meta:
        model = Order

    id = factory.Sequence(lambda n: n + 1)
    user = factory.SubFactory(UserFactory)  # 自动创建关联 User
    amount = factory.fuzzy.FuzzyDecimal(10.0, 5000.0)
    status = factory.fuzzy.FuzzyChoice(["pending", "paid", "shipped"])

# 使用工厂
def test_order_creation():
    order = OrderFactory()
    assert order.user is not None  # user 自动创建
    assert order.user.name  # 有真实姓名

# 在 fixture 中使用
@pytest.fixture
def user(db):
    return UserFactory()

@pytest.fixture
def orders(db, user):
    return OrderFactory.create_batch(5, user=user)  # 创建 5 个订单

def test_user_orders(orders, user):
    assert len(orders) == 5
    assert all(o.user == user for o in orders)
''',
        "避坑": (
            "- factory_boy 默认每次 build() 是内存对象，create() 才写 DB\n"
            "- SubFactory 创建的关联对象可以在 fixture 中共享\n"
            "- LazyAttribute 不要引用未定义的属性（在类定义阶段执行）"
        ),
        "进阶": "factory_boy 的 PostGeneration 钩子在对象创建后执行，适合复杂关系",
    },

    "fixture_data": {
        "title": "Fixture 中集成数据生成",
        "概念": (
            "fixture 是数据生成的天然场所。可以在 fixture 中用 Faker/factory_boy "
            "生成数据，结合 pytest 的 scope 控制数据的复用范围。"
        ),
        "何时用": (
            "- 同一数据在多个测试中复用\n"
            "- 需要根据参数生成不同数据\n"
            "- 想把数据生成和测试逻辑分离"
        ),
        "示例": '''import pytest
from faker import Faker

# 简单：function scope，每次测试新鲜数据
@pytest.fixture
def sample_user():
    fake = Faker("zh_CN")
    return {
        "name": fake.name(),
        "email": fake.email(),
        "phone": fake.phone_number(),
        "age": fake.random_int(18, 60),
    }

# 中等：module scope，同模块共享
@pytest.fixture(scope="module")
def user_pool():
    fake = Faker("zh_CN")
    return [UserFactory() for _ in range(10)]  # 需要 UserFactory

# 进阶：参数化 fixture 生成不同类型用户
@pytest.fixture(params=["student", "worker", "admin"])
def typed_user(request):
    fake = Faker("zh_CN")
    if request.param == "student":
        return {"name": fake.name(), "type": "student", "age": 20}
    elif request.param == "worker":
        return {"name": fake.name(), "type": "worker", "age": 35}
    else:
        return {"name": fake.name(), "type": "admin", "age": 45}

# pytest_generate_tests 自动参数化
def pytest_generate_tests(metafunc):
    if "user_type" in metafunc.fixturenames:
        metafunc.parametrize("user_type", ["student", "worker", "admin"])

# 组合：faker + factory_boy
@pytest.fixture
def enterprise_users():
    """生成企业测试用户数据"""
    fake = Faker("zh_CN")
    return [
        {
            "username": fake.user_name(),
            "company": fake.company(),
            "email": fake.company_email(),
            "address": fake.address(),
        }
        for _ in range(5)
    ]
''',
        "避坑": (
            "- function scope 性能好但数据不共享，module/session scope 共享但可能冲突\n"
            "- Faker 实例创建有开销，大批量生成时创建一个实例复用\n"
            "- fixture 返回的对象不要在测试中修改（会污染其他测试）"
        ),
        "进阶": "factory_boy 的 FactoryboyFixture 需要 pytest-factoryboy 插件",
    },

    "seed": {
        "title": "固定种子复现数据",
        "概念": (
            "Faker 默认每次运行数据都不同。"
            "用 seed() 固定种子可以让数据在多次运行间复现，方便调试和报告。"
        ),
        "何时用": (
            "- 调试时需要重现某个特定数据\n"
            "- CI 环境和本地环境需要一致的数据\n"
            "- 想把测试数据 snapshot 到测试报告中"
        ),
        "示例": '''from faker import Faker

# 固定全局种子
Faker.seed(42)
fake = Faker("zh_CN")
print(fake.name())  # 每次运行都是同一个名字

# session scope fixture：固定种子，数据稳定可复现
@pytest.fixture(scope="session")
def fixed_faker():
    fake = Faker("zh_CN")
    Faker.seed(2024)  # 固定种子
    return fake

@pytest.fixture
def reproducible_user(fixed_faker):
    return {
        "name": fixed_faker.name(),
        "email": fixed_faker.email(),
        "address": fixed_faker.address(),
    }

# 同一个测试数据固定 ID
import uuid
@pytest.fixture
def fixed_uuid():
    return uuid.UUID("12345678-1234-5678-1234-567812345678")

# 用 factory_boy 的 params 做可复现序列
import factory

class UserFactory(factory.Factory):
    class Meta:
        model = User

    id = factory.Sequence(lambda n: n)  # 确定性序列
    name = factory.Faker("name", locale="zh_CN")

    class Params:
        deterministic = factory.Trait(
            name="TestUser",  # 固定名字
            email="test@example.com",
        )

# deterministic trait 生成固定数据
user = UserFactory(deterministic=True)
assert user.name == "TestUser"
''',
        "避坑": (
            "- Faker.seed() 影响全局 Faker 实例，避免在测试中调用\n"
            "- 如果用了多个 Faker locale，每个都要单独 seed\n"
            "- CI 中固定 seed 方便复现 bug，但不能替代测试隔离"
        ),
        "进阶": "pytest-repeat 可以让测试重复执行固定次数，配合固定种子排查偶发问题",
    },

    "strategy": {
        "title": "测试数据策略选择",
        "概念": (
            "不同场景选不同的数据策略：hardcode（简单场景）、Faker（真实感）、"
            "factory_boy（结构化 ORM）、boundary（边界值）。选错策略会浪费大量时间。"
        ),
        "何时用": "不知道该用哪种数据生成方式时参考此指南",
        "示例": '''# 策略对比
# ============
# 1. Hardcode（最简单）
def test_login_success():
    user = {"name": "alice", "password": "secret123"}
    assert login(**user)["status"] == "ok"

# 适用：简单单元测试、测试逻辑不依赖数据细节

# 2. Faker（最通用）
@pytest.fixture
def user_data():
    fake = Faker("zh_CN")
    return {
        "name": fake.name(),
        "email": fake.email(),
        "phone": fake.phone_number(),
    }

# 适用：API 测试、集成测试，需要真实感数据

# 3. factory_boy（结构化，ORM）
class UserFactory(factory.Factory):
    name = factory.Faker("name")

# 适用：Django/Flask SQLAlchemy 模型测试、关联对象

# 4. 边界值（特殊场景）
BOUNDARY_VALUES = [0, 1, 127, 128, 255, 256, 32767, 32768, 65535]
@pytest.mark.parametrize("value", BOUNDARY_VALUES)
def test_boundary(value):
    assert process_value(value) >= 0

# 适用：数值处理、协议解析、格式验证

# 5. 从文件加载（数据驱动）
# test_data/users.json
# [
#   {"name": "Alice", "email": "alice@example.com"},
#   ...
# ]
@pytest.fixture(params=load_json("test_data/users.json"))
def test_user(request):
    return request.param

# 适用：大量测试数据，数据和代码分离

# 策略组合：boundary + faker
@pytest.fixture(params=[
    0, 1, 999999, None
] + [Faker("zh_CN").random_int() for _ in range(5)])
def edge_case_value(request):
    return request.param
''',
        "避坑": (
            "- 不要 all() hardcode equal 1，要用真实数据\n"
            "- 数据策略不是非此即彼，可以组合使用\n"
            "- 边界值 + Faker 组合是覆盖最全面的测试数据方案"
        ),
        "进阶": "hypothesis 是另一种数据策略：用属性测试（Property-based testing）生成海量数据",
    },
}


# ============================
# 主程序逻辑
# ============================

ALL_TOPICS = {
    "fixtures": FIXTURES_CONTENT,
    "mock": MOCK_CONTENT,
    "parametrize": PARAMETRIZE_CONTENT,
    "coverage": COVERAGE_CONTENT,
    "data": DATA_CONTENT,
}


def get_topic_keys(subcommand: str) -> List[str]:
    """获取子命令下的所有 topic key"""
    content = ALL_TOPICS.get(subcommand, {})
    return list(content.keys())


def output_content(subcommand: str, topic: Optional[str]) -> str:
    """输出指定主题的内容"""
    if subcommand not in ALL_TOPICS:
        return f"未知子命令: {subcommand}，可用: {', '.join(ALL_TOPICS.keys())}"

    topics = ALL_TOPICS[subcommand]

    if not topic:
        # 输出所有 topic 列表
        lines = [f"【{subcommand.upper()}】可用主题:"]
        for key, info in topics.items():
            lines.append(f"  {key:15s} — {info['title']}")
        lines.append("")
        lines.append(f"用法: pytest-test-master {subcommand} <topic>")
        lines.append(f"  例如: pytest-test-master {subcommand} {list(topics.keys())[0]}")
        return "\n".join(lines)

    if topic not in topics:
        available = ", ".join(topics.keys())
        return f"未知主题: {topic}，可用: {available}"

    info = topics[topic]
    lines = []
    lines.append("=" * 60)
    lines.append(f"【{subcommand.upper()} · {info['title']}】")
    lines.append("=" * 60)
    lines.append("")

    for section in ["概念", "何时用", "示例", "避坑", "进阶"]:
        if section in info:
            lines.append(f"📌 {section}：")
            lines.append(info[section])
            lines.append("")

    return "\n".join(lines)


def list_all_topics() -> str:
    """列出所有主题"""
    lines = ["=" * 60, "pytest-test-master 全部主题", "=" * 60, ""]
    for subcommand, topics in ALL_TOPICS.items():
        lines.append(f"【{subcommand.upper()}】")
        for key, info in topics.items():
            lines.append(f"  {key:15s} — {info['title']}")
        lines.append("")
    return "\n".join(lines)
