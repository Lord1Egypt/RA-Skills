import json
from typing import List, Optional
from datetime import datetime, timezone

# Assumes ContentOutline, TaskReferenceFile, SchemaBlock are imported from models.py
# in the caller.  schema_engine functions accept duck-typed outline / trf objects.

SCHEMA_SELECTION_MATRIX = {
    # Always generated
    "always": ["Article", "BreadcrumbList", "WebPage"],

    # Generated based on content type flags in the outline
    "if_faq_block_present":       ["FAQPage"],
    "if_how_to_steps_present":    ["HowToArticle"],
    "if_comparison_table_present": ["ItemList"],
    "if_definition_answer":       ["DefinedTerm"],
    "if_review_content":          ["Review", "AggregateRating"],
    "if_product_mentioned":       ["Product"],
    "if_event_content":           ["Event"],

    # Generated if competitors DON'T use it (gap opportunity)
    "if_schema_gap": ["SpeakableSpecification", "DefinedTerm"],
}


def select_schema_types(outline, trf=None) -> List[str]:
    """
    Selects schema types based on the generated outline content and competitive
    gaps identified in the TRF.  `trf` may be None on new-post runs.
    """
    types = list(SCHEMA_SELECTION_MATRIX["always"])

    for section in outline.sections:
        if section.content_type == "faq_block":
            types.append("FAQPage")
        elif section.content_type == "how_to_steps":
            types.append("HowToArticle")
        elif section.content_type == "comparison":
            types.append("ItemList")

    if outline.answer_block.answer_type == "definition":
        types.append("DefinedTerm")

    # Gap schema: add types competitors don't use
    competitor_types = set(trf.competitor_schema_types_combined) if trf else set()
    if "SpeakableSpecification" not in competitor_types:
        types.append("SpeakableSpecification")

    return list(dict.fromkeys(types))  # deduplicate, preserve order


def count_schema_entities(obj, count: int = 0) -> int:
    """Recursively counts distinct @type nodes in a parsed JSON-LD object."""
    if isinstance(obj, dict):
        if "@type" in obj:
            count += 1
        for v in obj.values():
            count = count_schema_entities(v, count)
    elif isinstance(obj, list):
        for item in obj:
            count = count_schema_entities(item, count)
    return count


def validate_and_count_schema(json_ld_string: str) -> dict:
    """
    Validates that JSON-LD is parseable and counts distinct @type entity nodes.
    Returns a dict matching the SchemaBlock model.
    Raises ValueError on malformed JSON.
    """
    try:
        parsed = json.loads(json_ld_string)
    except json.JSONDecodeError as e:
        raise ValueError(f"Schema JSON-LD is not valid JSON: {e}")

    entity_count = count_schema_entities(parsed)
    schema_type  = parsed.get("@type", "Unknown")

    return {
        "schema_type":  schema_type,
        "json_ld":      json_ld_string,
        "entity_count": entity_count,
    }


ANSWER_BLOCK_GENERATION_RULES = """
ANSWER BLOCK GENERATION RULES:

LENGTH: 40-60 words. This is not a suggestion.
  - Under 40: too thin to trigger featured snippet
  - Over 60: may be truncated by answer engines in ways that lose context

STRUCTURE by answer_type:
  "definition" → "{Term} is {direct definition}. {Key characteristic}. {Use case or why it matters}."
  "process"    → "To {achieve outcome}, {action 1}, then {action 2}, and finally {action 3}.
                  This typically takes {timeframe} and requires {prerequisites}."
  "list"       → "{Topic} includes: {item 1}, {item 2}, {item 3}, and {item 4}.
                  Each {characteristic that makes them relevant}."
  "yes_no"     → "Yes/No, {topic} {direct answer}. {Reason}. {Important caveat or condition}."
  "table"      → Do NOT use table format in the answer block itself.
                 Use prose summary + table below the answer block.

FORBIDDEN in answer blocks:
  - "In this article we will..."
  - "Great question..."
  - "It depends..."
  - "According to some experts..."
  - Passive voice as the opening construction
  - Hedging qualifiers as the first word ("Generally", "Typically", "Often")

REQUIRED in answer blocks:
  - Primary keyword in first 10 words
  - At least one specific, concrete detail (number, name, timeframe)
  - Complete thought — answer engines may serve this alone

HTML WRAPPER:
  <div class="answer-block" itemscope itemtype="https://schema.org/Answer">
    <span itemprop="text">{answer_text}</span>
  </div>
"""

