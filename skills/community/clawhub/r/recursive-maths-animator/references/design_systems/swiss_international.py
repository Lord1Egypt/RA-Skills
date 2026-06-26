"""
Swiss International Aesthetic for Manim Animations
==================================================

Inspired by Josef Müller-Brockmann and the Swiss International Style.

- Strict grid systems
- Asymmetric layouts
- Rational hierarchy
- Clinical precision
- Black / white / restrained red accent

Color Palette:
- BACKGROUND: #FFFFFF (pure white)
- CONTAINER: #F5F5F5 (near-white)
- BORDER: #E0E0E0 (light gray)
- GRID: #D0D0D0 (dot grid)
- TEXT_PRIMARY: #111111 (near-black)
- TEXT_SECONDARY: #666666 (medium gray)
- ACCENT_RED: #D62828 (Swiss red)

Typography (Inter):
- Headings: 18px, Bold, -0.02em letter-spacing
- Body: 13px, Regular, 1.5 line-height
- Metadata: 10px, Medium, uppercase, +0.08em letter-spacing

Motion:
- EASE_SWISS_SNAP: instant settle, no bounce, precision timing

Usage:
    from swiss_international import SwissScene

    class MyScene(SwissScene):
        def construct(self):
            self.setup_swiss_background()
            # Your content here
"""

from manim import *
from manim_voiceover import VoiceoverScene

# Inter is the primary; JetBrains Mono for code-style labels if needed
FONT_PRIMARY = "Inter"
FONT_MONO = "JetBrains Mono"


# =============================================================================
# COLOR PALETTE
# =============================================================================

class SwissColors:
    """Swiss International color palette — clinical precision."""
    # Background
    BACKGROUND = "#FFFFFF"          # Pure white
    VIGNETTE_CENTER = "#FFFFFF"
    VIGNETTE_EDGE = "#F7F7F7"

    # Containers
    CONTAINER = "#F5F5F5"           # Near-white
    BORDER = "#E0E0E0"              # Light gray
    GRID = "#D0D0D0"                # Dot grid

    # Text
    TEXT_PRIMARY = "#111111"         # Near-black
    TEXT_SECONDARY = "#666666"       # Medium gray

    # Accents
    RED = "#D62828"                  # Swiss red
    BLACK = "#111111"                # Structural black
    WHITE = "#FFFFFF"                # Knockout white

    # Data flow
    CYAN = "#0891B2"                 # Rules / policies
    GREEN = "#16A34A"                # Success


# =============================================================================
# TYPOGRAPHY
# =============================================================================

class SwissTypography:
    """Typography using Inter (primary) and JetBrains Mono (code)."""

    FONT_FAMILY = FONT_PRIMARY
    FONT_FAMILY_MONO = FONT_MONO

    # Sizes (Manim units, roughly pixels/100)
    SIZE_HEADING = 0.18              # 18px
    SIZE_BODY = 0.13                 # 13px
    SIZE_METADATA = 0.10             # 10px
    SIZE_CODE = 0.11                 # 11px

    @classmethod
    def heading(cls, text, color=SwissColors.TEXT_PRIMARY):
        """Create heading text — bold, tight tracking."""
        return Text(
            text,
            font=cls.FONT_FAMILY,
            font_size=cls.SIZE_HEADING * 100,
            color=color,
            weight=BOLD,
            slant=ITALIC if False else None,  # Swiss rarely uses italic for headings
        )

    @classmethod
    def body(cls, text, color=SwissColors.TEXT_SECONDARY):
        """Create body text — neutral, readable."""
        return Text(
            text,
            font=cls.FONT_FAMILY,
            font_size=cls.SIZE_BODY * 100,
            color=color
        )

    @classmethod
    def metadata(cls, text, color=SwissColors.TEXT_SECONDARY):
        """Create metadata label — uppercase, spaced."""
        return Text(
            text.upper(),
            font=cls.FONT_FAMILY,
            font_size=cls.SIZE_METADATA * 100,
            color=color,
            weight=MEDIUM
        )

    @classmethod
    def code(cls, text, color=SwissColors.TEXT_PRIMARY):
        """Create code-style text using JetBrains Mono."""
        return Text(
            text,
            font=cls.FONT_FAMILY_MONO,
            font_size=cls.SIZE_CODE * 100,
            color=color,
            weight=MEDIUM
        )


# =============================================================================
# MOTION — Swiss snap: instant settle, no bounce
# =============================================================================

def EASE_SWISS_SNAP(t: float) -> float:
    """
    Swiss snap easing: sharp, precise, no overshoot.
    cubic-bezier(0.0, 0.0, 0.2, 1.0) approximation.
    """
    # Approximation of a very sharp ease-out
    if t < 0.2:
        return t * t * t * 12.5  # fast initial move
    return 1 - (1 - t) * (1 - t)  # gentle landing


# =============================================================================
# BACKGROUND GENERATORS
# =============================================================================

