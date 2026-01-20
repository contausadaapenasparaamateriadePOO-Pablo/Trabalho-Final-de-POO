from abc import ABC, abstractmethod

class Planta(ABC):
    def __init__(self, nomePopular, nomeCientifico, familia, fruto, habitat, descricao, cheiro=None, curiosidades=None):
        self.__nomePopular = nomePopular
        self.__nomeCientifico = nomeCientifico
        self.__familia = familia
        self.__fruto = fruto
        self.__habitat = habitat
        self.__descricao = descricao
        self.__cheiro = cheiro if cheiro else "Sem cheiro característico."
        self.__curiosidades = curiosidades if curiosidades else "Informações não disponíveis."

    # Métodos Getters para permitir que as filhas acessem os dados privados
    def get_nome_popular(self): return self.__nomePopular
    def get_nome_cientifico(self): return self.__nomeCientifico
    def get_familia(self): return self.__familia
    def get_fruto(self): return self.__fruto
    def get_habitat(self): return self.__habitat
    def get_descricao(self): return self.__descricao
    def get_cheiro(self): return self.__cheiro
    def get_curiosidades(self): return self.__curiosidades

    @abstractmethod
    def exibirFicha(self):
        pass

class Suculento(Planta):
    def __init__(self, nomePopular, nomeCientifico, familia, fruto, habitat, descricao, tipoEspinho, cheiro=None, curiosidades=None):
        super().__init__(nomePopular, nomeCientifico, familia, fruto, habitat, descricao, cheiro, curiosidades)
        self.__tipoEspinho = tipoEspinho

    def exibirFicha(self):
        print('_' * 80 + '\n' +
              f'Nome Popular: {self.get_nome_popular()}\n' +
              f'Cientifico: {self.get_nome_cientifico()}\n' +
              f'Familia: {self.get_familia()}\n' +
              f'Habitat: {self.get_habitat()}\n' +
              f'\nDescrição Visual: {self.get_descricao()}\n' +
              f'Tipo Espinho: {self.__tipoEspinho}\n' +
              f'\nCheiro: {self.get_cheiro()}\n' +
              f'\nCuriosidades: {self.get_curiosidades()}\n')

class Arboreo(Planta):
    def __init__(self, nomePopular, nomeCientifico, familia, fruto, habitat, descricao, alturaCopa, cheiro=None, curiosidades=None):
        super().__init__(nomePopular, nomeCientifico, familia, fruto, habitat, descricao, cheiro, curiosidades)
        self.__alturaCopa = alturaCopa

    def exibirFicha(self):
        print('_' * 80 + '\n' +
              f'Nome Popular: {self.get_nome_popular()}\n' +
              f'Cientifico: {self.get_nome_cientifico()}\n' +
              f'Familia: {self.get_familia()}\n' +
              f'Habitat: {self.get_habitat()}\n' +
              f'\nDescrição Visual: {self.get_descricao()}\n' +
              f'Altura Copa: {self.__alturaCopa}\n' +
              f'\nCheiro: {self.get_cheiro()}\n' +
              f'\nCuriosidades: {self.get_curiosidades()}\n')

class Trepadeira(Planta):
    def __init__(self, nomePopular, nomeCientifico, familia, fruto, habitat, descricao, mecanismoFixacao, cheiro=None, curiosidades=None):
        super().__init__(nomePopular, nomeCientifico, familia, fruto, habitat, descricao, cheiro, curiosidades)
        self.__mecanismoFixacao = mecanismoFixacao

    def exibirFicha(self):
        print('_' * 80 + '\n' +
              f'Nome Popular: {self.get_nome_popular()}\n' +
              f'Cientifico: {self.get_nome_cientifico()}\n' +
              f'Familia: {self.get_familia()}\n' +
              f'Habitat: {self.get_habitat()}\n' +
              f'\nDescrição Visual: {self.get_descricao()}\n' +
              f'Mecanismo Fixacao: {self.__mecanismoFixacao}\n' +
              f'\nCheiro: {self.get_cheiro()}\n' +
              f'\nCuriosidades: {self.get_curiosidades()}\n')

class Herbaceas(Planta):
    def __init__(self, nomePopular, nomeCientifico, familia, fruto, habitat, descricao, corFlor, cheiro=None, curiosidades=None):
        super().__init__(nomePopular, nomeCientifico, familia, fruto, habitat, descricao, cheiro, curiosidades)
        self.__corFlor = corFlor

    def exibirFicha(self):
        print('_' * 80 + '\n' +
              f'Nome Popular: {self.get_nome_popular()}\n' +
              f'Cientifico: {self.get_nome_cientifico()}\n' +
              f'Familia: {self.get_familia()}\n' +
              f'Habitat: {self.get_habitat()}\n' +
              f'\nDescrição Visual: {self.get_descricao()}\n' +
              f'Cor da Flor: {self.__corFlor}\n' +
              f'\nCheiro: {self.get_cheiro()}\n' +
              f'\nCuriosidades: {self.get_curiosidades()}\n')