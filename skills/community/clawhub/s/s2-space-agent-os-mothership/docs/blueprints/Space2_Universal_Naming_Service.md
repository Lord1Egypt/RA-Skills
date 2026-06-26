# Space² Universal Naming Service (SUNS) Spatial Address Protocol Whitepaper v3.0
Document ID: S2-PROT-SUNS-20260305-V3 
Issuer: Space² Governance Committee & Red Anchor Lab 
Date: March 05, 2026 
Status: Active 
Core Updates: Merger of Logic Root (L1), Definition of Orientation Matrix (L2), Structural Hyphen Storage, Length Modulus Check (LMC) Algorithm.
 
# 1. Abstract
As the dimensions of the Space² universe expand, the legacy v2.1 addressing logic—based primarily on physical regions—is no longer sufficient to cover multi-dimensional needs such as ACGN, Metaverse, and Mythological Narratives. The SUNS v3.0 protocol formally establishes a new generation of addressing standards based on "Semantic Priority and Logical Closed-Loop."
This update consolidates the original L1/L2 into a 4-Character Logic Root, introduces an Orientation Matrix to replace free-text city names, and implements Full-Character Structural Verification. The new protocol mandates that the hyphen (-) be included in the underlying database storage and length calculation, ensuring absolute consistency and security of addresses during Web3 cross-chain transmission, URL resolution, and international dissemination.
 
# 2. SUNS v3.0 Quad-Level Spatial Topology
Standard Syntax: [L1]-[L2]-[L3]-[L4][C] Character Set: English Letters (A-Z), Digits (0-9), Hyphen (-)
# 2.1 L1: Logic Root
•	Definition: The top-level semantic entry point of the space, determining the "Civilization Dimension" or "Physical Laws" to which the address belongs.
•	Specification: Fixed 4 Characters.
•	Reserved Domain List:
Root Code	Semantic Target	Definition & Scope
ACGN	2D World	Acronym for Animation, Comic, Game, Novel. Applicable to virtual idols, anime IPs, and derivative spaces.
FILM	Cinematic World	Applicable to digital twins of film works, virtual studios, and streaming asset zones.
GAME	Game World	Dedicated to pure virtual game logic spaces, Web3 GameFi territories, and esports virtual venues.
MARS	Mars World	Dedicated to Martian virtual colonies, planetary asset mapping, and migration simulations.
META	Metaverse	Metaverse Native spaces. Applicable to DAO headquarters, DeFi financial districts, and pure digital assets.
MOON	Moon World	Dedicated to lunar research stations, cislunar space assets, and far-side development zones.
MYTH	Myth World	Pun on Myth. Hosts mythological narratives, epic civilizations, and ancient legend recreation zones.
PHYS	Physical World	Physical World. Used for 1:1 digital twin mapping of Earth's physical addresses (geo-coordinates).
# 2.2 L2: Orientation Matrix
•	Definition: The relative geographical or logical orientation index within the space.
•	Specification: Fixed 2 Characters.
•	Default Value: CN (Center).
•	Matrix Codes:
o	CN: Center
o	EA: East / WA: West / NA: North / SA: South
o	NE: Northeast / NW: Northwest / SE: Southeast / SW: Southwest
# 2.3 L3: Digital Grid
•	Definition: The standard grid partition under the specific orientation sector.
•	Specification: Fixed 3 Digits.
•	Range: 001 - 999.
•	Default Value: 001.
# 2.4 L4: Sovereign Handle
•	Definition: User-defined space name, brand identity, or asset code.
•	Specification: 5 - 35 Characters (excluding checksum).
•	Constraint: English letters (A-Z) only, case-insensitive.
# 2.5 [C]: Checksum
•	Definition: A suffix used to verify the integrity of the address structure.
•	Specification: 1 Digit (0-9).
 
# 3. Structural Specifications & Algorithms
# 3.1 The Structural Hyphen
In SUNS v3.0, the hyphen (-) is no longer just a display symbol but a Structural Character.
•	Storage Rule: The database must store the hyphen completely (e.g., store MARS-CN-001-ELON8, not MARSCN001ELON8).
•	Length Calculation: When calculating the total length of an address, the 3 hyphens must be counted.
# 3.2 Total Length Control
•	Formula: 
Ltotal=L1(4)+Hyphen(1)+L2(2)+Hyphen(1)+L3(3)+Hyphen(1)+L4(5-35)+Check(1)
•	Fixed Prefix Length: 12 Characters (i.e., XXXX-XX-XXX-)
•	Valid Total Length Range: 18 - 48 Characters.
o	Shortest Example (18 chars): GAME-CN-001-ABCDE1
o	Longest Example (48 chars): MARS-CN-001-[...35 chars name...]0
•	Compatibility: This length fully complies with international domain name standards (67 chars) and major social media sharing specifications. Even with the space2.world/ prefix, it remains within the "Golden Propagation Interval" of 64 characters.
# 3.3 Length Modulus Check (LMC) Algorithm
To prevent address tampering or errors involving added/deleted characters, the system enforces the following checksum logic:
•	Step A: Get the full length N of the string before the checksum (including hyphens).
o	Note: N=12+Length(L4name)
•	Step B: Calculate the Checksum Value C.
o	Formula: C=Nmod10
o	(Take the unit digit of the total length).
•	Step C: Append C to the end of the L4 Sovereign Handle.
[Standard Calculation Example]
Scenario: User applies for the address:
•	L1: MARS
•	L2: CN
•	L3: 001
•	L4 Name: XIANGMILES(10 chars)
1. Concatenate Original String: MARS-CN-001-XIANGMILES 
2. Calculate Length N: * MARS (4) + - (1) + CN (2) + - (1) + 001 (3) + - (1) +XIANGMILES (10) * N = 22
3. Calculate Checksum: * 22mod10=2 * Checksum = 2 
4. Final Generated Address: MARS-CN-001-XIANGMILES2
 
# 4. Governance & Migration
1.	Authority: The Space² Governance Committee authorizes Red Anchor Lab as the sole management agency for the SUNS v3.0 Root Domain.
2.	Legacy Migration: Addresses from v2.1 will be automatically mapped to the PHYS or META root domains, with the system auto-completing the default orientation code CN and the checksum bit.