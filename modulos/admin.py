import os 

import matplotlib.pyplot as plt

from .dados import produtos_estoque, servicos_disponiveis, agendamentos, pets_estoque, usuarios 

BACKUP_DIR = 'backups' 


def verifica_float(s):
    if not s: return False
    
    ponto_decimal_encontrado = 0
    i = 0
    while i < len(s):
        verificacao = s[i]
        if verificacao == '.':
            ponto_decimal_encontrado = ponto_decimal_encontrado + 1
            if ponto_decimal_encontrado > 1: return False
        elif verificacao < '0' or verificacao > '9':
            return False
        i = i + 1
            
    if s.strip() == '0' or s.strip() == '0.0': return False
    if s.strip() == '.': return False

    return True

def verifica_int(s):
    if not s: return False
    
    i = 0
    while i < len(s):
        verificacao = s[i]
        if verificacao < '0' or verificacao > '9':
            return False
        i = i + 1
            
    if s[0] == '-': return False
    if len(s) == 0: return False
    
    return True


def formatar_horarios(horarios):
    horarios_str = ''
    tamanho = len(horarios)

    if tamanho > 0:
        i = 0
        while i < tamanho:
            horarios_str = horarios_str + horarios[i]
            if i < tamanho - 1: 
                horarios_str = horarios_str + ', '
            i = i + 1
        return horarios_str
    return 'N/A'


def listar_produtos_e_servicos():
    print('\n=== ITENS CADASTRADOS ===')
    
    print('--- Produtos (Estoque) ---')
    for nome in produtos_estoque: 
        detalhes = produtos_estoque[nome]
        print(f'Produto: {nome} | Preço: R${detalhes["preço"]:.2f} | Estoque: {detalhes["quantidade"]}')
        
    print('--- Pets (Estoque) ---')
    for nome in pets_estoque:
        detalhes = pets_estoque[nome]
        print(f'Pet: {nome} | Preço: R${detalhes["preço"]:.2f} | Estoque: {detalhes["quantidade"]}')

    print('--- Serviços ---')
    for nome in servicos_disponiveis:
        detalhes = servicos_disponiveis[nome]
        horarios_str = formatar_horarios(detalhes['horarios'])
        print(f'Serviço: {nome} | Valor: R${detalhes["valor"]:.2f} | Horários: {horarios_str}')


def cadastrar_item():
    print('\n=== CADASTRO DE NOVO ITEM ===')
    while True:
        tipo = input('Tipo (P=Produto, E=Pet, S=Serviço): ').strip().upper()
        if tipo in ['P', 'E', 'S']:
            break
        print('Opção inválida.')

    nome = input('Nome do item: ').strip().upper()
    
    while True:
        valor_str = input('Valor (R$): ').strip()
        if verifica_float(valor_str):
            valor = float(valor_str)
            break
        print('Valor inválido. Digite um número decimal positivo.')

    if tipo == 'P' or tipo == 'E':
        while True:
            quantidade_str = input('Quantidade em estoque: ').strip()
            if verifica_int(quantidade_str):
                quantidade = int(quantidade_str)
                break
            print('Quantidade inválida. Digite um número inteiro não negativo.')
        
        if tipo == 'P':
            produtos_estoque[nome] = {'preço': valor, 'quantidade': quantidade}
            print(f'Produto {nome} cadastrado com sucesso!')
        else:
            pets_estoque[nome] = {'preço': valor, 'quantidade': quantidade}
            print(f'Pet {nome} cadastrado com sucesso!')

    elif tipo == 'S':
        horarios_str = input('Horários disponíveis (ex: 09:00,10:00 - ou deixe em branco): ').strip()
        
        lista_horarios = () 
        if horarios_str:
            horarios_temp = () 
            temp_horario = ''
            
            i = 0
            s_com_virgula = horarios_str + ','
            while i < len(s_com_virgula):
                verificacao = s_com_virgula[i]
                if verificacao == ',':
                    item_limpo = temp_horario.strip()
                    if len(item_limpo) > 0: 
                        horarios_temp = horarios_temp + (item_limpo,) 
                    temp_horario = ''
                else:
                    temp_horario = temp_horario + verificacao
                i = i + 1
            
            lista_horarios = horarios_temp
        
        servicos_disponiveis[nome] = {'valor': valor, 'horarios': lista_horarios}
        print(f'Serviço {nome} cadastrado com sucesso!')


