#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Spider API with x402 Payment
"""

import os
import sys
import json
from typing import Dict, Any, Optional

# 动态添加当前目录到路径
_current_dir = os.path.dirname(os.path.abspath(__file__))
if _current_dir not in sys.path:
    sys.path.insert(0, _current_dir)

from x402_core import X402Processor, X402PaymentProof, X402PaymentRequired
from quota_manager import UserQuotaManager
from async_queue import AsyncTaskQueue
from wechat_mp_crawler import crawl_account_articles


class WeChatSpiderAPI:
    """微信公众号爬虫 API"""
    
    def __init__(self):
        self.x402 = X402Processor()
        self.queue = AsyncTaskQueue()
        self.queue.start_worker(self._do_crawl)
    
    def _do_crawl(self, account_name: str, max_articles: int):
        return crawl_account_articles(account_name, max_articles)
    
    def get_user_status(self, user_id: str) -> Dict[str, Any]:
        manager = UserQuotaManager(user_id)
        return manager.get_status()
    
    def crawl_with_free_quota(self, user_id: str, account_name: str, max_articles: int) -> Dict[str, Any]:
        manager = UserQuotaManager(user_id)
        quota = manager.get_free_quota()
        
        if quota.remaining < max_articles:
            return {"success": False, "error": f"免费额度不足", "free_remaining": quota.remaining}
        
        try:
            result = self._do_crawl(account_name, max_articles)
            manager.use_free_quota(len(result))
            manager.add_usage("crawl", account_name, len(result), 0, "free")
            
            return {
                "success": True,
                "articles": result,
                "count": len(result),
                "cost": 0,
                "paid_by": "free",
                "free_remaining": quota.remaining - len(result),
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def crawl_realtime(self, user_id: str, account_name: str, max_articles: int, payment_token: Optional[str] = None) -> Dict[str, Any]:
        manager = UserQuotaManager(user_id)
        can_exec, cost, method = manager.can_execute("per_article", max_articles)
        
        if not can_exec:
            return {"success": False, "error": "无法执行"}
        
        if method == "free":
            return self.crawl_with_free_quota(user_id, account_name, max_articles)
        
        if method == "subscription":
            result = self._do_crawl(account_name, max_articles)
            manager.add_usage("crawl", account_name, len(result), 0, "subscription")
            return {"success": True, "articles": result, "count": len(result), "cost": 0, "paid_by": "subscription"}
        
        if not payment_token:
            price = self.x402.calculate_price("per_article", max_articles)
            request = self.x402.create_payment_request(user_id, "article", f"{account_name}_{max_articles}", price)
            raise X402PaymentRequired(request)
        
        proof = X402PaymentProof.from_token(payment_token)
        price = self.x402.calculate_price("per_article", max_articles)
        request = self.x402.create_payment_request(user_id, "article", f"{account_name}_{max_articles}", price)
        
        if not self.x402.verify_payment(proof, request):
            return {"success": False, "error": "支付验证失败"}
        
        result = self._do_crawl(account_name, max_articles)
        self.x402.confirm_payment(proof)
        manager.add_usage("crawl", account_name, len(result), price, "x402", proof.tx_hash)
        
        return {"success": True, "articles": result, "count": len(result), "cost": price, "paid_by": "x402", "tx_hash": proof.tx_hash}
    
    def crawl_async(self, user_id: str, account_name: str, max_articles: int, payment_token: Optional[str] = None) -> Dict[str, Any]:
        manager = UserQuotaManager(user_id)
        if manager.check_subscription():
            task = self.queue.create_task(user_id, account_name, max_articles, "subscription", 0)
            self.queue.confirm_payment(task.task_id, {"type": "subscription"})
            return {"success": True, "mode": "async", "task_id": task.task_id, "message": "任务已提交"}
        
        price = self.x402.calculate_price("per_account")
        
        if not payment_token:
            request = self.x402.create_payment_request(user_id, "account", account_name, price)
            task = self.queue.create_task(user_id, account_name, max_articles, "async", price)
            raise X402PaymentRequired(request)
        
        proof = X402PaymentProof.from_token(payment_token)
        request = self.x402.create_payment_request(user_id, "account", account_name, price)
        
        if not self.x402.verify_payment(proof, request):
            return {"success": False, "error": "支付验证失败"}
        
        task = self.queue.create_task(user_id, account_name, max_articles, "async", price)
        self.queue.confirm_payment(task.task_id, {"tx_hash": proof.tx_hash})
        self.x402.confirm_payment(proof)
        
        return {"success": True, "mode": "async", "task_id": task.task_id, "message": "支付成功"}
    
    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        task = self.queue.get_task(task_id)
        if not task:
            return {"success": False, "error": "任务不存在"}
        return {"success": True, "task_id": task.task_id, "status": task.status, "account": task.account_name}
    
    def subscribe_monthly(self, user_id: str, payment_token: str) -> Dict[str, Any]:
        manager = UserQuotaManager(user_id)
        proof = X402PaymentProof.from_token(payment_token)
        price = self.x402.calculate_price("monthly")
        request = self.x402.create_payment_request(user_id, "subscription", "monthly", price)
        
        if not self.x402.verify_payment(proof, request):
            return {"success": False, "error": "支付验证失败"}
        
        manager.subscribe(proof.tx_hash)
        self.x402.confirm_payment(proof)
        
        return {"success": True, "message": "包月订阅开通成功", "expires_at": manager.get_subscription().expires_at}


# 延迟初始化
_api_instance = None

def get_api() -> WeChatSpiderAPI:
    global _api_instance
    if _api_instance is None:
        _api_instance = WeChatSpiderAPI()
    return _api_instance
