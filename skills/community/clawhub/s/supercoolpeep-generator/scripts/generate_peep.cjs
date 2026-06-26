const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');

(async () => {
    const args = process.argv.slice(2);
    let seed = args[0];
    const type = args[1]; // optional: 'ape', 'skeleton', 'zombie'

    // Generate random 68-digit seed if not provided
    if (!seed) {
        seed = "";
        for (let i = 0; i < 68; i++) {
            seed += Math.floor(Math.random() * 10).toString();
        }
        
        // Force traits if type requested
        let traitDigits = "";
        if (type === 'ape') traitDigits = (92 + Math.floor(Math.random() * 5)).toString();
        else if (type === 'zombie') traitDigits = (97 + Math.floor(Math.random() * 2)).toString();
        else if (type === 'skeleton') traitDigits = "99";

        if (traitDigits) {
            seed = seed.substring(0, 2) + traitDigits + seed.substring(4);
        }
    }

    const browser = await puppeteer.launch({
        headless: "new",
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });

    const page = await browser.newPage();
    await page.setViewport({ width: 1000, height: 1000 });

    const url = `https://supercoolpeeps.com/app.html?s=${seed}`;
    console.log(`Generating Peep from seed: ${seed}`);
    
    await page.goto(url, { waitUntil: 'networkidle2' });

    // Wait for p5.js canvas to breathe
    await new Promise(r => setTimeout(r, 2000));

    const outputPath = path.join(process.cwd(), `peep_${Date.now()}.png`);
    
    // Select the canvas and screenshot it specifically
    const canvas = await page.$('canvas');
    if (canvas) {
        await canvas.screenshot({ path: outputPath });
        console.log(`SUCCESS:${outputPath}`);
    } else {
        console.error('Canvas not found');
        process.exit(1);
    }

    await browser.close();
})();
