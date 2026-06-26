/**
 * SpielerPlus Scraper - Generic team management data extractor
 * 
 * @example
 * const scraper = new SpielerPlusScraper({
 *   email: 'user@example.com',
 *   password: 'password'
 * });
 * await scraper.init();
 * const events = await scraper.getEvents();
 */

require('dotenv').config();

class SpielerPlusScraper {
  /**
   * @param {Object} config - Configuration
   * @param {string} config.email - SpielerPlus email
   * @param {string} config.password - SpielerPlus password
   * @param {string} [config.defaultTeam] - Default team name to select
   */
  constructor(config = {}) {
    this.email = config.email || process.env.SPIELERPLUS_EMAIL;
    this.password = config.password || process.env.SPIELERPLUS_PASSWORD;
    this.defaultTeam = config.defaultTeam || process.env.DEFAULT_TEAM;
    
    if (!this.email || !this.password) {
      throw new Error('Email and password required. Set SPIELERPLUS_EMAIL and SPIELERPLUS_PASSWORD environment variables or pass in config.');
    }
    
    this.browser = null;
    this.context = null;
    this.page = null;
    this.currentTeam = null;
  }

  /**
   * Initialize browser and login
   */
  async init() {
    const { chromium } = require('playwright');
    
    this.browser = await chromium.launch({ headless: true });
    this.context = await this.browser.newContext();
    this.page = await this.context.newPage();
    
    await this._login();
    
    // Auto-select default team if configured
    if (this.defaultTeam) {
      await this.selectTeam(this.defaultTeam);
    }
    
    return this;
  }

  /**
   * Login to SpielerPlus
   * @private
   */
  async _login() {
    await this.page.goto('https://www.spielerplus.de/', { waitUntil: 'networkidle' });
    await this._wait(1000);
    
    await this.page.click('a[href*="login"]');
    await this._wait(1500);
    
    await this.page.fill('input[type="email"]', this.email);
    await this.page.fill('input[type="password"]', this.password);
    await this.page.click('button[type="submit"]');
    await this._wait(5000);
    
    // Handle cookie consent
    await this.acceptCookies();
  }

