"""MemOS Cloud Skill runtime package.

The top-level functions preserve the previous import surface for callers that
used `import memos_cloud` instead of executing the CLI script.
"""

from __future__ import annotations

from typing import Iterable, Optional

__all__ = [
    "__version__",
    "add_feedback",
    "add_kb_doc",
    "add_message",
    "create_knowledge_base",
    "delete_kb_documents",
    "delete_memory",
    "get_kb_documents",
    "get_user_profile",
    "remove_knowledge_base",
    "search_memory",
]

__version__ = "1.0.0"


def _client():
    from .client import MemosClient
    from .config import load_config

    return MemosClient(load_config())


def search_memory(user_id: str, query: str, conversation_id: Optional[str] = None):
    from .operations import search_memory as operation

    return operation(_client(), user_id, query, conversation_id)


def add_message(user_id: str, conversation_id: str, messages_json_str: str):
    from .operations import add_message as operation

    return operation(_client(), user_id, conversation_id, messages_json_str)


def delete_memory(memory_ids_str: str):
    from .operations import delete_memory as operation

    return operation(_client(), memory_ids_str)


def add_feedback(
    user_id: str,
    conversation_id: str,
    feedback_content: str,
    allow_knowledgebase_ids: Optional[str] = None,
):
    from .operations import add_feedback as operation

    return operation(
        _client(),
        user_id,
        conversation_id,
        feedback_content,
        allow_knowledgebase_ids,
    )


def add_kb_doc(
    knowledgebase_id: str,
    files: Iterable[str],
    file_type: str = "document",
    name: Optional[str] = None,
    stdin: bool = False,
):
    import sys

    from .files import build_file_payloads, build_stdin_file_payload
    from .operations import add_kb_doc as operation

    if stdin:
        file_list = [build_stdin_file_payload(sys.stdin.buffer, file_type, name)]
    else:
        file_list = build_file_payloads(files, file_type)
    return operation(_client(), knowledgebase_id, file_list)


def get_user_profile(
    user_id: Optional[str] = None,
    page: Optional[int] = None,
    size: Optional[int] = None,
    filter_obj: Optional[dict] = None,
    include_preference: Optional[bool] = None,
    include_tool_memory: Optional[bool] = None,
):
    from .operations import get_user_profile as operation

    c = _client()
    uid = user_id or c.config.user_id
    if not uid:
        from .errors import ConfigurationError
        raise ConfigurationError("user_id is required or MEMOS_USER_ID must be set.")
    return operation(c, uid, page, size, filter_obj, include_preference, include_tool_memory)


def create_knowledge_base(
    knowledgebase_name: str,
    knowledgebase_description: Optional[str] = None,
):
    from .operations import create_knowledge_base as operation

    return operation(_client(), knowledgebase_name, knowledgebase_description)


def get_kb_documents(
    file_ids: Optional[str] = None,
    knowledgebase_id: Optional[str] = None,
    doc_type: Optional[str] = None,
    page: Optional[int] = None,
    page_size: Optional[int] = None,
):
    from .operations import get_kb_documents as operation

    return operation(_client(), file_ids, knowledgebase_id, doc_type, page, page_size)


def delete_kb_documents(file_ids: str):
    from .operations import delete_kb_documents as operation

    return operation(_client(), file_ids)


def remove_knowledge_base(knowledgebase_id: str):
    from .operations import remove_knowledge_base as operation

    return operation(_client(), knowledgebase_id)
