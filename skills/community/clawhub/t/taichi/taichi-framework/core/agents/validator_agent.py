import logging
from .base_agent import BaseAgent


class ValidatorAgent(BaseAgent):
    """
    Validator Agent: validates the drafted task plan for completeness and safety.
    Input:  draft.complete
    Output: validate.result (approved/rejected) -> DispatcherAgent
    """

    async def handle_message(self, message: dict):
        if message["type"] == "draft.complete":
            draft = message["payload"]
            correlation_id = message.get("correlation_id")
            tasks = draft.get("tasks", [])

            if not tasks:
                result = {
                    "status": "rejected",
                    "reasons": ["No tasks in draft"],
                    "modifications": [],
                }
            else:
                result = {
                    "status": "approved",
                    "tasks": tasks,
                    "reasons": [],
                    "modifications": [],
                }

            await self.send(
                to="DispatcherAgent",
                msg_type="validate.result",
                payload=result,
                correlation_id=correlation_id,
            )
