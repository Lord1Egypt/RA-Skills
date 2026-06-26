"""Cyberpunk theme matching the RedditRank web UI."""

from textual.theme import Theme

cyberpunk = Theme(
    name="cyberpunk",
    primary="#00f0ff",
    secondary="#b967ff",
    accent="#ff4500",
    foreground="#e8e6f0",
    background="#0a0a12",
    success="#39ff14",
    warning="#f9f002",
    error="#ff003c",
    surface="#1a1a2e",
    panel="#16213e",
    dark=True,
    variables={
        "block-cursor-text-style": "bold",
        "block-cursor-background": "#ff4500",
        "block-cursor-foreground": "#0a0a12",
        "footer-key-foreground": "#00f0ff",
        "footer-description-foreground": "#8b8696",
        "footer-background": "#0a0a12",
        "input-cursor-background": "#00f0ff",
        "input-selection-background": "#b967ff 35%",
        "scrollbar": "#b967ff 40%",
        "scrollbar-hover": "#b967ff 70%",
        "scrollbar-active": "#00f0ff",
        "border": "#00f0ff 50%",
    },
)
