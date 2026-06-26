# Source Reference — Ultimate Skills Finder

## Primary Registries

### ClawHub (clawhub.ai)
- **Type:** Official OpenClaw registry
- **Scale:** ~20,000 skills
- **CLI:** `clawhub search/install/update`
- **Strength:** Official, versioned, vector search

### SkillsMP (skillsmp.com)
- **Type:** Community aggregator from GitHub
- **Scale:** 1,000,000+ skills indexed
- **API:** REST API at `/api/v1/skills`
- **Strength:** Largest catalog, REST API
- **Note:** Raw/uncrated — minimum 2 stars filter

## GitHub Curated Collections

### VoltAgent/awesome-openclaw-skills
- **Scale:** 5,200+ curated skills
- **URL:** https://github.com/VoltAgent/awesome-openclaw-skills
- **Note:** Spam-filtered, categorized README

### LeoYeAI/openclaw-master-skills
- **Scale:** 560+ curated skills
- **URL:** https://github.com/LeoYeAI/openclaw-master-skills
- **Note:** Bilingual (EN/ZH), weekly updated

## Security

### Gen Digital (ai.gendigital.com)
- **Purpose:** Skill security scanning
- **API:** POST `/api/scan/lookup` with `{"skillUrl": "..."}`
- **Response:** `status: "done"` + `severity: "SAFE"|"WARNING"|"DANGEROUS"|"MALICIOUS"`
- **Note:** Free, no API key required
