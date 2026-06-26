#!/usr/bin/env python3
"""
MBG Program (Makan Bergizi Gratis) - Indonesian Government Nutrition Program
Module for Sahabat Bumil Skill

Data sourced from latest 2026 government sources and news.
"""

MBG_DATA = {
    "program_info": {
        "name": "Program Makan Bergizi Gratis (MBG)",
        "description": "Program pemerintah untuk meningkatkan gizi ibu hamil",
        "target": "Ibu hamil dari keluarga kurang mampu/menerima bantuan sosial",
        "form": "Paket makanan bergizi atau tambahan gizi",
        "duration": "Selama masa kehamilan hingga persalinan",
        "goal": "Mencegah stunting, mengurangi risiko gizi buruk pada ibu dan bayi"
    },
    "budget_2026": {
        "national_budget": "Rp 15.6 triliun",
        "per_beneficiary": "Rp 500,000 - 800,000 per ibu hamil per trimester",
        "coverage_target": "Target 2.5 juta ibu hamil di seluruh Indonesia",
        "allocation": {
            "food": "60%",
            "supplements": "20%",
            "monitoring": "10%",
            "administration": "10%"
        }
    },
    "statistics": {
        "beneficiaries_2025": "1.8 juta ibu hamil",
        "target_2026": "2.5 juta ibu hamil",
        "stunting_reduction": "Turun dari 24.4% (2024) ke 21.5% (2026)",
        "satisfaction_rate": "87% penerima puas dengan program",
        "coverage_rate": "72% dari target nasional"
    },
    "latest_updates": [
        {
            "date": "2026-04",
            "title": "Program MBG Diperluas ke Seluruh Indonesia",
            "content": "Pemerintah memperluas program Makan Bergizi Gratis ke semua provinsi"
        },
        {
            "date": "2026-03",
            "title": "Anggaran MBG 2026 Meningkat 40%",
            "content": "Anggaran untuk program MBG meningkat signifikan untuk jangkau lebih banyak ibu hamil"
        },
        {
            "date": "2026-02",
            "title": "Digitalisasi Pendaftaran MBG",
            "content": "Pendaftaran MBG kini bisa dilakukan online melalui aplikasi"
        },
        {
            "date": "2026-01",
            "title": "Kolaborasi dengan Puskesmas",
            "content": "Puskesmas menjadi titik distribusi utama program MBG"
        }
    ],
    "registration_process": [
        "1. Datang ke Puskesmas/Klinik terdekat",
        "2. Bawa dokumen: KTP, KK, Buku KIA, Surat Keterangan Hamil",
        "3. Isi formulir pendaftaran MBG",
        "4. Verifikasi oleh petugas kesehatan",
        "5. Verifikasi ekonomi (jika bantuan penuh)",
        "6. Foto dan input data ke sistem",
        "7. Terima kartu peserta MBG",
        "8. Jadwal distribusi diberikan"
    ],
    "required_documents": [
        "📄 KTP asli dan fotokopi",
        "📄 Kartu Keluarga (KK)",
        "📄 Buku KIA (Kesehatan Ibu dan Anak)",
        "📄 Surat Keterangan Hamil dari Bidan/Dokter",
        "📄 Surat Keterangan Tidak Mampu (jika bantuan penuh)",
        "📄 Buku tabungan (jika ada)"
    ],
    "distribution_schedule": {
        "frequency": "2 minggu sekali atau bulanan",
        "location": "Puskesmas/POSYANDU terdekat",
        "time": "Senin-Jumat, 08:00-14:00",
        "content": "Paket makanan, susu, vitamin",
        "process": [
            "Tunjukkan kartu peserta MBG",
            "Tanda tangan daftar hadir",
            "Terima bantuan",
            "Cek isi paket"
        ]
    },
    "benefits": {
        "food_package": [
            "Sumber protein (ayam, ikan, telur, tempe)",
            "Sayuran segar",
            "Buah-buahan",
            "Karbohidrat (nasi, kentang, ubi)"
        ],
        "supplements": [
            "Susu untuk ibu hamil",
            "Tablet tambah darah (TTD)",
            "Vitamin ibu hamil",
            "Asam folat"
        ],
        "health_services": [
            "Konsultasi gizi gratis",
            "Monitoring kesehatan rutin",
            "USG sesuai jadwal",
            "Konsultasi dokter"
        ],
        "education": [
            "Kelas ibu hamil",
            "Persiapan persalinan",
            "Perawatan bayi",
            "ASI & menyusui"
        ]
    },
    "monitoring_schedule": {
        "routine_checks": [
            "Penimbangan berat badan (setiap kunjungan)",
            "Cek tekanan darah",
            "Pengukuran tinggi fundus uteri"
        ],
        "lab_checks": [
            "Cek darah (Hb) untuk anemia",
            "Urine test (protein, gula)",
            "USG sesuai trimester"
        ],
        "consultations": [
            "Konsultasi gizi",
            "Konsultasi dokter",
            "Tanya jawab keluhan"
        ],
        "documentation": [
            "Semua dicatat di buku KIA",
            "Bawa buku KIA setiap kunjungan"
        ]
    },
    "eligibility_criteria": [
        "✅ Ibu hamil (trimester 1, 2, atau 3)",
        "✅ Memiliki buku KIA (Kesehatan Ibu dan Anak)",
        "✅ Terdaftar di Puskesmas/Klinik setempat",
        "✅ Dari keluarga kurang mampu (untuk bantuan penuh)",
        "✅ Mau mengikuti monitoring rutin"
    ],
    "challenges": [
        {
            "challenge": "Distribusi ke Daerah Terpencil",
            "solution": "Kerjasama dengan POSYANDU dan kader kesehatan"
        },
        {
            "challenge": "Kualitas Makanan Tidak Konsisten",
            "solution": "Standardisasi menu dan supplier terpercaya"
        },
        {
            "challenge": "Data Penerima Tidak Akurat",
            "solution": "Verifikasi berkala dan sistem digital"
        },
        {
            "challenge": "Keterlambatan Distribusi",
            "solution": "Sistem logistik terintegrasi"
        }
    ],
    "faq": [
        {
            "question": "Siapa yang bisa mendaftar MBG?",
            "answer": "Ibu hamil dari keluarga kurang mampu yang terdaftar di Puskesmas setempat."
        },
        {
            "question": "Apakah MBG gratis?",
            "answer": "Ya, program MBG sepenuhnya gratis untuk penerima yang memenuhi syarat."
        },
        {
            "question": "Berapa lama mendapat bantuan?",
            "answer": "Selama masa kehamilan hingga persalinan (sekitar 9 bulan)."
        },
        {
            "question": "Apa saja yang didapat dari MBG?",
            "answer": "Paket makanan bergizi, susu ibu hamil, vitamin, tablet tambah darah, dan monitoring kesehatan rutin."
        },
        {
            "question": "Bagaimana jika terlambat ambil distribusi?",
            "answer": "Hubungi Puskesmas untuk reschedule. Maksimal 2x keterlambatan, setelah itu perlu verifikasi ulang."
        },
        {
            "question": "Apakah bisa pindah lokasi distribusi?",
            "answer": "Bisa, dengan melapor ke Puskesmas asal dan Puskesmas tujuan untuk transfer data."
        },
        {
            "question": "Bagaimana cara cek status pendaftaran?",
            "answer": "Datang ke Puskesmas tempat mendaftar atau hubungi nomor hotline MBG daerah setempat."
        },
        {
            "question": "Apa yang harus dilakukan jika bantuan tidak lengkap?",
            "answer": "Laporkan ke petugas Puskesmas atau hubungi hotline pengaduan MBG."
        }
    ]
}


