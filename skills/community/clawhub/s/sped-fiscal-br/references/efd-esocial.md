# EFD, eSocial e DCTFWeb

## EFD-ICMS/IPI — Escrituração Fiscal Digital

### Conceito
Escrituração digital dos livros fiscais (entradas, saídas, apuração ICMS e IPI).

### Base legal
- **Ajuste SINIEF 02/2009** + Convênio ICMS 143/2006
- Legislação estadual específica (cada UF regulamenta)

### Obrigados
- Contribuintes de ICMS e/ou IPI
- Conforme lista da SEFAZ de cada estado
- **Simples Nacional**: obrigado em alguns estados

### Prazo
- **Mensal** — até o dia fixado pela SEFAZ estadual (geralmente dia 15-20 do mês seguinte)

### Blocos principais
| Bloco | Conteúdo |
|---|---|
| 0 | Abertura e tabelas |
| C | Documentos fiscais de mercadorias (NF-e, NFC-e) |
| D | Documentos fiscais de serviço de transporte (CT-e) |
| E | Apuração ICMS e IPI |
| G | CIAP — Crédito ICMS do ativo permanente |
| H | Inventário físico |
| K | Controle de produção e estoque (Bloco K) |
| 1 | Informações complementares |

---

## EFD-Contribuições (PIS/COFINS)

### Conceito
Escrituração digital das contribuições PIS/PASEP e COFINS.

### Base legal
- **IN RFB nº 1.252/2012**

### Obrigados
- Lucro Real e Lucro Presumido
- Imunes e isentas com receita > R$ 4,8 milhões
- **Simples Nacional**: dispensado

### Prazo
- **Mensal** — até o 15º dia útil do 2º mês seguinte ao período de apuração
- Ex: competência janeiro → prazo até 15º dia útil de março

### Regimes de apuração
**Cumulativo (Presumido):**
- PIS: 0,65% | COFINS: 3,00%
- Sem direito a créditos

**Não cumulativo (Real):**
- PIS: 1,65% | COFINS: 7,60%
- Com direito a créditos (insumos, energia, aluguel, depreciação etc.)

---

## EFD-Reinf

### Conceito
Informações de retenções na fonte e pagamentos a PF/PJ, complementar ao eSocial.

### Base legal
- **IN RFB nº 2.043/2021**

### Eventos principais
| Série | Evento | Conteúdo |
|---|---|---|
| R-1000 | Informações do contribuinte | Cadastro e classificação tributária |
| R-1050 | Tabela de entidades ligadas | Obras, processos |
| R-2010 | Retenção INSS — serviços tomados | Cessão de mão de obra (11%) |
| R-2020 | Retenção INSS — serviços prestados | Quando a empresa presta serviço |
| R-2055 | Aquisição de produção rural PF | Retenção FUNRURAL |
| R-4010 | Pagamentos a PF | IRRF sobre serviços PF |
| R-4020 | Pagamentos a PJ | IRRF, CSRF (PIS/COFINS/CSLL) |
| R-4040 | Pagamentos a beneficiários não identificados | Tributação exclusiva |
| R-4080 | Retenção na fonte — auto-retenção | IR retido na própria |
| R-4099 | Fechamento/reabertura | Encerramento do período |
| R-9000 | Exclusão de eventos | Cancelamento |

### Prazo
- **Mensal** — até o dia **15 do mês seguinte** à competência
- Fechamento (R-4099) no mesmo prazo

### Quem deve enviar
- Todas as PJ que efetuam retenções (INSS, IRRF, CSRF)
- **Simples Nacional**: desde 2024 (séries R-4010/R-4020)
- **Setor público**: sim (retenções de serviços tomados)

---

## eSocial

### Conceito
Sistema de escrituração digital de obrigações trabalhistas, previdenciárias e fiscais.

### Base legal
- **Decreto 8.373/2014**
- Portarias e manuais atualizados periodicamente

### Grupos de eventos

**Eventos de tabelas (S-1xxx):**
- S-1000: Empregador/contribuinte
- S-1005: Estabelecimentos
- S-1010: Rubricas
- S-1020: Lotações tributárias
- S-1070: Processos judiciais/administrativos

**Eventos não periódicos (S-2xxx):**
- S-2190: Registro preliminar
- S-2200: Admissão
- S-2205: Alteração de dados cadastrais
- S-2206: Alteração contratual
- S-2230: Afastamento temporário
- S-2299: Desligamento
- S-2300: TSVE — Trabalhador sem vínculo (autônomos, estagiários)
- S-2399: TSVE — Término

**Eventos periódicos (S-1200/S-1210/S-1299):**
- S-1200: Remuneração do trabalhador
- S-1210: Pagamentos de rendimentos
- S-1260: Comercialização produção rural PF
- S-1270: Contratação de avulsos não portuários
- S-1299: Fechamento dos eventos periódicos

### Prazo de envio
| Evento | Prazo |
|---|---|
| Admissão (S-2200) | Até 1 dia antes do início |
| Desligamento (S-2299) | Até 10 dias após |
| Periódicos (S-1200/1210) | Até dia 15 do mês seguinte |
| Fechamento (S-1299) | Até dia 15 do mês seguinte |
| CAT — Comunicação de Acidente (S-2210) | Até 1 dia útil após |

---

## DCTFWeb

### Conceito
Declaração que consolida débitos previdenciários e de terceiros apurados no eSocial e EFD-Reinf.

### Base legal
- **IN RFB nº 2.005/2021**

### Funcionamento
1. eSocial envia eventos → gera débitos previdenciários
2. EFD-Reinf envia retenções → gera créditos
3. DCTFWeb consolida: débitos - créditos = saldo a pagar
4. Emissão de DARF unificado

### Prazo
- **Mensal**: até dia **15 do mês seguinte**
- **13º salário**: até dia **20 de dezembro**
- **Anual (DIRF substituição)**: conforme calendário RFB

### DARF gerado
- Código 1840 (contribuições previdenciárias)
- Pagamento via e-CAC ou banco

---

## Autor

**Valleko Vagner de Freitas Ferreira**
Contador — Controlador Geral, Câmara Municipal de Timon/MA
