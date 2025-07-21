#!/usr/bin/env python3
"""
Servidor MCP simples usando FastMCP com estrutura modular
"""
from fastmcp import FastMCP
from mcp_tools import saudar, despedir

# Criar o servidor FastMCP
mcp = FastMCP("MCPSaudacao")

# Registrar as ferramentas
mcp.tool()(saudar)
mcp.tool()(despedir)

def main():
    """Função principal para entry point"""
    mcp.run()

if __name__ == "__main__":
    # Executar o servidor
    main() 