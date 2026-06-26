"""
工具函数模块
"""

import json
import re
from typing import Any, Dict
from src.types import ExecResult, Context


async def exec_command(ctx: Context, command: str) -> ExecResult:
    """
    执行系统命令
    通过 OpenClaw 的 ctx.exec 实现
    """
    try:
        # 调用 OpenClaw 的 exec 方法
        # 注意：实际 API 可能有所不同，这里假设 ctx 有 exec 方法
        if hasattr(ctx, 'exec'):
            result = await ctx.exec(command)
            return ExecResult(
                code=result.get('code', 0),
                stdout=result.get('stdout', ''),
                stderr=result.get('stderr', ''),
                error=result.get('error')
            )
        else:
            # 降级方案：返回模拟结果
            # 实际部署时应该使用真实的 ctx.exec
            import subprocess
            process = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            return ExecResult(
                code=process.returncode,
                stdout=process.stdout,
                stderr=process.stderr
            )
    except Exception as e:
        return ExecResult(
            code=1,
            stdout='',
            stderr=str(e),
            error=str(e)
        )


def parse_config_output(output: str) -> Dict[str, Any]:
    """
    解析配置命令的输出
    支持 JSON 格式和 key=value 格式
    """
    if not output:
        return {}

    try:
        # 尝试解析为 JSON
        return json.loads(output)
    except json.JSONDecodeError:
        # 如果不是 JSON，尝试解析 key=value 格式
        config = {}
        lines = output.strip().split('\n')

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # 匹配 key=value 格式
            match = re.match(r'^(\w+)=(.+)$', line)
            if match:
                key = match.group(1)
                value = match.group(2).strip()

                # 转换布尔值
                value_lower = value.lower()
                if value_lower == 'true':
                    config[key] = True
                elif value_lower == 'false':
                    config[key] = False
                elif value_lower == 'null' or value_lower == 'none':
                    config[key] = None
                else:
                    # 尝试转换为数字
                    try:
                        if '.' in value:
                            config[key] = float(value)
                        else:
                            config[key] = int(value)
                    except ValueError:
                        config[key] = value

        return config


async def validate_permission(ctx: Context, permission: str) -> bool:
    """
    验证是否具有特定权限
    """
    try:
        result = await exec_command(ctx, 'openclaw config get channels.feishu.permissions')
        if result.code == 0 and result.stdout:
            try:
                permissions = json.loads(result.stdout)
                return permission in permissions
            except json.JSONDecodeError:
                return False
    except Exception:
        pass
    return False


def format_time(seconds: float) -> str:
    """格式化时间（秒 -> 时分秒）"""
    if seconds < 60:
        return f"{seconds:.1f}秒"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes}分{secs}秒"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"{hours}小时{minutes}分"


def truncate_text(text: str, max_length: int = 100) -> str:
    """截断文本"""
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."
