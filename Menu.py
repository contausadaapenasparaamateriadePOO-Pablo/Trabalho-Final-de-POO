import keyboard
import time
import os
from Plants import *


def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')


class MenuPrincipal:
    def __init__(self, botanico):
        self.botanico = botanico
        self.opcoes = ["1. Identificar uma Planta", "2. Ver Plantas Existentes", "3. Sair"]
        self.selecionado = 0
        self.categorias = ["Suculento", "Arboreo", "Trepadeira", "Herbaceas"]
        
        # Descrições visuais dos mecanismos de fixação para pessoas sem conhecimento botânico
        self.descricoes_mecanismos = {
            "Gavinhas": "Filamentos finos que se enroscam como uma corda (tipo: videira, maracujá)",
            "Caule volúvel": "O caule inteiro se enrola em espiral ao redor do suporte (tipo: feijão trepadeiro)",
            "Escandente": "Ramos longos que se apoiam sobre o suporte sem se enrolar (tipo: cipó solto)",
            "Raízes aderentes": "Raízes especiais que grudam nas superfícies como cola (tipo: hera em parede)",
            "Acúleos": "Espinhos que ajudam a se apoiar na superfície (tipo: roseira, buganvília)"
        }

    def menu_perguntas(self, titulo, opcoes):
        selecionado = 0
        while True:
            limpar_tela()
            print(f"=== {titulo} ===")
            print("Navegue com as SETAS e confirme com ENTER:\n")
            for i, opt in enumerate(opcoes):
                if i == selecionado:
                    print(f" > {opt.upper()} < ")
                else:
                    print(f"   {opt}")

            evento = keyboard.read_event()
            if evento.event_type == keyboard.KEY_DOWN:
                if evento.name == 'up':
                    selecionado = (selecionado - 1) % len(opcoes)
                elif evento.name == 'down':
                    selecionado = (selecionado + 1) % len(opcoes)
                elif evento.name == 'enter':
                    while keyboard.is_pressed('enter'): pass
                    return selecionado
            time.sleep(0.1)

    def filtrar_por_caracteristicas(self, lista_atual):
        if not lista_atual: return lista_atual

        # Identificamos o tipo da planta baseando-se na classe do primeiro item
        tipo_planta = type(lista_atual[0]).__name__
        sobra = lista_atual

        # ==========================================
        # 1. FUNIL PARA CACTOS / SUCULENTAS
        # ==========================================
        if tipo_planta == "Suculento":
            # Detecta dinamicamente se há plantas com/sem espinhos
            com_espinhos = [p for p in lista_atual if "ausente" not in p._Suculento__tipoEspinho.lower()]
            sem_espinhos = [p for p in lista_atual if "ausente" in p._Suculento__tipoEspinho.lower()]
            
            opcoes_defesa = []
            if com_espinhos:
                opcoes_defesa.append("Possui espinhos visíveis")
            if sem_espinhos:
                opcoes_defesa.append("Não possui espinhos (lisa/articulada)")
            
            # Se há mais de 1 opção real (sem contar "Pular"), faz a pergunta
            if len(opcoes_defesa) > 1:
                opcoes_defesa.append("Pular")
                p1 = self.menu_perguntas("OBSERVAÇÃO DE DEFESA", opcoes_defesa)
            else:
                # Se há apenas 1 opção, pula automaticamente
                p1 = 0 if opcoes_defesa else 2

            # Filtro visual de espinho
            if p1 == 0 and com_espinhos:
                sobra = com_espinhos
            elif p1 == 0 and not com_espinhos:
                sobra = sem_espinhos
            elif p1 == 1 and sem_espinhos:
                sobra = sem_espinhos
            elif p1 == 1 and not sem_espinhos:
                sobra = com_espinhos

            if len(sobra) > 1:
                opcoes = [f"Tipo de Espinho/Caule: {p._Suculento__tipoEspinho}" for p in sobra]
                opcoes.append("Nenhuma dessas")
                sel = self.menu_perguntas("DETALHE TÉCNICO", opcoes)
                if sel == len(opcoes) - 1:
                    self.catalogar_nova_planta("Suculento")
                    return []
                return [sobra[sel]]

        # ==========================================
        # 2. FUNIL PARA ÁRVORES / GRANDE PORTE
        # ==========================================
        elif tipo_planta == "Arboreo":
            # Detecta dinamicamente tipos de folhagem disponíveis
            caducifolias = [p for p in lista_atual if any(termo in p.get_descricao().lower()
                                                           for termo in ["perde", "cai", "caducif", "seca"])]
            perenifolias = [p for p in lista_atual if any(termo in p.get_descricao().lower()
                                                           for termo in ["sempre verde", "mantém", "perenif", "não perde"])]
            
            opcoes_folha = []
            if caducifolias:
                opcoes_folha.append("Perde as folhas no período seco (Caducifólia)")
            if perenifolias:
                opcoes_folha.append("Mantém as folhas verdes o ano todo (Perenifólia)")
            
            # Se há mais de 1 opção real, faz a pergunta
            if len(opcoes_folha) > 1:
                opcoes_folha.append("Pular")
                p1 = self.menu_perguntas("COMPORTAMENTO DAS FOLHAS", opcoes_folha)
            else:
                # Se há apenas 1 opção, pula automaticamente
                p1 = 0 if opcoes_folha else 2

            if p1 == 0 and caducifolias:
                sobra = caducifolias
            elif p1 == 0 and not caducifolias:
                sobra = perenifolias
            elif p1 == 1 and perenifolias:
                sobra = perenifolias
            elif p1 == 1 and not perenifolias:
                sobra = caducifolias

            # Segunda pergunta: Tamanho/Formato da Copa - DINÂMICA
            if len(sobra) > 1:
                # Mapeia copos por características
                copos_baixos = [p for p in sobra if any(termo in p._Arboreo__alturaCopa.lower()
                                                         for termo in ["baixa", "densa", "guarda-chuva", "compacta"])]
                copos_altos = [p for p in sobra if any(termo in p._Arboreo__alturaCopa.lower()
                                                        for termo in ["alta", "aberta", "dominante", "piramidal", "elegante"])]
                copos_leque = [p for p in sobra if any(termo in p._Arboreo__alturaCopa.lower()
                                                        for termo in ["leque", "palmeira"])]
                copos_frondosos = [p for p in sobra if any(termo in p._Arboreo__alturaCopa.lower()
                                                            for termo in ["larga", "frondosa"])]
                
                opcoes_copa = []
                if copos_baixos:
                    opcoes_copa.append("Copa baixa e densa (guarda-chuva ou compacta)")
                if copos_altos:
                    opcoes_copa.append("Copa alta e aberta (dominante, piramidal ou elegante)")
                if copos_leque:
                    opcoes_copa.append("Copa em leque ou palmeira")
                if copos_frondosos:
                    opcoes_copa.append("Copa larga e frondosa")
                
                # Se há mais de 1 opção real, faz a pergunta
                if len(opcoes_copa) > 1:
                    opcoes_copa.append("Pular")
                    p2 = self.menu_perguntas("FORMATO E TAMANHO DA COPA", opcoes_copa)
                else:
                    # Se há apenas 1 opção, pula automaticamente
                    p2 = 0 if opcoes_copa else 4

                if p2 == 0 and copos_baixos:
                    sobra = copos_baixos
                elif p2 == 0 and not copos_baixos:
                    sobra = copos_altos if copos_altos else copos_leque if copos_leque else copos_frondosos
                elif p2 == 1 and copos_altos:
                    sobra = copos_altos
                elif p2 == 1 and not copos_altos:
                    sobra = copos_baixos if copos_baixos else copos_leque if copos_leque else copos_frondosos
                elif p2 == 2 and copos_leque:
                    sobra = copos_leque
                elif p2 == 2 and not copos_leque:
                    sobra = copos_baixos if copos_baixos else copos_altos if copos_altos else copos_frondosos
                elif p2 == 3 and copos_frondosos:
                    sobra = copos_frondosos
                elif p2 == 3 and not copos_frondosos:
                    sobra = copos_baixos if copos_baixos else copos_altos if copos_altos else copos_leque

            # Terceira pergunta: Especificidade visual final
            if len(sobra) > 1:
                opcoes = [f"Copa: {p._Arboreo__alturaCopa}" for p in sobra]
                opcoes.append("Nenhuma dessas")
                sel = self.menu_perguntas("DETALHE VISUAL FINAL", opcoes)
                if sel == len(opcoes) - 1:
                    self.catalogar_nova_planta("Arboreo")
                    return []
                return [sobra[sel]]

            return sobra

        # ==========================================
        # 3. FUNIL PARA TREPADEIRAS / CIPÓS
        # ==========================================
        elif tipo_planta == "Trepadeira":
            # Primeira pergunta: Mecanismo de fixação
            mecanismos = sorted(list(set([p._Trepadeira__mecanismoFixacao for p in sobra])))
            opcoes_mec = [f"{m} - {self.descricoes_mecanismos.get(m, '')}" for m in mecanismos]
            
            # Se há mais de 1 opção real, faz a pergunta
            if len(opcoes_mec) > 1:
                opcoes_mec.append("Pular")
                p1 = self.menu_perguntas("COMO ELA SE APOIA NO SUPORTE?", opcoes_mec)
            else:
                # Se há apenas 1 opção, pula automaticamente
                p1 = 0 if opcoes_mec else len(opcoes_mec)
            
            if p1 < len(mecanismos):
                mec_escolhido = mecanismos[p1]
                sobra = [p for p in sobra if p._Trepadeira__mecanismoFixacao == mec_escolhido]

            # Segunda pergunta: Tipo de habitat/ambiente
            if len(sobra) > 1:
                habitats = sorted(list(set([p.get_habitat().strip(". ") for p in sobra])))
                opcoes_hab = habitats.copy()
                
                # Se há mais de 1 opção real, faz a pergunta
                if len(opcoes_hab) > 1:
                    opcoes_hab.append("Pular")
                    p2 = self.menu_perguntas("ONDE ELA CRESCE?", opcoes_hab)
                else:
                    # Se há apenas 1 opção, pula automaticamente
                    p2 = 0 if opcoes_hab else len(opcoes_hab)
                
                if p2 < len(habitats):
                    hab_escolhido = habitats[p2]
                    sobra = [p for p in sobra if p.get_habitat().strip(". ").lower() == hab_escolhido.lower()]

            # Terceira pergunta: Floração/Características visuais
            if len(sobra) > 1:
                opcoes = []
                for p in sobra:
                    # Extrai características visuais das flores da descrição
                    descricao = p.get_descricao()
                    
                    # Procura por cores de flores mencionadas
                    cores_flores = []
                    palavras_chave_flores = {
                        "branca": "flores Brancas",
                        "branco": "flores Brancas",
                        "amarela": "flores Amarelas",
                        "amarelo": "flores Amarelas",
                        "rosa": "flores Rosas",
                        "rosada": "flores Rosas",
                        "roxa": "flores Roxas",
                        "roxas": "flores Roxas",
                        "azul": "flores Azuis",
                        "laranja": "flores Laranja",
                        "vermelha": "flores Vermelhas",
                        "vermelho": "flores Vermelhas",
                        "vermelhos": "flores Vermelhas",
                    }
                    
                    for palavra, cor in palavras_chave_flores.items():
                        if palavra in descricao.lower() and "flor" in descricao.lower():
                            if cor not in cores_flores:
                                cores_flores.append(cor)
                    
                    # Se encontrou cores, mostra; se não, mostra tipo de floração
                    if cores_flores:
                        opcoes.append(" / ".join(cores_flores[:2]))  # Mostra até 2 cores principais
                    else:
                        # Tenta extrair outras características visuais
                        if "pendente" in descricao.lower():
                            opcoes.append("Flores pendentes")
                        elif "cachos" in descricao.lower() or "cacho" in descricao.lower():
                            opcoes.append("Flores em cachos")
                        elif "trepadeira" in descricao.lower():
                            opcoes.append("Cobertura densa")
                        else:
                            opcoes.append("Floração vistosa")
                
                # Remove duplicatas mantendo ordem
                opcoes_unicas = []
                for opt in opcoes:
                    if opt not in opcoes_unicas:
                        opcoes_unicas.append(opt)
                opcoes = opcoes_unicas
                
                # Se há mais de 1 opção real, faz a pergunta
                if len(opcoes) > 1:
                    opcoes.append("Pular")
                    p3 = self.menu_perguntas("QUAL É A CARACTERÍSTICA VISUAL?", opcoes)
                else:
                    # Se há apenas 1 opção ou nenhuma, pula
                    p3 = len(opcoes)
                
                if p3 < len(opcoes) - 1:  # Não é "Pular"
                    caracteristica_escolhida = opcoes[p3]
                    # Filtra plantas que correspondem à característica visual
                    sobra = [p for p in sobra if caracteristica_escolhida in " / ".join([
                        "Flores Brancas" if "branca" in p.get_descricao().lower() else "",
                        "Flores Amarelas" if "amarela" in p.get_descricao().lower() else "",
                        "Flores Rosas" if "rosa" in p.get_descricao().lower() else "",
                        "Flores Roxas" if "roxa" in p.get_descricao().lower() else "",
                        "Flores Azuis" if "azul" in p.get_descricao().lower() else "",
                        "Flores Laranja" if "laranja" in p.get_descricao().lower() else "",
                        "Flores Vermelhas" if "vermelha" in p.get_descricao().lower() else "",
                        "Flores pendentes" if "pendente" in p.get_descricao().lower() else "",
                        "Flores em cachos" if "cachos" in p.get_descricao().lower() or "cacho" in p.get_descricao().lower() else "",
                        "Cobertura densa" if "densa" in p.get_descricao().lower() else "",
                        "Floração vistosa" if "vistosa" in p.get_descricao().lower() else ""
                    ])]

            return sobra

        # ==========================================
        # 4. FUNIL PARA ERVAS / PLANTAS PEQUENAS
        # ==========================================
        elif tipo_planta == "Herbaceas":
            # Primeira pergunta: Cor da flor
            # Extrai cores únicas (plantas podem ter múltiplas cores separadas por vírgula)
            cores_unicas = set()
            for p in sobra:
                # Separa as cores se houver múltiplas (separadas por vírgula)
                cores_planta = [c.strip() for c in p._Herbaceas__corFlor.split(',')]
                cores_unicas.update(cores_planta)
            
            cores = sorted(list(cores_unicas))
            opcoes_cor = cores.copy()
            
            # Se há mais de 1 opção real, faz a pergunta
            if len(opcoes_cor) > 1:
                opcoes_cor.append("Pular")
                p1 = self.menu_perguntas("COR PREDOMINANTE DA FLOR", opcoes_cor)
            else:
                # Se há apenas 1 opção, pula automaticamente
                p1 = 0 if opcoes_cor else len(opcoes_cor)
            
            if p1 < len(cores):
                cor_escolhida = cores[p1]
                # Filtra plantas que contenham a cor escolhida
                sobra = [p for p in sobra if cor_escolhida in [c.strip() for c in p._Herbaceas__corFlor.split(',')]]

            # Segunda pergunta: Habitat/Ambiente
            if len(sobra) > 1:
                habitats = sorted(list(set([p.get_habitat().strip(". ") for p in sobra])))
                opcoes_hab = habitats.copy()
                
                # Se há mais de 1 opção real, faz a pergunta
                if len(opcoes_hab) > 1:
                    opcoes_hab.append("Pular")
                    p2 = self.menu_perguntas("AMBIENTE PREFERIDO", opcoes_hab)
                else:
                    # Se há apenas 1 opção, pula automaticamente
                    p2 = 0 if opcoes_hab else len(opcoes_hab)
                
                if p2 < len(habitats):
                    hab_escolhido = habitats[p2]
                    sobra = [p for p in sobra if p.get_habitat().strip(". ").lower() == hab_escolhido.lower()]

            # Terceira pergunta: Características da flor (tamanho, forma, uso)
            if len(sobra) > 1:
                opcoes = []
                for p in sobra:
                    descricao = p.get_descricao()
                    # Limita a exibição para não ficar muito longo (aumentado para 150 caracteres)
                    desc_curta = descricao[:150] + "..." if len(descricao) > 150 else descricao
                    opcoes.append(f"{p.get_nome_popular()}: {desc_curta}")
                
                opcoes.append("Nenhuma dessas")
                sel = self.menu_perguntas("QUAL DESTAS VOCÊ OBSERVA?", opcoes)
                if sel == len(opcoes) - 1:
                    self.catalogar_nova_planta("Herbaceas")
                    return []
                return [sobra[sel]]

            return sobra

        return sobra

    def mostrar(self):
        limpar_tela()
        print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   ██████╗  █████╗ ██╗███████╗    ██████╗  ██████╗            ║
