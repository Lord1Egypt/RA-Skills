"""
Pie Chart Animation Patterns
AutoAgent-trained: Pie chart variants and transitions
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "references"))

from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService


class BasicPieChart(VoiceoverScene):
    """
    Basic animated pie chart with segments appearing simultaneously.
    
    Configurable:
        data: List of (label, value) tuples
        colors: List of colors for segments
        show_percentages: Whether to show percentage labels
        animation_duration: Total animation time
    """
    
    data = [
        ("A", 35),
        ("B", 25),
        ("C", 20),
        ("D", 20)
    ]
    colors = [BLUE, GREEN, YELLOW, RED]
    show_percentages = True
    animation_duration = 8
    
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
        title = Text("Market Share", font_size=36)
        title.to_edge(UP, buff=0.5)
        
        with self.voiceover(text="Let's look at market share distribution.") as tracker:
            self.play(FadeIn(title), run_time=1)
        
        self.wait(0.5)
        
        # Create pie chart
        chart_group = self.create_pie_chart()
        chart_group.move_to(ORIGIN)
        
        with self.voiceover(text="Here's the breakdown by segment.") as tracker:
            self.play(FadeIn(chart_group), run_time=2)
        
        self.wait(1)
        
        # Highlight each segment
        segments = chart_group[0]  # The pie sectors
        labels = chart_group[1]    # The labels
        
        for i, (segment, label) in enumerate(zip(segments, labels)):
            label_text, value = self.data[i]
            
            with self.voiceover(text=f"{label_text} represents {value} percent.") as tracker:
                self.play(
                    segment.animate.set_fill(opacity=1),
                    run_time=0.5
                )
                self.wait(0.3)
        
        self.wait(1)
        
        with self.voiceover(text="Pie charts show proportional relationships clearly.") as tracker:
            self.wait(1)
        
        self.play(FadeOut(title), FadeOut(chart_group))
    
    def create_pie_chart(self):
        """Create a pie chart from self.data"""
        total = sum(value for _, value in self.data)
        angles = [(value / total) * TAU for _, value in self.data]
        
        # Create sectors
        sectors = VGroup()
        labels = VGroup()
        
        start_angle = 0
        for i, ((label_text, value), angle) in enumerate(zip(self.data, angles)):
            # Create sector
            sector = Sector(
                start_angle=start_angle,
                angle=angle,
                radius=2.5,
                fill_color=self.colors[i % len(self.colors)],
                fill_opacity=0.8,
                stroke_color=WHITE,
                stroke_width=2
            )
            sectors.add(sector)
            
            # Calculate label position
            mid_angle = start_angle + angle / 2
            label_radius = 3.2
            label_x = label_radius * np.cos(mid_angle)
            label_y = label_radius * np.sin(mid_angle)
            
            # Create label
            percentage = int((value / total) * 100)
            if self.show_percentages:
                label = Text(f"{label_text}\n{percentage}%", font_size=20)
            else:
                label = Text(label_text, font_size=20)
            
            label.move_to([label_x, label_y, 0])
            labels.add(label)
            
            start_angle += angle
        
        chart = VGroup(sectors, labels)
        return chart


class StaggeredPieChart(VoiceoverScene):
    """
    Pie chart with staggered segment entry and optional explosion.
    
    Configurable:
        data: List of (label, value) tuples
        colors: List of colors for segments
        explode_index: Which segment to highlight (None for none)
        explode_distance: How far to pull out
        animation_duration: Total animation time
    """
    
    data = [
        ("Product A", 40),
        ("Product B", 30),
        ("Product C", 20),
        ("Product D", 10)
    ]
    colors = ["#5B8FF9", "#5AD8A6", "#F6BD16", "#E8684A"]
    explode_index = 0  # Highlight first segment
    explode_distance = 0.5
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
        title = Text("Revenue Breakdown", font_size=36)
        title.to_edge(UP, buff=0.5)
        
        with self.voiceover(text="Here's our revenue breakdown by product.") as tracker:
            self.play(FadeIn(title), run_time=1)
        
        self.wait(0.5)
        
        # Create pie chart elements
        chart_group = self.create_pie_chart()
        chart_group.move_to(ORIGIN)
        
        sectors = chart_group[0]
        labels = chart_group[1]
        
        # Animate segments appearing one by one
        with self.voiceover(text="Each segment appears in sequence.") as tracker:
            for i, (sector, label) in enumerate(zip(sectors, labels)):
                label_text, value = self.data[i]
                
                self.play(
                    GrowFromCenter(sector),
                    FadeIn(label),
                    run_time=0.8
                )
                self.wait(0.2)
        
        self.wait(0.5)
        
        # Explode segment if configured
        if self.explode_index is not None and 0 <= self.explode_index < len(sectors):
            sector = sectors[self.explode_index]
            label = labels[self.explode_index]
            label_text, value = self.data[self.explode_index]
            
            # Calculate explosion direction
            start_angle = sum((self.data[j][1] / sum(v for _, v in self.data)) * TAU 
                            for j in range(self.explode_index))
            angle_width = (self.data[self.explode_index][1] / sum(v for _, v in self.data)) * TAU
            mid_angle = start_angle + angle_width / 2
            
            explode_x = self.explode_distance * np.cos(mid_angle)
            explode_y = self.explode_distance * np.sin(mid_angle)
            
            with self.voiceover(text=f"{label_text} is our largest segment at {value} percent.") as tracker:
                self.play(
                    sector.animate.shift([explode_x, explode_y, 0]),
                    label.animate.shift([explode_x, explode_y, 0]),
                    run_time=0.8
                )
                
                # Highlight with glow effect
                highlight = SurroundingRectangle(VGroup(sector, label), 
                                                color=YELLOW, 
                                                buff=0.3,
                                                stroke_width=3)
                self.play(Create(highlight))
                self.wait(0.5)
                self.play(FadeOut(highlight))
        
        self.wait(2)
        
        with self.voiceover(text="Staggered animation helps viewers process each segment.") as tracker:
            self.wait(1)
        
        self.play(FadeOut(title), FadeOut(chart_group))
    
    def create_pie_chart(self):
        """Create a pie chart from self.data"""
        total = sum(value for _, value in self.data)
        angles = [(value / total) * TAU for _, value in self.data]
        
        sectors = VGroup()
        labels = VGroup()
        
        start_angle = 0
        for i, ((label_text, value), angle) in enumerate(zip(self.data, angles)):
            sector = Sector(
                start_angle=start_angle,
                angle=angle,
                radius=2.5,
                fill_color=self.colors[i % len(self.colors)],
                fill_opacity=0.8,
                stroke_color=WHITE,
                stroke_width=2
            )
            sectors.add(sector)
            
            mid_angle = start_angle + angle / 2
            label_radius = 3.3
            label_x = label_radius * np.cos(mid_angle)
            label_y = label_radius * np.sin(mid_angle)
            
            percentage = int((value / total) * 100)
            label = Text(f"{label_text}\n{percentage}%", font_size=18)
            label.move_to([label_x, label_y, 0])
            labels.add(label)
            
            start_angle += angle
        
        chart = VGroup(sectors, labels)
        return chart


class PieToBarTransition(VoiceoverScene):
    """
    Morph between pie chart and bar chart to show data transformation.
    
    Configurable:
        data: List of (label, value) tuples
        pie_colors: Colors for pie chart
        bar_color: Color for bar chart
        animation_duration: Total animation time
    """
    
    data = [
        ("Q1", 25),
        ("Q2", 35),
        ("Q3", 20),
        ("Q4", 20)
    ]
    pie_colors = [BLUE, GREEN, YELLOW, ORANGE]
    bar_color = BLUE
    animation_duration = 12
    
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
        title = Text("Quarterly Comparison", font_size=36)
        title.to_edge(UP, buff=0.5)
        
        with self.voiceover(text="Let's compare quarterly performance.") as tracker:
            self.play(FadeIn(title), run_time=1)
        
        self.wait(0.5)
        
        # Create pie chart
        pie_chart = self.create_pie_chart()
        pie_chart.move_to(ORIGIN)
        
        with self.voiceover(text="First, as a pie chart showing proportions.") as tracker:
            self.play(FadeIn(pie_chart), run_time=1.5)
        
        self.wait(1)
        
        # Create bar chart
        bar_chart = self.create_bar_chart()
        bar_chart.move_to(ORIGIN)
        
        # Transform pie to bar
        with self.voiceover(text="Now let's transform this to a bar chart for absolute comparison.") as tracker:
            self.play(
                FadeOut(pie_chart),
                FadeIn(bar_chart),
                run_time=2
            )
        
        self.wait(1)
        
        # Animate bars growing
        bars = bar_chart[1]  # The bars
        labels = bar_chart[2]  # The labels
        
        with self.voiceover(text="Bars make it easier to compare absolute values.") as tracker:
            for bar, label in zip(bars, labels):
                self.play(
                    GrowFromEdge(bar, DOWN),
                    run_time=0.6
                )
        
        self.wait(1)
        
        # Highlight max value
        max_value = max(value for _, value in self.data)
        max_index = [value for _, value in self.data].index(max_value)
        max_bar = bars[max_index]
        
        highlight = SurroundingRectangle(max_bar, color=YELLOW, buff=0.1)
        
        with self.voiceover(text="Quarter two shows the strongest performance.") as tracker:
            self.play(Create(highlight))
            self.wait(1)
            self.play(FadeOut(highlight))
        
        self.wait(2)
        
        with self.voiceover(text="Different chart types reveal different insights.") as tracker:
            self.wait(1)
        
        self.play(FadeOut(title), FadeOut(bar_chart))
    
    def create_pie_chart(self):
        """Create a pie chart from self.data"""
        total = sum(value for _, value in self.data)
        angles = [(value / total) * TAU for _, value in self.data]
        
        sectors = VGroup()
        labels = VGroup()
        
        start_angle = 0
        for i, ((label_text, value), angle) in enumerate(zip(self.data, angles)):
            sector = Sector(
                start_angle=start_angle,
                angle=angle,
                radius=2.5,
                fill_color=self.pie_colors[i % len(self.pie_colors)],
                fill_opacity=0.8,
                stroke_color=WHITE,
                stroke_width=2
            )
            sectors.add(sector)
            
            mid_angle = start_angle + angle / 2
            label_radius = 3.2
            label_x = label_radius * np.cos(mid_angle)
            label_y = label_radius * np.sin(mid_angle)
            
            label = Text(label_text, font_size=20)
            label.move_to([label_x, label_y, 0])
            labels.add(label)
            
            start_angle += angle
        
        chart = VGroup(sectors, labels)
        return chart
    
    def create_bar_chart(self):
        """Create a bar chart from self.data"""
        labels = [d[0] for d in self.data]
        values = [d[1] for d in self.data]
        max_value = max(values)
        
        # Create axes
        axes = Axes(
            x_range=[0, len(values) + 1, 1],
            y_range=[0, max_value * 1.2, max_value / 4],
            x_length=10,
            y_length=5,
            axis_config={"include_numbers": True}
        )
        
        axes.x_axis.numbers.set_opacity(0)
        
        # Create bars
        bars = VGroup()
        bar_labels = VGroup()
        
        for i, (label_text, value) in enumerate(self.data):
            bar_height = (value / max_value) * axes.y_length * 0.8
            bar = Rectangle(
                width=0.8,
                height=bar_height,
                fill_color=self.bar_color,
                fill_opacity=0.8,
                stroke_width=1
            )
            
            x_pos = axes.c2p(i + 1, 0)[0]
            y_pos = axes.c2p(0, 0)[1] + bar_height / 2
            bar.move_to([x_pos, y_pos, 0])
            
            bars.add(bar)
            
            label = Text(label_text, font_size=20)
            label.next_to(bar, DOWN, buff=0.3)
            bar_labels.add(label)
        
        chart = VGroup(axes, bars, bar_labels)
        return chart


if __name__ == "__main__":
    config.quality = "high_quality"
    scene = BasicPieChart()
    scene.render()
