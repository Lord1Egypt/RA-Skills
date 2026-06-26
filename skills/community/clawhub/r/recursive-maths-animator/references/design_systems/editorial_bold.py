"""
Editorial Bold Aesthetic for Manim Animations
=============================================

Inspired by Paula Scher / Pentagram and high-end editorial design.

- Dramatic scale contrast
- Deep navy + warm cream
- Magazine confidence
- Serif headlines + sans body
- Expressive, storytelling-forward

Color Palette:
- BACKGROUND: #F8F5F0 (warm cream — paper)
- CONTAINER: #FFFFFF (bright white)
- BORDER: #D4CEC5 (warm taupe)
- GRID: #E5E0D8 (subtle dot grid)
- TEXT_PRIMARY: #0F1B2E (deep navy)
- TEXT_SECONDARY: #4A5568 (slate)
- ACCENT: #C0392B (editorial red — bold, assertive)
- GOLD: #B8860B (warm gold for luxury moments)

Typography:
- Headings: Playfair Display, 20px, Bold, dramatic serifs
- Body: Inter, 13px, Regular, 1.5 line-height
- Metadata: Inter, 10px, Medium, uppercase

Motion:
- EASE_EDITORIAL_DRAMA: slow reveal, cinematic, weighty

Usage:
    from editorial_bold import EditorialScene

    class MyScene(EditorialScene):
        def construct(self):
            self.setup_editorial_background()
            # Your content here
"""

from manim import *
from manim_voiceover import VoiceoverScene

FONT_HEADING = "Playfair Display"
FONT_BODY = "Inter"


# =============================================================================
# COLOR PALETTE
# =============================================================================

class EditorialColors:
    """Editorial Bold color palette — dramatic, warm, confident."""
    # Background
    BACKGROUND = "#F8F5F0"           # Warm cream paper
    VIGNETTE_CENTER = "#F8F5F0"
    VIGNETTE_EDGE = "#EDEAE3"

    # Containers
    CONTAINER = "#FFFFFF"             # Bright white
    BORDER = "#D4CEC5"              # Warm taupe
    GRID = "#E5E0D8"                # Subtle dot grid

    # Text
    TEXT_PRIMARY = "#0F1B2E"          # Deep navy
    TEXT_SECONDARY = "#4A5568"       # Slate

    # Accents
    RED = "#C0392B"                   # Editorial red
    GOLD = "#B8860B"                 # Warm gold
    GREEN = "#2E7D4A"                # Forest green


# =============================================================================
# TYPOGRAPHY
# =============================================================================

class EditorialTypography:
    """
    Typography using Playfair Display for headings, Inter for body/metadata.
    Dramatic serif + clean sans pairing — classic editorial.
    """

    FONT_FAMILY_PRIMARY = FONT_HEADING      # Playfair Display
    FONT_FAMILY_SECONDARY = FONT_BODY       # Inter

    SIZE_HEADING = 0.20                      # 20px — slightly larger for drama
    SIZE_BODY = 0.13
    SIZE_METADATA = 0.10
    SIZE_CODE = 0.11

    @classmethod
    def heading(cls, text, color=EditorialColors.TEXT_PRIMARY):
        """Dramatic serif heading — large, bold, expressive."""
        return Text(
            text,
            font=cls.FONT_FAMILY_PRIMARY,
            font_size=cls.SIZE_HEADING * 100,
            color=color,
            weight=BOLD,
        )

    @classmethod
    def body(cls, text, color=EditorialColors.TEXT_SECONDARY):
        """Clean sans body — readable, understated."""
        return Text(
            text,
            font=cls.FONT_FAMILY_SECONDARY,
            font_size=cls.SIZE_BODY * 100,
            color=color
        )

    @classmethod
    def metadata(cls, text, color=EditorialColors.TEXT_SECONDARY):
        """Metadata label — uppercase, spaced, Inter."""
        return Text(
            text.upper(),
            font=cls.FONT_FAMILY_SECONDARY,
            font_size=cls.SIZE_METADATA * 100,
            color=color,
            weight=MEDIUM
        )

    @classmethod
    def code(cls, text, color=EditorialColors.TEXT_PRIMARY):
        return Text(
            text,
            font=cls.FONT_FAMILY_SECONDARY,
            font_size=cls.SIZE_CODE * 100,
            color=color,
            weight=MEDIUM
        )


