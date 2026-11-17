# UnreadBadgeOpenClaw

[![ClawHub](https://img.shields.io/badge/ClawHub-unreadbadgeopenclaw-blue)](https://clawhub.ai/pondsi/skills/unreadbadgeopenclaw)
[![License](https://img.shields.io/badge/License-MIT--style%20%2B%20attribution-green)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-OpenClaw%20Control%20UI-orange)](https://openclaw.ai)

Persistent **unread badges** for OpenClaw session rows in the Control UI sidebar.

| 简体中文界面 | English UI |
|---|---|
| ![Sidebar unread mark (中文)](screenshots/sidebar-mark-zh.png) | ![Sidebar unread mark (English)](screenshots/sidebar-mark-en.png) |

---

## English

A finished reply puts a **flag** icon + `[New reply] HH:mm` note on the session
row; a failure puts an **alert** icon + `[Failed] HH:mm`. The gateway clears the
mark natively when you open the session, send it a new message, or when its TTL
expires — the badge means "unread", not "stale decoration". Works even with
"Show message preview" disabled.

### Which package should I install?

| | GitHub repo (this) | ClawHub artifact |
|---|---|---|
| Content | Full project: portable core + `.github/` (issue templates, security policy) + screenshots + git metadata | Audited portable core |
| Install | `git clone` + copy `scripts/` | `clawhub install unreadbadgeopenclaw` |
| Version | Same tag as ClawHub release | Same tag |
| Best for | Source browsing, issues, contributions | One-command install into OpenClaw |

Both contain the identical core: `scripts/unread-mark.js`,
`scripts/unread-mark-keepalive.js`, `references/internals.md`.

### Quick start

```bash
# Reply completed → flag icon + "[New reply] HH:mm"
node scripts/unread-mark.js --key <sessionKey> --event done

# Reply failed → alert icon + "[Failed] HH:mm"
node scripts/unread-mark.js --key <sessionKey> --event warn

# Keep unread marks alive past the 120-min TTL (run every 90 min, max 7 days)
node scripts/unread-mark-keepalive.js
```

Schedule the keep-alive with an OpenClaw automation, cron, or Task Scheduler.
Full parameter reference in [SKILL.md](SKILL.md); deep internals in
[references/internals.md](references/internals.md); 中文详细说明见
[说明.md](说明.md).

### Why the icon matters

The sidebar subtitle chain is
`attentionNote ?? agentStatusNote ?? runHeadline ?? messagePreview ?? subtitle`.
When "Show message preview" is off, only `attentionNote ?? headline` render —
a pure-text note becomes invisible. The `attention` **icon** rides a separate
always-rendered channel. This skill therefore always sets an icon (`flag` for
success, `alert` for failures) and treats the note as a bonus.

### Design principles

- **Silent failure** — every error path exits 0; a notification helper must
  never break the pipeline it reports for.
- **Native lifecycle** — no shadow state to "resurrect" read marks: opening
  the session, sending a new message, TTL expiry, and the 7-day fallback are
  the only clear points. A cleared mark is never re-created.
- **Portable core** — two Node scripts, no dependencies, cross-platform path
  discovery for the local `openclaw` CLI. State stays in
  `$OPENCLAW_STATE_DIR/unread-marks.json` (default `~/.openclaw`).

### Compatibility

OpenClaw with the `sessions.patch` / `sessions.list` gateway RPC (current
stable). Windows / macOS / Linux.

### Sponsors & License

Support the project via [SPONSORS.md](SPONSORS.md). Licensed MIT-style **with
mandatory attribution** — see [LICENSE](LICENSE).

---

## 简体中文

给 OpenClaw Control UI 侧边栏的会话行加**持久未读徽章**：回复完成 → 🚩 flag 图标 +
`[New reply] HH:mm`；回复失败 → ⚠️ alert 图标 + `[Failed] HH:mm`。打开会话、发送新消息、
TTL 到期时由网关原生清除——徽章代表「未读」，不是过期装饰。

- **图标必须带**：关闭「显示消息预览」后纯文字不渲染，图标走独立的常显通道。
- **已清除的标记绝不复活**（v1.1.1 修复）：网关才是标记的持有者。
- 静默失败设计：任何异常 exit 0，绝不打断主流程。
- 两个脚本零依赖，状态文件 `$OPENCLAW_STATE_DIR/unread-marks.json`。

安装 / 用法 / 参数 / 该装哪个包，见上方 **English** 节；完整中文说明书见
[说明.md](说明.md)；深度原理见 [references/internals.md](references/internals.md)。

## 繁體中文

為 OpenClaw Control UI 側邊欄的會話列加上**持久未讀徽章**：回覆完成 → 🚩 flag 圖示 +
`[New reply] HH:mm`；回覆失敗 → ⚠️ alert 圖示 + `[Failed] HH:mm`。開啟會話、傳送新訊息、
TTL 到期時由閘道原生清除——徽章代表「未讀」，不是過期裝飾。

- 圖示必須設定：關閉「顯示訊息預覽」後純文字不會渲染，圖示走獨立的常顯通道。
- 已被清除的標記**絕不復活**：閘道才是標記的持有者。
- 靜默失敗設計：任何異常 exit 0，絕不干擾主流程。

安裝 / 用法 / 參數見上方 **English** 節；完整中文說明見
[说明.md](说明.md)。

## 한국어

OpenClaw Control UI 사이드바의 세션 행에 **읽지 않음 배지**를 붙입니다: 회신 완료 →
🚩 flag 아이콘 + `[New reply] HH:mm`, 회신 실패 → ⚠️ alert 아이콘 + `[Failed] HH:mm`.
세션을 열거나 새 메시지를 보내거나 TTL이 끝나면 게이트웨이가 원래 동작으로 지웁니다 —
배지는 "읽지 않음"이지 낡은 장식이 아닙니다.

- 아이콘은 필수입니다: "메시지 미리보기"를 끄면 텍스트 노트는 렌더링되지 않지만
  아이콘은 항상 표시되는 별도 채널을 사용합니다.
- 이미 지워진 표식은 **절대 되살아나지 않습니다** — 게이트웨이가 표식의 소유자입니다.
- 조용한 실패 설계: 모든 오류는 exit 0으로 끝나며 본체 파이프라인을 막지 않습니다.

설치 / 사용법 / 매개변수는 위 **English** 절을 보십시오.

## Русский

Ставит **постоянные метки «не прочитано»** на строки сессий в сайдбаре OpenClaw
Control UI: ответ завершён → иконка 🚩 flag + `[New reply] HH:mm`; ошибка →
иконка ⚠️ alert + `[Failed] HH:mm`. Шлюз стирает метку сам при открытии сессии,
отправке нового сообщения или по истечении TTL — метка значит «не прочитано».

- Иконка обязательна: при выключенном «Show message preview» текстовая заметка
  не рендерится, а иконка идёт по отдельному всегда отображаемому каналу.
- Уже снятая метка **не восстанавливается**: владелец метки — шлюз.
- Тихие сбои: любая ошибка завершается с exit 0 и не ломает основной процесс.

Установка, использование и параметры — в разделе **English** выше.

## 日本語

OpenClaw Control UI サイドバーのセッション行に**永続的な未読バッジ**を付けます：
返信完了 → 🚩 flag アイコン + `[New reply] HH:mm`、返信失敗 → ⚠️ alert アイコン +
`[Failed] HH:mm`。セッションを開く・新しいメッセージを送る・TTL 期限切れのいずれかで
ゲートウェイがネイティブに消します — バッジは「未読」の意味です。

- アイコンは必須です：「メッセージ プレビュー」を無効にするとテキスト ノートは
  描画されませんが、アイコンは常に表示される別チャンネルを通ります。
- すでに消えたマークは**復活しません** — マークの持ち主はゲートウェイです。
- 静かな失敗設計：どんなエラーも exit 0 で終了し、本体を壊しません。

インストール・使い方・パラメータは上記 **English** 節を参照。

## Español

Añade **insignias de no leído persistentes** a las filas de sesión en la barra
lateral de OpenClaw Control UI: respuesta completada → icono 🚩 flag +
`[New reply] HH:mm`; respuesta fallida → icono ⚠️ alert + `[Failed] HH:mm`.
La pasarela borra la marca de forma nativa al abrir la sesión, enviar un mensaje
nuevo o al expirar el TTL — la insignia significa «no leído».

- El icono es obligatorio: con «Show message preview» desactivado, la nota de
  texto no se renderiza; el icono viaja por un canal siempre visible.
- Una marca ya borrada **nunca se recrea**: la pasarela es la dueña de la marca.
- Fallo silencioso: cualquier error termina con exit 0 y no rompe el proceso.

Instalación, uso y parámetros en la sección **English** de arriba.

## Français

Ajoute des **badges « non lu » persistants** aux lignes de session dans la barre
latérale d'OpenClaw Control UI : réponse terminée → icône 🚩 flag +
`[New reply] HH:mm` ; réponse en échec → icône ⚠️ alert + `[Failed] HH:mm`.
La passerelle efface le badge nativement à l'ouverture de la session, à l'envoi
d'un nouveau message ou à l'expiration du TTL — le badge signifie « non lu ».

- L'icône est obligatoire : avec « Show message preview » désactivé, la note
  texte n'est pas rendue ; l'icône emprunte un canal toujours affiché.
- Un badge déjà effacé **n'est jamais recréé** : la passerelle est propriétaire
  du badge.
- Échec silencieux : toute erreur se termine par exit 0 et ne casse rien.

Installation, utilisation et paramètres : voir la section **English** ci-dessus.

---

Pondsi (+MiMo-v2.5/v2.5pro+deepseek-v4-flash/pro+deepseek-v4.1-flash-expires-on-0910+GLM5.3-flash+Gemini3.1-pro+Qwen3.8-27b+Gemini3.8-flash) — automatically committed by OpenClaw
