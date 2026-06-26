"""
Apple Precision Aesthetic for Manim Animations
==============================================

Inspired by Jony Ive and Apple industrial design.

- Cool neutrals
- Generous whitespace
- Subtle depth and layering
- Thin-to-medium weights
- Sleek, tech-forward motion

Color Palette:
- BACKGROUND: #F5F5F7 (Apple light gray)
- CONTAINER: #FFFFFF (pure white)
- BORDER: #D2D2D7 (Apple border gray)
- GRID: #E8E8ED (subtle dot grid)
- TEXT_PRIMARY: #1D1D1F (Apple near-black)
- TEXT_SECONDARY: #86868B (Apple gray)
- ACCENT_BLUE: #0071E3 (Apple blue)
- ACCENT_GREEN: #34C759 (Apple green)
- ACCENT_ORANGE: #FF9500 (Apple orange)

Typography (DM Sans):
- Headings: 18px, Medium, generous letter-spacing
- Body: 13px, Regular, 1.4 line-height
- Metadata: 10px, Medium, uppercase

Motion:
- EASE_APPLE_FLOAT: smooth, floating, weightless precision

Usage:
    from apple_precision import AppleScene

    class MyScene(AppleScene):
        def construct(self):
            self.setup_apple_background()
            # Your content here
"""

from manim import *
from manim_voiceover import VoiceoverScene

FONT_PRIMARY = "DM Sans"


# =============================================================================
# COLOR PALETTE
# =============================================================================

class AppleColors:
    """Apple Precision color palette — cool, sleek, tech-forward."""
    # Background
    BACKGROUND = "#F5F5F7"           # Apple light gray
    VIGNETTE_CENTER = "#F5F5F7"
    VIGNETTE_EDGE = "#EBEBEF"

    # Containers
    CONTAINER = "#FFFFFF"             # Pure white
    BORDER = "#D2D2D7"              # Apple border gray
    GRID = "#E8E8ED"                # Subtle dot grid

    # Text
    TEXT_PRIMARY = "#1D1D1F"          # Apple near-black
    TEXT_SECONDARY = "#86868B"       # Apple gray

    # Accents — Apple system colors
    BLUE = "#0071E3"                 # Apple blue
    GREEN = "#34C759"                # Apple green
    ORANGE = "#FF9500"               # Apple orange
    PINK = "#FF2D55"                 # Apple pink
    PURPLE = "#AF52DE"               # Apple purple
    YELLOW = "#FFCC00"               # Apple yellow

    # System
    RED = "#FF3B30"                  # Apple red (alarm)


# =============================================================================
# TYPOGRAPHY
# =============================================================================

class AppleTypography:
    """Typography using DM Sans — geometric, modern, Apple-like."""

    FONT_FAMILY = FONT_PRIMARY

    SIZE_HEADING = 0.18
    SIZE_BODY = 0.13
    SIZE_METADATA = 0.10
    SIZE_CODE = 0.11

    @classmethod
    def heading(cls, text, color=AppleColors.TEXT_PRIMARY):
        return Text(
            text,
            font=cls.FONT_FAMILY,
            font_size=cls.SIZE_HEADING * 100,
            color=color,
            weight=MEDIUM,
        )

    @classmethod
    def body(cls, text, color=AppleColors.TEXT_SECONDARY):
        return Text(
            text,
            font=cls.FONT_FAMILY,
            font_size=cls.SIZE_BODY * 100,
            color=color
        )

    @classmethod
    def metadata(cls, text, color=AppleColors.TEXT_SECONDARY):
        return Text(
            text.upper(),
            font=cls.FONT_FAMILY,
            font_size=cls.SIZE_METADATA * 100,
            color=color,
            weight=MEDIUM
        )

    @classmethod
    def code(cls, text, color=AppleColors.TEXT_PRIMARY):
        return Text(
            text,
            font=cls.FONT_FAMILY,
            font_size=cls.SIZE_CODE * 100,
            color=color,
            weight=MEDIUM
        )


# =============================================================================
# MOTION — Apple float: smooth, floating, weightless precision
# =============================================================================

