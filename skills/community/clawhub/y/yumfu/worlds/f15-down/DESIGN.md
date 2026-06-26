# 🌍 New YumFu World: F15 Down (F15坠落)

## World Concept

**Genre**: Modern military strategy RPG with geopolitical choices
**Setting**: Fictional Middle East region "Azure Peninsula" (蔚蓝半岛)
**Time Period**: Alternative 2026
**Style**: Realistic military tactics + diplomatic choices + moral dilemmas

**⚠️ Content Policy**:
- ALL factions are fictional with made-up names
- ALL characters have fictional names (no real historical figures)
- Inspired by real conflicts but fully fictionalized
- No real country names, only faction codenames
- No real terrorist organizations, only fictional groups

---

## Factions (All Renamed)

### Major Powers

1. **United States** → **Western Alliance (WA / 西盟)**
   - Military superpower
   - Advanced tech: drones, stealth aircraft
   - Strong navy presence
   - Attributes: Technology 95, Diplomacy 70, Resources 85

2. **Israel** → **Phoenix State (PS / 凤凰国)**
   - Elite special forces (Falcon Unit - 猎鹰特遣队)
   - Advanced missile defense (Iron Dome → Steel Shield 钢盾)
   - Intelligence agency (Mossad → Shadow Eye 影眼)
   - Attributes: Elite Forces 98, Intelligence 95, Tech 90

3. **Iran** → **Mountain Republic (MR / 山岳共和国)**
   - Revolutionary Guards → Highland Corps (高地军团)
   - Proxy forces across region
   - Missile/drone capabilities
   - Attributes: Asymmetric War 90, Resources 70, Influence 75

### Regional Players

4. **UAE** → **Gulf Emirates (GE / 海湾联盟)**
   - Economic powerhouse
   - Modern air force
   - Diplomatic bridge-builder
   - Attributes: Wealth 95, Diplomacy 85, Tech 75

5. **China** → **Eastern Coalition (EC / 东方联盟)**
   - Economic ties, infrastructure deals
   - Naval presence
   - Diplomatic mediator
   - Attributes: Economy 98, Diplomacy 80, Naval 70

6. **Saudi Arabia** → **Desert Kingdom (DK / 沙漠王国)**
   - Oil wealth, modern weapons
   - Regional influence
   - Sunni leadership
   - Attributes: Wealth 90, Military 75, Influence 80

---

## Recent Events (Fictionalized)

### Major Incidents Timeline

**Day 1 - "Viper Strike"**
- Phoenix State special forces eliminate MR general "Hassan al-Qamar" (虚构)
- Location: Neutral zone safehouse
- Reaction: MR vows retaliation

**Day 7 - "Sky Fall"**
- MR launches drone swarm attack
- Targets: PS power grid, oil refinery in Port Azure
- 3 stealth drones shot down, 12 hit targets
- Civilian infrastructure damaged

**Day 14 - "Thunder Response"**
- WA-PS joint strike on MR weapon facilities
- 50+ targets: missile factories, drone bases, command centers
- Collateral damage: school in Damascus District (虚构), hospital wing

**Day 21 - "Shadow Raid"**
- MR-backed militia kidnaps WA contractors in Border City
- PS Falcon Unit launches rescue operation
- 2 hostages saved, 1 killed in crossfire

**Day 28 - "Black Friday"**
- MR shoots down WA surveillance drone over Azure Strait
- International waters dispute
- EC calls for ceasefire, DK stays neutral

**Day 35 - "Fallen Eagle" (CSAR)**
- MR SA-400 shoots down WA F-15E near Highland Fortress
- Pilot "Vega" ejects 85km behind enemy lines
- Full Combat Search and Rescue operation launched
- Assets: A-10 Warthogs, HH-60W Jolly Green, AH-64 Apache, CV-22 Osprey, C-130J, MQ-9 Reaper
- Complications: active SAM, sandstorm, MR search parties, damaged aircraft
- Key dilemma: if aircraft can't return — switch to smaller planes, emergency highway landings, or abandon and walk to border

---

## Gameplay Mechanics

### Player Choices

**Choose Your Faction**: Each has unique strengths/weaknesses
- **WA**: Air superiority, tech advantage, international support
- **PS**: Elite special ops, intelligence network, defensive tech
- **MR**: Asymmetric warfare, proxy forces, missile arsenal
- **GE**: Diplomacy, economic leverage, modern air force
- **EC**: Economic sanctions, UN influence, naval blockade

### Decision Tree Examples

**Scenario 1: Hostage Crisis**
```
MR militia captures 5 WA engineers in border town
→ [PS Falcon Unit] Immediate rescue raid (high risk, diplomatic fallout)
→ [Negotiate] Trade prisoner exchange (slow, unpopular at home)
→ [Economic Pressure] Freeze MR assets, wait (civilian risk)
```

