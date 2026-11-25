# apk-pipeline.md — APK WebView do chat (pipeline PENDENTE, retomável)

Objetivo: gerar `tunnel/demo/chat.apk` — um WebView Android que abre a URL
do chat (persistida em SharedPreferences) — e distribuí-lo PELO TÚNEL demo
(o usuário baixa do celular via `URL(demo)/chat.apk`).

## Estado atual (2026-10-24)

- Pipeline v2 pronto em `tunnel/build_apk.sh` (155MB de downloads,
  retomáveis com `curl -C -`).
- Status dos downloads: `tunnel/run/apk_status.txt`; parciais em
  `tunnel/android/` (`jdk.tgz`, `jre.tgz` já presentes).
- Cadeia de build (SEM Android Studio/Gradle):
  aapt → ECJ (compilador Java) → d8 (dex) → zipalign → apksigner
  → `tunnel/demo/chat.apk`.

## Como retomar (quando o usuário pedir)

```bash
# 1. Conferir o que já baixou:
cat /home/z/my-project/tunnel/run/apk_status.txt

# 2. Rodar o pipeline (chamada longa EM PRIMEIRO PLANO com timeout 600000 —
#    padrão que funcionou antes; downloads retomam de onde pararam):
bash /home/z/my-project/tunnel/build_apk.sh

# 3. Resultado em tunnel/demo/chat.apk; se o demo estiver on:
bash /home/z/my-project/tunnel/ctl/tunnelctl status
#    → URL(demo)/chat.apk é o link de download para o celular
```

## Pré-requisitos de exposição

- O APK baixa pela rede pública: o `demo` PRECISA estar on (por ordem do
  usuário) para o celular baixar `chat.apk`.
- O APK aponta para a URL DO CHAT atual — como a URL do Quick Tunnel muda a
  cada start, o APK guarda a URL na PRIMEIRA abertura (SharedPreferences) e
  permite digitar outra; regenere/reinstale se a URL do chat mudar.

## Instalação no celular

1. Baixar `URL(demo)/chat.apk` no navegador do Android.
2. Permitir "instalar app de fonte desconhecida" (é assinado com apksigner
   com chave de debug gerada no pipeline).
3. Abrir → informar/confirmar a URL do chat → conversar.

## Limitações conhecidas

- Requer Android com permissão de instalação externa; sem Play Protect
  approval formal (avise o usuário).
- Pipeline consome RAM/disco considerável na VM; rode quando não houver
  outra tarefa pesada em paralelo.
- Se a VM for reciclada no meio, `curl -C -` retoma os downloads — não
  recomece do zero; confira `apk_status.txt` primeiro.

## Histórico

- `tunnel/run/apk_status.txt` registrou progresso em 2026-10-23/24; etapa
  pendente: concluir downloads e rodar a cadeia aapt→apksigner até o APK.
