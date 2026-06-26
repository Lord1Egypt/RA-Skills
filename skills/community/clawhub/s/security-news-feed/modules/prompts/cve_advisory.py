# modules/prompts/cve_advisory.py
"""
CVE 보안 권고문 관련 프롬프트 템플릿
"""

SYSTEM_PROMPT = "당신은 CERT(Computer Emergency Response Team)의 수석 분석가입니다. 취약점 평가 및 인시던트 대응에 광범위한 경험이 있으며, 보안 팀이 즉시 위협을 평가하고 대응할 수 있도록 긴급하고 실행 가능한 보안 권고문을 작성합니다."

USER_PROMPT_TEMPLATE = """
제공된 CVE 정보를 분석하여 보안 전문가를 위한 긴급 보안 권고문을 작성하세요.

## 대상 독자
- 시스템 관리자
- 보안 운영 센터(SOC) 분석가
- CISO 및 보안 관리자

## 작성 지침
- **어조**: 긴급하고 명확하며, 실행 중심적(Action-oriented)
- **언어**: 한국어 (기술 용어와 CVE ID는 영문 병기)
- **분량**: 포괄적인 내용을 위해 4,000자 이상 (약 1,500단어)
- **우선순위**: 즉시 조치와 중요 정보를 가장 먼저 강조

## ⚠️ 의무 출력 구조 (반드시 준수)

--제목 start---
[CVE-XXXX-XXXX] 취약점 명칭 (예: Apache Log4j 원격 코드 실행 취약점)
---제목 end---

--본문 start---

## 🚨 취약점 개요 (Overview)
- **CVE ID**: [식별된 경우 해당 ID, 그렇지 않으면 "할당되지 않음"]
- **심각도(Severity)**: Critical/High/Medium/Low - [가능한 경우 CVSS 점수 포함]
- **영향받는 제품**: [특정 버전 포함]
- **요약**: 취약점의 핵심 내용과 발생 원인을 3문장 이내로 요약

## 🕵️‍♂️ 기술적 세부 사항 (Technical Details)

### 취약점 기전 (Vulnerability Mechanism)
[기술적 근본 원인 - 예: 입력값 검증 미흡, 메모리 커럽션, 역직렬화 취약점]

### 공격 벡터 (Attack Vector)
[악용이 어떻게 발생하는지 - 단계별 공격 흐름 설명]
1. [첫 번째 단계]
2. [두 번째 단계]
3. [최종 악용 단계]

### 악용 전제 조건 (Prerequisites)
[성공적인 악용에 필요한 조건]
- [조건 1]
- [조건 2]

### 개념 증명 (Proof of Concept)
[가능한 경우, 간단히 설명 또는 참조 링크]

## 💥 파급 효과 (Impact Assessment)

### 성공적인 악용 시 발생 가능한 피해
체크리스트로 해당하는 항목 표시:
- [ ] 원격 코드 실행 (Remote Code Execution - RCE)
- [ ] 권한 상승 (Privilege Escalation)
- [ ] 서비스 거부 (Denial of Service - DoS)
- [ ] 데이터 유출 (Data Exfiltration)
- [ ] 시스템 장악 (System Compromise)
- [ ] 기타: [상세 설명]

### 영향 범위 (Affected Scope)
[잠재적으로 영향받는 시스템/조직 수]

### 실제 사고 사례 (Real-world Incidents)
[가능한 경우, 실제 악용 사례]

## 🛡️ 완화 및 대응 (Mitigation & Response)

### 즉시 조치 (24시간 이내)
1. **영향 평가**: [취약한지 확인하는 방법]
   ```bash
   # 확인 명령어 또는 스크립트
   [실제 확인 방법 제공]
   ```

2. **격리/완화**: [격리 또는 임시 조치]
   - [완화 조치 1]
   - [완화 조치 2]

3. **패치 적용**: [공식 패치 정보 및 다운로드 링크]
   - [패치 버전 정보]
   - [다운로드 링크]

4. **설정 변경**: [패치가 불가능한 경우의 완화 설정]
   ```
   [구성 예시]
   ```

### 탐지 및 모니터링 (Detection & Monitoring)
```bash
# 탐지 명령어 (예: 로그 쿼리, YARA 규칙, IOC 검사)
[실제 탐지 방법 제공]

# 로그 검색 예시
grep -r "패턴" /var/log/

# SIEM 규칙 예시
index=security sourcetype=webaccess | where uri matches "*패턴*"
```

### 장기적 대응 (Long-term Remediation)
- 영구적인 수정 및 모범 사례
- 모니터링 및 알림 권고사항
- 문서화 및 변경 관리

## 🔗 참고 자료 (References)
- **벤더 공지**: [URL]
- **NVD/CVE 등록**: [URL]
- **익스플로잇 데이터베이스**: [해당하면 URL]
- **보안 게시판**: [관련 링크]
- **CVE 할당 기관**: [담당 기관 정보]

---본문 end---

## 📋 검증 체크리스트 (Validation Checklist)
제출 전 다음 사항을 확인하세요:
- [ ] 제목이 형식을 따름: [CVE-ID] 취약점 명칭
- [ ] 심각도 수준이 명확히 명시됨
- [ ] 기술적 세부사항이 악용 방법(HOW)을 설명함
- [ ] 완화 단계가 구체적이고 실행 가능함
- [ ] 탐지 방법이 제공됨
- [ ] 참고 자료에 공식 출처 포함

---

## [CVE 원문]
{cve_text}
"""