def EASE_APPLE_FLOAT(t: float) -> float:
    """
    Apple float easing: smooth, weightless, almost floating.
    Very gentle ease-out — like objects settling into place in zero gravity.
    cubic-bezier(0.32, 0.72, 0, 1.0) approximation.
    """
    return 1 - (1 - t) ** 3.5  # very soft landing


# =============================================================================
# BACKGROUND GENERATORS
# =============================================================================

class AppleBackground:
    """Background generators for Apple Precision aesthetic."""

    @staticmethod
    def dot_grid(width, height, spacing=0.55, dot_color=AppleColors.GRID,
                 dot_radius=0.014, fade_edges=True):
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
    def vignette(width, height, center_color=AppleColors.VIGNETTE_CENTER,
                 edge_color=AppleColors.VIGNETTE_EDGE):
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

class AppleContainers:
    """Container components — clean, generous rounding, subtle depth."""

    @staticmethod
    def bezel(width, height, corner_radius=0.20, fill_color=AppleColors.CONTAINER,
              border_color=AppleColors.BORDER, stroke_width=0.5, shadow=True):
        """
        Apple-style container — generous 20px rounding, thin 0.5px border,
        soft diffuse shadow.
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
                fill_opacity=0.08,
                stroke_width=0
            )
            shadow_rect.shift(DOWN * 0.06 + RIGHT * 0.04)
            shadow_rect.set_z_index(-1)
            return VGroup(shadow_rect, container)
        return container

    @staticmethod
    def pill_label(text, bg_color=AppleColors.CONTAINER, text_color=AppleColors.TEXT_SECONDARY,
                   border_color=AppleColors.BORDER):
        label = Text(text, font=FONT_PRIMARY, font_size=12, color=text_color)
        pill = RoundedRectangle(
            corner_radius=0.18,
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

class AppleScene(VoiceoverScene):
    """
    Base scene class with Apple Precision Aesthetic pre-configured.
    """

    def setup_apple_background(self, show_grid=True, show_vignette=True):
        """Setup the Apple Precision background."""
        self.camera.background_color = AppleColors.BACKGROUND
        if show_grid:
            grid = AppleBackground.dot_grid(
                self.camera.frame_width,
                self.camera.frame_height,
                spacing=0.55,
                dot_color=AppleColors.GRID,
                fade_edges=True
            )
            self.add(grid)
        if show_vignette:
            vignette = AppleBackground.vignette(
                self.camera.frame_width * 1.2,
                self.camera.frame_height * 1.2
            )
            self.add(vignette)

    def make_apple_subtitle(self, text, position=DOWN * 2.5):
        subtitle = Text(
            text,
            font=FONT_PRIMARY,
            font_size=16,
            color=AppleColors.TEXT_SECONDARY,
            weight=MEDIUM
        )
        subtitle.move_to(position)
        return subtitle

    def make_heading(self, text, position=UP * 3):
        heading = AppleTypography.heading(text)
        heading.move_to(position)
        return heading

    def make_metadata_label(self, text, position):
        label = AppleTypography.metadata(text)
        label.move_to(position)
        return label


# =============================================================================
# EXAMPLE USAGE
# =============================================================================

class ExampleAppleScene(AppleScene):
    """Example scene demonstrating Apple Precision Aesthetic."""

    def construct(self):
        self.setup_apple_background()
        heading = self.make_heading("Apple Precision")
        container = AppleContainers.bezel(4, 2.5, corner_radius=0.20)
        container.move_to(ORIGIN)
        content = Text(
            "Cool neutrals\nGenerous whitespace\nSleek motion",
            font=FONT_PRIMARY,
            font_size=14,
            color=AppleColors.TEXT_SECONDARY,
            line_spacing=1.4
        )
        content.move_to(container.get_center())
        pill = AppleContainers.pill_label("v1.0", position=RIGHT * 3 + UP * 2)
        self.play(
            FadeIn(heading, run_time=0.7, rate_func=EASE_APPLE_FLOAT),
            FadeIn(container, run_time=0.7, rate_func=EASE_APPLE_FLOAT),
            lag_ratio=0.2
        )
        self.play(
            FadeIn(content, run_time=0.5),
            FadeIn(pill, run_time=0.5),
            lag_ratio=0.1
        )
        self.wait(1)
