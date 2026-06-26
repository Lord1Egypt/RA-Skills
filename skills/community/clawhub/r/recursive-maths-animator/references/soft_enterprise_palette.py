"""
Soft Enterprise Aesthetic for Manim Animations
==============================================

A warm, sophisticated visual system for professional/educational content.

Color Palette:
- BACKGROUND: #FDF4E3 (warm cream)
- CONTAINER: #FAF5EB (paper white)
- BORDER: #DED6C4 (warm gray)
- GRID: #E0D8C3 (dot grid)
- TEXT_PRIMARY: #333333 (charcoal)
- TEXT_SECONDARY: #4A4A4A (slate gray)
- ROSE: #B57B8A (muted rose for metadata/accent)

Typography (Roboto font — skill default; see default_typography.py):
- Headings: 16-18px, Semi-Bold, -0.02em letter-spacing
- Body: 12-13px, Regular, 1.4 line-height
- Metadata: 10px, Medium, uppercase, +0.05em letter-spacing

Motion:
- EASE_GAS_SPRING: cubic-bezier(0.2, 0.8, 0.2, 1.0)
- Weighted, deliberate motion - never bouncy

Usage:
    from soft_enterprise_palette import SoftEnterpriseScene
    
    class MyScene(SoftEnterpriseScene):
        def construct(self):
            self.setup_soft_background()
            # Your content here
"""

from manim import *
from manim_voiceover import VoiceoverScene

from default_typography import DEFAULT_FONT


# =============================================================================
# COLOR PALETTE
# =============================================================================

class SoftColors:
    """Soft Enterprise color palette."""
    # Background
    BACKGROUND = "#FDF4E3"      # Warm cream
    VIGNETTE_CENTER = "#FDF4E3"
    VIGNETTE_EDGE = "#F7EFE0"
    
    # Containers
    CONTAINER = "#FAF5EB"       # Paper white
    BORDER = "#DED6C4"          # Warm gray
    GRID = "#E0D8C3"             # Dot grid
    
    # Text
    TEXT_PRIMARY = "#333333"     # Charcoal
    TEXT_SECONDARY = "#4A4A4A"    # Slate gray
    
    # Accents
    ROSE = "#B57B8A"              # Muted rose (metadata)
    GREEN = "#16A34A"             # Living green (success)
    RED = "#B04040"               # Rose alarm (warning)
    
    # Data flow
    CYAN = "#0891B2"              # Rules/policies
    LAVENDER = "#7C3AED"          # Databases/memory


# =============================================================================
# TYPOGRAPHY
# =============================================================================

class SoftTypography:
    """Typography helpers using the skill default sans font (Roboto)."""

    FONT_FAMILY = DEFAULT_FONT
    
    # Sizes (in Manim units, roughly pixels/100)
    SIZE_HEADING = 0.18           # 18px
    SIZE_BODY = 0.13              # 13px
    SIZE_METADATA = 0.10          # 10px
    
    @classmethod
    def heading(cls, text, color=SoftColors.TEXT_PRIMARY):
        """Create heading text."""
        return Text(
            text,
            font=cls.FONT_FAMILY,
            font_size=cls.SIZE_HEADING * 100,
            color=color,
            weight=SEMIBOLD
        )
    
    @classmethod
    def body(cls, text, color=SoftColors.TEXT_SECONDARY):
        """Create body text."""
        return Text(
            text,
            font=cls.FONT_FAMILY,
            font_size=cls.SIZE_BODY * 100,
            color=color
        )
    
    @classmethod
    def metadata(cls, text, color=SoftColors.ROSE):
        """Create metadata label (uppercase)."""
        return Text(
            text.upper(),
            font=cls.FONT_FAMILY,
            font_size=cls.SIZE_METADATA * 100,
            color=color,
            weight=MEDIUM
        )


# =============================================================================
# EASING
# =============================================================================

def EASE_GAS_SPRING(t: float) -> float:
    """
    Gas-spring easing: cubic-bezier(0.2, 0.8, 0.2, 1.0)
    Weighted, deliberate motion - never bouncy or frantic.
    """
    # Cubic bezier approximation
    return 3 * (1 - t) * (1 - t) * t * 0.2 + 3 * (1 - t) * t * t * 0.8 + t * t * t


# =============================================================================
# BACKGROUND GENERATORS
# =============================================================================

class SoftBackground:
    """Background generators for Soft Enterprise aesthetic."""
    
    @staticmethod
    def dot_grid(width, height, spacing=0.4, dot_color=SoftColors.GRID, 
                 dot_radius=0.02, fade_edges=True):
        """
        Create a dot grid background.
        
        Args:
            width: Frame width
            height: Frame height
            spacing: Distance between dots
            dot_color: Color of dots
            dot_radius: Radius of each dot
            fade_edges: Whether to fade dots at edges
        """
        dots = VGroup()
        
        # Calculate grid
        cols = int(width / spacing) + 2
        rows = int(height / spacing) + 2
        
        start_x = -width / 2
        start_y = -height / 2
        
        for row in range(rows):
            for col in range(cols):
                x = start_x + col * spacing
                y = start_y + row * spacing
                
                # Skip if outside frame
                if abs(x) > width/2 + spacing or abs(y) > height/2 + spacing:
                    continue
                
                dot = Circle(radius=dot_radius, fill_color=dot_color, fill_opacity=1)
                dot.move_to([x, y, 0])
                
                # Fade at edges
                if fade_edges:
                    dist_from_center = np.sqrt(x*x + y*y)
                    max_dist = np.sqrt((width/2)**2 + (height/2)**2)
                    fade_start = max_dist * 0.6
                    if dist_from_center > fade_start:
                        opacity = 1 - (dist_from_center - fade_start) / (max_dist - fade_start)
                        dot.set_fill(opacity=max(0, opacity))
                
                dots.add(dot)
        
        return dots
    
    @staticmethod
    def vignette(width, height, center_color=SoftColors.VIGNETTE_CENTER,
                 edge_color=SoftColors.VIGNETTE_EDGE):
        """
        Create a vignette gradient overlay.
        
        Note: Manim doesn't support true radial gradients natively.
        This creates a large circle with gradient-like effect using concentric circles.
        """
        # Create a rectangle covering the frame
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

