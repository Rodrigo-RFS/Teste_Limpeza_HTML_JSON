import os
import json
import re
import shutil
import html
import unicodedata
from bs4 import BeautifulSoup
from natsort import natsorted

# 🔧 Função para limpar o campo HTML
def aplicar_limpeza_html(texto_html):
    if not texto_html:
        return ""
    texto_html = html.unescape(texto_html)
    soup = BeautifulSoup(texto_html, "html.parser")
    texto_limpo = soup.get_text(separator=" ", strip=True)
    texto_limpo = re.sub(r"\s{2,}", " ", texto_limpo)
    texto_seguro = ''.join(
        c for c in texto_limpo
        if unicodedata.category(c)[0] != "C"  # Remove caracteres invisíveis
    )
    return texto_seguro.strip()

# 📦 Função principal para processar a pasta
def processar_pasta(pasta_raiz):
    for nome_pasta in os.listdir(pasta_raiz):
        caminho_pasta = os.path.join(pasta_raiz, nome_pasta)
        if not os.path.isdir(caminho_pasta):
            continue

        print(f"\n🔍 Processando pasta: {nome_pasta}")
        pasta_limpa = os.path.join(pasta_raiz, f"{nome_pasta}_Limpo")
        os.makedirs(pasta_limpa, exist_ok=True)

        arquivos = [f for f in os.listdir(caminho_pasta) if f.endswith(".json")]
        arquivos_ordenados = natsorted(arquivos)

        arquivos_processados = []
        erros = []

        for arquivo in arquivos_ordenados:
            caminho_arquivo = os.path.join(caminho_pasta, arquivo)
            try:
                with open(caminho_arquivo, "r", encoding="utf-8") as f:
                    dados = json.load(f)

                itens = dados.get("items")
                if itens and isinstance(itens, list):
                    for item in itens:
                        if isinstance(item, dict) and "texto" in item:
                            item["texto"] = aplicar_limpeza_html(item["texto"])
                elif "texto" in dados:
                    dados["texto"] = aplicar_limpeza_html(dados["texto"])
                else:
                    raise ValueError("Arquivo sem campo 'texto' ou 'items' válido")

                caminho_saida = os.path.join(pasta_limpa, arquivo)
                with open(caminho_saida, "w", encoding="utf-8") as f_out:
                    json.dump(dados, f_out, ensure_ascii=False, indent=2)

                arquivos_processados.append(arquivo)

            except Exception as e:
                erros.append(f"[ERRO] Pasta: {nome_pasta} | Arquivo: {arquivo} | Motivo: {str(e)}")

        total = len(arquivos_processados)
        print(f"✅ Arquivos limpos: {total}")

        # 📁 Subdividir em subpastas (1, 2, 3...)
        if total > 60:
            for i, arquivo in enumerate(arquivos_processados):
                idx_subpasta = i // 60 + 1
                subpasta = os.path.join(pasta_limpa, f"{idx_subpasta}")
                os.makedirs(subpasta, exist_ok=True)
                origem = os.path.join(pasta_limpa, arquivo)
                destino = os.path.join(subpasta, arquivo)
                shutil.move(origem, destino)
            print("📂 Distribuído em subpastas com até 60 arquivos.")

        # ⚠️ Exibir erros encontrados
        if erros:
            print("\n🚨 Arquivos com erro:")
            for erro in erros:
                print(erro)

# ▶️ Execução
if __name__ == "__main__":
    pasta_raiz = r"C:\JSON"
    if os.path.isdir(pasta_raiz):
        processar_pasta(pasta_raiz)
    else:
        print("❌ Caminho inválido. Verifique e tente novamente.")

