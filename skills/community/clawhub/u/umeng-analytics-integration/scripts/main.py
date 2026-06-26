#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
友盟Android统计SDK集成工具
主工作流编排
"""

import os
import sys
import argparse
from datetime import datetime

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from env_checker import EnvChecker
from project_validator import ProjectValidator

# 全局变量
backup_dir_path = None


def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description='友盟Android统计SDK集成工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python main.py --project-path /path/to/android/project
  python main.py --project-path /path/to/project --app-module myapp
        """
    )
    
    parser.add_argument(
        '--project-path',
        required=True,
        help='Android项目路径'
    )
    
    parser.add_argument(
        '--app-module',
        default='app',
        help='App模块名称(默认: app)'
    )
    
    return parser.parse_args()


def collect_sdk_config():
    """
    收集SDK配置参数(appkey和channel)
    
    Returns:
        dict: {'appkey': str, 'channel': str, 'using_placeholder': bool}
    """
    print("\n" + "=" * 60)
    print("友盟统计SDK配置")
    print("=" * 60)
    print("\n友盟统计SDK集成需要提供以下参数:")
    print("  - appkey: 友盟后台创建应用后获取")
    print("  - channel: 应用分发渠道标识(如: googleplay, huawei, xiaomi)")
    print()
    
    choice = input("是否现在提供这些参数? (y/n, 默认n): ").strip().lower()
    
    using_placeholder = False
    
    if choice == 'y':
        appkey = input("\n请输入appkey: ").strip()
        channel = input("请输入channel: ").strip()
        
        if not appkey:
            print("\n⚠️  appkey为空,将使用占位符")
            appkey = "YOUR_UMENG_APPKEY"
            using_placeholder = True
        
        if not channel:
            print("⚠️  channel为空,将使用占位符")
            channel = "YOUR_CHANNEL"
            using_placeholder = True
    else:
        appkey = "YOUR_UMENG_APPKEY"
        channel = "YOUR_CHANNEL"
        using_placeholder = True
        print("\n⚠️  将使用占位符进行集成")
        print("⚠️  请后续替换为真实appkey和channel后SDK才可正常上报数据")
    
    # 确认配置
    print("\n" + "=" * 60)
    print("配置确认")
    print("=" * 60)
    print(f"  appkey: {appkey}")
    print(f"  channel: {channel}")
    if using_placeholder:
        print("\n  ⚠️  使用占位符,后续需要替换!")
    print()
    
    confirm = input("是否继续集成? (y/n, 默认y): ").strip().lower()
    if confirm == 'n':
        print("\n❌ 用户取消集成")
        sys.exit(0)
    
    return {
        'appkey': appkey,
        'channel': channel,
        'using_placeholder': using_placeholder
    }


def step1_check_environment():
    """步骤1: 环境检查"""
    print("\n" + "=" * 60)
    print("步骤 1/7: 环境检查")
    print("=" * 60)
    
    checker = EnvChecker()
    checker.check_all()
    
    if not checker.report():
        print("❌ 环境检查失败,无法继续")
        return False
    
    return True


def step2_validate_project(project_path, app_module):
    """步骤2: 项目验证"""
    print("\n" + "=" * 60)
    print("步骤 2/7: 项目验证")
    print("=" * 60)
    
    validator = ProjectValidator(project_path, app_module)
    success, message = validator.validate()
    
    if not success:
        print(f"❌ 项目验证失败: {message}")
        print("\nSDK集成目标需要是一个可正常完成编译,")
        print("正常产出apk执行安装包的应用工程源码。")
        print("\n请先修复项目编译问题后再运行SDK集成。")
        return False
    
    return True


def step3_collect_config():
    """步骤3: 参数交互"""
    print("\n" + "=" * 60)
    print("步骤 3/7: SDK配置")
    print("=" * 60)
    
    config = collect_sdk_config()
    return config


def step4_integrate_sdk(project_path, app_module, config):
    """步骤4: SDK集成"""
    print("\n" + "=" * 60)
    print("步骤 4/7: SDK集成")
    print("=" * 60)
    
    from sdk_integrator import SDKIntegrator
    
    integrator = SDKIntegrator(project_path, app_module, config)
    success, message = integrator.integrate()
    
    if not success:
        print(f"❌ SDK集成失败: {message}")
        print(f"\n备份目录: {integrator.backup_dir}")
        print("如需回滚,请运行:")
        print(f"  python3 scripts/rollback.py --backup-dir {integrator.backup_dir} --project-path {project_path}")
        return False
    
    # 保存备份目录路径供后续使用
    global backup_dir_path
    backup_dir_path = integrator.backup_dir
    
    return True


