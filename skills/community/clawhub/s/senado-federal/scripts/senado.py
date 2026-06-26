#!/usr/bin/env python3
"""
senado.py - CLI para a API de Dados Abertos do Senado Federal
Uso: python3 senado.py <comando> [opções]

Comandos:
  senadores               Lista todos os senadores em exercício
  senador <nome>          Busca senador por nome
  senador-id <codigo>     Perfil completo de um senador
  agenda [data]           Agenda plenária (default: hoje). Data: YYYYMMDD ou YYYY-MM-DD
  agenda-comissoes [mes]  Agenda das comissões. Mês: YYYYMM (default: mês atual)
  votacoes <inicio> <fim> Votações no plenário. Datas: YYYYMMDD
  buscar-pl <assunto>     Busca matérias/proposições
  materia <sigla> <num> <ano>   Detalhes de uma matéria (ex: PL 1234 2026)
  materia-id <codigo>     Matéria pelo código interno
  tramitacao <codigo>     Histórico de tramitação de uma matéria
  comissoes               Lista comissões permanentes
  filiacoes <codigo>      Filiações partidárias de um senador
  cargos <codigo>         Cargos exercidos por um senador
  relatorias <codigo>     Relatorias de um senador
  licencas <codigo>       Licenças de um senador
  situacao <codigo>       Situação atual de uma matéria
  emendas-materia <codigo>  Emendas de uma matéria
  textos <codigo>         Textos de uma matéria
  votacao-nominal <ano>   Votações nominais de um ano
  resultado-dia <data>    Resultado do plenário em um dia (YYYYMMDD)
  discursos-plenario <inicio> <fim>  Discursos em plenário no período (YYYYMMDD)
  mesa-senado             Mesa diretora do Senado
  liderancas              Lideranças partidárias
  blocos                  Blocos parlamentares
  comissao-detalhe <codigo>  Detalhes de uma comissão
  composicao <codigo>     Composição (membros) de uma comissão
  processo <codigo>       Processo legislativo completo de uma matéria
"""

import sys
import json
import urllib.request
import urllib.parse
from datetime import date, datetime

BASE = "https://legis.senado.leg.br/dadosabertos"

def get(path, params=None):
    path = path if path.endswith(".json") else path + ".json"
    url = f"{BASE}{path}"
    if params:
        url += "?" + urllib.parse.urlencode({k: v for k, v in params.items() if v is not None})
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read())

def norm_date(d):
    """Accept YYYY-MM-DD or YYYYMMDD, return YYYYMMDD."""
    return d.replace("-", "")

def senadores():
    r = get("/senador/lista/atual")
    sens = r["ListaParlamentarEmExercicio"]["Parlamentares"]["Parlamentar"]
    print(f"\n🏛️  Senadores em exercício ({len(sens)})\n{'='*60}")
    for s in sorted(sens, key=lambda x: x["IdentificacaoParlamentar"]["NomeParlamentar"]):
        i = s["IdentificacaoParlamentar"]
        print(f"  {i['CodigoParlamentar']:5} | {i['NomeParlamentar']:40} | {i['SiglaPartidoParlamentar']:12} | {i['UfParlamentar']}")
    print()

def buscar_senador(nome):
    r = get("/senador/lista/atual")
    sens = r["ListaParlamentarEmExercicio"]["Parlamentares"]["Parlamentar"]
    nome_lower = nome.lower()
    encontrados = [s for s in sens if nome_lower in s["IdentificacaoParlamentar"]["NomeParlamentar"].lower()]
    if not encontrados:
        print(f"Nenhum senador encontrado para '{nome}'.")
        return
    print(f"\n👤 Senadores — '{nome}'\n{'='*60}")
    for s in encontrados:
        i = s["IdentificacaoParlamentar"]
        print(f"  Código: {i['CodigoParlamentar']} | {i['NomeParlamentar']} | {i['SiglaPartidoParlamentar']}/{i['UfParlamentar']}")
        print(f"  Email: {i.get('EmailParlamentar','')} | {i.get('UrlPaginaParlamentar','')}")
    print()

