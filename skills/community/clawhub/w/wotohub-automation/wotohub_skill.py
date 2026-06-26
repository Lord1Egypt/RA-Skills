#!/usr/bin/env python3
"""WotoHub Skill Entry Point for OpenClaw.

Release refactor rule:
- upper-layer brain can be upgraded here
- lower execution layer stays delegated to existing api/task runners
"""

from __future__ import annotations

from typing import Optional

import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

ENABLE_UPPER_LAYER_BRAIN = True
UPPER_LAYER_TASK_TYPES = {
    "product_analysis",
    "search",
    "recommend",
    "campaign_create",
    "generate_email",
    "monitor_replies",
}


def _should_use_upper_layer(req: dict) -> bool:
    if not ENABLE_UPPER_LAYER_BRAIN:
        return False
    if req.get("action") != "task":
        return False
    task_type = req.get("type")
    if task_type and task_type not in UPPER_LAYER_TASK_TYPES:
        return False
    raw_input = ((req.get("input") or {}).get("input"))
    return isinstance(raw_input, str) and bool(raw_input.strip())


def _first_present(*values):
    for value in values:
        if value not in (None, "", [], {}):
            return value
    return None



def _extract_host_semantic_inputs(req: dict) -> dict:
    input_data = req.get("input", {}) or {}
    metadata = req.get("metadata", {}) or {}
    config = req.get("config", {}) or {}

    host_analysis = _first_present(
        input_data.get("understanding"),
        input_data.get("hostAnalysis"),
        input_data.get("modelAnalysis"),
        metadata.get("understanding"),
        metadata.get("hostAnalysis"),
        metadata.get("modelAnalysis"),
        config.get("understanding"),
        config.get("hostAnalysis"),
        config.get("modelAnalysis"),
    )
    host_product_summary = _first_present(
        input_data.get("productSummary"),
        input_data.get("hostProductSummary"),
        metadata.get("productSummary"),
        metadata.get("hostProductSummary"),
        config.get("productSummary"),
        config.get("hostProductSummary"),
    )
    host_drafts = _first_present(
        input_data.get("hostDrafts"),
        input_data.get("hostEmailDrafts"),
        input_data.get("emailModelDrafts"),
        metadata.get("hostDrafts"),
        metadata.get("hostEmailDrafts"),
        metadata.get("emailModelDrafts"),
        config.get("hostDrafts"),
        config.get("hostEmailDrafts"),
        config.get("emailModelDrafts"),
    )
    host_reply_analysis = _first_present(
        input_data.get("replyModelAnalysis"),
        input_data.get("conversationAnalysis"),
        metadata.get("replyModelAnalysis"),
        metadata.get("conversationAnalysis"),
        config.get("replyModelAnalysis"),
        config.get("conversationAnalysis"),
    )
    host_search_results = _first_present(
        input_data.get("searchResults"),
        metadata.get("searchResults"),
        config.get("searchResults"),
    )
    return {
        "host_analysis": host_analysis,
        "host_product_summary": host_product_summary,
        "host_drafts": host_drafts,
        "host_reply_analysis": host_reply_analysis,
        "host_search_results": host_search_results,
    }


def _run_upper_layer_once(req: dict) -> dict:
    task_type = req.get("type")
    input_data = req.get("input", {}) or {}
    raw_input = input_data.get("input")
    host_inputs = _extract_host_semantic_inputs(req)
    request_passthrough = {
        "campaignId": input_data.get("campaignId"),
        "contactedBloggerIds": input_data.get("contactedBloggerIds"),
        "pageSize": input_data.get("pageSize"),
    }
    from orchestrator import UpperLayerOrchestrator
    orchestrator = UpperLayerOrchestrator(req.get("auth", {}).get("token"))
    orchestrated = orchestrator.run_from_user_input(
        raw_input,
        explicit_task=task_type,
        config=req.get("config", {}) or {},
        host_analysis=host_inputs.get("host_analysis"),
        host_product_summary=host_inputs.get("host_product_summary"),
        host_drafts=host_inputs.get("host_drafts"),
        host_reply_analysis=host_inputs.get("host_reply_analysis"),
        host_search_results=host_inputs.get("host_search_results"),
        request_passthrough=request_passthrough,
    )
    return {"orchestrator": orchestrator, "orchestrated": orchestrated}


def _extract_host_url_analysis_request(orchestrated: dict) -> Optional[dict]:
    result = (orchestrated or {}).get("result") or {}
    if isinstance(result.get("hostUrlAnalysisRequest"), dict) and result.get("hostUrlAnalysisRequest"):
        return result.get("hostUrlAnalysisRequest")
    semantic_context = (orchestrated or {}).get("semanticContext") or {}
    resolved = semantic_context.get("resolvedArtifacts") or {}
    product_resolve = resolved.get("productResolve") or {}
    request = product_resolve.get("hostUrlAnalysisRequest")
    return request if isinstance(request, dict) and request else None


def _maybe_auto_resolve_host_url_analysis(req: dict, orchestrator: object, orchestrated: dict) -> tuple[dict, Optional[dict]]:
    request = _extract_host_url_analysis_request(orchestrated)
    if not request:
        return req, None
    config = req.get("config", {}) or {}
    executor = None
    if hasattr(orchestrator, "_get_host_analysis_executor"):
        executor = orchestrator._get_host_analysis_executor(config=config)
    if not executor:
        return req, {
            "status": "no_executor_configured",
            "request": request,
        }
    payload = orchestrator._run_host_analysis_executor(request=request, executor_spec=executor)
    extracted = orchestrator._extract_host_analysis_payload(payload)
    analysis = extracted.get("analysis")
    product_summary = extracted.get("productSummary")
    if not isinstance(analysis, dict) or not analysis:
        return req, {
            "status": "executor_returned_empty",
            "request": request,
            "executor": orchestrator._describe_executor(executor),
        }
    prepared_req = dict(req)
    prepared_input = dict(prepared_req.get("input", {}) or {})
    prepared_input["hostAnalysis"] = analysis
    prepared_input["productSummary"] = product_summary or prepared_input.get("productSummary") or {}
    prepared_req["input"] = prepared_input
    return prepared_req, {
        "status": "resolved_from_executor",
        "request": request,
        "executor": orchestrator._describe_executor(executor),
        "hostAnalysis": analysis,
        "productSummary": product_summary,
    }


def _maybe_handle_with_upper_layer(req: dict) -> Optional[dict]:
    if not _should_use_upper_layer(req):
        return None
    try:
        first_run = _run_upper_layer_once(req)
        orchestrator = first_run.get("orchestrator")
        orchestrated = first_run.get("orchestrated") or {}
        auto_resolution = None
        prepared_req, auto_resolution = _maybe_auto_resolve_host_url_analysis(req, orchestrator, orchestrated)
        if auto_resolution and auto_resolution.get("status") == "resolved_from_executor":
            orchestrated = (_run_upper_layer_once(prepared_req) or {}).get("orchestrated") or orchestrated
        return {
            "requestId": req.get("requestId"),
            "status": "success",
            "result": orchestrated.get("result"),
            "error": None,
            "metadata": {
                "analysisPath": orchestrated.get("analysisPath"),
                "delegatedTask": orchestrated.get("delegatedTask"),
                "semanticContext": orchestrated.get("semanticContext"),
                "legacyInput": orchestrated.get("legacyInput"),
                "route": orchestrated.get("route"),
                "observations": orchestrated.get("observations"),
                **({"hostUrlAnalysisAutoResolution": auto_resolution} if auto_resolution else {}),
            },
        }
    except Exception as e:
        return {
            "_upper_layer_error": str(e),
        }


def _load_brief_from_request(req: dict) -> Optional[dict]:
    input_data = req.get("input", {}) or {}
    brief = input_data.get("brief")
    if isinstance(brief, dict):
        return brief
    brief_path = input_data.get("briefPath")
    if not brief_path:
        return None
    try:
        loaded = json.loads(Path(brief_path).read_text(encoding="utf-8"))
    except Exception:
        return None
    return loaded if isinstance(loaded, dict) else None


def _extract_campaign_cycle_raw_input(brief: dict) -> Optional[str]:
    if not isinstance(brief, dict):
        return None
    product = brief.get("product") or {}
    search = brief.get("search") or {}
    candidates = [
        brief.get("input"),
        product.get("url"),
        product.get("productName"),
    ]
    for candidate in candidates:
        if isinstance(candidate, str) and candidate.strip():
            return candidate.strip()
    platform = search.get("platform")
    region = search.get("region")
    if isinstance(platform, str) and platform.strip():
        if isinstance(region, list) and region:
            return f"{platform} {' '.join(str(x) for x in region if str(x).strip())}".strip()
        return platform.strip()
    return None