**Scenario 2: Civilian Casualty**
```
Your airstrike hits school (intel failure)
→ [Admit] Apologize, compensate families (domestic backlash)
→ [Deny] Claim MR propaganda (international criticism)
→ [Blame MR] Say they used human shields (evidence needed)
```

**Scenario 3: Oil Refinery Attack**
```
MR drones target your oil facility
→ [Retaliate] Strike MR energy infrastructure
→ [Defend] Invest in air defense, absorb loss
→ [Escalate] Target MR leadership (risk of wider war)
```

---

## Game Features

### 1. **Strategic Map**
- Azure Peninsula terrain
- Key cities: Port Azure, Mountain City, Desert Gate, Border Town
- Infrastructure: oil fields, power plants, ports, airbases
- Real-time threat tracker (missile launches, drone swarms)

### 2. **Unit Types**
- **Special Forces**: Stealth raids, hostage rescue
- **Air Force**: Stealth bombers, fighter jets, drones
- **Navy**: Carriers, destroyers, submarines
- **Missiles**: Precision strikes, infrastructure damage
- **Cyber**: Hack enemy comms, disable defense systems
- **Proxies**: Militia groups, deniable ops

### 3. **Resources**
- **Budget**: Funding for operations
- **International Support**: UN votes, sanctions
- **Intelligence**: Intel on enemy positions
- **Public Opinion**: Domestic/global approval
- **Energy**: Oil/gas control affects economy

### 4. **Consequences**
- Civilian casualties → international outcry
- Failed ops → domestic backlash
- Escalation → neighboring countries join
- Economic damage → budget constraints
- War crimes → UN sanctions

---

## Story Arcs

### Arc 1: Viper's Nest (Day 1-30)
Assassination of MR general triggers spiral of retaliation

### Arc 2: Shadow Lines (Day 31-60)
Proxy war intensifies, hostage crises, border skirmishes

### Arc 3: Storm Horizon (Day 61-90)
Risk of full-scale war, diplomatic endgame or total conflict

---

## Special Operations (Playable Missions)

1. **"Falcon Dawn"** - Rescue hostages from Border City
2. **"Steel Rain"** - Defend against MR missile barrage
3. **"Silent Hunter"** - Submarine infiltration to plant surveillance
4. **"Fire and Shadow"** - Night raid on MR weapons cache
5. **"Last Light"** - Evacuate civilians before airstrike
6. **"Fallen Eagle"** - CSAR: Full air armada rescues downed F-15 pilot deep behind enemy lines

---

## Moral Dilemmas

**The Trolley Problem Scenarios**:
- Strike weapons depot in residential area? (10 civilians vs 100 future deaths)
- Torture captured enemy for intel on imminent attack?
- Use economic sanctions knowing they harm civilians?
- Arm questionable rebel groups to weaken enemy?

---

## Technical Implementation

### File Structure
```
~/clawd/skills/yumfu/worlds/
  shadow-war/
    world.json          # World metadata
    factions.json       # 6 major factions
    events.json         # 50+ scripted events
    locations.json      # Map data
    units.json          # Military units
    decisions.json      # Choice trees
    consequences.json   # Outcome matrices
```

### Art Style
- Satellite imagery aesthetic for map
- Military-grade HUD
- News report style event narration
- Intel briefing documents
- Propaganda posters for each faction

---

## Sample Opening

```
📰 BREAKING NEWS - Azure Peninsula Crisis

Day 1, 0600 Hours
Port Azure Times

MOUNTAIN REPUBLIC GENERAL ASSASSINATED

Hassan al-Qamar, commander of MR Highland Corps, 
eliminated in precision strike on neutral zone safehouse.

Phoenix State claims responsibility. 
Western Alliance confirms intelligence support.
Mountain Republic vows "thunder and fire" retaliation.

Your role: [Choose Faction]
- Western Alliance: Maintain regional stability
- Phoenix State: Ensure national security
- Mountain Republic: Defend sovereignty
- Gulf Emirates: Protect economic interests
- Eastern Coalition: Mediate and gain influence
- Desert Kingdom: Navigate sectarian tensions

The world is watching. What will you do?
```

---

## Next Steps

1. Create world.json with faction balance
2. Write 50+ event scenarios
3. Build decision tree system
4. Design consequence matrices
5. Generate first round of AI art (military HUD, maps)
6. Test gameplay locally
7. Balance difficulty/realism

---

**Themes**: 
- No clear "good guys" - all factions have valid and flawed motives
- Fog of war - incomplete intel leads to tragic mistakes
- Blowback - today's ally is tomorrow's enemy
- Civilian cost - every military choice has human consequences
- Diplomacy vs Force - when to negotiate, when to strike

**Goal**: Make players think hard about real-world geopolitical complexity