def senador_id(codigo):
    r = get(f"/senador/{codigo}")
    d = r.get("DetalheParlamentar", {}).get("Parlamentar", {})
    i = d.get("IdentificacaoParlamentar", {})
    m = d.get("DadosBasicosParlamentar", {})
    print(f"\n👤 {i.get('NomeCompletoParlamentar')}")
    print(f"  Partido: {i.get('SiglaPartidoParlamentar')} | UF: {i.get('UfParlamentar')}")
    print(f"  Tratamento: {i.get('FormaTratamento')}")
    print(f"  Email: {i.get('EmailParlamentar')}")
    print(f"  Nascimento: {m.get('DataNascimento','')} | Naturalidade: {m.get('Naturalidade','')}")
    print(f"  Página: {i.get('UrlPaginaParlamentar')}")
    # mandatos
    try:
        mr = get(f"/senador/{codigo}/mandatos")
        mands = mr.get("MandatosParlamentar", {}).get("Parlamentar", {}).get("Mandatos", {}).get("Mandato", [])
        if isinstance(mands, dict):
            mands = [mands]
        print(f"\n  Mandatos: {len(mands)}")
        for m in mands[-2:]:
            print(f"    UF: {m.get('UfParlamentar')} | {m.get('PrimeiraLegislaturaDoMandato',{}).get('DataInicio','')} - {m.get('SegundaLegislaturaDoMandato',{}).get('DataFim','')}")
    except Exception:
        pass
    print()

def agenda(data=None):
    d = norm_date(data) if data else date.today().strftime("%Y%m%d")
    try:
        r = get(f"/plenario/agenda/dia/{d}")
        ag = r.get("AgendaDia", {})
        sessoes = ag.get("Sessoes", {}).get("Sessao", [])
        if isinstance(sessoes, dict):
            sessoes = [sessoes]
        print(f"\n📅 Agenda Plenário Senado — {d[:4]}-{d[4:6]}-{d[6:]}\n{'='*60}")
        if not sessoes:
            print("  Sem sessões plenárias neste dia.")
        for s in sessoes:
            print(f"  {s.get('HoraInicioSessao','?')[:5]} | {s.get('SiglasSessao',''):10} | {s.get('NomeSessao','')}")
    except Exception as e:
        print(f"  Sem dados de agenda para {d}: {e}")
    print()

def agenda_comissoes(mes=None):
    m = mes or date.today().strftime("%Y%m")
    try:
        r = get(f"/comissao/agenda/mes/{m}")
        ag = r.get("AgendaReunioesComissoes", {})
        reunioes = ag.get("Reunioes", {}).get("Reuniao", [])
        if isinstance(reunioes, dict):
            reunioes = [reunioes]
        print(f"\n🏛️  Agenda Comissões — {m}\n{'='*60}")
        for re in reunioes:
            dt = re.get("DataReuniao","")
            hr = re.get("HoraReuniao","")
            sigla = re.get("SiglaComissao","")
            desc = re.get("DescricaoReuniao","")[:60]
            print(f"  {dt} {hr[:5]} | {sigla:8} | {desc}")
    except Exception as e:
        print(f"  Erro ao buscar agenda de comissões: {e}")
    print()

def votacoes(inicio, fim):
    r = get(f"/plenario/lista/votacao/{norm_date(inicio)}/{norm_date(fim)}")
    vots = r.get("ListaVotacoes", {}).get("Votacoes", {}).get("Votacao", [])
    if isinstance(vots, dict):
        vots = [vots]
    if not vots:
        print(f"Sem votações entre {inicio} e {fim}.")
        return
    print(f"\n🗳️  Votações — Senado — {inicio} a {fim}\n{'='*60}")
    for v in vots:
        resultado = v.get("DescricaoResultado","")
        materia = v.get("IdentificacaoMateria","")
        sessao = v.get("SessaoPlenaria","")
        print(f"  {sessao[:10]} | {materia:20} | {resultado}")
    print()

