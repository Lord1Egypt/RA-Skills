# Changelog

## 1.1.0 (2026-05-02)

### Features
- **Volcengine video generation support**: Added full support for Volcengine Ark video generation API (`doubao-seedance-2-0-260128`)
- **Unified video provider**: Video and image generation now both use `VOLC_API_KEY`
- **Provider-aware VideoAPIClient**: Automatically switches between Kling and Volcengine API formats
- **Updated DeepSeek models**: Default text model changed from `deepseek-chat` to `deepseek-v4-pro` (old names deprecated 2026-07-24)

### API Changes
- Video endpoint: `POST /contents/generations/tasks` (Volcengine)
- Video query: `GET /contents/generations/tasks/{task_id}` (Volcengine)
- Image references use `role: "reference_image"` for Volcengine

## 1.0.0 (2026-05-01)

### Features
- Complete rewrite from toonvid with new architecture
- **Quick Mode**: Single-command interactive workflow for beginners
- **Craft Mode**: Stage-by-stage professional control
- **Friendly onboarding**: Guided API key setup with provider-specific instructions
- **Style anchor mechanism**: Style sample confirmation before batch generation
- **Character consistency**: Four-view reference sheets with seed locking
- **Dependency tracking**: Automatic stale file detection when upstream changes
- **Cross-platform**: Pure Python scripts, no BSD/GNU tool dependencies
- **Unified API client**: Single client for image/video/TTS with retry logic
- **Post-processing pipeline**: Video concatenation + audio mixing + subtitle burn-in
- **Quality gates**: Automated consistency checks across all stages
- **Preset styles**: 20+ built-in art styles for quick selection

### Security
- No hardcoded API tokens
- Environment variable support with `${ENV_VAR}` syntax
- No secrets in project files

### Architecture
- Modular script design with shared utilities
- Template-based project initialization
- Provider-agnostic API layer
- Sentence-level subtitle generation (not word-level)
