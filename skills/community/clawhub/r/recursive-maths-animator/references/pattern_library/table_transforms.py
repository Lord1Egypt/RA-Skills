"""
Table to Bar Chart Animation Pattern
AutoAgent-trained: Table transforms to animated bar chart
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "references"))

from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService


class TableToBarChartPattern(VoiceoverScene):
    """
    Transform a data table into an animated bar chart.
    
    Configurable:
        data: List of (label, value) tuples
        bar_colors: List of colors for bars
        bar_width: Width of each bar
        animation_duration: Total animation time
    """
    
    data = [
        ("Q1", 2500),
        ("Q2", 3200),
        ("Q3", 2800),
        ("Q4", 4100)
    ]
    bar_colors = [BLUE, GREEN, YELLOW, RED]
    bar_width = 0.8
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
        title = Text("Quarterly Sales", font_size=36)
        title.to_edge(UP, buff=0.5)
        
        with self.voiceover(text="Let's look at the quarterly sales data.") as tracker:
            self.play(FadeIn(title), run_time=1)
        
        self.wait(0.5)
        
        # Create table
        table = self.create_table()
        table.next_to(title, DOWN, buff=1)
        
        with self.voiceover(text="Here's the data in table format.") as tracker:
            self.play(Create(table), run_time=2)
        
        self.wait(1)
        
        # Create bar chart
        chart = self.create_bar_chart()
        chart.next_to(title, DOWN, buff=1)
        chart.align_to(table, DOWN)
        
        # Transform table to chart
        with self.voiceover(text="Now let's see this as a bar chart.") as tracker:
            self.play(
                FadeOut(table),
                FadeIn(chart),
                run_time=2
            )
        
        self.wait(1)
        
        # Animate bars growing
        bars = chart[0]  # The bars group
        with self.voiceover(text="The bars represent the sales values.") as tracker:
            for i, bar in enumerate(bars):
                self.play(
                    GrowFromEdge(bar, DOWN),
                    run_time=0.5
                )
        
        self.wait(2)
        
        with self.voiceover(text="This makes the trends much clearer.") as tracker:
            self.wait(1)
        
        self.play(FadeOut(title), FadeOut(chart))
    
    def create_table(self):
        """Create a table from self.data using Text (no LaTeX required)"""
        # Create table manually with Text objects
        col1_label = Text("Quarter", font_size=28, weight=BOLD)
        col2_label = Text("Sales", font_size=28, weight=BOLD)
        
        header = VGroup(col1_label, col2_label)
        header.arrange(RIGHT, buff=2)
        
        rows = VGroup()
        for label, value in self.data:
            row_label = Text(label, font_size=24)
            row_value = Text(str(value), font_size=24)
            row = VGroup(row_label, row_value)
            row.arrange(RIGHT, buff=2)
            rows.add(row)
        
        rows.arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        
        # Combine header and rows
        table = VGroup(header, rows)
        table.arrange(DOWN, buff=0.5)
        
        # Add border
        border = SurroundingRectangle(table, buff=0.3, stroke_width=2)
        table.add(border)
        
        return table
    
    def create_bar_chart(self):
        """Create a bar chart from self.data"""
        # Extract values
        labels = [d[0] for d in self.data]
        values = [d[1] for d in self.data]
        max_value = max(values)
        
        # Create axes
        axes = Axes(
            x_range=[0, len(values) + 1, 1],
            y_range=[0, max_value * 1.2, max_value / 5],
            x_length=8,
            y_length=5,
            axis_config={"include_numbers": True}
        )
        
        # Hide x-axis numbers, we'll add custom labels
        axes.x_axis.numbers.set_opacity(0)
        
        # Create bars
        bars = VGroup()
        bar_width = self.bar_width
        
        for i, (label, value) in enumerate(self.data):
            # Create bar
            bar_height = (value / max_value) * axes.y_length * 0.8
            bar = Rectangle(
                width=bar_width,
                height=bar_height,
                fill_color=self.bar_colors[i % len(self.bar_colors)],
                fill_opacity=0.8,
                stroke_width=1
            )
            
            # Position bar
            x_pos = axes.c2p(i + 1, 0)[0]
            y_pos = axes.c2p(0, 0)[1] + bar_height / 2
            bar.move_to([x_pos, y_pos, 0])
            
            bars.add(bar)
            
            # Add label
            label_text = Text(label, font_size=24)
            label_text.next_to(bar, DOWN, buff=0.3)
            bars.add(label_text)
            
            # Add value label
            value_text = Text(str(value), font_size=20)
            value_text.next_to(bar, UP, buff=0.2)
            bars.add(value_text)
        
        chart = VGroup(axes, bars)
        return chart


class TableToLineGraphPattern(VoiceoverScene):
    """
    Transform a data table into an animated line graph.
    
    Configurable:
        data: List of (label, value) tuples
        line_color: Color for the line
        show_points: Whether to show data points
        animation_duration: Total animation time
    """
    
    data = [
        ("Jan", 100),
        ("Feb", 150),
        ("Mar", 120),
        ("Apr", 200),
        ("May", 180),
        ("Jun", 250)
    ]
    line_color = BLUE
    show_points = True
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
        title = Text("Monthly Trends", font_size=36)
        title.to_edge(UP, buff=0.5)
        
        with self.voiceover(text="Let's analyze the monthly trends.") as tracker:
            self.play(FadeIn(title), run_time=1)
        
        self.wait(0.5)
        
        # Create table
        table = self.create_table()
        table.next_to(title, DOWN, buff=1)
        
        with self.voiceover(text="Here's our data table.") as tracker:
            self.play(Create(table), run_time=2)
        
        self.wait(1)
        
        # Create line graph
        graph = self.create_line_graph()
        graph.next_to(title, DOWN, buff=1)
        
        # Transform table to graph
        with self.voiceover(text="Now as a line graph to see the trend.") as tracker:
            self.play(
                FadeOut(table),
                FadeIn(graph),
                run_time=2
            )
        
        self.wait(1)
        
        # Animate line drawing
        line = graph[1]  # The line
        points = graph[2]  # The points
        
        with self.voiceover(text="The line shows how values change over time.") as tracker:
            self.play(Create(line), run_time=2)
            
            if self.show_points:
                self.play(LaggedStart(*[Create(p) for p in points], lag_ratio=0.2))
        
        self.wait(2)
        
        with self.voiceover(text="Trends become much clearer this way.") as tracker:
            self.wait(1)
        
        self.play(FadeOut(title), FadeOut(graph))
    
    def create_table(self):
        """Create a table from self.data"""
        col1_label = Text("Month", font_size=28, weight=BOLD)
        col2_label = Text("Value", font_size=28, weight=BOLD)
        
        header = VGroup(col1_label, col2_label)
        header.arrange(RIGHT, buff=2)
        
        rows = VGroup()
        for label, value in self.data:
            row_label = Text(label, font_size=24)
            row_value = Text(str(value), font_size=24)
            row = VGroup(row_label, row_value)
            row.arrange(RIGHT, buff=2)
            rows.add(row)
        
        rows.arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        
        table = VGroup(header, rows)
        table.arrange(DOWN, buff=0.5)
        
        border = SurroundingRectangle(table, buff=0.3, stroke_width=2)
        table.add(border)
        
        return table
    
    def create_line_graph(self):
        """Create a line graph from self.data"""
        labels = [d[0] for d in self.data]
        values = [d[1] for d in self.data]
        max_value = max(values)
        min_value = min(values)
        
        # Create axes
        axes = Axes(
            x_range=[0, len(values) + 1, 1],
            y_range=[min_value * 0.8, max_value * 1.2, (max_value - min_value) / 4],
            x_length=10,
            y_length=5,
            axis_config={"include_numbers": True}
        )
        
        axes.x_axis.numbers.set_opacity(0)
        
        # Create line points
        points = []
        for i, (label, value) in enumerate(self.data):
            x = i + 1
            y = value
            point = axes.c2p(x, y)
            points.append(point)
            
            # Add label
            label_text = Text(label, font_size=20)
            label_text.next_to(axes.c2p(x, 0), DOWN, buff=0.3)
            axes.add(label_text)
        
        # Create line
        line = VMobject()
        line.set_points_as_corners(points)
        line.set_stroke(self.line_color, width=3)
        
        # Create dots at each point
        dots = VGroup()
        for point in points:
            dot = Dot(point, color=self.line_color, radius=0.1)
            dots.add(dot)
        
        graph = VGroup(axes, line, dots)
        return graph


class TableToScatterPlotPattern(VoiceoverScene):
    """
    Transform a data table into a scatter plot with optional trend line.
    
    Configurable:
        data: List of (x, y) tuples
        point_color: Color for data points
        show_trend_line: Whether to show trend line
        animation_duration: Total animation time
    """
    
    data = [
        (1, 2),
        (2, 3),
        (3, 5),
        (4, 4),
        (5, 7),
        (6, 6),
        (7, 8)
    ]
    point_color = GREEN
    show_trend_line = True
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
        title = Text("Correlation Analysis", font_size=36)
        title.to_edge(UP, buff=0.5)
        
        with self.voiceover(text="Let's examine the relationship between variables.") as tracker:
            self.play(FadeIn(title), run_time=1)
        
        self.wait(0.5)
        
        # Create table
        table = self.create_table()
        table.next_to(title, DOWN, buff=1)
        
        with self.voiceover(text="Here's our data table with X and Y values.") as tracker:
            self.play(Create(table), run_time=2)
        
        self.wait(1)
        
        # Create scatter plot
        plot = self.create_scatter_plot()
        plot.next_to(title, DOWN, buff=1)
        
        # Transform table to plot
        with self.voiceover(text="Now as a scatter plot to see the correlation.") as tracker:
            self.play(
                FadeOut(table),
                FadeIn(plot),
                run_time=2
            )
        
        self.wait(1)
        
        # Animate points appearing
        points = plot[1]  # The points
        trend_line = plot[2] if self.show_trend_line else None
        
        with self.voiceover(text="Each point represents one data pair.") as tracker:
            self.play(LaggedStart(*[GrowFromCenter(p) for p in points], lag_ratio=0.15))
        
        # Show trend line if enabled
        if trend_line:
            with self.voiceover(text="The trend line shows the overall pattern.") as tracker:
                self.play(Create(trend_line), run_time=1.5)
        
        self.wait(2)
        
        with self.voiceover(text="Scatter plots reveal correlations clearly.") as tracker:
            self.wait(1)
        
        self.play(FadeOut(title), FadeOut(plot))
    
    def create_table(self):
        """Create a table from self.data"""
        col1_label = Text("X Value", font_size=28, weight=BOLD)
        col2_label = Text("Y Value", font_size=28, weight=BOLD)
        
        header = VGroup(col1_label, col2_label)
        header.arrange(RIGHT, buff=2)
        
        rows = VGroup()
        for x, y in self.data:
            row_x = Text(str(x), font_size=24)
            row_y = Text(str(y), font_size=24)
            row = VGroup(row_x, row_y)
            row.arrange(RIGHT, buff=2)
            rows.add(row)
        
        rows.arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        
        table = VGroup(header, rows)
        table.arrange(DOWN, buff=0.5)
        
        border = SurroundingRectangle(table, buff=0.3, stroke_width=2)
        table.add(border)
        
        return table
    
    def create_scatter_plot(self):
        """Create a scatter plot from self.data"""
        x_values = [d[0] for d in self.data]
        y_values = [d[1] for d in self.data]
        
        x_min, x_max = min(x_values), max(x_values)
        y_min, y_max = min(y_values), max(y_values)
        
        # Create axes
        axes = Axes(
            x_range=[x_min - 1, x_max + 1, 1],
            y_range=[y_min - 1, y_max + 1, 1],
            x_length=10,
            y_length=6,
            axis_config={"include_numbers": True}
        )
        
        # Create points
        points = VGroup()
        for x, y in self.data:
            point = Dot(axes.c2p(x, y), color=self.point_color, radius=0.1)
            points.add(point)
        
        # Create trend line if enabled
        trend_line = None
        if self.show_trend_line and len(self.data) > 1:
            # Simple linear regression
            n = len(self.data)
            sum_x = sum(x_values)
            sum_y = sum(y_values)
            sum_xy = sum(x * y for x, y in self.data)
            sum_x2 = sum(x * x for x in x_values)
            
            slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
            intercept = (sum_y - slope * sum_x) / n
            
            # Calculate trend line points
            x_trend_min = x_min - 0.5
            x_trend_max = x_max + 0.5
            y_trend_min = slope * x_trend_min + intercept
            y_trend_max = slope * x_trend_max + intercept
            
            trend_line = Line(
                axes.c2p(x_trend_min, y_trend_min),
                axes.c2p(x_trend_max, y_trend_max),
                color=YELLOW,
                stroke_width=2
            )
        
        if trend_line:
            plot = VGroup(axes, points, trend_line)
        else:
            plot = VGroup(axes, points)
        
        return plot


if __name__ == "__main__":
    config.quality = "high_quality"
    scene = TableToBarChartPattern()
    scene.render()
