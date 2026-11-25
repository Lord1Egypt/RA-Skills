# U1 color workflow

Use the current official documentation and installed compatible profiles; avoid copying arbitrary ratios into G-code.

## How mixing works

U1 has four physical toolheads. Full Spectrum produces additional apparent colors with alternating colored layers. It is an optical process, not a continuously variable nozzle pigment blender. Shape, viewing angle, filament translucency and layer choices affect appearance. Preserve target colors and evaluate mixing rather than imposing four flat colors. Source: [Full Spectrum overview](https://wiki.snapmaker.com/en/snapmaker_orca/snapmaker_orca_full_spectrum%20).

## Configure a real project

1. Confirm the installed Orca and firmware meet the current guide requirements. The `0.10mm Color Mixing @Snapmaker U1 (0.4 nozzle)` preset was verified with Orca 2.4.1; discover availability in each installation.
2. Identify actual material family, brand and pigmentation/translucency; the names red/white/black/yellow are insufficient to predict a mix. Test key skin, dark clothing and neutral jacket tones with the intended spools and geometry. Record unachievable colors rather than promising exact skin tone.
3. Import and verify meaningful color regions. Set explicit object/region assignments instead of leaving them at default. The documented **Color Mixing Match → Manual** path uses the configured filament list and can select up to four. Auto mode is documented around the official bundle; use it only when applicable.
4. Review before/after colors and the matching differences. The guide recommends the dedicated 0.10 mm mixing preset for a 0.4 mm U1. Confirm that preset in the actual installation, then slice; do not silently apply a standard 0.20 mm recipe to a mixing job.
5. Inspect surfaces from several directions, tool changes and model/support/tower usage. Check physical swatches before committing to a detailed portrait. Save the verified result as an Orca project 3MF.

Source for matching workflow: [Color Mixing Match Guide](https://wiki.snapmaker.com/en/snapmaker_orca/color_mixing_match_guide).

## Preserve the complete color pipeline

The generator's RGB texture is an intermediate asset. Conversion must produce slicer-supported color regions or paint data. Generic 3MF support does not guarantee that a particular exporter and slicer exchange these correctly. Maintain the textured master, inspect imported assignments, then configure U1 virtual colors in Snapmaker Orca. Do not treat a Meshy/Tripo multicolor export as already calibrated Full Spectrum.

The wider Full Spectrum guide describes mixing controls, local subdivision of mixed regions, whole-domain subdivision, and optional subdivision of infill. Choose these for the actual geometry and preview; more subdivisions can increase tool changes and duration. Current material guidance favors suitable PLA and translucent/high-transmission filaments; assess ordinary opaque spools with tests. Additional sources: [Full Spectrum FAQ](https://wiki.snapmaker.com/en/snapmaker_u1/printing_guides/FAQ_for_Full_Spectrum), [2.3.6 release notes](https://wiki.snapmaker.com/en/snapmaker_orca/release_notes/v236), [Full Spectrum filament guidance](https://wiki.snapmaker.com/en/FAQ/Modules_Accessories_Materials/PLA_Full_Spectrum_Filament_Bundle).
