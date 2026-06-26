#!/usr/bin/env python3
"""Campaign cycle execution for WotoHub API.

Minimal wrapper around campaign_engine, with a host-model-first runtime bridge for
scheduled per-cycle draft generation.

Release principle:
- host runtime / host model owns personalized draft generation
- script layer only orchestrates waiting -> request -> rerun
- runner must not masquerade as an internal model layer or silently fabricate
  personalized drafts as the main path
"""

from __future__ import annotations

import json
import os
import shlex
import subprocess
import tempfile
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any, Optional, Union

PROMPT_PATH = "prompts/outreach-email-generation.md"
SCHEMA_PATH = "references/outreach-email-schema.md"
HOST_ANALYSIS_SCHEMA_PATH = "references/model-analysis-schema.md"

from html_email_utils import normalize_html_body, html_to_plain_text
from campaign_reply_analysis import coerce_model_reply_analysis, validate_model_reply_analysis


class CampaignRunner:
    """Execute campaign cycles.

    Release principle:
    - host model first for semantic generation tasks
    - script layer stays deterministic for cycle execution
    - if scheduled cycle pauses for host drafts, this runner may orchestrate one
      host-draft generation round, then rerun deterministically
    """

    def run_cycle(self, campaign_id: str, brief: dict, config: Optional[dict]= None) -> dict:
        """Run one campaign cycle."""
        from campaign_engine import run_engine_from_brief

        config = config or {}
        host_analysis_resolution = self._ensure_host_analysis_for_cycle(
            campaign_id=campaign_id,
            brief=brief,
            config=config,
        )
        effective_brief = host_analysis_resolution.get("brief") or dict(brief or {})
        if host_analysis_resolution.get("result"):
            final_result = host_analysis_resolution["result"]
        else:
            first_result = self._run_engine_once(
                run_engine_from_brief,
                campaign_id=campaign_id,
                brief=effective_brief,
                config=config,
            )
            host_draft_generator = self._build_host_draft_generator(config, effective_brief)
            effective_config = dict(config or {})
            if host_draft_generator and not effective_config.get("hostDraftGenerator"):
                effective_config["hostDraftGenerator"] = host_draft_generator

            final_result = self._maybe_complete_with_host_drafts(
                run_engine_from_brief,
                campaign_id=campaign_id,
                brief=effective_brief,
                config=effective_config,
                first_result=first_result,
            )
            final_result = self._maybe_complete_with_host_reply_analysis(
                run_engine_from_brief,
                campaign_id=campaign_id,
                brief=effective_brief,
                config=effective_config,
                current_result=final_result,
            )
        pre_runtime = host_analysis_resolution.get("runtimeOrchestration") or {}
        if pre_runtime:
            merged_runtime = dict(pre_runtime)
            merged_runtime.update(final_result.get("runtimeOrchestration") or {})
            final_result["runtimeOrchestration"] = merged_runtime
        compact_error = self._extract_compact_error(final_result)
        status = self._derive_status(final_result, compact_error)
        return {
            "campaignId": campaign_id,
            "cycleNo": final_result.get("cycle") or final_result.get("cycleNo"),
            "status": status,
            "error": compact_error,
            "humanSummary": final_result.get("humanCycleSummary"),
            "progress": final_result.get("progress"),
            "summary": final_result.get("cycleSummary"),
            "nextAction": self._next_action(final_result),
            "draftGeneration": final_result.get("draftGeneration"),
            "runtimeOrchestration": final_result.get("runtimeOrchestration"),
            "hostAnalysisRequest": final_result.get("hostAnalysisRequest"),
            "hostDraftGenerationRequest": final_result.get("hostDraftGenerationRequest"),
            "hostReplyAnalysisRequest": final_result.get("hostReplyAnalysisRequest"),
            "rawResult": final_result,
        }

    def _ensure_host_analysis_for_cycle(self, *, campaign_id: str, brief: dict[str, Any], config: dict[str, Any]) -> dict[str, Any]:
        orchestration = {
            "enabled": bool(config.get("enableRuntimeOrchestration", True)),
            "attempted": False,
            "completed": False,
            "status": "not_needed",
            "hostAnalysisSource": None,
        }
        analysis = self._extract_host_analysis_artifact(brief, config)
        product_summary = self._extract_product_summary_artifact(brief, config)
        if analysis:
            orchestration.update({
                "completed": True,
                "status": "already_available",
                "hostAnalysisSource": "provided_by_input",
            })
            result = {
                "runtimeOrchestration": {
                    "hostAnalysis": orchestration,
                }
            }
            return {"brief": self._inject_host_analysis_into_brief(brief, analysis, product_summary), "result": None, "runtimeOrchestration": result}

        if not orchestration["enabled"]:
            orchestration["status"] = "disabled"
            return {
                "brief": dict(brief or {}),
                "result": {
                    "runtimeOrchestration": {"hostAnalysis": orchestration},
                    "hostAnalysisRequest": self._build_host_analysis_request(campaign_id=campaign_id, brief=brief, config=config),
                },
            }

        request = self._build_host_analysis_request(campaign_id=campaign_id, brief=brief, config=config)
        resolution = self._resolve_host_analysis_with_meta(request, brief, config)
        orchestration["attempted"] = True
        orchestration["hostAnalysisSource"] = resolution.get("source")
        if resolution.get("error"):
            orchestration["hostAnalysisError"] = resolution.get("error")
        if resolution.get("executor"):
            orchestration["hostAnalysisExecutor"] = resolution.get("executor")

        resolved_analysis = resolution.get("analysis")
        resolved_summary = resolution.get("productSummary")
        if resolved_analysis:
            orchestration.update({
                "completed": True,
                "status": "resolved_from_executor" if resolution.get("status") == "resolved_from_executor" else (resolution.get("status") or "resolved"),
                "hostAnalysisSource": resolution.get("source") or "host_analysis_bridge",
            })
            injected_brief = self._inject_host_analysis_into_brief(brief, resolved_analysis, resolved_summary)
            return {
                "brief": injected_brief,
                "result": None,
                "runtimeOrchestration": {"hostAnalysis": orchestration},
            }

        orchestration["status"] = resolution.get("status") or "waiting_for_external_host_analysis"
        waiting_result = {
            "runtimeOrchestration": {"hostAnalysis": orchestration},
            "hostAnalysisRequest": request,
        }
        return {"brief": dict(brief or {}), "result": waiting_result}

    def _extract_host_analysis_artifact(self, brief: dict[str, Any], config: dict[str, Any]) -> Optional[dict[str, Any]]:
        for container in (config, brief, (brief or {}).get("product") or {}):
            if not isinstance(container, dict):
                continue
            for key in ("hostAnalysis", "host_analysis", "understanding", "modelAnalysis", "model_analysis"):
                candidate = container.get(key)
                if isinstance(candidate, dict) and candidate:
                    return candidate
        return None

    def _extract_product_summary_artifact(self, brief: dict[str, Any], config: dict[str, Any]) -> Optional[dict[str, Any]]:
        for container in (config, brief):
            if not isinstance(container, dict):
                continue
            for key in ("productSummary", "hostProductSummary"):
                candidate = container.get(key)
                if isinstance(candidate, dict) and candidate:
                    return candidate
        return None

    def _inject_host_analysis_into_brief(self, brief: dict[str, Any], analysis: dict[str, Any], product_summary: Optional[dict[str, Any]]= None) -> dict[str, Any]:
        injected = dict(brief or {})
        injected["host_analysis"] = analysis
        injected["hostAnalysis"] = analysis
        injected["model_analysis"] = analysis
        injected["modelAnalysis"] = analysis
        if product_summary:
            injected["productSummary"] = product_summary
            injected["hostProductSummary"] = product_summary
        return injected

    def _resolve_host_analysis_with_meta(self, request: dict[str, Any], brief: dict[str, Any], config: dict[str, Any]) -> dict[str, Any]:
        injected = self._extract_host_analysis_artifact({}, config)
        if injected:
            return {
                "analysis": injected,
                "productSummary": self._extract_product_summary_artifact(brief, config),
                "source": "config_injected_host_analysis",
                "status": "resolved_from_config",
            }

        generator = config.get("hostAnalysisGenerator") or config.get("host_analysis_generator")
        if callable(generator):
            try:
                generated = generator({"hostAnalysisRequest": request, "brief": brief})
            except Exception as exc:
                return {
                    "analysis": None,
                    "productSummary": None,
                    "source": "host_runtime_callable",
                    "status": "host_analysis_generator_failed",
                    "error": f"{type(exc).__name__}: {exc}",
                }
            extracted = self._extract_host_analysis_from_payload(generated)
            if extracted.get("analysis"):
                return {**extracted, "source": "host_runtime_callable", "status": "resolved_from_callable"}

        bridge_executor = self._get_host_analysis_executor(config=config, brief=brief)
        if bridge_executor:
            bridge_payload = self.build_host_analysis_bridge_payload(request=request)
            try:
                generated = self._run_host_bridge_executor(bridge_payload=bridge_payload, executor_spec=bridge_executor)
            except Exception as exc:
                return {
                    "analysis": None,
                    "productSummary": None,
                    "source": "host_analysis_bridge_executor",
                    "status": "host_analysis_bridge_executor_failed",
                    "error": f"{type(exc).__name__}: {exc}",
                    "executor": self._describe_executor(bridge_executor),
                }
            extracted = self._extract_host_analysis_from_payload(generated)
            if extracted.get("analysis"):
                return {
                    **extracted,
                    "source": "host_analysis_bridge_executor",
                    "status": "resolved_from_executor",
                    "executor": self._describe_executor(bridge_executor),
                }
            return {
                "analysis": None,
                "productSummary": None,
                "source": "host_analysis_bridge_executor",
                "status": "host_analysis_bridge_executor_returned_invalid",
                "executor": self._describe_executor(bridge_executor),
            }

        return {"analysis": None, "productSummary": None, "source": None, "status": "waiting_for_external_host_analysis"}

    def _get_host_analysis_executor(self, *, config: dict[str, Any], brief: dict[str, Any]) -> Any:
        for key in ("hostAnalysisExecutor", "host_analysis_executor", "hostSemanticExecutor", "host_semantic_executor"):
            if config.get(key):
                return config.get(key)
        scheduler = brief.get("scheduler") or {}
        for container in (brief, scheduler):
            if not isinstance(container, dict):
                continue
            for key in ("hostAnalysisExecutor", "host_analysis_executor", "hostSemanticExecutor", "host_semantic_executor"):
                if container.get(key):
                    return container.get(key)
        env_default = os.environ.get("WOTOHUB_HOST_ANALYSIS_EXECUTOR") or os.environ.get("HOST_ANALYSIS_EXECUTOR")
        if env_default:
            return env_default
        return None

    def _build_host_analysis_request(self, *, campaign_id: str, brief: dict[str, Any], config: dict[str, Any]) -> dict[str, Any]:
        return {
            "task": "generate_host_analysis_for_campaign_cycle",
            "mode": "host_analysis_request",
            "campaign": {"campaignId": campaign_id},
            "input": {
                "rawInput": brief.get("input") or "",
                "brief": brief,
            },
            "schemaPath": HOST_ANALYSIS_SCHEMA_PATH,
            "deliveryContract": {
                "field": "host_analysis",
                "acceptedAliases": ["host_analysis", "hostAnalysis", "understanding", "modelAnalysis", "model_analysis"],
                "canonicalField": "host_analysis",
            },
            "runtimeHints": {
                "modelUnderstandingRequired": True,
                "runnerAutoGenerationAllowed": False,
                "targetUseCases": ["scheduled_search", "campaign_cycle", "host_model_first_search_compile"],
                "platform": brief.get("platform") or ((brief.get("search") or {}).get("platform")) or config.get("platform") or "tiktok",
            },
        }

    def _extract_host_analysis_from_payload(self, payload: Any) -> dict[str, Any]:
        if isinstance(payload, dict):
            analysis = None
            for key in ("host_analysis", "hostAnalysis", "understanding", "modelAnalysis", "model_analysis", "analysis"):
                candidate = payload.get(key)
                if isinstance(candidate, dict) and candidate:
                    analysis = candidate
                    break
            product_summary = None
            for key in ("productSummary", "hostProductSummary"):
                candidate = payload.get(key)
                if isinstance(candidate, dict) and candidate:
                    product_summary = candidate
                    break
            return {"analysis": analysis, "productSummary": product_summary}
        return {"analysis": None, "productSummary": None}

    def _run_engine_once(self, run_engine_from_brief, *, campaign_id: str, brief: dict[str, Any], config: dict[str, Any]) -> dict[str, Any]:
        brief_path = self._save_brief(brief)
        try:
            return run_engine_from_brief(
                campaign_id=campaign_id,
                brief_path=brief_path,
                token=config.get("token"),
                target_count=config.get("targetCount", 30),
                mode=config.get("mode", "single_cycle"),
                page_size=config.get("pageSize", 10),
                send_policy=config.get("sendPolicy"),
                reply_send_policy=config.get("replySendPolicy"),
                review_required=config.get("reviewRequired"),
                timing=config.get("timing", ""),
            )
        finally:
            try:
                Path(brief_path).unlink()
            except Exception:
                pass

    def _maybe_complete_with_host_drafts(
        self,
        run_engine_from_brief,
        *,
        campaign_id: str,
        brief: dict[str, Any],
        config: dict[str, Any],
        first_result: dict[str, Any],
    ) -> dict[str, Any]:
        draft_generation = first_result.get("draftGeneration") or {}
        orchestration = {
            "enabled": bool(config.get("enableRuntimeOrchestration", True)),
            "attempted": False,
            "completed": False,
            "status": "not_needed",
            "hostDraftSource": None,
        }

        if config.get("mode") != "scheduled_cycle":
            first_result["runtimeOrchestration"] = orchestration
            return first_result

        if draft_generation.get("status") != "waiting_for_host_drafts":
            first_result["runtimeOrchestration"] = orchestration
            return first_result

        if not orchestration["enabled"]:
            orchestration["status"] = "disabled"
            first_result["runtimeOrchestration"] = orchestration
            return first_result

        draft_input = draft_generation.get("draftGenerationInput") or {}
        resolution = self._resolve_host_drafts_with_meta(draft_input, brief, config)
        generated_host_drafts = resolution.get("drafts") or []
        generated_host_draft_metadata = resolution.get("metadata") or {}
        orchestration["attempted"] = True
        orchestration["hostDraftSource"] = resolution.get("source")
        if resolution.get("error"):
            orchestration["hostDraftError"] = resolution.get("error")
        if resolution.get("executor"):
            orchestration["hostDraftExecutor"] = resolution.get("executor")

        if not generated_host_drafts:
            orchestration["status"] = resolution.get("status") or "waiting_for_external_host_drafts"
            first_result["runtimeOrchestration"] = orchestration
            first_result["hostDraftGenerationRequest"] = self._build_host_draft_generation_request(
                draft_input=draft_input,
                brief=brief,
                config=config,
            )
            return first_result

        rerun_brief = dict(brief or {})
        rerun_brief["host_drafts_per_cycle"] = generated_host_drafts
        if generated_host_draft_metadata:
            rerun_brief["host_drafts_metadata_per_cycle"] = generated_host_draft_metadata
        rerun_result = self._run_engine_once(
            run_engine_from_brief,
            campaign_id=campaign_id,
            brief=rerun_brief,
            config=config,
        )
        orchestration.update({
            "completed": True,
            "status": "rerun_completed",
            "hostDraftSource": resolution.get("source") or "runtime_host_model_bridge",
            "generatedDraftCount": len(generated_host_drafts),
            "hostDraftMetadata": generated_host_draft_metadata,
        })
        rerun_result["runtimeOrchestration"] = orchestration
        return rerun_result

    def _maybe_complete_with_host_reply_analysis(
        self,
        run_engine_from_brief,
        *,
        campaign_id: str,
        brief: dict[str, Any],
        config: dict[str, Any],
        current_result: dict[str, Any],
    ) -> dict[str, Any]:
        strict_mode = current_result.get("replyStrictMode") or {}
        orchestration = dict(current_result.get("runtimeOrchestration") or {})
        orchestration.setdefault("replyAnalysis", {
            "enabled": bool(config.get("enableRuntimeOrchestration", True)),
            "attempted": False,
            "completed": False,
            "status": "not_needed",
            "hostReplyAnalysisSource": None,
        })
        reply_orch = orchestration["replyAnalysis"]

        if config.get("mode") != "scheduled_cycle":
            current_result["runtimeOrchestration"] = orchestration
            return current_result

        if strict_mode.get("status") != "waiting_for_host_reply_analysis":
            current_result["runtimeOrchestration"] = orchestration
            return current_result

        if not reply_orch.get("enabled"):
            reply_orch["status"] = "disabled"
            current_result["runtimeOrchestration"] = orchestration
            return current_result

        request = current_result.get("hostReplyAnalysisRequest") or strict_mode.get("hostReplyAnalysisRequest") or {}
        resolution = self._resolve_host_reply_analysis_with_meta(request, brief, config)
        resolved_analysis = resolution.get("analysis")
        reply_orch["attempted"] = True
        reply_orch["hostReplyAnalysisSource"] = resolution.get("source")
        if resolution.get("error"):
            reply_orch["hostReplyAnalysisError"] = resolution.get("error")
        if resolution.get("executor"):
            reply_orch["hostReplyAnalysisExecutor"] = resolution.get("executor")

        if not resolved_analysis:
            reply_orch["status"] = resolution.get("status") or "waiting_for_external_host_reply_analysis"
            current_result["runtimeOrchestration"] = orchestration
            return current_result

        rerun_brief = dict(brief or {})
        rerun_brief["reply_model_analysis"] = resolved_analysis
        rerun_result = self._run_engine_once(
            run_engine_from_brief,
            campaign_id=campaign_id,
            brief=rerun_brief,
            config=config,
        )
        reply_orch.update({
            "completed": True,
            "status": "rerun_completed",
            "hostReplyAnalysisSource": resolution.get("source") or "runtime_host_reply_bridge",
            "analysisCount": len((resolved_analysis or {}).get("items") or []),
        })
        rerun_result["runtimeOrchestration"] = orchestration
        return rerun_result

    def _resolve_host_drafts(self, draft_input: dict[str, Any], brief: dict[str, Any], config: dict[str, Any]) -> list[dict[str, Any]]:
        resolution = self._resolve_host_drafts_with_meta(draft_input, brief, config)
        return resolution.get("drafts") or []

    def _resolve_host_drafts_with_meta(self, draft_input: dict[str, Any], brief: dict[str, Any], config: dict[str, Any]) -> dict[str, Any]:
        """Resolve host drafts for one scheduled cycle.

        Priority:
        1. explicit config injection (`hostDraftsPerCycle` / `host_drafts_per_cycle`)
        2. callable bridge injected by host runtime (`hostDraftGenerator`)
        3. configured bridge executor command (`hostBridgeExecutor` / `host_bridge_executor`)
        4. otherwise return [] and keep waiting state
        """
        injected = config.get("hostDraftsPerCycle") or config.get("host_drafts_per_cycle")
        injected_meta = config.get("hostDraftsMetadataPerCycle") or config.get("host_drafts_metadata_per_cycle")
        if isinstance(injected, list) and injected:
            return {"drafts": injected, "metadata": injected_meta if isinstance(injected_meta, dict) else {}, "source": "config_injected_host_drafts", "status": "resolved_from_config"}

        generator = config.get("hostDraftGenerator")
        if callable(generator):
            try:
                generated = generator({
                    "draftGenerationInput": draft_input,
                    "brief": brief,
                })
            except Exception as exc:
                return {
                    "drafts": [],
                    "source": "host_runtime_callable",
                    "status": "host_draft_generator_failed",
                    "error": f"{type(exc).__name__}: {exc}",
                }
            if isinstance(generated, list) and generated:
                return {"drafts": generated, "metadata": {}, "source": "host_runtime_callable", "status": "resolved_from_callable"}

        bridge_executor = self._get_host_bridge_executor(config=config, brief=brief)
        if bridge_executor:
            request = self._build_host_draft_generation_request(
                draft_input=draft_input,
                brief=brief,
                config=config,
            )
            bridge_payload = self.build_host_model_bridge_payload(request=request)
            try:
                generated = self._run_host_bridge_executor(bridge_payload=bridge_payload, executor_spec=bridge_executor)
            except Exception as exc:
                return {
                    "drafts": [],
                    "source": "host_bridge_executor",
                    "status": "host_bridge_executor_failed",
                    "error": f"{type(exc).__name__}: {exc}",
                    "executor": self._describe_executor(bridge_executor),
                }
            if generated:
                return {
                    "drafts": generated.get("drafts") or [],
                    "metadata": generated.get("metadata") or {},
                    "source": "host_bridge_executor",
                    "status": "resolved_from_executor",
                    "executor": self._describe_executor(bridge_executor),
                }
            return {
                "drafts": [],
                "source": "host_bridge_executor",
                "status": "host_bridge_executor_returned_empty",
                "executor": self._describe_executor(bridge_executor),
            }

        return {"drafts": [], "metadata": {}, "source": None, "status": "waiting_for_external_host_drafts"}

    def _build_host_draft_generator(self, config: dict[str, Any], brief: dict[str, Any]):
        """Build a host draft generator.

        Priority:
        1. explicit host draft artifacts already injected by caller
        2. host runtime callable bridge injected by caller

        Runner only orchestrates host-provided artifacts and must not become an
        implicit model-generation layer by itself.
        """
        direct_drafts = config.get("hostDrafts") or config.get("emailModelDrafts") or config.get("host_drafts")
        normalized_pool = self._normalize_host_draft_items(direct_drafts) if isinstance(direct_drafts, list) else []
        if not normalized_pool:
            return None

        def _generator(payload: dict[str, Any]) -> list[dict[str, Any]]:
            draft_input = payload.get("draftGenerationInput") or {}
            selected = draft_input.get("selectedCreators") or []
            target_ids = {
                str(item.get("bloggerId") or item.get("besId") or item.get("bEsId") or item.get("id"))
                for item in selected
                if isinstance(item, dict) and (item.get("bloggerId") or item.get("besId") or item.get("bEsId") or item.get("id"))
            }
            if normalized_pool:
                if not target_ids:
                    return normalized_pool
                matched = [
                    item for item in normalized_pool
                    if str(item.get("bloggerId") or item.get("besId") or item.get("bEsId") or item.get("id")) in target_ids
                ]
                if matched:
                    return matched
            return []

        return _generator

    def _resolve_host_reply_analysis_with_meta(self, request: dict[str, Any], brief: dict[str, Any], config: dict[str, Any]) -> dict[str, Any]:
        injected = config.get("replyModelAnalysis") or config.get("reply_model_analysis") or config.get("conversationAnalysis")
        normalized = coerce_model_reply_analysis(injected)
        validation = validate_model_reply_analysis(normalized) if normalized else None
        if normalized and validation and validation.get("ok"):
            return {"analysis": normalized, "source": "config_injected_reply_model_analysis", "status": "resolved_from_config"}

        generator = config.get("hostReplyAnalysisGenerator")
        if callable(generator):
            try:
                generated = generator({"replyAnalysisRequest": request, "brief": brief})
            except Exception as exc:
                return {
                    "analysis": None,
                    "source": "host_runtime_callable",
                    "status": "host_reply_analysis_generator_failed",
                    "error": f"{type(exc).__name__}: {exc}",
                }
            normalized = coerce_model_reply_analysis(generated)
            validation = validate_model_reply_analysis(normalized) if normalized else None
            if normalized and validation and validation.get("ok"):
                return {"analysis": normalized, "source": "host_runtime_callable", "status": "resolved_from_callable"}

        bridge_executor = self._get_host_reply_bridge_executor(config=config, brief=brief)
        if bridge_executor:
            bridge_payload = self.build_host_reply_bridge_payload(request=request)
            try:
                generated = self._run_host_bridge_executor(bridge_payload=bridge_payload, executor_spec=bridge_executor)
            except Exception as exc:
                return {
                    "analysis": None,
                    "source": "host_reply_bridge_executor",
                    "status": "host_reply_bridge_executor_failed",
                    "error": f"{type(exc).__name__}: {exc}",
                    "executor": self._describe_executor(bridge_executor),
                }
            normalized = coerce_model_reply_analysis(generated)
            validation = validate_model_reply_analysis(normalized) if normalized else None
            if normalized and validation and validation.get("ok"):
                return {
                    "analysis": normalized,
                    "source": "host_reply_bridge_executor",
                    "status": "resolved_from_executor",
                    "executor": self._describe_executor(bridge_executor),
                }
            return {
                "analysis": None,
                "source": "host_reply_bridge_executor",
                "status": "host_reply_bridge_executor_returned_invalid",
                "executor": self._describe_executor(bridge_executor),
            }

        return {"analysis": None, "source": None, "status": "waiting_for_external_host_reply_analysis"}

    def _get_host_bridge_executor(self, *, config: dict[str, Any], brief: dict[str, Any]) -> Any:
        for key in ("hostBridgeExecutor", "host_bridge_executor"):
            if config.get(key):
                return config.get(key)
        scheduler = brief.get("scheduler") or {}
        for container in (brief, scheduler):
            if not isinstance(container, dict):
                continue
            for key in ("hostBridgeExecutor", "host_bridge_executor"):
                if container.get(key):
                    return container.get(key)
        env_default = os.environ.get("WOTOHUB_HOST_DRAFT_EXECUTOR") or os.environ.get("HOST_DRAFT_EXECUTOR")
        if env_default:
            return env_default
        return None

    def _get_host_reply_bridge_executor(self, *, config: dict[str, Any], brief: dict[str, Any]) -> Any:
        for key in ("hostReplyBridgeExecutor", "host_reply_bridge_executor"):
            if config.get(key):
                return config.get(key)
        scheduler = brief.get("scheduler") or {}
        for container in (brief, scheduler):
            if not isinstance(container, dict):
                continue
            for key in ("hostReplyBridgeExecutor", "host_reply_bridge_executor"):
                if container.get(key):
                    return container.get(key)
        env_default = os.environ.get("WOTOHUB_HOST_REPLY_ANALYSIS_EXECUTOR") or os.environ.get("HOST_REPLY_ANALYSIS_EXECUTOR")
        if env_default:
            return env_default
        return None

    def _describe_executor(self, executor_spec: Any) -> str:
        if isinstance(executor_spec, str):
            return executor_spec
        if isinstance(executor_spec, dict):
            return str(executor_spec.get("command") or executor_spec.get("args") or executor_spec.get("path") or "")
        return str(executor_spec)

    def _run_host_bridge_executor(self, *, bridge_payload: dict[str, Any], executor_spec: Any) -> Any:
        skill_root = Path(__file__).resolve().parent.parent
        with tempfile.TemporaryDirectory(prefix="wotohub-host-bridge-") as tmp:
            tmp_dir = Path(tmp)
            input_path = tmp_dir / "host-bridge-payload.json"
            output_path = tmp_dir / "host-bridge-drafts.json"
            input_path.write_text(json.dumps(bridge_payload, ensure_ascii=False, indent=2), encoding="utf-8")

            command: list[str]
            timeout_seconds = 180
            cwd = str(skill_root)
            env_overrides: dict[str, Any] = {}
            stdout_mode = "file_or_stdout"

            if isinstance(executor_spec, str):
                command = shlex.split(executor_spec.format(input=str(input_path), output=str(output_path), skill_root=str(skill_root)))
            elif isinstance(executor_spec, dict):
                timeout_seconds = int(executor_spec.get("timeoutSeconds") or executor_spec.get("timeout") or 180)
                cwd = str(executor_spec.get("cwd") or skill_root)
                env_overrides = executor_spec.get("env") or {}
                stdout_mode = str(executor_spec.get("outputMode") or "file_or_stdout")
                args = executor_spec.get("args")
                if isinstance(args, list) and args:
                    command = [
                        str(x).format(input=str(input_path), output=str(output_path), skill_root=str(skill_root))
                        for x in args
                    ]
                else:
                    raw_command = str(executor_spec.get("command") or executor_spec.get("path") or "").strip()
                    if not raw_command:
                        raise ValueError("host bridge executor requires command or args")
                    command = shlex.split(raw_command.format(input=str(input_path), output=str(output_path), skill_root=str(skill_root)))
            else:
                raise TypeError("host bridge executor must be string or dict")

            env = os.environ.copy()
            pythonpath_parts: list[str] = []
            existing_pythonpath = env.get("PYTHONPATH")
            if existing_pythonpath:
                pythonpath_parts.append(existing_pythonpath)
            pythonpath_parts.extend([
                str(skill_root),
                str(skill_root / "scripts"),
            ])
            env["PYTHONPATH"] = os.pathsep.join(part for part in pythonpath_parts if part)
            for key, value in (env_overrides or {}).items():
                env[str(key)] = str(value)

            completed = subprocess.run(
                command,
                cwd=cwd,
                env=env,
                capture_output=True,
                text=True,
                timeout=timeout_seconds,
                check=False,
            )
            if completed.returncode != 0:
                stderr = (completed.stderr or completed.stdout or "").strip()
                raise RuntimeError(f"executor exited with code {completed.returncode}: {stderr[:500]}")

            payload: Any = None
            if output_path.exists() and stdout_mode != "stdout_only":
                payload = json.loads(output_path.read_text(encoding="utf-8"))
            elif (completed.stdout or "").strip():
                payload = json.loads(completed.stdout)
            else:
                return []
            write_back_field = str(((bridge_payload.get("writeBack") or {}).get("field")) or "")
            if write_back_field == "host_analysis":
                return self._extract_host_analysis_from_payload(payload)
            if write_back_field == "reply_model_analysis":
                return self._extract_host_reply_analysis_from_payload(payload)
            return self._extract_host_drafts_from_payload(payload)

    def _extract_host_drafts_from_payload(self, payload: Any) -> dict[str, Any]:
        if isinstance(payload, list):
            return {"drafts": self._normalize_host_draft_items(payload), "metadata": {}}
        if isinstance(payload, dict):
            metadata = payload.get("writeBackMetadata") or payload.get("hostDraftsMetadataPerCycle") or payload.get("host_drafts_metadata_per_cycle") or {}
            if not isinstance(metadata, dict):
                metadata = {}
            for key in ("host_drafts_per_cycle", "hostDraftsPerCycle", "hostDrafts", "emailModelDrafts", "items"):
                items = payload.get(key)
                if isinstance(items, list):
                    return {"drafts": self._normalize_host_draft_items(items), "metadata": metadata}
        return {"drafts": [], "metadata": {}}

    def _extract_host_reply_analysis_from_payload(self, payload: Any) -> Optional[dict[str, Any]]:
        if isinstance(payload, dict):
            for key in ("reply_model_analysis", "replyModelAnalysis", "conversationAnalysis"):
                candidate = payload.get(key)
                normalized = coerce_model_reply_analysis(candidate)
                if normalized:
                    return normalized
            normalized = coerce_model_reply_analysis(payload)
            if normalized:
                return normalized
        if isinstance(payload, list):
            normalized = coerce_model_reply_analysis(payload)
            if normalized:
                return normalized
        return None

    def build_host_reply_bridge_payload(self, *, request: dict[str, Any], skill_root: Optional[Union[str, Path]]= None) -> dict[str, Any]:
        skill_root_path = Path(skill_root) if skill_root else Path(__file__).resolve().parent.parent
        request = request or {}
        prompt_path = (skill_root_path / (request.get("promptPath") or "prompts/conversation-analysis.md")).resolve()
        schema_path = (skill_root_path / (request.get("schemaPath") or "references/conversation-analysis-schema.md")).resolve()
        prompt_text = prompt_path.read_text(encoding="utf-8") if prompt_path.exists() else ""
        schema_text = schema_path.read_text(encoding="utf-8") if schema_path.exists() else ""
        return {
            "task": request.get("task") or "generate_host_reply_understanding",
            "mode": "host_reply_bridge_payload",
            "resolvedPromptPath": str(prompt_path),
            "resolvedSchemaPath": str(schema_path),
            "promptText": prompt_text,
            "schemaText": schema_text,
            "campaign": request.get("campaign") or {},
            "replyModelInput": request.get("input") or {},
            "writeBack": {
                "field": ((request.get("deliveryContract") or {}).get("field")) or "reply_model_analysis",
                "acceptedAliases": ((request.get("deliveryContract") or {}).get("acceptedAliases")) or ["reply_model_analysis"],
            },
            "runtimeHints": request.get("runtimeHints") or {},
        }

    def build_host_analysis_bridge_payload(self, *, request: dict[str, Any], skill_root: Optional[Union[str, Path]]= None) -> dict[str, Any]:
        skill_root_path = Path(skill_root) if skill_root else Path(__file__).resolve().parent.parent
        request = request or {}
        schema_path = (skill_root_path / (request.get("schemaPath") or HOST_ANALYSIS_SCHEMA_PATH)).resolve()
        schema_text = schema_path.read_text(encoding="utf-8") if schema_path.exists() else ""
        host_input = request.get("input") or {}
        return {
            "task": request.get("task") or "generate_host_analysis_for_campaign_cycle",
            "mode": "host_analysis_request",
            "resolvedSchemaPath": str(schema_path),
            "schemaText": schema_text,
            "campaign": request.get("campaign") or {},
            "rawInput": host_input.get("rawInput") or "",
            "brief": host_input.get("brief") or {},
            "writeBack": {
                "field": ((request.get("deliveryContract") or {}).get("field")) or "host_analysis",
                "acceptedAliases": ((request.get("deliveryContract") or {}).get("acceptedAliases")) or ["host_analysis"],
            },
            "runtimeHints": request.get("runtimeHints") or {},
        }

    def _normalize_host_draft_items(self, drafts: list[dict[str, Any]]) -> list[dict[str, Any]]:
        out: list[dict[str, Any]] = []
        for item in drafts or []:
            if not isinstance(item, dict):
                continue
            blogger_id = item.get("bloggerId") or item.get("besId") or item.get("bEsId") or item.get("id")
            if blogger_id in (None, ""):
                continue
            subject = str(item.get("subject") or "").strip()
            html_body = item.get("htmlBody") or ""
            plain_text = item.get("plainTextBody") or item.get("body") or item.get("content") or ""
            if html_body:
                html_body = normalize_html_body(str(html_body))
            if not plain_text and html_body:
                plain_text = html_to_plain_text(html_body)
            if not html_body and plain_text:
                html_body = normalize_html_body(f"<p>{str(plain_text).replace(chr(10), '<br/>')}</p>")
            if not subject or not (html_body or plain_text):
                continue
            out.append({
                **item,
                "bloggerId": str(blogger_id),
                "subject": subject,
                "htmlBody": html_body,
                "plainTextBody": str(plain_text or ""),
                "draftSource": item.get("draftSource") or item.get("source") or "host-model",
            })
        return out

    def _build_host_draft_generation_request(self, *, draft_input: dict[str, Any], brief: dict[str, Any], config: dict[str, Any]) -> dict[str, Any]:
        return {
            "task": "generate_host_drafts_for_selected_creators",
            "mode": "host_model_request",
            "input": draft_input,
            "promptPath": PROMPT_PATH,
            "schemaPath": SCHEMA_PATH,
            "deliveryContract": {
                "field": "host_drafts_per_cycle",
                "acceptedAliases": ["host_drafts_per_cycle", "hostDraftsPerCycle", "hostDrafts", "emailModelDrafts"],
                "canonicalField": "host_drafts_per_cycle",
                "compatibilityAliasesOnly": True,
                "requiredBatchMetadata": [
                    "selectedCreatorCount",
                    "generatedDraftCount",
                    "uniqueBloggerIdCount",
                    "missingBloggerIds",
                    "duplicateBloggerIds",
                    "unexpectedBloggerIds",
                ],
            },
            "runtimeHints": {
                "defaultLanguage": ((draft_input.get("outreachPolicy") or {}).get("emailLanguage")) or brief.get("language") or "en",
                "batchExecution": True,
                "perCreatorModelGeneration": True,
                "maxRecommendedBatchSize": 20,
                "modelGenerationRequired": True,
                "runnerAutoGenerationAllowed": False,
            },
        }

    def build_host_model_bridge_payload(self, *, request: dict[str, Any], skill_root: Optional[Union[str, Path]]= None) -> dict[str, Any]:
        """Build a ready-to-consume host-side bridge payload from hostDraftGenerationRequest.

        This does not call any model itself. It packages:
        - resolved prompt/schema absolute paths
        - canonical selected creator list
        - compact campaign / outreach context
        - explicit write-back contract for host_drafts_per_cycle

        Intended for host runtime / upper layer to consume directly.
        """
        skill_root_path = Path(skill_root) if skill_root else Path(__file__).resolve().parent.parent
        request = request or {}
        draft_input = request.get("input") or {}
        outreach_policy = draft_input.get("outreachPolicy") or {}
        product = draft_input.get("product") or {}
        creators = draft_input.get("selectedCreators") or []
        prompt_path = (skill_root_path / (request.get("promptPath") or PROMPT_PATH)).resolve()
        schema_path = (skill_root_path / (request.get("schemaPath") or SCHEMA_PATH)).resolve()
        prompt_text = prompt_path.read_text(encoding="utf-8") if prompt_path.exists() else ""
        schema_text = schema_path.read_text(encoding="utf-8") if schema_path.exists() else ""
        return {
            "task": request.get("task") or "generate_host_drafts_for_selected_creators",
            "mode": "host_model_bridge_payload",
            "resolvedPromptPath": str(prompt_path),
            "resolvedSchemaPath": str(schema_path),
            "promptText": prompt_text,
            "schemaText": schema_text,
            "campaign": {
                "campaignId": draft_input.get("campaignId"),
                "cycleNo": draft_input.get("cycleNo"),
            },
            "product": product,
            "outreachPolicy": outreach_policy,
            "selectedCreators": creators,
            "generationPlan": {
                "strategy": "per_creator_model_generation",
                "batchExecution": bool(((request.get("runtimeHints") or {}).get("batchExecution")) is not False),
                "perCreatorModelGeneration": True,
                "targetCount": len(creators),
                "defaultLanguage": outreach_policy.get("emailLanguage") or ((request.get("runtimeHints") or {}).get("defaultLanguage")) or "en",
            },
            "writeBack": {
                "field": ((request.get("deliveryContract") or {}).get("field")) or "host_drafts_per_cycle",
                "acceptedAliases": ((request.get("deliveryContract") or {}).get("acceptedAliases")) or ["host_drafts_per_cycle"],
                "requiredPerDraftFields": ((draft_input.get("outputContract") or {}).get("requiredPerDraftFields")) or ["bloggerId", "subject", "plainTextBody|htmlBody"],
                "requiredBatchMetadata": ((request.get("deliveryContract") or {}).get("requiredBatchMetadata")) or ((draft_input.get("outputContract") or {}).get("requiredBatchMetadata")) or ["selectedCreatorCount", "generatedDraftCount", "uniqueBloggerIdCount", "missingBloggerIds", "duplicateBloggerIds", "unexpectedBloggerIds"],
                "selectedCreatorIds": [str((item or {}).get("bloggerId") or (item or {}).get("besId") or (item or {}).get("bEsId") or (item or {}).get("id") or "") for item in creators if isinstance(item, dict)],
            },
        }

    def build_host_model_messages(self, *, bridge_payload: dict[str, Any], creator: dict[str, Any]) -> list[dict[str, str]]:
        prompt_text = bridge_payload.get("promptText") or ""
        schema_text = bridge_payload.get("schemaText") or ""
        product = bridge_payload.get("product") or {}
        outreach_policy = bridge_payload.get("outreachPolicy") or {}
        task = {
            "campaign": bridge_payload.get("campaign") or {},
            "product": product,
            "outreachPolicy": outreach_policy,
            "creator": creator,
            "outputRequirements": {
                "language": ((bridge_payload.get("generationPlan") or {}).get("defaultLanguage")) or "en",
                "writeBackField": ((bridge_payload.get("writeBack") or {}).get("field")) or "host_drafts_per_cycle",
                "requiredPerDraftFields": ((bridge_payload.get("writeBack") or {}).get("requiredPerDraftFields")) or [],
            },
        }
        return [
            {"role": "system", "content": prompt_text.strip()},
            {"role": "system", "content": "Output schema:\n" + schema_text.strip()},
            {"role": "user", "content": json.dumps(task, ensure_ascii=False, indent=2)},
        ]

    def build_host_drafts_writeback(
        self,
        *,
        bridge_payload: dict[str, Any],
        drafts: list[dict[str, Any]],
    ) -> dict[str, Any]:
        selected_creators = [item for item in (bridge_payload.get("selectedCreators") or []) if isinstance(item, dict)]
        selected_ids = [
            str(item.get("bloggerId") or item.get("besId") or item.get("bEsId") or item.get("id") or "").strip()
            for item in selected_creators
            if str(item.get("bloggerId") or item.get("besId") or item.get("bEsId") or item.get("id") or "").strip()
        ]
        normalized_drafts = self._normalize_host_draft_items(drafts or [])
        returned_ids = [
            str(item.get("bloggerId") or "").strip()
            for item in normalized_drafts
            if str(item.get("bloggerId") or "").strip()
        ]
        seen = set()
        duplicate_ids: list[str] = []
        for blogger_id in returned_ids:
            if blogger_id in seen and blogger_id not in duplicate_ids:
                duplicate_ids.append(blogger_id)
            seen.add(blogger_id)
        returned_id_set = set(returned_ids)
        selected_id_set = set(selected_ids)
        payload = {
            "writeBackField": ((bridge_payload.get("writeBack") or {}).get("field")) or "host_drafts_per_cycle",
            "host_drafts_per_cycle": normalized_drafts,
            "writeBackMetadata": {
                "selectedCreatorCount": len(selected_ids),
                "generatedDraftCount": len(normalized_drafts),
                "uniqueBloggerIdCount": len(returned_id_set),
                "missingBloggerIds": [blogger_id for blogger_id in selected_ids if blogger_id not in returned_id_set],
                "duplicateBloggerIds": duplicate_ids,
                "unexpectedBloggerIds": [blogger_id for blogger_id in returned_ids if blogger_id not in selected_id_set],
            },
        }
        return payload

    def build_host_model_executor_example(self, *, bridge_payload: dict[str, Any]) -> dict[str, Any]:
        creators = bridge_payload.get("selectedCreators") or []
        samples = []
        for creator in creators[: min(3, len(creators))]:
            samples.append(
                {
                    "creator": creator,
                    "messages": self.build_host_model_messages(bridge_payload=bridge_payload, creator=creator),
                }
            )
        return {
            "executor": "host_model_executor_example",
            "mode": "advisory",
            "writeBackField": ((bridge_payload.get("writeBack") or {}).get("field")) or "host_drafts_per_cycle",
            "targetCount": len(creators),
            "messageSamples": samples,
            "expectedDraftShape": {
                "bloggerId": "string",
                "nickname": "string",
                "language": ((bridge_payload.get("generationPlan") or {}).get("defaultLanguage")) or "en",
                "subject": "string",
                "htmlBody": "string",
                "plainTextBody": "string",
            },
            "expectedWriteBackMetadata": {
                "selectedCreatorCount": len(creators),
                "generatedDraftCount": len(creators),
                "uniqueBloggerIdCount": len(creators),
                "missingBloggerIds": [],
                "duplicateBloggerIds": [],
                "unexpectedBloggerIds": [],
            },
        }


    def _save_brief(self, brief: dict) -> str:
        """Save brief to temp file."""
        with NamedTemporaryFile(mode="w", suffix=".json", delete=False, dir="/tmp") as f:
            json.dump(brief, f, ensure_ascii=False, indent=2)
            return f.name

    def _extract_compact_error(self, result: dict) -> Optional[dict[str, Any]]:
        search = result.get("search") or {}
        summary_search = (result.get("cycleSummary") or {}).get("search") or {}
        top_error = result.get("error") or {}
        search_error = search.get("error") or summary_search.get("error") or {}
        runtime = result.get("runtimeOrchestration") or {}
        host_analysis_runtime = runtime.get("hostAnalysis") or {}
        host_analysis_status = host_analysis_runtime.get("status")

        if result.get("hostAnalysisRequest") or host_analysis_status in {
            "waiting_for_external_host_analysis",
            "disabled",
            "host_analysis_bridge_executor_returned_invalid",
            "host_analysis_bridge_executor_failed",
            "host_analysis_generator_failed",
        }:
            return {
                "code": "upper_layer_required",
                "message": "host_bridge_missing",
                "nextStep": "generate_host_analysis",
                "stage": "upper_layer",
            }

        source = top_error if top_error else search_error
        if not source and search.get("success") is False:
            source = {"code": "SEARCH_FAILED", "message": "Search failed before candidate selection."}
        if not source:
            return None

        return {
            "code": source.get("code") or "SEARCH_FAILED",
            "message": source.get("message") or "Search failed before candidate selection.",
            "nextStep": ((source.get("details") or {}).get("nextStep")) or source.get("nextStep") or source.get("next_step"),
            "stage": ((source.get("details") or {}).get("stage")) or ("search" if search.get("success") is False else None),
        }

    def _derive_status(self, result: dict, compact_error: Optional[dict[str, Any]]) -> str:
        draft_generation = result.get("draftGeneration") or {}
        runtime = result.get("runtimeOrchestration") or {}
        if result.get("hostAnalysisRequest"):
            return "waiting_for_host_analysis"
        if (runtime.get("hostAnalysis") or {}).get("status") in {"waiting_for_external_host_analysis", "disabled", "host_analysis_bridge_executor_returned_invalid", "host_analysis_bridge_executor_failed", "host_analysis_generator_failed"}:
            return (runtime.get("hostAnalysis") or {}).get("status") or "waiting_for_host_analysis"
        if compact_error:
            return "failed"
        if draft_generation.get("status") == "waiting_for_host_drafts":
            return "waiting_for_host_drafts"
        if runtime.get("status") == "waiting_for_external_host_drafts":
            return "waiting_for_external_host_drafts"
        if (result.get("replyStrictMode") or {}).get("status") == "waiting_for_host_reply_analysis":
            return "waiting_for_host_reply_analysis"
        if (runtime.get("replyAnalysis") or {}).get("status") == "waiting_for_external_host_reply_analysis":
            return "waiting_for_external_host_reply_analysis"
        return "success"

    def _next_action(self, result: dict) -> str:
        """Suggest next action."""
        draft_generation = result.get("draftGeneration") or {}
        runtime = result.get("runtimeOrchestration") or {}
        if (result.get("search") or {}).get("success") is False:
            return "inspect_search_payload_and_retry"
        if result.get("hostAnalysisRequest"):
            return "generate_host_analysis"
        if draft_generation.get("status") == "waiting_for_host_drafts":
            return "generate_host_drafts"
        if runtime.get("status") == "waiting_for_external_host_drafts":
            return "inject_host_drafts_and_rerun"
        if (result.get("replyStrictMode") or {}).get("status") == "waiting_for_host_reply_analysis":
            return "generate_host_reply_analysis"
        if (runtime.get("replyAnalysis") or {}).get("status") == "waiting_for_external_host_reply_analysis":
            return "inject_host_reply_analysis_and_rerun"
        if result.get("protocol", {}).get("reviewRequired"):
            return "review_required"
        if result.get("replyActions"):
            return "process_replies"
        if result.get("send", {}).get("autoSendExecuted"):
            return "wait_for_replies"
        if result.get("progress", {}).get("progressPercent", 0) < 100:
            return "continue_search"
        return "cycle_complete"