def atualizar_item():
    print('\n=== ATUALIZAR ITEM ===')
    listar_produtos_e_servicos()
    nome_item = input('Digite o NOME do item a ser atualizado: ').strip().upper()
    
    detalhes = 0
    if nome_item in produtos_estoque:
        detalhes = produtos_estoque[nome_item]
    elif nome_item in pets_estoque:
        detalhes = pets_estoque[nome_item]
    elif nome_item in servicos_disponiveis:
        detalhes = servicos_disponiveis[nome_item]
        
    if detalhes:
        print(f'Atualizando: {nome_item}')

        while True:
            novo_valor_str = input('Novo preço/valor (deixe em branco para manter): ').strip()
            if not novo_valor_str:
                break
            
            if verifica_float(novo_valor_str):
                novo_valor = float(novo_valor_str)
                if 'preço' in detalhes:
                    detalhes['preço'] = novo_valor
                if 'valor' in detalhes:
                    detalhes['valor'] = novo_valor
                break
            print('Valor inválido. Digite um número decimal positivo.')

        if nome_item in produtos_estoque or nome_item in pets_estoque:
            while True:
                nova_qtd_str = input('Nova quantidade em estoque (deixe em branco para manter): ').strip()
                if not nova_qtd_str:
                    break
                
                if verifica_int(nova_qtd_str):
                    detalhes['quantidade'] = int(nova_qtd_str)
                    break
                print('Quantidade inválida. Digite um número inteiro não negativo.')
        
        if nome_item in servicos_disponiveis:
            novos_horarios_str = input('Novos horários (09:00,10:00 - deixe em branco para manter): ').strip()
            if novos_horarios_str:
                horarios_temp = ()
                temp_horario = ''
                
                i = 0
                s_com_virgula = novos_horarios_str + ','
                while i < len(s_com_virgula):
                    verificacao = s_com_virgula[i]
                    if verificacao == ',':
                        item_limpo = temp_horario.strip()
                        if len(item_limpo) > 0: 
                            horarios_temp = horarios_temp + (item_limpo,)
                        temp_horario = ''
                    else:
                        temp_horario = temp_horario + verificacao
                    i = i + 1
                
                detalhes['horarios'] = horarios_temp
                    
        print(f'Item {nome_item} atualizado com sucesso!')
            
    else:
        print('Item não encontrado.')


def remover_item():
    print('\n=== REMOVER ITEM ===')
    listar_produtos_e_servicos()
    nome_item = input('Digite o NOME do item a ser removido: ').strip().upper()
    
    if nome_item in produtos_estoque:
        del produtos_estoque[nome_item]
        print(f'Produto {nome_item} removido!')
    elif nome_item in pets_estoque:
        del pets_estoque[nome_item]
        print(f'Pet {nome_item} removido!')
    elif nome_item in servicos_disponiveis:
        del servicos_disponiveis[nome_item]
        print(f'Serviço {nome_item} removido!')
    else:
        print('Item não encontrado.')


def buscar_item():
    print('\n=== BUSCAR ITEM ===')
    termo = input('Digite o nome ou parte do nome do item: ').strip().upper()
    encontrados = {}
    i = 0
    
    for nome in produtos_estoque:
        if termo in nome:
            detalhes = produtos_estoque[nome]
            encontrados[i] = f'PRODUTO: {nome} | Preço: R${detalhes["preço"]:.2f} | Estoque: {detalhes["quantidade"]}'
            i = i + 1
            
    for nome in pets_estoque:
        if termo in nome:
            detalhes = pets_estoque[nome]
            encontrados[i] = f'PET: {nome} | Preço: R${detalhes["preço"]:.2f} | Estoque: {detalhes["quantidade"]}'
            i = i + 1

    for nome in servicos_disponiveis:
        if termo in nome:
            detalhes = servicos_disponiveis[nome]
            horarios_str = formatar_horarios(detalhes['horarios'])
            encontrados[i] = f'SERVIÇO: {nome} | Valor: R${detalhes["valor"]:.2f} | Horários: {horarios_str}'
            i = i + 1
            
    if i > 0:
        print('\nResultados da busca:')
        for _, item in encontrados.items():
            print(f'- {item}')
    else:
        print('Nenhum item encontrado com esse termo.')


