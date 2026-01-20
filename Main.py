from BotanicoVirtual import *
from Menu import *



if __name__ == "__main__":
    # 1. Instancia o gerenciador (BotanicoVirtual) com o caminho do seu JSON
    meu_botanico = BotanicoVirtual("plantas.json")

    # 2. Instanc
    # ia o Menu passando o botanico
    menu = MenuPrincipal(meu_botanico)

    # 3. Roda o sistema
    menu.rodar()

