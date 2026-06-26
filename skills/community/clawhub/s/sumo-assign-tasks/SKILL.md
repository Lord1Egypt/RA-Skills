# SKILL.md - Sumo Assign Tasks Switch

## 功能
切換蘇茉派發任務給其他蘇茉時使用的方法。

## 觸發指令
`/Sumo_Assign_Tasks [0|1|2]`

---

## 📋 使用方式

### 查看目前使用的方法（不帶參數）
```
/Sumo_Assign_Tasks
```

顯示：
```
| 參數 | 工具 | 使用中 |
| -- | -------------- | ---------------- |
| 0 | sessions_spawn | ✅ 蘇茉現在用的 |
| 1 | clawteam | |
| 2 | SumoSubAgent | |
```

### 切換到 sessions_spawn（預設）
```
/Sumo_Assign_Tasks 0
```

### 切換到 clawteam
```
/Sumo_Assign_Tasks 1
```

### 切換到 SumoSubAgent
```
/Sumo_Assign_Tasks 2
```

---

## 🔧 三種方法說明

| 方法 | 工具 | 說明 |
|------|------|------|
| **sessions_spawn** | OpenClaw 內建 | 直接派發 subagent 任務，最穩定 |
| **clawteam** | clawteam 框架 | 多代理團隊協調框架 |
| **SumoSubAgent** | SumoSubAgent | 蘇茉家族自建的子代理管理框架 |

---

## 📝 實作說明

目前蘇茉派發任務預設使用 `sessions_spawn`，因為：
1. OpenClaw 原生功能，最穩定
2. 直接派發給 subagent，不需要額外設定
3. 所有蘇茉分身都支援

---

## 💾 設定儲存

設定會儲存在：
```
C:\Users\rayray\.openclaw\workspace\memory\assign_method.json
```

---

蘇茉已經準備好了！🎉
