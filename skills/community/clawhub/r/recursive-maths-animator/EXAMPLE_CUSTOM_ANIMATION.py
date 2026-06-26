"""
Example: Customized Quarterly Report Animation
Based on TableToBarChartPattern from the library
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "references"))

from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService


class MyQuarterlyReport(VoiceoverScene):
    """
    Customized animation for quarterly sales report.
    Modify the data and styling below for your needs.
    """
    
    # ✏️ CUSTOMIZE: Your data here
    data = [
        ("Jan", 45000),
        ("Feb", 52000),
        ("Mar", 48000),
        ("Apr", 61000),
        ("May", 58000),
        ("Jun", 67000)
    ]
    
    # ✏️ CUSTOMIZE: Your colors here (hex or Manim constants)
    bar_colors = ["#3498db", "#2ecc71", "#f1c40f", "#e74c3c", "#9b59b6", "#1abc9c"]
    
    # ✏️ CUSTOMIZE: Animation speed
    animation_duration = 12  # seconds
    
    def __init__(self, **kwargs):
        config.pixel_width = 1920
        config.pixel_height = 1080
        config.frame_width = 14
        config.frame_height = 8
        config.frame_rate = 60
        
        super().__init__(**kwargs)
        self.set_speech_service(GTTSService(lang='en'))
    
    def construct(self):
        # Title - ✏️ CUSTOMIZE: Your title
        title = Text("H1 2024 Sales Report", font_size=40, color="#2c3e50")
        title.to_edge(UP, buff=0.5)
        
        with self.voiceover(text="Here's our first half 2024 sales performance.") as tracker:
            self.play(FadeIn(title), run_time=1)
        
        self.wait(0.5)
        
        # Create table
        table = self.create_table()
        table.next_to(title, DOWN, buff=1)
        
        with self.voiceover(text="Starting with the raw numbers.") as tracker:
            self.play(Create(table), run_time=2)
        
        self.wait(1)
        
        # Create bar chart
        chart = self.create_bar_chart()
        chart.next_to(title, DOWN, buff=1)
        
        # Transform
        with self.voiceover(text="And now visualized as a bar chart.") as tracker:
            self.play(
                FadeOut(table),
                FadeIn(chart),
                run_time=2
            )
        
        # Animate bars
        bars = chart[0]
        with self.voiceover(text="Notice the strong growth in April and June.") as tracker:
            for bar in bars:
                self.play(GrowFromEdge(bar, DOWN), run_time=0.6)
        
        self.wait(2)
        
        # ✏️ CUSTOMIZE: Add more animations here
        # Example: Highlight best month
        best_month_idx = 5  # June
        best_bar = bars[best_month_idx]
        highlight = SurroundingRectangle(best_bar, color=YELLOW, buff=0.1)
        
        with self.voiceover(text="June was our best month.") as tracker:
            self.play(Create(highlight))
            self.wait(1)
            self.play(FadeOut(highlight))
        
        self.wait(1)
        
        with self.voiceover(text="Overall strong first half performance.") as tracker:
            self.wait(1)
        
        self.play(FadeOut(title), FadeOut(chart))
    
    def create_table(self):
        """Create data table"""
        col1 = Text("Month", font_size=28, weight=BOLD)
        col2 = Text("Sales", font_size=28, weight=BOLD)
        
        header = VGroup(col1, col2)
        header.arrange(RIGHT, buff=2.5)
        
        rows = VGroup()
        for month, sales in self.data:
            row_month = Text(month, font_size=24)
            row_sales = Text(f"${sales:,}", font_size=24)
            row = VGroup(row_month, row_sales)
            row.arrange(RIGHT, buff=2.5)
            rows.add(row)
        
        rows.arrange(DOWN, buff=0.6, aligned_edge=LEFT)
        
        table = VGroup(header, rows)
        table.arrange(DOWN, buff=0.6)
        
        border = SurroundingRectangle(table, buff=0.3, stroke_width=2)
        table.add(border)
        
        return table
    
    def create_bar_chart(self):
        """Create bar chart"""
        labels = [d[0] for d in self.data]
        values = [d[1] for d in self.data]
        max_value = max(values)
        
        axes = Axes(
            x_range=[0, len(values) + 1, 1],
            y_range=[0, max_value * 1.2, max_value / 5],
            x_length=10,
            y_length=5,
            axis_config={"include_numbers": False}
        )
        
        axes.x_axis.numbers.set_opacity(0)
        
        bars = VGroup()
        bar_labels = VGroup()
        
        for i, (label, value) in enumerate(self.data):
            bar_height = (value / max_value) * axes.y_length * 0.8
            bar = Rectangle(
                width=0.9,
                height=bar_height,
                fill_color=self.bar_colors[i % len(self.bar_colors)],
                fill_opacity=0.85,
                stroke_width=1
            )
            
            x_pos = axes.c2p(i + 1, 0)[0]
            y_pos = axes.c2p(0, 0)[1] + bar_height / 2
            bar.move_to([x_pos, y_pos, 0])
            
            bars.add(bar)
            
            label_text = Text(label, font_size=22)
            label_text.next_to(bar, DOWN, buff=0.3)
            bar_labels.add(label_text)
            
            # Value label on top
            value_text = Text(f"${value/1000:.0f}k", font_size=18)
            value_text.next_to(bar, UP, buff=0.2)
            bar_labels.add(value_text)
        
        chart = VGroup(axes, bars, bar_labels)
        return chart


if __name__ == "__main__":
    # ✏️ CUSTOMIZE: Quality settings
    # -ql = low quality (fast, for testing)
    # -qm = medium quality
    # -qh = high quality (slow, for final)
    
    config.quality = "medium_quality"
    scene = MyQuarterlyReport()
    scene.render()
