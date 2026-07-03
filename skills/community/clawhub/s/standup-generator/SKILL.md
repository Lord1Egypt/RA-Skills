---
name: 鏅鸿兘绔欎細鐢熸垚鍣?slug: standup-generator
description: >
  鍩轰簬Git鎻愪氦璁板綍銆丣ira浠诲姟鏇存柊銆丼lack/椋炰功娑堟伅鍜屾棩鍘嗕簨浠讹紝鑷姩鐢熸垚姣忔棩绔欎細鎶ュ憡銆?  鏀寔Scrum/Kanban/鑷畾涔夋ā鏉匡紝鍖呭惈鏄ㄦ棩瀹屾垚銆佷粖鏃ヨ鍒掋€侀樆濉為」涓夎绱狅紝
  鍙嚜鍔ㄦ帹閫佽嚦Slack/椋炰功/閽夐拤/Teams/閭欢锛屾敮鎸?0+璇█鍜屽洟闃熶釜鎬у寲椋庢牸銆?version: 1.0.0
author: ai-gaoqian
tags:
  - standup
  - scrum
  - agile
  - daily-report
  - team-communication
  - productivity
  - automation
metadata:
  openclaw:
    requires:
      python: ">=3.10"
      packages:
        - gitpython>=3.1.0
        - requests>=2.28.0
        - jinja2>=3.1.0
      api_keys:
        - optional: JIRA_API_TOKEN
        - optional: SLACK_BOT_TOKEN
        - optional: FEISHU_APP_TOKEN
        - optional: DINGTALK_APP_KEY
      memory: 128MB
      cpu: 0.2
    pricing:
      model: per-use
      currency: CNY
      amount: 0.50
      payment_method: alipay_ai_receipt
---

# 鏅鸿兘绔欎細鐢熸垚鍣?(Standup Generator)

## 姒傝堪
鏅鸿兘绔欎細鐢熸垚鍣ㄤ粠寮€鍙戣€呯殑瀹為檯宸ヤ綔鐥曡抗涓嚜鍔ㄦ彁鍙栦俊鎭紝鐢熸垚缁撴瀯鍖栥€佷俊鎭赴瀵岀殑姣忔棩绔欎細鎶ュ憡锛岃妭鐪佸洟闃熸瘡澶?5-30鍒嗛挓鐨勭珯浼氬噯澶囨椂闂淬€?
## 鏍稿績鍔熻兘

### 1. 鏅鸿兘鏁版嵁閲囬泦
鑷姩浠庝互涓嬫潵婧愯仛鍚堝伐浣滄暟鎹細
- **Git鎻愪氦璁板綍** - 瑙ｆ瀽commit message锛屾彁鍙栧伐浣滃唴瀹?- **Jira/Linear/Asana** - 鍚屾浠诲姟鐘舵€佸彉鏇淬€佽瘎璁?- **Slack/椋炰功/閽夐拤** - 鎻愬彇鍏抽敭宸ヤ綔璁ㄨ
- **Google Calendar/Outlook** - 鎻愬彇浼氳鍙備笌鎯呭喌
- **IDE娲诲姩锛堝彲閫夛級** - 缂栫爜鏃堕棿娈电粺璁?
### 2. 鏅鸿兘鎶ュ憡鐢熸垚
- **鏄ㄦ棩瀹屾垚** - 鍩轰簬宸插悎骞禤R銆佸凡鍏抽棴Issue銆丟it鎻愪氦鑷姩姹囨€?- **浠婃棩璁″垝** - 鍩轰簬杩涜涓殑浠诲姟鍜孲print Backlog鎺ㄦ柇
- **闃诲椤?* - 鑷姩璇嗗埆鏍囪涓築locked鐨勪换鍔″拰闀挎湡鍋滄粸椤?- **鍏抽敭鎸囨爣** - 鎻愪氦娆℃暟銆佷唬鐮佽鏁般€丳R鍚堝苟鏁扮瓑

### 3. 澶氭ā鏉挎敮鎸?- **Scrum妯℃澘** - 鏍囧噯涓夐棶鏍煎紡
- **Kanban妯℃澘** - 鎸夊伐浣滄祦闃舵缁勭粐
- **绠＄悊灞傛憳瑕?* - 闈㈠悜绠＄悊鑰呯殑绮剧畝鐗?- **鑷畾涔夋ā鏉?* - 鏀寔Jinja2妯℃澘鑷畾涔?
### 4. 澶氭笭閬撴帹閫?- Slack棰戦亾鑷姩鎺ㄩ€?- 椋炰功缇ゆ満鍣ㄤ汉
- 閽夐拤缇ゆ秷鎭?- Microsoft Teams
- 閭欢鍙戦€?- Markdown/PDF瀵煎嚭

### 5. 鍥㈤槦鍗忎綔澧炲己
- 鍥㈤槦绔欎細姹囨€伙細鑱氬悎鍏ㄥ憳鎶ュ憡
- 璺ㄥ洟闃熶緷璧栭」楂樹寒
- 閲嶅宸ヤ綔妫€娴嬫彁閱?- 鐭ヨ瘑鍒嗕韩鏈轰細璇嗗埆

## 浣跨敤鏂瑰紡
```
clawhub install standup-generator
```

## 鍏稿瀷鍛戒护
```
璇风敓鎴愭垜浠婂ぉ鐨勭珯浼氭姤鍛?璇风敓鎴愬洟闃熶粖澶╃殑绔欎細姹囨€诲苟鎺ㄩ€佸埌Slack
璇风敤涓枃鐢熸垚鏈懆绔欎細鍛ㄦ姤
璇峰垎鏋愬洟闃熸湰鍛ㄧ殑宸ヤ綔瓒嬪娍
```

## 杈撳嚭绀轰緥
```markdown
## 馃棧锔?姣忔棩绔欎細 - 寮犱笁 | 2026-06-13

### 鉁?鏄ㄦ棩瀹屾垚
- 瀹屾垚鐢ㄦ埛璁よ瘉妯″潡閲嶆瀯 [PR #2341]
- 淇鐧诲綍椤甸潰鍝嶅簲寮忓竷灞€bug [JIRA-892]
- 鍙備笌鎶€鏈柟妗堣瘎瀹′細 (14:00-15:30)

### 馃搵 浠婃棩璁″垝
- 寮€鍙戞敮浠樺洖璋冩帴鍙?[JIRA-893]
- Code Review: 璁㈠崟妯″潡 [PR #2345]
- 缂栧啓API鏂囨。

### 馃毀 闃诲椤?- [JIRA-890] 闇€瑕佸悗绔彁渚涚粨绠桝PI鏂囨。 鈫?绛夊緟鏉庡洓鍥炲

### 馃搳 缁熻
Commits: 7 | PRs鍚堝苟: 2 | 浠ｇ爜琛? +342/-128
```

## 瀹夊叏涓庨殣绉?- 鎵€鏈夋暟鎹湰鍦板鐞嗭紝鎸夐渶鎺ㄩ€佽嚦鎸囧畾娓犻亾
- Git浠撳簱浠呰鍙栨湰鍦癱lone锛屼笉涓婁紶浠ｇ爜
- 鏁忔劅淇℃伅锛堝瘑鐮?瀵嗛挜/涓汉鏁版嵁锛夎嚜鍔ㄨ繃婊?- 鏀寔鎺掗櫎鐗瑰畾浠撳簱鎴栭」鐩?