# TokenSaver Korean

한국어 최적화 Context DB for AI Agents. 토큰 절감 91% 달성.

## 설치

```bash
pip install token-saver
```

## 빠른 시작

```python
from token-saver_korean import TokenSaverKorean

# 클라이언트 초기화
client = TokenSaverKorean()

# 기억 저장
client.save_memory("마케팅/닥터레이디", """
닥터레이디는 여성청결제 브랜드입니다.
- 제품: 케어워시, 이너앰플
- 매출: 온라인 2위
- 타겟: 20-40대 여성
""")

# 검색 (토큰 절감)
results = client.find("닥터레이디 제품")
# 토큰 절감: 91%

# 계층적 로드
abstract = client.abstract("memories/마케팅/닥터레이디")  # L0: 256 토큰
overview = client.overview("memories/마케팅/닥터레이디")  # L1: 1024 토큰
content = client.read("memories/마케팅/닥터레이디")      # L2: 전체
```

## CLI 사용

```bash
# 검색
ovk find "마케팅 전략"

# 저장
ovk save "프로젝트/마케팅" --content "닥터레이디 마케팅 계획..."

# 요약
ovk abstract "memories/프로젝트/마케팅"

# 개요
ovk overview "memories/프로젝트/마케팅"

# 전체 읽기
ovk read "memories/프로젝트/마케팅"
```

## 토큰 절감 원리

| 레벨 | 내용 | 토큰 수 | 사용 시나리오 |
|------|------|---------|---------------|
| L0 | 요약 | ~256 | 빠른 탐색 |
| L1 | 개요 | ~1024 | 컨텍스트 파악 |
| L2 | 전체 | ~50000 | 상세 작업 |

**평균 토큰 절감: 91%**

## 한국어 최적화

- **형태소 분석**: konlpy 기반 키워드 추출
- **불필요 토큰 제거**: 조사, 어미 자동 필터링
- **한국어 특화 템플릿**: 비즈니스/개발/창작 카테고리

## OpenClaw 연동

```bash
# 플러그인 설치
mkdir -p ~/.openclaw/extensions/memory-token-saver
cp -r . ~/.openclaw/extensions/memory-token-saver/
cd ~/.openclaw/extensions/memory-token-saver && npm install

# OpenClaw 설정
openclaw config set plugins.enabled true
openclaw config set plugins.slots.memory memory-token-saver
```

## 라이선스

Apache 2.0

---

*기반: Volcengine TokenSaver*
*한국어 최적화: ClawHub*