import logging
from .base_agent import BaseAgent


class PlannerAgent(BaseAgent):
    """
    Planner Agent: receives user request, generates task DAG.
    Input:  user.request
    Output: plan.task.graph -> DrafterAgent
    """

    async def handle_message(self, message: dict):
        if message["type"] == "user.request":
            user_text = message["payload"].get("text", "")
            correlation_id = message.get("correlation_id")
            dag = self._create_dag(user_text)
            await self.send(
                to="DrafterAgent",
                msg_type="plan.task.graph",
                payload=dag,
                correlation_id=correlation_id,
            )

    def _create_dag(self, text: str) -> dict:
        return {
            "nodes": [
                {
                    "id": "node1",
                    "description": f"处理: {text}",
                    "depends_on": [],
                    "complexity": 1,
                }
            ],
            "entry_points": ["node1"],
            "exit_points": ["node1"],
        }
