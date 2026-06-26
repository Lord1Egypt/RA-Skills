# supercoolpeep-generator

Generate a SuperCoolPeep from supercoolpeeps.com using a 68-digit seed.

## Usage

### Generate Random Peep
```bash
node scripts/generate_peep.cjs
```

### Generate Specific Trait (Ape, Skeleton, Zombie)
```bash
node scripts/generate_peep.cjs "" [type]
```
Example: `node scripts/generate_peep.cjs "" ape`

## Traits Mapping (Seed Digits 3 & 4)
- 00-39: Normal
- 40-71: Skinny
- 72-91: Tattoo
- 92-96: Ape
- 97-98: Zombie
- 99: Skeleton
