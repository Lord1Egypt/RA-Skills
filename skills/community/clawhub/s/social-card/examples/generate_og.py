"""ClawHub example — generate an OG image."""
from social_card import SocialCard

SocialCard("og").title("Hello World").subtitle("My first social card").render("og.png")
