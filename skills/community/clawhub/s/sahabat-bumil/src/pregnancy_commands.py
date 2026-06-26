#!/usr/bin/env python3
"""
Pregnancy Companion - Command Handler
Integrates Jakarta hospitals, Indonesian nutrition, and financial planning
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from jakarta_hospitals import (
    search_hospitals, format_hospital_info, get_bpjs_info,
    get_prenatal_classes, compare_hospitals
)
from indonesian_nutrition import (
    get_food_recommendations, search_recipes, format_recipe,
    get_morning_sickness_tips, get_young_mom_nutrition, get_warung_safety_guide
)
from financial_planning import (
    get_cost_estimate, get_bpjs_coverage, compare_insurance,
    get_money_saving_tips, get_maternity_leave_info, get_financial_checklist
)

def handle_pregnancy_command(command, args):
    """
    Handle pregnancy-related commands
    
    Args:
        command: Command name (e.g., 'hospitals', 'nutrition')
        args: Command arguments
    
    Returns:
        str: Response message
    """
    
    cmd = command.lower().strip('/').replace('-', '_')
    
    # Hospital commands
    if cmd == 'hospitals':
        if len(args) >= 1 and args[0] == 'search':
            area = args[1] if len(args) > 1 else 'all'
            budget = args[2] if len(args) > 2 else 'all'
            hospitals = search_hospitals(area=area, budget_range=budget)
            if hospitals:
                result = f"🏥 Found {len(hospitals)} hospitals:\n\n"
                for h in hospitals[:5]:
                    result += format_hospital_info(h) + "\n\n"
                return result
            return "❌ No hospitals found matching criteria"
        elif len(args) >= 1 and args[0] == 'bpjs':
            return get_bpjs_info()
        elif len(args) >= 1 and args[0] == 'classes':
            return get_prenatal_classes()
        elif len(args) == 3 and args[0] == 'compare':
            return compare_hospitals(args[1], args[2])
        else:
            return """
🏥 Hospital Commands:
  /hospitals search <area> <budget>  → Search hospitals
  /hospitals bpjs                    → BPJS coverage info
  /hospitals classes                 → Prenatal classes
  /hospitals compare <rs1> <rs2>     → Compare hospitals
  
Examples:
  /hospitals search jaksel mid
  /hospitals bpjs
  /hospitals classes
  /hospitals compare Brawijaya Pondok Indah
"""
    
    # Nutrition commands
    elif cmd == 'nutrition':
        if len(args) >= 1 and args[0] == 'foods':
            recs = get_food_recommendations()
            result = "🍎 Indonesian Foods Safe for Pregnancy:\n\n"
            for category, foods in recs['safe_foods'].items():
                result += f"\n📌 {category.upper().replace('_', ' ')}:"
                for food in foods[:5]:
                    result += f"\n• {food['name']} - {food['benefits']}"
            return result
        elif len(args) >= 1 and args[0] == 'avoid':
            recs = get_food_recommendations()
            result = "❌ Foods to Avoid:\n\n"
            for item in recs['foods_to_avoid']['definitely_avoid']:
                result += f"\n🚫 {item['name']}"
                result += f"\n   Examples: {', '.join(item['examples'])}"
                result += f"\n   Reason: {item['reason']}\n"
            return result
        elif len(args) >= 1 and args[0] == 'recipes':
            recipes = search_recipes()
            result = "🍽️ Indonesian Pregnancy Recipes:\n\n"
            for recipe in recipes:
                result += format_recipe(recipe) + "\n\n"
            return result
        elif len(args) >= 1 and args[0] == 'morning-sickness':
            return get_morning_sickness_tips()
        elif len(args) >= 1 and args[0] == 'young-mom':
            return get_young_mom_nutrition()
        elif len(args) >= 1 and args[0] == 'warung':
            return get_warung_safety_guide()
        else:
            return """
🍎 Nutrition Commands:
  /nutrition foods           → Safe Indonesian foods
  /nutrition avoid           → Foods to avoid
  /nutrition recipes         → Indonesian recipes
  /nutrition morning-sickness → Morning sickness tips
  /nutrition young-mom       → Young mom nutrition
  /nutrition warung          → Eating outside guide
  