CONTENT_FORMAT_RULES = {
    "definition_query": {
        "answer_block_type": "definition",
        "open_with": "answer_block + DefinedTerm schema",
        "follow_with": ["prose_explanation", "use_cases_list", "faq_block"],
        "schema_priority": ["Article", "DefinedTerm", "FAQPage", "WebPage", "BreadcrumbList"],
    },
    "process_query": {
        "answer_block_type": "process",
        "open_with": "answer_block (summary of process)",
        "follow_with": ["how_to_steps_numbered", "pro_tips_list", "faq_block"],
        "schema_priority": ["HowToArticle", "Article", "FAQPage", "WebPage", "BreadcrumbList"],
    },
    "comparison_query": {
        "answer_block_type": "list",
        "open_with": "answer_block (verdict + key differentiator)",
        "follow_with": ["comparison_table", "detailed_prose_per_option", "faq_block"],
        "schema_priority": ["ItemList", "Article", "FAQPage", "WebPage", "BreadcrumbList"],
    },
    "best_of_query": {
        "answer_block_type": "list",
        "open_with": "answer_block (top 3 in prose)",
        "follow_with": ["numbered_list_with_descriptions", "comparison_table", "faq_block"],
        "schema_priority": ["ItemList", "Article", "FAQPage", "WebPage", "BreadcrumbList"],
    },
    "troubleshooting_query": {
        "answer_block_type": "process",
        "open_with": "answer_block (root cause + first fix step)",
        "follow_with": ["how_to_steps", "cause_list", "faq_block"],
        "schema_priority": ["HowToArticle", "Article", "FAQPage", "WebPage", "BreadcrumbList"],
    },
}


def build_graph_schema(
    article:       dict,
    breadcrumb:    dict,
    canonical_url: str,
    config:        dict,
    faq:           dict = None,
    how_to:        dict = None,
    item_list:     dict = None,
    defined_term:  dict = None,
) -> str:
    """
    Assembles all schema blocks into a single @graph JSON-LD object.
    Uses @id strings to cross-reference nodes explicitly.

    NOTE: Prefer calling generate_dynamic_schema() from daily_worker.py — it
    selects the correct optional blocks automatically based on outline content
    and calls this function as its final assembly step.
    """
    page_id    = f"{canonical_url}#webpage"
    article_id = f"{canonical_url}#article"
    author_id  = f"{config['BRAND_ENTITY_URL']}#author"
    org_id     = f"{config['BRAND_ENTITY_URL']}#organization"

    graph = []

    # --- WebPage (with SpeakableSpecification) ---
    graph.append({
        "@type": "WebPage",
        "@id":   page_id,
        "url":   canonical_url,
        "name":  article.get("headline", ""),
        "description": article.get("description", ""),
        "inLanguage":  "en-US",
        "isPartOf":    {"@id": f"{config['BRAND_ENTITY_URL']}#website"},
        "primaryImageOfPage": article.get("image", {}),
        "speakable": {
            "@type":       "SpeakableSpecification",
            "cssSelector": [".answer-block", "h1", ".speakable-summary"]
        },
        "breadcrumb": {"@id": f"{canonical_url}#breadcrumb"},
    })

    # --- Article ---
    graph.append({
        "@type":       "Article",
        "@id":         article_id,
        "isPartOf":    {"@id": page_id},
        "headline":    article.get("headline", ""),
        "description": article.get("description", ""),
        "datePublished": article.get("datePublished", ""),
        "dateModified":  article.get("dateModified", ""),
        "author":      {"@id": author_id},
        "publisher":   {"@id": org_id},
        "mainEntityOfPage": {"@id": page_id},
        "keywords":    article.get("keywords", ""),
        "about":       article.get("about", {}),
        "mentions":    article.get("mentions", []),
        "image":       article.get("image", {}),
    })

    # --- Author Person entity ---
    graph.append({
        "@type": "Person",
        "@id":   author_id,
        "name":  config.get("BRAND_ENTITY_NAME", ""),
        "url":   config.get("BRAND_ENTITY_URL", ""),
        "sameAs": [
            config.get("SCHEMA_AUTHOR_TWITTER",  ""),
            config.get("SCHEMA_AUTHOR_LINKEDIN", ""),
        ]
    })

    # --- Publisher Organization entity ---
    graph.append({
        "@type": "Organization",
        "@id":   org_id,
        "name":  config.get("SCHEMA_SITE_NAME") or config.get("BRAND_ENTITY_NAME", ""),
        "url":   config.get("BRAND_ENTITY_URL", ""),
        "logo":  {
            "@type": "ImageObject",
            "url":   config.get("SCHEMA_LOGO_URL", "")
        }
    })

    # --- BreadcrumbList ---
    graph.append({**breadcrumb, "@id": f"{canonical_url}#breadcrumb"})

    # --- FAQPage ---
    if faq:
        graph.append({
            **faq,
            "@id": f"{canonical_url}#faq",
            "mainEntityOfPage": {"@id": page_id},
        })

    # --- HowTo ---
    if how_to:
        graph.append({
            **how_to,
            "@id": f"{canonical_url}#howto",
            "mainEntityOfPage": {"@id": page_id},
        })

    # --- ItemList ---
    if item_list:
        graph.append({
            **item_list,
            "@id": f"{canonical_url}#itemlist",
        })

    # --- DefinedTerm ---
    if defined_term:
        graph.append({
            **defined_term,
            "@id": f"{canonical_url}#definedterm",
        })

    schema_object = {
        "@context": "https://schema.org",
        "@graph":   graph,
    }

    return json.dumps(schema_object, indent=2, ensure_ascii=False)


