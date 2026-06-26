#!/usr/bin/env python3
"""
Financial Planning for Young Parents in Jakarta
Cost estimates, budgeting, insurance guidance
"""

# Pregnancy & Delivery Cost Estimates (Jakarta 2026)
COST_ESTIMATES = {
    'prenatal_care': {
        'checkup_per_visit': {
            'public': 'Rp 0 - 300K (BPJS)',
            'private': 'Rp 500K - 1.5M',
            'premium': 'Rp 1M - 2M'
        },
        'ultrasound': {
            '2d': 'Rp 300K - 600K',
            '3d/4d': 'Rp 600K - 1.5M',
            'anatomy_scan': 'Rp 800K - 2M'
        },
        'blood_tests': {
            'routine': 'Rp 500K - 1.5M',
            'comprehensive': 'Rp 2M - 4M'
        },
        'total_prenatal': {
            'bpjs': 'Rp 0 - 2M (mostly covered)',
            'private': 'Rp 5M - 15M',
            'premium': 'Rp 10M - 25M'
        }
    },
    'delivery': {
        'normal': {
            'public_bpjs': 'Rp 0 - 2M',
            'private_mid': 'Rp 10M - 30M',
            'private_premium': 'Rp 30M - 70M'
        },
        'caesar': {
            'public_bpjs': 'Rp 0 - 5M',
            'private_mid': 'Rp 20M - 50M',
            'private_premium': 'Rp 50M - 100M+'
        }
    },
    'baby_gear': {
        'essential': {
            'stroller': 'Rp 500K - 3M',
            'car_seat': 'Rp 1M - 5M',
            'crib': 'Rp 1M - 5M',
            'total': 'Rp 5M - 15M'
        },
        'monthly': {
            'diapers': 'Rp 500K - 1.5M',
            'milk_formula': 'Rp 500K - 2M (if not breastfeeding)',
            'clothes': 'Rp 300K - 1M',
            'total_monthly': 'Rp 2M - 5M'
        }
    }
}

# BPJS Pregnancy Coverage Details
BPJS_COVERAGE = {
    'covered': [
        '✅ Prenatal checkups (minimum 6x)',
        '✅ Ultrasound (2x during pregnancy)',
        '✅ Blood tests & lab work',
        '✅ Iron & folic acid supplements',
        '✅ Normal delivery',
        '✅ Caesar if medically necessary',
        '✅ Complications coverage',
        '✅ Postpartum care (42 days)',
        '✅ Newborn care (first 28 days)',
        '✅ Immunizations (BCG, Polio, Hepatitis B)'
    ],
    'not_covered': [
        '❌ VIP room upgrade',
        '❌ Elective Caesar (without medical indication)',
        '❌ 3D/4D ultrasound for non-medical reasons',
        '❌ Private room (unless medically necessary)',
        '❌ Baby care products (diapers, formula, etc.)'
    ],
    'requirements': [
        'Active BPJS membership (paid up)',
        'Referral from Puskesmas (for non-emergency)',
        'KTP & KK copies',
        'Buku KIA (Kesehatan Ibu & Anak)',
        'BPJS card (physical or digital)'
    ],
    'process': [
        '1. Register at nearest Puskesmas with KTP & KK',
        '2. Get pregnant verification from doctor',
        '3. Receive referral to hospital',
        '4. Register at chosen hospital BPJS counter',
        '5. Receive schedule for prenatal visits',
        '6. Bring BPJS card to every visit',
        '7. For delivery: come with referral letter'
    ],
    'hospitals_jakarta': [
        'RSUD Tarakan (Jakpus)',
        'RSUD Pasar Rebo (Jaktim)',
        'RSUD Cengkareng (Jakbar)',
        'RSUD Koja (Jakut)',
        'RSIA Brawijaya (selected branches)',
        'RS Siloam (selected branches)',
        'RS Hermina (selected branches)'
    ]
}

# Private Insurance Comparison
INSURANCE_COMPARISON = {
    'bpjs': {
        'monthly_cost': 'Rp 42K - 150K (depending on class)',
        'coverage': 'Basic to standard care',
        'pros': [
            'Affordable',
            'Covers most medical needs',
            'Nationwide coverage',
            'No age limit'
        ],
        'cons': [
            'Limited hospital choice',
            'May have waiting times',
            'Standard facilities only',
            'Need referral for specialists'
        ],
        'best_for': 'Budget-conscious, basic coverage'
    },
    'private_basic': {
        'monthly_cost': 'Rp 300K - 800K',
        'coverage': 'Better hospitals, faster service',
        'pros': [
            'More hospital choices',
            'Shorter waiting times',
            'Better facilities',
            'Direct specialist access'
        ],
        'cons': [
            'Higher cost',
            'May have coverage limits',
            'Age restrictions',
            'Pre-existing conditions may not covered'
        ],
        'best_for': 'Middle income, want better service'
    },
    'private_premium': {
        'monthly_cost': 'Rp 1M - 3M+',
        'coverage': 'Premium hospitals, comprehensive',
        'pros': [
            'Best hospitals',
            'VIP rooms',
            'Comprehensive coverage',
            'International coverage (some plans)'
        ],
        'cons': [
            'Expensive',
            'May have deductible',
            'Complex claims process'
        ],
        'best_for': 'High income, want best care'
    }
}

