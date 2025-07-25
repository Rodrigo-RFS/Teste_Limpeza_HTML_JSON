import os
import json
import re
import html
import unicodedata
from bs4 import BeautifulSoup

# 🔧 Função para limpar HTML e remover caracteres invisíveis
def aplicar_limpeza_html(texto_html):
    texto_html = html.unescape(texto_html)
    soup = BeautifulSoup(texto_html, "html.parser")
    texto_limpo = soup.get_text(separator=" ", strip=True)
    texto_limpo = re.sub(r"\s{2,}", " ", texto_limpo)

    texto_seguro = ''.join(
        c for c in texto_limpo
        if unicodedata.category(c)[0] != "C"  # Remove caracteres de controle
    )

    return texto_seguro.strip()

# 📁 Diretório principal com as pastas de origem
diretorio_raiz = "C:\\JSON"  # ajuste conforme necessário

# 🔄 Percorre todas as pastas como TJRS, TJSP etc.
for pasta_principal in os.listdir(diretorio_raiz):
    caminho_pasta_principal = os.path.join(diretorio_raiz, pasta_principal)

    if not os.path.isdir(caminho_pasta_principal) or "_Limpo" in pasta_principal:
        continue

    # ✅ Cria pasta final com sufixo _Limpo
    pasta_limpa_principal = os.path.join(diretorio_raiz, f"{pasta_principal}_Limpo")
    os.makedirs(pasta_limpa_principal, exist_ok=True)

    # 🔎 Lista apenas subpastas reais
    subpastas = [
        nome for nome in os.listdir(caminho_pasta_principal)
        if os.path.isdir(os.path.join(caminho_pasta_principal, nome))
    ]

    if subpastas:
        print(f"📁 Pasta '{pasta_principal}' contém {len(subpastas)} subpasta(s): {', '.join(subpastas)}")

        # 🧼 Processa cada subpasta individualmente
        for subpasta in subpastas:
            caminho_subpasta = os.path.join(caminho_pasta_principal, subpasta)
            caminho_subpasta_limpa = os.path.join(pasta_limpa_principal, subpasta)
            os.makedirs(caminho_subpasta_limpa, exist_ok=True)

            for nome_arquivo in os.listdir(caminho_subpasta):
                if nome_arquivo.endswith(".json"):
                    caminho_entrada = os.path.join(caminho_subpasta, nome_arquivo)
                    caminho_saida = os.path.join(caminho_subpasta_limpa, nome_arquivo)

                    try:
                        with open(caminho_entrada, "r", encoding="utf-8") as f:
                            dados = json.load(f)

                        if isinstance(dados, dict) and "items" in dados and isinstance(dados["items"], list):
                            for item in dados["items"]:
                                if "texto" in item and isinstance(item["texto"], str):
                                    item["texto"] = aplicar_limpeza_html(item["texto"])

                        with open(caminho_saida, "w", encoding="utf-8") as f:
                            json.dump(dados, f, indent=4, ensure_ascii=False)

                        print(f"✅ {pasta_principal}\\{subpasta} → {nome_arquivo} limpo com sucesso")

                    except Exception as e:
                        print(f"⚠️ Erro ao limpar {pasta_principal}\\{subpasta}\\{nome_arquivo}: {e}")
    else:
        # 📄 Caso não haja subpastas, tenta processar arquivos diretamente na pasta_principal
        arquivos_na_raiz = [
            nome for nome in os.listdir(caminho_pasta_principal)
            if os.path.isfile(os.path.join(caminho_pasta_principal, nome)) and nome.endswith(".json")
        ]

        if arquivos_na_raiz:
            print(f"📂 Pasta '{pasta_principal}' não possui subpastas, mas contém {len(arquivos_na_raiz)} arquivo(s) JSON.")

            for nome_arquivo in arquivos_na_raiz:
                caminho_entrada = os.path.join(caminho_pasta_principal, nome_arquivo)
                caminho_saida = os.path.join(pasta_limpa_principal, nome_arquivo)

                try:
                    with open(caminho_entrada, "r", encoding="utf-8") as f:
                        dados = json.load(f)

                    if isinstance(dados, dict) and "items" in dados and isinstance(dados["items"], list):
                        for item in dados["items"]:
                            if "texto" in item and isinstance(item["texto"], str):
                                item["texto"] = aplicar_limpeza_html(item["texto"])

                    with open(caminho_saida, "w", encoding="utf-8") as f:
                        json.dump(dados, f, indent=4, ensure_ascii=False)

                    print(f"✅ {pasta_principal} → {nome_arquivo} limpo com sucesso")

                except Exception as e:
                    print(f"⚠️ Erro ao limpar {pasta_principal}\\{nome_arquivo}: {e}")
        else:
            print(f"ℹ️ Pasta '{pasta_principal}' está vazia ou não contém arquivos JSON.")