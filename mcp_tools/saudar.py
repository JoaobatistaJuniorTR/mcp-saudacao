"""
Ferramenta de saudação para o MCP
"""

def saudar(nome: str = "mundo") -> str:
    """
    Saúda uma pessoa com uma mensagem personalizada.
    
    Args:
        nome: Nome da pessoa para saudar (padrão: "mundo")
        
    Returns:
        Uma mensagem de saudação
    """
    return f"Olá, {nome}! Bem-vindo ao MCP!" 