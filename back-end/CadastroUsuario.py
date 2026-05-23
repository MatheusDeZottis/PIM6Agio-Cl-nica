# Cadastro de usuário
import hashlib #Importa a biblioteca para criptografar a senha

# Solicitar informações do usuário
nome_usuario = input ("Digite o nome do usuário: ")
email_usuario = input ("Digite o email do usuário: ")
senha_usuario = input ("Digite a senha do usuário: ")

# Criptografa a senha
senha_hash = hashlib.sha256(senha_usuario.encode('utf-8')).hexdigest()

# Apresentar os tipos de usuários disponíveis
print("\nSelecione o tipo de usuário:")
print("1 - Administrador (ADMIN)")
print("2 - Médico (MEDICO)")
print("3 - Recepcionista (RECEPCAO)")
print("4 - Enfermeiro (ENFERMEIRO)")

# Solicitar a escolha do tipo de usuário
tipo_usuario = input("Digite o número correspondente ao tipo de usuário: ")

# Solicitar registro profissional para médicos e enfermeiros
registro_profissional = None

if tipo_usuario == "2":
    print (f"Digite o CRM do médico {nome_usuario}: ")
    registro_profissional = input()
elif tipo_usuario == "4":
    print (f"Digite o COREN do enfermeiro {nome_usuario}: ")
    registro_profissional = input()
  
   
    # Mostra como o cadastro ficou estruturado no final
print("\n--- USUÁRIO CADASTRADO COM SUCESSO ---")
print (f"{nome_usuario}")
print (f"{email_usuario}")
if tipo_usuario == "1":
    print ("1-Administrador")
elif tipo_usuario == "2":
    print (f"2-Médico - CRM: {registro_profissional}")
elif tipo_usuario == "3":
    print ("3-Recepcionista")
elif tipo_usuario == "4":
    print (f"4-Enfermeiro - COREN: {registro_profissional}")

print (f"Senha criptografada: {senha_hash}")
