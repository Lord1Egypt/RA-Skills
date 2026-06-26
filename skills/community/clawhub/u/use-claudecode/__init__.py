import subprocess
import os
import shutil

class ClaudeCLISkill:
    """
    Universal MCP-compatible Skill to delegate complex coding tasks and interact with the local Claude CLI.
    Provides local terminal execution, file system modification, and deep codebase analysis.
    Keywords: code refactoring, large scale code generation, terminal execution, bash shell, run tests, local environment, bypass token limit.
    """
    def __init__(self, workspace_path: str = None):
        self.workspace_path = workspace_path
        
    def talk_to_claude(self, message: str, is_new_session: bool = False, project_path: str = None) -> str:
        """
        Execute a prompt against the Claude CLI to read, write, fix code, or execute terminal commands.
        Returns the raw terminal output so the Agent can observe the progress.
        Use for code refactoring, codebase analysis, bash execution, or debugging errors.
        
        Args:
            message (str): The instructions for Claude CLI.
            is_new_session (bool): Set to True to start a fresh sequence, False to append '--continue'.
            project_path (str): Optional absolute path to execute Claude in. Defaults to the skill's initialized workspace.
        """
        cwd = project_path or self.workspace_path
        if not cwd or not os.path.exists(cwd):
            return f"Error: Project path '{cwd}' does not exist or is not specified."
            
        cmd = ["claude"]
        cmd.extend(["--permission-mode", "bypassPermissions"]) 
        cmd.extend(["--print"]) 
        
        if not is_new_session:
            cmd.append("--continue")
            
        cmd.append(f'"{message}"')
        env = os.environ.copy()
        
        # Check if claude CLI is installed
        if shutil.which("claude") is None:
            return (
                "Error: Claude Code CLI is not installed or not in the system's PATH.\n"
                "Please install it globally using npm: `npm install -g @anthropic-ai/claude-code`\n"
                "Or follow the official documentation at https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview"
            )
        
        
        try:
            if os.name == 'nt':
                ps_cmd = " ".join(cmd)
                full_ps_cmd = f"[Console]::OutputEncoding = [System.Text.Encoding]::UTF8; {ps_cmd}"
                result = subprocess.run(
                    ["powershell", "-Command", full_ps_cmd],
                    capture_output=True,
                    text=True,
                    encoding='utf-8',
                    errors='replace',
                    cwd=cwd,
                    env=env,
                    timeout=600 
                )
            else:
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    encoding='utf-8',
                    errors='replace',
                    cwd=cwd,
                    env=env,
                    timeout=600
                )
                
            output_log = []
            if result.stdout:
                output_log.append("--- Claude CLI Output ---")
                output_log.append(result.stdout)
                
            if result.returncode != 0:
                output_log.append(f"\n--- Claude CLI exited with code {result.returncode} ---")
                if result.stderr:
                    output_log.append(f"\n--- Subprocess Error ---\n{result.stderr}")
                    
            if not output_log:
                return "Command executed but produced no output."
                
            return "\n".join(output_log)
            
        except subprocess.TimeoutExpired:
            return "Error: Claude CLI execution timed out after 600 seconds."
        except Exception as e:
            return f"Error executing Claude: {str(e)}"
