import os
import shutil
import pyodbc
from datetime import datetime

# 📂 Caminhos dos bancos de dados
caminho_main = r"E:\\python_flask\\database\\Controle_Frequencia.accdb"
caminho_oculto = r"E:\\python_flask\\database\\Controle_Frequencia_oculto.accdb"
caminho_log_backup = r"E:\\python_flask\\database\\backups\\backup_log.accdb"
pasta_backups = r"E:\\python_flask\\database\\backups\\consultas_backup"


# 🛠 Criar estrutura de pastas se não existir
def criar_estrutura_pastas():
    if not os.path.exists(pasta_backups):
        os.makedirs(pasta_backups)
        print(f"📁 Pasta criada: {pasta_backups}")

# 🔄 Sincronização RAID 1 (Copia e Sobrescreve os Arquivos)
def sincronizar_arquivos():
    """Mantém `arquivo_main.accdb` e `arquivo_oculto.accdb` sempre idênticos."""
    if not os.path.exists(caminho_main) and os.path.exists(caminho_oculto):
        shutil.copy2(caminho_oculto, caminho_main)
        print("🟢 Arquivo principal restaurado a partir do backup oculto.")
    elif os.path.exists(caminho_main) and not os.path.exists(caminho_oculto):
        shutil.copy2(caminho_main, caminho_oculto)
        print("🟢 Backup oculto restaurado a partir do arquivo principal.")
    elif not os.path.exists(caminho_main) and not os.path.exists(caminho_oculto):
        print("⚠️ ERRO CRÍTICO: Nenhum dos bancos de dados foi encontrado. Restauração impossível!")

# 🔍 Verifica se já existe um backup do mês passado
def verificar_backup_mes_passado():
    try:
        conn_str = f"DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={caminho_log_backup}"
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Obtém o mês e ano passado
        hoje = datetime.now()
        if hoje.month == 1:
            mes_passado = 12
            ano_passado = hoje.year - 1
        else:
            mes_passado = hoje.month - 1
            ano_passado = hoje.year

        nome_backup = f"Arquivos_{mes_passado:02d}_{ano_passado}.accdb"

        # Consulta se o backup do mês passado já existe no log
        cursor.execute("SELECT COUNT(*) FROM Controle_Backup WHERE Nome_Arquivo = ?", (nome_backup,))
        resultado = cursor.fetchone()[0]
        conn.close()

        if resultado > 0:
            print(f"[OK] Backup do mês passado ({nome_backup}) já existe no log.")
            return True
        else:
            print(f"[ALERTA] Backup do mês passado ({nome_backup}) NÃO encontrado. Criando agora...")
            return False

    except Exception as e:
        print(f"⚠️ Erro ao verificar backup do mês passado: {e}")
        return False

# 📦 Backup Mensal
def fazer_backup_mensal(mes=None, ano=None):
    agora = datetime.now()
    ano = ano if ano else agora.strftime("%Y")
    mes = mes if mes else agora.strftime("%m")
    
    pasta_ano = os.path.join(pasta_backups, str(ano))
    pasta_mes = os.path.join(pasta_ano, str(mes))

    os.makedirs(pasta_ano, exist_ok=True)
    os.makedirs(pasta_mes, exist_ok=True)

    nome_backup = f"Arquivos_{mes}_{ano}.accdb"
    caminho_backup_mes = os.path.join(pasta_mes, nome_backup)

    try:
        shutil.copy2(caminho_main, caminho_backup_mes)
        print(f"[OK] Backup criado: {caminho_backup_mes}")
        registrar_backup_no_bd(nome_backup)
    except Exception as e:
        print(f"[ERRO] Erro ao fazer backup: {e}")

# 📦 Backup Trimestral
def fazer_backup_trimestral():
    agora = datetime.now()
    ano = agora.strftime("%Y")
    trimestre = (agora.month - 1) // 3 + 1

    pasta_trimestre = os.path.join(pasta_backups, ano, f"Trimestre_{trimestre}")

    os.makedirs(pasta_trimestre, exist_ok=True)

    nome_backup = f"Backup_Trimestral_{trimestre}_{ano}.accdb"
    caminho_backup_trimestre = os.path.join(pasta_trimestre, nome_backup)

    try:
        shutil.copy2(caminho_main, caminho_backup_trimestre)
        print(f"📦 Backup TRIMESTRAL criado: {caminho_backup_trimestre}")
        registrar_backup_no_bd(nome_backup)
    except Exception as e:
        print(f"⚠️ Erro ao fazer backup trimestral: {e}")

# 📝 Registrar Backup no Banco de Logs
def registrar_backup_no_bd(nome_arquivo):
    try:
        conn_str = f"DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={caminho_log_backup}"
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        data_modificacao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute(
            "INSERT INTO Controle_Backup (Data_Modificacao, Nome_Arquivo) VALUES (?, ?)",
            (data_modificacao, nome_arquivo)
        )
        conn.commit()
        conn.close()
        print(f"📋 Registro de backup salvo: {nome_arquivo} ({data_modificacao})")
    except Exception as e:
        print(f"⚠️ Erro ao registrar backup no banco de logs: {e}")

# 📅 Verifica se deve fazer backup mensal ou trimestral
def verificar_data_e_fazer_backup():
    hoje = datetime.now()

    # Se hoje é dia 1, faz o backup normalmente
    if hoje.day == 1:
        fazer_backup_mensal()

    # Se estamos no começo de um trimestre, faz o backup trimestral
    if hoje.month in [1, 4, 7, 10] and hoje.day == 1:
        fazer_backup_trimestral()

    # Se não encontrou o backup do mês passado, cria um agora
    if not verificar_backup_mes_passado():
        fazer_backup_mensal(mes=f"{hoje.month - 1:02d}", ano=f"{hoje.year}")
