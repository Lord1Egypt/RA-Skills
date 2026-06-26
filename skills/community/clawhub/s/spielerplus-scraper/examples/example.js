/**
 * Example: Using SpielerPlus Scraper as a library
 */

const SpielerPlusScraper = require('../src/index.js');

async function main() {
  // Initialize with config
  const scraper = new SpielerPlusScraper({
    email: process.env.SPIELERPLUS_EMAIL,
    password: process.env.SPIELERPLUS_PASSWORD,
    defaultTeam: 'Männer' // Optional: auto-select team
  });

  try {
    await scraper.init();

    // Get teams
    const teams = await scraper.getTeams();
    console.log('Teams:', teams);

    // Select specific team
    await scraper.selectTeam('Herren');

    // Get data
    const events = await scraper.getEvents();
    const members = await scraper.getTeamMembers();
    const absences = await scraper.getAbsences();
    const finances = await scraper.getFinances();
    const participation = await scraper.getParticipationStats();
    const profile = await scraper.getTeamProfile();
    const roles = await scraper.getRoles();

    // Output results
    console.log('\n=== Team Profile ===');
    console.log(profile);

    console.log('\n=== Upcoming Events ===');
    console.log(events);

    console.log('\n=== Participation Stats ===');
    console.log(participation);

    console.log('\n=== Finances ===');
    console.log(finances);

  } catch (error) {
    console.error('Error:', error.message);
  } finally {
    await scraper.close();
  }
}

main();
