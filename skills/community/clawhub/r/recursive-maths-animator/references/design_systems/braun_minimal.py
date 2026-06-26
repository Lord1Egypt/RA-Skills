"""
Braun Minimal Aesthetic for Manim Animations
============================================

Inspired by Dieter Rams and the Braun design philosophy.

- "Less but better"
- Warm light grays, systematic spacing
- Tiny functional accents
- Form follows function
- Quiet confidence, no visual noise

Color Palette:
- BACKGROUND: #F7F5F2 (warm light gray)
- CONTAINER: #FFFFFF (pure white)
- BORDER: #E2DFDA (subtle warm border)
- GRID: #EDEAE5 (barely-there dot grid)
- TEXT_PRIMARY: #2C2C2C (soft black)
- TEXT_SECONDARY: #8A8680 (warm gray)
- ACCENT: #C75B3A (Braun orange — muted, functional)
- GREEN: #5A8F6E (functional green)

Typography (Work Sans):
- Headings: 18px, Semi-Bold, clean proportions
- Body: 13px, Regular, 1.45 line-height
- Metadata: 10px, Medium, uppercase

Motion:
- EASE_BRAUN_LINEAR: calm, deliberate, almost mechanical precision

Usage:
    from braun_minimal import BraunScene

    class MyScene(BraunScene):
        def construct(self):
            self.setup_braun_background()
            # Your content here
"""

from manim import *
from manim_voiceover import VoiceoverScene

FONT_PRIMARY = "Work Sans"


# =============================================================================
# COLOR PALETTE
# =============================================================================

class BraunColors:
    """Braun Minimal color palette — warm, systematic, functional."""
    # Background
    BACKGROUND = "#F7F5F2"           # Warm light gray
    VIGNETTE_CENTER = "#F7F5F2"
    VIGNETTE_EDGE = "#EFEDE8"

    # Containers
    CONTAINER = "#FFFFFF"             # Pure white
    BORDER = "#E2DFDA"              # Subtle warm border
    GRID = "#EDEAE5"                # Barely-there dot grid

    # Text
    TEXT_PRIMARY = "#2C2C2C"          # Soft black
    TEXT_SECONDARY = "#8A8680"       # Warm gray

    # Accents — Braun orange and functional green
    ORANGE = "#C75B3A"               # Muted Braun orange
    GREEN = "#5A8F6E"                # Functional green
    BLUE = "#4A7C9B"                 # Cool functional blue

    # System
    ALARM = "#B04040"                # Rose alarm (emergency)


# =============================================================================
# TYPOGRAPHY
# =============================================================================

class BraunTypography:
    """Typography using Work Sans — clean, readable, systematic."""

    FONT_FAMILY = FONT_PRIMARY

    SIZE_HEADING = 0.18
    SIZE_BODY = 0.13
    SIZE_METADATA = 0.10
    SIZE_CODE = 0.11

    @classmethod
    def heading(cls, text, color=BraunColors.TEXT_PRIMARY):
        return Text(
            text,
            font=cls.FONT_FAMILY,
            font_size=cls.SIZE_HEADING * 100,
            color=color,
            weight=SEMIBOLD,
        )

    @classmethod
    def body(cls, text, color=BraunColors.TEXT_SECONDARY):
        return Text(
            text,
            font=cls.FONT_FAMILY,
            font_size=cls.SIZE_BODY * 100,
            color=color
        )

    @classmethod
    def metadata(cls, text, color=BraunColors.TEXT_SECONDARY):
        return Text(
            text.upper(),
            font=cls.FONT_FAMILY,
            font_size=cls.SIZE_METADATA * 100,
            color=color,
            weight=MEDIUM
        )

    @classmethod
    def code(cls, text, color=BraunColors.TEXT_PRIMARY):
        return Text(
            text,
            font=cls.FONT_FAMILY,
            font_size=cls.SIZE_CODE * 100,
            color=color,
            weight=MEDIUM
        )


# =============================================================================
# MOTION — Braun linear: calm, deliberate, mechanical precision
# =============================================================================

def EASE_BRAUN_LINEAR(t: float) -> float:
    """
    Braun linear easing: calm, deliberate motion.
    Very slight ease-out — almost mechanical, no drama.
    cubic-bezier(0.1, 0.0, 0.2, 1.0) approximation.
    """
    return t * t * (3 - 2 * t)  # smoothstep — gentle, controlled


# =============================================================================
# BACKGROUND GENERATORS
# =============================================================================

