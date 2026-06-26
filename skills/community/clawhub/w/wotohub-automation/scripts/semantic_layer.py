#!/usr/bin/env python3
"""
Semantic helpers for WotoHub.

Policy:
- Host model output should be preferred by the caller for semantic understanding.
- This module provides transitional helpers, schema shaping, embeddings, and local fallbacks.
- Keep it efficient and usable; do not require a full rewrite before the skill can run.
"""

from __future__ import annotations

import json
import os
import shlex
import subprocess
import sys
from pathlib import Path
from typing import Any, Optional

ROOT = Path(__file__).resolve().parents[1]
JINA_API_KEY: Optional[str]= os.environ.get("JINA_API_KEY")
JINA_EMBED_URL: str = "https://api.jina.ai/v1/embed"


class SemanticLayer:
    """Semantic helper interface.

    Preferred path: consume host-model-produced structured analysis.
    Local analysis methods remain available as transitional fallbacks for usability,
    but should not silently replace host understanding on core execution paths.
    """

    @staticmethod
    def understand_user_input(raw_input: str, explicit_task: Optional[str]= None) -> dict[str, Any]:
        """Upper-layer input understanding helper.

        Current skill behavior:
        - stays host-model-analysis-preferred in interface shape
        - uses lightweight local shaping as compatibility fallback
        - only allows local structured understanding in product_analysis or explicit debug mode
        - explicitly reports usedHostModel / usedFallback / needsHostAnalysis
        """
        text = (raw_input or "").strip()
        lowered = text.lower()

        primary_task = explicit_task or None
        if not primary_task:
            if any(token in lowered for token in ["reply", "回复", "收件箱", "inbox"]):
                primary_task = "monitor_replies"
            elif any(token in lowered for token in ["email", "outreach", "邀约", "邮件"]):
                primary_task = "generate_email"
            elif any(token in lowered for token in ["search", "达人", "红人", "creator", "influencer"]):
                primary_task = "search"
            else:
                primary_task = "product_analysis"

        analysis = SemanticLayer.analyze_model(text)
        allow_local_understanding = (
            explicit_task == "product_analysis"
            or os.environ.get("WOTOHUB_ALLOW_LOCAL_UNDERSTANDING_FALLBACK", "").strip().lower() in {"1", "true", "yes", "on"}
        )
        product = analysis.get("product") or {}
        constraints = analysis.get("constraints") or {}
        marketing = analysis.get("marketing") or {}

        resolved_artifacts = {
            "productResolve": None,
            "modelAnalysis": analysis if allow_local_understanding else None,
            "replyModelAnalysis": None,
            "localHeuristicAnalysis": analysis,
            "productSummary": None,
        }

        notes = []
        if allow_local_understanding:
            notes.append("local compatibility understanding used as structured analysis (allowed only for product_analysis or explicit debug mode)")
        else:
            notes.append("local heuristic understanding used only for shaping and hints")
            notes.append("core execution tasks should inject host understanding or pass through product_resolve before delegate")

        return {
            "intent": {
                "primaryTask": primary_task,
                "secondaryTasks": [],
            },
            "productSignals": {
                "rawInput": text,
                "urls": [],
                "productName": product.get("productName"),
                "brand": product.get("brand"),
                "category": product.get("productType") or product.get("productSubtype"),
                "priceHint": product.get("price"),
                "features": product.get("features") or product.get("coreBenefits") or [],
                "useCases": product.get("functions") or [],
                "sourcePlatform": None,
                "sourceHost": None,
            },
            "marketingContext": {
                "targetMarkets": constraints.get("regions") or [],
                "platforms": marketing.get("platformPreference") or [],
                "creatorTypes": marketing.get("creatorTypes") or [],
                "followerRange": {
                    "min": constraints.get("minFansNum"),
                    "max": constraints.get("maxFansNum"),
                },
                "offerType": None,
                "budgetLevel": None,
                "goal": None,
                "languages": constraints.get("languages") or [],
            },
            "operationalHints": {
                "needsProductResolve": text.startswith("http://") or text.startswith("https://"),
                "needsSearch": primary_task in {"search", "recommend"},
                "needsCampaignBuild": primary_task == "campaign_create",
                "needsOutreachDraft": primary_task == "generate_email",
                "needsInboxAssist": primary_task == "monitor_replies",
            },
            "missingFields": [],
            "resolvedArtifacts": resolved_artifacts,
            "meta": {
                "usedHostModel": False,
                "usedFallback": True,
                "needsHostAnalysis": not allow_local_understanding,
                "confidence": "medium",
                "analysisPath": "semantic_layer_local_understanding" if allow_local_understanding else "semantic_layer_local_heuristic_only",
                "notes": notes,
            },
        }

    @staticmethod
    def get_embedding(text: str) -> Optional[list[float]]:
        """Get text embedding via Jina API."""
        if not JINA_API_KEY:
            return None
        try:
            import requests
            resp = requests.post(
                JINA_EMBED_URL,
                json={
                    "model": "jina-embeddings-v3",
                    "task": "semantic-text-matching",
                    "input": [text],
                },
                headers={"Authorization": f"Bearer {JINA_API_KEY}"},
                timeout=15,
            )
            resp.raise_for_status()
            data = resp.json()
            embedding = data.get("data", [])
            if embedding and isinstance(embedding, list):
                return embedding[0].get("embedding")
            return None
        except Exception:
            return None

    @staticmethod
    def cosine_sim(a: list[float], b: list[float]) -> float:
        """Compute cosine similarity between two vectors."""
        import math
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = math.sqrt(sum(x * x for x in a))
        norm_b = math.sqrt(sum(x * x for x in b))
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot / (norm_a * norm_b)

    @staticmethod
    def expand_keywords(keywords: list[str]) -> list[str]:
        """Expand keywords via semantic enrichment."""
        if not keywords:
            return []
        return keywords

    @staticmethod
    def match_to_form(
        text: str,
        forms: Optional[dict[str, Any]]= None,
        top_k: int = 5,
    ) -> list[tuple[str, float]]:
        """Match text to form categories via embedding similarity."""
        if not JINA_API_KEY:
            return []

        if forms is None:
            forms_path = ROOT / "references" / "custom-forms.json"
            if forms_path.exists():
                try:
                    forms = json.loads(forms_path.read_text(encoding="utf-8")).get("forms", {})
                except Exception:
                    forms = {}
            else:
                forms = {}

        if not forms:
            return []

        form_names = list(forms.keys())
        text_emb = SemanticLayer.get_embedding(text)
        if text_emb is None:
            return []

        scores: list[tuple[str, float]] = []
        for name in form_names:
            form_def = forms[name]
            aliases = " ".join(form_def.get("aliases", []))
            functions = " ".join(form_def.get("functions", []))
            target_areas = " ".join(form_def.get("targetAreas", []))
            form_text = f"{name} {aliases} {functions} {target_areas}".strip()

            form_emb = SemanticLayer.get_embedding(form_text)
            if form_emb is not None:
                score = SemanticLayer.cosine_sim(text_emb, form_emb)
                scores.append((name, round(score, 4)))

        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]

    @staticmethod
    def analyze_model(
        user_input: str,
        url: Optional[str]= None,
        page_title: Optional[str]= None,
        brand: Optional[str]= None,
        price: Optional[float]= None,
        features: Optional[list[str]]= None,
    ) -> dict[str, Any]:
        """Build model-analysis-style output from local fallback logic.

        Note: despite the legacy name, this is now a compatibility helper that
        shapes local/transitional analysis into the shared model-analysis schema.
        Callers should prefer host-model-produced analysis when available.
        """
        import product_analyze
        from query_constraints import build_region_list

        fallback = product_analyze.analyze_input(user_input)
        product_summary = fallback.get("productSummary", {}) or {}
        search_conditions = fallback.get("searchConditions", {}) or {}
        payload_hints = search_conditions.get("payloadHints", {}) or {}

        product_name = product_summary.get("productName") or page_title or ""
        core_benefits = product_summary.get("sellingPoints") or []
        functions = product_summary.get("detectedFunctions") or []
        target_audiences = product_summary.get("targetAudiences") or []
        category_forms = product_summary.get("detectedForms") or []
        price_hint = product_summary.get("priceHint", price)
        price_tier = product_summary.get("priceTier") or "unknown"

        platform_pref = product_summary.get("platformHints") or search_conditions.get("platforms") or ["tiktok"]
        creator_types = product_summary.get("creatorAngles") or []

        regions = product_summary.get("regionHints") or search_conditions.get("regions") or ["us"]
        languages = product_summary.get("languageHints") or search_conditions.get("languages") or ["en"]

        clarifications_needed = []
        if not product_name:
            clarifications_needed.append({"field": "productName", "reason": "缺少明确产品名或产品锚点"})
        if not category_forms and not core_benefits:
            clarifications_needed.append({"field": "productSemantics", "reason": "缺少明确产品品类或核心卖点"})

        product_subtype = product_summary.get("productSubtype") or product_summary.get("productTypeHint") or (category_forms[0] if category_forms else None)
        creator_intent = creator_types[:]

        content_angles = product_summary.get("contentAngles") or []
        if not content_angles:
            lowered = " ".join([str(x) for x in [product_name, *core_benefits, *functions] if x]).lower()
            heuristic_angles = []
            if any(k in lowered for k in ["before", "after", "whitening", "clean", "cleaning", "deep clean"]):
                heuristic_angles.append("before_after_or_problem_solution")
            if any(k in lowered for k in ["routine", "daily", "convenience", "time saving", "portable"]):
                heuristic_angles.append("routine_integration")
            if any(k in lowered for k in ["demo", "review", "feature", "setup", "stabilization", "tracking"]):
                heuristic_angles.append("review_or_demo")
            content_angles = heuristic_angles[:3]

        return {
            "product": {
                "productName": product_name,
                "productType": product_summary.get("productTypeHint"),
                "productSubtype": product_subtype,
                "categoryForms": category_forms,
                "coreBenefits": core_benefits,
                "functions": functions,
                "targetAreas": product_summary.get("detectedTargetAreas") or [],
                "targetAudiences": target_audiences,
                "price": price_hint,
                "priceTier": price_tier,
                "brand": brand or product_summary.get("brand"),
                "sourceUrl": url,
                "pageTitle": page_title,
                "features": features or [],
            },
            "marketing": {
                "platformPreference": platform_pref,
                "creatorTypes": creator_types,
                "creatorIntent": creator_intent,
                "contentAngles": content_angles,
            },
            "constraints": {
                "regions": regions,
                "languages": languages,
                "minFansNum": search_conditions.get("minFansNum"),
                "maxFansNum": search_conditions.get("maxFansNum"),
                "hasEmail": search_conditions.get("hasEmail", True),
            },
            "searchPayloadHints": {
                "platform": payload_hints.get("platform", platform_pref[0] if platform_pref else "tiktok"),
                "blogCateIds": payload_hints.get("blogCateIds", []),
                "regionList": payload_hints.get("regionList", build_region_list(regions)),
                "blogLangs": payload_hints.get("blogLangs", languages),
                "hasEmail": payload_hints.get("hasEmail", search_conditions.get("hasEmail", True)),
            },
            "clarificationsNeeded": clarifications_needed,
        }

    @staticmethod
    def call_external_backend(payload: dict[str, Any]) -> dict[str, Any]:
        """Call external semantic provider."""
        backend_cmd = os.environ.get("WOTOHUB_LLM_BACKEND_CMD", "").strip()
        if not backend_cmd:
            return SemanticLayer._build_mock_response(payload.get("input", {}).get("rawText", ""))

        try:
            backend_args = shlex.split(backend_cmd)
            completed = subprocess.run(
                backend_args,
                input=json.dumps(payload, ensure_ascii=False),
                text=True,
                capture_output=True,
                cwd=str(ROOT),
                timeout=60,
            )
            if completed.returncode != 0:
                return SemanticLayer._build_mock_response(payload.get("input", {}).get("rawText", ""))

            stdout = (completed.stdout or "").strip()
            if not stdout:
                return SemanticLayer._build_mock_response(payload.get("input", {}).get("rawText", ""))

            return json.loads(stdout)
        except Exception:
            return SemanticLayer._build_mock_response(payload.get("input", {}).get("rawText", ""))

    @staticmethod
    def _build_mock_response(raw: str) -> dict[str, Any]:
        """Build mock semantic response."""
        raw_l = raw.lower()
        product = {
            "name": None,
            "brand": None,
            "category_labels": [],
            "benefit_labels": [],
            "audience_labels": [],
            "price_tier": "unknown",
        }
        constraints = {
            "regions": ["us"] if ("美国" in raw or "us" in raw_l or "united states" in raw_l) else [],
            "languages": ["en"] if ("英语" in raw or "english" in raw_l) else [],
            "platforms": ["tiktok"] if "tiktok" in raw_l else [],
            "min_fans": 10000 if "1万粉以上" in raw else None,
            "max_fans": None,
            "has_email": True if ("有邮箱" in raw or "email" in raw_l) else None,
        }
        marketing = {
            "goal": "awareness",
            "style_signals": ["authentic"] if ("真实" in raw or "不要太硬广" in raw) else [],
            "creator_archetypes": [],
        }
        keyword_clusters = {"core": [], "benefit": [], "scenario": [], "creator": []}

        if "洁面" in raw or "洗面奶" in raw or "cleanser" in raw_l:
            product["category_labels"] = ["cleanser", "skincare"]
            keyword_clusters["core"] = ["cleanser", "face wash"]
            keyword_clusters["benefit"] = ["gentle cleanser"]
            marketing["creator_archetypes"] = ["skincare_creator"]
        if "口腔" in raw or "漱口水" in raw or "mouthwash" in raw_l:
            product["category_labels"] = ["oral care"]
            keyword_clusters["core"] = ["mouthwash", "oral care"]
            marketing["creator_archetypes"] = ["oral_care_creator"]
        if "真实" in raw or "不要太硬广" in raw:
            keyword_clusters["creator"] = ["authentic review", "lifestyle creator"]

        return {
            "product": product,
            "constraints": constraints,
            "marketing": marketing,
            "keyword_clusters": keyword_clusters,
            "uncertainties": [],
        }
