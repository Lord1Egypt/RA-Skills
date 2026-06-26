#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple rhythm analyzer for novel chapters
"""

import re
from pathlib import Path


class RhythmAnalyzer:
    """Rhythm analyzer class"""

    def __init__(self, file_path=None):
        self.file_path = file_path
        self.content = None
        self.analysis = {}

    def load_file(self, file_path=None):
        """Load chapter file"""
        if file_path:
            self.file_path = file_path

        if not self.file_path:
            print("Error: No file path specified")
            return False

        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                self.content = f.read()
            return True
        except Exception as e:
            print(f"Cannot read file: {e}")
            return False

    def analyze_dialogue_density(self):
        """Analyze dialogue density"""
        if not self.content:
            return 0

        # Extract dialogues (including quotes)
        dialogues = re.findall(r'["「『](.+?)["」』]', self.content)
        dialogue_chars = sum(len(d) for d in dialogues)

        # Count total characters
        total_chars = len(re.findall(r'[\u4e00-\u9fa5]', self.content))

        if total_chars == 0:
            return 0

        # Calculate dialogue density (dialogue chars / total chars)
        density = dialogue_chars / total_chars

        return {
            'dialogue_chars': dialogue_chars,
            'total_chars': total_chars,
            'density': density,
            'percentage': density * 100
        }

    def analyze_conflict_density(self):
        """Analyze conflict density"""
        if not self.content:
            return 0

        # Conflict keywords
        conflict_keywords = [
            '打', '骂', '杀', '威胁', '冲突', '对抗', '反击',
            '威胁', '警告', '逼迫', '挣扎', '拒绝', '破坏',
            '反目', '拒绝', '背叛', '愤怒', '战斗'
        ]

        total_count = 0
        for keyword in conflict_keywords:
            count = self.content.count(keyword)
            total_count += count

        # Estimate density
        total_chars = len(re.findall(r'[\u4e00-\u9fa5]', self.content))
        density = total_count / total_chars if total_chars > 0 else 0

        return {
            'conflict_count': total_count,
            'density': density,
            'conflicts_per_1000_chars': (total_count / total_chars * 1000) if total_chars > 0 else 0
        }

    def analyze_pacing(self):
        """Analyze pacing and rhythm"""
        if not self.content:
            return {}

        # Split into paragraphs
        paragraphs = [p.strip() for p in self.content.split('\n\n') if p.strip()]

        # Count sentence lengths
        sentence_lengths = []
        for para in paragraphs:
            sentences = re.split(r'[。！？]', para)
            for sent in sentences:
                if sent.strip():
                    sentence_lengths.append(len(sent))

        if not sentence_lengths:
            return {}

        avg_length = sum(sentence_lengths) / len(sentence_lengths)

        return {
            'total_paragraphs': len(paragraphs),
            'total_sentences': len(sentence_lengths),
            'avg_sentence_length': avg_length,
            'short_sentences': sum(1 for l in sentence_lengths if l < 10),
            'long_sentences': sum(1 for l in sentence_lengths if l > 50)
        }

    def analyze(self, verbose=True):
        """Run analysis (compatibility method)"""
        result = self.analyze_all()

        # Calculate overall score
        dialogue_pct = result.get('dialogue', {}).get('percentage', 0)
        conflict_density = result.get('conflict', {}).get('conflicts_per_1000_chars', 0)

        # Score: dialogue 20-40% is good, conflict >2 per 1000 chars is good
        score = 50
        if 20 <= dialogue_pct <= 40:
            score += 20
        elif dialogue_pct > 0:
            score += 10

        if conflict_density >= 2:
            score += 20
        elif conflict_density >= 1:
            score += 10

        score = min(100, score)

        # Determine grade
        if score >= 90:
            grade = 'S'
        elif score >= 80:
            grade = 'A'
        elif score >= 60:
            grade = 'B'
        else:
            grade = 'C'

        result['overall_score'] = {
            'overall_score': score,
            'grade': grade
        }

        if verbose:
            print(f"Dialogue density: {dialogue_pct:.1f}%")
            print(f"Conflict density: {conflict_density:.2f} per 1000 chars")
            print(f"Overall score: {score}/100 ({grade})")

        return result

    def analyze_all(self):
        """Run all analysis"""
        self.analysis = {}

        if not self.content:
            if not self.load_file():
                return self.analysis

        self.analysis['dialogue'] = self.analyze_dialogue_density()
        self.analysis['conflict'] = self.analyze_conflict_density()
        self.analysis['pacing'] = self.analyze_pacing()

        return self.analysis


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        analyzer = RhythmAnalyzer(sys.argv[1])
        result = analyzer.analyze_all()
        print("Rhythm Analysis Results:")
        for key, value in result.items():
            print(f"{key}: {value}")
