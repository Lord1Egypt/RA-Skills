# -*- coding: utf-8 -*-
"""
SkillPilot - 智能技能路由引擎
降级处理器
"""

import time
from typing import List, Dict, Optional
from .models import SkillRequest, SkillResult, CircuitBreaker, CircuitState
from .registry import SkillRegistry


class FallbackHandler:
    """降级处理器"""
    
    def __init__(self, registry: SkillRegistry, engine=None):
        self.registry = registry
        self.engine = engine  # ExecutionEngine 引用 (延迟绑定)
        self.max_retries = 3
        self.circuit_breakers: Dict[str, CircuitBreaker] = {}
    
    def set_engine(self, engine):
        """设置执行引擎引用"""
        self.engine = engine
    
    def execute_with_fallback(self, request: SkillRequest, ranked_skills: List[str]) -> SkillResult:
        """
        执行技能调用，自动降级
        返回：调用结果
        """
        last_error = None
        tried_skills = []
        fallback_count = 0
        start_time = time.time()
        
        primary_skill = ranked_skills[0] if ranked_skills else None
        
        for i, skill_name in enumerate(ranked_skills):
            # 检查熔断器
            if self._is_circuit_open(skill_name):
                print(f"  ⚡ 技能 {skill_name} 熔断中，跳过")
                continue
            
            tried_skills.append(skill_name)
            
            try:
                # 执行技能调用
                print(f"  → 调用技能：{skill_name}")
                result = self._call_skill(skill_name, request)
                
                # 验证结果
                if self._validate_result(result):
                    # 成功：更新指标
                    response_time = (time.time() - start_time) * 1000
                    self._record_success(skill_name, response_time)
                    
                    return SkillResult(
                        success=True,
                        content=result.get('content'),
                        used_skill=skill_name,
                        primary_skill=primary_skill,
                        tried_skills=tried_skills,
                        fallback_count=fallback_count,
                        response_time=response_time,
                        metadata=result.get('metadata', {})
                    )
                else:
                    # 结果无效：视为失败
                    error_msg = "结果验证失败"
                    print(f"  ✗ {skill_name}: {error_msg}")
                    self._record_failure(skill_name, error_msg)
                    
            except Exception as e:
                last_error = str(e)
                print(f"  ✗ {skill_name} 失败：{last_error}")
                self._record_failure(skill_name, last_error)
                
                # 判断是否继续降级
                if i >= self.max_retries - 1:
                    print(f"  ⚠ 已达最大重试次数 {self.max_retries}")
                    break
                
                # 检查是否有下一个技能
                if i >= len(ranked_skills) - 1:
                    print(f"  ⚠ 已无备用技能")
                    break
                
                fallback_count += 1
                print(f"  ↓ 降级到下一个技能...")
        
        # 全部失败
        response_time = (time.time() - start_time) * 1000
        return SkillResult(
            success=False,
            error=f"所有技能失败：{last_error}",
            primary_skill=primary_skill,
            tried_skills=tried_skills,
            fallback_count=fallback_count,
            response_time=response_time
        )
    
    def _call_skill(self, skill_name: str, request: SkillRequest) -> Dict:
        """调用技能 (通过执行引擎)"""
        if not self.engine:
            raise Exception("执行引擎未设置")
        
        return self.engine.call_skill(skill_name, request)
    
    def _validate_result(self, result: Dict) -> bool:
        """验证结果有效性"""
        if not result:
            return False
        
        # 检查是否有内容或明确的成功标志
        if result.get('success') is True:
            return True
        
        if result.get('content'):
            return True
        
        return False
    
    def _is_circuit_open(self, skill_name: str) -> bool:
        """检查熔断器状态"""
        if skill_name not in self.circuit_breakers:
            return False
        
        cb = self.circuit_breakers[skill_name]
        
        if cb.state == CircuitState.OPEN:
            # 检查是否可以半开
            if time.time() - cb.last_failure > cb.cooldown:
                cb.state = CircuitState.HALF_OPEN
                print(f"  🔄 技能 {skill_name} 熔断冷却结束，进入半开状态")
                return False
            return True
        
        return False
    
    def _record_success(self, skill_name: str, response_time: float):
        """记录成功"""
        meta = self.registry.get_skill(skill_name)
        if not meta:
            return
        
        # 更新成功率 (滑动平均)
        meta.success_rate = (meta.success_rate * meta.total_calls + 1) / (meta.total_calls + 1)
        meta.total_calls += 1
        
        # 更新健康分数
        meta.health_score = min(100, meta.health_score + 1)
        
        # 更新平均响应时间
        meta.avg_response_time = (meta.avg_response_time * 0.9 + response_time * 0.1)
        
        # 重置熔断器
        if skill_name in self.circuit_breakers:
            cb = self.circuit_breakers[skill_name]
            if cb.state == CircuitState.HALF_OPEN:
                cb.half_open_successes += 1
                if cb.half_open_successes >= 1:
                    cb.state = CircuitState.CLOSED
                    cb.failure_count = 0
                    cb.half_open_successes = 0
                    print(f"  ✓ 技能 {skill_name} 恢复正常状态")
    
    def _record_failure(self, skill_name: str, error: str):
        """记录失败"""
        meta = self.registry.get_skill(skill_name)
        if not meta:
            return
        
        # 更新成功率
        meta.success_rate = (meta.success_rate * meta.total_calls) / (meta.total_calls + 1)
        meta.total_calls += 1
        meta.failed_calls += 1
        
        # 更新健康分数
        meta.health_score = max(0, meta.health_score - 5)
        
        # 更新熔断器
        if skill_name not in self.circuit_breakers:
            self.circuit_breakers[skill_name] = CircuitBreaker()
        
        cb = self.circuit_breakers[skill_name]
        cb.failure_count += 1
        cb.last_failure = time.time()
        
        # 连续失败 5 次，打开熔断器
        if cb.failure_count >= 5 and cb.state == CircuitState.CLOSED:
            cb.state = CircuitState.OPEN
            print(f"  ⚡ 技能 {skill_name} 熔断 (连续失败{cb.failure_count}次)，冷却{cb.cooldown}秒")
        elif cb.state == CircuitState.HALF_OPEN:
            cb.state = CircuitState.OPEN
            cb.last_failure = time.time()
            print(f"  ⚡ 技能 {skill_name} 半开测试失败，重新熔断")
    
    def get_circuit_status(self) -> Dict[str, Dict]:
        """获取所有熔断器状态"""
        return {
            name: cb.__dict__
            for name, cb in self.circuit_breakers.items()
        }
    
    def reset_circuit(self, skill_name: str = None):
        """重置熔断器"""
        if skill_name:
            if skill_name in self.circuit_breakers:
                del self.circuit_breakers[skill_name]
                print(f"✓ 已重置技能 {skill_name} 的熔断器")
        else:
            self.circuit_breakers.clear()
            print("✓ 已重置所有熔断器")
