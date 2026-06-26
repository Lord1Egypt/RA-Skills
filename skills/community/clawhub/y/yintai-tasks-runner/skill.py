"""
OpenClaw Task Runner Skill - 主 Skill 类
"""

import asyncio
import logging
from decimal import Decimal
from typing import Optional
from uuid import UUID

from .config import SkillConfig, load_config
from .api_client import TaskAPIClient, TaskDetail, AvailableTask
from .executor import TaskExecutor, TaskExecutionResult

logger = logging.getLogger(__name__)


class YintaiTasksRunnerSkill:
    """
    OpenClaw 任务抢单与执行 Skill

    功能：
    1. 每隔 x 秒轮询 bots 的任务接口
    2. 找到可接单的任务
    3. 尝试锁定任务（抢单）
    4. 执行任务
    5. 更新交付结果（.zip 格式 + 一段话）

    使用方式：
    ```python
    config = load_config(
        api_base_url="https://claw-dev.int-os.com",
        api_key="your_api_key",
        api_secret="your_api_secret",
        poll_interval_seconds=10,
    )
    skill = YintaiTasksRunnerSkill(config)

    # 一次性运行
    await skill.run_once()

    # 持续运行（轮询模式）
    await skill.run_forever()
    ```

    或者通过 CLI：
    ```bash
    python -m skills.yintai_tasks_runner --poll-interval 10
    ```
    """

    def __init__(self, config: Optional[SkillConfig] = None, **kwargs):
        """
        初始化 Skill

        Args:
            config: Skill配置对象，如果为None则从环境变量/参数加载
            **kwargs: 配置参数，会覆盖环境变量
        """
        self.config = config or load_config(**kwargs)
        self.api_client = TaskAPIClient(self.config)
        self.executor = TaskExecutor(self.config, self.api_client)
        self._running = False

    async def poll_and_grab_tasks(self) -> list[UUID]:
        """
        轮询可接单任务并尝试抢单

        Returns:
            抢单成功的任务ID列表
        """
        grabbed_task_ids = []

        # 获取可接单任务列表
        tasks, total = await self.api_client.get_available_tasks(
            page=1,
            page_size=self.config.page_size,
        )

        logger.info(f"发现 {total} 个可接单任务，拉取到 {len(tasks)} 个")

        if not tasks:
            return grabbed_task_ids

        # 按赏金排序（可选）
        if self.config.min_bounty is not None:
            tasks = [
                t for t in tasks if t.bounty >= Decimal(str(self.config.min_bounty))
            ]

        # 按分类过滤（可选）
        if self.config.categories:
            tasks = [t for t in tasks if t.category in self.config.categories]

        # 尝试抢单
        for task in tasks:
            try:
                success = await self.api_client.grab_task(task.id)
                if success:
                    logger.info(f"抢单成功: {task.id} - {task.title}")
                    grabbed_task_ids.append(task.id)
                else:
                    logger.debug(f"抢单失败（已被抢）: {task.id}")
            except Exception as e:
                logger.error(f"抢单异常: {task.id}, error={e}")

        return grabbed_task_ids

    async def execute_task(self, task_id: UUID) -> TaskExecutionResult:
        """
        执行单个任务

        Args:
            task_id: 任务ID

        Returns:
            执行结果
        """
        # 获取任务详情
        task_detail = await self.api_client.get_task_detail(task_id)
        if not task_detail:
            logger.error(f"无法获取任务详情: {task_id}")
            return TaskExecutionResult(success=False, error="无法获取任务详情")

        logger.info(f"开始执行任务: {task_detail.title} (ID: {task_id})")

        # 更新状态为进行中
        await self.api_client.update_task_status(task_id, "in_progress")
        logger.info(f"任务状态已更新为进行中: {task_id}")

        # 执行任务
        result = await self.executor.execute(task_detail)

        if result.success:
            # 状态已在 backend upload_deliverable 时自动更新为 completed
            logger.info(f"任务已完成: {task_id}")
            logger.info(f"交付物: {result.delivery_zip_path}")
            if result.upload_result:
                logger.info(f"上传结果: {result.upload_result}")
            logger.info(f"交付话语:\n{result.delivery_message}")
        else:
            # 更新状态为已取消
            await self.api_client.update_task_status(task_id, "cancelled")
            logger.error(f"任务执行失败: {task_id}, error={result.error}")

        return result

    async def run_once(self) -> list[TaskExecutionResult]:
        """
        运行一次（轮询 -> 抢单 -> 执行所有抢到的任务）

        Returns:
            所有抢单任务的执行结果列表
        """
        results = []

        # 1. 轮询并抢单
        grabbed_task_ids = await self.poll_and_grab_tasks()

        if not grabbed_task_ids:
            logger.info("本次轮询没有抢到任何任务")
            return results

        logger.info(f"成功抢到 {len(grabbed_task_ids)} 个任务")

        # 2. 依次执行任务
        for task_id in grabbed_task_ids:
            result = await self.execute_task(task_id)
            results.append(result)

        return results

    async def run_forever(self, max_iterations: Optional[int] = None):
        """
        持续运行（轮询模式）

        Args:
            max_iterations: 最大迭代次数，None表示无限循环
        """
        self._running = True
        iteration = 0

        logger.info(
            f"开始持续运行模式，轮询间隔={self.config.poll_interval_seconds}秒"
        )

        while self._running:
            iteration += 1
            logger.info(f"=== 第 {iteration} 次轮询 ===")

            try:
                await self.run_once()
            except Exception as e:
                logger.error(f"轮询异常: {e}", exc_info=True)

            # 检查是否达到最大迭代次数
            if max_iterations and iteration >= max_iterations:
                logger.info(f"达到最大迭代次数 {max_iterations}，停止运行")
                break

            # 等待下次轮询
            await asyncio.sleep(self.config.poll_interval_seconds)

        logger.info("持续运行模式结束")

    def stop(self):
        """停止持续运行"""
        self._running = False
        logger.info("收到停止信号")


# CLI 入口点
async def main():
    """CLI 入口"""
    import argparse

    parser = argparse.ArgumentParser(
        description="OpenClaw Task Runner Skill - 自动抢单并执行任务"
    )
    parser.add_argument(
        "--api-base-url",
        type=str,
        default=None,
        help="任务系统 API 地址",
    )
    parser.add_argument(
        "--api-key",
        type=str,
        default=None,
        help="API Key",
    )
    parser.add_argument(
        "--api-secret",
        type=str,
        default=None,
        help="API Secret",
    )
    parser.add_argument(
        "--poll-interval",
        type=int,
        default=None,
        help="轮询间隔（秒）",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=None,
        help="输出目录",
    )
    parser.add_argument(
        "--min-bounty",
        type=float,
        default=None,
        help="最低赏金阈值(元)",
    )
    parser.add_argument(
        "--categories",
        type=str,
        default=None,
        help="允许的任务分类(逗号分隔)",
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="只运行一次，不持续轮询",
    )

    args = parser.parse_args()

    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    # 加载配置
    categories = None
    if args.categories:
        categories = [c.strip() for c in args.categories.split(",") if c.strip()]

    config = load_config(
        api_base_url=args.api_base_url,
        api_key=args.api_key,
        api_secret=args.api_secret,
        poll_interval_seconds=args.poll_interval,
        output_dir=args.output_dir,
        min_bounty=args.min_bounty,
        categories=categories,
    )

    # 创建并运行 Skill
    skill = YintaiTasksRunnerSkill(config)

    if args.once:
        await skill.run_once()
    else:
        await skill.run_forever()


if __name__ == "__main__":
    asyncio.run(main())
