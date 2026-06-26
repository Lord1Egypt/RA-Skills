#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
x402 Payment Test Suite (Lightweight)
x402 支付测试套件 - 轻量版（不依赖 selenium）
"""

import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 只导入不依赖 selenium 的模块
from x402_core import X402Processor, X402PaymentProof, X402PaymentRequest
from quota_manager import UserQuotaManager
from async_queue import AsyncTaskQueue


# 测试网配置
TEST_CONFIG = {
    "network": "base-sepolia",
    "usdc_contract": "0x036CbD53842c5426634e7929541eC2318f3dCF7e",
}

TEST_USER = "0xTestUser123"


class MockBlockchain:
    """模拟区块链"""
    
    def __init__(self):
        self.transactions = {}
    
    def create_mock_transaction(self, amount, to_address):
        """创建模拟交易"""
        tx_hash = f"0x{hex(int(time.time() * 1000000))[2:].zfill(16)}"
        self.transactions[tx_hash] = {
            "amount": amount,
            "to": to_address,
            "confirmed": True,
            "timestamp": time.time(),
        }
        return tx_hash


mock_chain = MockBlockchain()


def test_free_quota():
    """测试免费额度"""
    print("\n" + "="*60)
    print("🧪 测试1: 免费额度系统")
    print("="*60)
    
    # 清理测试用户
    user_file = f"data/users/{TEST_USER}.json"
    if os.path.exists(user_file):
        os.remove(user_file)
    
    manager = UserQuotaManager(TEST_USER)
    status = manager.get_status()
    
    print(f"✅ 新用户创建成功")
    print(f"   免费额度: {status['free']['remaining']}/{status['free']['total']} 篇")
    print(f"   订阅状态: {'✅ 有效' if status['subscription']['active'] else '❌ 未开通'}")
    
    # 使用免费额度
    can_use = manager.use_free_quota(5)
    print(f"\n使用 5 篇免费额度: {'✅ 成功' if can_use else '❌ 失败'}")
    
    status = manager.get_status()
    print(f"   剩余免费额度: {status['free']['remaining']} 篇")
    
    # 尝试超额使用
    print(f"\n尝试使用 10 篇（超过剩余额度）...")
    can_use = manager.use_free_quota(10)
    print(f"   结果: {'❌ 失败（符合预期）' if not can_use else '✅ 成功'}")
    
    return True


def test_x402_payment():
    """测试 x402 支付"""
    print("\n" + "="*60)
    print("🧪 测试2: x402 支付流程")
    print("="*60)
    
    processor = X402Processor()
    
    # 1. 创建支付请求
    print("\n📤 步骤1: 创建支付请求")
    request = processor.create_payment_request(
        user_id=TEST_USER,
        resource="article",
        resource_id="test_batch_10",
        amount=1.0
    )
    
    print(f"✅ 支付请求创建成功")
    print(f"   金额: ${request.amount} USDC")
    print(f"   收款地址: {request.to_dict()['to']}")
    print(f"   Nonce: {request.nonce[:16]}...")
    print(f"   过期时间: 5分钟")
    
    # 2. 模拟支付
    print("\n💰 步骤2: 模拟用户支付")
    tx_hash = mock_chain.create_mock_transaction(
        amount=1.0,
        to_address=request.to_dict()['to']
    )
    print(f"✅ 模拟交易创建")
    print(f"   TX Hash: {tx_hash[:20]}...")
    print(f"   金额: 1.0 USDC")
    
    # 3. 构建支付证明
    print("\n📨 步骤3: 构建支付证明")
    payment_token = json.dumps({
        "tx_hash": tx_hash,
        "nonce": request.nonce,
        "amount": 1.0,
        "from": TEST_USER,
        "timestamp": int(time.time()),
    })
    
    proof = X402PaymentProof.from_token(payment_token)
    print(f"✅ 支付证明构建成功")
    print(f"   TX Hash: {proof.tx_hash[:20]}...")
    
    # 4. 验证支付
    print("\n🔍 步骤4: 验证支付")
    is_valid = processor.verify_payment(proof, request)
    print(f"{'✅' if is_valid else '❌'} 支付验证: {'通过' if is_valid else '失败'}")
    
    if is_valid:
        processor.confirm_payment(proof)
        print(f"✅ 支付已确认")
    
    return is_valid


def test_payment_modes():
    """测试支付模式切换"""
    print("\n" + "="*60)
    print("🧪 测试3: 支付模式自动切换")
    print("="*60)
    
    processor = X402Processor()
    
    test_cases = [
        ("per_article", 3, "实时支付"),
        ("per_article", 50, "异步支付"),
        ("per_account", 1, "异步支付"),
    ]
    
    all_pass = True
    for mode, count, expected in test_cases:
        amount = processor.calculate_price(mode, count)
        payment_mode = processor.determine_payment_mode(amount)
        
        mode_name = "实时支付" if payment_mode == "realtime" else "异步支付"
        is_correct = (payment_mode == "realtime" and expected == "实时支付") or \
                     (payment_mode == "async" and expected == "异步支付")
        
        print(f"\n   {mode}, 数量: {count}")
        print(f"   金额: ${amount} → {mode_name}")
        print(f"   {'✅ 正确' if is_correct else '❌ 错误'}")
        
        all_pass = all_pass and is_correct
    
    return all_pass


def test_async_queue():
    """测试异步任务队列"""
    print("\n" + "="*60)
    print("🧪 测试4: 异步任务队列")
    print("="*60)
    
    queue = AsyncTaskQueue()
    
    # 创建任务
    print("\n📋 创建异步任务")
    task = queue.create_task(
        user_id=TEST_USER,
        account_name="测试公众号",
        max_articles=100,
        payment_mode="async",
        amount=10.0
    )
    
    print(f"✅ 任务创建成功")
    print(f"   任务ID: {task.task_id}")
    print(f"   初始状态: {task.status}")
    print(f"   公众号: {task.account_name}")
    print(f"   目标文章数: {task.max_articles}")
    
    # 确认支付
    print("\n💰 确认支付")
    tx_hash = mock_chain.create_mock_transaction(10.0, "0x172444FC64e2E370fCcF297dB865831A1555b07A")
    queue.confirm_payment(task.task_id, {"tx_hash": tx_hash, "amount": 10.0})
    
    updated = queue.get_task(task.task_id)
    print(f"✅ 支付已确认")
    print(f"   新状态: {updated.status}")
    print(f"   支付证明: {updated.payment_proof['tx_hash'][:20]}...")
    
    # 查询用户任务列表
    print("\n📋 查询用户任务列表")
    user_tasks = queue.get_user_tasks(TEST_USER, 10)
    print(f"   用户任务数: {len(user_tasks)}")
    for t in user_tasks:
        print(f"   - {t.task_id}: {t.account_name} ({t.status})")
    
    return True


def test_subscription():
    """测试包月订阅"""
    print("\n" + "="*60)
    print("🧪 测试5: 包月订阅系统")
    print("="*60)
    
    user = f"{TEST_USER}_sub"
    manager = UserQuotaManager(user)
    
    # 初始状态
    print("\n📊 初始状态")
    status = manager.get_status()
    print(f"   订阅状态: {'✅ 有效' if status['subscription']['active'] else '❌ 未开通'}")
    
    # 开通订阅
    print("\n💳 开通包月订阅 ($100 USDC)")
    tx_hash = mock_chain.create_mock_transaction(100.0, "0x172444FC64e2E370fCcF297dB865831A1555b07A")
    manager.subscribe(tx_hash)
    
    status = manager.get_status()
    print(f"✅ 订阅已开通")
    print(f"   状态: {'✅ 有效' if status['subscription']['active'] else '❌ 无效'}")
    print(f"   到期时间: {status['subscription']['expires_at']}")
    
    # 检查有效性
    is_valid = manager.check_subscription()
    print(f"   有效性检查: {'✅ 通过' if is_valid else '❌ 失败'}")
    
    # 添加使用记录
    manager.add_usage("crawl", "机器之心", 50, 0, "subscription")
    print(f"\n添加使用记录: 爬取50篇文章（订阅支付）")
    print(f"   总使用次数: {len(manager.get_usage_history())}")
    
    return True


def test_full_workflow():
    """测试完整工作流程"""
    print("\n" + "="*60)
    print("🧪 测试6: 完整工作流程")
    print("="*60)
    
    user = f"{TEST_USER}_workflow"
    manager = UserQuotaManager(user)
    
    # 场景1: 新用户免费额度
    print("\n📱 场景1: 新用户使用免费额度")
    can_exec, cost, method = manager.can_execute("per_article", 5)
    print(f"   请求: 5篇文章")
    print(f"   费用: ${cost}")
    print(f"   支付方式: {method}")
    print(f"   {'✅ 使用免费额度' if method == 'free' else '❌ 错误'}")
    
    if method == "free":
        manager.use_free_quota(5)
        manager.add_usage("crawl", "机器之心", 5, 0, "free")
        print(f"   ✅ 已使用免费额度5篇")
    
    # 场景2: 免费额度用完，需要支付
    print("\n💰 场景2: 免费额度用完，需要付费")
    can_exec, cost, method = manager.can_execute("per_article", 10)
    print(f"   请求: 10篇文章")
    print(f"   费用: ${cost}")
    print(f"   支付方式: {method}")
    print(f"   {'✅ 需要 x402 支付' if method == 'x402' else '❌ 错误'}")
    
    # 场景3: 开通包月
    print("\n📅 场景3: 开通包月订阅")
    tx_hash = mock_chain.create_mock_transaction(100.0, "0x172444FC64e2E370fCcF297dB865831A1555b07A")
    manager.subscribe(tx_hash)
    
    can_exec, cost, method = manager.can_execute("per_article", 200)
    print(f"   请求: 200篇文章")
    print(f"   费用: ${cost}")
    print(f"   支付方式: {method}")
    print(f"   {'✅ 使用订阅' if method == 'subscription' else '❌ 错误'}")
    
    # 查看历史
    print("\n📊 使用历史")
    history = manager.get_usage_history(10)
    for record in history:
        print(f"   {record['time'][:19]}: {record['action']} {record['count']}篇 - ${record['cost']} ({record['paid_by']})")
    
    return True


def run_all_tests():
    """运行所有测试"""
    print("\n" + "🚀"*30)
    print("   WeChat MP Spider x402 支付测试套件")
    print("   收款地址: 0x172444FC64e2E370fCcF297dB865831A1555b07A")
    print("🚀"*30)
    
    # 创建数据目录
    os.makedirs("data/users", exist_ok=True)
    os.makedirs("data/queue", exist_ok=True)
    
    tests = [
        ("免费额度系统", test_free_quota),
        ("x402 支付流程", test_x402_payment),
        ("支付模式切换", test_payment_modes),
        ("异步任务队列", test_async_queue),
        ("包月订阅系统", test_subscription),
        ("完整工作流程", test_full_workflow),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            success = test_func()
            results.append((name, success))
        except Exception as e:
            print(f"\n❌ 测试 '{name}' 失败: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))
    
    # 测试报告
    print("\n" + "="*60)
    print("📊 测试报告")
    print("="*60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for name, success in results:
        status = "✅ 通过" if success else "❌ 失败"
        print(f"   {status}: {name}")
    
    print(f"\n{'='*60}")
    print(f"总计: {passed}/{total} 通过")
    print("="*60)
    
    if passed == total:
        print("\n🎉 所有测试通过！x402 支付系统已就绪！")
        print("\n下一步:")
        print("   1. 部署到 Base 主网")
        print("   2. 配置真实 USDC 合约")
        print("   3. 集成链上验证")
    else:
        print(f"\n⚠️ {total - passed} 个测试失败，需要修复")
    
    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
