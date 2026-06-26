#!/usr/bin/env node

/**
 * Traffic Intelligence Module
 * Real-time traffic monitoring for J's commute
 * 
 * Features:
 * - Real-time traffic flow data
 * - Route calculation with traffic
 * - Dynamic departure time recommendations
 * - Congestion alerts
 */

const fs = require('fs');
const path = require('path');

// Configuration
const CONFIG = {
  apiKey: process.env.TOMTOM_API_KEY,
  
  // Default locations (Seattle area)
  locations: {
    home: { lat: 47.6062, lon: -122.3321, name: 'Seattle' },
    work: { lat: 47.6101, lon: -122.2015, name: 'Bellevue' },
    coffee: { lat: 47.6132, lon: -122.1899, name: 'Bellevue Coffee Shop' }
  },
  
  // Buffer times (minutes)
  buffers: {
    parking: 5,
    coffeeOrder: 3,
    meetingBuffer: 15
  },
  
  // API endpoints
  endpoints: {
    flow: 'https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json',
    route: 'https://api.tomtom.com/routing/1/calculateRoute'
  }
};

class TrafficIntelligence {
  constructor(apiKey) {
    this.apiKey = apiKey;
    if (!apiKey) {
      throw new Error('TOMTOM_API_KEY environment variable not set');
    }
  }

  /**
   * Get traffic flow data for a specific location
   */
  async getTrafficFlow(lat, lon) {
    const url = `${CONFIG.endpoints.flow}?point=${lat},${lon}&key=${this.apiKey}`;
    
    try {
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`API error: ${response.status} ${response.statusText}`);
      }
      return await response.json();
    } catch (error) {
      console.error(`Traffic flow error: ${error.message}`);
      return null;
    }
  }

  /**
   * Calculate route with real-time traffic
   */
  async calculateRoute(origin, destination, options = {}) {
    const { lat: lat1, lon: lon1 } = origin;
    const { lat: lat2, lon: lon2 } = destination;
    
    const params = new URLSearchParams({
      key: this.apiKey,
      traffic: 'true',
      routeType: options.routeType || 'fastest',
      travelMode: options.travelMode || 'car',
      avoid: options.avoid || '',
      vehicleMaxSpeed: options.maxSpeed || '',
      vehicleWeight: options.weight || ''
    });
    
    const url = `${CONFIG.endpoints.route}/${lat1},${lon1}:${lat2},${lon2}/json?${params}`;
    
    try {
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`API error: ${response.status} ${response.statusText}`);
      }
      const data = await response.json();
      
      if (!data.routes || data.routes.length === 0) {
        throw new Error('No route found');
      }
      
      return this.formatRouteData(data.routes[0], origin, destination);
    } catch (error) {
      console.error(`Route calculation error: ${error.message}`);
      return null;
    }
  }

  /**
   * Format route data into usable format
   */
  formatRouteData(route, origin, destination) {
    const summary = route.summary;
    const legs = route.legs || [];
    
    // Calculate congestion segments
    const congestion = this.analyzeCongestion(legs);
    
    return {
      origin: origin.name || 'Origin',
      destination: destination.name || 'Destination',
      distanceMiles: (summary.lengthInMeters / 1609.34).toFixed(1),
      baseTimeMinutes: Math.floor(summary.travelTimeInSeconds / 60),
      trafficDelayMinutes: Math.floor(summary.trafficDelayInSeconds / 60),
      totalTimeMinutes: Math.floor((summary.travelTimeInSeconds + summary.trafficDelayInSeconds) / 60),
      departureTime: new Date().toISOString(),
      congestion: congestion,
      routeSummary: {
        hasTolls: summary.hasTollRoad || false,
        hasFerry: summary.hasFerry || false,
        hasUnpaved: summary.hasUnpaved || false,
        hasSeasonalClosure: summary.hasSeasonalClosure || false
      }
    };
  }

  /**
   * Analyze congestion in route legs
   */
  analyzeCongestion(legs) {
    if (!legs || legs.length === 0) return [];
    
    const congestion = [];
    legs.forEach((leg, index) => {
      if (leg.points && leg.points.length > 0) {
        const points = leg.points;
        points.forEach(point => {
          if (point.speed && point.speed < 20) { // Less than 20 mph = congestion
            congestion.push({
              segment: index + 1,
              location: { lat: point.latitude, lon: point.longitude },
              speedMph: (point.speed * 0.621371).toFixed(1),
              delayMinutes: point.delay ? Math.floor(point.delay / 60) : 0
            });
          }
        });
      }
    });
    
    return congestion.slice(0, 3); // Return top 3 congestion points
  }

  /**
   * Calculate optimal departure time for a meeting
   */
  calculateDepartureTime(meetingTime, travelTimeMinutes, buffers = {}) {
    const meetingDate = new Date(meetingTime);
    const totalBuffer = 
      (buffers.parking || CONFIG.buffers.parking) +
      (buffers.coffeeOrder || CONFIG.buffers.coffeeOrder) +
      (buffers.meetingBuffer || CONFIG.buffers.meetingBuffer);
    
    const totalMinutesNeeded = travelTimeMinutes + totalBuffer;
    
    const departureDate = new Date(meetingDate.getTime() - (totalMinutesNeeded * 60000));
    
    return {
      meetingTime: meetingDate.toLocaleTimeString('en-US', { 
        hour: 'numeric', 
        minute: '2-digit',
        timeZone: 'America/Los_Angeles'
      }),
      departureTime: departureDate.toLocaleTimeString('en-US', { 
        hour: 'numeric', 
        minute: '2-digit',
        timeZone: 'America/Los_Angeles'
      }),
      travelTimeMinutes,
      bufferMinutes: totalBuffer,
      totalMinutesNeeded,
      isUrgent: totalMinutesNeeded > 60 // More than 1 hour = plan ahead
    };
  }

  /**
   * Generate traffic alert message
   */
  generateAlert(routeData, meetingInfo = null) {
    let message = `🚗 **TRAFFIC INTELLIGENCE**\n\n`;
    message += `**Route:** ${routeData.origin} → ${routeData.destination}\n`;
    message += `**Distance:** ${routeData.distanceMiles} miles\n`;
    message += `**Current Travel Time:** ${routeData.totalTimeMinutes} minutes\n`;
    message += `**Traffic Delay:** ${routeData.trafficDelayMinutes} minutes\n`;
    
    if (routeData.congestion.length > 0) {
      message += `\n**⚠️ CONGESTION ALERTS:**\n`;
      routeData.congestion.forEach((cong, i) => {
        message += `${i + 1}. Segment ${cong.segment}: ${cong.speedMph} mph (${cong.delayMinutes} min delay)\n`;
      });
    }
    
    if (meetingInfo) {
      message += `\n**📅 MEETING PLANNING:**\n`;
      message += `Meeting at: ${meetingInfo.meetingTime}\n`;
      message += `Depart by: ${meetingInfo.departureTime}\n`;
      message += `Total buffer: ${meetingInfo.bufferMinutes} minutes\n`;
      
      if (meetingInfo.isUrgent) {
        message += `\n**🔴 URGENT:** Plan extra time for this trip\n`;
      }
    }
    
    message += `\n_Data source: TomTom Traffic API • Updated: ${new Date().toLocaleTimeString()}_`;
    
    return message;
  }
}

