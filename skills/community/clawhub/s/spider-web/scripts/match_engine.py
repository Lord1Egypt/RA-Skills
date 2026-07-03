#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Spider Web - Match Engine
Matches user queries against the trigger database with AND/OR logic, 
fuzzy matching, and intelligent scoring.
"""
import os, re, json, sys, difflib
from pathlib import Path

def setup_encoding():
    if sys.platform == 'win32':
        try:
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
            sys.stderr.reconfigure(encoding='utf-8', errors='replace')
        except: pass

# ── Core Match Engine ──────────────────────────────────────────────

class SpiderMatchEngine:
    """Main matching engine for the Spider Web trigger system."""

    def __init__(self, db_path=None):
        if db_path is None:
            db_path = os.path.join(os.path.dirname(__file__), "trigger_db.json")
        self.db = self._load(db_path)
        self.reverse_index = self.db.get("reverse_index", {}) if self.db else {}
        self.skills = self.db.get("skills", {}) if self.db else {}
        self.skill_names_index = self.db.get("skill_names_index", {}) if self.db else {}
        self._compute_idf()

    def _load(self, path):
        if not os.path.exists(path):
            return None
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _compute_idf(self):
        """Compute Inverse Document Frequency for each trigger.
        IDF = log(total_skills / skills_with_this_trigger)
        Higher IDF = more specific trigger word."""
        total = max(len(self.skills), 1)
        self.idf = {}
        for trigger, skills in self.reverse_index.items():
            df = len(skills)
            self.idf[trigger] = __import__('math').log(total / max(df, 1)) + 1.0
        # Cache for fast lookup
        self._max_idf = max(self.idf.values()) if self.idf else 1.0

    @staticmethod
    def _is_chinese(text):
        """Check if text contains Chinese characters."""
        return any('\u4e00' <= c <= '\u9fff' for c in text)

    @staticmethod
    def _char_overlap_score(trigger, query):
        """
        Calculate character-level overlap for Chinese text.
        Uses ordered subsequence matching + character set Jaccard.
        Returns (score_0_to_1, matched_chars_ratio).
        """
        # Method 1: Character bigram overlap (works well for Chinese)
        def get_bigrams(s):
            return set(s[i:i+2] for i in range(len(s)-1))

        t_bigrams = get_bigrams(trigger)
        q_bigrams = get_bigrams(query)

        if not t_bigrams:
            return 0.0, 0.0

        bigram_overlap = len(t_bigrams & q_bigrams) / len(t_bigrams)

        # Method 2: Character set Jaccard
        t_chars = set(trigger)
        q_chars = set(query)
        char_jaccard = len(t_chars & q_chars) / len(t_chars) if t_chars else 0

        # Method 3: Longest ordered subsequence
        def lcs_ratio(a, b):
            """Longest common subsequence ratio (ordered)."""
            m, n = len(a), len(b)
            if m == 0:
                return 0.0
            dp = [[0] * (n + 1) for _ in range(m + 1)]
            for i in range(m):
                for j in range(n):
                    if a[i] == b[j]:
                        dp[i+1][j+1] = dp[i][j] + 1
                    else:
                        dp[i+1][j+1] = max(dp[i][j+1], dp[i+1][j])
            return dp[m][n] / m

        lcs = lcs_ratio(trigger, query)

        # Combine scores
        combined = bigram_overlap * 0.5 + char_jaccard * 0.3 + lcs * 0.2
        return combined, bigram_overlap

    def _find_substring_matches(self, query_lower, triggers_dict):
        """Find matching triggers. Uses exact substring for short triggers,
        character-level overlap for Chinese triggers."""
        matches = []
        for trigger, skills in triggers_dict.items():
            # Exact substring match (fastest)
            if trigger in query_lower:
                matches.append((trigger, skills, 1.0, 'exact'))
                continue

            # For Chinese triggers, use character-level matching
            if self._is_chinese(trigger) and len(trigger) >= 2:
                overlap, bigram = self._char_overlap_score(trigger, query_lower)
                # Lower threshold for short triggers to catch partial matches
                if len(trigger) <= 3:
                    min_bigram = 0.3
                    min_overlap = 0.4
                elif len(trigger) <= 4:
                    min_bigram = 0.25
                    min_overlap = 0.35
                else:
                    min_bigram = 0.2
                    min_overlap = 0.3
                if bigram >= min_bigram or overlap >= min_overlap:
                    matches.append((trigger, skills, overlap, 'chinese'))

        return matches

    def _find_fuzzy_matches(self, query_lower, triggers_dict, threshold=0.7):
        """Find triggers that are similar to words in the query."""
        matches = []
        words = re.split(r'[\s,，。！？、]+', query_lower)
        words = [w for w in words if len(w) >= 2]

        for word in words:
            for trigger, skills in triggers_dict.items():
                if trigger in word or word in trigger:
                    if (trigger, skills, 0.5, 'partial') not in [
                        (t, s, sc, tp) for t, s, sc, tp in matches
                    ]:
                        matches.append((trigger, skills, 0.5, 'partial'))
                        break

            if len(word) >= 3:
                candidates = difflib.get_close_matches(word, triggers_dict.keys(), n=3, cutoff=threshold)
                for c in candidates:
                    match_entry = (c, triggers_dict[c], 0.3, 'fuzzy')
                    if match_entry not in matches:
                        matches.append(match_entry)

        return matches

    def _score_match(self, trigger, skills, overlap_score, match_type, query_lower):
        """Score a trigger-skill match. Higher = better."""
        score = 0.0

        if match_type == 'exact':
            score += 10.0
        elif match_type == 'chinese':
            score += overlap_score * 8.0  # 0-8 range
        elif match_type == 'partial':
            score += 4.0
        elif match_type == 'fuzzy':
            score += 2.0
        else:
            score += difflib.SequenceMatcher(None, trigger, query_lower).ratio() * 5.0

        # Length bonus: longer trigger = more specific
        score += min(len(trigger) / 20.0, 1.5)

        # IDF bonus: more specific triggers get higher weight
        idf = self.idf.get(trigger, 1.0) if hasattr(self, 'idf') else 1.0
        max_idf = self._max_idf if hasattr(self, '_max_idf') else 1.0
        idf_bonus = (idf / max_idf) * 3.0  # 0-3 bonus based on specificity
        score += idf_bonus

        # Skill name match bonus
        for skill in skills:
            if skill.lower() in query_lower:
                score += 5.0
            # Partial skill name match (Chinese)
            elif self._is_chinese(skill):
                overlap, _ = self._char_overlap_score(skill.lower(), query_lower)
                if overlap > 0.5:
                    score += overlap * 3.0

        return score

    def match(self, query, mode="auto", top_k=5, fuzzy=False, min_score=2.0):
        """
        Match a user query against the trigger database.

        Args:
            query: User's natural language input
            mode: "auto" (smart), "or" (parallel/any), "and" (serial/all)
            top_k: Max results to return
            fuzzy: Enable fuzzy matching
            min_score: Minimum score threshold

        Returns:
            dict with 'matches', 'best_match', 'suggestion'
        """
        if not self.reverse_index:
            return {"matches": [], "best_match": None, "suggestion": "No trigger database found. Run index first."}

        query_lower = query.strip().lower()
        all_matches = []  # (trigger, [skills], score)

        # Level 1: Smart matching (substring + Chinese char overlap)
        substring_matches = self._find_substring_matches(query_lower, self.reverse_index)
        for trigger, skills, overlap, match_type in substring_matches:
            score = self._score_match(trigger, skills, overlap, match_type, query_lower)
            all_matches.append((trigger, skills, score))

        # Level 2: Skill name matching (direct skill name mention)
        for skill_name in self.skills:
            if skill_name.lower() in query_lower:
                # Add all triggers from this skill
                skill_triggers = self.skills.get(skill_name, [])
                if skill_triggers:
                    all_matches.append((f"[skill:{skill_name}]", [skill_name], 12.0))
                break

        # Level 3: Fuzzy matching (if enabled or no results)
        if fuzzy or len(all_matches) == 0:
            fuzzy_matches = self._find_fuzzy_matches(query_lower, self.reverse_index,
                                                      threshold=0.6 if fuzzy else 0.75)
            for trigger, skills, overlap, match_type in fuzzy_matches:
                if not any(t == trigger and s == skills for t, s, _ in all_matches):
                    score = self._score_match(trigger, skills, overlap, match_type, query_lower) * 0.7
                    all_matches.append((trigger, skills, score))

        # Aggregate by skill (max score + diminishing bonus for additional matches)
        skill_scores = {}
        skill_triggers_matched = {}
        skill_trigger_details = {}  # Store (trigger, score) pairs per skill
        for trigger, skills, score in all_matches:
            for skill in skills:
                if skill not in skill_trigger_details:
                    skill_trigger_details[skill] = []
                skill_trigger_details[skill].append((trigger, score))
        
        for skill, details in skill_trigger_details.items():
            details.sort(key=lambda x: x[1], reverse=True)
            # Max score + 0.3 * sum of remaining (diminishing returns)
            max_score = details[0][1]
            bonus = sum(s[1] for s in details[1:]) * 0.3
            skill_scores[skill] = max_score + bonus
            skill_triggers_matched[skill] = [s[0] for s in details]

        # Filter by min_score
        filtered = {s: sc for s, sc in skill_scores.items() if sc >= min_score}

        # Sort by score descending
        ranked = sorted(filtered.items(), key=lambda x: x[1], reverse=True)

        # Apply mode logic
        if mode == "and":
            # AND mode: multiple trigger words in query must ALL match the same skill
            # This is for serial matching: query must contain ALL specified triggers
            # In practice, only include skills where multiple triggers matched
            ranked = [(s, sc) for s, sc in ranked
                      if len(skill_triggers_matched.get(s, [])) >= 2]
            # Re-sort
            ranked.sort(key=lambda x: x[1], reverse=True)

        # Top K
        top = ranked[:top_k]

        result = {
            "query": query,
            "mode": mode,
            "matches": [
                {
                    "skill": skill,
                    "score": round(score, 1),
                    "matched_triggers": skill_triggers_matched.get(skill, []),
                    "trigger_count": len(self.skills.get(skill, [])),
                }
                for skill, score in top
            ],
            "best_match": top[0][0] if top else None,
            "best_score": round(top[0][1], 1) if top else 0,
            "total_candidates": len(ranked),
            "suggestion": None,
        }

        # Generate suggestion
        if not top:
            result["suggestion"] = self._generate_suggestion(query)
        elif len(top) > 1 and top[0][1] - top[1][1] < 2.0:
            result["suggestion"] = f"Multiple skills matched with close scores. Showing top {len(top)}."
        elif top[0][1] < 5.0:
            result["suggestion"] = f"Best match has low confidence ({top[0][1]:.1f}). Consider being more specific."

        return result

    def match_and(self, query, *required_triggers):
        """AND logic: query must contain ALL specified triggers to match."""
        query_lower = query.lower()
        matching_skills = set()

        # Check each required trigger
        all_matching = None
        for trigger in required_triggers:
            trigger_lower = trigger.lower().strip()
            triggered_skills = set()

            for t, skills in self.reverse_index.items():
                if trigger_lower in query_lower and t in query_lower:
                    triggered_skills.update(skills)

            if all_matching is None:
                all_matching = triggered_skills
            else:
                all_matching = all_matching.intersection(triggered_skills)

        return list(all_matching) if all_matching else []

    def match_or(self, query):
        """OR logic: any trigger match activates the skill."""
        result = self.match(query, mode="or")
        return [m["skill"] for m in result["matches"]]

    def _generate_suggestion(self, query):
        """Generate helpful suggestion when no match found."""
        query_lower = query.lower()
        words = re.split(r'[\s,，。！？、]+', query_lower)
        words = [w for w in words if len(w) >= 2]

        # Try to find partial matches
        partial_skills = set()
        for word in words:
            for trigger, skills in self.reverse_index.items():
                if word in trigger or trigger in word:
                    partial_skills.update(skills)

        if partial_skills:
            skills_list = list(partial_skills)[:5]
            return f"No exact match. Did you mean: {', '.join(skills_list)}?"
        return "No matching skill found. Try different keywords or check trigger database."

    def query_to_skill_name(self, query):
        """Simple: given a user query, return the best skill name to activate."""
        result = self.match(query, top_k=1)
        return result["best_match"]

    def print_match_report(self, query, mode="auto", top_k=5):
        """Print a formatted match report."""
        result = self.match(query, mode=mode, top_k=top_k)
        print("=" * 60)
        print(f"  🕷️  SPIDER WEB - Match Report")
        print("=" * 60)
        print(f"  Query:  {query}")
        print(f"  Mode:   {mode}")
        print(f"  DB:     {self.db['meta']['total_skills']} skills, {self.db['meta']['total_triggers']} triggers")
        print()

        if result["matches"]:
            print(f"  Matches found: {len(result['matches'])} (of {result['total_candidates']} candidates)")
            print()
            for i, m in enumerate(result["matches"]):
                bar = "█" * min(int(m["score"]), 20) + "░" * max(0, 20 - int(m["score"]))
                print(f"  #{i+1} {m['skill']}")
                print(f"      Score: {m['score']:.1f}  {bar}")
                print(f"      Triggers: {', '.join(m['matched_triggers'][:5])}")
                if len(m['matched_triggers']) > 5:
                    print(f"                ... and {len(m['matched_triggers'])-5} more")
                print()

            if result["best_match"]:
                print(f"  🎯 Best match: {result['best_match']} (score: {result['best_score']})")
        else:
            print("  ❌ No matches found.")

        if result["suggestion"]:
            print(f"\n  💡 {result['suggestion']}")

    def get_stats(self):
        """Return quick stats about the trigger database."""
        if not self.db:
            return {}
        meta = self.db["meta"]
        overlap_skills = set()
        for skills in self.reverse_index.values():
            if len(skills) > 1:
                overlap_skills.update(skills)
        return {
            "skills_indexed": meta["total_skills"],
            "total_triggers": meta["total_triggers"],
            "unique_triggers": meta["unique_triggers"],
            "overlap_triggers": meta["overlap_triggers"],
            "skills_with_overlap": len(overlap_skills),
            "network_density": round(meta["overlap_triggers"] / max(meta["unique_triggers"], 1) * 100, 1),
        }


# ── CLI ────────────────────────────────────────────────────────────

def main():
    setup_encoding()
    engine = SpiderMatchEngine()

    if not engine.db:
        print("No trigger database found. Run index_triggers.py first.")
        return

    import argparse
    parser = argparse.ArgumentParser(description="Spider Web Match Engine")
    parser.add_argument("query", nargs="*", help="Query to match against triggers")
    parser.add_argument("--mode", default="auto", choices=["auto", "or", "and"],
                        help="Matching mode (default: auto)")
    parser.add_argument("--top", type=int, default=5, help="Max results")
    parser.add_argument("--fuzzy", action="store_true", help="Enable fuzzy matching")
    parser.add_argument("--stats", action="store_true", help="Show database stats")
    parser.add_argument("--skill", action="store_true", help="Return only best skill name")
    args = parser.parse_args()

    if args.stats:
        stats = engine.get_stats()
        print("🕷️ Spider Web Stats:")
        for k, v in stats.items():
            print(f"  {k}: {v}")
        return

    if not args.query:
        # Interactive mode
        print("🕷️ Spider Web Match Engine")
        print("Type a query to find matching skills, or 'quit' to exit.")
        print(f"Database: {engine.db['meta']['total_skills']} skills, "
              f"{engine.db['meta']['total_triggers']} triggers")
        print()
        while True:
            try:
                q = input("Query> ").strip()
                if q.lower() in ('quit', 'exit', 'q'):
                    break
                if not q:
                    continue
                if args.skill:
                    name = engine.query_to_skill_name(q)
                    print(f"  → {name}")
                else:
                    engine.print_match_report(q, mode=args.mode, top_k=args.top)
            except (KeyboardInterrupt, EOFError):
                break
        return

    query = ' '.join(args.query)
    if args.skill:
        name = engine.query_to_skill_name(query)
        print(name or "None")
    else:
        engine.print_match_report(query, mode=args.mode, top_k=args.top)


if __name__ == "__main__":
    main()
