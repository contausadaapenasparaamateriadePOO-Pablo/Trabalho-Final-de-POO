import json
from Plants import *

class BotanicoVirtual:
    def __init__(self, arquivo_json):
        self.colecao = []
        self._carregar_dados(arquivo_json)

    def _carregar_dados(self, caminho):
        try:
            with open(caminho, 'r', encoding='utf-8') as f:
                dados = json.load(f)

            p_json = dados['plantas']

            for p in p_json.get('Suculento', []):
                self.colecao.append(
                    Suculento(p['nomePopular'], p['nomeCientifico'], p['familia'],
                              p.get('fruto', 'Não informado'), p['habitat'], p['descricao'],
                              p['tipoEspinho'], p.get('cheiro'), p.get('curiosidades')))

            for p in p_json.get('Arboreo', []):
                self.colecao.append(
                    Arboreo(p['nomePopular'], p['nomeCientifico'], p['familia'],
                            p.get('fruto', 'Não informado'), p['habitat'], p['descricao'],
                            p['alturaCopa'], p.get('cheiro'), p.get('curiosidades')))

            for p in p_json.get('Trepadeira', []):
                self.colecao.append(
                    Trepadeira(p['nomePopular'], p['nomeCientifico'], p['familia'],
                               p.get('fruto', 'Não informado'), p['habitat'], p['descricao'],
                               p['mecanismoFixacao'], p.get('cheiro'), p.get('curiosidades')))

            for p in p_json.get('Herbacea', []):
                self.colecao.append(
                    Herbaceas(p['nomePopular'], p['nomeCientifico'], p['familia'],
                              p.get('fruto', 'Não informado'), p['habitat'], p['descricao'],
                              p['corFlor'], p.get('cheiro'), p.get('curiosidades')))

        except (FileNotFoundError, json.JSONDecodeError):
            print(f"Aviso: Arquivo {caminho} não encontrado ou vazio. Iniciando coleção vazia.")
            self.colecao = []

    def buscar_por_nome(self, nome):
        """Busca uma planta na coleção pelo nome popular (ignora maiúsculas/minúsculas)"""
        for planta in self.colecao:
            if planta.get_nome_popular().lower() == nome.lower():
                return planta
        return None

    def adicionar_planta_customizada(self, tipo, nome_popular, nome_cientifico, familia, fruto, habitat, descricao, caracteristica):
        """Adiciona uma nova planta à coleção e salva no JSON"""
        # Cria a planta baseado no tipo
        if tipo == "Suculento":
            nova_planta = Suculento(nome_popular, nome_cientifico, familia, fruto, habitat, descricao, caracteristica)
        elif tipo == "Arboreo":
            nova_planta = Arboreo(nome_popular, nome_cientifico, familia, fruto, habitat, descricao, caracteristica)
        elif tipo == "Trepadeira":
            nova_planta = Trepadeira(nome_popular, nome_cientifico, familia, fruto, habitat, descricao, caracteristica)
        elif tipo == "Herbaceas":
            nova_planta = Herbaceas(nome_popular, nome_cientifico, familia, fruto, habitat, descricao, caracteristica)
        else:
            return False
        
        # Adiciona à coleção em memória
        self.colecao.append(nova_planta)
        
        # Salva no arquivo JSON
        self._salvar_planta_json(tipo, {
            'nomePopular': nome_popular,
            'nomeCientifico': nome_cientifico,
            'familia': familia,
            'fruto': fruto,
            'habitat': habitat,
            'descricao': descricao,
            'caracteristica': caracteristica  # tipoEspinho, alturaCopa, mecanismoFixacao ou corFlor
        })
        
        return True

    def _salvar_planta_json(self, tipo, dados_planta):
        """Salva uma nova planta no arquivo JSON"""
        try:
            # Mapeia o tipo para a chave correta no JSON
            tipo_json = tipo if tipo != "Herbaceas" else "Herbacea"
            
            # Mapeia a característica para o campo correto
            mapa_campos = {
                "Suculento": "tipoEspinho",
                "Arboreo": "alturaCopa",
                "Trepadeira": "mecanismoFixacao",
                "Herbaceas": "corFlor"
            }
            
            # Lê o arquivo JSON
            with open('plantas.json', 'r', encoding='utf-8') as f:
                dados = json.load(f)
            
            # Prepara o novo registro
            novo_registro = {
                'nomePopular': dados_planta['nomePopular'],
                'nomeCientifico': dados_planta['nomeCientifico'],
                'familia': dados_planta['familia'],
                'fruto': dados_planta['fruto'],
                'habitat': dados_planta['habitat'],
                'descricao': dados_planta['descricao'],
                mapa_campos[tipo]: dados_planta['caracteristica']
            }
            
            # Adiciona à seção apropriada
            if tipo_json not in dados['plantas']:
                dados['plantas'][tipo_json] = []
            
            dados['plantas'][tipo_json].append(novo_registro)
            
            # Salva de volta ao arquivo
            with open('plantas.json', 'w', encoding='utf-8') as f:
                json.dump(dados, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            print(f"[!] Erro ao salvar planta: {e}")
            return False