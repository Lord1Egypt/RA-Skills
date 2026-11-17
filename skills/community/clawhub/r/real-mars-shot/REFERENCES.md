# References / 文献

`data/science.json` 里每个数字都指向下面的 `source_id`。叶子上 `estimate: true` 的值是估计，叙述时必须说成估计，不能说成测量结果。机构名只出现在文献里，不作为游戏里的反派。

Every number in `data/science.json` points at a `source_id` below. A leaf with `estimate: true` must be spoken as an estimate, not as a measurement. Agencies appear here as sources, not as villains in the game.

## std_gravity

Standard gravity g0 = 9.80665 m/s^2

BIPM / ISO 80000-3 standard gravity, the conventional value used in the rocket equation.

https://www.bipm.org/en/publications/si-brochure

## codata_c

Speed of light 299792458 m/s

CODATA / SI definition of the metre. Light time = distance / c.

https://physics.nist.gov/cgi-bin/cuu/Value?c

## tsiolkovsky

Tsiolkovsky rocket equation

Δv = Isp · g0 · ln(m0/mf). Classical. Used here with vacuum Isp planning values.

https://www.grc.nasa.gov/www/k-12/rocket/rktpow.html

## zeitlin2013_cruise

MSL/RAD cruise dose

Zeitlin, C. et al. Measurements of Energetic Particle Radiation in Transit to Mars on the Mars Science Laboratory. Science 340, 1080–1084 (2013). doi:10.1126/science.1235989. Tissue-equivalent dose 0.48 ± 0.08 mGy/day; dose equivalent 1.84 ± 0.30 mSv/day inside the spacecraft over ~253 days. Shortest comparable round trip 0.66 ± 0.12 Sv.

https://www.science.org/doi/10.1126/science.1235989

## zeitlin2014_surface

MSL/RAD Mars surface dose

Zeitlin, C. et al. Mars’ Surface Radiation Environment Measured with the Mars Science Laboratory’s Curiosity Rover. Science 343, 1244797 (2014). doi:10.1126/science.1244797. First ~300 sols near solar maximum: 0.21 ± 0.04 mGy/day absorbed; 0.64 ± 0.12 mSv/day dose equivalent, on the rover deck (RTG background subtracted).

https://www.science.org/doi/10.1126/science.1244797

## nasa_bvad_2022

NASA BVAD metabolic loads

Ewert, M.K. et al. Life Support Baseline Values and Assumptions Document. NASA/TP-20210024855 (2022 update). Table 3-31, 82 kg crewmember, RQ 0.86, exercise included: O2 0.895 kg/CM-d, CO2 1.085 kg/CM-d, food solids 0.800 kg/CM-d, food energy 12.778 MJ/CM-d, potable water 3.217 kg/CM-d. ISS food logistics 2.39 kg/CM-d including packaging is discussed in the same section from Ewert et al. 2019.

https://ntrs.nasa.gov/citations/20210024855

## nasa_iss_water_2023

ISS 98% water recovery

NASA. NASA Achieves Water Recovery Milestone on International Space Station (2023). Brine Processor Assembly brought total ECLSS water recovery to 98%; before BPA, about 93–94%.

https://www.nasa.gov/missions/station/iss-research/nasa-achieves-water-recovery-milestone-on-international-space-station/

## nasa_eclss_o2_2021

Oxygen recovery from CO2

NASA life-support briefing, NTRS 20210013975 (2021). Current O2 recovery from CO2 about 47%; goal >75%. Sabatier reaction CO2 + 4 H2 → CH4 + 2 H2O is hydrogen-limited by electrolysis.

https://ntrs.nasa.gov/citations/20210013975

## colaprete2010

LCROSS lunar water ice

Colaprete, A. et al. Detection of Water in the LCROSS Ejecta Plume. Science 330, 463–468 (2010). doi:10.1126/science.1186986. Cabeus permanently shadowed crater: 5.6 ± 2.9% water ice by mass; 155 ± 12 kg water vapor and ice in the instrument field of view.

https://www.science.org/doi/10.1126/science.1186986

## hecht2009

Phoenix perchlorate

Hecht, M.H. et al. Detection of Perchlorate and the Soluble Chemistry of Martian Soil at the Phoenix Lander Site. Science 325, 64–67 (2009). doi:10.1126/science.1172466. Perchlorate at the Phoenix site on the order of 0.4–0.6 wt%.

https://www.science.org/doi/10.1126/science.1172466

## nasa_moxie_2023

MOXIE oxygen demo

NASA. NASA’s Oxygen-Generating Experiment MOXIE Completes Mars Mission (2023). 16 runs, 122 g O2 total, peak 12 g/h, purity ≥98%. A demonstration, not a crew-scale propellant plant.

https://www.nasa.gov/missions/mars-2020-perseverance/perseverance-rover/nasas-oxygen-generating-experiment-moxie-completes-mars-mission/

## nasa_dra5_2009

Mars DRA 5.0