# Budget Templates
BUDGET_TEMPLATES = {
    'young_couple_low': {
        'income_range': 'Rp 8M - 15M/month',
        'recommended_savings': 'Rp 2M - 4M/month for pregnancy',
        'breakdown': {
            'prenatal_care': 'Rp 3M - 5M (with BPJS)',
            'delivery': 'Rp 5M - 15M (BPJS + some private)',
            'baby_gear': 'Rp 5M - 10M (essential only)',
            'emergency_fund': 'Rp 5M - 10M',
            'total_recommended': 'Rp 18M - 40M'
        },
        'tips': [
            'Use BPJS for prenatal & delivery',
            'Buy baby gear secondhand or wait for sales',
            'Start saving 6 months before due date',
            'Ask family for baby shower gifts',
            'Prioritize essentials over nice-to-haves'
        ]
    },
    'young_couple_mid': {
        'income_range': 'Rp 15M - 30M/month',
        'recommended_savings': 'Rp 4M - 8M/month for pregnancy',
        'breakdown': {
            'prenatal_care': 'Rp 8M - 12M (private hospital)',
            'delivery': 'Rp 20M - 40M (private)',
            'baby_gear': 'Rp 10M - 20M',
            'emergency_fund': 'Rp 10M - 20M',
            'total_recommended': 'Rp 48M - 92M'
        },
        'tips': [
            'Mix of BPJS and private care',
            'Choose mid-range private hospital',
            'Buy quality essential items',
            'Consider prenatal classes',
            'Keep 3-6 months emergency fund'
        ]
    },
    'young_couple_high': {
        'income_range': 'Rp 30M+/month',
        'recommended_savings': 'Rp 8M - 15M/month for pregnancy',
        'breakdown': {
            'prenatal_care': 'Rp 15M - 25M (premium)',
            'delivery': 'Rp 50M - 100M+ (premium hospital)',
            'baby_gear': 'Rp 20M - 40M',
            'emergency_fund': 'Rp 20M - 50M',
            'total_recommended': 'Rp 105M - 215M+'
        },
        'tips': [
            'Premium hospital care',
            'Best facilities available',
            'Hire postpartum help (babysitter/nanny)',
            'Consider international insurance',
            'Invest in quality items that last'
        ]
    }
}

# Money-Saving Tips
MONEY_SAVING_TIPS = """
💰 Money-Saving Tips for Young Parents
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🏥 MEDICAL COSTS:
✅ Use BPJS for prenatal & delivery (saves 70-90%)
✅ Ask for generic medications
✅ Compare hospital packages
✅ Look for hospital promotions
✅ Attend free prenatal classes at Puskesmas

👶 BABY GEAR:
✅ Buy secondhand (babies outgrow fast!)
✅ Join mom groups for hand-me-downs
✅ Wait for sales (Harbolnas, 9.9, 10.10)
✅ Focus on essentials only
✅ Borrow from friends/family
✅ Register for baby shower gifts

🍼 MONTHLY EXPENSES:
✅ Breastfeed if possible (saves Rp 500K-2M/month)
✅ Buy diapers in bulk
✅ Use cloth diapers (one-time cost)
✅ Make baby food at home
✅ Buy clothes 1-2 sizes up (grow into them)

💡 GENERAL TIPS:
✅ Start saving early (ideally 6 months before)
✅ Track all pregnancy expenses
✅ Compare prices online (Tokopedia, Shopee)
✅ Ask for discounts (some hospitals offer)
✅ Don't buy everything new!

🚫 AVOID:
❌ Impulse buying cute baby clothes
❌ Expensive nursery decorations
❌ Too many newborn-size clothes
❌ Single-use baby gadgets
❌ Brand-name everything
"""

# Maternity Leave Info (Indonesia 2026)
MATERNITY_LEAVE_INFO = """
👶 Maternity Leave in Indonesia (2026)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⏱️ DURATION:
• 3 months total (1.5 months before + 1.5 months after)
• Can start 1.5 months before due date
• Mandatory 1.5 months after delivery

💰 SALARY:
• 100% salary during maternity leave
• Paid by employer (BPJS Kesehatan reimburses)
• Bonuses & THR still applicable

📋 REQUIREMENTS:
• Doctor's letter confirming pregnancy
• Estimated due date
• Submit to HR at least 2 months before leave
• Copy of marriage certificate (some companies)

👨 PATERNITY LEAVE (for husbands):
• 2 days paid leave (government regulation)
• Some companies offer more (check your policy)
• Request in advance with HR

📝 IMPORTANT:
• Confirm policy with your HR department
• Get everything in writing
• Know your rights!
• Some companies offer additional benefits

💡 TIPS:
• Plan handover before leave
• Prepare work documents
• Set up out-of-office email
• Discuss work-from-home options (if available)
• Know when you'll return
"""

