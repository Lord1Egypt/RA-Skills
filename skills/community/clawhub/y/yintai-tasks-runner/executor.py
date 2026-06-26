"""
OpenClaw Task Runner Skill - 任务执行器
"""

import os
import zipfile
import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional

from .api_client import TaskDetail, TaskAPIClient
from .config import SkillConfig


class TaskExecutionResult:
    """任务执行结果"""

    def __init__(
        self,
        success: bool,
        delivery_zip_path: Optional[str] = None,
        delivery_message: Optional[str] = None,
        upload_result: Optional[dict] = None,
        error: Optional[str] = None,
    ):
        self.success = success
        self.delivery_zip_path = delivery_zip_path
        self.delivery_message = delivery_message
        self.upload_result = upload_result
        self.error = error


class TaskExecutor:
    """任务执行器"""

    def __init__(self, config: SkillConfig, api_client: TaskAPIClient):
        self.config = config
        self.output_dir = Path(config.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.api_client = api_client

    async def execute(self, task: TaskDetail) -> TaskExecutionResult:
        """
        执行任务

        Args:
            task: 任务详情

        Returns:
            任务执行结果
        """
        try:
            # 生成交付物
            delivery_zip_path, delivery_message, result_description = await self._create_delivery(task)

            # 上传到任务系统
            upload_result = None
            try:
                upload_result = await self.api_client.upload_deliverable(
                    task_id=task.id,
                    result_description=result_description,
                    zip_file_path=delivery_zip_path,
                )
            except Exception as upload_err:
                # 上传失败不影响任务完成，只记录日志
                import logging
                logging.warning(f"上传交付物失败: {upload_err}")

            return TaskExecutionResult(
                success=True,
                delivery_zip_path=delivery_zip_path,
                delivery_message=delivery_message,
                upload_result=upload_result,
            )

        except Exception as e:
            return TaskExecutionResult(
                success=False,
                error=str(e),
            )

    async def _create_delivery(
        self, task: TaskDetail
    ) -> tuple[str, str, str]:
        """
        创建交付物

        Args:
            task: 任务详情

        Returns:
            (zip文件路径, 交付话语, 结果描述)
        """
        # 创建任务专属目录
        task_id_str = str(task.id)
        task_dir = self.output_dir / task_id_str
        task_dir.mkdir(parents=True, exist_ok=True)

        # 生成 metadata.json
        metadata = {
            "task_id": task_id_str,
            "title": task.title,
            "category": task.category,
            "bounty": str(task.bounty),
            "deadline": task.deadline.isoformat(),
            "status": "completed",
            "completed_at": datetime.utcnow().isoformat(),
            "assigned_claw_id": task.assigned_claw_id,
            "creator_id": task.creator_id,
        }

        metadata_path = task_dir / "metadata.json"
        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)

        # 生成 result.txt (任务执行结果说明)
        result_content = self._generate_result_content(task)
        result_path = task_dir / "result.txt"
        with open(result_path, "w", encoding="utf-8") as f:
            f.write(result_content)

        # 生成 output 目录 (存放具体执行产物)
        output_subdir = task_dir / f"output_{task_id_str}"
        output_subdir.mkdir(exist_ok=True)

        # 在 output 目录下创建一个占位文件，实际使用时这里会是真正的执行产物
        placeholder_file = output_subdir / "artifacts.txt"
        with open(placeholder_file, "w", encoding="utf-8") as f:
            f.write(f"# 任务执行产物\n")
            f.write(f"# 生成时间: {datetime.utcnow().isoformat()}\n")
            f.write(f"# 任务ID: {task_id_str}\n")

        # 创建 ZIP 文件
        zip_filename = f"delivery_{task_id_str}_{uuid.uuid4().hex[:8]}.zip"
        zip_path = self.output_dir / zip_filename

        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            # 添加 metadata.json
            zipf.write(metadata_path, arcname="metadata.json")
            # 添加 result.txt
            zipf.write(result_path, arcname="result.txt")
            # 添加 output 目录下的所有文件
            for root, dirs, files in os.walk(output_subdir):
                for file in files:
                    file_path = Path(root) / file
                    arcname = f"output_{task_id_str}/{file}"
                    zipf.write(file_path, arcname=arcname)

        # 清理临时目录
        import shutil

        shutil.rmtree(task_dir, ignore_errors=True)

        # 生成交付话语
        delivery_message = self._generate_delivery_message(task, zip_filename)

        return str(zip_path), delivery_message, result_content

    def _generate_result_content(self, task: TaskDetail) -> str:
        """生成结果说明内容"""
        content_lines = [
            "=" * 60,
            "任务执行报告",
            "=" * 60,
            "",
            f"任务ID: {task.id}",
            f"任务标题: {task.title}",
            f"任务分类: {task.category}",
            f"赏金: {task.bounty} 元",
            f"截止时间: {task.deadline.isoformat()}",
            f"创建时间: {task.created_at.isoformat()}",
            f"接单Bot: {task.assigned_claw_id or '-'}",
            f"完成时间: {datetime.utcnow().isoformat()}",
            "",
            "-" * 60,
            "任务描述:",
            "-" * 60,
        ]

        if task.description:
            content_lines.append(task.description)
        else:
            content_lines.append("(无详细描述)")

        content_lines.extend(
            [
                "",
                "-" * 60,
                "执行状态: 已完成",
                "-" * 60,
                "",
                "交付物:",
                f"  - 详情见附件 ZIP 文件",
                "",
                "=" * 60,
            ]
        )

        return "\n".join(content_lines)

    def _generate_delivery_message(self, task: TaskDetail, zip_filename: str) -> str:
        """生成交付话语"""
        message_template = self.config.delivery_message

        # 格式化消息
        message = f"""任务已完成！

📋 任务ID: {task.id}
📝 任务标题: {task.title}
📁 交付物: {zip_filename}

{message_template}

如有疑问，请联系管理员。"""

        return message
