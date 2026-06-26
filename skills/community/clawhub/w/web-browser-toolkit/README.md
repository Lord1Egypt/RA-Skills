# OpenClaw Web Browser Toolkit

OpenClaw용 종합 웹 브라우징 스킬. 정보 수집, 데이터 추출, 변경 모니터링을 하나의 스킬로 통합.

## 설치

```bash
# 글로벌 설치
cp -r openclaw-web-browser/ ~/.openclaw/skills/web-browser-toolkit/

# 또는 프로젝트별 설치
cp -r openclaw-web-browser/ ./skills/web-browser-toolkit/

# 의존성 설치
pip install requests beautifulsoup4
```

## 핵심 개념: 3계층 브라우징 엔진

| 계층 | 도구 | 용도 |
|------|------|------|
| Layer 1 | `web_fetch` / `curl` | 단순 페이지 읽기 (가장 빠름) |
| Layer 2 | `scripts/fetcher.py` | 구조적 데이터 추출 (CSS 셀렉터) |
| Layer 3 | `openclaw browser` | JS 렌더링, 로그인, 인터랙션 |

상황에 맞게 자동 선택. 가벼운 방법부터 시도하고 필요 시 상위 계층으로 승격.

## 주요 기능

### 웹 수집
```bash
python3 scripts/fetcher.py fetch "https://example.com" --output result.json
python3 scripts/fetcher.py search "ICAO UAM regulation" --max-results 10
python3 scripts/fetcher.py batch urls.txt --output batch.json
```

### 항공 프리셋
```bash
python3 scripts/fetcher.py preset faa-ad --query "boeing 737"
python3 scripts/fetcher.py preset icao-safety --query "UAM"
python3 scripts/fetcher.py preset --list
```

### 모니터링
```bash
python3 scripts/monitor.py add --url "https://faa.gov/ad" --name "faa-ad" --check-interval daily
python3 scripts/monitor.py check-all
python3 scripts/monitor.py weekly-report
```

### HTML 변환
```bash
curl -sL "https://example.com" | python3 scripts/html_to_text.py
```

## 파일 구조

```
openclaw-web-browser/
├── SKILL.md                             # 스킬 정의
├── README.md                            # 이 파일
├── scripts/
│   ├── fetcher.py                       # 핵심 웹 수집 엔진
│   ├── monitor.py                       # 변경 모니터링 엔진
│   └── html_to_text.py                  # HTML → 텍스트 변환
└── references/
    ├── aviation_presets.json             # 항공 기관 수집 프리셋
    └── selector_guide.md                # CSS 셀렉터 치트시트
```

## 정기 실행 (cron)

```bash
# crontab -e
0 8 * * * cd ~/skills/web-browser-toolkit && python3 scripts/monitor.py check-all
0 9 * * 1 cd ~/skills/web-browser-toolkit && python3 scripts/monitor.py weekly-report
```
