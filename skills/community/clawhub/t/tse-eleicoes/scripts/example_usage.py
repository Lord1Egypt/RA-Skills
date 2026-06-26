"""
Exemplos de uso do cliente TSE.

Execute:
    python scripts/example_usage.py
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

from tse_client import (
    get_tse_client,
    ELEICOES_ORDINARIAS,
    CARGOS,
    nome_cargo,
    nome_eleicao,
)


async def main():
    client = get_tse_client()

    try:
        print("=" * 60)
        print("TSE Eleições — Exemplos de uso")
        print("=" * 60)

        # 1. Anos eleitorais
        print("\n📅 Anos eleitorais disponíveis:")
        anos = await client.get_anos_eleitorais()
        print(f"  {anos}")

        # 2. Eleições ordinárias
        print("\n🗳️  Eleições ordinárias (IDs conhecidos):")
        for ano, eleicao_id in ELEICOES_ORDINARIAS.items():
            print(f"  {ano} → {eleicao_id} ({nome_eleicao(eleicao_id)})")

        # 3. Cargos disponíveis
        print("\n🎖️  Cargos eleitorais:")
        for cod, nome in CARGOS.items():
            print(f"  {cod} = {nome}")

        # 4. Candidatos a prefeito em São Paulo (Municipais 2024)
        print("\n👤 Buscando candidatos a Prefeito em São Paulo (2024)...")
        try:
            candidatos = await client.get_candidatos(
                ano=2024,
                municipio_cod="71072",
                eleicao_id=ELEICOES_ORDINARIAS["2024"],
                cargo_cod="11",
            )
            print(f"  Total encontrado: {len(candidatos)}")
            for c in candidatos[:3]:
                print(f"  → {c.get('nomeUrna', c.get('nome', 'N/A'))}")
        except Exception as e:
            print(f"  ⚠️  {e}")

        # 5. Datasets CKAN
        print("\n📦 Datasets disponíveis no portal de dados abertos...")
        try:
            datasets = await client.get_datasets()
            print(f"  Total de datasets: {len(datasets)}")
            print(f"  Primeiros 5: {datasets[:5]}")
        except Exception as e:
            print(f"  ⚠️  {e}")

        # 6. Busca de datasets de candidatos
        print("\n🔍 Buscando datasets de candidatos...")
        try:
            ds_candidatos = await client.get_datasets_candidatos()
            print(f"  Encontrados: {len(ds_candidatos)} datasets")
            for ds in ds_candidatos[:2]:
                print(f"  → {ds.get('title', ds.get('name', 'N/A'))}")
        except Exception as e:
            print(f"  ⚠️  {e}")

        print("\n✅ Exemplos concluídos!")

    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())
