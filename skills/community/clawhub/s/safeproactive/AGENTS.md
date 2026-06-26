\# AGENTS.md — SafeProactive Operational Routines



\## 🤖 Routine di Background

Questo file definisce come SafeProactive opera in background per il monitoraggio dell'integrità.



\---



\## 💓 Protocollo Heartbeat (Ogni 30 Minuti)



\### Check 1: Integrità WAL

\*\*Comando:\*\* Verificare i Log Locali



\- \*\*Analisi Sequenziale:\*\* Verificare che non ci siano salti negli ID delle Proposte in `proposals/WAL/`.

\- \*\*Integrità Log:\*\* Confrontare `proposals/APPROVAL\_LOG.md` con il file locale `proposals/EXECUTION\_LOG.md`.

\- \*\*Privacy Guard:\*\* Confermare che l'agente NON abbia tentato di accedere a file fuori dal workspace (es. `/var/log` o `\~/.bash\_history`).



\*\*In caso di errore:\*\*

1\. Loggare l'incidente in `proposals/SECURITY\_LOG.md`.

2\. Allertare l'operatore immediatamente.

3\. Entrare in "Audit Mode" (richiedere approvazione per ogni azione).



\---



\### Check 2: Deriva dei Vincoli

\- Verificare che le priorità di sicurezza (Livello 0) siano ancora in cima alla lista.

\- Assicurarsi che l'agente non stia proponendo espansioni di Livello 2 senza dati sufficienti.



\---



\## 🚨 Procedure di Emergenza

\- \*\*Livello Rosso:\*\* Arresto immediato in caso di manomissione dei log WAL.

\- \*\*Livello Giallo:\*\* Richiesta di supervisione aumentata se l'ambiente locale risulta instabile.