class SoftContainers:
    """Container components for Soft Enterprise aesthetic."""
    
    @staticmethod
    def bezel(width, height, corner_radius=0.24, fill_color=SoftColors.CONTAINER,
              border_color=SoftColors.BORDER, shadow=True):
        """
        Create a bezel container with rounded corners.
        
        Args:
            width: Container width
            height: Container height
            corner_radius: Corner radius (default 24px = 0.24 Manim units)
            fill_color: Background color
            border_color: Border color
            shadow: Whether to add drop shadow
        """
        container = RoundedRectangle(
            corner_radius=corner_radius,
            width=width,
            height=height,
            fill_color=fill_color,
            fill_opacity=1,
            stroke_color=border_color,
            stroke_width=1
        )
        
        if shadow:
            # Create shadow (slightly larger, offset, low opacity)
            shadow_rect = RoundedRectangle(
                corner_radius=corner_radius,
                width=width,
                height=height,
                fill_color="#000000",
                fill_opacity=0.1,
                stroke_width=0
            )
            shadow_rect.shift(DOWN * 0.05 + RIGHT * 0.03)
            shadow_rect.set_z_index(-1)
            
            return VGroup(shadow_rect, container)
        
        return container
    
    @staticmethod
    def pill_label(text, bg_color=SoftColors.CONTAINER, text_color=SoftColors.TEXT_SECONDARY,
                   border_color=SoftColors.BORDER):
        """
        Create a pill-shaped label.
        
        Args:
            text: Label text
            bg_color: Background color
            text_color: Text color
            border_color: Border color
        """
        label = Text(text, font=DEFAULT_FONT, font_size=12, color=text_color)
        
        # Create pill background
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

class SoftEnterpriseScene(VoiceoverScene):
    """
    Base scene class with Soft Enterprise Aesthetic pre-configured.
    
    Usage:
        class MyScene(SoftEnterpriseScene):
            def construct(self):
                self.setup_soft_background()
                # Your animation here
    """
    
    def setup_soft_background(self, show_grid=True, show_vignette=True):
        """
        Setup the Soft Enterprise background.
        
        Args:
            show_grid: Whether to show dot grid
            show_vignette: Whether to show vignette overlay
        """
        # Set background color
        self.camera.background_color = SoftColors.BACKGROUND
        
        # Add dot grid
        if show_grid:
            grid = SoftBackground.dot_grid(
                self.camera.frame_width,
                self.camera.frame_height,
                spacing=0.4,
                dot_color=SoftColors.GRID,
                fade_edges=True
            )
            self.add(grid)
        
        # Add vignette
        if show_vignette:
            vignette = SoftBackground.vignette(
                self.camera.frame_width * 1.2,
                self.camera.frame_height * 1.2
            )
            self.add(vignette)
    
    def make_soft_subtitle(self, text, position=DOWN * 2.5):
        """
        Create a subtitle with Soft Enterprise styling.
        
        Args:
            text: Subtitle text
            position: Position on screen
        """
        subtitle = Text(
            text,
            font=DEFAULT_FONT,
            font_size=16,
            color=SoftColors.TEXT_SECONDARY,
            weight=MEDIUM
        )
        subtitle.move_to(position)
        return subtitle
    
    def make_heading(self, text, position=UP * 3):
        """
        Create a heading with Soft Enterprise styling.
        
        Args:
            text: Heading text
            position: Position on screen
        """
        heading = SoftTypography.heading(text)
        heading.move_to(position)
        return heading
    
    def make_metadata_label(self, text, position):
        """
        Create a metadata label with Soft Enterprise styling.
        
        Args:
            text: Label text
            position: Position on screen
        """
        label = SoftTypography.metadata(text)
        label.move_to(position)
        return label


# =============================================================================
# EXAMPLE USAGE
# =============================================================================

class ExampleSoftScene(SoftEnterpriseScene):
    """Example scene demonstrating Soft Enterprise Aesthetic."""
    
    def construct(self):
        # Setup background
        self.setup_soft_background()
        
        # Create heading
        heading = self.make_heading("Soft Enterprise Aesthetic")
        
        # Create a bezel container
        container = SoftContainers.bezel(4, 2.5)
        container.move_to(ORIGIN)
        
        # Create content inside container
        content = Text(
            "Warm cream backgrounds\nDot grid patterns\nGas-spring easing",
            font=DEFAULT_FONT,
            font_size=14,
            color=SoftColors.TEXT_SECONDARY,
            line_spacing=1.4
        )
        content.move_to(container.get_center())
        
        # Create pill label
        pill = SoftContainers.pill_label("v2.0", position=RIGHT * 3 + UP * 2)
        
        # Animate
        self.play(
            FadeIn(heading, run_time=0.6),
            FadeIn(container, run_time=0.6, rate_func=EASE_GAS_SPRING),
            lag_ratio=0.2
        )
        self.play(
            FadeIn(content, run_time=0.5),
            FadeIn(pill, run_time=0.5),
            lag_ratio=0.1
        )
        
        self.wait(1)
