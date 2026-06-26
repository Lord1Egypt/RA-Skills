#!/usr/bin/env python3
"""
Indonesian Pregnancy Nutrition Guide
Local food recommendations, recipes, and nutrition advice for Indonesian moms
"""

# Indonesian Foods - Safe to Eat
INDONESIAN_SAFE_FOODS = {
    'carbohydrates': [
        {'name': 'Nasi putih/merah', 'benefits': 'Energy, B vitamins', 'tips': 'Choose brown rice for more fiber'},
        {'name': 'Kentang', 'benefits': 'Carbs, potassium, vitamin C', 'tips': 'Boiled or baked, avoid fried'},
        {'name': 'Ubi jalar', 'benefits': 'Fiber, vitamin A, beta-carotene', 'tips': 'Great snack option'},
        {'name': 'Jagung', 'benefits': 'Fiber, folate', 'tips': 'Boiled or grilled'},
        {'name': 'Roti gandum', 'benefits': 'Fiber, iron', 'tips': 'Choose whole grain'}
    ],
    'proteins': [
        {'name': 'Ayam (well-cooked)', 'benefits': 'Lean protein, B vitamins', 'tips': 'Avoid raw/undercooked'},
        {'name': 'Ikan (low mercury)', 'benefits': 'Omega-3, protein', 'tips': 'Choose salmon, tuna (limited), kembung'},
        {'name': 'Telur (fully cooked)', 'benefits': 'Protein, choline', 'tips': 'Avoid soft-boiled/poached'},
        {'name': 'Tempe', 'benefits': 'Protein, probiotics, iron', 'tips': 'Excellent plant protein'},
        {'name': 'Tahu', 'benefits': 'Protein, calcium', 'tips': 'Well-cooked'},
        {'name': 'Daging sapi (lean)', 'benefits': 'Iron, protein, B12', 'tips': 'Well-cooked, lean cuts'},
        {'name': 'Kacang-kacangan', 'benefits': 'Protein, fiber, folate', 'tips': 'Almond, kacang merah, edamame'}
    ],
    'vegetables': [
        {'name': 'Bayam', 'benefits': 'Iron, folate, vitamin K', 'tips': 'Cook thoroughly'},
        {'name': 'Kangkung', 'benefits': 'Iron, vitamin A', 'tips': 'Well-cooked'},
        {'name': 'Wortel', 'benefits': 'Vitamin A, beta-carotene', 'tips': 'Raw or cooked'},
        {'name': 'Brokoli', 'benefits': 'Folate, fiber, vitamin C', 'tips': 'Lightly steamed'},
        {'name': 'Labu siam', 'benefits': 'Folate, fiber', 'tips': 'Common in sayur bening'},
        {'name': 'Daun singkong', 'benefits': 'Iron, calcium', 'tips': 'Well-cooked'}
    ],
    'fruits': [
        {'name': 'Pisang', 'benefits': 'Potassium, vitamin B6', 'tips': 'Great for morning sickness'},
        {'name': 'Pepaya (ripe)', 'benefits': 'Vitamin C, fiber', 'tips': 'Only RIPE, avoid unripe'},
        {'name': 'Jeruk', 'benefits': 'Vitamin C, folate', 'tips': 'Fresh juice OK'},
        {'name': 'Apel', 'benefits': 'Fiber, vitamin C', 'tips': 'Wash thoroughly'},
        {'name': 'Alpukat', 'benefits': 'Healthy fats, folate', 'tips': 'Great for baby brain development'},
        {'name': 'Mangga', 'benefits': 'Vitamin A, C', 'tips': 'In moderation (sugar)'},
        {'name': 'Semangka', 'benefits': 'Hydration, vitamin C', 'tips': 'Good for hydration'}
    ],
    'dairy': [
        {'name': 'Susu pasteurisasi', 'benefits': 'Calcium, vitamin D', 'tips': 'Low-fat preferred'},
        {'name': 'Yogurt', 'benefits': 'Probiotics, calcium', 'tips': 'Plain, low sugar'},
        {'name': 'Keju (pasteurized)', 'benefits': 'Calcium, protein', 'tips': 'Avoid soft cheeses'}
    ]
}