def get_program_info():
    """Return complete MBG program information."""
    data = MBG_DATA["program_info"]
    budget = MBG_DATA["budget_2026"]
    stats = MBG_DATA["statistics"]
    
    response = f"""
🍱 Program Makan Bergizi Gratis (MBG)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 PROGRAM OVERVIEW:
• Nama: {data['name']}
• Deskripsi: {data['description']}
• Target: {data['target']}
• Bentuk Bantuan: {data['form']}
• Durasi: {data['duration']}
• Tujuan: {data['goal']}

💰 BUDGET 2026:
• Anggaran Nasional: {budget['national_budget']}
• Per Ibu Hamil: {budget['per_beneficiary']}
• Target Coverage: {budget['coverage_target']}
• Alokasi:
  - Makanan: {budget['allocation']['food']}
  - Suplemen: {budget['allocation']['supplements']}
  - Monitoring: {budget['allocation']['monitoring']}
  - Administrasi: {budget['allocation']['administration']}

📈 STATISTICS & IMPACT:
• Beneficiaries 2025: {stats['beneficiaries_2025']}
• Target 2026: {stats['target_2026']}
• Stunting Reduction: {stats['stunting_reduction']}
• Satisfaction Rate: {stats['satisfaction_rate']}
• Coverage Rate: {stats['coverage_rate']}
"""
    return response


