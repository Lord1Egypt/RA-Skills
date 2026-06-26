#!/usr/bin/env node

/**
 * Validate .openclaw-skills.json Configuration
 * 
 * Validates the structure and content of the skills configuration file.
 */

const fs = require('fs');
const path = require('path');

const CONFIG_FILE = '.openclaw-skills.json';

// Schema definition
const SCHEMA = {
  required: [],
  optional: {
    name: 'string',
    skills: 'array',
    excludeGlobal: 'boolean',
    sources: 'array',
    cache: 'object',
    autoSync: 'object'
  },
  nested: {
    'skills[]': {
      required: [],
      optional: {
        name: 'string',
        version: 'string'
      },
      allowString: true
    },
    'sources[]': {
      required: ['name', 'type'],
      optional: {
        priority: 'number',
        enabled: 'boolean',
        api: 'string',
        paths: 'array',
        repos: 'array',
        branch: 'string',
        baseUrl: 'string',
        format: 'string',
        host: 'string',
        port: 'number',
        path: 'string',
        auth: 'object'
      }
    },
    'cache': {
      required: [],
      optional: {
        enabled: 'boolean',
        ttlHours: 'number'
      }
    },
    'autoSync': {
      required: [],
      optional: {
        onProjectEnter: 'boolean',
        onSkillMissing: 'boolean'
      }
    }
  }
};

// Valid source types
const VALID_SOURCE_TYPES = ['registry', 'filesystem', 'git', 'url', 'network'];

// Validate type
function validateType(value, expectedType, fieldPath) {
  const errors = [];
  
  const typeMap = {
    'string': (v) => typeof v === 'string',
    'number': (v) => typeof v === 'number',
    'boolean': (v) => typeof v === 'boolean',
    'array': (v) => Array.isArray(v),
    'object': (v) => typeof v === 'object' && v !== null && !Array.isArray(v)
  };
  
  if (!typeMap[expectedType](value)) {
    errors.push(`${fieldPath}: expected ${expectedType}, got ${typeof value}`);
  }
  
  return errors;
}

// Validate object against schema
function validateObject(obj, schema, parentPath = '') {
  const errors = [];
  
  if (typeof obj !== 'object' || obj === null || Array.isArray(obj)) {
    errors.push(`${parentPath || 'root'}: expected object`);
    return errors;
  }
  
  // Check optional fields
  for (const [field, type] of Object.entries(schema.optional || {})) {
    if (field in obj) {
      const fieldPath = parentPath ? `${parentPath}.${field}` : field;
      errors.push(...validateType(obj[field], type, fieldPath));
    }
  }
  
  return errors;
}