# Foods to Avoid
INDONESIAN_FOODS_TO_AVOID = {
    'definitely_avoid': [
        {
            'name': 'Makanan mentah/setengah matang',
            'examples': ['Sate babi', 'Steak rare', 'Telur setengah matang', 'Sushi/sashimi'],
            'reason': 'Risk of bacteria (Salmonella, E. coli, Listeria)'
        },
        {
            'name': 'Ikan high-mercury',
            'examples': ['Hiu', 'Tongkol (excessive)', 'Tenggiri (excessive)', 'Marlin'],
            'reason': 'Mercury can harm baby nervous system'
        },
        {
            'name': 'Susu/keju unpasteurized',
            'examples': ['Susu kambing segar', 'Keju lunak import'],
            'reason': 'Listeria risk'
        },
        {
            'name': 'Alkohol',
            'examples': ['Beer', 'Wine', 'Traditional alcoholic drinks'],
            'reason': 'Can cause fetal alcohol syndrome'
        },
        {
            'name': 'Makanan jalanan yang kurang higienis',
            'examples': ['Gorengan pinggir jalan', 'Es tidak jelas', 'Nasi goreng kaki lima'],
            'reason': 'Food poisoning risk'
        }
    ],
    'limit': [
        {
            'name': 'Kafein',
            'limit': '< 200mg/day (≈ 1 cup coffee)',
            'examples': ['Kopi', 'Teh', 'Coklat', 'Energy drinks'],
            'tips': 'Switch to decaf or herbal tea'
        },
        {
            'name': 'Makanan terlalu pedas',
            'limit': 'Moderate amounts',
            'examples': ['Sambal level tinggi', 'Rica-rica', 'Balado'],
            'tips': 'Can cause heartburn, especially in 3rd trimester'
        },
        {
            'name': 'Garam',
            'limit': '< 2300mg/day',
            'examples': ['Makanan kaleng', 'Mie instan', 'Snack asin'],
            'tips': 'High sodium can increase blood pressure'
        },
        {
            'name': 'Gula',
            'limit': 'Moderate',
            'examples': ['Es manis', 'Kue', 'Coklat'],
            'tips': 'Risk of gestational diabetes'
        }
    ],
    'traditional_concerns': [
        {
            'name': 'Nanas (unripe)',
            'concern': 'Contains bromelain, may cause contractions',
            'advice': 'Small amounts of ripe pineapple OK, avoid unripe'
        },
        {
            'name': 'Pepaya (unripe)',
            'concern': 'Latex content may trigger contractions',
            'advice': 'Only eat RIPE papaya, avoid unripe/young papaya'
        },
        {
            'name': 'Kelapa muda',
            'concern': 'Traditional belief: can make baby have more vernix',
            'advice': 'Scientifically safe in moderation, water is hydrating'
        },
        {
            'name': 'Es terlalu dingin',
            'concern': 'Traditional belief: baby will have thick vernix',
            'advice': 'No scientific evidence, but moderation is key'
        }
    ]
}

# Trimester-Specific Nutrition
TRIMESTER_NUTRITION = {
    'first': {
        'weeks': '1-12',
        'focus': ['Folate', 'Vitamin B6', 'Iron', 'Hydration'],
        'key_nutrients': {
            'folate': {
                'amount': '600 mcg/day',
                'sources': ['Bayam', 'Kacang-kacangan', 'Alpukat', 'Jeruk', 'Suplemen asam folat'],
                'importance': 'Prevents neural tube defects'
            },
            'vitamin_b6': {
                'amount': '1.9 mg/day',
                'sources': ['Pisang', 'Ayam', 'Kentang', 'Kacang'],
                'importance': 'Helps with morning sickness'
            },
            'iron': {
                'amount': '27 mg/day',
                'sources': ['Daging merah', 'Bayam', 'Kacang', 'Sereal fortified'],
                'importance': 'Prevents anemia, supports baby growth'
            }
        },
        'common_issues': {
            'morning_sickness': {
                'tips': [
                    'Eat small frequent meals',
                    'Keep crackers by bed, eat before getting up',
                    'Avoid spicy/greasy foods',
                    'Ginger tea or ginger candies',
                    'Stay hydrated'
                ],
                'foods_to_try': ['Crackers', 'Pisang', 'Roti tawar', 'Jahe tea', 'Es batu']
            }
        }
    },
    'second': {
        'weeks': '13-26',
        'focus': ['Calcium', 'Protein', 'Omega-3', 'Iron'],
        'key_nutrients': {
            'calcium': {
                'amount': '1000 mg/day',
                'sources': ['Susu', 'Yogurt', 'Keju', 'Tahu', 'Bayam'],
                'importance': 'Baby bone development, protect mom bone density'
            },
            'protein': {
                'amount': '71 g/day',
                'sources': ['Ayam', 'Ikan', 'Telur', 'Tempe', 'Kacang'],
                'importance': 'Baby tissue growth'
            },
            'omega3': {
                'amount': '200-300 mg DHA/day',
                'sources': ['Ikan salmon', 'Ikan kembung', 'Telur omega-3', 'Suplemen DHA'],
                'importance': 'Baby brain & eye development'
            }
        },
        'common_issues': {
            'constipation': {
                'tips': [
                    'High fiber foods',
                    'Drink plenty of water',
                    'Regular exercise',
                    'Prunes or prune juice'
                ],
                'foods_to_try': ['Pepaya', 'Sayuran hijau', 'Gandum', 'Air putih 8-10 glasses']
            }
        }
    },
    'third': {
        'weeks': '27-40',
        'focus': ['Iron', 'Protein', 'Vitamin K', 'Frequent small meals'],
        'key_nutrients': {
            'iron': {
                'amount': '27 mg/day',
                'sources': ['Daging merah', 'Ayam', 'Ikan', 'Bayam', 'Suplemen'],
                'importance': 'Prepare for blood loss during delivery'
            },
            'vitamin_k': {
                'amount': '90 mcg/day',
                'sources': ['Sayuran hijau', 'Brokoli', 'Bayam'],
                'importance': 'Blood clotting'
            }
        },
        'common_issues': {
            'heartburn': {
                'tips': [
                    'Eat small frequent meals',
                    'Avoid lying down after eating',
                    'Avoid spicy/fried foods',
                    'Sleep with head elevated'
                ],
                'foods_to_avoid': ['Sambal', 'Gorengan', 'Coklat', 'Mint', 'Kopi']
            },
            'swelling': {
                'tips': [
                    'Reduce salt intake',
                    'Stay hydrated',
                    'Elevate feet',
                    'Wear comfortable shoes'
                ]
            }
        }
    }
}