def buscar_materia(assunto, sigla=None, tramitando="S"):
    params = {"assunto": assunto, "tramitando": tramitando}
    if sigla:
        params["sigla"] = sigla
    r = get("/materia/pesquisa/lista", params)
    mats = r.get("PesquisaBasicaMateria", {}).get("Materias", {}).get("Materia", [])
    if isinstance(mats, dict):
        mats = [mats]
    if not mats:
        print(f"Nenhuma matéria encontrada para '{assunto}'.")
        return
    print(f"\n📑 Matérias — '{assunto}'\n{'='*60}")
    for m in mats[:20]:
        # Nova estrutura da API pesquisa/lista
        codigo = m.get("Codigo", m.get("CodigoMateria", ""))
        desc = m.get("DescricaoIdentificacao", f"{m.get('Sigla','')} {m.get('Numero','')}/{m.get('Ano','')}")
        ementa = m.get("Ementa", m.get("EmentaMateria", ""))[:70]
        autor = m.get("Autor", "")
        data = m.get("Data", "")
        print(f"  {codigo:7} | {desc:20} | {data[:10]} | {ementa}")
        if autor:
            print(f"          Autor: {autor}")
    print()

def materia(sigla, numero, ano):
    r = get(f"/materia/pesquisa/lista", {"sigla": sigla, "numero": numero, "ano": ano})
    mats = r.get("PesquisaBasicaMateria", {}).get("Materias", {}).get("Materia", [])
    if isinstance(mats, dict):
        mats = [mats]
    if not mats:
        print(f"Matéria {sigla} {numero}/{ano} não encontrada.")
        return
    m = mats[0]
    i = m.get("IdentificacaoMateria", {})
    s = m.get("SituacaoAtual", {})
    codigo = i.get("CodigoMateria", "")
    print(f"\n📄 {sigla} {numero}/{ano} (código: {codigo})")
    print(f"  Ementa: {i.get('EmentaMateria','')}")
    print(f"  Situação: {s.get('DescricaoSituacao','')}")
    print(f"  Local atual: {s.get('Local','')}")
    if codigo:
        tramitacao(codigo)

def materia_id(codigo):
    r = get(f"/materia/situacaoatual/{codigo}")
    sit = r.get("SituacaoAtualMateria", {})
    i = sit.get("IdentificacaoMateria", {})
    s = sit.get("Autuacao", {})
    print(f"\n📄 Matéria {codigo}")
    print(f"  {i.get('SiglaSubtipoMateria','')} {i.get('NumeroMateria','')}/{i.get('AnoMateria','')}")
    print(f"  Ementa: {i.get('EmentaMateria','')}")
    print(f"  Situação: {s.get('DescricaoSituacao','')}")
    tramitacao(codigo)

def tramitacao(codigo):
    try:
        r = get(f"/materia/movimentacoes/{codigo}")
        movs = r.get("MovimentacaoMateria", {}).get("Materia", {}).get("Movimentacoes", {}).get("Movimentacao", [])
        if isinstance(movs, dict):
            movs = [movs]
        print(f"\n  📋 Tramitação (últimas 8):")
        for m in movs[-8:]:
            dt = m.get("DataMovimentacao","")
            desc = m.get("DescricaoMovimentacao","")[:60]
            local = m.get("DescricaoLocal","")
            print(f"    {dt} | {local:20} | {desc}")
    except Exception as e:
        print(f"  Tramitação não disponível: {e}")

def comissoes():
    r = get("/comissao/lista/colegiados")
    cols = r.get("ListaColegiados", {}).get("Colegiados", {}).get("Colegiado", [])
    if isinstance(cols, dict):
        cols = [cols]
    print(f"\n🏛️  Comissões Permanentes do Senado ({len(cols)})\n{'='*60}")
    for c in sorted(cols, key=lambda x: x.get("SiglaColegiado","")):
        print(f"  {c.get('CodigoColegiado',''):5} | {c.get('SiglaColegiado',''):10} | {c.get('NomeColegiado','')}")
    print()