Drake, B.G. (ed.). Human Exploration of Mars Design Reference Architecture 5.0. NASA/SP-2009-566 (2009). Addendum NASA/SP-2009-566-ADD. Conjunction-class long-stay missions, opportunities about every 26 months / 2.1 years, 15-year synodic cycle. Example communications two-way 6–44 minutes. Moon vs Mars comparison table: Mars total mission mass ~800–1200 t, total Δv LEO to surface and back 12–14 km/s; Moon ~9.5 km/s and ~200 t. Crew of 6, surface stay on the order of 500 days, transits on the order of 180–210 days. Pre-deploy cargo one opportunity (~26 months) ahead.

https://ntrs.nasa.gov/citations/20090040343

## borowski_ntr_2012

DRA 5.0 NTR Isp

Borowski, S.K., McCurdy, D.R., Packard, T.W. Nuclear Thermal Rocket/Vehicle Characteristics and Sensitivity Trades for NASA’s Mars DRA 5.0. NASA NTRS 20120012928. NERVA-derived NTR Isp ~900–910 s. Cargo vehicles on minimum-energy paths; crewed vehicle on a faster conjunction trajectory.

https://ntrs.nasa.gov/citations/20120012928

## nssdc_mars_factsheet

NSSDC Mars fact sheet

NASA Goddard NSSDC Mars Fact Sheet. Surface pressure ~6.36 mb (variable), CO2 95.32%, N2 2.7%, Ar 1.6%, O2 0.13%, CO 0.08%. Mean temperature ~210 K. Surface gravity 3.71 m/s^2. Sidereal orbit 686.98 d. Semi-major axis 1.5237 AU.

https://nssdc.gsfc.nasa.gov/planetary/factsheet/marsfact.html

## nssdc_moon_factsheet

NSSDC Moon fact sheet

NASA Goddard NSSDC Moon Fact Sheet. Surface gravity 1.62 m/s^2. Mean distance 384,400 km. Sidereal month 27.3 d; synodic month ~29.5 d so a lunar night is ~14.8 d away from the poles.

https://nssdc.gsfc.nasa.gov/planetary/factsheet/moonfact.html

## braun_manning_2007

Mars EDL mass ceiling

Braun, R.D. and Manning, R.M. Mars Exploration Entry, Descent, and Landing Challenges. Journal of Spacecraft and Rockets 44(2), 310–323 (2007). doi:10.2514/1.25116. Heritage landed mass is about one tonne. Human-scale landers (tens of tonnes) need supersonic retropropulsion or other new EDL and are not demonstrated.

https://doi.org/10.2514/1.25116

## severinghaus1994_biosphere2

Biosphere 2 oxygen collapse

Severinghaus, J.P. et al. Oxygen loss in Biosphere 2. Eos, Transactions AGU 75(3), 33–37 (1994). doi:10.1029/94EO00285. Closed ecological systems can drift: O2 fell from ~20.9% toward ~14.5% as unaccounted respiration and CO2 uptake (including structural concrete) unbalanced the air. Social fracture accompanied the physical one.

https://doi.org/10.1029/94EO00285

## esa_mars500

Mars-500 isolation

IBMP / ESA Mars-500 (2010–2011), 520-day isolation study with a 6-person crew. Psychology and operations analog, not a closed ecological life-support closure test.

https://www.esa.int/Science_Exploration/Human_and_Robotic_Exploration/Mars500

## nasa_std_3001

NASA crew health standard

NASA Spaceflight Human-System Standard NASA-STD-3001. Career radiation control is framed as risk of exposure-induced death (REID), historically a 3% REID criterion at high confidence, and is age- and sex-specific. It is not a single sievert number. The game’s 600 mSv dose-equivalent planning cap is a conservative operational screen, marked as an estimate, not a quotation of the standard.

https://standards.nasa.gov/standard/NASA/NASA-STD-3001

## icrp103

ICRP occupational dose analogy

ICRP Publication 103 (2007). Planned occupational exposure is typically managed around 20 mSv/year averaged over 5 years, with no single year above 50 mSv. The ember uses 20 mSv/year as a permanent-settlement design target. The 500-day crew foothold uses the 50 mSv single-year figure. Both are game analogies, not a spaceflight rule and not a claim that ICRP certifies planetary habitats.

https://www.icrp.org/publication.asp?id=ICRP%20Publication%20103

## smith2014

Genetic census for a new world

Smith, C.M. Estimation of a genetically viable population for multigenerational interstellar voyaging: Review and data for world ships. Acta Astronautica 97, 16–29 (2014). doi:10.1016/j.actaastro.2013.12.013. Order-of-magnitude census runs to the tens of thousands without a germplasm bank. A hundred living people are an engineering seed only if a large archive travels with them.

https://doi.org/10.1016/j.actaastro.2013.12.013

## spacex_falcon_heavy

Published heavy-lift class figures

SpaceX public Falcon Heavy capability figures widely published in the early 2020s: about 63,800 kg to LEO expendable, 26,700 kg to GTO, 16,800 kg to Mars. Commercial claims change. The game’s purchasable ‘heavy’ class is deliberately lower and is an estimate of what a program can repeatedly buy, not a quote of one rocket.

https://www.spacex.com/vehicles/falcon-heavy/

