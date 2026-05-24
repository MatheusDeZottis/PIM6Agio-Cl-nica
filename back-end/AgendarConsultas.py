# Módulo de Agendamento e Triagem — Ágil Clínica
from datetime import datetime



def buscar_paciente_por_cpf(banco_pacientes: list, cpf_busca: str) -> dict:
    
    #Varr11122233344e a base de dados de pacientes procurando pelo CPF informado e retorna o dicionário do paciente se encontrado, ou None se não existir.
    
    # Remove espaços em branco que o usuário possa ter digitado sem querer
    cpf_limpo = cpf_busca.strip()
    
    for paciente in banco_pacientes:
        if paciente["cpf"] == cpf_limpo:
            return paciente  # Paciente encontrado! Retorna os dados dele.
            
    return None  # Se percorrer toda a lista e não achar, retorna None


def registrar_agendamento_fila(id_paciente: int, classificacao: str) -> dict:
    """
    Recebe o ID do paciente validado e os dados da triagem, 
    estruturando o registro para a tabela 'agendamentos_fila'.
    """
    classificacoes_validas = ['EMERGENCIA', 'URGENTE', 'POUCO_URGENTE', 'NAO_URGENTE']
    classificacao = classificacao.upper().strip()
    
    if classificacao not in classificacoes_validas:
        raise ValueError(f"Classificação inválida. Escolha entre: {classificacoes_validas}")
        
    # Monta o registro exatamente como a tabela do SQL Server espera
    # O 'id_agendamento' não entra aqui pois é IDENTITY no banco de dados
    novo_agendamento = {
        "id_paciente": id_paciente, # Chave Estrangeira (FK) amarrada com sucesso
        "data_hora_chegada": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "classificacao_risco": classificacao,
        "status_atendimento": "AGUARDANDO"
    }
    
    return novo_agendamento

# ============================================================
# SIMULAÇÃO DO FLUXO NO TERMINAL (PROCESSO DA RECEPÇÃO)
# ============================================================

# Simulação de dados já existentes no banco de dados do SQL Server
MOCK_BANCO_PACIENTES = [
    {"id_paciente": 1, "cpf": "11122233344", "nome": "Matheus Coutinho de Souza", "telefone": "62999998888"},
    {"id_paciente": 2, "cpf": "55566677788", "nome": "Jeferson Cruz Almeida", "telefone": "62988887777"}
]

print("--- SISTEMA ÁGIL CLÍNICA: MÓDULO DE AGENDAMENTO E TRIAGEM ---")

# Passo 1: Solicita o CPF para buscar no banco de dados
cpf_digitado = input("Digite o CPF do paciente para iniciar o agendamento: ")

# Executa a função de busca
paciente_encontrado = buscar_paciente_por_cpf(MOCK_BANCO_PACIENTES, cpf_digitado)

# Passo 2: Condicional de verificação
if paciente_encontrado:
    print(f"\n[✓] Paciente Encontrado: {paciente_encontrado['nome']}")
    print(f"    ID Interno do Banco: {paciente_encontrado['id_paciente']}")
    
    # Passo 3: Se o paciente existe, prossegue para a Triagem/Agendamento
    print("\n--- INICIAR TRIAGEM CLÍNICA ---")
    print("Opções: EMERGENCIA, URGENTE, POUCO_URGENTE, NAO_URGENTE")
    risco = input("Digite a classificação de risco do paciente: ")
    
    try:
        # Gera o agendamento vinculando o ID do paciente encontrado
        agendamento_final = registrar_agendamento_fila(
            id_paciente=paciente_encontrado["id_paciente"], 
            classificacao=risco
        )
        
        # Passo 4: Sucesso
        print("\n--- AGENDAMENTO ESTRUTURADO COM SUCESSO ---")
        print(agendamento_final)
        print("\n* O objeto acima está pronto para ser enviado ao SQL Server,")
        print(f"  onde a FK 'id_paciente' apontará corretamente para o registro de {paciente_encontrado['nome']}.")
        
    except ValueError as erro:
        print(f"\n[X] Erro no agendamento: {erro}")
        
else:
    print("\n[X] Erro: Paciente não encontrado com o CPF informado.")
    print("Por favor, realize primeiro o cadastro do paciente no módulo 'CadastroPaciente.py'.")