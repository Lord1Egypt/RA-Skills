# Design DNA Schema

Three-dimensional design profile:
- **design_system** — measurable tokens
- **design_style** — qualitative perception
- **visual_effects** — special rendering (Canvas, WebGL, 3D, particles, shaders, scroll effects, cursor effects, SVG animation, glassmorphism)

Every field below must appear in the final JSON output.

## Top-Level Structure

### `meta`
- `name`
- `description`
- `source_references`
- `created_at`

### `design_system`

#### `design_system.color`
- `palette_type` — "monochromatic", "complementary", "analogous", "triadic", "split-complementary"
- `primary.hex`, `primary.role`
- `secondary.hex`, `secondary.role`
- `accent.hex`, `accent.role`
- `neutral.scale`, `neutral.usage`
- `semantic.success`, `semantic.warning`, `semantic.error`, `semantic.info`
- `surface.background`, `surface.card`, `surface.elevated`
- `contrast_strategy` — "high contrast", "subtle layers", "dark-on-light dominant"

#### `design_system.typography`
- `type_scale.display/heading_1/heading_2/heading_3/body/body_small/caption/overline` — size, weight, line_height, tracking
- `font_families.heading`, `font_families.body`, `font_families.mono`
- `font_style_notes`

#### `design_system.spacing`
- `base_unit`
- `scale`
- `content_density` — "compact", "comfortable", "spacious"
- `section_rhythm`

#### `design_system.layout`
- `grid_system`, `max_content_width`, `columns`, `gutter`
- `breakpoints`
- `alignment_tendency` — "strict grid", "centered", "asymmetric"

#### `design_system.shape`
- `border_radius.small/medium/large/pill`
- `border_usage`, `divider_style`

#### `design_system.elevation`
- `shadow_style`
- `levels.low/medium/high`
- `depth_cues`

#### `design_system.iconography`
- `style`, `stroke_weight`, `size_scale`, `preferred_set`

#### `design_system.motion`
- `easing`
- `duration_scale.micro/normal/macro`
- `entrance_pattern`, `exit_pattern`, `philosophy`

#### `design_system.components`
- `button_style`, `input_style`, `card_style`
- `navigation_pattern`, `modal_style`, `list_style`
- `component_notes`

### `design_style`

#### `design_style.aesthetic`
- `mood`, `visual_metaphor`, `era_influence`, `genre`
- `personality_traits`, `adjectives`

#### `design_style.visual_language`
- `complexity`, `ornamentation`, `whitespace_usage`
- `visual_weight_distribution`, `focal_strategy`
- `contrast_level`, `texture_usage`

#### `design_style.composition`
- `hierarchy_method`, `balance_type`, `flow_direction`
- `grouping_strategy`, `negative_space_role`

#### `design_style.imagery`
- `photo_treatment`, `illustration_style`
- `graphic_elements`, `pattern_usage`, `image_shape`

#### `design_style.interaction_feel`
- `feedback_style`, `hover_behavior`, `transition_personality`
- `loading_style`, `microinteraction_density`

#### `design_style.brand_voice_in_ui`
- `tone`, `formality`, `cta_style`
- `empty_state_approach`, `error_tone`

### `visual_effects`

#### `visual_effects.overview`
- `effect_intensity` — "none", "subtle", "moderate", "heavy"
- `performance_tier` — "lightweight", "medium", "heavy"
- `fallback_strategy`, `primary_technology`

#### Effect categories (each has `enabled`, `type`, `description`, `technology`, `params`):
- `background_effects`
- `particle_systems`
- `3d_elements`
- `shader_effects`
- `scroll_effects.parallax`, `scroll_effects.scroll_triggered_animations`, `scroll_effects.scroll_morphing`
- `text_effects`
- `cursor_effects`
- `image_effects`
- `glassmorphism_neumorphism`
- `canvas_drawings`
- `svg_animations`
- `composite_notes` — free text for layered effects, ambiguity, performance notes
