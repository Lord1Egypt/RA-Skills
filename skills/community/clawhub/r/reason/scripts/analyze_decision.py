#!/usr/bin/env python3
"""Analyze decision with framework."""
import json
import os
import uuid
import argparse
from datetime import datetime

REASON_DIR = os.path.expanduser("~/.openclaw/workspace/memory/reason")

def ensure_dir():
    os.makedirs(REASON_DIR, exist_ok=True)

def main():
    parser = argparse.ArgumentParser(description='Analyze decision')
    parser.add_argument('--decision', required=True, help='Decision to analyze')
    parser.add_argument('--factors', help='Key factors (comma-separated)')
    
    args = parser.parse_args()
    
    print(f"\n🧠 DECISION ANALYSIS: {args.decision}")
    print("=" * 60)
    
    print("\nDECISION FRAMEWORK:")
    print("-" * 40)
    print("1. CLARIFY THE DECISION")
    print("   • What exactly are you deciding?")
    print("   • What are your options?")
    print("   • What is the timeline?")
    
    print("\n2. IDENTIFY FACTORS")
    if args.factors:
        factors = [f.strip() for f in args.factors.split(',')]
        for i, f in enumerate(factors, 1):
            print(f"   {i}. {f}")
    else:
        print("   • List all relevant factors")
        print("   • Consider: cost, time, risk, impact")
    
    print("\n3. EVALUATE OPTIONS")
    print("   • Pros and cons of each option")
    print("   • Trade-offs between factors")
    print("   • Short-term vs long-term consequences")
    
    print("\n4. CHECK BIASES")
    print("   • Confirmation bias (seeking confirming evidence)")
    print("   • Sunk cost fallacy (throwing good after bad)")
    print("   • Availability bias (overweighting recent events)")
    
    print("\n5. MAKE DECISION")
    print("   • Which option best aligns with your goals?")
    print("   • What would you advise a friend?")
    print("   • Can you test or reverse the decision?")
    
    # Save analysis
    analysis_id = f"DECISION-{str(uuid.uuid4())[:6].upper()}"
    analysis = {
        "id": analysis_id,
        "decision": args.decision,
        "factors": args.factors,
        "created_at": datetime.now().isoformat()
    }
    
    decisions_file = os.path.join(REASON_DIR, "decisions.json")
    data = {"decisions": []}
    if os.path.exists(decisions_file):
        with open(decisions_file, 'r') as f:
            data = json.load(f)
    
    data['decisions'].append(analysis)
    
    ensure_dir()
    with open(decisions_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"\n✓ Analysis saved: {analysis_id}")

if __name__ == '__main__':
    main()