// Main validation
function validate(configPath) {
  console.log(`🔍 Validating: ${configPath}\n`);
  
  // Read file
  let content;
  try {
    content = fs.readFileSync(configPath, 'utf8');
  } catch (err) {
    console.error(`❌ Cannot read file: ${err.message}`);
    return false;
  }
  
  // Parse JSON
  let config;
  try {
    config = JSON.parse(content);
  } catch (err) {
    console.error(`❌ Invalid JSON: ${err.message}`);
    console.error(`   Line: ${err.lineNumber || '?'}`);
    return false;
  }
  
  const errors = [];
  const warnings = [];
  
  // Validate root object
  errors.push(...validateObject(config, SCHEMA));
  
  // Validate skills array
  if (config.skills) {
    if (!Array.isArray(config.skills)) {
      errors.push('skills: must be an array');
    } else {
      config.skills.forEach((skill, index) => {
        const skillPath = `skills[${index}]`;
        
        if (typeof skill === 'string') {
          // Simple string format is allowed
          if (!skill.trim()) {
            errors.push(`${skillPath}: skill name cannot be empty`);
          }
        } else if (typeof skill === 'object') {
          if (!skill.name) {
            errors.push(`${skillPath}: missing required field "name"`);
          }
          if (skill.version && typeof skill.version !== 'string') {
            errors.push(`${skillPath}.version: must be a string`);
          }
        } else {
          errors.push(`${skillPath}: must be string or object`);
        }
      });
      
      // Check for duplicates
      const skillNames = config.skills.map(s => typeof s === 'string' ? s : s.name);
      const duplicates = skillNames.filter((name, i) => skillNames.indexOf(name) !== i);
      if (duplicates.length > 0) {
        warnings.push(`skills: duplicate entries found: ${[...new Set(duplicates)].join(', ')}`);
      }
    }
  }
  
  // Validate sources array
  if (config.sources) {
    if (!Array.isArray(config.sources)) {
      errors.push('sources: must be an array');
    } else {
      config.sources.forEach((source, index) => {
        const sourcePath = `sources[${index}]`;
        
        if (!source.name) {
          errors.push(`${sourcePath}: missing required field "name"`);
        }
        
        if (!source.type) {
          errors.push(`${sourcePath}: missing required field "type"`);
        } else if (!VALID_SOURCE_TYPES.includes(source.type)) {
          errors.push(`${sourcePath}.type: must be one of ${VALID_SOURCE_TYPES.join(', ')}`);
        }
        
        // Type-specific validation
        if (source.type === 'filesystem' && !source.paths) {
          errors.push(`${sourcePath}: filesystem source requires "paths" array`);
        }
        
        if (source.type === 'git' && !source.repos) {
          errors.push(`${sourcePath}: git source requires "repos" array`);
        }
        
        if (source.type === 'url' && !source.baseUrl) {
          errors.push(`${sourcePath}: url source requires "baseUrl"`);
        }
        
        if (source.type === 'network' && (!source.host || !source.port)) {
          errors.push(`${sourcePath}: network source requires "host" and "port"`);
        }
        
        if (source.priority !== undefined && typeof source.priority !== 'number') {
          errors.push(`${sourcePath}.priority: must be a number`);
        }
        
        if (source.enabled !== undefined && typeof source.enabled !== 'boolean') {
          errors.push(`${sourcePath}.enabled: must be a boolean`);
        }
      });
      
      // Check priority uniqueness (warning only)
      const priorities = config.sources.filter(s => s.priority !== undefined).map(s => s.priority);
      const uniquePriorities = new Set(priorities);
      if (priorities.length !== uniquePriorities.size) {
        warnings.push('sources: duplicate priority values found (first match will be used)');
      }
    }
  }
  
  // Validate cache object
  if (config.cache) {
    if (typeof config.cache !== 'object') {
      errors.push('cache: must be an object');
    } else {
      if (config.cache.enabled !== undefined && typeof config.cache.enabled !== 'boolean') {
        errors.push('cache.enabled: must be a boolean');
      }
      if (config.cache.ttlHours !== undefined && typeof config.cache.ttlHours !== 'number') {
        errors.push('cache.ttlHours: must be a number');
      }
    }
  }
  
  // Validate autoSync object
  if (config.autoSync) {
    if (typeof config.autoSync !== 'object') {
      errors.push('autoSync: must be an object');
    } else {
      if (config.autoSync.onProjectEnter !== undefined && typeof config.autoSync.onProjectEnter !== 'boolean') {
        errors.push('autoSync.onProjectEnter: must be a boolean');
      }
      if (config.autoSync.onSkillMissing !== undefined && typeof config.autoSync.onSkillMissing !== 'boolean') {
        errors.push('autoSync.onSkillMissing: must be a boolean');
      }
    }
  }
  
  // Report results
  if (errors.length === 0 && warnings.length === 0) {
    console.log('✅ Configuration is valid!');
    return true;
  }
  
  if (warnings.length > 0) {
    console.log('⚠️  Warnings:');
    warnings.forEach(w => console.log(`   - ${w}`));
    console.log();
  }
  
  if (errors.length > 0) {
    console.log('❌ Errors:');
    errors.forEach(e => console.log(`   - ${e}`));
    console.log();
    console.log('📖 Example config:');
    console.log(JSON.stringify({
      name: "my-project",
      skills: [
        { name: "feishu-doc", version: "latest" },
        "weather"
      ],
      excludeGlobal: true,
      sources: [
        { name: "clawhub", type: "registry", priority: 1 },
        { name: "local", type: "filesystem", paths: ["~/.openclaw/skills"] }
      ],
      cache: { enabled: true, ttlHours: 24 },
      autoSync: { onProjectEnter: true, onSkillMissing: true }
    }, null, 2));
    return false;
  }
  
  console.log('✅ Configuration is valid with warnings.');
  return true;
}

// CLI
const configPath = process.argv[2] || path.join(process.cwd(), CONFIG_FILE);

if (!fs.existsSync(configPath)) {
  console.error(`❌ File not found: ${configPath}`);
  process.exit(1);
}

const valid = validate(configPath);
process.exit(valid ? 0 : 1);
