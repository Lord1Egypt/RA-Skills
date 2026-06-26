---
name: quick-test
description: Quick system test to verify OpenClaw environment. Simple command execution with output validation. Use when testing if OpenClaw is working correctly, verifying command execution, or need a simple command run. Perfect for debugging or confirming system status.
---

# Quick Test

## Overview / Visão Geral

Simple system test to verify OpenClaw environment. Run basic commands and validate output.

Teste de sistema simples para verificar o ambiente do OpenClaw. Rode comandos básicos e valide a saída.

## Quick Start / Início Rápido

```bash
# Run all tests
python3 scripts/run_tests.py

# Run specific test
python3 scripts/run_tests.py --test date
python3 scripts/run_tests.py --test files

# Test with custom command
python3 scripts/run_tests.py --command "echo 'Hello World'"
```

## Installation / Instalação

1. **Clone this repository / Clone este repositório:**
```bash
git clone https://github.com/GustavoZiaugra/quick-test-skill.git
cd quick-test-skill
```

2. **No dependencies required / Sem dependências necessárias**
   - Uses only Python standard library
   - Não requer dependências externas

## Usage / Uso

### Run All Tests / Rodar Todos os Testes

```bash
python3 scripts/run_tests.py
```

This will:
- Check Python availability
- Verify current working directory
- Test file system access
- Run system commands
- Validate all outputs

Isso irá:
- Verificar disponibilidade do Python
- Confirmar diretório de trabalho atual
- Testar acesso ao sistema de arquivos
- Rodar comandos do sistema
- Validar todas as saídas

### Run Specific Test / Rodar Test Específico

```bash
# Test date functionality
python3 scripts/run_tests.py --test date

# Test file system
python3 scripts/run_tests.py --test files

# Run custom command
python3 scripts/run_tests.py --command "pwd"
```

## Parameters / Parâmetros

| Parameter | Description | Descrição | Default |
|-----------|-------------|-------------|----------|
| `--test` | Specific test to run / Teste específico para rodar | all | `--test date` |
| `--command` | Custom command to execute / Comando customizado para executar | none | `--command "ls -la"` |
| `--quiet` | Suppress output / Suprimir saída | false | `--quiet` |

## Output Format / Formato de Saída

```
✅ Quick Test Results

System Status: OK
Python: 3.12.7
Working Directory: /home/zig/.openclaw/workspace

Tests Run: 3/3 Passed
[✓] Python test
[✓] Date test
[✓] File system test

All tests passed successfully!
```

## Features / Funcionalidades

- ✅ **Python Availability Check** / **Verificação de Disponibilidade do Python** - Confirms Python 3.x installed
- ✅ **System Command Execution** / **Execução de Comando do Sistema** - Runs and validates system commands
- ✅ **File System Access** / **Acesso ao Sistema de Arquivos** - Verifies directory access and permissions
- ✅ **Custom Command Support** / **Suporte a Comandos Customizados** - Run any command with validation
- ✅ **Working Directory Check** / **Verificação de Diretório de Trabalho** - Confirms current location
- 📝 **Detailed Logging** / **Log Detalhado** - Comprehensive output for debugging

## How It Works / Como Funciona

1. **System Check** / **Verificação de Sistema** - Verifies Python and OS environment
2. **Directory Check** / **Verificação de Diretório** - Validates working directory permissions
3. **Test Execution** / **Execução do Teste** - Runs requested tests
4. **Validation** / **Validação** - Checks outputs and returns
5. **Reporting** / **Relatório** - Formats clear success/failure messages

## Use Cases / Casos de Uso

### System Verification / Verificação do Sistema

Confirm OpenClaw is running correctly:

```bash
python3 scripts/run_tests.py --test date --test files --test command
```

### Debugging Commands / Comandos de Debugging

Run specific system commands:

```bash
python3 scripts/run_tests.py --command "pwd"
python3 scripts/run_tests.py --command "ls -la"
python3 scripts/run_tests.py --command "env | head -10"
```

### Before/After Testing / Antes/Depois de Testar

Use Quick Test to verify system before/after:

```bash
# Before installing a skill
python3 scripts/run_tests.py

# After installing a skill
python3 scripts/run_tests.py
```

## Examples / Exemplos

### Basic Test / Teste Básico

```bash
# Check if everything works
python3 scripts/run_tests.py
```

Output:
```
✅ Quick Test - System Verification

Environment Check:
✓ Python 3.12.7
✓ Linux Ubuntu
✓ User: zig
✓ Working Directory: /home/zig/.openclaw/workspace

Tests:
[✓] Command: `pwd` → Passed
[✓] Command: `ls -la` → Passed
[✓] Command: `date` → Passed

All tests passed!
```

### Custom Command / Comando Customizado

```bash
# Run a specific command
python3 scripts/run_tests.py --command "echo 'Custom test'"
```

