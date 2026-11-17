# Subtitle templates

Vibbit dynamic subtitle templates are temporarily unavailable. This Skill does not expose their discovery, selection, or application. Do not submit `template_type=1` or `subtitle_template_configs`, even when a template ID is known.

Explain the limitation when requested and retain the requested style. Offer ordinary subtitles or local subtitle production when alternatives are useful, stating the visual difference instead of silently replacing the requirement.

Ordinary captions remain available through [subtitle addition](../capabilities/processing/subtitle-addition.md) or translation's `subtitle_enabled`. Use [ordinary packaging templates](packaging-templates.md) with `template_type=0` when needed.

Local subtitle styles can use actual [render templates](render-templates.md). A generic caption request follows the ordinary subtitle path; do not report local styling as an applied Vibbit dynamic subtitle template.
