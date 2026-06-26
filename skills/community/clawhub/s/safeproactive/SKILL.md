\---

name: SafeProactive

version: 1.1.2

description: Framework di sicurezza locale con Write-Ahead Logging (WAL) e gate di approvazione umana obbligatori.

triggers:

&#x20; - every\_turn

&#x20; - constraint\_violation

maintainer: Roberto De Biase

license: MIT

\---



\# SafeProactive v1.1.2



\## 🔒 Sicurezza e Scopo (Strict)

1\. \*\*Confini del Filesystem:\*\* L'agente è limitato alle cartelle `./proposals/`, `./memory/` e al workspace corrente. È \*\*vietato\*\* l'accesso a log di sistema o cronologia della shell (es. .bash\_history).

2\. \*\*Cronologia Azioni:\*\* Ogni riferimento alla "storia" o "cronologia" si riferisce esclusivamente al file di audit locale `proposals/EXECUTION\_LOG.md`.

3\. \*\*Zero API Esterne:\*\* Questa skill non gestisce né richiede credenziali esterne. Ogni integrazione di Livello 2 deve essere configurata manualmente dall'operatore.



\---



\## 🏛️ Architettura

Il framework segue un ciclo decisionale rigido:

1\. \*\*Self-Location:\*\* Identificazione dei confini del sistema.

2\. \*\*Constraint Mapping:\*\* Definizione dei limiti di sicurezza (Livello 0).

3\. \*\*Proposal \& WAL:\*\* Scrittura dell'azione intenzionale in `./proposals/` PRIMA dell'esecuzione.

4\. \*\*Approval Gate:\*\* Le azioni di Livello 2+ richiedono conferma umana esplicita.







\---



\## 🚦 Livelli Operativi



| Livello | Nome | Descrizione | Approvazione |

| :--- | :--- | :--- | :--- |

| \*\*0\*\* | \*\*Integrità\*\* | Stabilità e sicurezza locale. | \*\*Auto\*\* |

| \*\*1\*\* | \*\*Esplorazione\*\* | Analisi e ricerca nel workspace locale. | \*\*Auto\*\* |

| \*\*2\*\* | \*\*Espansione\*\* | Creazione di nuovi file o strumenti locali. | \*\*MANUALE\*\* |

| \*\*3\*\* | \*\*Ricorsione\*\* | Modifica del protocollo (SKILL.md). | \*\*STRETTAMENTE MANUALE\*\* |



\---



\## 📄 Manutenzione

L'integrità è monitorata via `HEARTBEAT.md`, verificando la coerenza tra i log in `proposals/WAL/` e `proposals/EXECUTION\_LOG.md`.