## nasa_sls

SLS Block 1 class

NASA Space Launch System reference figures: Block 1 on the order of 95 t to LEO and about 27 t to trans-lunar injection. Cadence and cost are not those of a commercial medium launcher. NASA OIG has reported multi-billion-dollar per-flight costs; the game does not treat that as the only price of heavy lift.

https://www.nasa.gov/humans-in-space/space-launch-system/

## nasa_kilopower

Kilopower / KRUSTY

NASA Kilopower project and the KRUSTY ground test: fission power in the roughly 1–10 kWe class aimed at Moon and Mars surface systems. A crew settlement’s grow-lights need megawatts; kilowatts keep robots and storm survival alive.

https://www.nasa.gov/directorates/stmd/tech-demo-missions-program/kilopower/

## jonsson2008_tardigrade

Tardigrades survive exposure, they do not colonize

Jönsson, K.I. et al. Tardigrades survive exposure to space in low Earth orbit. Current Biology 18(17), R729–R731 (2008). doi:10.1016/j.cub.2008.06.048. Vacuum and radiation survival on FOTON-M3. Survival of a dormant animal is not an ecosystem.

https://doi.org/10.1016/j.cub.2008.06.048

## sancho2007_lichen

Lichens survive space exposure

Sancho, L.G. et al. Lichens survive in space: results from the 2005 LICHENS experiment. Astrobiology 7(3), 443–454 (2007). doi:10.1089/ast.2006.0046. Exposure survival again, not growth of a biosphere. On Mars, UV, desiccation, and perchlorates still block open-air establishment.

https://doi.org/10.1089/ast.2006.0046

## lenski_travisano_1994

10,000 generations of E. coli, not 10,000 years

Lenski, R.E. and Travisano, M. Dynamics of adaptation and diversification: a 10,000-generation experiment with bacterial populations. PNAS 91(15), 6808–6814 (1994). doi:10.1073/pnas.91.15.6808. Early results of the long-term evolution experiment: adaptation and divergence among populations. E. coli in that experiment divides several times a day, so 10,000 generations are a few years of flasks. The game stores this number so it is not confused with the 10,000-year deep-time tier. Microbial experimental evolution is much faster than speciation-scale calendar time. The tier does not claim otherwise.

https://doi.org/10.1073/pnas.91.15.6808

## hendry2007_speciation

Ecological speciation has no single clock

Hendry, A.P., Nosil, P. and Rieseberg, L.H. The speed of ecological speciation. Functional Ecology 21(3), 455–464 (2007). doi:10.1111/j.1365-2435.2007.01240.x. The paper's point is that "how long does speciation take" has no single answer. Some ecological cases are a few hundred generations. Many animal lineages are closer to a million years. The game's 10,000-year mark is an estimate set at the low end of "thousands to tens of thousands of years." It is not a measurement from this paper, and it is not a schedule on which a moss or a microbe becomes a named new species.

https://doi.org/10.1111/j.1365-2435.2007.01240.x

## nasa_cp2255_1982

1980 NASA study of a self-replicating lunar factory

Freitas, R.A. Jr. and Gilbreath, W.P. (eds). Advanced Automation for Space Missions. NASA Conference Publication 2255 (1982). Proceedings of the 1980 NASA/ASEE summer study on a lunar factory that would maintain itself and grow from local material. It is a concept study. The factory was not built. This game does not copy its design and does not provide a way to build one. The 50-year machine tier, the metal rate, and the "copies got better" die roll are estimates anchored to that idea: ore, energy, heat rejection, repair, and replication. They are not figures quoted from the study as demonstrated performance.

https://ntrs.nasa.gov/citations/19830007077

## von_neumann_1966

Theory of a self-reproducing automaton

von Neumann, J. Theory of Self-Reproducing Automata. Edited and completed by A.W. Burks. University of Illinois Press (1966). A theoretical machine that contains a description of itself and a constructor that can copy both. The argument needs the copy to be faithful enough that the description survives. It is not a spacecraft design and not a measured error rate. The game's fidelity floor (0.90, an estimate) and the seed factory's starting fidelity (0.97, an estimate) are game numbers in that spirit. Drift can pull a line under the floor. The floor is then a reason the next epoch is refused, not a protocol for building the machine.

https://archive.org/details/theoryofselfrepr00vonn_0

## cospar_planetary_protection

COSPAR planetary protection

COSPAR Policy on Planetary Protection. Mars missions are typically Category IV; missions that can reach special regions are more stringent. The policy limits forward contamination of other worlds. It does not describe how to release organisms, and this game does not either. The political cost of a sealed off-world culture is an estimate of that constraint.

https://cosparhq.cnes.fr/scientific-structure/panels/panel-on-planetary-protection-ppp/

## game_calibration

Game calibration marked as estimates

Where a single published number does not exist (shielding transmission curve, farm lighting power, IMLEO campaign splits, dramatic solar-particle odds, ascent-propellant threshold), the value is an order-of-magnitude estimate anchored to the cited literature. Estimates are flagged estimate=true and must be spoken as estimates.

https://github.com/yumyumtum/real-mars-shot
