"""Small static SVG chart renderer for the GitLab agent profile."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from html import escape
from typing import Iterable


@dataclass(frozen=True)
class MonthStats:
    month: str
    owner_mrs: int
    agent_with_owner: int
    agent_autonomous: int
    direct_owner_main: int
    owner_mr_points: int = 0
    agent_with_owner_points: int = 0
    agent_autonomous_points: int = 0

    @property
    def merged_total(self) -> int:
        return self.owner_mrs + self.agent_with_owner + self.agent_autonomous

    @property
    def mr_points(self) -> int:
        return self.owner_mr_points + self.agent_with_owner_points + self.agent_autonomous_points

    @property
    def contribution_score(self) -> float:
        return self.mr_points + self.direct_owner_main * 0.2


class ProfileDeliveryChart:
    width = 1280
    height = 720
    margin_left = 86
    margin_right = 58
    margin_top = 84
    margin_bottom = 126
    colors = {
        "owner": "#315f72",
        "agent_with_owner": "#e07a2f",
        "agent_autonomous": "#7a4ea3",
        "direct": "#6a994e",
        "score": "#c1292e",
        "grid": "#dce3e8",
        "text": "#1f2933",
        "muted": "#637381",
    }

    def __init__(self, months: Iterable[MonthStats], owner: str, agent: str) -> None:
        self.months = list(months)
        self.owner = owner
        self.agent = agent

    @staticmethod
    def month_label(month: str) -> str:
        return datetime.strptime(month, "%Y-%m").strftime("%b %Y")

    def render(self) -> str:
        max_count = max(
            [1]
            + [
                max(
                    month.owner_mrs,
                    month.agent_with_owner,
                    month.agent_autonomous,
                    month.direct_owner_main,
                    month.merged_total,
                )
                for month in self.months
            ]
        )
        max_score = max([1.0] + [month.contribution_score for month in self.months])
        plot_width = self.width - self.margin_left - self.margin_right
        plot_height = self.height - self.margin_top - self.margin_bottom
        group_width = plot_width / max(1, len(self.months))
        bar_width = min(18, group_width / 7)

        svg: list[str] = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.width}" height="{self.height}" viewBox="0 0 {self.width} {self.height}" role="img" aria-labelledby="title desc">',
            "<title id=\"title\">GitLab agent contribution performance</title>",
            "<desc id=\"desc\">Monthly delivery chart for merged merge requests, direct owner commits to main, and a weighted contribution score.</desc>",
            "<defs>",
            "<linearGradient id=\"background\" x1=\"0\" x2=\"1\" y1=\"0\" y2=\"1\"><stop offset=\"0\" stop-color=\"#f8fbfc\"/><stop offset=\"1\" stop-color=\"#eef4f2\"/></linearGradient>",
            "<filter id=\"shadow\" x=\"-10%\" y=\"-10%\" width=\"120%\" height=\"130%\"><feDropShadow dx=\"0\" dy=\"8\" stdDeviation=\"10\" flood-color=\"#1f2933\" flood-opacity=\"0.13\"/></filter>",
            "</defs>",
            f'<rect width="{self.width}" height="{self.height}" rx="22" fill="url(#background)"/>',
            f'<rect x="36" y="32" width="{self.width - 72}" height="{self.height - 70}" rx="18" fill="#ffffff" filter="url(#shadow)"/>',
            f'<text x="{self.margin_left}" y="68" font-family="Inter, Arial, sans-serif" font-size="30" font-weight="700" fill="{self.colors["text"]}">Contribution Performance</text>',
            f'<text x="{self.margin_left}" y="100" font-family="Inter, Arial, sans-serif" font-size="15" fill="{self.colors["muted"]}">Merged work by {escape(self.owner)} and {escape(self.agent)}, plus direct owner commits to main</text>',
        ]

        for tick in range(0, 6):
            value = max_count * tick / 5
            y = self.margin_top + plot_height - (plot_height * tick / 5)
            svg.append(
                f'<line x1="{self.margin_left}" y1="{y:.1f}" x2="{self.margin_left + plot_width}" y2="{y:.1f}" stroke="{self.colors["grid"]}" stroke-width="1"/>'
            )
            svg.append(
                f'<text x="{self.margin_left - 18}" y="{y + 5:.1f}" text-anchor="end" font-family="Inter, Arial, sans-serif" font-size="12" fill="{self.colors["muted"]}">{value:.0f}</text>'
            )

        def count_y(value: float) -> float:
            return self.margin_top + plot_height - (value / max_count * plot_height)

        def score_y(value: float) -> float:
            return self.margin_top + plot_height - (value / max_score * plot_height)

        score_points = []
        for index, month in enumerate(self.months):
            center = self.margin_left + group_width * index + group_width / 2
            values = [
                ("owner", month.owner_mrs, -1.65),
                ("agent_with_owner", month.agent_with_owner, -0.55),
                ("agent_autonomous", month.agent_autonomous, 0.55),
                ("direct", month.direct_owner_main, 1.65),
            ]
            for key, value, offset in values:
                height = 0 if max_count == 0 else value / max_count * plot_height
                x = center + offset * bar_width
                y = self.margin_top + plot_height - height
                svg.append(
                    f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_width:.1f}" height="{height:.1f}" rx="4" fill="{self.colors[key]}"/>'
                )
                if value > 0:
                    label_y = y - 6 if height >= 18 else y - 3
                    svg.append(
                        f'<text x="{x + bar_width / 2:.1f}" y="{label_y:.1f}" text-anchor="middle" font-family="Inter, Arial, sans-serif" font-size="10" font-weight="700" fill="{self.colors["text"]}">{value}</text>'
                    )
            score_points.append((center, score_y(month.contribution_score)))
            svg.append(
                f'<text x="{center:.1f}" y="{self.margin_top + plot_height + 26}" text-anchor="middle" font-family="Inter, Arial, sans-serif" font-size="11" fill="{self.colors["muted"]}" transform="rotate(-35 {center:.1f} {self.margin_top + plot_height + 26})">{escape(self.month_label(month.month))}</text>'
            )

        if len(score_points) > 1:
            path = " ".join(
                f'{"M" if index == 0 else "L"} {x:.1f} {y:.1f}'
                for index, (x, y) in enumerate(score_points)
            )
            svg.append(
                f'<path d="{path}" fill="none" stroke="{self.colors["score"]}" stroke-width="4" stroke-linejoin="round" stroke-linecap="round"/>'
            )
        for x, y in score_points:
            svg.append(
                f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5.5" fill="#ffffff" stroke="{self.colors["score"]}" stroke-width="3"/>'
            )

        svg.append(
            f'<line x1="{self.margin_left}" y1="{self.margin_top + plot_height}" x2="{self.margin_left + plot_width}" y2="{self.margin_top + plot_height}" stroke="#9aa8b2" stroke-width="1.5"/>'
        )
        svg.append(
            f'<line x1="{self.margin_left}" y1="{self.margin_top}" x2="{self.margin_left}" y2="{self.margin_top + plot_height}" stroke="#9aa8b2" stroke-width="1.5"/>'
        )

        legend = [
            ("owner", "Owner MRs"),
            ("agent_with_owner", "Agent + reviewer MRs"),
            ("agent_autonomous", "Agent MRs (autonomous)"),
            ("direct", "Direct owner commits"),
            ("score", "Contribution score"),
        ]
        legend_y = self.height - 66
        legend_x = self.margin_left
        for key, label in legend:
            svg.append(
                f'<rect x="{legend_x}" y="{legend_y - 12}" width="18" height="12" rx="3" fill="{self.colors[key]}"/>'
            )
            svg.append(
                f'<text x="{legend_x + 26}" y="{legend_y - 2}" font-family="Inter, Arial, sans-serif" font-size="13" fill="{self.colors["text"]}">{escape(label)}</text>'
            )
            legend_x += 54 + len(label) * 7

        latest = self.months[-1]
        svg.append(
            f'<text x="{self.width - self.margin_right}" y="70" text-anchor="end" font-family="Inter, Arial, sans-serif" font-size="24" font-weight="700" fill="{self.colors["score"]}">{latest.contribution_score:.1f}</text>'
        )
        svg.append(
            f'<text x="{self.width - self.margin_right}" y="94" text-anchor="end" font-family="Inter, Arial, sans-serif" font-size="13" fill="{self.colors["muted"]}">latest contribution score</text>'
        )
        svg.append("</svg>")
        return "\n".join(svg) + "\n"
