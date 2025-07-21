# Ferramentas MCP

Este diretório contém todas as ferramentas disponíveis no servidor MCP.

## Estrutura

Cada ferramenta é definida em seu próprio arquivo Python:

```
mcp_tools/
├── __init__.py      # Exporta as ferramentas
├── saudar.py        # Ferramenta de saudação
├── despedir.py      # Ferramenta de despedida (exemplo)
└── README.md        # Esta documentação
```

## Como adicionar uma nova ferramenta

1. **Crie um novo arquivo** em `mcp_tools/` com o nome da sua ferramenta:
   ```python
   # mcp_tools/minha_ferramenta.py
   def minha_ferramenta(parametro: str = "padrão") -> str:
       """
       Descrição da ferramenta.
       
       Args:
           parametro: Descrição do parâmetro
           
       Returns:
           Descrição do retorno
       """
       return f"Resultado: {parametro}"
   ```

2. **Exporte a ferramenta** em `mcp_tools/__init__.py`:
   ```python
   from .minha_ferramenta import minha_ferramenta
   
   __all__ = ["saudar", "minha_ferramenta"]  # Adicione aqui
   ```

3. **Registre no servidor** em `server.py`:
   ```python
   from mcp_tools import saudar, minha_ferramenta
   
   # Registrar as ferramentas
   mcp.tool()(saudar)
   mcp.tool()(minha_ferramenta)  # Nova ferramenta
   ```

## Convenções

- Nome do arquivo = nome da função principal
- Use docstrings detalhadas para documentar os parâmetros
- Mantenha uma ferramenta por arquivo para melhor organização
- Use type hints para todos os parâmetros e retornos 