#!/usr/bin/env python3
from __future__ import annotations

import copy
import importlib.util
import json
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Optional, Union

from build_conversation_analysis_input import build_input_from_inbox
from campaign_state_store import CampaignStateStore
from campaign_cycle_summary import build_cycle_summary, build_human_cycle_summary
from campaign_send_protocol import normalize_send_policy, normalize_reply_policy, execute_outreach_send
from common import get_token
from incremental_monitor import monitor_campaign_replies
from brief_schema import normalize_campaign_brief, validate_scheduled_execution_brief
from reply_handler import ReplyHandler
from reply_processor import ReplyProcessor
from execution_layer import prepare_emails_from_host_drafts, normalize_email_once
from draft_consistency_audit import build_creator_profile_map


_RUN_CAMPAIGN_MODULE: Optional[Any]= None


def _load_run_campaign_module():
    global _RUN_CAMPAIGN_MODULE
    if _RUN_CAMPAIGN_MODULE is not None:
        return _RUN_CAMPAIGN_MODULE

    module_path = Path(__file__).resolve().parent / "run_campaign.py"
    spec = importlib.util.spec_from_file_location("wotohub_scripts_run_campaign", module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to load run_campaign module from {module_path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    _RUN_CAMPAIGN_MODULE = module
    return module




def _extract_selected_creators_from_search_result(search_result: dict[str, Any]) -> list[dict[str, Any]]:
    emails = search_result.get("emails") or []
    if emails:
        return emails
    recommendations = search_result.get("recommendations") or {}
    for key in ("items", "topRecommendations"):
        items = recommendations.get(key) or []
        if isinstance(items, list) and items:
            return items
    raw_search = search_result.get("searchResult") or {}
    raw_result = (raw_search.get("result") or {}).get("data") if isinstance(raw_search, dict) else None
    if isinstance(raw_result, dict):
        for key in ("bloggerList", "records", "list", "rows", "dataList"):
            items = raw_result.get(key) or []
            if isinstance(items, list) and items:
                return items
    return []


def _creator_identity(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "bloggerId": item.get("bloggerId") or item.get("besId") or item.get("bEsId") or item.get("id"),
        "nickname": item.get("nickname") or item.get("bloggerName") or item.get("channelName") or item.get("username"),
        "followers": item.get("fansNum") or item.get("followers"),
        "avgViews": item.get("avgViews") or item.get("averageViews"),
        "platform": item.get("platform"),
        "country": item.get("country"),
        "language": item.get("language") or item.get("blogLang"),
        "category": item.get("category"),
        "email": item.get("email") or item.get("contactEmail") or item.get("contact"),
        "link": item.get("link") or item.get("wotohubLink"),
        "tagList": item.get("tagList") or [],
        "matchScore": item.get("matchScore"),
        "matchTier": item.get("matchTier"),
        "historyAnalysis": item.get("historyAnalysis"),
        "wotohubLink": item.get("wotohubLink"),
        "channelName": item.get("channelName") or item.get("nickname") or item.get("bloggerName"),
        "bloggerName": item.get("bloggerName") or item.get("nickname") or item.get("channelName"),
        "contentStyle": item.get("contentStyle") or item.get("category"),
        "recentTopics": item.get("recentTopics") or item.get("tagList") or [],
    }


def _creator_id(item: dict[str, Any]) -> str:
    return str(item.get("bloggerId") or item.get("besId") or item.get("bEsId") or item.get("id") or "").strip()


def _content_fingerprint(email: dict[str, Any]) -> str:
    subject = re.sub(r"\s+", " ", str(email.get("subject") or "").strip()).lower()
    plain = re.sub(
        r"\s+",
        " ",
        str(email.get("plainTextBody") or email.get("body") or email.get("content") or "").strip(),
    ).lower()
    return f"{subject}\n{plain}".strip()


def _align_host_drafts_to_selected_creators(
    *,
    selected_creators: list[dict[str, Any]],
    host_drafts: list[dict[str, Any]],
    draft_metadata: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    creator_map: dict[str, dict[str, Any]] = {}
    creator_order: list[str] = []
    for item in selected_creators or []:
        if not isinstance(item, dict):
            continue
        blogger_id = _creator_id(item)
        if not blogger_id or blogger_id in creator_map:
            continue
        creator_map[blogger_id] = _creator_identity(item)
        creator_order.append(blogger_id)

    normalized_drafts = [normalize_email_once(item) for item in prepare_emails_from_host_drafts(host_drafts)]
    drafts_by_id: dict[str, list[dict[str, Any]]] = defaultdict(list)
    unexpected_ids: list[str] = []
    for draft in normalized_drafts:
        blogger_id = _creator_id(draft)
        if not blogger_id:
            continue
        if blogger_id not in creator_map:
            unexpected_ids.append(blogger_id)
            continue
        drafts_by_id[blogger_id].append(draft)

    missing_ids = [blogger_id for blogger_id in creator_order if not drafts_by_id.get(blogger_id)]
    duplicate_ids = [blogger_id for blogger_id, items in drafts_by_id.items() if len(items) > 1]

    aligned_emails: list[dict[str, Any]] = []
    for blogger_id in creator_order:
        drafts = drafts_by_id.get(blogger_id) or []
        if not drafts:
            continue
        draft = drafts[0]
        creator = creator_map.get(blogger_id) or {}
        merged = {
            **creator,
            **draft,
            "bloggerId": blogger_id,
            "nickname": creator.get("nickname") or draft.get("nickname"),
            "bloggerName": creator.get("bloggerName") or draft.get("bloggerName") or creator.get("nickname"),
            "channelName": creator.get("channelName") or draft.get("channelName") or creator.get("nickname"),
            "platform": creator.get("platform") or draft.get("platform"),
            "country": creator.get("country") or draft.get("country"),
            "language": creator.get("language") or draft.get("language"),
            "category": creator.get("category") or draft.get("category"),
            "contentStyle": creator.get("contentStyle") or draft.get("contentStyle"),
            "tagList": creator.get("tagList") or draft.get("tagList") or [],
            "recentTopics": creator.get("recentTopics") or draft.get("recentTopics") or [],
            "followers": creator.get("followers") or draft.get("followers") or creator.get("fansNum") or draft.get("fansNum"),
            "fansNum": creator.get("followers") or draft.get("fansNum") or creator.get("fansNum") or draft.get("followers"),
        }
        aligned_emails.append(normalize_email_once(merged))

    fingerprint_groups: dict[str, list[str]] = defaultdict(list)
    for email in aligned_emails:
        fingerprint = _content_fingerprint(email)
        if not fingerprint:
            continue
        fingerprint_groups[fingerprint].append(str(email.get("bloggerId") or ""))
    duplicate_content_groups = [ids for ids in fingerprint_groups.values() if len(ids) > 1]
    metadata_mismatches: list[str] = []
    draft_metadata = draft_metadata or {}
    expected_selected_count = draft_metadata.get("selectedCreatorCount")
    if expected_selected_count not in (None, "") and int(expected_selected_count) != len(creator_order):
        metadata_mismatches.append("selectedCreatorCount_mismatch")
    expected_generated_count = draft_metadata.get("generatedDraftCount")
    if expected_generated_count not in (None, "") and int(expected_generated_count) != len(normalized_drafts):
        metadata_mismatches.append("generatedDraftCount_mismatch")
    expected_unique_count = draft_metadata.get("uniqueBloggerIdCount")
    actual_unique_count = len(drafts_by_id)
    if expected_unique_count not in (None, "") and int(expected_unique_count) != actual_unique_count:
        metadata_mismatches.append("uniqueBloggerIdCount_mismatch")
    declared_missing = sorted(str(x) for x in (draft_metadata.get("missingBloggerIds") or []))
    if declared_missing and declared_missing != sorted(missing_ids):
        metadata_mismatches.append("missingBloggerIds_mismatch")
    declared_duplicates = sorted(str(x) for x in (draft_metadata.get("duplicateBloggerIds") or []))
    if declared_duplicates and declared_duplicates != sorted(duplicate_ids):
        metadata_mismatches.append("duplicateBloggerIds_mismatch")
    declared_unexpected = sorted(str(x) for x in (draft_metadata.get("unexpectedBloggerIds") or []))
    if declared_unexpected and declared_unexpected != sorted(set(unexpected_ids)):
        metadata_mismatches.append("unexpectedBloggerIds_mismatch")

    issues = {
        "selectedCreatorCount": len(creator_order),
        "inputDraftCount": len(normalized_drafts),
        "alignedDraftCount": len(aligned_emails),
        "missingCreatorIds": missing_ids,
        "duplicateDraftCreatorIds": duplicate_ids,
        "unexpectedDraftCreatorIds": sorted(set(unexpected_ids)),
        "duplicateContentGroups": duplicate_content_groups,
        "declaredWriteBackMetadata": draft_metadata,
        "metadataMismatches": metadata_mismatches,
    }
    ok = not missing_ids and not duplicate_ids and not unexpected_ids and not duplicate_content_groups and not metadata_mismatches and len(aligned_emails) == len(creator_order)
    return {
        "ok": ok,
        "emails": aligned_emails,
        "issues": issues,
    }


def build_draft_generation_input(
    *,
    campaign_id: str,
    brief: dict[str, Any],
    selected_creators: list[dict[str, Any]],
    cycle_no: int,
) -> dict[str, Any]:
    normalized_brief = normalize_campaign_brief(brief)
    return {
        "campaignId": campaign_id,
        "cycleNo": cycle_no,
        "task": "generate_host_drafts_for_selected_creators",
        "draftPolicy": normalized_brief.get("draft_policy") or {},
        "product": {
            "productName": normalized_brief.get("product_name"),
            "brandName": normalized_brief.get("brand_name"),
            "targetMarket": normalized_brief.get("target_market"),
            "input": normalized_brief.get("input"),
            "modelAnalysis": normalized_brief.get("model_analysis"),
        },
        "outreachPolicy": {
            "senderName": normalized_brief.get("sender_name"),
            "offerType": normalized_brief.get("offer_type"),
            "emailLanguage": normalized_brief.get("language") or "en",
            "deliverable": normalized_brief.get("deliverable"),
            "compensation": normalized_brief.get("compensation"),
            "ctaGoal": normalized_brief.get("cta_goal"),
        },
        "selectionRule": normalized_brief.get("selection_rule"),
        "selectedCreators": [_creator_identity(item) for item in (selected_creators or [])],
        "outputContract": {
            "field": "host_drafts_per_cycle",
            "acceptedAliases": ["host_drafts_per_cycle", "hostDraftsPerCycle"],
            "requiredPerDraftFields": ["bloggerId", "subject", "plainTextBody|htmlBody"],
            "requiredBatchMetadata": [
                "selectedCreatorCount",
                "generatedDraftCount",
                "uniqueBloggerIdCount",
                "missingBloggerIds",
                "duplicateBloggerIds",
                "unexpectedBloggerIds",
            ],
        },
    }


def _build_customer_reply_review_summary(reply_actions: list[dict[str, Any]]) -> dict[str, Any]:
    high_risk_items = [
        item for item in (reply_actions or [])
        if item.get("deliveryMode") == "human_review"
    ]
    lines = []
    for item in high_risk_items[:10]:
        reasons = ", ".join(item.get("reasons") or []) or "manual_review_required"
        latest_incoming = str(item.get("latestIncoming") or "").strip()
        latest_incoming = latest_incoming if len(latest_incoming) <= 180 else latest_incoming[:180].rstrip() + "..."
        lines.append(
            f"- {item.get('nickname') or item.get('bloggerId') or 'unknown'} | risk={item.get('riskLevel') or 'unknown'} | reasons={reasons} | subject={item.get('subject') or '-'} | latest={latest_incoming or '-'}"
        )
    return {
        "count": len(high_risk_items),
        "items": high_risk_items,
        "text": "\n".join(lines) if lines else "",
    }


def build_reply_analysis_request(
    *,
    campaign_id: str,
    cycle_no: int,
    reply_model_input: dict[str, Any],
) -> dict[str, Any]:
    return {
        "task": "generate_host_reply_understanding",
        "mode": "host_model_request",
        "campaign": {
            "campaignId": campaign_id,
            "cycleNo": cycle_no,
        },
        "input": reply_model_input,
        "promptPath": "prompts/conversation-analysis.md",
        "schemaPath": "references/conversation-analysis-schema.md",
        "deliveryContract": {
            "field": "reply_model_analysis",
            "acceptedAliases": ["reply_model_analysis", "replyModelAnalysis", "conversationAnalysis"],
            "canonicalField": "reply_model_analysis",
            "compatibilityAliasesOnly": True,
        },
        "runtimeHints": {
            "modelUnderstandingRequired": True,
            "runnerAutoGenerationAllowed": False,
            "riskRoutingMode": "low_risk_auto_reply_with_high_risk_summary",
        },
    }


class CampaignEngine:
    """Single-cycle campaign engine.

    Use this from both manual and scheduled entrypoints. Each invocation runs one safe,
    cron-friendly cycle and persists cumulative state.

    Send protocol principles:
    - host-model analysis preferred, script-first execution
    - scheduled mode defaults to prepare-only for outreach
    - review-required paths never silently send
    - only explicit send policies may execute WotoHub send APIs
    """

    def __init__(self, campaign_id: str, brief: dict[str, Any], token: Optional[str]= None, target_count: Optional[int]= None):
        self.campaign_id = campaign_id
        self.brief = normalize_campaign_brief(brief)
        self.token = token
        self.state = CampaignStateStore(campaign_id)
        if target_count is not None:
            self.state.set_target_count(target_count)
        # 仅在 state 中保存的是宿主/外部模型结果时，才允许跨周期注入 reply_model_analysis。
        # 旧的 rule-based fallback 结果不应再冒充正式 reply understanding 主链路。
        if not self.brief.get("reply_model_analysis"):
            saved = self.state.get_saved_reply_model_analysis()
            saved_meta = self.state.get_saved_reply_model_analysis_meta() or {}
            saved_source = str(saved_meta.get("source") or "")
            if saved and saved_source and saved_source != "rule_based_fallback_self_generated":
                self.brief["reply_model_analysis"] = saved

    def _reply_assist_classification(self, reply: dict[str, Any]) -> dict[str, Any]:
        return ReplyHandler.classify_reply(reply)

    def _classify_intent(self, reply: dict[str, Any]) -> str:
        return ReplyHandler.classify_intent(reply)

    def _generate_reply_model_analysis_fallback(
        self,
        candidate_items: list[dict[str, Any]],
        reply_model_input: Optional[dict[str, Any]],
    ) -> Optional[dict[str, Any]]:
        """Generate fallback reply analysis from candidate items.

        Preferred path is still host-provided reply_model_analysis.
        This method is a local rule-based fallback builder.
        """
        from execution_layer import analyze_reply_rule_based

        if not candidate_items:
            return None

        items_out: list[dict[str, Any]] = []

        injected_reply_analysis = None
        if isinstance(reply_model_input, dict):
            candidate_analysis = reply_model_input.get("replyModelAnalysis") or reply_model_input.get("conversationAnalysis")
            if isinstance(candidate_analysis, dict):
                injected_reply_analysis = candidate_analysis

        for candidate in candidate_items:
            chat_id = str(candidate.get("chatId") or "")
            blogger_id = str(candidate.get("bloggerId") or "")
            blogger_name = str(candidate.get("bloggerName") or candidate.get("bloggerUserName") or "")
            email_id = str(candidate.get("id") or candidate.get("emailId") or "")
            latest_content = str(candidate.get("cleanContent") or candidate.get("content") or "").strip()

            # Rule-based fallback reply analysis (host analysis preferred upstream)
            analysis = analyze_reply_rule_based(
                candidate,
                self.brief,
                reply_model_analysis=injected_reply_analysis,
                allow_fallback=True,
            )
            assist_analysis = ReplyHandler.classify_reply(candidate)
            requires_human = bool(
                analysis.get("requiresHuman")
                if "requiresHuman" in analysis
                else assist_analysis.get("requiresHuman")
            )
            classification = analysis.get("classification") or assist_analysis.get("classification") or "unknown"
            intent = analysis.get("intent") or assist_analysis.get("intent") or "unknown"
            stage = (
                analysis.get("conversationStage")
                or analysis.get("stage")
                or assist_analysis.get("stage")
                or ("human_review" if requires_human else "reply_ready")
            )
            tone = analysis.get("tone") or assist_analysis.get("tone") or "neutral"
            reply_body = (
                analysis.get("replyBody")
                or analysis.get("body")
                or self._build_safe_reply_body(
                    blogger_name=blogger_name,
                    intent=str(intent),
                    classification=str(classification),
                    requires_human=requires_human,
                    latest_content=latest_content,
                )
            )
            subject = str(candidate.get("subject") or "")

            items_out.append({
                "replyId": int(email_id) if email_id.isdigit() else 0,
                "chatId": chat_id,
                "bloggerId": blogger_id,
                "bloggerName": blogger_name,
                "subject": subject,
                "conversationStage": stage,
                "replyBody": reply_body,
                "latestIncoming": latest_content,
                "lastIncoming": latest_content,
                "lastOutgoing": "",
                "classification": classification,
                "intent": intent,
                "tone": tone,
                "requiresHuman": requires_human,
                "riskFlags": analysis.get("riskFlags", []) or assist_analysis.get("riskFlags", []),
                "analysis": {
                    "latestIntent": intent,
                    "tone": tone,
                    "riskFlags": analysis.get("riskFlags", []) or assist_analysis.get("riskFlags", []),
                },
            })

        if not items_out:
            return None
        return {
            "items": items_out,
            "analysisMode": "rule-based-fallback",
            "analysisProvenance": {
                "source": "campaign_engine_fallback",
                "usedInjectedReplyModelAnalysis": bool(injected_reply_analysis),
            },
        }

    def _build_safe_reply_body(
        self,
        *,
        blogger_name: str,
        intent: str,
        classification: str,
        requires_human: bool,
        latest_content: str,
    ) -> str:
        """Build safe reply body."""
        first_name = blogger_name.split()[0] if blogger_name else "there"
        if requires_human:
            return (
                f"Hi {first_name},\n\n"
                f"Thank you for getting back to us!\n\n"
                f"I've received your message and will have our team review your question. "
                f"We'll get back to you with a detailed response shortly.\n\n"
                f"Best regards"
            )
        return (
            f"Hi {first_name},\n\n"
            f"Thank you for your interest!\n\n"
            f"We're excited to work with you. "
            f"Looking forward to collaborating.\n\n"
            f"Best regards"
        )



    def run_cycle(self, *, mode: str = "single_cycle", page_size: int = 10, enable_reply_assist: bool = True, include_email_preview: bool = True, send_policy: Optional[str]= None, reply_send_policy: Optional[str]= None, review_required: Optional[bool]= None, timing: str = "") -> dict[str, Any]:
        cycle = self.state.start_cycle(mode=mode, metadata={"startedBy": "campaign_engine", "pageSize": page_size})
        cycle_no = int(cycle["cycle"])
        send_policy_info = normalize_send_policy(mode=mode, send_policy=send_policy, review_required=review_required)
        reply_policy_info = normalize_reply_policy(mode=mode, reply_send_policy=reply_send_policy, review_required=review_required)
        scheduled_brief_validation = validate_scheduled_execution_brief(self.brief) if mode == "scheduled_cycle" else {"ok": True, "errors": [], "forbiddenFields": []}
        result: dict[str, Any] = {
            "campaignId": self.campaign_id,
            "mode": mode,
            "cycle": cycle_no,
            "startedAt": cycle.get("startedAt"),
            "search": {},
            "send": {},
            "replies": {},
            "replyActions": {},
            "replyStrictMode": {},
            "protocol": {
                "sendPolicy": send_policy_info,
                "replySendPolicy": reply_policy_info,
                "includeEmailPreview": include_email_preview,
                "replyAssistEnabled": enable_reply_assist,
                "replyModelInjectionRequired": bool(self.brief.get("require_reply_model_analysis", False)),
            },
            "draftGeneration": {
                "mode": None,
                "needsHostDrafts": False,
                "hostDraftsInjected": False,
                "selectedCreatorCount": 0,
                "generatedDraftCount": 0,
                "status": "inactive",
                "nextRecommendedAction": None,
            },
            "briefValidation": scheduled_brief_validation,
            "hostReplyAnalysisRequest": None,
        }

        if mode == "scheduled_cycle" and not scheduled_brief_validation.get("ok"):
            result["send"] = {
                "status": "blocked",
                "preparedCount": 0,
                "autoSendExecuted": False,
                "reviewRequired": True,
                "notes": "Scheduled brief contains forbidden near-final search fields and was blocked before execution.",
            }
            result["replyActions"] = {
                "count": 0,
                "items": [],
                "autoSendEligible": 0,
                "humanReviewRequired": 0,
                "execution": {"status": "blocked_by_brief_schema", "sent": 0, "blocked": 0},
                "highRiskSummary": {"count": 0, "items": [], "text": ""},
                "customerSummary": "",
            }
            result["cycleSummary"] = build_cycle_summary(result)
            result["humanCycleSummary"] = (
                "本轮 campaign 已阻塞：scheduled brief 携带了不允许直接执行的近终态搜索字段。"
                f" 请移除这些字段后再重跑：{', '.join(scheduled_brief_validation.get('forbiddenFields') or [])}"
            )
            result["progress"] = self.state.get_progress()
            result["endedAt"] = datetime.now().astimezone().isoformat(timespec="seconds")
            self.state.finish_cycle(cycle_no, summary={
                "progress": result.get("progress"),
                "send": result.get("send"),
                "replyActions": result.get("replyActions"),
                "briefValidation": scheduled_brief_validation,
                "cycleSummary": result.get("cycleSummary"),
            })
            result["statePath"] = str(self.state.path)
            result["stateSummary"] = {
                "contacted": len(self.state.data.get("contacted") or {}),
                "replies": len(self.state.data.get("replies") or {}),
                "replyActions": len(self.state.data.get("replyActions") or {}),
                "metrics": self.state.data.get("metrics") or {},
            }
            result["error"] = {
                "code": "SCHEDULED_BRIEF_SCHEMA_BLOCKED",
                "message": "Scheduled cycle blocked because the brief contains forbidden near-final search fields.",
                "details": {"forbiddenFields": scheduled_brief_validation.get("forbiddenFields") or []},
            }
            return result

        contacted_ids = sorted(self.state.get_contacted_ids())
        selected_blogger_ids = self.brief.get("selected_blogger_ids")
        selected_ranks = self.brief.get("selected_ranks")
        selection_rule = self.brief.get("selection_rule")
        all_search_results_selected = bool(self.brief.get("all_search_results_selected", False))
        run_campaign = _load_run_campaign_module()
        draft_policy = self.brief.get("draft_policy") or {}
        per_cycle_host_drafts = self.brief.get("host_drafts_per_cycle") or self.brief.get("hostDraftsPerCycle") or self.brief.get("email_model_drafts")
        waiting_for_per_cycle_host_drafts = bool(
            mode == "scheduled_cycle"
            and draft_policy.get("mode") == "host_model_per_cycle"
            and not per_cycle_host_drafts
        )
        should_generate_email_preview = bool(
            include_email_preview
            and (selected_blogger_ids or selected_ranks or all_search_results_selected or selection_rule)
            and not waiting_for_per_cycle_host_drafts
        )
        search_result = run_campaign.run_campaign(
            user_input=self.brief.get("product_description") or self.brief.get("input") or "",
            token=self.token,
            platform=self.brief.get("platform", "tiktok"),
            min_fans=int(self.brief.get("min_fans", 10000) or 10000),
            max_fans=int(self.brief.get("max_fans", 500000) or 500000),
            has_email=bool(self.brief.get("has_email", True)),
            exclude_contacted=False,
            page_size=page_size,
            semantic_mode=self.brief.get("semantic_mode", "mock"),
            retry_fallbacks=True,
            debug=bool(self.brief.get("debug", False)),
            sender_name=self.brief.get("sender_name"),
            include_email_preview=should_generate_email_preview,
            offer_type=self.brief.get("offer_type", "sample"),
            email_language=self.brief.get("language", "en"),
            selected_blogger_ids=selected_blogger_ids,
            selected_ranks=selected_ranks,
            selection_rule=selection_rule,
            all_search_results_selected=all_search_results_selected,
            exclude_blogger_ids=contacted_ids,
            model_analysis=self.brief.get("model_analysis"),
            url_model_analysis=self.brief.get("url_model_analysis"),
            email_model_drafts=per_cycle_host_drafts,
            brand_name=self.brief.get("brand_name"),
            deliverable=self.brief.get("deliverable"),
            compensation=self.brief.get("compensation"),
            target_market=self.brief.get("target_market"),
            cta_goal=self.brief.get("cta_goal"),
        )
        selected_creators = _extract_selected_creators_from_search_result(search_result)
        creator_profiles_by_id = build_creator_profile_map(selected_creators)
        if mode == "scheduled_cycle" and draft_policy.get("mode") == "host_model_per_cycle":
            draft_generation_input = build_draft_generation_input(
                campaign_id=self.campaign_id,
                brief=self.brief,
                selected_creators=selected_creators,
                cycle_no=cycle_no,
            )
            result["draftGeneration"] = {
                "mode": "host_model_per_cycle",
                "needsHostDrafts": True,
                "hostDraftsInjected": False,
                "selectedCreatorCount": len(selected_creators),
                "generatedDraftCount": 0,
                "status": "waiting_for_host_drafts",
                "nextRecommendedAction": "Use draftGenerationInput to call the host model per selected creator, write personalized drafts into host_drafts_per_cycle, then rerun scheduled_cycle.",
                "draftGenerationInput": draft_generation_input,
            }
            injected_host_drafts = self.brief.get("host_drafts_per_cycle") or self.brief.get("hostDraftsPerCycle") or []
            injected_host_draft_metadata = self.brief.get("host_drafts_metadata_per_cycle") or self.brief.get("hostDraftsMetadataPerCycle") or {}
            if injected_host_drafts and selected_creators:
                draft_alignment = _align_host_drafts_to_selected_creators(
                    selected_creators=selected_creators,
                    host_drafts=injected_host_drafts,
                    draft_metadata=injected_host_draft_metadata if isinstance(injected_host_draft_metadata, dict) else {},
                )
                generated = draft_alignment.get("emails") or []
                alignment_issues = draft_alignment.get("issues") or {}
                alignment_ok = bool(draft_alignment.get("ok"))
                result["draftGeneration"] = {
                    "mode": "host_model_per_cycle",
                    "needsHostDrafts": False,
                    "hostDraftsInjected": True,
                    "selectedCreatorCount": len(selected_creators),
                    "generatedDraftCount": len(generated),
                    "status": "host_drafts_injected" if alignment_ok and generated else ("host_drafts_identity_conflict" if injected_host_drafts else "host_drafts_no_match"),
                    "nextRecommendedAction": None if alignment_ok and generated else "Ensure host writes exactly one personalized draft per selected creator, with unique bloggerId values and no repeated full email bodies across creators.",
                    "draftGenerationInput": draft_generation_input,
                    "validation": alignment_issues,
                }
                if alignment_ok and generated:
                    search_result["emails"] = generated
                    per_cycle_host_drafts = injected_host_drafts
                else:
                    search_result.setdefault("nextRecommendedAction", "Fix host draft write-back mapping, then rerun scheduled_cycle.")
        if include_email_preview and not should_generate_email_preview:
            search_result.setdefault("nextRecommendedAction", "先确认目标达人，再生成邮件预览。")
            search_result.setdefault("emailPreviewDeferred", True)
        search_error = None
        if not search_result.get("success"):
            search_error = {
                "code": ((search_result.get("error") or {}).get("code")) or search_result.get("code") or "SEARCH_FAILED",
                "message": ((search_result.get("error") or {}).get("message")) or search_result.get("message") or "Search failed before candidate selection.",
                "nextStep": ((search_result.get("error") or {}).get("next_step")) or search_result.get("next_step") or search_result.get("nextStep"),
            }
        result["search"] = {
            "success": bool(search_result.get("success")),
            "recommendationCount": (search_result.get("recommendations") or {}).get("count", 0),
            "payloadSource": search_result.get("payloadSource"),
            "perCycleDraftMode": draft_policy.get("mode"),
            "perCycleHostDraftsInjected": bool(per_cycle_host_drafts),
            "draftGenerationStatus": (result.get("draftGeneration") or {}).get("status"),
            "draftValidation": (result.get("draftGeneration") or {}).get("validation"),
            "error": search_error,
        }
        if search_error:
            result["error"] = {
                "code": search_error.get("code") or "SEARCH_FAILED",
                "message": search_error.get("message") or "Search failed before candidate selection.",
                "details": {
                    "stage": "search",
                    "payloadSource": search_result.get("payloadSource"),
                    "nextStep": search_error.get("nextStep"),
                },
            }
        self.state.update_cycle_section(cycle_no, "search", result["search"])

        emails = search_result.get("emails") or []
        for email in emails:
            blogger_id = str(email.get("bloggerId") or "")
            if blogger_id:
                self.state.record_contacted(blogger_id, email)
        result["send"] = execute_outreach_send(
            emails=emails,
            send_policy_info=send_policy_info,
            token=self.token,
            brief=self.brief,
            timing=timing,
            creator_profiles_by_id=creator_profiles_by_id,
            draft_generation=result.get("draftGeneration"),
        )
        self.state.update_cycle_section(cycle_no, "send", result["send"])

        reply_summary = {"newReplies": 0, "classified": {"confirmed": 0, "discussing": 0, "rejected": 0}}
        reply_actions: list[dict[str, Any]] = []
        reply_execution: dict[str, Any] = {"status": "not_requested", "sent": 0, "blocked": 0}
        reply_previews: list[dict[str, Any]] = []
        customer_reply_review_summary = {"count": 0, "items": [], "text": ""}
        reply_model_input: Optional[dict[str, Any]]= None
        reply_model_analysis: Optional[dict[str, Any]]= None
        injected_reply_analysis = ReplyProcessor.coerce_model_reply_analysis(self.brief.get("reply_model_analysis"))
        injected_reply_analysis_validation = ReplyProcessor.validate_model_reply_analysis(injected_reply_analysis) if injected_reply_analysis else None
        require_reply_model_analysis = bool(
            self.brief.get("require_reply_model_analysis", False)
            or (mode == "scheduled_cycle" and self.brief.get("auto_reply_policy") == "low_risk_auto_reply_with_high_risk_summary")
        )
        strict_mode_contract: dict[str, Any] = {
            "enabled": require_reply_model_analysis,
            "needsReplyModelAnalysis": False,
            "status": "inactive" if not require_reply_model_analysis else "waiting_for_check",
            "nextRecommendedAction": None,
            "replyModelInput": None,
            "acceptedInputField": "reply_model_analysis",
            "acceptedSchema": "references/conversation-analysis-schema.md",
            "promptPath": "prompts/conversation-analysis.md",
            "validation": injected_reply_analysis_validation,
        }
        if enable_reply_assist and self.token and self.state.get_contacted_ids():
            monitor_result = monitor_campaign_replies(
                token=self.token,
                campaign_id=self.campaign_id,
                contacted_blogger_ids=self.state.get_contacted_ids(),
                page_size=max(20, page_size),
            )
            replies = monitor_result.get("replies") or []
            reply_summary["newReplies"] = len(replies)

            candidate_items = []
            for reply in replies:
                intent = self._classify_intent(reply)
                self.state.record_reply(reply, classification=intent)
                reply_summary["classified"][intent] += 1
                candidate_items.append({
                    "id": reply.get("emailId") or reply.get("id"),
                    "chatId": reply.get("chatId"),
                    "bloggerId": reply.get("bloggerId"),
                    "bloggerName": reply.get("bloggerName") or reply.get("bloggerUserName"),
                    "bloggerUserName": reply.get("bloggerUserName"),
                    "subject": reply.get("subject"),
                    "cleanContent": reply.get("cleanContent") or reply.get("content"),
                    "content": reply.get("content") or reply.get("cleanContent"),
                })

            if candidate_items:
                reply_model_input = build_input_from_inbox(
                    token=self.token,
                    page_size=max(20, page_size),
                    only_unread=False,
                    only_unreplied=False,
                    limit=len(candidate_items),
                    include_dialogue=True,
                    candidate_items=candidate_items,
                )
                reply_model_analysis = injected_reply_analysis
                if require_reply_model_analysis and not reply_model_analysis:
                    host_reply_request = build_reply_analysis_request(
                        campaign_id=self.campaign_id,
                        cycle_no=cycle_no,
                        reply_model_input=reply_model_input,
                    )
                    strict_mode_contract = {
                        "enabled": True,
                        "needsReplyModelAnalysis": True,
                        "status": "waiting_for_host_reply_analysis",
                        "nextRecommendedAction": "Use replyModelInput with the conversation-analysis prompt/schema via the host model, write valid reply_model_analysis, then rerun scheduled_cycle.",
                        "replyModelInput": reply_model_input,
                        "acceptedInputField": "reply_model_analysis",
                        "acceptedSchema": "references/conversation-analysis-schema.md",
                        "promptPath": "prompts/conversation-analysis.md",
                        "candidateCount": len(candidate_items),
                        "validation": None,
                        "hostReplyAnalysisRequest": host_reply_request,
                    }
                    reply_execution = {
                        "status": "waiting_for_host_reply_analysis",
                        "sent": 0,
                        "blocked": len(candidate_items),
                        "prepared": 0,
                    }
                elif require_reply_model_analysis and injected_reply_analysis_validation and not injected_reply_analysis_validation.get("ok"):
                    strict_mode_contract = {
                        "enabled": True,
                        "needsReplyModelAnalysis": True,
                        "status": "model_analysis_invalid",
                        "nextRecommendedAction": "Fix reply_model_analysis so every item includes replyId/chatId, conversationStage, and replyBody, then rerun the campaign cycle.",
                        "replyModelInput": reply_model_input,
                        "acceptedInputField": "reply_model_analysis",
                        "acceptedSchema": "references/conversation-analysis-schema.md",
                        "promptPath": "prompts/conversation-analysis.md",
                        "candidateCount": len(candidate_items),
                        "validation": injected_reply_analysis_validation,
                        "analysisProvenance": {"source": "external_model", "confidence": "high", "validation": injected_reply_analysis_validation},
                    }
                    reply_execution = {
                        "status": "model_analysis_invalid",
                        "sent": 0,
                        "blocked": len(candidate_items),
                        "prepared": 0,
                    }
                else:
                    if require_reply_model_analysis and reply_model_analysis:
                        self.state.save_reply_model_analysis(reply_model_analysis, source="host_model_or_external")
                    reply_previews = ReplyProcessor.generate_preview(
                        reply_model_analysis or {},
                        template="Thank you for your message.",
                    ) if reply_model_analysis else {}

                for preview in reply_previews:
                    model_classification = ((preview.get("contextSummary") or {}).get("analysis") or {})
                    assist_classification = model_classification if isinstance(model_classification, dict) and model_classification else self._reply_assist_classification(preview.get("latestMail") or preview)
                    risk = ReplyProcessor.classify_risk(preview.get("latestMail") or preview, assist_classification)
                    action = {
                        "replyId": str(preview.get("replyId") or ""),
                        "bloggerId": preview.get("bloggerId"),
                        "nickname": preview.get("nickname"),
                        "subject": preview.get("subject") or "",
                        "classification": assist_classification.get("classification"),
                        "conversationStage": (preview.get("contextSummary") or {}).get("stage"),
                        "analysisMode": preview.get("analysisMode"),
                        "riskLevel": risk.get("riskLevel"),
                        "deliveryMode": "auto_send" if risk.get("autoSendAllowed") else "human_review",
                        "status": "eligible" if risk.get("autoSendAllowed") else "blocked",
                        "reviewRequired": risk.get("reviewRequired"),
                        "reasons": risk.get("reasons"),
                        "latestIncoming": ((preview.get("contextSummary") or {}).get("latestIncoming") or (preview.get("latestMail") or {}).get("cleanContent") or ""),
                        "replyPreview": {
                            "replyId": preview.get("replyId"),
                            "chatId": preview.get("chatId"),
                            "bloggerId": preview.get("bloggerId"),
                            "nickname": preview.get("nickname"),
                            "subject": preview.get("subject") or "",
                            "body": preview.get("plainTextBody") or preview.get("body") or "",
                        },
                    }
                    if action["replyId"]:
                        self.state.record_reply_action(action["replyId"], action)
                    reply_actions.append(action)

                customer_reply_review_summary = _build_customer_reply_review_summary(reply_actions)

                if reply_previews and reply_policy_info.get("executeSend") and not reply_policy_info.get("reviewRequired"):
                    auto_send_reply_ids = {
                        str(item.get("replyId") or "")
                        for item in reply_actions
                        if item.get("deliveryMode") == "auto_send" and str(item.get("replyId") or "")
                    }
                    auto_send_previews = [
                        item for item in reply_previews
                        if str(item.get("replyId") or "") in auto_send_reply_ids
                    ]
                    commands = ReplyProcessor.build_commands(auto_send_previews, dry_run=False)
                    execution_results = ReplyProcessor.run_commands(commands, campaign_id=self.campaign_id)
                    reply_execution = {
                        "status": "executed" if any(x.get("status") == "success" for x in execution_results) else "completed_without_send",
                        "sent": len([x for x in execution_results if x.get("status") == "success"]),
                        "blocked": len([x for x in execution_results if x.get("status") == "blocked"]),
                        "failed": len([x for x in execution_results if x.get("status") in {"failed", "error"}]),
                        "prepared": len(auto_send_previews),
                        "results": execution_results,
                    }
                elif reply_previews:
                    reply_execution = {
                        "status": "review_required" if reply_policy_info.get("reviewRequired") else "prepared",
                        "sent": 0,
                        "blocked": len([x for x in reply_actions if x.get("reviewRequired")]),
                        "prepared": len(reply_previews),
                    }

                if require_reply_model_analysis and reply_model_analysis and injected_reply_analysis_validation and injected_reply_analysis_validation.get("ok"):
                    strict_mode_contract = {
                        "enabled": True,
                        "needsReplyModelAnalysis": False,
                        "status": "model_analysis_valid",
                        "nextRecommendedAction": "Reply previews generated successfully; continue with risk review or safe send policy as configured.",
                        "replyModelInput": None,
                        "acceptedInputField": "reply_model_analysis",
                        "acceptedSchema": "references/conversation-analysis-schema.md",
                        "promptPath": "prompts/conversation-analysis.md",
                        "candidateCount": len(candidate_items),
                        "analysisCount": len((reply_model_analysis or {}).get("items") or []),
                        "validation": injected_reply_analysis_validation,
                    }
        result["replies"] = reply_summary
        result["replyActions"] = {
            "count": len(reply_actions),
            "items": reply_actions,
            "autoSendEligible": len([x for x in reply_actions if x.get("deliveryMode") == "auto_send"]),
            "humanReviewRequired": len([x for x in reply_actions if x.get("reviewRequired")]),
            "execution": reply_execution,
            "modelInputCount": len((reply_model_input or {}).get("items") or []),
            "modelAnalysisCount": len((reply_model_analysis or {}).get("items") or []),
            "previewCount": len(reply_previews),
            "highRiskSummary": customer_reply_review_summary,
            "customerSummary": customer_reply_review_summary.get("text") or "",
        }
        result["replyStrictMode"] = strict_mode_contract
        result["hostReplyAnalysisRequest"] = strict_mode_contract.get("hostReplyAnalysisRequest")
        self.state.update_cycle_section(cycle_no, "replies", result["replies"])
        self.state.update_cycle_section(cycle_no, "replyActions", result["replyActions"])

        progress = self.state.get_progress()
        cycle_summary = build_cycle_summary(result)
        result["cycleSummary"] = cycle_summary
        result["humanCycleSummary"] = build_human_cycle_summary(result)
        result["progress"] = progress
        result["endedAt"] = datetime.now().astimezone().isoformat(timespec="seconds")
        self.state.finish_cycle(cycle_no, summary={"progress": progress, "send": result.get("send"), "replyActions": result.get("replyActions"), "replyStrictMode": result.get("replyStrictMode"), "protocol": result.get("protocol"), "cycleSummary": cycle_summary})
        result["statePath"] = str(self.state.path)
        result["stateSummary"] = {
            "contacted": len(self.state.data.get("contacted") or {}),
            "replies": len(self.state.data.get("replies") or {}),
            "replyActions": len(self.state.data.get("replyActions") or {}),
            "metrics": self.state.data.get("metrics") or {},
        }
        return result


def load_brief(brief_path: Union[str, Path]) -> dict[str, Any]:
    return json.loads(Path(brief_path).read_text())


def run_engine_from_brief(
    *,
    campaign_id: str,
    brief_path: Union[str, Path],
    token: Optional[str]= None,
    target_count: Optional[int]= None,
    mode: str = "single_cycle",
    page_size: int = 10,
    send_policy: Optional[str]= None,
    reply_send_policy: Optional[str]= None,
    review_required: Optional[bool]= None,
    timing: str = "",
) -> dict[str, Any]:
    brief = load_brief(brief_path)
    resolved_token = get_token(token, required=False)
    engine = CampaignEngine(campaign_id=campaign_id, brief=brief, token=resolved_token, target_count=target_count)
    return engine.run_cycle(
        mode=mode,
        page_size=page_size,
        send_policy=send_policy,
        reply_send_policy=reply_send_policy,
        review_required=review_required,
        timing=timing,
    )
