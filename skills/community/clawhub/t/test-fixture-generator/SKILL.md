# test-fixture-generator

## 名称
test-fixture-generator

## 描述
自动生成pytest fixtures的工具，支持常见测试场景（数据库、API mock、文件处理等）

## 触发词
fixture, pytest fixture, conftest, 测试夹具

## 指令
生成pytest fixtures代码

## 使用方式
```bash
# 生成数据库fixture
python -m test_fixture_generator generate --type db --db-type mysql

# 生成API mock fixture
python -m test_fixture_generator generate --type api --framework requests

# 生成文件处理fixture
python -m test_fixture_generator generate --type file --format json

# 生成conftest.py
python -m test_fixture_generator init

# 交互式生成
python -m test_fixture_generator interactive
```

## 参数说明
- `--type`: fixture类型 (db|api|file|random)
- `--db-type`: 数据库类型 (mysql|postgres|sqlite)
- `--framework`: mock框架 (requests|httpx|boto3)
- `--format`: 文件格式 (json|yaml|csv|toml)
- `--output`: 输出文件路径

## 输出
生成符合pytest规范的fixture代码，自动处理setup/teardown