/**
 * Main function for CLI usage
 */
async function main() {
  const args = process.argv.slice(2);
  const command = args[0] || 'check';
  
  const apiKey = process.env.TOMTOM_API_KEY;
  if (!apiKey) {
    console.error('❌ Error: TOMTOM_API_KEY environment variable not set');
    console.error('Set it with: export TOMTOM_API_KEY="your_key_here"');
    process.exit(1);
  }
  
  const traffic = new TrafficIntelligence(apiKey);
  
  switch (command) {
    case 'check':
      // Check home → work commute
      const route = await traffic.calculateRoute(
        CONFIG.locations.home,
        CONFIG.locations.work
      );
      
      if (route) {
        console.log(traffic.generateAlert(route));
      } else {
        console.error('❌ Failed to get traffic data');
      }
      break;
      
    case 'meeting':
      // Calculate for a specific meeting time
      const meetingTime = args[1];
      if (!meetingTime) {
        console.error('❌ Usage: node traffic-check.js meeting "HH:MM"');
        process.exit(1);
      }
      
      const today = new Date();
      const [hours, minutes] = meetingTime.split(':');
      const meetingDate = new Date(today.getFullYear(), today.getMonth(), today.getDate(), hours, minutes);
      
      const route2 = await traffic.calculateRoute(
        CONFIG.locations.home,
        CONFIG.locations.coffee
      );
      
      if (route2) {
        const meetingInfo = traffic.calculateDepartureTime(
          meetingDate,
          route2.totalTimeMinutes,
          { meetingBuffer: 10 } // 10 minutes buffer for coffee meeting
        );
        
        console.log(traffic.generateAlert(route2, meetingInfo));
      }
      break;
      
    case 'test':
      // Test API connectivity
      const flow = await traffic.getTrafficFlow(
        CONFIG.locations.home.lat,
        CONFIG.locations.home.lon
      );
      
      if (flow) {
        console.log('✅ API Connection: ACTIVE');
        console.log(`Current Speed: ${flow.flowSegmentData?.currentSpeed || 'N/A'} km/h`);
      } else {
        console.log('❌ API Connection: FAILED');
      }
      break;
      
    default:
      console.log('Usage:');
      console.log('  node traffic-check.js check          - Check current commute');
      console.log('  node traffic-check.js meeting HH:MM  - Plan departure for meeting');
      console.log('  node traffic-check.js test           - Test API connection');
      break;
  }
}

// Run if called directly
if (require.main === module) {
  main().catch(console.error);
}

module.exports = TrafficIntelligence;