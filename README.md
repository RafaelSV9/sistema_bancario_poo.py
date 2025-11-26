# Sistema Bancário em Python com POO (DIO)

Projeto desenvolvido como desafio da Digital Innovation One (DIO) para refatorar o sistema bancário, armazenando os dados de clientes e contas bancárias em **objetos** ao invés de dicionários, seguindo um modelo de classes **UML**.

O foco deste desafio é aplicar **orientação a objetos** em Python, utilizando classes, herança, classes abstratas e polimorfismo.

---

## 🎯 Objetivo

- Modelar o sistema bancário utilizando POO.
- Substituir dicionários por **classes e objetos**.
- Implementar classes para:
  - Cliente (e Pessoa Física)
  - Conta (Conta Corrente)
  - Histórico de transações
  - Transações (Depósito e Saque)

---

## 🧩 Modelagem (UML resumido)

O código segue o modelo apresentado na aula/desafio:

- **Transacao (interface/ABC)**
  - `valor: float`
  - `registrar(conta: Conta)` (método abstrato)

- **Deposito (Transacao)**
- **Saque (Transacao)**

- **Historico**
  - `transacoes: list`
  - `adicionar_transacao(transacao: Transacao)`

- **Conta**
  - `saldo: float`
  - `numero: int`
  - `agencia: str`
  - `cliente: Cliente`
  - `historico: Historico`
  - `nova_conta(cliente, numero) -> Conta`
  - `sacar(valor) -> bool`
  - `depositar(valor) -> bool`

- **ContaCorrente (Conta)**
  - `limite: float`
  - `limite_saques: int`
  - sobrescreve `sacar`

- **Cliente**
  - `endereco: str`
  - `contas: list`
  - `realizar_transacao(conta, transacao)`
  - `adicionar_conta(conta)`

- **PessoaFisica (Cliente)**
  - `cpf: str`
  - `nome: str`
  - `data_nascimento: date`

---

## 🏗 Estrutura do projeto

```text
.
├── sistema_bancario_poo.py   # Código principal do sistema
└── README.md                 # Documentação do projeto
