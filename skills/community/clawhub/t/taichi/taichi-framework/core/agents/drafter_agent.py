from .base_agent import BaseAgent


class DrafterAgent(BaseAgent):
    """
    Drafter Agent: receives DAG, generates detailed task plan for each node.
    Input:  plan.task.graph
    Output: draft.complete -> ValidatorAgent
    """

    async def handle_message(self, message: dict):
        if message["type"] == "plan.task.graph":
            dag = message["payload"]
            correlation_id = message.get("correlation_id")

            tasks = []
            for node in dag.get("nodes", []):
                tasks.append(
                    {
                        "task_id": node["id"],
                        "skill": "bash_executor",
                        "params": {"command": f"echo 'Executing: {node['description']}'"},
                        "expected_output": {"stdout": "string"},
                        "timeout": 30,
                        "retry": 2,
                    }
                )

            await self.send(
                to="ValidatorAgent",
                msg_type="draft.complete",
                payload={"plan_id": correlation_id, "tasks": tasks},
                correlation_id=correlation_id,
            )
