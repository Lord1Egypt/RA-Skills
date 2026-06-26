---
name: user-story-generator
description: Creates well-structured agile user stories with acceptance criteria for product development
version: 1.0.0
author: muqing
tags: [agile, user-story, product-development, scrum, requirements]
---

# User Story Generator

## Description
Transform feature requests and product ideas into properly structured agile user stories. Generates stories following the "As a [role], I want [action], so that [benefit]" format with detailed acceptance criteria, story points estimation, and technical considerations.

## How to Use
1. Input feature description or user need
2. Specify target user personas
3. Define technical constraints (if any)
4. Receive structured user stories with acceptance criteria

## Example

**Input:**
```
Feature: Add social sharing capability to mobile app
Users: App users who want to share achievements
Priority: High
Sprint capacity: 8 story points
```

**Output:**
```
## User Stories: Social Sharing Feature

### Epic
**Epic:** Social Engagement Enhancement

---

### User Stories

#### Story 1: Share Achievement
**As a** mobile app user
**I want to** share my achievements to social media
**So that** I can celebrate with friends and motivate myself

**Acceptance Criteria:**
- [ ] Share button appears after completing any achievement
- [ ] Generates shareable image with achievement badge
- [ ] Supports Facebook, Twitter, Instagram, and WhatsApp
- [ ] Includes app download link in shared content
- [ ] User can add personal message before sharing

**Story Points:** 5
**Priority:** High

---

#### Story 2: View Friends' Achievements
**As a** mobile app user
**I want to** see my friends' shared achievements
**So that** I can stay motivated by their progress

**Acceptance Criteria:**
- [ ] "Friends Activity" tab visible on home screen
- [ ] Chronological feed of friends' achievements
- [ ] Ability to send congratulations emoji/reaction
- [ ] Privacy setting to hide achievements from specific friends

**Story Points:** 8
**Priority:** Medium

---

### Technical Considerations
- Implement native share sheet (iOS/Android)
- Generate OG images for social media preview
- Track sharing events in analytics
- Consider deep linking for shared content

### Dependencies
- Authentication system (existing)
- Achievement/badge system (existing)
- Privacy settings framework (existing)
```