# Checklist for Financial Preparation
FINANCIAL_CHECKLIST = {
    'first_trimester': [
        '☐ Calculate total estimated costs',
        '☐ Review health insurance (BPJS/private)',
        '☐ Start pregnancy savings fund',
        '☐ Compare hospital packages',
        '☐ Check employee benefits (maternity leave)'
    ],
    'second_trimester': [
        '☐ Open dedicated baby savings account',
        '☐ Buy essential baby gear (watch for sales)',
        '☐ Review life insurance coverage',
        '☐ Create post-baby budget',
        '☐ Discuss financial goals with partner'
    ],
    'third_trimester': [
        '☐ Finalize hospital payment plan',
        '☐ Pack hospital bag (avoid last-minute buying)',
        '☐ Prepare emergency fund (3-6 months expenses)',
        '☐ Set up automatic bill payments',
        '☐ Review will/beneficiaries (if applicable)'
    ]
}

def get_cost_estimate(budget_level='mid'):
    """
    Get cost estimates by budget level
    
    Args:
        budget_level: 'low', 'mid', 'high'
    
    Returns:
        dict: Cost breakdown
    """
    if budget_level == 'low':
        return BUDGET_TEMPLATES['young_couple_low']
    elif budget_level == 'high':
        return BUDGET_TEMPLATES['young_couple_high']
    else:
        return BUDGET_TEMPLATES['young_couple_mid']

def get_bpjs_coverage():
    """Get detailed BPJS coverage information"""
    result = """
🏥 BPJS Pregnancy Coverage
━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ COVERED SERVICES:
"""
    for item in BPJS_COVERAGE['covered']:
        result += f"\n{item}"
    
    result += "\n\n❌ NOT COVERED:"
    for item in BPJS_COVERAGE['not_covered']:
        result += f"\n{item}"
    
    result += "\n\n📋 REQUIREMENTS:"
    for item in BPJS_COVERAGE['requirements']:
        result += f"\n{item}"
    
    result += "\n\n🔄 REGISTRATION PROCESS:"
    for i, step in enumerate(BPJS_COVERAGE['process'], 1):
        result += f"\n{i}. {step}"
    
    result += "\n\n🏥 HOSPITALS IN JAKARTA:"
    for hospital in BPJS_COVERAGE['hospitals_jakarta']:
        result += f"\n• {hospital}"
    
    return result.strip()

def compare_insurance():
    """Compare different insurance options"""
    result = """
💳 Insurance Comparison
━━━━━━━━━━━━━━━━━━━━━━━━

"""
    for insurance_type, info in INSURANCE_COMPARISON.items():
        result += f"""
🏥 {insurance_type.upper().replace('_', ' ')}
   💰 Monthly Cost: {info['monthly_cost']}
   📋 Coverage: {info['coverage']}
   
   ✅ PROS:
"""
        for pro in info['pros']:
            result += f"   • {pro}\n"
        
        result += "\n   ❌ CONS:\n"
        for con in info['cons']:
            result += f"   • {con}\n"
        
        result += f"\n   👍 Best For: {info['best_for']}\n\n"
    
    return result.strip()

def get_money_saving_tips():
    """Get comprehensive money-saving tips"""
    return MONEY_SAVING_TIPS

def get_maternity_leave_info():
    """Get maternity leave information"""
    return MATERNITY_LEAVE_INFO

def get_financial_checklist(trimester='all'):
    """Get financial preparation checklist"""
    if trimester == 'all':
        result = """
📋 Financial Preparation Checklist
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FIRST TRIMESTER:
"""
        for item in FINANCIAL_CHECKLIST['first_trimester']:
            result += f"\n{item}"
        
        result += "\n\nSECOND TRIMESTER:"
        for item in FINANCIAL_CHECKLIST['second_trimester']:
            result += f"\n{item}"
        
        result += "\n\nTHIRD TRIMESTER:"
        for item in FINANCIAL_CHECKLIST['third_trimester']:
            result += f"\n{item}"
        
        return result.strip()
    else:
        items = FINANCIAL_CHECKLIST.get(trimester, [])
        result = f"\n📋 {trimester.replace('_', ' ').title()} Checklist\n"
        for item in items:
            result += f"\n{item}"
        return result.strip()

def calculate_savings_goal(current_savings=0, months_until_due=0, target_amount=0):
    """
    Calculate monthly savings needed
    
    Args:
        current_savings: Current savings amount
        months_until_due: Months until due date
        target_amount: Target savings amount
    
    Returns:
        dict: Savings calculation
    """
    if months_until_due <= 0:
        return {'error': 'Invalid months until due date'}
    
    remaining = target_amount - current_savings
    monthly_needed = remaining / months_until_due
    
    return {
        'target': target_amount,
        'current': current_savings,
        'remaining': remaining,
        'months': months_until_due,
        'monthly_needed': monthly_needed
    }