def listar_agendamentos_admin():
    print('\n=== LISTA DE TODOS OS AGENDAMENTOS ===')
    
    tamanho_agendamentos = len(agendamentos)

    if tamanho_agendamentos == 0:
        print('Nenhum agendamento realizado.')
        return
    
    i = 0
    while i < tamanho_agendamentos:
        ag = agendamentos[i]
        
        horario = 'N/A'
        if 'horario' in ag:
            horario = ag['horario']
            
        print(f'{i+1} - Cliente: {ag["cliente_email"]} | Serviço: {ag["servico"]} | Data: {ag["data"]} | Horário: {horario}')
        i = i + 1


def relatorio_estoque_baixo():
    print('\n=== RELATÓRIO DE ESTOQUE BAIXO ===')
    estoque_baixo = {}
    i = 0
    
    for nome in produtos_estoque:
        detalhes = produtos_estoque[nome]
        if detalhes['quantidade'] < 5:
            estoque_baixo[i] = f'Produto: {nome} | Quantidade: {detalhes["quantidade"]}'
            i = i + 1
            
    for nome in pets_estoque:
        detalhes = pets_estoque[nome]
        if detalhes['quantidade'] < 5:
            estoque_baixo[i] = f'Pet: {nome} | Quantidade: {detalhes["quantidade"]}'
            i = i + 1
            
    if i > 0:
        for _, item in estoque_baixo.items():
            print(f'- {item}')
    else:
        print('Nenhum item com estoque abaixo de 5.')

def fazer_backup():
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
        
    print('\n=== GERANDO BACKUP DE DADOS ===')
    with open(os.path.join(BACKUP_DIR, 'usuarios_backup.txt'), 'w', encoding='utf-8') as usuarios_backup:
        usuarios_backup.write("--- LISTA DE USUÁRIOS ---\n")
        usuarios_backup.write(str(usuarios)) 
    print('- Usuários salvos em usuarios_backup.txt')

    produtos_completo = {}
    for chave in produtos_estoque:
        produtos_completo[chave] = produtos_estoque[chave]
    for chave in pets_estoque:
        produtos_completo[chave] = pets_estoque[chave]
        
    with open(os.path.join(BACKUP_DIR, 'produtos_backup.txt'), 'w', encoding='utf-8') as produtos_pets_backup:
        produtos_pets_backup.write("--- LISTA DE PRODUTOS E PETS ---\n")
        produtos_pets_backup.write(str(produtos_completo))
    print('- Produtos e Pets salvos em produtos_backup.txt')

    with open(os.path.join(BACKUP_DIR, 'servicos_backup.txt'), 'w', encoding='utf-8') as servicos_backup:
        servicos_backup.write("--- LISTA DE SERVIÇOS ---\n")
        servicos_backup.write(str(servicos_disponiveis))
    print('- Serviços salvos em servicos_backup.txt')
    
    print('\nBackup de dados concluído com sucesso!')

def importar_backup():
    print('\n=== IMPORTANDO DADOS DE BACKUP (SIMULAÇÃO) ===')
    
    arquivo_existe = os.path.exists(os.path.join(BACKUP_DIR, 'usuarios_backup.txt'))
    if not arquivo_existe:
        print('Erro: Arquivos de backup não encontrados. Usando dados de teste.')
        
    dados_simulados_usuarios = (
        {'nome': 'Cliente Teste', 'tipo': 'CLIENTE', 'email': 'importado@teste.com', 'senha': '123'},
    )
    dados_simulados_produtos = {
        'RAÇÃO NOVA': {'preço': 55.0, 'quantidade': 20}
    }
    
    usuarios[:] = dados_simulados_usuarios
    produtos_estoque.clear()
    
    for chave in dados_simulados_produtos:
        produtos_estoque[chave] = dados_simulados_produtos[chave]
    
    print('AVISO: Dados importados de um conjunto de TESTE.')