class BraunBackground:
    """Background generators for Braun Minimal aesthetic."""

    @staticmethod
    def dot_grid(width, height, spacing=0.6, dot_color=BraunColors.GRID,
                 dot_radius=0.012, fade_edges=True):
        """Very sparse, subtle dot grid — Braun hides structure."""
        dots = VGroup()
        cols = int(width / spacing) + 2
        rows = int(height / spacing) + 2
        start_x = -width / 2
        start_y = -height / 2

        for row in range(rows):
            for col in range(cols):
                x = start_x + col * spacing
                y = start_y + row * spacing
                if abs(x) > width / 2 + spacing or abs(y) > height / 2 + spacing:
                    continue
                dot = Circle(radius=dot_radius, fill_color=dot_color, fill_opacity=1)
                dot.move_to([x, y, 0])
                if fade_edges:
                    dist_from_center = np.sqrt(x * x + y * y)
                    max_dist = np.sqrt((width / 2) ** 2 + (height / 2) ** 2)
                    fade_start = max_dist * 0.55
                    if dist_from_center > fade_start:
                        opacity = 1 - (dist_from_center - fade_start) / (max_dist - fade_start)
                        dot.set_fill(opacity=max(0, opacity))
                dots.add(dot)
        return dots

    @staticmethod
    def vignette(width, height, center_color=BraunColors.VIGNETTE_CENTER,
                 edge_color=BraunColors.VIGNETTE_EDGE):
        vignette = Rectangle(
            width=width,
            height=height,
            fill_color=center_color,
            fill_opacity=1,
            stroke_width=0
        )
        return vignette


# =============================================================================
# CONTAINER COMPONENTS
# =============================================================================

class BraunContainers:
    """Container components — minimal, warm, almost invisible borders."""

    @staticmethod
    def bezel(width, height, corner_radius=0.08, fill_color=BraunColors.CONTAINER,
              border_color=BraunColors.BORDER, stroke_width=0.5, shadow=False):
        """
        Subtle container — thin 0.5px borders, slight rounding,
        barely perceptible.
        """
        container = RoundedRectangle(
            corner_radius=corner_radius,
            width=width,
            height=height,
            fill_color=fill_color,
            fill_opacity=1,
            stroke_color=border_color,
            stroke_width=stroke_width
        )
        if shadow:
            shadow_rect = RoundedRectangle(
                corner_radius=corner_radius,
                width=width,
                height=height,
                fill_color="#000000",
                fill_opacity=0.04,
                stroke_width=0
            )
            shadow_rect.shift(DOWN * 0.03 + RIGHT * 0.02)
            shadow_rect.set_z_index(-1)
            return VGroup(shadow_rect, container)
        return container

    @staticmethod
    def pill_label(text, bg_color=BraunColors.CONTAINER, text_color=BraunColors.TEXT_SECONDARY,
                   border_color=BraunColors.BORDER):
        label = Text(text, font=FONT_PRIMARY, font_size=12, color=text_color)
        pill = RoundedRectangle(
            corner_radius=0.15,
            width=label.width + 0.3,
            height=label.height + 0.15,
            fill_color=bg_color,
            fill_opacity=1,
            stroke_color=border_color,
            stroke_width=0.5
        )
        label.move_to(pill.get_center())
        return VGroup(pill, label)


# =============================================================================
# BASE SCENE CLASS
# =============================================================================

class BraunScene(VoiceoverScene):
    """
    Base scene class with Braun Minimal Aesthetic pre-configured.
    """

    def setup_braun_background(self, show_grid=True, show_vignette=True):
        """Setup the Braun Minimal background."""
        self.camera.background_color = BraunColors.BACKGROUND
        if show_grid:
            grid = BraunBackground.dot_grid(
                self.camera.frame_width,
                self.camera.frame_height,
                spacing=0.6,
                dot_color=BraunColors.GRID,
                fade_edges=True
            )
            self.add(grid)
        if show_vignette:
            vignette = BraunBackground.vignette(
                self.camera.frame_width * 1.2,
                self.camera.frame_height * 1.2
            )
            self.add(vignette)

    def make_braun_subtitle(self, text, position=DOWN * 2.5):
        subtitle = Text(
            text,
            font=FONT_PRIMARY,
            font_size=16,
            color=BraunColors.TEXT_SECONDARY,
            weight=MEDIUM
        )
        subtitle.move_to(position)
        return subtitle

    def make_heading(self, text, position=UP * 3):
        heading = BraunTypography.heading(text)
        heading.move_to(position)
        return heading

    def make_metadata_label(self, text, position):
        label = BraunTypography.metadata(text)
        label.move_to(position)
        return label


# =============================================================================
# EXAMPLE USAGE
# =============================================================================

class ExampleBraunScene(BraunScene):
    """Example scene demonstrating Braun Minimal Aesthetic."""

    def construct(self):
        self.setup_braun_background()
        heading = self.make_heading("Braun Minimal")
        container = BraunContainers.bezel(4, 2.5, corner_radius=0.08)
        container.move_to(ORIGIN)
        content = Text(
            "Less but better\nSystematic spacing\nQuiet confidence",
            font=FONT_PRIMARY,
            font_size=14,
            color=BraunColors.TEXT_SECONDARY,
            line_spacing=1.45
        )
        content.move_to(container.get_center())
        pill = BraunContainers.pill_label("v1.0", position=RIGHT * 3 + UP * 2)
        self.play(
            FadeIn(heading, run_time=0.6),
            FadeIn(container, run_time=0.6, rate_func=EASE_BRAUN_LINEAR),
            lag_ratio=0.2
        )
        self.play(
            FadeIn(content, run_time=0.5),
            FadeIn(pill, run_time=0.5),
            lag_ratio=0.1
        )
        self.wait(1)