║   ██╔══██╗██╔══██╗██║╚══███╔╝    ██╔══██╗██╔═══██╗           ║
║   ██████╔╝███████║██║  ███╔╝     ██║  ██║██║   ██║           ║
║   ██╔══██╗██╔══██║██║ ███╔╝      ██║  ██║██║   ██║           ║
║   ██║  ██║██║  ██║██║███████╗    ██████╔╝╚██████╔╝           ║
║   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚══════╝    ╚═════╝  ╚═════╝            ║
║                                                              ║
║         ███████╗███████╗██████╗ ████████╗ █████╗  ██████╗    ║
║         ██╔════╝██╔════╝██╔══██╗╚══██╔══╝██╔══██╗██╔═══██╗   ║
║         ███████╗█████╗  ██████╔╝   ██║   ███████║██║   ██║   ║
║         ╚════██║██╔══╝  ██╔══██╗   ██║   ██╔══██║██║   ██║   ║
║         ███████║███████╗██║  ██║   ██║   ██║  ██║╚██████╔╝   ║
║         ╚══════╝╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝    ║
║                                                              ║
║              🌵 Sistema de Identificação Botânica 🌿           ║
╚══════════════════════════════════════════════════════════════╝
""")
        print("Navegue com as SETAS e confirme com ENTER\n")
        opcoes_texto = ["Identificar uma Planta", "Ver Plantas Existentes", "Sair"]
        for i, texto in enumerate(opcoes_texto):
            if i == self.selecionado:
                print(f" > {texto.upper()} < ")
            else:
                print(f"   {texto}")

    def menu_identificar(self):
        opcoes_tipo = ["Cacto / Suculenta", "Árvore / Grande porte", "Trepadeira / Cipó", "Erva / Planta pequena",
                       "Voltar"]
        selecionado_tipo = 0
        while True:
            limpar_tela()
            print("=== QUESTIONÁRIO DE IDENTIFICAÇÃO ===")
            for i, tipo in enumerate(opcoes_tipo):
                if i == selecionado_tipo:
                    print(f" > {tipo.upper()} < ")
                else:
                    print(f"   {tipo}")

            evento = keyboard.read_event()
            if evento.event_type == keyboard.KEY_DOWN:
                tecla = evento.name
                if tecla == 'up':
                    selecionado_tipo = (selecionado_tipo - 1) % len(opcoes_tipo)
                elif tecla == 'down':
                    selecionado_tipo = (selecionado_tipo + 1) % len(opcoes_tipo)
                elif tecla == 'enter':
                    while keyboard.is_pressed('enter'): pass
                    if selecionado_tipo == 4: return

                    mapa_classes = {0: "Suculento", 1: "Arboreo", 2: "Trepadeira", 3: "Herbaceas"}
                    classe_procurada = mapa_classes.get(selecionado_tipo)
                    candidatas = [p for p in self.botanico.colecao if
                                  type(p).__name__.strip().lower() == classe_procurada.lower()]

                    if not candidatas:
                        print(f"\n[!] Nenhuma planta do tipo '{classe_procurada}' encontrada.")
                        time.sleep(2.0)
                        continue

                    self.filtrar_por_habitat(candidatas)
                    break
            time.sleep(0.1)

    def catalogar_nova_planta(self, tipo_planta):
        """Permite ao usuário catalogar uma nova planta no sistema."""
        limpar_tela()
        print("=== CATALOGAÇÃO DE NOVA PLANTA ===\n")
        
        # Coleta informações básicas
        nome_popular = input("Nome Popular da planta: ").strip()
        if not nome_popular:
            print("[!] Operação cancelada.")
            time.sleep(1)
            return
        
        nome_cientifico = input("Nome Científico (opcional, pressione ENTER para pular): ").strip()
        familia = input("Família (ex: Cactaceae, Fabaceae): ").strip()
        habitat = input("Habitat (ex: Caatinga, Mata Atlântica): ").strip()
        descricao = input("Descrição da planta: ").strip()
        fruto = input("Fruto/Características especiais: ").strip()
        
        # Coleta características específicas do tipo
        if tipo_planta == "Suculento":
            tipo_espinho = input("Tipo de Espinho (ex: Agudos, rígidos / Ausente): ").strip()
            self.botanico.adicionar_planta_customizada(
                tipo_planta, nome_popular, nome_cientifico, familia, 
                fruto, habitat, descricao, tipo_espinho
            )
        elif tipo_planta == "Arboreo":
            altura_copa = input("Altura/Formato da Copa (ex: Copa baixa e densa / Copa alta e aberta): ").strip()
            self.botanico.adicionar_planta_customizada(
                tipo_planta, nome_popular, nome_cientifico, familia, 
                fruto, habitat, descricao, altura_copa
            )
        elif tipo_planta == "Trepadeira":
            mecanismo_fixacao = input("Mecanismo de Fixação (ex: Gavinhas / Caule volúvel / Raízes grampiformes): ").strip()
            self.botanico.adicionar_planta_customizada(
                tipo_planta, nome_popular, nome_cientifico, familia, 
                fruto, habitat, descricao, mecanismo_fixacao
            )
        elif tipo_planta == "Herbaceas":
            cor_flor = input("Cor predominante da flor: ").strip()
            self.botanico.adicionar_planta_customizada(
                tipo_planta, nome_popular, nome_cientifico, familia, 
                fruto, habitat, descricao, cor_flor
            )
        
        limpar_tela()
        print("✓ Planta catalogada com sucesso!")
        print(f"\n'{nome_popular}' foi adicionada ao sistema.\n")
        print("Pressione ESPAÇO para voltar...")
        keyboard.wait('space')

    def filtrar_por_habitat(self, candidatas):
        # 1. Criamos a lista de habitats únicos e "limpos" (sem pontos ou espaços extras)
        habitats = sorted(list(set([p.get_habitat().strip(". ") for p in candidatas])))
        habitats.append("Voltar")
        selecionado_hab = 0

        while True:
            limpar_tela()
            print("=== REFINAR POR HABITAT ===")
            for i, hab in enumerate(habitats):
                if i == selecionado_hab:
                    print(f" > {hab.upper()} < ")
                else:
                    print(f"   {hab}")

            evento = keyboard.read_event()
            if evento.event_type == keyboard.KEY_DOWN:
                tecla = evento.name
                if tecla == 'up':
                    selecionado_hab = (selecionado_hab - 1) % len(habitats)
                elif tecla == 'down':
                    selecionado_hab = (selecionado_hab + 1) % len(habitats)
                elif tecla == 'enter':
                    while keyboard.is_pressed('enter'): pass
                    if habitats[selecionado_hab] == "Voltar": return

                    habitat_escolhido = habitats[selecionado_hab]

                    # --- O SEGREDO ESTÁ AQUI ---
                    # Comparamos o habitat da planta "limpo" com o nome do menu "limpo"
                    intermediarias = [
                        p for p in candidatas
                        if p.get_habitat().strip(". ").lower() == habitat_escolhido.lower()
                    ]

                    if not intermediarias:
                        print(f"\n[!] Nenhuma planta encontrada para: {habitat_escolhido}")
                        time.sleep(2.0)
                        continue

                    resultado = intermediarias
                    if len(intermediarias) > 1:
                        print(f"\n   Encontradas {len(intermediarias)} plantas. Refinando...")
                        time.sleep(0.6)
                        resultado = self.filtrar_por_caracteristicas(intermediarias)

                    if not resultado:
                        continue

                    # --- EXIBIÇÃO ---
                    limpar_tela()
                    print(f"=== RESULTADO DA IDENTIFICAÇÃO ({len(resultado)} encontrada(s)) ===")
                    for planta in resultado:
                        planta.exibirFicha()

                    print("\n" + "=" * 50)
                    print(">> Pressione ESPAÇO, ESC ou ENTER para voltar.")
                    time.sleep(0.4)
                    while True:
                        saida = keyboard.read_event()
                        if saida.event_type == keyboard.KEY_DOWN:
                            if saida.name in ['space', 'esc', 'enter']:
                                while keyboard.is_pressed(saida.name): pass
                                return
            time.sleep(0.1)

    def menu_listar(self):
        limpar_tela()
        print("=== TODAS AS PLANTAS CADASTRADAS ===\n")
        if not self.botanico.colecao:
            print("Nenhuma planta no banco de dados.")
        else:
            for p in self.botanico.colecao:
                print(f"[{type(p).__name__}] {p.get_nome_popular()} - {p.get_nome_cientifico()}")
        print("\nPressione ESPAÇO para voltar...")
        keyboard.wait('space')

    def rodar(self):
        while True:
            self.mostrar()
            tecla = keyboard.read_key()
            if tecla == 'up':
                self.selecionado = (self.selecionado - 1) % 3
                time.sleep(0.15)
            elif tecla == 'down':
                self.selecionado = (self.selecionado + 1) % 3
                time.sleep(0.15)
            elif tecla == 'enter':
                while keyboard.is_pressed('enter'): pass
                print("\n   Carregando...")
                time.sleep(0.6)
                if self.selecionado == 0:
                    self.menu_identificar()
                elif self.selecionado == 1:
                    self.menu_listar()
                elif self.selecionado == 2:
                    break
            time.sleep(0.05)