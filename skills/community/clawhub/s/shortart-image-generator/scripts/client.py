#!/usr/bin/env python3
"""Unified ShortArt API Client"""
from typing import Dict, Any, List, Optional, Union
import base64
import io
import os
import tempfile


def _get_requests():
    try:
        import requests
        return requests
    except ImportError:
        raise ImportError("requests is required: pip install requests")


class ShortArtClient:
    def __init__(self, api_key: str = None, base_url: str = "https://api.shortart.ai"):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self._requests = _get_requests()

    def _headers(self) -> Dict[str, str]:
        h = {"Content-Type": "application/json", "Accept": "*/*"}
        if self.api_key:
            h["Authorization"] = f"Bearer {self.api_key}"
        return h

    def _post(self, path: str, payload: dict) -> dict:
        resp = self._requests.post(
            f"{self.base_url}{path}",
            headers=self._headers(),
            json=payload,
            timeout=60,
        )
        resp.raise_for_status()
        return resp.json()

    def _get(self, path: str, params: dict = None) -> dict:
        resp = self._requests.get(
            f"{self.base_url}{path}",
            headers=self._headers(),
            params=params,
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()

    def upload_image(self, image_input: Union[str, bytes]) -> Dict[str, Any]:
        """
        Upload image to OSS - supports multiple input formats:
        1. File path (str): "/path/to/image.jpg"
        2. Base64 string (str): "data:image/png;base64,iVBORw0KG..." or "iVBORw0KG..."
        3. Raw bytes (bytes): b'\x89PNG\r\n...'
        """
        try:
            file_obj = None
            filename = "image.jpg"
            temp_file = None

            # Determine input type and prepare file object
                # Check if it's a base64 string
            if image_input.startswith("data:image/"):
                # Data URI format: data:image/png;base64,iVBORw0KG...
                try:
                    header, encoded = image_input.split(",", 1)
                    image_data = base64.b64decode(encoded)
                    file_obj = io.BytesIO(image_data)

                    # Extract file extension from MIME type
                    if "image/png" in header:
                        filename = "image.png"
                    elif "image/jpeg" in header or "image/jpg" in header:
                        filename = "image.jpg"
                    elif "image/webp" in header:
                        filename = "image.webp"
                except Exception as e:
                    return {"status": "error", "error": f"Invalid base64 data URI: {e}"}

            elif image_input.strip().replace("\n", "").replace(" ", "").isalnum() or "==" in image_input:
                # Pure base64 string (without data URI prefix)
                try:
                    image_data = base64.b64decode(image_input)
                    file_obj = io.BytesIO(image_data)
                    filename = "image.jpg"
                except Exception as e:
                    return {"status": "error", "error": f"Invalid base64 string: {e}"}

            elif os.path.isfile(image_input):
                # File path
                file_obj = open(image_input, "rb")
                filename = os.path.basename(image_input)

            else:
                return {"status": "error", "error": f"Invalid input: not a valid file path or base64 string"}

            # Upload to OSS
            resp = self._requests.post(
                f"{self.base_url}/api/oss/upload",
                headers={"Authorization": f"Bearer {self.api_key}"},
                files={"file": (filename, file_obj)},
                data={"type": "temp"},
                timeout=60,
            )

            # Clean up
            if isinstance(file_obj, io.IOBase):
                file_obj.close()
            if temp_file and os.path.exists(temp_file):
                os.unlink(temp_file)

            resp.raise_for_status()
            data = resp.json()
            if data.get("code") == 0:
                d = data.get("data", {})
                return {
                    "status": "success",
                    "path": d.get("path"),
                    "domain": d.get("domain"),
                    "width": d.get("width"),
                    "height": d.get("height"),
                }
            return {"status": "error", "error": data.get("message", "Upload failed")}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def fetch_status(self, project_ids: str) -> Dict[str, Any]:
        """Fetch project status"""
        try:
            data = self._get("/api/project/fetch-status", params={"projectIds": project_ids})
            if data.get("code") == 0:
                projects = data.get("data", {}).get("projects", [])
                if projects:
                    project = projects[0]
                    return {
                        "status": "success",
                        "project_status": project.get("status"),
                        "project_error": project.get("error"),
                    }
                return {"status": "error", "error": "No project found"}
            return {"status": "error", "error": data.get("message", "Unknown error")}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def get_project(self, project_id: str) -> Dict[str, Any]:
        """Get project details"""
        try:
            data = self._get("/api/project/get", params={"projectID": project_id})
            if data.get("code") == 0:
                project = data["data"].get("project", )
                domain = project.get("domain", "")
                result = project.get("result") or {}
                images = []
                for img in result.get("images") or []:
                    path = img.get("path", "")
                    images.append({
                        "id": img.get("id"),
                        "path": path,
                        "url": f"{domain}{path}" if domain and not path.startswith("http") else path,
                        "width": img.get("width"),
                        "height": img.get("height"),
                        "risk_level": img.get("riskLevel"),
                    })
                return {
                    "status": "success",
                    "project_status": project.get("status"),
                    "project_error": project.get("error"),
                    "domain": domain,
                    "images": images,
                    "result": result,
                }
            return {"status": "error", "error": data.get("message", "Unknown error")}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    # Text-to-image
    def create_project(
        self,
        prompt: str,
        model: str,
        count: int = 1,
        images: Optional[List[str]] = None,
        resolution: str = "2k",
        aspect_ratio: str = "1:1",
    ) -> Dict[str, Any]:
        """Create text-to-image project"""
        payload: Dict[str, Any] = {
            "model": model,
            "prompt": prompt,
            "count": count,
            "resolution": resolution,
            "aspectRatio": aspect_ratio,
        }
        if images:
            payload["images"] = images

        try:
            data = self._post("/api/project/create", payload)
            if data.get("code") == 0:
                d = data.get("data", {})
                return {
                    "status": "success",
                    "project_id": d.get("projectId"),
                    "credit": d.get("credit"),
                    "sub_credit": d.get("subCredit"),
                    "consumed_credit": d.get("consumedCredit"),
                }
            return {"status": "error", "error": data.get("message", "Unknown error")}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    # Suit image
    def create_suit_image(self, prompt: str, image: str) -> Dict[str, Any]:
        """Create suit image project"""
        try:
            payload = {"images": [image], "prompt": prompt}
            data = self._post("/api/project/create-image-suit", payload)
            if data.get("code") == 0:
                d = data["data"]
                return {
                    "status": "success",
                    "project_id": d["projectId"],
                    "credit": d.get("credit"),
                    "sub_credit": d.get("subCredit"),
                    "consumed_credit": d.get("consumedCredit"),
                }
            return {"status": "error", "error": data.get("message", "Unknown error")}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    # Template
    def list_templates(self, keywords: List[str], count: int = 6) -> Dict[str, Any]:
        """List templates by keywords"""
        try:
            data = self._get("/api/template/list-for-agent", params={"keywords": keywords, "count": count})
            if data.get("code") == 0:
                return {"status": "success", "templates": data.get("data", [])}
            return {"status": "error", "error": data.get("message", "Unknown error")}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def get_template(self, slug: str) -> Dict[str, Any]:
        """Get template by slug"""
        try:
            data = self._get("/api/template/get", params={"slug": slug})
            if data.get("code") == 0:
                return {"status": "success", "template": data.get("data", {}).get("template", {})}
            return {"status": "error", "error": data.get("message", "Unknown error")}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def create_from_template(
        self, template_id: str, args: List[Dict], images: List[str]
    ) -> Dict[str, Any]:
        """Create project from template"""
        try:
            payload = {"templateId": template_id, "args": args, "images": images}
            data = self._post("/api/project/create-by-template", payload)
            if data.get("code") == 0:
                d = data.get("data", {})
                return {
                    "status": "success",
                    "project_id": d.get("projectId"),
                    "credit": d.get("credit"),
                    "sub_credit": d.get("subCredit"),
                    "consumed_credit": d.get("consumedCredit"),
                }
            error_msg = data.get("message") or data.get("info") or "Unknown error"
            return {"status": "error", "error": f"Create failed: {error_msg} (code: {data.get('code')})"}
        except Exception as e:
            return {"status": "error", "error": str(e)}
