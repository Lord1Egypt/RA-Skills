#!/usr/bin/env python3
"""Single-shot task execution for WotoHub API.

Design principle: host-model-first understanding, script-first execution.
- Host model layer: semantic analysis, strategy generation, ranking, draft generation
- Script layer: deterministic payload compilation, API execution
"""

from __future__ import annotations

import json
from typing import Any, Optional

from api_types import TaskType
import subprocess
import os


def _unique_keep_order(values: list[Any]) -> list[Any]:
    out: list[Any] = []
    seen: set[str] = set()
    for value in values or []:
        if value in (None, '', [], {}):
            continue
        key = json.dumps(value, ensure_ascii=False, sort_keys=True) if isinstance(value, (dict, list)) else str(value).strip().lower()
        if not key or key in seen:
            continue
        seen.add(key)
        out.append(value)
    return out


def _to_advanced_keywords(values: list[Any], limit: int = 8) -> list[dict[str, Any]]:
    from build_search_payload import focus_advanced_keywords

    normalized = []
    for value in _unique_keep_order(values):
        text = str(value or '').strip()
        if not text:
            continue
        normalized.append({"value": text, "exclude": False})
    return focus_advanced_keywords(normalized, limit=limit)


def _select_core_keywords(model_analysis: dict[str, Any], limit: int = 2) -> list[str]:
    product = model_analysis.get("product") or {}
    marketing = model_analysis.get("marketing") or {}

    candidates: list[str] = []
    product_name = str(product.get("productName") or "").strip()
    product_type = str(product.get("productType") or "").strip()
    product_subtype = str(product.get("productSubtype") or "").strip()

    if product_type:
        candidates.append(product_type)
    if product_subtype and product_subtype.lower() != product_type.lower():
        candidates.append(product_subtype)

    for item in product.get("categoryForms") or []:
        text = str(item or "").strip()
        if text:
            candidates.append(text)

    if not candidates and product_name:
        candidates.append(product_name)

    content_angles = [str(x).strip() for x in (marketing.get("contentAngles") or []) if str(x).strip()]
    refined: list[str] = []
    for candidate in _unique_keep_order(candidates):
        low = candidate.lower()
        if any(token in low for token in ["review", "comparison", "test ride", "minute", "battery", "brake", "motor", "speed"]):
            continue
        refined.append(candidate)
        if len(refined) >= limit:
            break

    if not refined:
        refined = [str(x).strip() for x in _unique_keep_order(candidates) if str(x).strip()][:limit]

    return refined[:limit]


