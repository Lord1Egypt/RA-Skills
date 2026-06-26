"""
任务编排器
"""
import asyncio
from typing import List, Dict, Any
from pydantic import BaseModel
from src.models.scene import SceneTask
from src.services.ha_client import HAClient


class TaskResult(BaseModel):
    """任务执行结果"""
    entity: str
    service: str
    success: bool
    result: Any = None
    error: str = ""


class OrchestratorResult(BaseModel):
    """编排结果"""
    succeeded: List[TaskResult]
    failed: List[TaskResult]
    markdown: str


class TaskOrchestrator:
    """异步任务编排器"""
    
    def __init__(self, ha_client: HAClient):
        self.ha_client = ha_client
    
    async def execute_tasks(self, tasks: List[SceneTask]) -> OrchestratorResult:
        """并发执行任务"""
        # 并发执行所有任务
        results = await asyncio.gather(
            *[self._execute_task(task) for task in tasks],
            return_exceptions=True
        )
        
        # 分类成功/失败
        succeeded = []
        failed = []
        
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                failed.append(TaskResult(
                    entity=tasks[i].entity,
                    service=tasks[i].service,
                    success=False,
                    error=str(result)
                ))
            elif result.get('success'):
                succeeded.append(TaskResult(
                    entity=tasks[i].entity,
                    service=tasks[i].service,
                    success=True,
                    result=result
                ))
            else:
                failed.append(TaskResult(
                    entity=tasks[i].entity,
                    service=tasks[i].service,
                    success=False,
                    error=result.get('error', 'Unknown error')
                ))
        
        # 生成 Markdown
        markdown = self._generate_markdown(succeeded, failed)
        
        return OrchestratorResult(
            succeeded=succeeded,
            failed=failed,
            markdown=markdown
        )
    
    async def _execute_task(self, task: SceneTask) -> dict:
        """执行单个任务"""
        try:
            # 解析 domain 和 service
            parts = task.service.split('.')
            if len(parts) == 2:
                domain, service = parts
            else:
                domain = task.entity.split('.')[0] if '.' in task.entity else task.entity
                service = task.service
            
            # 调用 HA
            result = await self.ha_client.call_service(
                domain=domain,
                service=service,
                entity_id=task.entity,
                **task.data
            )
            
            return {"success": True, "result": result}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _generate_markdown(
        self, 
        succeeded: List[TaskResult], 
        failed: List[TaskResult]
    ) -> str:
        """生成 Markdown 响应"""
        lines = []
        
        if succeeded:
            lines.append("✅ 已执行:")
            for r in succeeded:
                lines.append(f"- {r.entity}: {r.service}")
        
        if failed:
            lines.append("\n⚠️ 执行失败:")
            for r in failed:
                lines.append(f"- {r.entity}: {r.error}")
        
        return "\n".join(lines) if lines else "执行完成"