def step5_verify_build(project_path):
    """步骤5: 编译验证"""
    print("\n" + "=" * 60)
    print("步骤 5/7: 编译验证")
    print("=" * 60)
    
    from project_validator import ProjectValidator
    
    # 重新创建验证器并执行编译
    validator = ProjectValidator(project_path, 'app')
    
    print("执行编译验证...")
    if not validator._check_build():
        print("\n❌ SDK集成后编译失败")
        print(f"\n备份目录: {backup_dir_path}")
        print("建议执行回滚:")
        print(f"  python3 scripts/rollback.py --backup-dir {backup_dir_path} --project-path {project_path}")
        return False
    
    print("✅ SDK集成后编译成功\n")
    return True


def step6_verify_sdk(project_path, app_module):
    """步骤6: SDK验证"""
    print("\n" + "=" * 60)
    print("步骤 6/7: SDK验证")
    print("=" * 60)
    
    from sdk_verifier import SDKVerifier
    
    verifier = SDKVerifier(project_path, app_module)
    success, message = verifier.verify()
    
    if success:
        print("✅ SDK验证通过\n")
    else:
        print(f"⚠️  SDK验证未通过: {message}\n")
        print("注意: SDK验证失败不影响代码集成,请后续手动验证")
        print("查看logcat日志命令:")
        print("  adb logcat | grep -E 'UMConfigure|umeng'")
        print("\n成功关键词:")
        print("  本次启动数据: 发送成功!")
        print()
    
    return True  # 不阻塞流程


def step7_generate_report(project_path, config, build_success, verify_success):
    """步骤7: 生成报告"""
    print("\n" + "=" * 60)
    print("步骤 7/7: 生成报告")
    print("=" * 60)
    
    report = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'project_path': project_path,
        'sdk_config': {
            'appkey': config['appkey'],
            'channel': config['channel'],
            'using_placeholder': config['using_placeholder']
        },
        'integration_status': 'partial',
        'build_status': 'pending',
        'verification_status': 'pending'
    }
    
    print("\n📋 集成报告")
    print("=" * 60)
    print(f"时间: {report['timestamp']}")
    print(f"项目: {report['project_path']}")
    print(f"\nSDK配置:")
    print(f"  appkey: {report['sdk_config']['appkey']}")
    print(f"  channel: {report['sdk_config']['channel']}")
    if report['sdk_config']['using_placeholder']:
        print(f"  ⚠️  使用占位符,需要替换!")
    print(f"\n集成状态: {report['integration_status']}")
    print("=" * 60)
    
    if config['using_placeholder']:
        print("\n⚠️  下一步:")
        print("  1. 在友盟后台创建应用获取真实appkey")
        print("  2. 替换Application类中的appkey和channel")
        print("  3. 重新编译运行应用")
        print("  4. 查看logcat日志确认SDK是否成功上报")
        print()


def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("友盟Android统计SDK集成工具")
    print("=" * 60)
    
    # 解析参数
    args = parse_arguments()
    project_path = args.project_path
    app_module = args.app_module
    
    # 步骤1: 环境检查
    if not step1_check_environment():
        sys.exit(1)
    
    # 步骤2: 项目验证
    if not step2_validate_project(project_path, app_module):
        sys.exit(1)
    
    # 步骤3: 参数交互
    config = step3_collect_config()
    
    # 步骤4: SDK集成(占位)
    if not step4_integrate_sdk(project_path, app_module, config):
        sys.exit(1)
    
    # 步骤5: 编译验证(占位)
    if not step5_verify_build(project_path):
        sys.exit(1)
    
    # 步骤6: SDK验证(占位)
    # 注意: 此步骤可选,失败不阻塞
    
    # 步骤7: 生成报告
    step7_generate_report(project_path, config, True, True)
    
    print("\n✅ SDK集成完成\n")


if __name__ == '__main__':
    main()
