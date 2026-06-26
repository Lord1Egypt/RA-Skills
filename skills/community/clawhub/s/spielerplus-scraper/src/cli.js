#!/usr/bin/env node

/**
 * SpielerPlus Scraper CLI
 * 
 * Usage: node cli.js <command> [team] [options]
 */

const SpielerPlusScraper = require('./index.js');

// Parse arguments
const args = process.argv.slice(2);
const command = args[0] || 'help';
const teamArg = args[1];
const options = args.slice(2);

// Check for help
if (command === 'help' || command === '--help' || command === '-h') {
  console.log(`
SpielerPlus Scraper CLI

Usage: node cli.js <command> [team] [options]

Commands:
  teams         List all teams
  events        List upcoming events
  event [n]     Event details (index, default: 0)
  team          Team members
  absences      Absences (vacation, sick, inactive)
  finances      Team finances
  participation Participation statistics
  profile       Team profile
  roles         Roles & permissions
  benefits      Benefits & deals
  all           Full report for all teams

Options:
  -h, --help    Show this help
  -j, --json    Output as JSON
  -t, --team    Team name

Examples:
  node cli.js teams
  node cli.js events "Männer"
  node cli.js finances --json
  node cli.js event 0 "Herren"
`);
  process.exit(0);
}

// Check for JSON output flag
const outputJson = options.includes('--json') || options.includes('-j');

// Load config from environment
const config = {
  email: process.env.SPIELERPLUS_EMAIL,
  password: process.env.SPIELERPLUS_PASSWORD,
  defaultTeam: teamArg || process.env.DEFAULT_TEAM
};

if (!config.email || !config.password) {
  console.error('Error: SPIELERPLUS_EMAIL and SPIELERPLUS_PASSWORD environment variables required.');
  console.error('Create a .env file or export the variables.');
  console.error('');
  console.error('Example .env file:');
  console.error('  SPIELERPLUS_EMAIL=your@email.com');
  console.error('  SPIELERPLUS_PASSWORD=yourpassword');
  process.exit(1);
}

