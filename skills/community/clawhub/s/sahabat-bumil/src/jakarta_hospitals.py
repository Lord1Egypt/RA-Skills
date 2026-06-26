#!/usr/bin/env python3
"""
Jakarta Hospital & OBGYN Finder
Database of hospitals, clinics, and doctors for pregnancy care in Jakarta
"""

# Jakarta Hospital Database (2026)
JAKARTA_HOSPITALS = {
    # South Jakarta (Jaksel)
    'jaksel': [
        {
            'name': 'RSIA Brawijaya Duren Tiga',
            'area': 'Duren Tiga, Pancoran',
            'type': 'RSIA (Specialized)',
            'price_range': 'Rp 15M - 40M (Normal), Rp 25M - 60M (Caesar)',
            'insurance': ['BPJS', 'Private'],
            'facilities': ['NICU', 'ICU Neonatal', 'Kamar VIP', 'Laktasi Konselor'],
            'rating': 4.5,
            'phone': '(021) 79189999',
            'notes': 'Populer, perlu booking early'
        },
        {
            'name': 'RS Pondok Indah - Pondok Indah',
            'area': 'Pondok Indah',
            'type': 'General Hospital',
            'price_range': 'Rp 30M - 70M (Normal), Rp 50M - 100M (Caesar)',
            'insurance': ['BPJS', 'Private'],
            'facilities': ['NICU', 'PICU', 'Kamar VIP', 'Prenatal Classes'],
            'rating': 4.7,
            'phone': '(021) 7657525',
            'notes': 'Premium, fasilitas lengkap'
        },
        {
            'name': 'RS Siloam Hospitals Semanggi',
            'area': 'Semanggi, Setiabudi',
            'type': 'General Hospital',
            'price_range': 'Rp 20M - 50M (Normal), Rp 35M - 70M (Caesar)',
            'insurance': ['BPJS', 'Private'],
            'facilities': ['NICU', 'Kamar VIP', '24/7 Emergency'],
            'rating': 4.4,
            'phone': '(021) 29962888',
            'notes': 'Strategic location, good facilities'
        },
        {
            'name': 'RSIA Bunda Jakarta',
            'area': 'Blok M, Kebayoran Baru',
            'type': 'RSIA (Specialized)',
            'price_range': 'Rp 12M - 35M (Normal), Rp 20M - 50M (Caesar)',
            'insurance': ['BPJS', 'Private'],
            'facilities': ['NICU', 'Kamar VIP', 'Prenatal Classes'],
            'rating': 4.3,
            'phone': '(021) 7209191',
            'notes': 'Established, trusted'
        }
    ],
    
    # Central Jakarta (Jakpus)
    'jakpus': [
        {
            'name': 'RSIA Brawijaya Menteng',
            'area': 'Menteng',
            'type': 'RSIA (Specialized)',
            'price_range': 'Rp 18M - 45M (Normal), Rp 28M - 65M (Caesar)',
            'insurance': ['BPJS', 'Private'],
            'facilities': ['NICU', 'Kamar VIP', 'Laktasi Konselor'],
            'rating': 4.5,
            'phone': '(021) 3904004',
            'notes': 'Central location, popular'
        },
        {
            'name': 'RSUD Tarakan',
            'area': 'Cideng, Gambir',
            'type': 'Public Hospital',
            'price_range': 'BPJS: Gratis, Umum: Rp 5M - 15M',
            'insurance': ['BPJS', 'Private'],
            'facilities': ['NICU', 'Emergency 24/7'],
            'rating': 4.0,
            'phone': '(021) 3441006',
            'notes': 'Good for BPJS, can be crowded'
        }
    ],
    
    # West Jakarta (Jakbar)
    'jakbar': [
        {
            'name': 'RSIA Brawijaya Kedoya',
            'area': 'Kedoya, Kebayoran Lama',
            'type': 'RSIA (Specialized)',
            'price_range': 'Rp 12M - 35M (Normal), Rp 20M - 50M (Caesar)',
            'insurance': ['BPJS', 'Private'],
            'facilities': ['NICU', 'Kamar VIP', 'Prenatal Classes'],
            'rating': 4.4,
            'phone': '(021) 5812008',
            'notes': 'Good value, quality care'
        },
        {
            'name': 'RS Siloam Hospitals Kebon Jeruk',
            'area': 'Kebon Jeruk',
            'type': 'General Hospital',
            'price_range': 'Rp 18M - 45M (Normal), Rp 30M - 60M (Caesar)',
            'insurance': ['BPJS', 'Private'],
            'facilities': ['NICU', 'PICU', 'Kamar VIP'],
            'rating': 4.3,
            'phone': '(021) 25678000',
            'notes': 'Modern facilities'
        }
    ],
    
    # East Jakarta (Jaktim)
    'jaktim': [
        {
            'name': 'RSUD Pasar Rebo',
            'area': 'Pasar Rebo',
            'type': 'Public Hospital',
            'price_range': 'BPJS: Gratis, Umum: Rp 3M - 10M',
            'insurance': ['BPJS', 'Private'],
            'facilities': ['NICU', 'Emergency 24/7'],
            'rating': 3.9,
            'phone': '(021) 8404012',
            'notes': 'Budget-friendly, BPJS friendly'
        },
        {
            'name': 'RS Hermina Jatinegara',
            'area': 'Jatinegara',
            'type': 'General Hospital',
            'price_range': 'Rp 10M - 30M (Normal), Rp 18M - 45M (Caesar)',
            'insurance': ['BPJS', 'Private'],
            'facilities': ['NICU', 'Kamar VIP', 'Prenatal Classes'],
            'rating': 4.2,
            'phone': '(021) 29001500',
            'notes': 'Affordable, good service'
        }
    ],
    
    # North Jakarta (Jakut)
    'jakut': [
        {
            'name': 'RS Pluit',
            'area': 'Pluit, Penjaringan',
            'type': 'General Hospital',
            'price_range': 'Rp 15M - 40M (Normal), Rp 25M - 55M (Caesar)',
            'insurance': ['BPJS', 'Private'],
            'facilities': ['NICU', 'Kamar VIP'],
            'rating': 4.1,
            'phone': '(021) 6696000',
            'notes': 'North Jakarta option'
        },
        {
            'name': 'RSIA Brawijaya Pantai Indah Kapuk',
            'area': 'PIK',
            'type': 'RSIA (Specialized)',
            'price_range': 'Rp 20M - 50M (Normal), Rp 30M - 70M (Caesar)',
            'insurance': ['BPJS', 'Private'],
            'facilities': ['NICU', 'Kamar VIP', 'Laktasi Konselor'],
            'rating': 4.6,
            'phone': '(021) 50888000',
            'notes': 'New, modern facilities'
        }
    ]
}

