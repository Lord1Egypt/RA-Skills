# modules/prompts/translation.py
"""
번역 관련 프롬프트 템플릿
"""

SYSTEM_PROMPT = "당신은 보안 및 기술 전문 번역가입니다. 자연스럽고 정확하며 업계 표준 용어를 사용하는 번역을 제공합니다."

USER_PROMPT_TEMPLATE = """다음 텍스트를 {target_lang}로 번역해 주세요.

요구사항:
- 자연스러운 흐름: 직역보다는 의미가 통하도록 자연스럽게 번역
- 전문 용어: 업계 표준 기술 용어 사용 (예: vulnerability→취약점, exploit→익스플로잇)
- 문맥 유지: 원래의 의미와 어조 유지
- 출력: 번역된 텍스트만, 부가 설명 없음

예시:
입력: "Remote Code Execution vulnerability allows attackers to execute arbitrary commands."
출력: "원격 코드 실행 취약점을 통해 공격자가 임의의 명령을 실행할 수 있습니다."

원본 텍스트: {text}"""