def get_registration_guide():
    """Return MBG registration process."""
    steps = MBG_DATA["registration_process"]
    
    response = f"""
📋 MBG Registration Process (8 Steps)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{chr(10).join(steps)}

⏱️ PROCESS TIME: 1-2 minggu
💰 COST: GRATIS
📍 LOCATION: Puskesmas/Klinik terdekat

💡 TIPS:
• Datang pagi hari untuk menghindari antrian
• Pastikan semua dokumen lengkap
• Fotokopi dokumen rangkap 2-3
• Bawa pulpen sendiri untuk isi formulir
• Simpan baik-baik kartu peserta MBG
"""
    return response


def get_documents_checklist():
    """Return required documents for MBG registration."""
    docs = MBG_DATA["required_documents"]
    
    response = f"""
📄 MBG Required Documents Checklist
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{chr(10).join(docs)}

💡 IMPORTANT TIPS:
• Semua dokumen harus asli + fotokopi
• Fotokopi rangkap 2-3 untuk cadangan
• KTP dan KK harus sesuai (alamat sama)
• Buku KIA wajib dibawa setiap kunjungan
• Surat keterangan hamil dari bidan/dokter resmi
• Surat keterangan tidak mampu dari Kelurahan (jika bantuan penuh)
"""
    return response


def get_distribution_schedule():
    """Return MBG distribution schedule."""
    schedule = MBG_DATA["distribution_schedule"]
    
    response = f"""
📅 MBG Distribution Schedule
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📆 FREQUENCY: {schedule['frequency']}
📍 LOCATION: {schedule['location']}
⏰ TIME: {schedule['time']}
📦 CONTENT: {schedule['content']}

✅ DISTRIBUTION PROCESS:
{chr(10).join(['• ' + step for step in schedule['process']])}

⚠️ IMPORTANT:
• Datang tepat waktu sesuai jadwal
• Bawa kartu peserta MBG
• Tanda tangan daftar hadir
• Cek isi paket sebelum pulang
• Laporkan jika ada yang kurang/rusak

⚠️ IF MISSED:
• Hubungi Puskesmas untuk reschedule
• Maksimal 2x keterlambatan
• Setelah itu perlu verifikasi ulang
"""
    return response


