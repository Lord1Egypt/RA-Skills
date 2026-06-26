#!/usr/bin/env python3
"""
gen_api_test.py — 接口测试脚本生成器
用法：
    python gen_api_test.py --name "用户登录" --method POST --path "/auth/login" --auth bearer --out ./tests
    python gen_api_test.py --help
"""

import argparse
import os
import re
import sys
from datetime import date


def to_snake_case(name: str) -> str:
    """将中文或英文名称转为 snake_case 模块名"""
    # 移除非字母数字字符，空格转下划线
    s = re.sub(r'[^\w\s]', '', name)
    s = re.sub(r'\s+', '_', s.strip())
    # 如果是中文，直接用拼音首字母（简单处理）
    if re.search(r'[\u4e00-\u9fff]', s):
        # 无法转拼音时使用时间戳作为后缀
        s = f"api_{date.today().strftime('%m%d')}"
    return s.lower()


def generate_conftest() -> str:
    return '''\
import pytest
import requests

# ======================================================
# conftest.py — 全局 Fixtures
# 修改 BASE_URL、用户名、密码为你的真实环境配置
# ======================================================

BASE_URL = "https://api.example.com"  # TODO: 替换为真实 base URL


@pytest.fixture(scope="session")
def base_url():
    """返回接口基础 URL"""
    return BASE_URL


@pytest.fixture(scope="session")
def auth_token(base_url):
    """登录并获取 Bearer Token，整个测试会话只登录一次"""
    resp = requests.post(f"{base_url}/auth/login", json={
        "username": "test@example.com",  # TODO: 替换为测试账号
        "password": "Test@1234"          # TODO: 替换为测试密码
    })
    assert resp.status_code == 200, f"登录失败: {resp.text}"
    token = resp.json().get("data", {}).get("token", "")
    assert token, "未能从响应中获取 token，请检查接口返回结构"
    return token


@pytest.fixture(scope="session")
def auth_headers(auth_token):
    """返回带 Bearer Token 的请求头"""
    return {"Authorization": f"Bearer {auth_token}"}
'''


def generate_test_file(name: str, method: str, path: str, auth: str, module: str) -> str:
    method_upper = method.upper()
    method_lower = method.lower()
    auth_fixture = ""
    auth_call = ""

    if auth == "bearer":
        auth_fixture = "auth_headers, "
        auth_call = ", headers=auth_headers"
    elif auth == "none":
        auth_fixture = ""
        auth_call = ""

    # 生成请求体示例（仅 POST/PUT/PATCH）
    body_example = ""
    body_param = ""
    if method_upper in ("POST", "PUT", "PATCH"):
        body_example = '''
        # TODO: 替换为真实的请求体参数
        payload = {
            "key": "value",
        }'''
        body_param = ", json=payload"

    return f'''\
"""
{name} — 接口自动化测试
生成日期: {date.today()}
接口: {method_upper} {path}

使用方法:
    pytest {module}.py -v
    pytest {module}.py -v --html=report.html
"""

import pytest
import requests


class Test{name.replace(" ", "").replace("-", "").replace("（", "").replace("）", "")}:
    """
    {name} 接口测试套件
    覆盖场景：正向成功 / 参数缺失 / 未授权 / 边界值
    """

    # ============================================================
    # 正向测试：期望接口正常返回
    # ============================================================
    def test_{module}_success(self, base_url, {auth_fixture}):
        """正向：请求合法参数，期望返回成功"""
        url = f"{{base_url}}{path}"{body_example}

        resp = requests.{method_lower}(url{body_param}{auth_call})

        # 1. 状态码断言
        assert resp.status_code == 200, (
            f"期望状态码 200，实际 {{resp.status_code}}\\n响应内容: {{resp.text}}"
        )

        # 2. 响应时间断言（超 2s 视为性能问题）
        elapsed = resp.elapsed.total_seconds()
        assert elapsed < 2.0, f"响应时间 {{elapsed:.2f}}s 超过 2s 阈值"

        # 3. 响应体基础校验
        body = resp.json()
        # TODO: 替换为实际的业务码字段名和成功值
        assert body.get("code") == 0, f"业务码异常: {{body}}"
        assert "data" in body, f"响应体缺少 data 字段: {{body}}"

        # 4. 字段完整性校验（TODO: 补充实际必返字段）
        # data = body["data"]
        # assert "id" in data, "响应缺少 id 字段"

    # ============================================================
    # 负向测试：未授权
    # ============================================================
    def test_{module}_unauthorized(self, base_url):
        """负向：不带 token 请求，期望返回 401"""
        url = f"{{base_url}}{path}"
        resp = requests.{method_lower}(url)
        assert resp.status_code == 401, (
            f"期望 401，实际 {{resp.status_code}}，响应: {{resp.text}}"
        )

    # ============================================================
    # 负向测试：缺少必填参数
    # ============================================================
    def test_{module}_missing_required_param(self, base_url, {auth_fixture}):
        """负向：缺少必填参数，期望返回 400"""
        url = f"{{base_url}}{path}"
        # TODO: 传入缺少必填字段的请求体
        payload = {{}}  # 空 payload 触发必填校验

        resp = requests.{method_lower}(url, json=payload{auth_call})
        assert resp.status_code == 400, (
            f"期望 400，实际 {{resp.status_code}}，响应: {{resp.text}}"
        )

    # ============================================================
    # 参数化测试：多场景批量覆盖
    # ============================================================
    @pytest.mark.parametrize("description,payload,expected_status", [
        # TODO: 根据实际接口补充参数化用例
        # ("描述",     {{"字段": "值"}},  期望状态码),
        ("空 payload", {{}},              400),
    ])
    def test_{module}_parametrize(
        self, base_url, {auth_fixture}description, payload, expected_status
    ):
        """参数化：批量覆盖多种输入场景"""
        url = f"{{base_url}}{path}"
        resp = requests.{method_lower}(url, json=payload{auth_call})
        assert resp.status_code == expected_status, (
            f"[{{description}}] 期望 {{expected_status}}，实际 {{resp.status_code}}\\n响应: {{resp.text}}"
        )
'''