def filiacoes(codigo):
    r = get(f"/senador/{codigo}/filiacoes")
    filiacoes = r.get("FiliacaoParlamentar", {}).get("Parlamentar", {}).get("Filiacoes", {}).get("Filiacao", [])
    if isinstance(filiacoes, dict):
        filiacoes = [filiacoes]
    print(f"\n🏷️  Filiações Partidárias — Senador {codigo}\n{'='*60}")
    for f in filiacoes:
        partido = f.get("Partido", {}) if isinstance(f.get("Partido"), dict) else {"SiglaPartido": f.get("Partido", "")}
        sigla = partido.get("SiglaPartido", str(partido))
        data_fil = f.get("DataFiliacao", "")
        data_des = f.get("DataDesfiliacao", "atual")
        print(f"  {sigla:12} | {data_fil} - {data_des}")
    print()

def cargos(codigo):
    r = get(f"/senador/{codigo}/cargos")
    cargos = r.get("CargoParlamentar", {}).get("Parlamentar", {}).get("Cargos", {}).get("Cargo", [])
    if isinstance(cargos, dict):
        cargos = [cargos]
    print(f"\n💼 Cargos — Senador {codigo}\n{'='*60}")
    for c in cargos:
        desc = c.get("DescricaoCargo", "")
        inicio = c.get("DataInicio", "")
        fim = c.get("DataFim", "atual")
        print(f"  {desc:40} | {inicio} - {fim}")
    print()

def relatorias_senador(codigo):
    r = get(f"/senador/{codigo}/relatorias")
    rels = r.get("RelatoriaParlamentar", {}).get("Parlamentar", {}).get("Relatorias", {}).get("Relatoria", [])
    if isinstance(rels, dict):
        rels = [rels]
    print(f"\n📋 Relatorias — Senador {codigo}\n{'='*60}")
    for rel in rels[:20]:
        materia = rel.get("IdentificacaoMateria", {})
        desc = f"{materia.get('SiglaSubtipoMateria','')} {materia.get('NumeroMateria','')}/{materia.get('AnoMateria','')}"
        comissao = rel.get("SiglaComissao", "")
        print(f"  {desc:20} | Comissão: {comissao}")
    print()

def licencas(codigo):
    r = get(f"/senador/{codigo}/licencas")
    # Use DFS to find list
    def find_list(obj):
        if isinstance(obj, list): return obj
        if isinstance(obj, dict):
            for v in obj.values():
                result = find_list(v)
                if result is not None: return result
        return None
    lics = find_list(r) or []
    print(f"\n📅 Licenças — Senador {codigo}\n{'='*60}")
    if not lics:
        print("  Nenhuma licença registrada.")
    for l in lics:
        inicio = l.get("DataInicio", "")
        fim = l.get("DataFim", "")
        motivo = l.get("Descricao", l.get("DescricaoMotivo", ""))
        print(f"  {inicio} - {fim:10} | {motivo}")
    print()

def situacao(codigo):
    r = get(f"/materia/situacaoatual/{codigo}")
    sit = r.get("SituacaoAtualMateria", r)
    ident = sit.get("IdentificacaoMateria", {})
    aut = sit.get("Autuacao", {})
    print(f"\n📄 Situação Atual — Matéria {codigo}\n{'='*60}")
    print(f"  {ident.get('SiglaSubtipoMateria','')} {ident.get('NumeroMateria','')}/{ident.get('AnoMateria','')}")
    print(f"  Ementa: {ident.get('EmentaMateria','')}")
    print(f"  Situação: {aut.get('DescricaoSituacao', sit.get('DescricaoSituacao',''))}")
    print()

