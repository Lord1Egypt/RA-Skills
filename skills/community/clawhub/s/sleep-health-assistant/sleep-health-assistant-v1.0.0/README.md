# Sleep Health Assistant

A scientific sleep and stress analysis skill for OpenClaw, focusing on evidence-based wellness techniques.

## Features

### 🧠 Stress Analysis
- Real-time stress level assessment
- Personalized recommendations
- Privacy-focused processing

### 😴 Sleep Optimization  
- Sleep quality analysis
- Evidence-based suggestions
- Sleep hygiene guidance

### 🔊 Audio Guidance
- Relaxation techniques
- Sleep preparation guidance
- Focus enhancement methods

### 🌬️ Breathing Guidance
- Calm breathing techniques
- Sleep breathing patterns
- Energy breathing methods

### 🧘 Mindfulness Guidance
- Awareness practices
- Relaxation techniques
- Compassion cultivation

### 📊 Health Monitoring
- User-data based monitoring
- In-memory processing only
- Privacy assurance

## Quick Start

### Installation
```bash
# Install from ClawHub
npx clawhub install sleep-health-assistant
```

### Basic Usage
```bash
# Analyze stress
/sleep-health analyze-stress

# Analyze sleep  
/sleep-health analyze-sleep

# Audio guidance
/sleep-health audio-guidance relaxation

# Breathing guidance
/sleep-health breathing-guidance calm_breathing

# Mindfulness guidance
/sleep-health mindfulness-guidance awareness
```

## Security & Privacy

### Core Principles
- ✅ **100% local operation** - No network access
- ✅ **No dangerous functions** - No eval, exec, subprocess
- ✅ **Memory-only storage** - No disk persistence
- ✅ **No file operations** - No system file access
- ✅ **Transparent code** - Full source available

### Data Handling
- All processing done locally on your device
- Session data stored in memory only
- No data collection or transmission
- No file system access

## Scientific Basis

### Evidence-Based Techniques
- Stress management research
- Sleep hygiene research
- Respiratory physiology
- Mindfulness research
- Cognitive behavioral principles

### Content Policy
- ✅ Modern scientific techniques only
- ✅ Cultural neutrality maintained
- ✅ Educational focus
- ❌ No religious content
- ❌ No medical advice
- ❌ No external dependencies

## Performance

### System Requirements
- **Python**: 3.8+
- **OpenClaw**: 2026.3+
- **Memory**: < 50MB
- **Storage**: Minimal

### Response Times
- Command response: < 100ms
- Analysis completion: < 500ms
- Guidance generation: < 200ms

## Configuration

### Basic Settings
Edit `config.yaml` to customize:
- Enable/disable features
- Set default protocols
- Adjust performance parameters

### No External Dependencies
The skill uses only Python standard library modules.

## Advanced Usage

### Health Monitoring
```bash
# Monitor health with custom data
/sleep-health health-monitoring stress_level=high sleep_quality=poor

# Check monitoring status
/sleep-health status

# Clear session data
/sleep-health cleanup
```

### Custom Data Input
Provide your own data for analysis:
```bash
# Stress analysis with custom data
/sleep-health analyze-stress heart_rate=85 sleep_hours=6.5

# Sleep analysis with custom data  
/sleep-health analyze-sleep duration_hours=7.5 quality_rating=4 wakeups=2
```

## Troubleshooting

### Common Issues

**Command not working?**
- Verify installation: `npx clawhub list | grep sleep-health`
- Check OpenClaw logs for errors
- Ensure correct command syntax

**No response from skill?**
- Check skill status: `/sleep-health status`
- Verify OpenClaw is running
- Restart OpenClaw if needed

**Performance issues?**
- Check system resource usage
- Verify Python version compatibility
- Review configuration settings

### Getting Help
- Check full documentation in `SKILL.md`
- Review configuration in `config.yaml`
- Check version history in `CHANGELOG.md`

## Development

### Code Structure
- `skill.py` - Main implementation
- `config.yaml` - Configuration
- `SKILL.md` - Full documentation
- `README.md` - User guide
- `CHANGELOG.md` - Version history
- `requirements.txt` - Dependencies (empty)

### Testing
```python
# Quick test
from skill import SleepHealthAssistantSkill
skill = SleepHealthAssistantSkill()
result = skill.handle_command('status')
print(result)
```

## License

MIT License - Free to use, modify, and distribute.

## Version

**Current**: 1.0.0  
**Status**: Initial release  
**Security**: Designed for maximum security

## Support

- **Documentation**: This file and `SKILL.md`
- **Community**: OpenClaw community
- **Updates**: Via ClawHub registry

---

**Note**: This skill is designed for educational and self-improvement purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment.