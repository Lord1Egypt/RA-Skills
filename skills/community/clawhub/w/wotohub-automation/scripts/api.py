#!/usr/bin/env python3
"""Unified external API for WotoHub skill.

Design: Minimal wrapper. Delegates to existing scripts.
- Validation: api_validator
- Task execution: api_task_runner
- Campaign execution: api_campaign_runner
"""

from __future__ import annotations

from typing import Optional

import json
import uuid
from datetime import datetime
from pathlib import Path

from api_validator import validate_request, validate_task_input, validate_campaign_input
from api_task_runner import TaskRunner
from api_campaign_runner import CampaignRunner


class WotoHubAPI:
    """Unified API. Thin wrapper around existing scripts."""

    def __init__(self, token: Optional[str]= None):
        self.token = token

    def handle_request(self, req: dict) -> dict:
        """Main entry point."""
        request_id = req.get("requestId", str(uuid.uuid4()))

        valid, error_msg = validate_request(req)
        if not valid:
            return self._error(request_id, error_msg)

        try:
            action = req["action"]
            task_type = req["type"]
            input_data = req.get("input", {})
            config = req.get("config", {})
            token = req.get("auth", {}).get("token") or self.token

            if action == "task":
                return self._task(request_id, task_type, input_data, config, token)
            elif action == "campaign":
                return self._campaign(request_id, task_type, input_data, config, token)
            else:
                return self._error(request_id, f"Unknown action: {action}")
        except Exception as e:
            return self._error(request_id, str(e))

    def _task(self, request_id: str, task_type: str, input_data: dict, config: dict, token: Optional[str]) -> dict:
        """Execute single-shot task."""
        valid, error_msg = validate_task_input(task_type, input_data)
        if not valid:
            return self._error(request_id, error_msg)

        start = datetime.now()
        try:
            result = TaskRunner(token).run(task_type, input_data, config)
            return {
                "requestId": request_id,
                "status": "success",
                "result": result,
                "error": None,
                "metadata": {
                    "duration": (datetime.now() - start).total_seconds(),
                    "timestamp": datetime.now().isoformat(),
                },
            }
        except Exception as e:
            return self._error(request_id, f"Task failed: {str(e)}")

    def _campaign(self, request_id: str, action: str, input_data: dict, config: dict, token: Optional[str]) -> dict:
        """Execute campaign cycle."""
        if action != "cycle":
            return self._error(request_id, f"Unknown campaign action: {action}")

        valid, error_msg = validate_campaign_input(input_data)
        if not valid:
            return self._error(request_id, error_msg)

        brief = input_data.get("brief")
        if not isinstance(brief, dict):
            brief_path = input_data.get("briefPath")
            try:
                loaded = json.loads(Path(brief_path).read_text(encoding="utf-8")) if brief_path else None
            except Exception as e:
                return self._error(request_id, f"Failed to load briefPath: {e}")
            if not isinstance(loaded, dict):
                return self._error(request_id, "briefPath must point to a JSON object")
            brief = loaded

        start = datetime.now()
        try:
            result = CampaignRunner().run_cycle(
                input_data["campaignId"],
                brief,
                {**config, "token": token},
            )
            host_request = result.get("hostDraftGenerationRequest")
            host_reply_request = result.get("hostReplyAnalysisRequest")
            host_bridge_payload = None
            host_reply_bridge_payload = None
            host_executor_example = None
            if host_request:
                runner = CampaignRunner()
                host_bridge_payload = runner.build_host_model_bridge_payload(request=host_request)
                host_executor_example = runner.build_host_model_executor_example(bridge_payload=host_bridge_payload)
            if host_reply_request:
                runner = CampaignRunner()
                host_reply_bridge_payload = runner.build_host_reply_bridge_payload(request=host_reply_request)
            return {
                "requestId": request_id,
                "status": "success",
                "result": result,
                "error": None,
                "metadata": {
                    "duration": (datetime.now() - start).total_seconds(),
                    "timestamp": datetime.now().isoformat(),
                    "nextAction": result.get("nextAction"),
                    "hostDraftGenerationRequest": host_request,
                    "hostReplyAnalysisRequest": host_reply_request,
                    "hostModelBridgePayload": host_bridge_payload,
                    "hostReplyBridgePayload": host_reply_bridge_payload,
                    "hostModelExecutorExample": host_executor_example,
                    "draftGeneration": result.get("draftGeneration"),
                    "runtimeOrchestration": result.get("runtimeOrchestration"),
                },
            }
        except Exception as e:
            return self._error(request_id, f"Campaign failed: {str(e)}")

    def _error(self, request_id: str, message: str) -> dict:
        """Build error response."""
        return {
            "requestId": request_id,
            "status": "error",
            "result": None,
            "error": {"message": message},
            "metadata": {"timestamp": datetime.now().isoformat()},
        }


def handle_api_request(req: dict) -> dict:
    """Public entry point."""
    token = req.get("auth", {}).get("token")
    return WotoHubAPI(token).handle_request(req)
