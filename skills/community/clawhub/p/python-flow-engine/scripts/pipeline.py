"""
pipeline.py — Lightweight Python flow orchestration library.

A minimal pipeline engine supporting serial, parallel, and conditional
execution of processing nodes. No external dependencies required.

Core concepts:
  Node      — A single processing step wrapping a callable
  Pipeline  — Orchestrates nodes and their connections
  Operators — >> (serial), // (parallel), | (conditional)

Example:
    from pipeline import Node, Pipeline

    def double(x): return x * 2
    def add_one(x): return x + 1

    pipe = Pipeline()
    n1 = Node(double, name="double")
    n2 = Node(add_one, name="add_one")
    pipe.add_node(n1)
    pipe.add_node(n2)
    n1 >> n2
    result = pipe.run(n1, 5)  # 5*2+1 = 11
"""

import threading
import time
import functools
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional, Tuple


class NodeStatus(Enum):
    """Execution status for a Node."""
    PENDING = auto()
    RUNNING = auto()
    SUCCESS = auto()
    FAILED = auto()
    TIMEOUT = auto()
    SKIPPED = auto()


class Node:
    """A single processing step in a pipeline.

    Args:
        fn: The callable to execute. Receives (context, input_data) where
            context is a dict shared across the pipeline run.
        name: Human-readable label for this node.
        timeout: Maximum execution time in seconds (None = no limit).
        retry: Number of additional attempts on failure (0 = no retry).
        condition: Optional callable(context, data) -> bool. If provided,
            the node runs only when condition returns True (for | operator).
    """

    def __init__(
        self,
        fn: Callable,
        name: str = "",
        timeout: Optional[float] = None,
        retry: int = 0,
        condition: Optional[Callable[..., bool]] = None,
    ):
        self.fn = fn
        self.name = name or getattr(fn, "__name__", "unnamed")
        self.timeout = timeout
        self.retry = retry
        self.condition = condition
        # Connection lists
        self._serial_next: List["Node"] = []   # >> serial successors
        self._parallel: List["Node"] = []       # // parallel peers
        self._conditional: List[Tuple["Node", Optional[Callable]]] = []  # | conditional successors
        # Run state (reset on each run)
        self._status = NodeStatus.PENDING
        self._result: Any = None
        self._error: Optional[Exception] = None
        self._duration: float = 0.0

    # --- Operator overloads ---

    def __rshift__(self, other: "Node") -> "Node":
        """Serial connection: self >> other means self runs, then other runs."""
        self._serial_next.append(other)
        return other

    def __floordiv__(self, other: "Node") -> "Node":
        """Parallel connection: self // other means both run concurrently."""
        self._parallel.append(other)
        other._parallel.append(self)  # bidirectional link
        return other

    def __or__(self, other: "Node") -> "Node":
        """Conditional connection: self | other means the pipeline decides
        whether to run other based on self's output or a condition."""
        self._conditional.append((other, None))
        return other

    # --- Internal ---

    def reset(self):
        """Reset run state so the node can be reused."""
        self._status = NodeStatus.PENDING
        self._result = None
        self._error = None
        self._duration = 0.0

    def __repr__(self) -> str:
        return f"Node({self.name}, status={self._status.name})"


