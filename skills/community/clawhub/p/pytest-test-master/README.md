# pytest-test-master

> pytest 专项技能：fixtures / mock / parametrize / coverage / 测试数据

[![PyPI version](https://img.shields.io/pypi/v/pytest-test-master.svg)](https://pypi.org/project/pytest-test-master/)
[![Tests](https://github.com/shenghoo123-png/pytest-test-master/workflows/Test/badge.svg)](https://github.com/shenghoo123-png/pytest-test-master/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 痛点

- 会写测试，但 fixtures 用得乱，setup/teardown 纠缠不清
- 不知道什么时候用 scope、params、yield_fixture
- mock/patch 混用，容易写错 target 路径导致假通过
- conftest.py 越写越乱，跨文件 fixtures 共享搞不清
- parametrize 只会简单列表，多维度组合测试不知怎么写
- coverage 跑出来了但不知道怎么看报告找盲区
- 测试数据靠手写 hardcode，faker 和 factory_boy 不知道哪个场景用

## 安装

```bash
pip install pytest
```

直接运行（无需安装）：

```bash
python cli.py --list
python cli.py fixtures scope
python cli.py mock patch
python cli.py parametrize combine
python cli.py coverage html
python cli.py data factory
```

## 快速开始

### 列出所有主题

```bash
python cli.py --list
```

### 查看具体主题

```bash
# Fixtures 最佳实践
python cli.py fixtures scope         # fixture scope 四种级别
python cli.py fixtures yield        # yield vs setup/teardown
python cli.py fixtures params        # 参数化 fixture
python cli.py fixtures autouse      # autouse 自动执行
python cli.py fixtures session      # session-scope 跨文件共享

# Mock/Patch 模式
python cli.py mock patch            # @patch 装饰器用法
python cli.py mock mock_obj         # MagicMock/PropertyMock
python cli.py mock assert_calls    # 断言调用次数和参数
python cli.py mock freeze          # freeze_time 时间冻结
python cli.py mock spy             # Spy 模式

# Parametrize 参数化
python cli.py parametrize basic     # @pytest.mark.parametrize 基础
python cli.py parametrize ids       # 自定义测试 ID
python cli.py parametrize indirect  # 间接参数化
python cli.py parametrize combine   # 多个 parametrize 组合
python cli.py parametrize product   # 笛卡尔积

# Coverage 报告分析
python cli.py coverage report       # coverage report 阅读
python cli.py coverage html         # HTML 报告生成
python cli.py coverage xml          # CI 集成
python cli.py coverage threshold   # 阈值设置

# 测试数据生成
python cli.py data faker           # Faker.py 用法
python cli.py data factory         # factory_boy 工厂模式
python cli.py data seed           # 固定种子复现
python cli.py data strategy        # 数据策略选择
```

### 列出子命令所有主题

```bash
python cli.py --all fixtures
python cli.py --all mock
```

### 查看子命令 Topic Keys

```bash
python cli.py --topics fixtures
```

## 内容结构

| 子命令 | 主题数 | 说明 |
|--------|--------|------|
| `fixtures` | 8 | scope/yield/params/autouse/request/teardown/session/inject |
| `mock` | 7 | patch/mock_obj/assert_calls/freeze/spy/scope_mock/common |
| `parametrize` | 6 | basic/ids/indirect/combine/generate/product |
| `coverage` | 6 | report/html/xml/threshold/exclude/debug |
| `data` | 5 | faker/factory/fixture_data/seed/strategy |

每个主题包含：
- **概念**：何时用、解决什么问题
- **代码示例**：拿来即用的真实代码
- **避坑指南**：常见错误和修复方法
- **进阶技巧**：高级用法和扩展

## 定价

| 版本 | 价格 | 内容 |
|------|------|------|
| Free | 免费 | fixtures 基础用法 + mock/patch 入门 |
| Pro | ¥19 | conftest 进阶 + parametrize 组合 + pytest-cov + faker |
| Team | ¥49 | factory_boy 高级 + CI/CD coverage gate + 全量模板 |

## 项目结构

```
pytest-test-master/
├── SKILL.md              # 技能文档
├── README.md             # 本文件
├── pytest_master.py      # 核心库（内容 + 逻辑，约 500 行）
├── cli.py                # CLI 入口
├── tests/
│   └── test_pytest_master.py  # 单元测试（38 个）
├── .github/workflows/
│   └── test.yml          # CI 配置
├── clawhub.json          # ClawHub 配置
├── setup.sh              # 一键安装测试
└── requirements.txt      # 依赖
```

## 开发

### 运行测试

```bash
pytest tests/ -v
```

### 完整演示

```bash
bash setup.sh
```

## 与 test-master 的互补关系

- **test-master**：测试数据生成（输入）
- **pytest-test-master**：pytest 编写技巧（过程）

两者配合：`生成数据 → 编写测试 → 覆盖报告`

## ClawHub 发布

本项目已配置 `clawhub.json`，可用于发布到 ClawHub：

```bash
# 1. 创建 GitHub 仓库（手动）
# 2. Push 代码
# 3. ClawHub 提交
```

## License

MIT