# Indonesian Recipes for Pregnancy
INDONESIAN_RECIPES = [
    {
        'name': 'Sayur Bening Bayam',
        'trimester': 'All',
        'prep_time': '15 minutes',
        'servings': '4',
        'ingredients': [
            '2 ikat bayam, petik daunnya',
            '1 buah labu siam, potong dadu',
            '2 liter air',
            '2 siung bawang putih, geprek',
            'Garam secukupnya',
            'Gula secukupnya'
        ],
        'instructions': [
            'Didihkan air dengan bawang putih',
            'Masukkan labu siam, masak hingga empuk',
            'Masukkan bayam, masak sebentar (1-2 menit)',
            'Bumbui dengan garam dan gula',
            'Sajikan hangat'
        ],
        'nutritional_benefits': 'High in iron, folate, vitamin K'
    },
    {
        'name': 'Ayam Bakar Madu',
        'trimester': '2nd & 3rd',
        'prep_time': '45 minutes',
        'servings': '4',
        'ingredients': [
            '500g ayam (dada/paha)',
            '3 sdm madu',
            '2 sdm kecap manis',
            'Bumbu: bawang putih, ketumbar, kunyit',
            'Jeruk nipis'
        ],
        'instructions': [
            'Marinasi ayam dengan bumbu, madu, kecap (min. 30 min)',
            'Bakar ayam hingga matang sempurna',
            'Oles sisa marinasi saat membakar',
            'Sajikan dengan nasi dan sayuran'
        ],
        'nutritional_benefits': 'High protein, iron for baby growth'
    },
    {
        'name': 'Tumis Brokoli Wortel',
        'trimester': 'All',
        'prep_time': '15 minutes',
        'servings': '3',
        'ingredients': [
            '1 buah brokoli, potong per kuntum',
            '2 buah wortel, iris serong',
            '2 siung bawang putih, cincang',
            '1 sdm minyak zaitun',
            'Garam, lada secukupnya'
        ],
        'instructions': [
            'Tumis bawang putih dengan minyak zaitun',
            'Masukkan wortel, tumis 2 menit',
            'Masukkan brokoli, tumis hingga layu',
            'Bumbui dengan garam dan lada',
            'Sajikan segera'
        ],
        'nutritional_benefits': 'High in folate, vitamin A, fiber'
    },
    {
        'name': 'Bubur Kacang Hijau',
        'trimester': 'All',
        'prep_time': '45 minutes',
        'servings': '4',
        'ingredients': [
            '200g kacang hijau',
            '1 liter air',
            '2 lembar daun pandan',
            'Gula merah secukupnya (moderate)',
            'Santan encer (optional)'
        ],
        'instructions': [
            'Rendam kacang hijau 2 jam',
            'Rebus kacang hijau dengan daun pandan hingga empuk',
            'Tambahkan gula merah',
            'Tambahkan santan encer (optional)',
            'Sajikan hangat atau dingin'
        ],
        'nutritional_benefits': 'High in folate, protein, fiber'
    }
]

# Warung/Restaurant Safety Guide
WARUNG_SAFETY_TIPS = """
🍽️ Eating Outside During Pregnancy - Safety Tips
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ SAFE OPTIONS:
• Warung with good hygiene (clean tables, utensils)
• Food cooked fresh and served hot
• Bottled/sealed drinks
• Fruit you peel yourself
• Established restaurants with good reviews

❌ AVOID:
• Street food with questionable hygiene
• Food left out at room temperature
• Ice from unknown sources
• Pre-cut fruit from street vendors
• Raw vegetables (lalapan) from street vendors

💡 TIPS:
• Choose busy warungs (high turnover = fresh food)
• Ask for food to be cooked thoroughly
• Bring your own water bottle
• Avoid peak lunch rush (food may be pre-cooked)
• Trust your instincts - if it doesn't look clean, skip it
"""

