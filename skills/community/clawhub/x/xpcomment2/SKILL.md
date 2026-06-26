---
name: xpcomment
version: 1.0.0
description: >
  JPEG/이미지 파일의 XPComment(Windows 사진 코멘트) 메타데이터를 exiftool로 읽고, 추가하고, 제거하는 skill.
  사용자가 "xpcomment add", "xpcomment remove", "xpcomment read", "코멘트 추가", "사진에 태그", 
  "exiftool comment", "XPComment", "이미지 메타데이터 코멘트"를 언급하면 반드시 이 skill을 사용하라.
  사용자가 이미지 파일에 텍스트 코멘트를 붙이거나 제거하거나 확인하려 할 때도 즉시 이 skill을 참조하라.
compatibility:
  required_tools: [tmux, bash]
  dependencies: [exiftool]
---

# XPComment Skill

이미지 파일의 XPComment 메타데이터를 exiftool로 관리한다.
XPComment는 Windows 탐색기 → 속성 → 자세히 탭의 "설명(Comments)" 필드에 표시되는 값이다.

---

## 명령어 패턴

사용자는 아래와 같은 자연어 또는 단축 명령어로 요청한다:

| 사용자 입력 예시 | 동작 |
|---|---|
| `xpcomment add "텍스트" 파일.jpg` | 코멘트 추가/덮어쓰기 |
| `xpcomment remove 파일.jpg` | 코멘트 삭제 |
| `xpcomment read 파일.jpg` | 현재 코멘트 읽기 |
| `코멘트 추가해줘 "텍스트" 파일.jpg` | 동일하게 add로 처리 |
| `파일.jpg 코멘트 지워줘` | 동일하게 remove로 처리 |

---

## exiftool 명령어 변환 규칙

### ADD (추가 / 덮어쓰기)
```bash
exiftool -XPComment="코멘트 텍스트" -overwrite_original "파일경로"
```
- `-overwrite_original` 을 반드시 붙인다 (백업 파일 _original 생성 방지)
- 한국어/유니코드 텍스트도 그대로 사용 가능
- 기존 코멘트가 있으면 덮어씀

### REMOVE (삭제)
```bash
exiftool -XPComment= -overwrite_original "파일경로"
```
- 값을 빈칸으로 두면 필드가 삭제됨

### READ (읽기)
```bash
exiftool -XPComment "파일경로"
```

---

## 여러 파일 일괄 처리

```bash
# 특정 폴더 전체
exiftool -XPComment="텍스트" -overwrite_original /폴더경로/*.jpg

# 재귀적으로 하위 폴더까지
exiftool -XPComment="텍스트" -overwrite_original -r /폴더경로/
```

---

## 주의사항

1. 파일 경로에 공백이 있으면 반드시 따옴표로 감싼다
2. exiftool 미설치 시 먼저 설치: `sudo apt install libimage-exiftool-perl`
3. 작업 후 확인은 read 명령으로

---

## 응답 형식

작업 완료 후:
```
완료: photo.jpg
XPComment: "아리가 토끼 귀리"

실행한 명령어:
exiftool -XPComment="아리가 토끼 귀리" -overwrite_original "photo.jpg"
```