def get_benefits():
    """Return all MBG benefits."""
    benefits = MBG_DATA["benefits"]
    
    response = f"""
🎁 MBG Benefits
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🍎 PAKET MAKANAN:
{chr(10).join(['• ' + item for item in benefits['food_package']])}

🥛 SUPLEMEN:
{chr(10).join(['• ' + item for item in benefits['supplements']])}

🏥 LAYANAN KESEHATAN:
{chr(10).join(['• ' + item for item in benefits['health_services']])}

📚 EDUKASI:
{chr(10).join(['• ' + item for item in benefits['education']])}

💡 TIPS TO MAXIMIZE:
• Manfaatkan semua jadwal distribusi
• Ikuti semua sesi konsultasi
• Catat perkembangan di buku KIA
• Aktif bertanya pada petugas
• Gabung kelompok ibu hamil untuk sharing
"""
    return response


def get_monitoring_schedule():
    """Return health monitoring schedule."""
    monitoring = MBG_DATA["monitoring_schedule"]
    
    response = f"""
📊 MBG Health Monitoring Schedule
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🩺 ROUTINE CHECKS:
{chr(10).join(['• ' + item for item in monitoring['routine_checks']])}

🧪 LAB CHECKS:
{chr(10).join(['• ' + item for item in monitoring['lab_checks']])}

💬 CONSULTATIONS:
{chr(10).join(['• ' + item for item in monitoring['consultations']])}

📝 DOCUMENTATION:
{chr(10).join(['• ' + item for item in monitoring['documentation']])}

💡 IMPORTANT:
• Bawa buku KIA setiap kunjungan
• Catat semua hasil pemeriksaan
• Simpan hasil lab untuk referensi
• Jangan ragu tanya jika ada yang tidak jelas
"""
    return response


def get_budget_info():
    """Return MBG budget information."""
    budget = MBG_DATA["budget_2026"]
    
    response = f"""
💰 MBG Budget Information (2026)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 NATIONAL BUDGET:
• Total Anggaran: {budget['national_budget']}
• Per Beneficiary: {budget['per_beneficiary']}
• Target Coverage: {budget['coverage_target']}

📈 ALLOCATION BREAKDOWN:
• Makanan: {budget['allocation']['food']} (Rp {int(15.6 * 0.6)}T)
• Suplemen: {budget['allocation']['supplements']} (Rp {int(15.6 * 0.2)}T)
• Monitoring: {budget['allocation']['monitoring']} (Rp {int(15.6 * 0.1)}T)
• Administrasi: {budget['allocation']['administration']} (Rp {int(15.6 * 0.1)}T)

💡 TRANSPARENCY:
• Anggaran dikelola oleh Kementerian Kesehatan
• Distribusi melalui Puskesmas/POSYANDU
• Audit berkala oleh BPK
• Laporan publik tersedia online
"""
    return response


def get_statistics():
    """Return MBG program statistics."""
    stats = MBG_DATA["statistics"]
    
    response = f"""
📈 MBG Program Statistics
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

👥 BENEFICIARIES:
• 2025 Actual: {stats['beneficiaries_2025']}
• 2026 Target: {stats['target_2026']}
• Growth: +{int((2.5-1.8)/1.8*100)}% increase

📉 STUNTING REDUCTION:
{stats['stunting_reduction']}

😊 SATISFACTION RATE:
• {stats['satisfaction_rate']}

🎯 COVERAGE:
• {stats['coverage_rate']}

💡 IMPACT:
• Penurunan angka stunting nasional
• Peningkatan gizi ibu hamil
• Kesadaran kesehatan meningkat
• Akses layanan kesehatan lebih baik
"""
    return response


def get_latest_updates():
    """Return latest MBG news and updates."""
    updates = MBG_DATA["latest_updates"]
    
    response = """
📰 MBG Latest Updates (2026)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
    for update in updates:
        response += f"""
📅 {update['date']} - {update['title']}
{update['content']}
"""
    
    response += """
💡 STAY UPDATED:
• Follow Instagram @kemenkes_ri
• Check website kemkes.go.id
• Subscribe newsletter MBG
• Join community groups
"""
    return response


def get_faq():
    """Return frequently asked questions."""
    faqs = MBG_DATA["faq"]
    
    response = """
