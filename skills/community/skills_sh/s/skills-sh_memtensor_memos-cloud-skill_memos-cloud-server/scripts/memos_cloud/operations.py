from __future__ import annotations

from typing import Any, Dict, Optional

from .client import MemosClient
from .payloads import (
    add_feedback_payload,
    add_kb_doc_payload,
    add_message_payload,
    create_knowledge_base_payload,
    delete_kb_documents_payload,
    delete_memory_payload,
    get_kb_documents_payload,
    get_user_profile_payload,
    remove_knowledge_base_payload,
    resolve_conversation_id,
    search_memory_payload,
)


def search_memory(
    client: MemosClient,
    user_id: str,
    query: str,
    conversation_id: Optional[str] = None,
    conversation_first_message: Optional[str] = None,
    filter_obj: Optional[Dict[str, Any]] = None,
    knowledgebase_ids: Optional[str] = None,
    memory_limit_number: Optional[int] = None,
    include_preference: Optional[bool] = None,
    preference_limit_number: Optional[int] = None,
    include_tool_memory: Optional[bool] = None,
    tool_memory_limit_number: Optional[int] = None,
    include_skill: Optional[bool] = None,
    skill_limit_number: Optional[int] = None,
    relativity: Optional[float] = None,
):
    return client.post(
        "/search/memory",
        search_memory_payload(
            user_id, query, conversation_id, conversation_first_message,
            filter_obj, knowledgebase_ids, memory_limit_number,
            include_preference, preference_limit_number,
            include_tool_memory, tool_memory_limit_number,
            include_skill, skill_limit_number, relativity,
        ),
    )


def add_message(
    client: MemosClient,
    user_id: str,
    conversation_id: Optional[str] = None,
    messages_json_str: str = "",
    conversation_first_message: Optional[str] = None,
    agent_id: Optional[str] = None,
    app_id: Optional[str] = None,
    tags: Optional[str] = None,
    info_json: Optional[str] = None,
    allow_public: Optional[bool] = None,
    allow_knowledgebase_ids: Optional[str] = None,
    async_mode: Optional[bool] = None,
):
    cid = resolve_conversation_id(user_id, conversation_id, conversation_first_message)
    if not cid:
        from .errors import ValidationError
        raise ValidationError("Either conversation_id or conversation_first_message is required.")
    return client.post(
        "/add/message",
        add_message_payload(
            user_id, cid, messages_json_str,
            agent_id, app_id, tags, info_json,
            allow_public, allow_knowledgebase_ids, async_mode,
        ),
    )


def delete_memory(client: MemosClient, memory_ids_str: str):
    return client.post("/delete/memory", delete_memory_payload(memory_ids_str))


def add_feedback(
    client: MemosClient,
    user_id: str,
    conversation_id: Optional[str],
    feedback_content: str,
    allow_knowledgebase_ids: Optional[str] = None,
    agent_id: Optional[str] = None,
    app_id: Optional[str] = None,
    feedback_time: Optional[str] = None,
    allow_public: Optional[bool] = None,
    conversation_first_message: Optional[str] = None,
):
    cid = resolve_conversation_id(user_id, conversation_id, conversation_first_message)
    if not cid:
        from .errors import ValidationError
        raise ValidationError("Either conversation_id or conversation_first_message is required.")
    return client.post(
        "/add/feedback",
        add_feedback_payload(
            user_id,
            cid,
            feedback_content,
            allow_knowledgebase_ids,
            agent_id,
            app_id,
            feedback_time,
            allow_public,
        ),
    )


def add_kb_doc(client: MemosClient, knowledgebase_id: str, file_list: list[dict[str, str]]):
    return client.post(
        "/add/knowledgebase-file",
        add_kb_doc_payload(knowledgebase_id, file_list),
    )


def get_user_profile(
    client: MemosClient,
    user_id: str,
    page: Optional[int] = None,
    size: Optional[int] = None,
    filter_obj: Optional[Dict[str, Any]] = None,
    include_preference: Optional[bool] = None,
    include_tool_memory: Optional[bool] = None,
):
    return client.post(
        "/get/memory",
        get_user_profile_payload(user_id, page, size, filter_obj, include_preference, include_tool_memory),
    )


def create_knowledge_base(
    client: MemosClient,
    knowledgebase_name: str,
    knowledgebase_description: Optional[str] = None,
):
    return client.post(
        "/create/knowledgebase",
        create_knowledge_base_payload(knowledgebase_name, knowledgebase_description),
    )


def get_kb_documents(
    client: MemosClient,
    file_ids: Optional[str] = None,
    knowledgebase_id: Optional[str] = None,
    doc_type: Optional[str] = None,
    page: Optional[int] = None,
    page_size: Optional[int] = None,
):
    return client.post(
        "/get/knowledgebase-file",
        get_kb_documents_payload(file_ids, knowledgebase_id, doc_type, page, page_size),
    )


def delete_kb_documents(client: MemosClient, file_ids: str):
    return client.post(
        "/delete/knowledgebase-file",
        delete_kb_documents_payload(file_ids),
    )


def remove_knowledge_base(client: MemosClient, knowledgebase_id: str):
    return client.post(
        "/delete/knowledgebase",
        remove_knowledge_base_payload(knowledgebase_id),
    )