def _compile_payload_from_model_analysis(model_analysis: dict[str, Any], input_data: dict[str, Any]) -> dict[str, Any]:
    """Compile payload through the shared standard mapping chain, not near-final hints."""
    import claw_search
    from context_schema import normalize_context
    from build_search_payload import build_payload_from_context, should_expect_category_mapping, build_semantic_input_from_model_analysis

    model_analysis = model_analysis or {}
    product = model_analysis.get("product") or {}
    marketing = model_analysis.get("marketing") or {}
    constraints = model_analysis.get("constraints") or {}

    target_markets = []
    for item in ([input_data.get("country")] if input_data.get("country") else []):
        text = str(item or "").strip().lower()
        if text and text not in target_markets:
            target_markets.append(text)
    for item in (constraints.get("regions") or []):
        text = str(item or "").strip().lower()
        if text and text not in target_markets:
            target_markets.append(text)

    languages = []
    raw_langs = input_data.get("blogLangs") or constraints.get("languages") or []
    if isinstance(raw_langs, str):
        raw_langs = [raw_langs]
    for item in raw_langs:
        text = str(item or "").strip().lower()
        if text and text not in languages:
            languages.append(text)

    features = []
    for item in [*(product.get("coreBenefits") or []), *(product.get("features") or [])]:
        text = str(item or "").strip()
        if text and text not in features:
            features.append(text)

    creator_types = []
    for item in (marketing.get("creatorTypes") or []):
        text = str(item or "").strip()
        if text and text not in creator_types:
            creator_types.append(text)

    ctx = normalize_context({
        "intent": {"primaryTask": "search"},
        "productSignals": {
            "rawInput": input_data.get("input"),
            "urls": [input_data.get("input")] if str(input_data.get("input") or "").startswith(("http://", "https://")) else [],
            "productName": product.get("productName"),
            "brand": product.get("brand"),
            "category": product.get("productSubtype") or product.get("productType"),
            "features": features,
            "useCases": product.get("functions") or [],
        },
        "marketingContext": {
            "targetMarkets": target_markets,
            "platforms": [input_data.get("platform")] if input_data.get("platform") else (marketing.get("platformPreference") or []),
            "creatorTypes": creator_types,
            "followerRange": {
                "min": input_data.get("minFansNum") if input_data.get("minFansNum") is not None else constraints.get("minFansNum"),
                "max": input_data.get("maxFansNum") if input_data.get("maxFansNum") is not None else constraints.get("maxFansNum"),
            },
            "languages": languages,
        },
        "resolvedArtifacts": {
            "modelAnalysis": model_analysis,
            "productSummary": input_data.get("productSummary"),
        },
        "meta": {
            "usedHostModel": True,
            "usedFallback": False,
            "analysisPath": "api_task_runner_standard_compiler",
        },
    })

    payload: dict[str, Any] = build_payload_from_context(ctx)
    semantic = build_semantic_input_from_model_analysis(model_analysis)
    category_expected = should_expect_category_mapping({
        "productSummary": {
            "productTypeHint": product.get("productType"),
            "detectedForms": product.get("categoryForms") or [],
            "keywordHints": [product.get("productSubtype"), product.get("productType")],
        },
        "searchConditions": model_analysis.get("searchConditions") or {},
    }, semantic, query=str(input_data.get("input") or product.get("productName") or ""))

    explicit_overrides = {
        "platform": input_data.get("platform"),
        "blogLangs": input_data.get("blogLangs"),
        "minFansNum": input_data.get("minFansNum"),
        "maxFansNum": input_data.get("maxFansNum"),
        "hasEmail": input_data.get("hasEmail"),
        "pageSize": input_data.get("pageSize"),
        "pageNum": input_data.get("pageNum"),
        "searchSort": input_data.get("searchSort"),
        "viewVolumeCombination": input_data.get("viewVolumeCombination"),
        "searchFilterList": input_data.get("searchFilterList"),
    }
    for key, value in explicit_overrides.items():
        if value not in (None, '', [], {}):
            payload[key] = value

    explicit_keywords = input_data.get("keywords") or []
    if explicit_keywords:
        payload["advancedKeywordList"] = _to_advanced_keywords(explicit_keywords, limit=8)
        payload["searchType"] = "KEYWORD"

    if category_expected and not payload.get("blogCateIds"):
        raise ValueError(
            "CATEGORY_MAPPING_REQUIRED: host/model analysis indicates this search should compile blogCateIds first, but the standard compiler produced none."
        )

    if payload.get("blogCateIds") and not payload.get("advancedKeywordList"):
        payload.pop("searchType", None)

    payload.setdefault("pageNum", 1)
    payload.setdefault("pageSize", 50)
    payload.setdefault("hasEmail", True)
    payload.setdefault("searchFilterList", ["THIS_UNTOUCH"])

    return claw_search.normalize_search_payload(payload)


