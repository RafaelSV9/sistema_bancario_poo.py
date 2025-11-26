
---

## 3️⃣ Arquivo Python (`sistema_bancario_poo.py`)

Cria um arquivo com esse nome e cola o código abaixo:

```python
from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime, date
from typing import List, Optional


# =========================
#   MODELO DE TRANSACÕES
# =========================

class Transacao(ABC):
    """Interface para operações de conta (Depósito / Saque)."""

    @property
    @abstractmethod
    def valor(self) -> float:
        ...

    @abstractmethod
    def registrar(self, conta: "Conta") -> None:
        ...


class Deposito(Transacao):
    def __init__(self, valor: float) -> None:
        self._valor = valor

    @property
    def valor(self) -> float:
        return self._valor

    def registrar(self, conta: "Conta") -> None:
        sucesso = conta.depositar(self.valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)


class Saque(Transacao):
    def __init__(self, valor: float) -> None:
        self._valor = valor

    @property
    def valor(self) -> float:
        return self._valor

    def registrar(self, conta: "Conta") -> None:
        sucesso = conta.sacar(self.valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)


# =========================
#        HISTÓRICO
# =========================

class Historico:
    def __init__(self) -> None:
        self._transacoes: List[dict] = []

    @property
    def transacoes(self) -> List[dict]:
        return self._transacoes

    def adicionar_transacao(self, transacao: Transacao) -> None:
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            }
        )


# =========================
#          CONTAS
# =========================

class Conta:
    def __init__(self, numero: int, cliente: "Cliente") -> None:
        self._saldo: float = 0.0
        self._numero: int = numero
        self._agencia: str = "0001"
        self._cliente: Cliente = cliente
        self._historico: Historico = Historico()

    @classmethod
    def nova_conta(cls, cliente: "Cliente", numero: int) -> "Conta":
        return cls(numero, cliente)

    @property
    def saldo(self) -> float:
        return self._saldo

    @property
    def numero(self) -> int:
        return self._numero

    @property
    def agencia(self) -> str:
        return self._agencia

    @property
    def cliente(self) -> "Cliente":
        return self._cliente

    @property
    def historico(self) -> Historico:
        return self._historico

    def sacar(self, valor: float) -> bool:
        if valor <= 0:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False

        if valor > self.saldo:
            print("\n@@@ Operação falhou! Saldo insuficiente. @@@")
            return False

        self._saldo -= valor
        print("\n=== Saque realizado com sucesso! ===")
        return True

    def depositar(self, valor: float) -> bool:
        if valor <= 0:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False

        self._saldo += valor
        print("\n=== Depósito realizado com sucesso! ===")
        return True


class ContaCorrente(Conta):
    def __init__(
        self,
        numero: int,
        cliente: "Cliente",
        limite: float = 500.0,
        limite_saques: int = 3,
    ) -> None:
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor: float) -> bool:
        numero_saques = len(
            [
                t
                for t in self.historico.transacoes
                if t["tipo"] == "Saque"
            ]
        )

        excedeu_saques = numero_saques >= self._limite_saques
        excedeu_limite = valor > self._limite

        if excedeu_saques:
            print("\n@@@ Operação falhou! Limite de saques excedido. @@@")
            return False

        if excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
            return False

        return super().sacar(valor)

    def __str__(self) -> str:
        return f"Agência: {self.agencia} | Número: {self.numero} | Titular: {self.cliente.nome}"


# =========================
#         CLIENTES
# =========================

class Cliente:
    def __init__(self, endereco: str) -> None:
        self.endereco = endereco
        self.contas: List[Conta] = []

    def realizar_transacao(self, conta: Conta, transacao: Transacao) -> None:
        transacao.registrar(conta)

    def adicionar_conta(self, conta: Conta) -> None:
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(
        self,
        nome: str,
        cpf: str,
        data_nascimento: date,
        endereco: str,
    ) -> None:
        super().__init__(endereco)
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento


# =========================
#      FUNÇÕES DE MENU
# =========================

clientes: List[PessoaFisica] = []
contas: List[Conta] = []


def menu() -> str:
    print("""
=========== MENU ===========
[1] Cadastrar cliente
[2] Criar conta corrente
[3] Listar contas
[4] Depositar
[5] Sacar
[6] Extrato
[0] Sair
============================
""")
    return input("Escolha uma opção: ").strip()


def filtrar_cliente(cpf: str) -> Optional[PessoaFisica]:
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def recuperar_conta_cliente(cliente: PessoaFisica) -> Optional[Conta]:
    if not cliente.contas:
        print("\n@@@ Cliente não possui conta cadastrada. @@@")
        return None

    # Para simplificar, sempre usamos a primeira conta
    return cliente.contas[0]


def cadastrar_cliente() -> None:
    cpf = input("Informe o CPF (somente números): ").strip()
    cliente = filtrar_cliente(cpf)

    if cliente:
        print("\n@@@ Já existe cliente com esse CPF. @@@")
        return

    nome = input("Informe o nome completo: ").strip()
    data_str = input("Informe a data de nascimento (dd/mm/aaaa): ").strip()
    endereco = input("Informe o endereço (logradouro, nº - bairro - cidade/UF): ").strip()

    try:
        data_nascimento = datetime.strptime(data_str, "%d/%m/%Y").date()
    except ValueError:
        print("\n@@@ Data de nascimento inválida. @@@")
        return

    novo_cliente = PessoaFisica(
        nome=nome,
        cpf=cpf,
        data_nascimento=data_nascimento,
        endereco=endereco,
    )
    clientes.append(novo_cliente)
    print("\n=== Cliente cadastrado com sucesso! ===")


def criar_conta() -> None:
    cpf = input("Informe o CPF do cliente: ").strip()
    cliente = filtrar_cliente(cpf)

    if not cliente:
        print("\n@@@ Cliente não encontrado. Cadastre o cliente primeiro. @@@")
        return

    numero_conta = len(contas) + 1
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.adicionar_conta(conta)
    print("\n=== Conta criada com sucesso! ===")
    print(conta)


def listar_contas() -> None:
    if not contas:
        print("\n@@@ Não há contas cadastradas. @@@")
        return

    print("\n======= CONTAS CADASTRADAS =======")
    for conta in contas:
        print(conta)
    print("==================================")


def depositar() -> None:
    cpf = input("Informe o CPF do cliente: ").strip()
    cliente = filtrar_cliente(cpf)

    if not cliente:
        print("\n@@@ Cliente não encontrado. @@@")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    try:
        valor = float(input("Informe o valor do depósito: ").replace(",", "."))
    except ValueError:
        print("\n@@@ Valor inválido. @@@")
        return

    transacao = Deposito(valor)
    cliente.realizar_transacao(conta, transacao)


def sacar() -> None:
    cpf = input("Informe o CPF do cliente: ").strip()
    cliente = filtrar_cliente(cpf)

    if not cliente:
        print("\n@@@ Cliente não encontrado. @@@")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    try:
        valor = float(input("Informe o valor do saque: ").replace(",", "."))
    except ValueError:
        print("\n@@@ Valor inválido. @@@")
        return

    transacao = Saque(valor)
    cliente.realizar_transacao(conta, transacao)


def exibir_extrato() -> None:
    cpf = input("Informe o CPF do cliente: ").strip()
    cliente = filtrar_cliente(cpf)

    if not cliente:
        print("\n@@@ Cliente não encontrado. @@@")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n=========== EXTRATO ===========")
    if not conta.historico.transacoes:
        print("Não foram realizadas movimentações.")
    else:
        for transacao in conta.historico.transacoes:
            print(
                f"{transacao['data']} - {transacao['tipo']}: R$ {transacao['valor']:.2f}"
            )

    print(f"\nSaldo atual: R$ {conta.saldo:.2f}")
    print("================================")


# =========================
#      PROGRAMA PRINCIPAL
# =========================

def main() -> None:
    while True:
        opcao = menu()

        if opcao == "1":
            cadastrar_cliente()
        elif opcao == "2":
            criar_conta()
        elif opcao == "3":
            listar_contas()
        elif opcao == "4":
            depositar()
        elif opcao == "5":
            sacar()
        elif opcao == "6":
            exibir_extrato()
        elif opcao == "0":
            print("\nAté mais! 👋")
            break
        else:
            print("\n@@@ Opção inválida, tente novamente. @@@")

if __name__ == "__main__":
    main()
