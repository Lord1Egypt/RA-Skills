# pytest-test-master — pytest 专项技能

## 痛点
- 会写测试，但 fixtures 用得乱，setup/teardown 纠缠不清
- 不知道什么时候用 scope、params、yield_fixture
- mock/patch 混用，容易写错 target 路径导致假通过
- conftest.py 越写越乱，跨文件 fixtures 共享搞不清
- parametrize 只会简单列表，多维度组合测试不知怎么写
- coverage 跑出来了但不知道怎么看报告找盲区
- 测试数据靠手写 hardcode，faker 和 factory_boy 不知道哪个场景用

## 场景
- 接手老项目，看到 conftest.py 里有 200 行不知道从哪入手
- 想用 pytest-mock 替代 unittest.mock 但不确定哪个更合适
- 需要参数化测试覆盖 10 种边界组合，手动写 10 个 test 函数太累
- 新人入职，问你 fixture scope 怎么选，autouse 什么时候开
- 想知道 coverage 怎么配合 CI，threshold 怎么设才合理
- 想快速生成真实感测试数据而不是 all() equal 1

## 定价
- **Free**：fixtures 基础用法 + mock/patch 入门（单文件示例）
- **Pro 19元**：conftest 进阶 + parametrize 组合 + pytest-cov 报告解读 + faker 集成
- **Team 49元**：factory_boy 高级模式 + CI/CD coverage gate + 全量示例模板 + 技术支持

## 指令格式

### 子命令
```
pytest-test-master fixtures [topic]    # fixtures 最佳实践
pytest-test-master mock [topic]         # mock/patch 使用模式
pytest-test-master parametrize [topic]  # 参数化测试
pytest-test-master coverage [topic]     # coverage 报告分析
pytest-test-master data [topic]         # 测试数据生成
pytest-test-master --list               # 列出所有可用主题
pytest-test-master --all                # 输出完整指南（Pro/Team）
```

### fixtures 子主题
```
pytest-test-master fixtures scope       # function/class/module/session 区别
pytest-test-master fixtures yield        # yield_fixture vs setup
pytest-test-master fixtures params       # 参数化 fixture
pytest-test-master fixtures autouse     # autouse 自动执行
pytest-test-master fixtures request      # request.fixture_registry
pytest-test-master fixtures teardown     # yield vs addfinalizer
pytest-test-master fixtures session      # session-scope 跨文件共享
pytest-test-master fixtures inject       # 依赖注入模式
```

### mock 子主题
```
pytest-test-master mock patch            # @patch 装饰器用法
pytest-test-master mock mock_obj         # MagicMock/PropertyMock
pytest-test-master mock assert           # 断言调用次数和参数
pytest-test-master mock freeze           # freeze_time 时间冻结
pytest-test-master mock spy              # Spy 模式保留真实行为
pytest-test-master mock scope            # session/class/function mock scope
pytest-test-master mock common          # 常见错误和修复
```

### parametrize 子主题
```
pytest-test-master parametrize basic     # @pytest.mark.parametrize
pytest-test-master parametrize ids       # 自定义测试 ID
pytest-test-master parametrize indirect  # 间接参数化
pytest-test-master parametrize combine   # 多个 parametrize 组合
pytest-test-master parametrize generate  # 动态生成参数
pytest-test-master parametrize product  # 笛卡尔积组合
```

### coverage 子主题
```
pytest-test-master coverage report      # coverage report 阅读
pytest-test-master coverage html        # HTML 报告生成
pytest-test-master coverage xml         # CI 集成 XML 报告
pytest-test-master coverage threshold  # 阈值设置
pytest-test-master coverage combine    # 多文件合并覆盖
pytest-test-master coverage exclude    # 排除文件和行
pytest-test-master coverage debug      # 调试覆盖问题
```

### data 子主题
```
pytest-test-master data faker          # Faker.py 用法
pytest-test-master data factory         # factory_boy 工厂模式
pytest-test-master data fixture         # fixture 中集成数据生成
pytest-test-master data fixture         # @pytest.fixture 结合 faker
pytest-test-master data seed           # 固定种子复现数据
pytest-test-master data strategy       # 不同数据策略
```

## Free 内容示例（fixtures scope）

```python
# fixture scope 四种级别
import pytest

# function（默认）：每个测试函数前后执行
@pytest.fixture
def db_connection():
    conn = create_connection()
    yield conn  # yield 前 = setup，yield 后 = teardown
    conn.close()

# class：类的所有测试方法共享同一个实例
@pytest.fixture(scope="class")
def test_client():
    client = FlaskClient()
    client.connect()
    yield client
    client.disconnect()

# module：一个模块只执行一次
@pytest.fixture(scope="module")
def django_db_setup():
    # 模块级别 setup
    pass

# session：整个测试 session 只执行一次
@pytest.fixture(scope="session")
def base_url():
    return "https://api.example.com"
```

## Free 内容示例（mock patch）

```python
# @patch 装饰器：mock 外部依赖
from unittest.mock import patch

@patch("myapp.service.requests.get")
def test_fetch_user(mock_get):
    mock_get.return_value = Mock(status_code=200, json=lambda: {"name": "Alice"})
    result = fetch_user(1)
    assert result["name"] == "Alice"
    # mock_get.assert_called_once()  # 可选断言
```

## 输出格式
每个子命令输出：
1. **概念说明**（何时用）
2. **代码示例**（拿来即用）
3. **常见错误**（避坑指南）
4. **进阶技巧**（Pro/Team 内容会注明）

## 与 test-master 的互补关系
- **test-master**：测试数据生成（输入）
- **pytest-test-master**：pytest 编写技巧（过程）
- 两者配合：生成数据 → 编写测试 → 覆盖报告
