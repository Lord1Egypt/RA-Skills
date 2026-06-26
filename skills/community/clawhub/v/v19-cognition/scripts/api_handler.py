import json, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from billing import get_price, verify_payment

def handle_request(task_type, content, depth=3, payment_credential=None):
    """处理Skill API请求"""
    # 1. 验证支付
    if payment_credential:
        payment_result = verify_payment(task_type, payment_credential)
        if payment_result['status'] != 'verified':
            return payment_result

    # 2. 获取定价
    price = get_price(task_type)
    if price is None:
        return {"status": "error", "message": "不支持的任务类型"}

    # 3. 返回分析结果（实际分析由V19-Cognition核心引擎完成）
    return {
        "status": "success",
        "task_type": task_type,
        "price": price,
        "depth": depth,
        "result": f"{task_type}分析已纳入数字大脑工厂处理队列，结果将通过回调地址返回。"
    }

if __name__ == '__main__':
    # 命令行测试
    task = sys.argv[1] if len(sys.argv) > 1 else "paper_review"
    content = sys.argv[2] if len(sys.argv) > 2 else "测试内容"
    result = handle_request(task, content)
    print(json.dumps(result, indent=2, ensure_ascii=False))
