# ECD e ECF — Escriturações Contábil e Fiscal

## ECD — Escrituração Contábil Digital

### Conceito
Substituição dos livros contábeis em papel pela escrituração digital:
- Livro Diário e auxiliares
- Livro Razão e auxiliares
- Livro Balancetes Diários, Balanços e fichas de lançamento

### Base legal
- **IN RFB nº 2.003/2021** (e alterações posteriores)
- **Decreto 6.022/2007** (instituiu o SPED)

### Obrigados
- Pessoas jurídicas tributadas pelo **Lucro Real**
- Pessoas jurídicas tributadas pelo **Lucro Presumido** que distribuíram lucros acima da presunção sem escrituração contábil
- Imunes e isentas obrigadas a entregar a ECF
- SCP (Sociedade em Conta de Participação) como livro próprio

### Não obrigados
- Simples Nacional (exceto se distribuiu lucro acima da presunção)
- MEI
- Órgãos públicos (usam SICONFI)
- Pessoas jurídicas inativas

### Prazo de entrega
- **Último dia útil de junho** do ano seguinte ao ano-calendário
- Ex: ECD 2025 → prazo até **30/06/2026**

### Estrutura do arquivo
- Formato texto (TXT) com layout definido pela RFB
- Blocos: 0 (abertura), I (lançamentos), J (demonstrações), K (conglomerados), 9 (encerramento)

### Registros principais

| Bloco | Registro | Conteúdo |
|---|---|---|
| 0 | 0000 | Abertura do arquivo |
| 0 | 0007 | Escrituração contábil descentralizada |
| 0 | 0150 | Tabela de participantes |
| 0 | 0500 | Plano de contas |
| I | I050 | Plano de contas referenciado |
| I | I155 | Saldos periódicos |
| I | I200 | Lançamento contábil |
| J | J100 | Balanço Patrimonial |
| J | J150 | DRE |
| J | J210 | DLPA/DMPL |
| J | J930 | Signatários (contador + responsável) |

### Assinatura
- **Obrigatório**: assinatura digital do representante legal + contador
- Certificado: e-CPF ou e-CNPJ (tipo A1 ou A3)
- Sem assinatura = não entregue

### Substituição/Retificação
- Possível até o prazo de entrega da ECF do mesmo ano-calendário
- Após: apenas via processo administrativo no e-CAC
- Autenticação automática (não precisa mais ir à Junta Comercial)

---

## ECF — Escrituração Contábil Fiscal

### Conceito
Apuração do IRPJ e da CSLL em formato digital. Substituiu a DIPJ.

### Base legal
- **IN RFB nº 2.004/2021** (e alterações)

### Obrigados
- Todas as pessoas jurídicas (inclusive imunes e isentas)
- **Exceto**: Simples Nacional, órgãos públicos, autarquias, fundações públicas, empresas inativas

### Prazo de entrega
- **Último dia útil de julho** do ano seguinte
- Ex: ECF 2025 → prazo até **31/07/2026**
- A ECF deve recuperar os dados da ECD (obrigatório quando houver ECD)

### Estrutura do arquivo

| Bloco | Conteúdo |
|---|---|
| 0 | Abertura e identificação |
| C | Recuperação da ECD |
| E | Informações do Lucro Real (LALUR/LACS) |
| J | Plano de contas e mapeamento |
| K | Saldos das contas contábeis |
| L | Balanço Patrimonial (Lucro Real) |
| M | Livro eletrônico e-LALUR/e-LACS |
| N | Cálculo do IRPJ e CSLL |
| P | Balanço Patrimonial (Lucro Presumido) |
| Q | DRE (Lucro Presumido) |
| T | Lucro arbitrado |
| U | Imunes e isentas |
| X | Informações econômicas |
| Y | Informações gerais |

### Recuperação da ECD
- A ECF **deve obrigatoriamente** recuperar dados da ECD transmitida
- Se não recuperar: inconsistência detectada e possível intimação

### Apuração IRPJ/CSLL por regime

**Lucro Real:**
- Trimestral: apura a cada trimestre (definitivo)
- Anual: estimativa mensal + ajuste anual (LALUR)
- Alíquota IRPJ: 15% + adicional 10% (sobre excedente de R$ 20mil/mês)
- Alíquota CSLL: 9% (regra geral)

**Lucro Presumido:**
- Base de cálculo presumida sobre receita bruta
- Percentuais de presunção: 8% (comércio/indústria), 32% (serviços), outros
- IRPJ: 15% sobre base presumida + adicional 10%
- CSLL: 9% sobre base presumida (12% ou 32%)

**Imunes e isentas:**
- Preencher Bloco U
- Demonstrar que cumprem requisitos de imunidade/isenção
- Informar receitas e despesas

### Retificação
- Possível em até 5 anos
- Se alterar IRPJ/CSLL: pode gerar auto de infração se aumentar imposto
- Retificação após início de fiscalização: vedada para reduzir tributo

---

## Autor

**Valleko Vagner de Freitas Ferreira**
Contador — Controlador Geral, Câmara Municipal de Timon/MA
