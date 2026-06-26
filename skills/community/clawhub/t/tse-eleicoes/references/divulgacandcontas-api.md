# DivulgaCandContas API — Referência

Base URL: `https://divulgacandcontas.tse.jus.br/divulga/rest/v1`

Sem autenticação. Não funciona direto no browser (sem CORS), mas funciona server-side com httpx.

## Endpoints

### Eleições

```
GET /eleicao/ordinarias
→ Lista eleições ordinárias disponíveis

GET /eleicao/anos-eleitorais
→ Array de anos com eleições

GET /eleicao/listar/municipios/{eleicaoId}/{municipioCod}/cargos
→ Cargos disponíveis em um município para uma eleição

GET /eleicao/estados/{ano}/ano
→ Estados com eleições suplementares no ano

GET /eleicao/suplementares/{ano}/{uf}
→ Eleições suplementares de um estado
```

### Candidatos

```
GET /candidatura/listar/{ano}/{municipioCod}/{eleicaoId}/{cargoCod}/candidatos
→ Lista candidatos

GET /candidatura/buscar/{ano}/{municipioCod}/{eleicaoId}/candidato/{candidatoId}
→ Detalhe completo do candidato (bens, redes sociais, foto, arquivos)
```

### Prestação de Contas

```
GET /prestador/consulta/{eleicaoId}/{ano}/{municipioCod}/{cargoCod}/90/90/{candidatoId}
→ Prestação de contas do candidato
```

## IDs de Eleições Confirmados (27/04/2026)

| Ano  | ID           | Tipo               |
|------|--------------|--------------------|
| 2024 | 2045202024   | Municipais         |
| 2022 | 2040602022   | Geral Federal      |
| 2020 | 2030402020   | Municipais         |
| 2018 | 2022802018   | Geral Federal      |
| 2016 | 2            | Municipais         |
| 2014 | 680          | Gerais             |

## Códigos de Cargos

| Código | Cargo           |
|--------|-----------------|
| 3      | Governador      |
| 4      | Vice-Governador |
| 5      | Senador         |
| 6      | Dep. Federal    |
| 7      | Dep. Estadual   |
| 9      | 1º Suplente     |
| 10     | 2º Suplente     |
| 11     | Prefeito        |
| 12     | Vice-Prefeito   |
| 13     | Vereador        |

## Exemplos de Municípios

| Município     | Código TSE |
|---------------|------------|
| São Paulo/SP  | 71072      |
| Rio de Janeiro/RJ | 60011  |
| Brasília/DF   | 97012      |
| Salvador/BA   | 38490      |
| Fortaleza/CE  | 16292      |
