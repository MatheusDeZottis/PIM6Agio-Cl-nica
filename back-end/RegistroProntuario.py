# Módulo de Registro de Prontuário Clínico — Ágil Clínica
from datetime import datetime
import json

# ============================================================
# FUNÇÃO DA REGRA DE NEGÓCIO
# ============================================================

def estruturar_prontuario_medico(id_paciente: int, crm_medico: str, queixa: str, 
                                 pressao_arterial: str, temperatura: float, 
                                 diagnostico: str, prescricao: list) -> dict:
    """
    Valida os dados da consulta, monta o prontuário em formato de documento 
    dinâmico e prepara o objeto para inserção na tabela 'prontuarios_clinicos'.
    """
    # 1. Validação de Regras de Negócio Obrigatórias
    if not crm_medico.strip():
        raise ValueError("O CRM do médico é obrigatório para assinar o prontuário.")
    if not queixa.strip():
        raise ValueError("A queixa principal do paciente deve ser preenchida.")
    if not diagnostico.strip():
        raise ValueError("O diagnóstico clínico é obrigatório para encerrar a consulta.")

    # 2. Montagem da Estrutura Semiestruturada (Dicionário que vira JSON)
    # Copia exatamente o layout de chaves que definimos nos inserts do SQL Server
    dados_atendimento = {
        "crm_medico": crm_medico.strip().upper(),
        "data_hora_atendimento": datetime.now().isoformat() + "Z", # Padrão UTC internacional
        "queixa_principal": queixa.strip(),
        "sinais_vitais": {
            "pressao_arterial": pressao_arterial.strip(),
            "temperatura_celsius": float(temperatura)
        },
        "diagnostico": diagnostico.strip(),
        "prescricao": prescricao # Lista de dicionários com os medicamentos
    }

    # 3. Preparação para o Banco de Dados
    # O SQL Server recebe o JSON como uma String/Texto longo (VARCHAR(MAX))
    # Usamos o json.dumps para transformar o dicionário Python em uma String JSON válida
    dados_atendimento_string_json = json.dumps(dados_atendimento, ensure_ascii=False)

    registro_final = {
        "id_paciente": id_paciente, # Chave Estrangeira (FK)
        "dados_atendimento": dados_atendimento_string_json
    }

    return registro_final

# ============================================================
# SIMULAÇÃO DO FLUXO NO CONSULTÓRIO MÉDICO (TERMINAL)
# ============================================================

print("--- SISTEMA ÁGIL CLÍNICA: MÓDULO DE PRONTUÁRIO CLÍNICO ---")

# Simulando que o médico buscou o paciente da fila de agendamentos
id_paciente_atendido = 1  # Ex: Matheus Coutinho (recuperado do agendamento)
crm_medico_logado = "CRM-GO12345"

print(f"\nMédico Autenticado: {crm_medico_logado}")
print(f"Atendendo Paciente ID: {id_paciente_atendido}")
print("-" * 50)

# Entrada de dados da consulta
queixa_input = input("Queixa Principal: ")
pa_input = input("Sinais Vitais - Pressão Arterial (ex: 120/80): ")
temp_input = input("Sinais Vitais - Temperatura (°C): ")
diagnostico_input = input("Diagnóstico Clínico: ")

# Coleta dinâmica de medicamentos (Prescrição)
lista_prescricao = []
print("\n--- Prescrição Médica (Deixe o nome em branco para encerrar) ---")

while True:
    nome_medicamento = input("Nome do Medicamento: ")
    if not nome_medicamento.strip():
        break # Sai do laço se o médico apenas apertar Enter
        
    dosagem = input("Dosagem (ex: 500mg): ")
    frequencia = input("Frequência (ex: De 8 em 8 horas): ")
    
    # Adiciona o medicamento na lista temporária
    lista_prescricao.append({
        "medicamento": nome_medicamento.strip(),
        "dosagem": dosagem.strip(),
        "frequencia": frequencia.strip()
    })

# Processamento e Fechamento do Prontuário
try:
    prontuario_final = estruturar_prontuario_medico(
        id_paciente=id_paciente_atendido,
        crm_medico=crm_medico_logado,
        queixa=queixa_input,
        pressao_arterial=pa_input,
        temperatura=float(temp_input),
        diagnostico=diagnostico_input,
        prescricao=lista_prescricao
    )
    
    print("\n[✓] PRONTUÁRIO CONCLUÍDO E ASSINADO COM SUCESSO!")
    print("\n--- OBJETO ESTRUTURADO PARA ENVIO AO SQL SERVER ---")
    print(f"ID Paciente (FK): {prontuario_final['id_paciente']}")
    print(f"Texto JSON gerado para a coluna 'dados_atendimento':\n{prontuario_final['dados_atendimento']}")

except ValueError as erro:
    print(f"\n[X] Erro Crítico ao validar prontuário: {erro}")