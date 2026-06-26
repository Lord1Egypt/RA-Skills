# CTA Variants — Slide 7

CTA selalu mengarah ke `https://openjournaltheme.com/`. Hanya copy yang berotasi.

Aturan rotasi:
- Track varian terakhir di handoff log via field `cta_variant_used`
- Tidak boleh pakai varian yang sama dalam 5 artikel berturut-turut
- Default selection: hash(article_id) mod len(varian) untuk distribusi merata

## Catalog (15 varian, label-stable)

### Tone: Practical / Functional

| Label | Headline | Sub |
|-------|----------|-----|
| `upgrade-tampilan` | Upgrade Tampilan Jurnal Anda | Tema OJS profesional siap pakai |
| `tema-premium` | Lihat Tema OJS Premium | Desain modern untuk jurnal akademik |
| `langganan-tema` | Langganan Tema OJS | Akses semua tema, update berkala |
| `mulai-jurnal-baru` | Mulai Jurnal Baru | Tema OJS siap deploy hari ini |
| `revamp-jurnal` | Revamp Jurnal Lama Anda | Update tampilan tanpa migrasi data |

### Tone: Authority / Standard

| Label | Headline | Sub |
|-------|----------|-----|
| `standar-internasional` | Tampilan Setara Standar Internasional | Tema OJS yang lolos uji indeksasi |
| `kompatibel-ojs3` | Kompatibel OJS 3.x Terbaru | Tema yang selalu update versi |
| `siap-doaj-scopus` | Siap Indeks DOAJ & Scopus | Tema dengan markup metadata lengkap |
| `wcag-compliant` | Tema WCAG-Compliant | Aksesibilitas untuk semua pembaca |

### Tone: Curiosity / Discovery

| Label | Headline | Sub |
|-------|----------|-----|
| `lihat-koleksi` | Lihat Koleksi Tema OJS | 30+ desain untuk berbagai disiplin |
| `temukan-tema` | Temukan Tema yang Pas | Filter by audience, layout, palette |
| `inspirasi-tampilan` | Inspirasi Tampilan Jurnal | Browse showcase jurnal real |

### Tone: Urgency / Practical Pressure

| Label | Headline | Sub |
|-------|----------|-----|
| `instal-hari-ini` | Instal Hari Ini | Tema OJS plug-and-play |
| `tanpa-koding` | Ganti Tema Tanpa Koding | Konfigurasi via dashboard OJS |
| `support-bahasa-id` | Support Bahasa Indonesia | Dokumentasi & bantuan dalam Bahasa Indonesia |

## Anti-Pattern (jangan pakai)

- "Klik di sini" / "Click here" — generik, tidak deskriptif
- "Beli sekarang!" — too aggressive untuk audiens akademik
- Klaim numerik tanpa basis: "1000+ jurnal pakai tema kami" — kecuali ada sumber verifiable
- Janji ranking: "Naikkan ranking jurnal Anda" — over-promise, tidak terverifikasi
- Bahasa marketing kasar: "WAJIB punya!", "RAHASIA editor"

## Format dalam Handoff JSON

```json
{
  "cta_variant_used": "upgrade-tampilan",
  "cta_url": "https://openjournaltheme.com/"
}
```

`cta_variant_used` selalu pakai label dari catalog di atas, bukan headline string. Ini agar SENKU bisa enforce no-repeat-in-5 dengan exact match.
