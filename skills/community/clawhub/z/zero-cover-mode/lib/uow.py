"""Unit of Work — 事务管理模式

提供 UnitOfWork（本地事务）和 SagaTransaction（分布式补偿事务）。
P3-FIX: 修复双重 rollback 问题 — __exit__ 检查 _rolled_back 标志，
避免手动 rollback() 后 __exit__ 再次触发回滚。
"""

import logging, os, shutil
from typing import Callable, List, Tuple

log = logging.getLogger("uow")


class UnitOfWork:
    """本地事务 — 注册 do/undo 操作对

    用法:
        with UnitOfWork() as uow:
            uow.register(do_fn, undo_fn)
            # ... 更多操作
            uow.commit()  # 成功时清理注册表
            # 如果异常，__exit__ 自动回滚（仅当未 commit 且未 rollback）
    """

    def __init__(self):
        self._actions: List[Tuple[Callable, Callable]] = []
        self._committed = False
        self._rolled_back = False  # P3-FIX: 防止双重 rollback

    def register(self, do: Callable, undo: Callable):
        """注册一对 do/undo 操作"""
        self._actions.append((do, undo))

    def commit(self):
        """提交事务：清空 undo 注册表（do 操作已执行，无需重复）"""
        self._committed = True
        self._actions.clear()

    def rollback(self):
        """回滚事务：逆序执行所有 undo"""
        if self._committed or self._rolled_back:
            return
        self._rolled_back = True
        for _, undo in reversed(self._actions):
            try:
                undo()
            except Exception as e:
                log.error("rollback undo 失败: %s", e)
        self._actions.clear()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # P3-FIX: 只在异常发生且未 commit 且未手动 rollback 时才回滚
        if exc_type is not None and not self._committed and not self._rolled_back:
            self.rollback()
        return False  # 不吞异常


def undo_rmdir(p: str) -> Callable:
    """返回删除目录的 undo 函数"""
    def _u():
        if os.path.exists(p):
            shutil.rmtree(p)
    _u.__name__ = f"u_rmdir_{os.path.basename(p)}"
    return _u


def undo_rmfile(p: str) -> Callable:
    """返回删除文件的 undo 函数"""
    def _u():
        if os.path.exists(p):
            os.remove(p)
    _u.__name__ = f"u_rmfile_{os.path.basename(p)}"
    return _u


def composite_undo(*undos: Callable) -> Callable:
    """组合多个 undo 为一个"""
    def _u():
        for uf in reversed(undos):
            try:
                uf()
            except Exception as e:
                log.warning("composite_undo: %s", e)
    _u.__name__ = "u_composite"
    return _u


class SagaTransaction:
    """分布式 Saga 事务 — 每个节点有独立的 compensate 操作

    用法:
        saga = SagaTransaction()
        saga.add_node("step1", do_step1, compensate_step1)
        saga.add_node("step2", do_step2, compensate_step2)
        saga.execute()  # 按顺序执行，失败时逆序补偿
    """

    def __init__(self):
        self._nodes: List[Tuple[str, Callable, Callable]] = []
        self._committed = False

    def add_node(self, name: str, do: Callable, compensate: Callable):
        """添加一个事务节点"""
        self._nodes.append((name, do, compensate))

    def execute(self):
        """按顺序执行，失败时逆序补偿"""
        executed: List[Tuple[str, Callable]] = []
        for name, do, compensate in self._nodes:
            try:
                do()
                executed.append((name, compensate))
            except Exception as e:
                log.error("Saga 节点 %s 失败，开始补偿 %d 个已完成节点", name, len(executed))
                for ename, comp in reversed(executed):
                    try:
                        comp()
                    except Exception as ce:
                        log.warning("Saga 补偿 %s 失败: %s", ename, ce)
                raise
        self._committed = True
