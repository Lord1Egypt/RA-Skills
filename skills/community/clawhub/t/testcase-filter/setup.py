from setuptools import setup, find_packages

setup(
    name="testcase-filter",
    version="1.0.0",
    description="筛选测试用例Excel文件，提取P0/P1优先级用例，重新编号并保持原格式",
    author="custom",
    packages=find_packages(),
    install_requires=[
        "openpyxl>=3.0.0",
    ],
    entry_points={
        'console_scripts': [
            'testcase-filter=testcase_filter:main',
        ],
    },
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Software Development :: Testing',
        'Topic :: Utilities',
    ],
)


def main():
    import sys
    if len(sys.argv) < 3:
        print("用法: testcase-filter <输入文件> <输出文件>")
        print("示例: testcase-filter input.xlsx output.xlsx")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    from testcase_filter import analyze_excel, process_excel

    # 先分析
    analyze_excel(input_file)

    # 再处理
    result = process_excel(input_file, output_file)

    print(f"\n✅ 处理完成！")
    print(f"输出文件: {output_file}")
    print(f"处理了 {result['processed']} 个sheet")
    print(f"跳过了 {result['skipped']} 个sheet")