# Young Mom Specific Nutrition
YOUNG_MOM_NUTRITION = """
👶 Nutrition for Young Moms (Age 22)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SPECIAL CONSIDERATIONS:

At age 22, your body is still developing! You need EXTRA nutrition:

🦴 EXTRA CALCIUM (1300 mg/day vs 1000 mg for older moms)
   Why: Your bones are still densifying
   Sources: Susu, yogurt, keju, tahu, bayam, ikan teri

💪 EXTRA PROTEIN (75-80g/day)
   Why: You're still growing too
   Sources: Ayam, ikan, telur, tempe, kacang-kacangan

🩸 EXTRA IRON (27 mg/day + consider supplement)
   Why: Young moms at higher risk of anemia
   Sources: Daging merah, bayam, kacang, sereal fortified

🍽️ DON'T SKIP MEALS!
   Common mistake: Busy with studies/work, skip meals
   Solution: Keep healthy snacks handy (kacang, fruit, yogurt)

⚖️ WEIGHT GAIN MONITORING
   Recommended: 11-16 kg total (normal BMI)
   Track monthly with doctor
   Don't restrict calories - baby needs nutrition!

💧 HYDRATION
   8-10 glasses water/day
   More if exercising or hot weather
   Limit sugary drinks
"""

def get_food_recommendations(trimester='all', dietary_preference='all'):
    """
    Get food recommendations by trimester
    
    Args:
        trimester: 'first', 'second', 'third', 'all'
        dietary_preference: 'all', 'vegetarian', 'high-protein'
    
    Returns:
        dict: Food recommendations
    """
    recommendations = {
        'safe_foods': INDONESIAN_SAFE_FOODS,
        'foods_to_avoid': INDONESIAN_FOODS_TO_AVOID,
        'trimester_focus': TRIMESTER_NUTRITION
    }
    
    return recommendations

def search_recipes(trimester='all', difficulty='easy'):
    """
    Search Indonesian pregnancy recipes
    
    Args:
        trimester: 'first', 'second', 'third', 'all'
        difficulty: 'easy', 'medium', 'all'
    
    Returns:
        list: Matching recipes
    """
    if trimester == 'all':
        return INDONESIAN_RECIPES
    else:
        return [r for r in INDONESIAN_RECIPES if r['trimester'] == trimester or r['trimester'] == 'All']

def format_recipe(recipe):
    """Format recipe for display"""
    result = f"""
🍽️ {recipe['name']}
━━━━━━━━━━━━━━━━━━━━━━━━━━
⏱️ Prep Time: {recipe['prep_time']}
👥 Servings: {recipe['servings']}
🤰 Trimester: {recipe['trimester']}

🛒 INGREDIENTS:
"""
    for ingredient in recipe['ingredients']:
        result += f"\n• {ingredient}"
    
    result += "\n\n👨‍🍳 INSTRUCTIONS:"
    for i, step in enumerate(recipe['instructions'], 1):
        result += f"\n{i}. {step}"
    
    result += f"\n\n💚 Nutritional Benefits: {recipe['nutritional_benefits']}"
    
    return result.strip()

def get_morning_sickness_tips():
    """Get morning sickness management tips"""
    tips = """
🤢 Morning Sickness Management
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🍽️ EATING TIPS:
• Eat small, frequent meals (5-6x/day)
• Keep crackers by bed, eat before getting up
• Avoid empty stomach
• Choose bland, easy-to-digest foods
• Avoid spicy, greasy, strong-smelling foods

💧 HYDRATION:
• Sip water throughout the day
• Try ginger tea or ginger candies
• Ice chips or popsicles
• Electrolyte drinks if vomiting

🌿 NATURAL REMEDIES:
• Ginger (tea, candies, supplements)
• Peppermint tea
• Lemon water
• Vitamin B6 supplements (consult doctor)

⏰ WHEN TO SEE DOCTOR:
• Can't keep any food/fluids down
• Losing weight
• Signs of dehydration
• Vomiting blood
• Severe fatigue or weakness

📞 EMERGENCY CONTACT:
Call your doctor if vomiting is severe!
"""
    return tips

def get_young_mom_nutrition():
    """Get nutrition guide specifically for young moms"""
    return YOUNG_MOM_NUTRITION

def get_warung_safety_guide():
    """Get guide for eating at warungs/restaurants"""
    return WARUNG_SAFETY_TIPS
