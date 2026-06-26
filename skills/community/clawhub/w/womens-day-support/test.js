// Test script for Women's Day Support skill
const fs = require('fs');
const path = require('path');

// Load the main skill module
const skillModule = require('./womens-day-support.js');

// Create a mock context for testing
const mockContext = {
  reply: (message) => {
    console.log('Skill would reply with:', message);
  },
  tools: {
    web_search: async (query) => {
      // Mock search results
      return [
        { title: 'Mock Resource 1', url: 'https://example.com/1', snippet: 'Helpful resource for women' },
        { title: 'Mock Resource 2', url: 'https://example.com/2', snippet: 'Support service for women' }
      ];
    }
  }
};

async function testSkill() {
  console.log('Testing Women\'s Day Support Skill...\n');
  
  // Test different commands
  const testCommands = [
    'women resources',
    'women support',
    'women help',
    'women day'
  ];
  
  for (const command of testCommands) {
    console.log(`\n--- Testing command: "${command}" ---`);
    try {
      await skillModule.handleCommand(command, mockContext);
    } catch (error) {
      console.error('Error during test:', error.message);
    }
  }
  
  console.log('\nTest completed!');
}

// Run the test if this file is executed directly
if (require.main === module) {
  testSkill().catch(console.error);
}