# Extraction Schema (Canonical)

Use internally and when returning structured JSON/YAML.

```json
{
  "dish_name": "string",
  "dish_name_aliases": ["string"],
  "cuisine_region": "川菜|粤菜|湘菜|鲁菜|苏菜|浙菜|闽菜|徽菜|家常菜|融合|unknown",
  "category": "热菜|凉菜|汤羹|主食|小吃|早餐|甜品|酱料|unknown",
  "servings": "number|string|unknown",
  "difficulty": "easy|medium|hard|unknown",
  "times": {
    "prep_minutes": "number|unknown",
    "cook_minutes": "number|unknown",
    "total_minutes": "number|unknown",
    "estimated": "boolean"
  },
  "ingredients": [
    {
      "name": "string",
      "amount": "string",
      "unit": "string",
      "prep": "string",
      "optional": "boolean",
      "substitutions": ["string"]
    }
  ],
  "seasonings": [
    {
      "name": "string",
      "amount": "string",
      "unit": "string",
      "notes": "string"
    }
  ],
  "steps": [
    {
      "idx": 1,
      "instruction": "string",
      "heat": "小火|中小火|中火|中大火|大火|unknown",
      "time_minutes": "number|unknown",
      "visual_cues": ["string"],
      "warnings": ["string"]
    }
  ],
  "tips": ["string"],
  "common_failures": ["string"],
  "variants": [
    {
      "name": "string",
      "difference": "string",
      "source_type": "structured|video|social"
    }
  ],
  "nutrition_notes": ["string"],
  "confidence": "high|medium|low",
  "source_urls": ["string"],
  "source_titles": ["string"],
  "source_type": ["structured|video|social"],
  "traceability_notes": ["string"]
}
```
