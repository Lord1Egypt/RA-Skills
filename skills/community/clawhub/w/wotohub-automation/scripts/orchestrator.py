#!/usr/bin/env python3
"""Upper-layer orchestrator for WotoHub upper-layer architecture.

Responsibilities:
- understand raw user input
- optionally resolve product context
- map semantic context into legacy task inputs
- delegate execution to existing API task runner / legacy entrypoints

Non-goals:
- do not replace campaign engine
- do not directly call low-level WotoHub API layer
"""

from __future__ import annotations

from typing import Any, Optional

import json
import os
import shlex
import subprocess
import tempfile
from pathlib import Path

from context_schema import normalize_context
from context_to_payload import (
    get_required_fields,
    to_campaign_create_input,
    to_generate_email_input,
    to_legacy_task_input,
    to_monitor_replies_input,
    to_product_analysis_input,
    to_recommend_input,
    to_search_input,
)
from input_understanding import understand_input


class UpperLayerOrchestrator:
    HOST_ANALYSIS_TASKS = {"product_analysis", "search", "recommend", "campaign_create", "generate_email"}
    HOST_REPLY_ANALYSIS_TASKS = {"monitor_replies"}
    HOST_DRAFT_TASKS = {"generate_email"}

    def __init__(self, token: Optional[str]= None):
        self.token = token

    def run_from_user_input(
        self,
        raw_input: str,
        explicit_task: Optional[str]= None,
        config: Optional[dict[str, Any]]= None,
        host_analysis: Optional[dict[str, Any]]= None,
        host_product_summary: Optional[dict[str, Any]]= None,
        host_drafts: Optional[list[dict[str, Any]]]= None,
        host_reply_analysis: Optional[dict[str, Any]]= None,
        host_search_results: Optional[list[dict[str, Any]]]= None,
        request_passthrough: Optional[dict[str, Any]]= None,
    ) -> dict[str, Any]:
        config = config or {}
        ctx = self._build_initial_context(
            raw_input,
            explicit_task=explicit_task,
            host_analysis=host_analysis,
            host_product_summary=host_product_summary,
            host_drafts=host_drafts,
            host_reply_analysis=host_reply_analysis,
            host_search_results=host_search_results,
            request_passthrough=request_passthrough,
        )
        primary_task = ((ctx.get("intent") or {}).get("primaryTask")) or "product_analysis"
        ctx = self._ensure_host_analysis_if_needed(
            ctx,
            primary_task=primary_task,
            raw_input=raw_input,
            config=config,
        )
        ctx = self._ensure_host_reply_analysis_if_needed(
            ctx,
            primary_task=primary_task,
            raw_input=raw_input,
            config=config,
        )
        ctx = self._ensure_host_drafts_if_needed(
            ctx,
            primary_task=primary_task,
            raw_input=raw_input,
            config=config,
        )
        product_resolve_before = bool(((ctx.get("resolvedArtifacts") or {}).get("productResolve")))
        ctx = self._resolve_product_if_needed(ctx)
        ctx = normalize_context(ctx)

        primary_task = ((ctx.get("intent") or {}).get("primaryTask")) or "product_analysis"
        route = self._route_primary_task(primary_task, ctx)
        legacy_input = route["legacyInput"]
        delegated_task = route["delegatedTask"]
        observations = self._build_observations(
            ctx,
            explicit_task=explicit_task,
            delegated_task=delegated_task,
            route=route,
            product_resolve_before=product_resolve_before,
        )

        if route.get("needsUserInput"):
            return {
                "analysisPath": "upper_layer_brain",
                "semanticContext": ctx,
                "delegatedTask": delegated_task,
                "legacyInput": legacy_input,
                "observations": observations,
                "result": {
                    "status": "needs_user_input",
                    "missingFields": route.get("missingFields") or [],
                    "message": route.get("message"),
                },
                "route": route,
            }

        result = self._delegate_task(delegated_task, legacy_input, config)
        return {
            "analysisPath": "upper_layer_brain",
            "semanticContext": ctx,
            "delegatedTask": delegated_task,
            "legacyInput": legacy_input,
            "observations": observations,
            "result": result,
            "route": route,
        }

    def _build_initial_context(
        self,
        raw_input: str,
        explicit_task: Optional[str]= None,
        host_analysis: Optional[dict[str, Any]]= None,
        host_product_summary: Optional[dict[str, Any]]= None,
        host_drafts: Optional[list[dict[str, Any]]]= None,
        host_reply_analysis: Optional[dict[str, Any]]= None,
        host_search_results: Optional[list[dict[str, Any]]]= None,
        request_passthrough: Optional[dict[str, Any]]= None,
    ) -> dict[str, Any]:
        ctx = understand_input(raw_input, explicit_task=explicit_task)
        resolved = ctx.setdefault("resolvedArtifacts", {})
        meta = ctx.setdefault("meta", {})
        marketing = ctx.setdefault("marketingContext", {})
        product = ctx.setdefault("productSignals", {})
        request_passthrough = request_passthrough or {}

        campaign_id = request_passthrough.get("campaignId")
        if campaign_id not in (None, ""):
            meta["campaignId"] = campaign_id

        contacted_ids = request_passthrough.get("contactedBloggerIds")
        if isinstance(contacted_ids, list) and contacted_ids:
            meta["contactedBloggerIds"] = contacted_ids

        page_size = request_passthrough.get("pageSize")
        if page_size not in (None, ""):
            meta["pageSize"] = page_size

        has_host_analysis = isinstance(host_analysis, dict) and bool(host_analysis)
        if has_host_analysis:
            self._apply_host_analysis_to_context(
                ctx,
                host_analysis=host_analysis,
                host_product_summary=host_product_summary,
                analysis_path="host_model_injected_understanding",
                note_prefix="host model analysis injected into upper-layer context",
            )

        if isinstance(host_drafts, list) and host_drafts:
            resolved["hostDrafts"] = host_drafts
            resolved["hostEmailDrafts"] = host_drafts
            meta.setdefault("notes", [])
            meta["notes"] = [*meta.get("notes", []), "host drafts injected"]
            self._record_host_resolution(
                meta,
                "hostDrafts",
                status="provided_by_input",
                source="host_input",
                fulfilled=True,
            )

        if isinstance(host_reply_analysis, dict) and host_reply_analysis:
            resolved["replyModelAnalysis"] = host_reply_analysis
            meta.setdefault("notes", [])
            meta["notes"] = [*meta.get("notes", []), "host reply analysis injected"]
            self._record_host_resolution(
                meta,
                "replyModelAnalysis",
                status="provided_by_input",
                source="host_input",
                fulfilled=True,
            )

        if isinstance(host_search_results, list) and host_search_results:
            resolved["searchResults"] = [item for item in host_search_results if isinstance(item, dict)]
            meta.setdefault("notes", [])
            meta["notes"] = [*meta.get("notes", []), "search results injected for recommendation/rerank stage"]

        if isinstance(host_product_summary, dict) and host_product_summary and not resolved.get("productSummary"):
            resolved["productSummary"] = host_product_summary

        if has_host_analysis:
            self._record_host_resolution(
                meta,
                "hostAnalysis",
                status="provided_by_input",
                source="host_input",
                fulfilled=True,
            )

        return normalize_context(ctx)

    def _record_host_resolution(
        self,
        meta: dict[str, Any],
        field: str,
        *,
        status: str,
        source: Optional[str]= None,
        executor: Optional[str]= None,
        fulfilled: Optional[bool]= None,
        error: Optional[str]= None,
    ) -> None:
        resolution = meta.setdefault("hostResolution", {})
        entry = dict(resolution.get(field) or {})
        entry["status"] = status
        if source is not None:
            entry["source"] = source
        if executor is not None:
            entry["executor"] = executor
        if fulfilled is not None:
            entry["fulfilled"] = fulfilled
        if error is not None:
            entry["error"] = error
        elif "error" in entry and not error:
            entry.pop("error", None)
        resolution[field] = entry

    def _task_requires_host_analysis(self, primary_task: str) -> bool:
        return primary_task in self.HOST_ANALYSIS_TASKS

    def _ensure_host_analysis_if_needed(
        self,
        ctx: dict[str, Any],
        *,
        primary_task: str,
        raw_input: str,
        config: Optional[dict[str, Any]]= None,
    ) -> dict[str, Any]:
        config = config or {}
        resolved = ctx.setdefault("resolvedArtifacts", {})
        meta = ctx.setdefault("meta", {})

        if not self._task_requires_host_analysis(primary_task):
            return ctx
        if isinstance(resolved.get("modelAnalysis"), dict) and resolved.get("modelAnalysis"):
            meta["needsHostAnalysis"] = False
            if not ((meta.get("hostResolution") or {}).get("hostAnalysis")):
                self._record_host_resolution(
                    meta,
                    "hostAnalysis",
                    status="already_available",
                    source="semantic_context",
                    fulfilled=True,
                )
            return ctx

        resolution = self._resolve_host_analysis(raw_input=raw_input, primary_task=primary_task, ctx=ctx, config=config)
        status = resolution.get("status") or "unknown"
        meta.setdefault("notes", [])
        meta["notes"] = [*meta.get("notes", []), f"host analysis orchestration status: {status}"]
        self._record_host_resolution(
            meta,
            "hostAnalysis",
            status=status,
            source=resolution.get("source"),
            executor=resolution.get("executor"),
            fulfilled=bool(resolution.get("analysis")),
            error=resolution.get("error"),
        )

        model_analysis = resolution.get("analysis")
        if isinstance(model_analysis, dict) and model_analysis:
            self._apply_host_analysis_to_context(
                ctx,
                host_analysis=model_analysis,
                host_product_summary=resolution.get("productSummary"),
                analysis_path=f"{resolution.get('source') or 'host_model'}_requested_understanding",
                note_prefix="host analysis requested by upper-layer orchestrator",
            )
            return normalize_context(ctx)

        if resolution.get("error"):
            meta["hostAnalysisError"] = resolution.get("error")
        if resolution.get("executor"):
            meta["hostAnalysisExecutor"] = resolution.get("executor")
        return ctx

    def _task_requires_host_reply_analysis(self, primary_task: str) -> bool:
        return primary_task in self.HOST_REPLY_ANALYSIS_TASKS

    def _ensure_host_reply_analysis_if_needed(
        self,
        ctx: dict[str, Any],
        *,
        primary_task: str,
        raw_input: str,
        config: Optional[dict[str, Any]]= None,
    ) -> dict[str, Any]:
        config = config or {}
        resolved = ctx.setdefault("resolvedArtifacts", {})
        meta = ctx.setdefault("meta", {})

        if not self._task_requires_host_reply_analysis(primary_task):
            return ctx
        if isinstance(resolved.get("replyModelAnalysis"), dict) and resolved.get("replyModelAnalysis"):
            if not ((meta.get("hostResolution") or {}).get("replyModelAnalysis")):
                self._record_host_resolution(
                    meta,
                    "replyModelAnalysis",
                    status="already_available",
                    source="semantic_context",
                    fulfilled=True,
                )
            return ctx

        resolution = self._resolve_host_reply_analysis(raw_input=raw_input, primary_task=primary_task, ctx=ctx, config=config)
        status = resolution.get("status") or "unknown"
        meta.setdefault("notes", [])
        meta["notes"] = [*meta.get("notes", []), f"host reply analysis orchestration status: {status}"]
        self._record_host_resolution(
            meta,
            "replyModelAnalysis",
            status=status,
            source=resolution.get("source"),
            executor=resolution.get("executor"),
            fulfilled=bool(resolution.get("analysis")),
            error=resolution.get("error"),
        )

        reply_analysis = resolution.get("analysis")
        if isinstance(reply_analysis, dict) and reply_analysis:
            resolved["replyModelAnalysis"] = reply_analysis
            meta["usedHostModel"] = True
            meta["usedFallback"] = False
            return normalize_context(ctx)

        if resolution.get("error"):
            meta["hostReplyAnalysisError"] = resolution.get("error")
        if resolution.get("executor"):
            meta["hostReplyAnalysisExecutor"] = resolution.get("executor")
        return ctx

    def _task_requires_host_drafts(self, primary_task: str) -> bool:
        return primary_task in self.HOST_DRAFT_TASKS

    def _ensure_host_drafts_if_needed(
        self,
        ctx: dict[str, Any],
        *,
        primary_task: str,
        raw_input: str,
        config: Optional[dict[str, Any]]= None,
    ) -> dict[str, Any]:
        config = config or {}
        resolved = ctx.setdefault("resolvedArtifacts", {})
        meta = ctx.setdefault("meta", {})

        if not self._task_requires_host_drafts(primary_task):
            return ctx
        existing = resolved.get("hostDrafts") or resolved.get("hostEmailDrafts")
        if isinstance(existing, list) and existing:
            if not ((meta.get("hostResolution") or {}).get("hostDrafts")):
                self._record_host_resolution(
                    meta,
                    "hostDrafts",
                    status="already_available",
                    source="semantic_context",
                    fulfilled=True,
                )
            return ctx
        if not (isinstance(resolved.get("modelAnalysis"), dict) and resolved.get("modelAnalysis")):
            self._record_host_resolution(
                meta,
                "hostDrafts",
                status="blocked_missing_host_analysis",
                source="semantic_context",
                fulfilled=False,
            )
            return ctx

        resolution = self._resolve_host_drafts(raw_input=raw_input, primary_task=primary_task, ctx=ctx, config=config)
        status = resolution.get("status") or "unknown"
        meta.setdefault("notes", [])
        meta["notes"] = [*meta.get("notes", []), f"host draft orchestration status: {status}"]
        self._record_host_resolution(
            meta,
            "hostDrafts",
            status=status,
            source=resolution.get("source"),
            executor=resolution.get("executor"),
            fulfilled=bool(resolution.get("drafts")),
            error=resolution.get("error"),
        )

        drafts = resolution.get("drafts") or []
        if isinstance(drafts, list) and drafts:
            resolved["hostDrafts"] = drafts
            resolved["hostEmailDrafts"] = drafts
            meta["usedHostModel"] = True
            meta["usedFallback"] = False
            return normalize_context(ctx)

        if resolution.get("error"):
            meta["hostDraftsError"] = resolution.get("error")
        if resolution.get("executor"):
            meta["hostDraftsExecutor"] = resolution.get("executor")
        return ctx

    def _resolve_host_analysis(
        self,
        *,
        raw_input: str,
        primary_task: str,
        ctx: dict[str, Any],
        config: dict[str, Any],
    ) -> dict[str, Any]:
        generator = config.get("hostAnalysisGenerator") or config.get("host_analysis_generator")
        if callable(generator):
            try:
                generated = generator({
                    "kind": self._host_analysis_kind(primary_task),
                    "rawInput": raw_input,
                    "semanticContext": ctx,
                    "taskType": primary_task,
                })
            except Exception as exc:
                return {
                    "analysis": None,
                    "productSummary": None,
                    "source": "host_runtime_callable",
                    "status": "host_analysis_generator_failed",
                    "error": f"{type(exc).__name__}: {exc}",
                }
            extracted = self._extract_host_analysis_payload(generated)
            if extracted.get("analysis"):
                return {**extracted, "source": "host_runtime_callable", "status": "resolved_from_callable"}

        bridge_executor = self._get_host_analysis_executor(config=config)
        if bridge_executor:
            request = self._build_host_analysis_request(raw_input=raw_input, primary_task=primary_task, ctx=ctx)
            try:
                payload = self._run_host_analysis_executor(request=request, executor_spec=bridge_executor)
            except Exception as exc:
                return {
                    "analysis": None,
                    "productSummary": None,
                    "source": "host_bridge_executor",
                    "status": "host_analysis_executor_failed",
                    "error": f"{type(exc).__name__}: {exc}",
                    "executor": self._describe_executor(bridge_executor),
                }
            extracted = self._extract_host_analysis_payload(payload)
            if extracted.get("analysis"):
                return {
                    **extracted,
                    "source": "host_bridge_executor",
                    "status": "resolved_from_executor",
                    "executor": self._describe_executor(bridge_executor),
                }
            return {
                "analysis": None,
                "productSummary": None,
                "source": "host_bridge_executor",
                "status": "host_analysis_executor_returned_empty",
                "executor": self._describe_executor(bridge_executor),
            }

        return {
            "analysis": None,
            "productSummary": None,
            "source": None,
            "status": "no_host_analysis_bridge_configured",
        }

    def _host_analysis_kind(self, primary_task: str) -> str:
        if primary_task in {"search", "recommend", "campaign_create"}:
            return "search_understanding"
        if primary_task == "generate_email":
            return "email_understanding"
        return "product_analysis"

    def _build_host_analysis_request(self, *, raw_input: str, primary_task: str, ctx: dict[str, Any]) -> dict[str, Any]:
        return {
            "mode": "host_analysis_request",
            "kind": self._host_analysis_kind(primary_task),
            "taskType": primary_task,
            "rawInput": raw_input,
            "semanticContext": ctx,
            "writeBack": {
                "analysisField": "hostAnalysis",
                "productSummaryField": "productSummary",
            },
        }

    def _get_host_analysis_executor(self, *, config: dict[str, Any]) -> Any:
        for key in ("hostAnalysisExecutor", "host_analysis_executor", "hostSemanticExecutor", "host_semantic_executor"):
            if config.get(key):
                return config.get(key)
        env_default = os.environ.get("WOTOHUB_HOST_ANALYSIS_EXECUTOR") or os.environ.get("HOST_ANALYSIS_EXECUTOR")
        if env_default:
            return env_default
        return None

    def _describe_executor(self, executor_spec: Any) -> str:
        if isinstance(executor_spec, str):
            return executor_spec
        if isinstance(executor_spec, dict):
            return str(executor_spec.get("command") or executor_spec.get("args") or executor_spec.get("path") or "")
        return str(executor_spec)

    def _run_host_analysis_executor(self, *, request: dict[str, Any], executor_spec: Any) -> Any:
        skill_root = Path(__file__).resolve().parent.parent
        with tempfile.TemporaryDirectory(prefix="wotohub-host-analysis-") as tmp:
            tmp_dir = Path(tmp)
            input_path = tmp_dir / "host-analysis-request.json"
            output_path = tmp_dir / "host-analysis-output.json"
            input_path.write_text(json.dumps(request, ensure_ascii=False, indent=2), encoding="utf-8")

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
                        raise ValueError("host analysis executor requires command or args")
                    command = shlex.split(raw_command.format(input=str(input_path), output=str(output_path), skill_root=str(skill_root)))
            else:
                raise TypeError("host analysis executor must be string or dict")

            env = os.environ.copy()
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

            if output_path.exists() and stdout_mode != "stdout_only":
                return json.loads(output_path.read_text(encoding="utf-8"))
            if (completed.stdout or "").strip():
                return json.loads(completed.stdout)
            return None

    def _extract_host_analysis_payload(self, payload: Any) -> dict[str, Any]:
        if isinstance(payload, dict):
            analysis = payload.get("hostAnalysis") or payload.get("modelAnalysis") or payload.get("understanding") or payload.get("analysis")
            product_summary = payload.get("productSummary") or payload.get("hostProductSummary")
            if not analysis and payload.get("product") and payload.get("marketing"):
                analysis = payload
            return {
                "analysis": analysis if isinstance(analysis, dict) and analysis else None,
                "productSummary": product_summary if isinstance(product_summary, dict) and product_summary else None,
            }
        return {"analysis": None, "productSummary": None}

    def _apply_host_analysis_to_context(
        self,
        ctx: dict[str, Any],
        *,
        host_analysis: dict[str, Any],
        host_product_summary: Optional[dict[str, Any]]= None,
        analysis_path: str,
        note_prefix: str,
    ) -> None:
        resolved = ctx.setdefault("resolvedArtifacts", {})
        meta = ctx.setdefault("meta", {})
        marketing = ctx.setdefault("marketingContext", {})
        product = ctx.setdefault("productSignals", {})

        sanitized_host_analysis = dict(host_analysis)
        sanitized_host_analysis.pop("searchPayloadHints", None)
        resolved["modelAnalysis"] = sanitized_host_analysis
        if isinstance(host_product_summary, dict) and host_product_summary:
            resolved["productSummary"] = host_product_summary

        host_product = sanitized_host_analysis.get("product") or {}
        host_marketing = sanitized_host_analysis.get("marketing") or {}
        host_constraints = sanitized_host_analysis.get("constraints") or {}

        product["productName"] = host_product.get("productName") or product.get("productName")
        product["brand"] = host_product.get("brand") or product.get("brand")
        product["category"] = host_product.get("productSubtype") or host_product.get("productType") or product.get("category")
        product["priceHint"] = host_product.get("price") or product.get("priceHint")
        product["features"] = product.get("features") or host_product.get("features") or host_product.get("coreBenefits") or []
        product["useCases"] = product.get("useCases") or host_product.get("functions") or []

        marketing["platforms"] = marketing.get("platforms") or host_marketing.get("platformPreference") or []
        marketing["creatorTypes"] = marketing.get("creatorTypes") or host_marketing.get("creatorTypes") or []
        marketing["targetMarkets"] = marketing.get("targetMarkets") or host_constraints.get("regions") or []
        marketing["languages"] = marketing.get("languages") or host_constraints.get("languages") or []
        if host_constraints.get("minFansNum") is not None:
            marketing.setdefault("followerRange", {})["min"] = host_constraints.get("minFansNum")
        if host_constraints.get("maxFansNum") is not None:
            marketing.setdefault("followerRange", {})["max"] = host_constraints.get("maxFansNum")

        meta["usedHostModel"] = True
        meta["usedFallback"] = False
        meta["needsHostAnalysis"] = False
        meta["analysisPath"] = analysis_path
        meta.setdefault("notes", [])
        semantic = resolved.setdefault("semantic", {"semanticBrief": {}, "strategies": []})
        semantic_brief = semantic.setdefault("semanticBrief", {})
        semantic_brief["product"] = {
            "category_forms": {"value": [str(x).strip() for x in (host_product.get("categoryForms") or [host_product.get("productSubtype"), host_product.get("productType")]) if str(x).strip()]},
            "functions": {"value": [str(x).strip() for x in ((host_product.get("functions") or []) + (host_product.get("coreBenefits") or []) + (host_product.get("features") or [])) if str(x).strip()]},
        }
        semantic_brief["keyword_clusters"] = {
            "core": {"value": [str(x).strip() for x in [host_product.get("productName"), host_product.get("productSubtype"), host_product.get("productType"), *(host_product.get("categoryForms") or [])] if str(x).strip()]},
            "benefit": {"value": [str(x).strip() for x in ((host_product.get("coreBenefits") or []) + (host_product.get("features") or [])) if str(x).strip()]},
            "creator": {"value": [str(x).strip() for x in ((host_marketing.get("creatorTypes") or []) + (host_marketing.get("contentAngles") or [])) if str(x).strip()]},
        }
        semantic_brief["marketing"] = {
            "creator_types": {"value": [str(x).strip() for x in (host_marketing.get("creatorTypes") or []) if str(x).strip()]},
        }
        meta["notes"] = [
            *meta.get("notes", []),
            note_prefix,
            "searchPayloadHints stripped; search payload must be compiled through standard mapping chain",
            "semantic category forms/functions preserved so standard compiler can produce blogCateIds before keyword refinement",
        ]

    def _resolve_host_reply_analysis(
        self,
        *,
        raw_input: str,
        primary_task: str,
        ctx: dict[str, Any],
        config: dict[str, Any],
    ) -> dict[str, Any]:
        generator = config.get("hostReplyAnalysisGenerator") or config.get("host_reply_analysis_generator")
        if callable(generator):
            try:
                generated = generator({
                    "kind": "reply_analysis",
                    "rawInput": raw_input,
                    "semanticContext": ctx,
                    "taskType": primary_task,
                })
            except Exception as exc:
                return {
                    "analysis": None,
                    "source": "host_runtime_callable",
                    "status": "host_reply_analysis_generator_failed",
                    "error": f"{type(exc).__name__}: {exc}",
                }
            extracted = self._extract_host_reply_analysis_payload(generated)
            if extracted.get("analysis"):
                return {**extracted, "source": "host_runtime_callable", "status": "resolved_from_callable"}

        bridge_executor = self._get_host_reply_analysis_executor(config=config)
        if bridge_executor:
            request = self._build_host_reply_analysis_request(raw_input=raw_input, primary_task=primary_task, ctx=ctx)
            try:
                payload = self._run_host_analysis_executor(request=request, executor_spec=bridge_executor)
            except Exception as exc:
                return {
                    "analysis": None,
                    "source": "host_reply_bridge_executor",
                    "status": "host_reply_analysis_executor_failed",
                    "error": f"{type(exc).__name__}: {exc}",
                    "executor": self._describe_executor(bridge_executor),
                }
            extracted = self._extract_host_reply_analysis_payload(payload)
            if extracted.get("analysis"):
                return {
                    **extracted,
                    "source": "host_reply_bridge_executor",
                    "status": "resolved_from_executor",
                    "executor": self._describe_executor(bridge_executor),
                }
            return {
                "analysis": None,
                "source": "host_reply_bridge_executor",
                "status": "host_reply_analysis_executor_returned_empty",
                "executor": self._describe_executor(bridge_executor),
            }

        return {
            "analysis": None,
            "source": None,
            "status": "no_host_reply_analysis_bridge_configured",
        }

    def _build_host_reply_analysis_request(self, *, raw_input: str, primary_task: str, ctx: dict[str, Any]) -> dict[str, Any]:
        meta = ctx.get("meta") or {}
        return {
            "mode": "host_reply_analysis_request",
            "kind": "reply_analysis",
            "taskType": primary_task,
            "rawInput": raw_input,
            "semanticContext": ctx,
            "campaignId": meta.get("campaignId"),
            "contactedBloggerIds": meta.get("contactedBloggerIds"),
            "pageSize": meta.get("pageSize"),
            "writeBack": {
                "analysisField": "replyModelAnalysis",
            },
        }

    def _get_host_reply_analysis_executor(self, *, config: dict[str, Any]) -> Any:
        for key in ("hostReplyAnalysisExecutor", "host_reply_analysis_executor", "hostReplyBridgeExecutor", "host_reply_bridge_executor"):
            if config.get(key):
                return config.get(key)
        env_default = os.environ.get("WOTOHUB_HOST_REPLY_ANALYSIS_EXECUTOR") or os.environ.get("HOST_REPLY_ANALYSIS_EXECUTOR")
        if env_default:
            return env_default
        return None

    def _extract_host_reply_analysis_payload(self, payload: Any) -> dict[str, Any]:
        if isinstance(payload, dict):
            analysis = payload.get("replyModelAnalysis") or payload.get("conversationAnalysis") or payload.get("analysis")
            if not analysis and payload.get("items"):
                analysis = payload
            return {
                "analysis": analysis if isinstance(analysis, dict) and analysis else None,
            }
        return {"analysis": None}

    def _resolve_host_drafts(
        self,
        *,
        raw_input: str,
        primary_task: str,
        ctx: dict[str, Any],
        config: dict[str, Any],
    ) -> dict[str, Any]:
        generator = config.get("hostDraftGenerator") or config.get("host_draft_generator")
        request = self._build_host_draft_request(raw_input=raw_input, primary_task=primary_task, ctx=ctx)
        if callable(generator):
            try:
                generated = generator(request)
            except Exception as exc:
                return {
                    "drafts": [],
                    "source": "host_runtime_callable",
                    "status": "host_draft_generator_failed",
                    "error": f"{type(exc).__name__}: {exc}",
                }
            extracted = self._extract_host_drafts_payload(generated)
            if extracted.get("drafts"):
                return {**extracted, "source": "host_runtime_callable", "status": "resolved_from_callable"}

        bridge_executor = self._get_host_draft_executor(config=config)
        if bridge_executor:
            try:
                payload = self._run_host_analysis_executor(request=request, executor_spec=bridge_executor)
            except Exception as exc:
                return {
                    "drafts": [],
                    "source": "host_draft_bridge_executor",
                    "status": "host_draft_executor_failed",
                    "error": f"{type(exc).__name__}: {exc}",
                    "executor": self._describe_executor(bridge_executor),
                }
            extracted = self._extract_host_drafts_payload(payload)
            if extracted.get("drafts"):
                return {
                    **extracted,
                    "source": "host_draft_bridge_executor",
                    "status": "resolved_from_executor",
                    "executor": self._describe_executor(bridge_executor),
                }
            return {
                "drafts": [],
                "source": "host_draft_bridge_executor",
                "status": "host_draft_executor_returned_empty",
                "executor": self._describe_executor(bridge_executor),
            }

        return {
            "drafts": [],
            "source": None,
            "status": "no_host_draft_bridge_configured",
        }

    def _build_host_draft_request(self, *, raw_input: str, primary_task: str, ctx: dict[str, Any]) -> dict[str, Any]:
        resolved = ctx.get("resolvedArtifacts") or {}
        marketing = ctx.get("marketingContext") or {}
        product = ctx.get("productSignals") or {}
        selected_creators = resolved.get("selectedCreators") or []
        if not selected_creators and resolved.get("allSearchResultsSelected"):
            selected_creators = resolved.get("searchResults") or []
        brief = {
            "productName": product.get("productName") or ((resolved.get("productSummary") or {}).get("productName")),
            "brand": product.get("brand") or ((resolved.get("productSummary") or {}).get("brand")),
            "offerType": marketing.get("offerType"),
            "goal": marketing.get("goal"),
            "targetMarkets": marketing.get("targetMarkets") or None,
            "platforms": marketing.get("platforms") or None,
            "creatorTypes": marketing.get("creatorTypes") or None,
            "languages": marketing.get("languages") or None,
        }
        return {
            "mode": "host_draft_request",
            "kind": "draft_generation",
            "taskType": primary_task,
            "rawInput": raw_input,
            "semanticContext": ctx,
            "brief": {k: v for k, v in brief.items() if v not in (None, "", [], {})},
            "productSummary": resolved.get("productSummary"),
            "modelAnalysis": resolved.get("modelAnalysis"),
            "selectedCreators": selected_creators,
            "emailLanguage": (marketing.get("languages") or [None])[0],
            "writeBack": {
                "draftsField": "hostDrafts",
            },
        }

    def _get_host_draft_executor(self, *, config: dict[str, Any]) -> Any:
        for key in ("hostDraftExecutor", "host_draft_executor", "hostBridgeExecutor", "host_bridge_executor"):
            if config.get(key):
                return config.get(key)
        env_default = os.environ.get("WOTOHUB_HOST_DRAFT_EXECUTOR") or os.environ.get("HOST_DRAFT_EXECUTOR")
        if env_default:
            return env_default
        return None

    def _extract_host_drafts_payload(self, payload: Any) -> dict[str, Any]:
        if isinstance(payload, list):
            return {"drafts": payload}
        if isinstance(payload, dict):
            for key in ("hostDrafts", "emailModelDrafts", "host_drafts_per_cycle", "hostDraftsPerCycle", "drafts", "items"):
                candidate = payload.get(key)
                if isinstance(candidate, list) and candidate:
                    return {"drafts": candidate}
        return {"drafts": []}

    def _resolve_product_if_needed(self, ctx: dict[str, Any]) -> dict[str, Any]:
        hints = ctx.get("operationalHints") or {}
        if not hints.get("needsProductResolve"):
            return ctx

        from product_resolve import resolve_product

        product = ctx.get("productSignals") or {}
        urls = product.get("urls") or []
        raw_input = urls[0] if urls else product.get("rawInput")
        if not raw_input:
            return ctx

        meta = ctx.setdefault("meta", {})
        artifacts = ctx.setdefault("resolvedArtifacts", {})
        host_analysis_present = bool(artifacts.get("modelAnalysis")) and meta.get("usedHostModel")

        resolved = resolve_product(raw_input, mode="url" if urls else "text")
        artifacts["productResolve"] = resolved
        if not host_analysis_present:
            artifacts["modelAnalysis"] = resolved.get("analysis")
            artifacts["productSummary"] = resolved.get("productSummary")
            if artifacts.get("modelAnalysis"):
                meta["needsHostAnalysis"] = False
                meta["analysisPath"] = "product_resolve_understanding"
                meta.setdefault("notes", [])
                meta["notes"] = [*meta.get("notes", []), "product_resolve produced structured understanding before delegate"]

        summary = resolved.get("productSummary") or {}
        product["productName"] = product.get("productName") or summary.get("productName")
        product["brand"] = product.get("brand") or summary.get("brand")
        product["sourcePlatform"] = product.get("sourcePlatform") or summary.get("sourcePlatform") or ((resolved.get("resolvedProduct") or {}).get("sourcePlatform"))
        product["sourceHost"] = product.get("sourceHost") or summary.get("sourceHost") or ((resolved.get("resolvedProduct") or {}).get("sourceHost"))
        product["features"] = product.get("features") or summary.get("features") or []

        fallback = resolved.get("fallback") or {}
        meta["usedFallback"] = bool(fallback.get("active"))
        if fallback.get("needsUserInput"):
            if host_analysis_present:
                meta.setdefault("notes", [])
                if fallback.get("reason"):
                    meta["notes"].append(f"product_resolve_blocked_but_host_analysis_preserved:{fallback.get('reason')}")
            else:
                existing_missing = ctx.get("missingFields") or []
                requested_fields = fallback.get("requestedFields") or []
                ctx["missingFields"] = list(dict.fromkeys([*existing_missing, *requested_fields]))
                meta["missingFieldPrompt"] = fallback.get("userPrompt")
                meta.setdefault("notes", [])
                if fallback.get("reason"):
                    meta["notes"].append(f"product_resolve_blocked:{fallback.get('reason')}")
        return ctx

    def _route_primary_task(self, primary_task: str, ctx: dict[str, Any]) -> dict[str, Any]:
        existing_missing = ctx.get("missingFields") or []
        required_missing = get_required_fields(primary_task, ctx)
        missing_fields = list(dict.fromkeys([*existing_missing, *required_missing]))

        if primary_task == "product_analysis":
            legacy_input = to_product_analysis_input(ctx)
            delegated_task = "product_analysis"
        elif primary_task == "search":
            legacy_input = to_search_input(ctx)
            delegated_task = "search"
        elif primary_task == "recommend":
            has_search_results = bool((ctx.get("resolvedArtifacts") or {}).get("searchResults"))
            if has_search_results:
                legacy_input = to_recommend_input(ctx)
                delegated_task = "recommend"
            else:
                legacy_input = to_search_input(ctx)
                delegated_task = "search"
        elif primary_task == "campaign_create":
            legacy_input = to_campaign_create_input(ctx)
            delegated_task = "campaign_create"
        elif primary_task == "generate_email":
            legacy_input = to_generate_email_input(ctx)
            delegated_task = "generate_email"
        elif primary_task == "monitor_replies":
            legacy_input = to_monitor_replies_input(ctx)
            delegated_task = "monitor_replies"
        else:
            legacy_input = to_legacy_task_input(primary_task, ctx)
            delegated_task = primary_task

        message = self._build_missing_fields_message(primary_task, missing_fields)
        return {
            "delegatedTask": delegated_task,
            "legacyInput": legacy_input,
            "missingFields": missing_fields,
            "needsUserInput": bool(missing_fields),
            "message": message,
            "whyRoutedThisWay": self._build_route_reason(primary_task, delegated_task, missing_fields, legacy_input),
        }

    def _build_missing_fields_message(self, primary_task: str, missing_fields: list[str]) -> Optional[str]:
        task_label_map = {
            "product_analysis": "产品分析",
            "search": "达人搜索",
            "recommend": "达人推荐",
            "campaign_create": "campaign 创建",
            "generate_email": "邀约邮件生成",
            "monitor_replies": "回复辅助",
        }
        field_label_map = {
            "product_anchor": "产品链接或产品名",
            "offerType": "合作方式",
            "input": "输入内容",
            "platforms": "投放平台",
            "hostAnalysis": "结构化理解结果",
            "hostDrafts": "宿主邮件草稿",
            "productName": "产品名称",
            "replyModelAnalysis": "对话理解结果",
            "selectedCreators": "已选达人",
            "campaignId_or_input": "campaignId 或回复上下文",
        }
        if not missing_fields:
            return None
        labels = [field_label_map.get(field, field) for field in missing_fields]
        task_label = task_label_map.get(primary_task, primary_task)
        return f"当前无法继续执行{task_label}，还缺少：{'、'.join(labels)}"

    def _build_route_reason(self, primary_task: str, delegated_task: str, missing_fields: list[str], legacy_input: dict[str, Any]) -> str:
        if missing_fields:
            return f"understood {primary_task}, but blocked before delegate because required fields are missing or product evidence is not reliable enough"
        if primary_task != delegated_task:
            return f"understood {primary_task}, then mapped into legacy task {delegated_task} for compatibility"
        if legacy_input.get("searchPayload"):
            return f"understood {primary_task}, compiled context into searchPayload, then delegated"
        return f"understood {primary_task}, mapped to legacy input, then delegated"

    def _build_observations(
        self,
        ctx: dict[str, Any],
        explicit_task: Optional[str],
        delegated_task: str,
        route: dict[str, Any],
        product_resolve_before: bool,
    ) -> dict[str, Any]:
        intent = ctx.get("intent") or {}
        hints = ctx.get("operationalHints") or {}
        resolved = ctx.get("resolvedArtifacts") or {}
        meta = ctx.get("meta") or {}
        legacy_input = route.get("legacyInput") or {}
        product = ctx.get("productSignals") or {}
        marketing = ctx.get("marketingContext") or {}
        summary = (resolved.get("productSummary") or {})
        used_product_resolve = bool(resolved.get("productResolve")) and not product_resolve_before

        resolved_product_name = (
            product.get("productName")
            or summary.get("productName")
            or legacy_input.get("productName")
        )
        search_payload = legacy_input.get("searchPayload") or {}
        category_resolution = (ctx.get("resolvedArtifacts") or {}).get("categoryResolution") or {}
        resolved_platforms = (
            marketing.get("platforms")
            or legacy_input.get("platforms")
            or summary.get("platforms")
            or ([] if not product.get("sourcePlatform") else [product.get("sourcePlatform")])
        )
        resolved_target_markets = marketing.get("targetMarkets") or legacy_input.get("targetMarkets") or []
        resolved_offer_type = marketing.get("offerType") or legacy_input.get("offerType")
        resolved_goal = marketing.get("goal") or legacy_input.get("goal")
        resolved_creator_types = marketing.get("creatorTypes") or legacy_input.get("creatorTypes") or []
        resolved_languages = marketing.get("languages") or legacy_input.get("blogLangs") or []
        resolved_brand = product.get("brand") or summary.get("brand")
        resolved_source_platform = product.get("sourcePlatform") or summary.get("sourcePlatform")
        resolved_source_host = product.get("sourceHost") or summary.get("sourceHost")

        return {
            "explicitTask": explicit_task,
            "understoodPrimaryTask": intent.get("primaryTask"),
            "delegatedTask": delegated_task,
            "whyRoutedThisWay": route.get("whyRoutedThisWay"),
            "usedProductResolve": used_product_resolve,
            "usedSearchPayloadFromContext": bool(legacy_input.get("searchPayload")),
            "searchPayloadDecision": {
                "hasBlogCateIds": bool(search_payload.get("blogCateIds")),
                "hasAdvancedKeywordList": bool(search_payload.get("advancedKeywordList")),
                "blogCateIds": search_payload.get("blogCateIds") or [],
                "advancedKeywordList": search_payload.get("advancedKeywordList") or [],
                "categoryResolutionStrategy": category_resolution.get("strategy"),
                "categoryReasonSummary": category_resolution.get("reasonSummary"),
            },
            "needsUserInput": bool(route.get("needsUserInput")),
            "missingFields": route.get("missingFields") or [],
            "missingFieldPrompt": meta.get("missingFieldPrompt"),
            "usedHostModel": meta.get("usedHostModel"),
            "usedFallback": meta.get("usedFallback"),
            "needsHostAnalysis": meta.get("needsHostAnalysis"),
            "analysisPath": meta.get("analysisPath"),
            "hostResolution": meta.get("hostResolution") or {},
            "resolvedProductName": resolved_product_name,
            "resolvedBrand": resolved_brand,
            "resolvedPlatforms": resolved_platforms,
            "resolvedSourcePlatform": resolved_source_platform,
            "resolvedSourceHost": resolved_source_host,
            "resolvedTargetMarkets": resolved_target_markets,
            "resolvedOfferType": resolved_offer_type,
            "resolvedGoal": resolved_goal,
            "resolvedCreatorTypes": resolved_creator_types,
            "resolvedLanguages": resolved_languages,
            "operationalHints": {
                "needsProductResolve": hints.get("needsProductResolve"),
                "needsSearch": hints.get("needsSearch"),
                "needsCampaignBuild": hints.get("needsCampaignBuild"),
                "needsOutreachDraft": hints.get("needsOutreachDraft"),
                "needsInboxAssist": hints.get("needsInboxAssist"),
            },
        }

    def _delegate_task(self, task_type: str, input_data: dict[str, Any], config: dict[str, Any]) -> dict[str, Any]:
        from api_task_runner import TaskRunner

        return TaskRunner(self.token).run(task_type, input_data, config or {})