Output:
```
Custom Command: echo 'Custom test'
Result: ✅ Passed
Output: Custom test
```

## Testing Results / Resultados dos Testes

### Success Indicators / Indicadores de Sucesso

- ✅ **All tests passed** - System is working correctly / Sistema funcionando corretamente
- ⚠️ **Some tests failed** - Minor issues detected / Problemas menores detectados
- ❌ **Critical failures** - System issues requiring attention / Problemas de sistema requerendo atenção

### Common Test Failures / Falhas Comuns de Teste

**Permission Denied:** `pwd` or `ls` returns errors
- Check user permissions / Verifique permissões do usuário
- Verify directory access / Confirme acesso ao diretório

**Command Not Found:** Custom command not executable
- Verify command exists / Verifique se o comando existe
- Check PATH / Verifique o PATH

**Directory Not Found:** Working directory check fails
- Verify path / Verifique o caminho
- Check permissions / Verifique permissões

## Scripts Included / Scripts Incluídos

### scripts/run_tests.py
Main test runner script.
Script principal de execução dos testes.

### scripts/tests.py
Test suite with individual test functions.
Suíte de testes com funções de testes individuais.

### scripts/system_check.py
System validation functions.
Funções de validação do sistema.

## Philosophy / Filosofia

**Keep It Simple** / **Mantenha Simples**
- Test core functionality only
- Avoid complex dependencies / Evite dependências complexas
- Clear, readable output / Saída clara e legível

**Fast Feedback** / **Feedback Rápido**
- Show results immediately / Mostre resultados imediatamente
- Pass/fail clear / Sucesso/Falha claro
- No waiting or timeout / Sem espera ou timeout

**Debugging Friendly** / **Amigável para Debugging**
- Detailed error messages / Mensagens de erro detalhadas
- System information included / Informações do sistema incluídas
- Suggest fixes / Sugere correções

## Resources / Recursos

### scripts/run_tests.py
Main runner script that executes all tests and formats results.
Script principal que executa todos os testes e formata os resultados.

### scripts/tests.py
Individual test functions for system verification.
Funções de teste individuais para verificação do sistema.

### scripts/system_check.py
System validation and environment check functions.
Funções de validação e verificação de ambiente do sistema.

## Dependencies / Dependências

**None!** / **Nenhuma!**

Uses only Python standard library (sys, os, subprocess, datetime, json, pathlib).
Usa apenas biblioteca padrão do Python (sys, os, subprocess, datetime, json, pathlib).

## Limitations / Limitações

**User Permissions:** Requires read and execute access to directories
- **Permissões do Usuário:** Requer acesso de leitura e execução a diretórios
- System commands must be in PATH / Comandos do sistema devem estar no PATH

**System Differences:** Behavior may vary by OS (Linux, macOS, Windows)
- **Diferenças do Sistema:** Comportamento pode variar por sistema operacional (Linux, macOS, Windows)

## Troubleshooting / Solução de Problemas

### Tests Fail / Testes Falhando

If tests fail:
1. **Check permissions** / **Verifique permissões** - Ensure user has read/write access
2. **Verify Python** / **Confirme Python** - Test `python3 --version`
3. **Check commands** / **Verifique comandos** - Ensure basic commands exist
4. **Review logs** / **Revise logs** - Look for specific error messages

### Command Not Executing / Comando Não Executando

If a custom command returns nothing or errors:
1. **Verify command exists** / **Verifique se o comando existe** - Use `which` or `whereis`
2. **Test directly** / **Teste diretamente** - Run command outside of this skill
3. **Check PATH** / **Verifique o PATH** - Ensure command is in system PATH

### Python Not Found / Python Não Encontrado

If Python test fails:
1. **Check Python version** / **Verifique versão do Python** - Requires 3.7+
2. **Verify installation** / **Confirme instalação** - Check `which python3`
3. **Reinstall if needed** / **Reinstale se necessário** - See Python documentation

## License / Licença

MIT License - Use freely for personal and commercial purposes.
Licença MIT - Use livremente para fins pessoais e comerciais.

## Credits / Créditos

Created by **Gustavo (GustavoZiaugra)** with OpenClaw
Criado por **Gustavo (GustavoZiaugra)** com OpenClaw

- Simple system testing / Teste de sistema simples
- Python environment verification / Verificação de ambiente Python
- Command validation / Validação de comandos
- Debug-friendly output / Saída amigável para debug

---

**Find this and more OpenClaw skills at ClawHub.com**
**Encontre este e mais habilidades do OpenClaw em ClawHub.com**

⭐ **Star this repository if you find it useful!**
**⭐ Dê uma estrela neste repositório se você achar útil!**

✅ **Simple, fast, no dependencies** / **Simples, rápido, sem dependências** - Works everywhere, tests everything / Funciona em qualquer lugar, testa tudo / Test everywhere