def simular_analise_rentabilidade():
    print('\n=== ANÁLISE DE RENTABILIDADE COM GRÁFICO ===')
    
    while True:
        custo_str = input('Digite o Custo de Aquisição Unitário (R$): ').strip()
        if verifica_float(custo_str):
            custo = float(custo_str)
            break
        print('Valor de Custo inválido. Digite um número decimal positivo.')
    
    while True:
        preco_str = input('Digite o Preço de Venda Unitário (R$): ').strip()
        if verifica_float(preco_str):
            preco_venda = float(preco_str)
            break
        print('Valor de Venda inválido. Digite um número decimal positivo.')

    while True:
        unidades_str = input('Digite as Unidades Vendidas (inteiro): ').strip()
        if verifica_int(unidades_str):
            unidades = int(unidades_str)
            break
        print('Unidades inválidas. Digite um número inteiro não negativo.')
    
    lucro_unitario = preco_venda - custo
    lucro_total = lucro_unitario * unidades
    margem_percentual = 0.0
    
    if preco_venda > 0.0:
        margem_percentual = (lucro_unitario / preco_venda) * 100

    print('\n--- Resultados da Análise ---')
    print(f'Lucro Unitário: R${lucro_unitario:.2f}')
    print(f'Lucro Total Gerado: R${lucro_total:.2f}')
    print(f'Margem Bruta (%): {margem_percentual:.2f}%')
    
    if margem_percentual >= 30.0:
        rentabilidade_status = 'ALTA (Acima de 30%)'
    elif margem_percentual >= 15.0:
        rentabilidade_status = 'MÉDIA'
    else:
        rentabilidade_status = 'BAIXA (Abaixo de 15%)'

    print(f'Status de Rentabilidade: {rentabilidade_status}')
    print('-------------------------------------------')

    if lucro_unitario > 0:
        labels = 'Custo', 'Lucro'
        sizes = [custo, lucro_unitario]
        
        fig1, ax1 = plt.subplots()
        
        ax1.pie(
            sizes, 
            labels=labels, 
            autopct='%1.1f%%', 
            startangle=90,
            colors=['#ff9999', '#66b3ff']
        )
        
        ax1.set_title(f'Divisão Custo vs Lucro (Margem Bruta: {margem_percentual:.2f}%)')
        ax1.axis('equal') 
        
        print('\nGerando gráfico de rentabilidade...')
        plt.show() 
        print('Gráfico exibido com sucesso!')
    else:
        print('Não é possível gerar gráfico de pizza, pois o lucro não é positivo.')
    print('-------------------------------------------')


def menu_admin(usuario):
    while True:
        print('\n\n======= MENU ADMINISTRADOR =======')
        print(f'Bem-vindo, {usuario["nome"]}!')
        print('1 - Cadastrar Produto/Pet/Serviço')
        print('2 - Buscar Item')
        print('3 - Atualizar Item')
        print('4 - Remover Item')
        print('5 - Listar Todos os Itens')
        print('6 - Lista de Agendamentos')
        print('7 - Relatório de Estoque Baixo')
        print('8 - Gerar Arquivos de Backup')
        print('9 - Importar Dados de Backup')
        print('10 - Análise de Rentabilidade')
        print('0 - Sair')
        
        opcao = input('Escolha uma opção: ').strip()

        if opcao == '1':
            cadastrar_item()
        elif opcao == '2':
            buscar_item()
        elif opcao == '3':
            atualizar_item()
        elif opcao == '4':
            remover_item()
        elif opcao == '5':
            listar_produtos_e_servicos()
        elif opcao == '6':
            listar_agendamentos_admin()
        elif opcao == '7':
            relatorio_estoque_baixo()
        elif opcao == '8':
            fazer_backup() 
        elif opcao == '9':
            fazer_backup() 
        elif opcao == '10':
            simular_analise_rentabilidade()
        elif opcao == '0':
            print('Você voltou ao menu pricipal.')
            break
        else:
            print('Opção inválida!')