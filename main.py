import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modulos.usuario import cadastrar_usuario, login
from modulos.admin import menu_admin
from modulos.cliente import menu_cliente
from modulos.dados import usuarios

if not usuarios:
    usuarios.append({
        'nome': 'Admin Padrão', 
        'nascimento': '01/01/2000', 
        'tipo': 'ADMIN', 
        'email': 'admin@petsertao.com', 
        'senha': '123'
    })
    print("ADM Padrão criado: admin@petsertao.com / 123")

def main():
    while True:
        print('\n\n=============================================')
        print('=======  BEM-VINDO AO PETSERTÃO  =======')
        print('=============================================')
        print('1 - Login (Acesso a ADM e Cliente)')
        print('2 - Cadastrar Novo Usuário')
        print('0 - Sair do Sistema')
        
        opcao = input('Escolha a opção desejada: ').strip()

        if opcao == '1':
            usuariologado = login()
            
            if usuariologado:
                if usuariologado['tipo'] == 'ADMIN':
                    print("Acesso de ADMINISTRADOR concedido.")
                    menu_admin(usuariologado)
                elif usuariologado['tipo'] == 'CLIENTE':
                    print("Acesso de CLIENTE concedido.")
                    menu_cliente(usuariologado)
                else:
                    print("Erro: Tipo de usuário desconhecido.")
        
        elif opcao == '2':
            cadastrar_usuario()
            
        elif opcao == '0':
            print('Saindo do sistema. Até logo!')
            break
            
        else:
            print('Opção inválida! Tente novamente.')

if __name__ == '__main__':
    main()