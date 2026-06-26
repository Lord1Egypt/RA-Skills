#!/usr/bin/env python3.9
"""
百度 Agent Sandbox 沙箱创建工具
支持快速创建各种类型的沙箱实例
"""

import os
import sys
import argparse
from datetime import datetime
from dotenv import load_dotenv

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check_api_key():
    """检查 API Key 是否配置"""
    load_dotenv(os.path.expanduser('~/.env'))

    api_key = os.getenv('E2B_API_KEY')
    domain = os.getenv('E2B_DOMAIN')

    if not api_key:
        print("❌ 未配置 API Key!")
        print("\n请按以下步骤配置:")
        print("1. 访问 https://console.cloud.baidu-int.com/aitools/sandbox-square")
        print("2. 进入空间后点击『沙箱』→『API Key 管理』")
        print("3. 获取 API Key 后,让 Agent 帮你配置到 ~/.env 文件")
        return False

    print(f"✅ API Key 已配置: {api_key[:10]}...")
    print(f"✅ Domain: {domain}")
    return True

def check_dependencies():
    """检查依赖是否安装"""
    try:
        from e2b_code_interpreter import Sandbox
        print("✅ SDK 已安装")
        return True
    except ImportError:
        print("❌ SDK 未安装!")
        print("\n请运行以下命令安装:")
        print("pip3.9 install e2b==1.11.2+baidu --index=https://pip.baidu-int.com/simple/")
        print("pip3.9 install e2b-code-interpreter==1.5.2 --index=https://pip.baidu-int.com/simple/")
        print("pip3.9 install load_dotenv==0.1.0 --index=https://pip.baidu-int.com/simple/")
        return False

def create_sandbox(template, timeout, name=None, creator=None, comate_token=None):
    """
    创建沙箱实例

    Args:
        template: 沙箱模板名称 (code_test/browser_use/aio/coding_agent)
        timeout: 超时时间(秒)
        name: 沙箱名称
        creator: 创建人
        comate_token: Comate 认证 Token(用于 iCode 权限注入)

    Returns:
        Sandbox 对象
    """
    from e2b_code_interpreter import Sandbox

    # 构建元数据
    metadata = {}
    if creator:
        metadata["agent-sandbox/creator"] = creator
    if name:
        metadata["agent-sandbox/name"] = name

    # 构建环境变量
    envs = {}
    if comate_token:
        envs["COMATE_AUTH_TOKEN"] = comate_token
        # 如果有 comate_token,也设置 codeBean
        if creator:
            metadata["codeBean"] = f'{{"username": "{creator}"}}'

    print(f"\n🚀 正在创建沙箱...")
    print(f"  模板: {template}")
    print(f"  超时: {timeout}秒 ({timeout/3600:.1f}小时)")
    if metadata:
        print(f"  元数据: {metadata}")

    # 创建沙箱
    sbx = Sandbox(
        timeout=timeout,
        template=template,
        metadata=metadata if metadata else None,
        envs=envs if envs else None,
        request_timeout=120
    )

    return sbx

def print_sandbox_info(sbx):
    """打印沙箱信息"""
    info = sbx.get_info()

    print(f"\n✅ 沙箱创建成功!")
    print(f"\n{'='*60}")
    print(f"📋 基本信息")
    print(f"{'='*60}")
    print(f"  沙箱ID: {sbx.sandbox_id}")
    print(f"  模板: {info.template_id}")
    print(f"  创建时间: {info.started_at.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  过期时间: {info.end_at.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  存活时长: {(info.end_at - info.started_at).total_seconds()/3600:.1f}小时")

    print(f"\n{'='*60}")
    print(f"🌐 访问地址")
    print(f"{'='*60}")
    print(f"  管理页面: https://8200-{sbx.sandbox_id}.agent-sandbox.baidu-int.com/")
    print(f"    - VSCode 视图")
    print(f"    - Terminal 视图")
    print(f"    - Jupyter 视图")
    print(f"  MCP服务:  https://8080-{sbx.sandbox_id}.agent-sandbox.baidu-int.com/mcp")

    log_url = info.metadata.get('logURL')
    if log_url:
        print(f"\n{'='*60}")
        print(f"📝 日志链接")
        print(f"{'='*60}")
        print(f"  {log_url}")

    print(f"\n{'='*60}")
    print(f"💡 使用提示")
    print(f"{'='*60}")
    print(f"  - 通过 Agent 对话: '在沙箱 {sbx.sandbox_id} 中执行命令...'")
    print(f"  - 通过 SDK 连接: Sandbox(sandbox_id='{sbx.sandbox_id}')")
    print(f"  - 沙箱将在 {info.end_at.strftime('%H:%M')} 自动销毁")
    print(f"{'='*60}\n")

    return info

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='百度 Agent Sandbox 沙箱创建工具')

    parser.add_argument(
        '--template', '-t',
        default='code_test',
        choices=['code_test', 'browser_use', 'aio', 'coding_agent'],
        help='沙箱模板名称 (默认: code_test)'
    )

    parser.add_argument(
        '--timeout', '-T',
        type=int,
        default=3600,
        help='沙箱存活时间(秒),最大86400 (默认: 3600)'
    )

    parser.add_argument(
        '--name', '-n',
        help='沙箱名称'
    )

    parser.add_argument(
        '--creator', '-c',
        help='创建人用户名'
    )

    parser.add_argument(
        '--comate-token',
        help='Comate 认证 Token (用于 iCode 权限注入)'
    )

    parser.add_argument(
        '--check-only',
        action='store_true',
        help='仅检查环境配置,不创建沙箱'
    )

    args = parser.parse_args()

    # 检查环境
    print("="*60)
    print("🔍 检查环境配置")
    print("="*60)

    if not check_api_key():
        sys.exit(1)

    if not check_dependencies():
        sys.exit(1)

    if args.check_only:
        print("\n✅ 环境检查通过,可以创建沙箱")
        sys.exit(0)

    # 验证超时时间
    if args.timeout > 86400:
        print(f"❌ 超时时间不能超过 86400 秒(1天),当前: {args.timeout}")
        sys.exit(1)

    # 创建沙箱
    sbx = create_sandbox(
        template=args.template,
        timeout=args.timeout,
        name=args.name,
        creator=args.creator,
        comate_token=args.comate_token
    )

    # 打印信息
    info = print_sandbox_info(sbx)

    # 返回沙箱ID (用于脚本调用)
    print(f"\n# SANDBOX_ID={sbx.sandbox_id}")

    return sbx

if __name__ == '__main__':
    main()