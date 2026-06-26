#!/usr/bin/env python3
"""
X Algorithm Post Evaluator

Usage: python evaluate_post.py "Your post text here" [--video] [--duration 10] [--has-media]

This script evaluates a post draft against the X For You algorithm optimization criteria
from the x-algorithm-optimization skill and provides actionable feedback.
"""

import sys
import re
from dataclasses import dataclass
from typing import List, Tuple, Dict


@dataclass
class PostEvaluation:
    """Results of post evaluation."""
    score: int  # 0-100 overall score
    strengths: List[str]
    weaknesses: List[str]
    recommendations: List[str]
    engagement_potential: Dict[str, int]  # engagement type -> 0-10 score
    estimated_next_actions: List[str]


class XAlgorithmEvaluator:
    """Evaluates X posts based on algorithm insights."""

    # Engagement types and their relative weights (normalized)
    ENGAGEMENT_WEIGHTS = {
        'reply': 10,
        'quote': 9,
        'retweet': 8,
        'share': 7,
        'video_view': 7,
        'dwell': 6,
        'follow': 6,
        'click': 4,
        'profile_click': 4,
        'photo_expand': 4,
        'favorite': 3,
        'negative': -10,  # blocks, mutes, reports
    }

    def __init__(self, post_text: str, has_video: bool = False, video_duration: int = 0, has_media: bool = False):
        self.post_text = post_text.strip()
        self.has_video = has_video
        self.video_duration = video_duration
        self.has_media = has_media

    def evaluate(self) -> PostEvaluation:
        """Run full evaluation."""
        strengths = []
        weaknesses = []
        recommendations = []
        engagement = {k: 0 for k in self.ENGAGEMENT_WEIGHTS.keys()}

        # Length analysis
        char_count = len(self.post_text)
        word_count = len(self.post_text.split())

        if 200 <= char_count <= 500:
            strengths.append("Optimal length (200-500 chars) for dwell time")
            engagement['dwell'] += 3
        elif char_count < 50:
            weaknesses.append("Too short - may not provide enough value")
            recommendations.append("Add more substance or context")
            engagement['dwell'] -= 2
        elif char_count > 500:
            weaknesses.append("May be too long for mobile feed")
            recommendations.append("Consider breaking into threads")

        # Hook analysis (first 1-2 lines)
        first_line = self.post_text.split('\n')[0][:100]
        has_question = '?' in first_line
        has_hook_word = any(word in first_line.lower() for word in ['how', 'why', 'what', 'secret', 'trick', 'change', 'break', 'discover'])
        has_emotional = any(word in first_line.lower() for word in ['love', 'hate', 'angry', 'excited', 'shocking', 'unbelievable'])

        if has_question:
            strengths.append("Opening with a question encourages replies")
            engagement['reply'] += 3
        if has_hook_word:
            strengths.append("Contains curiosity-driving words")
            engagement['dwell'] += 2
        if has_emotional:
            strengths.append("Emotional trigger increases engagement likelihood")
            engagement['retweet'] += 2
            engagement['reply'] += 2

        # Call to action check
        cta_phrases = ['reply', 'comment', 'retweet', 'share', 'quote', 'thoughts?', 'agree?', 'what do you think']
        has_cta = any(phrase in self.post_text.lower() for phrase in cta_phrases)
        if has_cta:
            strengths.append("Explicit call-to-action present")
            engagement['reply'] += 2
            engagement['retweet'] += 2
        else:
            weaknesses.append("No clear call-to-action")
            recommendations.append("Add a subtle CTA: 'Reply with your thoughts' or 'RT if you agree'")

        # Tag analysis
        mentions = re.findall(r'@(\w+)', self.post_text)
        if 1 <= len(mentions) <= 2:
            strengths.append(f"Strategic mentions ({len(mentions)}) encourage profile clicks and replies")
            engagement['profile_click'] += 2
            engagement['reply'] += 1
        elif len(mentions) > 3:
            weaknesses.append("Too many @mentions may look spammy")
            recommendations.append("Limit to 1-2 relevant mentions")

        # Video analysis
        if self.has_video:
            if self.video_duration >= 2:
                strengths.append("Video duration qualifies for VQV weight")
                engagement['video_view'] += 4
            else:
                weaknesses.append("Video too short for VQV weight (< 2 seconds)")
                recommendations.append("Ensure native video is at least 2 seconds")
            strengths.append("Native video content favored by algorithm")
            engagement['dwell'] += 2
        else:
            # No video - check for media
            if self.has_media:
                strengths.append("Media (images) increase photo expand potential")
                engagement['photo_expand'] += 3
            else:
                weaknesses.append("No media - consider adding image or video")
                recommendations.append("Add relevant image or native video for higher engagement")

        # Controversy/scoring
        controversial_words = ['hot take', 'unpopular opinion', 'controversial', 'change my mind', 'debate', 'wrong']
        is_controversial = any(word in self.post_text.lower() for word in controversial_words)
        if is_controversial:
            strengths.append("Controversial angle encourages replies and quotes")
            engagement['reply'] += 3
            engagement['quote'] += 2
            weaknesses.append("Risk of negative signals if tone is aggressive")
            recommendations.append("Ensure controversial content is respectful, not hostile")

        # Value proposition
        value_indicators = ['free', 'save', 'earn', 'make', 'grow', 'increase', 'decrease', 'reduce', 'tips', 'guide', 'how to']
        has_value = sum(1 for word in value_indicators if word in self.post_text.lower()) >= 1
        if has_value:
            strengths.append("Clear value proposition")
            engagement['retweet'] += 2
            engagement['share'] += 2
        else:
            weaknesses.append("Missing clear value proposition")
            recommendations.append("Make the value explicit: what the audience gains")

        # Formatting
        has_line_breaks = '\n' in self.post_text
        has_emoji = bool(re.search(r'[\U00010000-\U0010ffff]', self.post_text))
        has_hashtags = '#' in self.post_text

        if has_line_breaks:
            strengths.append("Multi-line formatting improves readability")
            engagement['dwell'] += 1
        if has_emoji:
            strengths.append("Emojis increase visual appeal and emotional connection")
            engagement['favorite'] += 1
        if has_hashtags:
            strengths.append("Hashtags help topic categorization")
            # Minor impact on discovery, not directly on ML scoring

        # Check for spam signals
        spam_indicators = ['$$$', '!!!', 'ALL CAPS', 'make money fast', 'click here', 'free followers']
        is_spammy = any(indicator in self.post_text for indicator in spam_indicators)
        if is_spammy:
            weaknesses.append("Contains spam-like elements")
            engagement['negative'] -= 5
            recommendations.append("Remove excessive punctuation, ALL CAPS, and money symbols")

        # Check for self-promotion only
        self_promo_words = ['buy now', 'limited offer', 'sale', 'discount', 'promo', 'my product']
        is_overly_promotional = sum(1 for word in self_promo_words if word in self.post_text.lower()) >= 2
        if is_overly_promotional:
            weaknesses.append("Heavy self-promotion may trigger negative signals")
            engagement['negative'] -= 3
            recommendations.append("Balance promotion with value; follow 80/20 rule (80% value, 20% promotion)")

        # Calculate overall score
        positive_score = sum(v for k, v in engagement.items() if k != 'negative' and v > 0)
        negative_penalty = abs(engagement['negative']) if engagement['negative'] < 0 else 0

        base_score = min(100, positive_score * 3)
        final_score = max(0, base_score - negative_penalty * 5)

        # Estimate most likely next actions
        sorted_engagements = sorted(
            [(k, v) for k, v in engagement.items() if k != 'negative'],
            key=lambda x: x[1],
            reverse=True
        )
        top_actions = [k for k, v in sorted_engagements[:3] if v > 0]

        return PostEvaluation(
            score=final_score,
            strengths=strengths,
            weaknesses=weaknesses,
            recommendations=recommendations,
            engagement_potential=engagement,
            estimated_next_actions=top_actions
        )

    def format_report(self, evaluation: PostEvaluation) -> str:
        """Create a formatted report."""
        lines = [
            "═══════════════════════════════════════════════════",
            "  X ALGORITHM POST EVALUATION",
            "═══════════════════════════════════════════════════",
            f"\nOverall Score: {evaluation.score}/100",
            "",
            "STRENGTHS:",
        ]
        if evaluation.strengths:
            for s in evaluation.strengths:
                lines.append(f"  ✓ {s}")
        else:
            lines.append("  (None identified)")

        lines.append("\nWEAKNESSES:")
        if evaluation.weaknesses:
            for w in evaluation.weaknesses:
                lines.append(f"  ✗ {w}")
        else:
            lines.append("  (None identified)")

        lines.append("\nRECOMMENDATIONS:")
        if evaluation.recommendations:
            for r in evaluation.recommendations:
                lines.append(f"  • {r}")
        else:
            lines.append("  (No urgent recommendations)")

        lines.append("\nESTIMATED ENGAGEMENT POTENTIAL:")
        for eng, score in sorted(evaluation.engagement_potential.items(), key=lambda x: x[1], reverse=True):
            if score > 0:
                bar = '█' * min(score, 10)
                lines.append(f"  {eng:15} {score:3}/10  {bar}")
            elif score < 0:
                bar = '█' * min(abs(score), 10)
                lines.append(f"  {eng:15} {score:3}/10  {bar} (negative)")

        lines.append("\nMOST LIKELY NEXT ACTIONS:")
        for action in evaluation.estimated_next_actions[:3]:
            lines.append(f"  → {action}")

        lines.append("\n═══════════════════════════════════════════════════")
        lines.append("\nNote: This evaluation is based on publicly documented")
        lines.append("algorithm features. Actual performance may vary.")
        lines.append("Test and validate with your audience.\n")

        return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: python evaluate_post.py \"Your post text\" [--video] [--duration SECONDS] [--has-media]")
        print("\nExamples:")
        print('  python evaluate_post.py "This changed everything. Thread 🧵" --has-media')
        print('  python evaluate_post.py "How I gained 10k followers in 30 days" --video --duration 15')
        sys.exit(1)

    post_text = sys.argv[1]
    has_video = '--video' in sys.argv
    has_media = '--has-media' in sys.argv

    video_duration = 0
    if has_video:
        try:
            duration_idx = sys.argv.index('--duration')
            video_duration = int(sys.argv[duration_idx + 1])
        except (ValueError, IndexError):
            video_duration = 0

    evaluator = XAlgorithmEvaluator(post_text, has_video, video_duration, has_media)
    evaluation = evaluator.evaluate()
    print(evaluator.format_report(evaluation))


if __name__ == "__main__":
    main()
