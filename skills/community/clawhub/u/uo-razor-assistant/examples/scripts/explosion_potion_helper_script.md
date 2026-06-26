// Outlands Explosion Potion Helper
// Example reference script for Ultima Online Outlands.
// This script is intentionally treated as a shard/version-sensitive exemplar.
// Validate it in-client before relying on it in PvP or competitive play.

if pvp
    sysmsg 'Structured PvP detected; cooldown and serial helpers may be restricted'
else
    // Saved target persists between throws. Initialize if your Razor build supports this syntax.
    @setvar! savedtarget 0

    // Attempt to find an explosion potion in your backpack.
    @findtype '0x0F0C' 'backpack' as potion

    if potion != 0
        if cooldown 'Explosion' == 0
            lift potion 1
            waitfortarget

            if savedtarget != 0
                target savedtarget
            else
                overhead 'Select an explosion target'
                target
                @setvar savedtarget lasttarget
            endif

            drop
        else
            sysmsg 'Explosion potion is still on cooldown'
        endif
    else
        sysmsg 'No explosion potions found in your backpack'
    endif
endif