# Prenatal Classes in Jakarta
PRENATAL_CLASSES = [
    {
        'name': 'Brawijaya Women & Children Hospital',
        'locations': ['Duren Tiga', 'Menteng', 'Kedoya', 'PIK'],
        'price': 'Rp 500K - 1.5M (package)',
        'topics': ['Labor & Delivery', 'Breastfeeding', 'Newborn Care', 'Pain Management'],
        'partner_friendly': True,
        'online': False,
        'phone': '(021) 79189999'
    },
    {
        'name': 'RS Pondok Indah',
        'locations': ['Pondok Indah', 'Puri Indah'],
        'price': 'Rp 1M - 2M (package)',
        'topics': ['Prenatal Yoga', 'Labor Techniques', 'Breastfeeding', 'Baby Care'],
        'partner_friendly': True,
        'online': True,
        'phone': '(021) 7657525'
    },
    {
        'name': 'Parentalk (Online)',
        'locations': ['Online'],
        'price': 'Rp 300K - 800K (per class)',
        'topics': ['Various topics, expert speakers'],
        'partner_friendly': True,
        'online': True,
        'website': 'parentalk.id'
    },
    {
        'name': 'The Asian Parent Indonesia',
        'locations': ['Online & Offline events'],
        'price': 'Free - Rp 500K',
        'topics': ['Parenting workshops', 'Pregnancy webinars'],
        'partner_friendly': True,
        'online': True,
        'website': 'theasianparent.co.id'
    }
]

# OBGYN Doctors (Popular in Jakarta)
OBGYN_DOCTORS = {
    'jaksel': [
        {
            'name': 'Dr. ___ , SpOG',
            'hospital': 'RSIA Brawijaya Duren Tiga',
            'schedule': 'Mon, Wed, Fri',
            'price': 'Rp 500K - 1M per visit',
            'languages': ['Indonesian', 'English'],
            'notes': 'Need to book in advance'
        }
        # Add more doctors as needed
    ]
}

# BPJS Information
BPJS_INFO = {
    'coverage': [
        '✅ Prenatal checkups (min. 6x during pregnancy)',
        '✅ Ultrasound (2x during pregnancy)',
        '✅ Blood tests & lab work',
        '✅ Delivery (normal & caesar)',
        '✅ Complications coverage',
        '✅ Postpartum care',
        '✅ Newborn care (first 28 days)'
    ],
    'requirements': [
        'Active BPJS membership',
        'Referral from Puskesmas (for non-emergency)',
        'KTP & KK copies',
        'Buku KIA (Kesehatan Ibu & Anak)'
    ],
    'process': [
        '1. Register at Puskesmas with KTP & KK',
        '2. Get referral to hospital',
        '3. Bring referral to chosen hospital',
        '4. Register at hospital BPJS counter',
        '5. Regular checkups as scheduled'
    ],
    'hospitals_accepting_bpjs': [
        'RSUD Tarakan',
        'RSUD Pasar Rebo',
        'RSIA Brawijaya (selected branches)',
        'RS Siloam (selected branches)',
        'Most RSUD hospitals'
    ]
}