# =============================================================================
# MOTION — Editorial drama: slow reveal, cinematic, weighty
# =============================================================================

def EASE_EDITORIAL_DRAMA(t: float) -> float:
    """
    Editorial drama easing: slow, weighty, cinematic.
    Very gentle ease-out — like a curtain rising.
    cubic-bezier(0.25, 0.1, 0.25, 1.0) approximation.
    """
    return 1 - (1 - t) ** 2.5  # slow start, graceful finish


# =============================================================================
# BACKGROUND GENERATORS
# =============================================================================

class EditorialBackground:
    """Background generators for Editorial Bold aesthetic."""

    @staticmethod
    def dot_grid(width, height, spacing=0.5, dot_color=EditorialColors.GRID,
                 dot_radius=0.016, fade_edges=True):
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
    def vignette(width, height, center_color=EditorialColors.VIGNETTE_CENTER,
                 edge_color=EditorialColors.VIGNETTE_EDGE):
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

class EditorialContainers:
    """Container components — elegant, slightly more rounding than Swiss."""

    @staticmethod
    def bezel(width, height, corner_radius=0.16, fill_color=EditorialColors.CONTAINER,
              border_color=EditorialColors.BORDER, stroke_width=1, shadow=True):
        """
        Elegant container — slightly softer corners than Swiss,
        subtle warm shadow.
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
            shadow_rect.shift(DOWN * 0.05 + RIGHT * 0.03)
            shadow_rect.set_z_index(-1)
            return VGroup(shadow_rect, container)
        return container

    @staticmethod
    def pill_label(text, bg_color=EditorialColors.CONTAINER, text_color=EditorialColors.TEXT_SECONDARY,
                   border_color=EditorialColors.BORDER):
        label = Text(text, font=FONT_BODY, font_size=12, color=text_color)
        pill = RoundedRectangle(
            corner_radius=0.15,
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

class EditorialScene(VoiceoverScene):
    """
    Base scene class with Editorial Bold Aesthetic pre-configured.
    """

    def setup_editorial_background(self, show_grid=True, show_vignette=True):
        """Setup the Editorial Bold background."""
        self.camera.background_color = EditorialColors.BACKGROUND
        if show_grid:
            grid = EditorialBackground.dot_grid(
                self.camera.frame_width,
                self.camera.frame_height,
                spacing=0.5,
                dot_color=EditorialColors.GRID,
                fade_edges=True
            )
            self.add(grid)
        if show_vignette:
            vignette = EditorialBackground.vignette(
                self.camera.frame_width * 1.2,
                self.camera.frame_height * 1.2
            )
            self.add(vignette)

    def make_editorial_subtitle(self, text, position=DOWN * 2.5):
        subtitle = Text(
            text,
            font=FONT_BODY,
            font_size=16,
            color=EditorialColors.TEXT_SECONDARY,
            weight=MEDIUM
        )
        subtitle.move_to(position)
        return subtitle

    def make_heading(self, text, position=UP * 3):
        """Dramatic serif heading."""
        heading = EditorialTypography.heading(text)
        heading.move_to(position)
        return heading

    def make_metadata_label(self, text, position):
        label = EditorialTypography.metadata(text)
        label.move_to(position)
        return label


# =============================================================================
# EXAMPLE USAGE
# =============================================================================

class ExampleEditorialScene(EditorialScene):
    """Example scene demonstrating Editorial Bold Aesthetic."""

    def construct(self):
        self.setup_editorial_background()
        heading = self.make_heading("Editorial Bold")
        container = EditorialContainers.bezel(4, 2.5, corner_radius=0.16)
        container.move_to(ORIGIN)
        content = Text(
            "Dramatic scale contrast\nDeep navy + warm cream\nMagazine confidence",
            font=FONT_BODY,
            font_size=14,
            color=EditorialColors.TEXT_SECONDARY,
            line_spacing=1.5
        )
        content.move_to(container.get_center())
        pill = EditorialContainers.pill_label("v1.0", position=RIGHT * 3 + UP * 2)
        self.play(
            FadeIn(heading, run_time=0.8, rate_func=EASE_EDITORIAL_DRAMA),
            FadeIn(container, run_time=0.6, rate_func=EASE_EDITORIAL_DRAMA),
            lag_ratio=0.2
        )
        self.play(
            FadeIn(content, run_time=0.5),
            FadeIn(pill, run_time=0.5),
            lag_ratio=0.1
        )
        self.wait(1)
