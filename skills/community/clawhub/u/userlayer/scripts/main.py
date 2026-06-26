import os
import requests
from typing import Dict, Any

from .call_api import call_api

LAUNCHBASE_API_URL = os.environ.get("LAUNCHBASE_API_URL", "https://lb-api.workflowhunt.com")
SERVICE_NAME = "userlayer"

def analyze(app_url: str, max_reviews: int | None = None) -> Dict[str, Any]:
    """
    Submit a full async analysis job.
    Default review count is 100 latest reviews. Callers may explicitly raise it when they want broader coverage.
    """
    params: Dict[str, Any] = {"app_url": app_url}
    if max_reviews is not None:
        params["max_reviews"] = max_reviews

    return call_api(
        service=SERVICE_NAME,
        endpoint="/analyze",
        params=params,
    )

def query(pain_point_id: str, question: str) -> Dict[str, Any]:
    """
    针对已分析生成的痛点进行追问。
    基于 pgvector 语义检索提供回答及引用来源。
    """
    return call_api(
        service=SERVICE_NAME,
        endpoint="/query",
        params={"pain_point_id": pain_point_id, "question": question},
    )

def check_status(analysis_id: str) -> Dict[str, Any]:
    """
    Poll async analysis status.
    """
    api_key = os.environ.get("API_KEY")
    if not api_key:
        return {"success": False, "error": "AUTH_NO_API_KEY"}
        
    try:
        response = requests.get(
            f"{LAUNCHBASE_API_URL}/v1/{SERVICE_NAME}/analyze/{analysis_id}/status",
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=30
        )
        if response.status_code != 200:
            try:
                err_data = response.json()
                if "error" in err_data:
                    return err_data
            except Exception:
                pass
            response.raise_for_status()
            
        return response.json()
    except Exception as e:
        return {"success": False, "error": str(e)}