class Pipeline:
    """Orchestrates a graph of Node instances.

    Handles execution routing: serial (>>), parallel (//), and
    conditional (|) connections.
    """

    def __init__(self):
        self._nodes: Dict[str, Node] = {}

    def add_node(self, node: Node) -> Node:
        """Register a node with the pipeline."""
        self._nodes[node.name] = node
        return node

    def get_node(self, name: str) -> Optional[Node]:
        """Retrieve a registered node by name."""
        return self._nodes.get(name)

    @property
    def nodes(self) -> List[Node]:
        return list(self._nodes.values())

    def connect(
        self,
        from_node: Node,
        to_node: Node,
        mode: str = "serial",
        condition: Optional[Callable] = None,
    ):
        """Explicitly connect two nodes.

        Args:
            from_node: Source node.
            to_node: Target node.
            mode: "serial" (>>), "parallel" (//), or "conditional" (|).
            condition: Callable(context, data) -> bool for conditional mode.
        """
        if mode == "serial":
            from_node._serial_next.append(to_node)
        elif mode == "parallel":
            from_node._parallel.append(to_node)
            to_node._parallel.append(from_node)
        elif mode == "conditional":
            from_node._conditional.append((to_node, condition))
        else:
            raise ValueError(f"Unknown connection mode: {mode}")

    def run(self, start_node: Node, input_data: Any) -> Any:
        """Execute the pipeline starting from *start_node*.

        Args:
            start_node: The first node to execute.
            input_data: Initial data passed to the first node.

        Returns:
            The result from the terminal node(s) of the pipeline.
        """
        context: Dict[str, Any] = {}
        self._reset_all()
        return self._execute_node(start_node, context, input_data)

    # ------------------------------------------------------------------
    # Internal execution engine
    # ------------------------------------------------------------------

    def _reset_all(self):
        for node in self._nodes.values():
            node.reset()

    def _execute_node(self, node: Node, context: dict, data: Any) -> Any:
        """Execute a single node and route to its successors."""
        if node._status != NodeStatus.PENDING:
            return node._result

        # Check condition (for | operator / conditional routing)
        if node.condition is not None:
            if not node.condition(context, data):
                node._status = NodeStatus.SKIPPED
                node._result = data
                return data

        # Attempt execution (with retry)
        node._status = NodeStatus.RUNNING
        last_error = None
        attempts = 1 + node.retry

        for attempt in range(attempts):
            try:
                start = time.perf_counter()
                if node.timeout is not None:
                    node._result = self._run_with_timeout(node.fn, context, data, node.timeout)
                else:
                    node._result = node.fn(context, data)
                node._duration = time.perf_counter() - start
                node._status = NodeStatus.SUCCESS
                last_error = None
                break
            except Exception as e:
                last_error = e
                node._duration = time.perf_counter() - time.perf_counter()  # 0
                if attempt < attempts - 1:
                    continue
                node._status = NodeStatus.FAILED
                node._error = last_error
                raise RuntimeError(
                    f"Node '{node.name}' failed after {attempts} attempt(s): {last_error}"
                ) from last_error

        # Route output to successors
        return self._route(node, context, node._result)

    def _run_with_timeout(self, fn: Callable, context: dict, data: Any, timeout: float) -> Any:
        """Run a function with a timeout using a thread."""
        result_container: List = [None]
        exception_container: List[Optional[Exception]] = [None]

        def target():
            try:
                result_container[0] = fn(context, data)
            except Exception as e:
                exception_container[0] = e

        thread = threading.Thread(target=target, daemon=True)
        thread.start()
        thread.join(timeout)

        if thread.is_alive():
            raise TimeoutError(f"Node execution timed out after {timeout}s")

        if exception_container[0] is not None:
            raise exception_container[0]  # type: ignore

        return result_container[0]

    def _route(self, node: Node, context: dict, data: Any) -> Any:
        """Route data from *node* to its successors based on connection type."""
        results = []

        # 1) Serial successors (>>) — run sequentially
        serial_output = data
        for next_node in node._serial_next:
            serial_output = self._execute_node(next_node, context, serial_output)

        if node._serial_next:
            results.append(serial_output)

        # 2) Parallel peers (//) — run concurrently
        if node._parallel:
            # Deduplicate: avoid launching already-running nodes
            parallel_nodes = [
                n for n in node._parallel
                if n._status == NodeStatus.PENDING
            ]
            if parallel_nodes:
                parallel_results = self._run_parallel(parallel_nodes, context, data)
                results.extend(parallel_results)

        # 3) Conditional successors (|) — evaluate conditions
        for next_node, condition in node._conditional:
            should_run = True
            if condition is not None:
                should_run = condition(context, data)
            if should_run:
                results.append(
                    self._execute_node(next_node, context, data)
                )

        if results:
            return results[-1]  # return last meaningful result
        return data

    def _run_parallel(self, nodes: List[Node], context: dict, data: Any) -> List[Any]:
        """Execute a list of nodes in parallel threads."""
        results: List[Any] = [None] * len(nodes)
        threads: List[threading.Thread] = []

        def worker(idx: int, n: Node):
            try:
                results[idx] = self._execute_node(n, context, data)
            except Exception:
                pass  # error is recorded on the node itself

        for i, n in enumerate(nodes):
            t = threading.Thread(target=worker, args=(i, n), daemon=True)
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        return results

    # ------------------------------------------------------------------
    # Visualization
    # ------------------------------------------------------------------

    def visualize(self) -> str:
        """Generate a Mermaid.js flowchart string from the pipeline graph."""
        lines = ["flowchart TD"]
        seen_edges = set()

        for node in self._nodes.values():
            node_id = self._sanitize_mermaid_id(node.name)

            # Node label with status info
            node_def = f'{node_id}["{node.name}"]'
            lines.append(f"    {node_def}")

            # Serial edges (>>)
            for next_n in node._serial_next:
                next_id = self._sanitize_mermaid_id(next_n.name)
                edge = (node_id, next_id, "serial")
                if edge not in seen_edges:
                    seen_edges.add(edge)
                    lines.append(f"    {node_id} --> {next_id}")

            # Parallel edges (//)
            for par_n in node._parallel:
                par_id = self._sanitize_mermaid_id(par_n.name)
                edge = (node_id, par_id, "parallel")
                if edge not in seen_edges:
                    seen_edges.add(edge)
                    lines.append(f"    {node_id} -.-> {par_id}")

            # Conditional edges (|)
            for cond_n, _ in node._conditional:
                cond_id = self._sanitize_mermaid_id(cond_n.name)
                edge = (node_id, cond_id, "conditional")
                if edge not in seen_edges:
                    seen_edges.add(edge)
                    lines.append(f"    {node_id} -- condition --> {cond_id}")

        return "\n".join(lines)

    @staticmethod
    def _sanitize_mermaid_id(name: str) -> str:
        """Convert a node name to a valid Mermaid node ID."""
        sanitized = "".join(c if c.isalnum() else "_" for c in name)
        if not sanitized or sanitized[0].isalpha():
            return "n_" + sanitized
        return sanitized


def pipe_decorator(name: str = "", timeout: Optional[float] = None, retry: int = 0):
    """Decorator that wraps a function as a Pipeline Node.

    Usage:
        @pipe_decorator(name="double", timeout=5)
        def double(context, data):
            return data * 2
    """
    def decorator(fn: Callable):
        @functools.wraps(fn)
        def wrapper(context, data):
            return fn(context, data)
        wrapper._node_meta = {"name": name, "timeout": timeout, "retry": retry}
        return wrapper
    return decorator