def _extract_campaign_host_inputs(brief: dict, req: dict) -> dict:
    config = req.get("config", {}) or {}
    scheduler = (brief.get("scheduler") or {}) if isinstance(brief, dict) else {}
    host_analysis = _first_present(
        (brief or {}).get("hostAnalysis"),
        (brief or {}).get("host_analysis"),
        (brief or {}).get("modelAnalysis"),
        (brief or {}).get("model_analysis"),
        config.get("hostAnalysis"),
        config.get("modelAnalysis"),
        scheduler.get("hostAnalysis"),
        scheduler.get("modelAnalysis"),
    )
    host_product_summary = _first_present(
        (brief or {}).get("productSummary"),
        (brief or {}).get("hostProductSummary"),
        config.get("productSummary"),
        config.get("hostProductSummary"),
    )
    host_reply_analysis = _first_present(
        (brief or {}).get("replyModelAnalysis"),
        (brief or {}).get("reply_model_analysis"),
        config.get("replyModelAnalysis"),
    )
    return {
        "host_analysis": host_analysis,
        "host_product_summary": host_product_summary,
        "host_reply_analysis": host_reply_analysis,
    }


def _maybe_prepare_campaign_cycle_with_upper_layer(req: dict) -> tuple[dict, Optional[dict]]:
    if req.get("action") != "campaign" or req.get("type") != "cycle":
        return req, None

    brief = _load_brief_from_request(req)
    if not isinstance(brief, dict):
        return req, None

    raw_input = _extract_campaign_cycle_raw_input(brief)
    if not raw_input:
        return req, None

    try:
        from orchestrator import UpperLayerOrchestrator

        host_inputs = _extract_campaign_host_inputs(brief, req)
        orchestrated = UpperLayerOrchestrator(req.get("auth", {}).get("token")).run_from_user_input(
            raw_input,
            explicit_task="campaign_create",
            config=req.get("config", {}) or {},
            host_analysis=host_inputs.get("host_analysis"),
            host_product_summary=host_inputs.get("host_product_summary"),
            host_reply_analysis=host_inputs.get("host_reply_analysis"),
            request_passthrough={"campaignId": (req.get("input", {}) or {}).get("campaignId")},
        )
    except Exception as e:
        return req, {"error": str(e), "prepared": False}

    semantic_context = orchestrated.get("semanticContext") or {}
    resolved = semantic_context.get("resolvedArtifacts") or {}
    model_analysis = resolved.get("modelAnalysis")
    product_summary = resolved.get("productSummary")

    prepared_req = dict(req)
    prepared_input = dict(prepared_req.get("input", {}) or {})
    prepared_brief = dict(brief)
    prepared = False

    if isinstance(model_analysis, dict) and model_analysis:
        prepared_brief["hostAnalysis"] = model_analysis
        prepared_brief["host_analysis"] = model_analysis
        prepared_brief["modelAnalysis"] = model_analysis
        prepared_brief["model_analysis"] = model_analysis
        prepared = True

    if isinstance(product_summary, dict) and product_summary:
        prepared_brief["productSummary"] = product_summary
        prepared_brief["hostProductSummary"] = product_summary
        prepared = True

    if prepared:
        prepared_input["brief"] = prepared_brief
        prepared_req["input"] = prepared_input

    return prepared_req, {
        "prepared": prepared,
        "analysisPath": orchestrated.get("analysisPath"),
        "delegatedTask": orchestrated.get("delegatedTask"),
        "route": orchestrated.get("route"),
        "observations": orchestrated.get("observations"),
    }


def main():
    """OpenClaw entry point. Read request from stdin, output response to stdout."""
    try:
        req = json.loads(sys.stdin.read())
    except json.JSONDecodeError as e:
        print(json.dumps({
            "status": "error",
            "error": f"Invalid JSON: {str(e)}"
        }))
        return 1

    try:
        upper_layer_response = _maybe_handle_with_upper_layer(req)
        if upper_layer_response is not None:
            if not upper_layer_response.get("_upper_layer_error"):
                print(json.dumps(upper_layer_response, ensure_ascii=False))
                return 0

        prepared_req, campaign_upper_layer = _maybe_prepare_campaign_cycle_with_upper_layer(req)

        from api import handle_api_request
        response = handle_api_request(prepared_req)
        if upper_layer_response and upper_layer_response.get("_upper_layer_error"):
            if isinstance(response, dict):
                metadata = response.setdefault("metadata", {})
                metadata["upperLayerFallbackReason"] = upper_layer_response.get("_upper_layer_error")
                metadata["fellBackToLegacy"] = True
        if campaign_upper_layer and isinstance(response, dict):
            metadata = response.setdefault("metadata", {})
            metadata["campaignUpperLayer"] = campaign_upper_layer
        print(json.dumps(response, ensure_ascii=False))
        return 0
    except Exception as e:
        print(json.dumps({
            "status": "error",
            "error": str(e)
        }))
        return 1


if __name__ == "__main__":
    sys.exit(main())
