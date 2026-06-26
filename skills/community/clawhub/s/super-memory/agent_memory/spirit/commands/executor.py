from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Optional

from ..interface import SpiritInterface, WrappedOutput
from ..llm_layer import SpiritLLMLayer
from .parser import ParsedCommand

logger = logging.getLogger(__name__)


@dataclass
class ExecutionResult:
    success: bool = False
    intent: str = ''
    action_taken: str = ''
    preview: str = ''
    output: str = ''
    error: str = ''

    def to_dict(self) -> dict:
        return {
            'success': self.success,
            'intent': self.intent,
            'action_taken': self.action_taken,
            'preview': self.preview[:200],
            'output': self.output[:500],
            'error': self.error,
        }


class CommandExecutor:
    """Command executor with confirmation protocol.

    All write operations require confirmation:
    1. Preview what will happen
    2. User confirms
    3. Execute
    4. Report result
    """

    WRITE_INTENTS = frozenset({'consolidate', 'archive', 'correct'})
    ALLOWED_INTENTS = frozenset({'consolidate', 'review', 'archive', 'find', 'report', 'correct'})

    def __init__(self, interface: SpiritInterface, llm_layer: SpiritLLMLayer = None):
        self.interface = interface
        self.llm_layer = llm_layer
        self._pending_confirmations: dict[str, ParsedCommand] = {}

    def execute(self, command: ParsedCommand, confirm: bool = True) -> ExecutionResult:
        if command.intent not in self.ALLOWED_INTENTS:
            logger.warning("Rejected disallowed intent: %s", command.intent)
            return ExecutionResult(
                success=False,
                intent=command.intent,
                error=f"Intent '{command.intent}' is not allowed. Allowed: {sorted(self.ALLOWED_INTENTS)}",
            )

        handler = self._get_handler(command.intent)
        if handler is None:
            logger.warning("Rejected unknown intent: %s (allowed: %s)", command.intent, sorted(self.ALLOWED_INTENTS))
            return ExecutionResult(
                success=False,
                intent=command.intent,
                error=f"Intent '{command.intent}' is not allowed. Allowed intents: {sorted(self.ALLOWED_INTENTS)}",
            )

        is_write = command.intent in self.WRITE_INTENTS

        if is_write and not confirm:
            preview = handler(command, preview_only=True)
            cmd_key = f"{command.intent}:{command.target}"
            self._pending_confirmations[cmd_key] = command
            return ExecutionResult(
                success=False,
                intent=command.intent,
                action_taken='preview',
                preview=preview,
            )

        try:
            result = handler(command, preview_only=False)
            return ExecutionResult(
                success=True,
                intent=command.intent,
                action_taken='executed',
                output=result,
            )
        except Exception as e:
            logger.error("CommandExecutor.execute(%s): %s", command.intent, e)
            return ExecutionResult(
                success=False,
                intent=command.intent,
                error=str(e),
            )

    def confirm_pending(self, cmd_key: str) -> ExecutionResult:
        pending = self._pending_confirmations.pop(cmd_key, None)
        if pending is None:
            return ExecutionResult(
                success=False,
                error=f"No pending command: {cmd_key}",
            )
        return self.execute(pending, confirm=True)

    def _get_handler(self, intent: str):
        handlers = {
            'consolidate': self._handle_consolidate,
            'review': self._handle_review,
            'archive': self._handle_archive,
            'find': self._handle_find,
            'report': self._handle_report,
            'correct': self._handle_correct,
        }
        return handlers.get(intent)

    def _handle_consolidate(self, command: ParsedCommand, preview_only: bool = False) -> str:
        topic = command.params.get('topic', command.target)

        if preview_only:
            result = self.interface.write(
                'maintain',
                confirm=False,
                operations=['consolidate'],
            )
            return result.to_string()

        result = self.interface.write(
            'maintain',
            confirm=True,
            operations=['consolidate'],
        )
        return result.to_string()

    def _handle_review(self, command: ParsedCommand, preview_only: bool = False) -> str:
        topic = command.params.get('topic', command.target)
        time_range = command.params.get('time_range')

        kwargs = {}
        if topic:
            kwargs['query'] = topic
        if time_range:
            time_from, time_to = self._resolve_time_range(time_range)
            if time_from:
                kwargs['time_from'] = time_from
            if time_to:
                kwargs['time_to'] = time_to

        result = self.interface.read('recall', limit=20, **kwargs)
        return result.to_string()

    def _handle_archive(self, command: ParsedCommand, preview_only: bool = False) -> str:
        importance = command.params.get('importance', 'low')

        if preview_only:
            result = self.interface.write(
                'maintain',
                confirm=False,
                operations=['decay'],
            )
            return result.to_string()

        result = self.interface.write(
            'maintain',
            confirm=True,
            operations=['decay'],
        )
        return result.to_string()

    def _handle_find(self, command: ParsedCommand, preview_only: bool = False) -> str:
        query = command.params.get('query', command.target)
        if not query:
            return "[ERROR] No query specified for find operation"

        result = self.interface.read('recall', query=query, limit=10)
        return result.to_string()

    def _handle_report(self, command: ParsedCommand, preview_only: bool = False) -> str:
        report_type = command.params.get('report_type', 'daily')
        time_range = command.params.get('time_range')

        return f"[REPORT REQUEST] type={report_type}, time_range={time_range or 'default'}"

    def _handle_correct(self, command: ParsedCommand, preview_only: bool = False) -> str:
        target = command.target

        if preview_only:
            result = self.interface.write(
                'maintain',
                confirm=False,
                operations=['heal'],
            )
            return result.to_string()

        result = self.interface.write(
            'maintain',
            confirm=True,
            operations=['heal'],
        )
        return result.to_string()

    def _resolve_time_range(self, time_range: str):
        import time as _time
        now = int(_time.time())
        today_start = now - now % 86400

        ranges = {
            'today': (today_start, today_start + 86400),
            'yesterday': (today_start - 86400, today_start),
            'this_week': (today_start - (now - today_start) % (7 * 86400), today_start + 86400),
            'last_week': (today_start - 14 * 86400 + (now - today_start) % (7 * 86400),
                          today_start - 7 * 86400 + (now - today_start) % (7 * 86400)),
            'this_month': (today_start - (today_start % (30 * 86400)), today_start + 86400),
            'last_month': (today_start - 60 * 86400 + (today_start % (30 * 86400)),
                           today_start - 30 * 86400 + (today_start % (30 * 86400))),
        }

        return ranges.get(time_range, (None, None))
