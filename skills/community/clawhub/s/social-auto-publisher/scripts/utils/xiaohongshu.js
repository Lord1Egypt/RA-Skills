/**
 * Xiaohongshu Browser Automation Publishing Module
 * Dependency: Logged-in browser environment (host mode)
 */
const path = require('path');
const fs = require('fs');

const CREATOR_URL = 'https://creator.xiaohongshu.com/publish/publish';

/**
 * Format Xiaohongshu content (title <= 20 characters, body <= 1000 characters)
 */
function formatContent(content) {
  const title = content.title.slice(0, 20);
  const body = content.body.slice(0, 1000);
  const tags = (content.tags || []).map(t => `#${t.replace(/^#/, '')}`).join(' ');
  return { title, body, tags };
}

/**
 * Generate a sequence of Xiaohongshu publishing commands
 * Returns an array of browser act commands for external AI execution
 */
function buildPublishCommands(content) {
  const { title, body, tags } = formatContent(content);

  return [
    {
      step: 1,
      action: 'navigate',
      description: 'Open the publishing page',
      command: `browser navigate ${CREATOR_URL}`,
    },
    {
      step: 2,
      action: 'screenshot',
      description: 'Check login status',
      command: 'browser screenshot',
    },
    {
      step: 3,
      action: 'click',
      description: 'Click to upload image-text post',
      command: 'browser act ref=<upload-image-text-button> kind=click',
    },
    {
      step: 4,
      action: 'type',
      description: 'Fill in the title',
      command: `browser act ref=<title-input> kind=type text="${title}"`,
      value: title,
    },
    {
      step: 5,
      action: 'type',
      description: 'Fill in the body',
      command: `browser act ref=<body-input> kind=type text="${body.slice(0, 200)}..."`,
      value: body,
    },
    {
      step: 6,
      action: 'type',
      description: 'Enter tags',
      command: `browser act ref=<tag-input-area> kind=type text="${tags}"`,
      value: tags,
    },
    {
      step: 7,
      action: 'click',
      description: 'Activate topic tags',
      command: 'browser act ref=<topic-button> kind=click',
    },
    {
      step: 8,
      action: 'click',
      description: 'Check the originality declaration',
      command: 'browser act ref=<original-declaration-checkbox> kind=click',
    },
    {
      step: 9,
      action: 'click',
      description: 'Click publish',
      command: 'browser act ref=<publish-button> kind=click',
    },
  ];
}

/**
 * Generate AI illustration commands
 */
function buildImageGenerationCommands(imageDescription) {
  return [
    { step: 'img-1', action: 'click', command: 'browser act ref=<text-illustration-button> kind=click' },
    { step: 'img-2', action: 'type', command: `browser act ref=<text-input> kind=type text="${imageDescription}"` },
    { step: 'img-3', action: 'click', command: 'browser act ref=<generate-button> kind=click' },
    { step: 'img-4', action: 'click', command: 'browser act ref=<style-button> kind=click' },
    { step: 'img-5', action: 'click', command: 'browser act ref=<next-step-button> kind=click' },
  ];
}

module.exports = { formatContent, buildPublishCommands, buildImageGenerationCommands };