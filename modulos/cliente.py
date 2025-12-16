from .dados import produtos_estoque, servicos_disponiveis, agendamentos, pets_estoque
from .admin import verifica_int 


def formatar_data(data_str):
    if len(data_str) != 10:
        return False
        
    for i in range(10):
        verificacao = data_str[i]
        if i in [2, 5]:
            if verificacao != '/':
                return False
        elif verificacao < '0' or verificacao > '9':
            return False
            
    dia_str = data_str[0] + data_str[1]
    mes_str = data_str[3] + data_str[4]
    
    if int(dia_str) > 31 or int(mes_str) > 12:
        return False
        
    return True

def exibir_carrinho(carrinho):
    if not carrinho:
        print('\nCarrinho vazio.')
        return 0
        
    print('\n=== ITENS NO CARRINHO ===')
    total = 0
    for i in range(len(carrinho)):
        item = carrinho[i]
        print(str(i+1) + ' - [' + item[0] + '] ' + item[1] + ' | R$' + str(item[2]))
        total += item[2]
    return total

def comprar_item(carrinho):
    print('\n=== COMPRA DE ITENS ===')
    print('--- Produtos ---')
    for nome in produtos_estoque:
        detalhes = produtos_estoque[nome]
        print('Produto: ' + nome + ' | Preço: R$' + str(detalhes['preço']) + ' | Estoque: ' + str(detalhes['quantidade']))

    print('--- Pets ---')
    for nome in pets_estoque:
        detalhes = pets_estoque[nome]
        print('Pet: ' + nome + ' | Preço: R$' + str(detalhes['preço']) + ' | Estoque: ' + str(detalhes['quantidade']))

    nome_item = input('Digite o nome do Produto/Pet para adicionar ao carrinho (ou 0 para voltar): ').strip().upper()
    
    if nome_item == '0':
        return

    detalhes = 0
    tipo = ''
    
    if nome_item in produtos_estoque:
        detalhes = produtos_estoque[nome_item]
        tipo = 'Produto'
    elif nome_item in pets_estoque:
        detalhes = pets_estoque[nome_item]
        tipo = 'Pet'
    
    if detalhes:
        if detalhes['quantidade'] > 0:
            carrinho.append((tipo, nome_item, detalhes['preço']))
            detalhes['quantidade'] = detalhes['quantidade'] - 1 
            print(tipo + ' ' + nome_item + ' adicionado ao carrinho.')
        else:
            print('Estoque de ' + nome_item + ' esgotado.')
    else:
        print('Item não encontrado.')


def agendar_servico(cliente_email, carrinho):
    print('\n=== AGENDAMENTO DE SERVIÇOS ===')
    
    servicos_disponiveis = []
    
    print('\nServiços disponíveis:')
    for nome in servicos_disponiveis: 
        servicos_disponiveis.append(nome)
        detalhes = servicos_disponiveis[nome]
        
        horarios_str = ''
        if detalhes['horarios']:
            lista_horarios = detalhes['horarios']
            tamanho = len(lista_horarios)
            for i in range(tamanho):
                horarios_str = horarios_str + lista_horarios[i]
                if i < tamanho - 1:
                    horarios_str = horarios_str + ', '
        else:
            horarios_str = 'N/A'
            
        print('[' + nome + '] | Valor: R$' + str(detalhes['valor']) + ' | Horários disponíveis: ' + horarios_str)

    nome_servico = input('Digite o NOME do serviço que deseja agendar (ou 0 para voltar): ').strip().upper()
    
    if nome_servico == '0':
        return
        
    if nome_servico in servicos_disponiveis:
        servico_detalhes = servicos_disponiveis[nome_servico]
        
        while True:
            data_agendamento = input('Digite a Data do serviço (DD/MM/AAAA): ').strip()
            if formatar_data(data_agendamento):
                break
            print('Formato de data inválido (Use DD/MM/AAAA).')

        while True:
            horario_agendamento = input('Digite o Horário (ex: 10:00). Escolha entre: ' + horarios_str + ' : ').strip()
            horario_valido = False
            lista_horarios = servico_detalhes['horarios']
            for h in lista_horarios:
                if h == horario_agendamento:
                    horario_valido = True
                    break
            
            if horario_valido:
                break
            print('Horário inválido ou não disponível para este serviço.')

        agendamentos.append({
            'cliente_email': cliente_email,
            'servico': nome_servico,
            'data': data_agendamento,
            'horario': horario_agendamento,
            'status': 'AGENDADO'
        })
        
        carrinho.append(('Serviço', nome_servico, servico_detalhes['valor']))
        
        print('\nServiço ' + nome_servico + ' agendado e adicionado ao carrinho para pagamento.')
        
    else:
        print('Serviço não encontrado.')


def finalizar_compra(carrinho, cliente_email):
    if not carrinho:
        print('\nCarrinho vazio. Nada para finalizar.')
        return

    total = exibir_carrinho(carrinho)
    print('\nTOTAL A PAGAR: R$' + str(total))
    
    confirmar = input('Confirmar pagamento? (S/N): ').strip().upper()
    
    if confirmar == 'S':
        print('Pagamento processado com sucesso!')
        print('Recibo enviado para: ' + cliente_email)
        carrinho[:] = []
    else:
        print('Compra cancelada.')


def listar_agendamentos_cliente(cliente_email):
    print('\n=== MEUS AGENDAMENTOS ===')
    encontrados = []
    
    for agendamento in agendamentos:
        if agendamento['cliente_email'] == cliente_email:
            encontrados.append(agendamento)
            
    if not encontrados:
        print('Você não possui agendamentos.')
        return
        
    for i in range(len(encontrados)):
        ag = encontrados[i]
        horario = ag['horario'] if ag['horario'] else 'N/A'
        print(str(i+1) + ' - Serviço: ' + ag['servico'] + ' | Data: ' + ag['data'] + ' | Horário: ' + horario + ' | Status: ' + ag['status'])
 

def menu_cliente(usuario):
    carrinho = []
    cliente_email = usuario['email']

    while True:
        print('\n\n======= MENU CLIENTE =======')
        print('Bem-vindo, ' + usuario['nome'] + '!')
        print('1 - Comprar Produtos/Pets')
        print('2 - Agendar Serviço')
        print('3 - Visualizar Carrinho (' + str(len(carrinho)) + ' itens)')
        print('4 - Finalizar Compra')
        print('5 - Meus Agendamentos')
        print('0 - Sair')
        
        opcao = input('Escolha uma opção: ').strip()

        if opcao == '1':
            comprar_item(carrinho)
        elif opcao == '2':
            agendar_servico(cliente_email, carrinho)
        elif opcao == '3':
            exibir_carrinho(carrinho)
        elif opcao == '4':
            finalizar_compra(carrinho, cliente_email)
        elif opcao == '5':
            listar_agendamentos_cliente(cliente_email)
        elif opcao == '0':
            print('Você voltou ao menu pricipal')
            break
        else:
            print('Opção inválida!')