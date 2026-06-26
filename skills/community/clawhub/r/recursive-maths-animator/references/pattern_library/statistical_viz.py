"""
Statistical Visualization Patterns
AutoAgent-trained: Statistical concepts animated
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "references"))

from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService
import random


class DistributionAnimation(VoiceoverScene):
    """
    Visualize a probability distribution (normal/Gaussian).
    
    Configurable:
        mean: Center of distribution
        std_dev: Standard deviation
        show_area: Show shaded area under curve
        animation_duration: Total animation time
    """
    
    mean = 0
    std_dev = 1
    show_area = True
    animation_duration = 10
    
    def __init__(self, **kwargs):
        config.pixel_width = 1920
        config.pixel_height = 1080
        config.frame_width = 14
        config.frame_height = 8
        config.frame_rate = 60
        
        super().__init__(**kwargs)
        self.set_speech_service(GTTSService(lang='en'))
    
    def gaussian(self, x, mu, sigma):
        """Gaussian function"""
        import math
        return (1 / (sigma * math.sqrt(2 * math.pi))) * math.exp(-0.5 * ((x - mu) / sigma) ** 2)
    
    def construct(self):
        # Title
        title = Text("Normal Distribution", font_size=36)
        title.to_edge(UP, buff=0.5)
        
        with self.voiceover(text="Let's explore the normal distribution.") as tracker:
            self.play(FadeIn(title), run_time=1)
        
        self.wait(0.5)
        
        # Create axes
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[0, 0.5, 0.1],
            x_length=10,
            y_length=4,
            axis_config={"include_numbers": True}
        )
        axes.next_to(title, DOWN, buff=1)
        
        with self.voiceover(text="This is the classic bell curve.") as tracker:
            self.play(Create(axes), run_time=1.5)
        
        # Plot the curve
        curve = axes.plot(
            lambda x: self.gaussian(x, self.mean, self.std_dev),
            color=BLUE,
            stroke_width=3
        )
        
        with self.voiceover(text="The curve shows probability density.") as tracker:
            self.play(Create(curve), run_time=2)
        
        self.wait(0.5)
        
        # Show mean
        mean_line = DashedLine(
            axes.c2p(self.mean, 0),
            axes.c2p(self.mean, self.gaussian(self.mean, self.mean, self.std_dev)),
            color=YELLOW
        )
        mean_label = Text("Mean", font_size=20, color=YELLOW)
        mean_label.next_to(mean_line, UP, buff=0.1)
        
        with self.voiceover(text="The center line marks the mean.") as tracker:
            self.play(Create(mean_line), FadeIn(mean_label))
        
        self.wait(0.5)
        
        # Show standard deviation intervals
        std_lines = VGroup()
        for offset in [-1, 1]:
            x_pos = self.mean + offset * self.std_dev
            line = DashedLine(
                axes.c2p(x_pos, 0),
                axes.c2p(x_pos, self.gaussian(x_pos, self.mean, self.std_dev)),
                color=GREEN,
                stroke_opacity=0.5
            )
            std_lines.add(line)
        
        std_label = Text("±1σ", font_size=20, color=GREEN)
        std_label.next_to(axes, DOWN, buff=0.3)
        
        with self.voiceover(text="These lines mark one standard deviation from the mean.") as tracker:
            self.play(Create(std_lines), FadeIn(std_label))
        
        self.wait(0.5)
        
        # Shade area under curve if enabled
        if self.show_area:
            area = axes.get_area(
                curve,
                x_range=[-4, 4],
                color=BLUE,
                opacity=0.2
            )
            
            with self.voiceover(text="The total area under the curve equals one.") as tracker:
                self.play(FadeIn(area))
        
        self.wait(2)
        
        with self.voiceover(text="This distribution appears everywhere in nature.") as tracker:
            self.wait(1)
        
        self.play(FadeOut(title), FadeOut(axes), FadeOut(curve), 
                 FadeOut(mean_line), FadeOut(mean_label),
                 FadeOut(std_lines), FadeOut(std_label))
        if self.show_area:
            self.play(FadeOut(area))


class FormulaDerivation(VoiceoverScene):
    """
    Show step-by-step formula derivation or mathematical concept.
    
    Configurable:
        formula_steps: List of (formula, explanation) tuples
        highlight_color: Color for highlighting
        animation_duration: Total animation time
    """
    
    formula_steps = [
        ("a² + b² = c²", "The Pythagorean theorem"),
        ("c = √(a² + b²)", "Solving for c"),
        ("c = √c²", "The hypotenuse")
    ]
    highlight_color = YELLOW
    animation_duration = 10
    
    def __init__(self, **kwargs):
        config.pixel_width = 1920
        config.pixel_height = 1080
        config.frame_width = 14
        config.frame_height = 8
        config.frame_rate = 60
        
        super().__init__(**kwargs)
        self.set_speech_service(GTTSService(lang='en'))
    
    def construct(self):
        # Title
        title = Text("Formula Derivation", font_size=36)
        title.to_edge(UP, buff=0.5)
        
        with self.voiceover(text="Let's derive this formula step by step.") as tracker:
            self.play(FadeIn(title), run_time=1)
        
        self.wait(0.5)
        
        # Show formulas step by step
        previous_formula = None
        
        for i, (formula_text, explanation) in enumerate(self.formula_steps):
            # Create formula
            formula = Text(formula_text, font_size=48)
            formula.move_to(ORIGIN)
            
            if i == 0:
                # First formula
                with self.voiceover(text=f"{explanation}.") as tracker:
                    self.play(FadeIn(formula), run_time=1.5)
            else:
                # Transform from previous
                with self.voiceover(text=f"{explanation}.") as tracker:
                    self.play(Transform(previous_formula, formula), run_time=1.5)
                formula = previous_formula
            
            # Highlight
            highlight = SurroundingRectangle(formula, color=self.highlight_color, buff=0.2)
            
            with self.voiceover(text="Notice the relationship.") as tracker:
                self.play(Create(highlight), run_time=0.5)
                self.wait(0.5)
                self.play(FadeOut(highlight))
            
            previous_formula = formula
            self.wait(0.5)
        
        # Final result
        final_text = Text("Final Result", font_size=28, color=GREEN)
        final_text.next_to(previous_formula, DOWN, buff=1)
        
        with self.voiceover(text="And we arrive at the final result.") as tracker:
            self.play(FadeIn(final_text), run_time=1)
        
        self.wait(2)
        
        self.play(FadeOut(title), FadeOut(previous_formula), FadeOut(final_text))


class SamplingVisualization(VoiceoverScene):
    """
    Visualize sampling and the Central Limit Theorem.
    
    Configurable:
        sample_size: Number of samples to show
        population_mean: Mean of population
        animation_duration: Total animation time
    """
    
    sample_size = 30
    population_mean = 50
    animation_duration = 10
    
    def __init__(self, **kwargs):
        config.pixel_width = 1920
        config.pixel_height = 1080
        config.frame_width = 14
        config.frame_height = 8
        config.frame_rate = 60
        
        super().__init__(**kwargs)
        self.set_speech_service(GTTSService(lang='en'))
    
    def construct(self):
        # Title
        title = Text("Sampling Distribution", font_size=36)
        title.to_edge(UP, buff=0.5)
        
        with self.voiceover(text="Let's explore sampling and distributions.") as tracker:
            self.play(FadeIn(title), run_time=1)
        
        self.wait(0.5)
        
        # Create population representation
        population_label = Text("Population", font_size=28)
        population_label.to_edge(LEFT, buff=2)
        population_label.shift(UP * 2)
        
        # Create population dots
        population_dots = VGroup()
        for _ in range(50):
            dot = Dot(
                point=[random.uniform(-3, 3), random.uniform(-2, 2), 0],
                radius=0.05,
                color=BLUE
            )
            population_dots.add(dot)
        
        population_dots.next_to(population_label, DOWN, buff=0.5)
        
        with self.voiceover(text="Here's our population distribution.") as tracker:
            self.play(
                FadeIn(population_label),
                LaggedStart(*[FadeIn(d) for d in population_dots], lag_ratio=0.02)
            )
        
        self.wait(1)
        
        # Show sampling
        sample_label = Text("Sample", font_size=28)
        sample_label.to_edge(RIGHT, buff=2)
        sample_label.shift(UP * 2)
        
        sample_dots = VGroup()
        for _ in range(self.sample_size):
            dot = Dot(
                point=[random.uniform(3, 6), random.uniform(-2, 2), 0],
                radius=0.08,
                color=GREEN
            )
            sample_dots.add(dot)
        
        sample_dots.next_to(sample_label, DOWN, buff=0.5)
        
        with self.voiceover(text=f"Now we take a sample of {self.sample_size} observations.") as tracker:
            self.play(
                FadeIn(sample_label),
                LaggedStart(*[GrowFromCenter(d) for d in sample_dots], lag_ratio=0.05)
            )
        
        self.wait(1)
        
        # Show sample mean
        sample_mean = sum(d.get_center()[1] for d in sample_dots) / len(sample_dots)
        mean_line = DashedLine(
            [3, sample_mean, 0],
            [6, sample_mean, 0],
            color=YELLOW
        )
        mean_label = Text("Sample Mean", font_size=20, color=YELLOW)
        mean_label.next_to(mean_line, RIGHT)
        
        with self.voiceover(text="The sample has its own mean.") as tracker:
            self.play(Create(mean_line), FadeIn(mean_label))
        
        self.wait(1)
        
        # Show multiple samples converging
        convergence_text = Text("Many Samples → Normal Distribution", font_size=24)
        convergence_text.move_to(DOWN * 2)
        
        with self.voiceover(text="With many samples, means form a normal distribution.") as tracker:
            self.play(FadeIn(convergence_text))
        
        # Show normal curve forming
        normal_curve = VMobject()
        normal_curve.set_points_as_corners([
            [-1, -1, 0],
            [0, 1, 0],
            [1, -1, 0]
        ])
        normal_curve.set_stroke(YELLOW, width=3)
        normal_curve.move_to(DOWN * 3)
        
        with self.voiceover(text="This is the Central Limit Theorem.") as tracker:
            self.play(Create(normal_curve))
        
        self.wait(2)
        
        self.play(
            FadeOut(title), FadeOut(population_label), FadeOut(population_dots),
            FadeOut(sample_label), FadeOut(sample_dots), FadeOut(mean_line),
            FadeOut(mean_label), FadeOut(convergence_text), FadeOut(normal_curve)
        )


if __name__ == "__main__":
    config.quality = "high_quality"
    scene = DistributionAnimation()
    scene.render()
