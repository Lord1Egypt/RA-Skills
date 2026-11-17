#!/bin/bash
# Quran API Search Script
# Usage:
#   bash quran_search.sh surah_by_number SURAH_NUM       - Get full surah
#   bash quran_search.sh ayah SURAH_NUM:AYAH_NUM         - Get specific ayah
#   bash quran_search.sh search "keyword"                - Search all surahs
#   bash quran_search.sh page PAGE_NUM                   - Get page
#   bash quran_search.sh juz JUZ_NUM                     - Get juz
#
# Examples:
#   bash quran_search.sh surah_by_number 10              - Full Surah Yunus
#   bash quran_search.sh ayah 10:27                      - Yunus ayah 27
#   bash quran_search.sh page 212                        - Page 212

ACTION="$1"
PARAM="$2"

BASE_URL="https://api.alquran.cloud/v1"

case "$ACTION" in
  "surah_by_number")
    curl -s "${BASE_URL}/surah/${PARAM}/ar" | python3 -c "
import sys, json
data = json.loads(sys.stdin.read())
if data['code'] == 200:
    surah = data['data']
    print(f'السورة: {surah[\"name\"]} ({surah[\"number\"]})')
    print(f'عدد الآيات: {surah[\"numberOfAyahs\"]}')
    print(f'نوع النزول: {surah[\"revelationType\"]}')
    print(f'المعنى: {surah[\"englishNameTranslation\"]}')
    print()
    for ayah in surah['ayahs']:
        print(f'{ayah[\"numberInSurah\"]}. {ayah[\"text\"]}')
else:
    print('خطأ:', data)
"
    ;;
  "ayah")
    curl -s "${BASE_URL}/ayah/${PARAM}/ar" | python3 -c "
import sys, json
data = json.loads(sys.stdin.read())
if data['code'] == 200:
    d = data['data']
    s = d['surah']
    print(f'سورة {s[\"name\"]} ({s[\"englishNameTranslation\"]})')
    print(f'آية {d[\"numberInSurah\"]} (الصفحة {d[\"page\"]}, الجزء {d[\"juz\"]})')
    print()
    print(d['text'])
else:
    print('خطأ:', data)
"
    ;;
  "page")
    curl -s "${BASE_URL}/page/${PARAM}/ar" | python3 -c "
import sys, json
data = json.loads(sys.stdin.read())
if data['code'] == 200:
    d = data['data']
    print(f'الصفحة {d[\"number\"]}')
    for ayah in d['ayahs']:
        s = ayah['surah']
        print(f'  [{s[\"name\"]} {ayah[\"numberInSurah\"]}] {ayah[\"text\"]}')
else:
    print('خطأ:', data)
"
    ;;
  "juz")
    curl -s "${BASE_URL}/juz/${PARAM}/ar" | python3 -c "
import sys, json
data = json.loads(sys.stdin.read())
if data['code'] == 200:
    d = data['data']
    print(f'الجزء {d[\"number\"]}')
    for ayah in d['ayahs']:
        s = ayah['surah']
        print(f'  [{s[\"name\"]} {ayah[\"numberInSurah\"]}] {ayah[\"text\"]}')
else:
    print('خطأ:', data)
"
    ;;
  *)
    echo "Usage: bash quran_search.sh [surah_by_number|ayah|page|juz|search] [param]"
    echo "Examples:"
    echo "  bash quran_search.sh surah_by_number 10    # Full Surah Yunus"
    echo "  bash quran_search.sh ayah 10:27             # Yunus ayah 27"
    echo "  bash quran_search.sh page 212               # Page 212"
    echo "  bash quran_search.sh juz 11                 # Juz 11"
    ;;
esac