def generate_dynamic_schema(outline, trf, canonical_url: str, config: dict) -> str:
    """
    Master integration function — the correct entry point from daily_worker.py.

    Maps a Pydantic ContentOutline model into dynamic dicts, selects the right
    optional schema blocks (FAQPage, HowToArticle, ItemList, DefinedTerm) based
    on outline content and competitive gaps, builds the unified @graph JSON-LD,
    and validates/counts entities before returning the final JSON string.
    """
    selected_types = select_schema_types(outline, trf)

    # 1. Base Article Data
    article_data = {
        "headline":      outline.page_title,
        "description":   outline.meta_description,
        "datePublished": datetime.now(timezone.utc).isoformat(),
        "dateModified":  datetime.now(timezone.utc).isoformat(),
        "keywords": f"{outline.primary_keyword}, {', '.join(outline.secondary_keywords)}"
    }

    # 2. Base Breadcrumb Data
    breadcrumb_data = {
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home",
             "item": config.get("WP_URL", "")},
            {"@type": "ListItem", "position": 2, "name": outline.page_title,
             "item": canonical_url},
        ]
    }

    # 3. Conditional Blocks
    faq_data         = None
    how_to_data      = None
    item_list_data   = None
    defined_term_data = None

    if "FAQPage" in selected_types:
        faq_data = {
            "@type":      "FAQPage",
            "mainEntity": []  # FAQ Q&A pairs injected downstream via chunked pipeline
        }

    if "DefinedTerm" in selected_types and outline.answer_block.answer_type == "definition":
        defined_term_data = {
            "@type":       "DefinedTerm",
            "name":        outline.primary_keyword,
            "description": outline.answer_block.answer_text,
            "inDefinedTermSet": {
                "@type": "DefinedTermSet",
                "name":  config.get("TARGET_NICHE", "Glossary"),
                "url":   f"{config.get('BRAND_ENTITY_URL', '').rstrip('/')}/glossary"
            }
        }

    if "ItemList" in selected_types:
        item_list_data = {
            "@type":           "ItemList",
            "name":            f"Top {outline.primary_keyword}",
            "itemListElement": []
        }

    if "HowToArticle" in selected_types or "HowTo" in selected_types:
        how_to_data = {
            "@type": "HowTo",
            "name":  outline.page_title,
            "step":  []
        }

    # 4. Build Unified JSON-LD String
    raw_json_ld = build_graph_schema(
        article=article_data,
        breadcrumb=breadcrumb_data,
        canonical_url=canonical_url,
        config=config,
        faq=faq_data,
        how_to=how_to_data,
        item_list=item_list_data,
        defined_term=defined_term_data
    )

    # 5. Gatekeeper Validation
    validated_block = validate_and_count_schema(raw_json_ld)

    return validated_block["json_ld"]
 