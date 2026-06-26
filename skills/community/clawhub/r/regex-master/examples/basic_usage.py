"""
Regex Master - 基础使用示例
"""
from scripts.regex_engine import RegexMaster


def main():
    rm = RegexMaster()

    print("=" * 50)
    print("示例 1: 测试正则是否匹配")
    print("=" * 50)
    result = rm.test(r"^\d{11}$", "13800138000")
    print(f"测试 13800138000 匹配 ^\\d{{11}}$: {result}")

    result2 = rm.test(r"^\d{11}$", "1380013800")
    print(f"测试 1380013800 匹配 ^\\d{{11}}$: {result2}")

    print("\n" + "=" * 50)
    print("示例 2: 解释正则含义")
    print("=" * 50)
    exp = rm.explain(r"^(?=.*[A-Z])(?=.*\d).{8,}$")
    print(f"解释密码强度正则: {exp}")

    print("\n" + "=" * 50)
    print("示例 3: 从自然语言生成正则")
    print("=" * 50)
    patterns = [
        "提取中国大陆手机号",
        "匹配邮箱地址",
        "匹配 IPv4 地址",
    ]
    for desc in patterns:
        pat = rm.generate(desc)
        print(f"'{desc}' -> {pat}")

    print("\n" + "=" * 50)
    print("示例 4: 从文本中提取所有邮箱")
    print("=" * 50)
    text = """
    联系方式:
    张三: zhangsan@example.com
    李四: lisi@company.cn
    王五: wangwu@gmail.com
    """
    emails = rm.extract_all(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    print(f"提取到的邮箱: {emails}")

    print("\n" + "=" * 50)
    print("示例 5: 使用内置模板")
    print("=" * 50)
    print("可用模板:", list(rm.list_templates().keys()))
    print(f"邮箱模板: {rm.get_template('email')}")
    print(f"手机号模板: {rm.get_template('phone_cn')}")

    print("\n" + "=" * 50)
    print("示例 6: 验证正则语法")
    print("=" * 50)
    valid = rm.validate_pattern(r"^[a-z]+$")
    print(f"验证 ^[a-z]+$: {valid}")
    invalid = rm.validate_pattern(r"[a-z")
    print(f"验证 [a-z: {invalid}")

    print("\n" + "=" * 50)
    print("示例 7: 正则替换")
    print("=" * 50)
    text = "我的电话是 138-1234-5678，备用 139-8765-4321"
    result = rm.replace(r"(\d{3})-(\d{4})-(\d{4})", text, r"\1****\3")
    print(f"替换后: {result}")


if __name__ == "__main__":
    main()
