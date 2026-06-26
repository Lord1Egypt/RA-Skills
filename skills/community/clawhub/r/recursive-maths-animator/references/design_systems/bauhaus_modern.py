"""
Bauhaus Modern Aesthetic for Manim Animations
===============================================

Inspired by the Bauhaus school — Herbert Bayer, László Moholy-Nagy.

- Geometric abstraction
- Primary colors (red, yellow, blue)
- Asymmetric balance
- Functional art — form follows function
- Bold shapes, minimal ornament

Color Palette:
- BACKGROUND: #F4F1EA (warm off-white — canvas)
- CONTAINER: #FFFFFF (paper)
- BORDER: #D4CFC5 (warm gray)
- GRID: #E8E3DA (subtle dot grid)
- TEXT_PRIMARY: #1A1A1A (charcoal)
- TEXT_SECONDARY: #5C5C5C (slate)
- RED: #E63946 (Bauhaus red)
- YELLOW: #F4A261 (Bauhaus yellow — muted)
- BLUE: #264653 (Bauhaus blue — deep)

Typography (Space Grotesk):
- Headings: 18px, Bold, geometric proportions
- Body: 13px, Regular, 1.4 line-height
- Metadata: 10px, Medium, uppercase

Motion:
- EASE_BAUHAUS_SPRING: lively, geometric, slightly playful

Usage:
    from bauhaus_modern import BauhausScene

    class MyScene(BauhausScene):
        def construct(self):
            self.setup_bauhaus_background()
            # Your content here
"""

from manim import *
from manim_voiceover import VoiceoverScene

FONT_PRIMARY = "Space Grotesk"
FONT_MONO = "Space Mono"


# =============================================================================
# COLOR PALETTE
# =============================================================================

class BauhausColors:
    """Bauhaus Modern color palette — primary, geometric, functional."""
    # Background
    BACKGROUND = "#F4F1EA"           # Warm off-white canvas
    VIGNETTE_CENTER = "#F4F1EA"
    VIGNETTE_EDGE = "#EDE9E0"

    # Containers
    CONTAINER = "#FFFFFF"             # Paper white
    BORDER = "#D4CFC5"              # Warm gray
    GRID = "#E8E3DA"                # Subtle dot grid

    # Text
    TEXT_PRIMARY = "#1A1A1A"          # Charcoal
    TEXT_SECONDARY = "#5C5C5C"       # Slate

    # Primary accents — Bauhaus red/yellow/blue
    RED = "#E63946"                   # Primary red
    YELLOW = "#F4A261"                # Warm yellow
    BLUE = "#264653"                  # Deep blue

    # Secondary accents
    GREEN = "#2A9D8F"                 # Teal green
    ORANGE = "#E76F51"              # Burnt orange


# =============================================================================
# TYPOGRAPHY
# =============================================================================

class BauhausTypography:
    """Typography using Space Grotesk and Space Mono."""

    FONT_FAMILY = FONT_PRIMARY
    FONT_FAMILY_MONO = FONT_MONO

    SIZE_HEADING = 0.18
    SIZE_BODY = 0.13
    SIZE_METADATA = 0.10
    SIZE_CODE = 0.11

    @classmethod
    def heading(cls, text, color=BauhausColors.TEXT_PRIMARY):
        return Text(
            text,
            font=cls.FONT_FAMILY,
            font_size=cls.SIZE_HEADING * 100,
            color=color,
            weight=BOLD,
        )

    @classmethod
    def body(cls, text, color=BauhausColors.TEXT_SECONDARY):
        return Text(
            text,
            font=cls.FONT_FAMILY,
            font_size=cls.SIZE_BODY * 100,
            color=color
        )

    @classmethod
    def metadata(cls, text, color=BauhausColors.TEXT_SECONDARY):
        return Text(
            text.upper(),
            font=cls.FONT_FAMILY,
            font_size=cls.SIZE_METADATA * 100,
            color=color,
            weight=MEDIUM
        )

    @classmethod
    def code(cls, text, color=BauhausColors.TEXT_PRIMARY):
        return Text(
            text,
            font=cls.FONT_FAMILY_MONO,
            font_size=cls.SIZE_CODE * 100,
            color=color,
            weight=MEDIUM
        )


# =============================================================================
# MOTION — Bauhaus spring: lively, slightly playful, geometric
# =============================================================================

def EASE_BAUHAUS_SPRING(t: float) -> float:
    """
    Bauhaus spring easing: lively, geometric motion with slight overshoot.
    cubic-bezier(0.34, 1.56, 0.64, 1.0) approximation.
    """
    # Springy ease-out with a tiny overshoot
    return 1 + 0.05 * np.sin(t * np.pi * 2.5) * (1 - t) ** 2 - (1 - t) ** 3


# =============================================================================
# BACKGROUND GENERATORS
# =============================================================================