def search_hospitals(area='all', budget_range='all', insurance='all'):
    """
    Search hospitals by criteria
    
    Args:
        area: 'jaksel', 'jakpus', 'jakbar', 'jaktim', 'jakut', 'all'
        budget_range: 'budget' (<15M), 'mid' (15-30M), 'premium' (>30M)
        insurance: 'BPJS', 'Private', 'all'
    
    Returns:
        list: Matching hospitals
    """
    results = []
    
    # Filter by area
    if area == 'all':
        hospitals = []
        for area_hospitals in JAKARTA_HOSPITALS.values():
            hospitals.extend(area_hospitals)
    else:
        hospitals = JAKARTA_HOSPITALS.get(area, [])
    
    # Filter by budget
    for hospital in hospitals:
        price = hospital['price_range']
        
        # Budget filter
        if budget_range == 'budget':
            if 'Rp 5M' in price or 'Rp 10M' in price or 'Rp 12M' in price:
                results.append(hospital)
        elif budget_range == 'mid':
            if 'Rp 15M' in price or 'Rp 20M' in price:
                results.append(hospital)
        elif budget_range == 'premium':
            if 'Rp 30M' in price or 'Rp 50M' in price or 'Rp 70M' in price:
                results.append(hospital)
        else:
            results.append(hospital)
    
    # Filter by insurance
    if insurance != 'all':
        results = [h for h in results if insurance in h['insurance']]
    
    return results

def format_hospital_info(hospital):
    """Format hospital information for display"""
    result = f"""
🏥 {hospital['name']}
━━━━━━━━━━━━━━━━━━━━━━━━━━
📍 Area: {hospital['area']}
🏨 Type: {hospital['type']}
💰 Price Range: {hospital['price_range']}
🏆 Rating: ⭐ {hospital['rating']}/5.0
📞 Phone: {hospital['phone']}
💳 Insurance: {', '.join(hospital['insurance'])}
🏥 Facilities: {', '.join(hospital['facilities'])}
📝 Notes: {hospital['notes']}
    """
    return result.strip()

def get_bpjs_info():
    """Get BPJS pregnancy coverage information"""
    result = """
🏥 BPJS Pregnancy Coverage
━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ COVERED SERVICES:
"""
    for item in BPJS_INFO['coverage']:
        result += f"\n{item}"
    
    result += "\n\n📋 REQUIREMENTS:"
    for item in BPJS_INFO['requirements']:
        result += f"\n{item}"
    
    result += "\n\n🔄 PROCESS:"
    for item in BPJS_INFO['process']:
        result += f"\n{item}"
    
    result += "\n\n🏥 HOSPITALS ACCEPTING BPJS:"
    for hospital in BPJS_INFO['hospitals_accepting_bpjs'][:5]:
        result += f"\n• {hospital}"
    
    return result.strip()

def get_prenatal_classes(area='all'):
    """Get prenatal classes information"""
    result = """
🎓 Prenatal Classes in Jakarta
━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    for cls in PRENATAL_CLASSES:
        result += f"""

📚 {cls['name']}
   📍 Locations: {', '.join(cls['locations'])}
   💰 Price: {cls['price']}
   👫 Partner Friendly: {'✅ Yes' if cls['partner_friendly'] else '❌ No'}
   💻 Online: {'✅ Yes' if cls['online'] else '❌ No'}
   📞 Contact: {cls.get('phone', cls.get('website', 'N/A'))}
   📝 Topics: {', '.join(cls['topics'][:3])}...
"""
    return result.strip()

def compare_hospitals(hospital1_name, hospital2_name):
    """Compare two hospitals"""
    # Search for hospitals
    found1 = None
    found2 = None
    
    for area_hospitals in JAKARTA_HOSPITALS.values():
        for hospital in area_hospitals:
            if hospital1_name.lower() in hospital['name'].lower():
                found1 = hospital
            if hospital2_name.lower() in hospital['name'].lower():
                found2 = hospital
    
    if not found1 or not found2:
        return "❌ Hospital(s) not found. Please check the names."
    
    result = f"""
🆚 Hospital Comparison
━━━━━━━━━━━━━━━━━━━━━━━━━━

🏥 {found1['name']} vs {found2['name']}

📍 Location:
   • {found1['name']}: {found1['area']}
   • {found2['name']}: {found2['area']}

💰 Price:
   • {found1['name']}: {found1['price_range']}
   • {found2['name']}: {found2['price_range']}

🏆 Rating:
   • {found1['name']}: ⭐ {found1['rating']}/5.0
   • {found2['name']}: ⭐ {found2['rating']}/5.0

💳 Insurance:
   • {found1['name']}: {', '.join(found1['insurance'])}
   • {found2['name']}: {', '.join(found2['insurance'])}

🏥 Facilities:
   • {found1['name']}: {', '.join(found1['facilities'][:3])}...
   • {found2['name']}: {', '.join(found2['facilities'][:3])}...

📝 Notes:
   • {found1['name']}: {found1['notes']}
   • {found2['name']}: {found2['notes']}
"""
    return result.strip()