def emendas_materia(codigo):
    r = get(f"/materia/emendas/{codigo}")
    def find_list(obj):
        if isinstance(obj, list): return obj
        if isinstance(obj, dict):
            for v in obj.values():
                result = find_list(v)
                if result is not None: return result
        return None
    emendas = find_list(r) or []
    print(f"\n📝 Emendas — Matéria {codigo}\n{'='*60}")
    if not emendas:
        print("  Nenhuma emenda encontrada.")
    for e in emendas[:20]:
        autor = e.get("AutorEmenda", e.get("Autor", ""))
        num = e.get("NumeroEmenda", e.get("Numero", ""))
        print(f"  Emenda {num:5} | Autor: {autor}")
    print()

def textos_materia(codigo):
    r = get(f"/materia/textos/{codigo}")
    def find_list(obj):
        if isinstance(obj, list): return obj
        if isinstance(obj, dict):
            for v in obj.values():
                result = find_list(v)
                if result is not None: return result
        return None
    textos = find_list(r) or []
    print(f"\n📄 Textos — Matéria {codigo}\n{'='*60}")
    if not textos:
        print("  Nenhum texto encontrado.")
    for t in textos:
        tipo = t.get("TipoTexto", t.get("DescricaoTipoTexto", ""))
        url = t.get("UrlTexto", "")
        print(f"  {tipo:30} | {url}")
    print()

def votacao_nominal(ano):
    r = get(f"/plenario/votacao/nominal/{ano}")
    def find_list(obj):
        if isinstance(obj, list): return obj
        if isinstance(obj, dict):
            for v in obj.values():
                result = find_list(v)
                if result is not None: return result
        return None
    vots = find_list(r) or []
    print(f"\n🗳️  Votações Nominais — {ano} ({len(vots)} votações)\n{'='*60}")
    for v in vots[:30]:
        resultado = v.get("DescricaoResultado", v.get("Resultado", ""))
        data = v.get("DataSessao", "")
        materia = v.get("DescricaoIdentificacaoMateria", v.get("Materia", ""))
        print(f"  {data:10} | {str(materia)[:40]:40} | {resultado}")
    print()

def resultado_dia(data):
    d = norm_date(data)
    r = get(f"/plenario/resultado/{d}")
    print(f"\n📊 Resultado Plenário — {d[:4]}-{d[4:6]}-{d[6:]}\n{'='*60}")
    print(f"  {json.dumps(r, ensure_ascii=False, indent=2)[:2000]}")
    print()

def discursos_plenario(inicio, fim):
    i = norm_date(inicio)
    f = norm_date(fim)
    r = get(f"/plenario/lista/discursos/{i}/{f}")
    def find_list(obj):
        if isinstance(obj, list): return obj
        if isinstance(obj, dict):
            for v in obj.values():
                result = find_list(v)
                if result is not None: return result
        return None
    discursos = find_list(r) or []
    print(f"\n🎤 Discursos em Plenário — {inicio} a {fim} ({len(discursos)})\n{'='*60}")
    for d in discursos[:20]:
        nome = d.get("NomeParlamentar", d.get("Autor", ""))
        data = d.get("DataPronunciamento", d.get("Data", ""))
        tipo = d.get("TipoPronunciamento", "")
        print(f"  {data:10} | {nome:30} | {tipo}")
    print()

def mesa_senado():
    r = get("/composicao/mesaSF")
    print(f"\n🏛️  Mesa Diretora do Senado\n{'='*60}")
    print(f"  {json.dumps(r, ensure_ascii=False, indent=2)[:2000]}")
    print()

def liderancas_cmd():
    r = get("/composicao/lideranca")
    print(f"\n👥 Lideranças Partidárias\n{'='*60}")
    print(f"  {json.dumps(r, ensure_ascii=False, indent=2)[:2000]}")
    print()

