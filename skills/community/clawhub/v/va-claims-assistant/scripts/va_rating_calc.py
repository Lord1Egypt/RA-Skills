#!/usr/bin/env python3
"""
VA Combined Disability Rating Calculator
Uses the VA's "whole person" method (not simple addition).

Usage:
    python3 va_rating_calc.py 70 30 20 10
    python3 va_rating_calc.py --ratings 70 30 20 10
    python3 va_rating_calc.py --json 70 30 20 10

The VA method:
1. Sort ratings highest to lowest
2. Apply first rating to 100% whole person
3. Each subsequent rating applies to remaining "whole person"
4. Round final result to nearest 10%
"""

import sys
import json
import argparse


def calculate_combined_rating(ratings: list[int]) -> dict:
    """
    Calculate VA combined disability rating.
    
    Args:
        ratings: List of individual disability percentages (e.g. [70, 30, 20, 10])
    
    Returns:
        dict with raw, rounded, and step-by-step breakdown
    """
    if not ratings:
        return {"error": "No ratings provided"}
    
    # Validate input
    for r in ratings:
        if not (0 <= r <= 100):
            return {"error": f"Invalid rating {r}: must be 0-100"}
    
    # Sort descending
    sorted_ratings = sorted(ratings, reverse=True)
    
    remaining = 100.0
    steps = []
    
    for i, rating in enumerate(sorted_ratings):
        disability = remaining * (rating / 100)
        remaining -= disability
        steps.append({
            "rating": rating,
            "applied_to": round(100 - (remaining + disability), 1),
            "disability_added": round(disability, 2),
            "remaining_whole_person": round(remaining, 2)
        })
    
    raw_combined = round(100 - remaining, 2)
    
    # VA rounds to nearest 10, with 5+ rounding up
    if raw_combined % 10 >= 5:
        final_rating = (int(raw_combined / 10) + 1) * 10
    else:
        final_rating = int(raw_combined / 10) * 10
    
    final_rating = min(final_rating, 100)  # Cap at 100%
    
    return {
        "input_ratings": sorted_ratings,
        "raw_combined": raw_combined,
        "va_final_rating": final_rating,
        "steps": steps,
        "summary": f"Combined rating: {raw_combined:.1f}% → rounded to {final_rating}% (VA official)"
    }


def tdiu_eligible(ratings: list[int]) -> dict:
    """Check TDIU (Total Disability Individual Unemployability) eligibility."""
    if not ratings:
        return {"eligible": False, "reason": "No ratings"}
    
    combined = calculate_combined_rating(ratings)
    combined_pct = combined["va_final_rating"]
    max_single = max(ratings)
    
    # TDIU rules: 60%+ single OR 70%+ combined with at least one at 40%+
    single_eligible = max_single >= 60
    combined_eligible = combined_pct >= 70 and max_single >= 40
    
    eligible = single_eligible or combined_eligible
    
    if single_eligible:
        reason = f"Single rating of {max_single}% meets 60% threshold"
    elif combined_eligible:
        reason = f"Combined {combined_pct}% with single {max_single}% meets 70%/40% threshold"
    else:
        reason = f"Combined {combined_pct}%, highest single {max_single}% — does not meet TDIU thresholds"
    
    return {
        "eligible": eligible,
        "combined_rating": combined_pct,
        "highest_single": max_single,
        "reason": reason,
        "note": "TDIU pays at 100% rate even if combined rating is lower"
    }


def main():
    parser = argparse.ArgumentParser(
        description="VA Combined Disability Rating Calculator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 va_rating_calc.py 70 30 20 10
  python3 va_rating_calc.py --json 70 30 20 10
  python3 va_rating_calc.py --tdiu 70 30 20 10
        """
    )
    parser.add_argument("ratings", nargs="+", type=int, help="Individual disability ratings")
    parser.add_argument("--ratings", dest="ratings_flag", nargs="+", type=int, 
                       help="Alternative: --ratings 70 30 20")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--tdiu", action="store_true", help="Also check TDIU eligibility")
    
    args = parser.parse_args()
    ratings = args.ratings_flag if args.ratings_flag else args.ratings
    
    result = calculate_combined_rating(ratings)
    
    if args.tdiu:
        result["tdiu"] = tdiu_eligible(ratings)
    
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"\n{'='*50}")
        print(f"VA COMBINED DISABILITY RATING CALCULATOR")
        print(f"{'='*50}")
        print(f"\nInput ratings: {', '.join(str(r)+'%' for r in result['input_ratings'])}")
        print(f"\nStep-by-step breakdown:")
        for i, step in enumerate(result["steps"], 1):
            print(f"  {i}. {step['rating']}% applied → adds {step['disability_added']:.1f}% disability | "
                  f"{step['remaining_whole_person']:.1f}% whole person remaining")
        print(f"\nRaw combined: {result['raw_combined']:.1f}%")
        print(f"VA official rating: {result['va_final_rating']}%")
        
        if args.tdiu:
            tdiu = result["tdiu"]
            print(f"\nTDIU Eligibility: {'✅ ELIGIBLE' if tdiu['eligible'] else '❌ NOT ELIGIBLE'}")
            print(f"  {tdiu['reason']}")
            if tdiu['eligible']:
                print(f"  → Can receive 100% pay rate even at {tdiu['combined_rating']}% rating")
        print()


if __name__ == "__main__":
    main()