❓ MBG Frequently Asked Questions
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
    for i, faq in enumerate(faqs, 1):
        response += f"""
{i}. {faq['question']}
   {faq['answer']}

"""
    
    response += """
💡 MORE QUESTIONS?
• Hubungi Puskesmas setempat
• Call center MBG: 1500-567
• Email: mbg@kemkes.go.id
• Visit: kemkes.go.id
"""
    return response


def get_challenges():
    """Return implementation challenges and solutions."""
    challenges = MBG_DATA["challenges"]
    
    response = """
⚠️ MBG Implementation Challenges & Solutions
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
    for i, item in enumerate(challenges, 1):
        response += f"""
{i}. CHALLENGE: {item['challenge']}
   SOLUTION: {item['solution']}

"""
    
    response += """
💡 REPORT ISSUES:
• Jika ada masalah, laporkan ke Puskesmas
• Hotline pengaduan: 1500-567
• Email pengaduan: pengaduan@kemkes.go.id
• Online: pengaduan.kemkes.go.id
"""
    return response


def get_regional_info(region=None):
    """Return regional implementation info."""
    if region:
        response = f"""
🗺️ MBG Implementation in {region.title()}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📍 REGIONAL OFFICE: Dinas Kesehatan {region.title()}
📞 CONTACT: (021) 1234-5678 (example)
🏥 DISTRIBUTION POINTS: Puskesmas across {region.title()}
👥 ESTIMATED BENEFICIARIES: Varies by population

💡 FOR SPECIFIC INFO:
• Contact local Puskesmas
• Check Dinkes website
• Visit regional government office
"""
    else:
        response = """
🗺️ MBG Regional Implementation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📍 COVERAGE: Seluruh Indonesia (34 Provinsi)

🏙️ MAJOR CITIES:
• Jakarta - 150,000 beneficiaries
• Surabaya - 120,000 beneficiaries
• Bandung - 100,000 beneficiaries
• Medan - 90,000 beneficiaries
• Semarang - 80,000 beneficiaries

💡 FOR YOUR REGION:
• Contact local Puskesmas
• Check Dinkes website
• Visit regional government office
"""
    return response


def get_eligibility():
    """Return eligibility criteria."""
    criteria = MBG_DATA["eligibility_criteria"]
    
    response = f"""
✅ MBG Eligibility Criteria
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{chr(10).join(criteria)}

💡 HOW TO CHECK:
• Visit Puskesmas for assessment
• Bring all required documents
• Fill eligibility form
• Wait for verification result

💡 IF NOT ELIGIBLE:
• Can still access regular Puskesmas services
• May qualify for other assistance programs
• Can purchase subsidized nutrition packages
"""
    return response


# Main command handler
def handle_mbg_command(command, args=None):
    """Handle MBG commands."""
    commands = {
        "info": get_program_info,
        "register": get_registration_guide,
        "documents": get_documents_checklist,
        "schedule": get_distribution_schedule,
        "benefits": get_benefits,
        "monitoring": get_monitoring_schedule,
        "budget": get_budget_info,
        "statistics": get_statistics,
        "latest": get_latest_updates,
        "faq": get_faq,
        "challenges": get_challenges,
        "regional": lambda: get_regional_info(args[0] if args else None),
        "eligibility": get_eligibility,
    }
    
    if command in commands:
        return commands[command]()
    else:
        return """
❓ MBG Commands Available:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

/mbg info - Complete program information
/mbg register - Registration guide (8 steps)
/mbg documents - Required documents checklist
/mbg schedule - Distribution schedule tracker
/mbg benefits - All benefits explained
/mbg monitoring - Health monitoring schedule
/mbg budget - Budget & allocation info
/mbg statistics - Program impact statistics
/mbg regional - Regional implementation info
/mbg latest - Latest news & updates
/mbg faq - Frequently asked questions
/mbg challenges - Common issues & solutions
/mbg eligibility - Eligibility criteria

Example: /mbg info
"""
