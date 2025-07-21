#!/usr/bin/env python3
"""
Script para fazer build e upload do pacote para JFrog Artifactory
"""

import os
import subprocess
import sys

def build_package():
    """Constrói o pacote wheel"""
    print("🔨 Construindo o pacote...")
    
    # Limpar builds anteriores
    if os.path.exists("dist"):
        import shutil
        shutil.rmtree("dist")
    
    # Construir o pacote
    result = subprocess.run(
        ["uv", "build"],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print(f"❌ Erro ao construir o pacote:")
        print(result.stderr)
        return False
    
    print("✅ Pacote construído com sucesso!")
    return True

def upload_to_jfrog():
    """Faz upload do pacote para o JFrog usando API REST"""
    import glob
    import requests
    from requests.auth import HTTPBasicAuth
    
    # Configurações
    base_url = os.environ.get("JFROG_URL", "https://tr1.jfrog.io/artifactory")
    username = os.environ.get("JFROG_USER", "")
    token = os.environ.get("JFROG_TOKEN", "")
    
    if not username or not token:
        print("❌ Configure as variáveis de ambiente JFROG_USER e JFROG_TOKEN")
        print("   Exemplo:")
        print("   $env:JFROG_USER = 'seu_usuario'")
        print("   $env:JFROG_TOKEN = 'seu_token'")
        return 1
    
    auth = HTTPBasicAuth(username, token)
    
    # Encontrar arquivos wheel
    whl_files = glob.glob("dist/*.whl")
    
    if not whl_files:
        print("❌ Nenhum arquivo .whl encontrado em dist/")
        return False
    
    success_count = 0
    
    for whl_path in whl_files:
        filename = os.path.basename(whl_path)
        
        # Extrair nome e versão do arquivo
        # mcp_saudacao-0.1.0-py3-none-any.whl
        parts = filename.replace('.whl', '').split('-')
        name = parts[0]
        version = parts[1]
        
        # URL de destino na pasta taxone
        url = f"{base_url}/pypi-local/taxone/{name}/{version}/{filename}"
        
        print(f"\n📤 Fazendo upload de {filename}...")
        print(f"   Destino: pypi-local/taxone/{name}/{version}/")
        
        try:
            with open(whl_path, 'rb') as f:
                response = requests.put(
                    url,
                    auth=auth,
                    data=f,
                    headers={'Content-Type': 'application/octet-stream'}
                )
            
            if response.status_code == 201:
                print(f"   ✅ Upload bem-sucedido!")
                success_count += 1
            elif response.status_code == 409:
                print(f"   ⚠️  Arquivo já existe no repositório")
                success_count += 1
            elif response.status_code == 403:
                print(f"   ❌ Erro 403: Sem permissão para upload")
                print(f"   Resposta: {response.text}")
            else:
                print(f"   ❌ Erro {response.status_code}: {response.text}")
                
        except Exception as e:
            print(f"   ❌ Erro de conexão: {e}")
    
    if success_count > 0:
        print("\n✓ Upload concluído!")
        print("\n📥 Para baixar diretamente:")
        print(f"curl -u {username}:TOKEN {base_url}/pypi-local/taxone/{name}/{version}/{filename} -o {filename}")
        print("\n🚀 Para executar:")
        print(f"uvx --from {filename} mcp-saudacao")
        print("\n💡 Dica: Peça ao admin do JFrog para criar um repositório virtual que inclua a pasta taxone")
        
    return success_count > 0

def main():
    """Função principal"""
    print("🚀 Setup JFrog para mcp-saudacao")
    print("=" * 50)
    
    # Verificar se requests está instalado
    try:
        import requests
    except ImportError:
        print("📦 Instalando requests...")
        subprocess.run([sys.executable, "-m", "pip", "install", "requests"])
        import requests
    
    # Build
    if not build_package():
        return 1
    
    # Upload
    if not upload_to_jfrog():
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 