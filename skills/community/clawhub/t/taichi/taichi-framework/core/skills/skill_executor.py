import asyncio
import subprocess
import shlex
from typing import Dict, Any, Optional


class SkillExecutor:
    """
    Executes skills based on their executor type.
    Currently supports 'subprocess' type with whitelist enforcement.
    """

    def __init__(self, skill_registry):
        self.registry = skill_registry

    async def execute(self, skill_name: str, params: dict) -> Dict[str, Any]:
        """Execute a skill by name with given params."""
        skill_def = self.registry.get(skill_name)
        if not skill_def:
            return {"status": "error", "error": f"Skill '{skill_name}' not found"}

        executor_type = skill_def["executor"].get("type", "subprocess")

        if executor_type == "subprocess":
            return await self._execute_subprocess(skill_def, params)
        else:
            return {"status": "error", "error": f"Unsupported executor type: {executor_type}"}

    async def _execute_subprocess(self, skill_def: Dict, params: Dict) -> Dict[str, Any]:
        """Execute via subprocess with whitelist check."""
        allowed_commands = skill_def.get("allowed_commands", [])
        allowed_paths = skill_def.get("allowed_paths", [])
        timeout_ms = skill_def["executor"].get("timeout_ms", 30000)

        # Build command from template
        template = skill_def["executor"].get("command", "")
        command = self._build_command(template, params)

        # Whitelist check
        if allowed_commands:
            first_word = shlex.split(command)[0] if command else ""
            if first_word not in allowed_commands:
                return {
                    "status": "error",
                    "error": f"Command '{first_word}' not in whitelist: {allowed_commands}",
                }

        try:
            proc = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout_b, stderr_b = await asyncio.wait_for(
                proc.communicate(), timeout=timeout_ms / 1000
            )
            return {
                "status": "success",
                "data": {
                    "stdout": stdout_b.decode(),
                    "stderr": stderr_b.decode(),
                    "exit_code": proc.returncode,
                },
            }
        except asyncio.TimeoutError:
            try:
                proc.kill()
            except Exception:
                pass
            return {"status": "error", "error": "Execution timeout"}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def _build_command(self, template: str, params: Dict) -> str:
        """Simple template substitution: {{key}} -> value."""
        result = template
        for k, v in params.items():
            result = result.replace(f"{{{{{k}}}}}", str(v))
        return result