class TaskRunner:
    """Execute single-shot tasks. Minimal wrapper around existing scripts."""

    def __init__(self, token: Optional[str]= None):
        self.token = token

    def run(self, task_type: str, input_data: dict, config: Optional[dict]= None) -> dict:
        """Execute task. Dispatch to handler."""
        handlers = {
            TaskType.PRODUCT_ANALYSIS.value: self._product_analysis,
            TaskType.SEARCH.value: self._search,
            TaskType.RECOMMEND.value: self._recommend,
            TaskType.GENERATE_EMAIL.value: self._generate_email,
            TaskType.SEND_EMAIL.value: self._send_email,
            TaskType.MONITOR_REPLIES.value: self._monitor_replies,
            "campaign_create": self._campaign_create,
        }
        handler = handlers.get(task_type)
        if not handler:
            raise ValueError(f"Unknown task type: {task_type}")
        return handler(input_data, config or {})

    def _product_analysis(self, input_data: dict, config: dict) -> dict:
        """Model-first: semantic understanding of product."""
        import product_resolve
        result = product_resolve.resolve_product(
            input_data["input"],
            mode=input_data.get("mode", "auto"),
            timeout=input_data.get("timeout", 12),
            host_analysis=input_data.get("hostAnalysis") or input_data.get("modelAnalysis"),
            product_summary=input_data.get("productSummary"),
        )
        return {
            "productSummary": result.get("productSummary", {}),
            "analysis": result.get("analysis", {}),
            "fallback": result.get("fallback"),
        }

    def _search(self, input_data: dict, config: dict) -> dict:
        """Script-first: deterministic search execution with retry.

        Preferred contract: caller provides host-generated strategy in input.strategy.
        Fallback: if missing, use rule-based strategy from productSummary.
        """
        from execution_layer import retry_api_call
        import claw_search

        model_analysis = input_data.get("modelAnalysis") or input_data.get("model_analysis")
        if model_analysis:
            payload = _compile_payload_from_model_analysis(model_analysis, input_data)
        else:
            raise ValueError("HOST_ANALYSIS_REQUIRED: main search chain requires structured understanding before executing search.")

        token = self.token or config.get("token")
        path = claw_search.claw_search_path() if token else claw_search.open_search_path()

        # Execute search with retry
        def _search():
            search_output = claw_search.execute_search(path, token, payload)
            enriched = claw_search.enrich_recommendations(search_output)
            return enriched

        result = retry_api_call(_search, max_retries=3, base_delay=1.0)
        return {
            "results": result.get("topRecommendations", []),
            "count": result.get("count", len(result.get("topRecommendations", []))),
            "recallCount": result.get("recallCount", 0),
            "payload": payload,
            "tableRows": result.get("tableRows", []),
            "summary": result.get("summary"),
            "priorityText": result.get("priorityText"),
            "displayText": result.get("displayText"),
            "markdownTable": result.get("markdownTable"),
            "plainTextTable": result.get("plainTextTable"),
            "rankingMode": result.get("rankingMode"),
            "recommendationLayers": result.get("recommendationLayers", {}),
        }

    def _recommend(self, input_data: dict, config: dict) -> dict:
        """Recommendation ranking.

        Preferred contract: host model should already rerank or annotate candidates.
        This task currently applies existing deterministic rerank/formatting helpers
        on top of host-understood candidate sets. It should not become a substitute
        for the main understanding layer.
        """
        import claw_search
        if not (input_data.get("modelAnalysis") or input_data.get("model_analysis")):
            return {
                "recommendations": [],
                "topN": [],
                "needsHostAnalysis": True,
                "status": "needs_user_input",
                "missingFields": ["hostAnalysis"],
                "message": "当前无法继续推荐，还缺少结构化理解结果。",
            }
        search_results = input_data.get("searchResults") or []
        if not search_results:
            return {
                "recommendations": [],
                "topN": [],
                "needsUserInput": True,
                "status": "needs_user_input",
                "missingFields": ["searchResults"],
                "message": "当前无法继续推荐，还缺少候选达人结果。",
            }
        synthetic_search_output = {
            "data": {"list": search_results},
            "payload": input_data.get("searchPayload") or {},
        }
        enriched = claw_search.enrich_recommendations(synthetic_search_output)
        return {
            "recommendations": enriched.get("topRecommendations", []),
            "topN": (enriched.get("topRecommendations") or [])[:10],
            "count": enriched.get("count", len(enriched.get("topRecommendations", []))),
            "summary": enriched.get("summary"),
            "priorityText": enriched.get("priorityText"),
            "displayText": enriched.get("displayText"),
            "markdownTable": enriched.get("markdownTable"),
            "plainTextTable": enriched.get("plainTextTable"),
            "tableRows": enriched.get("tableRows", []),
            "rankingMode": enriched.get("rankingMode"),
            "recommendationLayers": enriched.get("recommendationLayers", {}),
        }

    def _generate_email(self, input_data: dict, config: dict) -> dict:
        """Prepare sendable email drafts.

        Preferred contract: caller provides hostDrafts generated by the host model.
        Fallback draft generation is disabled by default and must be explicitly allowed upstream.
        Explicit target set may come from selectedCreators or sendTargetCreatorIds.
        """
        from execution_layer import prepare_emails_from_host_drafts, normalize_email_once

        host_drafts = input_data.get("hostDrafts") or input_data.get("emailModelDrafts") or []
        selected_creators = input_data.get("selectedCreators") or []
        explicit_target_ids = {
            str(value)
            for value in (input_data.get("sendTargetCreatorIds") or [])
            if value not in (None, "")
        }
        creator_target_ids = {
            str(item.get("bloggerId") or item.get("besId") or item.get("id"))
            for item in selected_creators
            if isinstance(item, dict) and (item.get("bloggerId") or item.get("besId") or item.get("id"))
        }
        allowed_ids = explicit_target_ids or creator_target_ids

        if not (input_data.get("modelAnalysis") or input_data.get("model_analysis")):
            return {
                "emails": [],
                "needsHostAnalysis": True,
                "needsHostDrafts": not bool(host_drafts),
                "selectedCreatorCount": len(allowed_ids),
                "emailLanguage": input_data.get("emailLanguage") or config.get("language") or "en",
                "status": "needs_user_input",
                "missingFields": ["hostAnalysis"],
            }

        emails = prepare_emails_from_host_drafts(host_drafts)
        if allowed_ids:
            emails = [
                email for email in emails
                if str(email.get("bloggerId") or email.get("besId") or email.get("id")) in allowed_ids
            ]
        emails = [normalize_email_once(email) for email in emails]
        return {
            "emails": emails,
            "needsHostAnalysis": False,
            "needsHostDrafts": len(emails) == 0,
            "selectedCreatorCount": len(allowed_ids),
            "emailLanguage": input_data.get("emailLanguage") or config.get("language") or "en",
        }

    def _send_email(self, input_data: dict, config: dict) -> dict:
        """Script-first: deterministic send execution.

        Only explicit selected creators + prepared drafts may enter this path.
        Do not synthesize send targets from search results at execution time.
        """
        from send_generated_emails import build_batch_payload, send_batch
        from html_email_utils import plain_text_to_html, normalize_html_body
        from draft_consistency_audit import build_creator_profile_map

        emails = []
        allowed_creator_ids = {
            str(value)
            for value in (input_data.get("sendTargetCreatorIds") or [])
            if value not in (None, "")
        }

        creator_profile_candidates = []
        for key in ("selectedCreators", "creatorProfiles", "searchResults", "recommendations"):
            value = input_data.get(key)
            if isinstance(value, list):
                creator_profile_candidates.extend([item for item in value if isinstance(item, dict)])
            elif isinstance(value, dict):
                for nested_key in ("items", "topRecommendations", "bloggerList", "records", "list", "rows", "dataList"):
                    nested = value.get(nested_key)
                    if isinstance(nested, list):
                        creator_profile_candidates.extend([item for item in nested if isinstance(item, dict)])
                result_data = ((value.get("result") or {}).get("data") or {}) if isinstance(value.get("result"), dict) else {}
                if isinstance(result_data, dict):
                    for nested_key in ("bloggerList", "records", "list", "rows", "dataList"):
                        nested = result_data.get(nested_key)
                        if isinstance(nested, list):
                            creator_profile_candidates.extend([item for item in nested if isinstance(item, dict)])
        creator_profiles_by_id = build_creator_profile_map(creator_profile_candidates)

        personalized_drafts = input_data.get("drafts") or input_data.get("generatedDrafts") or input_data.get("hostDrafts") or input_data.get("emailModelDrafts") or []
        if personalized_drafts:
            for draft in personalized_drafts:
                blogger_id = draft.get("bloggerId") or draft.get("besId") or draft.get("id")
                blogger_id = None if blogger_id in (None, "") else str(blogger_id)
                if allowed_creator_ids and blogger_id not in allowed_creator_ids:
                    continue
                nickname = draft.get("nickname") or draft.get("channelName") or draft.get("username")
                subject = draft.get("subject") or input_data.get("subject") or "Partnership Opportunity"
                html_body = draft.get("htmlBody") or ""
                plain_body = draft.get("plainTextBody") or draft.get("body") or draft.get("content") or ""
                if not html_body and plain_body:
                    html_body = normalize_html_body(plain_text_to_html(plain_body))
                if not blogger_id or not subject or not (html_body or plain_body):
                    continue
                emails.append({
                    "bloggerId": blogger_id,
                    "nickname": nickname,
                    "subject": subject,
                    "body": plain_body or html_body,
                    "plainTextBody": plain_body or html_body,
                    "htmlBody": html_body,
                    "draftSource": draft.get("draftSource") or draft.get("source") or input_data.get("draftSource") or "host-model",
                    "emailAvailable": True,
                })
        else:
            for email in (input_data.get("emails") or []):
                blogger_id = email.get("bloggerId") or email.get("besId") or email.get("id")
                blogger_id = None if blogger_id in (None, "") else str(blogger_id)
                if allowed_creator_ids and blogger_id not in allowed_creator_ids:
                    continue
                normalized_email = dict(email)
                if blogger_id:
                    normalized_email["bloggerId"] = blogger_id
                emails.append(normalized_email)

        batch = build_batch_payload(
            {"emails": emails},
            expected_language=input_data.get("emailLanguage") or config.get("language", "en"),
            allow_fallback_send=bool(config.get("allowFallbackSend", False)),
            creator_profiles_by_id=creator_profiles_by_id,
        )
        result = send_batch(batch, dry_run=config.get("dryRun", True))
        return {
            "sent": result.get("sent", []),
            "failed": result.get("failed", []),
            "status": result.get("status"),
            "count": result.get("count", 0),
            "response": result.get("response"),
            "bloggerInfos": result.get("bloggerInfos", []),
            "emails": result.get("emails", []),
            "allowedCreatorIds": sorted(allowed_creator_ids),
        }

    def _monitor_replies(self, input_data: dict, config: dict) -> dict:
        """Script-first: deterministic reply monitoring."""
        from incremental_monitor import monitor_campaign_replies
        from reply_processor import ReplyProcessor
        from campaign_state_store import CampaignStateStore

        coerced_reply_analysis = ReplyProcessor.coerce_model_reply_analysis(input_data.get("replyModelAnalysis"))
        validation = ReplyProcessor.validate_model_reply_analysis(coerced_reply_analysis)
        campaign_id = str(input_data.get("campaignId") or config.get("campaignId") or "").strip()
        if not campaign_id:
            return {
                "replies": [],
                "count": 0,
                "status": "needs_user_input",
                "missingFields": ["campaignId"],
                "message": "monitor_replies 需要 campaignId。",
            }
        if not coerced_reply_analysis:
            return {
                "replies": [],
                "count": 0,
                "needsHostAnalysis": True,
                "status": "needs_user_input",
                "missingFields": ["replyModelAnalysis"],
                "message": "当前无法继续回复辅助，还缺少对话理解结果。",
            }
        if not validation.get("ok"):
            return {
                "replies": [],
                "count": 0,
                "needsHostAnalysis": True,
                "status": "needs_user_input",
                "missingFields": ["replyModelAnalysis"],
                "message": "replyModelAnalysis 结构不合规，当前无法继续回复辅助。",
                "validation": validation,
            }
        token = str(
            config.get("token")
            or input_data.get("token")
            or os.environ.get("WOTOHUB_API_KEY")
            or ""
        ).strip()
        if not token:
            return {
                "replies": [],
                "count": 0,
                "status": "needs_user_input",
                "missingFields": ["token"],
                "message": "monitor_replies 需要可用 token。",
            }
        contacted_ids = input_data.get("contactedBloggerIds") or config.get("contactedBloggerIds") or []
        if not contacted_ids:
            contacted_ids = sorted(CampaignStateStore(campaign_id).get_contacted_ids())
        if not contacted_ids:
            return {
                "replies": [],
                "count": 0,
                "status": "needs_user_input",
                "missingFields": ["contactedBloggerIds"],
                "message": "monitor_replies 需要已联系达人列表，当前 campaign state 中也没有可用记录。",
            }
        monitor_result = monitor_campaign_replies(
            token=token,
            campaign_id=campaign_id,
            contacted_blogger_ids={str(x) for x in contacted_ids if str(x).strip()},
            page_size=int(config.get("pageSize") or input_data.get("pageSize") or 50),
        )
        return {
            "campaignId": campaign_id,
            "replies": monitor_result.get("replies", []),
            "count": int(monitor_result.get("new_replies_count") or 0),
            "monitorSummary": monitor_result,
            "replyModelAnalysis": coerced_reply_analysis,
            "validation": validation,
        }

    def _campaign_create(self, input_data: dict, config: dict) -> dict:
        """Create scheduled campaign artifacts without affecting one-shot task chain.

        Main-chain principle:
        - host model / upper layer understands user intent first
        - this layer compiles canonical brief and persists it
        - OpenClaw cron is preferred for scheduling, but only after required fields are complete
        """
        from campaign_planner import build_campaign_plan, build_brief_from_campaign_plan
        from campaign_registry import save_campaign_brief, save_campaign_registry_entry

        raw_input = input_data.get("input") or ""
        semantic_context = input_data.get("semanticContext") or {}
        legacy_input = input_data.get("legacyInput") or {}
        campaign_id = input_data.get("campaignId") or config.get("campaignId") or "scheduled-campaign"
        create_cron = bool(config.get("createCron") or input_data.get("createCron"))

        plan = build_campaign_plan(
            raw_input=raw_input,
            semantic_context=semantic_context,
            legacy_input=legacy_input,
            config=config,
        )
        missing = plan.get("missingFields") or []
        brief = build_brief_from_campaign_plan(campaign_id, plan)
        brief_path = save_campaign_brief(campaign_id, brief)
        registry_path = save_campaign_registry_entry(campaign_id, {
            "briefPath": brief_path,
            "status": "draft" if missing else "ready",
            "schedule": plan.get("schedule"),
            "draftPolicy": plan.get("draftPolicy"),
        })
        scheduler = brief.get("scheduler") or {}
        safe_cycle_command = (
            f"python3 run_cycle_via_skill.py --campaign-id {campaign_id} --brief-path {brief_path} --mode scheduled_cycle"
        )
        cron_spec = {
            "name": campaign_id,
            "description": f"WotoHub scheduled campaign for {campaign_id}",
            "schedule": scheduler,
            "payload": {
                "kind": "agentTurn",
                "message": (
                    f"Run WotoHub scheduled campaign cycle for campaignId={campaign_id}. "
                    f"Use this short safe command from the skill root: `{safe_cycle_command}`. "
                    f"Do not construct complex inline Python, nested JSON CLI args, or direct run_campaign.py / campaign_engine.py calls. "
                    f"If the result stops at waiting_for_host_analysis or waiting_for_host_drafts, follow the returned structured request and rerun via the same wrapper."
                ),
                "timeoutSeconds": 1800,
            },
            "sessionTarget": "isolated",
            "delivery": {"mode": "announce"},
        }

        cron_create = None
        if create_cron and not missing:
            cron_create = self._create_openclaw_cron(cron_spec)
            if cron_create.get("ok"):
                save_campaign_registry_entry(campaign_id, {
                    "status": "scheduled",
                    "cronJobId": cron_create.get("jobId"),
                    "cronName": campaign_id,
                })

        validation = plan.get("validation") or {}
        if validation.get("forbiddenScheduledSearchOverrides"):
            return {
                "campaignId": campaign_id,
                "campaignPlan": plan,
                "brief": brief,
                "briefPath": brief_path,
                "registryPath": registry_path,
                "cronSpec": cron_spec,
                "cronCreate": None,
                "needsUserInput": True,
                "missingFields": list(dict.fromkeys([*(missing or []), "scheduled_search_overrides_not_allowed"])),
                "status": "needs_user_input",
                "nextAction": "remove_forbidden_scheduled_search_overrides_then_retry",
                "error": {
                    "code": "SCHEDULED_SEARCH_OVERRIDE_NOT_ALLOWED",
                    "message": "Scheduled campaign creation must not inject near-final search payload fields. Use semantic inputs only and let the standard compiler build WotoHub search params.",
                    "details": {
                        "forbiddenFields": validation.get("forbiddenScheduledSearchOverrides") or [],
                    },
                },
            }

        result_status = "needs_user_input" if missing else ("scheduled" if (cron_create or {}).get("ok") else "ready")
        next_action = "fill_missing_fields_then_create_cron" if missing else ("monitor_cron_runs" if (cron_create or {}).get("ok") else "create_or_bind_cron")

        return {
            "campaignId": campaign_id,
            "campaignPlan": plan,
            "brief": brief,
            "briefPath": brief_path,
            "registryPath": registry_path,
            "cronSpec": cron_spec,
            "cronCreate": cron_create,
            "needsUserInput": bool(missing),
            "missingFields": missing,
            "status": result_status,
            "nextAction": next_action,
        }

    def _create_openclaw_cron(self, cron_spec: dict[str, Any]) -> dict[str, Any]:
        """Create OpenClaw cron job via current stable CLI contract.

        Keep this isolated to scheduled campaign create only.
        Do not reuse for one-shot task chain.

        Notes:
        - Prefer the official `openclaw cron add` surface over legacy `gateway cron`.
        - Keep payload explicit and fail loudly with structured errors.
        """
        schedule = cron_spec.get("schedule") or {}
        payload = cron_spec.get("payload") or {}
        delivery = cron_spec.get("delivery") or {}

        command = ["openclaw", "cron", "add", "--json"]

        name = cron_spec.get("name")
        if name:
            command.extend(["--name", str(name)])
        description = cron_spec.get("description")
        if description:
            command.extend(["--description", str(description)])

        schedule_kind = schedule.get("kind")
        if schedule_kind == "every" and schedule.get("everyMs"):
            every_ms = int(schedule.get("everyMs") or 0)
            if every_ms <= 0:
                return {"ok": False, "error": "invalid_schedule_everyMs"}
            if every_ms % 1000 != 0:
                return {"ok": False, "error": "everyMs_must_be_whole_seconds_for_cli"}
            command.extend(["--every", f"{every_ms // 1000}s"])
        elif schedule_kind == "cron" and schedule.get("expr"):
            command.extend(["--cron", str(schedule.get("expr"))])
            if schedule.get("tz"):
                command.extend(["--tz", str(schedule.get("tz"))])
            if schedule.get("staggerMs") == 0:
                command.append("--exact")
        elif schedule_kind == "at" and schedule.get("at"):
            command.extend(["--at", str(schedule.get("at"))])
        else:
            return {"ok": False, "error": f"unsupported_schedule: {schedule}"}

        session_target = cron_spec.get("sessionTarget") or "isolated"
        command.extend(["--session", str(session_target)])

        payload_kind = payload.get("kind")
        if payload_kind == "agentTurn":
            message = payload.get("message") or ""
            command.extend(["--message", str(message)])
            timeout_seconds = payload.get("timeoutSeconds")
            if timeout_seconds not in (None, ""):
                command.extend(["--timeout-seconds", str(int(timeout_seconds))])
            model = payload.get("model")
            if model:
                command.extend(["--model", str(model)])
            thinking = payload.get("thinking")
            if thinking:
                command.extend(["--thinking", str(thinking)])
            tools_allow = payload.get("toolsAllow")
            if isinstance(tools_allow, list) and tools_allow:
                command.extend(["--tools", ",".join(str(x) for x in tools_allow if str(x).strip())])
            if payload.get("lightContext"):
                command.append("--light-context")
        elif payload_kind == "systemEvent":
            text = payload.get("text") or ""
            command.extend(["--system-event", str(text)])
        else:
            return {"ok": False, "error": f"unsupported_payload_kind: {payload_kind}"}

        if delivery.get("mode") == "announce":
            command.append("--announce")
            if delivery.get("channel"):
                command.extend(["--channel", str(delivery.get("channel"))])
            if delivery.get("to"):
                command.extend(["--to", str(delivery.get("to"))])
            if delivery.get("bestEffort"):
                command.append("--best-effort-deliver")
        elif delivery.get("mode") == "none":
            command.append("--no-deliver")

        if cron_spec.get("enabled") is False:
            command.append("--disabled")

        gateway_url = os.environ.get("OPENCLAW_GATEWAY_URL")
        gateway_token = os.environ.get("OPENCLAW_GATEWAY_TOKEN")
        if gateway_url:
            command.extend(["--url", gateway_url])
        if gateway_token:
            command.extend(["--token", gateway_token])

        try:
            proc = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=False,
            )
        except Exception as exc:
            return {
                "ok": False,
                "error": f"failed_to_invoke_openclaw_cron_add: {exc}",
                "command": command,
            }

        stdout = (proc.stdout or "").strip()
        stderr = (proc.stderr or "").strip()
        if proc.returncode != 0:
            return {
                "ok": False,
                "error": stderr or stdout or f"openclaw cron add failed with code {proc.returncode}",
                "returncode": proc.returncode,
                "command": command,
            }

        parsed: Optional[dict[str, Any]]= None
        if stdout:
            try:
                parsed = json.loads(stdout)
            except Exception:
                parsed = {"raw": stdout}
        job_id = None
        if isinstance(parsed, dict):
            job_id = parsed.get("jobId") or parsed.get("id") or ((parsed.get("job") or {}).get("jobId")) or ((parsed.get("job") or {}).get("id"))
        return {
            "ok": True,
            "jobId": job_id,
            "response": parsed or stdout,
            "command": command,
        }
