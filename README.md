# MCP Saudação

Servidor MCP (Model Context Protocol) modular em Python que fornece ferramentas personalizáveis.

## Sobre o projeto

Este projeto demonstra como criar um servidor MCP com estrutura modular, facilitando a adição de novas ferramentas. Ideal para aprender os conceitos do MCP e pode ser facilmente distribuído via uvx.

## Estrutura do projeto

```
mcp-saudacao/
├── mcp_tools/              # Diretório com as ferramentas MCP
│   ├── __init__.py        # Exporta as ferramentas
│   ├── saudar.py          # Ferramenta de saudação
│   └── README.md          # Documentação das ferramentas
├── server.py               # Servidor MCP principal
├── pyproject.toml          # Configuração do projeto
├── mcp.json               # Configuração para clientes MCP
└── setup_jfrog.py         # Script para deploy no JFrog
```

## Requisitos

- Python 3.10+
- uv (gerenciador de pacotes Python)

## Instalação

### Via uv (local)

```bash
# Clonar o repositório
git clone <seu-repositorio>
cd mcp-saudacao

# Instalar dependências
uv sync

# Executar o servidor
uv run python server.py
```

### Via uvx (do JFrog)

```bash
# Executar diretamente do JFrog
uvx --index-url https://USERNAME:TOKEN@tr1.jfrog.io/artifactory/api/pypi/pypi-local/simple --extra-index-url https://pypi.org/simple mcp-saudacao
```

## Deploy no JFrog

### Configuração

1. Configure as variáveis de ambiente:
```bash
# PowerShell
$env:JFROG_USER = "seu_usuario"
$env:JFROG_TOKEN = "seu_token"

# Bash
export JFROG_USER="seu_usuario"
export JFROG_TOKEN="seu_token"
```

2. Faça o build e upload:
```bash
python setup_jfrog.py
```

## Adicionando novas ferramentas

1. Crie um novo arquivo em `mcp_tools/`:
   ```python
   # mcp_tools/minha_ferramenta.py
   def minha_ferramenta(param: str) -> str:
       return f"Resultado: {param}"
   ```

2. Exporte em `mcp_tools/__init__.py`:
   ```python
   from .minha_ferramenta import minha_ferramenta
   __all__ = ["saudar", "minha_ferramenta"]
   ```

3. Registre em `server.py`:
   ```python
   from mcp_tools import saudar, minha_ferramenta
   mcp.tool()(saudar)
   mcp.tool()(minha_ferramenta)
   ```

## Uso com Claude Desktop

Para usar este servidor com o Claude Desktop, adicione a seguinte configuração no arquivo de configuração do Claude Desktop:

```json
{
  "mcpServers": {
    "mcp-saudacao": {
      "command": "python",
      "args": ["C:/learn/mcp-uvx/server.py"]
    }
  }
}
```

Ou via uvx (após publicar no JFrog ou PyPI):
```json
{
  "mcpServers": {
    "mcp-saudacao": {
      "command": "uvx",
      "args": ["mcp-saudacao"]
    }
  }
}
```

## Uso com Cursor

Para usar com o Cursor IDE, adicione no arquivo de configuração:

```json
{
  "mcpServers": {
    "mcp-saudacao": {
      "command": "uvx",
      "args": [
        "--index-url",
        "https://USERNAME:TOKEN@tr1.jfrog.io/artifactory/api/pypi/pypi-local/simple",
        "--extra-index-url", 
        "https://pypi.org/simple",
        "mcp-saudacao"
      ]
    }
  }
}
```

## Deploy para JFrog

Para fazer deploy de uma nova versão:

```bash
# Atualizar versão em pyproject.toml se necessário
# Executar o script de deploy
python setup_jfrog.py
```

## Desenvolvimento

```bash
# Executar localmente para desenvolvimento
uv run python server.py

# Construir o pacote
uv build

# Testar a instalação local
uv pip install dist/*.whl
```

## Licença

MIT 