class SwissBackground:
    """Background generators for Swiss International aesthetic."""

    @staticmethod
    def dot_grid(width, height, spacing=0.5, dot_color=SwissColors.GRID,
                 dot_radius=0.015, fade_edges=True):
        """
        Create a precise dot grid — larger spacing than soft enterprise
        to emphasize the grid system.
        """
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
                    fade_start = max_dist * 0.65
                    if dist_from_center > fade_start:
                        opacity = 1 - (dist_from_center - fade_start) / (max_dist - fade_start)
                        dot.set_fill(opacity=max(0, opacity))
                dots.add(dot)
        return dots

    @staticmethod
    def vignette(width, height, center_color=SwissColors.VIGNETTE_CENTER,
                 edge_color=SwissColors.VIGNETTE_EDGE):
        """Subtle vignette — barely perceptible on white."""
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

class SwissContainers:
    """Container components — sharp corners, thin borders, systematic spacing."""

    @staticmethod
    def bezel(width, height, corner_radius=0.0, fill_color=SwissColors.CONTAINER,
              border_color=SwissColors.BORDER, stroke_width=1, shadow=False):
        """
        Create a bezel container — Swiss style uses sharp corners (radius=0)
        or very slight rounding. Thin 1px borders.
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
                fill_opacity=0.06,
                stroke_width=0
            )
            shadow_rect.shift(DOWN * 0.04 + RIGHT * 0.02)
            shadow_rect.set_z_index(-1)
            return VGroup(shadow_rect, container)
        return container

    @staticmethod
    def pill_label(text, bg_color=SwissColors.CONTAINER, text_color=SwissColors.TEXT_SECONDARY,
                     border_color=SwissColors.BORDER):
        """Pill-shaped label with restrained styling."""
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

    @staticmethod
    def grid_line(start, end, color=SwissColors.GRID, stroke_width=0.5):
        """A single grid line — used for explicit grid compositions."""
        return Line(start, end, color=color, stroke_width=stroke_width)


# =============================================================================
# BASE SCENE CLASS
# =============================================================================

class SwissScene(VoiceoverScene):
    """
    Base scene class with Swiss International Aesthetic pre-configured.

    Usage:
        class MyScene(SwissScene):
            def construct(self):
                self.setup_swiss_background()
                # Your animation here
    """

    def setup_swiss_background(self, show_grid=True, show_vignette=True):
        """Setup the Swiss International background."""
        self.camera.background_color = SwissColors.BACKGROUND
        if show_grid:
            grid = SwissBackground.dot_grid(
                self.camera.frame_width,
                self.camera.frame_height,
                spacing=0.5,
                dot_color=SwissColors.GRID,
                fade_edges=True
            )
            self.add(grid)
        if show_vignette:
            vignette = SwissBackground.vignette(
                self.camera.frame_width * 1.2,
                self.camera.frame_height * 1.2
            )
            self.add(vignette)

    def make_swiss_subtitle(self, text, position=DOWN * 2.5):
        """Create a subtitle with Swiss styling."""
        subtitle = Text(
            text,
            font=FONT_PRIMARY,
            font_size=16,
            color=SwissColors.TEXT_SECONDARY,
            weight=MEDIUM
        )
        subtitle.move_to(position)
        return subtitle

    def make_heading(self, text, position=UP * 3):
        """Create a heading with Swiss styling."""
        heading = SwissTypography.heading(text)
        heading.move_to(position)
        return heading

    def make_metadata_label(self, text, position):
        """Create a metadata label with Swiss styling."""
        label = SwissTypography.metadata(text)
        label.move_to(position)
        return label

    def make_code_label(self, text, position):
        """Create a code-style label with JetBrains Mono."""
        label = SwissTypography.code(text)
        label.move_to(position)
        return label


# =============================================================================
# EXAMPLE USAGE
# =============================================================================

class ExampleSwissScene(SwissScene):
    """Example scene demonstrating Swiss International Aesthetic."""

    def construct(self):
        self.setup_swiss_background()
        heading = self.make_heading("Swiss International Style")
        container = SwissContainers.bezel(4, 2.5, corner_radius=0.0)
        container.move_to(ORIGIN)
        content = Text(
            "Asymmetric grids\nRational hierarchy\nClinical precision",
            font=FONT_PRIMARY,
            font_size=14,
            color=SwissColors.TEXT_SECONDARY,
            line_spacing=1.5
        )
        content.move_to(container.get_center())
        pill = SwissContainers.pill_label("v1.0", position=RIGHT * 3 + UP * 2)
        self.play(
            FadeIn(heading, run_time=0.5),
            FadeIn(container, run_time=0.5, rate_func=EASE_SWISS_SNAP),
            lag_ratio=0.2
        )
        self.play(
            FadeIn(content, run_time=0.4),
            FadeIn(pill, run_time=0.4),
            lag_ratio=0.1
        )
        self.wait(1)