Examples:
  /nutrition foods
  /nutrition avoid
  /nutrition recipes
  /nutrition morning-sickness
"""
    
    # Financial commands
    elif cmd == 'finance' or cmd == 'financial':
        if len(args) >= 1 and args[0] == 'budget':
            budget_level = args[1] if len(args) > 1 else 'mid'
            return get_cost_estimate(budget_level)
        elif len(args) >= 1 and args[0] == 'bpjs':
            return get_bpjs_coverage()
        elif len(args) >= 1 and args[0] == 'insurance':
            return compare_insurance()
        elif len(args) >= 1 and args[0] == 'tips':
            return get_money_saving_tips()
        elif len(args) >= 1 and args[0] == 'maternity':
            return get_maternity_leave_info()
        elif len(args) >= 1 and args[0] == 'checklist':
            return get_financial_checklist()
        else:
            return """
💰 Financial Commands:
  /finance budget <level>      → Cost estimates (low/mid/high)
  /finance bpjs                → BPJS coverage
  /finance insurance           → Insurance comparison
  /finance tips                → Money-saving tips
  /finance maternity           → Maternity leave info
  /finance checklist           → Financial checklist
  
Examples:
  /finance budget mid
  /finance bpjs
  /finance tips
  /finance maternity
"""
    
    # General pregnancy info
    elif cmd == 'pregnancy':
        if len(args) >= 1 and args[0] == 'week':
            return """
🤰 Pregnancy Week Calculator

To calculate your current week:
1. Note your Last Menstrual Period (LMP)
2. Count weeks from that date
3. Or use online calculator:
   https://www.whattoexpect.com/pregnancy/due-date-calculator/

Example:
LMP: January 1, 2026
Current Week: Week 14 (as of April 6, 2026)
Due Date: October 8, 2026

Want me to help calculate? Tell me your LMP date!
"""
        elif len(args) >= 1 and args[0] == 'trimester':
            return """
📅 Pregnancy Trimesters

FIRST TRIMESTER (Weeks 1-12):
• Baby's organs forming
• Morning sickness common
• Fatigue, breast tenderness
• First ultrasound (8-12 weeks)

SECOND TRIMESTER (Weeks 13-26):
• Energy returns
• Baby movements felt (16-20 weeks)
• Anatomy scan (18-22 weeks)
• Gender reveal possible

THIRD TRIMESTER (Weeks 27-40):
• Baby grows rapidly
• More frequent checkups
• Prepare hospital bag
• Watch for labor signs
"""
        else:
            return """
🤰 Pregnancy Commands:
  /pregnancy week      → Calculate current week
  /pregnancy trimester → Trimester information
  
Examples:
  /pregnancy week
  /pregnancy trimester
"""
    
    # Help command
    elif cmd == 'help':
        return """
🤰 Pregnancy Companion - All Commands
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🏥 HOSPITALS (Jakarta):
  /hospitals search <area> <budget>
  /hospitals bpjs
  /hospitals classes
  /hospitals compare <rs1> <rs2>

🍎 NUTRITION (Indonesian):
  /nutrition foods
  /nutrition avoid
  /nutrition recipes
  /nutrition morning-sickness
  /nutrition young-mom
  /nutrition warung

💰 FINANCIAL:
  /finance budget <level>
  /finance bpjs
  /finance insurance
  /finance tips
  /finance maternity
  /finance checklist

🤰 PREGNANCY INFO:
  /pregnancy week
  /pregnancy trimester

💕 SUPPORT:
  Just chat! I'm here to listen and help.

Examples:
  /hospitals search jaksel mid
  /nutrition recipes
  /finance budget mid
  /pregnancy week
"""
    
    # Default response
    else:
        return """
🤰 Welcome to Pregnancy Companion!

I'm here to support your pregnancy journey! 💕

Type /help to see all commands.

Or just tell me what's on your mind!
"""

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(handle_pregnancy_command('help', []))
    else:
        command = sys.argv[1]
        args = sys.argv[2:] if len(sys.argv) > 2 else []
        result = handle_pregnancy_command(command, args)
        print(result)
