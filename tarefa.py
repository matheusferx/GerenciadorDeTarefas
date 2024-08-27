import json as js
from datetime import datetime

class Tarefa:
    def __init__(self, titulo, descricao, data_criacao, data_vencimento, status='Pendente'):
        self.titulo = titulo
        self.descricao = descricao
        self.data_criacao = data_criacao
        self.data_vencimento = data_vencimento
        self.status = status

    def mudar_status(self):
        self.status = 'Completa'

    def exibir_tarefa(self):
        return (f"Título: {self.titulo}\n"
                f"Descrição: {self.descricao}\n"
                f"Data de criação: {self.data_criacao}\n"
                f"Data de vencimento: {self.data_vencimento}\n"
                f"Status: {self.status}\n")

    def dicionario(self):
        return {
            'titulo': self.titulo,
            'descricao': self.descricao,
            'data_criacao': self.data_criacao,
            'data_vencimento': self.data_vencimento,
            'status': self.status
        }

    @classmethod
    def de_dicionario(cls, data):
        return cls(
            titulo=data['titulo'],
            descricao=data['descricao'],
            data_criacao=data['data_criacao'],
            data_vencimento=data['data_vencimento'],
            status=data.get('status', 'Pendente')
        )

class JsonUtils:
    @staticmethod
    def validar_data(data_str):
        try:
            datetime.strptime(data_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False
        
    @staticmethod
    def validar_data_vencimento(data_criacao_str, data_vencimento_str):
        try:
            data_criacao = datetime.strptime(data_criacao_str, "%Y-%m-%d")
            data_vencimento = datetime.strptime(data_vencimento_str, "%Y-%m-%d")
            return data_vencimento >= data_criacao
        except ValueError:
            return False
    
    @staticmethod
    def salvar_tarefas(tarefas, nome_arquivo='tarefas.json'):
        try:
            with open(nome_arquivo, 'w') as file:
                js.dump([tarefa.dicionario() for tarefa in tarefas], file, indent=4)
            print(f"Tarefas salvas em {nome_arquivo}")
        except IOError as e:
            print(f"Erro ao salvar o arquivo: {e}")
    
    @staticmethod
    def carregar_tarefas(nome_arquivo='tarefas.json'):
        try:
            with open(nome_arquivo, 'r') as file:
                tarefas_data = js.load(file)
                return [Tarefa.de_dicionario(tarefa) for tarefa in tarefas_data]
        except FileNotFoundError:
            return []
        except IOError as e:
            print(f"Erro ao carregar o arquivo: {e}")
            return []

class GerenciadorDeTarefas:
    def __init__(self):
        self.tarefas = JsonUtils.carregar_tarefas()

    def adicionar_tarefa(self):
        titulo = input("Título: ")
        descricao = input("Descrição: ")
        data_criacao = input("Data de criação (YYYY-MM-DD): ")
        data_vencimento = input("Data de vencimento (YYYY-MM-DD): ")
         
        if not JsonUtils.validar_data(data_criacao) or not JsonUtils.validar_data(data_vencimento):
            print("Data inválida. Certifique-se de que está no formato YYYY-MM-DD.")
            return
        
        if not JsonUtils.validar_data_vencimento(data_criacao, data_vencimento):
            print("Data de vencimento não pode ser anterior à data de criação.")
            return
        
        tarefa = Tarefa(titulo, descricao, data_criacao, data_vencimento)
        self.tarefas.append(tarefa)
        print("Tarefa adicionada com sucesso!\n")
        self.salvar_tarefas_em_json()

    def listar_tarefas(self):
        if not self.tarefas:
            print("Nenhuma tarefa encontrada!")
            return

        for tarefa in self.tarefas:
            print(tarefa.exibir_tarefa())

    def remover_tarefa(self):
        titulo = input("Título da tarefa a ser removida: ")
        tarefa_para_remover = next((tarefa for tarefa in self.tarefas if tarefa.titulo == titulo), None)
        
        if tarefa_para_remover:
            self.tarefas.remove(tarefa_para_remover)
            self.salvar_tarefas_em_json()
            print(f"Tarefa '{titulo}' removida com sucesso!\n")
        else:
            print("Tarefa não encontrada.")

    def mudar_status_tarefa(self):
        titulo = input("Título da tarefa para mudar o status: ")
        tarefa_encontrada = next((tarefa for tarefa in self.tarefas if tarefa.titulo == titulo), None)
        
        if tarefa_encontrada:
            tarefa_encontrada.mudar_status()
            self.salvar_tarefas_em_json()
            print(f"Status da tarefa '{titulo}' alterado para 'Completa'.\n")
        else:
            print("Tarefa não encontrada.")

    def salvar_tarefas_em_json(self):
        JsonUtils.salvar_tarefas(self.tarefas)
    
# Exemplo de uso
def menu():
    gerenciador = GerenciadorDeTarefas()

    while True:
        acao = input("Deseja adicionar uma tarefa? (sim/não): ").strip().lower()
        if acao == 'sim':
            gerenciador.adicionar_tarefa()
        elif acao == 'não':
            break
        else:
            print("Opção inválida. Digite 'sim' ou 'não'.")

    while True:
        acao = input("Deseja alterar o status de uma tarefa (1) ou remover uma tarefa (2)? (Digite 'sair' para encerrar): ").strip().lower()
        if acao == '1':
            gerenciador.mudar_status_tarefa()
        elif acao == '2':
            gerenciador.remover_tarefa()
        elif acao == 'sair':
            break
        else:
            print("Opção inválida. Tente novamente.")

    print("Listagem final das tarefas:\n")
    gerenciador.listar_tarefas()

if __name__ == "__main__":
    menu()