def main():
    parser = argparse.ArgumentParser(
        description="生成 pytest 接口测试脚本",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  python gen_api_test.py --name "用户登录" --method POST --path "/auth/login" --auth bearer --out ./tests
  python gen_api_test.py --name "获取商品列表" --method GET --path "/api/products" --auth bearer
        """
    )
    parser.add_argument("--name",   required=True,  help="接口名称（中英文均可），如：用户登录")
    parser.add_argument("--method", required=True,  choices=["GET", "POST", "PUT", "PATCH", "DELETE"],
                        help="HTTP 请求方法")
    parser.add_argument("--path",   required=True,  help="接口路径，如 /api/user/info")
    parser.add_argument("--auth",   default="bearer", choices=["bearer", "none"],
                        help="认证方式：bearer（默认）或 none")
    parser.add_argument("--out",    default="./tests", help="输出目录（默认 ./tests）")

    args = parser.parse_args()

    # 生成文件名
    module = to_snake_case(args.name)
    test_filename = f"test_{module}.py"

    # 创建输出目录
    os.makedirs(args.out, exist_ok=True)

    # 生成测试文件
    test_path = os.path.join(args.out, test_filename)
    with open(test_path, "w", encoding="utf-8") as f:
        f.write(generate_test_file(args.name, args.method, args.path, args.auth, module))
    print(f"✅ 测试文件已生成: {test_path}")

    # 如果 conftest.py 不存在，同时生成
    conftest_path = os.path.join(args.out, "conftest.py")
    if not os.path.exists(conftest_path):
        with open(conftest_path, "w", encoding="utf-8") as f:
            f.write(generate_conftest())
        print(f"✅ conftest.py 已生成: {conftest_path}")
    else:
        print(f"ℹ️  conftest.py 已存在，跳过生成: {conftest_path}")

    print()
    print("📋 下一步:")
    print(f"  1. 编辑 {test_path}，填写 TODO 注释处的实际接口参数")
    print(f"  2. 编辑 {conftest_path}，填写真实的 base_url 和登录账号")
    print(f"  3. 运行测试: pytest {args.out} -v")


if __name__ == "__main__":
    main()