class BauhausBackground:
    """Background generators for Bauhaus Modern aesthetic."""

    @staticmethod
    def dot_grid(width, height, spacing=0.45, dot_color=BauhausColors.GRID,
                 dot_radius=0.018, fade_edges=True):
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
                    fade_start = max_dist * 0.6
                    if dist_from_center > fade_start:
                        opacity = 1 - (dist_from_center - fade_start) / (max_dist - fade_start)
                        dot.set_fill(opacity=max(0, opacity))
                dots.add(dot)
        return dots

    @staticmethod
    def vignette(width, height, center_color=BauhausColors.VIGNETTE_CENTER,
                 edge_color=BauhausColors.VIGNETTE_EDGE):
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

class BauhausContainers:
    """Container components — Bauhaus favors sharp geometry + bold color blocks."""

    @staticmethod
    def bezel(width, height, corner_radius=0.0, fill_color=BauhausColors.CONTAINER,
              border_color=BauhausColors.BORDER, stroke_width=1, shadow=False):
        """Sharp-cornered container — Bauhaus eschews excessive rounding."""
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
                fill_opacity=0.08,
                stroke_width=0
            )
            shadow_rect.shift(DOWN * 0.05 + RIGHT * 0.03)
            shadow_rect.set_z_index(-1)
            return VGroup(shadow_rect, container)
        return container

    @staticmethod
    def color_block(width, height, color=BauhausColors.RED, corner_radius=0.0):
        """Bold colored rectangle — a Bauhaus staple."""
        return RoundedRectangle(
            corner_radius=corner_radius,
            width=width,
            height=height,
            fill_color=color,
            fill_opacity=1,
            stroke_width=0
        )

    @staticmethod
    def pill_label(text, bg_color=BauhausColors.CONTAINER, text_color=BauhausColors.TEXT_SECONDARY,
                   border_color=BauhausColors.BORDER):
        label = Text(text, font=FONT_PRIMARY, font_size=12, color=text_color)
        pill = RoundedRectangle(
            corner_radius=0.12,
            width=label.width + 0.3,
            height=label.height + 0.15,
            fill_color=bg_color,
            fill_opacity=1,
            stroke_color=border_color,
            stroke_width=1
        )
        label.move_to(pill.get_center())
        return VGroup(pill, label)


# =============================================================================
# BASE SCENE CLASS
# =============================================================================

class BauhausScene(VoiceoverScene):
    """
    Base scene class with Bauhaus Modern Aesthetic pre-configured.
    """

    def setup_bauhaus_background(self, show_grid=True, show_vignette=True):
        """Setup the Bauhaus Modern background."""
        self.camera.background_color = BauhausColors.BACKGROUND
        if show_grid:
            grid = BauhausBackground.dot_grid(
                self.camera.frame_width,
                self.camera.frame_height,
                spacing=0.45,
                dot_color=BauhausColors.GRID,
                fade_edges=True
            )
            self.add(grid)
        if show_vignette:
            vignette = BauhausBackground.vignette(
                self.camera.frame_width * 1.2,
                self.camera.frame_height * 1.2
            )
            self.add(vignette)

    def make_bauhaus_subtitle(self, text, position=DOWN * 2.5):
        subtitle = Text(
            text,
            font=FONT_PRIMARY,
            font_size=16,
            color=BauhausColors.TEXT_SECONDARY,
            weight=MEDIUM
        )
        subtitle.move_to(position)
        return subtitle

    def make_heading(self, text, position=UP * 3):
        heading = BauhausTypography.heading(text)
        heading.move_to(position)
        return heading

    def make_metadata_label(self, text, position):
        label = BauhausTypography.metadata(text)
        label.move_to(position)
        return label

    def make_code_label(self, text, position):
        label = BauhausTypography.code(text)
        label.move_to(position)
        return label


# =============================================================================
# EXAMPLE USAGE
# =============================================================================

class ExampleBauhausScene(BauhausScene):
    """Example scene demonstrating Bauhaus Modern Aesthetic."""

    def construct(self):
        self.setup_bauhaus_background()
        heading = self.make_heading("Bauhaus Modern")
        red_block = BauhausContainers.color_block(1.5, 1.5, BauhausColors.RED)
        red_block.move_to(LEFT * 2 + UP * 0.5)
        blue_block = BauhausContainers.color_block(1.2, 2.0, BauhausColors.BLUE)
        blue_block.move_to(RIGHT * 2 + DOWN * 0.5)
        yellow_block = BauhausContainers.color_block(0.8, 0.8, BauhausColors.YELLOW)
        yellow_block.move_to(ORIGIN)
        self.play(
            FadeIn(heading, run_time=0.5),
            FadeIn(red_block, run_time=0.6, rate_func=EASE_BAUHAUS_SPRING),
            FadeIn(blue_block, run_time=0.6, rate_func=EASE_BAUHAUS_SPRING),
            FadeIn(yellow_block, run_time=0.6, rate_func=EASE_BAUHAUS_SPRING),
            lag_ratio=0.15
        )
        self.wait(1)
