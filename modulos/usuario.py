from .dados import usuarios

def cadastrar_usuario():
    print('\n=== CADASTRO DE NOVO USUÁRIO ===')
    nome = input('Nome: ').strip()
    nascimento = input('Data de Nascimento: ').strip()
    
    while True:
        tipo = input('Tipo (Admin ou Cliente): ').strip().upper()
        if tipo in ['ADMIN', 'CLIENTE']:
            break
        print('Tipo inválido. Digite "Admin" ou "Cliente".')

    while True:
        email_cadastro = input('E-mail: ').strip()
        if '@' in email_cadastro and '.' in email_cadastro:
            email_existe = False
            for u in usuarios: 
                if u['email'] == email_cadastro:
                    email_existe = True
                    break
            
            if email_existe:
                print('E-mail já cadastrado. Tente outro.')
            else:
                break
        else:
            print('E-mail inválido! Deve conter "@" e ".".')

    senha_cadastro = input('Senha: ').strip()
    
    novo_usuario = {
        'nome': nome, 
        'nascimento': nascimento, 
        'tipo': tipo, 
        'email': email_cadastro, 
        'senha': senha_cadastro
    }
    usuarios.append(novo_usuario)
    print('Usuário ' + nome + ' (' + tipo + ') cadastrado com sucesso!')

def login():
    print('\n=== LOGIN ===')
    email_login = input('E-mail: ').strip()
    senha_login = input('Senha: ').strip()
    
    for usuario in usuarios:
        if usuario['email'] == email_login and usuario['senha'] == senha_login:
            print('Login realizado com sucesso! Bem-vindo(a), ' + usuario["nome"] + '!')
            return usuario  
    
    print('E-mail ou senha inválidos! Tente novamente.')
    return 0