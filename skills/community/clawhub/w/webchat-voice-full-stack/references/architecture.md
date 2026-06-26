# Architecture

Meta-skill orchestration order:

1. `faster-whisper-local-service`
   - Creates local STT endpoint on `127.0.0.1:18790/transcribe`
   - Input validation: magic-byte check, configurable upload size limit
2. `webchat-https-proxy`
   - Starts HTTPS/WSS proxy on `:8443`
   - Adds gateway allowed origin
   - TLS 1.2+ enforced, SSRF protection, constant-time auth
3. `webchat-voice-gui`
   - Injects voice input UI (mic button, VU meter, i18n)
   - Installs gateway startup hook for update safety

Rationale:
- Backend first avoids proxy/UI working without transcription.
- Proxy second ensures HTTPS is ready before GUI tries to use it.
- Each component independently maintainable, reusable, and uninstallable.