async function main() {
  let scraper;
  
  try {
    scraper = new SpielerPlusScraper(config);
    await scraper.init();
    
    // Handle teams command specially (no team selection needed)
    if (command === 'teams') {
      const teams = await scraper.getTeams();
      if (outputJson) {
        console.log(JSON.stringify(teams, null, 2));
      } else {
        console.log('\n📋 Available Teams:');
        teams.forEach((t, i) => console.log(`  ${i+1}. ${t.name}`));
      }
      return;
    }
    
    // Select team if specified
    if (teamArg) {
      await scraper.selectTeam(teamArg);
    }
    
    let result;
    
    switch (command) {
      case 'events':
        result = await scraper.getEvents();
        if (outputJson) {
          console.log(JSON.stringify(result, null, 2));
        } else {
          console.log('\n📅 Upcoming Events:');
          if (result.length === 0) {
            console.log('  No events found');
          } else {
            result.forEach(e => {
              console.log(`  ${e.date} | ${e.time} | ${e.type}`);
              if (e.meeting) console.log(`    Treffen: ${e.meeting}`);
            });
          }
        }
        break;
        
      case 'event':
        const idx = parseInt(options[0]) || 0;
        result = await scraper.getEventDetails(idx);
        if (outputJson) {
          console.log(JSON.stringify(result, null, 2));
        } else {
          console.log(`\n🎯 Event Details (Index: ${idx}):`);
          console.log(`  Date: ${result.date}`);
          console.log(`  Type: ${result.type}`);
          console.log(`  Time: ${result.time.meeting} - ${result.time.start} to ${result.time.end}`);
          console.log(`  Status: ${result.status || 'Active'}`);
        }
        break;
        
      case 'team':
        result = await scraper.getTeamMembers();
        if (outputJson) {
          console.log(JSON.stringify(result, null, 2));
        } else {
          console.log('\n👥 Team Members:');
          result.forEach(m => console.log(`  - ${m}`));
          console.log(`\n  Total: ${result.length} members`);
        }
        break;
        
      case 'absences':
        result = await scraper.getAbsences();
        if (outputJson) {
          console.log(JSON.stringify(result, null, 2));
        } else {
          console.log('\n🏥 Absences:');
          if (result.length === 0) {
            console.log('  No absences');
          } else {
            result.forEach(a => {
              console.log(`  - ${a.name}`);
              if (a.reason) console.log(`    ${a.reason}`);
              if (a.period) console.log(`    ${a.period}`);
            });
          }
        }
        break;
        
      case 'finances':
        result = await scraper.getFinances();
        if (outputJson) {
          console.log(JSON.stringify(result, null, 2));
        } else {
          console.log('\n💰 Team Finances:');
          console.log(`  Balance: ${result.balance || 'N/A'}`);
          if (result.transactions && result.transactions.length > 0) {
            console.log('  Recent Transactions:');
            result.transactions.slice(0, 10).forEach(t => {
              console.log(`    ${t.name} | ${t.type} | ${t.amount}`);
            });
          }
        }
        break;
        
      case 'participation':
        result = await scraper.getParticipationStats();
        if (outputJson) {
          console.log(JSON.stringify(result, null, 2));
        } else {
          console.log('\n📊 Participation Statistics:');
          if (result.summary) {
            console.log(`  Total: ${result.summary.total} events (${result.summary.trainings} trainings, ${result.summary.games} games)`);
          }
          if (result.players && result.players.length > 0) {
            console.log('  Top Attendees:');
            result.players.slice(0, 10).forEach(p => {
              console.log(`    ${p.name}: ${p.count} (${p.percentage}%)`);
            });
          }
        }
        break;
        
      case 'profile':
        result = await scraper.getTeamProfile();
        if (outputJson) {
          console.log(JSON.stringify(result, null, 2));
        } else {
          console.log('\n🏠 Team Profile:');
          console.log(`  Name: ${result.name}`);
          console.log(`  Sport: ${result.sport || 'N/A'}`);
          console.log(`  Type: ${result.teamType || 'N/A'}`);
          console.log(`  Address: ${result.address || 'N/A'}`);
          console.log(`  Website: ${result.website || 'N/A'}`);
        }
        break;
        
      case 'roles':
        result = await scraper.getRoles();
        if (outputJson) {
          console.log(JSON.stringify(result, null, 2));
        } else {
          console.log('\n👔 Roles & Permissions:');
          if (result.length === 0) {
            console.log('  No roles found');
          } else {
            result.forEach(r => {
              console.log(`  - ${r.name}: ${r.permissions} permissions`);
            });
          }
        }
        break;
        
      case 'benefits':
        result = await scraper.getBenefits();
        if (outputJson) {
          console.log(JSON.stringify(result, null, 2));
        } else {
          console.log('\n🎁 Benefits:');
          console.log(`  Active Deals: ${result.activeDeals}`);
        }
        break;
        
      case 'all':
        const teams = await scraper.getTeams();
        for (const team of teams) {
          console.log(`\n${'='.repeat(50)}`);
          console.log(`📋 ${team.name}`);
          console.log('='.repeat(50));
          
          await scraper.selectTeam(team.name);
          
          const profile = await scraper.getTeamProfile();
          console.log(`Sport: ${profile.sport || 'N/A'} | Type: ${profile.teamType || 'N/A'}`);
          
          const events = await scraper.getEvents();
          console.log(`Events: ${events.length} upcoming`);
          
          const members = await scraper.getTeamMembers();
          console.log(`Members: ${members.length}`);
          
          const finances = await scraper.getFinances();
          console.log(`Balance: ${finances.balance || 'N/A'}`);
          
          const participation = await scraper.getParticipationStats();
          if (participation.summary) {
            console.log(`Participation: ${participation.summary.total} events`);
          }
        }
        break;
        
      default:
        console.log(`Unknown command: ${command}`);
        console.log('Run "node cli.js help" for usage information');
    }
    
  } catch (error) {
    console.error('Error:', error.message);
    process.exit(1);
  } finally {
    if (scraper) {
      await scraper.close();
    }
  }
}

main();
