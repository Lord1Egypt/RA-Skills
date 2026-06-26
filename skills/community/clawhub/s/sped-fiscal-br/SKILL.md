---
name: sped-fiscal-br
description: "SPED — Sistema Público de Escrituração Digital brasileiro. Obrigações acessórias federais para empresas privadas e entidades públicas. Use quando o usuário perguntar sobre: (1) ECD — Escrituração Contábil Digital, (2) ECF — Escrituração Contábil Fiscal, (3) EFD-Contribuições (PIS/COFINS), (4) EFD-ICMS/IPI (Fiscal), (5) EFD-Reinf, (6) eSocial — eventos e prazos, (7) DCTFWeb, (8) DIRF e sua substituição, (9) Prazos e calendário de entrega das obrigações, (10) Penalidades por atraso ou erro, (11) Leiautes e registros dos arquivos SPED, (12) Certificado digital para transmissão, (13) Regimes tributários (Simples, Presumido, Real) e suas obrigações, (14) Retenções na fonte (INSS, IRRF, CSRF, ISS), (15) DCTF, PERDCOMP, e-CAC. Autor: Valleko Vagner de Freitas Ferreira — Contador, CRC ativo. Idioma: Português do Brasil."
---

# SPED — Sistema Público de Escrituração Digital

Skill especializada nas obrigações acessórias federais do SPED, cobrindo todos os módulos, prazos, leiautes e regimes tributários.

**Autor:** Valleko Vagner de Freitas Ferreira — Contador, Controlador Geral da Câmara Municipal de Timon/MA

## Princípios

1. Prazos são **inegociáveis** — alertar sempre sobre datas limite
2. Fundamentar na legislação vigente (IN RFB específica de cada obrigação)
3. Distinguir obrigações por **regime tributário** (Simples, Presumido, Real)
4. Considerar se é entidade pública ou privada (obrigações diferentes)
5. Penalidades são severas — orientar preventivamente

## Referências Detalhadas

- **ECD e ECF**: Ver [references/ecd-ecf.md](references/ecd-ecf.md)
- **EFD e eSocial**: Ver [references/efd-esocial.md](references/efd-esocial.md)
- **Calendário e penalidades**: Ver [references/calendario-penalidades.md](references/calendario-penalidades.md)
- **Retenções na fonte**: Ver [references/retencoes.md](references/retencoes.md)

## Workflow Principal

### Ao receber pergunta sobre SPED

1. Identificar a **obrigação** específica (ECD, ECF, EFD, eSocial, DCTFWeb)
2. Identificar o **regime tributário** da empresa/entidade
3. Carregar referência específica em `references/`
4. Verificar prazos vigentes
5. Responder com fundamentação na IN RFB aplicável
6. Alertar sobre penalidades e retificações

## Visão Geral do SPED

### Módulos

| Módulo | O que escritura | IN RFB |
|---|---|---|
| **ECD** | Livros contábeis (Diário, Razão, Balancetes) | IN 2.003/2021 |
| **ECF** | Apuração IRPJ e CSLL | IN 2.004/2021 |
| **EFD-ICMS/IPI** | Escrituração fiscal (ICMS e IPI) | Ajuste SINIEF 02/2009 |
| **EFD-Contribuições** | PIS/PASEP e COFINS | IN 1.252/2012 |
| **EFD-Reinf** | Retenções e informações complementares | IN 2.043/2021 |
| **eSocial** | Eventos trabalhistas e previdenciários | Decreto 8.373/2014 |
| **DCTFWeb** | Débitos/créditos previdenciários e de terceiros | IN 2.005/2021 |
| **DCTF** | Débitos e créditos tributários federais | IN 2.005/2021 |

### Obrigatoriedade por regime

| Obrigação | Simples | Presumido | Real | Imune/Isenta | Setor Público |
|---|---|---|---|---|---|
| ECD | Não* | Não** | Sim | Sim*** | Não**** |
| ECF | Não | Sim | Sim | Sim | Não |
| EFD-ICMS/IPI | Depende UF | Sim | Sim | Depende | Não |
| EFD-Contribuições | Não | Sim | Sim | Sim*** | Não |
| EFD-Reinf | Sim***** | Sim | Sim | Sim | Sim |
| eSocial | Sim | Sim | Sim | Sim | Sim |
| DCTFWeb | Sim | Sim | Sim | Sim | Sim |

\* Exceto se distribuiu lucro acima da presunção
\** Exceto se distribuiu lucro acima da presunção
\*** Se receita bruta > R$ 4,8 milhões
\**** Entes públicos usam SICONFI, não ECD
\***** Desde 2024 (eventos de retenções)

## Certificado Digital

### Tipos aceitos
- **e-CPF A1/A3** — pessoa física (responsável legal)
- **e-CNPJ A1/A3** — pessoa jurídica
- **Procuração eletrônica** — via e-CAC

### Procuração e-CAC
Para contador assinar: cadastrar procuração no e-CAC (acesso.gov.br) com poderes específicos para cada obrigação.

## Siglas

| Sigla | Significado |
|---|---|
| SPED | Sistema Público de Escrituração Digital |
| ECD | Escrituração Contábil Digital |
| ECF | Escrituração Contábil Fiscal |
| EFD | Escrituração Fiscal Digital |
| IRPJ | Imposto de Renda Pessoa Jurídica |
| CSLL | Contribuição Social sobre Lucro Líquido |
| PIS | Programa de Integração Social |
| COFINS | Contribuição para Financiamento da Seguridade Social |
| DCTF | Declaração de Débitos e Créditos Tributários Federais |
| DCTFWeb | DCTF Previdenciária (via web) |
| PERDCOMP | Pedido de Restituição, Ressarcimento ou Compensação |
| LALUR | Livro de Apuração do Lucro Real |
| LACS | Livro de Apuração da CSLL |
