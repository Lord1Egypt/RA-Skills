// VAM Scripter Example: Multiple Atoms Loop
// Iterates through all atoms and performs operations

import { scripter, scene } from "vam-scripter";

// Get a reference atom
const referenceAtom = scene.getAtom("Reference");

// Store all other atoms for processing
let otherAtoms = [];

// Initialize on enable
scripter.onEnable(() => {
    // Store all non-reference atoms
    const allAtoms = scene.getAtoms();
    otherAtoms = allAtoms.filter(atom => atom.name !== referenceAtom.name);
    console.log(`Tracking ${otherAtoms.length} atoms`);
});

// Process every frame
scripter.onUpdate(() => {
    // Find closest atom
    let closestAtom = null;
    let closestDistance = Infinity;
    
    for (const atom of otherAtoms) {
        const distance = atom.distance(referenceAtom);
        
        if (distance < closestDistance) {
            closestDistance = distance;
            closestAtom = atom;
        }
        
        // Log distance to reference
        if (distance < 3.0) {
            console.log(`${atom.name} is ${distance.toFixed(2)}m away`);
        }
    }
    
    // Update reference atom with closest info
    if (closestAtom) {
        console.log(`Closest: ${closestAtom.name} at ${closestDistance.toFixed(2)}m`);
    }
});