  /**
   * Wait helper
   * @private
   */
  _wait(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  /**
   * Accept cookies if present
   */
  async acceptCookies() {
    const btn = await this.page.$('text=Okay - einverstanden');
    if (btn) {
      await btn.click();
      await this._wait(500);
    }
  }

  /**
   * Get all available teams
   * @returns {Promise<Array<{name: string, url: string}>>}
   */
  async getTeams() {
    await this.page.goto('https://www.spielerplus.de/de-li/site/select-team', { waitUntil: 'networkidle' });
    await this._wait(1500);
    await this.acceptCookies();
    
    return await this.page.evaluate(() => {
      const teams = [];
      const links = document.querySelectorAll('a[href*="team"], a[href*="select-team"]');
      
      links.forEach(link => {
        const text = link.textContent.trim();
        const href = link.getAttribute('href');
        
        // Filter for actual team links (not navigation items)
        if (text.length > 2 && text.length < 100 && 
            (text.includes('Humboldt') || text.includes('Männer') || 
             text.includes('Frauen') || text.includes('Herren') ||
             text.includes('Damen') || text.includes('Team ') || text.includes('Jugend'))) {
          teams.push({ name: text, url: href });
        }
      });
      
      // Deduplicate
      return [...new Map(teams.map(t => [t.name, t])).values()];
    });
  }

  /**
   * Select a team by name
   * @param {string} teamName - Team name (partial match works)
   */
  async selectTeam(teamName) {
    await this.page.goto('https://www.spielerplus.de/de-li/site/select-team', { waitUntil: 'networkidle' });
    await this._wait(1500);
    await this.acceptCookies();
    
    const teams = await this.getTeams();
    const targetTeam = teams.find(t => 
      t.name.toLowerCase().includes(teamName.toLowerCase()) ||
      teamName.toLowerCase().includes(t.name.toLowerCase().split(' ')[0])
    );
    
    if (!targetTeam) {
      throw new Error(`Team "${teamName}" not found. Available: ${teams.map(t => t.name).join(', ')}`);
    }
    
    await this.page.goto(`https://www.spielerplus.de${targetTeam.url}`, { waitUntil: 'networkidle' });
    await this._wait(2000);
    this.currentTeam = targetTeam.name;
    
    return targetTeam.name;
  }

  /**
   * Get upcoming events
   * @returns {Promise<Array>}
   */
  async getEvents() {
    await this.page.goto('https://www.spielerplus.de/de-li/site/events', { waitUntil: 'networkidle' });
    await this._wait(2000);
    await this.acceptCookies();
    
    return await this.page.evaluate(() => {
      const events = [];
      const lines = document.body.innerText.split('\n');
      
      for (let i = 0; i < lines.length; i++) {
        const line = lines[i].trim();
        if (/^(Mo|Di|Mi|Do|Fr|Sa|So)\.?/.test(line)) {
          events.push({
            date: line,
            time: lines[i+1]?.trim() || '',
            type: lines[i+2]?.trim() || '',
            meeting: lines[i+3]?.trim() || ''
          });
        }
      }
      return events;
    });
  }

  /**
   * Get event details including participants and carpool
   * @param {number} eventIndex - Index of event (0 = first)
   * @returns {Promise<Object>}
   */
  async getEventDetails(eventIndex = 0) {
    await this.page.goto('https://www.spielerplus.de/de-li/site/events', { waitUntil: 'networkidle' });
    await this._wait(2000);
    await this.acceptCookies();
    
    const eventCards = await this.page.$$('[class*="termin"], [class*="event"], [class*="termin-item"]');
    if (eventCards.length > eventIndex) {
      await eventCards[eventIndex].click();
      await this._wait(3000);
    }
    
    const participantBtn = await this.page.$('text=Teilnehmer');
    if (participantBtn) {
      await participantBtn.click();
      await this._wait(2000);
    }
    
    return await this.page.evaluate(() => {
      const text = document.body.innerText;
      const eventData = {
        date: '', type: '',
        time: { meeting: '', start: '', end: '' },
        status: '',
        participants: { yes: [], no: [], maybe: [] },
        carpool: []
      };
      
      const lines = text.split('\n');
      for (let i = 0; i < lines.length; i++) {
        const line = lines[i].trim();
        
        if (/^(Mo|Di|Mi|Do|Fr|Sa|So)\.?/.test(line)) {
          eventData.date = line;
          eventData.type = lines[i+2]?.trim() || '';
        }
        if (line === 'Treffen') eventData.time.meeting = lines[i+1]?.trim() || '';
        if (line === 'Beginn') eventData.time.start = lines[i+1]?.trim() || '';
        if (line === 'Ende') eventData.time.end = lines[i+1]?.trim() || '';
        if (line.includes('abgelaufen')) eventData.status = line;
      }
      
      return eventData;
    });
  }

  /**
   * Get team members
   * @returns {Promise<Array<string>>}
   */
  async getTeamMembers() {
    await this.page.goto('https://www.spielerplus.de/de-li/site/team', { waitUntil: 'networkidle' });
    await this._wait(2000);
    await this.acceptCookies();
    
    return await this.page.evaluate(() => {
      const members = [];
      const els = document.querySelectorAll('h1, h2, h3');
      
      els.forEach(el => {
        const text = el.textContent.trim();
        if (text.length > 2 && text.length < 100 && !text.includes('Team')) {
          members.push(text);
        }
      });
      
      return [...new Set(members)];
    });
  }

  /**
   * Get absences (vacation, sick leave, inactive)
   * @returns {Promise<Array>}
   */
  async getAbsences() {
    await this.page.goto('https://www.spielerplus.de/de-li/absence', { waitUntil: 'networkidle' });
    await this._wait(2000);
    await this.acceptCookies();
    
    return await this.page.evaluate(() => {
      const absences = [];
      const lines = document.body.innerText.split('\n');
      let current = null;
      
      for (const line of lines) {
        const trimmed = line.trim();
        if (!trimmed) continue;
        
        if (/^[A-Z][a-zäöüß].*?[A-Z]/.test(trimmed) && trimmed.length < 100) {
          if (current) absences.push(current);
          current = { name: trimmed, reason: '', period: '' };
        } else if (current && !current.reason && /Urlaub|Krank|Verletzt|Inaktiv|Sabatical/.test(trimmed)) {
          current.reason = trimmed;
        } else if (current && current.reason && !current.period && /\d{2}\.\d{2}/.test(trimmed)) {
          current.period = trimmed;
        }
      }
      if (current) absences.push(current);
      return absences;
    });
  }

  /**
   * Get team finances/cashbox
   * @returns {Promise<Object>}
   */
  async getFinances() {
    await this.page.goto('https://www.spielerplus.de/de-li/cashbox', { waitUntil: 'networkidle' });
    await this._wait(2000);
    await this.acceptCookies();
    
    return await this.page.evaluate(() => {
      const text = document.body.innerText;
      const balanceMatch = text.match(/EUR\s*([\d.,]+)/);
      const transactions = [];
      
      const lines = text.split('\n');
      for (let i = 0; i < lines.length; i++) {
        const line = lines[i].trim();
        if (line.includes('EUR') && line.includes('.') && line.match(/\d/)) {
          const amountMatch = line.match(/(-?EUR\s*[\d.,]+)/);
          const name = lines[i-1]?.trim() || '';
          const type = lines[i-2]?.trim() || '';
          if (amountMatch && name.length > 0 && name.length < 100) {
            transactions.push({ type, name, amount: amountMatch[1] });
          }
        }
      }
      
      return {
        balance: balanceMatch ? `EUR ${balanceMatch[1]}` : null,
        transactions: transactions.slice(0, 30)
      };
    });
  }

  /**
   * Get participation statistics
   * @returns {Promise<Object>}
   */
  async getParticipationStats() {
    await this.page.goto('https://www.spielerplus.de/de-li/participation', { waitUntil: 'networkidle' });
    await this._wait(2000);
    await this.acceptCookies();
    
    return await this.page.evaluate(() => {
      const text = document.body.innerText;
      const stats = [];
      
      const lines = text.split('\n');
      for (let i = 0; i < lines.length; i++) {
        const line = lines[i].trim();
        if (/^[A-Z][a-zäöüß].*?[A-Z]/.test(line) && line.length < 60) {
          const nextLine = lines[i+1]?.trim() || '';
          const match = nextLine.match(/(\d+)\s*\((\d+)%\)/);
          if (match) {
            stats.push({ name: line, count: parseInt(match[1]), percentage: parseInt(match[2]) });
          }
        }
      }
      
      const summaryMatch = text.match(/(\d+)\s*Termine.*?(\d+)\s*Trainings.*?(\d+)\s*Spiele/);
      
      return {
        summary: summaryMatch ? {
          total: parseInt(summaryMatch[1]),
          trainings: parseInt(summaryMatch[2]),
          games: parseInt(summaryMatch[3])
        } : null,
        players: stats.sort((a, b) => b.percentage - a.percentage)
      };
    });
  }

  /**
   * Get team profile info
   * @returns {Promise<Object>}
   */
  async getTeamProfile() {
    await this.page.goto('https://www.spielerplus.de/de-li/site/team', { waitUntil: 'networkidle' });
    await this._wait(1500);
    await this.acceptCookies();
    
    const teamLink = await this.page.$('a[href*="team/view"]');
    const href = await teamLink?.getAttribute('href');
    const teamId = href ? new URL(href, 'https://example.com').searchParams.get('id') : null;
    
    if (teamId) {
      await this.page.goto(`https://www.spielerplus.de/de-li/team/view?id=${teamId}`, { waitUntil: 'networkidle' });
      await this._wait(2000);
    }
    
    return await this.page.evaluate(() => {
      const text = document.body.innerText;
      const data = { 
        name: '', 
        sport: '', 
        address: '', 
        teamType: '', 
        website: '', 
        gameReports: [] 
      };
      
      const h1 = document.querySelector('h1');
      if (h1) data.name = h1.textContent.trim();
      
      const lines = text.split('\n');
      for (let i = 0; i < lines.length; i++) {
        const line = lines[i].trim();
        
        if (line.includes('Handball')) data.sport = 'Handball';
        if (line.includes('Herren') || line.includes('Männer')) data.teamType = 'Herren';
        if (line.includes('Frauen')) data.teamType = 'Frauen';
        if (line.match(/\d{5}.*Berlin/)) data.address = line;
        if (line.includes('http')) data.website = line;
        
        if (line === 'Spielberichte') {
          const games = [];
          for (let j = i+1; j < i+10 && j < lines.length; j++) {
            const gameLine = lines[j].trim();
            if (gameLine.match(/\d{2}\.\d{2}\.\d{2}/)) {
              games.push(gameLine);
            }
          }
          if (games.length > 0) data.gameReports = games;
        }
      }
      return data;
    });
  }

  /**
   * Get team roles
   * @returns {Promise<Array>}
   */
  async getRoles() {
    await this.page.goto('https://www.spielerplus.de/de-li/role', { waitUntil: 'networkidle' });
    await this._wait(2000);
    await this.acceptCookies();
    
    return await this.page.evaluate(() => {
      const roles = [];
      const lines = document.body.innerText.split('\n');
      
      for (let i = 0; i < lines.length; i++) {
        const line = lines[i].trim();
        if (line.match(/^\d+\s*Berechtigung/)) {
          const roleName = lines[i-2]?.trim() || '';
          const permMatch = line.match(/(\d+)\s*Berechtigung/);
          if (roleName && permMatch && roleName.length < 50) {
            roles.push({ name: roleName, permissions: parseInt(permMatch[1]) });
          }
        }
      }
      return roles;
    });
  }

  /**
   * Get benefits/deals
   * @returns {Promise<Object>}
   */
  async getBenefits() {
    await this.page.goto('https://www.spielerplus.de/de-li/a/appstauber', { waitUntil: 'networkidle' });
    await this._wait(2000);
    await this.acceptCookies();
    
    return await this.page.evaluate(() => {
      const text = document.body.innerText;
      const match = text.match(/(\d+)\s*aktive Deals/);
      return { activeDeals: match ? parseInt(match[1]) : 0 };
    });
  }

  /**
   * Close browser
   */
  async close() {
    if (this.browser) {
      await this.browser.close();
    }
  }
}

module.exports = SpielerPlusScraper;