def blocos():
    r = get("/composicao/lista/blocos")
    def find_list(obj):
        if isinstance(obj, list): return obj
        if isinstance(obj, dict):
            for v in obj.values():
                result = find_list(v)
                if result is not None: return result
        return None
    blocs = find_list(r) or []
    print(f"\n🧩 Blocos Parlamentares ({len(blocs)})\n{'='*60}")
    for b in blocs:
        nome = b.get("NomeBloco", b.get("Nome", ""))
        sigla = b.get("SiglaBloco", b.get("Sigla", ""))
        print(f"  {sigla:15} | {nome}")
    print()

def comissao_detalhe(codigo):
    r = get(f"/comissao/{codigo}")
    print(f"\n🏛️  Comissão — {codigo}\n{'='*60}")
    print(f"  {json.dumps(r, ensure_ascii=False, indent=2)[:2000]}")
    print()

def composicao(codigo):
    r = get(f"/composicao/comissao/{codigo}")
    def find_list(obj):
        if isinstance(obj, list): return obj
        if isinstance(obj, dict):
            for v in obj.values():
                result = find_list(v)
                if result is not None: return result
        return None
    membros = find_list(r) or []
    print(f"\n👥 Composição Comissão — {codigo} ({len(membros)} membros)\n{'='*60}")
    for m in membros:
        nome = m.get("NomeParlamentar", m.get("Nome", ""))
        cargo = m.get("DescricaoCargo", m.get("Cargo", ""))
        partido = m.get("SiglaPartido", "")
        print(f"  {nome:35} | {partido:8} | {cargo}")
    print()

def processo(codigo):
    r = get(f"/processo/{codigo}")
    print(f"\n⚖️  Processo Legislativo — {codigo}\n{'='*60}")
    print(f"  {json.dumps(r, ensure_ascii=False, indent=2)[:3000]}")
    print()

COMMANDS = {
    "senadores": lambda args: senadores(),
    "senador": lambda args: buscar_senador(" ".join(args)),
    "senador-id": lambda args: senador_id(args[0]),
    "agenda": lambda args: agenda(args[0] if args else None),
    "agenda-comissoes": lambda args: agenda_comissoes(args[0] if args else None),
    "votacoes": lambda args: votacoes(args[0], args[1]),
    "buscar-pl": lambda args: buscar_materia(" ".join(args[3:]) if len(args) > 3 else args[0], sigla=args[0] if len(args) > 1 else None),
    "buscar": lambda args: buscar_materia(" ".join(args)),
    "materia": lambda args: materia(args[0], args[1], args[2]),
    "materia-id": lambda args: materia_id(args[0]),
    "tramitacao": lambda args: tramitacao(args[0]),
    "comissoes": lambda args: comissoes(),
    "filiacoes": lambda args: filiacoes(args[0]),
    "cargos": lambda args: cargos(args[0]),
    "relatorias": lambda args: relatorias_senador(args[0]),
    "licencas": lambda args: licencas(args[0]),
    "situacao": lambda args: situacao(args[0]),
    "emendas-materia": lambda args: emendas_materia(args[0]),
    "textos": lambda args: textos_materia(args[0]),
    "votacao-nominal": lambda args: votacao_nominal(args[0]),
    "resultado-dia": lambda args: resultado_dia(args[0]),
    "discursos-plenario": lambda args: discursos_plenario(args[0], args[1]),
    "mesa-senado": lambda args: mesa_senado(),
    "liderancas": lambda args: liderancas_cmd(),
    "blocos": lambda args: blocos(),
    "comissao-detalhe": lambda args: comissao_detalhe(args[0]),
    "composicao": lambda args: composicao(args[0]),
    "processo": lambda args: processo(args[0]),
}

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        print(__doc__)
        sys.exit(1)
    cmd = sys.argv[1]
    args = sys.argv[2:]
    try:
        COMMANDS[cmd](args)
    except Exception as e:
        print(f"Erro: {e}", file=sys.stderr)
        import traceback; traceback.print_exc()
        sys.exit(1)
